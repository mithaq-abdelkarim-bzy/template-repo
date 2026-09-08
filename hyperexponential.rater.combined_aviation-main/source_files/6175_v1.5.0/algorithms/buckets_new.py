def rate_change_buckets(hxd):

    ### --- GENERAL AVIATION --- ###
    if hxd.cds.is_ga:
        hull_buckets = {
            "model": [], # Start from expiry data priced with current model
            "exposure": [
                # Add policy dates to counteract term changes
                "hx_core/inception_date",
                "hx_core/expiry_date",
                "cds/experience_rating/as_at_date", # NOTE: as_at_date is here so that experience rating is calculated and doesn't create distortions

                "cds/exposure/granular/fleet_size", # YZ: Used to be in Risk Characteristic but is moved to Exposure Bucket. Override: This is a discount factor of exposure size.
                "cds/exposure/granular/aircrafts/include",
                "cds/exposure/granular/aircrafts/registration", # Including registration so fleet size is calculated correctly
                "cds/exposure/granular/aircrafts/no_of_aircraft",
                "cds/exposure/granular/aircrafts/value",
                "cds/exposure/granular/aircrafts/hull_ccy",
            ],
            "risk_characteristics": [
                "cds/exposure/granular/aircrafts/aircraft_class", # YZ: Used to be in exposure for additional aircraft and now is moved to risk characteristic      
                "cds/exposure/granular/aircrafts/build_location",
                "cds/exposure/granular/aircrafts/build_year", # FS: PL Update Addition
                "cds/exposure/granular/aircrafts/operator_country", # Doesn't affect rating
                "cds/exposure/granular/aircrafts/operator_region",  # FS: Need to update with operator region
                "cds/exposure/granular/aircrafts/use",
                "cds/exposure/granular/aircrafts/time_in_service"
            ],
            "deductible": [
                "cds/exposure/granular/aircrafts/per_occ_deductible_pct",
                "cds/exposure/granular/aircrafts/per_occ_deductible",
            ],
            "limit": [],
            "terms_conditions": [],
            "brokerage": [
                "cds/layers/coverages/hull/brokerage"
            ],
            "other": [
                # UW Adjustments
                "cds/layers/pilot_uw_adj",
                "cds/layers/coverages/hull/uw_adj",
                # Experience Rating
                "cds/experience_rating/historic_premium_known",
                "cds/experience_rating/claims/hull_attr_claims",
                "cds/experience_rating/claims/hull_large_losses",
                "cds/experience_rating/claims/hull_gross_premium",
                "cds/experience_rating/claims/hull_exposure_adj",
                "cds/experience_rating/claims/hull_rate_change"
            ]
        }

        liab_buckets = {
            "model": [], # Start from expiry data priced with current model
            "exposure": [
                # Add policy dates to counteract term changes
                "hx_core/inception_date",
                "hx_core/expiry_date",
                "cds/experience_rating/as_at_date", # NOTE: as_at_date is here so that experience rating is calculated and doesn't create distortions

                "cds/exposure/granular/fleet_size", # YZ: Moved from the Risk Characteristic to Exposure. Override
                "cds/exposure/granular/aircrafts/include",
                "cds/exposure/granular/aircrafts/registration", # Including registration so fleet size is calculated correctly
                "cds/exposure/granular/aircrafts/no_of_aircraft",
                "cds/exposure/granular/aircrafts/liability_ccy",
                # PAX
                "cds/exposure/granular/aircrafts/total_seats",
                "cds/exposure/granular/aircrafts/crew_seats",
                "cds/exposure/granular/aircrafts/pax_net_worth",
                # TPL
                "cds/exposure/granular/aircrafts/combined_single_limit", # Despite being a limit, it effectively determines the TPL exposure
                "cds/exposure/granular/aircrafts/tpl_limit_exposed"
            ],
            "risk_characteristics": [
                "cds/exposure/granular/aircrafts/aircraft_class", # YZ: Moved away from Exposure Bucket to Risk Characteristic. Putting class here so that frequency is calculated
                "cds/exposure/granular/aircrafts/time_in_service", # YZ: Moved away from Exposure Bucket to Risk Characteristic. 
                "cds/exposure/granular/aircrafts/operator_country", # YZ: add this in Liability. Doesn't affect rating 
                "cds/exposure/granular/aircrafts/operator_region", # YZ:  Moved away from Exposure Bucket to Risk Characteristic.  Calculates fatality rate and seat occupancy
                "cds/exposure/granular/aircrafts/use", # YZ:  Moved away from Exposure Bucket to Risk Characteristic. Calculates fatality rate and seat occupancy
            ],
            "deductible": [],
            "limit":[
                "cds/exposure/granular/aircrafts/per_pax_liab_limit"  # YZ: Moved away from Exposure Bucket to Limit. 
	        ],
            "terms_conditions": [],
            "brokerage": [
                "cds/layers/coverages/liability/brokerage"
            ],
            "other": [
                # UW Adjustments
                "cds/layers/pilot_uw_adj",
                "cds/layers/coverages/liability/uw_adj",
                # Experience Rating
                "cds/experience_rating/historic_premium_known",
                "cds/experience_rating/claims/liab_attr_claims",
                "cds/experience_rating/claims/liab_large_losses",
                "cds/experience_rating/claims/liab_gross_premium",
                "cds/experience_rating/claims/liab_exposure_adj",
                "cds/experience_rating/claims/liab_rate_change"
            ]
        }

    ### --- AIRLINES --- ###
    else:
        hull_buckets = {
            "model": [], # Start from expiry data priced with current model
            "exposure": [
                # Add policy dates to counteract term changes
                "hx_core/inception_date",
                "hx_core/expiry_date",
                "cds/experience_rating/as_at_date", # NOTE: as_at_date is here so that experience rating is calculated and doesn't create distortions

                "cds/exposure/granular/fleet_size", # YZ: Moved from Risk Characteristic to Exposure. Override
                "cds/exposure/granular/airlines/include",
                "cds/exposure/granular/airlines/registration", # Including registration so fleet size is calculated correctly
                "cds/exposure/granular/airlines/no_of_aircraft",
                "cds/exposure/granular/airlines/value",
                "cds/exposure/granular/airlines/hull_ccy",
                "cds/exposure/granular/airlines/attachment_date",
                "cds/exposure/granular/airlines/expiry_date"
            ],
            "risk_characteristics": [
                "cds/exposure/granular/selected_operator_class",
                "cds/exposure/granular/status_split/in_service",
                "cds/exposure/granular/status_split/storage",
                "cds/exposure/granular/status_split/other",
                "cds/exposure/granular/airlines/aircraft status",
                "cds/exposure/granular/airlines/coverage",
                "cds/exposure/granular/airlines/time_in_service",
                "cds/exposure/granular/airlines/operator_country", # Doesn't affect rating
                "cds/exposure/granular/airlines/operator_region",
                "cds/exposure/granular/airlines/previous12_months_hours",
                "cds/exposure/granular/airlines/market_class",
                "cds/exposure/granular/airlines/build_year",
                "cds/exposure/granular/airlines/usage",
                "cds/exposure/granular/airlines/russian_built",
		        "cds/exposure/granular/airlines/operating_mtow_lb" #YZ: Add MTOW in the Risk Characteristic bucket.
            ],
            "deductible": [
                "cds/exposure/granular/airlines/hull_excess"
            ],
            "limit":[
	         "cds/exposure/granular/airlines/hull_limit", # YZ: Moved from Exposure Bucket to Limit.
	        ],
            "terms_conditions": [],
            "brokerage": [
                "cds/layers/coverages/hull/brokerage"
            ],
            "other": [
                # UW Adjustments
                "cds/layers/pilot_uw_adj",
                "cds/layers/coverages/hull/uw_adj",
                # Experience Rating
                "cds/experience_rating/historic_premium_known",
                "cds/experience_rating/claims/hull_attr_claims",
                "cds/experience_rating/claims/hull_large_losses",
                "cds/experience_rating/claims/hull_gross_premium",
                "cds/experience_rating/claims/hull_exposure_adj",
                "cds/experience_rating/claims/hull_rate_change",
            ]
        }
        liab_buckets = {
            "model": [], # Start from expiry data priced with current model
            "exposure": [
                # Add policy dates to counteract term changes
                "hx_core/inception_date",
                "hx_core/expiry_date",
                "cds/experience_rating/as_at_date", # NOTE: as_at_date is here so that experience rating is calculated and doesn't create distortions

		        "cds/exposure/granular/fleet_size", # YZ Change from Risk Characteristic to Exposure. Override
                "cds/exposure/granular/airlines/include",
                "cds/exposure/granular/airlines/registration", # Including registration so fleet size is calculated correctly
                "cds/exposure/granular/airlines/no_of_aircraft",
                "cds/exposure/granular/airlines/liability_ccy",
                "cds/exposure/granular/airlines/attachment_date",
                "cds/exposure/granular/airlines/expiry_date",
                # PAX
                "cds/exposure/granular/airlines/total_seats",
                "cds/exposure/granular/airlines/liability_limit", # Despite being a limit, it effectively determines the PAX exposure
                # TPL
                "cds/exposure/granular/airlines/pll_award", # Override
                "cds/exposure/granular/airlines/tpl_limit_exposed" # Override
            ],
            "risk_characteristics": [
                "cds/exposure/granular/status_split/in_service",
                "cds/exposure/granular/status_split/storage",
                "cds/exposure/granular/status_split/other",
                "cds/exposure/granular/airlines/aircraft_status", # YZ: Change from Exposure Bucket to Risk Characteristic.
                # PAX
                "cds/exposure/granular/airlines/usage", # YZ: Move from Exposure to Risk Characteristic. Including usage because it's necessary to calculate TPL loss cost
                "cds/exposure/granular/airlines/build_year",
                "cds/exposure/granular/airlines/operator_country", # Doesn't affect rating
                "cds/exposure/granular/airlines/operator_region",
                "cds/exposure/granular/airlines/previous12_months_hours",
                "cds/exposure/granular/airlines/market_class",
                "cds/exposure/granular/airlines/time_in_service",
		        "cds/exposure/granular/airlines/operating_mtow_lb" #YZ: Add MTOW in the Risk Characteristic bucket.
                # TPL has no specific risk characteristics factor                
            ],
            "deductible": [
                "cds/exposure/granular/airlines/liability_excess"
            ],
            "limit": [],
            "terms_conditions": [],
            "brokerage": [
                "cds/layers/coverages/liability/brokerage"
            ],
            "other": [
                # UW Adjustments
                "cds/layers/pilot_uw_adj",
                "cds/layers/coverages/liability/uw_adj",
                # Experience Rating
                "cds/experience_rating/historic_premium_known",
                "cds/experience_rating/claims/liab_attr_claims",
                "cds/experience_rating/claims/liab_large_losses",
                "cds/experience_rating/claims/liab_gross_premium",
                "cds/experience_rating/claims/liab_exposure_adj",
                "cds/experience_rating/claims/liab_rate_change"
            ]
        }

    return hull_buckets, liab_buckets
