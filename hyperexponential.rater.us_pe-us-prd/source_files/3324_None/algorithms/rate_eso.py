import hx  # Importing the hx module
import pandas as pd  # Importing pandas for data manipulation
import numpy as np  # Importing numpy for numerical operations
import math as math  # Importing math for mathematical functions
from algorithms.rate_constants import (
    coverage_options_names,
)  # Importing coverage options names from rate constants
from operator import itemgetter  # Importing itemgetter for item extraction


# Function to rate eso
def rate_eso(hxd):
    hxd.cds.eso.requesting_underwriter = hxd.cds.standard_fields.underwriter
    hxd.cds.eso.amount_authorising.warning = "*Please ensure amount signed off on is explicit including FAC purchased if not authorised *"
    hxd.cds.eso.warning = "*Please ensure ESO is uploaded to Underwriting System or W:Drive within 21 days of Bind date/Endorsement bind date to ensure compliance with Control"
