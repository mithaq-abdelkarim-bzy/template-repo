import hx_data_schema as hx
import data_schema.sch_z_utilities as utils
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format


def sch_fine_art(cds):
    # Section Risk Information
    # SUMMARY -----------------------------------------------------
    for type_in in ["premises", "travel", "additional"]:
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_{type_in}", {
            "tsi": hx.Float(mode="output", view={"label": "TSI (cnv)", "format": thousands_format()}),
            # "deductible": hx.Float(mode="input", default=0, view={"label": "Ded", "format": thousands_format()}),
            "ded_perc": hx.Float(mode="input", default=0, view={"label": "Ded Perc", "format": percent_format(3)}),
            "credit": hx.Float(mode="output", view={"label": "Credit", "format": percent_format(3)}),
            # "uw_adj_impact": hx.Float(mode="input", default=0, optionality= "optional", view={"label": "Uw Select Credit", "format": percent_format(3)}),
            "prem_post_ded": hx.Float(mode="output", view={"label": "Prem Post Ded", "format": thousands_format()}),
            "implied_rate_post_ded": hx.Float(mode="output", view={"label": "Implied Rate Post Ded", "format": percent_format(3)}),
            "prem_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Premium LY", "format": thousands_format()}),
            "tsi_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "TSI LY (cnv)", "format": thousands_format()}),
            "ded_credit_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Ded Credit LY", "format": percent_format(3)}),
            "uw_adj_impact_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Uw Select Credit LY", "format": percent_format(3)}),
            "prem_post_ded_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Prem Post Ded LY", "format": thousands_format()}),
        })
        
        cds.override_node_properties(f"cds/layers/coverages/fa_{type_in}/premium", {"mode": "output", "view": {"label": "Premium"}})
        cds.override_node_properties(f"cds/layers/coverages/fa_{type_in}/uw_adj_impact", {"mode": "input", "default": None, "optionality": "optional", "view": {"label": "Uw Select Credit", "format": percent_format(3)}})

    # PREMISES RATING -----------------------------------------------------
    for premise in ["static_art", "exhibitions", "fa_misc"]:
        cds.extend_node_rater_defined("cds/layers/coverages/fa_premises", {
            f"{premise}_summary": hx.List(mode="output", children={ 
                "premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Bound Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "country": hx.Str(mode="output", view={"label": "Country"}),
                "tsi": hx.Float(mode="output", view={"label": "TSI (cnv)", "format": thousands_format()}),
                "exp_band_1": hx.Float(mode="output", view={"label": "0-1m", "format": thousands_format()}),
                "exp_band_2": hx.Float(mode="output", view={"label": "1m-3m", "format": thousands_format()}),
                "exp_band_3": hx.Float(mode="output", view={"label": "3m-5m", "format": thousands_format()}),
                "exp_band_4": hx.Float(mode="output", view={"label": "5m-10m", "format": thousands_format()}),
                "exp_band_5": hx.Float(mode="output", view={"label": "10m-20m", "format": thousands_format()}),
                "exp_band_6": hx.Float(mode="output", view={"label": "20m-50m", "format": thousands_format()}),
                "exp_band_7": hx.Float(mode="output", view={"label": "50m-100m", "format": thousands_format()}),
                "exp_band_8": hx.Float(mode="output", view={"label": ">100m", "format": thousands_format()}),
            })
        })

        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_premises", {
            f"{premise}_summary_rates": hx.List(mode="output", children={ 
                "country": hx.Str(mode="output", view={"label": "Country"}),
                "exp_band_1": hx.Float(mode="output", view={"label": "0-1m", "format": percent_format(3)}),
                "exp_band_2": hx.Float(mode="output", view={"label": "1m-3m", "format": percent_format(3)}),
                "exp_band_3": hx.Float(mode="output", view={"label": "3m-5m", "format": percent_format(3)}),
                "exp_band_4": hx.Float(mode="output", view={"label": "5m-10m", "format": percent_format(3)}),
                "exp_band_5": hx.Float(mode="output", view={"label": "10m-20m", "format": percent_format(3)}),
                "exp_band_6": hx.Float(mode="output", view={"label": "20m-50m", "format": percent_format(3)}),
                "exp_band_7": hx.Float(mode="output", view={"label": "50m-100m", "format": percent_format(3)}),
                "exp_band_8": hx.Float(mode="output", view={"label": ">100m", "format": percent_format(3)}),
            })
        })

        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_premises", {
            f"{premise}_summary_subtotal": hx.Structure(children={
                "tsi": hx.Float(mode="output", view={"label": "TSI (cnv)", "format": thousands_format()}),
                "exp_band_1": hx.Float(mode="output", view={"label": "0-1m", "format": thousands_format()}),
                "exp_band_2": hx.Float(mode="output", view={"label": "1m-3m", "format": thousands_format()}),
                "exp_band_3": hx.Float(mode="output", view={"label": "3m-5m", "format": thousands_format()}),
                "exp_band_4": hx.Float(mode="output", view={"label": "5m-10m", "format": thousands_format()}),
                "exp_band_5": hx.Float(mode="output", view={"label": "10m-20m", "format": thousands_format()}),
                "exp_band_6": hx.Float(mode="output", view={"label": "20m-50m", "format": thousands_format()}),
                "exp_band_7": hx.Float(mode="output", view={"label": "50m-100m", "format": thousands_format()}),
                "exp_band_8": hx.Float(mode="output", view={"label": ">100m", "format": thousands_format()}),
            })
        })

    # TRAVEL RATING -----------------------------------------------------
    # STANDARD
    for travel in range(5):
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_travel", {
            f"rating_{travel}": hx.Structure(children={
                "travel_type": hx.Str(mode="output", view={"label": "Type"}),
                "tsi": hx.Float(mode="input", default = 0, optionality = "optional", view={"label": "TSI", "format": thousands_format()}),
                "uw_rate_per_100_tsi": hx.Float(mode="input", default = None, optionality = "optional", view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    # FA SPECIFIC
    for specific in range(8):
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
            f"additional_{specific}": hx.Structure(children={
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
        "additional_custom": hx.List(mode="input", children={
            "coverage": hx.Str(mode="input", default=""),
            "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
            "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(4)}),
            "prem_rate_per_100_tsi": hx.Float(mode="input", default=0.0025, view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(4)}),
            "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        })
    })

    for specific in range(3):
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
            f"ancilliary_{specific}": hx.Structure(children={
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
        "ancilliary_custom": hx.List(mode="input", children={
            "coverage": hx.Str(mode="input", default=""),
            "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
            "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(4)}),
            "prem_rate_per_100_tsi": hx.Float(mode="input", default = 0.0025, view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(4)}),
            "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        })
    })


    # EXHIBITIONS -----------------------------------------------------
    for specific in range(3):
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
            f"exhibitions_{specific}": hx.Structure(children={
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "no_of_transits_per_month": hx.Float(mode="input", default = 0, view={"label": "Number of Transits per Months"}),
                "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    # EXHIBITIONS TRANSIT ------------------------------------------------
    for specific in range(5):
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
            f"exhibitions_transit_{specific}": hx.Structure(children={
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "no_of_transits_each_way": hx.Float(mode="input", default = 0, view={"label": "Number of Transits each Way"}),
                "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(4)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
        "exhibitions_transit_custom": hx.List(mode="input", children={
            "coverage": hx.Str(mode="input", default = "", view={"label": "Coverage"}),
            "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
            "no_of_transits_each_way": hx.Float(mode="input", default = 0, view={"label": "Number of Transits each Way"}),
            "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(4)}),
            "prem_rate_per_100_tsi": hx.Float(mode="input", default = 0.00025, view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(4)}),
            "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        })
    })


    # LIABILITY -----------------------------------------------------
    for employers in range(4):
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
            f"liability_employers_{employers}": hx.Structure(children={
                "employers_liability": hx.Str(mode="output", view = {"label" : "Employers Liability"}),
                "no_of_employees": hx.Float(mode="input", default = 0, view={"label": "No. of Employees"}),
                "per_employee": hx.Float(mode="output", view={"label": "Per Employee"}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    for manual in range(4):
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
            f"liability_manual_{manual}": hx.Structure(children={
                "manual_work_surcharge": hx.Str(mode="output", view={"label": "Manual Work Surcharge"}),
                "salary": hx.Float(mode="input", default = 0, view={"label": "Salary", "format": thousands_format()}),
                "prem_rate": hx.Float(mode="output", view={"label": "Prem. Rate", "format": percent_format(3)}),
                "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
        })

    cds.extend_node_rater_defined(f"cds/layers/coverages/fa_specific", {
        "liability_public": hx.Structure(children={
            "public_liability": hx.Str(mode="output", view={"label": "Public Liability"}),
            "include_flag": hx.Bool(mode="input", default = False, view={"label": "Include (Yes/No)"}),
            "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        })
    })

