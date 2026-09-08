import hx_data_schema as hx
import data_schema.utilities as utils
import algorithms.utils_global_lists as lst
from algorithms.utils_functions import create_title

def sch_exposure_details(cds):
    cds.extend_node_rater_defined("cds", {
        # Exposure details (state, layer limits/premiums, % share)
        "is_follow": hx.Bool(mode="input", default=False, view={"label": "(For cosurety only) Is Beazley following\nthe lead insurer's premium?"}),
        "lead_premium": hx.Float(mode="output", view={"format": utils.thousands_format(0)}),
        "has_social_engineering": hx.Bool(mode="input", default=True, view={"label": "Include Social Engineering Tower"}),
        "has_other_coverages": hx.Bool(mode="input", default=False, view={"label": "Include Other Coverages Tower"}),  

         # Excess Factor
        "entity_type": hx.Str(mode="output", view={"label": "Entity Type Factor"}),
        "excess_factor": hx.Float(mode="output", view={"label": "Excess Factor"}),        

        # Layer info
        "beazley_layer": hx.Str(mode="input", optionality="optional", options_data="../excess_layers", options_field="layer_label", default=None, view={"label": "Beazley Layer"}),
        "beazley_share":hx.Float(mode="input", default=1, view={"label": "Beazley Share", "format": utils.percent_format(0)}),
        "beazley_pre_layer": hx.Str(mode="output", view={"label": "Preceding Layer"}),
        "underlying_brokerage":hx.Float(mode="override", view={"label": "Underlying Insurer Commission", "format": utils.percent_format(1)}),
        "underlying_layer_limit": hx.Int(mode="output", view={"label": "Underlying Layer Limit"}),
        "underlying_premium": hx.Int(mode="output", view={"label": "Underlying Premium"}),
        "underlying_rate_per_m": hx.Int(mode="output", view={"label": "Underlying Rate per Million"}),
        "total_layer_limit": hx.Int(mode="output", view={"label": "Total Layer Limit"}),
        "beazley_limit": hx.Int(mode="output", view={"label": "Beazley's Limit"}),
        "beazley_layer_index": hx.Int(mode="output", view={"label": "Beazley Layer"}),

        # Program schedule - separate retention, primary, and excess layers given differences in output fields
        "retention": hx.Structure(view={"label": "Retention"}, children={
            "limit": hx.Int(mode="input", default=0, view={"label": "Full Layer\nLimit", "format":utils.thousands_format(0)}), #TOREMOVE
            "limit_social_engineering": hx.Int(mode="input", default=0, view={"label": "Social Engineering\nLimit", "format":utils.thousands_format(0)}),
            "limit_other_cov": hx.Int(mode="input", default=0, view={"label": "Other Coverages\nLimit", "format":utils.thousands_format(0)}),
            }), 
        
        # List of excess layers for dropdown options
        "excess_layers": hx.List(view={"label": "Excess Layers"}, mode="output", children={
            "layer_label": hx.Str(mode="output", view={"label": "Layer Label"})
        }),

        # Term adjustment
        "underlying_inception_date": hx.Date(mode="override", view={"label": "Underlying Layer's Inception Date"}),
        "underlying_expiry_date": hx.Date(mode="override", view={"label": "Underlying Layer's Expiry Date"}),

        # Social Engineering details
        "social_engineering_sublimit": hx.Float(mode="input", default=0, view={"label": "SE Limit in Underlying Layer", "format":utils.thousands_format(0)}),
        "social_engineering_limit": hx.Float(mode="input", default=0, view={"label": "SE Limit in Beazley Layer", "format":utils.thousands_format(0)}),
        "social_engineering_allocation": hx.Float(mode="input", default=0, view={"label": "Allocation of SE in Underlying Premium", "format": utils.percent_format(0)}),

        # Rating factors
        "rating_factors": hx.Structure(children={
                "claim_basis": hx.Str(mode="input", optionality= "required", options_table="claim_basis", options_column="Claim Basis", default_index=1, view={"label": "Claim Basis"}),
                "endt_extensions": hx.Str(mode="input", optionality= "required", options_table="endt_extensions", options_column="Endorsements and Coverages Extensions", default_index=0, 
                                    view={"label": "Endorsements &\nCoverage Extensions"}),
                "sublimited_perils": hx.Str(mode="input", optionality= "required", options_table="sublimited_perils", options_column="Sublimited Perils", default="None",
                                    view={"label": "Sublimited Perils"}),
                "other_on_premises": hx.Str(mode="input", optionality= "required", options_table="other_perils", options_column="Other Perils", default="None",
                                    view={"label": "Other On-Premises Perils"}),
                "other_off_premises": hx.Str(mode="input", optionality= "required", options_table="other_perils", options_column="Other Perils", default="None",
                                    view={"label": "Other Off-Premises Perils"}),
            })
    })
            
    cds.extend_node_rater_defined("cds/layers", {
        "layer_label": hx.Str(mode="output", view={"label": "Layer Label"}),
        "limit_social_engineering": hx.Int(mode="input", default=0, view={"label": "Social Engineering\nLimit", "format":utils.thousands_format(0)}), 
        "limit_other_cov": hx.Int(mode="input", default=0, view={"label": "Other Coverages\nLimit", "format":utils.thousands_format(0)}), 
        "excess_social_engineering": hx.Int(mode="output", view={"label": "Attachment Point Social Engineering", "format":utils.thousands_format(0)}), 
        "excess_other_cov": hx.Int(mode="output", view={"label": "Attachment Point Other", "format":utils.thousands_format(0)}),
        # Beazley's brokerage sits in layers[0] so need to create a separate variable
        "layer_brokerage": hx.Float(mode="override", view={"label": "Commission", "format":utils.percent_format(1)}), #TODO: remove if not needed
        "layer_quality": hx.Bool(mode="input", default=False, view={"label": "Layer Premium\nIs Reliable"}),
        "lead_underwriter": hx.Str(mode="input", default="", view={"label": "Lead\nUnderwriter"}),
        "participating_cosurety": hx.Str(mode="input", default="", view={"label": "Participating\nCosurety"}),
        "lead_percentage": hx.Float(mode="input", default=1, view={"label": "Lead\nPercentage", "format":utils.percent_format(0)}),
        "rate_per_m": hx.Float(mode="output", view={"label": "Rate per \nMillion", "format":utils.thousands_format(0)}),
        "percent_underlying_rate": hx.Float(mode="output", view={"label": "Percent of\nUnderlying Rate", "format":utils.percent_format(0)}),
        "internal_weighted_premium": hx.Float(mode="output", view={"label": "Internal\nWeighted Premium", "format":utils.thousands_format(0)})
    })

    cds.override_node_properties("cds/layers", {
        "default_element_count": 6
    })

    cds.override_node_properties("cds/layers/excess", {
        "mode": "output",
        "view": {"label": "Attachment\nPoint"}
    })

    cds.override_node_properties("cds/layers/premium", {
        "default": 0,
        "mode": "input",
        "view": {"label": "Premium"}
    })

    cds.override_node_properties("cds/layers/limit", {
        "default": 0,
        "view": {"label": "Full Layer\nLimit", "format":utils.thousands_format(0)}
    })

    cds.override_node_properties("cds/standard_fields/insured_state_or_province", {
        "default": None, 
        "options_table": "state_lookup", 
        "options_column": "State", 
        "view": {"label": "State"},
    })

    cds.override_node_properties("cds/key_industry/code_type", {
        "default": "SIC_USA"
    })
    
    cds.override_node_properties("cds/key_industry/code", {
        "default_index": 0, 
        "optionality": "optional",
        "options_table": "sic_lookup", 
        "options_column": "SIC Code 4ch",
        "view": {"label": "SIC Code"}
    })

    cds.override_node_properties("cds/key_industry/code_name", {
        "mode": "output", 
        "view": {"label": "Industry Group"}
    })

    cds.extend_node_rater_defined(
        "cds/key_industry", {
            "industry_group": hx.Str(mode="output", view={"label": "Industry Group"}),
            "industry": hx.Str(mode="output", view={"label": "Industry"}),
    })

    cds.extend_node_rater_defined(
        "cds/exposure/aggregate", {
            "revenue": hx.Int(mode="input", default=0, view={"label": "Annual Revenue", "format": utils.thousands_format(0)}),
            "assets": hx.Int(mode="input", default=0, view={"label": "Assets", "format": utils.thousands_format(0)}),
            "employees": hx.Int(mode="input", default=0, view={"label": "Number of Officers and Employees", "format": utils.thousands_format(0)}),
            "locations": hx.Int(mode="input", default=0, view={"label": "Number of Locations", "format": utils.thousands_format(0)}),
    })

def sch_exposure_details_non_cds():
    return {
        "info_date": hx.Str(mode="output"),
        "total_adj_factor": hx.Float(mode="output"),
        "beazley_layer_index": hx.Int(mode="output"),
    }
        

