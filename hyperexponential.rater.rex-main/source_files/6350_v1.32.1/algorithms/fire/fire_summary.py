import hx
import polars as pl
from algorithms.constant import fire_rating_factors

def fire_analysis_summary(hxd, df, other_data):

    for index, layer in enumerate(hxd.layers, start=1):
        sum_prod_df = fire_modifier_summary(hxd, df, other_data, layer, index)
        fire_risk_factors_summary(hxd, sum_prod_df, other_data, layer, index)
        fire_mb_summary(hxd, sum_prod_df, other_data, layer, index)
        fire_top_20_locations_summary(hxd, sum_prod_df, other_data, layer, index)

def fire_modifier_summary(hxd, df, other_data, layer, index):

    # Cache after each cumulative product of risk factor
    sum_cache = {}
    
    modifier_summary_dict = {}
    # Assign to Fire Modifier Summary
    modifier_summary_dict["peril_name"] = "Fire"
    modifier_summary_dict["no_of_locs"] = len(df)
    modifier_summary_dict["sum_tiv_total_usd"] = other_data["total_tiv_total_usd"]

    # Calculate the sum product per layer
    sum_prod_df = df[["country", "state", "county", "zip",
                        "industry", "occupancy", "constr_name", "sprinkler", 
                        "tiv_buildings", "tiv_contents_total", "tiv_bi", "tiv_total",
                        "tiv_buildings_usd", "tiv_contents_total_usd", "tiv_bi_usd", "tiv_total_usd", "floor_area",
                        f"fire_buildings_base_rate_layer{index}", f"fire_contents_base_rate_layer{index}",
                        f"fire_mb_base_rate_layer{index}", f"fire_bi_base_rate_layer{index}", "fire_construction_factor", "fire_pc_code_factor",
                        "fire_sprinkler_factor", "bi_waiting_period_factor", "fire_size_discount_factor", "fire_mexican_fonden_factor", "fire_mb_proportion",
                        f"fire_gg_technical_prem_final_pre_uw_layer{index}",
                        f"fire_gg_technical_prem_final_post_uw_layer{index}",
                        f"fire_total_expected_loss_pre_uw_layer{index}", f"fire_total_expected_loss_post_uw_layer{index}", f"fire_worth_percent_layer{index}",
                        f"fire_mb_expected_loss_pre_uw_layer{index}", f"fire_mb_expected_loss_post_uw_layer{index}"
                    ]]

    # Occupancy weighted adjustment
    sum_prod_df = sum_prod_df.with_columns(
        [
            (pl.col("tiv_buildings_usd") * pl.col(f"fire_buildings_base_rate_layer{index}")).alias("buildings_cumprod"),
            (pl.col("tiv_contents_total_usd") * (1 - pl.col("fire_mb_proportion")) * pl.col(f"fire_contents_base_rate_layer{index}")).alias("contents_total_cumprod"),
            (pl.col("tiv_bi_usd") * (1 - pl.col("fire_mb_proportion")) * pl.col(f"fire_bi_base_rate_layer{index}")).alias("bi_cumprod"),
            (pl.col("tiv_contents_total_usd") * pl.col("fire_mb_proportion") * pl.col(f"fire_mb_base_rate_layer{index}")).alias("mb_contents_cumprod"),
            (pl.col("tiv_bi_usd") * pl.col("fire_mb_proportion") * pl.col(f"fire_mb_base_rate_layer{index}") *\
                (pl.when(pl.col(f"fire_contents_base_rate_layer{index}") == 0)
                    .then(0)
                    .otherwise(pl.col(f"fire_bi_base_rate_layer{index}") / pl.col(f"fire_contents_base_rate_layer{index}"))))
                .alias("mb_bi_cumprod")
        ]
    )
    sum_prod_df = sum_prod_df.with_columns((pl.col("mb_contents_cumprod") + pl.col("mb_bi_cumprod")).alias("mb_cumprod"))

    sum_cache["occupancy_sum"] = (sum_prod_df["buildings_cumprod"].sum() or 0) + (sum_prod_df["contents_total_cumprod"].sum() or 0) + (sum_prod_df["mb_cumprod"].sum() or 0) + (sum_prod_df["bi_cumprod"].sum() or 0)
    modifier_summary_dict["occupancy"] = sum_cache["occupancy_sum"] / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0

    total_modifier_impact = 1
    rating_factors = fire_rating_factors
    multipliers = ["", pl.col("fire_construction_factor"), pl.col("fire_pc_code_factor"), pl.col("fire_sprinkler_factor"), pl.col("bi_waiting_period_factor"),
                    other_data['bi_indemnity_period_factor'], other_data['cbi_load'], pl.col("fire_size_discount_factor"), pl.col("fire_mexican_fonden_factor")]

    for idx, (factor, multiplier_col) in enumerate(zip(rating_factors, multipliers)):
        if idx == 0:
            continue
        
        column_prefix = "" if idx == 1 else f"{rating_factors[idx-1]}_"

        if factor == ("bi_waiting_period" or "bi_indemnity_period"):
            sum_prod_df = sum_prod_df.with_columns(
            [
                (pl.col(f"{column_prefix}buildings_cumprod") * 1).alias(f"{factor}_buildings_cumprod"),
                (pl.col(f"{column_prefix}contents_total_cumprod") * 1).alias(f"{factor}_contents_total_cumprod"),
                (pl.col(f"{column_prefix}bi_cumprod") * multiplier_col).alias(f"{factor}_bi_cumprod"),
                (pl.col(f"{column_prefix}mb_contents_cumprod") * 1).alias(f"{factor}_mb_contents_cumprod"),
                (pl.col(f"{column_prefix}mb_bi_cumprod") * multiplier_col).alias(f"{factor}_mb_bi_cumprod")
            ]
        )
        else:
            sum_prod_df = sum_prod_df.with_columns(
                [
                    (pl.col(f"{column_prefix}buildings_cumprod") * multiplier_col).alias(f"{factor}_buildings_cumprod"),
                    (pl.col(f"{column_prefix}contents_total_cumprod") * multiplier_col).alias(f"{factor}_contents_total_cumprod"),
                    (pl.col(f"{column_prefix}bi_cumprod") * multiplier_col).alias(f"{factor}_bi_cumprod"),
                    (pl.col(f"{column_prefix}mb_contents_cumprod") * multiplier_col).alias(f"{factor}_mb_contents_cumprod"),
                    (pl.col(f"{column_prefix}mb_bi_cumprod") * multiplier_col).alias(f"{factor}_mb_bi_cumprod")
                ]
            )
        sum_prod_df = sum_prod_df.with_columns((pl.col(f"{factor}_mb_contents_cumprod") + pl.col(f"{factor}_mb_bi_cumprod")).alias(f"{factor}_mb_cumprod"))

        sum_cache[f"{factor}_sum"] = (sum_prod_df[f"{factor}_buildings_cumprod"].sum() or 0) + (sum_prod_df[f"{factor}_contents_total_cumprod"].sum() or 0) + \
                                        (sum_prod_df[f"{factor}_mb_cumprod"].sum() or 0) + (sum_prod_df[f"{factor}_bi_cumprod"].sum() or 0)
        
        modifier_impact = sum_cache[f"{factor}_sum"] / sum_cache[f"{rating_factors[idx-1]}_sum"] if sum_cache[f"{rating_factors[idx-1]}_sum"] else 0

        modifier_summary_dict[factor] = modifier_impact
        total_modifier_impact *= modifier_impact

    modifier_summary_dict["total_modifier_impact"] = total_modifier_impact 

    # GU Tech Rate, Tech Rate, UW Tech Rate, UW Tech Prem
    fire_gg_technical_prem_final_pre_uw = (df[f"fire_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0)
    fire_gg_technical_prem_final_post_uw = (df[f"fire_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0)

    fire_total_expected_loss_pre_uw_sum = (df[f"fire_total_expected_loss_pre_uw_layer{index}"].sum() or 0)

    modifier_summary_dict["gu_tech_rate"] = (modifier_summary_dict["occupancy"] * modifier_summary_dict["total_modifier_impact"] * fire_gg_technical_prem_final_pre_uw / fire_total_expected_loss_pre_uw_sum
                                        if fire_total_expected_loss_pre_uw_sum else 0)

    modifier_summary_dict["tech_rate"] = fire_gg_technical_prem_final_pre_uw / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0

    # To be confirmed: worth change to weighted average on total_tiv
    # modifier_summary_dict["worth"] = modifier_summary_dict["tech_rate"] / modifier_summary_dict["gu_tech_rate"] if modifier_summary_dict["gu_tech_rate"] else 0
    cum_prod_worth = df.select(pl.col(f"fire_worth_percent_layer{index}") * pl.col("tiv_total_usd"))[f"fire_worth_percent_layer{index}"].sum()
    modifier_summary_dict["worth"] = cum_prod_worth / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0 

    modifier_summary_dict["uw_adj_tech_rate"] = fire_gg_technical_prem_final_post_uw / other_data["sum_tiv_total_usd"] if other_data["sum_tiv_total_usd"] else 0
    modifier_summary_dict["uw_adj_tech_prem"] = fire_gg_technical_prem_final_post_uw

    other_data[f"fire_modifier_summary_layer{index}"] = modifier_summary_dict

    return sum_prod_df


def fire_risk_factors_summary(hxd, sum_prod_df, other_data, layer, index):

    occupancy_summary_list = []
    constr_summary_list = []
    sprinkler_summary_list = []

    for column_name, target_list in zip(
                    ("occupancy", "constr_name", "sprinkler"), 
                    (occupancy_summary_list, constr_summary_list, sprinkler_summary_list)):

        for name, data in sum_prod_df.groupby(column_name):

            prod_sum_base = (data["buildings_cumprod"].sum() or 0) + (data["contents_total_cumprod"].sum() or 0) + (data["mb_cumprod"].sum() or 0) + (data["bi_cumprod"].sum() or 0)
            prod_sum_mexican_fonden = (data["mexican_fonden_buildings_cumprod"].sum() or 0) + (data["mexican_fonden_contents_total_cumprod"].sum() or 0) + \
                                            (data["mexican_fonden_mb_cumprod"].sum() or 0) + (data["mexican_fonden_bi_cumprod"].sum() or 0)

            total_tiv_usd = data["tiv_total_usd"].sum() or 0
            sum_buildings_tiv = data["tiv_buildings"].sum() or 0
            base_rate = prod_sum_base / total_tiv_usd if total_tiv_usd else 0
            total_modifier_impact = prod_sum_mexican_fonden / prod_sum_base if prod_sum_base else 0

            fire_gg_technical_prem_final_pre_uw = (data[f"fire_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0)
            fire_gg_technical_prem_final_post_uw = (data[f"fire_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0)
            fire_total_expected_loss_pre_uw_sum = (data[f"fire_total_expected_loss_pre_uw_layer{index}"].sum() or 0)
            # total_floor_area = data['floor_area'].fill_null(0).sum() or 0

            total_floor_area = data.filter(pl.col("tiv_buildings") != 0)['floor_area'].fill_null(0).sum() or 0
            
            gu_tech_rate = base_rate * total_modifier_impact * fire_gg_technical_prem_final_pre_uw / fire_total_expected_loss_pre_uw_sum if fire_total_expected_loss_pre_uw_sum else 0            
            tech_rate = fire_gg_technical_prem_final_pre_uw / total_tiv_usd if total_tiv_usd else 0
            tech_prem = fire_gg_technical_prem_final_pre_uw
            
            # To be confirmed: worth change to weighted average on total_tiv
            # worth = tech_rate / gu_tech_rate if gu_tech_rate else 0
            cum_prod_worth = data.select(pl.col(f"fire_worth_percent_layer{index}") * pl.col("tiv_total_usd"))[f"fire_worth_percent_layer{index}"].sum() or 0
            worth = cum_prod_worth / total_tiv_usd if total_tiv_usd else 0

            uw_adj_tech_rate = fire_gg_technical_prem_final_post_uw / total_tiv_usd if total_tiv_usd else 0
            uw_adj_tech_prem = fire_gg_technical_prem_final_post_uw
            gu_loss = fire_total_expected_loss_pre_uw_sum
            gu_prem = base_rate * total_modifier_impact * total_tiv_usd
            itv = sum_buildings_tiv / total_floor_area if total_floor_area else 0

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

    for summary_list in [occupancy_summary_list, constr_summary_list, sprinkler_summary_list]:
        summary_list.sort(key=lambda d: (d["tiv"], d["name"] or ""), reverse=True)
    
    other_data[f"fire_occupancy_summary_layer{index}"] = occupancy_summary_list[:10]
    other_data[f"fire_construction_summary_layer{index}"] = constr_summary_list
    other_data[f"fire_sprinkler_summary_layer{index}"] = sprinkler_summary_list 

def fire_mb_summary(hxd, sum_prod_df, other_data, layer, index):

    exchange_rate = hxd.policy_information.exchange_rate or 1
    
    industry_mb_summary_list = []

    for column_name, target_list in zip(("industry",), (industry_mb_summary_list,)):

        for name, data in sum_prod_df.groupby(column_name):

            prod_sum_base = (data["mb_cumprod"].sum() or 0)
            prod_sum_mexican_fonden = (data["mexican_fonden_mb_cumprod"].sum() or 0)

            total_tiv_usd = data["tiv_total_usd"].sum() or 0
            total_contents_bi_tiv_usd = (data["tiv_contents_total_usd"].sum() + data["tiv_bi_usd"].sum()) or 0
            fire_mb_proportion = (((data["tiv_contents_total_usd"] + data["tiv_bi_usd"]) * data["fire_mb_proportion"]).sum() / total_contents_bi_tiv_usd if total_contents_bi_tiv_usd else 0.0)
            base_rate = prod_sum_base / (total_contents_bi_tiv_usd * fire_mb_proportion) if total_contents_bi_tiv_usd and fire_mb_proportion else 0.0
            total_modifier_impact = prod_sum_mexican_fonden / prod_sum_base if prod_sum_base else 0

            fire_gg_technical_prem_final_pre_uw = (data[f"fire_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0)
            fire_gg_technical_prem_final_post_uw = (data[f"fire_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0)
            fire_total_expected_loss_pre_uw_sum = (data[f"fire_total_expected_loss_pre_uw_layer{index}"].sum() or 0)
            fire_total_expected_loss_post_uw_sum = (data[f"fire_total_expected_loss_post_uw_layer{index}"].sum() or 0)

            fire_mb_expected_loss_pre_uw_sum = (data[f"fire_mb_expected_loss_pre_uw_layer{index}"].sum() or 0)
            fire_mb_expected_loss_post_uw_sum = (data[f"fire_mb_expected_loss_post_uw_layer{index}"].sum() or 0)
            fire_mb_gg_technical_prem_final_pre_uw = fire_mb_expected_loss_pre_uw_sum * fire_gg_technical_prem_final_pre_uw / fire_total_expected_loss_pre_uw_sum if fire_total_expected_loss_pre_uw_sum else 0.0
            fire_mb_gg_technical_prem_final_post_uw = fire_mb_expected_loss_post_uw_sum * fire_gg_technical_prem_final_post_uw / fire_total_expected_loss_post_uw_sum if fire_total_expected_loss_post_uw_sum else 0.0
          
            gu_tech_rate = base_rate * total_modifier_impact * fire_gg_technical_prem_final_pre_uw / fire_total_expected_loss_pre_uw_sum if fire_total_expected_loss_pre_uw_sum else 0            
            tech_rate = fire_mb_gg_technical_prem_final_pre_uw / (total_contents_bi_tiv_usd * fire_mb_proportion) if total_contents_bi_tiv_usd and fire_mb_proportion else 0.0
            tech_prem = fire_mb_gg_technical_prem_final_pre_uw
            
            worth = tech_rate / gu_tech_rate if gu_tech_rate else 0

            uw_adj_tech_rate = fire_mb_gg_technical_prem_final_post_uw / (total_contents_bi_tiv_usd * fire_mb_proportion) if total_contents_bi_tiv_usd and fire_mb_proportion else 0.0
            uw_adj_tech_prem = fire_mb_gg_technical_prem_final_post_uw

            target_list.append({
                "name": name,
                "num_locations": len(data),
                "tiv":  total_contents_bi_tiv_usd * exchange_rate,
                "fire_mb_proportion": fire_mb_proportion,
                "gu_tech_rate": gu_tech_rate,
                "worth": worth,
                "tech_rate": tech_rate,
                "tech_prem": tech_prem * exchange_rate,
                "uw_adj_tech_rate": uw_adj_tech_rate,
                "uw_adj_tech_prem": uw_adj_tech_prem * exchange_rate
            })

    for summary_list in [industry_mb_summary_list]:
        summary_list.sort(key=lambda d: (d["tiv"], d["name"] or ""), reverse=True)

    # assign to hxd
    layer.perils.fire.machinery_breakdown_summary = summary_list
    

def fire_top_20_locations_summary(hxd, sum_prod_df, other_data, layer, index):
    df = sum_prod_df

    # Exposure Factors
    df = df.with_columns(
        [
            pl.lit(other_data['bi_indemnity_period_factor']).alias("bi_indemnity_period"),
            pl.lit(other_data['cbi_load']).alias("cbi"),
            (pl.col("tiv_buildings") / pl.col("floor_area")).fill_nan(0).alias("itv"),
            ((pl.col("buildings_cumprod") + pl.col("contents_total_cumprod") + pl.col("mb_cumprod") + pl.col("bi_cumprod")) / pl.col("tiv_total_usd")).fill_nan(0).alias("base_rate")
        ]
    )

    # Replace inf values
    df = df.with_columns(
        pl.when(pl.col("itv") == float('inf'))
        .then(0)
        .otherwise(pl.col("itv"))
        .alias("itv")
    )

    # Calculate weighted modifiers for BI specific factors
    for modifier in ["bi_waiting_period_factor", "bi_indemnity_period"]:
        df = df.with_columns(
            [
                (((pl.col("tiv_buildings_usd") * pl.col(f"fire_buildings_base_rate_layer{index}") + \
                    pl.col("tiv_contents_total_usd") * (1 - pl.col("fire_mb_proportion")) * pl.col(f"fire_contents_base_rate_layer{index}") + \
                    pl.col("tiv_contents_total_usd") * pl.col("fire_mb_proportion") * pl.col(f"fire_mb_base_rate_layer{index}") + \
                    pl.col("tiv_bi_usd") * pl.col(f"fire_bi_base_rate_layer{index}") * pl.col(f"{modifier}")) / pl.col("tiv_total_usd")) / pl.col("base_rate")).fill_null(0).fill_nan(0).alias(f"weighted_{modifier}")
            ]
        )

    df = df.with_columns(
        [
            (pl.col("fire_construction_factor") * pl.col("fire_pc_code_factor") * pl.col("fire_sprinkler_factor") * pl.col("weighted_bi_waiting_period_factor") *
                pl.col("weighted_bi_indemnity_period") * pl.col("cbi") * pl.col("fire_size_discount_factor")).fill_null(0).fill_nan(0).alias("total_modifier_impact"),
            pl.col("base_rate").alias("occupancy")
        ]
    )

    # GU Tech Rate, Tech Rate, UW Tech Rate, UW Tech Prem
    df = df.with_columns(
        [
            (pl.col("base_rate") * pl.col("total_modifier_impact") * pl.col(f"fire_gg_technical_prem_final_pre_uw_layer{index}") /
                pl.col(f"fire_total_expected_loss_pre_uw_layer{index}")).fill_nan(0).alias("gu_tech_rate"),
            (pl.col(f"fire_worth_percent_layer{index}")).alias("worth"),
            (pl.col(f"fire_gg_technical_prem_final_pre_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("tech_rate"),
            (pl.col(f"fire_gg_technical_prem_final_post_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("uw_adj_tech_rate"),
            pl.col(f"fire_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0).alias("uw_adj_tech_prem")
        ]
    )

    df_layer = df[[
        "country", "state", "county", "zip", "tiv_buildings_usd", 
        "tiv_contents_total_usd", "tiv_bi_usd", "tiv_total_usd", "itv",
        "base_rate", "occupancy", "fire_construction_factor", "fire_sprinkler_factor",
        "fire_pc_code_factor", "fire_size_discount_factor", "fire_mexican_fonden_factor", "weighted_bi_waiting_period_factor", 
        "weighted_bi_indemnity_period", "cbi", "total_modifier_impact", "gu_tech_rate", "worth",
        "tech_rate", "uw_adj_tech_rate", "uw_adj_tech_prem"
        ]]

    df_layer = df_layer.rename({
        "tiv_buildings_usd": "tiv_buildings", "tiv_contents_total_usd": "tiv_contents_total", "tiv_bi_usd": "tiv_bi", "tiv_total_usd": "tiv_total",
        "fire_construction_factor": "construction", "fire_pc_code_factor": "pc_code",
        "fire_sprinkler_factor": "sprinkler", "fire_size_discount_factor": "fire_size_discount","fire_mexican_fonden_factor": "mexican_fonden",
        "weighted_bi_waiting_period_factor": "bi_waiting_period",
        "weighted_bi_indemnity_period": "bi_indemnity_period"
        })

    df_layer_tiv = df_layer.sort("tiv_total", descending=True).head(20)
    df_layer_rate = df_layer.sort("uw_adj_tech_prem", descending=True).head(20)

    other_data[f"fire_top_20_locations_summary_layer{index}_tiv"] = df_layer_tiv.to_dicts()
    other_data[f"fire_top_20_locations_summary_layer{index}_rate"] = df_layer_rate.to_dicts()
    
