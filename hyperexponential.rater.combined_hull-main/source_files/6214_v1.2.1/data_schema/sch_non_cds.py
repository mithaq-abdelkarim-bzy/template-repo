import hx_data_schema as hx


def sch_non_cds_controllers():
    validation_prefix = "validation_"
    return {
        "tooltips": hx.Structure(
            children={
                "loh": hx.Structure(
                    children={
                        "number_of_vessels": hx.Str(
                            mode="input",
                            default='If rating multiple vessels that are identical in the same row, then enter # of vessels being "bulked", otherwise enter "1". For "bulked" vessels enter the total daily rate across the group, not the average.',
                        )
                    }
                ),
                "shipbuilders": hx.Structure(
                    children={
                        "other_deductions": hx.Str(
                            mode="input",
                            default="Other deductible% like Profit Commission, No Claim Discount",
                        ),
                        "credibility": hx.Str(
                            mode="input",
                            default="Pulled from the Experience Rater",
                        ),
                        "experience_premium": hx.Str(
                            mode="input",
                            default="Pulled from the Experience Rater",
                        ),
                        "number_of_vessels": hx.Str(
                            mode="input",
                            default="""If entering bulk rows (i.e. more than one vessel per row, please enter: 
                            a) The total months of build time across each stage/all stages (depending on the data you have available), not the average months per vessel 
                            b) The average deductible across the bulk risks.
                            c) The Total Sum Insured across the bulk risks.""",
                        ),
                    }
                ),
            }
        ),
        "show_rating_summary_table": hx.Structure(
            children={
                "show_hull_table": hx.Bool(
                    mode="output",
                ),
                "show_hull_war_table": hx.Bool(
                    mode="output",
                ),
                "show_hull_iv_table": hx.Bool(
                    mode="output",
                ),
                "show_hull_iv_war_table": hx.Bool(
                    mode="output",
                ),
                "show_loh_table": hx.Bool(
                    mode="output",
                ),
                "show_ship_building_table": hx.Bool(
                    mode="output",
                ),
            }
        ),
        "show_hide_toggles": hx.Structure(
            children={
                "show_mismatched_inception_year_warning": hx.Bool(mode="output"),
                "show_powersearch": hx.Bool(mode="output"),
                "rate_change": hx.Structure(
                    children={
                        "show_generate_output_summary_button": hx.Bool(
                            mode="output",
                        ),
                        "show_rarc_note_for_uw": hx.Bool(mode = "output"),
                    }
                ),
                "iv": hx.Structure(
                    children={
                        "show_iv_coverage": hx.Bool(
                            mode="output",
                            async_input=[
                                "generate_rating_summary_xlsx_task",
                                "rarc_task",
                                "push_vessels_to_datamart_task",
                                "upsert_hx_meta_policy_references_task",
                                "start_renewal_task",
                            ],
                        ),
                        "iv_show_vessel_details": hx.Bool(
                            mode="input",
                            default=False,
                            view={"label": "Show Vessel Details"},
                        ),
                        "iv_filter_by_errors": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Filter by Errors"},
                        ),
                        "iv_not_filter_by_errors": hx.Bool(mode="output"),
                        "show_written_line_warning": hx.Bool(mode="output"),
                        "hide_written_line_warning": hx.Bool(mode="output"),
                        "show_brokerage_warning": hx.Bool(mode="output"),
                        "hide_brokerage_warning": hx.Bool(mode="output"),
                        "show_data_mart_warning": hx.Bool(mode="output"),
                    }
                ),
                "war": hx.Structure(
                    children={
                        "show_war_coverage": hx.Bool(
                            mode="output",
                            async_input=[
                                "generate_rating_summary_xlsx_task",
                                "rarc_task",
                                "push_vessels_to_datamart_task",
                                "upsert_hx_meta_policy_references_task",
                                "start_renewal_task",
                            ],
                        ),
                        "war_show_vessel_details": hx.Bool(
                            mode="input",
                            default=False,
                            view={"label": "Show Vessel Details"},
                        ),
                        "war_filter_by_errors": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Filter by Errors"},
                        ),
                        "war_not_filter_by_errors": hx.Bool(mode="output"),
                        "show_written_line_warning": hx.Bool(mode="output"),
                        "hide_written_line_warning": hx.Bool(mode="output"),
                        "show_brokerage_warning": hx.Bool(mode="output"),
                        "hide_brokerage_warning": hx.Bool(mode="output"),
                        "show_data_mart_warning": hx.Bool(mode="output"),
                    }
                ),
                "loh": hx.Structure(
                    children={
                        "show_loh_coverage": hx.Bool(
                            mode="output",
                            async_input=[
                                "rarc_task",
                                "generate_rating_summary_xlsx_task",
                                "upsert_hx_meta_policy_references_task",
                                "start_renewal_task",
                                "push_vessels_to_datamart_task",
                            ],
                        ),
                        "show_defaults": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Show Defaults"},
                        ),
                        "show_number_of_vessels_warning": hx.Bool(mode="output"),
                        "show_written_line_warning": hx.Bool(mode="output"),
                        "hide_written_line_warning": hx.Bool(mode="output"),
                        "show_brokerage_warning": hx.Bool(mode="output"),
                        "hide_brokerage_warning": hx.Bool(mode="output"),
                        "show_data_mart_warning": hx.Bool(mode="output"),
                    }
                ),
                "hull": hx.Structure(
                    children={
                        "show_hull_coverage": hx.Bool(
                            mode="output",
                            async_input=[
                                "rarc_task",
                                "generate_rating_summary_xlsx_task",
                                "upsert_hx_meta_policy_references_task",
                                "start_renewal_task",
                                "push_vessels_to_datamart_task",
                            ],
                            view={"label": "Hull Coverage"},
                        ),
                        "show_modelling_page": hx.Bool(mode="output"),
                        "show_vessels_details": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Show Vessels Details"},
                        ),
                        "filter_by_errors": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Filter by Errors"},
                        ),
                        "not_filter_by_errors": hx.Bool(mode="output"),
                        "show_generated_vessels_xlsx": hx.Bool(
                            mode="input",
                            default=False,
                            async_output=[
                                "generate_vessels_xlsx_task",
                            ],
                        ),
                        "show_generated_output_summary_xlsx": hx.Bool(
                            mode="input",
                            default=False,
                            async_output=["generate_rating_summary_xlsx_task"],
                        ),
                        "show_generated_portfolio_analysis_excel": hx.Bool(
                            mode="input",
                            default=False,
                            async_output=["generate_portfolio_analysis_excel"],
                        ),
                        "show_written_line_warning": hx.Bool(mode="output"),
                        "hide_written_line_warning": hx.Bool(mode="output"),
                        "show_brokerage_warning": hx.Bool(mode="output"),
                        "hide_brokerage_warning": hx.Bool(mode="output"),
                        "show_data_mart_warning": hx.Bool(mode="output"),
                        "show_duplicate_vessel_warning": hx.Bool(mode="output"),
                    }
                ),
                "ship_building": hx.Structure(
                    children={
                        "show_number_of_vessels_warning": hx.Bool(mode="output"),
                        "show_ship_building_coverage": hx.Bool(
                            mode="output",
                            async_input=[
                                "set_vessels_defaults_task",
                                "rarc_task",
                                "generate_rating_summary_xlsx_task",
                                "upsert_hx_meta_policy_references_task",
                                "start_renewal_task",
                            ],
                        ),
                        "show_experience_number_of_vessels_warning": hx.Bool(
                            mode="output",
                        ),
                        "show_experience_signed_line_warning": hx.Bool(
                            mode="output",
                        ),
                        "show_experience_rating_warning": hx.Bool(
                            mode="output",
                        ),
                        "show_uw_adj_warning": hx.Bool(
                            mode="output",
                        ),
                        "hide_uw_adj_warning": hx.Bool(
                            mode="output",
                        ),
                        "show_written_line_warning": hx.Bool(mode="output"),
                        "hide_written_line_warning": hx.Bool(mode="output"),
                        "show_brokerage_warning": hx.Bool(mode="output"),
                        "hide_brokerage_warning": hx.Bool(mode="output"),
                        "show_ship_builders_actuarial_pricing": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Show Actuarial Pricing"},
                        ),
                    }
                ),
                "modelling": hx.Structure(
                    children={
                        "show_adjustment_factors": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Show Adjustment Factors"},
                        ),
                        "show_static_calculations": hx.Bool(
                            mode="input",
                            default=True,
                            optionality="required",
                            view={"label": "Show Static Calculations"},
                        ),
                        "show_behavioural_calculations": hx.Bool(
                            mode="input",
                            default=True,
                            optionality="required",
                            view={"label": "Show Behavioural Calculations"},
                        ),
                        "show_behavioural_build_up": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Show Behavioural Build Up"},
                        ),
                        "show_static_build_up": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Show Static Build Up"},
                        ),
                        "show_behavoural_rating_levels": hx.Bool(
                            mode="input",
                            default=False,
                            optionality="required",
                            view={"label": "Show Behavioural Rating Levels"},
                        ),
                    }
                ),
            }
        ),
        "labels": hx.Structure(
            children={
                "mismatched_inception_year_warning": hx.Str(
                    mode="output",
                    view={
                        "options": {
                            "warning_option": {
                                "style_cell": "hx-bad",
                            }
                        }
                    },
                ),
                "modelling": hx.Structure(
                    children={
                        "average_static_fleet_relativity": hx.Str(
                            mode="input", default="Average Static Fleet Relativity"
                        ),
                        "average_behavioural_fleet_relativity": hx.Str(
                            mode="input", default="Average Behavioural Fleet Relativity"
                        ),
                    }
                ),
                "ship_building": hx.Structure(
                    children={
                        "achieved_premium": hx.Str(
                            mode="output",
                            async_input=["generate_rating_summary_xlsx_task"],
                        ),
                        "exposure_benchmark_premium": hx.Str(
                            mode="output",
                            async_input=["generate_rating_summary_xlsx_task"],
                        ),
                        "experience_benchmark_premium": hx.Str(
                            mode="output",
                            async_input=["generate_rating_summary_xlsx_task"],
                        ),
                        "weight_to_experience": hx.Str(
                            mode="input",
                            async_input=["generate_rating_summary_xlsx_task"],
                            default="Credibility (Weight to Experience Rated)",
                        ),
                        "blended_premium_pre_adj": hx.Str(
                            mode="output",
                            async_input=["generate_rating_summary_xlsx_task"],
                        ),
                        "blended_premium_post_adj": hx.Str(
                            mode="output",
                            async_input=["generate_rating_summary_xlsx_task"],
                        ),
                        "experience_rating": hx.Structure(
                            children={
                                "currency_experience_rating_data_input_net_premium_shared_line_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_data_input_gross_premium_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_data_input_total_incurred_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_data_input_att_incurred_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_data_input_large_incurred_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_projection_net_premium_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_projection_att_incurred_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_projection_large_incurred_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_projection_on_levelled_net_premium_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_projection_on_levelled_att_incurred_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_rating_projection_on_levelled_large_claims_label": hx.Str(
                                    mode="output"
                                ),
                                "current_year_experience_rating_rate_change_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_claims_cost_label": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_claims_net_benchmark_premium_pure_experience": hx.Str(
                                    mode="output"
                                ),
                                "currency_experience_exchange_rate_label": hx.Str(
                                    mode="output"
                                ),
                            }
                        ),
                    }
                ),
                "required_vessels_columns_labels": hx.Structure(
                    children={
                        "name": hx.Str(mode="output"),
                        "inception_date": hx.Str(mode="output"),
                        "expiry_date": hx.Str(mode="output"),
                        "vessel_type": hx.Str(mode="output"),
                        "gross_tonnage": hx.Str(mode="output"),
                        "dwt": hx.Str(mode="output"),
                        "year_built": hx.Str(mode="output"),
                        "flag": hx.Str(mode="output"),
                        "vessel_class": hx.Str(mode="output"),
                        "order_percent": hx.Str(mode="output"),
                        "freight_conditions": hx.Str(mode="output"),
                        "vessel_quality": hx.Str(mode="output"),
                        "area_of_operation": hx.Str(mode="output"),
                        "coverage": hx.Str(mode="output"),
                        "agreed_value": hx.Str(mode="output"),
                        "deductible": hx.Str(mode="output"),
                        "achieved_rate": hx.Str(mode="output"),
                        "achieved_premium": hx.Str(mode="output"),
                        "static_benchmark_premium": hx.Str(mode="output"),
                        "behavioural_benchmark_premium": hx.Str(mode="output"),
                        "iv_benchmark_premium": hx.Str(mode="output"),
                        "war_benchmark_premium": hx.Str(mode="output"),
                    }
                ),
                "hull": hx.Structure(
                    children={
                        validation_prefix + "name": hx.Str(mode="output"),
                        validation_prefix + "inception_date": hx.Str(mode="output"),
                        validation_prefix + "expiry_date": hx.Str(mode="output"),
                        validation_prefix + "vessel_type": hx.Str(mode="output"),
                        validation_prefix + "gross_tonnage": hx.Str(mode="output"),
                        validation_prefix + "dwt": hx.Str(mode="output"),
                        validation_prefix + "year_built": hx.Str(mode="output"),
                        validation_prefix + "flag": hx.Str(mode="output"),
                        validation_prefix + "vessel_class": hx.Str(mode="output"),
                        validation_prefix + "order_percent": hx.Str(mode="output"),
                        validation_prefix + "freight_conditions": hx.Str(mode="output"),
                        validation_prefix + "vessel_quality": hx.Str(mode="output"),
                        validation_prefix + "area_of_operation": hx.Str(mode="output"),
                        validation_prefix + "coverage": hx.Str(mode="output"),
                        validation_prefix + "agreed_value": hx.Str(mode="output"),
                        validation_prefix + "deductible": hx.Str(mode="output"),
                        validation_prefix + "achieved_rate": hx.Str(mode="output"),
                        validation_prefix + "error_message": hx.Str(mode="output"),
                        "data_mart_warning_message": hx.Str(
                            mode="input",
                            default="Warning: Push latest vessels changes to Powersearch database",
                            view={
                                "options": {
                                    "read_only_option": {
                                        "read_only": True,
                                        "style_cell": "hx-bad",
                                    }
                                }
                            },
                        ),
                        "duplicate_imo_and_name_message": hx.Str(
                            mode="input",
                            default="Duplicate Vessel's IMO and Name exists",
                            view={
                                "options": {
                                    "read_only_option": {
                                        "read_only": True,
                                        "style_cell": "hx-bad",
                                    }
                                }
                            },
                        ),
                    }
                ),
                "iv": hx.Structure(
                    children={
                        validation_prefix + "iv_coverage": hx.Str(mode="output"),
                        validation_prefix + "iv_agreed_value": hx.Str(mode="output"),
                        validation_prefix + "iv_achieved_rate": hx.Str(mode="output"),
                        validation_prefix + "iv_error_message": hx.Str(mode="output"),
                    }
                ),
                "war": hx.Structure(
                    children={
                        validation_prefix + "war_coverage": hx.Str(mode="output"),
                        validation_prefix + "war_agreed_value": hx.Str(mode="output"),
                        validation_prefix + "war_achieved_rate": hx.Str(mode="output"),
                        validation_prefix + "war_error_message": hx.Str(mode="output"),
                    }
                ),
                "portfolio_analysis_labels": hx.Structure(
                    children={
                        "currency_avg_agreed_value": hx.Str(mode="output"),
                        "currency_agreed_value_converted": hx.Str(mode="output"),
                        "gross_tonnage_label": hx.Str(
                            mode="input", default="Gross Tonnage"
                        ),
                        "effective_date_label": hx.Str(
                            mode="input", default="Effective Date"
                        ),
                        "agreed_value_label": hx.Str(
                            mode="input", default="Agreed Value"
                        ),
                        "dwt_label": hx.Str(mode="input", default="DWT"),
                        "year_built_label": hx.Str(mode="input", default="Year Built"),
                    }
                ),
                "loh": hx.Structure(
                    children={
                        "loh_vessels_number_greater_than_one_warning": hx.Str(
                            mode="output"
                        ),
                        "achieved_premium_label": hx.Str(mode="output"),
                        "total_benchmark_premium_label": hx.Str(mode="output"),
                        "data_mart_warning_message": hx.Str(
                            mode="input",
                            default="Warning: Push latest vessels changes to Powersearch database",
                            view={
                                "options": {
                                    "read_only_option": {
                                        "read_only": True,
                                        "style_cell": "hx-bad",
                                    }
                                }
                            },
                        ),
                    }
                ),
                "shipbuilders": hx.Structure(
                    children={
                        "shipbuilders_vessels_number_greater_than_one_warning": hx.Str(
                            mode="output"
                        ),
                        "number_of_vessels_warning": hx.Str(
                            mode="input",
                            default="• Warning: Experience Pricing will not be used if Vessels Number is Empty or Zero.",
                            view={"options": {"read_only_option": {"read_only": True}}},
                        ),
                        "experience_signed_line_warning": hx.Str(
                            mode="input",
                            default="• Warning: Need to input Signed Line % if Gross Premium >0",
                            view={"options": {"read_only_option": {"read_only": True}}},
                        ),
                    }
                ),
                "currency_loh_benchmark_premium_label": hx.Str(mode="output"),
                "currency_loh_daily_rate_label": hx.Str(mode="output"),
            }
        ),
    }
