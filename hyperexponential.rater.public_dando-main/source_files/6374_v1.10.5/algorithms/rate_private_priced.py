import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_constants as const
from algorithms import rate_constants as const

def private_priced(hxd):
    stn = hxd.cds.standard_fields


    methodology = hxd.cds.rating_methodology
 
    methodology_map = {
        "Public D&O": (True, False),
        "Private D&O": (False, True),
    }
 
    rp, pp = methodology_map.get(methodology, (False, False))
    hxd.cds.review_type.rater_priced = rp
    hxd.cds.review_type.private_priced = pp
    hxd.cds.standard_fields.is_rater_priced = rp

    if methodology == "Public D&O":
        hxd.cds.standard_fields.rating_methodology = "Rater"
    else:
        hxd.cds.standard_fields.rating_methodology = "Private D&O"
                
    
    
    # ######## Rate Change components ################
    
    for layer in hxd.cds.layers:
        rc = layer.rate_change

        if hxd.cds.coverage == "Side A":
            active_cov = layer.coverages.side_a
            layer.coverages.side_a.total_excess = ((layer.coverages.side_a.excess or 0) + (layer.coverages.side_a.tower or 0))
        
        else:
            active_cov = layer.coverages.abc

        # set prem 
        layer.quoted_premium = active_cov.premium
        
        layer.written_line = active_cov.written_line


        layer.benchmark_premium = active_cov.private_priced.benchmark_premium
        layer.technical_premium = active_cov.private_priced.technical_premium

        active_cov.private_priced.bpi = (active_cov.premium/layer.benchmark_premium) if (layer.benchmark_premium not in (None, 0) and active_cov.premium is not None) else None
        active_cov.private_priced.tpi = (active_cov.premium/layer.technical_premium) if (layer.technical_premium not in (None, 0) and active_cov.premium is not None) else None
        
        layer.bpi = active_cov.private_priced.bpi
        layer.tpi = active_cov.private_priced.tpi 

        active_cov.quoted_market_share = (active_cov.written_line *  active_cov.premium) if (active_cov.written_line is not None and  active_cov.premium is not None) else None

        layer.limit = active_cov.limit
        layer.excess = active_cov.excess
        layer.deductible = active_cov.deductible
        layer.brokerage = active_cov.brokerage

        rc.premium_annualized_100pct.renewal = active_cov.premium
        rc.limit.renewal = layer.limit
        rc.deductible.renewal = layer.deductible
        rc.excess.renewal = layer.excess
        rc.side_a_excess.renewal = layer.coverages.side_a.excess
        rc.abc_tower.renewal = layer.coverages.side_a.tower
        rc.total_excess.renewal = (layer.excess or 0) + (layer.coverages.side_a.tower or 0)
        rc.asset_size.renewal = hxd.cds.exposure.aggregate.total_assets
        rc.brokerage.renewal = layer.brokerage
        

        

    # Reset the floating technical-premium tiles
    for slot in range(const.max_layers):
        setattr(hxd.cds, f"technical_premium_{slot + 1}", None)
        setattr(hxd.cds, f"show_tech_prem_{slot + 1}", False)

    # Populate tiles with the current option technical premiums
    for idx, layer in enumerate(hxd.cds.layers):
        if idx < const.max_layers:
            setattr(hxd.cds, f"technical_premium_{idx + 1}", layer.technical_premium)
            setattr(hxd.cds, f"show_tech_prem_{idx + 1}", layer.technical_premium is not None)
