## General ##
# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 6

## Summary metrics ##
benchmark_lr = 0.7
elr = 0.6
plan_year = 2025
roc_target = 0.15

## Comments ##
comment_dropdown = [
    "Underwriter Rationale", 
    "General Comments", 
    "Claims History", 
    "T&C's",
    "Management and Corporate Governance",
    "Business / Financial Model Factors",
    "Significant Event Factors",
    "Stock Market Factors",
    "Derivative",
    "Regulatory",
    "M&A",
    "Underwriter Override Comment",
    "Underwriter Override Comment 2",
    "Underwriter Override Comment 3",
    "Market Cap Comment",
    "IPO Date Comment"
    ]


#comment_location = ["cds/standard_fields/uw_rationale", "cds/comment", "cds/claims_history", "cds/t_and_c_comment"]

## Admitted ##
# All steps which are not calculated
bici_steps = [
    "step_2_im",
    "step_3_mam",
    "step_4_pm",
    "step_5_qm",
    "step_6_cm",
    "step_7_fm",
    "step_8_em",
    "step_9_om",
    "step_10_lm",
    "step_11_chm",
    "step_12_sm",
    "step_13_edm",
    "step_14_spm",
    "step_16_pcm",
    "step_17_icm",
    "step_18a_fcp"
    ]

def get_baic_steps(is_california):
    if is_california:
        baic_steps = [
            "step_2_im",
            "step_3_mam",
            "step_4_pm",
            "step_5_qm",
            "step_6_cm",
            "step_7_fm",
            "step_8_em",
            "step_9_om",
            "step_10_lm",
            "step_11_chm",
            "step_12_sm",
            "step_13_edm",
            "step_14_spm",
            "step_16_pcm",
            "step_17_icm",
            "step_18_yo_ca",
            "step_19_saf",
            "step_19a_fcp",
            "step_20a_fwic",
            "step_20b_iglp",
            "step_20c_rii",
            "step_20d_str",
            "step_20e_mcd",
            "step_20f_lre"
            ]
    else:
        baic_steps = [
            "step_2_im",
            "step_3_mam",
            "step_4_pm",
            "step_5_qm",
            "step_6_cm",
            "step_7_fm",
            "step_8_em",
            "step_9_om",
            "step_10_lm",
            "step_11_chm",
            "step_12_sm",
            "step_13_edm",
            "step_14_spm",
            "step_16_pcm",
            "step_17_icm",
            "step_18_yo",
            "step_19_saf",
            "step_19a_fcp",
            ]  

    return baic_steps        

# All steps excluding the final step
bici_all_steps = [
    "step_1_bpm",
    "step_2_im",
    "step_3_mam",
    "step_4_pm",
    "step_5_qm",
    "step_6_cm",
    "step_7_fm",
    "step_8_em",
    "step_9_om",
    "step_10_lm",
    "step_11_chm",
    "step_12_sm",
    "step_13_edm",
    "step_14_spm",
    "step_15_rm",
    "step_16_pcm",
    "step_17_icm",
    "step_18_llm"
]

baic_ca_input_steps = [
    "step_20a_fwic",
    "step_20b_iglp",
    "step_20c_rii",
    "step_20d_str",
    "step_20e_mcd",
    "step_20f_lre"
]

baic_ca_input_steps_numbers = [20, 21, 22, 23, 24, 25, 26] #this includes step_20_srf for the purposes of setting min max range

baic_ca_input_step_labels = [
    "Step 20a - Fit within Industry Classification",
    "Step 20b - Internal Governance & Loss Prevention",
    "Step 20c - Regulatory Investigations or Issues",
    "Step 20d - Susceptibility to Recession",
    "Step 20e - Major Customer Dependency",
    "Step 20f - Labor Relations Exposure",
]

def get_baic_all_steps(is_california):
    if is_california:
        baic_all_steps = [
            "step_1_bpm",
            "step_2_im",
            "step_3_mam",
            "step_4_pm",
            "step_5_qm",
            "step_6_cm",
            "step_7_fm",
            "step_8_em",
            "step_9_om",
            "step_10_lm",
            "step_11_chm",
            "step_12_sm",
            "step_13_edm",
            "step_14_spm",
            "step_15_clrm",
            "step_16_pcm",
            "step_17_icm",
            "step_18_yo",
            "step_19_saf",
            "step_20a_fwic",
            "step_20b_iglp",
            "step_20c_rii",
            "step_20d_str",
            "step_20e_mcd",
            "step_20f_lre",
            "step_20_srf"
            ]   
    else:
        baic_all_steps = [
            "step_1_bpm",
            "step_2_im",
            "step_3_mam",
            "step_4_pm",
            "step_5_qm",
            "step_6_cm",
            "step_7_fm",
            "step_8_em",
            "step_9_om",
            "step_10_lm",
            "step_11_chm",
            "step_12_sm",
            "step_13_edm",
            "step_14_spm",
            "step_15_clrm",
            "step_16_pcm",
            "step_17_icm",
            "step_18_yo",
            "step_19_saf"
            ]

    return baic_all_steps

def get_baic_calc_steps(is_california):
    '''
    Excludes the intermidiate 20a-f steps as only the summary factor is used in the final premium calc
    '''
    if is_california:
        baic_calc_steps = [
            "step_1_bpm",
            "step_2_im",
            "step_3_mam",
            "step_4_pm",
            "step_5_qm",
            "step_6_cm",
            "step_7_fm",
            "step_8_em",
            "step_9_om",
            "step_10_lm",
            "step_11_chm",
            "step_12_sm",
            "step_13_edm",
            "step_14_spm",
            "step_15_clrm",
            "step_16_pcm",
            "step_17_icm",
            "step_18_yo_ca",
            "step_19_saf",
            # "step_20a_fwic",
            # "step_20b_iglp",
            # "step_20c_rii",
            # "step_20d_str",
            # "step_20e_mcd",
            # "step_20f_lre",
            "step_20_srf"
            ]   
    else:
        baic_calc_steps = [
            "step_1_bpm",
            "step_2_im",
            "step_3_mam",
            "step_4_pm",
            "step_5_qm",
            "step_6_cm",
            "step_7_fm",
            "step_8_em",
            "step_9_om",
            "step_10_lm",
            "step_11_chm",
            "step_12_sm",
            "step_13_edm",
            "step_14_spm",
            "step_15_clrm",
            "step_16_pcm",
            "step_17_icm",
            "step_18_yo",
            "step_19_saf"
            ]

    return baic_calc_steps

#bici_all_steps = bici_steps + ["step_1_bpm", "step_15_rm", "step_18_llm"]
#biaic_all_steps = baic_steps + ["step_1_bpm", "step_15_clrm"]

# All other steps that don't need unique calc functions
bici_other_steps = [
    "step_3_mam",
    "step_4_pm",
    "step_5_qm",
    "step_6_cm",
    "step_7_fm",
    "step_8_em",
    "step_9_om",
    "step_10_lm",
    "step_11_chm",
    "step_12_sm",
    "step_13_edm",
    "step_14_spm",
    "step_16_pcm",
    "step_17_icm"
    ]
# Listed the numbers for these steps
bici_other_steps_nums = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17]
# Labels for the cds
bici_other_steps_labels = [
    "Step 3 - M&A", 
    "Step 4 - Profitability", 
    "Step 5 - Balance Sheet", 
    "Step 6 - Cash Flow", 
    "Step 7 - Restatements", 
    "Step 8 - Management Experience", 
    "Step 9 - Outside Directors", 
    "Step 10 - General Litigation", 
    "Step 11 - D&O Claim History", 
    "Step 12 - Shareholder Base", 
    "Step 13 - Equity or Debt", 
    "Step 14 - Stock Volatility", 
    "Step 16 - Private Company", 
    "Step 17 - Indemnifiable Coverage"]

# For the purposes of sch_admitted.py
baic_other_steps = [
    "step_3_mam",
    "step_4_pm",
    "step_5_qm",
    "step_6_cm",
    "step_7_fm",
    "step_8_em",
    "step_9_om",
    "step_10_lm",
    "step_11_chm",
    "step_12_sm",
    "step_13_edm",
    "step_14_spm",
    "step_16_pcm",
    "step_17_icm",
    "step_18_yo",
    "step_19_saf",
    "step_18_yo_ca"
    ]
baic_other_steps_nums = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27]
baic_other_steps_labels = [
    "Step 3 - M&A", 
    "Step 4 - Profitability", 
    "Step 5 - Balance Sheet", 
    "Step 6 - Cash Flow", 
    "Step 7 - Restatements", 
    "Step 8 - Management Experience", 
    "Step 9 - Outside Directors", 
    "Step 10 - General Litigation", 
    "Step 11 - D&O Claim History", 
    "Step 12 - Shareholder Base", 
    "Step 13 - Equity or Debt", 
    "Step 14 - Stock Volatility", 
    "Step 16 - Private Company", 
    "Step 17 - Indemnifiable Coverage",
    "Step 18 - Years in Operation",
    "Step 19 - Side A Factor",
    "Step 18 - Years in Operation"
    ]

# depending on whether ca is state
def get_baic_other(is_california):
    if is_california:
        baic_other_steps = [
            "step_3_mam",
            "step_4_pm",
            "step_5_qm",
            "step_6_cm",
            "step_7_fm",
            "step_8_em",
            "step_9_om",
            "step_10_lm",
            "step_11_chm",
            "step_12_sm",
            "step_13_edm",
            "step_14_spm",
            "step_16_pcm",
            "step_17_icm",
            "step_18_yo_ca",
            "step_19_saf",
            "step_20a_fwic",
            "step_20b_iglp",
            "step_20c_rii",
            "step_20d_str",
            "step_20e_mcd",
            "step_20f_lre",
            #"step_20_srf",
            ]
        baic_other_steps_nums = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 27, 19, 20, 21, 22, 23, 24, 25]
        baic_other_steps_labels = [
            "Step 3 - M&A", 
            "Step 4 - Profitability", 
            "Step 5 - Balance Sheet", 
            "Step 6 - Cash Flow", 
            "Step 7 - Restatements", 
            "Step 8 - Management Experience", 
            "Step 9 - Outside Directors", 
            "Step 10 - General Litigation", 
            "Step 11 - D&O Claim History", 
            "Step 12 - Shareholder Base", 
            "Step 13 - Equity or Debt", 
            "Step 14 - Stock Volatility", 
            "Step 16 - Private Company", 
            "Step 17 - Indemnifiable Coverage",
            "Step 18 - Years in Operation",
            "Step 19 - Side A Factor",
            "Step 20a - Fit within Industry Classification",
            "Step 20b - Internal Governance & Loss Prevention",
            "Step 20c - Regulatory Investigations or Issues",
            "Step 20d - Susceptibility to Recession",
            "Step 20e - Major Customer Dependency",
            "Step 20f - Labor Relations Exposure",
            #"Step_20 - Schedule Rating Factor",
            ]
    else:
        baic_other_steps = [
            "step_3_mam",
            "step_4_pm",
            "step_5_qm",
            "step_6_cm",
            "step_7_fm",
            "step_8_em",
            "step_9_om",
            "step_10_lm",
            "step_11_chm",
            "step_12_sm",
            "step_13_edm",
            "step_14_spm",
            "step_16_pcm",
            "step_17_icm",
            "step_18_yo",
            "step_19_saf"
            ]
        baic_other_steps_nums = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19]
        baic_other_steps_labels = [
            "Step 3 - M&A", 
            "Step 4 - Profitability", 
            "Step 5 - Balance Sheet", 
            "Step 6 - Cash Flow", 
            "Step 7 - Restatements", 
            "Step 8 - Management Experience", 
            "Step 9 - Outside Directors", 
            "Step 10 - General Litigation", 
            "Step 11 - D&O Claim History", 
            "Step 12 - Shareholder Base", 
            "Step 13 - Equity or Debt", 
            "Step 14 - Stock Volatility", 
            "Step 16 - Private Company", 
            "Step 17 - Indemnifiable Coverage",
            "Step 18 - Years in Operation",
            "Step 19 - Side A Factor"]     
    
    return baic_other_steps, baic_other_steps_nums, baic_other_steps_labels

# Calculated steps
bici_calc_steps = ["step_1_bpm","step_15_rm","step_18_llm"]
bici_calc_steps_labels = ["Step 1 - Base Premium", "Step 15 - Retention", "Step 18 - Limit of Liability"]

baic_calc_steps = ["step_1_bpm","step_15_clrm"] #, "step_20_srf"]
baic_calc_steps_labels = ["Step 1 - Base Premium", "Step 15 - Combined Limit/Retention"] #, "Step 20 - Schedule Rating Factor"]

# Max assets
baic_max_assets = 2500000

# Final premium factor min and max
admitted_final_premium_factor_min = 0.4
admitted_final_premium_factor_max = 1.6

incomplete_column = "\U0000274C"  # Red X
complete_column = "\U00002705"  # Green Check
column_labels_modifiers = "non_cds.modifier_labels"

