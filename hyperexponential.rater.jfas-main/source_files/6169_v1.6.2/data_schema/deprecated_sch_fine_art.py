import hx_data_schema as hx
import data_schema.sch_z_utilities as utils
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

# SA: Depreciated stuff should all be removed. That's what version history is for

def sch_fine_art():
    # Section Risk Information
    return {

        # SUMMARY -----------------------------------------------------
        "fa_class": hx.Str(mode="input", default="", view={"label": "FA Class"}),

        **{
            f"fa_{type_in}_summary": hx.Structure(view={"label": type_in.capitalize()}, children={
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
            for type_in in ["premises", "travel", "additional"]
        },
        # PREMISES RATING -----------------------------------------------------
        **{
            f"fa_{premise}_summary": hx.List(mode="output", children={
                "country": hx.Str(mode="output", view={"label": "Country"}),
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "exp_band_1": hx.Float(mode="output", view={"label": "0-1m", "format": thousands_format()}),
                "exp_band_2": hx.Float(mode="output", view={"label": "1m-3m", "format": thousands_format()}),
                "exp_band_3": hx.Float(mode="output", view={"label": "3m-5m", "format": thousands_format()}),
                "exp_band_4": hx.Float(mode="output", view={"label": "5m-10m", "format": thousands_format()}),
                "exp_band_5": hx.Float(mode="output", view={"label": "10m-20m", "format": thousands_format()}),
                "exp_band_6": hx.Float(mode="output", view={"label": "20m-50m", "format": thousands_format()}),
                "exp_band_7": hx.Float(mode="output", view={"label": "50m-100m", "format": thousands_format()}),
                "exp_band_8": hx.Float(mode="output", view={"label": ">100m", "format": thousands_format()}),
            })
            for premise in ["static_art", "exhibitions", "fa_misc"]
        },
        **{
            f"fa_{premise}_summary_rates": hx.List(mode="output", children={
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
            for premise in ["static_art", "exhibitions", "fa_misc"]
        },
        **{
            f"fa_{premise}_summary_subtotal": hx.Structure(view={"label":"Sub-Total"}, children={
                "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
                "exp_band_1": hx.Float(mode="output", view={"label": "0-1m", "format": thousands_format()}),
                "exp_band_2": hx.Float(mode="output", view={"label": "1m-3m", "format": thousands_format()}),
                "exp_band_3": hx.Float(mode="output", view={"label": "3m-5m", "format": thousands_format()}),
                "exp_band_4": hx.Float(mode="output", view={"label": "5m-10m", "format": thousands_format()}),
                "exp_band_5": hx.Float(mode="output", view={"label": "10m-20m", "format": thousands_format()}),
                "exp_band_6": hx.Float(mode="output", view={"label": "20m-50m", "format": thousands_format()}),
                "exp_band_7": hx.Float(mode="output", view={"label": "50m-100m", "format": thousands_format()}),
                "exp_band_8": hx.Float(mode="output", view={"label": ">100m", "format": thousands_format()}),
            })
            for premise in ["static_art", "exhibitions", "fa_misc"]
        },
        # TRAVEL RATING -----------------------------------------------------
        # STANDARD
        **{
            f"fa_travel_rating_{utils.clean_string(travel)}": hx.Structure(children={
                "travel_type": hx.Str(mode="input", default = travel, options_table="table_input_fa_travel_type", options_column="type", view={"label": "Type"}),
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "uw_rate_per_100_tsi": hx.Float(mode="input", default = None, optionality = "optional", view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for travel in ["Transits within city", "Transits within country", "Transits within EU", "Transits EU - USA", "Transits ROW"]
        },
        "fa_travel_rating": hx.Structure(children={
            "travel_type": hx.Str(mode="input", default_index=0, options_table="table_input_fa_travel_type", options_column="type", view={"label": "Type"}),
            "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
            "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(3)}),
            "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(3)}),
            # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        }),
        # FA SPECIFIC
        **{
            f"fa_specific_additional_{utils.clean_string(specific)}": hx.Structure(view = {"label" : None}, children={
                "coverage": hx.Str(mode="input", default = specific, view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for specific in ["Defective Title", "Computers/Laptops", "Glass", "Jewellery in safe", "Jewellery worn", "Library/Reference", "Money", "Office Contents"]
        },
        "fa_specific_additional_custom": hx.List(mode="input", children={
            "coverage": hx.Str(mode="input", default=""),
            "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
            "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(3)}),
            "prem_rate_per_100_tsi": hx.Float(mode="input", default = 0.0025, view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(3)}),
            # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        }),
        **{
            f"fa_specific_ancilliary_{utils.clean_string(specific)}": hx.Structure(view = {"label" : None}, children={
                "coverage": hx.Str(mode="input", default = specific, view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for specific in ["BI", "Buildings", "Terrorism"]
        },
        "fa_specific_ancilliary_custom": hx.List(mode="input", children={
            "coverage": hx.Str(mode="input", default=""),
            "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
            "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(3)}),
            "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(3)}),
            # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        }),
        # EXHIBITIONS -----------------------------------------------------
        **{
            f"fa_specific_exhibitions_{utils.clean_string(specific)}": hx.Structure(children={
                    "coverage": hx.Str(mode="input", default = specific, view={"label": "Coverage"}),
                    "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                    "no_of_transits_per_month": hx.Float(mode="input", default = 0, view={"label": "No. of Transits \nper Months"}),
                    "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(3)}),
                    "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                    # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for specific in ["Nat cat", "Stay", "Terrorism"]
        },
        "fa_specific_exhibitions_custom": hx.List(mode="input", children={
            "coverage": hx.Str(mode="input", default=""),
            "tsi": hx.Float(mode="input", default=0.0, view={"label": "TSI", "format": thousands_format()}),
            "no_of_transits_per_month": hx.Float(mode="input", default=0.0, view={"label": "No. of Transits \nper Months"}),
            "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(3)}),
            "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Premium Rate \n(per 100 TSI)", "format": percent_format(3)}),
            # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        }),
        # EXHIBITIONS TRANSIT ------------------------------------------------
        **{
            f"fa_specific_exhibitions_transit_{utils.clean_string(specific)}": hx.Structure(children={
                    "coverage": hx.Str(mode="input", default = specific, view={"label": "Coverage"}),
                    "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                    "no_of_transits_each_way": hx.Float(mode="input", default = 0, view={"label": "No. of Transits \neach Way"}),
                    "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Rate \n(per 100 TSI)", "format": percent_format(3)}),
                    "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                    # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for specific in ["Transits within city", "Transits within country", "Transits within EU", "Transits EU - USA", "Transits ROW"]
        },
        "fa_specific_exhibitions_transit_custom": hx.List(mode="input", children={
                "coverage": hx.Str(mode="input", default = "", view={"label": "Coverage"}),
                "tsi": hx.Float(mode="input", default = 0, view={"label": "TSI", "format": thousands_format()}),
                "no_of_transits_each_way": hx.Float(mode="input", default = 0, view={"label": "No. of Transits \neach Way"}),
                "uw_rate_per_100_tsi": hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                "prem_rate_per_100_tsi": hx.Float(mode="output", view={"label": "Prem. Rate \n(per 100 TSI)", "format": percent_format(3)}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        }),
        # LIABILITY -----------------------------------------------------
        **{
            f"fa_specific_liability_employers_{utils.remove_spaces_string(employers)}": hx.Structure(children={
                    "employers_liability": hx.Str(mode="input", default = employers),
                    "no_of_employees": hx.Float(mode="input", default = 0, view={"label": "No. of Employees"}),
                    "per_employee": hx.Float(mode="output", view={"label": "Per Employee"}),
                    # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for employers in ["Base Premium", "5-10 employees", "10-20 employees", "20 or more employees"]
        },
        **{
            f"fa_specific_liability_manual_{utils.clean_string(manual)}": hx.Structure(children={
                    "manual_work_surcharge": hx.Str(mode="input", default = manual, view={"label": "Manual Work \nSurcharge"}),
                    "salary": hx.Float(mode="input", default = 0, view={"label": "Salary", "format": thousands_format()}),
                    "prem_rate": hx.Float(mode="output", view={"label": "Prem. Rate", "format": percent_format(3)}),
                    # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
            })
            for manual in ["Woodworkers", "Warehouseman", "Drivers", "Metalworkers & Polishers"]
        },
        "fa_specific_liability_public": hx.Structure(children={
                "public_liability": hx.Str(mode="input", default="Public Liability", view={"label": "Public Liability"}),
                "include_flag": hx.Bool(mode="input", default = False, view={"label": "Include (Yes/No)"}),
                # "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
        }),

    }

