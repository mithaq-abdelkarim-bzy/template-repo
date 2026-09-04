import hx
import polars as pl

def earthquake_analysis_summary(hxd, df, other_data):

    for index, layer in enumerate(hxd.layers, start=1):
        sum_prod_df = earthquake_modifier_summary(hxd, df, other_data, layer, index)
        earthquake_risk_factors_summary(hxd, sum_prod_df, other_data, layer, index)
        earthquake_top_20_locations_summary(hxd, sum_prod_df, other_data, layer, index)
    
    return df


def earthquake_modifier_summary(hxd, df, other_data, layer, index):

    # Cache after each cumulative product of risk factor
    sum_cache = {}

    modifier_summary_dict = {}
    # Assign to Fire Modifier Summary
    modifier_summary_dict["peril_name"] = "Earthquake"
    modifier_summary_dict["no_of_locs"] = len(df)
    modifier_summary_dict["sum_tiv_total_usd"] = other_data["total_tiv_total_usd"]

    # Calculate the sum product per layer
    # Select a subset of fields to optimise sorting
    sum_prod_df = df[["country", "state", "county", "zip",
                        "tiv_buildings", "tiv_contents_total", "tiv_bi", "tiv_total",
                        "occupancy", "tiv_buildings_usd", "tiv_contents_total_usd", "tiv_bi_usd", "tiv_total_usd",
                        "eq_occupancy_factor", "eq_construction_factor", "eq_year_built_factor", "eq_num_floors_factor", "eq_zone",
                        "eq_construction_quality_factor", "eq_plan_irregularity_factor", "eq_soft_story_factor", "eq_vertical_irregularity_factor",
                        "eq_ornamentation_factor", "eq_equipment_bracing_factor", "eq_equipment_maintenance_factor", "eq_pounding_factor", "eq_catnet_intl_factor",
                        "cresta_zone", "risk_level_eq", "constr_name", "floor_area",
                        f"earthquake_us_buildings_base_rate_layer{index}", f"earthquake_intl_buildings_base_rate_layer{index}",
                        f"earthquake_us_contents_base_rate_layer{index}", f"earthquake_intl_contents_base_rate_layer{index}",
                        f"earthquake_us_bi_base_rate_layer{index}", f"earthquake_intl_bi_base_rate_layer{index}",
                        f"earthquake_us_gg_technical_prem_final_pre_uw_layer{index}",
                        f"earthquake_intl_gg_technical_prem_final_pre_uw_layer{index}",
                        f"earthquake_us_gg_technical_prem_final_post_uw_layer{index}",
                        f"earthquake_intl_gg_technical_prem_final_post_uw_layer{index}",
                        f"earthquake_us_total_expected_loss_pre_uw_layer{index}", f"earthquake_us_total_expected_loss_post_uw_layer{index}",
                        f"earthquake_intl_total_expected_loss_pre_uw_layer{index}", f"earthquake_intl_total_expected_loss_post_uw_layer{index}",
                        f"earthquake_us_worth_percent_layer{index}", f"earthquake_intl_worth_percent_layer{index}"
                    ]]

    sum_prod_df = sum_prod_df.with_columns(
        [
            (pl.col("tiv_buildings_usd") * 
                (
                    # pl.when(pl.col("country").is_in(["United States", "Canada"]))
                    # .then(pl.col(f"earthquake_us_buildings_base_rate_layer{index}"))
                    # .otherwise(pl.col(f"earthquake_intl_buildings_base_rate_layer{index}"))
                    pl.col(f"earthquake_us_buildings_base_rate_layer{index}") + pl.col(f"earthquake_intl_buildings_base_rate_layer{index}")
                )
            ).alias("buildings_cumprod"),
            (pl.col("tiv_contents_total_usd") *
                (
                    # pl.when(pl.col("country").is_in(["United States", "Canada"]))
                    # .then(pl.col(f"earthquake_us_contents_base_rate_layer{index}"))
                    # .otherwise(pl.col(f"earthquake_intl_contents_base_rate_layer{index}"))
                    pl.col(f"earthquake_us_contents_base_rate_layer{index}") + pl.col(f"earthquake_intl_contents_base_rate_layer{index}")
                )
            ).alias("contents_total_cumprod"),
            (pl.col("tiv_bi_usd") * 
                (
                    # pl.when(pl.col("country").is_in(["United States", "Canada"]))
                    # .then(pl.col(f"earthquake_us_bi_base_rate_layer{index}"))
                    # .otherwise(pl.col(f"earthquake_intl_bi_base_rate_layer{index}"))
                    pl.col(f"earthquake_us_bi_base_rate_layer{index}") + pl.col(f"earthquake_intl_bi_base_rate_layer{index}")
                )
            ).alias("bi_cumprod"),
            (
                # pl.when(pl.col("country") == "United States")
                # .then(pl.col(f"earthquake_us_worth_percent_layer{index}"))
                # .otherwise(pl.col(f"earthquake_intl_worth_percent_layer{index}"))
                pl.col(f"earthquake_us_worth_percent_layer{index}") + pl.col(f"earthquake_intl_worth_percent_layer{index}")
            ).alias(f"earthquake_worth_percent_layer{index}")
        ]
    )

    sum_cache["base_sum"] = (sum_prod_df["buildings_cumprod"].sum() or 0) + (sum_prod_df["contents_total_cumprod"].sum() or 0) + (sum_prod_df["bi_cumprod"].sum() or 0)

    total_modifier_impact = 1

    rating_factors = ["occupancy", "construction", "year_built", "num_of_floors", "construction_quality", "plan_irregularity",
                "soft_story", "vertical_irregularity", "ornamentation", "equipment_bracing", "equipment_maintenance", "pounding", "catnet_score"]
    
    multipliers = [
                pl.col("eq_occupancy_factor"), pl.col("eq_construction_factor"), pl.col("eq_year_built_factor"), pl.col("eq_num_floors_factor"),
                pl.col("eq_construction_quality_factor"), pl.col("eq_plan_irregularity_factor"), pl.col("eq_soft_story_factor"), pl.col("eq_vertical_irregularity_factor"),
                pl.col("eq_ornamentation_factor"), pl.col("eq_equipment_bracing_factor"), pl.col("eq_equipment_maintenance_factor"), pl.col("eq_pounding_factor"),
                pl.col("eq_catnet_intl_factor")
        ]
    
    for idx, (factor, multiplier_col) in enumerate(zip(rating_factors, multipliers)):

        column_prefix = "" if idx == 0 else f"{rating_factors[idx-1]}_"

        sum_prod_df = sum_prod_df.with_columns(
            [
                (pl.col(f"{column_prefix}buildings_cumprod") * multiplier_col).alias(f"{factor}_buildings_cumprod"),
                (pl.col(f"{column_prefix}contents_total_cumprod") * multiplier_col).alias(f"{factor}_contents_total_cumprod"),
                (pl.col(f"{column_prefix}bi_cumprod") * multiplier_col).alias(f"{factor}_bi_cumprod")
            ]
        )

        sum_cache[f"{factor}_sum"] = (sum_prod_df[f"{factor}_buildings_cumprod"].sum() or 0) + (sum_prod_df[f"{factor}_contents_total_cumprod"].sum() or 0) + \
                                        (sum_prod_df[f"{factor}_bi_cumprod"].sum() or 0)
        
        if idx == 0:
            modifier_impact = sum_cache[f"{factor}_sum"] / sum_cache["base_sum"] if sum_cache["base_sum"] else 0    
        else:
            modifier_impact = sum_cache[f"{factor}_sum"] / sum_cache[f"{rating_factors[idx-1]}_sum"] if sum_cache[f"{rating_factors[idx-1]}_sum"] else 0

        modifier_summary_dict[factor] = modifier_impact
        total_modifier_impact *= modifier_impact

    modifier_summary_dict["total_modifier_impact"] = total_modifier_impact

    # GU Tech Rate, Tech Rate, UW Tech Rate, UW Tech Prem
    earthquake_gg_technical_prem_final_pre_uw = ((df[f"earthquake_us_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0) + 
                                                    (df[f"earthquake_intl_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0))

    earthquake_gg_technical_prem_final_post_uw = ((df[f"earthquake_us_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0) + 
                                                    (df[f"earthquake_intl_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0))

    earthquake_total_expected_loss_pre_uw_sum = (df[f"earthquake_us_total_expected_loss_pre_uw_layer{index}"].sum() or 0) + (df[f"earthquake_intl_total_expected_loss_pre_uw_layer{index}"].sum() or 0)

    modifier_summary_dict["gu_tech_rate"] = ((sum_cache["base_sum"] / other_data["sum_tiv_total_usd"]) * modifier_summary_dict["total_modifier_impact"] * earthquake_gg_technical_prem_final_pre_uw / earthquake_total_expected_loss_pre_uw_sum
                                        if earthquake_total_expected_loss_pre_uw_sum and other_data["sum_tiv_total_usd"] else 0)
    
    modifier_summary_dict["tech_rate"] = earthquake_gg_technical_prem_final_pre_uw / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0

    # To be confirmed: worth change to weighted average on total_tiv
    # modifier_summary_dict["worth"] = modifier_summary_dict["tech_rate"] / modifier_summary_dict["gu_tech_rate"] if modifier_summary_dict["gu_tech_rate"] else 0
    cum_prod_worth = df.select(pl.col(f"earthquake_worth_percent_layer{index}") * pl.col("tiv_total_usd"))[f"earthquake_worth_percent_layer{index}"].sum()
    modifier_summary_dict["worth"] = cum_prod_worth / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0 

    modifier_summary_dict["uw_adj_tech_rate"] = earthquake_gg_technical_prem_final_post_uw / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0
    modifier_summary_dict["uw_adj_tech_prem"] = earthquake_gg_technical_prem_final_post_uw

    other_data[f"eq_modifier_summary_layer{index}"] = modifier_summary_dict

    return sum_prod_df


def earthquake_risk_factors_summary(hxd, sum_prod_df, other_data, layer, index):

    occupancy_summary_list = []
    constr_summary_list = []
    risk_level_eq_summary_list = []
    cresta_summary_list = []
    eq_zone_summary_list = []

    for column_name, target_list in zip(
                    ("cresta_zone", "risk_level_eq", "occupancy", "constr_name", "eq_zone"), 
                    (cresta_summary_list, risk_level_eq_summary_list, occupancy_summary_list, constr_summary_list, eq_zone_summary_list)):

        for name, data in sum_prod_df.groupby(column_name):

            prod_sum_base = (data["buildings_cumprod"].sum() or 0) + (data["contents_total_cumprod"].sum() or 0) + (data["bi_cumprod"].sum() or 0)
            prod_sum_last = (data["catnet_score_buildings_cumprod"].sum() or 0) + (data["catnet_score_contents_total_cumprod"].sum() or 0) + \
                                            (data["catnet_score_bi_cumprod"].sum() or 0)

            total_tiv_usd = data["tiv_total_usd"].sum() or 0
            sum_total_tiv = data["tiv_total"].sum() or 0
            sum_tiv_buildings = data["tiv_buildings"].sum() or 0
            base_rate = prod_sum_base / total_tiv_usd if total_tiv_usd else 0
            total_modifier_impact = prod_sum_last / prod_sum_base if prod_sum_base else 0

            earthquake_gg_technical_prem_final_pre_uw = ((data[f"earthquake_us_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0) + 
                                                (data[f"earthquake_intl_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0))

            earthquake_gg_technical_prem_final_post_uw = ((data[f"earthquake_us_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0) + 
                                                            (data[f"earthquake_intl_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0))

            earthquake_total_expected_loss_pre_uw_sum = (data[f"earthquake_us_total_expected_loss_pre_uw_layer{index}"].sum() or 0) + (data[f"earthquake_intl_total_expected_loss_pre_uw_layer{index}"].sum() or 0)
            
            # total_floor_area = data['floor_area'].fill_null(0).sum() or 0

            total_floor_area = data.filter(pl.col("tiv_buildings") != 0)['floor_area'].fill_null(0).sum() or 0

            gu_tech_rate = base_rate * total_modifier_impact * earthquake_gg_technical_prem_final_pre_uw / earthquake_total_expected_loss_pre_uw_sum if earthquake_total_expected_loss_pre_uw_sum else 0
            tech_rate = earthquake_gg_technical_prem_final_pre_uw / total_tiv_usd if total_tiv_usd else 0
            tech_prem = earthquake_gg_technical_prem_final_pre_uw

            # To be confirmed: worth change to weighted average on total_tiv
            # worth = tech_rate / gu_tech_rate if gu_tech_rate else 0
            cum_prod_worth = data.select(pl.col(f"earthquake_worth_percent_layer{index}") * pl.col("tiv_total_usd"))[f"earthquake_worth_percent_layer{index}"].sum() or 0
            worth = cum_prod_worth / total_tiv_usd if total_tiv_usd else 0

            uw_adj_tech_rate = earthquake_gg_technical_prem_final_post_uw / total_tiv_usd if total_tiv_usd else 0
            uw_adj_tech_prem = earthquake_gg_technical_prem_final_post_uw
            gu_loss = earthquake_total_expected_loss_pre_uw_sum
            gu_prem = base_rate * total_modifier_impact * total_tiv_usd 
            itv = sum_tiv_buildings / total_floor_area if total_floor_area else 0

            target_list.append({
                "name": name,
                "num_locations": len(data),
                "tiv":  total_tiv_usd,
                "gu_tech_rate": gu_tech_rate,
                "worth": worth,
                "tech_rate": tech_rate,
                "tech_prem": tech_prem,
                "uw_adj_tech_rate": uw_adj_tech_rate,
                "uw_adj_tech_prem": uw_adj_tech_prem,
                "gu_loss": gu_loss,
                "gu_prem": gu_prem,
                "itv": itv
            })

    for summary_list in [cresta_summary_list, risk_level_eq_summary_list, occupancy_summary_list, constr_summary_list, eq_zone_summary_list]:
        summary_list.sort(key=lambda d: (d["tiv"], d["name"] or ""), reverse=True)
    
    other_data[f"eq_occupancy_summary_layer{index}"] = occupancy_summary_list[:10]
    other_data[f"eq_construction_summary_layer{index}"] = constr_summary_list
    other_data[f"eq_cresta_summary_layer{index}"] = cresta_summary_list[:10]
    other_data[f"eq_risk_category_summary_layer{index}"] = risk_level_eq_summary_list[:10]
    other_data[f"eq_zone_summary_layer{index}"] = eq_zone_summary_list


def earthquake_top_20_locations_summary(hxd, sum_prod_df, other_data, layer, index):
    df = sum_prod_df

    # Exposure Factors
    df = df.with_columns(
        [
            (pl.col("tiv_buildings") / pl.col("floor_area")).fill_nan(0).alias("itv"),
            (((pl.col("buildings_cumprod") + pl.col("contents_total_cumprod") + pl.col("bi_cumprod")) / pl.col("tiv_total_usd")) * pl.col("eq_catnet_intl_factor")).fill_nan(0).alias("base_rate"),
            (pl.col("eq_occupancy_factor") * pl.col("eq_construction_factor") * pl.col("eq_year_built_factor") * pl.col("eq_num_floors_factor") *
                pl.col("eq_construction_quality_factor") * pl.col("eq_plan_irregularity_factor") * pl.col("eq_soft_story_factor") * pl.col("eq_vertical_irregularity_factor") *
                pl.col("eq_ornamentation_factor") * pl.col("eq_equipment_bracing_factor") * pl.col("eq_equipment_maintenance_factor") * pl.col("eq_pounding_factor")
            ).alias("total_modifier_impact")
        ]
    )

    # Replace inf values
    df = df.with_columns(
        pl.when(pl.col("itv") == float('inf'))
        .then(0)
        .otherwise(pl.col("itv"))
        .alias("itv")
    )

    # GU Tech Rate, Tech Rate, UW Tech Rate, UW Tech Prem
    df = df.with_columns(
        (
            # pl.when(pl.col("country").is_in(["United States", "Canada"]))  # Canada is treated as US for Earthquake
            # .then(pl.col(f"earthquake_us_gn_technical_prem_{other_data['pre_uw_selected_method_layer{index}']}_pre_uw_layer{index}"))
            # .otherwise(pl.col(f"earthquake_intl_gn_technical_prem_{other_data['pre_uw_selected_method_layer{index}']}_pre_uw_layer{index}"))
            pl.col(f"earthquake_us_gg_technical_prem_final_pre_uw_layer{index}") + pl.col(f"earthquake_intl_gg_technical_prem_final_pre_uw_layer{index}")
        ).alias(f"earthquake_gg_technical_prem_final_pre_uw_layer{index}"),
        (
            # pl.when(pl.col("country").is_in(["United States", "Canada"]))
            # .then(pl.col(f"earthquake_us_gn_technical_prem_{other_data['post_uw_selected_method_layer{index}']}_post_uw_layer{index}"))
            # .otherwise(pl.col(f"earthquake_intl_gn_technical_prem_{other_data['post_uw_selected_method_layer{index}']}_post_uw_layer{index}"))
            pl.col(f"earthquake_us_gg_technical_prem_final_post_uw_layer{index}") + pl.col(f"earthquake_intl_gg_technical_prem_final_post_uw_layer{index}")
        ).alias(f"earthquake_gg_technical_prem_final_post_uw_layer{index}"),
        (
            # pl.when(pl.col("country").is_in(["United States", "Canada"]))
            # .then(pl.col(f"earthquake_us_total_expected_loss_pre_uw_layer{index}"))
            # .otherwise(pl.col(f"earthquake_intl_total_expected_loss_pre_uw_layer{index}"))
            pl.col(f"earthquake_us_total_expected_loss_pre_uw_layer{index}") + pl.col(f"earthquake_intl_total_expected_loss_pre_uw_layer{index}")
        ).alias(f"earthquake_total_expected_loss_pre_uw_layer{index}"),
        (
            # pl.when(pl.col("country").is_in(["United States"]))  # TODO make sure Canada is being used correctly everywhere
            # .then(pl.col(f"earthquake_us_worth_percent_layer{index}"))
            # .otherwise(pl.col(f"earthquake_intl_worth_percent_layer{index}"))
            pl.col(f"earthquake_us_worth_percent_layer{index}") + pl.col(f"earthquake_intl_worth_percent_layer{index}")
        ).alias(f"earthquake_worth_percent_layer{index}")
    )

    df = df.with_columns(
        [
            (pl.col("base_rate") * pl.col("total_modifier_impact") * pl.col(f"earthquake_gg_technical_prem_final_pre_uw_layer{index}") /
                pl.col(f"earthquake_total_expected_loss_pre_uw_layer{index}")).fill_nan(0).alias("gu_tech_rate"),
            (pl.col(f"earthquake_worth_percent_layer{index}")).alias("worth"),
            (pl.col(f"earthquake_gg_technical_prem_final_pre_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("tech_rate"),
            (pl.col(f"earthquake_gg_technical_prem_final_post_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("uw_adj_tech_rate"),
            pl.col(f"earthquake_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0).alias("uw_adj_tech_prem")
        ]
    )

    # error catch if simulated results are 0 and simulation is used to avoid division by 0 error
    df = df.with_columns(pl.when(pl.col("gu_tech_rate") == float('inf')).then(0).otherwise(pl.col("gu_tech_rate")).alias("gu_tech_rate"))
    df_test = df[[
        "country", "state", "county", "zip", "tiv_total_usd",
        "base_rate", 
        f"earthquake_us_gg_technical_prem_final_post_uw_layer{index}",
        f"earthquake_intl_gg_technical_prem_final_post_uw_layer{index}",
        f"earthquake_gg_technical_prem_final_post_uw_layer{index}"
        ]]

    df_layer = df[[
        "country", "state", "county", "zip",
        "tiv_buildings_usd", "tiv_contents_total_usd", "tiv_bi_usd", "tiv_total_usd", "itv",
        "base_rate", "eq_occupancy_factor", "eq_construction_factor", "eq_year_built_factor", "eq_num_floors_factor",
        "eq_construction_quality_factor", "eq_plan_irregularity_factor", "eq_soft_story_factor", "eq_vertical_irregularity_factor",
        "eq_ornamentation_factor", "eq_equipment_bracing_factor", "eq_equipment_maintenance_factor", "eq_pounding_factor", "eq_catnet_intl_factor",
        "total_modifier_impact", "gu_tech_rate", "worth",
        "tech_rate", "uw_adj_tech_rate", "uw_adj_tech_prem"
        ]]

    df_layer = df_layer.rename({
        "tiv_buildings_usd": "tiv_buildings", "tiv_contents_total_usd": "tiv_contents_total", "tiv_bi_usd": "tiv_bi", "tiv_total_usd": "tiv_total",
        "eq_occupancy_factor": "occupancy", "eq_construction_factor": "construction", "eq_year_built_factor": "year_built", 
        "eq_num_floors_factor": "num_of_floors", "eq_construction_quality_factor": "construction_quality", "eq_plan_irregularity_factor": "plan_irregularity", 
        "eq_soft_story_factor": "soft_story", "eq_vertical_irregularity_factor": "vertical_irregularity", "eq_ornamentation_factor": "ornamentation", 
        "eq_equipment_bracing_factor": "equipment_bracing", "eq_equipment_maintenance_factor": "equipment_maintenance", 
        "eq_pounding_factor": "pounding", "eq_catnet_intl_factor": "catnet_score"
        })
    
    df_layer_tiv = df_layer.sort("tiv_total", descending=True).head(20)
    df_layer_rate = df_layer.sort("uw_adj_tech_prem", descending=True).head(20)

    other_data[f"eq_top_20_locations_summary_layer{index}_tiv"] = df_layer_tiv.to_dicts()
    other_data[f"eq_top_20_locations_summary_layer{index}_rate"] = df_layer_rate.to_dicts()
