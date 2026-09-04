import hx
import polars as pl
import numpy as np


def remove_inf_from_dict(dictionary, replace_with=0):
    for key, value in dictionary.items():
        if value == np.inf:
            dictionary[key] = replace_with

    return dictionary

def scs_analysis_summary(hxd, df, other_data):
    summary_lists = {
        "risk_category_summary": [],
        "construction_summary": [],
        "occupancy_summary": []
    }

    for index, layer in enumerate(hxd.layers, start=1):
        modifier_summary_df = create_modifier_summary_df(hxd, df, other_data, index)
        scs_modifier_summary_assigns(hxd, modifier_summary_df, other_data, layer, index)

        zipped_tables = zip(
            (
                "risk_level_scs", 
                "constr_name", 
                "occupancy"
            ), 
            (
                "risk_category_summary", 
                "construction_summary", 
                "occupancy_summary"
            )
        )
        
        for groupby_column, key in zipped_tables:
            adjustment_summaries = adjustment_summary(hxd, modifier_summary_df, groupby_column)
            summary_lists[key] = [remove_inf_from_dict(x) for x in adjustment_summaries]

        other_data[f"scs_risk_category_summary_layer{index}"] = summary_lists['risk_category_summary']
        other_data[f"scs_construction_summary_layer{index}"] = summary_lists['construction_summary']
        other_data[f"scs_occupancy_summary_layer{index}"] = summary_lists['occupancy_summary']

        display_scs_top_20_locations_summary(hxd, df, other_data, index, layer)

    return df

def create_modifier_summary_df(hxd, df, other_data, index):
    # Calculate the sum product per layer
    modifier_summary_df = df[[
        "tiv_buildings", 
        "tiv_contents_total", 
        "tiv_bi", 
        "tiv_total",

        "tiv_total_usd",
        "tiv_buildings_usd", 
        "tiv_contents_total_usd", 
        "tiv_bi_usd",
        "floor_area",

        f"tornado_buildings_base_rate_layer{index}",
        f"tornado_contents_base_rate_layer{index}",
        f"tornado_bi_base_rate_layer{index}",
        f"tornado_total_base_rate_layer{index}",

        "tornado_occupancy_load", 
        "tornado_construction_load", 
        "tornado_year_built_load",
        "tornado_catnet_score_load",
        "tornado_size_discount_load",

        f"hail_buildings_base_rate_layer{index}",
        f"hail_contents_base_rate_layer{index}",
        f"hail_bi_base_rate_layer{index}",
        f"hail_total_base_rate_layer{index}",
        
        "hail_occupancy_load",
        "hail_construction_load",
        "hail_year_built_load",
        "hail_floor_area_load",
        "hail_roof_age_load",
        "hail_roof_covering_load",
        "hail_roof_geometry_load",
        "hail_catnet_score_load",
        "hail_size_discount_load",

        "risk_level_scs", 
        "constr_name", 
        "occupancy",

        f"hail_us_gg_technical_prem_final_pre_uw_layer{index}",
        f"hail_us_gg_technical_prem_final_post_uw_layer{index}",
        f"hail_us_total_expected_loss_pre_uw_layer{index}",

        f"hail_intl_gg_technical_prem_final_pre_uw_layer{index}",
        f"hail_intl_gg_technical_prem_final_post_uw_layer{index}",
        f"hail_intl_total_expected_loss_pre_uw_layer{index}",

        f"tornado_us_gg_technical_prem_final_pre_uw_layer{index}",
        f"tornado_us_gg_technical_prem_final_post_uw_layer{index}",
        f"tornado_us_total_expected_loss_pre_uw_layer{index}",

        f"tornado_intl_gg_technical_prem_final_pre_uw_layer{index}",
        f"tornado_intl_gg_technical_prem_final_post_uw_layer{index}",
        f"tornado_intl_total_expected_loss_pre_uw_layer{index}",

        f"hail_worth_percent_layer{index}",
        f"tornado_worth_percent_layer{index}",
        ]]
    
    factors = ["base", "occupancy", "construction", "year_built", "floor_area", "roof_age", "roof_covering", "roof_geometry", "catnet_score", "size_discount"]
    hail_only = ["floor_area", "roof_age", "roof_covering", "roof_geometry"]
    
    modifier_summary_df = create_base_factors(modifier_summary_df, index)

    for i in range(len(factors) - 1):
        skip_tornado = factors[i+1] in hail_only
        modifier_summary_df = multiply_on_next_factor(modifier_summary_df, factors[i], factors[i+1], skip_tornado=skip_tornado)
    
    modifier_summary_df = modifier_summary_df.rename({
        f"hail_us_gg_technical_prem_final_pre_uw_layer{index}": "hail_us_gg_technical_prem_pre_uw",
        f"hail_us_gg_technical_prem_final_post_uw_layer{index}": "hail_us_gg_technical_prem_post_uw",
        f"hail_us_total_expected_loss_pre_uw_layer{index}": "hail_us_total_expected_loss_pre_uw",
        f"hail_intl_gg_technical_prem_final_pre_uw_layer{index}": "hail_intl_gg_technical_prem_pre_uw",
        f"hail_intl_gg_technical_prem_final_post_uw_layer{index}": "hail_intl_gg_technical_prem_post_uw",
        f"hail_intl_total_expected_loss_pre_uw_layer{index}": "hail_intl_total_expected_loss_pre_uw",
        f"tornado_us_gg_technical_prem_final_pre_uw_layer{index}": "tornado_us_gg_technical_prem_pre_uw",
        f"tornado_us_gg_technical_prem_final_post_uw_layer{index}": "tornado_us_gg_technical_prem_post_uw",
        f"tornado_us_total_expected_loss_pre_uw_layer{index}": "tornado_us_total_expected_loss_pre_uw",
        f"tornado_intl_gg_technical_prem_final_pre_uw_layer{index}": "tornado_intl_gg_technical_prem_pre_uw",
        f"tornado_intl_gg_technical_prem_final_post_uw_layer{index}": "tornado_intl_gg_technical_prem_post_uw",
        f"tornado_intl_total_expected_loss_pre_uw_layer{index}": "tornado_intl_total_expected_loss_pre_uw",
        f"hail_worth_percent_layer{index}": "hail_worth",
        f"tornado_worth_percent_layer{index}": "tornado_worth",
    })

    return modifier_summary_df



def scs_modifier_summary_assigns(hxd, modifier_summary_df, other_data, layer, index):
    # Assign to Modifier Summary
    modifier_summary_dict = {}

    modifier_summary_dict["peril_name"] = "SCS"
    modifier_summary_dict["num_locs"] = len(modifier_summary_df)

    modifier_summary_assign_df = calculate_tech_rates(hxd, modifier_summary_df)

    modifier_summary_dict["sum_tiv_total_usd"] = modifier_summary_assign_df["sum_tiv_total_usd"]
    modifier_summary_dict["occupancy"] = modifier_summary_assign_df["occupancy"]
    modifier_summary_dict["construction"] = modifier_summary_assign_df["construction"]
    modifier_summary_dict["year_built"] = modifier_summary_assign_df["year_built"]
    modifier_summary_dict["floor_area"] = modifier_summary_assign_df["floor_area"]
    modifier_summary_dict["roof_age"] = modifier_summary_assign_df["roof_age"]
    modifier_summary_dict["roof_covering"] = modifier_summary_assign_df["roof_covering"]
    modifier_summary_dict["roof_geometry"] = modifier_summary_assign_df["roof_geometry"]
    modifier_summary_dict["catnet_score"] = modifier_summary_assign_df["catnet_score"]
    modifier_summary_dict["size_discount"] = modifier_summary_assign_df["size_discount"]
    modifier_summary_dict["total_modifier_impact"] = modifier_summary_assign_df["total_modifier_impact"]
    modifier_summary_dict["worth"] = modifier_summary_assign_df["worth"]
    # modifier_summary_dict["worth"] = modifier_summary_assign_df["tech_rate"]/modifier_summary_assign_df["gu_tech_rate"] if modifier_summary_assign_df["gu_tech_rate"] else 0
    modifier_summary_dict["gu_tech_rate"] = modifier_summary_assign_df["gu_tech_rate"]
    modifier_summary_dict["tech_rate"] = modifier_summary_assign_df["tech_rate"]
    modifier_summary_dict["uw_adj_tech_rate"] = modifier_summary_assign_df["uw_adj_tech_rate"]
    modifier_summary_dict["uw_adj_tech_prem"] = modifier_summary_assign_df["uw_adj_tech_prem"]
    modifier_summary_dict["gu_loss"] = modifier_summary_assign_df["gu_loss"]

    other_data[f"scs_modifier_summary_layer{index}"] = modifier_summary_dict


def calculate_tech_rates(hxd, modifier_summary_df):
    tech_rate_dict = {}

    prod_sums = {}
    factors = ["base", "occupancy", "construction", "year_built", "floor_area", "roof_age", "roof_covering", "roof_geometry", "catnet_score", "size_discount"]
    for factor in factors:
        prod_sums[factor] = modifier_summary_df[f"scs_total_cumprod_{factor}"].sum()

    sum_tiv_total_usd = modifier_summary_df["tiv_total_usd"].sum()
    sum_tiv_total = modifier_summary_df[['tiv_total']].sum().sum(axis=1).item()
    sum_tiv_buildings = modifier_summary_df[['tiv_buildings']].sum().sum(axis=1).item()

    tech_rate_dict["total_modifier_impact"] = 1
    for i in range(len(factors) - 1):
        tech_rate_dict[factors[i+1]] = prod_sums[factors[i+1]] / prod_sums[factors[i]] if prod_sums[factors[i]] != 0 else 0
        tech_rate_dict["total_modifier_impact"] *= tech_rate_dict[factors[i+1]]

    # To be confirmed: worth change to weighted average on total_tiv
    # Also confirm SCS handling
    cum_prod_worth = modifier_summary_df.select(pl.col(f"hail_worth") * pl.col("tiv_total_usd"))[f"hail_worth"].sum() + modifier_summary_df.select(pl.col(f"tornado_worth") * pl.col("tiv_total_usd"))[f"tornado_worth"].sum()
    tech_rate_dict["worth"] = cum_prod_worth / (2 * sum_tiv_total_usd) if sum_tiv_total_usd else 0 
    
    # GU Tech Rate, Tech Rate, UW Tech Rate, UW Tech Prem
    scs_gg_technical_prem_final_pre_uw = (
        (modifier_summary_df["hail_us_gg_technical_prem_pre_uw"].fill_nan(0).sum() or 0) +
        (modifier_summary_df["hail_intl_gg_technical_prem_pre_uw"].fill_nan(0).sum() or 0) +
        (modifier_summary_df["tornado_us_gg_technical_prem_pre_uw"].fill_nan(0).sum() or 0) +
        (modifier_summary_df["tornado_intl_gg_technical_prem_pre_uw"].fill_nan(0).sum() or 0) 
    )
    scs_gg_technical_prem_final_post_uw = (
        (modifier_summary_df["hail_us_gg_technical_prem_post_uw"].fill_nan(0).sum() or 0) + 
        (modifier_summary_df["hail_intl_gg_technical_prem_post_uw"].fill_nan(0).sum() or 0) + 
        (modifier_summary_df["tornado_us_gg_technical_prem_post_uw"].fill_nan(0).sum() or 0) + 
        (modifier_summary_df["tornado_intl_gg_technical_prem_post_uw"].fill_nan(0).sum() or 0)
    )
    scs_total_expected_loss_pre_uw_sum = (
        (modifier_summary_df["hail_us_total_expected_loss_pre_uw"].sum() or 0) + 
        (modifier_summary_df["hail_intl_total_expected_loss_pre_uw"].sum() or 0) + 
        (modifier_summary_df["tornado_us_total_expected_loss_pre_uw"].sum() or 0) + 
        (modifier_summary_df["tornado_intl_total_expected_loss_pre_uw"].sum() or 0)
    )
    
    total_floor_area = modifier_summary_df.filter(pl.col('tiv_buildings') != 0) ['floor_area'].fill_null(0).sum() or 0

    tech_rate_dict["gu_tech_rate"] = (
        (
            (prod_sums['catnet_score'] / prod_sums['base']) * # total modifier impact
            (prod_sums['base'] / sum_tiv_total_usd) * # base rate
            scs_gg_technical_prem_final_pre_uw
        ) / scs_total_expected_loss_pre_uw_sum
        if scs_total_expected_loss_pre_uw_sum else 0  
        )

    tech_rate_dict["tech_rate"] = scs_gg_technical_prem_final_pre_uw / sum_tiv_total_usd if sum_tiv_total_usd else 0
    tech_rate_dict["tech_prem"] = scs_gg_technical_prem_final_pre_uw
    tech_rate_dict["uw_adj_tech_rate"] = scs_gg_technical_prem_final_post_uw / sum_tiv_total_usd if sum_tiv_total_usd else 0
    tech_rate_dict["uw_adj_tech_prem"] = scs_gg_technical_prem_final_post_uw
    tech_rate_dict["gu_loss"] = scs_total_expected_loss_pre_uw_sum
    tech_rate_dict["gu_prem"] = (
            (prod_sums['catnet_score'] / prod_sums['base']) * 
            (prod_sums['base'] / sum_tiv_total_usd) * 
            sum_tiv_total_usd
        ) if prod_sums['base'] and sum_tiv_total_usd else 0  # TODO: check this formula - it doesn't look right

    tech_rate_dict["sum_tiv_total_usd"] = sum_tiv_total_usd
    tech_rate_dict['sum_tiv_total'] = sum_tiv_total
    tech_rate_dict["itv"] = sum_tiv_buildings / total_floor_area if total_floor_area else 0

    return tech_rate_dict

def adjustment_summary(hxd, modifier_summary_df, groupby_column):
    results_list = []

    # Calculate the sum product per layer
    for name, data in modifier_summary_df.groupby(groupby_column):

        grouping_dict = calculate_tech_rates(hxd, data)

        results_list.append({
            "name": name,
            "num_locations": len(data),
            "tiv": grouping_dict["sum_tiv_total_usd"],
            "worth": grouping_dict["worth"],
            # "worth": grouping_dict["tech_rate"]/grouping_dict["gu_tech_rate"] if grouping_dict["gu_tech_rate"] else 0,
            "gu_tech_rate": grouping_dict["gu_tech_rate"],
            "tech_rate": grouping_dict["tech_rate"],
            "tech_prem": grouping_dict["tech_prem"],
            "uw_adj_tech_rate": grouping_dict["uw_adj_tech_rate"],
            "uw_adj_tech_prem": grouping_dict["uw_adj_tech_prem"],
            "gu_loss": grouping_dict["gu_loss"],
            "gu_prem": grouping_dict["gu_prem"],
            "itv": grouping_dict["itv"],
        })

    # Assign to hxd
    return results_list



def display_scs_top_20_locations_summary(hxd, df, other_data, index, layer):
    factors = ["base", "occupancy", "construction", "year_built", "floor_area", "roof_age", "roof_covering", "roof_geometry", "catnet_score", "size_discount"]
    hail_only = ["floor_area", "roof_age", "roof_covering", "roof_geometry"]

    df = create_base_factors(df, index)

    for i in range(len(factors) - 1):
        skip_tornado = factors[i+1] in hail_only
        df = multiply_on_next_factor(df, factors[i], factors[i+1], skip_tornado=skip_tornado)

    df = df.with_columns(
        (
            pl.col(f"hail_total_base_rate_layer{index}").fill_nan(0) +
            pl.col(f"tornado_total_base_rate_layer{index}").fill_nan(0)
        ).alias(f"scs_total_base_rate"),
        (
            (pl.col("scs_total_cumprod_catnet_score") / pl.col("scs_total_cumprod_base")).fill_nan(0)
        ).alias(f"scs_total_modifier_impact"),
        (
            pl.col(f"hail_us_total_expected_loss_pre_uw_layer{index}") +
            pl.col(f"hail_intl_total_expected_loss_pre_uw_layer{index}") +
            pl.col(f"tornado_us_total_expected_loss_pre_uw_layer{index}") +
            pl.col(f"tornado_intl_total_expected_loss_pre_uw_layer{index}")
        ).alias(f"scs_total_expected_loss_pre_uw_layer{index}"),
        (
            pl.col(f"hail_us_gg_technical_prem_final_pre_uw_layer{index}").fill_nan(0) +
            pl.col(f"hail_intl_gg_technical_prem_final_pre_uw_layer{index}").fill_nan(0) +
            pl.col(f"tornado_us_gg_technical_prem_final_pre_uw_layer{index}").fill_nan(0) +
            pl.col(f"tornado_intl_gg_technical_prem_final_pre_uw_layer{index}").fill_nan(0)
        ).alias(f"scs_gg_technical_prem_final_pre_uw_layer{index}"),
        (
            pl.col(f"hail_us_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0) +
            pl.col(f"hail_intl_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0) +
            pl.col(f"tornado_us_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0) +
            pl.col(f"tornado_intl_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0)
        ).alias(f"scs_gg_technical_prem_final_post_uw_layer{index}"),
        (pl.col("tiv_buildings") / pl.col("floor_area")).fill_nan(0).alias("itv"),
    )

    # Replace inf values
    df = df.with_columns(
        pl.when(pl.col("itv") == float('inf'))
        .then(0)
        .otherwise(pl.col("itv"))
        .alias("itv")
    )

    # Weighted Base Rate
    df = df.with_columns(
        (
            (
                pl.col("tiv_buildings_usd") * pl.col(f'tornado_buildings_base_rate_layer{index}') + 
                pl.col("tiv_contents_total_usd") * pl.col(f'tornado_contents_base_rate_layer{index}') +
                pl.col("tiv_bi_usd") * pl.col(f'tornado_bi_base_rate_layer{index}') + 
                pl.col("tiv_buildings_usd") * pl.col(f'hail_buildings_base_rate_layer{index}') + 
                pl.col("tiv_contents_total_usd") * pl.col(f'hail_contents_base_rate_layer{index}') +
                pl.col("tiv_bi_usd") * pl.col(f'hail_bi_base_rate_layer{index}')
            ) / (pl.col("tiv_buildings_usd") + pl.col("tiv_contents_total_usd") + pl.col("tiv_bi_usd"))
        ).alias("scs_base_rate")
    )

    # GU Tech Rate, Tech Rate, UW Tech Rate, UW Tech Prem
    df = df.with_columns(
        [
            (pl.col("scs_base_rate") * pl.col("scs_total_modifier_impact") * pl.col(f"scs_gg_technical_prem_final_pre_uw_layer{index}") /
                pl.col(f"scs_total_expected_loss_pre_uw_layer{index}")).fill_nan(0).alias("gu_tech_rate"),
            (pl.col(f"scs_gg_technical_prem_final_pre_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("tech_rate"),
            (pl.col(f"scs_gg_technical_prem_final_post_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("uw_adj_tech_rate"),
            pl.col(f"scs_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0).alias("uw_adj_tech_prem")
        ]
    )

    factors = ["base", "occupancy", "construction", "year_built", "floor_area", "roof_age", "roof_covering", "roof_geometry", "catnet_score", "size_discount"]
    hail_only = ["floor_area", "roof_age", "roof_covering", "roof_geometry"] 

    df = df.with_columns(
        pl.col(f"hail_total_base_rate_layer{index}").alias(f"hail_total_cumprod_base"),
        pl.col(f"tornado_total_base_rate_layer{index}").alias(f"tornado_total_cumprod_base"),
        pl.col("scs_total_base_rate").alias(f"scs_total_cumprod_base"),
    )

    for i in range(len(factors) - 1):
        skip_tornado = factors[i+1] in hail_only
        df = multiply_on_next_factor(df, factors[i], factors[i+1], skip_tornado=skip_tornado)

    for i in range(len(factors) - 1):
        df = df.with_columns(
            pl.when(pl.col(f"scs_total_cumprod_{factors[i]}") == 0).then(0).otherwise(pl.col(f"scs_total_cumprod_{factors[i+1]}") / pl.col(f"scs_total_cumprod_{factors[i]}")).alias(f"scs_{factors[i+1]}_load")
        )

    df = df.with_columns(
        # pl.when(pl.col("gu_tech_rate") == 0).then(pl.lit(0)).otherwise(pl.col("tech_rate")/pl.col("gu_tech_rate")).alias("worth")
        ((pl.col(f"hail_worth_percent_layer{index}") + pl.col(f"tornado_worth_percent_layer{index}")) / 2).alias("worth")
    )

    df_layer = df[
        [
            "country", 
            "state", 
            "county", 
            "zip", 
            "tiv_buildings_usd", 
            "tiv_contents_total_usd", 
            "tiv_bi_usd",
            "tiv_total_usd", 
            "itv",
            "scs_total_base_rate",
            "worth",
            "scs_total_modifier_impact",
            "gu_tech_rate", 
            "tech_rate", 
            "uw_adj_tech_rate", 
            "uw_adj_tech_prem"
        ] + [f"scs_{factor}_load" for factor in factors if factor != "base"]
        ]

    df_layer = df_layer.rename({
        "tiv_buildings_usd": "tiv_buildings",
        "tiv_contents_total_usd": "tiv_contents_total",
        "tiv_bi_usd": "tiv_bi",
        "tiv_total_usd": "tiv_total",
        "scs_total_base_rate": "base_rate",
        "scs_roof_age_load": "roof_age", 
        "scs_roof_covering_load": "roof_covering", 
        "scs_roof_geometry_load": "roof_geometry",
        "scs_catnet_score_load": "catnet_score",
        "scs_occupancy_load": "occupancy", 
        "scs_construction_load": "construction", 
        "scs_year_built_load": "year_built", 
        "scs_floor_area_load": "floor_area",
        "scs_size_discount_load": "size_discount",
        "scs_total_modifier_impact": "total_modifier_impact"
        })

    df_layer_tiv = df_layer.sort("tiv_total", descending=True).head(20)
    df_layer_rate = df_layer.sort("uw_adj_tech_prem", descending=True).head(20)

    other_data[f"scs_top_20_locations_summary_layer{index}_tiv"] = df_layer_tiv.to_dicts()
    other_data[f"scs_top_20_locations_summary_layer{index}_rate"] = df_layer_rate.to_dicts()

    return df


def multiply_on_next_factor(modifier_summary_df, previous_factor, new_factor, skip_tornado=False):
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col(f"hail_total_cumprod_{previous_factor}") * pl.col(f"hail_{new_factor}_load")).alias(f"hail_total_cumprod_{new_factor}"),
    )

    if skip_tornado:
        modifier_summary_df = modifier_summary_df.with_columns(
            pl.col(f"tornado_total_cumprod_{previous_factor}").alias(f"tornado_total_cumprod_{new_factor}"),
        )
        modifier_summary_df = modifier_summary_df.with_columns(
            (pl.col(f"tornado_total_cumprod_{new_factor}") + pl.col(f"hail_total_cumprod_{new_factor}")).alias(f"scs_total_cumprod_{new_factor}"),
        )

    else:
        modifier_summary_df = modifier_summary_df.with_columns(
            (pl.col(f"tornado_total_cumprod_{previous_factor}") * pl.col(f"tornado_{new_factor}_load")).alias(f"tornado_total_cumprod_{new_factor}"),
        )
        modifier_summary_df = modifier_summary_df.with_columns(
            (pl.col(f"tornado_total_cumprod_{new_factor}") + pl.col(f"hail_total_cumprod_{new_factor}")).alias(f"scs_total_cumprod_{new_factor}"),
        )

    return modifier_summary_df

def create_base_factors(modifier_summary_df, index):
    # Base
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("tiv_buildings_usd") * pl.col(f"tornado_buildings_base_rate_layer{index}")).alias("tornado_buildings_cumprod_base"),
        (pl.col("tiv_contents_total_usd") * pl.col(f"tornado_contents_base_rate_layer{index}")).alias("tornado_contents_total_cumprod_base"),
        (pl.col("tiv_bi_usd") * pl.col(f"tornado_bi_base_rate_layer{index}")).alias("tornado_bi_cumprod_base"),

        (pl.col("tiv_buildings_usd") * pl.col(f"hail_buildings_base_rate_layer{index}")).alias("hail_buildings_cumprod_base"),
        (pl.col("tiv_contents_total_usd") * pl.col(f"hail_contents_base_rate_layer{index}")).alias("hail_contents_total_cumprod_base"),
        (pl.col("tiv_bi_usd") * pl.col(f"hail_bi_base_rate_layer{index}")).alias("hail_bi_cumprod_base"),
    )
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("tornado_buildings_cumprod_base") + pl.col("hail_buildings_cumprod_base")).alias("scs_buildings_cumprod_base"),
        (pl.col("tornado_contents_total_cumprod_base") + pl.col("hail_contents_total_cumprod_base")).alias("scs_contents_total_cumprod_base"),
        (pl.col("tornado_bi_cumprod_base") + pl.col("hail_bi_cumprod_base")).alias("scs_bi_cumprod_base"),
    )
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("hail_buildings_cumprod_base") + pl.col("hail_contents_total_cumprod_base") + pl.col("hail_bi_cumprod_base")).alias("hail_total_cumprod_base"),
        (pl.col("tornado_buildings_cumprod_base") + pl.col("tornado_contents_total_cumprod_base") + pl.col("tornado_bi_cumprod_base")).alias("tornado_total_cumprod_base"),
        (pl.col("scs_buildings_cumprod_base") + pl.col("scs_contents_total_cumprod_base") + pl.col("scs_bi_cumprod_base")).alias("scs_total_cumprod_base")
    )

    return modifier_summary_df