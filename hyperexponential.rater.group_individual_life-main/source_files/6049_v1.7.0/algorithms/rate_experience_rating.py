import hx
import pandas as pd
import numpy as np
import math as math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from algorithms.rate_utilities import one_layer, ratio, pd_df_from_hx_list, look_up_closest
from algorithms.rate_utilities import sum_, array
from algorithms.rate_constants import benchmark_lr
pd.set_option('display.max_columns', None)


def rate_experience_rating(hxd):
    layer, cvg = one_layer(hxd)
    expe = hxd.cds.experience_rating
    expo = hxd.cds.exposure.granular
    claims = hxd.cds.experience_rating.claims
    tot = hxd.cds.experience_rating.claims_totals
    tblIBNR = hx.params.tblIBNR
    tblExposureWeights = hx.params.tblExposureWeights
    inception_date = hxd.hx_core.inception_date
    expiry_date = hxd.hx_core.expiry_date
    brokerage = layer.brokerage

    if not expe.claims_available:
        return

    # Get DataFrame with exposures
    lives = expo.lives
    lives_df = pd_df_from_hx_list(lives)

    # Set years
    inception_year = inception_date.year 
    [setattr(year, "year", inception_year - idx) for idx, year in enumerate(claims)]
    
    # Get selections
    if not expe.death_or_all_risks or not expe.cut_off_date:
        return

    ibnr_type = expe.death_or_all_risks + " " + hxd.cds.policy_info.direct_ri
    cut_off_date = expe.cut_off_date

    # Check date
    formatted_date = (inception_date - relativedelta(years=1)).strftime("%d/%m/%Y")
    if cut_off_date <= (inception_date - relativedelta(years=1)):
        expe.date_check = f"Cut-off date should be greater than {formatted_date}."
        expe.date_check_show = True
        hx.errors.validation(f"Cut-off date in Experience Rating should be greater than {formatted_date}.")
        return

    for idx, year in enumerate(claims):
        # Look up IBNR factor
        max_col = tblIBNR.shape[1] - 1
        col_no = idx + 1
        year.ibnr_factor = tblIBNR[tblIBNR["Col1"]==ibnr_type].iloc[0, col_no] if col_no <= max_col else 1

        # Calculate time adjustment
        next_year_date = cut_off_date + relativedelta(years=1)
        year.time_adj = ratio((next_year_date - inception_date).days, (expiry_date - inception_date).days) if idx == 0 else 1

        # Calculate burn
        year.burn = ratio(year.incurred * year.ibnr_factor, year.sum_insured * year.time_adj)
        year.burn_per_mille = year.burn * 1000

    # Calculate totals
    tot.no_lives = sum_("no_lives", claims)
    tot.sum_insured = sum_("sum_insured", claims)
    tot.incurred = sum_("incurred", claims)
    tot.number = sum_("number", claims)
    tot.burn = ratio(
        np.dot(array("incurred", claims), array("ibnr_factor", claims)),
        np.dot(array("sum_insured", claims), array("time_adj", claims))
    )
    tot.burn_per_mille = tot.burn * 1000

    # Calculate credibility and discounts
    expe.life_years = np.dot(array("no_lives", claims), array("time_adj", claims))
    expe.cred_weight = look_up_closest(
        lookup_value=expe.life_years,
        lookup_col="Over N lives",
        return_col="Credibility given",
        df=tblExposureWeights,
        lookup_type="single"
    )

    over_n_lives = look_up_closest(
        lookup_value=expe.life_years,
        lookup_col="Over N lives",
        return_col="Over N lives",
        df=tblExposureWeights,
        lookup_type="single"
    )
    expo_w_2nd_value = tblExposureWeights["Over N lives"].iloc[1]
    expo_w_param_a_2nd_value = tblExposureWeights["Parameter A"].iloc[1]
    expo_w_param_a_3rd_value = tblExposureWeights["Parameter A"].iloc[2]
    
    if expe.cred_weight == 0:
        expe.z_factor = 0
    elif over_n_lives == tblExposureWeights["Over N lives"].iloc[1]:
        expe.z_factor = ratio(
            (expe.life_years - expo_w_2nd_value),
            (expe.life_years + expo_w_param_a_2nd_value)
        )
    else:
        expe.z_factor = ratio(expe.life_years, (expe.life_years + expo_w_param_a_3rd_value))

    expe.one_minus_z = 1 - expe.z_factor

    total_exposed_si = sum(lives_df["sum_insured"])
    expe.burn_cost = tot.burn * total_exposed_si

    # The below should be safe because the df columns are coming from the hxd nodes
    # and if they're None, the sum function will return 0

    # Model premium - NOTE: used in a previous version of the rater where the discount was calculated through the model premium in the ratio
    db_model_premium = sum(lives_df[lives_df["db_technical_premium"] > 0]["db_technical_premium"])
    adb_model_premium = sum(lives_df[lives_df["adb_technical_premium"] > 0]["adb_technical_premium"])
    ti_model_premium = sum(lives_df[lives_df["ti_technical_premium"] > 0]["ti_technical_premium"])
    ci_model_premium = sum(lives_df[lives_df["ci_technical_premium"] > 0]["ci_technical_premium"])
    re_model_premium = sum(lives_df[lives_df["re_technical_premium"] > 0]["re_technical_premium"])
    death_model_premium = db_model_premium + adb_model_premium
    all_risk_model_premium = death_model_premium + ti_model_premium + ci_model_premium + re_model_premium

    # Expected loss
    db_el_cost_pre_uw_adj = sum(lives_df[lives_df["db_expected_loss_cost_pre_uw_adj"] > 0]["db_expected_loss_cost_pre_uw_adj"])
    adb_el_cost_pre_uw_adj = sum(lives_df[lives_df["adb_expected_loss_cost_pre_uw_adj"] > 0]["adb_expected_loss_cost_pre_uw_adj"])
    ti_el_cost_pre_uw_adj = sum(lives_df[lives_df["ti_expected_loss_cost_pre_uw_adj"] > 0]["ti_expected_loss_cost_pre_uw_adj"])
    ci_el_cost_pre_uw_adj = sum(lives_df[lives_df["ci_expected_loss_cost_pre_uw_adj"] > 0]["ci_expected_loss_cost_pre_uw_adj"])
    re_el_cost_pre_uw_adj = sum(lives_df[lives_df["re_expected_loss_cost_pre_uw_adj"] > 0]["re_expected_loss_cost_pre_uw_adj"])
    death_el_cost_pre_uw_adj = db_el_cost_pre_uw_adj + adb_el_cost_pre_uw_adj
    all_risk_el_cost_pre_uw_adj = death_el_cost_pre_uw_adj + ti_el_cost_pre_uw_adj + ci_el_cost_pre_uw_adj + re_el_cost_pre_uw_adj

    # Discounts
    expe.death_only_discount = ratio(
        expe.one_minus_z * death_el_cost_pre_uw_adj + (expe.z_factor * expe.burn_cost),
        death_el_cost_pre_uw_adj
    )
    expe.all_risk_discount = ratio(
        expe.one_minus_z * all_risk_el_cost_pre_uw_adj + (expe.z_factor * expe.burn_cost),
        all_risk_el_cost_pre_uw_adj
    )
    
    


