import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import ratio
from algorithms import parameter_tables_schema as params
from operator import itemgetter
import algorithms.rate_utilities as utils


def rate_rating_summary_mmp(hxd):
    
    mmp = hxd.cds.mmp

    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"



    #This is to set the option label
    # for index, x in enumerate(hxd.cds.layers):
    #     x.option_label = f"Option {index+1}"

    # Assigning Coverage TPIs and BPIs to the View
    for i in ("dno", "epl", "cll"):

        coverage = getattr(mmp, i)
        quoted_premium_100 = 0 if coverage.quoted_premium_100 is None else coverage.quoted_premium_100
        written_line = 1 if coverage.written_line is None else coverage.written_line

        bound_premium = quoted_premium_100 * written_line

        coverage.tpi = ratio(bound_premium, coverage.technical_premium, 0)
        coverage.bpi = ratio(bound_premium, coverage.benchmark_premium, 0)


    # Assigning Total Calculated Figures Such as Premium, Technical Premium, ..., etc.

    # Getting Figures and Replacing Nones with Zeros
    for i in ("quoted_premium_100", "brokerage", "written_line", "technical_premium", "benchmark_premium"):
        exec(f"globals()['mmp_coverage_{i}'] = [value if value is not None else 0 for value in [mmp.dno.{i}, mmp.epl.{i}, mmp.cll.{i}]]")

    mmp.total.quoted_premium_100 = sum(mmp_coverage_quoted_premium_100) or 0

    mmp.total.quoted_premium_annual_100 = ((mmp.total.quoted_premium_100 or 0) / hxd.cds.rating_factors.risk_information.policy_term) or 0


    # Totals Row is a Weighted Average by Premium. (Included a small positive value to avoid divide by zero errors)
    mmp.total.brokerage = np.average(np.array(mmp_coverage_brokerage), weights = np.array(mmp_coverage_quoted_premium_100 + np.float64(0.00001)))

    written_line_array = np.array([
        1 if mmp.dno.written_line is None else mmp.dno.written_line,
        1 if mmp.epl.written_line is None else mmp.epl.written_line,
        1 if mmp.cll.written_line is None else mmp.cll.written_line,
    ])

    mmp.total.written_line = np.average(written_line_array, weights = np.array(mmp_coverage_quoted_premium_100 + np.float64(0.00001)))

    mmp.total.technical_premium = sum(mmp_coverage_technical_premium)

    mmp.total.benchmark_premium = sum(mmp_coverage_benchmark_premium)

    mmp.total.benchmark_premium_100 = (mmp.total.benchmark_premium or 0) / mmp.total.written_line

    mmp.total.benchmark_premium_annual_100 = ((mmp.total.benchmark_premium_100 or 0) / hxd.cds.rating_factors.risk_information.policy_term) or 0

    mmp.total.tpi = ratio(mmp.total.quoted_premium_100 * mmp.total.written_line, mmp.total.technical_premium, 0)

    mmp.total.bpi = ratio(mmp.total.quoted_premium_100 * mmp.total.written_line, mmp.total.benchmark_premium, 0)

    # MMP PFLR
    
    if mmp.total.quoted_premium_100 is not None:
        mmp.total.pflr = utils.ratio(mmp.total.expected_loss_cost , (mmp.total.quoted_premium_100 * (1 - mmp.total.brokerage)), 0)
    else:
        mmp.total.pflr = None

    # Appetite Comments
    if hxd.cds.rating_factors.risk_information.industry_class_sic_code is not None:
        sic = int(utils.extract_sic(hxd.cds.rating_factors.risk_information.industry_class_sic_code).lstrip("0"))
        hxd.cds.mmp.dno.appetite_comment = utils.look_up(sic, "SIC", "Directors & Officers (D&O)", hx.params.tbl_mmp_appetite)
        if (hxd.cds.exposure.aggregate.us_ftes is not None and hxd.cds.exposure.aggregate.us_ftes > 1000):
            hxd.cds.mmp.epl.appetite_comment = "Outside"
        else:
            hxd.cds.mmp.epl.appetite_comment = utils.look_up(sic, "SIC", "Employer Practice Liability (EPL)", hx.params.tbl_mmp_appetite)
            hxd.cds.mmp.cll.appetite_comment = utils.look_up(sic, "SIC", "Corporate Legal Liability (CLL)", hx.params.tbl_mmp_appetite)



    # Validation for Inputs
    for j in ("dno", "epl", "cll"):  # coverage abbreviations
        cov_obj = getattr(hxd.cds.mmp, j)
        for opt_num in range(1, 5):  # option_1 .. option_4
            opt_obj = getattr(cov_obj, f"option_{opt_num}")
            for k in ("aggregate_limit", "aggregate_excess", "aggregate_deductible"):
                val = getattr(opt_obj, k)
                if val is not None and val < 0:
                    hx.errors.fatal("Rating Summary MMP: Entered value must be greater than zero.")
                    

    for cov in ("dno", "epl", "cll"):  # coverage abbreviations
        cov_obj = getattr(hxd.cds.mmp, cov)
        for field in ("limit", "excess", "deductible", "quoted_premium_100", "brokerage", "written_line"):
            val = getattr(cov_obj, field)
            if val is not None and val < 0:
                hx.errors.fatal("Rating Summary MMP: Entered value must be greater than zero")

    if mmp.total.status == "Bound" and mmp.total.section_reference is None:
            hx.errors.validation("Rating Summary MMP: Bound policy must have a Section Reference")

    # if hxd.cds.risk_information.mmp_flag is True and mmp.total.status is None:
    #     hx.errors.validation("Rating Summary MMP: Status must be set to mark a policy as final")


    # Validation on MMP Definition. This isn't a hard validation and policy can still be written if validation requires aren't met. Instead this notes to the 
    # UW that the given MMP definition isn't met.

    risk_info = hxd.cds.rating_factors.risk_information
    exp = hxd.cds.exposure.aggregate

    mmp.total.validation_note = ""

    # Exposure Metric

    if risk_info.ownership_type == "Private" and (
    (exp.total_assets is not None and exp.total_assets > 2.5e9) or
    (exp.net_sales is not None and exp.net_sales > 2.5e9)):
        mmp.total.validation_note += "Exposure above 2,500,000,000. Please Check. \n"
    elif risk_info.ownership_type == "Public" and (max(exp.market_cap_2_year_high or 0, exp.current_market_cap or 0) > 1.5e9):
        mmp.total.validation_note += "Market Cap above 1,500,000,000. Please Check. \n"
                                                                                    
    # High Risk Segment
    if risk_info.industry_class_sic_code is not None:
        if utils.look_up(int(utils.extract_sic(risk_info.industry_class_sic_code).lstrip("0")), "SIC", "MMP - High Risk Segments", hx.params.tbl_sic_freq) == "Yes":
            mmp.total.validation_note += "High Risk Industry Segment. \n"

    # Australia 
    if exp.us_listing_share == 1:
        country = risk_info.main_operating_country
    elif hxd.cds.risk_information.public_flag is True:
        country = risk_info.primary_listing_location
    else:
        country = risk_info.main_operating_country

    if country == "AUSTRALIA":
        mmp.total.validation_note += "Australian Company. \n"

    # Israel
    if country == "ISRAEL":
        mmp.total.validation_note += "Israeli Company. \n"

    # Level 2 and Above Listing
    if exp.adr_level in ("Full Listing", "Level 2", "Level 3") and risk_info.ownership_type == "Public":
        mmp.total.validation_note += "US Listed (Level 2 and above). \n"

    # Exposure has US FTEs, this sets all EPL premiums to zero
    if hxd.cds.exposure.aggregate.us_ftes is not None and hxd.cds.exposure.aggregate.us_ftes > 0:
        hxd.cds.mmp.epl.technical_premium = 0
        hxd.cds.mmp.epl.option_1.technical_premium = 0
        hxd.cds.mmp.epl.option_2.technical_premium = 0
        hxd.cds.mmp.epl.option_3.technical_premium = 0
        hxd.cds.mmp.epl.option_4.technical_premium = 0
        hxd.cds.mmp.epl.benchmark_premium = 0
        hxd.cds.mmp.epl.tpi = 0
        hxd.cds.mmp.epl.bpi = 0
        mmp.total.validation_note += "\n EPL Premiums Set to Zero as has US Employees. Use MyRate Rater. \n"




    # Checks if the validation note isn't empty and adds explanation
    if mmp.total.validation_note != "":
        mmp.total.validation_note = "Does not fit the MMP definition due to: \n" + mmp.total.validation_note
    

    if hxd.cds.rate_change.has_rarc_not_run is True and hxd.cds.rate_change.has_fetch_not_run is False:
        hx.errors.validation("Rate Change: 'Calculate Rate Change' must be run")
        

    a = 1


