import hx, datetime, numpy as np, pandas as pd
from algorithms.rate_constants import max_layers
from operator import itemgetter
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd






def rate_experience_rating(hxd):
    # predefine this to neaten up the code
    er = hxd.cds.experience_rating

    # dynamic variables used to track the number of rows in a list to use later
    num_layers = len(hxd.cds.layers)
    num_years = len(er.experience_table)

    #visibilities
    er.use_experience_rating_basic = not(er.claims_available)
    er.use_experience_rating_agg = er.claims_available and not er.claims_fgu
    er.use_experience_rating_full = er.claims_available and er.claims_fgu
    er.show_claims_input_table = er.use_experience_rating_agg or er.use_experience_rating_full
    # looped visibilities
    for index in range(1,max_layers+1):
        setattr(er, f"claims_show_layer_{index}", er.show_to_layer_fields * er.use_experience_rating_full) if index <= num_layers else False
        setattr(er, f"calculation_show_layer_{index}", er.use_experience_rating_full) if index <= num_layers else False


    #basic experience rating lookup
    table_basic_experience_rating = hx.params.table_basic_experience_rating
    er.experience_rating_basic.experience_adjustment = table_basic_experience_rating[table_basic_experience_rating["Clean Years"]==er.experience_rating_basic.clean_years]["Adjustment"].iloc[0]

    # Claims table #################
    # going to use pandas to work on claims table

    # Specify your override columns
    override_columns = ["currency", "estimated_yoa"]
    if er.use_experience_rating_full:
        # loop through dynamic override column
        for i in range(1, num_layers + 1):
            override_columns = override_columns + [f"deductible_to_use_layer_{i}"]

    # output columns are all columns except input & override columns
    output_columns = ["use_claim",
                    "total_incurred_clm_curr",
                    "clm_to_slip_fx_rate",
                    "total_incurred",
                    "inflated_total_incurred",
                    "claims_development",
                    "development_method",
                    "developed_inflated_total_incurred"]
    if er.use_experience_rating_full:
        # loop through dynamic output column
        for i in range(1, num_layers + 1):
            output_columns = output_columns + [f"limit_layer_{i}"] + [f"excess_layer_{i}"] + [f"cl_developed_total_incurred_layer_{i}"]


    # Pass that list node to Pandas as normal
    claims_df = pd_df_from_hx_list(er.claims)

    # calculate columns
    # asign variables to make code neater/shorter
    inception_date = hxd.hx_core.inception_date

    # estimated_yoa calculated value
    claims_df['currency_calculated'] = hxd.cds.currencies.source_currency
    #need to calculate a selected column to use later in the calcs
    claims_df['currency_selected'] = claims_df['currency_calculated']
    claims_df.loc[claims_df['currency_override'].notnull(), 'currency_selected'] = claims_df['currency_override']
    
    # EXAMPLE of how to use apply for if conditioning, though Seb recommends df.loc as apply is apparently much slower.
    # claims_df['currency_selected'] = claims_df.apply(
    #     #use axis = 1 here as the whole claims_df (since we need to access multiple columns) was taken before the apply, not just a single column
    #     lambda x: x['currency_calculated'] if pd.isnull(x['currency_override']) else x['currency_override'], axis = 1
    #     )

    # need to coerce to datetime owing to null values
    claims_df['claim_made_date'] = pd.to_datetime(claims_df['claim_made_date'], errors='coerce')

    # use_claim: true if date is not null and date year < inception date year
    claims_df['use_claim'] = True
    claims_df.loc[claims_df['claim_made_date'].isnull() | (claims_df['claim_made_date'].dt.year >= inception_date.year), 'use_claim'] = False
    
    # estimated_yoa calculated value
    claims_df['estimated_yoa_calculated'] = None
    # create a proxy claim made date column using the year of the claim but the month/day from inception date to estimate which YOA the claim fell in.
    claims_df['proxy_cmd'] = pd.to_datetime(dict(year=claims_df['claim_made_date'].dt.year, month=inception_date.month, day=inception_date.day))
    claims_df.loc[claims_df['proxy_cmd'] <= claims_df['claim_made_date'], 'estimated_yoa_calculated'] = claims_df['claim_made_date'].dt.year
    claims_df.loc[claims_df['proxy_cmd'] > claims_df['claim_made_date'], 'estimated_yoa_calculated'] = claims_df['claim_made_date'].dt.year - 1
    #remove the unnecessary column
    claims_df = claims_df.drop(['proxy_cmd'], axis = 1)

    claims_df['estimated_yoa_selected'] = claims_df['estimated_yoa_calculated']
    claims_df.loc[claims_df['estimated_yoa_override'].notnull(), 'estimated_yoa_selected'] = claims_df['estimated_yoa_override']

    if er.claims_net_of_deductible:
        claims_df['total_incurred_clm_curr'] = claims_df["incurred_claims"] + claims_df["deductible"]
    else:
        claims_df['total_incurred_clm_curr'] = claims_df["incurred_claims"]

    #preload the table to a variable to avoid calling it from hxd repeatedly
    table_currency = hx.params.table_currency
    #calculate the fx of the slip currency
    slip_fx_rate = table_currency[table_currency["currency"] == hxd.cds.currencies.source_currency]["exchange_rate"].iloc[0]
    #calculate the fx from claim currency to slip
    claims_df['clm_to_slip_fx_rate'] = claims_df.merge(table_currency, how='left', left_on = "currency_selected", right_on = "currency")["exchange_rate"] / slip_fx_rate

    claims_df['total_incurred'] = claims_df['total_incurred_clm_curr'] / claims_df['clm_to_slip_fx_rate']
    
    # Claims Inflation:
    #calculate cumulative claims inflation table
    table_claims_inflation = hx.params.table_claims_inflation
    # create a cumulative inflation column
    table_claims_inflation["cumulative_inflation"] = (1 + table_claims_inflation["claims_inflation"]).cumprod()
    # normalise the inflation to be 1 at the inception year
    inception_inflation = table_claims_inflation["cumulative_inflation"][table_claims_inflation["year"] == inception_date.year].iloc[0]
    table_claims_inflation["cumulative_inflation"] = table_claims_inflation["cumulative_inflation"] / inception_inflation
    # somewhat unnecessary step but just force all inflation values beyond the inception year to be 1
    table_claims_inflation.loc[table_claims_inflation["year"] > inception_date.year, "cumulative_inflation"] = 1

    #create a spare column with no null values (to prevent the merge breaking), but don't want to overwrite the original column
    claims_df["estimated_yoa_selected_2"] = claims_df["estimated_yoa_selected"].fillna(0)
    claims_df = claims_df.merge(table_claims_inflation, how="left", left_on="estimated_yoa_selected_2", right_on="year")
    claims_df['inflated_total_incurred'] = None
    claims_df.loc[claims_df["use_claim"], 'inflated_total_incurred'] = claims_df["total_incurred"] * claims_df["cumulative_inflation"]#.fillna(1) this will stop errors forming if claim is older than oldest year, but won't work correctly either
    claims_df = claims_df.drop(['estimated_yoa_selected_2'], axis = 1)


    table_development_patterns = hx.params.table_development_patterns
    claims_df['years_developed'] = inception_date.year - claims_df["estimated_yoa_selected"]
    claims_df['claims_development'] = claims_df.merge(table_development_patterns, how='left', left_on = "years_developed", right_on = "years")["development"]
    # make sure empty values are specifically "None", since the merge creates NaN which setattr has trouble when writing to the table
    claims_df['claims_development'] = claims_df['claims_development'].replace({np.nan: None})
    #remove the unnecessary column
    claims_df = claims_df.drop(['years_developed'], axis = 1)
    
    table_development_method = hx.params.table_development_method
    # replicating Excel VLOOKUP approximate match, can't use pandas merge_asof since need to sort data and it is then passed back out of order
    #reverese the range because the parameter table is ordered largest to smallest
    for i in reversed(range(table_development_method.shape[0])):
        # first row of parameter table
        if i == 0:
            claims_df.loc[
                (claims_df['claims_development'] >= table_development_method["development"].iloc[i])
                , "development_method"
                ] = table_development_method["method"].iloc[i]
        # last row of parameter table
        elif i == (table_development_method.shape[0] - 1):
            claims_df.loc[
                (claims_df['claims_development'] < table_development_method["development"].iloc[i])
                , "development_method"
                ] = table_development_method["method"].iloc[i]
        # all other rows of parameter table
        else:
            claims_df.loc[
                (claims_df['claims_development'] < table_development_method["development"].iloc[i])
                , "development_method"
                ] = table_development_method["method"].iloc[i+1]
            claims_df.loc[
                (claims_df['claims_development'] >= table_development_method["development"].iloc[i])
                , "development_method"
                ] = table_development_method["method"].iloc[i]

    # putting Nulls where appropriate, the "~" is the equivalent of "not" for a pandas df
    claims_df.loc[~claims_df["use_claim"], 'development_method'] = None


    claims_df["developed_inflated_total_incurred"] = claims_df['inflated_total_incurred']
    claims_df.loc[
        claims_df["claim_status"] == "Open", "developed_inflated_total_incurred"
        ] = claims_df['inflated_total_incurred'] / claims_df['claims_development']

    #calculate to layer columns, specifically if FGU losses being used
    if er.use_experience_rating_full:
        for index, layer in enumerate(hxd.cds.layers, start=1):
            claims_df[f"deductible_to_use_layer_{index}_calculated"] = layer.deductible or 0
            # create selected
            claims_df[f"deductible_to_use_layer_{index}_selected"] = claims_df[f"deductible_to_use_layer_{index}_calculated"]
            claims_df.loc[
                claims_df[f"deductible_to_use_layer_{index}_override"].notnull()
                , f"deductible_to_use_layer_{index}_selected"
                ] = claims_df[f"deductible_to_use_layer_{index}_override"]
                
            claims_df[f"limit_layer_{index}"] = layer.limit or 0
            claims_df[f"excess_layer_{index}"] = layer.excess or 0

            # apply layer structure (limits excess, deductible) to claims
            # use a number of intermediary steps
            claims_df["incurred_to_use"] = 0
            claims_df.loc[
                (claims_df["development_method"] == "CL") 
                & claims_df["inflated_total_incurred"].notnull(),
                "incurred_to_use"
            ] = claims_df["developed_inflated_total_incurred"]
            claims_df.loc[
                (claims_df["development_method"] != "CL") 
                & claims_df["inflated_total_incurred"].notnull(),
                "incurred_to_use"
            ] = claims_df["inflated_total_incurred"]

            # create a number of dummy columns to apply max across the whole column using vectorisation instead of apply
            #apply excess
            claims_df["zeros"] = 0
            claims_df["remove_excess"] = claims_df["incurred_to_use"] - claims_df[f"excess_layer_{index}"]
            claims_df["excess_applied"] = claims_df[["remove_excess", "zeros"]].max(axis = 1)
            # apply limit
            claims_df["limit_applied"] = claims_df[["excess_applied", f"limit_layer_{index}"]].min(axis = 1)
            # apply deductible
            claims_df["remove_deductible"] = claims_df["limit_applied"] - claims_df[f"deductible_to_use_layer_{index}_selected"]
            claims_df[f"cl_developed_total_incurred_layer_{index}"] = claims_df[["remove_deductible", "zeros"]].max(axis = 1)
            #drop all the spare columns
            claims_df = claims_df.drop([
                'incurred_to_use', 
                "zeros", 
                "remove_excess", 
                "excess_applied", 
                "limit_applied", 
                "remove_deductible"
                ], axis = 1)


                
    
    # output claims_df to claims list
    write_pd_to_hxd(claims_df, er.claims, output_columns, override_columns)


    # calculate experience rating years table
    for index, year in enumerate(er.experience_table, start = +1):
        # create yoa field for each historic year
        year.yoa = inception_date.year - index

        # create a table of the inflation values to apply based on historic year
        # perform cumulative multiplication of exposure inflation
        table_exposure_inflation = hx.params.table_exposure_inflation
        inflation_list = 1 + table_exposure_inflation[
                                (table_exposure_inflation["year"] >= year.yoa) 
                                & (table_exposure_inflation["year"] < inception_date.year)
                                ]["exposure_inflation"]
        # on-level exposure
        year.exposure_onlevelled = year.exposure * np.prod(inflation_list) if year.exposure else None

        # create a table of the rate change values to apply based on historic year
        # perform cumulative multiplication of premium rate change
        table_premium_rate_change = hx.params.table_premium_rate_change
        rate_change_list = table_premium_rate_change[
                                (table_premium_rate_change["year"] >= year.yoa) 
                                & (table_premium_rate_change["year"] < inception_date.year)
                                ]["rate_change"]
        # rate adjust premiums
        year.premium_rate_adjusted = year.premium * np.prod(rate_change_list) if year.premium else None

        #aggregate number and inflated claims by YOA
        year.agg_num_claims = claims_df.loc[
                                (claims_df["use_claim"]) 
                                & (claims_df["estimated_yoa_selected"] == year.yoa) 
                                & (claims_df["inflated_total_incurred"].notnull())
                                , "inflated_total_incurred"
                                ].shape[0]
        year.agg_sum_claims = claims_df.loc[
                                (claims_df["use_claim"]) 
                                & (claims_df["estimated_yoa_selected"] == year.yoa) 
                                & (claims_df["inflated_total_incurred"].notnull())
                                , "inflated_total_incurred"
                                ].sum()

        # default include all years with exposure except the most recent year as is unlikely to be fully reported                        
        year.include_year.calculated = 0 if index == 1 or year.exposure_onlevelled is None else 1
        #alternative method where a year might be given a partial weight instead of just include/exclude
        # year.include_year_2.calculated = 0 if index == 1 or year.exposure_onlevelled is None else 1

        # table_development_method parameter table was defined above
        year.claims_development = table_development_patterns[table_development_patterns["years"] == (index)]["development"].iloc[0]
        # for non FGU claims, use loss ratio approach as can't develop claims to ultimate since we only have information about claims to layer
        if er.use_experience_rating_agg:
            year.loss_ratio = year.agg_sum_claims/year.premium_rate_adjusted if year.premium_rate_adjusted and year.include_year.selected == 1 else None
        
        if er.use_experience_rating_full:
            year.ulr = 0.7 #PLACEHOLDER needs to be updated with the Benchamrk ULR for the class being modelled
            # table_development_method parameter table was defined above
            year.development_method = table_development_method[table_development_method["development"] <= year.claims_development]["method"].iloc[0]
            for index2 in range (1, num_layers + 1):
                # sum up inflated (and developed for CL years) claims by YOA
                setattr(year
                        , f"cl_developed_layer_{index2}"
                        , claims_df.loc[
                            (claims_df["use_claim"]) 
                            & (claims_df["estimated_yoa_selected"] == year.yoa) 
                            & (claims_df[f"cl_developed_total_incurred_layer_{index2}"].notnull())
                            , f"cl_developed_total_incurred_layer_{index2}"
                            ].sum()
                )
                # apply development of claims to ultimate
                if year.development_method == "IELR":
                        temp_ult = year.premium_rate_adjusted * year.ulr if not year.premium_rate_adjusted is None else None
                elif year.development_method == "BF":
                        temp_ult =  (
                                        getattr(year, f"cl_developed_layer_{index2}") 
                                        + (1-year.claims_development) * year.premium_rate_adjusted * year.ulr  
                                        if not year.premium_rate_adjusted is None else None
                                    )
                else:
                        temp_ult = getattr(year, f"cl_developed_layer_{index2}") 
                setattr(year, f"ult_layer_{index2}", temp_ult)
                # turn ultimate claims into a claims per million exposure rate (if exposure has been etnered)
                setattr(year
                        , f"ult_rate_layer_{index2}"
                        , getattr(year, f"ult_layer_{index2}") /( year.exposure_onlevelled/1e6) 
                            if (not year.exposure_onlevelled is None and  not getattr(year, f"ult_layer_{index2}") is None) 
                            else None
                        )
            
        
        # exposure weight comparing onlevelled exposure of historic yoa to this year's quoted policy exposure
        year.exposure_weight = (
                                min(year.exposure_onlevelled / hxd.cds.exposure.aggregate.exposure, 1) 
                                if (year.include_year.selected == 1 and not hxd.cds.exposure.aggregate.exposure is None) else None
                                )
        # default decay factor taken from BBT to represent reduction in relevance of older years
        year.decay_weight = pow(0.9,(index-1)) if year.include_year.selected == 1 else None

        year.development_weight = year.claims_development if year.include_year.selected == 1 else None

        #overall score is product of previosu weights
        year.overall_score = (
                                (year.exposure_weight or 0) 
                                * (year.decay_weight or 0) 
                                * (year.development_weight or 0) 
                                if year.include_year.selected == 1 else None)
        # alternative method where a year might be given a partial weight instead of just include/exclude
        # year.overall_score = (year.exposure_weight or 0) * (year.decay_weight or 0) * (year.development_weight or 0) * (year.include_year_2 or 0) if year.include_year.selected == 1 else None

    # reweight overall scores to sum to 100%, this needs to be done outside the original "years" loop to make sure all years have been calculated before doing this step
    for year in er.experience_table:
        # sum of overall scores across all years
        total_overall_score = sum([year.overall_score for year in er.experience_table if not year.overall_score is None])
        # scale the overall score for the yoa in question
        year.weight_to_year = year.overall_score / (total_overall_score or 1) if year.overall_score else None

    # expected loss ratio is the sumproduct of reweighted scores and calculated loss ratios for all included years
    for index in range(1, num_layers + 1):
            setattr(getattr(er, f"summary_layer_{index}"), "filter", True if index <= num_layers else False)
            # different outputs for non FGU claims
            if er.use_experience_rating_agg:
                loss_ratio = sum([
                                    year.weight_to_year * year.loss_ratio for year in er.experience_table 
                                    if (not year.weight_to_year is None and not year.loss_ratio is None)
                                    ])
                setattr(getattr(er, f"summary_layer_{index}"), "expected_loss_ratio", loss_ratio)
                layer_quoted_premium = hxd.cds.layers[index - 1].quoted_premium
                setattr(
                    getattr(er, f"summary_layer_{index}")
                    , "expected_losses"
                    , loss_ratio * layer_quoted_premium if (not layer_quoted_premium is None) else None
                    )

            # different outputs for FGU claims
            if er.use_experience_rating_full:
                loss_rate = sum([
                                    year.weight_to_year * getattr(year, f"ult_rate_layer_{index}") for year in er.experience_table 
                                    if (not year.weight_to_year is None and not getattr(year, f"ult_rate_layer_{index}") is None)
                                    ])
                setattr(getattr(er, f"summary_layer_{index}"), "loss_rate", loss_rate)
                setattr(getattr(er, f"summary_layer_{index}")
                        , "expected_losses"
                        , loss_rate * hxd.cds.exposure.aggregate.exposure/1e6 if (not hxd.cds.exposure.aggregate.exposure is None) else None
                        )

    