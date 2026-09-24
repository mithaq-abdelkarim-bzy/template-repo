import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
import algorithms.rate_utilities as utils
from operator import itemgetter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from functools import reduce
# Import helper functions:
from algorithms.rate_helpers import eec_ilf_calcs, agg_ilf_calcs, idf_calcs, benchmark_prem_calcs, technical_prem_calcs, nonstandard_idf_calcs

# Functions for rate_rating_summary.py

def pricing_standard_rater_calcs(hxd, tp_params, fx_rate, pro_rata_factor):
    '''
    Pricing primary layer for standard coverages, i.e. Media Liabilty, Music Liability, Annual TV & Film LARGE
    '''
    cds = hxd.cds
    ccy = cds.currencies.source_currency

    # Set up tp params ---------------
    che = tp_params['che'].iloc[0]
    var_exp = tp_params['var_exp'].iloc[0]
    inv_inc = tp_params['inv_inc'].iloc[0]
    cost_of_ri = tp_params['cost_of_ri'].iloc[0]
    ri_rec = tp_params['ri_rec'].iloc[0]
    roc = tp_params['roc'].iloc[0]
    fixed_exp_usd = tp_params['fixed_exp'].iloc[0]
    capital_req = tp_params['capital_req'].iloc[0]
    nmp_load = tp_params['nmp_load'].iloc[0]

    # Convert fixed expenses to model currency
    fixed_exp = fixed_exp_usd * fx_rate

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    # Options pricing --------------------------
    # Read in limits, retentions and quoted premium from UI
    options_df = utils.pd_df_from_hx_list(cds.options)
    options_df = options_df.drop(["option_label", "eec_excess", "aggregate_excess"], axis=1) # Remove unnecessary columns
    options_df = options_df.fillna(0)

    # ILF Calculation -----
    # EEC ILF calcs
    options_df = options_df.apply(lambda row: eec_ilf_calcs(hxd, row, fx_rate), axis=1)
    # Agg ILF calcs
    options_df = options_df.apply(lambda row: agg_ilf_calcs(hxd, row), axis=1)
    # ILF Factor
    options_df["ilf"] = options_df["eec_ilf"] * options_df["agg_ilf"]

    # IDF Calculation (Deductible Factor) -----
    # Work in separate df for intermediate calcs
    df = options_df.copy(deep=True) 
    df = df.apply(lambda row: idf_calcs(hxd, row), axis=1)
    
    # Add IDF column to options_df table
    options_df["idf"] = df["idf"]

    # Premium Calculations (in source currency) -----
    total_base_premium = cds.exposure.aggregate.total_base_premium or 0

    # Apply optional coverages: sum together factors and apply to base premium
    total_op_cover_factor = sum(
        getattr(getattr(cds.modifiers.optional_coverages, cover), "output", 0) or 0
        for cover in dir(cds.modifiers.optional_coverages)
    )
    options_df["premium_post_op_covers"] = total_base_premium * (1 + total_op_cover_factor)

    # Factors
    longevity_factor = cds.modifiers.longevity_factor
    experience_factor = cds.modifiers.experience_factor.output 
    territory_factor = cds.rating_factors.territory_factor
    schedule_rating_factor = cds.modifiers.total_schedule_mod # UW adjustments

    # Brokerage
    options_df["brokerage"] = cds.primary.brokerage or 0

    # Calculations: Pre UW adjustments
    # Base premium post deductible factor pre UW adj
    options_df_preUWadj = options_df.copy(deep=True) 
    options_df_preUWadj["factor"] = options_df_preUWadj["idf"] * longevity_factor * experience_factor * territory_factor
    # Benchmark premium calcs
    options_df_preUWadj = benchmark_prem_calcs(hxd, options_df_preUWadj, pro_rata_factor, nmp_load)
    # Technical premium calcs
    options_df_preUWadj = technical_prem_calcs(hxd, options_df_preUWadj, tp_params, fx_rate)

    # Calculations: Post UW adjustments
    # Base premium post deductible factor post UW adj
    options_df_postUWadj = options_df.copy(deep=True) 
    options_df_postUWadj["factor"] = options_df_postUWadj["idf"] * longevity_factor * experience_factor * territory_factor * schedule_rating_factor
    # Benchmark premium calcs
    options_df_postUWadj = benchmark_prem_calcs(hxd, options_df_postUWadj, pro_rata_factor, nmp_load)
    # Technical premium calcs
    options_df_postUWadj = technical_prem_calcs(hxd, options_df_postUWadj, tp_params, fx_rate)

    # Final calcs for options
    options_df["expected_loss_cost"] = options_df_postUWadj["expected_loss_cost"]
    options_df["expected_loss_cost_pre_uw_adj"] = options_df_preUWadj["expected_loss_cost"]
    options_df["model_premium"] = options_df_postUWadj["gross_technical_premium"]
    options_df["model_premium_pre_uw_adj"] = options_df_preUWadj["gross_technical_premium"]
    options_df["benchmark_premium"] = options_df_postUWadj["gross_benchmark_premium"]
    options_df["benchmark_premium_pre_uw_adj"] = options_df_preUWadj["gross_benchmark_premium"]
    options_df["technical_premium"] = np.where(options_df["benchmark_premium"] > 0, options_df["model_premium"], 0)
    options_df["technical_premium_pre_uw_adj"] = np.where(options_df["benchmark_premium_pre_uw_adj"] > 0, options_df["model_premium_pre_uw_adj"], 0)
    # Quoted BPI
    options_df["quoted_bpi"] = np.where(options_df["benchmark_premium"] > 0, options_df["quoted_premium"] / options_df["benchmark_premium"], 0)

    # Assign to nodes -----
    for i, option in enumerate(cds.options):
        option.technical_premium = options_df["technical_premium"].iloc[i]
        option.benchmark_premium = options_df["benchmark_premium"].iloc[i]
        option.quoted_bpi = options_df["quoted_bpi"].iloc[i]
        

    # Primary layer for selected option
    option_selected = cds.option_selected
    option_selected = int("".join([c for c in option_selected if c.isdigit()])) # Pull out integer
    bound_option = options_df.iloc[option_selected - 1]

    cds.primary.status_view = cds.primary.status
    cds.primary.section_reference_view = cds.primary.section_reference
    cds.primary.bound_premium = cds.primary.bound_premium_input

    cds.primary.quoted_premium_view = bound_option["quoted_premium"]
    cds.primary.benchmark_premium = bound_option["benchmark_premium"]
    cds.primary.technical_premium = bound_option["technical_premium"]

    if cds.primary.bound_premium is not None:
        cds.primary.bpi = cds.primary.bound_premium / cds.primary.benchmark_premium if cds.primary.benchmark_premium else None
        cds.primary.tpi = cds.primary.bound_premium / cds.primary.technical_premium if cds.primary.technical_premium else None
    else:
        cds.primary.bpi = cds.primary.quoted_premium_view / cds.primary.benchmark_premium if (cds.primary.quoted_premium_view is not None) and (cds.primary.benchmark_premium) else None
        cds.primary.tpi = cds.primary.quoted_premium_view / cds.primary.technical_premium if (cds.primary.quoted_premium_view is not None) and (cds.primary.technical_premium) else None
    
    cds.primary.aggregate_limit_view = bound_option["aggregate_limit"]
    cds.primary.attachment = bound_option["retention"]
    cds.primary.expected_loss_cost = bound_option["expected_loss_cost"]
    cds.primary.expected_loss_cost_pre_uw_adj = bound_option["expected_loss_cost_pre_uw_adj"]

    # Pre UW Adj calcs
    benchmark_premium_pre_uw_adj = bound_option["benchmark_premium_pre_uw_adj"]
    technical_premium_pre_uw_adj = bound_option["technical_premium_pre_uw_adj"]
    bound_premium = cds.primary.bound_premium or 0

    if cds.primary.bound_premium is not None:
        cds.primary.bpi_pre_uw_adj = bound_premium / benchmark_premium_pre_uw_adj if benchmark_premium_pre_uw_adj else None
        cds.primary.tpi_pre_uw_adj = bound_premium / technical_premium_pre_uw_adj if technical_premium_pre_uw_adj else None
    else:
        cds.primary.bpi_pre_uw_adj = cds.primary.quoted_premium_view / benchmark_premium_pre_uw_adj if (benchmark_premium_pre_uw_adj and cds.primary.quoted_premium_view) else None
        cds.primary.tpi_pre_uw_adj = cds.primary.quoted_premium_view / technical_premium_pre_uw_adj if (technical_premium_pre_uw_adj and cds.primary.quoted_premium_view) else None

    # Validation checks -----
    # EEC limit must be entered for option selected, and it must be >= 2000 USD
    min_limit_usd = 2000
    max_limit_usd = 200_000_000
    min_limit = round(min_limit_usd * fx_rate) # Minimum limit in source currency
    max_limit = round(max_limit_usd * fx_rate) # Maximum limit in source currency

   
    if (bound_option["eec_limit"] or 0) < min_limit:
        hx.errors.validation(f"EEC Limit of at least {min_limit:,.0f} {ccy} must be entered for option selected. [Rating Summary]")

    # Aggregate limit must be greater than or equal to the EEC limit
    if bound_option["aggregate_limit"] < bound_option["eec_limit"]:
        hx.errors.validation("Aggregate Limit must be at least the size of the EEC Limit, for the option selected. [Rating Summary]")

    # Aggregate limit cannot be > 5 * EEC limit
    if bound_option["aggregate_limit"] > 5 * bound_option["eec_limit"]:
        hx.errors.validation("Aggregate Limit cannot exceed 5 times the EEC Limit. [Rating Summary]")

    # Both EEC limit and aggregate limit must be max $15m
    if bound_option["eec_limit"] / fx_rate > max_limit_usd: # Convert to USD
        hx.errors.validation(f"EEC Limit cannot exceed {max_limit:,.0f} {ccy}. [Rating Summary]")
    if bound_option["aggregate_limit"] / fx_rate > max_limit_usd: # Convert to USD
        hx.errors.validation(f"Aggregate Limit cannot exceed {max_limit:,.0f} {ccy}. [Rating Summary]")

    # Retention must be entered for option selected
    if not bound_option["retention"] > 0:
        hx.errors.validation("Retention must be entered for option selected. [Rating Summary]")
    


def pricing_nonstandard_rater_calcs(hxd, tp_params, fx_rate):
    '''
    Pricing primary layer for non-standard coverages, i.e. Individual TV, Individual Film, Annual TV & Film SMALL
    '''
    cds = hxd.cds
    ccy = cds.currencies.source_currency

    # Set up tp params ---------------
    che = tp_params['che'].iloc[0]
    var_exp = tp_params['var_exp'].iloc[0]
    inv_inc = tp_params['inv_inc'].iloc[0]
    cost_of_ri = tp_params['cost_of_ri'].iloc[0]
    ri_rec = tp_params['ri_rec'].iloc[0]
    roc = tp_params['roc'].iloc[0]
    fixed_exp_usd = tp_params['fixed_exp'].iloc[0]
    capital_req = tp_params['capital_req'].iloc[0]
    nmp_load = tp_params['nmp_load'].iloc[0]

    # Convert fixed expenses to model currency
    fixed_exp = fixed_exp_usd * fx_rate

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    # Primary Layer calcs ----------------------------
    brokerage = cds.primary.brokerage or 0
    cds.primary.bound_premium = cds.primary.bound_premium_input
    cds.primary.status_view = cds.primary.status
    cds.primary.section_reference_view = cds.primary.section_reference

    # Options: read in limits, excesses and quoted premium from UI
    options_df = utils.pd_df_from_hx_list(cds.options)
    options_df = options_df.drop(["option_label", "retention"], axis=1) # Remove unnecessary columns
    options_df = options_df.fillna(0)

    # ILF Calculation -----
    # EEC ILF calcs
    options_df = options_df.apply(lambda row: eec_ilf_calcs(hxd, row, fx_rate), axis=1)
    # Agg ILF calcs
    options_df = options_df.apply(lambda row: agg_ilf_calcs(hxd, row), axis=1)
    # ILF Factor
    options_df["ilf"] = options_df["eec_ilf"] * options_df["agg_ilf"]

    # IDF Calculation -----
    options_df = options_df.apply(lambda row: nonstandard_idf_calcs(hxd, row, fx_rate), axis=1)
    cds.nonstandard_idf = options_df["idf"].iloc[0] # Save primary layer IDF as a constant for use in excess pricing later
    
    # Territory factor -----
    territory_factor = cds.rating_factors.territory_factor

    # Minimum premium calculations -----
    if cds.individualtv_masking:
        # Read in selections and modifiers
        selections = cds.individual_tv.selections
        modifiers = cds.individual_tv.modifiers
        # Parameter table
        minimum_params = hx.params.tbl_indtv_minimum
        # Minimum for genre and jurisdiction selected
        jurisdiction = getattr(selections, "jurisdiction").lower().replace(" ", "_")
        genre = getattr(selections, "genre")
        minimum = minimum_params[minimum_params["type"] == genre][jurisdiction].iloc[0] if genre is not None else 0
        # Minimum's modifiers product
        exclude_keys = {"jurisdiction", "coverage_basis", "established_format", "lawyers", "genre", "number_of_episodes"} # exclude these modifiers
        product_min = reduce(
            lambda x, y: x * y,
            [(value if value is not None else 1) for key, value in modifiers if key not in exclude_keys]
        )

    if cds.annualtv_masking:
        # Read in selections and modifiers
        selections = cds.annual_tv.selections
        modifiers = cds.annual_tv.modifiers
        # Parameter table
        minimum_params = hx.params.tbl_annualtv_minimum
        # Minimum for jurisdiction selected
        jurisdiction = getattr(selections, "jurisdiction")
        minimum = minimum_params[minimum_params["type"] == jurisdiction]["minimum"].iloc[0] 
        # Minimum's modifiers product
        product_min = modifiers.australian


    if cds.individualfilm_masking:
        # Read in selections and modifiers
        selections = cds.individual_film.selections
        modifiers = cds.individual_film.modifiers
        # Parameter table
        minimum_params = hx.params.tbl_film_jurisdiction_minimum
        # Minimum for scope of release and jurisdiction selected
        jurisdiction = getattr(selections, "jurisdiction", None)
        jurisdiction = jurisdiction.lower().replace(" ", "_") if jurisdiction else "ww" # IR: default is "WW". Manual catch here due to code tripping when changing from IndTV to IndFilm in some situations.
        scope = getattr(cds.exposure.aggregate.individual_film, "exhibition")
        minimum = minimum_params[minimum_params["type"] == scope][jurisdiction].iloc[0] if scope is not None else 0
        # Minimum's modifiers product
        exclude_keys = {"budget", "cast", "appeal", "subject_matter", "coverage_basis", "established_format", "lawyers", "exhibition"} # exclude these modifiers
        product_min = reduce(
            lambda x, y: x * y,
            [(value if value is not None else 1) for key, value in modifiers if key not in exclude_keys]
        )
        
    # Apply modifiers to get minimum premium
    options_df["minimum_premium"] = minimum * product_min * options_df["ilf"]
    
    # Premium calculations -----
    # Product of all modifiers
    product_all = reduce(
        lambda x, y: x * y,
        [(value if value is not None else 1) for key, value in modifiers]
    )
    product_all = product_all * territory_factor # Apply country factor
    
    # Apply ILF and IDF to get model premium before minimum
    total_base_premium = cds.exposure.aggregate.total_base_premium or 0
    if cds.individualtv_masking:
        options_df["model_premium_pre_min"] = product_all * options_df["ilf"] * options_df["idf"] # Note: "genre" modifier (included in product_all) is the base premium
    if cds.annualtv_masking:
        annual_policy_modifier = 0.75
        aggregate_limit_modifier = 0.65
        options_df["model_premium_pre_min"] = total_base_premium * product_all * options_df["ilf"] * options_df["idf"] * annual_policy_modifier * aggregate_limit_modifier
    if cds.individualfilm_masking:
        options_df["model_premium_pre_min"] = product_all * options_df["ilf"] * options_df["idf"] # Note: "exhibition" modifier (included in product_all) is the base premium

    # Apply minimum premium and commission adjustment factor to get gross model premium
    commission_adj_factor = max((1-0.25)/(1-brokerage), 1) if brokerage is not None else 1
    options_df["gross_model_premium"] = np.where(options_df["model_premium_pre_min"].notna(), 
        commission_adj_factor * np.maximum(options_df["model_premium_pre_min"], options_df["minimum_premium"]),
        0)
    # Net model premium
    options_df["model_premium"] = options_df["gross_model_premium"] * (1 - brokerage)

    # Benchmark Premium calculations
    if cds.annualtv_masking:
        options_df["final_term_premium"] = np.where(options_df["model_premium_pre_min"].notna(),
            (options_df["model_premium_pre_min"] / (annual_policy_modifier * aggregate_limit_modifier)) * commission_adj_factor,
            0)
    else:
        options_df["final_term_premium"] = np.where(options_df["model_premium_pre_min"].notna(),
            options_df["model_premium_pre_min"] * commission_adj_factor,
            0)
    options_df["final_net_premium"] = options_df["final_term_premium"] * (1 - brokerage)
    options_df["net_benchmark_premium"] = options_df["final_net_premium"] * (const.priced_to_lr / const.benchmark_lr)
    options_df["gross_benchmark_premium"] = options_df["net_benchmark_premium"] / (1 - brokerage)
    options_df["benchmark_premium"] = np.where(options_df["model_premium_pre_min"].notna(), options_df["gross_benchmark_premium"], 0)

    # Expected Loss calculations
    options_df["expected_loss_cost"] = options_df["net_benchmark_premium"] * const.benchmark_lr
    options_df["expected_loss_cost_pre_uw_adj"] = options_df["expected_loss_cost"] #IR: There are no UW adjustments for the non-standard raters.

    # Technical Premium calculations
    options_df["net_technical_premium"] = np.where(options_df["expected_loss_cost"] > 0,
        (options_df["expected_loss_cost"] * (1+che) + fixed_exp) / technical_lr,
        0)
    options_df["technical_premium"] = np.where(options_df["model_premium_pre_min"].notna(), options_df["net_technical_premium"] / (1 - brokerage), 0)

    # Quoted BPI
    options_df["quoted_bpi"] = np.where(options_df["benchmark_premium"] > 0, options_df["quoted_premium"] / options_df["benchmark_premium"], 0)

    # Assign to nodes ---
    for i, option in enumerate(cds.options):
        option.technical_premium = options_df["technical_premium"].iloc[i]
        option.benchmark_premium = options_df["benchmark_premium"].iloc[i]
        option.quoted_bpi = options_df["quoted_bpi"].iloc[i]

    # Primary layer for selected option
    option_selected = cds.option_selected
    option_selected = int("".join([c for c in option_selected if c.isdigit()])) # Pull out integer
    bound_option = options_df.iloc[option_selected - 1]
    
    cds.exposure.aggregate.minimum_premium = bound_option["minimum_premium"]
    cds.primary.quoted_premium_view = bound_option["quoted_premium"]

    cds.primary.expected_loss_cost = bound_option["expected_loss_cost"]
    cds.primary.expected_loss_cost_pre_uw_adj = bound_option["expected_loss_cost_pre_uw_adj"]
    cds.primary.model_premium = bound_option["model_premium"]
    cds.primary.benchmark_premium = bound_option["benchmark_premium"]
    cds.primary.benchmark_premium_net = bound_option["net_benchmark_premium"]
    cds.primary.technical_premium = bound_option["technical_premium"]
    cds.primary.technical_premium_net = bound_option["net_technical_premium"]
    if cds.primary.bound_premium is not None:
        cds.primary.bpi = cds.primary.bound_premium / cds.primary.benchmark_premium if cds.primary.benchmark_premium else None
        cds.primary.tpi = cds.primary.bound_premium / cds.primary.technical_premium if cds.primary.technical_premium else None
    else:
        cds.primary.bpi = cds.primary.quoted_premium_view / cds.primary.benchmark_premium if (cds.primary.quoted_premium_view is not None) and (cds.primary.benchmark_premium) else None
        cds.primary.tpi = cds.primary.quoted_premium_view / cds.primary.technical_premium if (cds.primary.quoted_premium_view is not None) and (cds.primary.technical_premium) else None
    cds.primary.aggregate_limit_view = bound_option["aggregate_limit"]
    # Necessary for excess pricing:
    cds.primary.attachment = bound_option["aggregate_excess"] # i.e. primary attachment = primary layer aggregate excess 


    # Validation checks -----

    # 2,000 USD <= EEC limit <= 15mil USD must be entered
    min_limit_usd = 2000
    max_limit_usd = 15_000_000
    min_limit = round(min_limit_usd * fx_rate) # Minimum limit in source currency
    max_limit = round(max_limit_usd * fx_rate) # Maximum limit in source currency
    eec_limit = bound_option["eec_limit"] or 0

    if eec_limit < min_limit:
        hx.errors.validation(f"EEC Limit of at least {min_limit:,.0f} {ccy} must be entered for option selected. [Rating Summary]")
    if eec_limit > max_limit:
        hx.errors.validation(f"EEC Limit cannot exceed {max_limit:,.0f} {ccy}. [Rating Summary]")

    # Aggregate limit <= 15 mil USD must be entered, and must be be >= EEC limit. 
    if bound_option["aggregate_limit"] < bound_option["eec_limit"]:
        hx.errors.validation("Aggregate Limit must be at least the size of the EEC Limit, for the option selected. [Rating Summary]")
    primary_eec_limit_usd = round((bound_option["aggregate_limit"] or 0) / fx_rate, 2)
    if round(bound_option["aggregate_limit"] / fx_rate, 2) > round(max_limit_usd, 2):
        hx.errors.validation(f"Aggregate Limit cannot exceed {max_limit:,.0f} {ccy}. [Rating Summary]")

    # Aggregate limit cannot be > 5 * EEC limit
    if bound_option["aggregate_limit"] > 5 * bound_option["eec_limit"]:
        hx.errors.validation("Aggregate Limit cannot exceed 5 times the EEC Limit. [Rating Summary]")

    # EEC excess >= 100,000 USD must be entered
    min_excess_usd = 2000
    min_excess = round(min_excess_usd * fx_rate)

    eec_excess = bound_option["eec_excess"] or 0

    if eec_excess < min_excess:
        hx.errors.validation(f"EEC Excess of at least {min_excess:,.0f} {ccy} must be entered for option selected. [Rating Summary]")
    
    # # Aggregate excess >= EEC excess must be entered
    # primary_agg_excess_usd = (bound_option["aggregate_excess"] or 0) / fx_rate
    # if primary_agg_excess_usd < primary_eec_excess_usd:
    #         hx.errors.validation("Aggregate Excess must be at least the size of the EEC Excess, for the option selected. [Rating Summary]")



def pricing_excess_calcs(hxd, tp_params, fx_rate, pro_rata_factor):
    '''
    Pricing excess layers for all coverages
    '''
    cds = hxd.cds
    layers = cds.layers

    # Set up tp params ---------------
    che = tp_params['che'].iloc[0]
    var_exp = tp_params['var_exp'].iloc[0]
    inv_inc = tp_params['inv_inc'].iloc[0]
    cost_of_ri = tp_params['cost_of_ri'].iloc[0]
    ri_rec = tp_params['ri_rec'].iloc[0]
    roc = tp_params['roc'].iloc[0]
    fixed_exp_usd = tp_params['fixed_exp'].iloc[0]
    capital_req = tp_params['capital_req'].iloc[0]
    nmp_load = tp_params['nmp_load'].iloc[0]

    # Convert fixed expenses to model currency
    fixed_exp = fixed_exp_usd * fx_rate

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    # Price excess layers -------------
    # Take aggregate limit inputs and assign to output node
    for index, layer in enumerate(layers):
        if (index==0):
            layer.aggregate_limit = cds.primary.aggregate_limit_view
        else:
            layer.aggregate_limit = layer.aggregate_limit_view

    for index, layer in enumerate(layers):
        # Attachment
        if (index==0):
            layer.attachment = cds.primary.attachment
        elif (index==1):
            layer.attachment = cds.primary.aggregate_limit_view if layer.aggregate_limit is not None else None
        else:
            layer.attachment = float(layers[index - 1].aggregate_limit) + float(layers[index - 1].attachment) if (layer.aggregate_limit is not None) and (layers[index - 1].aggregate_limit is not None) and (layers[index - 1].attachment is not None) else None

    layers_df = utils.pd_df_from_hx_list(cds.layers)
    # Filter for necessary columns
    layers_cols = ["aggregate_limit", "attachment", "brokerage_input", "quoted_premium_view", "bound_premium"]
    layers_df = layers_df[layers_cols].fillna(0)
    
    layers_df["quoted_premium"] = layers_df["quoted_premium_view"]
    layers_df["brokerage"] = layers_df["brokerage_input"]
    # Primary layer: carry over from cds.primary node
    layers_df.loc[0,"quoted_premium"] = cds.primary.quoted_premium_view or 0
    layers_df.loc[0,"bound_premium"] = cds.primary.bound_premium or 0
    layers_df.loc[0,"aggregate_limit"] = cds.primary.aggregate_limit_view or 0

    # Deductible Factor (IDF) Calculations -----
    # Note: Guideline deductible is the same as in primary layer pricing.
    layers_df["retention"] = layers_df["attachment"].iloc[0] # For every layer, the deductible is the retention, i.e. the attachment point for the primary layer.
    layers_df = layers_df.apply(lambda row: idf_calcs(hxd, row), axis=1)

    # For non-standard coverages, excess layers use same IDF as primary layer.
    if cds.nonstandard_rater_masking:
        layers_df["idf"] = cds.nonstandard_idf

    # ILF Calculations -----              
    # EEC ILF calcs
    # Lower EEC ILF: using the attachment point
    ## DJ Edits:
    layers_df["eec_limit"] = layers_df["attachment"] + (cds.primary.attachment or 0)
    ##

    layers_df = layers_df.apply(lambda row: eec_ilf_calcs(hxd, row, fx_rate), axis=1)
    layers_df["eec_ilf_lower"] = layers_df["eec_ilf"].copy()

    ## DJ Edits:
    #layers_df.loc[0,"eec_ilf_lower"] = 0 # set to zero for primary layer
    ##

    # Upper EEC ILF: using limit + attachment point
    ## DJ Edits:
    layers_df["eec_limit"] = layers_df["attachment"] + (cds.primary.attachment or 0) + layers_df["aggregate_limit"]
    ##

    ## DJ Edits:
    layers_df.loc[0,"eec_limit"] = layers_df.loc[0,"aggregate_limit"]
    ##
    
    layers_df = layers_df.apply(lambda row: eec_ilf_calcs(hxd, row, fx_rate), axis=1)
    layers_df["eec_ilf_upper"] = layers_df["eec_ilf"].copy()
    # EEC ILF is the difference
    layers_df["eec_ilf"] = layers_df["eec_ilf_upper"] - layers_df["eec_ilf_lower"]
    layers_df.loc[0,"eec_ilf"] = layers_df.loc[0, "eec_ilf_upper"]

    # Agg ILF calcs
    layers_df["eec_limit"] = layers_df["aggregate_limit"]
    layers_df = layers_df.apply(lambda row: agg_ilf_calcs(hxd, row), axis=1)

    # ILF Factor
    layers_df["ilf"] =  layers_df["eec_ilf"] * layers_df["agg_ilf"]

    # Drop unnecessary columns
    layers_df = layers_df.drop(columns = ["retention", "eec_limit", "eec_ilf_lower", "eec_ilf_upper", "eec_ilf", "agg_ilf"])

    # Expected Loss Calculations -----
    minimum_premium = cds.exposure.aggregate.minimum_premium or 0
    base_premium = cds.exposure.aggregate.total_base_premium or 0

    # Base Premium calcs for standard raters
    if cds.standard_rater_masking:
        # Apply optional coverages: sum together factors and apply to base premium
        total_op_cover_factor = sum(
            getattr(getattr(cds.modifiers.optional_coverages, cover), "output", 0) or 0
            for cover in dir(cds.modifiers.optional_coverages)
        )
        base_premium0 = base_premium * (1 + total_op_cover_factor)

        # Apply Factors
        longevity_factor = cds.modifiers.longevity_factor
        experience_factor = cds.modifiers.experience_factor.output 
        territory_factor = cds.rating_factors.territory_factor
        schedule_rating_factor = cds.modifiers.total_schedule_mod # UW adjustments
        base_premium = base_premium0 * longevity_factor * experience_factor * territory_factor * schedule_rating_factor
        base_premium_pre_uw_adj = base_premium0 * longevity_factor * experience_factor * territory_factor

    else: # i.e. cds.nonstandard_rater_masking
        territory_factor = cds.rating_factors.territory_factor
        base_premium = base_premium * territory_factor
        base_premium_pre_uw_adj = base_premium #IR: There are no UW adjustments for the non-standard raters.
    
    # Expected Loss
    layers_df.loc[0,"term_premium"] = max(base_premium, minimum_premium) * layers_df.loc[0,"idf"] * layers_df.loc[0,"ilf"] * pro_rata_factor

    ## DJ Edits:
    layers_df.loc[1:,"term_premium"] = max(base_premium, minimum_premium) * layers_df.loc[1:,"ilf"] * pro_rata_factor 
    ##

    layers_df["net_premium"] = layers_df["term_premium"] * (1 - layers_df["brokerage"])
    layers_df["expected_loss_cost"] = layers_df["net_premium"] * const.benchmark_lr

    layers_df.loc[0,"expected_loss_cost_pre_uw_adj"] = (max(base_premium_pre_uw_adj, minimum_premium) * layers_df.loc[0,"idf"] * layers_df.loc[0,"ilf"] * pro_rata_factor) * (1 - layers_df.loc[0,"brokerage"]) * const.benchmark_lr
    layers_df.loc[1:,"expected_loss_cost_pre_uw_adj"] = (max(base_premium_pre_uw_adj, minimum_premium) * layers_df.loc[1:,"ilf"] * pro_rata_factor) * (1 - layers_df.loc[1:,"brokerage"]) * const.benchmark_lr

    # Apply NMP load
    layers_df["expected_loss"] = layers_df["expected_loss_cost"] * (1 + nmp_load)
    layers_df["expected_loss_pre_uw_adj"] = layers_df["expected_loss_cost_pre_uw_adj"] * (1 + nmp_load)

    # Benchmark Premium
    layers_df["net_benchmark_premium"] =  layers_df["expected_loss"] / const.benchmark_lr
    layers_df["gross_benchmark_premium"] = layers_df["net_benchmark_premium"] / (1 - layers_df["brokerage"])
    layers_df["benchmark_premium_pre_uw_adj"] = (layers_df["expected_loss_pre_uw_adj"] / const.benchmark_lr) / (1 - layers_df["brokerage"])

    # Technical Premium
    layers_df["net_technical_premium"] = (layers_df["expected_loss"] * (1+che) + fixed_exp) / technical_lr
    layers_df["gross_technical_premium"] = layers_df["net_technical_premium"] / (1 - layers_df["brokerage"])
    layers_df["technical_premium_pre_uw_adj"] = ((layers_df["expected_loss_pre_uw_adj"] * (1+che) + fixed_exp) / technical_lr) / (1 - layers_df["brokerage"])

    # BPI, TPI
    # Use bound premium if entered, otherwise use quoted premium. If neither entered, set to None.
    layers_df["bound_premium"] = np.where(layers_df["bound_premium"] > 0, layers_df["bound_premium"], layers_df["quoted_premium"]) # Note, this is just for calcs; quoted premium figures will not be saved down as bound premium.

    layers_df["bpi"] = np.where((layers_df["gross_benchmark_premium"] > 0) & (layers_df["bound_premium"].notna()), layers_df["bound_premium"] / layers_df["gross_benchmark_premium"], None)
    layers_df["tpi"] = np.where((layers_df["gross_technical_premium"] > 0) & (layers_df["bound_premium"].notna()), layers_df["bound_premium"] / layers_df["gross_technical_premium"], None)
    # pre uw adj
    layers_df["bpi_pre_uw_adj"] = np.where((layers_df["benchmark_premium_pre_uw_adj"] > 0) & (layers_df["bound_premium"].notna()), layers_df["bound_premium"] / layers_df["benchmark_premium_pre_uw_adj"], None)
    layers_df["tpi_pre_uw_adj"] = np.where((layers_df["technical_premium_pre_uw_adj"] > 0) & (layers_df["bound_premium"].notna()), layers_df["bound_premium"] / layers_df["technical_premium_pre_uw_adj"], None)

    # Implied Price
    layers_df["implied_price_per_m"] = np.where((layers_df["aggregate_limit"] > 0) & (layers_df["gross_technical_premium"].notna()), 
        layers_df["gross_technical_premium"] / (layers_df["aggregate_limit"] / 1e6),
        None)
    layers_df["implied_ilf"] = np.where((layers_df["implied_price_per_m"].shift(1) > 0) & (layers_df["implied_price_per_m"].notna()), 
        layers_df["implied_price_per_m"] / layers_df["implied_price_per_m"].shift(1), # ratio of implied price for current layer to previous layer
        None)

    # Quoted Price
    layers_df["quoted_price_per_m"] = np.where((layers_df["aggregate_limit"] > 0) & (layers_df["quoted_premium"] > 0), 
        layers_df["quoted_premium"] / (layers_df["aggregate_limit"] / 1e6),
        None)
    layers_df["quoted_ilf"] = np.where((layers_df["quoted_price_per_m"].shift(1) > 0) & (layers_df["quoted_price_per_m"].notna()), 
        layers_df["quoted_price_per_m"] / layers_df["quoted_price_per_m"].shift(1), # ratio of quoted price for current layer to previous layer
        None)
    layers_df["quoted_premium_net"] = np.where(layers_df["quoted_premium"] > 0, layers_df["quoted_premium"] * (1 - layers_df["brokerage"]), 0)

    # UW Adj Impact calcs
    layers_df["uw_adj_impact"] = np.where((layers_df["expected_loss_cost_pre_uw_adj"] > 0) & (layers_df["expected_loss_cost"].notna()),
        (layers_df["expected_loss_cost"] / layers_df["expected_loss_cost_pre_uw_adj"]) - 1,
        None)

    layers_df["pflr"] = layers_df["bpi"].apply(lambda x: const.benchmark_lr / x if x not in [None, 0] else None)
    layers_df["pflr_pre_uw_adj"] = layers_df["bpi_pre_uw_adj"].apply(lambda x: const.benchmark_lr / x if x not in [None, 0] else None)

    # Assign to nodes
    for layer, row in zip(cds.layers, layers_df.itertuples(index=False)):
        layer.quoted_premium = row.quoted_premium or 0 # Output for Standard KPIs view
        layer.quoted_premium_net = row.quoted_premium_net or 0 
        layer.brokerage = row.brokerage or 0 # Output for Standard KPIs view
        layer.expected_loss_cost = row.expected_loss_cost
        layer.expected_loss_cost_pre_uw_adj = row.expected_loss_cost_pre_uw_adj
        layer.bpi = row.bpi
        layer.bpi_pre_uw_adj = row.bpi_pre_uw_adj
        if layer.bpi is not None:
            layer.benchmark_premium = row.gross_benchmark_premium
            layer.benchmark_premium_net = row.net_benchmark_premium
            layer.technical_premium = row.gross_technical_premium
            layer.technical_premium_net = row.net_technical_premium
            layer.tpi = row.tpi
            layer.tpi_pre_uw_adj = row.tpi_pre_uw_adj
            layer.implied_price_per_m = row.implied_price_per_m
            layer.implied_ilf = row.implied_ilf
            layer.quoted_price_per_m = row.quoted_price_per_m
            layer.quoted_ilf = row.quoted_ilf
            layer.uw_adj_impact = row.uw_adj_impact
        if layer.bpi: # If BPI for the layer is not None and > 0
            layer.pflr = row.pflr
            layer.pflr_pre_uw_adj = row.pflr_pre_uw_adj

    # Standard KPIs view ------------------------------
        for index, layer in enumerate(layers):
            if (index==0):
                layer.status = cds.primary.status
                layer.section_reference = cds.primary.section_reference
            else:
                layer.status = layer.status_view
                layer.section_reference = layer.section_reference_view
            # For all layers:    
            layer.written_line = 1