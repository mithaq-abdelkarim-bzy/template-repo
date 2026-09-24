import algorithms.validations.risk_information_validations as validations
from algorithms.risk_information.risk_information_helpers import (
    set_broker_details,
    apply_validations_checks
)
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

@time_me
def rate_risk_information(hxd):
    # Get references to risk information paths in both CDS and non-CDS sections
    ri = hxd.cds.risk_information
    non_cds_ri = hxd.non_cds.risk_information

    # Extract key risk info flags
    is_follow_main_syn = ri.follow_main_syndicate
    is_cat_model = ri.cat_modelling_available
    is_large_model_mode = ri.is_large_model_mode 
    
    # Store whether we are *not* in large model mode for downstream usage   
    non_cds_ri.not_large_model_mode = not is_large_model_mode


    # If not following a main syndicate and catastrophe modelling is available,
    # mark both flags as True. Otherwise, reset them to False.   
    if not is_follow_main_syn and is_cat_model:
        non_cds_ri.cat_modelling_available = True
        non_cds_ri.not_follow_main_syndicate = True
    else:
        non_cds_ri.cat_modelling_available = False
        non_cds_ri.not_follow_main_syndicate = False

    # Store complementary flags in non-CDS risk info
    non_cds_ri.not_follow_main_syndicate = not is_follow_main_syn
    non_cds_ri.expiring_id_not_available = (
        ri.expiring_option_id is None 
    )

    # Capture who priced the risk and set flags accordingly
    non_cds_ri.is_actuarial = (ri.priced_by == "Actuarial")
    non_cds_ri.is_underwriter = (ri.priced_by == "Underwriting")

    # Populate broker details (name, email, location) from broker contact info
    set_broker_details(hxd)
    
    # Run validation checks on the input data
    apply_validations_checks(hxd)

    hxd.cds.standard_fields.facility_reference = hxd.cds.standard_fields.policy_reference