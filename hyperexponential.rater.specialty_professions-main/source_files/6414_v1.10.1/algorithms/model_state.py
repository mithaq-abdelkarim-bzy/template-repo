
import hx
from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict , max_coverages


def model_state(hxd):

    ms = hxd.model_state

    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 109687 # For debugging in dev mode
    # save the record global variable in the snapshot for governance
    ms.coverage_use = RARC_COVERAGE_USE
    ms.insured_asset_use = RARC_INSURED_ASSET_USE
    # Controls which page to show and hide when the start renewal button is pressed
    # Only displays the landing page for policies which are a renewal
    if (expiring_policy_option_id is None) or (ms.pressed_start_renewal_task) or (ms.expiring_policy_option_id == expiring_policy_option_id):
        ms.show_landing_page = False
        ms.show_after_landing_page = True

        ms.show_rate_change_layer_no_ia_use = hxd.cds.standard_fields.is_renewal and not RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE

    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False

        ms.show_rate_change = False
        
        ms.show_rate_change_layer_no_ia_use = False


    # For layers not used in the pricing summary, the rate change and KPI Summary is hidden
    layers = hxd.cds.layers
    num_layers = len(layers)
    for layer_index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{layer_index}", True) if layer_index <= num_layers else False
    
    if RARC_COVERAGE_USE: # EDIT v0.3.0
        num_coverages = len(coverages_dict)
        for cvg_index in range(1,max_coverages):
            setattr(hxd.cds.rate_change, f"show_coverage_{cvg_index}", True) if cvg_index <= num_coverages else False

    
    # set the shown_by value # Edit # v0.5.0
    ms.layer_no_ia_use = (RARC_COVERAGE_USE==False and RARC_INSURED_ASSET_USE == False)
