# v0.5.0
# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers          = 1
benchmark_lr        = 0.7
NCB_FREQUENCY       = 0.762978738698309
ADVERSE_WEATHER_NMP = 0.0001                                    
IHS_EXP_BASE        = 2.2
CAT_NON_APP_LOAD    = 0.001125
EVENTS_MIN_UW_ADJ   = -0.5
EVENTS_MAX_UW_ADJ   =  0.5
EVENT_DEFAULT_LENGTH= 10 # days

NM_MIN_ADJ          = 0.5
NM_MAX_ADJ          = 1.5

NON_APP_UW_ADJ_MIN   = -0.5
NON_APP_UW_ADJ_MAX   =  0.5
NON_APP_DEFAULT_RATE = 0.0225

BP_CLASS             = "Contingency"
PLAN_GNLR            = 0.61788630  # Plan LR for 2027 from YZ teams 8/9/26 - day 2 job to expand this to a dictionary

# experience rating
EXPER_RATING_LOGIC_DICT   = {"IELR": 0.4, "BF":0.75, "CL":1}   
EXPER_RATING_DECAY        = 0.9
EXPER_RATING_LL_THRESHOLD = 700000
EXPER_RATING_MAX_NUM_YRS  = 8
EVALUATION_DATE_LAG       = -6


NUMBER_OF_SIMS          = 100000
NUMBER_OF_SIMS_T_HXD    = 100000
WEIGHT_TO_SIMS          = 1.0                                   # was 0.5 in excel model

RNG_SEED = 42
