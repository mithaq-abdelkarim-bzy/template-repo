### to activate timer find and replace " timer" with " timer" and then fix line 21

### From Skeleton Model
import hx
import algorithms.rate_utilities as utils
import datetime
from algorithms.rate_risk_information           import rate_risk_information
from algorithms.rate_rms                        import rate_rms
from algorithms.rate_triangle_projection        import rate_triangle_projection
from algorithms.rate_rating_summary             import rate_rating_summary
from algorithms.rate_claim_summary              import rate_claim_summary
from algorithms.rate_profit_commission          import rate_profit_commission
from algorithms.rate_show_hide                  import rate_show_hide
from algorithms.rate_validation_criteria        import rate_validation_criteria
from algorithms.graph_string_creation           import adjust_graph_strings
from algorithms.rate_model_state                import rate_model_state
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs
# from algorithms.timer import timer




@hx.rating
def rating_algorithm(hxd):
    rate_risk_information(hxd)
    rate_rms(hxd)
    rate_triangle_projection(hxd)
    rate_rating_summary(hxd)
    rate_claim_summary(hxd)     #after rating summary - uses some of its values
    rate_profit_commission(hxd)     #after rating summary - uses some of its values

    hxd.cds.rationale.help_file = ( "User Guide, Quick Starts, Training Videos are stored [here](https://beazley.sharepoint.com/sites/ActuarialPricing)."
                                   +"\n\r" + "This includes the rules that support the algorithm.")

    rate_model_state(hxd)
    rate_show_hide(hxd)
    rate_validation_criteria(hxd)
    sync_hx_core(hxd)
    adjust_graph_strings(hxd)
    provision_bug_report_inputs_outputs(hxd)

    pass