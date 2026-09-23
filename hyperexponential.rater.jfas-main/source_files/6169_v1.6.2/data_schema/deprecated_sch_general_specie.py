import hx_data_schema as hx
import data_schema.sch_z_utilities as utils
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_general_specie():
    # Section Risk Information
    return {

        # SUMMARY -----------------------------------------------------
        "gs_class": hx.Str(mode="input", default="", view={"label": "Gs Class"}),

        **{
            f"gs_{type_in}_summary": hx.Structure(view={"label": type_in.capitalize()}, children={
                "premium": hx.Int(mode="output", view={"label": "Premium", "format": thousands_format()}),
                "tsi": hx.Int(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "ded": hx.Int(mode="input", default=0, view={"label": "Ded", "format": thousands_format()}),
                "ded_perc": hx.Float(mode="input", default=0, view={"label": "Ded Perc", "format": percent_format(3)}),
                "credit": hx.Float(mode="output", view={"label": "Credit", "format": percent_format(3)}),
                "uw_adj_impact": hx.Float(mode="input", default=0, view={"label": "Uw Select Credit", "format": percent_format(3)}),
                "prem_post_ded": hx.Float(mode="output", view={"label": "Prem Post Ded", "format": thousands_format()}),
                "implied_rate_post_ded": hx.Float(mode="output", view={"label": "Implied Rate Post Ded", "format": percent_format(3)}),
                "prem_ly": hx.Float(mode="output", view={"label": "Premium LY", "format": thousands_format()}),
                "tsi_ly": hx.Float(mode="output", view={"label": "TSI LY", "format": thousands_format()}),
                "ded_credit_ly": hx.Float(mode="output", view={"label": "Ded Credit LY", "format": percent_format(3)}),
                "uw_adj_impact_ly": hx.Float(mode="output", view={"label": "Uw Select Credit LY", "format": percent_format(3)}),
                "prem_post_ded_ly": hx.Float(mode="output", view={"label": "Prem Post Ded LY", "format": thousands_format()}),
            })
            for type_in in ["metals", "cash", "securities"]
        },

        "gs_transit_relativity": hx.Float(mode="output", view={"label": "Transit Relativity", "format":{"output":"percent", "mantissa":0}}),
        # METALS -----------------------------------------------------
        # static
        **{
            f"gs_static_metals_region_{region}": hx.Structure(view= {"label":region.replace("_"," ").title()}, children={
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for region in utils.region_list_static
        },
        # transit
        **{
            f"gs_transit_metals_region_{region}": hx.Structure(view= {"label":region.replace("_"," ").title()}, children={
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for region in utils.region_list_transit
        },
        "gs_transit_metals_region_total": hx.Structure(view= {"label":"Total"}, children={
            "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
            "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
            # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        }),
        # CASH -----------------------------------------------------
        # static
        **{
            f"gs_static_cash_region_{region}": hx.Structure(view= {"label":region.replace("_"," ").title()}, children={
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for region in utils.region_list_static
        },
        # transit
        **{
            f"gs_transit_cash_region_{region}": hx.Structure(view= {"label":region.replace("_"," ").title()}, children={
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for region in utils.region_list_transit
        },
        "gs_transit_cash_region_total": hx.Structure(view= {"label":"Total"}, children={
            "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
            "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
            # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        }),
        # SECURITIES -----------------------------------------------------
        # static
        **{
            f"gs_static_securities_region_{region}": hx.Structure(view= {"label":region.replace("_"," ").title()}, children={
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for region in utils.region_list_static
        },
        # transit 
        **{
            f"gs_transit_securities_region_{region}": hx.Structure(view= {"label":region.replace("_"," ").title()}, children={
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for region in utils.region_list_transit
        },
        "gs_transit_securities_region_total": hx.Structure(view= {"label":"Total"}, children={
            "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
            "rate": hx.Float(mode="output", view={"label": "Rate", "format": percent_format(3)}),
            # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        }),
        "ded_input_metals_display" : hx.Str(mode = "output"),
        "ded_input_cash_display" : hx.Str(mode = "output"),
        "ded_input_securities_display" : hx.Str(mode = "output"),
    }

