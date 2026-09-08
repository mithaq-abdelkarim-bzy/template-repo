import hx
import polars as pl
import numpy as np

def join_param_table(df, lookup_df, desired_column, desired_column_name, parameter_table_join_column, df_join_column, filter_col=None, filter_val=None, int_col=False, force_int_df=False, drop=True, upper=False):
    lookup_pl = pl.from_pandas(lookup_df)

    if filter_col and filter_val:
        # SA: might want to raise an error if only one of these is set
        lookup_pl = lookup_pl.filter(pl.col(filter_col) == filter_val)

    if int_col:
        lookup_pl = lookup_pl.with_columns(pl.col(parameter_table_join_column).cast(pl.Int64).alias(parameter_table_join_column))

    if desired_column_name == df_join_column:
        df = df.rename({df_join_column: "temp_join_column"})
        df_join_column = "temp_join_column"

    lookup_pl = lookup_pl[[desired_column, parameter_table_join_column]].rename({desired_column: desired_column_name, parameter_table_join_column: df_join_column})
    lookup_pl = lookup_pl.unique()

    if force_int_df:
        df = df.with_columns(pl.col(df_join_column).cast(pl.Int64).alias(df_join_column))
    
    if upper:
        df = df.with_columns(pl.col(df_join_column).str.to_uppercase().alias(df_join_column))
        lookup_pl = lookup_pl.with_columns(pl.col(df_join_column).str.to_uppercase().alias(df_join_column))

    df = df.join(lookup_pl, on=df_join_column, how="left")
    if drop:
        df = df.drop(df_join_column)
    return df


def worth_lookup(hxd, df, peril):
    
    # get lookup column from the worth table. This will tell us which enrty and exit pattern to use. 
    worth_table = pl.from_pandas(hx.params.table_worth).sort("TIV_Band")
    worth_table = worth_table.select("TIV_Band", "Construction_Code", f"{peril}")

    df = (
        df.sort("loc_tiv_total")
        .join_asof(worth_table.select("TIV_Band").unique(), left_on="loc_tiv_total", right_on="TIV_Band", strategy="backward")
        .join(worth_table, left_on=["iso_constr", "TIV_Band"], right_on=["Construction_Code", "TIV_Band"], how="left")
        .drop("TIV_Band")
    )

    #create columns to find worth exit and entry lookup based on tiv
    worth_entry_exit_table = pl.from_pandas(hx.params.table_worth_entry_exit).sort("tiv_perc")
    worth_bands =  worth_entry_exit_table.select("tiv_perc").unique()


    df = df.with_columns(      
        pl.when((pl.col("loc_aop_ded") / pl.col("loc_tiv_total")) < 1)
            .then((pl.col("loc_aop_ded") / pl.col("loc_tiv_total")))
            .otherwise(1)
            .fill_null(0)
            .fill_nan(0)
            .alias("worth_entry_lookup"),

        pl.when(pl.col("loc_aop_limit").is_null())
            .then(1)
            .when(pl.col("loc_aop_limit").is_in([None, np.nan, 0]))
            .then(1)
            .when((pl.col("loc_aop_limit") / pl.col("loc_tiv_total")) < 1)
            .then((pl.col("loc_aop_limit") / pl.col("loc_tiv_total")))
            .otherwise(1)
            .fill_null(0)
            .fill_nan(0)
            .alias("worth_exit_lookup")
    )
    
    worth_entry_exit_melted = worth_entry_exit_table.melt(id_vars="tiv_perc", variable_name="curve", value_name="worth")

    df = (
        df.sort("worth_entry_lookup")
        .join_asof(worth_bands, left_on="worth_entry_lookup", right_on="tiv_perc", strategy="backward")
        .join(worth_entry_exit_melted, left_on=["tiv_perc", f"{peril}"], right_on=["tiv_perc", "curve"], how="left")
        .rename({"worth": "worth_entry"})
        .drop("worth_entry_lookup", "tiv_perc")
    )

    df = (
        df.sort("worth_exit_lookup")
        .join_asof(worth_bands, left_on="worth_exit_lookup", right_on="tiv_perc", strategy="backward")
        .join(worth_entry_exit_melted, left_on=["tiv_perc", f"{peril}"], right_on=["tiv_perc", "curve"], how="left")
        .rename({"worth": "worth_exit"})
    )

    df = df.with_columns(
        (pl.col("worth_exit") - pl.col("worth_entry")).alias(f"{peril.lower()}_worth")
    )

    df = df.drop(["tiv_perc", "worth_entry", "worth_exit", "worth_exit_lookup", f"{peril}"])

    return df


def spatial_key_modifier (hxd, df, peril):
    # This may need to change in future to allow for bdx with both US & Intl locations to work by location
    if hxd.cds.layers[0].country == "US":
        df = join_param_table(df, hx.params.table_us_spatial_key, f"{peril}", f"{peril.lower()}_spatial_key_modifier", "StateCounty", "state_county", drop=False)
    else:
        df = join_param_table(df, hx.params.table_intl_spatial_key, f"{peril}", f"{peril.lower()}_spatial_key_modifier", "State", "state", drop=False)


    

    return df

def iso_construction_modifier (hxd, df, peril):

    if peril == "TN":
        tn_construction_load_melted = pl.from_pandas(hx.params.table_tn_construction_load).melt(id_vars="StateCounty", variable_name="iso_constr", value_name=f"{peril.lower()}_construction_load")

        df = df.join(tn_construction_load_melted, left_on=(pl.col("state_county"),  pl.col("iso_constr")), right_on=(pl.col("StateCounty"), pl.col("iso_constr")), how="left")
        df = df.with_columns((pl.col(f"{peril.lower()}_construction_load") + 1).alias(f"{peril.lower()}_construction_modifier"))
        df = df.drop(f"{peril.lower()}_construction_load")

    else:
        df = join_param_table(df, hx.params.table_iso_construction_modifier, f"{peril}", f"{peril.lower()}_construction_modifier", "ISO", "iso_constr", drop=False)

        df = df.with_columns(
            (pl.col(f"{peril.lower()}_construction_modifier") + 1).alias(f"{peril.lower()}_construction_modifier")
        )

   

    return df


def num_floors_modifier (hxd, df, peril):

    # Load parameter table
    floors_df = hx.params.table_floors

    floors_pl = pl.from_pandas(floors_df).rename({"No. Floors": "num_floors", "Weight": f"{peril.lower()}_num_floors_modifier"}).sort("num_floors")
    
    df = df.with_columns(
        pl.when(pl.col("num_stories") < 1)
            .then(1)
            .when(pl.col("num_stories") > 10)
            .then(10)
            .otherwise("num_stories")
            .fill_null(1)
            .fill_nan(1)
            .alias("num_floors")
    )
    # join_asof matches on nearest key, not exact key
    
    df = df.sort("num_floors")
    df = df.join_asof(floors_pl, on="num_floors")


    df = df.with_columns(
        (pl.col(f"{peril.lower()}_num_floors_modifier").fill_null(1))
    )

    df.drop(["num_floors"])

    return df

def occupancy_modifier(hxd, df, peril):

    if peril == "WF":
        df = join_param_table(df, hx.params.table_atc_occupancy_modifier, "Mode", f"{peril.lower()}_occupancy_modifier", "Row Labels", "occupancy", drop=False)

        df = df.with_columns((pl.col(f"{peril.lower()}_occupancy_modifier") + 1).alias(f"{peril.lower()}_occupancy_modifier"))

    elif peril == "TN":
        tn_occupancy_modifier_melted = pl.from_pandas(hx.params.table_tn_occupancy_modifier).melt(id_vars="StateCounty", variable_name="occupancy", value_name=f"{peril.lower()}_occupancy_modifier")

        df = df.with_columns(pl.concat_str(pl.lit("Occ."), pl.col("atc_occupancy_code")).alias("temp_join_column"))
        df = df.join(tn_occupancy_modifier_melted, left_on=(pl.col("state_county"),  pl.col("temp_join_column")), right_on=(pl.col("StateCounty"), pl.col("occupancy")), how="left")
        df = df.with_columns((pl.col(f"{peril.lower()}_occupancy_modifier") + 1).alias(f"{peril.lower()}_occupancy_modifier"))
        df = df.drop("temp_join_column")

    elif peril == "HA":
        ha_occupancy_modifier_melted = pl.from_pandas(hx.params.table_ha_occupancy_modifier).melt(id_vars="State Code", variable_name="occupancy", value_name=f"{peril.lower()}_occupancy_modifier")
        df = df.with_columns(pl.concat_str(pl.lit("Occ."), pl.col("atc_occupancy_code")).alias("temp_join_column"))
        df = df.join(ha_occupancy_modifier_melted, left_on=(pl.col("state"),  pl.col("temp_join_column")), right_on=(pl.col("State Code"), pl.col("occupancy")), how="left")
        df = df.with_columns((pl.col(f"{peril.lower()}_occupancy_modifier") + 1).alias(f"{peril.lower()}_occupancy_modifier"))
        df = df.drop("temp_join_column")    

    return df

def ppc_modifer(hxd, df, peril):
    if peril in ("WF", "FL"):
        df = join_param_table(df, hx.params.table_ppc_modifier, f"{peril}", f"{peril.lower()}_ppc_modifier", "PPC", "ppc_code", drop=False)

        df = df.with_columns(
            (pl.col(f"{peril.lower()}_ppc_modifier") + 1).alias(f"{peril.lower()}_ppc_modifier")
        )

    if peril in ("BG1"):
        fire_ppc_table = pl.from_pandas(hx.params.table_fire_ppc)
        fire_ppc_metled = fire_ppc_table.melt(id_vars="Protection Class", variable_name="iso_class", value_name="bg1_ppc_modifier")
        df = df.join(fire_ppc_metled, left_on=["ppc_code", "iso_constr"], right_on=["Protection Class", "iso_class"], how="left")

    return df

def size_discount_modifier(hxd, df, peril):
    # I think we may be able to remove this if statment
    if peril in ("WF", "FL", "BG1", "BG2", "TN", "HA", "WTS", "SCL"):


        #this loop pulls the Size Discount modifier for both buildings and contents
        for modifier in ("buildings", "contents"):

            if peril in ("WF", "FL"):
                table_name = f"table_size_discount_wf_fl_{modifier}_rescale_bg1"
            elif peril in ("TN", "HA", "WTS"):
                table_name = f"table_size_discount_tn_ha_wts_{modifier}_rescale_bg2"
            elif peril in ("BG1", "BG2", "SCL"):
                table_name = f"table_size_discount_{peril.lower()}_{modifier}"

            df = df.sort(f"loc_tiv_{modifier}")

            param_table = pl.from_pandas(getattr(hx.params, table_name))
            tiv_bands =  param_table.select("TIV").unique().sort("TIV")

            df = df.join_asof(tiv_bands, left_on=f"loc_tiv_{modifier}", right_on="TIV", strategy="backward")

            if peril in ["WF", "FL"]:
                if hxd.cds.currencies.source_currency != "USD":
                    
                    df = join_param_table(df, getattr(hx.params, table_name), "ISO.1", f"{peril.lower()}_size_discount_{modifier}_modifier", "TIV", "TIV", drop=False)
                else:
                    param_table_melted = param_table.melt(id_vars="TIV", variable_name="iso_class", value_name=f"{peril.lower()}_size_discount_{modifier}_modifier")
                    df = df.join(param_table_melted, left_on=("TIV", "iso_constr"), right_on=("TIV", "iso_class"), how="left")

                # If this is the size discount curve why are we setting the min value to 1?
                df = df.with_columns(
                    pl.when(pl.col(f"{peril.lower()}_size_discount_{modifier}_modifier") < 1 ).then(1)
                    .otherwise(pl.col(f"{peril.lower()}_size_discount_{modifier}_modifier")).alias(f"{peril.lower()}_size_discount_{modifier}_modifier")
                )
            elif peril in ["BG2", "TN", "HA", "WTS"]:
                param_table_melted = param_table.melt(id_vars="TIV", variable_name="region", value_name=f"{peril.lower()}_size_discount_{modifier}_modifier")

                if hxd.cds.currencies.source_currency == "USD":
                    df = df.with_columns(
                        pl.when(pl.col("bg1_state").str.to_titlecase() == "Florida")
                        .then(pl.col("bg1_state").str.to_titlecase())
                        .otherwise(pl.col("bg2_region"))
                        .alias("temp_lookup_column")
                    )

                    df = df.join(param_table_melted, left_on=("TIV", "temp_lookup_column"), right_on=("TIV", "region"), how="left")
                    df = df.drop("temp_lookup_column")

                else:
                    param_table_melted = param_table_melted.filter(pl.col("region")=="Non-Southeast").drop("region")
                    df = df.join(param_table_melted, left_on=("TIV"), right_on=("TIV"), how="left")

                if peril in ["TN", "HA", "WTS"]:
                    # If this is the size discount curve why are we setting the min value to 1?
                    df = df.with_columns(
                        pl.when(pl.col(f"{peril.lower()}_size_discount_{modifier}_modifier") < 1 )
                        .then(1)
                        .otherwise(pl.col(f"{peril.lower()}_size_discount_{modifier}_modifier"))
                        .alias(f"{peril.lower()}_size_discount_{modifier}_modifier")
                    )


            elif peril == "BG1":
                param_table_melted = param_table.melt(id_vars="TIV", variable_name="iso_class", value_name=f"{peril.lower()}_size_discount_{modifier}_modifier")
                df = df.join(param_table_melted, left_on=("TIV", "iso_constr"), right_on=("TIV", "iso_class"), how="left")

            elif peril == "SCL":
                df = join_param_table(df, getattr(hx.params, table_name), "Factors", f"{peril.lower()}_size_discount_{modifier}_modifier", "TIV", "TIV", drop=False)


            df = df.drop("TIV")

    return df

def base_rates(hxd, df, peril):


    if peril not in ["BG1", "BG2", "SCL"]:
        
        if getattr(hxd.cds.risk_info, f"{peril.lower()}").selected == True:
            # This may need to change in future to allow for bdx with both US & Intl locations to work by location
            if hxd.cds.layers[0].country == "US":
                df = join_param_table(df, hx.params.table_us_base_rates, f"{peril} Buildings", f"{peril.lower()}_us_base_rate_buildings", "StateCounty", "state_county", drop=False)
                df = join_param_table(df, hx.params.table_us_base_rates, f"{peril} Contents", f"{peril.lower()}_us_base_rate_contents", "StateCounty", "state_county", drop=False)
                df = join_param_table(df, hx.params.table_us_base_rates, f"{peril} BI", f"{peril.lower()}_us_base_rate_bi", "StateCounty", "state_county", drop=False)
                
            else:
                df = join_param_table(df, hx.params.table_intl_base_rates, f"{peril} Buildings", f"{peril.lower()}_intl_base_rate_buildings", "State", "state", drop=False)
                df = join_param_table(df, hx.params.table_intl_base_rates, f"{peril} Contents", f"{peril.lower()}_intl_base_rate_contents", "State", "state", drop=False)
                df = join_param_table(df, hx.params.table_intl_base_rates, f"{peril} BI", f"{peril.lower()}_intl_base_rate_bi", "State", "state", drop=False)

            # if we change to use by location country flag then will need this separate section
            if hxd.cds.layers[0].country == "US":
                df = df.with_columns(
                    (pl.col(f"{peril.lower()}_us_base_rate_buildings")).alias(f"{peril.lower()}_base_rate_buildings"),
                    (pl.col(f"{peril.lower()}_us_base_rate_contents")).alias(f"{peril.lower()}_base_rate_contents"),
                    (pl.col(f"{peril.lower()}_us_base_rate_bi")).alias(f"{peril.lower()}_base_rate_bi")
                )
            else:
                df = df.with_columns(
                    (pl.col(f"{peril.lower()}_intl_base_rate_buildings")).alias(f"{peril.lower()}_base_rate_buildings"),
                    (pl.col(f"{peril.lower()}_intl_base_rate_contents")).alias(f"{peril.lower()}_base_rate_contents"),
                    (pl.col(f"{peril.lower()}_intl_base_rate_bi")).alias(f"{peril.lower()}_base_rate_bi")
                )

        # ERROR_FLAG: potential code error in original CMT, left commented for reconciliation
        # if peril != "WF": 
        #     df = df.with_columns(
        #         (pl.col(f"{peril.lower()}_base_rate_buildings") * pl.lit(100)).alias(f"{peril.lower()}_base_rate_buildings"),
        #         (pl.col(f"{peril.lower()}_base_rate_contents") * pl.lit(100)).alias(f"{peril.lower()}_base_rate_contents"),
        #         (pl.col(f"{peril.lower()}_base_rate_bi") * pl.lit(100)).alias(f"{peril.lower()}_base_rate_bi")
        #     )

        # ERROR_FIX: fixed version of code error in original CMT, can comment out for reconciliation

        else:
        
            df = df.with_columns([pl.lit(0).alias(f"{peril.lower()}_base_rate_buildings"),pl.lit(0).alias(f"{peril.lower()}_base_rate_contents"),pl.lit(0).alias(f"{peril.lower()}_base_rate_bi")])

        
        #############################################################################################

        df = df.with_columns(
                    pl.when(pl.col(f"{peril.lower()}_base_rate_buildings").is_null())
                    .then(0)
                    .otherwise(pl.col(f"{peril.lower()}_base_rate_buildings"))
                    .alias(f"{peril.lower()}_base_rate_buildings"),
                    pl.when(pl.col(f"{peril.lower()}_base_rate_contents").is_null())
                    .then(0)
                    .otherwise(pl.col(f"{peril.lower()}_base_rate_contents"))
                    .alias(f"{peril.lower()}_base_rate_contents"),
                    pl.when(pl.col(f"{peril.lower()}_base_rate_bi").is_null())
                    .then(0)
                    .otherwise(pl.col(f"{peril.lower()}_base_rate_bi"))
                    .alias(f"{peril.lower()}_base_rate_bi")
                )

        df = df.with_columns(
            pl.col([f"{peril.lower()}_base_rate_buildings", f"{peril.lower()}_base_rate_contents", f"{peril.lower()}_base_rate_bi"]).fill_null(0)
        )

    if peril == "BG1":
        df = df.with_columns(
            (pl.concat_str(pl.col("bg1_state"), pl.col("bg1_territory"), pl.col("occupancy")).str.to_uppercase()).alias("iso_lookup_1"),
            (pl.concat_str(pl.col("bg1_state"), pl.col("occupancy"), pl.lit("UNKNOWN")).str.to_uppercase()).alias("iso_lookup_2")
        )

        for item in ("buildings", "contents"):

            param_table = pl.from_pandas(getattr(hx.params, f"table_iso_bg1_{item}_base_rates")).select("Index", "ISO.1", "ISO.2", "ISO.3", "ISO.4", "ISO.5", "ISO.6")
            param_table_melted = param_table.melt(id_vars="Index", variable_name="iso_class", value_name=f"bg1_base_rate_{item}").unique()

            # In the CMT there is an if error that sets the lookup to ISO.1. I just set it to ISO.1 in the rate bordereau tab (where we do the data cleaning)
            # we techincally don't need to do the backup lookup for contents but leaving it in make the code clearer to scale to buildings and contetns (it won't impact calcs). 
            df = df.join(param_table_melted, left_on=("iso_lookup_2", "iso_constr"), right_on=("Index", "iso_class"), how="left")
            df = df.rename({f"bg1_base_rate_{item}": "lookup_2_rate"})
            df = df.join(param_table_melted, left_on=("iso_lookup_1", "iso_constr"), right_on=("Index", "iso_class"), how="left")

            df = df.with_columns(
                pl.col(f"bg1_base_rate_{item}").fill_null(pl.col("lookup_2_rate")).alias(f"bg1_base_rate_{item}")
            )
            df = df.drop("lookup_2_rate")

            df = df.with_columns(pl.col(f"bg1_base_rate_{item}").fill_null(0))

        df = df.drop("iso_lookup_1", "iso_lookup_2")

    if peril == "BG2":
        df = df.with_columns(
            pl.concat_str(pl.col("bg1_state"), pl.col("bg2_territory")).str.to_uppercase().alias("temp_base_rate_lookup")
            )

        df = join_param_table(df, hx.params.table_bg2_base_rates, "Buildings", "bg2_base_rate_buildings", "Index", "temp_base_rate_lookup", drop=False)
        df = join_param_table(df, hx.params.table_bg2_base_rates, "Contents", "bg2_base_rate_contents", "Index", "temp_base_rate_lookup", drop=False)
        df = df.drop("temp_base_rate_lookup")
        df = df.with_columns(pl.col(["bg2_base_rate_buildings", "bg2_base_rate_contents"]).fill_null(0))

    if peril == "SCL":

        df = df.with_columns(
            pl.concat_str(pl.col("bg1_state"), pl.lit("BUILDINGS")).str.to_uppercase().alias("temp_buildings_lookup"),
            pl.concat_str(pl.col("bg1_state"), pl.col("scl_occupancy")).str.to_uppercase().alias("temp_contents_lookup")
        )

        df = join_param_table(df, hx.params.table_scl_base_rates, "BUILDING", "scl_base_rate_buildings", "Index", "temp_buildings_lookup")
        df = join_param_table(df, hx.params.table_scl_base_rates, "CONTENTS", "scl_base_rate_contents", "Index", "temp_contents_lookup")
        df = df.with_columns(pl.col(["scl_base_rate_buildings", "scl_base_rate_contents"]).fill_null(0))

        df = df.drop("temp_buildings_lookup", "temp_contents_lookup")

    return df

def bg_scl_prop_covered (hxd, df, peril):

    bg_scl_prop_covered_table = pl.from_pandas(hx.params.table_bg_scl_prop_covered)
    bg_scl_coverage_selection_table = pl.from_pandas(hx.params.table_bg_scl_peril_selection)
    # bg1_prop_covered_rate_table = pl.from_pandas(hx.params.table_bg1_prop_covered_rates)

    cds = hxd.cds.risk_info
    # the order in this list matters and MUST line up with the table_bg1_peril_selection params table 
    special_list = [cds.fire.selected, cds.explosion.selected, cds.vandalism_and_malicious_mischief.selected, cds.sprinkler_leakage.selected, cds.mold_due_to_bg_1_perils.selected, cds.tn.selected,
        cds.ha.selected, cds.riot_or_civil_commotion.selected, cds.mold_due_to_bg_2_perils.selected, cds.theft.selected, cds.water_damage.selected, cds.all_other_causes.selected, cds.freezing.selected,
        cds.mold_due_to_scl_perils.selected, cds.collapse_due_to_weight_of_ice_etc.selected, cds.collapse_due_to_other_causes.selected]

    bg_scl_coverage_selection_table = bg_scl_coverage_selection_table.with_columns(
        pl.DataFrame({"Special": special_list})
    )

    # bg_scl_coverage_selection_table = bg_scl_coverage_selection_table.filter(pl.col("Peril").is_in(["Fire", "Explosion", "Vandalism & Malicious Mischief", "Sprinkler Leakage", "Mold due to BG I Perils"]))

    bg_scl_coverage_selection_melted = bg_scl_coverage_selection_table.melt(id_vars="Peril", variable_name="coverage_category", value_name="include")
    bg_scl_prop_covered_melted = bg_scl_prop_covered_table.melt(id_vars=("Peril", "Risk"), variable_name="coverage_type_location", value_name="rate")

    # bg1_prop_covered_rate_melted = bg1_prop_covered_rate_table.melt(id_vars="Peril", variable_name="coverage_type", value_name="rate")

    bg_scl_prop_covered_rate_df = bg_scl_coverage_selection_melted.join(bg_scl_prop_covered_melted, on="Peril", how="left")

    # using this to tell which perils should be included in special
    bg_scl_prop_covered_rate_df = bg_scl_prop_covered_rate_df.with_columns(
        pl.when(pl.col("include")==False)
        .then(pl.lit(0))
        .otherwise(pl.col("rate"))
        .alias("rate")
    )

    # Hail and Wind are not included in BG1 or BG2 (NOTE: Based on this I think we can remove Hail and Wind from the Special list)
    bg_scl_prop_covered_rate_df = bg_scl_prop_covered_rate_df.filter(~(pl.col("Peril").is_in(["Wind", "Hail"])))
    bg_scl_prop_covered_rate_df = bg_scl_prop_covered_rate_df.groupby("Risk", "coverage_category", "coverage_type_location").agg(pl.col("rate").sum().alias("total_rate"))
    
    # find coverage type and assign it back to df
    if cds.coverage == "": 
        lookup_coverage = "Special"
    else:
        lookup_coverage = cds.coverage

    # Filteres bg_scl_prop_covered_rate_df so that we only have the peril we are currently calculating
    bg_scl_prop_covered_rate_df = bg_scl_prop_covered_rate_df.filter(
        (pl.col("Risk") == peril) & (pl.col("coverage_category") == lookup_coverage)
    )

    bg_scl_prop_covered_rate_df = bg_scl_prop_covered_rate_df.select("coverage_type_location", "total_rate")

    if peril == "BG1":        

        df = df.with_columns(
            df.join(bg_scl_prop_covered_rate_df, left_on=pl.lit("Buildings"), right_on="coverage_type_location", how="left")["total_rate"].alias("bg1_buildings_prop_covered"),
            df.join(bg_scl_prop_covered_rate_df, left_on=pl.lit("Contents"), right_on="coverage_type_location", how="left")["total_rate"].alias("bg1_contents_prop_covered")
        )

    elif peril == "BG2":
        if hxd.cds.layers[0].country == "US":
            
            df = df.with_columns(
                df.join(bg_scl_prop_covered_rate_df, left_on=pl.concat_str(pl.lit("Buildings"), pl.col("bg2_region")), right_on="coverage_type_location", how="left")["total_rate"].alias("bg2_buildings_prop_covered"),
                df.join(bg_scl_prop_covered_rate_df, left_on=pl.concat_str(pl.lit("Contents"), pl.col("bg2_region")), right_on="coverage_type_location", how="left")["total_rate"].alias("bg2_contents_prop_covered")
            )
        else:
            df = df.with_columns(
                df.join(bg_scl_prop_covered_rate_df, left_on=pl.concat_str(pl.lit("Buildings"), pl.lit("Non-Southeast")), right_on="coverage_type_location", how="left")["total_rate"].alias("bg2_buildings_prop_covered"),
                df.join(bg_scl_prop_covered_rate_df, left_on=pl.concat_str(pl.lit("Contents"), pl.lit("Non-Southeast")), right_on="coverage_type_location", how="left")["total_rate"].alias("bg2_contents_prop_covered")
            )
    elif peril == "SCL":
        df = df.with_columns(
            df.join(bg_scl_prop_covered_rate_df, left_on=pl.concat_str(pl.lit("Buildings"), pl.col("scl_region")), right_on="coverage_type_location", how="left")["total_rate"].alias("scl_buildings_prop_covered"),
            df.join(bg_scl_prop_covered_rate_df, left_on=pl.concat_str(pl.lit("Buildings"), pl.col("scl_region")), right_on="coverage_type_location", how="left")["total_rate"].alias("scl_contents_prop_covered"),
        )
    
    df = df.with_columns(
        pl.col(f"{peril.lower()}_buildings_prop_covered").round(10).alias(f"{peril.lower()}_buildings_prop_covered"),
        pl.col(f"{peril.lower()}_contents_prop_covered").round(10).alias(f"{peril.lower()}_contents_prop_covered"),
    )


    return df


def bhi_modifier(hxd, df, peril):

    if hxd.cds.standard_fields.insured_name:
        binder_name = hxd.cds.standard_fields.insured_name
    else:
        binder_name = ""

    df = df.with_columns(
        pl.lit(binder_name).alias("binder_name")
    )

    df = join_param_table(df, hx.params.table_bhi_modifier, f"{peril}", f"{peril.lower()}_bhi_modifier", "Binder Name", "binder_name", drop=False)

    df = df.with_columns(
        pl.col(f"{peril.lower()}_bhi_modifier").fill_null(1).alias(f"{peril.lower()}_bhi_modifier")
    )
    
    df = df.drop("binder_name")

    return df

def floor_area_modifier(hxd, df, peril):

    table_floor_area_load = hx.params.table_floor_area_load

    table_floor_area_load_pl = pl.from_pandas(table_floor_area_load).rename({"State Code": "state"})

    #join on all columns
    df = df.join(table_floor_area_load_pl, on="state", how="left")
    df = df.with_columns(
        pl.lit(0).alias(f"{peril.lower()}_floor_area_load")
    )

    for cutoff in sorted([int(x) for x in list(table_floor_area_load.columns) if x != "State Code"]):
        df = df.with_columns(
            # Rex uses avg floor area, by didviding through by number of stories, CMT appears to just use floor area
            pl.when(pl.col("floor_area") >= cutoff).then(pl.col(str(cutoff))).otherwise(pl.col(f"{peril.lower()}_floor_area_load")).alias(f"{peril.lower()}_floor_area_load")
        )
        df.drop(str(cutoff))

    df = df.with_columns(
        (1 + pl.col(f"{peril.lower()}_floor_area_load")).fill_null(1).fill_nan(1).alias(f"{peril.lower()}_floor_area_modifier"),
    )

    df = df.drop(f"{peril.lower()}_floor_area_load")

    return df


def year_built_modifier(hxd, df, peril):

    if peril == "HA":

        table_year_built_load = pl.from_pandas(hx.params.table_year_built_load).rename({"HA": f"{peril.lower()}_year_built_load"})

        min_year = table_year_built_load["Year Built"].min()

        # ensure no years built prior to earliest (1900)
        df = df.with_columns(
            pl.when(pl.col("year_built") < min_year)
            .then(min_year)
            .otherwise("year_built")
            .alias("year_built_capped")
        )

        df = df.sort("year_built_capped")
        df = df.join_asof(table_year_built_load.sort("Year Built"), left_on="year_built_capped", right_on="Year Built", strategy="backward")

        df = df.with_columns(
            (1 + pl.col(f"{peril.lower()}_year_built_load")).fill_null(1).fill_nan(1).alias(f"{peril.lower()}_year_built_modifier"),
        )

        df.drop(f"{peril.lower()}_year_built_load", "year_built_capped")

    
    elif peril == "TN":

        table_year_built_tn_load = hx.params.table_year_built_tn_load

        table_year_built_tn_load_pl = pl.from_pandas(table_year_built_tn_load).rename({"StateCounty": "state_county"})

        min_year =  min(
                        sorted(
                            [int(x) for x in list(table_year_built_tn_load.columns) if x != "StateCounty"]
                        )
                    )
        # ensure no years built prior to earliest (1900)
        df = df.with_columns(
            pl.when(pl.col("year_built") < min_year)
            .then(min_year)
            .otherwise("year_built")
            .alias("year_built_capped")
        )

        #join on all columns
        df = df.join(table_year_built_tn_load_pl, on="state_county", how="left")
        df = df.with_columns(
            pl.lit(0).alias(f"{peril.lower()}_year_built_load")
        )

        for cutoff in sorted([int(x) for x in list(table_year_built_tn_load.columns) if x != "StateCounty"]):
            df = df.with_columns(
                # Rex uses avg floor area, by didviding through by number of stories, CMT appears to just use floor area
                pl.when(pl.col("year_built_capped") >= cutoff).then(pl.col(str(cutoff))).otherwise(pl.col(f"{peril.lower()}_year_built_load")).alias(f"{peril.lower()}_year_built_load")
            )
            df.drop(str(cutoff))

        df = df.with_columns(
            (1 + pl.col(f"{peril.lower()}_year_built_load")).fill_null(1).fill_nan(1).alias(f"{peril.lower()}_year_built_modifier"),
        )

        df = df.drop(f"{peril.lower()}_year_built_load", "year_built_capped")

    return df
    

