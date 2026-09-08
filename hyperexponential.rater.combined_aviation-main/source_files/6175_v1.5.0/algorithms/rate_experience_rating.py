import hx
import pandas as pd
import numpy as np
import math as math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from algorithms.rate_utilities import one_layer, ratio, pd_df_from_hx_list, write_pd_to_hxd, look_up
from algorithms.rate_utilities import sum_, array, usd, rgetattr, rsetattr
from algorithms.rate_constants import benchmark_lr


def rate_experience_rating(hxd, rating_df):
    layer, cvg = one_layer(hxd)
    expe = hxd.cds.experience_rating
    ms = hxd.model_state
    claims = expe.claims
    inception_date = hxd.hx_core.inception_date
    ccy = hxd.cds.currencies.source_currency
    current_yoa = inception_date.year

    hull = cvg.hull
    liab = cvg.liability
    tot = layer.totals

    al_DevFactors = hx.params.al_DevFactors
    ga_DevFactors = hx.params.ga_DevFactors
    HistoricPortfolioRC = hx.params.HistoricPortfolioRC # NOTE: can potentially link this to SQL table
    ClaimsInflation = hx.params.ClaimsInflation
    RateIncrease = hx.params.ga_RateIncrease # YZ: What is this RateIncrease? It now only have 2025
    claims_inflation_yoa = hx.params.Claims_Inflation_YOA

    # Exit early if no loss data available
    if not expe.claims_available:
        hull.benchmark_premium_exp = hull.exp_credibility = 0
        liab.benchmark_premium_exp = liab.exp_credibility = 0
        return

    # Show after Start Airlines/GA task has been pressed
    expe.show_experience_rating = expe.claims_available and ms.pressed_either_task


    # Convert dates to pandas Timestamps for comparison
    inception_ts = pd.Timestamp(inception_date)
    one_year_ago = inception_ts - relativedelta(years=1)

    # Check as-at date
    # YZ: Consider to add the validation for input number of years here too
    formatted_date = one_year_ago.strftime("%d/%m/%Y")
    if not expe.as_at_date:
        expe.show_date_message = True
        expe.as_at_date_message = "Please input the cut-off date for the claims (as-at date)."
        hx.errors.validation("Cut-off date for the claims (as-at date) must be input in Experience Rating.")
        return
    else:
        # Convert expe.as_at_date to a Timestamp for safe comparison
        as_at_ts = pd.Timestamp(expe.as_at_date)
        if as_at_ts <= one_year_ago:
            expe.show_date_message = True
            expe.as_at_date_message = f"Cut-off date should be greater than {formatted_date}."
            hx.errors.validation(f"Cut-off date in Experience Rating should be greater than {formatted_date}.")
            # return
    
    # Continue with Experience Rating
    coverages = ["hull", "liability"]

    # Perform the rest of the calculations in a df
    claims_df = pd_df_from_hx_list(claims)

    # Validate YOA
    if any(claims_df["yoa"].isna() | (claims_df["yoa"] <= 1900)):
        hx.errors.validation("YOA in Experience Rating cannot be empty and must be greater than 1900.")

    # On-level claims - NOTE: using inception date for inflation but as-at date for development
    claims_df["yoa"] = claims_df["yoa"].fillna(0)
    # claims_df["years_to_inception"] = inception_date.year - claims_df["yoa"]
    claims_df["quarter"] = math.ceil(expe.as_at_date.month / 3) + (expe.as_at_date.year - claims_df["yoa"]) * 4

    # Functionalise checking columns for None/NaN
    def safe(operation, columns_to_check, claims_df=claims_df):
        condition = np.logical_or.reduce([pd.isna(claims_df[col]) for col in columns_to_check])
        result = np.where(condition, None, operation)
        return pd.Series(result)

    for cov in coverages:
        cover = cov[:4] # Get the first 4 characters of Hull, Liability -> Hull, Liab

        # Calculate cumulative rate change
        if hxd.cds.rater == "Airlines":
            claims_df[f"{cover}_portfolio_rc"] = look_up(claims_df["yoa"], "YOA", f"Airlines {cover.capitalize()} Rate Change", HistoricPortfolioRC) 
        else:
            claims_df[f"{cover}_portfolio_rc"] = look_up(claims_df["yoa"], "YOA", f"GA {cover.capitalize()} Rate Change", HistoricPortfolioRC) 
        
        claims_df[f"{cover}_rc_to_use"] = claims_df[f"{cover}_rate_change"].fillna(claims_df[f"{cover}_portfolio_rc"]).fillna(1)
        claims_df.loc[0, f"{cover}_cumul_rc"] = rgetattr(cvg, f"{cov}/rate_change") if rgetattr(cvg, f"{cov}/rate_change") else 1 # YZ: Asign the starting point of the cumul_rc
        
        for i in range(1, len(claims_df)): # Choosing a loop to improve readability. Cumulative rc
            if pd.isna(claims_df.loc[i, f"{cover}_rc_to_use"]): # This is to check whether there are entered RARC on Risk Information tab
                claims_df.loc[i, f"{cover}_cumul_rc"] = claims_df.loc[i - 1, f"{cover}_cumul_rc"]
            else:
                claims_df.loc[i, f"{cover}_cumul_rc"] = claims_df.loc[i - 1, f"{cover}_cumul_rc"] * claims_df.loc[i - 1, f"{cover}_rc_to_use"]

        # On-levelling
        # YZ 08/06/2026: Add inflation lookup by YOA
        #claims_df[f"{cover}_inflation"] = (1 + look_up(cov.capitalize(), "Cover", "Inflation", ClaimsInflation, lookup_type="single")) ** claims_df["years_to_inception"].fillna(0)
        
        default_inflation = look_up(cov.capitalize(), "Cover", "Inflation", ClaimsInflation, lookup_type="single")
        claims_df[f"{cover}_inflation_yoa"] = 1 + look_up(claims_df["yoa"], "YOA", f"{cover.capitalize()}", claims_inflation_yoa)
        claims_df[f"{cover}_inflation_yoa"] = claims_df[f"{cover}_inflation_yoa"].fillna(1+default_inflation)

        # Calculate the cumulative inflation
        claims_df[f"{cover}_inflation"] = 1.0
        subset = claims_inflation_yoa[claims_inflation_yoa["YOA"] == current_yoa][f"{cover.capitalize()}"]
        value = default_inflation if subset.empty or pd.isna(subset.iloc[0]) else subset.iloc[0]
        claims_df.loc[0, f"{cover}_inflation"] = 1+value

        for i in  range (1, len(claims_df)): # Choosing a loop to improve readability. Cumulative Inflation
            claims_df.loc[i, f"{cover}_inflation"] = claims_df.loc[i-1, f"{cover}_inflation"] * claims_df.loc[i-1, f"{cover}_inflation_yoa"]
        
        # On level the premium
        claims_df[f"{cover}_as_if_premium"] = safe(
            claims_df[f"{cover}_gross_premium"] * claims_df[f"{cover}_exposure_adj"] * (claims_df[f"{cover}_cumul_rc"] if expe.historic_premium_known else 1), 
            [f"{cover}_gross_premium", f"{cover}_exposure_adj"]
        )

        if hxd.cds.rater == "Airlines":
            claims_df[f"{cover}_pct_developed"] = look_up(claims_df["quarter"], "Quarter", f"Airlines {cover.capitalize()}", al_DevFactors, if_not_found=1)
        else:
            claims_df[f"{cover}_pct_developed"] = look_up(claims_df["quarter"], "Quarter", f"Aviation {cover.capitalize()}", ga_DevFactors, if_not_found=1)
        
        # Ultimates
        claims_df[f"{cover}_ult_attr_claims"] = safe(
            ratio(claims_df[f"{cover}_attr_claims"] * claims_df[f"{cover}_inflation"], claims_df[f"{cover}_pct_developed"]),
            [f"{cover}_attr_claims", f"{cover}_inflation", f"{cover}_pct_developed"]
        )
        claims_df[f"{cover}_ulr"] = safe(
            ratio(claims_df[f"{cover}_ult_attr_claims"], claims_df[f"{cover}_as_if_premium"]),
            [f"{cover}_ult_attr_claims", f"{cover}_as_if_premium"]
        )

    # Push df to hxd
    claims_df = claims_df.fillna(np.nan).replace([np.nan], [None])
    output_cols = [
        "hull_portfolio_rc",
        "hull_rc_to_use",
        "hull_cumul_rc",
        "hull_inflation",
        "liab_portfolio_rc",
        "liab_rc_to_use",
        "liab_cumul_rc",
        "liab_inflation",
        "hull_as_if_premium",
        "hull_pct_developed",
        "hull_ult_attr_claims",
        "hull_ulr",
        "liab_as_if_premium",
        "liab_pct_developed",
        "liab_ult_attr_claims",
        "liab_ulr"
    ]
    write_pd_to_hxd(claims_df, claims, output_cols)

    # Large Loss Loading
    if hxd.cds.is_ga:
        expe.hull.max_insured_loss = ratio(
            (rating_df["exp_total_losses"] * rating_df["hull_severity"]).sum(),
            rating_df["exp_total_losses"].sum()
        )
        expe.liability.max_insured_loss = ratio(
            (rating_df["pax_exp_total_losses"] * rating_df["pax_apply_occ_limit_ded_to_max_loss"]).sum(),
            rating_df["pax_exp_total_losses"].sum()
        )
    else:
        expe.hull.max_insured_loss = ratio(
            (rating_df["bm_hull_large_severity"] * rating_df["hull_frequency"]).sum(),
            rating_df["hull_frequency"].sum()
        )
        expe.liability.max_insured_loss = ratio(
            (rating_df["bm_liab_large_severity"] * rating_df["bm_liab_large_frequency"]).sum(),
            rating_df["bm_liab_large_frequency"].sum()
        )

    expe.hull.implied_lllr = ratio(expe.hull.max_insured_loss, usd(hull.quoted_premium, ccy))
    expe.liability.implied_lllr = ratio(expe.liability.max_insured_loss, usd(liab.quoted_premium, ccy))

    # Implied RP
    if hxd.cds.is_ga:
        expe.hull.implied_rp = ratio(1, rating_df["exp_total_losses"].sum())
        expe.liability.implied_rp = ratio(1, rating_df["pax_exp_total_losses"].sum())
    else:
        expe.hull.implied_rp = ratio(1, rating_df["hull_frequency"].sum())
        expe.liability.implied_rp = ratio(1, rating_df[rating_df["aircraft_status"] == "In Service"]["bm_liab_large_frequency"].sum())
    
    expe.hull.large_loss_loading = ratio(expe.hull.implied_lllr, expe.hull.implied_rp)
    expe.liability.large_loss_loading = ratio(expe.liability.implied_lllr, expe.liability.implied_rp)

    # Summary
    cvg_objs = [hull, liab]
    expe_cvg_objs = [expe.hull, expe.liability]

    filtered_RateIncrease = RateIncrease[RateIncrease["Year"] <= inception_date.year]
    hull_rate_increase = filtered_RateIncrease["Hull"].iloc[0] if (not filtered_RateIncrease["Hull"].empty) and (hxd.cds.is_ga) else 1
    liab_rate_increase = filtered_RateIncrease["Liability"].iloc[0] if (not filtered_RateIncrease["Liability"].empty) and (hxd.cds.is_ga) else 1

    for cov, c_obj, e_obj in zip(coverages, cvg_objs, expe_cvg_objs):
        cover = cov[:4]

        e_obj.actual_no_of_years = claims_df[f"{cover}_attr_claims"].notna().sum()
        e_obj.quoted_premium = c_obj.quoted_premium
        e_obj.implied_attr_lr = ratio(
            (claims_df[f"{cover}_as_if_premium"] * claims_df[f"{cover}_ulr"]).sum(), 
            claims_df[f"{cover}_as_if_premium"].sum()
        ) * (hull_rate_increase if cov == "hull" else liab_rate_increase)
        
        e_obj.expected_lr = e_obj.implied_attr_lr + e_obj.large_loss_loading
        e_obj.expected_claims_label = f"{inception_date.year} Expected Claims"
        e_obj.expected_claims = e_obj.quoted_premium * e_obj.expected_lr

        y = e_obj.actual_no_of_years
        exp_y = np.exp(y - 2) 
        al_credibility = (y > 0) * ratio(exp_y, 25 + exp_y) * 0.5 * (1 - 0.5 * (e_obj==expe.liability))
        ga_credibility = (y > 0) * ratio(exp_y, 10 + exp_y) * 0.7

        e_obj.credibility = al_credibility if hxd.cds.rater == "Airlines" else ga_credibility

   