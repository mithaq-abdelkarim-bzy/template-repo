import hx
import polars as pl

def scs_hxd_assignment(hxd, df, other_data):
    '''
    Assign scs data to hxd
    '''

    for index, layer in enumerate(hxd.layers, start=1):
        df = df.with_columns(
            ((df[f"hail_buildings_base_rate_layer{index}"] * df["tiv_buildings_usd"] +
                df[f"hail_contents_base_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                df[f"hail_bi_base_rate_layer{index}"] * df["tiv_bi_usd"] +
                df[f"tornado_buildings_base_rate_layer{index}"] * df["tiv_buildings_usd"] +
                df[f"tornado_contents_base_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                df[f"tornado_bi_base_rate_layer{index}"] * df["tiv_bi_usd"]) / df["tiv_total_usd"])
                .fill_nan(0).alias(f"rate_base_total_scs_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"scs_us_tiv_exposed_layer{index}"))
                .otherwise(pl.col(f"scs_intl_tiv_exposed_layer{index}"))
                .alias(f"scs_tiv_exposed_layer{index}"),
        )

        df = df.with_columns(
            (
                (
                    df[f"hail_buildings_ground_up_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"hail_contents_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                    df[f"hail_bi_ground_up_rate_layer{index}"] * df["tiv_bi_usd"] +
                    df[f"tornado_buildings_ground_up_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"tornado_contents_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                    df[f"tornado_bi_ground_up_rate_layer{index}"] * df["tiv_bi_usd"]
                ) / df["tiv_total_usd"]
            ).fill_nan(0).alias(f"rate_gu_total_scs_layer{index}")
        )
        
    if hxd.policy_information.small_schedule_model:
        for index, layer in enumerate(hxd.layers, start=1):
            scs_ded_usd = df[f"scs_deductible_selected_layer{index}"].to_list()
            scs_sublimit_usd = df[f"scs_selected_sublimit_layer{index}"].to_list()
            scs_tiv_exposed_list = df[f"scs_tiv_exposed_layer{index}"].to_list()

            scs_base_rate_list = df[f"rate_base_total_scs_layer{index}"].to_list()

            scs_ground_up_rate_list = df[f"rate_gu_total_scs_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.deductible_usd_scs = scs_ded_usd[i]
                target_output_by_layer.sublimit_usd_scs = scs_sublimit_usd[i]
                target_output_by_layer.tivexposed_total_usd_scs = scs_tiv_exposed_list[i]
                target_output_by_layer.rate_base_total_scs = scs_base_rate_list[i]
                target_output_by_layer.rate_gu_total_scs = scs_ground_up_rate_list[i]

    elif other_data["large_model_assign"]:

        for index, layer in enumerate(hxd.layers, start=1):
            scs_ded_usd = df[f"scs_deductible_selected_layer{index}"].to_list()
            scs_tiv_exposed_list = df[f"scs_tiv_exposed_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.deductible_usd_scs = scs_ded_usd[i]
                target_output_by_layer.tivexposed_total_usd_scs = scs_tiv_exposed_list[i]
    
    return df
