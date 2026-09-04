import hx
import polars as pl
import pandas as pd
import numpy as np
from scipy import stats

def nmp_rating_calc(hxd, df, other_data, peril_node_names):
    '''
    Calcuates nmp EL
    '''
    ## AT Edit

    assumption_1_in_250_team_df = hx.params.assumption_1_in_250_team
    nmp_load = assumption_1_in_250_team_df.loc[assumption_1_in_250_team_df["Field"] == "NMP Load",f"{hxd.policy_information.team}"].iloc[0]

    peril_node_names_temp = [i for i in peril_node_names if i != "nmp"]

    for index, layer in enumerate(hxd.layers, start=1):
        df = df.with_columns(
            (df.select([f"{peril}_total_expected_loss_pre_uw_layer{index}" for peril in peril_node_names_temp]).sum(axis=1) * nmp_load)\
                .alias(f"nmp_total_expected_loss_pre_uw_layer{index}"),
            (df.select([f"{peril}_total_expected_loss_post_uw_layer{index}" for peril in peril_node_names_temp]).sum(axis=1) * nmp_load)\
                .alias(f"nmp_total_expected_loss_post_uw_layer{index}")
            )

    return df