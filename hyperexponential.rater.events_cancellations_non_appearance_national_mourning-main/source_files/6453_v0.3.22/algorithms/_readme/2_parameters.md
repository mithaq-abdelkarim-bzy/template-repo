# Overview
- Describe in 1 line the purpose of each parameter table
- Describe in 1 line the purpose of each library
- identify the parameter tables/library/constants that should be 
    1) updated annually 
    2) periodically due to external factors
    3) with rate review

# Parameters Purpose (prepared by AI)
- lst_country	                                        Provides country dropdown options for exposure/country selection fields.
- lst_event_national_mourning_level_of_cover	        Provides dropdown options for national mourning level of cover.
- lst_insured_names	                                	Provides insured-name dropdown options for overrides or selection inputs.
- table_input_underwriters		                        Provides underwriter/team dropdown options for override/input selection.
- tbl_country_us_states_codes		                    Provides US state and two-digit code options used in exposure location inputs.
- tbl_event_adverse_weather	                            Supplies country/state adverse weather rates and patterns for event cancellation CAT rating.
- tbl_event_aggregate_discount	                        Supplies aggregate limit and deductible discount factors for event cancellation rating.
- tbl_event_cyber	                                	Supplies cyber option factors/rates for event cancellation cyber peril pricing.
- tbl_event_earthquake	                                Supplies country/state earthquake rates and patterns for event cancellation CAT rating.
- tbl_event_ihs_parameters	                            Supplies segment-level IHS scoring parameters used to convert IHS scores into rating outputs.
- tbl_event_national_mourning	                        Supplies national mourning trigger rates for event cancellation pricing.
- tbl_event_national_mourning_mortality_by_age		    Supplies age-specific mortality rates for national mourning mortality calculations.
- tbl_event_national_mourning_mortality_by_age_group	Supplies assumed age and mortality rates by age group/gender for national mourning calculations.
- tbl_event_rates	                                	Supplies base event-type rates and adverse-weather relativities for event cancellation pricing.
- tbl_event_seasonality_adverse_weather		            Supplies monthly seasonality rates/patterns for adverse weather exposure.
- tbl_event_seasonality_wildfire		                Supplies monthly seasonality rates/patterns for wildfire exposure.
- tbl_event_seasonality_windstorm	                    Supplies monthly seasonality rates/patterns for windstorm exposure.
- tbl_event_terror_cityload		                        Supplies terrorism city-load multipliers and dropdown options.
- tbl_event_terror_eventprofile		                    Supplies terrorism event-profile multipliers and dropdown options.
- tbl_event_terror_timedistance		                    Supplies terrorism time/distance multipliers and dropdown options.
- tbl_event_venue		                                Supplies venue multipliers and venue dropdown options for event cancellation rating.
- tbl_event_wildfire		                            Supplies country/state wildfire rates and patterns for CAT rating.
- tbl_event_windstorm	                                Supplies country/state windstorm rates and patterns for CAT rating.
- tbl_experience_adj_lr	                                Supplies loss-ratio adjustment multipliers and dropdown options for experience rating assumptions.
- tbl_experience_dev_factors	                        Supplies development factors by month for experience rating loss development.
- tbl_experience_large_year_credibility		            Supplies credibility factors by number of years for large-loss experience credibility.
- tbl_experience_year_exposure_weight		            Supplies exposure-based year weighting assumptions for experience rating.
- tbl_experience_yoa_assump		                        Supplies year-of-account portfolio rate, claims inflation, and IELR assumptions for experience rating.
- tbl_exposure_curve_attr		                        Supplies attritional exposure curve parameters used in exposure curve calculations.
- tbl_exposure_curve_cat		                        Supplies CAT exposure curve parameters used in exposure curve calculations.
- tbl_ihs_country_codes		                            Maps countries to IHS country codes and provides country-code dropdown options.
- tbl_ihs_country_group		                            Maps IHS country groups/countries/codes/weights for IHS data fetching and event cancellation rating.
- tbl_non_app_base_rates		                        Supplies genre-level base rates and dropdown options for non-appearance pricing.
- tbl_non_app_claim_experience_mod		                Supplies claim-experience modifier factors and dropdown options for non-appearance pricing.
- tbl_non_app_loss_curves	                            Supplies non-appearance loss curve values by attachment for layer/ILF calculations.
- tbl_non_app_num_band_members_mod		                Supplies band-member-count modifier factors and dropdown options for non-appearance pricing.


# Library Purpose (prepared by AI)
- common_data_schema	        Provides shared cds schema and standard hx_core output syncing.
- email_notification	        Adds bug-report schema/view/tasks for creating and sending bug reports.
- schema_viewer	                Adds a schema viewer page and rating hook to expose the model schema in the UI.
- model_profiler	            Provides profiling/timing decorators and UI for rating performance diagnostics.
- tp_parameters	                Provides technical-pricing parameter table loading/support.
- fx_rates	                    Provides FX rate parameter data loaded into the model’s parameter table schema.
- hx_renew_api	                Wraps Renew API access for renewal/expiring policy fetches and API client setup.
- ihs_api	                    Provides IHS API client/endpoints for fetching IHS risk data.
- rate_change	                Provides coverage-level RARC/rate-change calculation and fetch logic.
- rate_change_insured_asset	    Provides insured-asset-level rate-change logic.


# (1) identify the parameters/library/constants that should be updated annually 
   - tbl_experience_dev_factors.csv
   - tbl_experience_yoa_assump.csv
   - rate_constants - PLAN_GNLR
   - library - tp_parameters
   - library - fx_rates

# (2) identify the parameters that should be updated periodically and checked annually
   - lst_country.csv
   - lst_insured_names.csv
   - table_input_underwriters.csv
   - tbl_country_us_states_codes.csv
   - tbl_ihs_country_codes.csv
   - tbl_ihs_country_group.csv
   - library - ALL

# (3) identify the parameters that should be updated with rate review
   - tbl_event_adverse_weather.csv
   - tbl_event_aggregate_discount.csv
   - lst_event_national_mourning_level_of_cover.csv
   - tbl_event_cyber.csv
   - tbl_event_earthquake.csv
   - tbl_event_ihs_parameters.csv
   - tbl_event_national_mourning.csv
   - tbl_event_national_mourning_mortality_by_age.csv
   - tbl_event_national_mourning_mortality_by_age_group.csv
   - tbl_event_rates.csv
   - tbl_event_seasonality_adverse_weather.csv
   - tbl_event_seasonality_wildfire.csv
   - tbl_event_seasonality_windstorm.csv
   - tbl_event_terror_cityload.csv
   - tbl_event_terror_eventprofile.csv
   - tbl_event_terror_timedistance.csv
   - tbl_event_venue.csv
   - tbl_event_wildfire.csv
   - tbl_event_windstorm.csv
   - tbl_experience_adj_lr.csv
   - tbl_experience_large_year_credibility.csv
   - tbl_experience_year_exposure_weight.csv
   - tbl_exposure_curve_attr.csv
   - tbl_exposure_curve_cat.csv
   - tbl_non_app_base_rates.csv
   - tbl_non_app_claim_experience_mod.csv
   - tbl_non_app_loss_curves.csv
   - tbl_non_app_num_band_members_mod.csv
   - rate_constants