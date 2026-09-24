import hx
import json
import math
import datetime
import os
import requests
import openpyxl
import copy
import pandas as pd
import numpy as np
import algorithms.rate_utilities as utils
from algorithms.year_frac import diffdays

from algorithms.rate_constants import (
    policy_structure_to_dataframe,
    policy_addl_structure_to_dataframe,
    retention_to_dataframe,
    territory_to_dataframe,
    client_details_lawyers_to_dataframe,
    client_details_aec_to_dataframe,
    project_type_aec_to_dataframe,
    get_fx_rate,
    get_fx_rate_base,
    get_base_params,
    get_tech_params,
    get_nmp_load,
    territory_labels,
    chart_revenue_steps,
    get_quotes_params,
    get_quotes_params_addl,
    area_mapping
)

def get_model_params(hxd, profession: str, expected_exposure: float = None, bool_populate_elc_experience=True):
    """
        returns ModelParamsFinal and ModelParamsUnadjustedFinal
        profession = "lpl" or "aec"
    """
    # get required param tables
    bp = get_base_params(profession)
    df_inflation = hx.params.ref_inflation
    inflation_col = "Lawyers Indemnity" if profession == "lpl" else "A&E Claims"
    future_inflation = df_inflation[df_inflation["Year"]=="Future"][inflation_col].iloc[0]
    df_tbl_complexity = hx.params.ref_tbl_complexity
    df_tbl_complexity_freq = hx.params.ref_tbl_complexity_freq
    complexity_col = "Lawyers Adjustment" if profession == "lpl" else "A&E Adjustment"
    df_retro_cover = hx.params.ref_tbl_retro_cover

    df_ter_loading = hx.params.ref_lpl_territory_loading if profession == "lpl" else hx.params.ref_ae_territory_loading
    df_aop_loading = hx.params.ref_lpl_aop_loading if profession == "lpl" else hx.params.ref_ae_aop_loading
    df_freq_curve = hx.params.ref_lst_lpl_freq_curve if profession == "lpl" else hx.params.ref_lst_ae_freq_curve
    #df_sev_curve = hx.params.ref_lst_lpl_sev_curve if profession == "lpl" else hx.params.ref_lst_ae_sev_curve
    
    start_date = hxd.cds.standard_fields.inception_date
    end_date = hxd.cds.standard_fields.expiry_date
    retro_date = hxd.cds.retro_date
    term_factor = diffdays(start_date, end_date) / 365.25
    if expected_exposure is None:
        expected_exposure = (hxd.cds.exposure.granular.exposure_expected_current_year or 0)
    risk_fx_rate = get_fx_rate(hxd.cds.currencies.source_currency)
    size_of_project = hxd.cds.exposure.granular.client_details_lawyers.size_of_matters if profession == "lpl" else hxd.cds.exposure.granular.client_details_AEC.size_of_matters

    ###### Model Prep Calcs Lawyers #######     
    df_ded_params = get_ded_params(hxd)

    # Geography Factors
    df_ter = territory_to_dataframe(hxd)
    df_ter["territory"] = df_ter["territory"].map(area_mapping)
    df_ter = df_ter[df_ter["weighted"] > 0].copy()       # filter out 
    df_ter = df_ter.merge(df_ter_loading, left_on="territory", right_on="Territory", how="inner")
    df_ter["freq_mult"] = 1 + df_ter["Frequency"]
    df_ter["sev_mult"] = 1 + df_ter["Severity"]
    df_ter["currency"] = df_ter["Currency"]
    df_ter["ded_class"] = df_ter["territory"].where(df_ter["territory"].isin(df_ded_params["Area"]),"not_specified")
    df_ter.drop(['Frequency', 'Severity', 'Currency'], axis=1, inplace=True)    #delete out unused cols

    geog_freq_mult_total = df_ter["freq_mult"].dot(df_ter["weighted"])
    geog_sev_mult_total = df_ter["sev_mult"].dot(df_ter["weighted"])

    # AOP Factors
    df_aop = client_details_lawyers_to_dataframe(hxd) if profession == "lpl" else client_details_aec_to_dataframe(hxd)
    df_aop = df_aop[df_aop["weighted"] > 0].copy()    # filter out
    df_aop = df_aop.merge(df_aop_loading, left_on="areas_of_practice", right_on="Area of Practice", how="inner")
    df_aop["freq_mult"] = 1 + df_aop["Frequency"]
    df_aop["sev_mult"] = 1 + df_aop["Severity"]

    aop_freq_mult_total = df_aop["freq_mult"].dot(df_aop["weighted"])
    # contractors - aop is 1.  
    aop_sev_mult_total = 1 if hxd.cds.profession == "Contractors" else df_aop["sev_mult"].dot(df_aop["weighted"]) 

    # PT Factors - only relevant for AEC
    df_ae_pt_loading = hx.params.ref_ae_pt_loading
    df_pt = project_type_aec_to_dataframe(hxd)
    df_pt = df_pt[df_pt["weighted"] > 0].copy()    # filter out
    df_pt = df_pt.merge(df_ae_pt_loading, left_on="project_type", right_on="Project Type", how="inner")
    df_pt["freq_mult"] = 1 + df_pt["Frequency"]
    df_pt["sev_mult"] = 1 + df_pt["Severity"]

    pt_freq_mult_total = 1 if profession == "lpl" else df_pt["freq_mult"].dot(df_pt["weighted"])
    pt_sev_mult_total = 1 if profession == "lpl" else df_pt["sev_mult"].dot(df_pt["weighted"])

    # Excel's current Model Prep U/W factor is PRODUCT of a single hard-coded 1
    # cell (AEC C11 -> AD7, Lawyers C10 -> X7). Keep it explicit so the
    # unadjusted En calculation mirrors the workbook path without pretending
    # there is a schema-driven UW factor here.
    uw_factor = 1
    rdi = None if not retro_date else diffdays(retro_date, start_date) / 365.25
    rdi_freq_mult = 1 if rdi is None else 1 + df_retro_cover[df_retro_cover["Retroactive Cover"]==min(4,int(rdi))]["Factor"].iloc[0]
    complexity_freq_mult = df_tbl_complexity_freq[df_tbl_complexity_freq["Complexity"]==size_of_project][complexity_col].iloc[0]

    non_geog_freq_mult = pt_freq_mult_total * aop_freq_mult_total * uw_factor * rdi_freq_mult * complexity_freq_mult
    non_geog_sev_mult = pt_sev_mult_total * aop_sev_mult_total

    ##### RInputs Lawyers #######
    df_ter = df_ter.merge(df_freq_curve, how="left",left_on="territory", right_on="Area") #frequency params
    df_ter = df_ter.where(pd.notna(df_ter), None) # replace NaN with None 

    ## -> freq
    df_ter["lambda"] = (bp.base_freq * pow((expected_exposure / risk_fx_rate / 1e6), bp.base_power_value) 
                        * (1 - bp.base_ncp) * term_factor * df_ter["weighted"] * df_ter["freq_mult"] * non_geog_freq_mult)
    df_ter["curve_type"] = df_ter["CurveType"]
    df_ter["currency_curve"] = df_ter["Currency"]
    df_ter["fx_rate"] = df_ter["currency_curve"].apply(get_fx_rate) / risk_fx_rate
    df_ter["ncp"] = df_ter["NCP"]
    # df_ter["coefp1"] from df_freq_curve
    # df_ter["coefp2"] from df_freq_curve
    # df_ter["coefp3"] from df_freq_curve
    df_ter.drop(['CurveType','Currency', 'NCP'], axis=1, inplace=True)
    df_ter["lambda_new_prep"] = expected_exposure * df_ter["fx_rate"] * df_ter["weighted"]
    df_ter["lambda_new"] = np.where(
        df_ter["curve_type"].isna(),  # CASE 1: curve_type is None
        df_ter["lambda"],
        np.where(
            df_ter["lambda_new_prep"] < df_ter["coefp3"],  # CASE 2: below breakpoint
            df_ter["coefp1"] * (df_ter["lambda_new_prep"] ** df_ter["coefp2"]),
            df_ter["coefp1"] * (df_ter["coefp3"] ** df_ter["coefp2"]) * df_ter["lambda_new_prep"] / df_ter["coefp3"]
        ) * non_geog_freq_mult * term_factor
    )

    ## -> severity
    #df_ter = df_ter.merge(df_sev_curve, how="left",left_on="territory", right_on="Area") 
    df_ter["mu_base"] = np.where(df_ter["territory"] == "united_kingdom",bp.mu_base_uk,bp.mu_base)
    df_ter["inflation_claims_sev"] = pow((1 + future_inflation), (diffdays(start_date, end_date)/2 + diffdays(bp.mc_date, start_date)) / 365.25)
    # severity_territory_mult - from above  
    # severity_other_mult - from above
    # specific exists
    df_ter["currency_sev_multiplier"] = df_ter["currency"].apply(get_fx_rate_base) / df_ter["currency"].apply(get_fx_rate)
    df_ter["mu_initial"] = df_ter["mu_base"]  + np.log(df_ter["inflation_claims_sev"]  * df_ter["sev_mult"] * non_geog_sev_mult)
    df_ter["mu_adj"] = df_ter["mu_initial"] + np.log(df_ter["currency_sev_multiplier"])
    df_ter["complexity_mult"] = df_tbl_complexity[df_tbl_complexity["Complexity"]==size_of_project][complexity_col].iloc[0]

    df_ter["sigma_adj"] = np.where(
        df_ter["territory"] == "united_kingdom",
        bp.sigma_uk,
        bp.sigma
    ) * (1 + df_ter["complexity_mult"])
    df_ter["dcaf"] = bp.dcaf
    df_ter["dcop"] = bp.dcop
    df_ter["dcp1"] = bp.dcp1     
    df_ter["sigma_unadj"] = df_ter["sigma_adj"] / (1 + df_ter["complexity_mult"])
    df_ter["lambda_new_unadj"] = utils.ratio(df_ter["lambda_new"], uw_factor)

    print(df_ter.to_string())

    # then filter the relevant columns and rename and is ready as ModelParamsFinal
    df_ModelParamsFinal = df_ter[["territory","ded_class","lambda_new","dcaf","dcop","dcp1","mu_adj","sigma_adj"]].copy()
    df_ModelParamsFinal = df_ModelParamsFinal.rename(columns={
        "territory": "Area",
        "ded_class": "Class",
        "lambda_new": "En",
        "dcaf": "DCAF",
        "dcop": "DCOP",
        "dcp1": "DCp1",
        "mu_adj":"mu",
        "sigma_adj":"sigma"
    })

    df_ModelParamsUnadjustedFinal = df_ter[["territory", "ded_class","lambda_new_unadj","dcaf","dcop","dcp1", "mu_adj", "sigma_unadj"]].copy()
    df_ModelParamsUnadjustedFinal = df_ModelParamsUnadjustedFinal.rename(columns={
        "territory": "Area",
        "ded_class": "Class",
        "lambda_new_unadj": "En",
        "dcaf": "DCAF",
        "dcop": "DCOP",
        "dcp1": "DCp1",
        "mu_adj":"mu",
        "sigma_unadj":"sigma"
    })

    if bool_populate_elc_experience:
        populate_expected_loss_cost_chart(hxd, df_ModelParamsFinal[["Area","En", "mu", "sigma"]].copy())

    return df_ModelParamsFinal, df_ModelParamsUnadjustedFinal

def populate_expected_loss_cost_chart(hxd, df: pd.DataFrame):
    # Area
    # En expected number of losses 
    # mu and sigma parameterise lognormal. 
    # mean_loss = math.exp(mu + sigma**2 / 2)
    # En * mean_loss (Expected loss of aggregate loss distribution)
    df = df.copy()
    df["mean_loss"] = np.exp(df["mu"] + df["sigma"]**2 / 2)
    df["elc"] = df["mean_loss"] * df["En"]

    total_elc = None
    if len(df) > 0:
        total_elc = df["elc"].sum()

    # populate the various ELC in territory and client details
    hxd.cds.exposure.granular.territory.summary.total.elc = total_elc
    hxd.cds.exposure.granular.client_details_AEC.individual_project_types.total.expected_loss_cost = total_elc
    hxd.cds.exposure.granular.client_details_AEC.areas_of_practice_total.elc = total_elc
    hxd.cds.exposure.granular.client_details_lawyers.areas_of_practice_total.elc = total_elc

    # 1st pass make all none
    df_full_ter = territory_to_dataframe(hxd)

    for _, row in df_full_ter.iterrows():     
        setattr(getattr(hxd.cds.exposure.granular.territory.summary, area_mapping[row["territory"]]), "expected_loss_cost", None)

    for _, row in df.iterrows():  
        #weighting= (getattr(getattr(hxd.cds.exposure.granular.territory.summary, row["Area"]), "weighted") or 0)
        # weighting not required as this is factored into calc for E(n)
        setattr(getattr(hxd.cds.exposure.granular.territory.summary, row["Area"]), "expected_loss_cost", row["elc"])

def get_ded_params(hxd):
    territory_labels["not_specified"] = "Not Specified"
    reverse_territory = {v: k for k, v in territory_labels.items()}
    risk_fx_rate = get_fx_rate(hxd.cds.currencies.source_currency)
    df = retention_to_dataframe(hxd)
    df = df.dropna(how="all").copy()
    df = df.rename(columns={
        "class": "Class",
        "region": "Area",
        "eec": "EEC",
        "aggregate": "aggRet",
        "retention_underlying": "InitialMaintenance",
        "retention_residual": "MaintenanceThereafter",
        "defence_cost_bool": "AppliesDefence",
    })

    # adjust for fx_rate
    df["EEC"] = df["EEC"].fillna(0) / risk_fx_rate
    df["aggRet"] = df["aggRet"].fillna(0) / risk_fx_rate
    df["InitialMaintenance"] = df["InitialMaintenance"].fillna(0) / risk_fx_rate
    df["MaintenanceThereafter"] = df["MaintenanceThereafter"].fillna(0) / risk_fx_rate
    df["Area"] = df["Area"].map(reverse_territory)
    df["Class"] = df["Area"]

    default_row = pd.DataFrame(
        [
            {
                "Class": "not_specified",
                "Area": "not_specified",
                "ccy": hxd.cds.currencies.source_currency,
                "EEC": 0.0,
                "aggRet": 0.0,
                "InitialMaintenance": 0.0,
                "MaintenanceThereafter": 0.0,
                "AppliesDefence": "No",
            }
        ]
    )

    if df.empty:
        df = default_row
    elif "not_specified" in df["Area"].values:
        df = pd.concat(
            [
                df[df["Area"] == "not_specified"],
                df[df["Area"] != "not_specified"],
            ],
            ignore_index=True,
        )
    else:
        df = pd.concat([default_row, df], ignore_index=True)

    return df


def _quote_amount_usd(series: pd.Series, risk_fx_rate: float, *, blank_zero_value):
    values = series.fillna(0)
    converted = values / risk_fx_rate
    if blank_zero_value == "inf":
        return np.where(values == 0, np.inf, converted)
    return np.where(values == 0, blank_zero_value, converted)


def _prepare_quote_params(df: pd.DataFrame, risk_fx_rate: float) -> pd.DataFrame:
    """Mirror the Excel RInputs quote/additional-quote parameter defaults."""
    df = df.copy()
    df["limit_eec"] = _quote_amount_usd(df["limit_eec"], risk_fx_rate, blank_zero_value=0.0)
    df["limit_agg"] = _quote_amount_usd(df["limit_agg"], risk_fx_rate, blank_zero_value="inf")
    df["excess_eec"] = _quote_amount_usd(df["excess_eec"], risk_fx_rate, blank_zero_value=0.0)
    df["excess_agg"] = _quote_amount_usd(df["excess_agg"], risk_fx_rate, blank_zero_value="inf")
    df["rtc"] = _quote_amount_usd(df["rtc"], risk_fx_rate, blank_zero_value=0.0)

    rtc_agg_raw = df["rtc_agg"].fillna(0)
    rtc_agg_converted = rtc_agg_raw / risk_fx_rate
    df["rtc_agg"] = np.where(rtc_agg_raw == 0, df["rtc"] * 10, rtc_agg_converted)
    return df


def get_quotes_params(hxd):
    risk_fx_rate = get_fx_rate(hxd.cds.currencies.source_currency)
    df = policy_structure_to_dataframe(hxd)
    df = df[df["include"] == True].copy()
    df = _prepare_quote_params(df, risk_fx_rate)
    df = df.rename(columns={
        "limit_eec": "Leec",
        "limit_agg": "Lagg",
        "excess_eec": "Xeec",
        "excess_agg": "Xagg",
        "rtc": "RTC_Lim",
        "rtc_agg": "RTC_Agg",
        "defense_cost": "DCIA",
        "wordings_adj": "Wordings",
        "brokerage": "Brokerage"
    })
    return df

def get_quotes_params_addl(hxd):
    risk_fx_rate = get_fx_rate(hxd.cds.currencies.source_currency)
    df = policy_addl_structure_to_dataframe(hxd)
    df = df[df["include"] == True].copy()
    df = _prepare_quote_params(df, risk_fx_rate)
    df = df.rename(columns={
        "limit_eec": "Leec",
        "limit_agg": "Lagg",
        "excess_eec": "Xeec",
        "excess_agg": "Xagg",
        "rtc": "RTC_Lim",
        "rtc_agg": "RTC_Agg",
        "defense_cost": "DCIA",
        "wordings_adj": "Wordings",
        "brokerage": "Brokerage"
    })
    return df


def validate_simulation_inputs(hxd, progress):
    df_pol_structure = get_quotes_params(hxd)
    expected_exposure = (hxd.cds.exposure.granular.exposure_expected_current_year or 0)
    risk_fx_rate = get_fx_rate(hxd.cds.currencies.source_currency) or 0
    error_string = "Exposure Rate Simulation has not completed: \n"

    bool_error = False

    #If ExposureDetails.Range("DB.ExposureDetails.ExpectedExposure.CurrentYear") = "" Then
    if expected_exposure == 0:
        bool_error = True
        error_string += "> Please ensure that revenue amounts have been entered in the exposure details page\n"

    # Territory
    if hxd.cds.exposure.granular.territory.summary.total.weighted == 0:
        bool_error = True
        error_string += "> Please ensure that the Territory splits have been entered correctly\n"

    # Client Details
    if hxd.cds.profession == "Lawyers":
        if hxd.cds.exposure.granular.client_details_lawyers.areas_of_practice_total.weighted == 0:
            bool_error = True
            error_string += "> Please ensure that the Areas of Practice splits have been entered correctly\n"
    else:
        if hxd.cds.exposure.granular.client_details_AEC.areas_of_practice_total.weighted == 0:
            bool_error = True
            error_string += "> Please ensure that the Areas of Practice splits have been entered correctly\n"

        if hxd.cds.exposure.granular.client_details_AEC.individual_project_types.total.weighted == 0:
            bool_error = True
            error_string += "> Please ensure that the Individual Project Type splits have been entered correctly\n"           

    # Simulation is not completed to create a valid exposure price. Error calculating Exchange Rate. Has a currency been selected?"
    if risk_fx_rate == 0:
        bool_error = True
        error_string += "> Error calculating Exchange Rate - has a currency been selected on the Risk Information Page?\n"

        # test a layer is selected
    count = 0 
    for layers in [hxd.cds.layers, hxd.cds.layers_addl]:
        for layer in layers:
            if layer.include:
                count +=1
    
    if count == 0:
        bool_error = True
        error_string += "> Please ensure that a layer has been included.\n"
    else:
        #If StructurePricing.Range("DB.StructurePricing.PolicyStructure.LimitEEC.Layer1") = "" Then
        if (df_pol_structure["Leec"].iloc[0] or 0) == 0:
            bool_error = True
            error_string += "> Please ensure that a primary limit has been entered in the policy structure\n"

    # retention split areas are unique
    regions = [item.region for item in hxd.cds.retention_split if item.region is not None]
    if len(regions) != len(set(regions)):
        bool_error = True
        error_string += "> There are duplicate regions in the Retention table\n"

    if bool_error:
        hx.errors.fatal(error_string)    

def _normalise_scalar(value):
    if value is None:
        return None
    if isinstance(value, (float, np.floating)):
        if math.isnan(float(value)):
            return None
        return round(float(value), 8)
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime().isoformat()
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    return value


def _dataframe_to_serializable(df):
    if df is None or df.empty:
        return []
    records = df.to_dict(orient="records")
    return [
        {key: _normalise_scalar(val) for key, val in record.items()}
        for record in records
    ]


def build_simulation_input_snapshot(
    hxd,
    *,
    df_ded_params=None,
    df_quote_params=None,
    df_quote_params_addl=None,
    df_model_params=None,
    base_params_obj=None,
    expected_exposure=None,
    profession=None,
    num_sims=100000,
):
    if expected_exposure is None:
        expected_exposure = float(hxd.cds.exposure.granular.exposure_expected_current_year or 0)
    if profession is None:
        profession = "lpl" if hxd.cds.profession == "Lawyers" else "aec"
    if base_params_obj is None:
        base_params_obj = get_base_params(profession)
    if df_quote_params is None:
        df_quote_params = get_quotes_params(hxd)
    if df_quote_params_addl is None:
        df_quote_params_addl = get_quotes_params_addl(hxd)
    if df_ded_params is None:
        df_ded_params = get_ded_params(hxd)
    if df_model_params is None:
        df_model_params, _ = get_model_params(hxd, profession, expected_exposure, False)
    snapshot = {
        "expected_exposure": _normalise_scalar(expected_exposure),
        "profession_key": profession,
        "profession_label": hxd.cds.profession,
        "source_currency": hxd.cds.currencies.source_currency,
        # "inception_date": _normalise_scalar(hxd.hx_core.inception_date),
        # "expiry_date": _normalise_scalar(hxd.hx_core.expiry_date),
        "retro_date": _normalise_scalar(hxd.cds.retro_date),
        "base_params": {
            "mu_base": _normalise_scalar(base_params_obj.mu_base),
            "mu_base_uk": _normalise_scalar(base_params_obj.mu_base_uk),
            "sigma": _normalise_scalar(base_params_obj.sigma),
            "sigma_uk": _normalise_scalar(base_params_obj.sigma_uk),
            "mc_date": _normalise_scalar(base_params_obj.mc_date),
            "dcaf": _normalise_scalar(base_params_obj.dcaf),
            "dcop": _normalise_scalar(base_params_obj.dcop),
            "dcp1": _normalise_scalar(base_params_obj.dcp1),
            "base_freq": _normalise_scalar(base_params_obj.base_freq),
            "base_power_value": _normalise_scalar(base_params_obj.base_power_value),
            "base_ncp": _normalise_scalar(base_params_obj.base_ncp),
            "odf": _normalise_scalar(base_params_obj.odf),
        },
        "ded_params": _dataframe_to_serializable(df_ded_params),
        "quote_params": _dataframe_to_serializable(df_quote_params),
        "additional_quote_params": _dataframe_to_serializable(df_quote_params_addl),
        "model_params": _dataframe_to_serializable(df_model_params),
        "num_sims": _normalise_scalar(num_sims),
    }
    return snapshot


def snapshot_to_json(snapshot):
    return json.dumps(snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def get_current_simulation_snapshot_json(hxd, **kwargs):
    return snapshot_to_json(build_simulation_input_snapshot(hxd, **kwargs))


def _persist_simulation_snapshot(hxd, snapshot_json):
    hxd.model_state.simulation_state.last_input_snapshot = snapshot_json
