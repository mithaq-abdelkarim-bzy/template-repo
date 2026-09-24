# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 6
tp_summary_layers = 1

benchmark_lr = 0.7

#FID constants
ne_deviation_min = -0.4
ne_deviation_max = 0.4
#values for benchmark
prior_claim_activity_min = 0.75
prior_claim_activity_max = 1.25
additional_risk_characteristics_min = 0.75
additional_risk_characteristics_max = 1.25
#values for foreign charge
foreign_charge_min = 1.00
foreign_charge_max = 1.25
foreign_charge_output_min = 0.25
foreign_charge_output_multiplier = 0.05
#expense rating
ny_expense_min = 1
ny_expense_max = 1.15        
basic_expense_min = 0.85
basic_expense_max = 1.15
alt_expense_min = 1
alt_expense_max = 1
requirements_ny_cutoff = 1000
#retention
default_retention = 5000
maximum_retention = 100000
retention_fid_min = 0
retention_ratio_max = 4
retention_multiplier = 50
retention_divider = 1000000
florida_ratio = 3
#limit compression
limit_compression_value = 5000000
limit_compression_multiplier = 0.05
criteria_list_compression_factor = 1.1
#adl
additional_defence_limit_factor_default = 0.8
additional_defence_limit_value_default = 0


#vcfdc
vcfdc_default = 100000
sub_limit_to_use_default = 500000
vcfdc_max = 500000
vcfdc_min = 100000
#Aggregate_limit
aggregate_limit_min = 250000
aggregate_limit_max = 30000000
aggregate_limit_default = 0
#schedule_rating
schedule_rating_min = 500
#active particpants factor
active_particpants_factor_default = 0
active_particpants_factor_min = 0
active_particpants_factor_max = 1
#base assets
base_assets_default = 0
base_assets_min = 0
base_assets_max = 1000000000
base_premium_assets_division = 1000
assets_base_rate_divider = 1000
#base employee
base_employee_default = 0
base_employee_min = 0
base_employee_max = 99999999
#esop
esop_input = 25000
#retention_ib
retention_ib_divider = 1000000
retention_ib_default_lower = 5000
retention_ib_default_upper = 100000
retention_fi_default = 0
#assets contribution
assets_contributions_default = 0
#employees
employees_default = 0
#fiduciary charge
fiduciary_charge_default = 0
fiduciary_charge_multiplier = 0.05
fiduciary_ny_value = 10000


#PCL constants
#assets
assets_base_rate_pcl_default = 1
assets_base_rate_pcl_min = 1
assets_base_rate_pcl_max = 999999999999
revenue_base_rate_pcl_min = 1
revenue_base_rate_pcl_max = 999999999999
#retention
retention_pcl_default = 0
retention_pcl_min_choice_1 = 0
retention_pcl_min_choice_2 = 5000
retention_pcl_min_choice_3 = 10000
retention_pcl_max_choice_1 = 250000
retention_pcl_max_choice_2 = 1000000
retention_pcl_max_choice_3 = 1000000
#limit
aggregate_limit_pcl_default = 0
aggregate_limit_pcl_min = 250000
aggregate_limit_pcl_max = 25000000
#retention
retention_pcl_min = 0
retention_pcl_max = 1000000

#cob
tableA_limit_pcl = 250000000
#punitive damages
punitive_damages_yes_min_pcl = 0.8
punitive_damages_yes_max_pcl = 1
punitive_damages_no_pcl = 1
punitive_damages_default_pcl = 0.9
punitive_damages_apply_to_all_pcl = 0.9
#ib guideline retention
ib_guideline_retention_default= 0
ib_basis = "Revenue"
#ib non admitted
ib_non_admitted_default = 0
#bnch prior activity
bnch_prior_min = -0.25
bnch_prior_max = 3



#epl
states_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District_of_Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New_Hampshire", "New_Jersey", "New_Mexico", "New_York_metro", "New_York_non_metro", "North_Carolina", "North_Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode_Island", "South_Carolina", "South_Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West_Virginia", "Wisconsin", "Wyoming"]

aggregate_limit_epl_min = 250000
aggregate_limit_epl_max = 30000000
retention_rate_epl_min = 5000
retention_rate_epl_max = 9999999
london_brokerage = 0.265
guideline_retention_min = 750000
bnch_risk_characteristics_min = -0.25
bnch_risk_characteristics_max = 3.0
bnch_pro_claim_activity_min = -0.25
bnch_pro_claim_activity_max = 3.0
bnch_hr_policies_min = -0.10
bnch_hr_policies_max = 0.1
bnch_turnover_ma_layoffs_min = 0
bnch_turnover_ma_layoffs_max = 0.25
bnch_financial_strength_min = -0.10
bnch_financial_strength_max = 0.1
bnch_demographic_min = -0.25
bnch_demographic_max = 0.25
client_coverage_not_purchased = 1
client_coverage_other = 1.25
adm_sch_rating_min = -0.25
adm_sch_rating_max = 0.25
adm_sch_rating_min_hi_ne = 0
adm_sch_rating_max_hi_ne = 0
adm_sch_rating_min_in = -0.1
adm_sch_rating_max_in = 0.1
adm_sch_rating_min_ny_la= -0.1
adm_sch_rating_max_ny_la = 0.1
adm_sch_rating_min_both = 0
adm_sch_rating_max_both = 0
adm_sch_rating_min_stability = -0.05
adm_sch_rating_max_stability = 0.05

coinsure_max_credit = 0.15

expected_loss_ratio = 0.7

excess_assumed_primary_brokerage = 0.15

#rate change
beazley_share = 1
weight_epl = 0.55
weight_fid = 0.1
weight_pcl = 0.35

#emojis
incomplete_column = "\U0000274C"  # Red X
#incomplete_column = "\U000026A0"  # Warning sign
complete_column = "\U00002705"  # Green Check

coverage_validation_mapping = {
    "epl": {
        "label": "EPL",
        "column_label_field": "required_epl_row_labels",
        "are_multiple_selected": lambda obj, val: setattr(obj, "is_multiple_epl_covers", val),
        "multiple_selected_error_msg": lambda obj, val: setattr(obj, "multiple_epl_covers_message", val),
    },
    "pcl": {
        "label": "PCL",
        "column_label_field": "required_pcl_row_labels",
        "are_multiple_selected": lambda obj, val: setattr(obj, "is_multiple_pcl_covers", val),
        "multiple_selected_error_msg": lambda obj, val: setattr(obj, "multiple_pcl_covers_message", val),
    },
    "fiduciary": {
        "label": "Fiduciary",
        "column_label_field": "required_fiduciary_row_labels",
        "are_multiple_selected": lambda obj, val: setattr(obj, "is_multiple_fiduciary_covers", val),
        "multiple_selected_error_msg": lambda obj, val: setattr(obj, "multiple_fiduciary_covers_message", val),
    }
}

def get_epl_admitted_factor_dict(statecode: str):
    if statecode == "CA":
        other_dict={
            "hr_policies": "EPL HR Policies Admitted Schedule Rating",
            "demographic_metro": "EPL Demographics/Metro Admitted Schedule Rating"
        }
        both_dict = {
            "management": "EPL Management Admitted Schedule Rating",
            "internal_controls": "EPL Internal Controls Admitted Schedule Rating",
            "cooperation": "EPL Cooperation Admitted Schedule Rating",
            "experience": "EPL Experience Admitted Schedule Rating",
            "staffing_turnover": "EPL Stafing Turnover Admitted Schedule Rating",
            "salary_structure": "EPL Salary Structure Admitted Schedule Rating"
        }
    elif statecode == "IN":
        other_dict={
            "demographic_metro": "EPL Demographics/Metro Admitted Schedule Rating"
        }
        both_dict = {
            "management": "EPL Management Admitted Schedule Rating",
            "internal_controls": "EPL Internal Controls Admitted Schedule Rating",
            "cooperation": "EPL Cooperation Admitted Schedule Rating",
            "experience": "EPL Experience Admitted Schedule Rating",
            "staffing_turnover": "EPL Stafing Turnover Admitted Schedule Rating",
            "salary_structure": "EPL Salary Structure Admitted Schedule Rating"
        }
    else:
        other_dict={
            "prior_claim_activity": "EPL Prior Claim Activity Admitted Schedule Rating",
            "turnover_rate": "EPL Turnover Rate Admitted Schedule Rating",
            "financial_strength": "EPL Financial Strength Admitted Schedule Rating",
            "hr_policies": "EPL HR Policies Admitted Schedule Rating",
            "demographic_metro": "EPL Demographics/Metro Admitted Schedule Rating"
        }
        both_dict = {}

    return other_dict, both_dict    