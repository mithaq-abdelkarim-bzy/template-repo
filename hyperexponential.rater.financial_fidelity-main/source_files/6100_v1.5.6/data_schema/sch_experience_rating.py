import hx_data_schema as hx
from libraries.common_data_schema.data_schema.utilities import thousands_format
from libraries.common_data_schema.data_schema.utilities import integer_format
import algorithms.utils_global_lists as lst

def sch_experience_rating(cds):
    cds.extend_node_rater_defined("cds/experience_rating", {
        "total": hx.Structure(view={"label": "Total"}, children={
            "exceeds_500k": hx.Int(mode="output"),
            "adjusted_loss": hx.Float(mode="output", view={"format": thousands_format(0)}),
        }),
        "use_excess_experience_mod": hx.Bool(mode="input", default=False, view={"label": "Use Excess Experience Mod?"}),
        "eligible_for_excess_experience_mod": hx.Bool(mode="output", view={"label": "Eligible for Excess Experience Mod?"}),
        "experience_modification": hx.Float(mode="output", view={"label": "Experience Modification"}),
    })

    cds.extend_node_rater_defined("cds/experience_rating/claims", {
        "date": hx.Date(mode="input", default="2000-01-01", view={"label": "Date of Loss"}),
        "loss": hx.Float(mode="input", default=0, view={"label": "Ground Up Loss", "format": thousands_format(0)}),
        "coverage": hx.Str(mode="input", default_index=0, options_table="Coverages", options_column="Coverage Type", view={"label": "Coverage"}),
        "limited_coverage": hx.Float(mode="output", view={"label": "Limited Coverage", "format": thousands_format(0)}),
        "limited_deductible": hx.Float(mode="output", view={"label": "Limited Deductible", "format": thousands_format(0)}),
        "net_direct_loss_incurred": hx.Float(mode="output", view={"label": "Net Direct Loss Incurred", "format": thousands_format(0)}),
        "exceeds_500k": hx.Str(mode="output", view={"label": "Exceeds $500k?"}),
        "exceeds_500k_num": hx.Int(mode="output"),
        "adjusted_loss": hx.Float(mode="output", view={"label": "Adjusted Loss", "format": thousands_format(0)}),
    })

    cds.extend_node_rater_defined("cds/layers", {
        "manual_premium_max_coverage": hx.Float(mode="output"),
        "manual_premium_max_deductible": hx.Float(mode="output"),
    })


        

