import hx
import polars as pl

def cyber_rating(hxd, df):
    
    is_cyber = [layer.perils.cyber.include for layer in hxd.layers]

    # Retrieve cyber loss RoLs
    cyber_df = pl.from_pandas(hx.params.cyber_base_rates)
    
    # Find industry with the largest TIV
    top_industry = (
        df
        .groupby("industry")
        .agg(pl.col("tiv_total_usd").sum())
        .sort("tiv_total_usd", descending=True)
        .select("industry")
        .head(1)
        .item()  # Extract as Python string
    )

    # Select cyber base rate based on top industry
    cyber_rates = cyber_df.filter(pl.col("industry") == top_industry).to_dicts()[0]
    
    for index, layer in enumerate(hxd.layers, start=1):
        
        # Note do not need to convert currency as limit and premium will align
        limit = layer.limit or 0
        excess = layer.excess or 0
        exchange_rate = hxd.policy_information.exchange_rate or 1

        # Retrieve affirmative cyber deductibles & sublimits
        cyber_deductible = layer.perils.cyber.deductible if (layer.perils.cyber.include and layer.perils.cyber.include_affirmative) else 0
        cyber_sublimit = (layer.perils.cyber.sublimit or (limit + excess)) if (layer.perils.cyber.include and layer.perils.cyber.include_affirmative) else 0

        df = df.with_columns([
            (pl.lit(cyber_deductible or 0) / exchange_rate)
                .alias(f"cyber_deductible_usd_layer{index}"),
            (pl.lit(cyber_sublimit or 0) / exchange_rate)
                .alias(f"cyber_selected_sublimit_layer{index}")
        ])
        
        # Calculate exposed cyber limit
        exposed_cyber_limit = min(
            max((cyber_sublimit or 0) - excess, 0),
            limit
        )

        # Calculate total cyber expected loss
        total_cyber_el = exposed_cyber_limit *  cyber_rates["cyber_base_rate"] / exchange_rate
        
        # Calculate total fire expected loss and total TIV
        total_fire_el = pl.col(f"fire_total_expected_loss_pre_uw_layer{index}").sum()
        total_tiv  = pl.col("tiv_total_usd").sum()

        # Assign pre uw adj cyber premium down to location level by fire expected loss (or total TIV)
        df = df.with_columns(
            (
                total_cyber_el *
                pl.when(total_fire_el > 0)
                .then(pl.col(f"fire_total_expected_loss_pre_uw_layer{index}") / total_fire_el)
                .otherwise(pl.col("tiv_total_usd") / total_tiv)
            ).alias(f"cyber_total_expected_loss_pre_uw_layer{index}")
        )
        
        # Assign pre uw adj premium to post uw adj premium (no adjustment possible)
        df = df.with_columns(
            pl.col(f"cyber_total_expected_loss_pre_uw_layer{index}")
            .alias(f"cyber_total_expected_loss_post_uw_layer{index}")
        )
    
    return df

def cyber_hxd_assignment(hxd, df, other_data):
    '''
    Assign cyber data to hxd
    '''

    if hxd.policy_information.small_schedule_model:

        for index, layer in enumerate(hxd.layers, start=1):
            cyber_el_pre_uw_list = df[f"cyber_total_expected_loss_pre_uw_layer{index}"].to_list()
            cyber_el_post_uw_list = df[f"cyber_total_expected_loss_post_uw_layer{index}"].to_list()
            cyber_deductible_list = df[f'cyber_deductible_usd_layer{index}'].to_list()
            cyber_sublimit_list = df[f"cyber_selected_sublimit_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]
                target_output_by_layer.el_pre_uw_usd_100_cyber_total = cyber_el_pre_uw_list[i]
                target_output_by_layer.el_post_uw_usd_100_cyber_total = cyber_el_post_uw_list[i]
                target_output_by_layer.deductible_usd_cyber = cyber_deductible_list[i]
                target_output_by_layer.sublimit_usd_cyber = cyber_sublimit_list[i]

    elif other_data["large_model_assign"]:

        for index, layer in enumerate(hxd.layers, start=1):
            cyber_el_pre_uw_list = df[f"cyber_total_expected_loss_pre_uw_layer{index}"].to_list()
            cyber_deductible_list = df[f'cyber_deductible_usd_layer{index}'].to_list()
            cyber_sublimit_list = df[f'cyber_selected_sublimit_layer{index}'].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.el_pre_uw_usd_100_cyber_total = cyber_el_pre_uw_list[i]
                target_output_by_layer.deductible_usd_cyber = cyber_deductible_list[i]

    return df

    
