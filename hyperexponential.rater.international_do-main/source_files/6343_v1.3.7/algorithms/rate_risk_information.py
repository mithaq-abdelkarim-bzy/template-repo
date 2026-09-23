import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import re
from algorithms import parameter_tables_schema as params
from operator import itemgetter


def rate_risk_information(hxd):
    
    # define cds paths
    cds = hxd.cds
    risk_info = hxd.cds.risk_information
    rf_risk_info = hxd.cds.rating_factors.risk_information
    exposure_aggregate = hxd.cds.exposure.aggregate

    # Extracts database id for the risk information tab
    hxd.cds.policy_option_id = hx.meta.policy_option_id    

    risk_info.test_info = "test"

    # Policy Term Calculation
    hxd.cds.rating_factors.risk_information.policy_term = utils.policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)
    
    # Define class or SIC code reference tables
    df_sic_param = hx.params.tbl_sic

    #Flags if PE Backer is "Other"
    if risk_info.pe_backer == "Other":
        risk_info.other_pe_backer_flag = True
    else:
        risk_info.other_pe_backer_flag = False

    #Flags if "Public" and "US"
    if rf_risk_info.ownership_type == "Public" and rf_risk_info.us_adr_exposure=="Yes":
        risk_info.public_us_flag = True
    else:
        risk_info.public_us_flag = False

    #Flags if not "Middle Market Private"
    risk_info.not_mmp_flag = not risk_info.mmp_flag

    #Flags if "Public"
    if rf_risk_info.ownership_type == "Public":
        risk_info.public_flag = True
        risk_info.private_flag = False
    else:
        risk_info.public_flag = False
        risk_info.private_flag = True

    # Flags if RI is selected in Direct/RI
    if risk_info.direct_ri == "RI":
        risk_info.ri_flag = True
    else:
        risk_info.ri_flag = False


    # Flags if ADR Level is 1
    if exposure_aggregate.adr_level == "Level 1":
        risk_info.adr_level_one_flag = True
    else:
        risk_info.adr_level_one_flag = False
   

    # Sets the SIC dropdown
    if rf_risk_info.search_sic is not None:
        cds.key_industry.sic_dropdown = create_sic_dropdown(hxd, df_sic_param, rf_risk_info.search_sic) 

    # Assign SIC code and description to Key Industry nodes
    if rf_risk_info.industry_class_sic_code is not None and rf_risk_info.search_sic is not None:
        sic_desc = rf_risk_info.industry_class_sic_code
        cds.key_industry.code_type = "SIC_USA"

        # Regex to extract 4 digit SIC code and description
        match = re.search(r"\b\d{4}\b", sic_desc)
        cds.key_industry.code = match.group(0) if match else None
        cds.key_industry.code_name = re.sub(r"\s*-\s*\b\d{4}\b|\b\d{4}\b\s*-\s*", "", sic_desc)
    
    # Gets Beazley Branch from UW Selection
    if cds.standard_fields.underwriter is not None:
        risk_info.beazley_branch = utils.look_up(cds.standard_fields.underwriter, "Underwriters", "Beazley Branch", hx.params.tbl_underwriter, "Not Found")

    # Climate Litigation Heatmap Dashboard Link
    # risk_info.climate_litigation = "Climate Litigation Heatmap Dashboard can be found [here](https://app.powerbi.com/groups/me/apps/4b854f37-b63a-418b-904a-b507574e6797/reports/9ddcd724-d9b1-421e-b20a-70128b95c96d/2d2caee2718320d9be3b?ctid=9a50eba8-7568-447a-bcb9-27a0d464aa80&experience=power-bi)"

    # Rationale Information Notes (Dont have a rate_rationale.py file so placing this here instead)
    hxd.cds.uw_rationale.esg_info = "ESG Commentary is required on: \n a.    Any account with over GBP/USD/EUR 5bn in assets; OR \n b.	   Any account with shares traded on a public exchange; OR \n c.    Any account with more than GBP 500m in revenue and 500 staff, \n [Note: Please refer to **D&O Insurance ESG Underwriting Guidance** for further information]"
    hxd.cds.uw_rationale.bpi_comment_info = "Rationales are required for all accounts where the net premium for Beazley share is greater than USD 100k for **new** business and USD 250k for **renewal** business. A rationale is also required for any D&O account with Level 1 Sponsored ADR or above."

    # Risk Information Validation
    if hxd.cds.standard_fields.underwriter is None:
        hx.errors.validation("Risk Information: Select Underwriter")

    if hxd.cds.standard_fields.insured_name is None:
        hx.errors.validation("Risk Information: Select Insured")

    if rf_risk_info.ownership_type == "Private" and risk_info.pe_backer is None:
        hx.errors.validation("Risk Information: Enter PE Backer if Private")
    
    if rf_risk_info.ownership_type == "Private" and rf_risk_info.us_adr_exposure == "Yes":
        hx.errors.validation("Risk Information: Private Company Cannot Have US ADR Exposure")

    # if rf_risk_info.ownership_type == "Public" and risk_info.pe_backer is not None:
    #     hx.errors.validation("Risk Information: Public Company Cannot Have a PE Backer")

    if rf_risk_info.country_of_domicile is None:
        hx.errors.validation("Risk Information: Select Country of Domicile")

    if rf_risk_info.main_operating_country is None:
        hx.errors.validation("Risk Information: Select Main Operating Country")

    if rf_risk_info.primary_listing_location is None and rf_risk_info.ownership_type == "Public":
        hx.errors.validation("Risk Information: Select Primary Listing Location")

    if rf_risk_info.industry_class_sic_code is None:
        hx.errors.validation("Risk Information: Select SIC Code")

    if utils.day_diff(hxd.hx_core.inception_date, hxd.hx_core.expiry_date, False) >= 367:
        risk_info.date_validation_flag = True
        risk_info.date_validation = "Policy Duration Longer Than One Year. Please Check Dates"




# Function that creates sector dropdown
# Looks up industry class or sic code depending on whether class or sic code is selected in risk_info_rf.search_sic
def create_sic_dropdown(hxd, df_sic, search_sic):

    col = "Sic Code" if search_sic == "Class" else "Sic Code2 (SIC first)"
    
    return df_sic[[col]].rename(columns={col: "SICClass"}).sort_values("SICClass").to_dict("records")

    



    


