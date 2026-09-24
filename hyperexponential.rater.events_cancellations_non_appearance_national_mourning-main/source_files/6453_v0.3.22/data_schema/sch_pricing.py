# v0.5.0
import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_pricing(cds):
    cds.extend_node_rater_defined("cds", {
    # Use the following bucket for policy level information which does not vary by layer. 
    # See the user guide for more information. 
    # Extend the below as required.
        "rating_factors": hx.Structure(children={
            "policy_term":          hx.Float(mode="output"),
            "use_nm_app_old_model": hx.Float(mode="output"), # copying these from model state as they affect pricing so can be seen in snowflake
            "use_determ_agg_calc":  hx.Float(mode="output"), # copying these from model state as they affect pricing so can be seen in snowflake
            "is_migrated":          hx.Float(mode="output"), # copying these from model state
            "disable_validation":   hx.Float(mode="output"), # copying these from model state as they affect pricing so can be seen in snowflake

            # Add rating factors here 
        }),
        "rate_on_line_factors": hx.Structure(children={
            "migrated_rol_bound": hx.Float(  mode="input", default=None, optionality="optional", view={"label": "Migrated RoL Bound"}),
            "migrated_rol_quote": hx.Float(  mode="input", default=None, optionality="optional", view={"label": "Migrated RoL Quote"}),
            "migrated_rol_all":   hx.Float(  mode="input", default=None, optionality="optional", view={"label": "Migrated RoL All"}),
            # Add rating factors here 
        }),

    })


