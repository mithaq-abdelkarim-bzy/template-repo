# v0.5.0
import hx_data_schema as hx
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict , max_coverages
from algorithms.rate_constants import max_layers, experience_rating_max_years
from data_schema.sch_rate_change import rarc_task_name

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
                default="Click the 'import expiring policy data' arrow in the top right corner then click **Start Policy**. ",
                async_output=["start_renewal_task"],
                view={"read_only":True}
            ),
            "expiring_policy_option_id": hx.Int(mode="input", default=None, optionality="optional", async_output=["start_renewal_task", "sync_expiring_ids"]),
            
            "coverage_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. Required for governance # Edit v0.3.0
            "insured_asset_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. Required for governance # Edit v0.3.0
            
            "show_rate_change_layer_no_ia_use": hx.Bool(mode="output"), # NOTE: Can be removed for the case unused Edit v0.3.0
            "show_rate_change_layer_ia_use": hx.Bool(mode="output"), # NOTE: Can be removed for the case unused Edit v0.3.0
            "show_rate_change_coverage_no_ia_use": hx.Bool(mode="output"), # NOTE: Can be removed for the case unused Edit v0.3.0
            "show_rate_change_coverage_ia_use": hx.Bool(mode="output"), # NOTE: Can be removed for the case unused Edit v0.3.0

            "layer_no_ia_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. ShownBy for skeleton. Can be remove for the case unused # Edit v0.3.0
            "layer_ia_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. ShownBy for skeleton. Can be remove for the case unused # Edit v0.3.0
            "coverage_no_ia_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. ShownBy for skeleton. Can be remove for the case unused # Edit v0.3.0
            "coverage_ia_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. ShownBy for skeleton. Can be remove for the case unused # Edit v0.3.0
            "is_steer": hx.Bool(mode="output", async_input=[rarc_task_name,"start_renewal_task"]),
            "is_clash": hx.Bool(mode="output",async_input=[rarc_task_name]),
            "is_healthcare_cat": hx.Bool(mode="output",async_input=[rarc_task_name,"start_renewal_task"]),
            "is_steer_experience_rating": hx.Bool(mode="output"),
            "show_layer_fgu": hx.Bool(mode="output"),
            **{f"show_layer_{index:02d}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
            **{f"show_data_year_{index:02d}": hx.Bool(mode="output") for index in range(1,experience_rating_max_years+1)},
            "is_steer_experience_rating": hx.Bool(mode="input", default=True, async_input= ["advanced_features_task",rarc_task_name], view={"label":"Experience rating?"}),
            # "is_steer_exposure_rating_risk_profil_banded":  hx.Bool(mode="input", default=True,view={"label":"Risk Profile Banded?"}),
            "is_steer_exposure_rating_risk_profil_bdx": hx.Bool(mode="input", default=True,view={"label":"Risk Profile Bdx?"}),
            "is_steer_exposure_rating_limit_average_severity": hx.Bool(mode="output", view={"label":"Limit Average Severity?"}),
            "is_steer_raw_data_validated": hx.Bool(mode="output",async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"]),
            "is_steer_raw_data_not_validated": hx.Bool(mode="output"),
            "is_bdx_input_issue":hx.Bool(mode="output"),
            "bc_ulr_message": hx.Str(mode="output"),
            **{f"bc_ulr_message_{index:02d}": hx.Str(mode="output") for index in range(1,max_layers+1)},
            **{f"show_las_chart_layer_{index:02d}": hx.Bool(mode="input", default=False,view={"label":"Show Chart"}) for index in range(1,max_layers+1)},
            "is_pure_premium_calculated": hx.Bool(mode="output"),
            "is_pure_premium_not_calculated": hx.Bool(mode="output", async_input=["advanced_features_task",rarc_task_name]),
            "pure_premium_error_message": hx.Str(mode="output"),
            "show_steer": hx.Bool(mode="output"),
            "show_healthcare_cat": hx.Bool(mode="output"),
            "show_clash": hx.Bool(mode="output"),
            "show_steer_experience_rating": hx.Bool(mode="output"),
            "show_steer_risk_bdx": hx.Bool(mode="output"),
            "show_steer_las_bdx": hx.Bool(mode="output"),
            "data_used_in_advanced_features_task": hx.Str(mode="output", async_output=["advanced_features_task"]),
            "layer_data_used_in_advanced_features_task": hx.Str(mode="output", async_output=["advanced_features_task"]),
            "has_run_advanced_features": hx.Bool(mode="output",async_output=["advanced_features_task"]),

            "data_used_in_steer_format_data_task": hx.Str(mode="output", async_output=["steer_format_raw_data_task"]),
            "layer_data_used_in_steer_format_data_task": hx.Str(mode="output", async_output=["steer_format_raw_data_task"]),
            "raw_data_used_in_steer_format_data_task": hx.Str(mode="output", async_output=["steer_format_raw_data_task"]),
            "expo_assumptions_data_used_in_steer_format_data_task": hx.Str(mode="output", async_output=["steer_format_raw_data_task"]),
            "has_run_steer_format_data": hx.Bool(mode="output",async_output=["steer_format_raw_data_task"]),

            "info_by_risk_bdx_exposure_prem": hx.Str(mode="output"),
            "info_by_include_swing_rates": hx.Str(mode="output"),
            "info_by_include_pc": hx.Str(mode="output"),
            "is_not_clash": hx.Bool(mode="output"),
            "show_rater_priced": hx.Bool(mode="output"),
            "show_case_priced": hx.Bool(mode="output"),
            "triangle_fgu_instructions": hx.Str(mode="input", default="**Triangles User Guide**\nTriangles are cumulative by default. Change the toggle to Incremental if required.\n\n **Triangles - Raw Data:** If transactional claims data has been provided, the triangle will populate automatically.\n\n **Triangles - Manual Input (Optional):**Only use this section if the triangle cannot be built from Raw Data or an alternative triangle is required.\nEnter the triangle as-at date, enter the number of treaty years, click ‘Setup Override Triangle’.\nEnter data manually or paste from Excel, enable ‘Use Override Triangle’ to use this triangle in subsequent calculations.\n\n **Triangles – Selected:**This section shows the triangle currently being used in the analysis, whether sourced from Raw Data or Manual Input. Review the calculated development factors.\n\n **Triangles - Exclusions (Optional):** Use this section if development factors need to be excluded from the calculations, for example where a large claim has distorted experience.\nClick ‘Setup Exclusions Triangle for Use’. Enter **1** in any cell to exclude that development factor. Excluded factors will appear with a strikethrough in the Selected triangle.\n\n **Triangles – Averages:** Displays various averaging periods, all-year is selected by default.\n\n **Algorithmic Development and Overrides (Optional):**To change the selected average, update the dropdown ‘Selected Average Option Input’ and review the resulting development pattern.\nTo override individual development factors, enter factors in the ‘Experience – Override’ row. It will immediately be applied to your selected pattern, please review before continuing.\n\n **Finalise Development Pattern**\nClick ‘Update Burning Cost Pattern’ to use the resulting development pattern in the burning cost calculations.", optionality="optional", view={"label": "Triangles Instructions", "read_only": True, "multiline": True}),
            "triangle_claim_count_instructions": hx.Str(mode="input", default="**Triangles User Guide**\nTriangles are cumulative by default. Change the toggle to Incremental if required.\n\n **Triangles - Raw Data:** If transactional claims data has been provided, the triangle will populate automatically.\n\n **Triangles - Manual Input (Optional):**Only use this section if the triangle cannot be built from Raw Data or an alternative triangle is required.\nEnter the triangle as-at date, enter the number of treaty years, click ‘Setup Override Triangle’.\nEnter data manually or paste from Excel, enable ‘Use Override Triangle’ to use this triangle in subsequent calculations.\n\n **Triangles – Selected:**This section shows the triangle currently being used in the analysis, whether sourced from Raw Data or Manual Input. Review the calculated development factors.\n\n **Triangles - Exclusions (Optional):** Use this section if development factors need to be excluded from the calculations, for example where a large claim has distorted experience.\nClick ‘Setup Exclusions Triangle for Use’. Enter **1** in any cell to exclude that development factor. Excluded factors will appear with a strikethrough in the Selected triangle.\n\n **Triangles – Averages:** Displays various averaging periods, all-year is selected by default.\n\n **Algorithmic Development and Overrides (Optional):**To change the selected average, update the dropdown ‘Selected Average Option Input’ and review the resulting development pattern.\nTo override individual development factors, enter factors in the ‘Experience – Override’ row. It will immediately be applied to your selected pattern, please review before continuing.\n\n **Finalise Development Pattern**\nClick ‘Update Burning Cost Pattern’ to use the resulting development pattern in the burning cost calculations.", optionality="optional", view={"label": "Triangles Instructions", "read_only": True, "multiline": True}),
            "triangle_per_layer_instructions": hx.Str(mode="input", default="**Triangles User Guide**\nTriangles are cumulative by default. Change the toggle to Incremental if required.\n\n **Triangles - Raw Data:** If transactional claims data has been provided, the triangle will populate automatically.\n\n **Triangles - Manual Input (Optional):**Only use this section if the triangle cannot be built from Raw Data or an alternative triangle is required.\nEnter the triangle as-at date, enter the number of treaty years, click ‘Setup Override Triangle’.\nEnter data manually or paste from Excel, enable ‘Use Override Triangle’ to use this triangle in subsequent calculations.\n\n **Triangles – Selected:**This section shows the triangle currently being used in the analysis, whether sourced from Raw Data or Manual Input. Review the calculated development factors.\n\n **Triangles - Exclusions (Optional):** Use this section if development factors need to be excluded from the calculations, for example where a large claim has distorted experience.\nClick ‘Setup Exclusions Triangle for Use’. Enter **1** in any cell to exclude that development factor. Excluded factors will appear with a strikethrough in the Selected triangle.\n\n **Triangles – Averages:** Displays various averaging periods, all-year is selected by default.\n\n **Algorithmic Development and Overrides (Optional):**To change the selected average, update the dropdown ‘Selected Average Option Input’ and review the resulting development pattern.\nTo override individual development factors, enter factors in the ‘Experience – Override’ row. It will immediately be applied to your selected pattern, please review before continuing.\n\n **Finalise Development Pattern**\nClick ‘Update Burning Cost Pattern’ to use the resulting development pattern in the burning cost calculations.", optionality="optional", view={"label": "Triangles Instructions", "read_only": True, "multiline": True}),
            "info_by_01": hx.Str(mode="input", default="", optionality="optional", view={"label": "", "read_only": True, "multiline": True}),
            "info_by_02": hx.Str(mode="input", default="", optionality="optional", view={"label": "", "read_only": True, "multiline": True}),
            "info_by_03": hx.Str(mode="input", default="", optionality="optional", view={"label": "", "read_only": True, "multiline": True}),
            "info_by_04": hx.Str(mode="input", default="", optionality="optional", view={"label": "", "read_only": True, "multiline": True}),
            "info_by_05": hx.Str(mode="input", default="", optionality="optional", view={"label": "", "read_only": True, "multiline": True}),
            
            

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