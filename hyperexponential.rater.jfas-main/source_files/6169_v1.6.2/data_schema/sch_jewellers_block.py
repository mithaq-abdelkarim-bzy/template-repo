import hx_data_schema as hx
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format


def sch_jewellers_block(cds):
    for sub_group in ["premises", "travel", "additional"]:
        cds.extend_node_rater_defined(f"cds/layers/coverages/jb_{sub_group}", {
            "tsi": hx.Float(mode="output", view={"label": "TSI (cnv)", "format": thousands_format()}),
            # "deductible": hx.Float(mode="input", default=None, optionality = "optional", view={"label": "Ded", "format": thousands_format()}),
            "ded_perc": hx.Float(mode="input", default=None, optionality = "optional", view={"label": "Ded Perc", "format": percent_format(3)}),
            "credit": hx.Float(mode="output", view={"label": "Credit", "format": percent_format(3)}),
            # "uw_adj_impact": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Uw Select Credit", "format": percent_format(3)}),
            "prem_post_ded": hx.Float(mode="output", view={"label": "Prem Post Ded", "format": thousands_format()}),
            "implied_rate_post_ded": hx.Float(mode="output", view={"label": "Implied Rate Post Ded", "format": percent_format(3)}),
            "prem_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Premium LY", "format": thousands_format()}),
            "tsi_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "TSI LY (cnv)", "format": thousands_format()}),
            "ded_credit_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Ded Credit LY", "format": percent_format(3)}),
            "uw_adj_impact_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Uw Select Credit LY", "format": percent_format(3)}),
            "prem_post_ded_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Prem Post Ded LY", "format": thousands_format()}),
        })

        cds.override_node_properties(f"cds/layers/coverages/jb_{sub_group}/premium", {"mode": "output", "view": {"label": "Premium"}})
        cds.override_node_properties(f"cds/layers/coverages/jb_{sub_group}/uw_adj_impact", {"mode": "input", "default": None, "optionality": "optional", "view": {"label": "Uw Select Credit", "format": percent_format(3)}})

    for premise in ["retail", "wholesale", "manufacturing"]:
        cds.extend_node_rater_defined(f"cds/layers/coverages/jb_premises", {
            f"{premise}_summary": hx.List(mode="output", children={  
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
                "country": hx.Str(mode="output", view={"label": "Country"}),
                "tsi": hx.Float(mode="output", view={"label": "TSI (cnv)", "format": thousands_format()}),
                "exp_band_1": hx.Float(mode="output", view={"label": "500K", "format": thousands_format()}),
                "exp_band_2": hx.Float(mode="output", view={"label": "1m", "format": thousands_format()}),
                "exp_band_3": hx.Float(mode="output", view={"label": "2m", "format": thousands_format()}),
                "exp_band_4": hx.Float(mode="output", view={"label": "5m", "format": thousands_format()}),
                "exp_band_5": hx.Float(mode="output", view={"label": ">10m", "format": thousands_format()}),
                "rate_band_1": hx.Float(mode="output", view={"label": "500K", "format": percent_format(3)}),
                "rate_band_2": hx.Float(mode="output", view={"label": "1m", "format": percent_format(3)}),
                "rate_band_3": hx.Float(mode="output", view={"label": "2m", "format": percent_format(3)}),
                "rate_band_4": hx.Float(mode="output", view={"label": "5m", "format": percent_format(3)}),
                "rate_band_5": hx.Float(mode="output", view={"label": ">10m", "format": percent_format(3)}),
            })
        })
                    
        cds.extend_node_rater_defined(f"cds/layers/coverages/jb_premises", {
            f"{premise}_summary_subtotal": hx.Structure(children={
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "exp_band_1": hx.Float(mode="output", view={"label": "500K", "format": thousands_format()}),
                "exp_band_2": hx.Float(mode="output", view={"label": "1m", "format": thousands_format()}),
                "exp_band_3": hx.Float(mode="output", view={"label": "2m", "format": thousands_format()}),
                "exp_band_4": hx.Float(mode="output", view={"label": "5m", "format": thousands_format()}),
                "exp_band_5": hx.Float(mode="output", view={"label": ">10m", "format": thousands_format()}),
                "rate_band_1": hx.Float(mode="output", view={"label": "500K", "format": percent_format(3)}),
                "rate_band_2": hx.Float(mode="output", view={"label": "1m", "format": percent_format(3)}),
                "rate_band_3": hx.Float(mode="output", view={"label": "2m", "format": percent_format(3)}),
                "rate_band_4": hx.Float(mode="output", view={"label": "5m", "format": percent_format(3)}),
                "rate_band_5": hx.Float(mode="output", view={"label": ">10m", "format": percent_format(3)}),
            })
        })

    cds.extend_node_rater_defined(f"cds/layers/coverages/jb_travel", {
        "rating": hx.List(mode="input", children={
            "origin_region": hx.Str(mode="input", default_index=0, options_table="table_input_jb_travel_region", options_column="region", view={"label": "Origin Region"}),
            "type_elsewhere_region": hx.Structure(linked_options_table="table_input_jb_travel_type", linked_options_columns=["type", "region"], linked_default_index=0, children={
                "type": hx.Str(mode="input", view={"label": "Type"}),
                "elsewhere_region": hx.Str(mode="input", view={"label": "Elsewhere Region"}),
            }),
            "max_carryings": hx.Float(mode="input", default=0.0, view={"label": "Max Carryings", "format": thousands_format()}),
            "average_carryings": hx.Float(mode="input", default=0.0, view={"label": "Average Carryings", "format": thousands_format()}),
            "no_of_days": hx.Int(mode="input", default=0, view={"label": "No of Days"}),
            "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate (per 100 TSI)", "format": percent_format(3)}),
            "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        })
    }),

    # Default coverages - Additional Peril Premiums
    for coverage in range(10):
        cds.extend_node_rater_defined(f"cds/layers/coverages/jb_specific", {
            f"additional_{coverage}": hx.Structure(children={
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate (per 100 TSI)", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    # Default coverages - Ancillary Premiums
    for coverage in range(4):
        cds.extend_node_rater_defined(f"cds/layers/coverages/jb_specific", {
            f"ancillary_{coverage}": hx.Structure(children={
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate (per 100 TSI)", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    # Default coverages - Shipping Premiums
    for coverage in range(8):
        cds.extend_node_rater_defined(f"cds/layers/coverages/jb_specific", {
            f"shipping_{coverage}": hx.Structure(children={
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate (per 100 TSI)", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    # User specified coverages
    for specific in ["additional", "ancillary", "shipping"]:
        cds.extend_node_rater_defined(f"cds/layers/coverages/jb_specific", {
            f"{specific}_custom": hx.List(mode="input", children={ 
                "coverage": hx.Str(mode="input", default="", view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
                "prem_rate_per_100_tsi": hx.Float(mode="input", default=0.0, view={"label": "Prem. Rate (per 100 TSI)", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })


        
