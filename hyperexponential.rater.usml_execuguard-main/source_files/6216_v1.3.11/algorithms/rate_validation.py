import hx
import pandas as pd
import numpy as np

def rate_validations(hxd):

    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation("Insured name field must be completed.")