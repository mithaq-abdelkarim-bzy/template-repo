import hx_data_schema as hx
import data_schema.sch_z_utilities as utils
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_general_specie(cds):
    # Section Risk Information

    cds.extend_node_rater_defined(f"cds", {
        "gs_transit_relativity": hx.Float(mode="output", view={"label": "Transit Relativity", "format":{"output":"percent", "mantissa":0}}),
    })

    # SUMMARY -----------------------------------------------------
    for type_in in ["metals", "cash", "securities", "additional"]:
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_{type_in}", {
            "tsi": hx.Int(mode="output", view={"label": "TSI (cnv)", "format": thousands_format()}),
            # "deductible": hx.Int(mode="input", default=0, view={"label": "Ded", "format": thousands_format()}),
            "ded_perc": hx.Float(mode="input", default=0, view={"label": "Ded Perc", "format": percent_format(3)}),
            "credit": hx.Float(mode="output", view={"label": "Credit", "format": percent_format(3)}),
            # "uw_adj_impact": hx.Float(mode="input", default=0, view={"label": "Uw Select Credit", "format": percent_format(3)}),
            "prem_post_ded": hx.Float(mode="output", view={"label": "Prem Post Ded", "format": thousands_format()}),
            "implied_rate_post_ded": hx.Float(mode="output", view={"label": "Implied Rate Post Ded", "format": percent_format(3)}),
            "prem_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label": "Premium LY", "format": thousands_format()}),
            "tsi_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "TSI LY (cnv)", "format": thousands_format()}),
            "ded_credit_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Ded Credit LY", "format": percent_format(3)}),
            "uw_adj_impact_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Uw Select Credit LY", "format": percent_format(3)}),
            "prem_post_ded_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Prem Post Ded LY", "format": thousands_format()}),
        })

        cds.override_node_properties(f"cds/layers/coverages/gs_{type_in}/premium", {"mode": "output", "view": {"label": "Premium"}})
        cds.override_node_properties(f"cds/layers/coverages/gs_{type_in}/uw_adj_impact", {"mode": "input", "default": None, "optionality": "optional", "view": {"label": "Uw Select Credit", "format": percent_format(3)}})

    # REGIONS -----------------------------------------------------
    # static - metals
    for region in range(7):
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_metals", {
            f"static_{region}": hx.Structure(children={
                "region": hx.Str(mode="output", view={"label": "Region"}),
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })
        
    # transit - metals
    for region in range(7):
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_metals", {
            f"transit_{region}": hx.Structure(children={
                "region": hx.Str(mode="output", view={"label": "Region"}),
                "tsi": hx.Float(mode="input", default =0, optionality = "optional", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })
        
    # Static - cash
    for region in range(7):
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_cash", {
            f"static_{region}": hx.Structure(children={
                "region": hx.Str(mode="output", view={"label": "Region"}),
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })
        
    # transit - cash
    for region in range(7):
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_cash", {
            f"transit_{region}": hx.Structure(children={
                "region": hx.Str(mode="output", view={"label": "Region"}),
                "tsi": hx.Float(mode="input", default =0, optionality = "optional", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    # Static - securities
    for region in range(7):
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_securities", {
            f"static_{region}": hx.Structure(children={
                "region": hx.Str(mode="output", view={"label": "Region"}),
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    # transit - securities
    for region in range(7):
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_securities", {
            f"transit_{region}": hx.Structure(children={
                "region": hx.Str(mode="output", view={"label": "Region"}),
                "tsi": hx.Float(mode="input", default =0, optionality = "optional", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    # additional
    cds.extend_node_rater_defined(f"cds/layers/coverages/gs_additional", {
        f"custom": hx.List(mode="input", default_element_count=3, children={
            "coverage": hx.Str(mode="input", default = "", view={"label": "Coverage"}),
            "tsi": hx.Float(mode="input", default = 0, optionality = "optional", view={"label": "TSI", "format": thousands_format()}),
            "prem_rate_per_100_tsi": hx.Float(mode="input", default = 0, view={"label": "Prem. Rate (per 100 TSI)", "format": percent_format(3)}),
            "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        })
    })


    # SUBTOTALS
    for gs_type in ["metals", "cash", "securities"]:
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_{gs_type}", {
            "static_subtotal": hx.Structure(children={
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            }),
            "transit_subtotal": hx.Structure(children={
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })
        
