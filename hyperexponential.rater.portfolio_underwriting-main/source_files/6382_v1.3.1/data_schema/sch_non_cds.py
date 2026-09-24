import hx_data_schema as hx
from algorithms import rate_constants as constants


def generate_years_headers_list(start: int, end: int):
    return [f"year_{year}" for year in range(start, end + 1)]


def sch_non_cds_controllers():
    num_refs= constants.NUMBER_SECTION_REFERENCES
    return {
        "global_fields":hx.Structure(
            children={
                "is_there_global_message":hx.Bool(mode="output", async_input=["generate_word_document_task"]),
                "is_projections_msg_shown":hx.Bool(mode="output"),
                "projections_error_msg": hx.Str(mode="output", view={"label":"Projections Errors:", "options":{"warning":{"style_cell":"strong-validation"}}}),
                "is_lobs_msg_shown":hx.Bool(mode="output"),
                "lobs_error_msg": hx.Str(mode="output", view={"label":" ", "options":{"warning":{"style_cell":"strong-validation"}}}),
                "is_pc_msg_shown":hx.Bool(mode="output"),
                "pc_error_msg": hx.Str(mode="output", view={"label":"PC Errors:", "options":{"warning":{"style_cell":"strong-validation"}}}),
                "is_oe_msg_shown": hx.Bool(mode="output"),
                "oe_error_msg": hx.Str(mode="output", view={"label": "Claims Data Errors:", "options": {"warning": {"style_cell": "strong-validation"}}}),
                "proj_status_msg": hx.Str(mode="output", view={"label":"Projections Task Status"}, async_output=[]),
                "is_proj_msg_shown": hx.Bool(mode="output", async_output=[]),
                "mismatched_lob_table_length": hx.Bool(mode="output"),
                "required_sel_lob_table_length": hx.Int(mode="output", async_input=["sync_lob_lists_task"]),
                "required_fac_lob_table_length": hx.Int(mode="output", async_input=["sync_lob_lists_task"]),
                "required_riskcode_table_length": hx.Int(mode="output", async_input=["sync_lob_lists_task"]),
                "mismatched_lob_error_msg_global": hx.Str(mode="input", default="LOB List Lengths have changed. Please re-run 'Sync Lob Lists' on the Risk Code Composition tab", view={"label": "LOB Sync Error:", "options": {"warning": {"style_cell": "strong-validation", "read_only": True}}}),
                "mismatched_lob_error_msg": hx.Str(mode="input", default="LOB List Lengths have changed. Please re-run 'Sync Lob Lists' to continue  --->", view={"label": "LOB Sync Error:", "options": {"warning": {"style_cell": "strong-validation", "read_only": True}}})

            }
        ),
        
        # Policy document download
        "excel_analysis": hx.Structure(children={
            "output_file":          hx.File(mode="output", async_output=["generate_excel_document_task"], file_name="analysis_overview.xlsx"), 
            "data_dict":            hx.Str( mode="output", async_input =["generate_excel_document_task"] ),
            "task_data_dict":       hx.Str( mode="output", async_output=["generate_excel_document_task"]),
            "projection_complete":  hx.Bool(mode="input", default=False, optionality="required", view={"label":"Checking this box marks the analysis as complete and ready for excel export"} ),
            "show_download":        hx.Bool(mode="output"),
            "premium_check":        hx.Str( mode="output"),
            "show_premium_check":   hx.Bool(mode="output"),
        }),
        
        "risk_information": hx.Structure(
            children={
                "not_follow_main_syndicate": hx.Bool(mode="output"),
                "expiring_id_not_available": hx.Bool(mode="output"),
                "insured_data_date_ref": hx.Date(mode="output", async_output=[]),
                "inception_date_ref": hx.Date(mode="output", async_output=[]),
                "cat_modelling_available": hx.Bool(mode="output"),
                "not_large_model_mode": hx.Bool(mode="output"),
                "is_actuarial": hx.Bool(mode="output"),
                "is_underwriter": hx.Bool(mode="output")
            }
        ),
        "policy_level_data": hx.Structure(
            children={
                "is_shown": hx.Bool(mode="output"),
                "duplicate_found": hx.Bool(mode="output", async_input=["import_policy_data_from_csv_task"]),
                "policy_level_data_df_str": hx.Str(mode="output", async_output=["write_policy_claim_data_to_hxd_task"])
            }
        ),
        "claim_level_data": hx.Structure(
            children={
                "is_shown": hx.Bool(mode="output"),
                "duplicate_found": hx.Bool(mode="output", async_input=["import_claim_data_from_csv_task"]),
                "claim_level_data_df_str": hx.Str(mode="output", async_output=["write_policy_claim_data_to_hxd_task"])
            }
        ),
        "risk_code_composition": hx.Structure(
            children={
                "is_manual": hx.Bool(mode="output"),
                "is_data": hx.Bool(mode="output"),
                "is_manual_and_prem_data_available_true": hx.Bool(mode="output"),
                "amount": hx.Str(mode="input", default="Amount"),
                ** {year: hx.Str(mode="output") for year in generate_years_headers_list(0, constants.YEARS_TO_CONSIDER_IN_RISK_CODE_COMPOSITION)},
                "final_composition": hx.List(mode="output", children={  "risk_code":            hx.Str(  mode="output"),
                                                                        "composition":          hx.Float(mode="output"),
                                                                        "modelled":             hx.Bool( mode="output"),
                                                                        "facility_lob":         hx.Str(  mode="output"),
                                                                        "selected_lob":         hx.Str(  mode="output"),
                                                                        "selected_bp_class":    hx.Str(  mode="output"),
                                                                        "selected_trifocus":    hx.Str(  mode="output"),
                                                                        "risk_code_description":hx.Str(  mode="output")       }),
                "final_composition_str": hx.Str(mode="output", async_input=[ "generate_word_document_task", "generate_excel_document_task"]),
                "final_composition_str_ref": hx.Str(mode="output", async_output=[])
            }
        ),
        "assumed_deductions": hx.Structure(children={
                ** {year: hx.Str(mode="output") for year in generate_years_headers_list(0, constants.YEARS_TO_CONSIDER_IN_RISK_CODE_COMPOSITION)},
                "is_manual": hx.Bool(mode="output"),
                "final_deductions":hx.List(mode="output",children={ "selected_lob":                 hx.Str(  mode="output"),
                                                                    "market_deductions":            hx.Float(mode="output"),
                                                                    "mga_fee":                      hx.Float(mode="output"),
                                                                    "facility_brokerage":           hx.Float(mode="output"),
                                                                    "leaders_fee":                  hx.Float(mode="output"),
                                                                    "service_fee":                  hx.Float(mode="output"),
                                                                    "other":                        hx.Float(mode="output"),
                                                                    "selected_effective_deductions":hx.Float(mode="output"),
                                                                    "total_fees":                   hx.Float(mode="output"),
                                                                    "is_row_visible":               hx.Float(mode="output"),                        }),
                "final_deductions_str": hx.Str(mode="output", async_input=[ "generate_word_document_task", "generate_excel_document_task"]),
                "final_deductions_str_ref": hx.Str(mode="output", async_output=[])
            }
        ),
        'rate_change': hx.Structure(children={  **{year: hx.Structure(children={'facility': hx.Str(mode='output')}) for year in generate_years_headers_list(0, constants.YEARS_TO_CONSIDER_IN_RATE_CHANGE-1)},
                                                "rate_change_str":      hx.Str(mode="output", async_input=[]),
                                                "rate_change_str_ref":  hx.Str(mode="output", async_output=[])}),
        'inflation':    hx.Structure(children={ "is_shown": hx.Bool(mode="output"),
                                                **{year: hx.Str(mode='output') for year in generate_years_headers_list(0, 25)},
                                                "inflation_summary_str": hx.Str(mode="output", async_input=[])}),   
        'base_inf':     hx.Structure(children={ **{year: hx.Str(mode='output') for year in generate_years_headers_list(0, 25)}}),
        'excess_inf':   hx.Structure(children={ **{year: hx.Str(mode='output') for year in generate_years_headers_list(0, 25)}}),
        'portfolio_profile': hx.Structure(children={
                "is_shown": hx.Bool(mode="output"),
                "rate_change_with_selection_override":  hx.Structure(children={**{year: hx.Str(mode='output') for year in generate_years_headers_list(0, 25)}}),
                "rate_change_no_override":              hx.Structure(children={**{year: hx.Str(mode='output') for year in generate_years_headers_list(0, 25)}}),
                "lloyds_incurred_development":          hx.Structure(children={**{year: hx.Str(mode='output') for year in generate_years_headers_list(0, 25)}}),
                "lloyds_paid_development":              hx.Structure(children={**{year: hx.Str(mode='output') for year in generate_years_headers_list(0, 25)}}),
                "lloyds_premium_development":           hx.Structure(children={**{year: hx.Str(mode='output') for year in generate_years_headers_list(0, 25)}}),        }),

        'own_experience': hx.Structure(children={   "is_shown":             hx.Bool(mode="output", async_output=[]),
                                                    "is_error_msg_shown":   hx.Bool(mode="output", async_output=[], async_input=[])}),
        'lloyds_projections':   hx.Structure(children={"is_shown":          hx.Bool(mode="output"                   )}),
        "beazley_data":         hx.Structure(children={"beazley_data_str":  hx.Str( mode="output", async_input=[]   )}),
        "bp_projections":       hx.Structure(children={"is_shown":          hx.Bool(mode="output"                   )}),
        'beazley_projections':  hx.Structure(children={
                "is_shown": hx.Bool(mode="output"),
                'year_dev_of_beazley_data': hx.Structure(children={ 'lastest_lloyds_year':          hx.Int( mode='output',  async_output=[]),
                                                                    'lastest_beazley_year':         hx.Int( mode='output',  async_output=[]),
                                                                    'lloyds_end_date':              hx.Date(mode='output',  async_output=[]),
                                                                    'beazley_start_date':           hx.Date(mode='output',  async_output=[]),
                                                                    'beazley_data_run_date':        hx.Date(mode='output',  async_output=[]),
                                                                    'lag_beazley_latest_to_lloyds': hx.Float(mode='output', async_output=[]),
                                                                    'lloyds_offset':                hx.Int( mode='output',  async_output=[]),
                                                                    'per_since_year_start':         hx.Float(mode='output', async_output=[])})}),
        'pc': hx.Structure(
            children={
                'show_pc':hx.Bool(mode="output"),
                'show_pc_bbt':hx.Bool(mode="output"),
                'pc_control': hx.Structure(children={   'is_amount':        hx.Bool(mode='output'),
                                                        'is_experience':    hx.Bool(mode='output'),
                                                        'is_none':          hx.Bool(mode='output'),
                                                        'is_pc_on_binders': hx.Bool(mode='output'),                         }),
                'pc_structure': hx.Structure(children={ "show_for_standard" :       hx.Bool(mode='output'),
                                                        "show_for_sliding_scale":   hx.Bool(mode='output'),
                                                        "for_sliding_scale":        hx.Structure(children={})               }),

                "profit_commission": hx.Structure(children={"lob": hx.File(mode="output", file_name="lob.xlsx", async_output=['calculate_profit_commission_task'])})
            }
        ),
        "rating_summary": hx.Structure(children={
                "pricing_adequacy_metrics": hx.Structure(children={
                        "pricing_adequacy_pre_adj": hx.Structure(children={"table_str": hx.Str(mode="output", async_input = ["generate_word_document_task", "generate_excel_document_task"])}),
                        "pricing_adequacy_actuarial_basis": hx.Structure(children={"table_str": hx.Str(mode="output", async_input = ["generate_word_document_task", "generate_excel_document_task"])})
                    }
                ),
                "section_ref_allocation": hx.Structure(children={      
                    "show_refs": hx.Structure(view={"label": "Show Refs"}, children={   **{f"ref_{i:02}": hx.Bool(mode="output", view={"label": f"Reference {i}"}) for i in range(1,num_refs+1)}}) 
                    }
                )
            }
        )
    }
