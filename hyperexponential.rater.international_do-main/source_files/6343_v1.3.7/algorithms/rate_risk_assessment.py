import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter


def rate_risk_assessment(hxd):

    # cds location
    mod = hxd.cds.modifiers

    # Parameter tables
    fx_rates = params.fx_rates.df()
    df_mod_bounds = hx.params.tbl_mod_bounds

    # Defining risk assessment range of adjustments i.e. maxs and mins
    mod_mapping = {
        "Management and Corporate Gov": [
            mod.management_corp_gov_factors,
            mod.management_corp_gov_factors_side_a
        ],
        "Business/Financial Model Factors": [
            mod.business_financial_model_factors,
            mod.business_financial_model_factors_side_a
        ],
        "Significant Event Factors": [
            mod.significant_event_factors,
            mod.significant_event_factors_side_a
        ],
        "Stock Market Factors": [
            mod.stock_market_factors,
            mod.stock_market_factors_side_a
        ],
        "Regulatory": [mod.regulatory_factors],
        "Mergers and Acquisitions": [mod.mergers_and_acquisitions_factors],
        "Territory of Operation": [mod.territory_of_operation_factors],
        "ESG Factor": [mod.esg_factors, mod.esg_factors_side_a],
        "Financial Stability": [mod.financial_stability_side_a_factors],
        "Indemnification": [mod.indemnification_side_a_factors],
    }

    # Apply min/max values in a loop
    for mod_name, targets in mod_mapping.items():
        mod_row = df_mod_bounds.loc[df_mod_bounds["Mod"] == mod_name].iloc[0]
        for target in targets:
            target.min = mod_row["Min"]
            target.max = mod_row["Max"]
    
    mod.total_factors.comment = "Maximum total discount allowed for Public is -30%; for Private is -50%."
    mod.total_factors_side_a.comment = "Maximum total discount allowed is -50% (excluding DIC adjustment)"
    
    
    # Calculating total adjustment factors 

    # Overall SCA Adjustment Factor AB/ABC
    values = [ 
        mod.management_corp_gov_factors.value, 
        mod.business_financial_model_factors.value, 
        mod.significant_event_factors.value, 
        mod.stock_market_factors.value 
        ]
   
    mod.sca_adj_factors.value = 1 

    for value in values: 
        if value is not None: 
            mod.sca_adj_factors.value *= (1 + value) 
        else: mod.sca_adj_factors.value *= 1

    mod.sca_adj_factors.value = (mod.sca_adj_factors.value - 1)

    # Total Factor AB/ABC
    values = [
        mod.regulatory_factors.value, 
        mod.mergers_and_acquisitions_factors.value, 
        mod.territory_of_operation_factors.value, 
        mod.esg_factors.value
    ]

    mod.total_factors.value = 1 

    for value in values: 
        if value is not None: 
            mod.total_factors.value *= (1 + value) 
        else: mod.total_factors.value *= 1


    if hxd.cds.rating_factors.risk_information.ownership_type == "Public":
        mod.total_factors.value = max((mod.total_factors.value - 1), -0.3)
    else:
        mod.total_factors.value = max((mod.total_factors.value - 1), -0.5)

    # Overall SCA Adjustment Factor Side A
    values = [ 
        mod.management_corp_gov_factors_side_a.value, 
        mod.business_financial_model_factors_side_a.value, 
        mod.significant_event_factors_side_a.value, 
        mod.stock_market_factors_side_a.value 
        ]
   
    mod.sca_adj_factors_side_a.value = 1 

    for value in values: 
        if value is not None: 
            mod.sca_adj_factors_side_a.value *= (1 + value) 
        else: mod.sca_adj_factors_side_a.value *= 1

    mod.sca_adj_factors_side_a.value = (mod.sca_adj_factors_side_a.value - 1)

    # Total Factor Side A
    values = [
        mod.financial_stability_side_a_factors.value, 
        mod.indemnification_side_a_factors.value, 
        mod.esg_factors_side_a.value
    ]

    mod.total_factors_side_a.value = 1 

    for value in values: 
        if value is not None: 
            mod.total_factors_side_a.value *= (1 + value) 
        else: mod.total_factors_side_a.value *= 1

    mod.total_factors_side_a.value = max((mod.total_factors_side_a.value - 1), -0.5)


    # Sector Commentary Lookup, this varies by SIC code
    rf_risk_info = hxd.cds.rating_factors.risk_information

    tbl_sic_freq = hx.params.tbl_sic_freq

    if rf_risk_info.industry_class_sic_code is not None:
        sic_code = utils.extract_sic(rf_risk_info.industry_class_sic_code).lstrip('0')
        if sic_code: 
            message = utils.look_up(int(float(sic_code)), "SIC", "Message", tbl_sic_freq, if_not_found = None)
            # Message is a long string with hyphons as delimeters, want the hyphons to represent a new line for ease of reading
            message = message.replace("-",  "\n") if message else None
            hxd.cds.modifiers.message = message 
        else: 
            hxd.cds.modifiers.message = None


    # Info bubble for SCA frequency adjustment factor
    hxd.cds.modifiers.sca_freq_adj_factor_info = "Range: -50% to +100%, only available for sectors where this may be required"


    # Side A suggested factor lookup
    tbl_intl_countries = hx.params.tbl_intl_countries

    if rf_risk_info.country_of_domicile is not None:
        matched_index = tbl_intl_countries[tbl_intl_countries.iloc[:, 0] == rf_risk_info.country_of_domicile].index
        if not matched_index.empty:
            hxd.cds.modifiers.suggested_factor = tbl_intl_countries.iloc[matched_index[0], 4]
        else:
            hxd.cds.modifiers.suggested_factor = None

    # Side A message for suggested factor
    if rf_risk_info.country_of_domicile is not None:
        matched_index = tbl_intl_countries[tbl_intl_countries.iloc[:, 0] == rf_risk_info.country_of_domicile].index
        if not matched_index.empty:
            hxd.cds.modifiers.suggested_factor_message = tbl_intl_countries.iloc[matched_index[0], 5]
        else:
            hxd.cds.modifiers.suggested_factor_message = None

    # Side A message for adjustments
    if rf_risk_info.country_of_domicile is not None:
        matched_index = tbl_intl_countries[tbl_intl_countries.iloc[:, 0] == rf_risk_info.country_of_domicile].index
        if not matched_index.empty:
            hxd.cds.modifiers.suggested_factor_message_for_adj = tbl_intl_countries.iloc[matched_index[0], 6]
        else:
            hxd.cds.modifiers.suggested_factor_message_for_adj = None


    # Error Validatoin for Modifier Values

    if mod.sca_freq_adj_factor is not None:
        if mod.sca_freq_adj_factor < -0.5 or mod.sca_freq_adj_factor > 1.0:
            hx.errors.validation("Risk Assessment: SCA Frequency Adjustment Factor must be within the accepted range")


    mod_list = ["management_corp_gov_factors", "business_financial_model_factors", "significant_event_factors", "stock_market_factors", 
    "regulatory_factors", "mergers_and_acquisitions_factors", "territory_of_operation_factors", "esg_factors",
    "management_corp_gov_factors_side_a", "business_financial_model_factors_side_a", "significant_event_factors_side_a", "stock_market_factors_side_a", 
    "financial_stability_side_a_factors", "indemnification_side_a_factors", "esg_factors_side_a"]

    # I want to be able to specify the modifier that is out of bounds by name, the label in the view isn't directly callable within this script so will do it manually
    mod_list_view_labels = ["Management and Corporate Governance", "Business / Financial Model Factors", "Significant Event Factors",
    "Stock Market Factors", "Regulatory", "Mergers and Acquisitions", "Territory of Operation", "ESG Factor", "Management and Corporate Governance",
    "Business / Financial Model Factors", "Significant Event Factors", "Stock Market Factors", "Financial Stability", "Indemnification", "ESG Factor"]

    for index, attr_name in enumerate(mod_list):
        mod_obj = getattr(mod, attr_name, None)
        if mod_obj is not None and mod_obj.value is not None:
            if mod_obj.value < mod_obj.min or mod_obj.value > mod_obj.max:
                hx.errors.validation(
                    f"Risk Assessment: Modifier ({mod_list_view_labels[index]}) must be within the accepted range"
                )

    if mod.total_factors.value is not None:
        if rf_risk_info.ownership_type == "Public" and mod.total_factors.value < -0.3:
            hx.errors.validation("Risk Assessment Side AB/ABC Total Factor must be within the accepted range")
        elif rf_risk_info.ownership_type == "Private" and mod.total_factors.value < -0.5:
            hx.errors.validation("Risk Assessment: Side AB/ABC Total Factor must be within the accepted range")


    if mod.total_factors_side_a.value is not None:
        if mod.total_factors_side_a.value < -0.5:
            hx.errors.validation("Risk Assessment: Side A Total Factor must be within the accepted range")

    for index, attr_name in enumerate(mod_list):
        mod_obj = getattr(mod, attr_name, None)
        if mod_obj is not None and mod_obj.value is not None and mod_obj.value != 0 and mod_obj.comment is None:
            hx.errors.validation(
                f"Risk Assessment: Modifier ({mod_list_view_labels[index]}) requires comment on adjustment"
            )
