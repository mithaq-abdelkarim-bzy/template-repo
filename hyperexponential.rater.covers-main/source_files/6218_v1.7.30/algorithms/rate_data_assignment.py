import hx
import polars as pl
from datetime import datetime
import algorithms.rate_constants as const
from algorithms.rate_common_rating_functions import join_param_table

def data_assignment(hxd, df):
    tp_components(hxd, df)
    exposure_rating_summary(hxd, df)
    rationale_tab(hxd, df)

    return 

    
def tp_components(hxd, df):
    cds = hxd.cds.layers[0]
    # this if statment is checking if the rater is run on its first time and thus has empty dfs
    if df.select(pl.col("loc_tiv_total").sum()).item() is not None:

        cds = hxd.cds.rating_summary.chart_premium_breakdown.tp_exposure_weights_pre_uw
        
        # We need to uplift the prem since we select prem based on max of the three methods but we are displaying the calcs based on tp calcs 1. 
        # Since the max of the three prem methods is higher than tp 1 calcs, we need to uplift the tp 1 calcs. We are allocating the uplift to all components excluding Expected Losses
        el = df.select(pl.col("loc_all_perils_beazley_share_aal_and_el").sum()).item()
        prem_uplift = (df.select(pl.col("loc_selected_beazley_share_gn_tp")).sum().item() - el) / (df.select(pl.col("loc_calc_1_beazley_share_gn_tp")).sum().item() - el)

        coc = df.with_columns(pl.sum_horizontal(f"loc_{peril}_cost_of_cap" for peril in ("fire", "fl", "tn", "ha", "wf", "wts", "ws", "eq")).alias("temp")).sum()["temp"].item()
        nmp = df.select(pl.col("loc_nmp_beazley_share_el").sum()).item()
        indirect_expense = df.with_columns(pl.sum_horizontal(f"loc_{peril}_indirect_expense" for peril in ("fire", "fl", "tn", "ha", "wf", "wts", "ws", "eq")).alias("temp")).sum()["temp"].item()
        ri = df.select(pl.col("loc_ws_ri_cost") + pl.col("loc_eq_ri_cost")).sum().item()
        lae = df.select(pl.col("loc_ws_lae") + pl.col("loc_eq_lae")).sum().item()
        direct_expenses_per_premium = pl.from_pandas(hx.params.table_tp_assumptions)["Direct Expenses Per Premium"].item()
        investment_income_load = pl.from_pandas(hx.params.table_tp_assumptions)["Investment Income Load"].item()

        # allocating Direct Expenses and Investment Income
        beazley_share_gn_tp = (el + nmp + coc + indirect_expense + ri + lae) / (1 - direct_expenses_per_premium + investment_income_load)        
        beazley_share_gn_tp_direct_expense_only = (el + nmp + coc + indirect_expense + ri + lae) / (1 - direct_expenses_per_premium)
        beazley_share_gn_tp_investment_income_only = (el + nmp + coc + indirect_expense + ri + lae) / (1 + investment_income_load)

        cds.brokerage = (((beazley_share_gn_tp / (1 - (hxd.cds.layers[0].total_deductions or 0))) - beazley_share_gn_tp) / el)

        direct_expenses = beazley_share_gn_tp_direct_expense_only - (el + nmp + coc + indirect_expense + ri + lae)
        investment_income = beazley_share_gn_tp_investment_income_only - (el + nmp + coc + indirect_expense + ri + lae)
        direct_expenses_less_investment_income = beazley_share_gn_tp - (el + nmp + coc + indirect_expense + ri + lae)

        interaction_effect =  (direct_expenses + investment_income) - direct_expenses_less_investment_income

        direct_expenses_adjusted = direct_expenses - interaction_effect * ( direct_expenses_per_premium / (direct_expenses_per_premium + investment_income_load))
        investment_income_adjusted = investment_income - interaction_effect * ( investment_income_load / (direct_expenses_per_premium + investment_income_load))

        cds.direct_expense = (direct_expenses_adjusted /el) * prem_uplift
        cds.investment_income = (investment_income_adjusted / el) * prem_uplift
        cds.coc = (coc / el) * prem_uplift
        cds.indirect_expense = (indirect_expense / el) * prem_uplift
        cds.lae = (lae / el) * prem_uplift
        cds.ri_cost = (ri / el) * prem_uplift
        cds.nmp_load = (nmp / el) * prem_uplift
       
    return

        

def exposure_rating_summary(hxd, df):

    cds = hxd.cds
    

    benchmark_parameters_df  = hx.params.table_benchmarkclassparameters

    ## GROSS NET - benchmark ULR for CAT - NON MODELLED LOSSES (NML)
    benchmark_row_df     = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "NML") 
                                                     & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
    gnlr_cat_non_modelled= 0  if benchmark_row_df.empty   else benchmark_row_df['Value'].iat[0]             #gross net LR
    gnlr_cat_non_modelled = 0 #TS - overriding based on JM guidance Dec 25, no NMP uplift

    ## GROSS NET - benchmark ***LOAD*** for CAT - Climate Change
    benchmark_row_df     = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "Climate Load") 
                                                     & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
    load_cat_climate     = 0  if benchmark_row_df.empty   else benchmark_row_df['Value'].iat[0]             #this is a load not a loss ratio


    if df.select(pl.col("loc_tiv_total").sum()).item() is not None:
        
        cds = hxd.cds.exposure_adj

        risk_info = hxd.cds.layers[0]
        
        hxd.cds.exposure_rating.pre_uw_adj.beazley_share_gn_tp = df.select(pl.col("loc_selected_beazley_share_gn_tp").fill_nan(0).sum()).item()
        
        gg_received_beazley_share_exposure_prem = df.select(pl.col("loc_beazley_share_received_gg_prem").fill_nan(0).sum()).item()   # this should actually be filtered for all attritional perils 

        att_expected_loss = df.with_columns(pl.sum_horizontal(f"loc_{peril}_beazley_share_el" for peril in ("fire", "fl", "tn", "ha", "wf", "wts")).alias("temp")).sum()["temp"].item()
        cat_expected_loss = df.with_columns(pl.sum_horizontal("loc_ws_beazley_share_aal", "loc_eq_beazley_share_aal"))["sum"].sum()                                         
        

        #att_GLR =  att_expected_loss / gg_received_beazley_share_exposure_prem
        #cat_GLR =  cat_expected_loss / gg_received_beazley_share_exposure_prem 

        

        # commented line shows previous calc: was working off risk info premium when should be working off location level sov premium
        
        cds.att_and_large.pre_uw_adj_gn_ulr = (att_expected_loss / (gg_received_beazley_share_exposure_prem  * (1 - risk_info.total_deductions))) if risk_info.quoted_premium_100pct not in [0, None] else 0
        
        pre_uw_adj_gn_ulr_no_NMP = (cat_expected_loss / (gg_received_beazley_share_exposure_prem   * (1 - risk_info.total_deductions)))  if risk_info.quoted_premium_100pct not in [0, None] else 0    # adding in the NMP load onto just the cat


        cds.cat.pre_uw_adj_gn_ulr = ((cat_expected_loss*(1+load_cat_climate)  / (gg_received_beazley_share_exposure_prem  * (1 - risk_info.total_deductions))) + gnlr_cat_non_modelled) if risk_info.quoted_premium_100pct not in [0, None] else 0    # adding in the NMP load onto just the cat and the climate load 


        

        
    return

def rationale_tab(hxd, df):
    # construction type #######################
    agg_df = df.group_by("iso_constr").agg(pl.col("loc_tiv_total").sum()).sort("loc_tiv_total", descending = True)
    agg_df = join_param_table(agg_df, hx.params.table_iso_construction_modifier, "Construction", "Construction", "ISO", "iso_constr")
    tot_tiv = agg_df["loc_tiv_total"].sum()
    # calc proportion of TIV in each construction type
    agg_df = agg_df.with_columns(
        (pl.col("loc_tiv_total") / pl.lit(tot_tiv)).alias("proportion")
    )
    # create string for any construction type over 25%
    trim_agg_df = agg_df.filter(pl.col("proportion") >= 0.25)

    # concat columns together to make strings for each row
    trim_agg_df = trim_agg_df.with_columns(
        pl.concat_str(
            [
                pl.col("Construction"),
                pl.lit(" "),
                pl.col("proportion").round(2) * 100,
                pl.lit("%"),
            ],
            separator="",
        ).alias("string"),
    )
    #combine all the rows into a single string
    final_constr_str = trim_agg_df.select(pl.col("string").str.concat(", ")).item()
    # assign to the rationale node
    hxd.cds.rationale.construction.calculated = final_constr_str

    # average limit #######################
    df = df.with_columns(
        (pl.col("loc_aop_limit") * pl.col("loc_tiv_total") / pl.lit(tot_tiv)).alias("weighted_limit")
    )
    # assign to the rationale node
    hxd.cds.rationale.avg_limit = df["weighted_limit"].sum()

    # top counties #######################
    agg_df = df.group_by("county").agg(pl.col("loc_tiv_total").sum()).sort("loc_tiv_total", descending = True)
    # calc proportion of TIV in each county
    agg_df = agg_df.with_columns(
        (pl.col("loc_tiv_total") / pl.lit(tot_tiv)).alias("proportion")
    )
    # create string for (up to) top 3 counties
    trim_agg_df = agg_df.top_k(3, by="proportion")
    # concat columns together to make strings for each row
    trim_agg_df = trim_agg_df.with_columns(
        pl.concat_str(
            [
                pl.col("county"),
                pl.lit(" "),
                pl.col("proportion").round(2) * 100,
                pl.lit("%"),
            ],
            separator="",
        ).alias("string"),
    )
    #combine all the rows into a single string
    final_county_str = trim_agg_df.select(pl.col("string").str.concat(", ")).item()
    # assign to the rationale node
    hxd.cds.rationale.top_counties.calculated = final_county_str

    # average rate #########################
    #rate of premium cents per $100 of TIV
    avg_rate = hxd.cds.layers[0].quoted_premium_100pct / (tot_tiv / 100)
    # assign to the rationale node
    hxd.cds.rationale.avg_rate.calculated = avg_rate

    return