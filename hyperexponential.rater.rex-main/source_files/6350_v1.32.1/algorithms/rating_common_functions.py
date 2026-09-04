import hx
import polars as pl


def ground_up_rate(hxd, df, other_data, layer, index, peril_name):

    # Ground Up Rate
    df = df.with_columns(
        [
            (pl.col(f'{peril_name}_buildings_total_adjustment') * pl.col(f'{peril_name}_buildings_base_rate_layer{index}'))
                .alias(f'{peril_name}_buildings_ground_up_rate_layer{index}'),
            (pl.col(f'{peril_name}_contents_total_adjustment') * pl.col(f'{peril_name}_contents_base_rate_layer{index}'))
                .alias(f'{peril_name}_contents_ground_up_rate_layer{index}'),
            (pl.col(f'{peril_name}_bi_total_adjustment') * pl.col(f'{peril_name}_bi_base_rate_layer{index}'))
                .alias(f'{peril_name}_bi_ground_up_rate_layer{index}')
        ]
    )

    return df


def ground_up_uw_rate(hxd, df, other_data, layer, index, peril_name, adj_name):

    # Ground Up Rate (UW Adjustment)
    # CB added 26/03/24 experience rating calculated by layer adjustment
    if peril_name in ["earthquake_us", "windstorm_us"]: #NOTE UW Adjustments only applicable to Intl EQ and Intl WS - NOT US
        df = df.with_columns(
            [
                (pl.col(f'{peril_name}_buildings_ground_up_rate_layer{index}') * (1 + other_data[f'{adj_name}_experience_rating_adj_layer{index}']))
                    .alias(f'{peril_name}_buildings_ground_up_uw_rate_layer{index}'),
                (pl.col(f'{peril_name}_contents_ground_up_rate_layer{index}') * (1 + other_data[f'{adj_name}_experience_rating_adj_layer{index}']))
                    .alias(f'{peril_name}_contents_ground_up_uw_rate_layer{index}'),
                (pl.col(f'{peril_name}_bi_ground_up_rate_layer{index}') * (1 + other_data[f'{adj_name}_experience_rating_adj_layer{index}']))
                    .alias(f'{peril_name}_bi_ground_up_uw_rate_layer{index}'),
            ]
        )
    else: 
        df = df.with_columns(
            [
                (pl.col(f'{peril_name}_buildings_ground_up_rate_layer{index}') * (1 + other_data[f'{adj_name}_uw_adjustments'] + other_data[f'{adj_name}_experience_rating_adj_layer{index}']))
                    .alias(f'{peril_name}_buildings_ground_up_uw_rate_layer{index}'),
                (pl.col(f'{peril_name}_contents_ground_up_rate_layer{index}') * (1 + other_data[f'{adj_name}_uw_adjustments'] + other_data[f'{adj_name}_experience_rating_adj_layer{index}']))
                    .alias(f'{peril_name}_contents_ground_up_uw_rate_layer{index}'),
                (pl.col(f'{peril_name}_bi_ground_up_rate_layer{index}') * (1 + other_data[f'{adj_name}_uw_adjustments'] + other_data[f'{adj_name}_experience_rating_adj_layer{index}']))
                    .alias(f'{peril_name}_bi_ground_up_uw_rate_layer{index}'),
            ]
        )

    return df

def loss_curve_lookup(hxd, df, curve_df, target_column, alias):
    default_loss_curves_df = hx.params.default_loss_curve_selection

    id_col = curve_df.columns[0]
    curve_pl = pl.from_pandas(curve_df.melt(id_vars=id_col)).rename({id_col: 'constr_code', 'variable': 'tiv_cutoff', 'value': 'exposure_curve'})
    curve_pl = curve_pl.with_columns(
        pl.col('tiv_cutoff').cast(pl.Float64),
        pl.col('constr_code').cast(pl.Int64),
        pl.col('tiv_cutoff').cast(pl.Float64).alias(target_column),
        )
    loss_curve_tiv_bands_pl = curve_pl[['tiv_cutoff', target_column]].unique().sort(by='tiv_cutoff')

    df = df.with_columns(
        pl.col(target_column).fill_null(-1).cast(pl.Float64)
    )
    df = df.sort(target_column)
    df = df.join_asof(loss_curve_tiv_bands_pl[['tiv_cutoff', target_column]], on=target_column, strategy="backward")

    if id_col == "Fire":
        df = df.with_columns(
            pl.when(pl.col("constr_code") == 0).then(pl.col("base_constr_code")).otherwise(pl.col("constr_code")).alias("constr_code_temp")
        )
        df = df.join(curve_pl[['constr_code', 'tiv_cutoff', 'exposure_curve']], left_on=['tiv_cutoff', 'constr_code_temp'], right_on=['tiv_cutoff', 'constr_code'], how="left")
        df = df.drop("constr_code_temp")
    else:
        df = df.join(curve_pl[['constr_code', 'tiv_cutoff', 'exposure_curve']], on=['tiv_cutoff', 'constr_code'], how='left')

    df = df.with_columns(
        pl.col('exposure_curve').fill_null(default_loss_curves_df.set_index("Peril").loc[id_col, "Curve"])
    ).rename({'exposure_curve': alias})

    df = df.drop("tiv_cutoff")
    df = df.sort("row_nr")

    return df


def peril_covered_layer(hxd, df, index, layer, peril, peril_node_name):

    include = getattr(layer.perils, peril_node_name).include
    
    df = df.with_columns(
        pl.when(pl.col(f"{peril}_covered") == "From Layer")
            .then(include)
            .when(pl.col(f"{peril}_covered") == "True")
            .then(True)
            .when(pl.col(f"{peril}_covered") == "False")
            .then(False)
            .otherwise(None)
            .alias(f"{peril}_covered_rating_layer{index}")
    )

    return df


def granularity_option_structure(hxd, df, other_data, layer, index, peril_abbr, peril_struct_name, option_granularity_lookup_df):
    '''
    Calculate the granularity in option structure 
    Parameters:
        - peril_abbr: peril abbreviation
        - peril_struct_name: name pointing to the structure of the peril
        - option_granularity_lookup_df: dataframe that looks up the granularity score
    '''

    ### Granularity Structure
    num_options = getattr(hxd.non_layer_perils, peril_struct_name).num_options or 0

    ### Get Tier Mapping, decide which granularity are applicable to locations
    if peril_abbr in ["ws", "eq", "scs"]:
        if peril_abbr == "ws":
            column_list = ["FL", "FL Tri County and Keys Only", "FL Tri County Only", "Tier 1: FL",
                        "Tier 1: NorthEast", "Tier 1: TX - ME", "Tier 1: TX - NC (Exc Harris)",
                        "Tier 1: TX - NC (Inc Harris)", "Tier 1: TX - VA (Exc Harris)",
                        "Tier 1: TX - VA (Inc Harris)", "Tier 2: FL", "Tier 2: TX - VA"]
        elif peril_abbr == "eq":
            column_list = ["CA A and B", "CA All Other", "South East", "Great Basin", 
                        "NM", "PNW Counties", "PNW"] 
        elif peril_abbr == "scs":
            column_list = ["CO, KS, MO, NE, OK, SD, TX", 
                        "AR, IA, IL, IN, MN, MT, ND, SD, WY",
                        "AR, CO, IA, IL, IN, KS, MN, MO, MT, ND, NE, OK, SD, TX, WY"]
        
        tiers_df = hx.params.tiers_covered[["StateCounty"] + column_list]
        tiers_pl = pl.from_pandas(tiers_df)

        granularity_pl = df[["state_county_lowercase", "state", "country"]]
    
        for option_num in range(1, num_options + 1):
            option_structure = getattr(getattr(layer.perils, peril_struct_name).location_ded, f"option_{option_num}")
            if option_structure.region_dropdown.tier == "":
                granularity_pl = granularity_pl.with_columns(
                    pl.lit(0).alias(f"{peril_abbr}_tier_mapping_layer{index}_option{option_num}")
                )
            else:
                option_tiers_pl = tiers_pl[["StateCounty"] + [option_structure.region_dropdown.tier]]
                option_tiers_pl = option_tiers_pl.rename({"StateCounty": "state_county", option_structure.region_dropdown.tier: "tier_mapping"})

                option_tiers_pl = option_tiers_pl.with_columns(
                    pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
                ).drop("state_county")

                option_tiers_pl = granularity_pl.join(option_tiers_pl, on="state_county_lowercase", how="left")
                granularity_pl = granularity_pl.with_columns(
                    option_tiers_pl.select(
                        pl.col("tier_mapping")
                            .fill_null(0)
                            .alias(f"{peril_abbr}_tier_mapping_layer{index}_option{option_num}")
                    )
                )
        
    elif peril_abbr == "fl":
        
        granularity_pl = df[["floodzone", "state", "country"]]
        tiers_pl = pl.from_pandas(hx.params.fl_tiers)

        for option_num in range(1, num_options + 1):
            option_structure = getattr(getattr(layer.perils, peril_struct_name).location_ded, f"option_{option_num}")
            if option_structure.region_dropdown.fema_zone == "":
                granularity_pl = granularity_pl.with_columns(
                    pl.lit(0).alias(f"{peril_abbr}_tier_mapping_layer{index}_option{option_num}")
                )
            else:
                option_tiers_pl = tiers_pl[["Zone"] + [option_structure.region_dropdown.fema_zone]]
                option_tiers_pl = option_tiers_pl.rename({"Zone": "floodzone", option_structure.region_dropdown.fema_zone: "tier_mapping"})
                option_tiers_pl = granularity_pl.join(option_tiers_pl, on="floodzone", how="left")
                granularity_pl = granularity_pl.with_columns(
                    option_tiers_pl.select(
                        pl.col("tier_mapping")
                            .fill_null(0)
                            .alias(f"{peril_abbr}_tier_mapping_layer{index}_option{option_num}")
                    )
                )


    for option_num in range(1, num_options + 1):
        option_structure = getattr(getattr(layer.perils, peril_struct_name).location_ded, f"option_{option_num}")

        option_granularity = 0

        if option_structure.region_dropdown.region == "All":
            option_granularity = 1
        elif option_structure.region_dropdown.region == "State":
            option_granularity = 100
        elif option_structure.region_dropdown.region == "Tier":
            if option_structure.region_dropdown.tier == "":
                option_granularity = 0
            else:
                option_granularity = option_granularity_lookup_df[option_granularity_lookup_df["Tier"] == option_structure.region_dropdown.tier]["Rank"].iloc[0]
        elif option_structure.region_dropdown.region == "FEMA Zone":
            if option_structure.region_dropdown.fema_zone == "":
                option_granularity = 0
            else:
                option_granularity = option_granularity_lookup_df[option_granularity_lookup_df["Tier"] == option_structure.region_dropdown.fema_zone]["Rank"].iloc[0]

        if option_num > (num_options or 0):
            granularity_pl = granularity_pl.with_columns(
                pl.lit(0).alias(f"{peril_abbr}_granularity_layer{index}_option{option_num}")
            )
        else:
            granularity_pl = granularity_pl.with_columns(
                pl.when((option_structure.region_dropdown.region == "All") | 
                        (option_structure.region_dropdown.state == pl.col("state")) |
                        (pl.col(f"{peril_abbr}_tier_mapping_layer{index}_option{option_num}") == 1)
                    )
                    .then(pl.lit(option_granularity))
                    .otherwise(0)
                    .alias(f"{peril_abbr}_granularity_layer{index}_option{option_num}")
            )

    # Getting the max granularity score
    if num_options > 0:
        granularity_pl = granularity_pl.with_columns(
            pl.max(*[f"{peril_abbr}_granularity_layer{index}_option{option_num}" for option_num in range(1, num_options + 1)]).alias(f"{peril_abbr}_max_granularity_layer{index}")
        )

    # Decide which column has the max score
    if num_options > 1:
        granularity_pl = granularity_pl.with_columns(
            pl.when(pl.col(f"{peril_abbr}_max_granularity_layer{index}") == pl.col(f"{peril_abbr}_granularity_layer{index}_option1"))
                .then(pl.lit(1))
                .when(pl.col(f"{peril_abbr}_max_granularity_layer{index}") == pl.col(f"{peril_abbr}_granularity_layer{index}_option2"))
                .then(pl.lit(2))
                .otherwise(pl.lit(3))
                .alias(f"{peril_abbr}_selected_option_layer{index}")
        )
    elif num_options == 1:
        granularity_pl = granularity_pl.with_columns(
            pl.lit(1).alias(f"{peril_abbr}_selected_option_layer{index}")
        )
    

    return df, granularity_pl


def deductible_option_structure(hxd, df, other_data, layer, index, granularity_pl, peril_abbr, peril_struct_name, us_percentage_tiv, us_ded_location):
    '''
    Calculate deductible for option structure
    Parameters:
        - peril_abbr: peril abbreviation
        - peril_struct_name: name pointing to the structure of the peril
        - granularity_pl: result from granularity score function
        - us_percentage_tiv: polars column that aggregates region tiv
        - us_ded_location: polars column that aggregates region count
    '''
    deductible_pl = granularity_pl.with_columns(df.select(us_percentage_tiv, us_ded_location))
    deductible_pl = deductible_pl.with_columns(df.select(pl.col("tiv_region"), pl.col("count_region")))
    
    num_options = getattr(hxd.non_layer_perils, peril_struct_name).num_options or 0
    exchange_rate = hxd.policy_information.exchange_rate

    df = df.with_columns(pl.lit(0).alias(f"{peril_abbr}_deductible_option_assigned_layer{index}"))
    for option_num in range(1, num_options + 1):
        
        option_structure = getattr(getattr(layer.perils, peril_struct_name).location_ded, f"option_{option_num}")
        location_min_max_usd = (option_structure.location_min_max or 0) / exchange_rate if exchange_rate else (option_structure.location_min_max or 0)

        # Percentage deductble
        percentage_expr = (option_structure.percent or 0) * \
                            (pl.when(pl.col("country") == "United States")
                                .then(us_percentage_tiv)
                                .otherwise(pl.col("tiv_region")))

        # Fixed amount deductible
        deductible_expr = (location_min_max_usd or 0)

        if option_structure.type == "Percentage with a $ minimum":
            deductible_expr = pl.max(percentage_expr, deductible_expr)
        elif option_structure.type == "Fixed $ amount":
            deductible_expr = deductible_expr
        elif option_structure.type == "Percentage uncapped":
            deductible_expr = percentage_expr
        elif option_structure.type == "Percentage capped by $ amount":
            deductible_expr = pl.min(percentage_expr, deductible_expr)
        else:
            deductible_expr = pl.lit(0)

        if option_num > (num_options or 0):
            deductible_pl = deductible_pl.with_columns(
                pl.lit(0).alias(f"{peril_abbr}_deductible_layer{index}_option{option_num}")
            )
        else:
            deductible_pl = deductible_pl.with_columns(
                pl.when((option_structure.region_dropdown.region == "All") | 
                        ((option_structure.region_dropdown.state == pl.col("state")) & (pl.col("state") != "")) |
                        (pl.col(f"{peril_abbr}_tier_mapping_layer{index}_option{option_num}") == 1)
                    )
                    .then(deductible_expr)
                    .otherwise(0)
                    .alias(f"{peril_abbr}_deductible_layer{index}_option{option_num}"))

        # FS Addition: This checks what options were assigned to each location. Options 3 is prioritised over option 2 and option 2 is prioritised over option 1.
        df = df.with_columns(deductible_pl.select(f"{peril_abbr}_deductible_layer{index}_option{option_num}"))
        df = df.with_columns(pl.when((pl.col(f"{peril_abbr}_deductible_layer{index}_option{option_num}") > 0) & (pl.col(f"{peril_abbr}_deductible_option_assigned_layer{index}") < option_num))
            .then(pl.lit(option_num))
            .otherwise(pl.col(f"{peril_abbr}_deductible_option_assigned_layer{index}"))
            .alias(f"{peril_abbr}_deductible_option_assigned_layer{index}"))
    
    per_occurrence_ded = getattr(layer.perils, peril_struct_name).per_occurrence_ded
    per_occurrence_ded_usd = (per_occurrence_ded or 0) / exchange_rate if exchange_rate else (per_occurrence_ded or 0)

    if num_options > 0:        
        ded_option_cols = [f"{peril_abbr}_deductible_layer{index}_option{option_num}" for option_num in range(1, num_options + 1)]
        max_ded = pl.fold(
            acc=pl.col(ded_option_cols[0]), 
            function=lambda acc, x: pl.when(acc > x).then(acc).otherwise(x), 
            exprs=[pl.col(c) for c in ded_option_cols[1:]])

        deductible_pl = deductible_pl.with_columns(
            pl.when((max_ded == 0) | (max_ded.is_null()))
            .then(pl.lit(per_occurrence_ded_usd))
            .otherwise(max_ded)
            .alias(f"{peril_abbr}_deductible_layer{index}")
        )
    else:
        deductible_pl = deductible_pl.with_columns(
            pl.lit(per_occurrence_ded_usd).alias(f"{peril_abbr}_deductible_layer{index}")
        )

    # merge deductible to df
    df = df.with_columns(deductible_pl.select(f"{peril_abbr}_deductible_layer{index}"))
    df = df.with_columns(
            deductible_pl.select(
                pl.col(f"{peril_abbr}_deductible_layer{index}")
                    .alias(f"{peril_abbr}_deductible_selected_layer{index}"))
            )

    
    if f"{peril_abbr}_deductible_layer{index}_option1" in deductible_pl.columns:
        df = df.with_columns(deductible_pl.select(f"{peril_abbr}_deductible_layer{index}_option1"))

    del deductible_pl

    return df


def sublimit_option_structure(hxd, df, other_data, layer, index, granularity_pl, peril_abbr, peril_struct_name):
    '''
    Calculate sublimit for option structures
    Parameters:
        - peril_abbr: peril abbreviation
        - peril_struct_name: name pointing to the structure of the peril
        - granularity_pl: result from granularity score function
    '''

    sublimit_pl = granularity_pl
    num_options = getattr(hxd.non_layer_perils, peril_struct_name).num_options or 0
    exchange_rate = hxd.policy_information.exchange_rate

    for option_num in range(1, num_options + 1):
        option_structure = getattr(getattr(layer.perils, peril_struct_name).location_ded, f"option_{option_num}")
        sublimit_usd = (option_structure.sublimit or 0) / exchange_rate if exchange_rate else (option_structure.sublimit or 0)

        if option_num > (num_options or 0):
            sublimit_pl = sublimit_pl.with_columns(
                pl.lit(0).alias(f"{peril_abbr}_sublimit_layer{index}_option{option_num}")
            )
        else:
            # Decide to use option sublimit or not
            sublimit_pl = sublimit_pl.with_columns(
                pl.when((option_structure.region_dropdown.region == "All") | 
                        (option_structure.region_dropdown.state == pl.col("state")) |
                        (pl.col(f"{peril_abbr}_tier_mapping_layer{index}_option{option_num}") == 1)
                    )
                    .then(option_structure.sublimit / exchange_rate if (exchange_rate and option_structure.sublimit) else (option_structure.sublimit or 0))
                    .otherwise(0)
                    .fill_null(0)
                    .alias(f"{peril_abbr}_sublimit_layer{index}_option{option_num}")
            )

    # Decide which sublimit layer to use given the option selected based on granularity
    if num_options == 3:
        df = df.with_columns(
            sublimit_pl.select(
                pl.when(pl.col(f"{peril_abbr}_selected_option_layer{index}") == 1)
                    .then(pl.col(f"{peril_abbr}_sublimit_layer{index}_option1"))
                    .when(pl.col(f"{peril_abbr}_selected_option_layer{index}") == 2)
                    .then(pl.col(f"{peril_abbr}_sublimit_layer{index}_option2"))
                    .otherwise(pl.col(f"{peril_abbr}_sublimit_layer{index}_option3"))
                    .alias(f"{peril_abbr}_selected_sublimit_layer{index}")
            )
        )
    elif num_options == 2:
        df = df.with_columns(
            sublimit_pl.select(
                pl.when(pl.col(f"{peril_abbr}_selected_option_layer{index}") == 1)
                    .then(pl.col(f"{peril_abbr}_sublimit_layer{index}_option1"))
                    .otherwise(pl.col(f"{peril_abbr}_sublimit_layer{index}_option2"))
                    .alias(f"{peril_abbr}_selected_sublimit_layer{index}")
            )
        )
    elif num_options == 1:
        df = df.with_columns(
            sublimit_pl.select(
                pl.col(f"{peril_abbr}_sublimit_layer{index}_option1").alias(f"{peril_abbr}_selected_sublimit_layer{index}")
            )
        )
    else:
        df = df.with_columns(
            sublimit_pl.select(
                pl.lit(0).alias(f"{peril_abbr}_selected_sublimit_layer{index}")
            )
        )

    del granularity_pl

    return df


def percent_worth(hxd, df, other_data, layer, index, peril):
    '''
    Calculate exit - entry percentage worth layer
    '''

    # Calculate % worth
    df = df.with_columns(
        (pl.col(f"{peril}_exit_perc_layer{index}") - pl.col(f"{peril}_entry_perc_layer{index}")).alias(f"{peril}_worth_percent_layer{index}")
    )

    return df


def expected_loss(hxd, df, other_data, layer, index, peril):
    '''
    Calculate expected loss given entry/exit perc
    '''

    # Calculate the expected loss pre UW adjustment
    df = df.with_columns(
        [
            (pl.col("tiv_buildings_usd") * pl.col(f"{peril}_buildings_ground_up_rate_layer{index}") * pl.col(f"{peril}_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"{peril}_buildings_expected_loss_pre_uw_layer{index}"),
            (pl.col("tiv_contents_total_usd") * pl.col(f"{peril}_contents_ground_up_rate_layer{index}") * pl.col(f"{peril}_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"{peril}_contents_expected_loss_pre_uw_layer{index}"),
            (pl.col("tiv_bi_usd") * pl.col(f"{peril}_bi_ground_up_rate_layer{index}") * pl.col(f"{peril}_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"{peril}_bi_expected_loss_pre_uw_layer{index}"),
            (pl.col("tiv_buildings_usd") * pl.col(f"{peril}_buildings_ground_up_uw_rate_layer{index}") * pl.col(f"{peril}_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"{peril}_buildings_expected_loss_post_uw_layer{index}"),
            (pl.col("tiv_contents_total_usd") * pl.col(f"{peril}_contents_ground_up_uw_rate_layer{index}") * pl.col(f"{peril}_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"{peril}_contents_expected_loss_post_uw_layer{index}"),
            (pl.col("tiv_bi_usd") * pl.col(f"{peril}_bi_ground_up_uw_rate_layer{index}") * pl.col(f"{peril}_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"{peril}_bi_expected_loss_post_uw_layer{index}"),
        ]
    )

    df = df.with_columns(
        [
            (pl.col(f"{peril}_buildings_expected_loss_pre_uw_layer{index}") + pl.col(f"{peril}_contents_expected_loss_pre_uw_layer{index}") + pl.col(f"{peril}_bi_expected_loss_pre_uw_layer{index}"))
                .alias(f"{peril}_total_expected_loss_pre_uw_layer{index}"),
            (pl.col(f"{peril}_buildings_expected_loss_post_uw_layer{index}") + pl.col(f"{peril}_contents_expected_loss_post_uw_layer{index}") + pl.col(f"{peril}_bi_expected_loss_post_uw_layer{index}"))
                .alias(f"{peril}_total_expected_loss_post_uw_layer{index}")
        ]
    )

    return df

