import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term, get_lookup_value, year_frac
from operator import itemgetter
from algorithms.rate_constants import all_perils


def rate_risk_information(hxd):
        
    # Extracts database id for the risk information tab
    hxd.cds.policy_option_id = hx.meta.policy_option_id
    
    hxd.cds.rating_factors.policy_term = year_frac(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)
    #hxd.cds.rating_factors.policy_term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)

    # Set source currency to USD
    hxd.cds.currencies.source_currency = 'USD'

    # Set benchmark class to E&S  Homeowners
    hxd.cds.standard_fields.benchmark_class = "E&S  Homeowners"

    # Adds the number of losses in the loss history section
    hxd.cds.experience_rating.coverages.total.number_of_losses = sum(
        getattr(hxd.cds.experience_rating.coverages, cov).number_of_losses
        for cov in all_perils if cov != 'paf'
    )

    # Adds the amount of losses in the loss history section
    hxd.cds.experience_rating.coverages.total.amount_of_losses = sum(
        getattr(hxd.cds.experience_rating.coverages, cov).amount_of_losses
        for cov in all_perils if cov != 'paf'
    )

    # Set Brokerage value
    if hxd.cds.standard_fields.broker:
        brokerage = get_lookup_value(
            hx.params.table_broker,
            'Brokerage',
            hxd.cds.standard_fields.broker,
            reference_column = 'Broker',
            error_behavior='default_value',
            default_value = 0.2)
        hxd.cds.brokerage.calculated = brokerage
    else:
        hxd.cds.brokerage.calculated = 0

    # Set distance to coast
    def get_distance_in_miles(value: str) -> float:
        """
        Converts a distance range string from the "Values" column into a numerical value (midpoint in miles).
        """
        distance_mapping = {
            "RISK<=1000FT": 1000 / 5280,  # Convert feet to miles
            "1000FT<RISK<=0.5MI": (1000 / 5280 + 0.5) / 2,
            "0.5MI<RISK<=1MI": (0.5 + 1) / 2,
            "1MI<RISK<=2MI": (1 + 2) / 2,
            "2MI<RISK<=5MI": (2 + 5) / 2,
            "5MI<RISK<=10MI": (5 + 10) / 2,
            "10MI<RISK<=20MI": (10 + 20) / 2,
            "20MI<RISK<=50MI": (20 + 50) / 2,
            "50MI<RISK<=100MI": (50 + 100) / 2,
            "100MI<RISK<=250MI": (100 + 250) / 2,
            "250MI<RISK": 250,  # Assuming minimum distance of 250 miles for open-ended range
        }
        
        return distance_mapping.get(value, None)  # Returns None if the value is not found
    hxd.cds.rating_factors.distance_to_coast = get_distance_in_miles(hxd.cds.rating_factors.distance_to_coast_options)

    # Checking if Updated Roof Year has a value and using that one, otherwise using the Year Built
    if hxd.cds.rating_factors.updated_roof_year:
        hxd.cds.rating_factors.roof_year = hxd.cds.rating_factors.updated_roof_year
    else:
        hxd.cds.rating_factors.roof_year = hxd.cds.rating_factors.year_built
