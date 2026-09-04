import hx, json, openpyxl, requests
import pandas as pd

from algorithms.rate_utilities                           import look_up, rgetattr, pd_df_from_hx_list, write_pd_to_hxd, date_to_string
from algorithms.rate_utilities                           import sanitize_and_sort_expiring_list_by_renewal, split_renewal_list_by_expiring
from algorithms.rate_utilities                           import get_countries_retrieved, one_layer, rgetkey, rsetattr, rgetattr

from copy                                                import deepcopy
from algorithms.data_schema.sch_rater_defined            import perils, ihs_risk_names

from libraries.ihs_api.algorithms.ihs_api import IhsAPIClient
from libraries.ihs_api.algorithms.ihs_common import get_violent_and_political_history

pd.set_option('display.max_rows', None)


# Generate policy document in Excel
@hx.task
def tsk_fetch_ihs_data(hxd, progress):
    inception_date = hxd.hx_core.inception_date
    expo = hxd.cds.exposure.granular
    countries_tbl = hx.params.countries
    IHSGroupCountry = hx.params.IHSGroupCountry

    # Get countries to retrieve
    codes_retrieved_original = [c.country_code_original for c in expo.countries if c.country_code_original is not None]
    codes_retrieved = deepcopy(codes_retrieved_original)

    country_groups = set(IHSGroupCountry["group"].unique())
    groups_retrieved = [c.rated_country for c in expo.countries if c.rated_country in country_groups]

    if groups_retrieved:
        additional_codes = IHSGroupCountry[IHSGroupCountry["group"].isin(groups_retrieved)]["code"].tolist()
        codes_retrieved.extend(additional_codes)

    # Process codes_retrieved
    if len(codes_retrieved) > 1:
        country_codes = ",".join(codes_retrieved)
    else:
        country_codes = codes_retrieved[0] if codes_retrieved else ""

    # Use the library helper to fetch & parse both endpoints
    expo.ihs_api_error_msg = ""
    client = IhsAPIClient()
    try:
        history_df = get_violent_and_political_history(client, codes_retrieved)
    except Exception as exc:
        # original function returned early on endpoint failures;
        hxd.ihs_countries_retrieved = "failed"
        expo.ihs_api_error_msg = f"{str(exc)}"
        return

    # result list of records (mirrors original 'result' list)
    result = history_df.where(pd.notnull(history_df), None).to_dict("records")

    # Aggregate country group values
    if groups_retrieved:
        df = pd.DataFrame(result)
        df["updated_on"] = pd.to_datetime(df["updated_on"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        inception_dt = pd.to_datetime(inception_date)
        df = df[df["updated_on"] < inception_dt]

        df_groups = IHSGroupCountry[IHSGroupCountry["group"].isin(groups_retrieved)]
        merged = pd.merge(df, df_groups, left_on="country_code", right_on="code", how="inner")

        latest_per_country = merged.loc[merged.groupby(["group", "risk_name", "country_code"])["updated_on"].idxmax()]

        grouped = latest_per_country.groupby(["group", "risk_name"]).agg({
            "value": "mean",
            "updated_on": "max"
        }).reset_index()

        for _, row in grouped.iterrows():
            result.append({
                "country_code": row["group"],
                "risk_name": row["risk_name"],
                "value": row["value"],
                "updated_on": row["updated_on"].strftime('%Y-%m-%d'),
                "description": ""
            })

    hxd.ihs = result
    expo.selected_country = expo.countries[0].rated_country

    # Merge the Scores
    full_df = pd.DataFrame(result)
    countries_df = pd.DataFrame([{"country_code": c.country_code, "inception_date": inception_date} for c in expo.countries])

    for node, risk_name in ihs_risk_names.items():
        df = full_df[full_df["risk_name"] == risk_name]
        df["updated_on"] = pd.to_datetime(df["updated_on"])

        countries_df["inception_date"] = pd.to_datetime(inception_date)
        df_sorted = df.sort_values("updated_on")

        result_df = pd.merge_asof(
            countries_df,
            df_sorted,
            left_on="inception_date",
            right_on="updated_on",
            by="country_code",
            direction="backward"
        )

        result_df.rename(columns={"value": node}, inplace=True)
        result_df[node] = result_df[node].fillna(0)
        write_pd_to_hxd(result_df, expo.countries, [node], replace_nan=True)

    # Calculate matching key
    for c in expo.countries:
        c.country_cvg_subcvg = "&".join([str(c.rated_country), str(c.coverage), str(c.subcoverage)])

    # Save countries retrieved
    countries_temp_storage = get_countries_retrieved(hxd)
    hxd.ihs_countries_retrieved = json.dumps(countries_temp_storage)

    # NOTE: in case IHS data needs to be saved to disk
    # with open('/workspace/editing/algorithms/ihs.json', 'w') as json_file:
    #     json.dump(result, json_file, indent=4)