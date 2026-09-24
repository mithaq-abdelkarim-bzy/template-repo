import hx
import pandas as pd
import numpy as np
import math as math

def rate_pricing_runoff(hxd):
    if hxd.cds.is_runoff:
        layers = hxd.cds.layers
        for idx, layer in enumerate(layers):
            if hxd.cds.is_abc:
                quoted_premium = layer.coverages.abc.premium
            elif hxd.cds.is_side_a:
                quoted_premium = layer.coverages.side_a.premium

        if quoted_premium and layer.runoff_adjustment and abs(quoted_premium - (layer.runoff_adjustment or 0) * (layer.runoff_original_premium or 0)) > 1:
            hx.errors.validation(f"With Original Runoff premium of {layer.runoff_original_premium} "
                                f"and a Runoff factor of {layer.runoff_adjustment}, "
                                f"the Final Premium must equal {(layer.runoff_original_premium or 0) * (layer.runoff_adjustment or 0)}")
            # layer.runoff_original_premium = 0 if layer.runoff_adjustment == 0 else (quoted_premium or 0) / layer.runoff_adjustment