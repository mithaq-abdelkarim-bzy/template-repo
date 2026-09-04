import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task": hx.Bool(mode="output", async_output=["start_renewal_task"]),
            "show_landing_page": hx.Bool(mode="output"),
            "show_after_landing_page": hx.Bool(mode="output"),
            "show_rate_change": hx.Bool(mode="output"),
            "landing_page_info": hx.Str(
                mode="input", 
                default="Click 'Import Expiring Policy Data' in the top right corner then click 'Start Policy'",
                async_output=["start_renewal_task"],
                view={"read_only":True}
            ),
            "expiring_policy_option_id": hx.Int(mode="input", default=None, optionality="optional", async_output=["start_renewal_task", "sync_expiring_ids"]),
        }),

        "messages": hx.Structure(children={
            "crime_website": hx.Str(mode="output"),
            "policy_info_note": hx.Str(mode="output"),
            "experience_rating_note": hx.Str(mode="output"),
            "fetch_bi_task_status": hx.Str(mode="output", async_output=["sql_bi_fetch_task", "sql_bi_clear","backfill_exposure"]),
            "epi_heading": hx.Str(mode="output"),
            "rating_summary_note": hx.Str(mode="output"),
            "min_premium_note": hx.Str(mode="output", view={"label": " "}),
        }),
               
        "flags": hx.Structure(children={
            "deductible_flag": hx.Bool(mode="output"),
            "excess_flag": hx.Bool(mode="output"),
            "er_source_bi": hx.Bool(mode="output"),
            "er_source_user": hx.Bool(mode="output"),
            "er_cat_yes": hx.Bool(mode="output"),
            "er_cat_no": hx.Bool(mode="output"),
            "er_experience_data": hx.Bool(mode="output"),
            "er_experience_data_no": hx.Bool(mode="output"),
            "er_actual_incurred": hx.Bool(mode="output"),
            "er_actual_incurred_no": hx.Bool(mode="output"),
            "show_bi_claims": hx.Bool(mode="input", default=False, view={"label": "Reveal Underlying BI Data"}),
            "extensions_comment_flag": hx.Bool(mode="output"),
            "validation_count": hx.Float(mode="output"),
        }),
        
        "subsector_rates_display": hx.List(mode="output", children={
            "Sector": hx.Str(mode="output", view={"label": "Sector"}),
            "SubSector": hx.Str(mode="output", view={"label": "SubSector"}),
            "BaseRate": hx.Float(mode="output", view={"label": "Base Rate\n(Freq Per Est.)", "format": percent_format(4)}),
            "Relativity": hx.Float(mode="output", view={"label": "Relativity Within\nSector", "format": integer_format(4)}),
        }),
        
        "city_rates_display": hx.List(mode="output", children={
            "State": hx.Str(mode="output", view={"label": "State"}),
            "City": hx.Str(mode="output", view={"label": "City"}),
            "Population": hx.Float(mode="output", view={"label": "Population", "format": thousands_format(0)}),
            "ViolentCrime": hx.Float(mode="output", view={"label": "Violent\nCrime", "format": thousands_format(0)}),
            "VCRate": hx.Float(mode="output", view={"label": "VC Rate", "format": percent_format(2)}),
            "Relativity": hx.Float(mode="output", view={"label": "Relativity", "format": integer_format(4)}),
            "CityRisk": hx.Str(mode="output", view={"label": "City\nRisk"}),
        }),
        
        "bug_report_email": hx.Str(mode="output"),

        "policy_doc": hx.Structure(children={
            "data_dict": hx.Str(mode="output", async_input=["policy_to_excel_task"]),
            "output_file": hx.File(mode="output", async_output=["policy_to_excel_task"], file_name="Policy_Summary.xlsx"),
            "task_data_dict": hx.Str(mode="output", async_output=["policy_to_excel_task"]),
            "show_generate_button": hx.Bool(mode="output"),
            "show_download": hx.Bool(mode="output"),
            "premium_check": hx.Str(mode="output"),
            "show_premium_check": hx.Bool(mode="output"),
        }),

    }