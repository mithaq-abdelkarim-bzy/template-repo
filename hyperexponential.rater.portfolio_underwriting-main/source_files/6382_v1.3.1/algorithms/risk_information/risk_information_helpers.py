import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from datetime import timedelta, date
import algorithms.validations.risk_information_validations as validations


def set_broker_details(hxd):
    risk_inform_path = hxd.cds.risk_information

    # Get the broker details table from input parameters
    broker_details_df = hx.params.table_input_broker_details
    # Extract the broker contact from the provided risk_inform_path
    broker_contact = risk_inform_path.broker_contact

    # Find the row in the broker details table that matches the broker contact
    broker_row = broker_details_df.loc[broker_details_df["broker_contact"] == broker_contact]

    # If a matching row exists, set calculated values on risk_inform_path fields
    if not broker_row.empty:
        row_data = broker_row.iloc[0]  # Take the first matching row
        fields = ['broker_email', 'broker_location']
        for field in fields:
            # For each field, set the "calculated" attribute to the corresponding table value
            setattr(getattr(risk_inform_path, field), "calculated", row_data[field])

        hxd.cds.standard_fields.broker.calculated = getattr(row_data, "broker_name")


def import_inception_date(hxd):
    # Return the inception_date from standard fields (wrapper for convenience)
    return hxd.cds.standard_fields.inception_date


def apply_validations_checks(hxd):
    # Reset global validation flags/messages before running checks
    hxd.non_cds.global_fields.is_there_global_message = False
    hxd.non_cds.global_fields.projections_error_msg   = ("Please check the “Insured Data as as Date” (Risk Information Tab) it is either missing or not 0-9mth prior to inception.")
    hxd.non_cds.global_fields.pc_error_msg            = ("Profit commission results are outdated. Please re-run the PC task to update them."                  )
    hxd.non_cds.global_fields.lobs_error_msg          = ("“Selected LoB” (Risk Code Composition Tab) is blank. Please review before submission."              )
    hxd.non_cds.global_fields.oe_error_msg            = ("Weight given to Own Experience when no claims data has been entered. Please adjust weighting in Rating Summary."                  )

    # Extract frequently used fields for validation checks
    policy_reference    = hxd.cds.standard_fields.policy_reference
    underwriter         = hxd.cds.standard_fields.underwriter
    deal_status         = hxd.cds.risk_information.deal_status
    facility_type       = hxd.cds.risk_information.facility_type
    insured_name        = hxd.cds.standard_fields.insured_name
    broker_name         = hxd.cds.standard_fields.broker.selected
    currency            = hxd.cds.currencies.source_currency
    insured_data_date   = hxd.cds.risk_information.insured_data_date
    inception_date      = hxd.hx_core.inception_date
    is_bbt              = hxd.cds.risk_information.follow_main_syndicate
    is_premium_avail    = hxd.cds.risk_information.prem_data_available

    # Run validation checks on extracted fields
    validations.check_deal_status_value(     deal_status     )
    validations.check_underwriter_value(     underwriter     )
    validations.check_facility_type_value(   facility_type   )
    validations.check_insured_name_value(    insured_name    )  
    validations.check_currency_value(        currency        )
    validations.check_policy_reference_value(policy_reference)
    validations.check_broker_name(           broker_name     )

    if not is_bbt and is_premium_avail:
        validations.check_insured_data_as_at_date_value(insured_data_date, inception_date, hxd)