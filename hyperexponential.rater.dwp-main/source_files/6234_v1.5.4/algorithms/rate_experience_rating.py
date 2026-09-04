import hx, datetime, numpy as np, pandas as pd
import statistics
from operator import itemgetter
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, df_to_dict, look_up, ratio, data_exists, calc_reverse_product, safe_sumproduct, calculate_percentage_change, tp_lookup
from algorithms import parameter_tables_schema as params



def rate_experience_rating(hxd):
      
    # Shortcuts
    hxd_er = hxd.cds.experience_rating
    hxd_pol = hxd.cds.experience_rating.bi_policy_data
    hxd_clm = hxd.cds.experience_rating.bi_claim_data

    # Set bool for data source
    hxd.flags.er_source_bi = (hxd_er.data_source == "Import from BI")
    hxd.flags.er_source_user = (hxd_er.data_source == "User to input data")

    #07/05/25 SB Added
    hxd.flags.er_cat_yes = (hxd_er.cat_event == "Yes")
    hxd.flags.er_cat_no = (hxd_er.cat_event == "No")
    hxd.flags.er_experience_data = (hxd_er.experience_data == "Yes")
    hxd.flags.er_experience_data_no = (hxd_er.experience_data == "No")
    hxd.flags.er_actual_incurred = (hxd_er.actual_incurred == "Yes")
    hxd.flags.er_actual_incurred_no = (hxd_er.actual_incurred == "No")
    
    # Import experience rating table from view
    er = pd_df_from_hx_list(hxd.cds.experience_rating.er_calcs).fillna(0)
    scalars = df_to_dict(hx.params.scalar_parameters, "Field", "Parameter")   

    # Keep only input columns as others will be calculated (will handle bi vs user input below)
    er = er[["include", "exp_non_ed", "exp_ed", "user_input_gnwp", "user_input_rate_change", "user_input_att", "user_input_large", "user_input_cat","user_input_att_ll_total","user_input_num_incidents","user_input_num_deaths","user_input_num_injuries","user_input_incurred_total"]]

    # Set up relevant years and exposure base
    yoa = hxd.hx_core.inception_date.year
    er["yoa"] = list(range(yoa - 8, yoa))

    er["yoa_label"] = er["yoa"]

    # Selects education vs non education based on most material
    if (er["exp_non_ed"] > 0).sum() > (er["exp_ed"] > 0).sum():
        er["sel_exp_base"] = er["exp_non_ed"]
        hxd_er.curr_yr.sel_exp_base = hxd_er.curr_yr.exp_non_ed
        credibility_weighting_tbl = hx.params.experience_rating_credibility_non_education
    else:
        er["sel_exp_base"] = er["exp_ed"]
        hxd_er.curr_yr.sel_exp_base = hxd_er.curr_yr.exp_ed
        credibility_weighting_tbl = hx.params.experience_rating_credibility_education

    # Set current year params
    hxd_er.curr_yr.yoa = hxd_er.curr_yr.yoa_label = yoa
    
    # Clean
    er["sel_exp_base"] = np.where(er["sel_exp_base"] == 0, None, er["sel_exp_base"])

    # Output year labels 
    write_pd_to_hxd(er, hxd.cds.experience_rating.er_calcs, [
            "yoa",
            "yoa_label",
            "sel_exp_base",
    ])
    # Add label for total
    hxd.cds.experience_rating.er_totals.yoa = "Total Exc " + str(yoa)

    # ~~~~~~~~~~~~~~~~~~~
    # USER INPUT / BI 
    if hxd.flags.er_source_bi:
        # Drop user input cols as using BI import
        er.drop(columns=[
            "user_input_gnwp", 
            "user_input_rate_change",
            "user_input_att",
            "user_input_large",
            "user_input_cat",
            #Added 15/04/25 SB
            "user_input_att_ll_total",
            "user_input_incurred_total"
        ], inplace=True)
        hxd_er.curr_yr.rate_change = scalars["Business Plan Rate Change"] + 1
    elif hxd.flags.er_source_user:
        # Conv user input to useable cols so they can be picked up in calcs below
        er.rename(columns={
            "user_input_gnwp": "gnwp",
            "user_input_rate_change": "rate_change", 
            "user_input_att": "attrition_incurred",
            "user_input_large": "large_incurred",
            "user_input_cat": "cat_incurred",
            #Added 15/04/25 SB
            "user_input_num_incidents": "num_incidents",
            "user_input_num_deaths": "num_deaths",
            "user_input_num_injuries": "num_injuries",
            "user_input_att_ll_total": "total_att_ll_incurred",
            "user_input_incurred_total": "total_frequency_incurred"
        }, inplace=True)

        hxd_er.curr_yr.rate_change = hxd_er.curr_yr.user_input_rate_change or 1

    # Only run the experience rating calcs if policy data has been found and data source is bi
    if data_exists(hxd_pol) and hxd.flags.er_source_bi:
        
        # ~~~~~~~~~~~~~~~~~~~
        # POLICY DATA

        pol = pd_df_from_hx_list(hxd_pol).fillna(0)

        # Convert premium to USD - DO NOT NEED AS WEP IN USD ALREADY
        # fx_rates_df = params.fx_rates.df()
        # fx_rates = df_to_dict(fx_rates_df, "ccy", "fx_rate")
        # pol["fx_rate"] = pol["SettlementCurrency"].map(fx_rates).fillna(1)
        # pol["gnwp"] = pol["WrittenOrEstimatedPremium"] * pol["fx_rate"]
        pol["gnwp"] = pol["TotalWrittenIfNotSignedMultiplier"] * 1

        # Calculate rate change divisors
        pol["pre_rc_prem"] = np.where(pol["RateChangeDivisor"] > 0, pol["gnwp"] / pol["RateChangeDivisor"], 0) 
        pol["post_rc_prem"] = np.where(pol["RateChangeDivisor"] > 0, pol["gnwp"], 0) 
        
        # Sum over yoa for merge onto main table
        pol_grp = pol.groupby("YOA")[["gnwp", "pre_rc_prem", "post_rc_prem"]].sum().reset_index()
        pol_grp = pol_grp.rename(columns={"YOA": "yoa"})

        # Calculate rate change
        pol_grp["rate_change"] = np.where(pol_grp["pre_rc_prem"] > 0,  pol_grp["post_rc_prem"] / pol_grp["pre_rc_prem"] , 1)
        
        # Merge on calculated policy data to main experience table
        er = er.merge(pol_grp[["yoa", "gnwp", "rate_change"]], on="yoa", how="left")


        # ~~~~~~~~~~~~~~~~~~~ 
        # CLAIM DATA

        # Check if claims exist
        if data_exists(hxd_clm):
            clm = pd_df_from_hx_list(hxd_clm).fillna(0)

            # Convert claims to USD - DO NOT NEED AS USING USD COLUMN FROM SQL
            # clm["fx_rate"] = clm["SettlementCurrency"].map(fx_rates).fillna(1)
            # clm["claims_usd"] = clm["BeazleyShareTotalIncurredInUSD"] * clm["fx_rate"]
            clm["claims_usd"] = clm["SlipOrderTotalIncurred"] * 1
            
            # Sum over claims data for Attrition, Large and Cat
            clm_att = clm.loc[
                (clm["claims_usd"] < scalars["Experience Rating LL Threshold"]) 
                & 
                ((clm["MarketCatCode"] == "") | (clm["MarketCatCode"].isna()))
            ].groupby("YOA")[["claims_usd"]].sum()

            clm_large = clm.loc[
                (clm["claims_usd"] >= scalars["Experience Rating LL Threshold"])
                & 
                ((clm["MarketCatCode"] == "") | (clm["MarketCatCode"].isna()))
            ].groupby("YOA")[["claims_usd"]].sum()

            clm_cat = clm.loc[
                (clm["MarketCatCode"] != "") & (clm["MarketCatCode"].notna())
            ].groupby("YOA")[["claims_usd"]].sum()

            # Convert to dictinary for easy merge with er table (note didn't resert index on previous sum)
            clm_att = clm_att["claims_usd"].to_dict()
            clm_large = clm_large["claims_usd"].to_dict()
            clm_cat = clm_cat["claims_usd"].to_dict()

            # Merge with main er table
            er["attrition_incurred"] = er["yoa"].map(clm_att).fillna(0)
            er["large_incurred"] = er["yoa"].map(clm_large).fillna(0)
            er["cat_incurred"] = er["yoa"].map(clm_cat).fillna(0)
            er["total_att_ll_incurred"] = er["attrition_incurred"] + er["large_incurred"]
            er["total_frequency_incurred"] = 0
        else:
            er["attrition_incurred"] = 0
            er["large_incurred"] = 0
            er["cat_incurred"] = 0
            er["total_att_ll_incurred"] = 0
            er["total_frequency_incurred"] = 0
        
        pass # End BI source code

    for col in ["num_incidents", "num_deaths", "num_injuries"]:
        if col not in er.columns:
            er[col] = 0        
            
    # ~~~~~~~~~~~~~~~~~~~
    # Only run the remaining calcs if either bi data exists OR alt rating is used 
    if data_exists(hxd_pol) or hxd.flags.er_source_user:

        # ~~~~~~~~~~~~~~~~~~~
        # RATE CHANGE
        
        # Clean zeros and nulls
        er["rate_change"].replace({np.nan: 1, 0: 1}, inplace=True)
        rc_list = list(er["rate_change"])
        rc_list.append(hxd_er.curr_yr.rate_change)
        # Calculate rate change index
        er["rate_change_index"] = calc_reverse_product(rc_list)

        # On level premium 
        er["on_level_premium"] = er["gnwp"] * er["rate_change_index"]

        # Clean for zeros
        er["gnwp"].replace(np.nan, 0, inplace=True)
        er["on_level_premium"].replace(np.nan, 0, inplace=True)

        # ~~~~~~~~~~~~~~~~~~~
        # Attritional projections
        ielr = df_to_dict(hx.params.ielr_terrorism, "YOA", "ILR")
        bp_cat = df_to_dict(hx.params.bp_cat_ulr, "YOA", "BP Cat LR")
        dfm = hx.params.dfm_terrorism

        er["attrition_ielr"] = er["yoa"].map(ielr).fillna(0)

        for dev_yr in er["yoa"]:
            if dev_yr == yoa:
                er.loc[er["yoa"] == dev_yr,"attrition_dev_factor"] = 0
            else:
                er.loc[er["yoa"] == dev_yr,"attrition_dev_factor"] = look_up((yoa - dev_yr)*4, "Dev Qtr", "DFM", dfm, if_not_found=1)

        er["attrition_ult_claims"] = np.where(
            er["attrition_dev_factor"] < scalars["Experience Rating Dev Perc"],
            er["attrition_incurred"] + (1 - er["attrition_dev_factor"]) * er["attrition_ielr"] * er["on_level_premium"],
            er["attrition_incurred"] / er["attrition_dev_factor"]
        )

        er["attrition_on_level_ulr"] = ratio(er["attrition_ult_claims"], er["on_level_premium"], if_undefined=0)    

        # Large loss projections

        large_avg_lr_selection = (er["attrition_dev_factor"] > 0.75) & (er["include"])
        er["large_avg_lr"] = ratio(
            er[large_avg_lr_selection]["large_incurred"].mean(),
            er[large_avg_lr_selection]["on_level_premium"].mean(),
            if_undefined=0
        )

        include_bool = (er["attrition_dev_factor"] > 0.75) & (er["include"]) & (er["gnwp"] > 0)

        avg_large_lr = ratio(
            er[include_bool]["large_incurred"].sum(), 
            er[include_bool]["on_level_premium"].sum(),
            if_undefined=0
        )      
        large_cred = look_up(include_bool.sum(), "Years", "Weight", hx.params.exp_rating_large_credibility)
        weighted_ll = scalars["Experience Rating LL Load"] * large_cred + avg_large_lr * (1 - large_cred)
        er["large_ult_claims"] = weighted_ll * er["on_level_premium"]
        
        er["large_ulr"] = np.where(er["on_level_premium"] > 0, weighted_ll, None)
        
        # Assign to view 
        er["large_avg_lr"] = np.where(er["on_level_premium"] > 0, avg_large_lr, None)
        er["large_ll_assumption"] = np.where(er["on_level_premium"] > 0, scalars["Experience Rating LL Load"], None)  
        er["large_weighted_ll"] = np.where(er["on_level_premium"] > 0, weighted_ll, None)
        # ~~~

        # Catastrophe claims projections
        er["cat_ulr"] = ratio(er["cat_incurred"], er["on_level_premium"], if_undefined=0)
        er["cat_ult_claims"] = er["cat_ulr"] * er["on_level_premium"]

        # rms_or_bp_cat_lr = scalars["Experience Rating Cat Load"]
        hxd_er.cat_rms_or_bp.calculated = scalars["Experience Rating Cat Load"]
        rms_or_bp_cat_lr = hxd_er.cat_rms_or_bp.selected

        cat_avg_lr = ratio(
            er[include_bool]["cat_incurred"].sum(), 
            er[include_bool]["on_level_premium"].sum(),
            if_undefined=0
        )           
        cat_ulr = max(rms_or_bp_cat_lr, cat_avg_lr)

        er["cat_avg"] = cat_avg_lr * er["on_level_premium"]
        er["cat_rms_or_bp"] = rms_or_bp_cat_lr * er["on_level_premium"]
        er["cat_ult_claims"] = cat_ulr * er["on_level_premium"]
        er["cat_ulr"] = np.where(er["on_level_premium"] > 0, cat_ulr, None) 
       
        #Base and Social Inflation Added 28/04/25 SB
        Baseinfl_df = hx.params.inflation
        Baseinfl_df.rename(columns={'YOA': 'yoa'}, inplace=True)
        Baseinfl_df = Baseinfl_df[["yoa", "Base Inflation"]]
        Baseinfl_curr_yr = look_up(yoa, "yoa", "Base Inflation", Baseinfl_df, if_not_found=0.02) + 1
        er = er.merge(Baseinfl_df, how="left", on="yoa")
        er["Base Inflation"] = np.where(pd.isna(er["Base Inflation"]), 0.02, er["Base Inflation"])
        lst = list(er["Base Inflation"] + 1)
        lst.append(Baseinfl_curr_yr)
        er["Baseinfl_index"] = calc_reverse_product(lst)

        
        Socialinfl_df = hx.params.inflation
        Socialinfl_df.rename(columns={'YOA': 'yoa'}, inplace=True)
        Socialinfl_df = Socialinfl_df[["yoa", "Social Inflation"]]
        Socialinfl_curr_yr = look_up(yoa, "yoa", "Social Inflation", Socialinfl_df, if_not_found=0) + 1
        er = er.merge(Socialinfl_df, how="left", on="yoa")
        er["Social Inflation"] = np.where(pd.isna(er["Social Inflation"]), 0, er["Social Inflation"])
        lst = list(er["Social Inflation"] + 1)
        lst.append(Socialinfl_curr_yr)
        er["Socialinfl_index"] = calc_reverse_product(lst)

        #Total Inflation for Total Incurred user input
        infl_df = hx.params.inflation
        infl_df["infl"] = infl_df["Base Inflation"] + infl_df["Social Inflation"]
        infl_df.rename(columns={'YOA': 'yoa'}, inplace=True)
        infl_df = infl_df[["yoa", "infl"]]
        infl_curr_yr = look_up(yoa, "yoa", "infl", infl_df, if_not_found=0.02) + 1
        er = er.merge(infl_df, how="left", on="yoa")
        er["infl"] = np.where(pd.isna(er["infl"]), 0.02, er["infl"])
        lst = list(er["infl"] + 1)
        lst.append(infl_curr_yr)
        er["infl_index"] = calc_reverse_product(lst)


        
        #Court Award Split
        #split_dict = df_to_dict(hx.params.court_award_split, "Cost Type", "Split")

        #Frequency Experience Rating Added 17/04/25 SB
        severity_dict = df_to_dict(hx.params.severity, "Component", "Cost of typical event")

        #Added 15/04/25 SB
        # Total projections
        er["total_att_ll_ielr"] = er["yoa"].map(ielr).fillna(0)

        er["cat_bp"] = np.where (hxd.flags.er_cat_no, scalars["Experience Rating Cat Load"] * er["on_level_premium"],0)

        for dev_yr in er["yoa"]:
            if dev_yr == yoa:
                er.loc[er["yoa"] == dev_yr,"total_att_ll_dev_factor"] = 0
            else:
                er.loc[er["yoa"] == dev_yr,"total_att_ll_dev_factor"] = look_up((yoa - dev_yr)*4, "Dev Qtr", "DFM", dfm, if_not_found=1)

        er["attrition_ll_ult_claims"] = np.where(
            er["total_att_ll_dev_factor"] < scalars["Experience Rating Dev Perc"],
            er["total_att_ll_incurred"] + (1 - er["total_att_ll_dev_factor"]) * er["total_att_ll_ielr"] * er["on_level_premium"],
            er["total_att_ll_incurred"] / er["total_att_ll_dev_factor"]
        )

        #Added 17/07/25 SB
        #Separate BF ultimate projection method for the total incurred entered during the frequency stage. This uses the exposure measure entered in the summary table
        er["total_frequency_incurred_ult"] = np.where(
            er["total_att_ll_dev_factor"] < scalars["Experience Rating Dev Perc"],
            er["total_frequency_incurred"] + (1 - er["total_att_ll_dev_factor"]) * er["total_att_ll_ielr"] * np.where(pd.isna(er["sel_exp_base"]),0,er["sel_exp_base"]),
            er["total_frequency_incurred"] / er["total_att_ll_dev_factor"]
        )


        er["frequency_ult_claims"]= np.where(hxd.flags.er_actual_incurred,er["total_frequency_incurred_ult"], (er["num_deaths"]+er["num_injuries"])*severity_dict["Legal Costs"]+ er["num_deaths"]*severity_dict["Funeral"] + (er["num_deaths"]+er["num_injuries"])*severity_dict["Counselling"]+ er["num_deaths"]*severity_dict["Death"]+ er["num_injuries"]*severity_dict["PPD"]+ er["num_injuries"]*severity_dict["Medical Expenses"]+ er["num_incidents"]*severity_dict["Crisis Management"])
        er["frequency_inf_ultimate"] = np.where(hxd.flags.er_actual_incurred,(er["total_frequency_incurred_ult"]*er["infl_index"]), (er["num_deaths"]+er["num_injuries"])*severity_dict["Legal Costs"]*0.7*er["Baseinfl_index"]+(er["num_deaths"]+er["num_injuries"])*severity_dict["Legal Costs"]*0.3*er["Socialinfl_index"]+ er["num_deaths"]*severity_dict["Funeral"] + (er["num_deaths"]+er["num_injuries"])*severity_dict["Counselling"]*er["Baseinfl_index"]+ er["num_deaths"]*severity_dict["Death"]+ er["num_injuries"]*severity_dict["PPD"]*er["Baseinfl_index"]+ er["num_injuries"]*severity_dict["Medical Expenses"]*er["Baseinfl_index"]+ er["num_incidents"]*severity_dict["Crisis Management"])
        er["frequency_infl_index"] = ratio(er["frequency_inf_ultimate"],er["frequency_ult_claims"], if_undefined=0)
        er["total_ult_claims"] = er["attrition_ll_ult_claims"] + er["cat_bp"]

        er["total_on_level_ulr"] = ratio(er["total_ult_claims"], er["on_level_premium"], if_undefined=0)

        # Ult claims
        er["ultimate_claims"] = np.where(hxd.flags.er_source_bi, er["attrition_ult_claims"] + er["large_ult_claims"] + er["cat_ult_claims"],
                                np.where(hxd.flags.er_experience_data, er["total_ult_claims"], er["frequency_ult_claims"]))

        #SB Added 10/05/25 Displayed inflation index changes based on method selection in the summary table
        er["sel_infl_index"] = np.where(hxd.flags.er_experience_data_no,er["frequency_infl_index"],er["infl_index"])

        # Does not inflate CAT where the business plan cat ULR has been used. 
        er["inf_ultimate"] = np.where(hxd.flags.er_source_bi,np.where(
            er["cat_avg"] == er["cat_ult_claims"],
            er["ultimate_claims"] * er["infl_index"],
            (er["attrition_ult_claims"] + er["large_ult_claims"]) * er["infl_index"] + er["cat_ult_claims"]
        ),
        np.where(hxd.flags.er_experience_data, er["attrition_ll_ult_claims"]* er["infl_index"] + er["cat_bp"],er["frequency_inf_ultimate"]))
        
        # ~~~~~~~~~~~~~~~~~~~
        # TOTALS EXCL. CURR YEAR
        
        er_totals = hxd.cds.experience_rating.er_totals
        er_excl_curr_yr = er.loc[(er["yoa"] < yoa) & (er["include"])]

        er_totals.exp_non_ed = er_excl_curr_yr["exp_non_ed"].sum()
        er_totals.exp_ed = er_excl_curr_yr["exp_ed"].sum()
        er_totals.sel_exp_base = er_excl_curr_yr["sel_exp_base"].sum()

        er_totals.on_level_premium = er_excl_curr_yr["on_level_premium"].sum()
        er_totals.attrition_ult_claims = er_excl_curr_yr["attrition_ult_claims"].sum()
        er_totals.attrition_on_level_ulr = ratio(er_totals.attrition_ult_claims, er_totals.on_level_premium, if_undefined=0)
        
        er_totals.large_ult_claims = er_excl_curr_yr["large_ult_claims"].sum()
        er_totals.large_ulr = ratio(er_totals.large_ult_claims, er_totals.on_level_premium, if_undefined=0)
        
        er_totals.cat_ult_claims = er_excl_curr_yr["cat_ult_claims"].sum()
        er_totals.cat_ulr = ratio(er_totals.cat_ult_claims, er_totals.on_level_premium, if_undefined=0)

        er_totals.ultimate_claims = er_excl_curr_yr["ultimate_claims"].sum()
        er_totals.inf_ultimate = er_excl_curr_yr["inf_ultimate"].sum()

        if hxd.flags.er_source_bi:
            er_totals.gnwp = er_excl_curr_yr["gnwp"].sum()
            er_totals.attrition_incurred = er_excl_curr_yr["attrition_incurred"].sum()
            er_totals.large_incurred = er_excl_curr_yr["large_incurred"].sum()
            er_totals.cat_incurred = er_excl_curr_yr["cat_incurred"].sum()
            # er_totals.total_incurred = er_excl_curr_yr["total_incurred"].sum()
        elif hxd.flags.er_source_user:
            er_totals.gnwp = er_totals.user_input_gnwp = er_excl_curr_yr["gnwp"].sum()
            er_totals.attrition_incurred = er_totals.user_input_att = er_excl_curr_yr["attrition_incurred"].sum()
            er_totals.large_incurred = er_totals.user_input_large = er_excl_curr_yr["large_incurred"].sum()
            er_totals.cat_incurred = er_totals.user_input_cat = er_excl_curr_yr["cat_incurred"].sum()
            #Added 15/04/25 SB
            er_totals.total_att_ll_incurred = er_totals.user_input_att_ll_total = er_excl_curr_yr["total_att_ll_incurred"].sum()
            er_totals.num_incidents = er_totals.user_input_num_incidents = er_excl_curr_yr["num_incidents"].sum()
            er_totals.num_deaths = er_totals.user_input_num_deaths = er_excl_curr_yr["num_deaths"].sum()
            er_totals.num_injuries = er_totals.user_input_num_injuries = er_excl_curr_yr["num_injuries"].sum()
            er_totals.frequency_ult_claims = er_totals.frequency_ult_claims = er_excl_curr_yr["frequency_ult_claims"].sum()
            er_totals.frequency_inf_ultimate = er_totals.frequency_inf_ultimate = er_excl_curr_yr["frequency_inf_ultimate"].sum()
            er_totals.user_input_incurred_total = er_totals.user_input_incurred_total = er_excl_curr_yr["total_frequency_incurred"].sum()
        # ~~~~~~~~~~~~~~~~~~~
        # WEIGHTING METHOD TO GET FINAL BURING COST

        er["decay_factor"] = [0.9**i for i in reversed(range(8))]
        er["exposure_factor"] = ratio(er["sel_exp_base"], er_totals.sel_exp_base, if_undefined=0)
        er["dev_factor"] = er["attrition_dev_factor"]
        #SB Added 15/0/25
        er["dev_factor"] = er["total_att_ll_dev_factor"]
        er["combined_factor"] = np.where(
            er["include"], 
            er["decay_factor"] * er["exposure_factor"] * er["dev_factor"], 
            0
        )
        er["weight_by_year"] = er["combined_factor"] / er["combined_factor"].sum()

        hxd_er.final_burning_cost = ratio(
            safe_sumproduct(er["inf_ultimate"], er["weight_by_year"], if_undefined=0),  # Weighted avg. claims
            safe_sumproduct(er["sel_exp_base"], er["weight_by_year"], if_undefined=0), # Weighted avg. exposure
        if_undefined=0) * (hxd_er.curr_yr.sel_exp_base or 0) # Curr yr exposure

        
        # ~~~~~~~~~~~~~~~~~~~
        # Add Non Modelled Perils Load 
        tp_params_df = params.tp_parameters.df()
        yoa = hxd.hx_core.inception_date.year
        # To stop the model erroring if the inception year defaults to an old year not in the TP data
        if yoa in list(tp_params_df["year"]):
            tp_year = yoa
        else:
            tp_year = tp_params_df["year"].max()
        
        bp_class = hxd.cds.standard_fields.benchmark_class # DWP
        nmp_load = tp_lookup("nmp_load", bp_class, tp_params_df, tp_year) or 0   

        hxd_er.final_burning_cost = hxd_er.final_burning_cost * (1 + nmp_load)

        # ~~~~~~~~~~~~~~~~~~~
        # CREDIBILITY WEIGHTING WITH EXPOSURE METHOD

        exp_lst = list(er["sel_exp_base"]) + [hxd_er.curr_yr.sel_exp_base]
        exp_lst = [0 if x is None else x for x in exp_lst]
        annual_avg_exposure = statistics.mean(exp_lst)
        
        estab_lst = [float(i) for i in credibility_weighting_tbl.columns[1:]]
        col_num = len([i for i in estab_lst if i <= annual_avg_exposure])

        yrs_of_data = (er["gnwp"] > 0).sum()

        # Can index directly from position in table
        hxd_er.credibility_weight = credibility_weighting_tbl.iloc[yrs_of_data - 1, col_num]
        

        # ~~~~~~~~~~~~~~~~~~~
        # CHART CALCS

        # Calculate data for the charts
        yr_lst = er["yoa"].tolist()
        yr_lst.pop(0)
        chart_data = pd.DataFrame({
            "yoa": yr_lst,
            "exp_non_ed_perc": calculate_percentage_change(er["exp_non_ed"].tolist()),
            "exp_ed_perc": calculate_percentage_change(er["exp_ed"].tolist()),
            "gnwp_perc": calculate_percentage_change(er["gnwp"].tolist())
        })
        
        # Remove rows which are all -100%s, to remove unused years from chart
        cols_to_check = chart_data.columns.difference(["yoa"])
        chart_data = chart_data.loc[~(chart_data[cols_to_check] == -1).all(axis=1)]
        chart_data.replace(-1, 0, inplace=True)
        
        hxd.cds.experience_rating.er_chart_data = chart_data.to_dict(orient="records")

        # ~~~~~~~~~~~~~~~~~~~
        # OUTPUT

        # Clean to remove unnecessary zeros in the table (order matters)        
        for col in ["rate_change", "rate_change_index", "on_level_premium"]:
            er[col] = np.where(er["gnwp"] == 0, None, er[col])

        for col in [
            "attrition_incurred",
            "large_incurred",
            "cat_incurred",
            "attrition_ielr",
            "attrition_dev_factor",
            "attrition_ult_claims",
            "attrition_on_level_ulr",
            "large_avg_lr",
            "large_ll_assumption",
            "large_weighted_ll",
            "large_ult_claims",
            "large_ulr",
            "cat_avg",
            "cat_rms_or_bp",
            "cat_ult_claims",
            "cat_ulr",
            "total_att_ll_ielr",
            "total_att_ll_dev_factor",
            "attrition_ll_ult_claims",
            "total_ult_claims",
            "total_on_level_ulr",
            "frequency_ult_claims",
            "frequency_infl_index",
            "frequency_inf_ultimate"

        ]:
            er[col] = np.where(
                (er["gnwp"] == 0) & (er[col] == 0), 
                None, 
                er[col]
            )
                    
        # Set last
        er["gnwp"] = np.where(er["gnwp"] == 0, None, er["gnwp"])       
        
        # Output
        write_pd_to_hxd(er, hxd.cds.experience_rating.er_calcs, [
            "gnwp",
            "rate_change",
            "rate_change_index",
            "on_level_premium",
            "attrition_incurred",
            "large_incurred",
            "cat_incurred",
            "attrition_ielr",
            "attrition_dev_factor",
            "attrition_ult_claims",
            "attrition_on_level_ulr",
            "large_avg_lr",
            "large_ll_assumption",
            "large_weighted_ll",
            "large_ult_claims",
            "large_ulr",
            "cat_avg",
            "cat_rms_or_bp",
            "cat_ult_claims",
            "cat_ulr",
            "ultimate_claims",
            "sel_infl_index",
            "inf_ultimate",
            "cat_bp",
            "total_att_ll_incurred",
            "total_att_ll_ielr",
            "total_att_ll_dev_factor",
            "attrition_ll_ult_claims",
            "total_ult_claims",
            "total_on_level_ulr",
            "frequency_ult_claims",
            "frequency_infl_index",
            "frequency_inf_ultimate",
        ])
        
        pass # End if



