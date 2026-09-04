import hx
import polars as pl

def flood_analysis_summary(hxd, df, other_data):
    
    for index, layer in enumerate(hxd.layers, start=1):
        sum_prod_df = flood_modifier_summary(hxd, df, other_data, layer, index)
        flood_risk_factors_summary(hxd, sum_prod_df, other_data, layer, index)
        flood_top_20_locations_summary(hxd, sum_prod_df, other_data, layer, index)
    
    return df


def flood_modifier_summary(hxd, df, other_data, layer, index):

    # Cache after each cumulative product of risk factor
    sum_cache = {}

    modifier_summary_dict = {}
    # Assign to Fire Modifier Summary
    modifier_summary_dict["peril_name"] = "Flood"
    modifier_summary_dict["no_of_locs"] = len(df)
    modifier_summary_dict["sum_tiv_total_usd"] = other_data["total_tiv_total_usd"]  

    # Calculate the sum product per layer
    # Select a subset of fields to optimise sorting
    sum_prod_df = df[["country", "state", "county", "zip",
                        "tiv_buildings", "tiv_contents_total", "tiv_bi", "tiv_total",
                        "occupancy", "tiv_buildings_usd", "tiv_contents_total_usd", "tiv_bi_usd", "tiv_total_usd",
                        "constr_name", "num_stories", "risk_level_fl", "floor_area",
                        f"flood_us_buildings_base_rate_layer{index}", f"flood_intl_buildings_base_rate_layer{index}",
                        f"flood_us_contents_base_rate_layer{index}", f"flood_intl_contents_base_rate_layer{index}",
                        f"flood_us_bi_base_rate_layer{index}", f"flood_intl_bi_base_rate_layer{index}",
                        "fl_construction_rating_factor", "fl_num_floors_rating_factor", "fl_basement_rating_factor",
                        "fl_elevation_rating_factor", "fl_catnet_rating_factor", "fl_size_discount_rating_factor", "fl_katrisk_risk_rating_factor",
                        f"flood_us_gg_technical_prem_final_pre_uw_layer{index}",
                        f"flood_intl_gg_technical_prem_final_pre_uw_layer{index}",
                        f"flood_us_gg_technical_prem_final_post_uw_layer{index}",
                        f"flood_intl_gg_technical_prem_final_post_uw_layer{index}",
                        f"flood_us_total_expected_loss_pre_uw_layer{index}", f"flood_intl_total_expected_loss_pre_uw_layer{index}",
                        f"flood_us_worth_percent_layer{index}", f"flood_intl_worth_percent_layer{index}"
                    ]]

    # Base weighted sum
    sum_prod_df = sum_prod_df.with_columns(
        [
            (pl.col("tiv_buildings_usd") * 
                (pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"flood_us_buildings_base_rate_layer{index}"))
                    .otherwise(pl.col(f"flood_intl_buildings_base_rate_layer{index}"))
                )
            ).alias("buildings_cumprod"),
            (pl.col("tiv_contents_total_usd") *
                (pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"flood_us_contents_base_rate_layer{index}"))
                    .otherwise(pl.col(f"flood_intl_contents_base_rate_layer{index}"))
                )
            ).alias("contents_total_cumprod"),
            (pl.col("tiv_bi_usd") * 
                (pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"flood_us_bi_base_rate_layer{index}"))
                    .otherwise(pl.col(f"flood_intl_bi_base_rate_layer{index}"))
                )
            ).alias("bi_cumprod"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_worth_percent_layer{index}"))
                .otherwise(pl.col(f"flood_intl_worth_percent_layer{index}"))
                .alias(f"flood_worth_percent_layer{index}")
        ]
    )

    sum_cache["base_sum"] = (sum_prod_df["buildings_cumprod"].sum() or 0) + (sum_prod_df["contents_total_cumprod"].sum() or 0) + (sum_prod_df["bi_cumprod"].sum() or 0)

    total_modifier_impact = 1

    rating_factors = ["construction", "num_of_floors", "basement", "elevation", "size_discount"]

    multipliers = [pl.col("fl_construction_rating_factor"), pl.col("fl_num_floors_rating_factor"), pl.col("fl_basement_rating_factor"), pl.col("fl_elevation_rating_factor"), pl.col("fl_size_discount_rating_factor")] 

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

    # Calculate KatRisk/CatNet Score

    sum_prod_df = sum_prod_df.with_columns(
            [
                (pl.when(pl.col("country") == "United States")
                    .then(pl.col("size_discount_buildings_cumprod") * pl.col("fl_katrisk_risk_rating_factor"))
                    .otherwise(pl.col("size_discount_buildings_cumprod") * pl.col("fl_catnet_rating_factor"))
                ).alias("katrisk_catnet_score_buildings_cumprod"),
                (pl.when(pl.col("country") == "United States")
                    .then(pl.col("size_discount_contents_total_cumprod") * pl.col("fl_katrisk_risk_rating_factor"))
                    .otherwise(pl.col("size_discount_contents_total_cumprod") * pl.col("fl_catnet_rating_factor"))
                ).alias("katrisk_catnet_score_contents_total_cumprod"),
                (pl.when(pl.col("country") == "United States")
                    .then(pl.col("size_discount_bi_cumprod") * pl.col("fl_katrisk_risk_rating_factor"))
                    .otherwise(pl.col("size_discount_bi_cumprod") * pl.col("fl_catnet_rating_factor"))
                ).alias("katrisk_catnet_score_bi_cumprod")
            ]
    )

    sum_cache["katrisk_catnet_score_sum"] = (sum_prod_df["katrisk_catnet_score_buildings_cumprod"].sum() or 0) + (sum_prod_df["katrisk_catnet_score_contents_total_cumprod"].sum() or 0) + \
                                                (sum_prod_df["katrisk_catnet_score_bi_cumprod"].sum() or 0)
    
    modifier_summary_dict["katrisk_catnet_score"] = sum_cache["katrisk_catnet_score_sum"] / sum_cache["size_discount_sum"] if sum_cache["size_discount_sum"] else 0
    modifier_summary_dict["total_modifier_impact"] = total_modifier_impact * modifier_summary_dict["katrisk_catnet_score"]

    # GU Tech Rate, Tech Rate, UW Tech Rate, UW Tech Prem
    flood_gg_technical_prem_final_pre_uw = ((df[f"flood_us_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0) + 
                                                    (df[f"flood_intl_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0))

    flood_gg_technical_prem_final_post_uw = ((df[f"flood_us_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0) + 
                                                    (df[f"flood_intl_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0))

    flood_total_expected_loss_pre_uw_sum = (df[f"flood_us_total_expected_loss_pre_uw_layer{index}"].fill_nan(0).sum() or 0) + (df[f"flood_intl_total_expected_loss_pre_uw_layer{index}"].fill_nan(0).sum() or 0)

    modifier_summary_dict["gu_tech_rate"] = ((sum_cache["base_sum"] / other_data["sum_tiv_total_usd"]) * modifier_summary_dict["total_modifier_impact"] * flood_gg_technical_prem_final_pre_uw / flood_total_expected_loss_pre_uw_sum
                                        if flood_total_expected_loss_pre_uw_sum and other_data["sum_tiv_total_usd"] else 0)

    modifier_summary_dict["tech_rate"] = flood_gg_technical_prem_final_pre_uw / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0

    # To be confirmed: worth change to weighted average on total_tiv
    # modifier_summary_dict["worth"] = modifier_summary_dict["tech_rate"] / modifier_summary_dict["gu_tech_rate"] if modifier_summary_dict["gu_tech_rate"] else 0
    cum_prod_worth = df.select(pl.col(f"flood_worth_percent_layer{index}") * pl.col("tiv_total_usd"))[f"flood_worth_percent_layer{index}"].sum()
    modifier_summary_dict["worth"] = cum_prod_worth / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0 

    modifier_summary_dict["uw_adj_tech_rate"] = flood_gg_technical_prem_final_post_uw / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0
    modifier_summary_dict["uw_adj_tech_prem"] = flood_gg_technical_prem_final_post_uw

    other_data[f"fl_modifier_summary_layer{index}"] = modifier_summary_dict

    return sum_prod_df


def flood_risk_factors_summary(hxd, sum_prod_df, other_data, layer, index):

    constr_summary_list = []
    num_of_floors_summary_list = []
    risk_level_fl_summary_list = []

    for column_name, target_list in zip(
                    ("constr_name", "num_stories", "risk_level_fl"), 
                    (constr_summary_list, num_of_floors_summary_list, risk_level_fl_summary_list)):

        for name, data in sum_prod_df.groupby(column_name):

            prod_sum_base = (data["buildings_cumprod"].sum() or 0) + (data["contents_total_cumprod"].sum() or 0) + (data["bi_cumprod"].sum() or 0)
            prod_sum_last = (data["katrisk_catnet_score_buildings_cumprod"].sum() or 0) + (data["katrisk_catnet_score_contents_total_cumprod"].sum() or 0) + \
                                            (data["katrisk_catnet_score_bi_cumprod"].sum() or 0)

            total_tiv_usd = data["tiv_total_usd"].sum() or 0
            sum_total_tiv = data["tiv_total"].sum() or 0
            sum_tiv_buildings = data["tiv_buildings"].sum() or 0
            base_rate = prod_sum_base / total_tiv_usd if total_tiv_usd else 0
            total_modifier_impact = prod_sum_last / prod_sum_base if prod_sum_base else 0

            flood_gg_technical_prem_final_pre_uw = ((data[f"flood_us_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0) + \
                (data[f"flood_intl_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0))

            flood_gg_technical_prem_final_post_uw = ((data[f"flood_us_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0) + \
                (data[f"flood_intl_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0))

            flood_total_expected_loss_pre_uw_sum = (data[f"flood_us_total_expected_loss_pre_uw_layer{index}"].fill_nan(0).sum() or 0) + (data[f"flood_intl_total_expected_loss_pre_uw_layer{index}"].fill_nan(0).sum() or 0)
            
            # total_floor_area = data['floor_area'].fill_null(0).sum() or 0

            total_floor_area = data.filter(pl.col("tiv_buildings") != 0)['floor_area'].fill_null(0).sum() or 0
            
            gu_tech_rate = base_rate * total_modifier_impact * flood_gg_technical_prem_final_pre_uw / flood_total_expected_loss_pre_uw_sum if flood_total_expected_loss_pre_uw_sum else 0
            tech_rate = flood_gg_technical_prem_final_pre_uw / total_tiv_usd if total_tiv_usd else 0
            tech_prem = flood_gg_technical_prem_final_pre_uw

            # To be confirmed: worth change to weighted average on total_tiv
            # worth = tech_rate / gu_tech_rate if gu_tech_rate else 0
            cum_prod_worth = data.select(pl.col(f"flood_worth_percent_layer{index}") * pl.col("tiv_total_usd"))[f"flood_worth_percent_layer{index}"].sum() or 0
            worth = cum_prod_worth / total_tiv_usd if total_tiv_usd else 0

            uw_adj_tech_rate = flood_gg_technical_prem_final_post_uw / total_tiv_usd if total_tiv_usd else 0
            uw_adj_tech_prem = flood_gg_technical_prem_final_post_uw
            gu_loss = flood_total_expected_loss_pre_uw_sum
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

    # added check if there are 0 floors to avoid sorting error
    for summary_list in [constr_summary_list, num_of_floors_summary_list, risk_level_fl_summary_list]:
        summary_list.sort(key=lambda d: (d["tiv"], 0 if d["name"] == 0 else d["name"] or ""), reverse=True)

    other_data[f"fl_risk_category_summary_layer{index}"] = risk_level_fl_summary_list
    other_data[f"fl_construction_summary_layer{index}"] = constr_summary_list
    other_data[f"fl_num_of_floors_summary_layer{index}"] = num_of_floors_summary_list


def flood_top_20_locations_summary(hxd, sum_prod_df, other_data, layer, index):
    df = sum_prod_df

    # Exposure Factors
    df = df.with_columns(
        [
            (pl.col("tiv_buildings") / pl.col("floor_area")).fill_nan(0).alias("itv"),
            ((pl.col("buildings_cumprod") + pl.col("contents_total_cumprod") + pl.col("bi_cumprod")) / pl.col("tiv_total_usd")).fill_nan(0).alias("base_rate"),
            (pl.when(pl.col("country") == "United States")
                .then(pl.col("fl_katrisk_risk_rating_factor"))
                .otherwise(pl.col("fl_catnet_rating_factor"))
                .alias("katrisk_catnet_score_factor"))
        ]
    )

    df = df.with_columns(
        (pl.col("fl_construction_rating_factor") * pl.col("fl_num_floors_rating_factor") * pl.col("fl_basement_rating_factor") *
            pl.col("fl_elevation_rating_factor") * pl.col("fl_size_discount_rating_factor") * pl.col("katrisk_catnet_score_factor")
        ).alias("total_modifier_impact")
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
        [
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_gg_technical_prem_final_pre_uw_layer{index}"))
                .otherwise(pl.col(f"flood_intl_gg_technical_prem_final_pre_uw_layer{index}"))
                .alias(f"flood_gg_technical_prem_final_pre_uw_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_gg_technical_prem_final_post_uw_layer{index}"))
                .otherwise(pl.col(f"flood_intl_gg_technical_prem_final_post_uw_layer{index}"))
                .alias(f"flood_gg_technical_prem_final_post_uw_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_total_expected_loss_pre_uw_layer{index}"))
                .otherwise(pl.col(f"flood_intl_total_expected_loss_pre_uw_layer{index}"))
                .alias(f"flood_total_expected_loss_pre_uw_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_worth_percent_layer{index}"))
                .otherwise(pl.col(f"flood_intl_worth_percent_layer{index}"))
                .alias(f"flood_worth_percent_layer{index}")
        ]
    )

    df = df.with_columns(
        [
            (pl.col("base_rate") * pl.col("total_modifier_impact") * pl.col(f"flood_gg_technical_prem_final_pre_uw_layer{index}") /
                pl.col(f"flood_total_expected_loss_pre_uw_layer{index}")).fill_nan(0).alias("gu_tech_rate"),
            (pl.col(f"flood_worth_percent_layer{index}")).alias("worth"),
            (pl.col(f"flood_gg_technical_prem_final_pre_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("tech_rate"),
            (pl.col(f"flood_gg_technical_prem_final_post_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("uw_adj_tech_rate"),
            pl.col(f"flood_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0).alias("uw_adj_tech_prem")
        ]
    )

    df = df.with_columns(pl.when(pl.col("gu_tech_rate") == float('inf')).then(0).otherwise(pl.col("gu_tech_rate")).alias("gu_tech_rate"))


    df_layer = df[[
        "country", "state", "county", "zip",
        "tiv_buildings_usd", "tiv_contents_total_usd", "tiv_bi_usd", "tiv_total_usd", "itv",
        "base_rate", "fl_construction_rating_factor", "fl_num_floors_rating_factor", "fl_basement_rating_factor",
        "fl_elevation_rating_factor", "katrisk_catnet_score_factor", "fl_size_discount_rating_factor",
        "total_modifier_impact", "gu_tech_rate", "worth",
        "tech_rate", "uw_adj_tech_rate", "uw_adj_tech_prem"
    ]]

    df_layer = df_layer.rename({
        "tiv_buildings_usd": "tiv_buildings", "tiv_contents_total_usd": "tiv_contents_total", "tiv_bi_usd": "tiv_bi", "tiv_total_usd": "tiv_total",
        "fl_construction_rating_factor": "construction", "fl_num_floors_rating_factor": "num_of_floors",
        "fl_basement_rating_factor": "basement", "fl_elevation_rating_factor": "elevation",
        "katrisk_catnet_score_factor": "katrisk_catnet_score", "fl_size_discount_rating_factor": "size_discount"
    })

    df_layer_tiv = df_layer.sort("tiv_total", descending=True).head(20)
    df_layer_rate = df_layer.sort("uw_adj_tech_prem", descending=True).head(20)

    other_data[f"fl_top_20_locations_summary_layer{index}_tiv"] = df_layer_tiv.to_dicts()
    other_data[f"fl_top_20_locations_summary_layer{index}_rate"] = df_layer_rate.to_dicts()