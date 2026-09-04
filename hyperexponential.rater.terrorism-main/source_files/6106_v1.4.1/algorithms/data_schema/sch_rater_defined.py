import hx_data_schema as hx
import algorithms.rate_constants as c
from algorithms.data_schema.sch_utilities import thousands_format, percent_format, integer_format, hx_node, get_existing_attributes

### --- DEFINING THE NODES HERE SO THAT THEIR PROPERTIES ARE DYNAMICALLY ACCESSIBLE BY THE RATING ALGORITHM --- ###


### --- EXPOSURE DICTIONARY FOR AGGREGATE AND GRANULAR --- ###
perils_dict = {
    "is_covered"    : hx.Str(  mode="override", async_input=["task_confirm_limits"], view={"label": "Covered"},                                  options=["Yes", "No"]),
    "limit"         : hx.Float(mode="override", async_input=["task_confirm_limits"], view={"label": "Limit",      "format": thousands_format()}, validation={"min_value": 0}),
    "excess"        : hx.Float(mode="override", async_input=["task_confirm_limits"], view={"label": "Excess",     "format": thousands_format()}, validation={"min_value": 0}),
    "deductible"    : hx.Float(mode="override", async_input=["task_confirm_limits"], view={"label": "Deductible", "format": thousands_format()}, validation={"min_value": 0}),
}

perils_dict_calculated = {
    "is_covered_calculated"    : hx.Str(  mode="output",                                        view={"label": "Covered\nCalculated"},                                  options=["Yes", "No"]),
    "limit_calculated"         : hx.Float(mode="output",                                        view={"label": "Limit\nCalculated",      "format": thousands_format()}, validation={"min_value": 0}),
    "excess_calculated"        : hx.Float(mode="output",                                        view={"label": "Excess\nCalculated",     "format": thousands_format()}, validation={"min_value": 0}),
    "deductible_calculated"    : hx.Float(mode="output",                                        view={"label": "Deductible\nCalculated", "format": thousands_format()}, validation={"min_value": 0}),
}

perils_dict_override = {
    "is_covered_override"      : hx.Str(  mode="input", default=None, optionality="optional",   view={"label": "Covered\nOverride"},                                    options=["Yes", "No"]),
    "limit_override"           : hx.Float(mode="input", default=None, optionality="optional",   view={"label": "Limit\nOverride",        "format": thousands_format()}, validation={"min_value": 0}),
    "excess_override"          : hx.Float(mode="input", default=None, optionality="optional",   view={"label": "Excess\nOverride",       "format": thousands_format()}, validation={"min_value": 0}),
    "deductible_override"      : hx.Float(mode="input", default=None, optionality="optional",   view={"label": "Deductible\nOverride",   "format": thousands_format()}, validation={"min_value": 0}),
}

perils_dict_selected = {
    "is_covered_selected"      : hx.Str(  mode="output", async_input=["task_confirm_limits"],        view={"label": "Covered\nSelected"},                                    options=["Yes", "No"]),
    "limit_selected"           : hx.Float(mode="output", async_input=["task_confirm_limits"],        view={"label": "Limit\nSelected",        "format": thousands_format()}, validation={"min_value": 0}),
    "excess_selected"          : hx.Float(mode="output", async_input=["task_confirm_limits"],        view={"label": "Excess\nSelected",       "format": thousands_format()}, validation={"min_value": 0}),
    "deductible_selected"      : hx.Float(mode="output", async_input=["task_confirm_limits"],        view={"label": "Deductible\nSelected",   "format": thousands_format()}, validation={"min_value": 0}),
}

perils_dict =  perils_dict_calculated | perils_dict_override | perils_dict_selected


perils = {
    "terrorism"     : hx.Structure(view={"label": "Terrorism"},             children=perils_dict),
    "sabotage"      : hx.Structure(view={"label": "Sabotage"},              children=perils_dict),
    "rscc"          : hx.Structure(view={"label": "RSCC"},                  children=perils_dict),
    "damage"        : hx.Structure(view={"label": "Malicious Damage"},      children=perils_dict),
    "insurrection"  : hx.Structure(view={"label": "Insurrection"},          children=perils_dict),
    "coup"          : hx.Structure(view={"label": "Coup d'Etat"},           children=perils_dict),
    "war"           : hx.Structure(view={"label": "War on Land"},           children=perils_dict),
    "insurgency"    : hx.Structure(view={"label": "Counter Insurgency"},    children=perils_dict),
    "liability"     : hx.Structure(view={"label": "Terrorism Liability"},   children=perils_dict),
    "cyber"         : hx.Structure(view={"label": "Terrorism Cyber"},       children=perils_dict),
    "nrcb"          : hx.Structure(view={"label": "NRCB"},                  children=perils_dict),
    "looting"       : hx.Structure(view={"label": "Looting"},               children=perils_dict),
}

def cbi_perils(read_only=False):
    return {
        "is_covered_selected"    : hx.Str(  mode="input", default="No",                         view={"label": "Covered"},                                                             options=["Yes", "No"]),
        "limit_selected"         : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Limit",        "format": thousands_format()},                          validation={"min_value": 0}),
        "excess_selected"        : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess",       "format": thousands_format()},                          validation={"min_value": 0}),
        "deductible_selected"    : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Deductible",   "format": thousands_format()},                          validation={"min_value": 0}),
        "distance_selected"      : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Distance",     "format": thousands_format(), "read_only": read_only},  validation={"min_value": 0}),
        "metric_selected"        : hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Distance\nMetric",                           "read_only": read_only},  options=["Meters", "Kilometers", "Miles"]),
    }


def cbi_perils(read_only_dist=False,read_only_terr=False):
    return {
        "is_covered_selected"    : hx.Str(  mode="input", default="No",                         view={"label": "Covered"},                                                                  options=["Yes", "No"]),
        "limit_selected"         : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Limit",        "format": thousands_format()},                               validation={"min_value": 0}),
        "excess_selected"        : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess",       "format": thousands_format()},                               validation={"min_value": 0}),
        "deductible_selected"    : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Deductible",   "format": thousands_format()},                               validation={"min_value": 0}),
        "distance_selected"      : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Distance",     "format": thousands_format(), "read_only": read_only_dist},  validation={"min_value": 0}),
        "metric_selected"        : hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Distance\nMetric",                           "read_only": read_only_dist},  options=["Meters", "Kilometers", "Miles"]),
        "territory_covered"      : hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Territory\nCovered",                         "read_only": read_only_terr},  options=["Scheduled", "Worldwide"]),
    }





aggregate_exposure_dict = {
    "total_sum_insured" : hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Total Sum Insured",    "format": thousands_format()}),
    "bi_sum_insured"    : hx.Float(mode="output", async_input=["rarc_task"], view={"label": "BI Sum Insured",       "format": thousands_format()}),
    "pd_sum_insured"    : hx.Float(mode="output", async_input=["rarc_task"], view={"label": "PD Sum Insured",       "format": thousands_format()}),
    "policy_limit"      : hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Policy Limit",         "format": thousands_format()}),
    "policy_sublimit"   : hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Policy Sub Limit",     "format": thousands_format()}),
    "policy_excess"     : hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Policy Excess",        "format": thousands_format()}),
    "policy_deductible" : hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Policy Deductible",    "format": thousands_format()}),
    "no_of_locations"   : hx.Float(mode="output",                            view={"label": "Number of Locations",  "format": thousands_format()}),
    "agg_discount"      : hx.Float(mode="output",                            view={"label": "Agg Discount",         "format": percent_format(1)}),
    "has_construction"  : hx.Bool( mode="output"),
    
    "details": hx.Structure(view={"label": None}, children={
        "limit_type"         : hx.Str( mode="input", default="Occurrence & Agg",           async_input=["rarc_task"], view={"label": "Type of Limit"},                  options=["Occurrence & Agg", "Occurrence only"]),
        "bi_wait_period"     : hx.Int( mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "BI Wait Period (days)", "info": "Leave the wait period blank to assume a combined monetary deductible."}),
        "bi_indemnity_period": hx.Int( mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "BI Indemnity Period (months)"}),
        "contingent_bi"      : hx.Bool(mode="input", default=False,                        async_input=["rarc_task"], view={"label": "Contingent BI"}),
        "aggregate_usage"    : hx.Str( mode="input", default="Low",                        async_input=["rarc_task"], view={"label": "Aggregate Usage"},                options=["High", "Medium", "Low"] )
    }),

    "perils":     hx.Structure(children=perils),
    "cbi_perils": hx.Structure(children={
        "unnamed"       : hx.Structure(view={"label": "Unnamed Customers & Suppliers"}, children=cbi_perils(read_only_dist=True, read_only_terr=False)),
        "named"         : hx.Structure(view={"label": "Named Customers & Suppliers"},   children=cbi_perils(read_only_dist=True, read_only_terr=False)),
        "interruption"  : hx.Structure(view={"label": "Service Interruption"},          children=cbi_perils(read_only_dist=True, read_only_terr=True)),
        "denial"        : hx.Structure(view={"label": "Denial of Access"},              children=cbi_perils(read_only_dist=False,read_only_terr=True)),
        "ingress"       : hx.Structure(view={"label": "Ingress/Egress"},                children=cbi_perils(read_only_dist=False,read_only_terr=True)),
        "authority"     : hx.Structure(view={"label": "Civil/Military Authority"},      children=cbi_perils(read_only_dist=False,read_only_terr=True)),
    }),
    "temp_perils":                      hx.Str( mode="input", default="{}", async_output=["task_confirm_limits","start_renewal_task"]),
    "are_limits_correct":               hx.Bool(mode="output"),
    "confirm_message":                  hx.Str( mode="output"),
    "peril_comments":                   hx.Str( mode="input", default=None, optionality="optional"),
    "cbi_peril_territory_covered_show": hx.Bool(mode="output", view={"label": "cbi_peril_territory_covered_show"}),

}

proxy_country_info = "This field is to be used when it is more appropriate to use a single countries score when rating a Region. Please still enter a region in the countries column."
ihs_risk_names = {
    "political"     : "Political",
    "terrorism_raw" : "Terrorism",
    "labour_strikes": "LabourStrikes",
    "protests_riots": "ProtestsAndRiots",
    "interstate_war": "InterstateWar",
    "civil_war"     : "CivilWar"
}
base_perils = ["civil_unrest", "war", "terrorism"]
#YZ 24/10/2025 Add a column of text input of Country before cleaning
granular_exposure_dict = {
    "countries": hx.List(mode="input", async_input=["task_fetch_ihs_data", "rarc_task"], async_output=[{"task": "rarc_task", "reset": False}], children={
        "country": hx.Str(mode="input", default=None, optionality="optional", options_table="countries", options_column="Country", allow_custom_value = True, async_input=["task_fetch_ihs_data", "rarc_task"],async_output = [{"task":"clean_country_task", "reset": False}], view={"label": "Country"}),
        "country_raw": hx.Str(mode = "input", optionality="optional", default = None, view = {"label": "Country Raw"}),
        "country_clean": hx.Str(mode = "output",async_input=["clean_country_task"] ,view = {"label": "Country Cleaned", "info": "Copy the column to 'Country' for rating"}),
        "proxy_rating_country": hx.Str(mode="input", default=None, optionality="optional", options_table="countries", options_column="Country", async_input=["rarc_task"], view={"label": "Proxy\nRating\nCountry", "info": proxy_country_info}),
        "rated_country": hx.Str(mode="output", async_input=["task_fetch_ihs_data", "rarc_task"], view={"label": "Rated Country"}),
        "country_code_original": hx.Str(mode="output", async_input=["task_fetch_ihs_data", "rarc_task"], view={"label": "Country Code"}),
        "country_code": hx.Str(mode="output", async_input=["task_fetch_ihs_data", "rarc_task"], view={"label": "Country Code\nAugmented"}),
        "no_of_locations": hx.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "# Locations / \nGroups"}),
        "pml": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "PML / \nTop Location TIV", "format": thousands_format()}),
        "coverage": hx.Str(mode="input", default=None, optionality="optional", options_table="coverage", options_column="Coverage", async_input=["task_fetch_ihs_data", "rarc_task","copy_country_covers_task"], async_output=[({"task": "copy_country_covers_task", "reset": False})],view={"label": "Coverage"}),
        "limit": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "copy_country_covers_task"], async_output=[({"task": "copy_country_covers_task", "reset": False})], view={"label": "Limit", "format": thousands_format()}),
        "excess": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "copy_country_covers_task"], async_output=[({"task": "copy_country_covers_task", "reset": False})], view={"label": "Excess", "format": thousands_format()}),
        "subcoverage": hx.Str(mode="input", default=None, optionality="optional", options_table="subcoverage", options_column="Sub Coverage", async_input=["task_fetch_ihs_data", "rarc_task", "copy_country_covers_task"], async_output=[({"task": "copy_country_covers_task", "reset": False})], view={"label": "Sub-coverage"}),
        "sublimit": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "copy_country_covers_task"], async_output=[({"task": "copy_country_covers_task", "reset": False})], view={"label": "Sub-limit", "format": thousands_format()}),
        "deductible": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "copy_country_covers_task"], async_output=[({"task": "copy_country_covers_task", "reset": False})], view={"label": "Deductible", "format": thousands_format()}),
        "total_sum_insured": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "copy_country_covers_task"], async_output=[({"task": "copy_country_covers_task", "reset": False})], view={"label": "Total\nSum Insured", "format": thousands_format(), "info": "Only to be used if BI / PD split is not available. A 70%/30% PD/BI split will be assumed."}),
        "bi_sum_insured": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "copy_country_covers_task"], async_output=[({"task": "copy_country_covers_task", "reset": False})], view={"label": "BI\nSum Insured", "format": thousands_format()}),
        "pd_sum_insured": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "copy_country_covers_task"], async_output=[({"task": "copy_country_covers_task", "reset": False})], view={"label": "PD\nSum Insured", "format": thousands_format()}),
        "liability_risk": hx.Str(mode="input", default="Default", options_table="country_risk", options_column="Liability", async_input=["rarc_task"], view={"label": "Liability\nRisk"}),
        "attritional_risk": hx.Str(mode="input", default="Default", options_table="country_risk", options_column="Attr Risk", async_input=["rarc_task"], view={"label": "Attritional\nRisk"}),
        "geog_risk": hx.Str(mode="input", default="Default", options_table="country_risk", options_column="Geog Risk", async_input=["rarc_task"], view={"label": "Geog\nRisk"}),
        "location_cat_risk": hx.Str(mode="input", default="Default", options_table="country_risk", options_column="Cat Risk", async_input=["rarc_task"], view={"label": "Location\nCat Risk"}),
        **{
            k: hx.Float(mode="input", default=0, async_input=["rarc_task"], async_output=["task_fetch_ihs_data","start_renewal_task"], view={"label": v, "format": thousands_format(2), "group": "From Raw IHS Data", "read_only": True})
            for k, v in ihs_risk_names.items()
        },
        "civil_unrest": hx.Float(mode="output", view={"label": "Civil Unrest (initial blend)", "format": thousands_format(2), "info": "Avg of 'Labour Strikes' and 'Protests and Riots'."}),
        "war": hx.Float(mode="output", view={"label": "War (initial blend)", "format": thousands_format(2), "info": "Avg of 'Interstate War' and 'Civil War'."}),
        "terrorism": hx.Float(mode="output", view={"label": "Terrorism (initial blend)", "format": thousands_format(2), "info": "Avg of 'Political', 'Terrorism', 'Civil Unrest', and 'War'."}),
        "selected_sum_insured": hx.Float(mode="output", view={"label": "Total\nSum Insured", "format": thousands_format()}),
        "warning": hx.Str(mode="output", view={"label": "Warning"}),
        
        # For IHS adjustments
        "civil_unrest_roe_calculated":  hx.Float(mode="output",                                      view={"label": "ROE (Calculated)",         "format": percent_format(4)}),
        "civil_unrest_roe_selected":    hx.Float(mode="output",                                      view={"label": "ROE (Selected)",           "format": percent_format(4)}),
        "war_roe_calculated":           hx.Float(mode="output",                                      view={"label": "ROE (Calculated)",         "format": percent_format(4)}),
        "war_roe_selected":             hx.Float(mode="output",                                      view={"label": "ROE (Selected)",           "format": percent_format(4)}),
        "terrorism_roe_calculated":     hx.Float(mode="output",                                      view={"label": "ROE (Calculated)",         "format": percent_format(4)}),
        "terrorism_roe_selected":       hx.Float(mode="output",                                      view={"label": "ROE (Selected)",           "format": percent_format(4)}),

        "civil_unrest_uw_adj":          hx.Float(mode="output",                                      view={"label": "UW Adjustment (implied)",  "format": percent_format(0), "options": {"red": {"style_row": "hx-bad"}}}),
        "war_uw_adj":                   hx.Float(mode="output",                                      view={"label": "UW Adjustment (implied)",  "format": percent_format(0), "options": {"red": {"style_row": "hx-bad"}}}),
        "terrorism_uw_adj":             hx.Float(mode="output",                                      view={"label": "UW Adjustment (implied)",  "format": percent_format(0), "options": {"red": {"style_row": "hx-bad"}}}),

        "override_civil_unrest":        hx.Float(mode="input", default=None, optionality="optional", view={"label": "Civil Unrest (Override)",  "format": thousands_format(2)}, async_input=["rarc_task"]),
        "override_war":                 hx.Float(mode="input", default=None, optionality="optional", view={"label": "War (Override)",           "format": thousands_format(2)}, async_input=["rarc_task"]),
        "override_terrorism":           hx.Float(mode="input", default=None, optionality="optional", view={"label": "Terrorism  (Override)",    "format": thousands_format(2)}, async_input=["rarc_task"]),

        "selected_civil_unrest":        hx.Float(mode="output",                                      view={"label": "Civil Unrest (Selected)",  "format": thousands_format(2)}),
        "selected_war":                 hx.Float(mode="output",                                      view={"label": "War (Selected)",           "format": thousands_format(2)}),
        "selected_terrorism":           hx.Float(mode="output",                                      view={"label": "Terrorism  (Selected)",    "format": thousands_format(2)
                                                                                                            ,"info": "Avg of 'Political', 'Terrorism', 'Civil Unrest (Selected)', and 'War (Selected)' unless an override has been applied to terrorism."}),

        "has_civil_unrest":             hx.Bool( mode="output"),
        "has_war":                      hx.Bool( mode="output"),
        "has_terrorism":                hx.Bool( mode="output"),

        "leading_peril":                    hx.Str(  mode="output",                                  view={"label": "Leading Peril"}),
        "selected_sum_insured_contribution":hx.Float(mode="output",                                  view={"label": "TIV%",                     "format": percent_format(0)}),

        # For rate change
        "country_cvg_subcvg":           hx.Str(  mode="input", default=None, optionality="optional",               async_input=["rarc_task"], async_output=["task_fetch_ihs_data","start_renewal_task"]),
        "country_cvg_subcvg_live":      hx.Str(  mode="output"),
    }),
    # For Exposure Details
    "ihs_uw_rationale": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Rationale"}),
    "show_ihs_adj_details": hx.Bool(mode="input", default=False, view={"label": "Show detailed IHS adjustment"}),
    "civil_unrest_info": hx.Str(mode="output"),
    "war_info": hx.Str(mode="output"),
    "terrorism_info": hx.Str(mode="output"),
    **{
        key: value
        for peril in base_perils
        for key, value in {
            f"{peril}_info": hx.Str(mode="output"),
            f"{peril}_uw_adj_info": hx.Str(mode="output"),
            f"{peril}_uw_adj_valid": hx.Bool(mode="output"),
            f"{peril}_uw_adj_invalid": hx.Bool(mode="output")
        }.items()
    },
    # For Countries
    "show_warning": hx.Bool(mode="output"),
    "show_ihs_scores": hx.Bool(mode="input", default=False, view={"label": "Show Raw IHS Scores"}),
    "show_pricing": hx.Bool(mode="input", default=False, view={"label": "Show Actuarial Pricing"}),
    "show_country_clean": hx.Bool(mode = "input", default = False, view = {"label":  "Cleanse the case formatting of country names"}),
    # For chart
    "has_at_least_one_country": hx.Bool(mode="output"),
    "refresh_message": hx.Str(mode="output"),
    "ihs_api_error_msg": hx.Str(mode="output", async_output=["task_fetch_ihs_data","start_renewal_task"]),
    "show_chart": hx.Bool(mode="output"),
    "selected_country": hx.Str(mode="input", default=None, optionality="optional", options_data="../countries", options_field="rated_country", async_output=["task_fetch_ihs_data","start_renewal_task"], view={"label": "Select country to visualise"}),
    "country_message": hx.Str(mode="input", default="Unable to show historical data for regions - please select a country instead.", view={"read_only": True}),
    "show_country_message": hx.Bool(mode="output"),

    # ROE calculations
    "bi_multiplier": hx.Float(mode="output", view={"label": "BI Multiplier", "format": thousands_format(4, True)}),
    "no_of_countries": hx.Int(mode="output", view={"label": "Number of Countries"}),
    "wa_nl_min_rol": hx.Float(mode="output", view={"label": "Non Liability", "format": percent_format(4)}),
    "wa_liab_min_rol": hx.Float(mode="output", view={"label": "Liability", "format": percent_format(4)}),
    "roe": hx.List(mode="output", children={
        "country":                  hx.Str(  mode="output", view={"label": "Country",                   "group": "Data"}),
        "no_of_locations":          hx.Int(  mode="output", view={"label": "Number of\nLocations"}),
        "attritional_risk":         hx.Str(  mode="output", view={"label": "Attritional risk",          "group": "Data"}),
        "geog_risk":                hx.Str(  mode="output", view={"label": "Geog risk",                 "group": "Data"}),
        "location_cat_risk":        hx.Str(  mode="output", view={"label": "Location cat risk",         "group": "Data"}),
        "total_sum_insured":        hx.Float(mode="output", view={"label": "Total Sum Insured",         "group": "Data",                            "format": thousands_format(4, True)}),
        "bi_sum_insured":           hx.Float(mode="output", view={"label": "BI Total Sum Insured",      "group": "Data",                            "format": thousands_format(4, True)}),
        "pd_sum_insured":           hx.Float(mode="output", view={"label": "PD Total Sum Insured",      "group": "Data",                            "format": thousands_format(4, True)}),
        "civil_unrest":             hx.Float(mode="output", view={"label": "Civil Unrest\n(Default)",   "group": "IHS Scores"}),
        "war":                      hx.Float(mode="output", view={"label": "War\n(Default)",            "group": "IHS Scores"}),
        "terrorism":                hx.Float(mode="output", view={"label": "Terrorism\n(Default)",      "group": "IHS Scores"}),
        "coverage":                 hx.Str(  mode="output", view={"label": "Coverage",                  "group": "Coverage codes"}),
        "coverage_code":            hx.Int(  mode="output", view={"label": "Coverage Code",             "group": "Coverage codes"}),
        "subcoverage":              hx.Str(  mode="output", view={"label": "Subcoverage",               "group": "Coverage codes"}),
        "subcoverage_code":         hx.Int(  mode="output", view={"label": "Subcoverage Code",          "group": "Coverage codes"}),
        "selected_sum_insured":     hx.Float(mode="output", view={"label": "Calculated Total Sum Insured",                                          "format": thousands_format(4, True)}),
        "risk_multiplier":          hx.Float(mode="output", view={"label": "Multiplier calc",                                                       "format": thousands_format(4, True)}),
        "bi_terrorism_c":           hx.Float(mode="output", view={"label": "Terrorism c",               "group": "BI - f(IHS) parameters",          "format": thousands_format(8, True)}),
        "bi_terrorism_b":           hx.Float(mode="output", view={"label": "Terrorism b",               "group": "BI - f(IHS) parameters",          "format": thousands_format(4, True)}),
        "bi_civil_unrest_c":        hx.Float(mode="output", view={"label": "Civil unrest c",            "group": "BI - f(IHS) parameters",          "format": thousands_format(8, True)}),
        "bi_civil_unrest_b":        hx.Float(mode="output", view={"label": "Civil unrest b",            "group": "BI - f(IHS) parameters",          "format": thousands_format(4, True)}),
        "bi_war_c":                 hx.Float(mode="output", view={"label": "War c",                     "group": "BI - f(IHS) parameters",          "format": thousands_format(8, True)}),
        "bi_war_b":                 hx.Float(mode="output", view={"label": "War b",                     "group": "BI - f(IHS) parameters",          "format": thousands_format(4, True)}),
        "bi_terrorism_roe":         hx.Float(mode="output", view={"label": "Terrorism RoE",             "group": "BI - RoE = f(IHS)*multiplier",    "format": percent_format(4)}),
        "bi_civil_unrest_roe":      hx.Float(mode="output", view={"label": "Civil unrest RoE",          "group": "BI - RoE = f(IHS)*multiplier",    "format": percent_format(4)}),
        "bi_war_roe":               hx.Float(mode="output", view={"label": "War RoE",                   "group": "BI - RoE = f(IHS)*multiplier",    "format": percent_format(4)}),
        "pd_terrorism_c":           hx.Float(mode="output", view={"label": "Terrorism c",               "group": "PD - f(IHS) parameters",          "format": thousands_format(8, True)}),
        "pd_terrorism_b":           hx.Float(mode="output", view={"label": "Terrorism b",               "group": "PD - f(IHS) parameters",          "format": thousands_format(4, True)}),
        "pd_civil_unrest_c":        hx.Float(mode="output", view={"label": "Civil unrest c",            "group": "PD - f(IHS) parameters",          "format": thousands_format(8, True)}),
        "pd_civil_unrest_b":        hx.Float(mode="output", view={"label": "Civil unrest b",            "group": "PD - f(IHS) parameters",          "format": thousands_format(4, True)}),
        "pd_war_c":                 hx.Float(mode="output", view={"label": "War c",                     "group": "PD - f(IHS) parameters",          "format": thousands_format(8, True)}),
        "pd_war_b":                 hx.Float(mode="output", view={"label": "War b",                     "group": "PD - f(IHS) parameters",          "format": thousands_format(4, True)}),
        "pd_terrorism_roe":         hx.Float(mode="output", view={"label": "Terrorism RoE",             "group": "PD - RoE = f(IHS)*multiplier",    "format": percent_format(4)}),
        "pd_civil_unrest_roe":      hx.Float(mode="output", view={"label": "Civil unrest RoE",          "group": "PD - RoE = f(IHS)*multiplier",    "format": percent_format(4)}),
        "pd_war_roe":               hx.Float(mode="output", view={"label": "War RoE",                   "group": "PD - RoE = f(IHS)*multiplier",    "format": percent_format(4)}),
        "selected_terrorism_roe":   hx.Float(mode="output", view={"label": "Terrorism RoE",             "group": "RoE Selected",                    "format": percent_format(4)}),
        "selected_civil_unrest_roe":hx.Float(mode="output", view={"label": "Civil unrest RoE",          "group": "RoE Selected",                    "format": percent_format(4)}),
        "selected_war_roe":         hx.Float(mode="output", view={"label": "War RoE",                   "group": "RoE Selected",                    "format": percent_format(4)}),
        "cvg_terrorism":            hx.Int(  mode="output", view={"label": "Terrorism",                 "group": "Main coverage identifiers"}),
        "cvg_civil_unrest":         hx.Int(  mode="output", view={"label": "Civil unrest",              "group": "Main coverage identifiers"}),
        "cvg_war":                  hx.Int(  mode="output", view={"label": "War",                       "group": "Main coverage identifiers"}),
        "cvg_loading":              hx.Int(  mode="output", view={"label": "Loading",                   "group": "Main coverage identifiers",       "format": thousands_format(4, True)}),
        "subcvg_terrorism":         hx.Int(  mode="output", view={"label": "Terrorism",                 "group": "Subcoverage identifiers"}),
        "subcvg_civil_unrest":      hx.Int(  mode="output", view={"label": "Civil unrest",              "group": "Subcoverage identifiers"}),
        "subcvg_war":               hx.Int(  mode="output", view={"label": "War",                       "group": "Subcoverage identifiers"}),
        "subcvg_loading":           hx.Int(  mode="output", view={"label": "Loading",                   "group": "Subcoverage identifiers",         "format": thousands_format(4, True)}),
        "ihs_average_default" :     hx.Float(mode="output", view={"label": "Average IHS Score Default",                                             "format": thousands_format(4, True)}),
        "ihs_average_selected":     hx.Float(mode="output", view={"label": "Average IHS Score Selected",                                            "format": thousands_format(4, True)}),
        "bi_cvg_nl_roe":            hx.Float(mode="output", view={"label": "BI Cover\nNon-Liability RoE", "group":        "Final RoEs",             "format": percent_format(4)}),
        "pd_cvg_nl_roe":            hx.Float(mode="output", view={"label": "PD Cover\nNon-Liability RoE", "group":        "Final RoEs",             "format": percent_format(4)}),
        "total_cvg_nl_roe":         hx.Float(mode="output", view={"label": "Total Cover\nNon-Liability RoE", "group":     "Final RoEs",             "format": percent_format(4)}),
        "bi_subcvg_nl_roe":         hx.Float(mode="output", view={"label": "BI Sub Cover\nNon-Liability RoE", "group":    "Final RoEs",             "format": percent_format(4)}),
        "pd_subcvg_nl_roe":         hx.Float(mode="output", view={"label": "PD Sub Cover\nNon-Liability RoE", "group":    "Final RoEs",             "format": percent_format(4)}),
        "total_subcvg_nl_roe":      hx.Float(mode="output", view={"label": "Total Sub Cover\nNon-Liability RoE", "group": "Final RoEs",             "format": percent_format(4)}),
        "cvg_multiplier":           hx.Float(mode="output", view={"label": "Cover",                     "group": "Multiplier",                      "format": percent_format(4)}),
        "subcvg_multiplier":        hx.Float(mode="output", view={"label": "Sub Cover",                 "group": "Multiplier",                      "format": percent_format(4)}),
        "nl_min_rol":               hx.Float(mode="output", view={"label": "Non Liability",             "group": "Min ROL",                         "format": percent_format(4)}),
        "liab_min_rol":             hx.Float(mode="output", view={"label": "Liability",                 "group": "Min ROL",                         "format": percent_format(4)}),
    }),

    # Expanded calcs (Exposure Curves)
    "trapped_exposure": hx.Float(mode="output", view={"label": "Trapped Exposure", "format": thousands_format(0)}),
    "limit_ded_difference": hx.Float(mode="output", view={"label": "Limit - Deductible", "format": thousands_format(0)}),
    "expo_limit_ratio": hx.Float(mode="output", view={"label": "Trapped Exposure / Limit", "format": thousands_format(2)}),
    "fx_to_usd": hx.Float(mode="output", view={"label": "FX to USD", "format": thousands_format(2)}),
    "curves": hx.List(mode="output", children={
        "index": hx.Int(mode="output"),
        "country_number": hx.Str(mode="output", view={"label": "Country\nNumber"}),
        "no_of_locations": hx.Int(mode="output", view={"label": "Number of\nLocations"}),
        "location_number": hx.Str(mode="output", view={"label": "Location\nNumber"}),
        "country": hx.Str(mode="output", view={"label": "Country"}),
        "pml": hx.Float(mode="output", view={"label": "PML /\nTop Location TIV", "format": thousands_format(4, True)}),
        "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
        "limit": hx.Float(mode="output", view={"label": "Limit", "format": thousands_format(4, True)}),
        "excess": hx.Float(mode="output", view={"label": "Excess", "format": thousands_format(4, True)}),
        "subcoverage": hx.Str(mode="output", view={"label": "Sub-coverage"}),
        "sublimit": hx.Float(mode="output", view={"label": "Sub-limit", "format": thousands_format(4, True)}),
        "deductible": hx.Float(mode="output", view={"label": "Deductible", "format": thousands_format(4, True)}),
        "total_sum_insured": hx.Float(mode="output", view={"label": "Total Sum Insured", "format": thousands_format(4, True)}),
        "bi_sum_insured": hx.Float(mode="output", view={"label": "BI Sum Insured", "format": thousands_format(4, True)}),
        "pd_sum_insured": hx.Float(mode="output", view={"label": "PD Sum Insured", "format": thousands_format(4, True)}),
        "selected_sum_insured": hx.Float(mode="output", view={"label": "Caculated TSI", "format": thousands_format(4, True)}),
        "band": hx.Str(mode="output", view={"label": "Band"}),
        "kth_smallest": hx.Int(mode="output", view={"label": "Kth Smallest"}),
        "decile": hx.Float(mode="output", view={"label": "Decile", "format": percent_format(0)}),
        "category": hx.Str(mode="output", view={"label": "Category"}),
        "no_in_category": hx.Float(mode="output", view={"label": "# in\ncategory"}),
        "si_unscaled": hx.Float(mode="output", view={"label": "Sum Insured -\nUnscaled", "format": thousands_format(0)}),
        "si_scaled": hx.Float(mode="output", view={"label": "Sum Insured -\nScaled", "format": thousands_format(0)}),
        "si_scaled_2": hx.Float(mode="output", view={"label": "Sum Insured -\nScaled Again", "format": thousands_format(0)}),
        "liability_risk": hx.Str(mode="output", view={"label": "Liability Risk"}),
        "attritional_risk": hx.Str(mode="output", view={"label": "Attritional\nRisk"}),
        "geog_risk": hx.Str(mode="output", view={"label": "Geog\nRisk"}),
        "location_cat_risk": hx.Str(mode="output", view={"label": "Location Cat\nRisk"}),
        "bi_cvg_nl_roe": hx.Float(mode="output", view={"label": "Cover", "group": "ROE - BI", "format": percent_format(4)}),
        "bi_subcvg_nl_roe": hx.Float(mode="output", view={"label": "Sub Cover", "group": "ROE - BI", "format": percent_format(4)}),
        "pd_cvg_nl_roe": hx.Float(mode="output", view={"label": "Cover", "group": "ROE - PD", "format": percent_format(4)}),
        "pd_subcvg_nl_roe": hx.Float(mode="output", view={"label": "Sub Cover", "group": "ROE - PD", "format": percent_format(4)}),
        "cvg_bi_rate_si": hx.Float(mode="output", view={"label": "BI - Rate x SI", "group": "Cover - Non-Liability", "format": thousands_format(0)}),
        "cvg_pd_rate_si": hx.Float(mode="output", view={"label": "PD - Rate x SI", "group": "Cover - Non-Liability", "format": thousands_format(0)}),
        "cvg_bi_mbbefd": hx.Float(mode="output", view={"label": "BI MBBEFD", "group": "Cover - Non-Liability", "format": thousands_format(4, True)}),
        "cvg_pd_mbbefd": hx.Float(mode="output", view={"label": "MBBEFD", "group": "Cover - Non-Liability", "format": thousands_format(4, True)}),
        "cvg_bi_base_premium": hx.Float(mode="output", view={"label": "BI - Base\nPremium", "info": " (SI * MBBEFD)", "group": "Cover - Non-Liability", "format": thousands_format(0)}),
        "cvg_pd_base_premium": hx.Float(mode="output", view={"label": "PD - Base\nPremium", "info": " (SI * MBBEFD)", "group": "Cover - Non-Liability", "format": thousands_format(0)}),
        "cvg_limit_usd": hx.Float(mode="output", view={"label": "Limit $", "group": "Cover - Liability", "format": thousands_format(0)}),
        "cvg_excess_usd": hx.Float(mode="output", view={"label": "Excess $", "group": "Cover - Liability", "format": thousands_format(0)}),
        "cvg_ilf_upper": hx.Float(mode="output", view={"label": "ILF\n(Limit + Excess)", "group": "Cover - Liability", "format": thousands_format(4, True)}),
        "cvg_ilf_lower": hx.Float(mode="output", view={"label": "ILF\n(Excess)", "group": "Cover - Liability", "format": thousands_format(4, True)}),
        "cvg_liab_base_premium": hx.Float(mode="output", view={"label": "Base Premium", "group": "Cover - Liability", "format": thousands_format(0)}),
        "subcvg_bi_rate_si": hx.Float(mode="output", view={"label": "BI - Rate x SI", "group": "Sub Cover - Non-Liability", "format": thousands_format(0)}),
        "subcvg_pd_rate_si": hx.Float(mode="output", view={"label": "PD - Rate x SI", "group": "Sub Cover - Non-Liability", "format": thousands_format(0)}),
        "subcvg_bi_mbbefd": hx.Float(mode="output", view={"label": "BI MBBEFD", "group": "Sub Cover - Non-Liability", "format": thousands_format(4, True)}),
        "subcvg_pd_mbbefd": hx.Float(mode="output", view={"label": "MBBEFD", "group": "Sub Cover - Non-Liability", "format": thousands_format(4, True)}),
        "subcvg_bi_base_premium": hx.Float(mode="output", view={"label": "BI - Base\nPremium", "info": " (SI * MBBEFD)", "group": "Sub Cover - Non-Liability", "format": thousands_format(0)}),
        "subcvg_pd_base_premium": hx.Float(mode="output", view={"label": "PD - Base\nPremium", "info": " (SI * MBBEFD)", "group": "Sub Cover - Non-Liability", "format": thousands_format(0)}),
        "subcvg_sublimit_usd": hx.Float(mode="output", view={"label": "Sub Limit $", "group": "Sub Cover - Liability", "format": thousands_format(0)}),
        "subcvg_ilf_upper": hx.Float(mode="output", view={"label": "ILF\n(Sub Limit + Excess)", "group": "Sub Cover - Liability", "format": thousands_format(4, True)}),
        "subcvg_liab_base_premium": hx.Float(mode="output", view={"label": "Base Premium", "group": "Sub Cover - Liability", "format": thousands_format(0)}),
        "trapped_exposure": hx.Float(mode="output", view={"label": "Trapped Exposure", "group": "Agg Discount", "format": thousands_format(0)}),
    }),

}

### --- COVERAGES --- ###
cover_selection_dict = {
    "cover_selection": hx.Structure(children={
        "are_fields_full": hx.Bool(mode="output"),
    }),
}

coverages_dict = {
    "property": {"label": "Total\nProperty"},
    "liability": {"label": "Liability"},
    "construction": {"label": "Construction"},
    "total": {"label": "Total @ 100%"}
}


# for cvg fields below be aware of the interplay with the cds - certain of these dictionary values need to be assigned (also) as part of the sch_rating_summary
cvg_fields_present = {
    "model_premium":                hx.Float(mode="output", view={"label": "Plan Premium",                                          "format": thousands_format()}),
    "benchmark_premium":            hx.Float(mode="output", view={"label": "Gross Benchmark Premium (100%)", "info": "Includes NMP adjustment",  "format": thousands_format()}),
    "quoted_premium":               hx.Float(mode="output", view={"label": "Offered Premium",                                       "format": thousands_format()}),
    "technical_premium":            hx.Float(mode="output", view={"label": "Gross Technical Premium (100%)",                                     "format": thousands_format()}),
    "technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Technical Premium (Pre-UW Adjustment)",                        "format": thousands_format()}),
    "tpi":                          hx.Float(mode="output", view={"label": "TPI",               "style_row": "hx-neutral",          "format": percent_format(1)}),
    "bpi":                          hx.Float(mode="output", view={"label": "BPI",               "style_row": "hx-neutral",          "format": percent_format(1)}),
    "tpi_pre_uw_adj":               hx.Float(mode="output", view={"label": "TPI (Pre-UW Adjustment)",                                      "format": percent_format(1)}),
    "bpi_pre_uw_adj":               hx.Float(mode="output", view={"label": "BPI (Pre-UW Adjustment)",                                      "format": percent_format(1)}),
    "benchmark_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Benchmark Premium (Pre-UW Adjustment)", "info":"Includes NMP adjustment","format": thousands_format()}), # removed from below and added here as part of new cds
}

cvg_fields_new = {
    "model_premium_pre_uw_adj":     hx.Float(mode="output", view={"label": "Plan Premium",                                          "format": thousands_format()}),
    "model_rol_pre_uw_adj":         hx.Float(mode="output", view={"label": "Plan Rate-on-Line",                                     "format": percent_format(2)}),
    "model_rol":                    hx.Float(mode="output", view={"label": "Plan Rate-on-Line",                                     "format": percent_format(2)}),
    "minimum_premium":              hx.Float(mode="output", view={"label": "Plan Premium (after minimums)",                         "format": thousands_format()}),
    "minimum_rol":                  hx.Float(mode="output", view={"label": "Plan Rate-on-Line (after minimums)",                    "format": percent_format(2)}),
    "quoted_rol":                   hx.Float(mode="output", view={"label": "Offered Rate-on-Line",                                  "format": percent_format(2)}),
    "quoted_roe":                   hx.Float(mode="output", view={"label": "Offered Rate-on-Exposure",  "style_row": "hx-neutral",  "format": percent_format(4)}),
    "expected_loss_ratio":          hx.Float(mode="output", view={"label": "Priced Loss Ratio - Gross Gross",                       "format": percent_format(1)}),
    # "benchmark_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Benchmark Premium",     "info":"Includes NMP adjustment","format": thousands_format()}), # removed from here and added above as part of new cds
    "expected_loss_ratio_pre_uw_adj":hx.Float(mode="output",view={"label": "Priced Loss Ratio - Gross Gross",                       "format": percent_format(1)}),
}

cvg_fields_combined = {
    **cvg_fields_present,
    **cvg_fields_new
}

totals_dict = {
    **cvg_fields_new,
    "policy_period": hx.Structure(view={"label": "Total @ 100%"}, children=cvg_fields_combined)
}
    
property_dict = {
    **cvg_fields_new,
    "bi": hx.Structure(view={"label": "BI\n(Incl. CBI)"},   children=cvg_fields_combined),
    "pd": hx.Structure(view={"label": "PD"},                children=cvg_fields_combined),

    "policy_period": hx.Structure(view={"label": "Total\nProperty"}, children={
        **cvg_fields_combined,
        "bi": hx.Structure(view={"label": "BI\n(Incl. CBI)"},   children=cvg_fields_combined),
        "pd": hx.Structure(view={"label": "PD"},                children=cvg_fields_combined),
    }),
}

liability_dict = {
    **cvg_fields_new,
    "policy_period": hx.Structure(view={"label": "Liability"},  children=cvg_fields_combined),
}

constr_premium_nodes = {
    "cvg_premium"               : hx.Float(mode="output", view={"label": "Premium\nCover",          "format": thousands_format(0)}),
    "subcvg_premium"            : hx.Float(mode="output", view={"label": "Premium\nSub Cover",      "format": thousands_format(0)}),
    "total_premium"             : hx.Float(mode="output", view={"label": "Premium\nTotal",          "format": thousands_format(0)}),
    "model_premium_pre_uw_adj"  : hx.Float(mode="output", view={"label": "Model\nPrice",            "format": thousands_format(0)}),
    "model_premium"             : hx.Float(mode="output", view={"label": "UW Adjusted\nPrice",      "format": thousands_format(0)}),
    "benchmark_premium"         : hx.Float(mode="output", view={"label": "Benchmark\nPrice",        "format": thousands_format(0)}),
    "model_premium_post_agg_adj": hx.Float(mode="output", view={"label": "Min Agg\nAdjusted Price", "format": thousands_format(0)}),
}

construction_dict = {
    **cvg_fields_new,
    "policy_period"  : hx.Structure(                                                        view={"label": "Construction"}, children=cvg_fields_combined),
    "is_covered"     : hx.Bool(     mode="input", default=False, async_input=["rarc_task"], view={"label": "Construction Cover"}),
    "days_difference": hx.Int(      mode="output",                                          view={"label": "Days Difference"}),
    "thirds"         : hx.List(     mode="output", children={
        "third"             : hx.Str(  mode="output", view={"label": "Third"}),
        "build_up"          : hx.Float(mode="output", view={"label": "Build Up %", "format": percent_format(1)}),
        "end_date"          : hx.Date( mode="output", view={"label": "End Date"}),
    }),
    "are_years_horizontal"  : hx.Bool(mode="input", default=False, view={"label": "Transpose Table Below"}),
    "are_years_vertical"    : hx.Bool(mode="output"),
    "years": hx.List(mode="input", default_element_count=5, children={
        "year"                  : hx.Str(  mode="output", view={"label": "Construction\nYear"}),
        "end_date"              : hx.Date( mode="output", view={"label": "Year End\nDate"}),
        "build_up_calculated"   : hx.Float(mode="output", view={"label": "Build Up %\nProposed", "format": percent_format(1)}),
        "build_up_override"     : hx.Float(mode="input",  view={"label": "Build Up %\nOverride", "format": percent_format(1)}, validation={"min_value": 0, "max_value": 1}, async_input=["rarc_task"], default=None, optionality="optional"),
        "build_up_selected"     : hx.Float(mode="output", view={"label": "Build Up %\nSelected", "format": percent_format(1)}),
        "sum_insured"           : hx.Float(mode="output", view={"label": "Sum Insured\nIn Year", "format": thousands_format(0)}),
        "total_cvg_nl_roe"      : hx.Float(mode="output", view={"label": "ROE\nCover", "format": percent_format(4)}),
        "total_subcvg_nl_roe"   : hx.Float(mode="output", view={"label": "ROE\nSub Cover", "format": percent_format(4)}),
        "cvg_expo_curve"        : hx.Float(mode="output", view={"label": "Exposure %\nCover", "format": percent_format(2)}),
        "subcvg_expo_curve"     : hx.Float(mode="output", view={"label": "Exposure %\nSub Cover", "format": percent_format(2)}),
        **constr_premium_nodes
    }),
    "years_total": hx.Structure(view={"label": "Total Premium"}, children=constr_premium_nodes),
    "years_annual": hx.Structure(view={"label": "Annual Premium"}, children=constr_premium_nodes),
}

# Using the following dictionary as a subset of the data schema that is accessible in rating
all_coverages_dict = {
    "property": property_dict,
    "liability": liability_dict,
    "construction": construction_dict,
    "total": totals_dict
}

### --- LAYERS --- ###
default_levels = ["Default", "Low Risk", "High Risk"]
risks = {
    "security"           : default_levels,
    "industry"           : default_levels,
    "policy"             : default_levels,
    "ihs_score"          : ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"],
    "ihs_score_read_only": ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"],
    "ihs_score_expiring" : ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"]
}

risks_labels = {
    "security"           : "Security",
    "industry"           : "Industry",
    "policy"             : "Policy",
    "ihs_score"          : "IHS Score",
    "ihs_score_read_only": "IHS Score",
    "ihs_score_expiring" : "IHS Score (expiring policy)"
}

authorities = {
    "nb_gross_line": hx.Float(mode="output", view={"label": "New Business Gross Line Cost", "format": thousands_format()}),
    "nb_net_premium": hx.Float(mode="output", view={"label": "New Business Beazley Net Premium", "format": thousands_format()}),
    "ren_gross_line": hx.Float(mode="output", view={"label": "Renewals Gross Line Cost", "format": thousands_format()}),
    "ren_net_premium": hx.Float(mode="output", view={"label": "Renewals Beazley Net Premium", "format": thousands_format()}),
    "term": hx.Float(mode="output", view={"label": "Term (months)", "format": thousands_format(1, True)})
}

def ihs_score_info(k):
    text = "For risks created in this model (not migrated):\n * This is a simple factor to summarise the overall IHS Score.\n * It considers the maximum peril contribution for each country.\n * It is comparable to the calculation on expiring periods below.\n * In many places the change in the IHS Score is a useful guide, but it does NOT directly affect the UW IHS Adjustment."
    return {"info" : text} if k == "ihs_score_read_only" else {}

uw_ihs_adj_info = "For risks created in this model (not migrated):\n * This is the overall exposure weighted ROE.\n * The ROE is calculated for each country as max of peril equivalent.\n * The input IHS factors default/overridden are at this granular level.\n * In many places the change in the IHS Score is a useful guide, but it does NOT directly affect the UW IHS Adjustment."

layers_dict = {
    "quoted_premium_case_priced": hx.Float(mode="output", view={"label": "Gross Quoted Premium", "format": thousands_format()}),
    "written_line_basis": hx.Str(mode="input", default="Of Order", options=["Of Order", "Of Whole"], view={"label": "Written Line Basis"}),
    "order": hx.Float(mode="input", default=1, validation={"min_value": 0, "max_value": 1}, view={"label": "Order", "format": percent_format(1)}),
    "line": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Line (Currency)", "format": thousands_format()}),
    "quoted_rol": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross Quoted ROL", "format": percent_format(2)}, async_output=["start_renewal_task"] ),
    "expected_loss_cost_annualised": hx.Float(mode="output", view={"label": "Expected Loss Cost", "format": thousands_format()}),
    "expected_loss_cost_pre_uw_adj_annualised": hx.Float(mode="output", view={"label": "Expected Loss Cost (Pre-UW Adjustment)", "format": thousands_format()}),
    "yellow_legend": hx.Str(mode="input", default="Pre UW Adjustments", view={"read_only": True, "style_cell": "hx-neutral"}),
    "green_legend": hx.Str(mode="input", default="Post UW Adjustments", view={"read_only": True, "style_cell": "hx-good"}),
    "risk_adjustments": hx.Structure(children={
        **{
            k: hx.Structure(view={"label": risks_labels[k], **ihs_score_info(k)}, children={
                "level":        hx.Str(  **({"mode":"input",  "default_index":0, "options":v}           if k not in {"ihs_score_read_only","ihs_score_expiring","ihs_score"} else {"mode":"output"})
                                        ,view={"label": "Risk\nLevel"}
                                        ,async_input=["rarc_task"]),
                "description":  hx.Str(  mode="output",                                                         view={"label": "Description",}),
                "min":          hx.Float(mode="output",                                                         view={"label": "Min", "format": thousands_format(3, True)}),
                "max":          hx.Float(mode="output",                                                         view={"label": "Max", "format": thousands_format(3, True)}),
                "override":     hx.Float(**({"mode":"input","default":None, "optionality":"optional"}   if k not in {"ihs_score_read_only","ihs_score_expiring"} else {"mode":"output"})
                                        ,**({"options_data": "../scores", "options_field": "score"}     if k not in {"ihs_score_read_only","ihs_score_expiring","ihs_score"} else {})
                                        ,async_input=["rarc_task"]
                                        ,**({"async_output" : ["start_renewal_task"]}                   if k == "ihs_score"                                         else {})
                                        ,view={  "label"    : "Override\nScore"
                                                , "format"  : thousands_format(3, True)
                                                , "options" : {"red": {"style_cell": "hx-bad"}}}),

                "is_override_valid":    hx.Bool(mode="output"),
                "is_override_invalid":  hx.Bool(mode="output"),
                "calculated":           hx.Float(mode="output"
                                                ,view={"label": "Calculated\nScore", "format": thousands_format(3, True)}
                                                ,**({"async_output" : ["start_renewal_task"]}           if k == "ihs_score_expiring"                                         else {})),
                "selected":             hx.Float(mode="output"
                                                ,view={"label": "Selected\nScore", "format": thousands_format(3, True)}
                                                ,**({"async_output" : ["start_renewal_task"]}           if k == "ihs_score_expiring"                                         else {})),
                "scores":               hx.List(mode="output", children={
                                                                            "score": hx.Int(mode="output")}),
                "roe_calculated":       hx.Float(mode="output",                                     view={"label": "ROE (Calculated)",  "format": percent_format(4)}),
                "roe_selected":         hx.Float(mode="output",                                     view={"label": "ROE (Selected)",    "format": percent_format(4)}),
                "uw_rationale":         hx.Str(mode="input", default=None, optionality="optional",  view={"label": "Comment"}),
            })
            for k, v in risks.items()
        },
        "total_adj_score":      hx.Int(  mode="output", view={"label": "Total Adjustment Score"}),
        "uw_multiplier":        hx.Float(mode="output", view={"label": "Underwriter Multiplier", "format": percent_format(1)}),
        "uw_ihs_adjustment":    hx.Float(mode="output", view={"label": "Underwriter IHS Adjustment", "format": percent_format(1),"info":uw_ihs_adj_info}),
        "uw_general_comments":  hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "General Comments"}),
        "uw_rationale":         hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Comment"}), # For all scores, to replace individual uw_rationale boxes.
        
    }),
    "uw_authorities": hx.Structure(children={
        "authority": hx.Structure(view={"label": "Authority"}, children=authorities),
        "policy": hx.Structure(view={"label": "Policy"}, children=authorities),
        "warning": hx.Structure(view={"label": "Warning"}, children={auth: hx.Str(mode="output") for auth in authorities.keys()}),
    }),
    "uw_authorities_current_currency": hx.Structure(children={
        "authority": hx.Structure(view={"label": "Authority"}, children=authorities),
        "policy": hx.Structure(view={"label": "Policy"}, children=authorities),
        "warning": hx.Structure(view={"label": "Warning"}, children={auth: hx.Str(mode="output") for auth in authorities.keys()}),
    }),
}