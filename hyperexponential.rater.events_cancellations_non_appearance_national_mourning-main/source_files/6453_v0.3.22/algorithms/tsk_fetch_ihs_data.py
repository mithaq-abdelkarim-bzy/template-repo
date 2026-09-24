import hx, json, openpyxl, requests
import pandas as pd
from typing                                 import List, Tuple
from libraries.ihs_api.algorithms.ihs_api   import RiskEndpoint, IhsAPIClient
from algorithms.rate_utilities              import look_up, rgetattr, pd_df_from_hx_list, write_pd_to_hxd, drop_and_merge
from libraries.ihs_api.algorithms.ihs_api   import IhsAPIClient
from datetime                               import datetime

pd.set_option('display.max_rows', None)

def ensure_ihs_cols_exist(df: pd.DataFrame, default = None):
    required_cols = ['Terrorism', 'ProtestsAndRiots',  'LabourStrikes',  'InterstateWar',  'CivilWar' ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = default
    return df


def get_strategic_risk_history(client: IhsAPIClient, country_codes: List[str], fail_strategic=False) -> pd.DataFrame:
    """
    Fetch /strategicrisk , parse and return a DataFrame.
    """
    params = {"countries": ",".join(list(set(country_codes))) if isinstance(country_codes, (list, tuple)) else str(country_codes)}
    strategic_data = client.fetch(RiskEndpoint.STRATEGIC, params=params, fail=fail_strategic)
    df_strategic = parse_ihs_json(strategic_data)
    return df_strategic


def parse_ihs_json(data: List[dict], filter_risks: List[str] = None) -> pd.DataFrame:
    """
    Convert raw IHS JSON (list of country blocks each with 'Risks') into
    a flat DataFrame with columns:
      ['country_code', 'risk_name', 'value', 'updated_on', 'latest_outlook', 'latest_description']
    Optionally filter to a list of risk names (filter_risks).
    """
    rows = []
    for country in data:
        risks = country.get("Risks", {}) or {}
        for risk_key, risk in risks.items():
            name = risk.get("Name", risk_key)
            if filter_risks and name not in filter_risks:
                continue
            for hist in risk.get("History", []) or []:
                rows.append({
                    "country_code":         country.get("Country"),
                    "risk_name":            name,
                    "value":                hist.get("Value"),
                    "updated_on":           hist.get("UpdatedOn"),
                    "latest_outlook":       risk.get("Outlook", ""),
                    "latest_description":   risk.get("Description", "")
                })
    return pd.DataFrame(rows)


def tsk_fetch_ihs_data(hxd, progress):

    # load inital info
    inception_date      = hxd.cds.standard_fields.inception_date
    inception_dt        = pd.to_datetime(inception_date)
    expo_path           = hxd.cds.exposure.granular.event_cancel
    ihs_path            = hxd.cds.ihs
    ihs_country_group   = hx.params.tbl_ihs_country_group

    # Get countries to retrieve
    country_groups  = set(ihs_country_group["group"].unique())
    codes_retrieved = [c.country_code for c in expo_path.events if (c.country_code != "") and (c.country_code not in country_groups)]
    groups_retrieved= [c.country_code for c in expo_path.events if (c.country_code in country_groups)]

    if groups_retrieved:
        additional_codes = ihs_country_group[ihs_country_group["group"].isin(groups_retrieved)]["code"].tolist()
        codes_retrieved = list(set(codes_retrieved) | set(additional_codes))                                        # using a set union to deduplicate

    # Process codes_retrieved
    if len(codes_retrieved) > 1:
        country_codes = ",".join(codes_retrieved)
    else:
        country_codes = codes_retrieved[0] if codes_retrieved else ""

    # Use the library helper to fetch & parse both endpoints
    ihs_path.internal_error_msg = ""
    client = IhsAPIClient()
    try:
        history_df = get_strategic_risk_history(client, codes_retrieved)
    except Exception as exc:
        # original function returned early on endpoint failures;
        hxd.cds.ihs.last_run_status = "failed"
        ihs_path.internal_error_msg = f"{str(exc)}"
        return

    # result list of records (mirrors original 'result' list)
    risk_lst    = ['Terrorism', 'ProtestsAndRiots', 'LabourStrikes', 'InterstateWar', 'CivilWar']
    risk_mask   = history_df['risk_name'].isin(risk_lst)
    history_df  = history_df[risk_mask]
    history_df  = history_df.where(pd.notnull(history_df), None)
    result      = history_df.to_dict("records")

    # Aggregate country group values
    if groups_retrieved:
        # load result into df and constrain to be less than inception date, assigning value types where needed
        df               = pd.DataFrame(result)
        df["updated_on"] = pd.to_datetime(df["updated_on"], errors="coerce")
        df["value"]      = pd.to_numeric( df["value"],      errors="coerce")
        df               = df[df["updated_on"] < inception_dt]

        # extract all the latest values relating to the countries within the regions requested and apply country weights to the values and aggregate
        ctry_groups_df          = ihs_country_group[ihs_country_group["group"].isin(groups_retrieved)]                                              # filter to countries in the required groups
        groups_all_df           = pd.merge(df, ctry_groups_df, left_on="country_code", right_on="code", how="inner")                                # inner join to give all ihs observations that attach to the countries in required groups... MANY-MANY join
        groups_latest_idx_ss    = groups_all_df.groupby(  ["group", "risk_name", "country_code"]  )["updated_on"].idxmax()                          # get the index of the latest value for each combination
        groups_lat_df           = groups_all_df.loc[  groups_latest_idx_ss  ]                                                                       # filter df to just those latest values
        groups_lat_df['wgt_val']= groups_lat_df['weight'] * groups_lat_df['value']                                                                  # apply a weight to each value, applying weights like this implicitly assumes countries are always present
        grouped_df              = groups_lat_df.groupby(  ["group", "risk_name"]  ).agg(  {"wgt_val":"sum",  "updated_on":"max"}  ).reset_index()   # summmarise by group and risk name, aggegregating the weighted value

        # append the region output to the results dictionary
        for _, row in grouped_df.iterrows():
            result.append({
                "country_code":         row["group"],
                "risk_name":            row["risk_name"],
                "value":                row["wgt_val"],
                "updated_on":           row["updated_on"].strftime('%Y-%m-%d'),
                "latest_outlook":       "",     
                "latest_description":   ""
            })

    # write result distionary to hxd
    ihs_path.ihs_detail = result

    ## mapping scores to events table
    # convert to df and filter to < inception date
    df               = pd.DataFrame(result)
    df["updated_on"] = pd.to_datetime(df["updated_on"])
    df               = df[df["updated_on"] < inception_dt]

    # filter scores to be latest and pivot
    latest_idx_ss    = df.groupby(  ["risk_name", "country_code"]  )["updated_on"].idxmax()
    ihs_df           = (df.loc[latest_idx_ss]
                          .pivot(index="country_code", columns="risk_name", values="value")
                          .fillna(0).reset_index())

    # filter scores to be latest and pivot
    ihs_df                                  = ensure_ihs_cols_exist(ihs_df)
    ihs_df['ihs_terrorism']                 = ihs_df['Terrorism'                  ].astype(float).fillna(0)
    ihs_df['ihs_riots_and_civil_commotion'] = ihs_df['ProtestsAndRiots'           ].astype(float).fillna(0)
    ihs_df['ihs_strike']                    = ihs_df['LabourStrikes'              ].astype(float).fillna(0)
    ihs_df['ihs_war']                       = ihs_df[['InterstateWar', 'CivilWar']].astype(float).mean(axis=1).fillna(0)

    # map ihs scores to country code in events table ans write to hxd
    ihs_cols  = ['ihs_terrorism', 'ihs_riots_and_civil_commotion', 'ihs_strike', 'ihs_war']
    events_df = pd.DataFrame([{"country_code": c.country_code} for c in expo_path.events])
    events_df = drop_and_merge(events_df, ihs_df[  ['country_code']+ihs_cols  ], "country_code" )
    events_df = events_df.astype(object).where(events_df.notna(), None)                                    # needed so we can pass None back and not "nan"
    write_pd_to_hxd(events_df, expo_path.events, ihs_cols)

    # writing ihs diagnostics to hxd
    ihs_path.last_run_value             = ihs_path.calc_run_value
    ihs_path.last_run_date              = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ihs_path.last_run_status            = f"IHS Load run successfully at {ihs_path.last_run_date}"
