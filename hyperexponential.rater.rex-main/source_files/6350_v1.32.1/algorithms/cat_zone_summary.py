import hx
import polars as pl
import pandas as pd
import numpy as np



def cat_zone_summary(hxd, df, other_data):

    df = calc_location_deductible(hxd, df)
    cat_zone_dict, gate_dict = calc_exposed_tiv(hxd, df, other_data)
    cat_zone_hxd_assignment(hxd, df, cat_zone_dict)
    gate_hxd_assignment(hxd, df, gate_dict)

    return df


def calc_exposed_tiv(hxd, df, other_data):
    # Load parameter tables
    fl_tiers = pl.from_pandas(hx.params.fl_tiers)
    fl_tiers = fl_tiers.select("Zone", "All A and V")

    exchange_rate = hxd.policy_information.exchange_rate

    df = df.join(fl_tiers, left_on = "floodzone", right_on = "Zone", how = "left")
    df = df.with_columns(pl.col("All A and V").fill_null(0).alias("All A and V"))

    cat_zone_dict = {}
    gate_dict = {}

    df = df.with_columns(
        (pl.col(f"tiv_total_usd") * pl.col("All A and V")).alias(f"tiv_total_usd_flood_zone_av")
    )

    for peril in ["eq", "ws"]:
        for index, layer in enumerate(hxd.layers, start=1):
            # Assign peril structure name
            peril_struct_name = "quake" if peril == "eq" else "named_windstorm"

            # Check if peril is included in layer
            included = getattr(layer.perils, peril_struct_name).include
            
            # Retrieve either written line or quoted line
            line = layer.written_line_perc if layer.written_line_perc > 0 else ( 
                layer.quoted_line_perc if layer.quoted_line_perc > 0 else 1
            )
            
            # Retrieve per occurrence deductibles
            per_occurrence_ded = getattr(layer.perils, peril_struct_name).per_occurrence_ded
            per_occurrence_ded_usd = (per_occurrence_ded or 0) / exchange_rate if exchange_rate else (per_occurrence_ded or 0)

            # Retrieve Regional Sublimit for US and Intl
            df = df.with_columns(pl.when(pl.col("country") == "United States")
                .then(pl.col(f"{peril}_selected_sublimit_layer{index}"))
                .otherwise(pl.col(f"{peril}_country_sublimit"))
                .fill_null(0)
                .cast(pl.Float64)
                .alias(f"{peril}_regional_sublimit_layer{index}")
            )

            # Regional Limit to Apply
            df = df.with_columns(pl.when(pl.col(f"{peril}_regional_sublimit_layer{index}") == 0)
                .then(other_data[f"policy_limit_usd_layer{index}"] + other_data[f"policy_excess_usd_layer{index}"])
                .otherwise(pl.col(f"{peril}_regional_sublimit_layer{index}"))
                .alias(f"{peril}_regional_limit_to_use_layer{index}"))

            # Aggregate location level exposed by tiv into respective cat regions and zones
            peril_cat_zone_df = (
                df.select(
                    f"{peril}_crit_cat_zone",
                    "tiv_total_usd",
                    f"tiv_total_usd_flood_zone_av",
                    f"{peril}_struct_loc_deductible_layer{index}",
                    f"{peril}_regional_limit_to_use_layer{index}",
                    f"{peril}_perc_loc_deductible_layer{index}",
                    f"{peril}_min_loc_deductible_layer{index}",
                    f"{peril}_max_loc_deductible_layer{index}"
                )
                .groupby(f"{peril}_crit_cat_zone")
                .agg(
                    pl.col(f"{peril}_struct_loc_deductible_layer{index}").first(),
                    pl.col("tiv_total_usd").sum(),
                    pl.col("tiv_total_usd_flood_zone_av").sum(),
                    pl.col(f"{peril}_regional_limit_to_use_layer{index}").max(),
                    pl.col(f"{peril}_perc_loc_deductible_layer{index}").sum(),
                    pl.col(f"{peril}_min_loc_deductible_layer{index}").max(),
                    pl.col(f"{peril}_max_loc_deductible_layer{index}").max()
                )
            )

            # Assign limit as the minimum of the policy peril sublimit and limit + excess
            other_data[f"{peril}_event_level_limit_layer{index}"] = (
                (other_data[f"policy_limit_usd_layer{index}"] + other_data[f"policy_excess_usd_layer{index}"]) if other_data[f"{peril}_policy_sublimit_usd_layer{index}"] == 0 else 
                min(
                    other_data[f"policy_limit_usd_layer{index}"] + other_data[f"policy_excess_usd_layer{index}"], 
                    other_data[f"{peril}_policy_sublimit_usd_layer{index}"] 
                    )
                )
            
            # Caculate applicable location deductible
            peril_cat_zone_df = peril_cat_zone_df.with_columns(
                pl.when((pl.col(f"{peril}_max_loc_deductible_layer{index}").is_null()) | (pl.col(f"{peril}_max_loc_deductible_layer{index}") == 0))
                .then(pl.max(pl.col(f"{peril}_min_loc_deductible_layer{index}"), pl.col(f"{peril}_perc_loc_deductible_layer{index}")))
                .otherwise(pl.max(
                    pl.min(pl.col(f"{peril}_max_loc_deductible_layer{index}"), pl.col(f"{peril}_perc_loc_deductible_layer{index}")),
                    pl.col(f"{peril}_min_loc_deductible_layer{index}"))
                    )
                .alias(f"{peril}_location_deductible_layer{index}"))

            # Assign deductible as maximum of minimum per occurrence and location deductible
            peril_cat_zone_df = peril_cat_zone_df.with_columns(
                pl.when((pl.col(f"{peril}_location_deductible_layer{index}").is_null()) | (pl.col(f"{peril}_location_deductible_layer{index}") == 0))
                .then(pl.lit(per_occurrence_ded_usd))
                .otherwise(pl.col(f"{peril}_location_deductible_layer{index}")) 
                .alias(f"{peril}_deductible_layer{index}")
            )
            
            # Calculate exposed tiv within cat zones as mininimum of limit and TIV exc location deductibles - excess - occurence deductibles
            peril_cat_zone_df = peril_cat_zone_df.with_columns([
                (
                    pl.max(
                        pl.min(
                            pl.col(f"tiv_total_usd") - pl.lit(other_data[f"policy_excess_usd_layer{index}"]) - pl.col(f"{peril}_deductible_layer{index}"),    
                            pl.min(other_data[f"{peril}_event_level_limit_layer{index}"], pl.col(f"{peril}_regional_limit_to_use_layer{index}")) - pl.lit(other_data[f"policy_excess_usd_layer{index}"])), 
                        pl.lit(0)
                    ) * line * included
                ).alias(f"{peril}_event_level_exposed_tiv_layer{index}"),
                (
                    pl.max(
                        pl.min(
                            pl.col(f"tiv_total_usd_flood_zone_av") - pl.lit(other_data[f"policy_excess_usd_layer{index}"]) - pl.col(f"{peril}_deductible_layer{index}"),    
                            pl.min(other_data[f"{peril}_event_level_limit_layer{index}"], pl.col(f"{peril}_regional_limit_to_use_layer{index}")) - pl.lit(other_data[f"policy_excess_usd_layer{index}"])), 
                        pl.lit(0)
                    ) * line * included
                ).alias(f"{peril}_event_level_exposed_tiv_layer{index}_flood_zone_av"),
                pl.lit(peril).alias("peril")
            ])
            
            peril_cat_zone_df = peril_cat_zone_df.with_columns(
                pl.col(f"{peril}_crit_cat_zone")
                .str.extract(r'(\d)$')
                .str.slice(-1)  
                .cast(pl.Int64)     
                .alias(f"{peril}_crit_cat_zone_num"))

            peril_label = 'Quake Zone ' if peril == "eq" else "WS Zone "
            peril_cat_zone_df = peril_cat_zone_df.with_columns(
                (
                    pl.lit(peril_label) + pl.col(f"{peril}_crit_cat_zone_num").cast(str)
                ).alias(f"{peril}_crit_cat_zone_summary"))


            cat_zone_dict[f"{peril}_layer{index}"] = peril_cat_zone_df

            ### 20/07/2026 GATEs Summary
            # Aggregate location level exposed by tiv into respective gates
            peril_gate_df = (
                df.select(
                    f"{peril}_gate",
                    "tiv_total_usd",
                    f"tiv_total_usd_flood_zone_av",
                    f"{peril}_struct_loc_deductible_layer{index}",
                    f"{peril}_regional_limit_to_use_layer{index}",
                    f"{peril}_perc_loc_deductible_layer{index}",
                    f"{peril}_min_loc_deductible_layer{index}",
                    f"{peril}_max_loc_deductible_layer{index}"
                )
                .groupby(f"{peril}_gate")
                .agg(
                    pl.col(f"{peril}_struct_loc_deductible_layer{index}").first(),
                    pl.col("tiv_total_usd").sum(),
                    pl.col("tiv_total_usd_flood_zone_av").sum(),
                    pl.col(f"{peril}_regional_limit_to_use_layer{index}").max(),
                    pl.col(f"{peril}_perc_loc_deductible_layer{index}").sum(),
                    pl.col(f"{peril}_min_loc_deductible_layer{index}").max(),
                    pl.col(f"{peril}_max_loc_deductible_layer{index}").max()
                )
            )

            # Caculate applicable location deductible
            peril_gate_df = peril_gate_df.with_columns(
                pl.when((pl.col(f"{peril}_max_loc_deductible_layer{index}").is_null()) | (pl.col(f"{peril}_max_loc_deductible_layer{index}") == 0))
                .then(pl.max(pl.col(f"{peril}_min_loc_deductible_layer{index}"), pl.col(f"{peril}_perc_loc_deductible_layer{index}")))
                .otherwise(pl.max(
                    pl.min(pl.col(f"{peril}_max_loc_deductible_layer{index}"), pl.col(f"{peril}_perc_loc_deductible_layer{index}")),
                    pl.col(f"{peril}_min_loc_deductible_layer{index}"))
                    )
                .alias(f"{peril}_location_deductible_layer{index}"))

            # Assign deductible as maximum of minimum per occurrence and location deductible
            peril_gate_df = peril_gate_df.with_columns(
                pl.when((pl.col(f"{peril}_location_deductible_layer{index}").is_null()) | (pl.col(f"{peril}_location_deductible_layer{index}") == 0))
                .then(pl.lit(per_occurrence_ded_usd))
                .otherwise(pl.col(f"{peril}_location_deductible_layer{index}")) 
                .alias(f"{peril}_deductible_layer{index}")
            )
            
            # Calculate exposed tiv within gates as mininimum of limit and TIV exc location deductibles - excess - occurence deductibles
            peril_gate_df = peril_gate_df.with_columns([
                (
                    pl.max(
                        pl.min(
                            pl.col(f"tiv_total_usd") - pl.lit(other_data[f"policy_excess_usd_layer{index}"]) - pl.col(f"{peril}_deductible_layer{index}"),    
                            pl.min(other_data[f"{peril}_event_level_limit_layer{index}"], pl.col(f"{peril}_regional_limit_to_use_layer{index}")) - pl.lit(other_data[f"policy_excess_usd_layer{index}"])), 
                        pl.lit(0)
                    ) * line * included
                ).alias(f"{peril}_event_level_exposed_tiv_layer{index}"),
                (
                    pl.max(
                        pl.min(
                            pl.col(f"tiv_total_usd_flood_zone_av") - pl.lit(other_data[f"policy_excess_usd_layer{index}"]) - pl.col(f"{peril}_deductible_layer{index}"),    
                            pl.min(other_data[f"{peril}_event_level_limit_layer{index}"], pl.col(f"{peril}_regional_limit_to_use_layer{index}")) - pl.lit(other_data[f"policy_excess_usd_layer{index}"])), 
                        pl.lit(0)
                    ) * line * included
                ).alias(f"{peril}_event_level_exposed_tiv_layer{index}_flood_zone_av"),
                pl.lit(peril).alias("peril")
            ])
            

            gate_dict[f"{peril}_layer{index}"] = peril_gate_df

    return cat_zone_dict, gate_dict



def calc_location_deductible(hxd, df):
    exchange_rate = hxd.policy_information.exchange_rate

    for peril in ["eq", "ws"]:

        # Assign peril structure name in order to retrieve location deductibles
        peril_struct_name = "quake" if peril == "eq" else "named_windstorm"

        for index, layer in enumerate(hxd.layers, start=1):

            # Find number of options to consider for peril and layer
            num_options = df.select(pl.col(f"{peril}_deductible_option_assigned_layer{index}").max()).item()

            us_location_min_deductible = pl.lit(0).alias(f"{peril}_us_min_loc_deductible_layer{index}")
            us_location_max_deductible = pl.lit(0).alias(f"{peril}_us_max_loc_deductible_layer{index}")
            us_perc_deductible = pl.lit(0).alias(f"{peril}_us_perc_loc_deductible_layer{index}")
            us_deductible_structure = pl.lit("No US Location Deductible").alias(f"{peril}_us_struct_loc_deductible_layer{index}")

            for option_num in range(1, num_options + 1):

                # Retrieve option structure
                option_structure = getattr(getattr(layer.perils, peril_struct_name).location_ded, f"option_{option_num}")

                us_deductible_structure = (
                    pl.when((pl.col(f"{peril}_deductible_option_assigned_layer{index}") == option_num) & (pl.col("country") == "United States"))
                    .then(pl.lit(option_structure.type))
                    .otherwise(us_deductible_structure)
                    .alias(f"{peril}_us_struct_loc_deductible_layer{index}")
                )

                # Calculate percentage and fixed components of deductible expression
                us_perc_deductible = (
                    pl.when((pl.col(f"{peril}_deductible_option_assigned_layer{index}") == option_num) & (pl.col("country") == "United States"))
                    .then(pl.col("tiv_total_usd") * pl.lit((option_structure.percent or 0)))
                    .otherwise(us_perc_deductible)
                    .alias(f"{peril}_us_perc_loc_deductible_layer{index}"))

                option_deductible_amount = (option_structure.location_min_max or 0) / exchange_rate if exchange_rate else (option_structure.location_min_max or 0)

                us_location_min_deductible = (
                    pl.when((pl.col(f"{peril}_deductible_option_assigned_layer{index}") == option_num) & (pl.col("country") == "United States") & (option_structure.type in ["Percentage with a $ minimum", "Fixed $ amount"]))
                    .then(pl.lit(option_deductible_amount))
                    .otherwise(us_location_min_deductible)
                    .alias(f"{peril}_us_min_loc_deductible_layer{index}"))

                us_location_max_deductible = (
                    pl.when((pl.col(f"{peril}_deductible_option_assigned_layer{index}") == option_num) & (pl.col("country") == "United States") & (option_structure.type == "Percentage capped by $ amount"))
                    .then(pl.lit(option_deductible_amount))
                    .otherwise(us_location_max_deductible)
                    .alias(f"{peril}_us_max_loc_deductible_layer{index}"))
                
            df = df.with_columns(us_deductible_structure, us_perc_deductible, us_location_min_deductible, us_location_max_deductible)
                
            # Attach appropriate deductible option
            df = df.with_columns(
                pl.when(pl.col("country") == "United States")
                .then(pl.col(f"{peril}_us_struct_loc_deductible_layer{index}"))
                .otherwise(pl.lit("intl_deductible_structure"))
                .alias(f"{peril}_struct_loc_deductible_layer{index}"),
                pl.when(pl.col("country") == "United States")
                .then(pl.col(f"{peril}_us_perc_loc_deductible_layer{index}"))
                .otherwise(pl.col(f"{peril}_intl_perc_loc_deductible"))
                .alias(f"{peril}_perc_loc_deductible_layer{index}"),
                pl.when(pl.col("country") == "United States")
                .then(pl.col(f"{peril}_us_min_loc_deductible_layer{index}"))
                .otherwise(pl.col(f"{peril}_intl_min_loc_deductible"))
                .alias(f"{peril}_min_loc_deductible_layer{index}"),
                pl.when(pl.col("country") == "United States")
                .then(pl.col(f"{peril}_us_max_loc_deductible_layer{index}"))
                .otherwise(pl.col(f"{peril}_intl_max_loc_deductible"))
                .alias(f"{peril}_max_loc_deductible_layer{index}")
            ) 

    return df



def cat_zone_hxd_assignment(hxd, df, cat_zone_dict):

    # Load parameter tables
    cat_zone_threshold = pl.from_pandas(hx.params.cat_limit_thresholds)
    team = hxd.policy_information.team

    max_version = cat_zone_threshold.select(pl.col("version").max()).item()
    cat_zone_threshold = cat_zone_threshold.filter((pl.col('class_of_business') == team) & (pl.col('version') == max_version))

    # Extract thresholds for crit and elevated
    critical_cat_threshold = cat_zone_threshold.select(pl.col('critical')).item() 
    elevated_cat_threshold = cat_zone_threshold.select(pl.col('elevated')).item() 

    # Intiate Warning Variables
    warning = False
    layers_with_breach = ""
    layers_with_breach_indexes = []

    # Calculate number of locations unassigned
    warning_unassigned =False

    eq_num_unassigned = df.filter((pl.col(f"eq_crit_cat_zone").str.slice(-1).str.extract(r'(\d)$').cast(pl.Int64) == 0) | (pl.col(f"eq_crit_cat_zone") == None)).height
    ws_num_unassigned = df.filter((pl.col(f"ws_crit_cat_zone").str.slice(-1).str.extract(r'(\d)$').cast(pl.Int64) == 0) | (pl.col(f"ws_crit_cat_zone") == None)).height

    if eq_num_unassigned + ws_num_unassigned > 0:
        assigning_cat_zone_warning = f"{eq_num_unassigned} locations have not been assigned a earthquake cat zones and {ws_num_unassigned} locations have not been assigned a windstorm cat zones. Please review the schedule to ensure all locations have been assigned a cat zone."
        warning_unassigned = True
    else:
        assigning_cat_zone_warning = ""

    for peril in ['eq', 'ws']:
        for index, layer in enumerate(hxd.layers, start=1):
            peril_struct_name = "quake" if peril == "eq" else "named_windstorm"

            # Retrieve CAT Zone table for current peril and layer
            peril_cat_zone_df = cat_zone_dict[f"{peril}_layer{index}"]

            # Remove zone 3's as no limit there
            peril_cat_zone_df = peril_cat_zone_df.filter((pl.col(f"{peril}_crit_cat_zone_num")<3) & (pl.col(f"{peril}_crit_cat_zone_num")>0))

            # Attach exposed limit thresholds to each table
            peril_cat_zone_df = peril_cat_zone_df.with_columns(
                pl.when(pl.col(f"{peril}_crit_cat_zone_num") == 2)
                .then(pl.lit(elevated_cat_threshold))
                .otherwise(pl.lit(critical_cat_threshold))
                .alias("exposed_limit_threshold")
            ) 

            # Adjust WS CAT Zones according to A & V FEMA Zone Exposure
            if peril == "ws":
                peril_cat_zone_df = peril_cat_zone_df.with_columns(
                    pl.when(pl.col(f"{peril}_crit_cat_zone").str.slice(0, 2).is_in(['CT', 'DE', 'MD', 'MA', 'NH', 'NJ', 'NY', 'RI']) & (pl.col(f"{peril}_event_level_exposed_tiv_layer{index}_flood_zone_av") == 0))
                    .then(pl.lit(elevated_cat_threshold))
                    .otherwise(pl.col("exposed_limit_threshold"))
                    .alias("exposed_limit_threshold")
                )

            # Check if exposed limit breaches the exposed limit threshold
            peril_cat_zone_df = peril_cat_zone_df.with_columns([
                pl.when(pl.col(f"{peril}_event_level_exposed_tiv_layer{index}") > pl.col("exposed_limit_threshold"))
                .then(pl.lit("❌"))
                .otherwise(pl.lit("✅"))
                .alias("within_threshold"),
                pl.when(pl.col(f"{peril}_event_level_exposed_tiv_layer{index}") > pl.col("exposed_limit_threshold"))
                .then(pl.lit(True))
                .otherwise(pl.lit(False))
                .alias("breach")
                ])

            # Sort the table by whether there is a breach, the exposed limit and then the ground up tiv
            peril_cat_zone_df = peril_cat_zone_df.sort(
                by=["breach", f"{peril}_event_level_exposed_tiv_layer{index}", "tiv_total_usd"],
                descending=[True, True, True]
            )

            # Warning message to be outputted to rating summary?
            if peril_cat_zone_df["breach"].any():
                warning = True
                if index not in layers_with_breach_indexes:
                    if layers_with_breach == "":
                        layers_with_breach = layers_with_breach + " " + str(index)
                    else:
                        layers_with_breach = layers_with_breach + ", " + str(index)
                
                layers_with_breach_indexes.append(index)


            # Output detailed CAT Zone table to the Underwriting Appetite page 
            struct = getattr(layer.perils, peril_struct_name)
            struct.crit_cat_zone_summary = peril_cat_zone_df.select([
                f"{peril}_crit_cat_zone",
                "tiv_total_usd",
                f"{peril}_event_level_exposed_tiv_layer{index}",
                "exposed_limit_threshold",
                "within_threshold",
                f"{peril}_event_level_exposed_tiv_layer{index}_flood_zone_av"
            ]).rename({
                f"{peril}_crit_cat_zone": "cat_zone",
                "tiv_total_usd": "tiv",
                f"{peril}_event_level_exposed_tiv_layer{index}": "exposed_limit",
                f"{peril}_event_level_exposed_tiv_layer{index}_flood_zone_av": "flood_zone_av_exposed_limit"
            }).to_dicts()

            # Create Summary Tables - Based on max WS and EQ exposures in each Zone 1 and 2
            crit_cat_summary_table = (peril_cat_zone_df
                .groupby(pl.col(f"{peril}_crit_cat_zone_summary"))
                .agg([
                    pl.col("breach").sum(),
                ])
            )                

            # Apply breach logic 
            crit_cat_summary_table = crit_cat_summary_table.with_columns([
                pl.when(pl.col('breach') > 0)
                .then(pl.lit("❌"))
                .otherwise(pl.lit("✅"))
                .alias("within_threshold"),
                pl.when(pl.col(f"{peril}_crit_cat_zone_summary") == ('Quake Zone 1' if peril == "eq" else "WS Zone 1"))
                .then(critical_cat_threshold)
                .otherwise(elevated_cat_threshold)
                .alias("exposed_limit_threshold")
                ])

            # Sort by Zones 1 to 2 
            crit_cat_summary_table = (
                crit_cat_summary_table
                .with_columns(
                    pl.col(f"{peril}_crit_cat_zone_summary")
                    .str.extract(r'(\d)$')
                    .str.slice(-1)
                    .cast(pl.Int64)
                    .alias(f"{peril}_crit_cat_zone_num")
                )
                .sort(f"{peril}_crit_cat_zone_num", descending=False)
            )

            # Write Summary Tables to HXD
            summary_struct = getattr(layer.perils, peril_struct_name)
            summary_struct.crit_cat_zone_total_summary = crit_cat_summary_table.select([
                f"{peril}_crit_cat_zone_summary",
                "exposed_limit_threshold",
                "within_threshold"
            ]).rename({
                f"{peril}_crit_cat_zone_summary": "cat_zone"
            }).to_dicts()
    
    # Output warnings
    if warning:
        hxd.control.show_run_rater_warning = warning
        hxd.info.run_rater_warning = f"**Catastrophe Limit Framework v{max_version} - CAT Zone Warnings**\nThe exposed TIV exceeds the permitted threshold in one or more CAT zones in layers{layers_with_breach}. **These layers may require referral before binding.**\nPlease review the Underwriter Appetite tab for details. \n\n{assigning_cat_zone_warning}"
    elif warning_unassigned:
        hxd.control.show_run_rater_warning = warning_unassigned
        hxd.info.run_rater_warning = f"**Catastrophe Limit Framework v{max_version} - CAT Zone Warnings**\n{assigning_cat_zone_warning}"

    # CAT Limit Information Output
    info_message = """Please note that the maximum net limit deployable is the lower of;
    1. the Exposure Limit Threshold set out below, and 
    2. the maximum net line per risk specified in the underwriter's Letter of Authority.

    Additionally, the exposures set out below are assessed on a gross-of basis and do not assume the use of facultative reinsurance, consortia, or catastrophe schemes to reduce the overall net line.

    Where underwriters can evidence that such arrangements reduce the net line to below the Exposure Limit Threshold, no referral is required.
    """

    if warning_unassigned:
        info_message = f"{info_message}\n**‼️{assigning_cat_zone_warning}‼️**"
        hxd.info.cat_limit_framwork_msg = info_message
    else:
        hxd.info.cat_limit_framwork_msg = info_message


    pass

def gate_hxd_assignment(hxd, df, gate_dict):

    for peril in ['eq', 'ws']:
        for index, layer in enumerate(hxd.layers, start=1):
            peril_struct_name = "quake" if peril == "eq" else "named_windstorm"

            # Retrieve gate table for current peril and layer
            peril_gate_df = gate_dict[f"{peril}_layer{index}"]

            # Sort the table by the exposed limit and then the ground up tiv
            peril_gate_df = peril_gate_df.sort(
                by=[f"{peril}_event_level_exposed_tiv_layer{index}", "tiv_total_usd"],
                descending=[True, True]
            )

            # Output detailed gate table to the Underwriting Appetite page 
            struct = getattr(layer.perils, peril_struct_name)
            struct.gate_appetite_summary = peril_gate_df.select([
                f"{peril}_gate",
                "tiv_total_usd",
                f"{peril}_event_level_exposed_tiv_layer{index}",
                f"{peril}_event_level_exposed_tiv_layer{index}_flood_zone_av"
            ]).rename({
                f"{peril}_gate": "gate",
                "tiv_total_usd": "tiv",
                f"{peril}_event_level_exposed_tiv_layer{index}": "exposed_limit",
                f"{peril}_event_level_exposed_tiv_layer{index}_flood_zone_av": "flood_zone_av_exposed_limit"
            }).to_dicts()
    pass
         



        

