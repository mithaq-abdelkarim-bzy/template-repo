import hx_data_schema as hx
from algorithms.data_schema.sch_utilities import thousands_format, percent_format, integer_format

### --- DEFINING THE NODES HERE SO THAT THEIR PROPERTIES ARE DYNAMICALLY ACCESSIBLE BY THE RATING ALGORITHM --- ###

### --- EXPOSURE --- ###
validation_cols = [
        "no_lives", 
        "sex", 
        "age_attained", 
        "salary", 
        "salary_multiple",
        "sum_insured",
        "nationality", 
        "location", 
        "region",
        "occupation_code"
        ]

exposure_dict = {   
    "country_finder": hx.Str(mode="input", default=None, optionality="optional", options_table="lstCountry", options_column="lstCountry", view={"label": "Country Finder"}),
    "data_check": hx.Str(mode="output"),
    "region_warning": hx.Str(mode="output"),
    "show_check_cols": hx.Bool(mode="input", default=False, view={"label": "Validate Data"}),
    "show_exposure_map": hx.Bool(mode="input", default=False, view={"label": "Show Exposure Map"}),
    "show_adb": hx.Bool(mode="output"),
    "show_ti": hx.Bool(mode="output"),
    "show_ci": hx.Bool(mode="output"),
    "show_re": hx.Bool(mode="output"),
    "check_col_labels": hx.Structure(children={
        (col + "_check_label"): hx.Str(mode="output") for col in validation_cols
    }),
    # Group
    "lives": hx.List(mode="input", async_input=["simulate_years_task"], children={
        "no_lives": hx.Int(mode="input", default=1, async_input=["rarc_task"], validation={"min_value": 1}, view={"label": "# Lives", "group": "Inputs"}), 
        "sex": hx.Str(mode="input", default="M", async_input=["rarc_task"], options=["M", "F"], allow_custom_value=True, view={"label": "Sex", "group": "Inputs"}), 
        "age_attained": hx.Int(mode="input", default=1, async_input=["rarc_task"], validation={"min_value": 0}, view={"label": "Age\nAttained", "group": "Inputs"}), 
        "salary": hx.Float(mode="input", default=1, async_input=["rarc_task"], validation={"min_value": 0}, view={"label": "Salary", "format": thousands_format(0), "group": "Inputs"}), 
        "salary_multiple": hx.Float(mode="input", default=1, async_input=["rarc_task"], validation={"min_value": 0}, view={"label": "Salary\nMultiple", "format": thousands_format(0), "group": "Inputs"}),
        "sum_insured": hx.Float(mode="output", async_input=["simulate_years_task"], view={"label": "Sum\nInsured", "format": thousands_format(0), "group": "Inputs"}),
        "nationality": hx.Str(mode="input", default="United Kingdom", async_input=["rarc_task"], options_table="lstCountry", options_column="lstCountry", allow_custom_value=True, view={"label": "Nationality", "group": "Inputs"}),
        "location": hx.Str(mode="input", default="United Kingdom", async_input=["rarc_task"], options_table="lstCountry", options_column="lstCountry", allow_custom_value=True,  view={"label": "Location", "group": "Inputs"}),
        "region": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality ="optional", options_data="../region_options_list", options_field="region_options", allow_custom_value=True,  view={"label": "Region", "group": "Inputs"}),
        "occupation_code": hx.Int(mode="input", default=1, async_input=["rarc_task"], options_table="tblOccupation", options_column="Occupation code", allow_custom_value=True, view={"label": "Occupation\nCode", "group": "Inputs"}),
        
        **{(col + "_check"): hx.Str(mode="output", view={"label": "Error", "group": "Inputs"}) for col in validation_cols},

        "region_options_list": hx.List(mode="output", children = {
            "region_options": hx.Str(mode = "output")
        }),

        "db_qx": hx.Float(mode="output", async_input=["simulate_years_task"], view={"label": "Pure Risk\nRate, qx", "format": thousands_format(2), "group": "Death Benefit"}),
        "db_expected_loss_cost_pre_uw_adj": hx.Float(mode="output", view={"label": "Expected\nLoss Cost", "format": thousands_format(0), "group": "Death Benefit"}),
        "db_technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Model\nPremium\n(Gross)", "format": thousands_format(0), "group": "Death Benefit"}),
        "db_expected_loss_cost": hx.Float(mode="output", view={"label": "UW Adj\nExpected\nLoss Cost", "format": thousands_format(0), "group": "Death Benefit"}),
        "db_technical_premium": hx.Float(mode="output", view={"label": "UW Adj\nModel\nPremium\n(Gross)", "format": thousands_format(0), "group": "Death Benefit"}),
        
        "adb_qx": hx.Float(mode="output", view={"label": "Pure\nRisk\nRate", "format": thousands_format(2), "group": "Additional Death Benefit"}),
        "adb_expected_loss_cost_pre_uw_adj": hx.Float(mode="output", view={"label": "Expected\nLoss Cost", "format": thousands_format(0), "group": "Additional Death Benefit"}),
        "adb_technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Model\nPremium\n(Gross)", "format": thousands_format(0), "group": "Additional Death Benefit"}),
        "adb_expected_loss_cost": hx.Float(mode="output", view={"label": "UW Adj\nExpected\nLoss Cost", "format": thousands_format(0), "group": "Additional Death Benefit"}),
        "adb_technical_premium": hx.Float(mode="output", view={"label": "UW Adj\nModel\nPremium\n(Gross)", "format": thousands_format(0), "group": "Additional Death Benefit"}),
        
        "ti_cover": hx.Bool(mode="output", view={"label": "TI Cover", "group": "Terminal Illness"}),
        "ti_proportion": hx.Float(mode="output", view={"label": "Proportion\nTI", "format": percent_format(1), "group": "Terminal Illness"}),
        "ti_rate": hx.Float(mode="output", view={"label": "TI Rate", "format": thousands_format(2), "group": "Terminal Illness"}),
        "ti_expected_loss_cost_pre_uw_adj": hx.Float(mode="output", view={"label": "Expected\nLoss Cost", "format": thousands_format(0), "group": "Terminal Illness"}),
        "ti_technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Model\nPremium\n(Gross)", "format": thousands_format(0), "group": "Terminal Illness"}),
        "ti_expected_loss_cost": hx.Float(mode="output", view={"label": "UW Adj\nExpected\nLoss Cost", "format": thousands_format(0), "group": "Terminal Illness"}),
        "ti_technical_premium": hx.Float(mode="output", view={"label": "UW Adj\nModel\nPremium\n(Gross)", "format": thousands_format(0), "group": "Terminal Illness"}),

        "ci_cover": hx.Bool(mode="output", view={"label": "CI Cover", "group": "Critical Illness"}),
        "ci_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(2), "group": "Critical Illness"}),
        "ci_sum_insured": hx.Float(mode="output", view={"label": "Sum\nInsured", "format": thousands_format(), "group": "Critical Illness"}),
        "ci_sum_insured_post_cap": hx.Float(mode="output", view={"label": "Sum\nInsured\nPost Cap", "format": thousands_format(), "group": "Critical Illness"}),
        "ci_expected_loss_cost_pre_uw_adj": hx.Float(mode="output", view={"label": "Expected\nLoss Cost", "format": thousands_format(0), "group": "Critical Illness"}),
        "ci_technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Model\nPremium\n(Gross)", "format": thousands_format(0), "group": "Critical Illness"}),
        "ci_expected_loss_cost": hx.Float(mode="output", view={"label": "UW Adj\nExpected\nLoss Cost", "format": thousands_format(0), "group": "Critical Illness"}),
        "ci_technical_premium": hx.Float(mode="output", view={"label": "UW Adj\nModel\nPremium\n(Gross)", "format": thousands_format(0), "group": "Critical Illness"}),

        "re_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(2), "group": "Repatriation Expenses"}),
        "re_expected_loss_cost_pre_uw_adj": hx.Float(mode="output", view={"label": "Expected\nLoss Cost", "format": thousands_format(0), "group": "Repatriation Expenses"}),
        "re_technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Model\nPremium\n(Gross)", "format": thousands_format(0), "group": "Repatriation Expenses"}),
        "re_expected_loss_cost": hx.Float(mode="output", view={"label": "UW Adj\nExpected\nLoss Cost", "format": thousands_format(0), "group": "Repatriation Expenses"}),
        "re_technical_premium": hx.Float(mode="output", view={"label": "UW Adj\nModel\nPremium\n(Gross)", "format": thousands_format(0), "group": "Repatriation Expenses"}),

        "no_claim_prob": hx.Float(mode="output", view={"label": "Probability\nof no claims", "format": percent_format(3)}),
    }),
    # Individual
    "life": hx.List(mode="input", max_element_count=1, children={
        "age_next_bday": hx.Int(mode="input", default=1, validation={"min_value": 1}, view={"label": "Age Next Birthday"}),
        "age_attained": hx.Int(mode="output", view={"label": "Age Attained"}),
        "sum_insured": hx.Float(mode="input", default=0, validation={"min_value": 0, "max_value": 5000000}, view={"label": "Sum Insured", "format": thousands_format(0)}),
        "nationality": hx.Str(mode="input", default="United Kingdom", options_table="RGAcountries", options_column="Country", view={"label": "Nationality"}),
        "location": hx.Str(mode="input", default="United Kingdom", options_table="RGAcountries", options_column="Country", view={"label": "Location"}),
        "coverage": hx.Str(mode="input", default="Death natural causes", options=["Death natural causes", "Death any cause"], view={"label": "Coverage"}),
        "smoker_status": hx.Str(mode="input", default="Non-smoker", options=["Non-smoker", "Smoker"], view={"label": "Smoker Status"}),  
        "term": hx.Int(mode="input", default=1, options=[1, 2, 3, 4, 5], view={"label": "Term"}),
        "rga_rate": hx.Float(mode="output", view={"label": "Rate", "format": thousands_format(3)}),
        "rga_premium": hx.Float(mode="output", view={"label": "Premium (Net of Brokerage)", "format": thousands_format()}),
        "gross_rga_premium": hx.Float(mode="output", view={"label": "Premium (Gross of Brokerage)", "format": thousands_format(0)}),
        "brokerage_ri_amount": hx.Float(mode="output", view={"label": "RI Brokerage Amount", "format": thousands_format(0)}),
        "bzl_rate": hx.Float(mode="output", view={"label": "Rate", "format": thousands_format(3)}),
        "bzl_premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
    }),
    # For map charts
    "lives_by_nation": hx.List(mode="output", children={
        "no_lives": hx.Int(mode="output", view={"label": "# Lives"}),
        "sum_insured": hx.Float(mode="output", view={"label": "Sum\nInsured", "format": thousands_format(0)}), 
        "total_sum_insured": hx.Float(mode="output", view={"label": "Total\nSum Insured", "format": thousands_format(0)}), 
        "nationality": hx.Str(mode="output", view={"label": "Country"}),
        "country_iso3": hx.Str(mode="output", view={"label": "Country"}), 
    }),
    "lives_by_location": hx.List(mode="output", children={
        "no_lives": hx.Int(mode="output", view={"label": "# Lives"}), 
        "sum_insured": hx.Float(mode="output", view={"label": "Sum\nInsured", "format": thousands_format(0)}), 
        "total_sum_insured": hx.Float(mode="output", view={"label": "Total\nSum Insured", "format": thousands_format(0)}), 
        "location": hx.Str(mode="output", view={"label": "Country"}),
        "country_iso3": hx.Str(mode="output", view={"label": "Country"}),
    }),
}

### --- COVERAGES --- ###
cover_selection_dict = {
    "cover_selection": hx.Structure(children={
        "are_db_fields_full": hx.Bool(mode="output"),
        "are_ci_fields_full": hx.Bool(mode="output"),
        "are_agg_limits_full": hx.Bool(mode="output"),
        "agg_limits_check_show": hx.Bool(mode="output"),
        "agg_limits_check_message": hx.Str(mode="output")
    }),
}

coverages_dict = {
    "death": {"label": "Death Benefit"},
    "additional_death": {"label": "Additional\nDeath Benefit"},
    "terminal_illness": {"label": "Terminal\nIllness"},
    "critical_illness": {"label": "Critical\nIllness"},
    "repat_exp": {"label": "Repatriation\nExpenses"}
}

cvg_fields_dict = {
    "el_cost_pre_uw_pre_exp": hx.Float(mode="output", view={"label": "Expected Loss Cost", "info": "Includes NMP adjustment", "format": thousands_format()}),
    "el_rate_pre_uw_pre_exp": hx.Float(mode="output", view={"label": "Expected Loss Rate per Mille (RPM)", "format": thousands_format(2)}),
    "el_cost_post_uw_pre_exp": hx.Float(mode="output", view={"label": "UW Adj Expected Loss Cost", "format": thousands_format()}),
    "el_rate_post_uw_pre_exp": hx.Float(mode="output", view={"label": "UW Adj Expected Loss RPM", "format": thousands_format(2)}),
    "expected_loss_cost": hx.Float(mode="output", view={"label": "Expected Loss Post Experience", "format": thousands_format()}),
    "uw_adj": hx.Float(mode="input", default=1, view={"label": "UW Risk Adjustment", "format": thousands_format(2)}),
    "benchmark_rate": hx.Float(mode="output", async_input=["simulate_years_task"], view={"label": "Gross Benchmark RPM","format": thousands_format(2)}),
    "technical_rate": hx.Float(mode="output", view={"label": "Gross Technical RPM","format": thousands_format(2)}),
    "quoted_rate": hx.Float(mode="input", default=0, async_input=["simulate_years_task"], view={"label": "Commercial RPM", "format": thousands_format(2)}),
}

death_dict = {
    "are_fields_full": hx.Bool(mode="output"),
    "label": hx.Str(mode="output"),
    "cover_type": hx.Str(mode="input", default="Nat Cause", async_input=["rarc_task"], async_output=["start_renewal_task"], options=["Any Cause", "Nat Cause"], view={"label": "Deaths covered"}),
    "accidental_death_adj": hx.Str(mode="input", default="No adjustment", async_input=["rarc_task"], async_output=["start_renewal_task"], options=["No adjustment", "Loading", "Discount"], view={"label": "Accidental death adjustment", "info": "For example, accidental motality for a builder in the UK may be 1.1x larger than the average accidental mortality. However, in a country with less strict building regulations it may be 1.2x larger. Select 'loading' in this case."}),
    "sick_affluence": hx.Bool(mode="input", default=False, async_input=["rarc_task"], async_output=["start_renewal_task"], view={"label": "Sickness - affluence correction", "info": "Sets nationality to UK and therefore typically decreases sickness mortality rate."}),
    "sick_weight_to_nationality": hx.Float(mode="input", default=0.98, async_input=["rarc_task"], async_output=["start_renewal_task"], optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "Sickness rate - weight to nationality", "format": percent_format(), "info": "When someone moves to a location that is different to their native country, sickness mortality gradually change from nationality mortality to location mortality.\nUse 100% if the insureds have just moved to new country. Use 0% if the insureds have lived in new country a long time."}),
    "accidental_death_rate": hx.Str(mode="input", default="Base - UK", async_input=["rarc_task"], async_output=["start_renewal_task"], options=["Base - UK", "More accidents", "More sickness"], view={"label": "Proportion of deaths which are accidents"}),
    "el_cost_no_sim": hx.Float(mode="output", view={"label": "DB Expected Loss Cost - Pre Agg", "info": "Without experience adjustment", "format": thousands_format()}),
    "el_cost_post_sim_pre_agg": hx.Float(mode="output", async_output=["simulate_years_task"], view={"label": "DB Expected Loss Cost - Pre Agg", "format": thousands_format()}),
    "el_cost_post_sim": hx.Float(mode="override", async_output=["simulate_years_task"], view={"label": "DB Expected Loss Cost - Post Agg", "format": thousands_format()}),
    "agg_impact_on_el": hx.Float(mode="output", view={"label": "Impact of Agg on Expected Loss", "format": percent_format(1)}),
    **cvg_fields_dict
}

additional_death_dict = {
    "is_covered": hx.Bool(mode="input", default=False, async_input=["rarc_task"], async_output=["start_renewal_task"], view={"label": "Additional death benefit?"}),
    **cvg_fields_dict
}

terminal_illness_dict = {
    "is_covered": hx.Bool(mode="input", async_input=["rarc_task"], async_output=["start_renewal_task"], default=False, view={"label": "Terminal illness?"}),
    "age_info": hx.Str(mode="input", default="Ages 18-70 only"),
    **cvg_fields_dict
}

critical_illness_dict = {
    "is_covered": hx.Bool(mode="input", async_input=["rarc_task"], async_output=["start_renewal_task"], default=False, view={"label": "Critical illness?"}),
    "age_info": hx.Str(mode="input", default="Ages 18-64 only"),
    "benefit": hx.Str(mode="input", default=None, async_input=["rarc_task"], async_output=["start_renewal_task"], optionality="optional", options=["Fixed", "Perc_salary"], view={"label": "Benefit"}),
    "benefit_amount_fixed": hx.Float(mode="input", async_input=["rarc_task"], async_output=["start_renewal_task"], default=None, optionality="optional", view={"label": "Benefit amount", "format": thousands_format()}),
    "benefit_amount_pct": hx.Float(mode="input", async_input=["rarc_task"], async_output=["start_renewal_task"], default=None, optionality="optional", view={"label": "Benefit amount", "format": percent_format()}),
    "show_benefit_amount": hx.Bool(mode="output"),
    "show_benefit_pct": hx.Bool(mode="output"),
    "cap_amount": hx.Float(mode="input", default=None, async_input=["rarc_task"], async_output=["start_renewal_task"], optionality="optional", view={"label": "Cap (amount)", "format": thousands_format(), "info": "Leave blank if no cap."}),
    "cap_pct": hx.Float(mode="input", default=None, async_input=["rarc_task"], async_output=["start_renewal_task"], optionality="optional", view={"label": "Cap (% salary)", "format": percent_format(1), "info": "Leave blank if no cap."}),
    **cvg_fields_dict
}

repat_exp_dict = {
    "is_covered": hx.Bool(mode="input", async_input=["rarc_task"], async_output=["start_renewal_task"], default=False, view={"label": "Repat exp?"}),
    **cvg_fields_dict
}

# Using the following dictionary as a subset of the data schema that is accessible in rating
all_coverages_dict = {
    "death": death_dict,
    "additional_death": additional_death_dict,
    "terminal_illness": terminal_illness_dict,
    "critical_illness": critical_illness_dict,
    "repat_exp": repat_exp_dict,
}

### --- LAYERS --- ###
pc_calcs_dict = {
    "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
    "net_profits": hx.Float(mode="output", view={"label": "Net Profits", "format": thousands_format()}),
    "pc_cost": hx.Float(mode="output", view={"label": "PC Cost", "format": thousands_format()}),
    "pc_load": hx.Float(mode="output", view={"label": "PC Load", "format": thousands_format()}),
    "payment": hx.Float(mode="output", view={"label": "Payment", "format": thousands_format()}),
}

ncb_calcs_dict = {
    "premium": hx.Float(mode="output", view={"label": "Premium", "format": thousands_format()}),
    "ncb_load": hx.Float(mode="output", view={"label": "NCB Load", "format": thousands_format()}),
    "ncb_premium": hx.Float(mode="output", view={"label": "Post-NCB Premium", "format": thousands_format()}),
}

pc_dict = {
    "gross": hx.Structure(view={"label": "Gross"}, children=pc_calcs_dict),
    "net": hx.Structure(view={"label": "Net"}, children=pc_calcs_dict),
}

ncb_dict = {
    "gross": hx.Structure(view={"label": "Gross"}, children=ncb_calcs_dict),
    "net": hx.Structure(view={"label": "Net"}, children=ncb_calcs_dict),
}

totals_dict = {
    "el_cost_pre_uw_pre_exp": hx.Float(mode="output", view={"label": "Expected Loss Cost", "info": "Includes NMP adjustment", "format": thousands_format()}),
    "el_rate_pre_uw_pre_exp": hx.Float(mode="output", view={"label": "Expected Loss Rate per Mille (RPM)", "format": thousands_format(2)}),
    "el_cost_post_uw_pre_exp": hx.Float(mode="output", view={"label": "UW Adj Expected Loss Cost", "format": thousands_format()}),
    "el_rate_post_uw_pre_exp": hx.Float(mode="output", view={"label": "UW Adj Expected Loss RPM", "format": thousands_format(2)}),
    "expected_loss_cost": hx.Float(mode="output", view={"label": "Expected Loss Post Experience", "format": thousands_format()}),
    "uw_adj": hx.Float(mode="output", view={"label": "UW Risk Adjustment", "format": thousands_format(2)}),
    "uw_adj_impact": hx.Float(mode="output", view={"label": "Implied Commercial Adjustment", "format": thousands_format(2)}),
    "benchmark_premium": hx.Float(mode="output", async_input=["rarc_task","simulate_years_task"], view={"label": "Gross Benchmark Premium","format": thousands_format()}),
    "benchmark_rate": hx.Float(mode="output",  async_input=["rarc_task","simulate_years_task"], view={"label": "Gross Benchmark RPM","format": thousands_format(2)}),
    "technical_premium": hx.Float(mode="output", view={"label": "Gross Technical Premium","format": thousands_format()}),
    "technical_rate": hx.Float(mode="output", view={"label": "Gross Technical RPM","format": thousands_format(2)}),
    "quoted_rate": hx.Float(mode="output", async_input=["simulate_years_task"], view={"label": "Commercial RPM", "format": thousands_format(2)}),
    "quoted_premium": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Commercially Achieved Premium", "format": thousands_format()}),
   }

layers_dict = {
    # --- For Individual
    "brokerage_ri": hx.Float(mode="input", default=0, validation={"min_value": 0, "max_value": 1}, view={"label": "Brokerage (Reinsurance)", "format": percent_format(1)}),
    "brokerage_label": hx.Str(mode="output"),
    "rga_load_mult": hx.Float(mode="input", default=0, view={"label": "RGA Loading (x)", "format": percent_format(1)}),
    "rga_load_add": hx.Float(mode="input", default=0, view={"label": "RGA Loading (+)", "format": thousands_format(3)}),
    "written_line_input": hx.Float(mode="input", default=0, validation={"min_value": 0, "max_value": 1}, view={"label": "Written Line", "format": percent_format(1)}, async_output=["start_renewal_task"]),
    "quoted_premium_net": hx.Float(mode="output", view={"label": "Gross Premium Retained", "format": thousands_format()}),
    "el_label": hx.Str(mode="input", default="EL Cost to Beazley"),
    "quoted_rate": hx.Float(mode="output", async_input=["simulate_years_task"], view={"label": "Gross Quoted Rate", "format": thousands_format(3)}),
    "quoted_premium_ind": hx.Float(mode="override", view={"label": "Gross Quoted Premium - Overridable", "format": thousands_format()}),

    # --- For Group
    "expe_adj_label": hx.Str(mode="input", default="After experience adjustment"),
    "model_premium_net": hx.Float(mode="output", view={"label": "Net Model Premium", "format": thousands_format()}),
    "no_claim_prob": hx.Float(mode="output", view={"label": "Probability of no claims", "format": percent_format(1)}),
    "expected_pc": hx.Float(mode="output", view={"label": "Expected PC", "format": thousands_format(), "info": "Based on Commercially Achieved Premium"}),
    "expected_ncb": hx.Float(mode="output", view={"label": "Expected NCB", "format": thousands_format(), "info": "Based on Commercially Achieved Premium"}),
    # Additional summary stats
    "lives_wtd_avg_age": hx.Float(mode="output", view={"label": "Weighted Avg Age (Lives)", "format": {**thousands_format(2), **{"trimMantissa": True}}}),
    "si_wtd_avg_age": hx.Float(mode="output", view={"label": "Weighted Avg Age (SI)", "format": {**thousands_format(2), **{"trimMantissa": True}}}),
    "max_age": hx.Float(mode="output", view={"label": "Max Age", "format": thousands_format()}),
    "min_age": hx.Float(mode="output", view={"label": "Min Age", "format": thousands_format()}),
    "lives_wtd_avg_salary": hx.Float(mode="output", view={"label": "Weighted Avg Salary (Lives)", "format": thousands_format()}),
    "max_salary": hx.Float(mode="output", view={"label": "Max Salary", "format": thousands_format()}),
    "min_salary": hx.Float(mode="output", view={"label": "Min Salary", "format": thousands_format()}),
    "lives_wtd_avg_si": hx.Float(mode="output", view={"label": "Weighted Avg Sum Insured (Lives)", "format": thousands_format()}),
    "max_si": hx.Float(mode="output", view={"label": "Max Sum Insured", "format": thousands_format()}),
    "min_si": hx.Float(mode="output", view={"label": "Min Sum Insured", "format": thousands_format()}),
    "total_no_lives": hx.Float(mode="output", view={"label": "Total Number of Lives", "format": thousands_format()}),
    "exp_no_deaths_per_thousand": hx.Float(mode="output", view={"label": "Expected number of deaths per 1000", "format": {**thousands_format(2), **{"trimMantissa": True}}, "info": "Need to adjust for the number of lives in  each group and the country."}),
    "exp_no_deaths": hx.Float(mode="output", view={"label": "Expected number of deaths", "format": {**thousands_format(2), **{"trimMantissa": True}}}),
    "avg_cost": hx.Float(mode="output", view={"label": "Average Cost", "format": thousands_format(), "info": "For death only, cost is fixed so adj factors are frequency scalars."}),
    "sd_cost": hx.Float(mode="output", view={"label": "SD of Cost", "format": thousands_format()}),
    # Agg limits
    "temp": hx.Structure(children={
        "aggregate_limit": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "aggregate_deductible": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "is_agg_priced": hx.Bool(mode="output", async_output=["simulate_years_task"]),
        "task_update_msg": hx.Str(mode="output", async_output=["simulate_years_task"]),
        "exp_pc_payment_net_sim": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "exp_pc_payment_gross_sim": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "exp_ncb_payment_net_sim": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "exp_ncb_payment_gross_sim": hx.Float(mode="output", async_output=["simulate_years_task"]),
        # NEW
        "exp_pc_payment_quoted_net_sim": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "exp_pc_payment_quoted_gross_sim": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "exp_ncb_payment_quoted_net_sim": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "exp_ncb_payment_quoted_gross_sim": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "profit_commission": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "pc_expenses": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "pc_deficit": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "ncb_pct": hx.Float(mode="output", async_output=["simulate_years_task"]),
        "total_quoted_rate_excl_pc_ncb": hx.Float(mode="output", async_output=["simulate_years_task"]),
    }),

    # PC and NCB calcs
    "pc": hx.Structure(children={
        "model": hx.Structure(children=pc_dict),      
        "quoted": hx.Structure(children=pc_dict),
    }),
    "ncb": hx.Structure(children={
        "model": hx.Structure(children=ncb_dict),      
        "quoted": hx.Structure(children=ncb_dict),
    }),

    # Totals for Premium Summary
    "totals": hx.Structure(children={
        "total_ex_pc_ncb": hx.Structure(view={"label": "Total\n(ex PC & NCB)"}, children=totals_dict),
        "pc": hx.Structure(view={"label": "Profit\nCommission"}, children=totals_dict),
        "ncb": hx.Structure(view={"label": "NCB"}, children=totals_dict),
        "total": hx.Structure(view={"label": "Total"}, children=totals_dict),
    })
}

