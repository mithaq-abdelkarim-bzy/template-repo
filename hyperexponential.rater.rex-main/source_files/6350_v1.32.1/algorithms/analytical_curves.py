import math
import polars as pl
import hx
import numpy as np
import pandas as pd

INTERP = False

# # Theoretical version
# def mbbefdg(b, g, x): 
#     if g == 1:
#         return x
#     elif b == 1 and g > 1:
#         return math.log(1 + (g - 1) * x) / math.log(g)
#     elif b * g == 1 and g > 1:
#         return (1 - b ** x) / (1 - b)
#     elif b > 0 and b != 1 and b * g != 1 and g > 1:
#         return math.log(((g - 1) * b + (1 - g * b) * (b ** x)) / (1 - b)) / math.log(g * b)
#     else:
#         return -1 # Error handling

def size_discount (loc_discount_df, acc_discount_df, total_acc_tiv, total_loc_tiv_df, peril, exclude_account_size_discount = False):
    # Gets accunt level TIV discount factor 
    acc_discount_df["tiv_low_times_selected_size_discount"] = acc_discount_df["tiv_low"] * acc_discount_df["selected_size_discount"]
    acc_discount_factor = (np.interp(total_acc_tiv, acc_discount_df["tiv_low"], acc_discount_df["tiv_low_times_selected_size_discount"])) / min(max(acc_discount_df["tiv_low"]), total_acc_tiv)
    
    # get location level TV discount factor
    loc_discount_df[f"tiv_low_times_{peril}"] = loc_discount_df["tiv_low"] * loc_discount_df [f"{peril}"]
    loc_tiv_discount_factor_df = (np.interp(total_loc_tiv_df, loc_discount_df["tiv_low"], loc_discount_df[f"tiv_low_times_{peril}"]))
    loc_tiv_discount_factor_df = pd.DataFrame(loc_tiv_discount_factor_df)
    capped_max = pd.DataFrame(np.minimum(total_loc_tiv_df, loc_discount_df["tiv_low"].max()))
    loc_discount_factor_df = np.divide(loc_tiv_discount_factor_df, np.where(capped_max ==0, 1, capped_max))
    
    if exclude_account_size_discount:
        size_discount_factor = (loc_discount_factor_df)[0].to_list() 
    else :
        size_discount_factor = (acc_discount_factor * loc_discount_factor_df)[0].to_list()
    
    return size_discount_factor

def loss_curve(hxd, df, index, peril):
    if not INTERP:
        df = loss_curve_interpolation(hxd, df, index, peril)
    else:
        exposure_curve_parameters_df = hx.params.exposure_curve_parameters

        exposure_curve_parameters_pl = pl.from_pandas(exposure_curve_parameters_df).rename({"exposure_curve": f"{peril}_exposure_curve", "b": f"b_{peril}_layer{index}", "g": f"g_{peril}_layer{index}"})
        df = df.join(exposure_curve_parameters_pl, on=f"{peril}_exposure_curve", how="left")

        df = mbbefdg_pl(df, f"b_{peril}_layer{index}", f"g_{peril}_layer{index}", f"{peril}_entry_over_tiv_layer{index}", f"{peril}_entry_layer{index}")
        df = mbbefdg_pl(df, f"b_{peril}_layer{index}", f"g_{peril}_layer{index}", f"{peril}_exit_over_tiv_layer{index}", f"{peril}_exit_layer{index}")

    return df


def mbbefdg_pl(df, b, g, x, alias):
    '''
    Closed form for loss curve
    '''
    df = df.with_columns(
        pl.when(
            pl.col(g) == 1
                ).then(
                    pl.col(x)
                )\
        .when(
            (pl.col(b) == 1) & (pl.col(g) > 1)
                ).then(
                    (1 + (pl.col(g) - 1) * pl.col(x)).log() / (pl.col(g)).log()
                )\
        .when(
            (pl.col(b) * pl.col(g) == 1) & (pl.col(g) > 1)
                ).then(
                    (1 - pl.col(b) ** pl.col(x)) / (1 - pl.col(b))
                )\
        .when(
            (pl.col(b) > 0) & (pl.col(b) != 1) & (pl.col(b) * pl.col(g) != 1) & (pl.col(g) > 1)
                ).then(
                    (((pl.col(g) - 1) * pl.col(b) + (1 - pl.col(g) * pl.col(b)) * (pl.col(b) ** pl.col(x))) / (1 - pl.col(b))).log() / (pl.col(g) * pl.col(b)).log()
                )\
        .otherwise(
            -1
        ).alias(alias)
    )

    return df


def loss_curve_interpolation(hxd, df, index, peril):

    # Load parameter table
    loss_curve_lookup_df = hx.params.loss_curve_lookup
    loss_curve_lookup_pl = pl.from_pandas(loss_curve_lookup_df).melt(
        id_vars="Percent", variable_name=f"{peril}_curve_selected", value_name="curve_value")
    
    loss_curve_lookup_pl = loss_curve_lookup_pl.with_columns(
        pl.col("Percent").alias("percent_lookup")
    )

    loss_curve_lookup_pl = loss_curve_lookup_pl.sort("Percent")

    # Use temp df because going to be sorting and joining a lot
    temp_df = df[[
        "row_nr",
        f"{peril}_entry_over_tiv_layer{index}",
        f"{peril}_exit_over_tiv_layer{index}",
        f"{peril}_curve_selected"
    ]]

    temp_df = temp_df.with_columns(
        (
            pl.when(pl.col(f"{peril}_entry_over_tiv_layer{index}") > 1000000).then(1000000).otherwise(pl.col(f"{peril}_entry_over_tiv_layer{index}")
            ).alias(f"{peril}_entry_over_tiv_layer{index}")
        ),
        (
            pl.when(pl.col(f"{peril}_exit_over_tiv_layer{index}") > 1000000).then(1000000).otherwise(pl.col(f"{peril}_exit_over_tiv_layer{index}")
            ).alias(f"{peril}_exit_over_tiv_layer{index}")
        )
    )

    temp_df = temp_df.sort(f"{peril}_entry_over_tiv_layer{index}")

    temp_df = (temp_df.join_asof(loss_curve_lookup_pl, 
                            left_on=f"{peril}_entry_over_tiv_layer{index}", right_on="Percent",
                            by=f"{peril}_curve_selected", strategy="forward")
                        .fill_null(0)
                        .rename({"percent_lookup": "entry_percent_upper", "curve_value": "entry_value_upper"}))

    temp_df = (temp_df.join_asof(loss_curve_lookup_pl, 
                            left_on=f"{peril}_entry_over_tiv_layer{index}", right_on="Percent",
                            by=f"{peril}_curve_selected", strategy="backward")
                        .fill_null(0)
                        .drop("Percent_right")
                        .rename({"percent_lookup": "entry_percent_lower", "curve_value": "entry_value_lower"}))

    temp_df = temp_df.sort(f"{peril}_exit_over_tiv_layer{index}")

    temp_df = (temp_df.join_asof(loss_curve_lookup_pl, 
                            left_on=f"{peril}_exit_over_tiv_layer{index}", right_on="Percent",
                            by=f"{peril}_curve_selected", strategy="forward")
                        .fill_null(0)
                        .drop("Percent_right")
                        .rename({"percent_lookup": "exit_percent_upper", "curve_value": "exit_value_upper"}))

    temp_df = (temp_df.join_asof(loss_curve_lookup_pl, 
                            left_on=f"{peril}_exit_over_tiv_layer{index}", right_on="Percent",
                            by=f"{peril}_curve_selected", strategy="backward")
                        .fill_null(0)
                        .drop("Percent_right")
                        .rename({"percent_lookup": "exit_percent_lower", "curve_value": "exit_value_lower"}))
    
    df = df.sort("row_nr")
    temp_df = temp_df.sort("row_nr")

    temp_df = temp_df.with_columns(
            pl.when(pl.col("entry_percent_upper") == pl.col("entry_percent_lower"))
                .then(pl.col("entry_value_lower"))
                .otherwise(
                    pl.col("entry_value_lower") + ((pl.col("entry_value_upper") - pl.col("entry_value_lower")) * (pl.col(f"{peril}_entry_over_tiv_layer{index}") - pl.col("entry_percent_lower"))) / (pl.col("entry_percent_upper") - pl.col("entry_percent_lower"))
                )
                .alias(f"{peril}_entry_perc_layer{index}"),
            pl.when(pl.col("exit_percent_upper") == pl.col("exit_percent_lower"))
                .then(pl.col("exit_value_lower"))
                .otherwise(
                    pl.col("exit_value_lower") + ((pl.col("exit_value_upper") - pl.col("exit_value_lower")) * (pl.col(f"{peril}_exit_over_tiv_layer{index}") - pl.col("exit_percent_lower"))) / (pl.col("exit_percent_upper") - pl.col("exit_percent_lower"))
                )
                .alias(f"{peril}_exit_perc_layer{index}")    
        )      

    temp_df = temp_df.with_columns(
            pl.when(pl.col("entry_percent_upper") == pl.col("entry_percent_lower"))
                .then(pl.col("entry_value_lower"))
                .otherwise(
                    pl.col("entry_value_lower") + ((pl.col("entry_value_upper") - pl.col("entry_value_lower")) * (pl.col(f"{peril}_entry_over_tiv_layer{index}") - pl.col("entry_percent_lower"))) / (pl.col("entry_percent_upper") - pl.col("entry_percent_lower"))
                )
                .alias(f"{peril}_entry_perc_layer{index}"),
            pl.when(pl.col("exit_percent_upper") == pl.col("exit_percent_lower"))
                .then(pl.col("exit_value_lower"))
                .otherwise(
                    pl.col("exit_value_lower") + ((pl.col("exit_value_upper") - pl.col("exit_value_lower")) * (pl.col(f"{peril}_exit_over_tiv_layer{index}") - pl.col("exit_percent_lower"))) / (pl.col("exit_percent_upper") - pl.col("exit_percent_lower"))
                )
                .alias(f"{peril}_exit_perc_layer{index}")    
        )      

    # Calculated the interpolated entry/exit percentage
    df = df.with_columns(
        temp_df.select([
            pl.col(f"{peril}_entry_perc_layer{index}"),
            pl.col(f"{peril}_exit_perc_layer{index}")    
        ])            
    )

    # Replace infinity values
    df = df.with_columns(
        [
            pl.when(pl.col(f"{peril}_entry_perc_layer{index}").is_infinite()).then(0).otherwise(pl.col(f"{peril}_entry_perc_layer{index}")).keep_name(),
            pl.when(pl.col(f"{peril}_exit_perc_layer{index}").is_infinite()).then(0).otherwise(pl.col(f"{peril}_exit_perc_layer{index}")).keep_name()
        ]
    )
    
    return df