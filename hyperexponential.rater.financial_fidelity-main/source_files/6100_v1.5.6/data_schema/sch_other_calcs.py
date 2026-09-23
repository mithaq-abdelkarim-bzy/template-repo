import hx_data_schema as hx
import libraries.common_data_schema.data_schema.utilities as utils
import algorithms.utils_global_lists as lst
from libraries.common_data_schema.data_schema.utilities import thousands_format

def sch_other_calcs(cds):
    cds.extend_node_rater_defined("cds/layers", {

        # Expsoure table sub totals
        **{
            loop_subtotal : hx.Structure(view={'label': 'Subtotal'}, children={
                "coverage_premium": hx.Float(mode="output", view={"label": "Unity Premium", "format":utils.thousands_format(0)}),
                "coverage_premium_post_schedule": hx.Float(mode="output", view={"label": "Premium Post Schedule Rating", "format":utils.thousands_format(0)}),
                "coverage_premium_post_a_rating": hx.Float(mode="output", view={"label": "Final Premium", "format":utils.thousands_format(0)}),
                "coverage_premium_post_a_rating_annual": hx.Float(mode="output", view={"label": "Annualized Premium", "format":utils.thousands_format(0)}),
            })
            for loop_subtotal in ['subtotal_forms','subtotal_safe_deposit_policy', 'subtotal_computer_crime_policy']
        },
        

        # Other
        "priced_to_lr": hx.Float(mode="output"),
        "benchmark_lr": hx.Float(mode="output"),
        "technical_lr": hx.Float(mode="output"),
        "assumed_brokerage": hx.Float(mode="output"),
        "min_deductible": hx.Float(mode="output"),
        "basic_unit_upper_limit": hx.Float(mode="output"),
        "term_adjustment": hx.Float(mode="output", view={"label": "Term Adjustment Factor"}),
        "insured_state_loss_cost_multiplier": hx.Float(mode="output"),
        "loss_cost_e_num": hx.Float(mode="output"),
             
        
        # Optional premium bearing endorsements (annual charge)
        "premium_bearing_endorsements": hx.List(mode="input", children={
                "endorsement": hx.Str(mode="input", default="", view={"label": "Endorsement"}),
                "coverage": hx.Float(mode="input", default=0, view={"label": "Coverage", "format": thousands_format(0)}),
                "deductible": hx.Float(mode="input", default=0, view={"label": "Deductible", "format": thousands_format(0)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format(0)}),
                "premium_annual": hx.Float(mode="input", default=0, view={"label": "Annualized Premium", "format": thousands_format(0)}),
                "is_impersonation_fraud": hx.Bool(mode="input", default=False, view={"label": "Is impersonation fraud?"}),
            }),

        "premium_bearing_endorsements_total": hx.Structure(view={"label": "Subtotal"}, children={
            "premium": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "premium_annual": hx.Float(mode="output", view={"label": "Annualized Premium", "format": thousands_format(0)}),
            "benchmark_premium": hx.Float(mode="output", view={"format": thousands_format(0)}),
        }),

        "has_endorsements":hx.Bool(mode="output"), 
    })

def sch_other_calcs_non_cds():
    return {
        "cols_flag": hx.Bool(mode="input", default=False, view={"label": "Show minimum and maximum coverage"}),
        
        "show_safe_deposit_policy_table": hx.Bool(mode="output"),
        "show_computer_crime_policy_table": hx.Bool(mode="output"),

        "pricing_info": hx.Str(mode="output"),

        # Debugging
        "debug_num": hx.Float(mode="output", view={"label":"Debug 1", "format": utils.integer_format(3)}),
        "debug_num2": hx.Float(mode="output", view={"label":"Debug 2","format": utils.integer_format(3)}),
        "debug_num3": hx.Float(mode="output", view={"label":"Debug 3","format": utils.integer_format(3)}),
        "debug_str": hx.Str(mode="output", view={"label":"Str"}),
    }

