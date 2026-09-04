import hx_data_schema as hx
from data_schema.dropdown_list import climate_perils, climate_aware_response, climate_protection_measures_response
from data_schema.utilities import run_schedule_rater_async_tasks

def thousands_format(mantissa = 0):
    return {"thousandSeparated": True, "mantissa": mantissa}

def percent_format(mantissa = 0):
    return {"output": "percent", "mantissa": mantissa}

def integer_format(mantissa = 0):
    return {"thousandSeparated": False, "mantissa": mantissa}


def non_layer_summary():
    '''
    data schema for summary (non-layer dependent)
    '''
    return {
        "non_layer_summary": hx.Structure(children={
            "climate_metrics": hx.Structure(children={
                "perils": hx.Structure(children={
                    "peril_selection": hx.Str(mode="input", optionality="optional", default=None, options=climate_perils, view={"label": "Peril Selection"}),
                    "ws_selected": hx.Bool(mode="output"),
                    "fl_selected": hx.Bool(mode="output")
                }),

                "flood": hx.Structure(children={
                    "flood_climate_risk_score": hx.Int(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=["generate_flood_climate_metrics_task"], view={"label": "US FL Climate Score", "read_only": True, "format": thousands_format(0)}),
                    "pol_current_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Policy Current Flood EL", "read_only": True, "format": thousands_format(0)}),
                    "pol_future_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Policy Future Flood EL", "read_only": True, "format": thousands_format(0)}),
                    "pol_change_all_years": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "US FL Change in Expected Loss by 2055", "read_only": True, "format": percent_format(0)}),
                    "pol_change_one_year": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "US FL Change in Expected Loss in One Year", "read_only": True, "format": percent_format(0)}),
                    "pol_change_five_years": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "US FL Change in Expected Loss in Five Years", "read_only": True, "format": percent_format(0)}),
                    "flood_el_projection": hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Description", "read_only": True}),

                    "flood_climate_table": hx.List(mode="output", async_input=["generate_climate_doc_task"], async_output=["generate_flood_climate_metrics_task"], children={
                        "loc_id": hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=["generate_flood_climate_metrics_task"], view={"label": "Loc ID", "read_only": True}),
                        "street_name": hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=["generate_flood_climate_metrics_task"], view={"label": "Street Name", "read_only": True}),
                        "state": hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=["generate_flood_climate_metrics_task"], view={"label": "State", "read_only": True}),
                        "latitude": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Latitude", "read_only": True, "format": thousands_format(6)}),
                        "longitude": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Longitude", "read_only": True, "format": thousands_format(6)}),
                        "industry": hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Industry", "read_only": True}),
                        "occupancy": hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Occupancy", "read_only": True}),
                        "constr_code": hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Constr Code", "read_only": True}),
                        "num_stories": hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Num Stories", "read_only": True}),
                        "tiv_total": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "TIV", "read_only": True, "format": thousands_format(0)}),
                        "tiv_total_usd": hx.Float(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=["generate_flood_climate_metrics_task"], view={"label": "TIV USD", "read_only": True, "format": thousands_format(0)}),
                        "el_post_uw_usd_100_fl_total": hx.Float(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "ind_map" : hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Ind Map", "read_only": True}),
                        "current_risk_score" : hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Current Risk Score", "read_only": True, "format": thousands_format(0)}),  
                        "future_risk_score" : hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Future Risk Score", "read_only": True, "format": thousands_format(0)}),  
                        "bzly_loc_score" : hx.Int(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=["generate_flood_climate_metrics_task"], view={"label": "Beazley Loc Score", "read_only": True, "format": thousands_format(0)}),  
                        "current_fl_el_with_score" : hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Current FL EL with Score", "read_only": True, "format": thousands_format(2)}),  
                        "current_fl_el_weighted_by_score" : hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Current FL EL Weighted by Score", "read_only": True, "format": thousands_format(2)}),  
                        "current_aadr" : hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Current AADR", "read_only": True, "format": percent_format(5)}),   
                        "future_aadr" : hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Current AADR", "read_only": True, "format": percent_format(5)}),   
                        "current_aal": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Current AAL", "read_only": True, "format": thousands_format(0)}),
                        "future_aal": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Future AAL", "read_only": True, "format": thousands_format(0)}),
                        "change": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Change", "read_only": True, "format": percent_format(1)}),
                        "current_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Current Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "future_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Future Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "status": hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Status", "read_only": True})
                    }),

                    "score_summary": hx.List(mode="output", async_output=["generate_flood_climate_metrics_task"], children={
                        "bzly_loc_score": hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Score", "read_only": True}),
                        "tiv_total_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Total TIV", "read_only": True, "format": thousands_format(0)}),
                        "tiv_total_usd_chart": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Total TIV ($m)", "read_only": True, "format": thousands_format(0)}),
                        "loc_count": hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Location Count", "read_only": True}),
                        "loc_prop": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Location Proportion", "read_only": True, "format": percent_format(0), "chart": {"series_type": "line", "series_axis": "secondary"}}),
                        "current_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood EL", "read_only": True, "format": thousands_format(0)}),
                    }),

                    "constr_summary": hx.List(mode="output", async_output=["generate_flood_climate_metrics_task"], children={
                        "constr_code": hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Constr Code", "read_only": True}),
                        "locations": hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Locations", "read_only": True}),
                        "tiv_total_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Total TIV", "read_only": True, "format": thousands_format(0)}),
                        "current_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "future_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Future Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "current_fl_el_with_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood EL with Score", "read_only": True, "format": thousands_format(0)}),
                        "current_fl_el_weighted_by_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Score Weighted Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "bzly_loc_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Avg Score", "read_only": True, "format": thousands_format(1)}),
                        "change_five_years": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Five-year EL change", "read_only": True, "format": percent_format(0)})
                    }),
                    "num_stories_summary": hx.List(mode="output", async_output=["generate_flood_climate_metrics_task"], children={
                        "num_stories": hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Num Stories", "read_only": True}),
                        "locations": hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Locations", "read_only": True}),
                        "tiv_total_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Total TIV", "read_only": True, "format": thousands_format(0)}),
                        "current_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "future_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Future Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "current_fl_el_with_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood EL with Score", "read_only": True, "format": thousands_format(0)}),
                        "current_fl_el_weighted_by_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Score Weighted Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "bzly_loc_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Avg Score", "read_only": True, "format": thousands_format(1)}),
                        "change_five_years": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Five-year EL change", "read_only": True, "format": percent_format(0)})
                    }),
                    "flood_risk_summary": hx.List(mode="output", async_output=["generate_flood_climate_metrics_task"], children={
                        "risk_level_fl": hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood Risk", "read_only": True}),
                        "locations": hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Locations", "read_only": True}),
                        "tiv_total_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Total TIV", "read_only": True, "format": thousands_format(0)}),
                        "current_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "future_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Future Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "current_fl_el_with_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood EL with Score", "read_only": True, "format": thousands_format(0)}),
                        "current_fl_el_weighted_by_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Score Weighted Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "bzly_loc_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Avg Score", "read_only": True, "format": thousands_format(1)}),
                        "change_five_years": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Five-year EL change", "read_only": True, "format": percent_format(0)})
                    }),
                    "top_10_locations_summary": hx.List(mode="output", async_output=["generate_flood_climate_metrics_task"], children={
                        "tiv_total_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Total TIV", "read_only": True, "format": thousands_format(0)}),
                        "bzly_loc_score": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Score", "read_only": True, "format": thousands_format(0)}),
                        "constr_code": hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Constr Code", "read_only": True}),
                        "industry": hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Industry", "read_only": True}),
                        "occupancy": hx.Str(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Occupancy", "read_only": True}),
                        "num_stories": hx.Int(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Num Stories", "read_only": True}),
                        "current_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "future_fl_el": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Future Flood EL", "read_only": True, "format": thousands_format(0)}),
                        "change_five_years": hx.Float(mode="input", optionality="optional", default=None, async_output=["generate_flood_climate_metrics_task"], view={"label": "Five-year EL change", "read_only": True, "format": percent_format(0)})
                    })                    
                }), 

                "weighted_climate_score": hx.Int(mode="output", async_input=["generate_climate_doc_task"], view={"label": "US HU Climate Score"}),
                "climate_score_description": hx.Str(mode="output", async_input=["generate_climate_doc_task"], view={"label": "Description"}),
                "score_locations": hx.Structure(children={
                    **{
                        f"score_{index}": hx.Structure(view={"label": f"{index}"}, children={
                            "score": hx.Int(mode="output", async_input=["generate_climate_doc_task"], view={"label": "Score"}),
                            "loc_count": hx.Int(mode="output", async_input=["generate_climate_doc_task"], view={"label": "Locations"}),
                            "loc_prop": hx.Float(mode="output", async_input=["generate_climate_doc_task"], view={"label": "Proportion", "format": percent_format(1), "chart": {"series_type": "line", "series_axis": "secondary"}}),
                            "total_tiv": hx.Int(mode="output", async_input=["generate_climate_doc_task"], view={"label": "Total TIV"}),
                            "gn_tech_pre_uw": hx.Int(mode="output", async_input=["generate_climate_doc_task"], view={"label": "Total Tech Prem Pre UW Adj", "format": thousands_format(), "chart": {"series_type": "line", "series_axis": "secondary"}}),
                            "aal_cgear_masked": hx.Int(mode="output", async_input=["generate_climate_doc_task"], view={"label": "AAL C-Gear Masked"}),
                            "aal_weighted_cgear": hx.Int(mode="output", async_input=["generate_climate_doc_task"], view={"label": "Weighted AAL"})
                        })
                        for index in range(6)
                    }
                }),
                "client_questions": hx.Structure(children={
                    "risk_mitigation_measures": hx.Structure(children={
                        "question": hx.Str(mode="input", default="Does the insured have any of the following risk mitigation measures in place? Please select the appropiate options.", view={"label": "Question", "read_only": True}),
                        "answer": hx.Str(mode="input", optionality="optional", default=None, options=climate_aware_response, async_input=["generate_climate_doc_task"], view={"label": "Response"}),
                        "show_risk_mitigation_measures": hx.Bool(mode="output"),
                    }),
                    "awareness_list": hx.List(mode = "output", async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), children={
                        "question": hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view = {"label": "Climate awareness?", "read_only": True}),
                        "response":hx.Bool(mode="input", default = False, async_output = run_schedule_rater_async_tasks(async_input = False), async_input=["generate_climate_doc_task"], view = {"label": "Response"})
                    }),   
                    "additional_risk_mitigation_practices": hx.Structure(children={
                        "question": hx.Str(mode="input", default="Does the insured have any additional risk mitigation practices beyond those listed above?", async_input=["generate_climate_doc_task"], view={"label": "Question", "read_only": True}),
                        "answer": hx.Str(mode="input", optionality="optional", default=None, options=climate_aware_response, async_input=["generate_climate_doc_task"], view={"label": "Response"}),
                        "rationale": hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], view={"label": "Rationale"}) ,                       
                        "show_additional_risk_mitigation_practices": hx.Bool(mode="output"), 
                    }),
                    "protection_measures_list": hx.List(mode = "output", async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), children={
                        "question": hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view = {"label": "What protection measures and emergency responses have the insured taken to account for climate related risks?", "read_only": True}),
                        "response":hx.Bool(mode="input", default = False, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view = {"label": "Response\n(Select one option only)"})
                    }),
                    **generate_climate_questions(),        
                }),
                "ws_cc_score_occupancy" : hx.List(mode = "output", async_output = run_schedule_rater_async_tasks(async_input = False), children = {
                    "occupancy" : hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view= {"label" : "Occupancy", "read_only": True}),
                    "cgear_score" : hx.Float(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view={"label": "Average Score", "read_only": True, "format": integer_format(1)}),
                    "tiv_total_usd" : hx.Int(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view={"label": "Total TIV", "read_only": True, "format": thousands_format()}),
                    "gn_tech_pre_uw_layer" : hx.Int(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view={"label": "US Windstorm Tech Prem Pre UW Adj", "read_only": True, "format": thousands_format()})
                }),
                "ws_cc_score_gate" : hx.List(mode = "output", async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), children = {
                    "ws_gate" : hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view = {"label" : "WS Gate", "read_only": True}),
                    **{
                       f"cgear_{score}" : hx.Int(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view = {"label" : f"Score {score}", "read_only": True})
                       for score in range (6)
                    }
                }),
                "ws_cc_score_location" : hx.List(mode = "output", async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), children = {
                    "tiv_total_usd" : hx.Int(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view={"label": "Total TIV", "read_only": True, "format": thousands_format()}),
                    "aal_weighted_cgear" : hx.Int(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view={"label": "Weighted AAL", "read_only": True, "format": thousands_format()}),
                    "cgear_score" :hx.Float(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view = {"label":"Score", "read_only": True, "format": integer_format()}),
                    "ws_gate" : hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view = {"label" : "WS Gate", "read_only": True}),
                    "distance_from_coast" : hx.Int(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view={"label": "DTC", "read_only": True, "format": thousands_format()}),
                    "zip" : hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view = {"label" : "Zip", "read_only": True}),
                    "occupancy" : hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view={"label": "Occupancy", "read_only": True}),
                    "constr_desc" : hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output = run_schedule_rater_async_tasks(async_input = False), view={"label": "Construction Type", "read_only": True}),

                }),
                "document": hx.File(mode="output", file_name="climate_change_spotlight.docx", async_output=["generate_climate_doc_task"], view={"label": "Document"}),
                "show_file_component": hx.Bool(mode="input", default=False, async_output=["produce_climate_map_task"]),
                "climate_heatmap_file": hx.File(mode="output", async_output=["produce_climate_map_task"], file_name="climate-exposure-map.html", view={"label": "Climate Map"}),
            })
        })
    }

def generate_climate_questions():
    climate_questions = {
        'emergency_response_plans':'**Emergency Response Plans**\nPost-event response plans to allow for restoration of essential services, establishment of temporary repairs etc. to allow normal operations to resume as quickly as possible following a catastrophe event.', 
        'hurricane_focused_renovations':'**Hurricane Focused Renovations**\nRenovations undergone specifically to re-fit buildings to improve resilience to hurricane-force winds.', 
        'emergency_generators':'**Emergency Generators**\nPossessing emergency back-up generators to allow facilities to resume operation more rapidly after a hurricane, in the event of regional power-cuts due to storm damage', 
        'flooding_mitigation_plans':'**Flooding Mitigation Plans**\nPre-event procedures to minimise exposure to storm surge damage, including actions such as removing inventory and critical systems from the ground floor / basement, or storing elevators at the top of the lift shaft before an event.'
    }
    climate_dict = {}
    for key, value in climate_questions.items():
        climate_dict[key] = hx.Structure(children=climate_children(value))
    
    return climate_dict

def climate_children(value):
    return {
        "selection": hx.Bool(mode="input", default=False),
        "climate_question": hx.Str(mode="input", default=value, view={"options": {"read_only": {"read_only": True}}}),
    }
