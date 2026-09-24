
# function to update rate change values
def task_map_expiring_rate_change(hxd):
    src_path = hxd.cds.expiring.rate_change
    dst_path = hxd.cds.rate_change
    dst_lobs = [row.selected_lob for row in dst_path]

    for src_row in src_path:
        src_lob = src_row.selected_lob
        if src_lob is None:
            continue
        if src_lob in dst_lobs:
            pos = dst_lobs.index(src_lob)
            for i in range(15):                             # year_0 -> year_1 ... year_14 -> year_15
                src = getattr(src_row,      f'year_{i}'  )
                dst = getattr(dst_path[pos],f'year_{i+1}')
                dst.facility = src.facility
    return