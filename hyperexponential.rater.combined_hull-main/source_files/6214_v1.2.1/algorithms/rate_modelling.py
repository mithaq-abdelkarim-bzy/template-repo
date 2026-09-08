import hx
import numpy as np
import math
import calendar
from algorithms.rate_utilities import (
    pd_df_from_hx_list,
    write_pd_to_hxd,
    safe_get_and_fillna,
    look_up,
    forecast,
)
import pandas as pd
from algorithms.helpers.rate_common import MBBEFDG3
from algorithms import parameter_tables_schema as params


def get_nmp_load(inception_year):
    is_dev = False
    bp_class = "Hull, IV, War" if is_dev else "Hull"
    if not bp_class:
        return
    # Pull in technical premium parameters and fx rates from user library
    tp_params_df = (
        hx.params.table_original_rater_params if is_dev else params.tp_parameters.df()
    )
    tp_year = inception_year
    if tp_year not in list(
        tp_params_df[tp_params_df["business_plan_class"] == bp_class]["year"]
    ):
        tp_year = tp_params_df[tp_params_df["business_plan_class"] == bp_class][
            "year"
        ].max()

    def tp_lookup(vbl, bp_class):
        out = tp_params_df[
            (tp_params_df["business_plan_class"] == bp_class)
            & (tp_params_df["year"] == tp_year)
        ][vbl].iloc[0]
        return out

    nmp_load = tp_lookup("nmp_load", bp_class)
    return nmp_load


def rate_modelling(hxd):
    if not hxd.non_cds.show_hide_toggles.hull.show_hull_coverage:
        hxd.non_cds.show_hide_toggles.hull.show_modelling_page = False
        return
    hxd.non_cds.show_hide_toggles.hull.show_modelling_page = (
        hxd.cds.exposure.granular.vessels.hull_rating.is_modelling
    )
    currency = hxd.cds.currencies.source_currency
    fx_rates_df = params.fx_rates.df()
    inception_year = (
        hxd.cds.standard_fields.inception_date.year
        if hxd.cds.standard_fields.inception_date
        else None
    )
    nmp_load = get_nmp_load(inception_year)
    conversion_rate = look_up(currency, "ccy", "fx_rate", fx_rates_df, if_not_found=1)
    modelling_prefix = "modelling_"
    vessels_details_prefix = "vessel_details/"
    build_up_prefix = "build_up_"
    static_prefix = "static_"
    behavioural_prefix = "behavioural_"
    severity_prefix = "severity_"
    frequency_prefix = "frequency_"
    model_types = ["static", "behavioural"]
    model_prefix_map = {
        "static": static_prefix,
        "behavioural": behavioural_prefix,
    }
    vessels = hxd.cds.exposure.granular.vessels
    fleet_average_relativity = vessels.hull_rating.fleet_average_relativity
    columns_to_keep = []
    fleet_casualty_history = (
        vessels.hull_rating.fleet_soft_factors.fleet_casualty_history
    )
    owner_quality = vessels.hull_rating.fleet_soft_factors.owner_quality
    vessels_list = vessels.hull_rating.vessels_list
    vessels_df = pd_df_from_hx_list(vessels_list)

    # Check for duplicates in the combination of vessel_imo and vessel_name
    vessel_duplicates_exist = vessels_df.duplicated(subset=[f"{vessels_details_prefix}imo", f"{vessels_details_prefix}name"], keep=False).any()
    hxd.non_cds.show_hide_toggles.hull.show_duplicate_vessel_warning = vessel_duplicates_exist

    vessels_df["unique_imo"] = (
        vessels_df[f"{vessels_details_prefix}imo"]
        + "_"
        + vessels_df[f"{vessels_details_prefix}name"].fillna("NA")
        + "_"
        + (vessels_df.groupby(f"{vessels_details_prefix}imo").cumcount() + 1).astype(
            str
        )
    )

    hxd.cds.exposure.granular.vessels.hull_rating.modelling_list = [{}] * len(
        vessels_df
    )
    # YZ: Add fleet size calculation
    fleet_size = len(vessels_df)
    hxd.cds.exposure.granular.vessels.hull_rating.fleet_size = fleet_size
    if vessels_df.empty:
        return

    freight_conditions_table = hx.params.table_freight_conditions
    vessel_quality_table = hx.params.table_vessel_quality
    area_of_operation_table = hx.params.table_area_of_operation
    fleet_casualty_history_table = hx.params.table_fleet_casualty_history
    owner_quality_table = hx.params.table_owner_quality
    modelling_parameters_table = hx.params.table_modelling_parameters

    vessels_imo_mask = vessels_df[f"{vessels_details_prefix}imo"].notna()
    behavioural_mask = vessels_imo_mask & vessels_df["age"].notna()

    vessels_df[f"{modelling_prefix}imo"] = vessels_df[f"{vessels_details_prefix}imo"]
    columns_to_keep.append(f"{modelling_prefix}imo")

    vessels_df[f"{modelling_prefix}unique_imo"] = (
        vessels_df[f"{modelling_prefix}imo"]
        + "_"
        + vessels_df[f"{vessels_details_prefix}name"].fillna("NA")
        + "_"
        + (vessels_df.groupby(f"{modelling_prefix}imo").cumcount() + 1).astype(str)
    )
    columns_to_keep.append(f"{modelling_prefix}unique_imo")

    vessels_df[f"{modelling_prefix}name"] = vessels_df[f"{vessels_details_prefix}name"]
    columns_to_keep.append(f"{modelling_prefix}name")

    vessels_df[f"{modelling_prefix}vessel_type"] = vessels_df[f"vessel_type"]
    columns_to_keep.append(f"{modelling_prefix}vessel_type")

    vessels_df[f"{modelling_prefix}agreed_value"] = vessels_df["agreed_value"]
    columns_to_keep.append(f"{modelling_prefix}agreed_value")

    vessels_df[f"{modelling_prefix}gross_tonnage"] = vessels_df[
        f"{vessels_details_prefix}gross_tonnage"
    ]
    columns_to_keep.append(f"{modelling_prefix}gross_tonnage")

    vessels_df[f"{modelling_prefix}dwt"] = vessels_df[f"dwt"]
    columns_to_keep.append(f"{modelling_prefix}dwt")

    vessels_df[f"{modelling_prefix}flag"] = vessels_df[f"flag"]
    columns_to_keep.append(f"{modelling_prefix}flag")

    vessels_df[f"{modelling_prefix}vessel_class"] = vessels_df[
        f"{vessels_details_prefix}vessel_class"
    ]
    columns_to_keep.append(f"{modelling_prefix}vessel_class")

    vessels_df[f"{modelling_prefix}year_built"] = vessels_df[f"year_built"]
    columns_to_keep.append(f"{modelling_prefix}year_built")

    average_build_year_mask = (
        vessels_df[f"year_built"].notna()
        & (vessels_df["agreed_value"].notna())
        & (vessels_df["agreed_value"] > 0)
    )
    mean_value = vessels_df.loc[average_build_year_mask, f"year_built"].mean()
    avg_build_year = np.nan if np.isnan(mean_value) else mean_value
    hxd.cds.exposure.aggregate.average_build_year = (
        None if avg_build_year is np.nan else avg_build_year
    )

    freight_conditions_mask = vessels_df[
        f"{vessels_details_prefix}freight_conditions"
    ].notna()
    vessels_df.loc[
        freight_conditions_mask,
        f"{modelling_prefix}freight_conditions",
    ] = vessels_df[f"{vessels_details_prefix}freight_conditions"].map(
        freight_conditions_table.set_index("freight_conditions")["default"]
    )
    del freight_conditions_table
    columns_to_keep.append(f"{modelling_prefix}freight_conditions")

    vessel_quality_mask = vessels_df[f"{vessels_details_prefix}vessel_quality"].notna()
    vessels_df.loc[vessel_quality_mask, f"{modelling_prefix}vessel_quality"] = (
        vessels_df[f"{vessels_details_prefix}vessel_quality"].map(
            vessel_quality_table.set_index("vessel_quality")["default"]
        )
    )
    del vessel_quality_table
    columns_to_keep.append(f"{modelling_prefix}vessel_quality")

    area_of_operation_mask = vessels_df[
        f"{vessels_details_prefix}area_of_operation"
    ].notna()
    vessels_df.loc[
        area_of_operation_mask,
        f"{modelling_prefix}area_of_operation",
    ] = vessels_df[f"{vessels_details_prefix}area_of_operation"].map(
        area_of_operation_table.set_index("area_of_operation")["default"]
    )
    del area_of_operation_table
    columns_to_keep.append(f"{modelling_prefix}area_of_operation")

    fleet_casualty_history_mask = (
        fleet_casualty_history_table["fleet_casualty_history"] == fleet_casualty_history
    )

    if fleet_casualty_history_mask.any():
        vessels_df[f"{modelling_prefix}fleet_casualty_history"] = (
            fleet_casualty_history_table.loc[
                fleet_casualty_history_mask, "default"
            ].iloc[0]
        )
        columns_to_keep.append(f"{modelling_prefix}fleet_casualty_history")
    del fleet_casualty_history_table

    owner_quality_mask = owner_quality_table["owner_quality"] == owner_quality
    if owner_quality_mask.any():
        vessels_df[f"{modelling_prefix}owner_quality"] = owner_quality_table.loc[
            owner_quality_mask, "default"
        ].iloc[0]
        columns_to_keep.append(f"{modelling_prefix}owner_quality")
    del owner_quality_table

    vessels_df[f"{modelling_prefix}uw_adjustment"] = 1 + vessels_df["uw_adjustment"]
    columns_to_keep.append(f"{modelling_prefix}uw_adjustment")

    # Produce the aggergate UW adjustment factors
    vessels_df[f"{modelling_prefix}agg_uw_adjustment"] = (
        vessels_df[f"{modelling_prefix}uw_adjustment"].fillna(1)
        * vessels_df[f"{modelling_prefix}freight_conditions"].fillna(1)
        * vessels_df[f"{modelling_prefix}vessel_quality"].fillna(1)
        * vessels_df[f"{modelling_prefix}area_of_operation"].fillna(1)
        * vessels_df[f"{modelling_prefix}fleet_casualty_history"].fillna(1)
        * vessels_df[f"{modelling_prefix}owner_quality"].fillna(1)
    )
    columns_to_keep.append(f"{modelling_prefix}agg_uw_adjustment")


    # YZ: Start working on the static model: Do we need to change the location of this code?
    vessels_df[f"{static_prefix}base"] = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "HullStaticModelBaseFreq", "value"
    ].iloc[0]
    vessels_df[f"{static_prefix}{build_up_prefix}base"] = vessels_df[
        f"{static_prefix}base"
    ]
    columns_to_keep.extend(
        [f"{static_prefix}base", f"{static_prefix}{build_up_prefix}base"]
    )

    # Clean the Vessel type for rating
    vessel_type_mask = vessels_imo_mask & vessels_df[f"vessel_type"].notna()
    vessels_df.loc[vessel_type_mask, "mapped_vessel_type"] = np.where(
        vessels_df.loc[vessel_type_mask, "vessel_type"]
        == vessels_df.loc[vessel_type_mask, "raw_ship_type"],
        vessels_df.loc[vessel_type_mask, "ship_type"],
        np.nan,
    )

    # Make sure that the vessel type is alligned with values in Freq tables
    # !!! Please check the parameter table vessel type columns have no space but underscore!!!
    vessels_df["mapped_vessel_type"] = vessels_df["mapped_vessel_type"].str.replace(
        " ", "_", regex=False
    )

    vessel_type_table = hx.params.table_vessel_types
    vessels_df.loc[vessel_type_mask, "mapped_vessel_type"] = vessels_df[
        "mapped_vessel_type"
    ].fillna(
        vessels_df.loc[vessel_type_mask, "vessel_type"].map(
            vessel_type_table.set_index("vessel_type")["vessel_type_group"]
        )
    )
    del vessel_type_table

    for model_type in model_types:
        model_prefix = model_prefix_map[model_type]

        """
            STATIC AND BEHAVIOURAL fleet size calculation
            """
        
        fleet_size = hxd.cds.exposure.granular.vessels.hull_rating.fleet_size

        if fleet_size > 0 :
            fleet_size_table = getattr(
                hx.params, f"table_{model_type}_fleet_size"
            )

            fleet_size_lookup_dict = dict(zip(fleet_size_table["fleet_size"], fleet_size_table["smoothed_factor"]))
            fleet_size_capped = (min(300, fleet_size)) # The parameter table will only be up to 300
            fleet_size_relativity = fleet_size_lookup_dict.get(fleet_size_capped)

            fleet_size_mask = vessels_imo_mask # only assign relativity to those valid imos
            vessels_df.loc[fleet_size_mask, f"{model_prefix}fleet_size"] = fleet_size_relativity
            # what does this build_up_prefix doing?
            vessels_df.loc[fleet_size_mask, f"{model_prefix}{build_up_prefix}fleet_size",
            ] = vessels_df.loc[fleet_size_mask, f"{model_prefix}fleet_size"] 
            columns_to_keep.extend(
                [
                    f"{model_prefix}fleet_size",
                    f"{model_prefix}{build_up_prefix}fleet_size",
                ]
            )

        """
            STATIC AND BEHAVIOURAL year built calculation
            """
        if vessels_df[f"{modelling_prefix}year_built"].any():
            build_year_table = getattr(
                hx.params, f"table_{model_type}_build_year_parameters"
            )
            build_year_table.rename(
                columns={"parameter": f"{model_prefix}_year_parameter"},
                inplace=True,
            )
            large_load_year_bins = build_year_table["lower_band"].tolist() + [
                float("inf")
            ]
            large_load_year_labels = build_year_table[
                f"{model_prefix}_year_parameter"
            ].tolist()
            build_year_mask = vessels_df[f"{vessels_details_prefix}imo"].notna()
            vessels_df.loc[build_year_mask, f"{model_prefix}year_built"] = pd.cut(
                vessels_df.loc[build_year_mask, f"year_built"].fillna(avg_build_year),
                bins=large_load_year_bins,
                labels=large_load_year_labels,
                right=False,
                ordered = False
            ).astype(float)
            vessels_df.loc[
                build_year_mask,
                f"{model_prefix}{build_up_prefix}year_built",
            ] = vessels_df.loc[build_year_mask, f"{model_prefix}year_built"]
            columns_to_keep.extend(
                [
                    f"{model_prefix}year_built",
                    f"{model_prefix}{build_up_prefix}year_built",
                ]
            )

            del build_year_table

        """
            STATIC AND BEHAVIOURAL FLAG MAPPING CALCULATION
            IT MAPS TO A GENERIC TABLE TO GET THE REGION TYPE
            THEN MAPS TO STATIC AND BEHAVIOURAL FREQUENCY TABLES TO GET THE FACTOR
        """
        flags_table = hx.params.table_flags
        flag_mask = vessels_imo_mask & vessels_df[f"flag"].notna()
        vessels_df["mapping_flag"] = vessels_df.loc[flag_mask, f"flag"].map(
            flags_table.set_index("vessel_flag")["model_mapping"]
        )
        del flags_table
        freq_flag_table = getattr(hx.params, f"table_{model_type}_freq_flag")
        vessels_df.loc[flag_mask, f"{model_prefix}flag"] = vessels_df.loc[
            flag_mask, "mapping_flag"
        ].map(freq_flag_table.set_index("flag")["factor"])

        vessels_df.loc[flag_mask, f"{model_prefix}{build_up_prefix}flag"] = (
            vessels_df.loc[flag_mask, f"{model_prefix}flag"]
        )
        del freq_flag_table
        columns_to_keep.extend(
            [f"{model_prefix}flag", f"{model_prefix}{build_up_prefix}flag"]
        )

        freq_vessel_type_table = getattr(
            hx.params, f"table_{model_type}_freq_vessel_type"
        )
        vessels_df.loc[
            vessel_type_mask, f"{model_prefix}{frequency_prefix}vessel_type"
        ] = vessels_df.loc[vessel_type_mask, "mapped_vessel_type"].map(
            freq_vessel_type_table.set_index("vessel_type")["parameter"]
        )
        del freq_vessel_type_table
        vessels_df.loc[
            vessel_type_mask,
            f"{model_prefix}{build_up_prefix}{frequency_prefix}vessel_type",
        ] = vessels_df.loc[
            vessel_type_mask, f"{model_prefix}{frequency_prefix}vessel_type"
        ]
        columns_to_keep.extend(
            [
                f"{model_prefix}{frequency_prefix}vessel_type",
                f"{model_prefix}{build_up_prefix}{frequency_prefix}vessel_type",
            ]
        )

        """
            STATIC AND BEHAVIOURAL DWT MAPPING CALCULATION
            """

        if vessels_df[f"dwt"].notna().any():
            dwt_table = getattr(hx.params, f"table_{model_type}_freq_dwt")
            dwt_mask = vessels_imo_mask & vessels_df[f"dwt"].notna()
            dwt_bins = dwt_table["lower_bound"].tolist() + [float("inf")]
            dwt_labels = dwt_table["lower_bound_factor"].tolist()

            cut_result = pd.cut(
                vessels_df.loc[dwt_mask, f"dwt"],
                bins=dwt_bins,
                labels=dwt_labels,
                right=False,
            )

            cut_result_indexes = cut_result.cat.codes

            lower_bounds = []
            upper_bounds = []
            lower_bound_factors = []
            upper_bound_factors = []
            for idx in cut_result_indexes:
                row = dwt_table.iloc[idx]
                lower_bounds.append(row["lower_bound"])
                upper_bounds.append(row["upper_bound"])
                lower_bound_factors.append(row["lower_bound_factor"])
                upper_bound_factors.append(row["upper_bound_factor"])

            dwt_df = pd.DataFrame(
                {
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_lower_bound": lower_bounds,
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_upper_bound": upper_bounds,
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_lower_bound_factor": lower_bound_factors,
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_upper_bound_factor": upper_bound_factors,
                }
            )

            vessels_df.loc[
                dwt_mask,
                [
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_lower_bound",
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_upper_bound",
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_lower_bound_factor",
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_upper_bound_factor",
                ],
            ] = dwt_df.values

            del dwt_table
            vessels_df.loc[
                dwt_mask, f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt"
            ] = vessels_df.loc[dwt_mask].apply(
                apply_forecast,
                axis=1,
                model_prefix=model_prefix,
                build_up_prefix=build_up_prefix,
                frequency_prefix=frequency_prefix,
                vessels_details_prefix=vessels_details_prefix,
            )
            vessels_df[f"{model_prefix}{frequency_prefix}dwt"] = vessels_df[
                f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt"
            ]
            columns_to_keep.extend(
                [
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_lower_bound",
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_upper_bound",
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_lower_bound_factor",
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_upper_bound_factor",
                    f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt",
                    f"{model_prefix}{frequency_prefix}dwt",
                ]
            )
    
    #End for

    # aggregate all the relativities together for Static. Behavioural will be at the later steps outside the loop.     

    vessels_df.loc[
        vessels_imo_mask,
        f"{static_prefix}{build_up_prefix}{frequency_prefix}predicted",
    ] = (
        safe_get_and_fillna(vessels_df.loc[vessels_imo_mask], f"{static_prefix}base", 1)
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask], f"{static_prefix}fleet_size", 1
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask], f"{static_prefix}year_built", 1
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask], f"{static_prefix}flag", 1
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask],
            f"{static_prefix}{frequency_prefix}vessel_type",
            1,
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask],
            f"{static_prefix}{frequency_prefix}dwt",
            1,
        )
    )

    #Severity base rate. YZ: This is an odd place. Need to move it to Severity coding
    hull_sev_intercept = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "HullModelSevIntercept", "value"
    ].iloc[0]

    hull_sev_year_built = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "HullModelSevYearBuilt", "value"
    ].iloc[0]

    hull_sev_agreed_value = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "HullModelSevAgreedValue", "value"
    ].iloc[0]

    columns_to_keep.append(
        f"{static_prefix}{build_up_prefix}{frequency_prefix}predicted"
    )

    vessels_df["expiry_date"] = pd.to_datetime(
        vessels_df["expiry_date"], errors="coerce"
    )
    vessels_df["inception_date"] = pd.to_datetime(
        vessels_df["inception_date"], errors="coerce"
    )

    pro_rata_mask = (
        vessels_imo_mask
        & vessels_df[f"inception_date"].notna()
        & vessels_df[f"expiry_date"].notna()
        & (vessels_df[f"expiry_date"] > vessels_df[f"inception_date"])
        & (vessels_df[f"expiry_date"] > pd.Timestamp("1900-01-01"))
        & (vessels_df[f"inception_date"] > pd.Timestamp("1900-01-01"))
    )

    days_in_period = (
        None
        if vessels_df.loc[pro_rata_mask].empty
        else (
            vessels_df.loc[pro_rata_mask, f"expiry_date"]
            - vessels_df.loc[pro_rata_mask, f"inception_date"]
        ).dt.days
        + 1.0
    )

    days_in_year = vessels_df.loc[pro_rata_mask, "inception_date"].apply(
        lambda x: (366 if calendar.isleap(x.year) else 365)
    )

    vessels_df.loc[pro_rata_mask, "pro_rata_adjustment"] = (
        float("nan")
        if (days_in_period is None) or (days_in_year is None)
        else (days_in_period / days_in_year)
    )

    columns_to_keep.append("pro_rata_adjustment")

    """
    BEHAVIOURAL BUILD UP CALCULATIONS
    THE BASIC MASK FOR BEHAVIOURAL BUILD UP CALCULATIONS IS TO HAVE AN AGE
    THE RELATIVE FACTORS WILL CONTINUE AS LONG AS THE IMO IS NOT NULL
    """

    vessels_df.loc[vessels_imo_mask, f"{behavioural_prefix}base"] = (
        modelling_parameters_table.loc[
            modelling_parameters_table["parameter"] == "HullBehaviouralModelBaseFreq",
            "value",
        ].iloc[0]
    )
    vessels_df.loc[vessels_imo_mask, f"{behavioural_prefix}{build_up_prefix}base"] = (
        vessels_df[f"{behavioural_prefix}base"]
    )
    columns_to_keep.extend(
        [f"{behavioural_prefix}base", f"{behavioural_prefix}{build_up_prefix}base"]
    )

    #Get parameter from GLM model
    max_distance_ratio = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"]
        == "HullBehaviouralModelMaxDistanceRatio",
        "value",
    ].iloc[0]
    num_unique_port_visits = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"]
        == "HullBehaviouralModelNumUniquePortVisits",
        "value",
    ].iloc[0]
    perc_time_eez = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "HullBehaviouralModelPercTimeEEZ",
        "value",
    ].iloc[0]
    ratio_moving = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "HullBehaviouralModelRatioMoving",
        "value",
    ].iloc[0]
    ratio_moored = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "HullBehaviouralModelRatioMoored",
        "value",
    ].iloc[0]

    #Get relativities for behavioural factors
    vessels_df.loc[
        vessels_imo_mask, f"{behavioural_prefix}{build_up_prefix}perc_time_eez"
    ] = (
        safe_get_and_fillna(vessels_df.loc[vessels_imo_mask], "perc_time_eez", 0)
        * perc_time_eez
    ).apply(
        math.exp
    )
    vessels_df.loc[vessels_imo_mask, f"{behavioural_prefix}perc_time_eez"] = (
        vessels_df.loc[
            vessels_imo_mask, f"{behavioural_prefix}{build_up_prefix}perc_time_eez"
        ]
    )

    vessels_df.loc[
        vessels_imo_mask, f"{behavioural_prefix}{build_up_prefix}ratio_moving"
    ] = (
        safe_get_and_fillna(vessels_df.loc[vessels_imo_mask], "ratio_moving", 0)
        * ratio_moving
    ).apply(
        math.exp
    )
    vessels_df.loc[vessels_imo_mask, f"{behavioural_prefix}ratio_moving"] = (
        vessels_df.loc[
            vessels_imo_mask, f"{behavioural_prefix}{build_up_prefix}ratio_moving"
        ]
    )

    vessels_df.loc[
        vessels_imo_mask,
        f"{behavioural_prefix}{build_up_prefix}number_of_unique_port_visits",
    ] = (
        safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask], "number_of_unique_port_visits", 0
        )
        * num_unique_port_visits
    ).apply(
        math.exp
    )
    vessels_df.loc[
        vessels_imo_mask, f"{behavioural_prefix}number_of_unique_port_visits"
    ] = vessels_df.loc[
        vessels_imo_mask,
        f"{behavioural_prefix}{build_up_prefix}number_of_unique_port_visits",
    ]

    vessels_df.loc[
        vessels_imo_mask, f"{behavioural_prefix}{build_up_prefix}max_distance_ratio"
    ] = (
        safe_get_and_fillna(vessels_df.loc[vessels_imo_mask], "max_distance_ratio", 0)
        * max_distance_ratio
    ).apply(
        math.exp
    )
    vessels_df.loc[vessels_imo_mask, f"{behavioural_prefix}max_distance_ratio"] = (
        vessels_df.loc[
            vessels_imo_mask, f"{behavioural_prefix}{build_up_prefix}max_distance_ratio"
        ]
    )

    vessels_df.loc[
        vessels_imo_mask, f"{behavioural_prefix}{build_up_prefix}ratio_moored"
    ] = (
        safe_get_and_fillna(vessels_df.loc[vessels_imo_mask], "ratio_moored", 0)
        * ratio_moored
    ).apply(
        math.exp
    )
    vessels_df.loc[vessels_imo_mask, f"{behavioural_prefix}ratio_moored"] = (
        vessels_df.loc[
            vessels_imo_mask, f"{behavioural_prefix}{build_up_prefix}ratio_moored"
        ]
    )


    #Aggregate the relativities for Behavioural Freqency 
    vessels_df.loc[
        vessels_imo_mask,
        f"{behavioural_prefix}{build_up_prefix}{frequency_prefix}predicted",
    ] = (
        safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask], f"{behavioural_prefix}base", 1
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask], f"{behavioural_prefix}fleet_size", 1
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask], f"{behavioural_prefix}year_built", 1
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask], f"{behavioural_prefix}flag", 1
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask],
            f"{behavioural_prefix}{frequency_prefix}vessel_type",
            1,
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask],
            f"{behavioural_prefix}{frequency_prefix}dwt",
            1,
        )
        * safe_get_and_fillna(
            vessels_df.loc[vessels_imo_mask],
            f"{behavioural_prefix}{build_up_prefix}ratio_moored", 1
        )
        # * safe_get_and_fillna(
        #     vessels_df.loc[vessels_imo_mask],
        #     f"{behavioural_prefix}{build_up_prefix}perc_time_eez",
        #     1,
        # )
        # * safe_get_and_fillna(
        #     vessels_df.loc[vessels_imo_mask],
        #     f"{behavioural_prefix}{build_up_prefix}ratio_moving",
        #     1,
        # )
        # * safe_get_and_fillna(
        #     vessels_df.loc[vessels_imo_mask],
        #     f"{behavioural_prefix}{build_up_prefix}number_of_unique_port_visits",
        #     1,
        # )
        # * safe_get_and_fillna(
        #     vessels_df.loc[vessels_imo_mask],
        #     f"{behavioural_prefix}{build_up_prefix}max_distance_ratio",
        #     1,
        # )
    )

    #This could consider to remove for the four rating factors
    vessels_df.loc[
        vessels_df["perc_time_eez"].notna(), "modelling_behavioural_perc_time_eez"
    ] = vessels_df.loc[vessels_df["perc_time_eez"].notna(), "perc_time_eez"]

    vessels_df.loc[
        vessels_df["ratio_moving"].notna(), "modelling_behavioural_ratio_moving"
    ] = vessels_df.loc[vessels_df["ratio_moving"].notna(), "ratio_moving"]

    vessels_df.loc[
        vessels_df["unique_port_ratio"].notna(),
        "modelling_behavioural_number_of_unique_port_visits",
    ] = vessels_df.loc[vessels_df["unique_port_ratio"].notna(), "unique_port_ratio"]

    vessels_df.loc[
        vessels_df["max_distance_ratio"].notna(),
        "modelling_behavioural_max_distance_ratio",
    ] = vessels_df.loc[vessels_df["max_distance_ratio"].notna(), "max_distance_ratio"]

    vessels_df.loc[
        vessels_df["ratio_moored"].notna(),
        "modelling_behavioural_ratio_moored",
    ] = vessels_df.loc[vessels_df["ratio_moored"].notna(), "ratio_moored"]

    columns_to_keep.extend(
        [
            f"{behavioural_prefix}{build_up_prefix}perc_time_eez",
            f"{behavioural_prefix}perc_time_eez",
            f"{behavioural_prefix}{build_up_prefix}ratio_moving",
            f"{behavioural_prefix}ratio_moving",
            f"{behavioural_prefix}{build_up_prefix}number_of_unique_port_visits",
            f"{behavioural_prefix}number_of_unique_port_visits",
            f"{behavioural_prefix}{build_up_prefix}max_distance_ratio",
            f"{behavioural_prefix}max_distance_ratio",
            f"{behavioural_prefix}{build_up_prefix}ratio_moored",
            f"{behavioural_prefix}ratio_moored",
            f"{behavioural_prefix}{build_up_prefix}{frequency_prefix}predicted",
            "modelling_behavioural_perc_time_eez",
            "modelling_behavioural_ratio_moving",
            "modelling_behavioural_number_of_unique_port_visits",
            "modelling_behavioural_max_distance_ratio",
            "modelling_behavioural_ratio_moored",
        ]
    )

    # Convert the agreed value to USD 
    converted_agreed_value_mask = (
        vessels_imo_mask
        & (vessels_df[f"{modelling_prefix}agreed_value"].notna())
        & (vessels_df[f"{modelling_prefix}agreed_value"] > 0)
    )
    vessels_df.loc[
        converted_agreed_value_mask,
        f"{modelling_prefix}converted_agreed_value",
    ] = np.where(
        vessels_df.loc[converted_agreed_value_mask, "coverage"] == "CL 290",
        vessels_df.loc[converted_agreed_value_mask, f"{modelling_prefix}agreed_value"]
        .div(conversion_rate)
        .mul(4),
        vessels_df.loc[
            converted_agreed_value_mask, f"{modelling_prefix}agreed_value"
        ].div(conversion_rate),
    )
    columns_to_keep.append(f"{modelling_prefix}converted_agreed_value")

    # YZ: Start severity from here
    vessels_severity_table = hx.params.table_sev_vessel_type
    for model_type in model_types:
        model_prefix = model_prefix_map[model_type]
        if vessels_df[f"{modelling_prefix}year_built"].any():
            vessels_df[
                f"{model_prefix}{severity_prefix}base_x_build_year_x_agreed_value"
            ] = (
                hull_sev_intercept
                + (
                    (
                        vessels_df[f"{modelling_prefix}year_built"].fillna(
                            avg_build_year
                        )
                    ).mul(hull_sev_year_built)
                )
                + (
                    vessels_df.loc[
                        converted_agreed_value_mask,
                        f"{modelling_prefix}converted_agreed_value",
                    ]
                    .apply(math.log)
                    .mul(hull_sev_agreed_value)
                )
            ).apply(
                math.exp
            )

            # From here to work on Severity rating:
            vessels_df[
                f"{model_prefix}{build_up_prefix}{severity_prefix}base_x_build_year_x_agreed_value"
            ] = vessels_df[
                f"{model_prefix}{severity_prefix}base_x_build_year_x_agreed_value"
            ]
            columns_to_keep.extend(
                [
                    f"{model_prefix}{severity_prefix}base_x_build_year_x_agreed_value",
                    f"{model_prefix}{build_up_prefix}{severity_prefix}base_x_build_year_x_agreed_value",
                ]
            )
        vessels_df.loc[
            vessel_type_mask, f"{model_prefix}{severity_prefix}vessel_type"
        ] = vessels_df.loc[vessel_type_mask, "mapped_vessel_type"].map(
            vessels_severity_table.set_index("vessel_type")["parameter"]
        )
        vessels_df.loc[
            vessel_type_mask,
            f"{model_prefix}{build_up_prefix}{severity_prefix}vessel_type",
        ] = vessels_df.loc[
            vessel_type_mask, f"{model_prefix}{severity_prefix}vessel_type"
        ]
        columns_to_keep.extend(
            [
                f"{model_prefix}{severity_prefix}vessel_type",
                f"{model_prefix}{build_up_prefix}{severity_prefix}vessel_type",
            ]
        )

        if vessels_df[f"dwt"].notna().any():
            dwt_table = hx.params.table_sev_dwt
            dwt_mask = vessels_imo_mask & vessels_df[f"dwt"].notna()
            dwt_bins = dwt_table["lower_bound"].tolist() + [float("inf")]
            dwt_labels = dwt_table["lower_bound_factor"].tolist()

            cut_result = pd.cut(
                vessels_df.loc[dwt_mask, f"dwt"],
                bins=dwt_bins,
                labels=dwt_labels,
                right=False,
            )

            cut_result_indexes = cut_result.cat.codes

            lower_bounds = []
            upper_bounds = []
            lower_bound_factors = []
            upper_bound_factors = []
            for idx in cut_result_indexes:
                row = dwt_table.iloc[idx]
                lower_bounds.append(row["lower_bound"])
                upper_bounds.append(row["upper_bound"])
                lower_bound_factors.append(row["lower_bound_factor"])
                upper_bound_factors.append(row["upper_bound_factor"])

            dwt_df = pd.DataFrame(
                {
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_lower_bound": lower_bounds,
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_upper_bound": upper_bounds,
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_lower_bound_factor": lower_bound_factors,
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_upper_bound_factor": upper_bound_factors,
                }
            )

            vessels_df.loc[
                dwt_mask,
                [
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_lower_bound",
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_upper_bound",
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_lower_bound_factor",
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_upper_bound_factor",
                ],
            ] = dwt_df.values

            del dwt_table
            vessels_df.loc[
                dwt_mask,
                f"{model_prefix}{build_up_prefix}{severity_prefix}dwt",
            ] = vessels_df.loc[dwt_mask].apply(
                apply_forecast,
                axis=1,
                model_prefix=model_prefix,
                build_up_prefix=build_up_prefix,
                frequency_prefix=severity_prefix,
                vessels_details_prefix=vessels_details_prefix,
            )
            vessels_df[f"{model_prefix}{severity_prefix}dwt"] = vessels_df[
                f"{model_prefix}{build_up_prefix}{severity_prefix}dwt"
            ]
            columns_to_keep.extend(
                [
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_lower_bound",
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_upper_bound",
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_lower_bound_factor",
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt_upper_bound_factor",
                    f"{model_prefix}{build_up_prefix}{severity_prefix}dwt",
                    f"{model_prefix}{severity_prefix}dwt",
                ]
            )

        vessels_df.loc[
            vessels_imo_mask,
            f"{model_prefix}{build_up_prefix}{severity_prefix}predicted",
        ] = (
            safe_get_and_fillna(
                vessels_df.loc[vessels_imo_mask],
                f"{model_prefix}{build_up_prefix}{severity_prefix}base_x_build_year_x_agreed_value",
                1,
            )
            * safe_get_and_fillna(
                vessels_df.loc[vessels_imo_mask],
                f"{model_prefix}{build_up_prefix}{severity_prefix}dwt",
                1,
            )
            * safe_get_and_fillna(
                vessels_df.loc[vessels_imo_mask],
                f"{model_prefix}{build_up_prefix}{severity_prefix}vessel_type",
                1,
            )
        )
        columns_to_keep.append(
            f"{model_prefix}{build_up_prefix}{severity_prefix}predicted"
        )
        severity_model_mask = (
            vessels_imo_mask
            & vessels_df[
                f"{model_prefix}{build_up_prefix}{severity_prefix}predicted"
            ].notna()
            & vessels_df[f"{modelling_prefix}agreed_value"].notna()
        )
        vessels_df.loc[
            severity_model_mask,
            f"{model_prefix}{build_up_prefix}{severity_prefix}model",
        ] = (
            vessels_df.loc[
                severity_model_mask,
                f"{model_prefix}{build_up_prefix}{severity_prefix}predicted",
            ]
            * vessels_df.loc[severity_model_mask, f"{modelling_prefix}agreed_value"]
        )
        columns_to_keep.append(f"{model_prefix}{build_up_prefix}{severity_prefix}model")

        vessels_df.loc[
            severity_model_mask,
            f"{model_prefix}{build_up_prefix}expected_loss",
        ] = (
            vessels_df.loc[
                severity_model_mask,
                f"{model_prefix}{build_up_prefix}{severity_prefix}model",
            ]
            * vessels_df.loc[
                severity_model_mask,
                f"{model_prefix}{build_up_prefix}{frequency_prefix}predicted",
            ]
        )
        columns_to_keep.append(f"{model_prefix}{build_up_prefix}expected_loss")

        model_frequency_mask = (
            vessels_df[
                f"{model_prefix}{build_up_prefix}{frequency_prefix}predicted"
            ].notna()
            & vessels_df["pro_rata_adjustment"].notna()
        )
        vessels_df.loc[model_frequency_mask, f"{model_prefix}model_frequency"] = (
            vessels_df.loc[
                model_frequency_mask,
                f"{model_prefix}{build_up_prefix}{frequency_prefix}predicted",
            ]
            * vessels_df.loc[
                model_frequency_mask,
                f"pro_rata_adjustment",
            ]
        )
        columns_to_keep.append(f"{model_prefix}model_frequency")

        vessels_df.loc[severity_model_mask, f"{model_prefix}model_severity"] = (
            vessels_df.loc[
                severity_model_mask,
                f"{model_prefix}{build_up_prefix}{severity_prefix}model",
            ]
        )
        columns_to_keep.append(f"{model_prefix}model_severity")

        if vessels_df[f"{modelling_prefix}year_built"].any():
            large_loss_overlay_mask = (
                (
                    vessels_df[f"{modelling_prefix}agreed_value"].notna()
                    & vessel_type_mask
                    & vessels_df[f"pro_rata_adjustment"].notna()
                )
                if model_type == "static"
                else (
                    vessels_df[f"{modelling_prefix}agreed_value"].notna()
                    & vessel_type_mask
                    & vessels_df[f"pro_rata_adjustment"].notna()
                    & behavioural_mask
                )
            )
            large_load_build_year_table = (
                hx.params.table_large_load_build_year_relativity
            )
            large_load_build_year_table.rename(
                columns={"relativity": f"large_{model_prefix}year_relativity"},
                inplace=True,
            )
            large_load_year_bins = large_load_build_year_table[
                "lower_band"
            ].tolist() + [float("inf")]
            large_load_year_labels = large_load_build_year_table[
                f"large_{model_prefix}year_relativity"
            ].tolist()
            vessels_df.loc[
                large_loss_overlay_mask, f"{model_prefix}large_load_year"
            ] = pd.cut(
                vessels_df.loc[large_loss_overlay_mask, f"year_built"].fillna(
                    avg_build_year
                ),
                bins=large_load_year_bins,
                labels=large_load_year_labels,
                right=False,
                ordered=False,
            ).astype(
                float
            )

            large_br = modelling_parameters_table.loc[
                modelling_parameters_table["parameter"] == "LargeBR", "value"
            ].iloc[0]

            large_vessel_relativity_table = hx.params.table_large_vessel_relativity
            vessels_df.loc[
                large_loss_overlay_mask, f"{model_prefix}large_vessel_relativity"
            ] = vessels_df.loc[large_loss_overlay_mask, f"vessel_type"].map(
                large_vessel_relativity_table.set_index("vessel_type_long")[
                    "relativity"
                ]
            )
            del large_vessel_relativity_table

            vessels_df.loc[
                large_loss_overlay_mask, f"{model_prefix}large_loss_overlay"
            ] = (
                vessels_df.loc[
                    large_loss_overlay_mask, f"{modelling_prefix}agreed_value"
                ]
                .div(conversion_rate)
                .div(1000000)
                .mul(large_br)
                .mul(
                    vessels_df.loc[
                        large_loss_overlay_mask,
                        f"{model_prefix}large_vessel_relativity",
                    ]
                )
                .mul(
                    vessels_df.loc[
                        large_loss_overlay_mask, f"{model_prefix}large_load_year"
                    ]
                )
                .mul(conversion_rate)
                .mul(vessels_df.loc[large_loss_overlay_mask, "pro_rata_adjustment"])
            )
            columns_to_keep.append(f"{model_prefix}large_loss_overlay")

        # Calculate Coverage
        coverage_mask = (
            vessels_df[f"inception_date"].notna() & vessels_df[f"coverage"].notna()
            if model_type == "static"
            else (
                vessels_df[f"inception_date"].notna()
                & vessels_df[f"coverage"].notna()
                & behavioural_mask
            )
        )
        vessels_df.loc[coverage_mask, f"{model_prefix}coverage"] = vessels_df.loc[
            coverage_mask, "coverage"
        ]
        columns_to_keep.append(f"{model_prefix}coverage")
        coverage_table = hx.params.table_coverage_factor
        vessels_df.loc[coverage_mask, f"{model_prefix}coverage_factor"] = (
            vessels_df.loc[coverage_mask, "coverage"].map(
                coverage_table.set_index("coverage")["factor"]
            )
        )

        # Calculate large overlay
        expected_loss_mask = (
            vessels_df[f"{model_prefix}model_frequency"].notna()
            & vessels_df[f"{model_prefix}model_severity"].notna()
            & vessels_df[f"{model_prefix}coverage_factor"].notna()
        )
        vessels_df.loc[expected_loss_mask, f"{model_prefix}expected_loss"] = (
            vessels_df.loc[expected_loss_mask, f"{model_prefix}model_frequency"]
            .mul(vessels_df.loc[expected_loss_mask, f"{model_prefix}model_severity"])
            .add(
                safe_get_and_fillna(
                    vessels_df.loc[expected_loss_mask],
                    f"{model_prefix}large_loss_overlay",
                    0,
                )
            )
            .mul(vessels_df.loc[expected_loss_mask, f"{model_prefix}coverage_factor"])
        )
        columns_to_keep.append(f"{model_prefix}expected_loss")
        del coverage_table
        columns_to_keep.append(f"{model_prefix}coverage_factor")

        # Calculate deductible based on MBBEFDG3 curve
        deductible_mask = (
            vessels_df[f"inception_date"].notna()
            if model_type == "static"
            else (vessels_df[f"inception_date"].notna() & behavioural_mask)
        )
        vessels_df.loc[deductible_mask, f"{model_prefix}deductible"] = (
            vessels_df.loc[deductible_mask, "deductible"]
        ).fillna(0)
        columns_to_keep.append(f"{model_prefix}deductible")
        MBBEFDG3_mask = (
            vessels_df[f"{modelling_prefix}agreed_value"].notna()
            & (vessels_df[f"{modelling_prefix}agreed_value"] > 0)
            if model_type == "static"
            else (
                vessels_df[f"{modelling_prefix}agreed_value"].notna()
                & behavioural_mask
                & (vessels_df[f"{modelling_prefix}agreed_value"] > 0)
            )
        )
        MBBEFDG3_param = modelling_parameters_table.loc[
            modelling_parameters_table["parameter"] == "MBBDFDHullParam", "value"
        ].iloc[0]
        vessels_df.loc[MBBEFDG3_mask, f"{model_prefix}mbbefdg"] = vessels_df.loc[
            MBBEFDG3_mask
        ].apply(
            apply_mbbefdg3,
            axis=1,
            modelling_prefix=modelling_prefix,
            mbbefdg3_param=MBBEFDG3_param,
            model_prefix=model_prefix,
        )
        columns_to_keep.append(f"{model_prefix}mbbefdg")
        order_mask = (
            vessels_df[f"inception_date"].notna()
            if model_type == "static"
            else (vessels_df[f"inception_date"].notna() & behavioural_mask)
        )
        vessels_df.loc[order_mask, f"{model_prefix}order_percent"] = vessels_df.loc[
            order_mask, f"{vessels_details_prefix}order_percent"
        ]
        columns_to_keep.append(f"{model_prefix}order_percent")
        el_pre_uw_adj_mask = (
            vessels_df[f"{model_prefix}expected_loss"].notna()
            & vessels_df[f"{model_prefix}mbbefdg"].notna()
            & vessels_df[f"vessel_type"].notna()
            if model_type == "static"
            else (
                vessels_df[f"{model_prefix}expected_loss"].notna()
                & vessels_df[f"{model_prefix}mbbefdg"].notna()
                & behavioural_mask
            )
        )

        vessels_df.loc[el_pre_uw_adj_mask, f"{model_prefix}el_pre_uw_adj"] = (
            vessels_df.loc[el_pre_uw_adj_mask, f"{model_prefix}expected_loss"]
            .mul(vessels_df.loc[el_pre_uw_adj_mask, f"{model_prefix}mbbefdg"])
            .mul(1 + nmp_load)
        )
        columns_to_keep.append(f"{model_prefix}el_pre_uw_adj")
        vessels_df[f"{model_prefix}all_uw_adj"] = vessels_df[
            f"{modelling_prefix}agg_uw_adjustment"
        ].fillna(1)
        columns_to_keep.append(f"{model_prefix}all_uw_adj")
        el_post_uw_adj_mask = (
            vessels_df[f"{model_prefix}el_pre_uw_adj"].notna()
            & vessels_df[f"{model_prefix}all_uw_adj"].notna()
        )
        vessels_df.loc[el_post_uw_adj_mask, f"{model_prefix}el_post_uw_adj"] = (
            vessels_df.loc[el_post_uw_adj_mask, f"{model_prefix}el_pre_uw_adj"].mul(
                vessels_df.loc[el_post_uw_adj_mask, f"{model_prefix}all_uw_adj"]
            )
        )
        columns_to_keep.append(f"{model_prefix}el_post_uw_adj")
        base_mask = (
            vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
            & vessels_df[f"{model_prefix}base"].notna()
        )
        expected_loss_post_uw_adj_sum = vessels_df.loc[
            vessel_type_mask, f"{model_prefix}el_post_uw_adj"
        ].sum()
        if (not expected_loss_post_uw_adj_sum) or (expected_loss_post_uw_adj_sum == 0):
            continue
        model_relativity = getattr(fleet_average_relativity, model_type)
        try:
            setattr(
                model_relativity,
                "base",
                (
                    vessels_df.loc[base_mask, f"{model_prefix}el_post_uw_adj"]
                    .mul(vessels_df.loc[base_mask, f"{model_prefix}base"])
                    .sum()
                )
                / (expected_loss_post_uw_adj_sum),
            )
        except:
            pass

        vessel_columns = vessels_df.columns
        if f"{model_prefix}fleet_size" in vessel_columns:
            fleet_size_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}fleet_size"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "fleet_size",
                    (
                        vessels_df.loc[fleet_size_mask, f"{model_prefix}el_post_uw_adj"]
                        .mul(
                            vessels_df.loc[fleet_size_mask, f"{model_prefix}fleet_size"]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        vessel_columns = vessels_df.columns
        if f"{model_prefix}year_built" in vessel_columns:
            year_built_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}year_built"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "year_built",
                    (
                        vessels_df.loc[year_built_mask, f"{model_prefix}el_post_uw_adj"]
                        .mul(
                            vessels_df.loc[year_built_mask, f"{model_prefix}year_built"]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}flag" in vessel_columns:
            flag_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}flag"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "flag",
                    (
                        vessels_df.loc[flag_mask, f"{model_prefix}el_post_uw_adj"]
                        .mul(vessels_df.loc[flag_mask, f"{model_prefix}flag"])
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}{frequency_prefix}vessel_type" in vessel_columns:
            vessel_type_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}{frequency_prefix}vessel_type"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "frequency_vessel_type",
                    (
                        vessels_df.loc[
                            vessel_type_mask, f"{model_prefix}el_post_uw_adj"
                        ]
                        .mul(
                            vessels_df.loc[
                                vessel_type_mask,
                                f"{model_prefix}{frequency_prefix}vessel_type",
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}{frequency_prefix}dwt" in vessel_columns:
            dwt_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}{frequency_prefix}dwt"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "frequency_dwt",
                    (
                        vessels_df.loc[dwt_mask, f"{model_prefix}el_post_uw_adj"]
                        .mul(
                            vessels_df.loc[
                                dwt_mask, f"{model_prefix}{frequency_prefix}dwt"
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if (
            f"{model_prefix}{severity_prefix}base_x_build_year_x_agreed_value"
            in vessel_columns
        ):
            base_x_year_x_value_mask = vessels_df[
                f"{model_prefix}{severity_prefix}base_x_build_year_x_agreed_value"
            ].notna()
            try:
                setattr(
                    model_relativity,
                    "base_x_year_x_value",
                    (
                        vessels_df.loc[
                            base_x_year_x_value_mask,
                            f"{model_prefix}el_post_uw_adj",
                        ]
                        .mul(
                            vessels_df.loc[
                                base_x_year_x_value_mask,
                                f"{model_prefix}{severity_prefix}base_x_build_year_x_agreed_value",
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}{severity_prefix}vessel_type" in vessel_columns:
            severity_vessel_type_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}{severity_prefix}vessel_type"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "severity_vessel_type",
                    (
                        vessels_df.loc[
                            severity_vessel_type_mask, f"{model_prefix}el_post_uw_adj"
                        ]
                        .mul(
                            vessels_df.loc[
                                severity_vessel_type_mask,
                                f"{model_prefix}{severity_prefix}vessel_type",
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}{severity_prefix}dwt" in vessel_columns:
            severity_dwt_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}{severity_prefix}dwt"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "severity_dwt",
                    (
                        vessels_df.loc[
                            severity_dwt_mask, f"{model_prefix}el_post_uw_adj"
                        ]
                        .mul(
                            vessels_df.loc[
                                severity_dwt_mask, f"{model_prefix}{severity_prefix}dwt"
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}max_distance_ratio" in vessel_columns:
            max_distance_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}max_distance_ratio"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "max_distance_ratio",
                    (
                        vessels_df.loc[
                            max_distance_mask, f"{model_prefix}el_post_uw_adj"
                        ]
                        .mul(
                            vessels_df.loc[
                                max_distance_mask, f"{model_prefix}max_distance_ratio"
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}number_of_unique_port_visits" in vessel_columns:
            unique_port_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}number_of_unique_port_visits"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "number_of_unique_port_visits",
                    (
                        vessels_df.loc[
                            unique_port_mask, f"{model_prefix}el_post_uw_adj"
                        ]
                        .mul(
                            vessels_df.loc[
                                unique_port_mask,
                                f"{model_prefix}number_of_unique_port_visits",
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}perc_time_eez" in vessel_columns:
            perc_time_eez_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}perc_time_eez"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "perc_time_eez",
                    (
                        vessels_df.loc[
                            perc_time_eez_mask, f"{model_prefix}el_post_uw_adj"
                        ]
                        .mul(
                            vessels_df.loc[
                                perc_time_eez_mask, f"{model_prefix}perc_time_eez"
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}ratio_moving" in vessel_columns:
            ratio_moving_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}ratio_moving"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "ratio_moving",
                    (
                        vessels_df.loc[
                            ratio_moving_mask, f"{model_prefix}el_post_uw_adj"
                        ]
                        .mul(
                            vessels_df.loc[
                                ratio_moving_mask, f"{model_prefix}ratio_moving"
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

        if f"{model_prefix}ratio_moored" in vessel_columns:
            ratio_moving_mask = (
                vessels_df[f"{model_prefix}el_post_uw_adj"].notna()
                & vessels_df[f"{model_prefix}ratio_moored"].notna()
            )
            try:
                setattr(
                    model_relativity,
                    "ratio_moored",
                    (
                        vessels_df.loc[
                            ratio_moving_mask, f"{model_prefix}el_post_uw_adj"
                        ]
                        .mul(
                            vessels_df.loc[
                                ratio_moving_mask, f"{model_prefix}ratio_moored"
                            ]
                        )
                        .sum()
                    )
                    / (expected_loss_post_uw_adj_sum),
                )
            except:
                pass

    del vessels_severity_table

    write_pd_to_hxd(vessels_df, vessels_list, ["unique_imo", "mapped_vessel_type"])

    vessels_df = vessels_df[columns_to_keep]
    vessels_df = vessels_df.replace({np.nan: None})

    hxd.cds.exposure.granular.vessels.hull_rating.modelling_list = vessels_df.to_dict(
        orient="records"
    )


def apply_mbbefdg3(row, model_prefix, modelling_prefix, mbbefdg3_param):
    return 1 - MBBEFDG3(
        mbbefdg3_param,
        row[f"{model_prefix}deductible"] / row[f"{modelling_prefix}agreed_value"],
    )


def apply_forecast(
    row, model_prefix, build_up_prefix, frequency_prefix, vessels_details_prefix
):
    return forecast(
        [
            row[f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_lower_bound"],
            row[f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_upper_bound"],
        ],
        [
            row[
                f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_lower_bound_factor"
            ],
            row[
                f"{model_prefix}{build_up_prefix}{frequency_prefix}dwt_upper_bound_factor"
            ],
        ],
        row[f"dwt"],
    )
