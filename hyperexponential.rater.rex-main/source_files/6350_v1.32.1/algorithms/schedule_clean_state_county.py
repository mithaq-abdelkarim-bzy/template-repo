import hx
import pandas as pd
import ast

def clean_state_county(hxd, df):
    rms_proxy_rate_df = hx.params.rms_proxy_rate
    rms_proxy_rate_df = rms_proxy_rate_df[["Zip Code", "State Code", "County"]]
    rms_proxy_rate_df = rms_proxy_rate_df.rename(columns = {"Zip Code": "zip", "State Code": "state", "County": "county"})
    rms_proxy_rate_df["country_lowercase"] = "united states"
    df["country_lowercase"] = df.country.str.lower()
    df['zip'] = df['zip'].astype('string')
    df = df.merge(rms_proxy_rate_df, how="left", on=["zip", "country_lowercase"]).drop("country_lowercase", axis=1)

    df = rejoin_saved_cols(hxd, df)
    df['state'] = df['state'].astype('string').fillna("")
    df['county'] = df['county'].astype('string').fillna("")

    return df

def rejoin_saved_cols(hxd, df):
    if hxd.policy_information.small_schedule_model:
            
        col_names = {"state": "original_state", "county": "original_county"}
        try:
            state_county_saved_cols = pd.read_csv("state_county_saved_cols.csv")
            state_county_saved_cols = state_county_saved_cols.rename(col_names, axis=1)
            df = df.join(state_county_saved_cols)
        except OSError:
            pass  # columns will be created below anyway
        except FileNotFoundError:
            pass  # columns will be created below anyway

        for key, val in col_names.items():
            if val not in df.columns:
                df[val] = None

        df["state"] = df["state"].fillna(df["original_state"])
        df = df.drop("original_state", axis=1)

        df["county"] = df["county"].fillna(df["original_county"])
        df = df.drop("original_county", axis=1)

    else:
        if hxd.schedule.large_schedule_workflow.load_from_schedule_file:
            with hxd.schedule.large_schedule_workflow.schedule_file.open("b") as f:
                original_df = pd.read_csv(f)
        elif hxd.schedule.large_schedule_workflow.load_from_em_database:
            with hxd.schedule.large_schedule_workflow.large_schedule_em_file.open("b") as f:
                original_df = pd.read_csv(f)
        # with hxd.schedule.large_schedule_workflow.large_schedule_em_file.open("b") as f:
        #     original_df = pd.read_csv(f)

        original_df = original_df[["address_dropdown/state", "address_dropdown/county"]]
        df["state"] = df["state"].fillna(original_df["address_dropdown/state"])
        df["county"] = df["county"].fillna(original_df["address_dropdown/county"])

    return df

def schedule_table_hxd_assignment_state_county(hxd, df, large_model):
    '''
    Assign schedule table related calculation to backend nodes for reporting purpose
    '''

    # When the model is large
    if large_model:

        state_list = df["state"].to_list()
        county_list = df["county"].to_list()

        for index, row in enumerate(hxd.schedule.large_schedule_output):
            row.state = state_list[index]
            row.county = county_list[index]

    else:

        state_list = df["state"].to_list()
        county_list = df["county"].to_list()

        for index, row in enumerate(hxd.schedule.schedule_table):
            if state_list[index]:
                row.address_dropdown.state = state_list[index]
            if county_list[index]:
                row.address_dropdown.county = county_list[index]