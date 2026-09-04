import hx
import polars as pl
import numpy as np


def remove_inf_from_dict(dictionary, replace_with=0):
    for key, value in dictionary.items():
        if value == np.inf:
            dictionary[key] = replace_with

    return dictionary

def wildfire_analysis_summary(hxd, df, other_data):
    summary_lists = {
        "risk_category_summary": [],
        "construction_summary": [],
        "occupancy_summary": []
    }

    for index, layer in enumerate(hxd.layers, start=1):
        modifier_summary_df = create_modifier_summary_df(hxd, df, other_data, index)
        wildfire_modifier_summary_assigns(hxd, modifier_summary_df, other_data, layer, index)

        zipped_tables = zip(
            (
                "wildfire_category", 
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

        other_data[f"wf_risk_category_summary_layer{index}"] = summary_lists['risk_category_summary']
        other_data[f"wf_construction_summary_layer{index}"] = summary_lists['construction_summary']
        other_data[f"wf_occupancy_summary_layer{index}"] = summary_lists['occupancy_summary']

        wildfire_top_20_locations_summary(hxd, df, other_data, index, layer)

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

        "wildfire_occupancy_load", 
        "wildfire_construction_load", 
        "wildfire_pc_code_load",
        "wildfire_catnet_score_load",
        "wildfire_size_discount_load",
        "bi_waiting_period_factor",
        "wildfire_total_modifier_impact",

        f'wildfire_buildings_base_rate_layer{index}', 
        f'wildfire_contents_base_rate_layer{index}', 
        f'wildfire_bi_base_rate_layer{index}', 
        f'wildfire_total_base_rate_layer{index}',

        "wildfire_category", 
        "constr_name", 
        "occupancy",

        f"wildfire_us_gg_technical_prem_final_pre_uw_layer{index}",
        f"wildfire_us_gg_technical_prem_final_post_uw_layer{index}",
        f"wildfire_us_total_expected_loss_pre_uw_layer{index}",

        f"wildfire_intl_gg_technical_prem_final_pre_uw_layer{index}",
        f"wildfire_intl_gg_technical_prem_final_post_uw_layer{index}",
        f"wildfire_intl_total_expected_loss_pre_uw_layer{index}",

        f"wildfire_worth_percent_layer{index}"
        ]]
    
    # Base
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("tiv_buildings_usd") * pl.col(f'wildfire_buildings_base_rate_layer{index}')).alias("buildings_cumprod"),
        (pl.col("tiv_contents_total_usd") * pl.col(f'wildfire_contents_base_rate_layer{index}')).alias("contents_total_cumprod"),
        (pl.col("tiv_bi_usd") * pl.col(f'wildfire_bi_base_rate_layer{index}')).alias("bi_cumprod"),
    )
    # Occupancy
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("tiv_buildings_usd") * pl.col(f'wildfire_buildings_base_rate_layer{index}') * pl.col('wildfire_occupancy_load')).alias("buildings_cumprod_occupancy"),
        (pl.col("tiv_contents_total_usd") * pl.col(f'wildfire_contents_base_rate_layer{index}') * pl.col('wildfire_occupancy_load')).alias("contents_total_cumprod_occupancy"),
        (pl.col("tiv_bi_usd") * pl.col(f'wildfire_bi_base_rate_layer{index}') * pl.col('wildfire_occupancy_load')).alias("bi_cumprod_occupancy")
    )
    # Construction
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("tiv_buildings_usd") * pl.col(f'wildfire_buildings_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load')).alias("buildings_cumprod_construction"),
        (pl.col("tiv_contents_total_usd") * pl.col(f'wildfire_contents_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load')).alias("contents_total_cumprod_construction"),
        (pl.col("tiv_bi_usd") * pl.col(f'wildfire_bi_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load')).alias("bi_cumprod_construction")
    )
    # PC Code
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("tiv_buildings_usd") * pl.col(f'wildfire_buildings_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load')).alias("buildings_cumprod_pc"),
        (pl.col("tiv_contents_total_usd") * pl.col(f'wildfire_contents_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load')).alias("contents_total_cumprod_pc"),
        (pl.col("tiv_bi_usd") * pl.col(f'wildfire_bi_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load')).alias("bi_cumprod_pc")
    )
    # Catnet
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("tiv_buildings_usd") * pl.col(f'wildfire_buildings_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load') * pl.col('wildfire_catnet_score_load')).alias("buildings_cumprod_catnet"),
        (pl.col("tiv_contents_total_usd") * pl.col(f'wildfire_contents_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load') * pl.col('wildfire_catnet_score_load')).alias("contents_total_cumprod_catnet"),
        (pl.col("tiv_bi_usd") * pl.col(f'wildfire_bi_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load') * pl.col('wildfire_catnet_score_load')).alias("bi_cumprod_catnet")
    )
    # Size Discount
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("tiv_buildings_usd") * pl.col(f'wildfire_buildings_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load') * pl.col('wildfire_catnet_score_load') * pl.col('wildfire_size_discount_load')).alias("buildings_cumprod_size_discount"),
        (pl.col("tiv_contents_total_usd") * pl.col(f'wildfire_contents_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load') * pl.col('wildfire_catnet_score_load')* pl.col('wildfire_size_discount_load')).alias("contents_total_cumprod_size_discount"),
        (pl.col("tiv_bi_usd") * pl.col(f'wildfire_bi_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load') * pl.col('wildfire_catnet_score_load')* pl.col('wildfire_size_discount_load')).alias("bi_cumprod_size_discount")
    )

    # BI Waiting Period 
    modifier_summary_df = modifier_summary_df.with_columns(
        (pl.col("tiv_buildings_usd") * pl.col(f'wildfire_buildings_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load') * pl.col('wildfire_catnet_score_load') * pl.col('wildfire_size_discount_load')).alias("buildings_cumprod_bi_waiting_period"),
        (pl.col("tiv_contents_total_usd") * pl.col(f'wildfire_contents_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load') * pl.col('wildfire_catnet_score_load')* pl.col('wildfire_size_discount_load')).alias("contents_total_cumprod_bi_waiting_period"),
        (pl.col("tiv_bi_usd") * pl.col(f'wildfire_bi_base_rate_layer{index}') * pl.col('wildfire_occupancy_load') * pl.col('wildfire_construction_load') * pl.col('wildfire_pc_code_load') * pl.col('wildfire_catnet_score_load')* pl.col('wildfire_size_discount_load') * pl.col("bi_waiting_period_factor")).alias("bi_cumprod_bi_waiting_period")
    )

    modifier_summary_df = modifier_summary_df.rename({
        f"wildfire_us_gg_technical_prem_final_pre_uw_layer{index}": "wildfire_us_gg_technical_prem_pre_uw",
        f"wildfire_us_gg_technical_prem_final_post_uw_layer{index}": "wildfire_us_gg_technical_prem_post_uw",
        f"wildfire_us_total_expected_loss_pre_uw_layer{index}": "wildfire_us_total_expected_loss_pre_uw",
        f"wildfire_intl_gg_technical_prem_final_pre_uw_layer{index}": "wildfire_intl_gg_technical_prem_pre_uw",
        f"wildfire_intl_gg_technical_prem_final_post_uw_layer{index}": "wildfire_intl_gg_technical_prem_post_uw",
        f"wildfire_intl_total_expected_loss_pre_uw_layer{index}": "wildfire_intl_total_expected_loss_pre_uw",
        f"wildfire_worth_percent_layer{index}": "wildfire_worth" 
    })

    return modifier_summary_df

def wildfire_modifier_summary_assigns(hxd, modifier_summary_df, other_data, layer, index):
    # Assign to Modifier Summary
    modifier_summary_dict = {}

    modifier_summary_dict["peril_name"] = "Wildfire"
    modifier_summary_dict["num_locs"] = len(modifier_summary_df)

    modifier_summary_assign_df = calculate_tech_rates(hxd, modifier_summary_df)

    modifier_summary_dict["sum_tiv_total_usd"] = modifier_summary_assign_df["sum_tiv_total_usd"]
    modifier_summary_dict["occupancy"] = modifier_summary_assign_df['occupancy']
    modifier_summary_dict["construction"] = modifier_summary_assign_df['construction']
    modifier_summary_dict["pc_code"] = modifier_summary_assign_df['pc_code']
    modifier_summary_dict["catnet_score"] = modifier_summary_assign_df['catnet_score']
    modifier_summary_dict["size_discount"] = modifier_summary_assign_df['size_discount']
    modifier_summary_dict["bi_waiting_period"] = modifier_summary_assign_df['bi_waiting_period']
    modifier_summary_dict["total_modifier_impact"] = modifier_summary_assign_df['total_modifier_impact']
    # modifier_summary_dict["worth"] = modifier_summary_assign_df["tech_rate"]/modifier_summary_assign_df["gu_tech_rate"] if modifier_summary_assign_df["gu_tech_rate"] else 0
    modifier_summary_dict["worth"] = modifier_summary_assign_df['worth']
    modifier_summary_dict["gu_tech_rate"] = modifier_summary_assign_df['gu_tech_rate']
    modifier_summary_dict["tech_rate"] = modifier_summary_assign_df['tech_rate']
    modifier_summary_dict["uw_adj_tech_rate"] = modifier_summary_assign_df['uw_adj_tech_rate']
    modifier_summary_dict["uw_adj_tech_prem"] = modifier_summary_assign_df['uw_adj_tech_prem']
    modifier_summary_dict["gu_loss"] = modifier_summary_assign_df['gu_loss']

    other_data[f"wf_modifier_summary_layer{index}"] = modifier_summary_dict

def calculate_tech_rates(hxd, modifier_summary_df):
    tech_rate_dict = {}

    prod_sum_base = modifier_summary_df[['buildings_cumprod', 'contents_total_cumprod', 'bi_cumprod']].sum().sum(axis=1).item()
    prod_sum_occupancy = modifier_summary_df[['buildings_cumprod_occupancy', 'contents_total_cumprod_occupancy', 'bi_cumprod_occupancy']].sum().sum(axis=1).item()
    prod_sum_construction = modifier_summary_df[['buildings_cumprod_construction', 'contents_total_cumprod_construction', 'bi_cumprod_construction']].sum().sum(axis=1).item()
    prod_sum_pc = modifier_summary_df[['buildings_cumprod_pc', 'contents_total_cumprod_pc', 'bi_cumprod_pc']].sum().sum(axis=1).item()
    prod_sum_catnet = modifier_summary_df[['buildings_cumprod_catnet', 'contents_total_cumprod_catnet', 'bi_cumprod_catnet']].sum().sum(axis=1).item()
    prod_sum_size_discount = modifier_summary_df[['buildings_cumprod_size_discount', 'contents_total_cumprod_size_discount', 'bi_cumprod_size_discount']].sum().sum(axis=1).item()
    prod_sum_bi_waiting_period = modifier_summary_df[['buildings_cumprod_bi_waiting_period', 'contents_total_cumprod_bi_waiting_period', 'bi_cumprod_bi_waiting_period']].sum().sum(axis=1).item()

    sum_tiv_total_usd = modifier_summary_df[['tiv_total_usd']].sum().sum(axis=1).item()
    sum_tiv_total = modifier_summary_df[['tiv_total']].sum().sum(axis=1).item()
    sum_tiv_buildings = modifier_summary_df[['tiv_buildings']].sum().sum(axis=1).item()

    tech_rate_dict['occupancy'] = prod_sum_occupancy / prod_sum_base if prod_sum_base != 0 else 0
    tech_rate_dict['construction'] = prod_sum_construction / prod_sum_occupancy if prod_sum_occupancy != 0 else 0
    tech_rate_dict['pc_code'] = prod_sum_pc / prod_sum_construction if prod_sum_construction != 0 else 0
    tech_rate_dict['catnet_score'] = prod_sum_catnet / prod_sum_pc if prod_sum_pc != 0 else 0
    tech_rate_dict['size_discount'] = prod_sum_size_discount / prod_sum_catnet if prod_sum_catnet != 0 else 0
    tech_rate_dict['bi_waiting_period'] = prod_sum_bi_waiting_period / prod_sum_size_discount if prod_sum_catnet != 0 else 0
    tech_rate_dict['total_modifier_impact'] = prod_sum_bi_waiting_period / prod_sum_base if prod_sum_base != 0 else 0  # equivalent to multiplying all the above # TODO check this sumproducts correctly

    # To be confirmed: worth change to weighted average on total_tiv
    cum_prod_worth = modifier_summary_df.select(pl.col(f"wildfire_worth") * pl.col("tiv_total_usd"))[f"wildfire_worth"].sum()
    tech_rate_dict["worth"] = cum_prod_worth / sum_tiv_total_usd if sum_tiv_total_usd else 0 

    # GU Tech Rate, Tech Rate, UW Tech Rate, UW Tech Prem
    wildfire_gg_technical_prem_final_pre_uw = (
        (modifier_summary_df["wildfire_us_gg_technical_prem_pre_uw"].fill_nan(0).sum() or 0) +
        (modifier_summary_df["wildfire_intl_gg_technical_prem_pre_uw"].fill_nan(0).sum() or 0)
    )
    wildfire_gg_technical_prem_final_post_uw = (
        (modifier_summary_df["wildfire_us_gg_technical_prem_post_uw"].fill_nan(0).sum() or 0) +
        (modifier_summary_df["wildfire_intl_gg_technical_prem_post_uw"].fill_nan(0).sum() or 0)
    )
    wildfire_total_expected_loss_pre_uw_sum = (
        (modifier_summary_df["wildfire_us_total_expected_loss_pre_uw"].sum() or 0) +
        (modifier_summary_df["wildfire_intl_total_expected_loss_pre_uw"].fill_nan(0).sum() or 0)
    )

    total_floor_area = modifier_summary_df.filter(pl.col("tiv_buildings") != 0)['floor_area'].fill_null(0).sum() or 0

    tech_rate_dict['gu_tech_rate'] = (
        (
            (prod_sum_base / sum_tiv_total_usd) * tech_rate_dict['total_modifier_impact'] *
            wildfire_gg_technical_prem_final_pre_uw
        ) / wildfire_total_expected_loss_pre_uw_sum
        if wildfire_total_expected_loss_pre_uw_sum and sum_tiv_total else 0  
        )

    tech_rate_dict['tech_rate'] = wildfire_gg_technical_prem_final_pre_uw / sum_tiv_total_usd if sum_tiv_total_usd else 0
    tech_rate_dict['tech_prem'] = wildfire_gg_technical_prem_final_pre_uw
    tech_rate_dict['uw_adj_tech_rate'] = wildfire_gg_technical_prem_final_post_uw / sum_tiv_total_usd if sum_tiv_total_usd else 0
    tech_rate_dict['uw_adj_tech_prem'] = wildfire_gg_technical_prem_final_post_uw
    tech_rate_dict['gu_loss'] = wildfire_total_expected_loss_pre_uw_sum
    tech_rate_dict['gu_prem'] = (
        (prod_sum_catnet / prod_sum_base) * 
        (prod_sum_base / sum_tiv_total_usd) * 
        sum_tiv_total_usd
    ) if prod_sum_base and sum_tiv_total_usd else 0  # TODO: check this formula - it doesn't look right

    tech_rate_dict['sum_tiv_total_usd'] = sum_tiv_total_usd
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
            "gu_tech_rate": grouping_dict['gu_tech_rate'],
            "tech_rate": grouping_dict['tech_rate'],
            "tech_prem": grouping_dict['tech_prem'],
            "uw_adj_tech_rate": grouping_dict['uw_adj_tech_rate'],
            "uw_adj_tech_prem": grouping_dict['uw_adj_tech_prem'],
            "gu_loss": grouping_dict["gu_loss"],
            "gu_prem": grouping_dict["gu_prem"],
            "itv": grouping_dict["itv"]
        })

    # Assign to hxd
    return results_list



def wildfire_top_20_locations_summary(hxd, df, other_data, index, layer):

    df = df.with_columns(
        (
            pl.col(f"wildfire_us_gg_technical_prem_final_pre_uw_layer{index}").fill_nan(0) +
            pl.col(f"wildfire_intl_gg_technical_prem_final_pre_uw_layer{index}").fill_nan(0)
        ).alias(f"wildfire_gg_technical_prem_final_pre_uw_layer{index}"),
        (
            pl.col(f"wildfire_us_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0) +
            pl.col(f"wildfire_intl_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0)
        ).alias(f"wildfire_gg_technical_prem_final_post_uw_layer{index}"),
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
                pl.col("tiv_buildings_usd") * pl.col(f'wildfire_buildings_base_rate_layer{index}') + 
                pl.col("tiv_contents_total_usd") * pl.col(f'wildfire_contents_base_rate_layer{index}') +
                pl.col("tiv_bi_usd") * pl.col(f'wildfire_bi_base_rate_layer{index}')
            ) / (pl.col("tiv_buildings_usd") + pl.col("tiv_contents_total_usd") + pl.col("tiv_bi_usd"))
        ).alias("wildfire_base_rate")
    )

    # GU Tech Rate, Tech Rate, UW Tech Rate, UW Tech Prem
    df = df.with_columns(
        [
            (pl.col("wildfire_base_rate") * pl.col("wildfire_total_modifier_impact") * pl.col(f"wildfire_gg_technical_prem_final_pre_uw_layer{index}") /
                pl.col(f"wildfire_total_expected_loss_pre_uw_layer{index}")).fill_nan(0).alias("gu_tech_rate"),
            (pl.col(f"wildfire_gg_technical_prem_final_pre_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("tech_rate"),
            (pl.col(f"wildfire_gg_technical_prem_final_post_uw_layer{index}") / pl.col("tiv_total_usd")).fill_nan(0).alias("uw_adj_tech_rate"),
            pl.col(f"wildfire_gg_technical_prem_final_post_uw_layer{index}").fill_nan(0).alias("uw_adj_tech_prem")
        ]
    )

    df = df.with_columns(
        # pl.when(pl.col("gu_tech_rate") == 0).then(pl.lit(0)).otherwise(pl.col("tech_rate")/pl.col("gu_tech_rate")).alias("worth")
        pl.col(f"wildfire_worth_percent_layer{index}").alias("worth")
    )

    df_layer = df[[
        "country", 
        "state", 
        "county", 
        "zip", 
        "tiv_buildings_usd", 
        "tiv_contents_total_usd", 
        "tiv_bi_usd",
        "tiv_total_usd", 
        "itv",
        f"wildfire_total_base_rate_layer{index}",
        "wildfire_occupancy_load", 
        "wildfire_construction_load", 
        "wildfire_pc_code_load", 
        "wildfire_catnet_score_load",
        "wildfire_size_discount_load",
        "wildfire_bi_waiting_period_factor",
        "wildfire_total_modifier_impact", 
        "worth", 
        "gu_tech_rate", 
        "tech_rate", 
        "uw_adj_tech_rate", 
        "uw_adj_tech_prem"
        ]]

    df_layer = df_layer.rename({
        "tiv_buildings_usd": "tiv_buildings",
        "tiv_contents_total_usd": "tiv_contents_total",
        "tiv_bi_usd": "tiv_bi",
        "tiv_total_usd": "tiv_total",
        f"wildfire_total_base_rate_layer{index}": "base_rate",
        "wildfire_construction_load": "construction", 
        "wildfire_occupancy_load": "occupancy",
        "wildfire_pc_code_load": "pc_code", 
        "wildfire_catnet_score_load": "catnet_score",
        "wildfire_size_discount_load": "size_discount",
        "wildfire_bi_waiting_period_factor": "bi_waiting_period",
        "wildfire_total_modifier_impact": "total_modifier_impact"
        })

    df_layer_tiv = df_layer.sort("tiv_total", descending=True).head(20)
    df_layer_rate = df_layer.sort("uw_adj_tech_prem", descending=True).head(20)

    other_data[f"wf_top_20_locations_summary_layer{index}_tiv"] = df_layer_tiv.to_dicts()
    other_data[f"wf_top_20_locations_summary_layer{index}_rate"] = df_layer_rate.to_dicts()

    return df
