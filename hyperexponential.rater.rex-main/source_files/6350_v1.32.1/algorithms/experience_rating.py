import hx, datetime, numpy as np, pandas as pd
from algorithms.exposure_management_task import  pull_exchange_rate_data
from algorithms.constant import MAX_LAYERS
from algorithms.utilities import pd_df_from_hx_list, write_pd_to_hxd

def apply_experience_adjustment(hxd,progress):
    if hxd.experience_rating.use_experience_rating_agg or hxd.experience_rating.use_experience_rating_full:
        for index, layer in enumerate(hxd.layers, start=1):
            layer.perils.fire.experience_rating_adj = getattr(hxd.experience_rating, f"summary_layer_{index}").experience_adjustment
            layer.perils.scs.experience_rating_adj = getattr(hxd.experience_rating, f"summary_layer_{index}").experience_adjustment
            layer.perils.flood.experience_rating_adj = getattr(hxd.experience_rating, f"summary_layer_{index}").experience_adjustment
            layer.perils.wildfire.experience_rating_adj = getattr(hxd.experience_rating, f"summary_layer_{index}").experience_adjustment
    
    if hxd.experience_rating.use_experience_rating_basic:
        for index, layer in enumerate(hxd.layers, start=1):
            layer.perils.fire.experience_rating_adj = hxd.experience_rating.experience_rating_basic.experience_adjustment
            layer.perils.scs.experience_rating_adj = hxd.experience_rating.experience_rating_basic.experience_adjustment
            layer.perils.flood.experience_rating_adj = hxd.experience_rating.experience_rating_basic.experience_adjustment
            layer.perils.wildfire.experience_rating_adj = hxd.experience_rating.experience_rating_basic.experience_adjustment

    # flags for validation
    hxd.experience_rating.experience_rating_run = True
    hxd.experience_rating.run_rater_run = False

def remove_experience_adjustment(hxd,progress):
    for index, layer in enumerate(hxd.layers, start=1):
        layer.perils.fire.experience_rating_adj = 0
        layer.perils.scs.experience_rating_adj = 0
        layer.perils.flood.experience_rating_adj = 0
        layer.perils.wildfire.experience_rating_adj = 0


def experience_rating(hxd):
    # predefine this to neaten up the code
    er = hxd.experience_rating

    # dynamic variables used to track the number of rows in a list to use later
    num_layers = len(hxd.layers)
    num_years = len(er.experience_table)

    #visibilities
    er.use_experience_rating_basic = not(er.claims_available)
    er.use_experience_rating_agg = er.claims_available and not er.claims_fgu
    er.use_experience_rating_full = er.claims_available and er.claims_fgu
    er.show_claims_input_table = er.use_experience_rating_agg or er.use_experience_rating_full
    # looped visibilities
    for index in range(1,MAX_LAYERS+1):
        setattr(er, f"claims_show_layer_{index}", er.show_to_layer_fields * er.use_experience_rating_full) if index <= num_layers else False
        setattr(er, f"calculation_show_layer_{index}", er.use_experience_rating_full) if index <= num_layers else False

    #basic experience rating lookup
    table_basic_experience_rating = hx.params.basic_experience_rating
    er.experience_rating_basic.experience_adjustment = table_basic_experience_rating[table_basic_experience_rating["Clean Years"]==er.experience_rating_basic.clean_years]["Adjustment"].iloc[0]

    # input instructions
    if er.use_experience_rating_full:
        er.input_instructions = "**Instructions:**\nPlease enter the exposure to include a year in the experience rating calculation."
    else:
        er.input_instructions = "**Instructions:**\nPlease enter both the exposure and the premium to include a year in the experience rating calculation."

    # CLAIMS TABLE ########################################################################################################################################
    # going to use pandas to work on claims table

    # Specify your override columns
    override_columns = ["currency", "estimated_yoa"]
    if er.use_experience_rating_full:
        # loop through dynamic override column
        for i in range(1, num_layers + 1):
            override_columns = override_columns + [f"deductible_to_use_layer_{i}"]

    # output columns are all columns except input & override columns
    output_columns = ["use_claim",
                    "is_cat",
                    "total_incurred_clm_curr",
                    "total_incurred",
                    "inflated_total_incurred",
                    "claims_development",
                    "development_method",
                    "developed_inflated_total_incurred",
                    "sublimit"]
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
    claims_df['currency_calculated'] = hxd.policy_information.slip_currency
    #need to calculate a selected column to use later in the calcs
    claims_df['currency_selected'] = claims_df['currency_calculated']
    claims_df.loc[claims_df['currency_override'].notnull(), 'currency_selected'] = claims_df['currency_override']

    # need to coerce to datetime owing to null values
    claims_df['claim_made_date'] = pd.to_datetime(claims_df['claim_made_date'], errors='coerce')

    #is cat: true for EQ or WS perils
    claims_df["is_cat"] = False
    claims_df.loc[claims_df['cause_of_loss'].isin(["Named Windstorm","Quake"]), "is_cat"] = True

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

    # use_claim: true if date is not null and date year < inception date year
    claims_df['use_claim'] = True
    claims_df.loc[claims_df['claim_made_date'].isnull() | (claims_df['estimated_yoa_selected'] >= inception_date.year), 'use_claim'] = False

    # force blank cells to 0 for calculations
    claims_df.loc[claims_df["incurred_claims"].isnull(), "incurred_claims"] = 0
    claims_df.loc[claims_df["deductible"].isnull(), "deductible"] = 0

    if er.claims_net_of_deductible:
        claims_df['total_incurred_clm_curr'] = claims_df["incurred_claims"] + claims_df["deductible"]
    else:
        claims_df['total_incurred_clm_curr'] = claims_df["incurred_claims"]

    # claims_df['clm_to_slip_fx_rate'] produced via async task "pull_exchange_rate_claim_data_task" 
    # to avoidconstantly querying Exposure Management DB
    claims_df['total_incurred'] = None
    claims_df.loc[
        claims_df['clm_to_slip_fx_rate'].notnull()
        , 'total_incurred'
    ] = claims_df['total_incurred_clm_curr'] * claims_df['clm_to_slip_fx_rate']

    # Claims Inflation & Development:
    #calculate cumulative claims inflation table
    team = hxd.policy_information.team
    #inflation initialisation
    table_claims_inflation = hx.params.claims_inflation
    claims_df['inflated_total_incurred'] = None
    #development inititalisation
    table_development_patterns = hx.params.development_patterns
    table_development_method = hx.params.development_method
    claims_df['claims_development'] = None
    claims_df['development_method'] = None
    claims_df['developed_inflated_total_incurred'] = None

    #"if" condition needed as if no UW, team is None and column lookups fail
    if not team is  None:
        # inflation
        # create a cumulative inflation column
        table_claims_inflation["cumulative_inflation"] = (1 + table_claims_inflation[f"{team}_Claims_Inflation"]).cumprod()
        # normalise the inflation to be 1 at the inception year
        inception_inflation = table_claims_inflation["cumulative_inflation"][table_claims_inflation["Year"] == inception_date.year].iloc[0]
        table_claims_inflation["cumulative_inflation"] = table_claims_inflation["cumulative_inflation"] / inception_inflation
        # somewhat unnecessary step but just force all inflation values beyond the inception year to be 1
        table_claims_inflation.loc[table_claims_inflation["Year"] > inception_date.year, "cumulative_inflation"] = 1

        #create a spare column with no null values (to prevent the merge breaking), but don't want to overwrite the original column
        claims_df["estimated_yoa_selected_2"] = claims_df["estimated_yoa_selected"].fillna(0)
        claims_df = claims_df.merge(table_claims_inflation, how="left", left_on="estimated_yoa_selected_2", right_on="Year")
        claims_df.loc[claims_df["use_claim"] & (claims_df["total_incurred"].notnull()), 'inflated_total_incurred'] = claims_df["total_incurred"] * claims_df["cumulative_inflation"]
        claims_df = claims_df.drop(['estimated_yoa_selected_2'], axis = 1)

        #development
        # turn inception date into a column for easy pandas manipulation
        claims_df["inception_date"] = pd.to_datetime(inception_date)
        # numpy timedelta turns the difference into months
        # +1.5 is to round to nearest quarter as // is modulus function
        claims_df['quarters_developed'] = (
                                            (claims_df["inception_date"] - claims_df["claim_made_date"]) 
                                            / np.timedelta64(1, 'M') 
                                            + 1.5
                                        ) // 3
        claims_df['claims_development'] = claims_df.merge(table_development_patterns, how='left', left_on = "quarters_developed", right_on = "quarters")[f"{team}_development"]
        # make sure empty values are specifically "None", since the merge creates NaN which setattr has trouble when writing to the table
        claims_df['claims_development'] = claims_df['claims_development'].replace({np.nan: None})
        #remove the unnecessary column
        claims_df = claims_df.drop(['quarters_developed'], axis = 1)
        
        
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
        # only develop open claims
        claims_df.loc[
            (claims_df["claim_status"] == "Open") & (claims_df['inflated_total_incurred'].notnull())
            , "developed_inflated_total_incurred"
            ] = claims_df['inflated_total_incurred'] / claims_df['claims_development']

    # capture peril specific sublimits and deductible
    peril_names = ["Fire","Named Windstorm","SCS","Flood","Quake","Wildfire"]
    sublimit_names = [None,"ws_sublimit","scs_sublimit","fl_sublimit","eq_sublimit",None]

    deductible_names_1 = ["fire","named_windstorm","scs","flood","quake","wildfire"]
    deductible_names_2 = ["deductible","per_occurrence_ded","per_occurrence_ded","per_occurrence_ded","per_occurrence_ded","deductible"]

    for i in range(len(peril_names)):
        if sublimit_names[i] is None:
            claims_df.loc[claims_df["cause_of_loss"] == peril_names[i], "sublimit"] = None
        else:
            claims_df.loc[claims_df["cause_of_loss"] == peril_names[i], "sublimit"] = getattr(hxd.sublimit,sublimit_names[i])

        #calculate "to layer" columns, specifically if FGU losses being used
        if er.use_experience_rating_full:
            for index, layer in enumerate(hxd.layers, start=1):
                # apply peril specific deductibles
                claims_df.loc[
                    claims_df["cause_of_loss"] == peril_names[i]
                    , f"deductible_to_use_layer_{index}_calculated"
                    ] = getattr(
                            getattr(layer.perils, deductible_names_1[i])
                            , deductible_names_2[i]
                        ) or 0

    if er.use_experience_rating_full:
        for index, layer in enumerate(hxd.layers, start=1):
            # create selected
            claims_df[f"deductible_to_use_layer_{index}_selected"] = claims_df[f"deductible_to_use_layer_{index}_calculated"]
            claims_df.loc[
                claims_df[f"deductible_to_use_layer_{index}_override"].notnull()
                , f"deductible_to_use_layer_{index}_selected"
                ] = claims_df[f"deductible_to_use_layer_{index}_override"]

            claims_df[f"excess_layer_{index}"] = layer.excess or 0
                    
            # apply sublimit column where relevant
            # create a number of dummy columns to apply max across the whole column using vectorisation instead of apply
            claims_df["zeros"] = 0
            claims_df[f"limit_layer_{index}"] = layer.limit or 0

            #apply excess
            claims_df["sublimit_remove_excess"] = claims_df["sublimit"] - claims_df[f"excess_layer_{index}"]
            claims_df["sublimit_excess_applied"] = claims_df[["sublimit_remove_excess", "zeros"]].max(axis = 1)
            # apply limit
            claims_df["sublimit_limit_applied"] = claims_df[["sublimit_excess_applied", f"limit_layer_{index}"]].min(axis = 1)

            claims_df.loc[claims_df["sublimit"].notnull(), f"limit_layer_{index}"] = claims_df["sublimit_limit_applied"]



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
            claims_df["remove_excess"] = claims_df["incurred_to_use"] - claims_df[f"excess_layer_{index}"]
            claims_df["excess_applied"] = claims_df[["remove_excess", "zeros"]].max(axis = 1)
            # apply limit
            claims_df["limit_applied"] = claims_df[["excess_applied", f"limit_layer_{index}"]].min(axis = 1)
            # apply deductible
            claims_df["remove_deductible"] = claims_df["limit_applied"] - claims_df[f"deductible_to_use_layer_{index}_selected"]
            claims_df[f"cl_developed_total_incurred_layer_{index}"] = claims_df[["remove_deductible", "zeros"]].max(axis = 1)
            #drop all the spare columnsinflation_list
            claims_df = claims_df.drop([
                'incurred_to_use', 
                "zeros", 
                "remove_excess", 
                "excess_applied", 
                "limit_applied",
                "sublimit_remove_excess", 
                "sublimit_excess_applied", 
                "sublimit_limit_applied", 
                "remove_deductible"
                ], axis = 1)

    # write columns back to claims table
    write_pd_to_hxd(claims_df, er.claims, output_columns, override_columns)

    # EXPERIENCE TABLE ##############################################################################################################################
    # predefine tables for rate change and claims inflation
    table_exposure_inflation = hx.params.exposure_inflation
    table_premium_rate_change = hx.params.premium_rate_change

    table_exposure_inflation_adj = table_exposure_inflation
    table_premium_rate_change_adj = table_premium_rate_change

    #apply any overrides to inflation/rate change
    for index, year in enumerate(er.experience_table, start = +1):
        if not team is  None:
            year_yoa = inception_date.year - index
            
            year.exposure_inflation.calculated = table_exposure_inflation.loc[(table_exposure_inflation["Year"] <= year_yoa), f"{team}_Exposure_Inflation"].iloc[0]
            year.premium_rate_change.calculated = table_premium_rate_change.loc[(table_premium_rate_change["Year"] <= year_yoa), f"{team}_Rate_Change"].iloc[0]
            #update values in adjusted table but retain original table (may not be necessary)
            table_exposure_inflation_adj.loc[(table_exposure_inflation_adj["Year"] == year_yoa), f"{team}_Exposure_Inflation"] = year.exposure_inflation.selected
            table_premium_rate_change_adj.loc[(table_premium_rate_change_adj["Year"] == year_yoa), f"{team}_Rate_Change"] = year.premium_rate_change.selected

    # initialise a variable
    premium_to_use = 0

    # calculate experience rating years table
    for index, year in enumerate(er.experience_table, start = +1):
        # create yoa field for each historic year
        year.yoa = inception_date.year - index
        # used for labelling
        year.str_yoa = str(year.yoa)

        # create a table of the inflation values and rate change values to apply based on historic year
        # perform cumulative multiplication of exposure inflation and premium rate change
        #"if" condition needed as if no UW, team is None and column lookups fail
        if not team is  None:
            # exposure
            inflation_list = 1 + table_exposure_inflation_adj[
                                    (table_exposure_inflation_adj["Year"] >= year.yoa) 
                                    & (table_exposure_inflation_adj["Year"] < inception_date.year)
                                    ][f"{team}_Exposure_Inflation"]

            # on-level exposure
            year.exposure_onlevelled = year.exposure * np.prod(inflation_list) if year.exposure else None

            #rate change
            rate_change_list = table_premium_rate_change_adj[
                                    (table_premium_rate_change_adj["Year"] >= year.yoa) 
                                    & (table_premium_rate_change_adj["Year"] < inception_date.year)
                                    ][f"{team}_Rate_Change"]
            # rate adjust premiums
            year.premium_rate_adjusted = year.premium * np.prod(rate_change_list) if year.premium else None
        else:
            year.exposure_onlevelled = None
            year.premium_rate_adjusted = None

        # to avoid snowball effect of using achieved premium to transform LR to expected losses, use a quoted premium from the most recent year
        if premium_to_use == 0 and not year.premium_rate_adjusted is None:
            premium_to_use = year.premium_rate_adjusted

        # aggregation colunns
        for peril in peril_names:
            setattr(year
                    , f"num_claims_{peril.replace(' ', '_').lower()}"
                    , claims_df.loc[
                                (claims_df["use_claim"]) 
                                & (claims_df["estimated_yoa_selected"] == year.yoa) 
                                & (claims_df["cause_of_loss"] == peril)
                                & (claims_df["inflated_total_incurred"].notnull())
                                , "inflated_total_incurred"
                                ].shape[0] 
            )
            setattr(year
                    , f"unadj_sum_claims_{peril.replace(' ', '_').lower()}"
                    , claims_df.loc[
                                (claims_df["use_claim"]) 
                                & (claims_df["estimated_yoa_selected"] == year.yoa) 
                                & (claims_df["cause_of_loss"] == peril)
                                & (claims_df["total_incurred"].notnull())
                                , "total_incurred"
                                ].sum() 
            )
            setattr(year
                    , f"sum_claims_{peril.replace(' ', '_').lower()}"
                    , claims_df.loc[
                                (claims_df["use_claim"]) 
                                & (claims_df["estimated_yoa_selected"] == year.yoa) 
                                & (claims_df["cause_of_loss"] == peril)
                                & (claims_df["inflated_total_incurred"].notnull())
                                , "inflated_total_incurred"
                                ].sum() 
            )
 
        # default include all years with exposure
        if er.use_experience_rating_full:
            year.include_year.calculated = 0 if year.exposure_onlevelled is None else 1
        else:
            year.include_year.calculated = 0 if ((year.premium_rate_adjusted is None) or (year.exposure_onlevelled is None)) else 1

        if not team is  None:
            # table_development_method parameter table was defined above
            # * 4 used to convert from years to quarters
            year.claims_development = table_development_patterns[table_development_patterns["quarters"] == (index * 4)][f"{team}_development"].iloc[0]
        else:
            year.claims_development = None

        # for non FGU claims, use loss ratio approach as can't develop claims to ultimate since we only have information about claims to layer
        if er.use_experience_rating_agg:
            # set up temporary variable the sum of claims across all perils
            year_agg_sum_claims = claims_df.loc[
                                    (claims_df["use_claim"]) 
                                    & (claims_df["estimated_yoa_selected"] == year.yoa) 
                                    & (claims_df["inflated_total_incurred"].notnull())
                                    # adjusted code to only use non-cat claims
                                    & (claims_df["is_cat"] == False)
                                    , "inflated_total_incurred"
                                    ].sum()
            year.loss_ratio = year_agg_sum_claims / year.premium_rate_adjusted if year.premium_rate_adjusted and year.include_year.selected == 1 else None
        
        if er.use_experience_rating_full:
            # set benchamrk ULRs split by cat and non-cat
            table_benchmark_ulr = hx.params.benchmark_ulr
            if not team is  None:
                year.non_cat_ulr = table_benchmark_ulr[(table_benchmark_ulr["team"] == team)]["non_cat"].iloc[0]
                # commented out as removing Cat component from experience rating for now
                # year.cat_ulr = table_benchmark_ulr[(table_benchmark_ulr["team"] == team)]["cat"].iloc[0]

            # table_development_method parameter table was defined above
            year.development_method = table_development_method[table_development_method["development"] <= year.claims_development]["method"].iloc[0] if team else None
            for index2 in range (1, num_layers + 1):
                # commented out as removing Cat component from experience rating for now
                # for IsCat in ["Non Cat", "Cat"]:
                for IsCat in ["Non Cat"]:
                    # temp variable to turn IsCat text into boolean
                    IsCat_TF = (IsCat == "Cat")
                    # sum up inflated (and developed for CL years) claims by YOA
                    setattr(year
                            , f"{IsCat.replace(' ', '_').lower()}_cl_developed_layer_{index2}"
                            , claims_df.loc[
                                (claims_df["use_claim"]) 
                                & (claims_df["estimated_yoa_selected"] == year.yoa) 
                                & (claims_df[f"cl_developed_total_incurred_layer_{index2}"].notnull())
                                & (claims_df["is_cat"] == IsCat_TF)
                                , f"cl_developed_total_incurred_layer_{index2}"
                                ].sum()
                    )
                    # apply development of claims to ultimate
                    if not team is None:
                        if year.development_method == "IELR":
                            temp_ult = year.premium_rate_adjusted * getattr(year, f"{IsCat.replace(' ', '_').lower()}_ulr") if not year.premium_rate_adjusted is None else None
                        elif year.development_method == "BF":
                            temp_ult =  (
                                getattr(year, f"{IsCat.replace(' ', '_').lower()}_cl_developed_layer_{index2}")
                                + (1-year.claims_development) * year.premium_rate_adjusted * getattr(year, f"{IsCat.replace(' ', '_').lower()}_ulr")
                                if not year.premium_rate_adjusted is None else None
                            )
                        else:
                            temp_ult = getattr(year, f"{IsCat.replace(' ', '_').lower()}_cl_developed_layer_{index2}")
                    else:
                        temp_ult = None
                    setattr(year, f"{IsCat.replace(' ', '_').lower()}_ult_layer_{index2}", temp_ult)
                    # turn ultimate claims into a cents per $100 rate (if exposure has been entered)
                    setattr(year
                            , f"{IsCat.replace(' ', '_').lower()}_ult_rate_layer_{index2}"
                            , getattr(year, f"{IsCat.replace(' ', '_').lower()}_ult_layer_{index2}") / year.exposure_onlevelled 
                                if (not year.exposure_onlevelled is None and  not getattr(year, f"{IsCat.replace(' ', '_').lower()}_ult_layer_{index2}") is None) 
                                else None
                            )

        total_tiv = hxd.schedule.schedule_total.tiv_total
            
        # exposure weight comparing onlevelled exposure of historic yoa to this year's quoted policy exposure
        year.exposure_weight = (
                                min(year.exposure_onlevelled / total_tiv, 1) 
                                if (
                                    year.include_year.selected == 1 
                                    and not total_tiv is None 
                                    and not total_tiv == 0 
                                    and not year.exposure_onlevelled is None
                                    ) else None
                                )
        # default decay factor taken from BBT to represent reduction in relevance of older years
        year.decay_weight = pow(0.9,(index-1)) if year.include_year.selected == 1 else None

        year.development_weight = year.claims_development if year.include_year.selected == 1 else None

        #overall score is product of previous weights
        year.overall_score = (
                                (year.exposure_weight or 0) 
                                * (year.decay_weight or 0) 
                                * (year.development_weight or 0) 
                                if year.include_year.selected == 1 else None)

    # variable to be used later for crediblity weighting
    years_history = 0
    # reweight overall scores to sum to 100%, this needs to be done outside the original "years" loop to make sure all years have been calculated before doing this step
    for year in er.experience_table:
        # sum of overall scores across all years
        total_overall_score = sum([year.overall_score for year in er.experience_table if not year.overall_score is None])
        # scale the overall score for the yoa in question
        year.weight_to_year = year.overall_score / (total_overall_score or 1) if year.overall_score else None
        # count how many years are included
        if year.include_year.selected:
            years_history += 1

    #lookup table has minimum of 1 year
    years_history = max(years_history, 1)

    # predefine credibiltiy weighting table
    table_cw = hx.params.credibility_weighting

    # expected loss ratio / loss rate is the sumproduct of reweighted scores and calculated loss ratios /loss rates for all included years
    for index in range(1, num_layers + 1):
        #filter is used to trigger visibilities
        setattr(getattr(er, f"summary_layer_{index}"), "filter", True if index <= num_layers else False)

        # model expected loss (non-cat)
        # commented out as removing Cat component from experience rating for now
        # layer_expected_losses = hxd.layers[index - 1].pre_uw_adjustment.expected_loss.expected_loss
        layer_expected_losses = (
            hxd.layers[index - 1].pre_uw_adjustment.expected_loss.fire
            + hxd.layers[index - 1].pre_uw_adjustment.expected_loss.us_cat.tornado_us
            + hxd.layers[index - 1].pre_uw_adjustment.expected_loss.us_cat.hail_us
            + hxd.layers[index - 1].pre_uw_adjustment.expected_loss.us_cat.flood_us
            + hxd.layers[index - 1].pre_uw_adjustment.expected_loss.us_cat.wildfire_us
            + hxd.layers[index - 1].pre_uw_adjustment.expected_loss.intl_cat.tornado_intl
            + hxd.layers[index - 1].pre_uw_adjustment.expected_loss.intl_cat.hail_intl
            + hxd.layers[index - 1].pre_uw_adjustment.expected_loss.intl_cat.flood_intl
            + hxd.layers[index - 1].pre_uw_adjustment.expected_loss.intl_cat.wildfire_intl
            ) if (
                not hxd.layers[index - 1].pre_uw_adjustment.expected_loss.fire is None
                and not hxd.layers[index - 1].pre_uw_adjustment.expected_loss.us_cat.tornado_us is None
                and not hxd.layers[index - 1].pre_uw_adjustment.expected_loss.us_cat.hail_us is None
                and not hxd.layers[index - 1].pre_uw_adjustment.expected_loss.us_cat.flood_us is None
                and not hxd.layers[index - 1].pre_uw_adjustment.expected_loss.us_cat.wildfire_us is None
                and not hxd.layers[index - 1].pre_uw_adjustment.expected_loss.intl_cat.tornado_intl is None
                and not hxd.layers[index - 1].pre_uw_adjustment.expected_loss.intl_cat.hail_intl is None
                and not hxd.layers[index - 1].pre_uw_adjustment.expected_loss.intl_cat.flood_intl is None
                and not hxd.layers[index - 1].pre_uw_adjustment.expected_loss.intl_cat.wildfire_intl is None
                ) else None
        setattr(getattr(er, f"summary_layer_{index}"), "model_non_cat_expected_losses", layer_expected_losses)

        # different outputs for non FGU claims
        if er.use_experience_rating_agg:
            # calculate experience & exposure (model) loss ratios and expected losses
            loss_ratio = sum([
                                year.weight_to_year * year.loss_ratio for year in er.experience_table 
                                if (not year.weight_to_year is None and not year.loss_ratio is None)
                                ])
            setattr(getattr(er, f"summary_layer_{index}"), "non_cat_expected_loss_ratio", loss_ratio)

            # need to make premiums net of brokerage to match expected loss calculation from the model
            layer_brokerage = hxd.layers[index - 1].brokerage
            layer_quoted_premium = hxd.layers[index - 1].achieved_premium_100_gg

            # model elr
            # commented out as removing Cat component from experience rating for now
            # layer_elr = hxd.layers[index - 1].pre_uw_adjustment.expected_loss.elr
            layer_elr = layer_expected_losses / (layer_quoted_premium * (1 - layer_brokerage)) if (
                                                                                not layer_quoted_premium is None 
                                                                                and not layer_brokerage is None
                                                                                and not layer_expected_losses is None
                                                                                ) else None
            setattr(getattr(er, f"summary_layer_{index}"), "model_non_cat_loss_ratio", layer_elr)

            # experience expected losses
            setattr(
                getattr(er, f"summary_layer_{index}")
                , "non_cat_expected_losses"
                , loss_ratio * premium_to_use * (1 - layer_brokerage) if not layer_brokerage is None else None
                )
            
            # select appropriate credibility
            # CB - 13/05/2024: We are starting by applying a 50% reduction to all credibility weights in the param table with the rollout of the experience rating. 
            # Once we are comfortable with the impact we may increase these back up to full weighting.
            cred_weight = table_cw.loc[
                total_tiv >= table_cw["tiv_threshold"]
                ][f"simple_{years_history}"].iloc[0] if not total_tiv is None else 0

            setattr(getattr(er, f"summary_layer_{index}"), "cred_weight", cred_weight)
            

        # different outputs for FGU claims
        if er.use_experience_rating_full:
            # calclate non-cat and cat loss rates based on experience
            non_cat_loss_rate = sum([
                                year.weight_to_year * getattr(year, f"non_cat_ult_rate_layer_{index}") for year in er.experience_table 
                                if (not year.weight_to_year is None and not getattr(year, f"non_cat_ult_rate_layer_{index}") is None)
                                ])
            setattr(getattr(er, f"summary_layer_{index}"), "non_cat_loss_rate", non_cat_loss_rate)
            # commented out as removing Cat component from experience rating for now
            # cat_loss_rate = sum([
            #                     year.weight_to_year * getattr(year, f"cat_ult_rate_layer_{index}") for year in er.experience_table 
            #                     if (not year.weight_to_year is None and not getattr(year, f"cat_ult_rate_layer_{index}") is None)
            #                     ])
            # setattr(getattr(er, f"summary_layer_{index}"), "cat_loss_rate", cat_loss_rate)

            # # rms loss rate calculation
            # rms_aal = hxd.layers[index - 1].risk_appetite_summary.us_all_perils_aal
            # if not total_tiv is None and not total_tiv == 0 and not rms_aal is None:
            #     # NOTE: If Cat gets re-enabled check if this rms_aal needs to be currency adjusted to slip currency in this calc
            #     rms_loss_rate = rms_aal / (total_tiv /1e6)
            # else:
            #     rms_loss_rate = None
            # setattr(getattr(er, f"summary_layer_{index}"), "rms_loss_rate", rms_loss_rate)

            # # weight between rms and experience rate for cat risks based on US/Int'l split
            # us_eq_prem = hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.earthquake_us 
            # us_ws_prem = hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.windstorm_us
            # us_cat_prem = us_eq_prem + us_ws_prem if not us_eq_prem is None and not us_ws_prem is None else None

            # intl_eq_prem = hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.earthquake_intl
            # intl_ws_prem = hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.windstorm_intl
            # intl_cat_prem = intl_eq_prem + intl_ws_prem if not intl_eq_prem is None and not intl_ws_prem is None else None
            
            # us_proportion = us_cat_prem / (us_cat_prem + intl_cat_prem) if not us_cat_prem is None and not intl_cat_prem is None else None

            # combined_loss_rate = (  non_cat_loss_rate 
            #                         + rms_loss_rate * us_proportion 
            #                         + cat_loss_rate * (1 - us_proportion)
            #                         ) if (
            #                             not rms_loss_rate is None 
            #                             and not cat_loss_rate is None 
            #                             and not us_proportion is None
            #                             ) else None
            # setattr(getattr(er, f"summary_layer_{index}")
            #         , "combined_loss_rate"
            #         , combined_loss_rate
            #         )
            combined_loss_rate = non_cat_loss_rate 

            # calculate expected loss from combined rate
            setattr(getattr(er, f"summary_layer_{index}")
                    , "non_cat_expected_losses"
                    , combined_loss_rate * total_tiv if (not total_tiv is None and not total_tiv == 0 and not combined_loss_rate is None) else None
                    )

            # select appropriate credibility
            # CB - 13/05/2024: We are starting by applying a 50% reduction to all credibility weights in the param table with the rollout of the experience rating. 
            # Once we are comfortable with the impact we may increase these back up to full weighting.
            cred_weight = table_cw.loc[
                total_tiv >= table_cw["tiv_threshold"]
                ][f"full_{years_history}"].iloc[0] if not total_tiv is None else 0
            
            
            setattr(getattr(er, f"summary_layer_{index}"), "cred_weight", cred_weight)
        
        # create non-cat ELR to non-cat premiums
        non_cat_tech_prem = (
            hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.fire
            + hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.tornado_us
            + hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.hail_us
            + hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.flood_us
            + hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.wildfire_us
            + hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.tornado_intl
            + hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.hail_intl
            + hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.flood_intl
            + hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.wildfire_intl
            ) if (
                not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.fire is None
                and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.tornado_us is None
                and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.hail_us is None
                and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.flood_us is None
                and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.us_cat.wildfire_us is None
                and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.tornado_intl is None
                and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.hail_intl is None
                and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.flood_intl is None
                and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.intl_cat.wildfire_intl is None
                ) else None

        non_cat_prem_proportion = non_cat_tech_prem / hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.gross_tech_prem_total if (
            not non_cat_tech_prem is None
            and not non_cat_tech_prem == 0
            and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.gross_tech_prem_total is None
            and not hxd.layers[index - 1].pre_uw_adjustment.gross_tech_prem.gross_tech_prem_total == 0
        ) else None


        layer_brokerage = hxd.layers[index - 1].brokerage

        non_cat_elr_non_cat_prem = getattr(er, f"summary_layer_{index}").non_cat_expected_losses / (premium_to_use * (1 - layer_brokerage) * non_cat_prem_proportion) if (
            not getattr(er, f"summary_layer_{index}").non_cat_expected_losses is None
            and not premium_to_use == 0
            and not layer_brokerage is None            
            and not layer_brokerage == 1
            and not non_cat_prem_proportion is None
            and not non_cat_prem_proportion == 0
        ) else None

        setattr(getattr(er, f"summary_layer_{index}"), "non_cat_elr_non_cat_prem", non_cat_elr_non_cat_prem)

        # credibiltiy weighting for experience adjustment
        # calculate experience adjustment
        experience_losses = getattr(er, f"summary_layer_{index}").non_cat_expected_losses
        model_losses = getattr(er, f"summary_layer_{index}").model_non_cat_expected_losses
        # apply cred weighting between experience and model
        experience_adj = max(
            ((experience_losses * cred_weight) + (model_losses * (1 - cred_weight))) / model_losses - 1
            , -0.5
            ) if (not model_losses is None) and (not experience_losses is None) else None
        
        if not experience_adj is None:
            if not np.isnan(experience_adj) and not np.isinf(experience_adj):
                setattr(
                    getattr(er, f"summary_layer_{index}")
                    , "experience_adjustment"
                    , experience_adj
                    )