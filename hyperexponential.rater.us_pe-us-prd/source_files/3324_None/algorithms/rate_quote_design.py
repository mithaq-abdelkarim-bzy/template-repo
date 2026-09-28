import hx  # Importing the hx module
import pandas as pd  # Importing pandas for data manipulation
import numpy as np  # Importing numpy for numerical operations
import math as math  # Importing math for mathematical functions
from algorithms.rate_constants import (
    coverage_options_names,
)  # Importing coverage options names from rate constants
from operator import itemgetter  # Importing itemgetter for item extraction


# Function to rate risk information and populate dynamic lists
def rate_quote_design(hxd):
    hxd.cds.quote_design.coverage_options_list = [
        {"option": item} for item in coverage_options_names
    ]

    hxd.cds.quote_design.is_e_cigarettes_check.show = (
        True if (hxd.cds.account_details.product_type == "Products") else False
    )
