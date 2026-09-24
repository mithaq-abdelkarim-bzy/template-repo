import hx, datetime, numpy as np, pandas as pd
import algorithms.rate_constants as const
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, remove_before_separator
from algorithms.model_profiler.profiling_hxd_functions import time_me

from scipy.interpolate import interp1d, PchipInterpolator

def steer_populate_bc_patterns(hxd, progress):
    """
    Assign experience_selected_set_in_task incremental_dev_factor and tail from experience_default and experience_override.
    Remove this task when Transient will be upgraded to address triangle nodes
    """

    def _select_value(node):
        """Return override if >0, else default, else 1 (preserve original logic)."""
        if node.experience_override is not None and node.experience_override > 0:
            return node.experience_override
        return node.experience_default or 1

    # Build layer list (fgu + dynamic layers)
    layer_list = ["fgu"] + [
        f"layer_{i+1:02d}" for i in range(len(hxd.cds.layers))
    ]

    for layer_name in layer_list:
        layer = getattr(hxd.cds.steer.experience_rating.layers, layer_name)

        tri = layer.triangle_projection
        cc = layer.claim_count

        # Incremental dev factors
        for i in range(len(tri.incremental_dev_factor)):
            tri.incremental_dev_factor[i].experience_selected_set_in_task = _select_value(
                tri.incremental_dev_factor[i]
            )
            cc.incremental_dev_factor[i].experience_selected_set_in_task = _select_value(
                cc.incremental_dev_factor[i]
            )

        # Tail factors
        tri.tail_factor.experience_selected_set_in_task = _select_value(tri.tail_factor)
        cc.tail_factor.experience_selected_set_in_task = _select_value(cc.tail_factor)

