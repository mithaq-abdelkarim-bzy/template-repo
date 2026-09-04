import hx_data_schema as hx
from data_schema.utilities import thousands_format, percent_format, merge_dicts, run_schedule_rater_async_tasks
from data_schema.dropdown_list import cyber_cover_list

MAX_OPTIONS = 3


def non_layer_perils():
    '''
    Data schema for perils related input (but not layers related)
    '''
    return {
        "non_layer_perils": hx.Structure(children={
            "fire": hx.Structure(children={
                "show_section": hx.Bool(mode="output"),
                **intl_deductibles(),
                **machinery_breakdown(),
                **occupancy_guide(),
            }),
            "named_windstorm": hx.Structure(children={
                "num_options": hx.Int(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["named_storm_ws_task", "all_tier_fl_ws_task", "fl_ws_task", "tx_ws_task", "tier_fl_ws_task", "all_wind_ws_scs_task", "clear_deductibles_task"], options=[index for index in range(1, MAX_OPTIONS + 1)], view={"label": "Options"}),
                **{f"show_option_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                "show_section": hx.Bool(mode="output"),
                **{f"show_state_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_tier_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_percent_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_location_min_max_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **intl_deductibles(),
            }),
            "scs": hx.Structure(children={
                "num_options": hx.Int(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["all_wind_ws_scs_task", "clear_deductibles_task"], options=[index for index in range(1, MAX_OPTIONS + 1)], view={"label": "Options"}),
                **{f"show_option_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                "show_section": hx.Bool(mode="output"),
                **{f"show_state_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_tier_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_percent_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_location_min_max_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **intl_deductibles(),
            }),
            "flood": hx.Structure(children={
                "num_options": hx.Int(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["clear_deductibles_task"], options=[index for index in range(1, MAX_OPTIONS + 1)], view={"label": "Options"}),
                **{f"show_option_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                "show_section": hx.Bool(mode="output"),
                **{f"show_state_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_tier_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_percent_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_location_min_max_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **intl_deductibles(),
            }),
            "quake": hx.Structure(children={
                "num_options": hx.Int(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["ca_eq_task", "all_ca_eq_task", "clear_deductibles_task"], options=[index for index in range(1, MAX_OPTIONS + 1)], view={"label": "Options"}),
                **{f"show_option_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                "show_section": hx.Bool(mode="output"),
                **{f"show_state_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_tier_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_percent_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **{f"show_location_min_max_{i}": hx.Bool(mode="output") for i in range(1, MAX_OPTIONS + 1)},
                **intl_deductibles(),
            }),
            "wildfire": hx.Structure(children={
                "show_section": hx.Bool(mode="output"),
                **intl_deductibles(),
            }),
            "hail": hx.Structure(children={
                "show_section": hx.Bool(mode="output"),
            }),
            "tornado": hx.Structure(children={
                "show_section": hx.Bool(mode="output"),
            }),
            "equipment_breakdown": hx.Structure(children={
                "show_section": hx.Bool(mode="output"),
                # Equipment Breakdown details
                "industry": hx.Str(mode="override", optionality="optional", async_output=run_schedule_rater_async_tasks(async_input = False), options_data="../industry_dropdown", options_field="industry", view={"label": "Industry"}),
                "occupancy": hx.Str(mode="override", optionality="optional", async_output=run_schedule_rater_async_tasks(async_input = False), options_data="../occupancy_dropdown", options_field="occupancy", view={"label": "Occupancy"}),
                "industry_dropdown": hx.List(mode="output", children={
                    "industry": hx.Str(mode="output", view={"label": "Industry"})
                }),
                "occupancy_dropdown": hx.List(mode="output", children={
                    "occupancy": hx.Str(mode="output", view={"label": "Occupancy"})
                }),
                "deductible": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Deductible", "format": thousands_format()}),
                "referral": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Referral?", "read_only": True}),
                "travelers": hx.Bool(mode="input", default=False, view={"label": "Travelers"}),
                # Coverage Extensions
                **coverage_extensions("perishable_goods", "Perishable Goods"),
                **coverage_extensions("expediting_expense", "Expediting Expense"),
                **coverage_extensions("pollution", "Pollution Cleanup and Removal"),
                **coverage_extensions("data_media", "Data Media"),
                **coverage_extensions("demolition", "Demolition and Increased cost of Construction"),
                **coverage_extensions("water_damage", "Water Damage"),
            }),
            "tria": hx.Structure(children={
                "show_section": hx.Bool(mode="output"),
            }),
            "cyber": hx.Structure(children={
                "show_section": hx.Bool(mode="output"),
                "cyber_coverage_note": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Coverage Note"}),
                "info_note": hx.Str(mode="output")
            }),
            "cyber_cover": hx.Structure(children={
                "cyber": cyber_cover_structure("Cyber"),
                "special_perils": cyber_cover_structure("Special Perils", clause=False),
                "contingent_direct": cyber_cover_structure("Contingent Time Element Direct", clause=False),
                "contingent_indirect": cyber_cover_structure("Contingent Time Element Indirect", clause=False),
                "green_coverage": cyber_cover_structure("Green Coverage Capture", clause=False),
                "option_1": cyber_cover_structure("Option 1"),
                "option_2": cyber_cover_structure("Option 2"),
                "option_3": cyber_cover_structure("Option 3"),
            }),
            "uw_adjustments": hx.Structure(children={
                "risk_man": hx.Structure(children=underwriter_adjustments(), view={"label": "Risk Man"}),
                "experience": hx.Structure(children=underwriter_adjustments(), view={"label": "Experience"}),
                "valuation": hx.Structure(children=underwriter_adjustments(), view={"label": "Valuation"}),
                "other": hx.Structure(children=underwriter_adjustments(), view={"label": "Other"}),
                "total": hx.Structure(children=underwriter_adjustments(mode="output"), view={"label": "Total"}),
            })
        })
    }

# Note cyber covers section was removed from view.
def cyber_cover_structure(label, clause=True):
    '''
    Cyber Cover Structure data schema
    Parameters:
        label (str): label of the coverage extension shown in the view
        clause (bool): if clause is used at the column
    '''
    children = {
        "covered": hx.Bool(mode="input", default=False, view={"label": "Covered"}),
        "sublimit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Sublimit", "format": thousands_format()}),
        "notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Notes"})
    }
    if clause:
        children["clause"] = hx.Str(mode="input", options=cyber_cover_list, default_index=0, view={"label": "Clause"})

    return hx.Structure(view={"label": label}, children=children)

def coverage_extensions(name, label):
    '''
    Equipment Breakdown - Coverage Extensions data schema
    Parameters:
        name (str): name of the coverage extension referenced in data schema
        label (str): label of the coverage extension shown in the view
    '''
    return {
        name: hx.Structure(view={"label": label}, children={
            "covered": hx.Bool(mode="input", default=True, async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Covered"}),
            "pd_sublimit": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True), options_table="eb_sublimits", options_column="PD Sublimits", default="25,000", optionality="optional", view={"label": "PD Sublimit"})
        })
    }


def underwriter_adjustments(mode="input"):
    '''
    Summary - Underwriter adjustments
    '''
    
    return {
        "fire": hx.Float(mode=mode, default=(0 if mode=="input" else hx.UNDEFINED), async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Fire", "format": {"output": "percent", "mantissa": 0}, "options": {"validation": {"style_cell": "strong-validation"}}}),
        "named_windstorm": hx.Float(mode=mode, default=(0 if mode=="input" else hx.UNDEFINED), async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl Windstorm", "format": {"output": "percent", "mantissa": 0}, "options": {"validation": {"style_cell": "strong-validation"}}}),
        "scs": hx.Float(mode=mode, default=(0 if mode=="input" else hx.UNDEFINED), async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "SCS", "format": {"output": "percent", "mantissa": 0}, "options": {"validation": {"style_cell": "strong-validation"}}}),
        "flood": hx.Float(mode=mode, default=(0 if mode=="input" else hx.UNDEFINED), async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Flood", "format": {"output": "percent", "mantissa": 0}, "options": {"validation": {"style_cell": "strong-validation"}}}),
        "quake": hx.Float(mode=mode, default=(0 if mode=="input" else hx.UNDEFINED), async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl Quake", "format": {"output": "percent", "mantissa": 0}, "options": {"validation": {"style_cell": "strong-validation"}}}),
        "wildfire": hx.Float(mode=mode, default=(0 if mode=="input" else hx.UNDEFINED), async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Wildfire", "format": {"output": "percent", "mantissa": 0}, "options": {"validation": {"style_cell": "strong-validation"}}}),
        "hail": hx.Float(mode=mode, default=(0 if mode=="input" else hx.UNDEFINED), async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Hail", "format": {"output": "percent", "mantissa": 0}, "options": {"validation": {"style_cell": "strong-validation"}}}),
        "tornado": hx.Float(mode=mode, default=(0 if mode=="input" else hx.UNDEFINED), async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Tornado", "format": {"output": "percent", "mantissa": 0}, "options": {"validation": {"style_cell": "strong-validation"}}}),        
    }


def conditional_formatting_options():
    return {"validation": {"style_cell": "strong-validation"}}


def intl_deductibles():
    return {
        "intl_ded": hx.List(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True)+["run_simulation_task"], async_output=[{"task": "fill_intl_ded_countries_task", "reset": False}, {"task": "copy_intl_ded_perils_task", "reset": False}], children={
            "country": hx.Str(mode="input", default="", view={"label": "Country", "format": thousands_format()}, async_input=run_schedule_rater_async_tasks(async_input = True)+["run_simulation_task"], async_output=[{"task": "fill_intl_ded_countries_task", "reset": False}, {"task": "copy_intl_ded_perils_task", "reset": False}]),
            "tiv": hx.Float(mode="input", optionality="optional", default=None, view={"label": "Total TIV", "read_only": True, "format": thousands_format()}, async_input=run_schedule_rater_async_tasks(async_input = True)+["run_simulation_task"], async_output=[{"task": "fill_intl_ded_countries_task", "reset": False}, {"task": "copy_intl_ded_perils_task", "reset": False}]),
            "perc_of_tiv": hx.Float(mode="input", optionality="optional", default=None, view={"label": "Deductible as\n% of TIV", "format": percent_format()}, async_input=run_schedule_rater_async_tasks(async_input = True)+["run_simulation_task"], async_output=[{"task": "fill_intl_ded_countries_task", "reset": False}, {"task": "copy_intl_ded_perils_task", "reset": False}]),
            "fixed_min": hx.Float(mode="input", optionality="optional", default=None, view={"label": "Base /\nMinimum Deductible (USD)", "format": thousands_format()}, async_input=run_schedule_rater_async_tasks(async_input = True)+["run_simulation_task"], async_output=[{"task": "fill_intl_ded_countries_task", "reset": False}, {"task": "copy_intl_ded_perils_task", "reset": False}]),
            "fixed_max": hx.Float(mode="input", optionality="optional", default=None, view={"label": "Maximum\nDeductible (USD)", "format": thousands_format()}, async_input=run_schedule_rater_async_tasks(async_input = True)+["run_simulation_task"], async_output=[{"task": "fill_intl_ded_countries_task", "reset": False}, {"task": "copy_intl_ded_perils_task", "reset": False}]),
            "country_sublimit": hx.Float(mode="input", optionality="optional", default=None, view={"label": "Sublimit (USD)", "format": thousands_format()}, async_input=run_schedule_rater_async_tasks(async_input = True)+["run_simulation_task"], async_output=[{"task": "fill_intl_ded_countries_task", "reset": False}, {"task": "copy_intl_ded_perils_task", "reset": False}]),
        })
    }

def machinery_breakdown():
    return {
        "machinery_breakdown": hx.List(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=[{"task": "machinery_breakdown_industry_task", "reset": False}], children={
            "industry": hx.Str(mode="input", default="", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=[{"task": "machinery_breakdown_industry_task", "reset": False}], view={"label": "Industry", "read_only": True}),
            "tiv_contents": hx.Float(mode="input", default=0, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=[{"task": "machinery_breakdown_industry_task", "reset": False}], view={"label": "Contents + BI\nTIV", "format": thousands_format(0), "read_only": True}),
            "fire_mb_proportion": hx.Float(mode="input", default=0, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=[{"task": "machinery_breakdown_industry_task", "reset": False}],view={"label": "Machinery\nBreakdown %", "format": percent_format(0)}),
        }),
        "machinery_breakdown_message": hx.Str(mode="input", optionality="optional", default=None, async_output=[{"task": "machinery_breakdown_industry_task", "reset": False}], view={"read_only": True}),
        "machinery_breakdown_sublimit": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Machinery Breakdown Sublimit", "format": thousands_format(0)})
    }

def occupancy_guide():
    return {
        "occupancy_guide": hx.Structure(children={
            "industry_occupancy_dropdown": hx.Structure(linked_default_index=0, linked_options_columns=["Industry", "Occupancy"], linked_options_table="non_cat_base_rates_live_dropdown", view={"linked_options_selector": "flat"}, children={
                "industry": hx.Str(mode="input", async_input=["fire_occupancy_guide_task"], view={"label": "Industry"}),
                "occupancy": hx.Str(mode="input", async_input=["fire_occupancy_guide_task"], view={"label": "Occupancy"}),
            }),
            "occupancy_description": hx.Str(mode="output", view={"label": "Occupancy Description"})
        })
    }