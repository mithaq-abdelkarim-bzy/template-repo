import numpy as np


def allocate_to_regions(lons, lats, geojson, region_property="name", process=None):
    """
    Assign each coordinate to a GeoJSON region using vectorized point-in-polygon.

    Args:
        lons:             Array-like of longitudes, length N.
        lats:             Array-like of latitudes, length N.
        geojson:          Pre-parsed GeoJSON dict (FeatureCollection, Feature, or geometry).
        region_property:  Feature property to use as the region label.
        process:          Optional boolean array of length N. True = allocate this point,
                          False = skip (result will be None). Defaults to processing all points.

    Returns:
        List of length N — the region label for each coordinate, or None if it
        falls outside every region or was skipped.
    """
    all_coords = np.column_stack([
        np.asarray(lons, dtype=np.float64),
        np.asarray(lats, dtype=np.float64),
    ])
    active = np.asarray(process, dtype=bool) if process is not None else np.ones(len(all_coords), dtype=bool)
    coords = all_coords[active]

    features = _extract_features(geojson)
    regions = _parse_regions(features, region_property)

    results = np.full(len(coords), None, dtype=object)
    unassigned = np.ones(len(coords), dtype=bool)

    for label, polygons in regions:
        if not unassigned.any():
            break

        pts = coords[unassigned]
        inside = np.zeros(len(pts), dtype=bool)

        for exterior, holes in polygons:
            mask = _bbox_filter(pts, exterior)
            if not mask.any():
                continue

            in_poly = _points_in_polygon(pts[mask], exterior)

            for hole in holes:
                in_poly_idx = np.where(in_poly)[0]
                in_hole = _points_in_polygon(pts[mask][in_poly], hole)
                in_poly[in_poly_idx[in_hole]] = False

            local = np.where(mask)[0]
            inside[local[in_poly]] = True

        results[np.where(unassigned)[0][inside]] = label
        unassigned[np.where(unassigned)[0][inside]] = False

    full_results = np.full(len(all_coords), None, dtype=object)
    full_results[active] = results
    
    return full_results.tolist()


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------

def _extract_features(geojson):
    t = geojson.get("type", "")
    if t == "FeatureCollection":
        return geojson["features"]
    if t == "Feature":
        return [geojson]
    return [{"type": "Feature", "geometry": geojson, "properties": {}}]


def _parse_regions(features, region_property):
    """Yield (label, [(exterior_arr, [hole_arr, ...]), ...]) per feature."""
    regions = []
    for i, feat in enumerate(features):
        props = feat.get("properties") or {}
        label = props.get(region_property) or props.get("id") or feat.get("id") or i
        geom = feat.get("geometry") or feat
        gtype = geom["type"]

        if gtype == "Polygon":
            raw = [geom["coordinates"]]
        elif gtype == "MultiPolygon":
            raw = geom["coordinates"]
        else:
            continue

        polygons = []
        for ring_group in raw:
            exterior = np.asarray(ring_group[0], dtype=np.float64)
            holes = [np.asarray(h, dtype=np.float64) for h in ring_group[1:]]
            polygons.append((exterior, holes))

        regions.append((label, polygons))
    return regions


def _bbox_filter(points, polygon):
    """Boolean mask: points whose (x, y) falls within the polygon bounding box."""
    min_x, min_y = polygon[:, 0].min(), polygon[:, 1].min()
    max_x, max_y = polygon[:, 0].max(), polygon[:, 1].max()
    return (
        (points[:, 0] >= min_x) & (points[:, 0] <= max_x) &
        (points[:, 1] >= min_y) & (points[:, 1] <= max_y)
    )


def _points_in_polygon(points, polygon):
    """
    Vectorized ray-casting: returns bool array of shape (N,).

    Broadcasts N points against all K edges simultaneously so there are no
    Python-level loops over either points or edges.
    """
    if len(points) == 0:
        return np.array([], dtype=bool)

    # Ensure ring is closed
    if not np.array_equal(polygon[0], polygon[-1]):
        polygon = np.vstack([polygon, polygon[0]])

    px = points[:, 0, np.newaxis]   # (N, 1)
    py = points[:, 1, np.newaxis]   # (N, 1)

    x1, y1 = polygon[:-1, 0], polygon[:-1, 1]  # (K,)
    x2, y2 = polygon[1:,  0], polygon[1:,  1]  # (K,)

    # Edge straddles the horizontal ray from each point
    crossed = ((y1 < py) & (y2 >= py)) | ((y2 < py) & (y1 >= py))

    # x-coordinate where the edge crosses py (safe divide)
    dy = np.where(y2 != y1, y2 - y1, 1.0)
    x_cross = x1 + (py - y1) / dy * (x2 - x1)

    # Ray goes rightward; count crossings to the right of each point
    hits = (crossed & (x_cross > px)).sum(axis=1)
    return hits % 2 == 1
