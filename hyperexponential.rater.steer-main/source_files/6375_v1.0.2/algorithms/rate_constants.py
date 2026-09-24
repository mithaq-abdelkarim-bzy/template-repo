# v0.5.0
# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 5

benchmark_lr = 0.7

reinstatement_max_number = 10

experience_rating_max_years = 25

max_data_layout = 4 # to match limitation of the excel model, sheet DataFormat, cell D9

raw_data_max_column = 109
# raw_data_max_column = 18 + 1 + 4 * (experience_rating_max_years-1)

las_risk_profile_max = 10

# dum_old_date = 19700101
dum_old_date = 19000101

default_num_rows = experience_rating_max_years

cl_dev_thres = 0.7

exposure_unit = 1000000

pareto_default_value = 1.5

odf_default_value = 2.5

no_of_simulations = 10000

unlimited_rips = 999

hc_max_trial_history_years = 29

hc_max_overall_exposure_years = 12

hc_location_number = 52 # in line with the number of location in params table tbale_hc_location

hc_band_size_0_to_75 = 0.005
hc_band_size_75_to_90 = 0.001
hc_band_size_90_to_100 = 0.0001  # 0.01%

n_forward = 150  # 0% to 75%
n_mid = 150      # 75% to 90%
n_high = 800 # 90% 98%
n_backward = 200  # 98% to 100%

# n_forward = (0.75-0) / hc_band_size_0_to_75  # 0% to 75%
# n_mid = (0.9-0.75) /  hc_band_size_75_to_90   # 75% to 90%
# n_high = (0.98-0.9)/hc_band_size_90_to_100 # 90% 98%
# n_backward = (1-0.9) / hc_band_size_90_to_100 # 98% to 100%

hc_percentile_display_number = 13

las_limit_number = 30