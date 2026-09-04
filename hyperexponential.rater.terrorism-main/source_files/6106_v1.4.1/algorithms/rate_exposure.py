##############################################################################################################################
################                             NOTES                                                            ################ 
##############################################################################################################################

### Below is organised into 3 exposure rating functions:
###     a) rate_cover_details   - XXXXXXXXX
###     b) rate_exposure        - XXXXXXXXX
###     c) rate_construction    - XXXXXXXXX
###

##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

###  1) row 260 x 5 rows - potential double counting
###  2) row 240 construction build up formula
###  3) 
###  4) 
###  5)
###  6) 
###  7) 
###  8) 
###  9) 
### 10)
##############################################################################################################################




import hx
import math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from algorithms.rate_utilities import one_layer, look_up, look_up_closest, ratio, rgetattr, rsetattr, pd_df_from_hx_list, title_rc, write_pd_to_hxd
from algorithms.rate_utilities import mbbefd, linear_interp, policy_term, tp_components
from algorithms.data_schema.sch_rater_defined import risks, constr_premium_nodes
from algorithms.rate_constants import benchmark_lr, bi_weighting

# Initialise parameter tables
UWRatingFactors = hx.params.UWRatingFactors
IHSUWAdjustment = hx.params.IHSUWAdjustment
IHSRate = hx.params.IHSRate
Scaling = hx.params.UWModifiersScaling

def rate_cover_details(hxd):
    cds = hxd.cds
    layer, cvg = one_layer(hxd)
    expo = hxd.cds.exposure.aggregate

    # Get countries
    countries_df = pd_df_from_hx_list(cds.exposure.granular.countries)
    
    # AC request - 22-July-25 calc bi or pd si after infilling using tsi & bi_weighting where dont have at a bi / pd level
    countries_df['bipd_si_or_nil']  = countries_df["bi_sum_insured"].fillna(0)  +  countries_df["pd_sum_insured"].fillna(0)
    countries_df['tsi_or_nil']      = countries_df["total_sum_insured"].fillna(0)
    countries_df['bi_si_infill']    = np.where(  countries_df['tsi_or_nil']==0,   countries_df["bi_sum_insured"].fillna(0),    countries_df['tsi_or_nil']  *  (    bi_weighting))
    countries_df['pd_si_infill']    = np.where(  countries_df['tsi_or_nil']==0,   countries_df["pd_sum_insured"].fillna(0),    countries_df['tsi_or_nil']  *  (1 - bi_weighting))

    # set mask to filter out any country where the name not filled in and establish if resulting df is empty
    mask_ctry_not_null       = countries_df["country"].notna()                                    
    countries_mask_df        = countries_df[mask_ctry_not_null]
    empty_dataframe          = countries_mask_df.empty

    # AC request - 22-July-25 calc bi or pd si after infilling using tsi & bi_weighting where dont have at a bi / pd level and then calculate total from it
    expo.bi_sum_insured      = 0 if empty_dataframe else countries_mask_df["bi_si_infill"].sum(skipna=True)
    expo.pd_sum_insured      = 0 if empty_dataframe else countries_mask_df["pd_si_infill"].sum(skipna=True)
    expo.total_sum_insured   = expo.bi_sum_insured + expo.pd_sum_insured

    expo.no_of_locations     = 0 if empty_dataframe else countries_mask_df["no_of_locations"].sum(skipna=True)
    expo.policy_limit        = 0 if empty_dataframe else countries_mask_df["limit"].fillna(0).max()
    expo.policy_sublimit     = 0 if empty_dataframe else countries_mask_df["sublimit"].fillna(0).max()
    expo.policy_excess       = 0 if empty_dataframe else countries_mask_df["excess"].fillna(0).min()
    expo.policy_deductible   = 0 if empty_dataframe else countries_mask_df["deductible"].fillna(0).min()




def rate_exposure(hxd, roe_df):

    # Defining pointers
    layer, cvg          = one_layer(hxd)
    ra                  = layer.risk_adjustments
    expo_a              = hxd.cds.exposure.aggregate
    expo_g              = hxd.cds.exposure.granular
    AggregateDiscount   = hx.params.AggregateDiscount

    is_migrated         = hxd.model_state.is_migrated


    # Calculate agg discount
    expo_limit_ratio = expo_g.expo_limit_ratio or 0
    if expo_a.details.limit_type == "Occurrence only":
        expo_a.agg_discount = 0
    elif expo_limit_ratio > AggregateDiscount["Trapped Exposure"].iloc[-1]:
        expo_a.agg_discount = 1 - AggregateDiscount["Agg Discount"].iloc[-1]
    else:
        expo_a.agg_discount = 1 - linear_interp(AggregateDiscount["Trapped Exposure"], AggregateDiscount["Agg Discount"], expo_limit_ratio)
    
    # Set risk scores
    ihs_risks = {"ihs_score_read_only","ihs_score_expiring","ihs_score"}
    
    for risk in risks.keys():
        if risk not in ihs_risks:
            risk_table  = UWRatingFactors
            risk_level  = rgetattr(ra, f"{risk}/level")

            min_score   = look_up(risk_level, "Category", "Min", risk_table, lookup_type="single")
            max_score   = look_up(risk_level, "Category", "Max", risk_table, lookup_type="single")
            rsetattr(ra, f"{risk}/min", min_score)
            rsetattr(ra, f"{risk}/max", max_score)

            description_col = f"{risk.capitalize()} Risk"
            description     = look_up(risk_level, "Category", description_col, risk_table, lookup_type="single")
            rsetattr(ra, f"{risk}/description", description)

            score_range     = range(int(min_score), int(max_score) + 1)
            mid_point       = int(len(score_range) / 2)
            override_score  = rgetattr(ra, f"{risk}/override")
            
            rsetattr(ra, f"{risk}/scores", [{"score": s} for s in score_range])
            rsetattr(ra, f"{risk}/calculated", score_range[mid_point])
            rsetattr(ra, f"{risk}/selected", score_range[mid_point] if override_score is None else override_score) # had to use "override_score is None" as sometime we have nil which "not override_score" returns True to


    # Treat IHS score separately - NOTE: old approach; keeping it here for rate reconciliation
    total_sum_insured = 0
    ihs_score_default = 0
    ihs_score_selected = 0

    if not roe_df.empty:
        total_sum_insured   = roe_df["selected_sum_insured"].sum()
        tsi_default_x_na    = (roe_df[pd.notna(roe_df["ihs_average_default"])]["selected_sum_insured"]).sum(skipna=True)
        tsi_select_x_na     = (roe_df[pd.notna(roe_df["ihs_average_selected"])]["selected_sum_insured"]).sum(skipna=True)
        ihs_score_default   = ratio((roe_df["ihs_average_default"]  * roe_df["selected_sum_insured"]).sum(skipna=True) or 0, tsi_default_x_na, 0)
        ihs_score_selected  = ratio((roe_df["ihs_average_selected"] * roe_df["selected_sum_insured"]).sum(skipna=True) or 0, tsi_select_x_na, 0)


        ## convert roe calculated & selected by 3 ihs groups and country to an overall, in order to calculate impact of ihs uw adjustments
        
        # specify columns for cross multiplication in order to determine overall roe
        roe_calc_cols   = ["terrorism_roe_calculated",  "civil_unrest_roe_calculated",  "war_roe_calculated"]
        roe_sel_cols    = ["terrorism_roe_selected",    "civil_unrest_roe_selected",    "war_roe_selected"]
        cvg_cols        = ["cvg_terrorism",             "cvg_civil_unrest",             "cvg_war"]
        subcvg_cols     = ["subcvg_terrorism",          "subcvg_civil_unrest",          "subcvg_war"]
        
        # determine a matrix of weights varying by row depending on whethere cvg or sub_cvg
        cvg_wgt_test_ss = roe_df[cvg_cols].sum(axis=1) == 0
        cvg_wgt_mtx     = np.where(  cvg_wgt_test_ss[:,np.newaxis],    roe_df[subcvg_cols].values,    roe_df[cvg_cols].values)       # newaxis was needed here to convert from a 1d array to 2d array for the np.where to function as intended
        
        # apply matrix of weights and calc max across columns (consistent main algo) to give an overall roe by country
        roe_calc_ss     = roe_df[  roe_calc_cols  ].mul(  cvg_wgt_mtx  ).max(axis=1)
        roe_sel_ss      = roe_df[  roe_sel_cols   ].mul(  cvg_wgt_mtx  ).max(axis=1)
        
        # calculate overall roe by weighting each country roe by selected sum insured
        roe_calc_overall= ratio((roe_calc_ss * roe_df["selected_sum_insured"]).sum(skipna=True) or 0, total_sum_insured, 0)
        roe_sel_overall = ratio((roe_sel_ss  * roe_df["selected_sum_insured"]).sum(skipna=True) or 0, total_sum_insured, 0)

    # update ihs_score_selected to contemplate migrated and whether it has overrides
    risk_table         = IHSUWAdjustment
    ihs_score_max      = risk_table["Max"].iat[-1]
    ihs_score_min      = risk_table["Min"].iat[0]

    # update ihs_score_selected for migrated risks considering overrides, max allowed and otherwise default
    if is_migrated:
        if ra.ihs_score.override:   ihs_score_selected = max(ihs_score_min,  min(ihs_score_max,  ra.ihs_score.override))
        else:                       ihs_score_selected = ihs_score_default

    # determine risk_level on ihs_score_selected 
    risk_table_filtered= risk_table[    risk_table["Min"] <= ihs_score_selected   ]                         # find all values <= max
    risk_table_filtered= risk_table if risk_table_filtered.empty else risk_table_filtered                   # error trap empty df
    risk_level         = risk_table_filtered["Category"].iat[-1]                                            # take bottom row of resulting table

    # determine min, max, description on ihs_score_selected
    min_score   = look_up(risk_level, "Category", "Min",     risk_table, lookup_type="single")
    max_score   = look_up(risk_level, "Category", "Max",     risk_table, lookup_type="single")
    description = look_up(risk_level, "Category", "IHSRisk", risk_table, lookup_type="single")

    # assigning values for ihs_risks
    for ihs_risk in ihs_risks:
        if ihs_risk != "ihs_score_expiring":
            rsetattr(ra, f"{ihs_risk}/calculated",  ihs_score_default   )
            rsetattr(ra, f"{ihs_risk}/selected",    ihs_score_selected  )
            rsetattr(ra, f"{ihs_risk}/level",       risk_level          )
            rsetattr(ra, f"{ihs_risk}/min",         min_score           )
            rsetattr(ra, f"{ihs_risk}/max",         max_score           )
            rsetattr(ra, f"{ihs_risk}/description", description         )

    
    # Validate override score for each risk
    for risk in risks.keys():
        rsetattr(ra, f"{risk}/is_override_invalid", False)
        rsetattr(ra, f"{risk}/is_override_valid", True)

        override_score  = rgetattr(ra, f"{risk}/override")
        min_score       = rgetattr(ra, f"{risk}/min")
        max_score       = rgetattr(ra, f"{risk}/max")

        if (is_migrated or risk not in ihs_risks):                                                                      # we dont want to do this test on ihs if it is not migrated
            if (override_score is not None) and ((override_score < min_score) or (override_score > max_score)):
                rsetattr(ra, f"{risk}/is_override_invalid", True)
                rsetattr(ra, f"{risk}/is_override_valid", False)
                risk_name = risk.replace("score", "")
                hx.errors.validation(f"{title_rc(risk_name)} Override Score in Exposure Details is invalid. Please enter a number between the min and max value.")

    if is_migrated:
        # Calculate ROE
        ihs_score_calculated        = ra.ihs_score.calculated
        ihs_score_selected          = ra.ihs_score.selected

        ihs_terrorism_c_calc        = look_up_closest(ihs_score_calculated, "ihs_score", "terrorism_c", IHSRate, if_not_found=0, lookup_type="single")
        ihs_terrorism_b_calc        = look_up_closest(ihs_score_calculated, "ihs_score", "terrorism_b", IHSRate, if_not_found=0, lookup_type="single")
        ra.ihs_score.roe_calculated = ( ihs_terrorism_c_calc    *    np.exp(ihs_terrorism_b_calc * ihs_score_calculated)    )
        

        ihs_terrorism_c_sel         = look_up_closest(ihs_score_selected,   "ihs_score", "terrorism_c", IHSRate, if_not_found=0, lookup_type="single")
        ihs_terrorism_b_sel         = look_up_closest(ihs_score_selected,   "ihs_score", "terrorism_b", IHSRate, if_not_found=0, lookup_type="single") 
        ra.ihs_score.roe_selected   = (ihs_terrorism_c_sel      *    np.exp(ihs_terrorism_b_sel  * ihs_score_selected)      )
    else:
        ra.ihs_score.roe_calculated = roe_calc_overall
        ra.ihs_score.roe_selected   = roe_sel_overall

    # Calculate summary
    ra.total_adj_score          = sum([rgetattr(ra, f"{risk}/selected") for risk in risks.keys() if risk not in {"ihs_score_read_only","ihs_score_expiring","ihs_score"} ])
    ra.uw_ihs_adjustment        = ratio(ra.ihs_score.roe_selected, ra.ihs_score.roe_calculated, 1) if ra.ihs_score.calculated != 0 else 1
    low_scaling                 = look_up("Low",  "Type", "Step", Scaling, lookup_type="single")
    high_scaling                = look_up("High", "Type", "Step", Scaling, lookup_type="single")
    ra.uw_multiplier            = ra.uw_ihs_adjustment * (1 - (ra.total_adj_score - 30) * (low_scaling if ra.total_adj_score < 30 else high_scaling))


def rate_construction(hxd, roe_df):
    cds         = hxd.cds
    sf          = cds.standard_fields
    layer, cvg  = one_layer(hxd)
    ra          = layer.risk_adjustments
    
    c           = cvg.construction
    expo        = hxd.cds.exposure.aggregate
    brokerage   = layer.brokerage

    # Get NMP load
    tp_dict     = tp_components(hxd, sf.benchmark_class)
    nmp_load    = tp_dict["nmp_load"]

    # Use datetime to allow for fractional days
    inception_date  = datetime(hxd.hx_core.inception_date.year, hxd.hx_core.inception_date.month,   hxd.hx_core.inception_date.day)
    expiry_date     = datetime(hxd.hx_core.expiry_date.year,    hxd.hx_core.expiry_date.month,      hxd.hx_core.expiry_date.day   )

    # Initialise param tables
    Construction        = hx.params.Construction
    AggregateDiscount   = hx.params.AggregateDiscount
    AggUsage            = hx.params.AggUsage
    BusPlanLossRatios   = hx.params.BusPlanLossRatios
    SalzmannB           = hx.params.SalzmannB

    # For page to show
    expo.has_construction = c.is_covered
    
    # factors to apply to pre uw adj - migrated approach used all figures before ihs, new approach main df is calculated after uw adjusting ihs
    uw_multiplier       = ra.uw_multiplier
    uw_ihs_multiplier   = ra.uw_ihs_adjustment
    is_migrated         = hxd.model_state.is_migrated
    pre_uw_adj_factor   = 1 if is_migrated else (uw_ihs_multiplier or 1)  

    # Calculate days difference - NOTE: needed in rating summary
    c.days_difference = (expiry_date - inception_date).days

    if (not c.is_covered) or (roe_df.empty):
        return

    # Set years for construction build-up
    for idx, year in enumerate(c.years):
        year.year = f"Year {idx + 1}"

    # Allow build-up table to be transposed
    c.are_years_vertical = not c.are_years_horizontal

    # Add default thirds
    c.thirds = Construction.to_dict("records")

    # Calculate end dates - defining separate variables to maintain datetime
    days = c.days_difference / 3
    end_date_1 = inception_date + timedelta(days=days)
    end_date_2 = end_date_1 + timedelta(days=days)
    end_date_3 = end_date_2 + timedelta(days=days)

    c.thirds[0].end_date = end_date_1
    c.thirds[1].end_date = end_date_2
    c.thirds[2].end_date = min(end_date_3, inception_date + relativedelta(years=5))

    # Calculate year end dates for build-up
    for idx, year in enumerate(c.years):
        prev_year_idx               = max(0, idx - 1)
        current_end_date            = inception_date + relativedelta(years=idx + 1)
        previous_end_date           = c.years[prev_year_idx].end_date or (current_end_date + relativedelta( years = -1 ))
        if previous_end_date:
            previous_end_datetime   = datetime(previous_end_date.year,    previous_end_date.month,    previous_end_date.day) # to allow comparison of datetime values
    
        if current_end_date        <= expiry_date:      year.end_date = current_end_date
        elif previous_end_datetime <  expiry_date:      year.end_date = expiry_date

        # Calculate proposed build-up
        if year.end_date is None:
            continue

        year_end_date = datetime(year.end_date.year, year.end_date.month, year.end_date.day)
        
        in_yr_build_up_0 = c.thirds[0].build_up * (year_end_date - inception_date).days / (end_date_1 - inception_date).days
        in_yr_build_up_1 = c.thirds[1].build_up * (year_end_date - end_date_1    ).days / (end_date_2 - end_date_1    ).days
        in_yr_build_up_2 = c.thirds[2].build_up * (year_end_date - end_date_2    ).days / (end_date_3 - end_date_2    ).days
        
        if   year_end_date <= end_date_1:   year.build_up_calculated = in_yr_build_up_0 
        elif year_end_date <= end_date_2:   year.build_up_calculated = in_yr_build_up_1 + c.thirds[0].build_up
        else:                               year.build_up_calculated = in_yr_build_up_2 + c.thirds[1].build_up + c.thirds[0].build_up

        # Assign proposed to selected
        year.build_up_selected = year.build_up_override or year.build_up_calculated

        if year.build_up_selected is None:
            continue
        
        # Sum insured
        year.sum_insured = expo.total_sum_insured * year.build_up_selected

        # ROE
        year.total_cvg_nl_roe    = roe_df["total_cvg_nl_roe"].iloc[0]
        year.total_subcvg_nl_roe = roe_df["total_subcvg_nl_roe"].iloc[0]

        # Exposure curves
        b = SalzmannB["b"].iloc[0]
        g = SalzmannB["g"].iloc[0]
        
        lim_xs          = expo.policy_limit    + expo.policy_excess
        sublim_xs       = expo.policy_sublimit + expo.policy_excess
        sublim_xs_ded   =(0 if expo.policy_sublimit != 0 else expo.policy_deductible) + sublim_xs                     # jb check this seems strange to contemplate sublimit
        sublim_pol_sel  =(0 if expo.policy_sublimit == 0 else expo.policy_excess    ) + expo.policy_excess   # jb check this seems strange doublecounting

        cvg_x_higher    = min(  ratio(lim_xs,         year.sum_insured),   1)                                       
        cvg_x_lower     = min(  ratio(sublim_xs_ded,  year.sum_insured),   1)                                                           # jb check this seems strange to contemplate sublimit
        subcvg_x_higher = min(  ratio(sublim_xs,      year.sum_insured),   1)                                       
        subcvg_x_lower  = min(  ratio(sublim_pol_sel, year.sum_insured),   1)                                                           # jb check this seems strange to contemplate sublimit as it does

        year.cvg_expo_curve    = mbbefd(b, g, cvg_x_higher)    - mbbefd(b, g, cvg_x_lower)
        year.subcvg_expo_curve = mbbefd(b, g, subcvg_x_higher) - mbbefd(b, g, subcvg_x_lower)

        # Premiums
        year.cvg_premium    = year.sum_insured * (year.total_cvg_nl_roe    or 0) * year.cvg_expo_curve    * (1 + nmp_load)
        year.subcvg_premium = year.sum_insured * (year.total_subcvg_nl_roe or 0) * year.subcvg_expo_curve * (1 + nmp_load)
        year.total_premium  = year.cvg_premium + year.subcvg_premium

        business_plan_lr = look_up(inception_date.year, "YoA", "LR", BusPlanLossRatios, if_not_found=BusPlanLossRatios["LR"].iloc[-1], lookup_type="single")

        year.model_premium_pre_uw_adj   = ratio(year.total_premium * (1 - expo.agg_discount) * benchmark_lr,    business_plan_lr * (1 - brokerage))
        year.model_premium              = year.model_premium_pre_uw_adj * uw_multiplier
        year.benchmark_premium          = ratio(year.model_premium * business_plan_lr,      benchmark_lr)

        agg_usage_risk                  = look_up(expo.details.aggregate_usage, "Agg Usage", "UW Multiplier", AggUsage, lookup_type="single")
        year.model_premium_post_agg_adj = max(year.model_premium * agg_usage_risk, expo.policy_limit * cds.exposure.granular.wa_nl_min_rol)

    # Totals

    incept_date_plus1yr = (inception_date + relativedelta(years=1))
    annualisation_factor= ratio(   (incept_date_plus1yr - inception_date).days,    c.days_difference)
    #YZ Change 23/10/2025: The expiry date adjustment. if term:  01/07/2024 - 30/06/2025, it is still one year.
    if ((incept_date_plus1yr - inception_date).days - c.days_difference <= 1)  and ((incept_date_plus1yr - inception_date).days - c.days_difference >= 0):
        annualisation_factor = 1


    for node in constr_premium_nodes:
        total = sum([getattr(year, node) or 0 for year in c.years])
        setattr(c.years_total, node, total)
        setattr(c.years_annual, node,       (total * annualisation_factor)   )