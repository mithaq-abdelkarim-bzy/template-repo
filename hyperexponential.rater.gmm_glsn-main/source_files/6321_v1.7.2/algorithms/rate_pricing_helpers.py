import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
import datetime as date
from operator import itemgetter
from algorithms.rate_tech_eo import rate_tech_eo
from scipy.stats import gamma, poisson, lognorm, norm
from algorithms.rate_umbrella import rate_umbrella
from algorithms.timer import timer


def show_hides_and_labels(hxd):
    cds=hxd.cds

    #This is to set the option label
    for index, x in enumerate(cds.options):
        x.option_label = f"Option {index+1}"
    
    # This sets the show hides for the coverages to be displayed in the Pricing tab
    if cds.gmm_masking : 
        for coverage in ["professional_liability",
            "sexual_abuse",
            "employee_benefits_liability",
            "product_liability",
            "eo",
            "general_liability",
            "employers_liability",
            "tech_eo_products_media"] :

            if cds.international_masking:
                setattr(getattr(cds.rating_factors.pricing,coverage),"show_row", True)
                setattr(cds.rating_factors.pricing.professional_liability,"label","Professional Liability/Medical Malpractice")
                setattr(cds.rating_factors.pricing.general_liability,"label","General Liability/Public Liability")
                setattr(cds.rating_factors.pricing.eo,"label","E&O/Professional Indemnity")
            else:
                setattr(getattr(cds.rating_factors.pricing,coverage),"show_row", True)
                setattr(cds.rating_factors.pricing.employers_liability,"show_row", False)
                setattr(cds.rating_factors.pricing.professional_liability,"label","Professional Liability")
                setattr(cds.rating_factors.pricing.general_liability,"label","General Liability")
                setattr(cds.rating_factors.pricing.eo,"label","E&O")

            if cds.exposure.granular.gmm_product.product == "Virtual Care" or cds.rating_factors.gmm.product_override == "Virtual Care" :
                setattr(getattr(cds.rating_factors.pricing,coverage),"show_row", True)
                setattr(cds.rating_factors.pricing.eo,"show_row", False)
                cds.punitive_damages_masking = False
            else:
                setattr(getattr(cds.rating_factors.pricing,coverage),"show_row", True)
                cds.punitive_damages_masking = True

            if cds.exposure.granular.gmm_product.product == "Triage":
                setattr(getattr(cds.rating_factors.pricing,coverage),"show_row", True)
                setattr(cds.rating_factors.pricing.tech_eo_products_media,"show_row", False)
            else:
                setattr(getattr(cds.rating_factors.pricing,coverage),"show_row", True)    
        tech_eo_selection = cds.rating_factors.pricing.tech_eo_products_media.include_primary
    elif cds.glsn_masking:
        for coverage in ["product_liability",
            "eo",
            "healthcare_professional_liability",
            "general_liability",
            "sexual_abuse",
            "employee_benefits_liability",
            "product_recall",
            "well_tech_eo_media"] :
            setattr(getattr(cds.rating_factors.pricing,coverage),"show_row", True)

            if cds.rating_factors.glsn.form.selected == "WellTech":
                setattr(getattr(cds.rating_factors.pricing,coverage),"show_row", True)
                setattr(cds.rating_factors.pricing.eo,"show_row", False)
            else:
                setattr(getattr(cds.rating_factors.pricing,coverage),"show_row", True)
        tech_eo_selection = cds.rating_factors.pricing.well_tech_eo_media.include_primary
        cds.punitive_damages_masking = True
       
    cds.tech_eo_selection = tech_eo_selection


def basic_inputs(hxd, option):
    cds=hxd.cds
    variables = {}

    # Product and Class
    variables["product"] = getattr(cds.exposure.granular, f"{option}_product").product
    
    if option == "gmm":
        variables["class"] = cds.exposure.granular.gmm_product.cob_class
    elif option == "glsn":
        cds.rating_factors.glsn.form.calculated = cds.exposure.granular.glsn_product.product
        glsn_class_table = utils.pd_df_from_hx_list(cds.exposure.granular.glsn_primary_exposure_details)
        variables["glsn_class_table"] = glsn_class_table
        variables["biosecure_product"] = (cds.rating_factors.glsn.form.selected == "BioSecure") | ((cds.rating_factors.glsn.form.selected != "NutraGuard") & (variables["product"] == "BioSecure"))
    
        if np.sum(glsn_class_table["selection"]) > 0 : 
            variables["class"] = glsn_class_table.loc[:,["exposure_base"]][glsn_class_table["selection"] == True].iloc[0].iloc[0]
    
    # Policy Term Pro-Rata Factor
    variables["inception_date"] = hxd.hx_core.inception_date
    expiry_date = hxd.hx_core.expiry_date
    variables["policy_term"] = utils.policy_term(variables["inception_date"],expiry_date)    
    
    # Currency Factor

    # FX rate for currency conversion - from user library
    fx_rates = params.fx_rates.df()
    ccy = cds.currencies.source_currency
    fx_rate = utils.look_up(ccy, 'ccy', 'fx_rate', fx_rates, if_not_found=1) # default to USD if error
    variables["currency_factor"] = 1 / fx_rate

    # Total revenue for account  
    variables["revenue"] = cds.exposure.aggregate.revenue * variables["currency_factor"]

    return variables


def schedule_mod_calculations(hxd, option, variables):
    '''
    Fill in the schedule rating table and get the total schedule mod
    '''    
    cds = hxd.cds

    schedule_rating_params= getattr(hx.params, f"table_{option}_schedule_mods")
    mod_name = schedule_rating_params["description_name"]
    mod_label = schedule_rating_params["description_label"]

    def set_schedule_rating_params_nodes(row):
        node = getattr(getattr(cds.modifiers, option), row["description_name"])
        # Set the min and max in the UI
        setattr(node, "min", row["min"]) 
        setattr(node, "max", row["max"])
        # Get schedule mod values from UI 
        row["schedule_mod_value"] = getattr(node, "value")
        row["schedule_mod_comment"] = getattr(node, "comment")
        return row 

    schedule_rating_params = schedule_rating_params.apply(set_schedule_rating_params_nodes, axis=1) 
    
    # Calculate total schedule mod
    total_schedule_mod = schedule_rating_params["schedule_mod_value"].sum()

    # Check schedule mod is within the bounds
    schedule_mod_min = float(schedule_rating_params[mod_name =="total_schedule_rating"]["min"].iloc[0])/100
    if total_schedule_mod < schedule_mod_min :
        total_schedule_mod = schedule_mod_min

    schedule_mod_validation =  schedule_rating_params
    schedule_mod_validation["min"]  = pd.to_numeric(schedule_mod_validation["min"]) / 100
    schedule_mod_validation["max"]  = schedule_mod_validation["max"].replace("Unlimited", 10000)
    schedule_mod_validation["max"]  = pd.to_numeric(schedule_mod_validation["max"]) / 100
    schedule_rating_params["validation"] = np.where((schedule_rating_params["schedule_mod_value"] < schedule_rating_params["min"]) | (schedule_rating_params["schedule_mod_value"] > schedule_rating_params["max"]) ,True,False)

    if schedule_rating_params["validation"].sum() > 0 :
        hx.errors.validation("Schedule Rating Value Outside Allowable Range")

    schedule_rating_params["validation_comment"] = np.where((pd.notnull(schedule_rating_params["schedule_mod_value"])) & (pd.isnull(schedule_rating_params["schedule_mod_comment"])) ,True,False)

    if schedule_rating_params["validation_comment"].sum() > 0 :
        hx.errors.validation("Please enter comments for all schedule ratings applied")

    variables["total_schedule_mod_factor"] = total_schedule_mod + 1 
    # Export total schedule mod back to UI
    getattr(cds.modifiers, option).total_schedule_rating.value = variables["total_schedule_mod_factor"]


def size_discount_gmm(hxd, variables):
    cds = hxd.cds
    revenue = variables["revenue"]
    if revenue <= 0:
        variables["size_discount_factor"] = 1
        hx.errors.validation("Revenue entered must be greater than 0")
    else:    
        gmm_size_discount = hx.params.table_gmm_size_discount
        gmm_size_discount["adjusted_revenue"] = 0.0
        for i in range(1,len(gmm_size_discount)):
            gmm_size_discount.at[i,"adjusted_revenue"] = gmm_size_discount.at[i-1,"adjusted_revenue"] + gmm_size_discount.at[i-1,"credit"] * (gmm_size_discount.at[i-1,"revenue_upper"] - gmm_size_discount.at[i-1,"revenue_lower"] )

        # Set revenue lower bound
        gmm_size_discount_lower = gmm_size_discount[gmm_size_discount["revenue_lower"]<=revenue] 
        revenue_lower_bound = gmm_size_discount_lower["revenue_lower"].iloc[-1]
        # Set adjusted revenue up to lower bound
        adjusted_revenue_up_to_lower_bound = gmm_size_discount_lower["adjusted_revenue"].iloc[-1]
        #Set factor for the band
        factor_for_band = gmm_size_discount_lower["credit"].iloc[-1]

        #Calculate the adjusted revenue 
        adjusted_revenue_in_band = factor_for_band * (revenue - revenue_lower_bound)
        total_adjusted_revenue = adjusted_revenue_in_band + adjusted_revenue_up_to_lower_bound

        #Calculate the revenue size discount factor 
        variables["size_discount_factor"] = total_adjusted_revenue / revenue


def size_discount_glsn(hxd, variables):
    cds = hxd.cds
    revenue = variables["revenue"]
    if revenue <= 0:
        variables["size_discount_factor"] = 1
        hx.errors.validation("Revenue entered must be greater than 0")
    else :     
        biosecure_product = variables["biosecure_product"]
              
        glsn_size_discount = cds.rating_factors.glsn.size_discount_selection.selected

        # Size discount for revenue 
        if glsn_size_discount == "Revenue":
            
            # Attach adjusted revenue bands to size discount curve
            glsn_size_discount_revenue = hx.params.table_glsn_size_discount_rev
            glsn_size_discount_revenue["life_sciences_adjusted"] = 0.0
            glsn_size_discount_revenue["nutra_adjusted"] = 0.0

            # Calculate the difference between revenue_upper and revenue_lower
            revenue_diff = glsn_size_discount_revenue["revenue_upper"] - glsn_size_discount_revenue["revenue_lower"]

            # Calculate the adjusted life_sciences values
            glsn_size_discount_revenue["life_sciences_adjusted"] = (glsn_size_discount_revenue["life_sciences"] * revenue_diff).shift(1).fillna(0).cumsum()
            glsn_size_discount_revenue["nutra_adjusted"] = (glsn_size_discount_revenue["nutra"] * revenue_diff).shift(1).fillna(0).cumsum()

            # OLD Method using For Loops
            # for i in range(1,len(glsn_size_discount_revenue)):
            #     glsn_size_discount_revenue.at[i,"life_sciences_adjusted"] = glsn_size_discount_revenue.at[i-1,"life_sciences_adjusted"] + glsn_size_discount_revenue.at[i-1,"life_sciences"] * (glsn_size_discount_revenue.at[i-1,"revenue_upper"] - glsn_size_discount_revenue.at[i-1,"revenue_lower"] )
            #     glsn_size_discount_revenue.at[i,"nutra_adjusted"] = glsn_size_discount_revenue.at[i-1,"life_sciences_adjusted"] + glsn_size_discount_revenue.at[i-1,"nutra"] * (glsn_size_discount_revenue.at[i-1,"revenue_upper"] - glsn_size_discount_revenue.at[i-1,"revenue_lower"] )

            #Set revenue lower bound
            glsn_size_discount_lower = glsn_size_discount_revenue[glsn_size_discount_revenue["revenue_lower"]<=revenue]
            revenue_lower_bound = glsn_size_discount_lower["revenue_lower"].iloc[-1]

            # Determine which adjusted revenue column to use based on the form selected being BioSecure or NutraGuard. If neither of these, then base the adjusted revenue column on the product selected. Also calculate the relevant factor. 
            if biosecure_product :
                adjusted_revenue_up_to_lower_bound = glsn_size_discount_lower["life_sciences_adjusted"].iloc[-1]
                factor_for_band = glsn_size_discount_lower["life_sciences"].iloc[-1]
            else :
                adjusted_revenue_up_to_lower_bound = glsn_size_discount_lower["nutra_adjusted"].iloc[-1]
                factor_for_band = glsn_size_discount_lower["nutra"].iloc[-1]


            #Calculate the adjusted revenue 
            adjusted_revenue_in_band = factor_for_band * (revenue - revenue_lower_bound)
            total_adjusted_revenue = adjusted_revenue_in_band + adjusted_revenue_up_to_lower_bound
            
            #Calculate the revenue size discount factor 
            size_discount_factor = total_adjusted_revenue / revenue
            
        elif glsn_size_discount == "Participants":
            # Size discount for participants 
            # Attach adjusted participant bands to size discount curve
            glsn_size_discount_participants = hx.params.table_glsn_size_discount_part
            glsn_size_discount_participants["participants_adjusted"] = 0.0

            participants_diff = glsn_size_discount_participants["number_of_participants_higher"] - glsn_size_discount_participants["number_of_participants_lower"]

            # Calculate the adjusted participants values
            glsn_size_discount_participants["participants_adjusted"] = (glsn_size_discount_participants["discount"] * participants_diff).shift(1).fillna(0).cumsum()

            # Old method using for loops
            # for i in range(1,len(glsn_size_discount_participants)):
            #     glsn_size_discount_participants.at[i,"participants_adjusted"] = glsn_size_discount_participants.at[i-1,"participants_adjusted"] + glsn_size_discount_participants.at[i-1,"discount"] * (glsn_size_discount_participants.at[i-1,"number_of_participants_higher"] - glsn_size_discount_participants.at[i-1,"number_of_participants_lower"] )

            #Calculate the lower bound and adjusted participant
            # glsn_class_table = variables["glsn_class_table"]
            # number_of_participants = np.where(glsn_class_table["exposure_measure"] == "Participants",glsn_class_table["current_year"],0).sum()
            number_of_participants = cds.rating_factors.glsn.number_of_participants
            participants_lower_bound = glsn_size_discount_participants[glsn_size_discount_participants["number_of_participants_lower"]<=number_of_participants]["number_of_participants_lower"].iloc[-1]
            adjusted_participants_up_to_lower_bound = glsn_size_discount_participants[glsn_size_discount_participants["number_of_participants_lower"]<=participants_lower_bound]["participants_adjusted"].iloc[-1]
            factor_for_band = glsn_size_discount_participants[glsn_size_discount_participants["number_of_participants_lower"]<=participants_lower_bound]["discount"].iloc[-1]
            adjusted_participants_in_band = factor_for_band * (number_of_participants - participants_lower_bound)
            total_adjusted_participants = adjusted_participants_up_to_lower_bound + adjusted_participants_in_band

            #Calculate the revenue size discount factor 
            size_discount_factor = total_adjusted_participants / number_of_participants

        variables["size_discount_factor"] = size_discount_factor


def gu_base_prem_gmm(hxd, variables):
    cds = hxd.cds 
    currency_factor = variables["currency_factor"]

    if variables["product"] == "Triage":
        total_obe = utils.pd_df_from_hx_list(cds.exposure.aggregate.triage_running_total_obe)
        total_obe = total_obe["current_year"].iloc[0]
        base_rate_per_obe = hx.params.table_triage_base_rate.loc[0,"base_rate_per_obe"]
        base_premium = total_obe * base_rate_per_obe
        variables["base_premium"] = base_premium
    else:
        variables["base_premium"] = cds.exposure.aggregate.gmm_total_base_premium_current_year * currency_factor


def gu_base_prem_glsn(hxd, variables):
    cds = hxd.cds
    currency_factor = variables["currency_factor"]

    base_rate_standard_commission = hx.params.table_glsn_base_rate_commission.loc[0,"base_rate_standard_commission"]
    supply_chain_factor = cds.rating_factors.glsn.supply_chain_factor
    clinical_trial_factor = cds.rating_factors.glsn.clinical_trial_factor
    exposure_premium = cds.exposure.aggregate.glsn_total_base_premium_current_year * currency_factor * (1 - base_rate_standard_commission)
    variables["base_premium"] = exposure_premium * supply_chain_factor * clinical_trial_factor


def primary_layer_prem_calcs(hxd, option, coverages, variables):
    cds = hxd.cds
    inception_date = variables["inception_date"]

    retro_table = getattr(hx.params, f"table_{option}_retroactive")
    variables["surcharge_table"] =  getattr(hx.params, f"table_{option}_surcharge")
    variables["us_international"] = cds.rating_factors.us_international_choice_of_law.us_international

    surcharge_table = variables["surcharge_table"]
    us_international = variables["us_international"]

    if option == "glsn":
        filtered_surcharge_table = surcharge_table[(surcharge_table["product"] == variables["product"]) & (surcharge_table["us_international"] == variables["us_international"])]

    # get the non-options coverages and factors
    include_primary = []
    additional_coverage = []
    significant_coverage = [] # only used for glsn
    retro_date = []
    retro_years = []
    retro_factor = []

    for coverage in coverages:
        include_primary_value = getattr(getattr(cds.rating_factors.pricing , coverage),"include_primary")
        include_primary.append(include_primary_value)

        if option == "glsn":
            signficant_coverage_value = getattr(getattr(cds.rating_factors.pricing , coverage),"significant_coverage")
            significant_coverage.append(signficant_coverage_value)
            filter_by = coverage

        if option == "gmm":
            gmm_class = variables["class"]
            filtered_surcharge_table = surcharge_table[(surcharge_table["coverage_name"] == coverage) & (surcharge_table["us_international"] == us_international) & (surcharge_table["class"] == gmm_class)]
            filter_by = "surcharge"

        if filtered_surcharge_table.shape[0] >= 1 :
            additional_coverage_value = filtered_surcharge_table[filter_by].iloc[0]
        else :
            additional_coverage_value = 0   
        additional_coverage.append(additional_coverage_value) 

        if getattr(getattr(cds.rating_factors.pricing , coverage),"claims_basis") == "Occurrence":
            retro_date_value = None
        else:    
            retro_date_value = getattr(getattr(cds.rating_factors.pricing , coverage),"retroactive_date")
      
        retro_date.append(retro_date_value)

        if retro_date_value:
            if utils.policy_term(retro_date_value, inception_date) - int(utils.policy_term(retro_date_value, inception_date)) < 0.01 :
                retro_years_value = int(utils.policy_term(retro_date_value, inception_date))
            else:
                retro_years_value = math.ceil(utils.policy_term(retro_date_value, inception_date))
        else:
            retro_years_value = None
        
        # retro_years_value = (math.ceil(utils.policy_term(retro_date_value,inception_date))) if retro_date_value and retro_date_value != inception_date else 0 if  retro_date_value and retro_date_value == inception_date else None 

        retro_years.append(retro_years_value)
        filtered_retro_table = retro_table[retro_table["retro_years"] == retro_years_value] 
        if filtered_retro_table.shape[0]:
            retro_factor_value = filtered_retro_table["factor"].iloc[0]
        else:
            retro_factor_value = 1

        retro_factor.append(retro_factor_value)
        
        #Retro validation
        if (include_primary_value) & (retro_date_value is None) & (getattr(getattr(cds.rating_factors.pricing , coverage),"claims_basis") != "Occurrence"):
            hx.errors.validation("Please enter retroactive date for selected coverages")

    coverage = pd.Series(coverages)
    
    include_primary = pd.Series(include_primary)
    additional_coverage = pd.Series(additional_coverage)
    retro_factor = pd.Series(retro_factor)

    # retrodate to use for excess layers - takes first non zero retro rate
    default_excess_retro_date_list = [value for value in retro_date if value is not None]
    if len(default_excess_retro_date_list) > 0 : 
        default_excess_retro_date = default_excess_retro_date_list[0].isoformat()
        variables["default_excess_retro_date"] = default_excess_retro_date
        #Validation error check on the retroactive dates
        latest_retro_date = max(default_excess_retro_date_list) 
        if latest_retro_date > inception_date:
            hx.errors.validation("Retro date must be before the policy inception date")
    else:
        variables["default_excess_retro_date"] = None    

       

    if significant_coverage:
        variables["non_option_coverages"] = pd.DataFrame({"coverage": coverage, "include_primary": include_primary,"significant_coverage": significant_coverage ,"additional_coverage": additional_coverage,"retro_factor": retro_factor}) 
    else:
        variables["non_option_coverages"] = pd.DataFrame({"coverage": coverage, "include_primary": include_primary, "additional_coverage": additional_coverage,"retro_factor": retro_factor}) 

    variables["filtered_surcharge_table"] = filtered_surcharge_table
    variables["retro_factor"] = retro_factor
    variables["retro_table"] = retro_table


def primary_layer_prem_calcs_gmm(hxd, coverages, variables):
    cds = hxd.cds
    gmm_class = variables["class"]
    base_premium = variables["base_premium"]
    non_option_coverages = variables["non_option_coverages"]
    size_discount_factor = variables["size_discount_factor"]
    venue_factor = variables["venue_factor"]
    policy_term = variables["policy_term"]
    total_schedule_mod_factor = variables["total_schedule_mod_factor"]
    surcharge_table = variables["surcharge_table"]
    us_international = variables["us_international"]


    # We need to adjust the Tech E&O additional coverage weight here - this uses the PL base premium
    pl_base_premium = base_premium * non_option_coverages.loc[0,["additional_coverage"]].iloc[0] * non_option_coverages.loc[0,["retro_factor"]].iloc[0] * size_discount_factor * venue_factor * policy_term 
    
    # We need to use PL base premium if PL included in primary or 1 if PL not inlcuded in primary
    pl_include_primary = non_option_coverages.loc[0,["include_primary"]].iloc[0] 

    # TECH EO
    non_option_tech_eo_filtered_temp = non_option_coverages[non_option_coverages["coverage"] == "tech_eo_products_media"]
    tech_eo_selection = non_option_tech_eo_filtered_temp["include_primary"].iloc[0]
    tech_eo_retro_factor = non_option_tech_eo_filtered_temp["retro_factor"].iloc[0]                
    
    # timer.start("rate_tech_eo")
    rate_tech_eo(hxd)
    # timer.end("rate_tech_eo")

    # tech_eo_selection = True
    tech_eo_primary_net_prem_usd = [0 for item in cds.options]
    tech_eo_base_net_prem_usd = [0 for item in cds.options]
    tech_eo_retention_ratio_factor = [0 for item in cds.options]
    tech_eo_eec_ilf = [0 for item in cds.options]
    tech_eo_agg_ilf_primary_factor = [0 for item in cds.options]
    if tech_eo_selection:
        for index,item in enumerate(cds.options):
            tech_eo_base_net_prem_usd[index] = cds.tech_eo_base_net_premium_usd
            tech_eo_primary_net_prem_usd[index] = item.tech_eo_primary_net_premium_usd     
            tech_eo_retention_ratio_factor[index] = item.tech_eo_retention_ratio_factor
            tech_eo_eec_ilf[index] = item.tech_eo_eec_ilf
            tech_eo_agg_ilf_primary_factor[index] = item.tech_eo_agg_ilf_primary_factor

    # Convert to dataframe        
    tech_eo_primary_net_prem_usd = pd.DataFrame({"tech_eo_primary_net_prem_usd":tech_eo_primary_net_prem_usd})
    tech_eo_base_net_prem_usd = pd.DataFrame({"tech_eo_base_net_prem_usd" :tech_eo_base_net_prem_usd})        
    tech_eo_retention_ratio_factor = pd.DataFrame({"tech_eo_retention_ratio_factor":tech_eo_retention_ratio_factor})
    tech_eo_eec_ilf = pd.DataFrame({"tech_eo_eec_ilf":tech_eo_eec_ilf})
    tech_eo_agg_ilf_primary_factor = pd.DataFrame({"tech_eo_agg_ilf_primary_factor":tech_eo_agg_ilf_primary_factor})

    # Add on retro factor, policy term and schedule modifier (schedule modifier only for primary)
    tech_eo_base_net_prem_usd["tech_eo_base_net_prem_raw_usd"] = tech_eo_base_net_prem_usd["tech_eo_base_net_prem_usd"] * policy_term
    tech_eo_base_net_prem_usd["tech_eo_base_net_prem_usd"] = tech_eo_base_net_prem_usd["tech_eo_base_net_prem_usd"] * tech_eo_retro_factor * policy_term                 
    tech_eo_primary_net_prem_usd["tech_eo_primary_net_prem_usd"] = tech_eo_primary_net_prem_usd["tech_eo_primary_net_prem_usd"] * tech_eo_retro_factor * policy_term * total_schedule_mod_factor          

    # tech_eo_coverage_weight
    tech_eo_coverage_weight = np.where(pl_include_primary == True, tech_eo_base_net_prem_usd.loc[0,["tech_eo_base_net_prem_usd"]].iloc[0] / pl_base_premium,1)       

    # Add on coverage weight into main table
    non_option_coverages["additional_coverage"] = np.where(non_option_coverages["coverage"] == "tech_eo_products_media", \
        tech_eo_coverage_weight , \
        non_option_coverages["additional_coverage"])
    
    # Get coverage enhancements values for the additional coverges 
    stop_gap_table = surcharge_table[(surcharge_table["coverage_name"] == "stop_gap") & (surcharge_table["us_international"] == us_international) & (surcharge_table["class"] == gmm_class)]["surcharge"]
    
    if stop_gap_table.shape[0] >=1 :
        stop_gap_additional_coverage_value = stop_gap_table.iloc[0]
    else :
        stop_gap_additional_coverage_value = 0 

    tria_table = surcharge_table[(surcharge_table["coverage_name"] == "tria") & (surcharge_table["us_international"] == us_international) & (surcharge_table["class"] == gmm_class)]["surcharge"]

    if tria_table.shape[0] >=1 :
        tria_additional_coverage_value = tria_table.iloc[0]
    else :
        tria_additional_coverage_value = 0 

    punitive_damages_table = surcharge_table[(surcharge_table["coverage_name"] == "punitive_damages") & (surcharge_table["us_international"] == us_international) & (surcharge_table["class"] == gmm_class)]["surcharge"]

    if punitive_damages_table.shape[0] >=1 :
        punitive_damages_additional_coverage_value = punitive_damages_table.iloc[0]
    else :
        punitive_damages_additional_coverage_value = 0   

    variables["tech_eo_primary_net_prem_usd"] = tech_eo_primary_net_prem_usd
    variables["tech_eo_base_net_prem_usd"] = tech_eo_base_net_prem_usd
    variables["tech_eo_retention_ratio_factor"] = tech_eo_retention_ratio_factor
    variables["tech_eo_eec_ilf"] = tech_eo_eec_ilf
    variables["tech_eo_agg_ilf_primary_factor"] = tech_eo_agg_ilf_primary_factor
    variables["stop_gap_additional_coverage_value"] = stop_gap_additional_coverage_value
    variables["tria_additional_coverage_value"] = tria_additional_coverage_value
    variables["punitive_damages_additional_coverage_value"] = punitive_damages_additional_coverage_value 


def primary_layer_prem_calcs_glsn(hxd, variables):
    filtered_surcharge_table = variables["filtered_surcharge_table"]
    
    if filtered_surcharge_table.shape[0] >= 1 :
        stop_gap_additional_coverage_value = filtered_surcharge_table["stop_gap"].iloc[0]
        tria_additional_coverage_value = filtered_surcharge_table["tria"].iloc[0]
        punitive_damages_additional_coverage_value = filtered_surcharge_table["punitive_damages"].iloc[0]
    else:
        stop_gap_additional_coverage_value = 0
        tria_additional_coverage_value = 0
        punitive_damages_additional_coverage_value = 0  

    variables["stop_gap_additional_coverage_value"] = stop_gap_additional_coverage_value
    variables["tria_additional_coverage_value"] = tria_additional_coverage_value
    variables["punitive_damages_additional_coverage_value"] = punitive_damages_additional_coverage_value

    
def options_dict_gmm(hxd):
    cds = hxd.cds
    ### Get the relevant columns from the options node - too slow using utils.pd_df_from_hx_list function
    return [{
        "coverages.professional_liability.retention": item.coverages.professional_liability.retention,
        "coverages.professional_liability.per_claim_limit":item.coverages.professional_liability.per_claim_limit,
        "coverages.professional_liability.aggregate_limit": item.coverages.professional_liability.aggregate_limit,

        "coverages.general_liability.retention": item.coverages.general_liability.retention,
        "coverages.general_liability.per_claim_limit":item.coverages.general_liability.per_claim_limit,
        "coverages.general_liability.aggregate_limit": item.coverages.general_liability.aggregate_limit,

        "coverages.product_liability.retention": item.coverages.product_liability.retention,
        "coverages.product_liability.per_claim_limit":item.coverages.product_liability.per_claim_limit,
        "coverages.product_liability.aggregate_limit": item.coverages.product_liability.aggregate_limit,

        "coverages.eo.retention": item.coverages.eo.retention,
        "coverages.eo.per_claim_limit":item.coverages.eo.per_claim_limit,
        "coverages.eo.aggregate_limit": item.coverages.eo.aggregate_limit,

        "coverages.employers_liability.retention": item.coverages.employers_liability.retention,
        "coverages.employers_liability.per_claim_limit":item.coverages.employers_liability.per_claim_limit,
        "coverages.employers_liability.aggregate_limit": item.coverages.employers_liability.aggregate_limit,

        "coverages.sexual_abuse.retention": item.coverages.sexual_abuse.retention,
        "coverages.sexual_abuse.per_claim_limit":item.coverages.sexual_abuse.per_claim_limit,
        "coverages.sexual_abuse.aggregate_limit": item.coverages.sexual_abuse.aggregate_limit,            

        "coverages.employee_benefits_liability.retention": item.coverages.employee_benefits_liability.retention,
        "coverages.employee_benefits_liability.per_claim_limit":item.coverages.employee_benefits_liability.per_claim_limit,
        "coverages.employee_benefits_liability.aggregate_limit": item.coverages.employee_benefits_liability.aggregate_limit,

        "coverages.tech_eo_products_media.retention": item.coverages.tech_eo_products_media.retention,
        "coverages.tech_eo_products_media.per_claim_limit":item.coverages.tech_eo_products_media.per_claim_limit,
        "coverages.tech_eo_products_media.aggregate_limit": item.coverages.tech_eo_products_media.aggregate_limit, 

        "agg_limit": item.agg_limit,
        "indemnity_only": item.indemnity_only,

        "include_auto_primary": item.include_auto_primary,
        "auto_measure": item.auto_measure,
        "auto_amount": item.auto_amount,

        "include_stop_gap_primary": item.include_stop_gap_primary,

        "include_tria_primary": item.include_tria_primary,

        "include_punitive_damages_primary": item.include_punitive_damages_primary,

        "costs_in_addition_selection": item.costs_in_addition_selection,
        "include_costs_in_addition_primary": item.include_costs_in_addition_primary,

        "brokerage_primary": item.brokerage_primary,
        "quoted_premium_primary": item.quoted_premium_primary,

        "coverages.professional_liability.per_claim_limit": item.coverages.professional_liability.per_claim_limit,
        "coverages.professional_liability.retention": item.coverages.professional_liability.retention,

        "per_claim_limit_1_excess": item.per_claim_limit_1_excess,
        "aggregate_limit_1_excess": item.aggregate_limit_1_excess,
        "brokerage_1_excess": item.brokerage_1_excess,
        "quoted_premium_1_excess": item.quoted_premium_1_excess,

        "per_claim_limit_2_excess": item.per_claim_limit_2_excess,
        "aggregate_limit_2_excess": item.aggregate_limit_2_excess,
        "brokerage_2_excess": item.brokerage_2_excess,
        "quoted_premium_2_excess": item.quoted_premium_2_excess,

        "per_claim_limit_3_excess": item.per_claim_limit_3_excess,
        "aggregate_limit_3_excess": item.aggregate_limit_3_excess,
        "brokerage_3_excess": item.brokerage_3_excess,
        "quoted_premium_3_excess": item.quoted_premium_3_excess,

        "per_claim_limit_4_excess": item.per_claim_limit_4_excess,
        "aggregate_limit_4_excess": item.aggregate_limit_4_excess,
        "brokerage_4_excess": item.brokerage_4_excess,
        "quoted_premium_4_excess": item.quoted_premium_4_excess,

        "per_claim_limit_5_excess": item.per_claim_limit_5_excess,
        "aggregate_limit_5_excess": item.aggregate_limit_5_excess,
        "brokerage_5_excess": item.brokerage_5_excess,
        "quoted_premium_5_excess": item.quoted_premium_5_excess,

        "per_claim_limit_6_excess": item.per_claim_limit_6_excess,
        "aggregate_limit_6_excess": item.aggregate_limit_6_excess,
        "brokerage_6_excess": item.brokerage_6_excess,
        "quoted_premium_6_excess": item.quoted_premium_6_excess,

        "per_claim_limit_7_excess": item.per_claim_limit_7_excess,
        "aggregate_limit_7_excess": item.aggregate_limit_7_excess,
        "brokerage_7_excess": item.brokerage_7_excess,
        "quoted_premium_7_excess": item.quoted_premium_7_excess,

        "per_claim_limit_8_excess": item.per_claim_limit_8_excess,
        "aggregate_limit_8_excess": item.aggregate_limit_8_excess,
        "brokerage_8_excess": item.brokerage_8_excess,
        "quoted_premium_8_excess": item.quoted_premium_8_excess,

        "per_claim_limit_9_excess": item.per_claim_limit_9_excess,
        "aggregate_limit_9_excess": item.aggregate_limit_9_excess,
        "brokerage_9_excess": item.brokerage_9_excess,
        "quoted_premium_9_excess": item.quoted_premium_9_excess,

        "per_claim_limit_10_excess": item.per_claim_limit_10_excess,
        "aggregate_limit_10_excess": item.aggregate_limit_10_excess,
        "brokerage_10_excess": item.brokerage_10_excess,
        "quoted_premium_10_excess": item.quoted_premium_10_excess,

        "cyber_premium_primary": item.cyber_premium_primary

    } for item in cds.options]
    

def options_dict_glsn(hxd):
    cds = hxd.cds
    return [{
           "coverages.product_liability.retention": item.coverages.product_liability.retention,
            "coverages.product_liability.per_claim_limit":item.coverages.product_liability.per_claim_limit,
            "coverages.product_liability.aggregate_limit": item.coverages.product_liability.aggregate_limit,

            "coverages.eo.retention": item.coverages.eo.retention,
            "coverages.eo.per_claim_limit":item.coverages.eo.per_claim_limit,
            "coverages.eo.aggregate_limit": item.coverages.eo.aggregate_limit,

            "coverages.healthcare_professional_liability.retention": item.coverages.healthcare_professional_liability.retention,
            "coverages.healthcare_professional_liability.per_claim_limit":item.coverages.healthcare_professional_liability.per_claim_limit,
            "coverages.healthcare_professional_liability.aggregate_limit": item.coverages.healthcare_professional_liability.aggregate_limit,

            "coverages.sexual_abuse.retention": item.coverages.sexual_abuse.retention,
            "coverages.sexual_abuse.per_claim_limit":item.coverages.sexual_abuse.per_claim_limit,
            "coverages.sexual_abuse.aggregate_limit": item.coverages.sexual_abuse.aggregate_limit,

            "coverages.employee_benefits_liability.retention": item.coverages.employee_benefits_liability.retention,
            "coverages.employee_benefits_liability.per_claim_limit":item.coverages.employee_benefits_liability.per_claim_limit,
            "coverages.employee_benefits_liability.aggregate_limit": item.coverages.employee_benefits_liability.aggregate_limit,

            "coverages.product_recall.retention": item.coverages.product_recall.retention,
            "coverages.product_recall.per_claim_limit":item.coverages.product_recall.per_claim_limit,
            "coverages.product_recall.aggregate_limit": item.coverages.product_recall.aggregate_limit,            

            "coverages.general_liability.retention": item.coverages.general_liability.retention,
            "coverages.general_liability.per_claim_limit":item.coverages.general_liability.per_claim_limit,
            "coverages.general_liability.aggregate_limit": item.coverages.general_liability.aggregate_limit,

            "coverages.well_tech_eo_media.retention": item.coverages.well_tech_eo_media.retention,
            "coverages.well_tech_eo_media.per_claim_limit":item.coverages.well_tech_eo_media.per_claim_limit,
            "coverages.well_tech_eo_media.aggregate_limit": item.coverages.well_tech_eo_media.aggregate_limit, 

            "agg_limit": item.agg_limit,
            "agg_retention": item.agg_retention,
            "indemnity_only": item.indemnity_only,

            "include_auto_primary": item.include_auto_primary,
            "auto_measure": item.auto_measure,
            "auto_amount": item.auto_amount,

            "include_stop_gap_primary": item.include_stop_gap_primary,

            "include_tria_primary": item.include_tria_primary,

            "include_punitive_damages_primary": item.include_punitive_damages_primary,

            "costs_in_addition_selection": item.costs_in_addition_selection,
            "include_costs_in_addition_primary": item.include_costs_in_addition_primary,

            "brokerage_primary": item.brokerage_primary,
            "quoted_premium_primary": item.quoted_premium_primary,

            "coverages.professional_liability.per_claim_limit": item.coverages.professional_liability.per_claim_limit,
            "coverages.professional_liability.retention": item.coverages.professional_liability.retention,

            "per_claim_limit_1_excess": item.per_claim_limit_1_excess,
            "aggregate_limit_1_excess": item.aggregate_limit_1_excess,
            "brokerage_1_excess": item.brokerage_1_excess,
            "quoted_premium_1_excess": item.quoted_premium_1_excess,

            "per_claim_limit_2_excess": item.per_claim_limit_2_excess,
            "aggregate_limit_2_excess": item.aggregate_limit_2_excess,
            "brokerage_2_excess": item.brokerage_2_excess,
            "quoted_premium_2_excess": item.quoted_premium_2_excess,

            "per_claim_limit_3_excess": item.per_claim_limit_3_excess,
            "aggregate_limit_3_excess": item.aggregate_limit_3_excess,
            "brokerage_3_excess": item.brokerage_3_excess,
            "quoted_premium_3_excess": item.quoted_premium_3_excess,

            "per_claim_limit_4_excess": item.per_claim_limit_4_excess,
            "aggregate_limit_4_excess": item.aggregate_limit_4_excess,
            "brokerage_4_excess": item.brokerage_4_excess,
            "quoted_premium_4_excess": item.quoted_premium_4_excess,

            "per_claim_limit_5_excess": item.per_claim_limit_5_excess,
            "aggregate_limit_5_excess": item.aggregate_limit_5_excess,
            "brokerage_5_excess": item.brokerage_5_excess,
            "quoted_premium_5_excess": item.quoted_premium_5_excess,

            "per_claim_limit_6_excess": item.per_claim_limit_6_excess,
            "aggregate_limit_6_excess": item.aggregate_limit_6_excess,
            "brokerage_6_excess": item.brokerage_6_excess,
            "quoted_premium_6_excess": item.quoted_premium_6_excess,

            "per_claim_limit_7_excess": item.per_claim_limit_7_excess,
            "aggregate_limit_7_excess": item.aggregate_limit_7_excess,
            "brokerage_7_excess": item.brokerage_7_excess,
            "quoted_premium_7_excess": item.quoted_premium_7_excess,

            "per_claim_limit_8_excess": item.per_claim_limit_8_excess,
            "aggregate_limit_8_excess": item.aggregate_limit_8_excess,
            "brokerage_8_excess": item.brokerage_8_excess,
            "quoted_premium_8_excess": item.quoted_premium_8_excess,

            "per_claim_limit_9_excess": item.per_claim_limit_9_excess,
            "aggregate_limit_9_excess": item.aggregate_limit_9_excess,
            "brokerage_9_excess": item.brokerage_9_excess,
            "quoted_premium_9_excess": item.quoted_premium_9_excess,

            "per_claim_limit_10_excess": item.per_claim_limit_10_excess,
            "aggregate_limit_10_excess": item.aggregate_limit_10_excess,
            "brokerage_10_excess": item.brokerage_10_excess,
            "quoted_premium_10_excess": item.quoted_premium_10_excess,

            "cyber_premium_primary": item.cyber_premium_primary

        } for item in cds.options]


def agg_limit_cols(hxd, option):
    if option == "gmm": 
        return ["coverages.professional_liability.aggregate_limit",\
        "coverages.general_liability.aggregate_limit",\
        "coverages.product_liability.aggregate_limit",\
        "coverages.eo.aggregate_limit",\
        "coverages.employee_benefits_liability.aggregate_limit",\
        "coverages.employers_liability.aggregate_limit",\
        "coverages.tech_eo_products_media.aggregate_limit"]
    else:
        return ["coverages.product_liability.aggregate_limit",\
        "coverages.eo.aggregate_limit",\
        "coverages.healthcare_professional_liability.aggregate_limit",\
        "coverages.general_liability.aggregate_limit",\
        "coverages.sexual_abuse.aggregate_limit",\
        "coverages.employee_benefits_liability.aggregate_limit",\
        "coverages.product_recall.aggregate_limit",\
        "coverages.well_tech_eo_media.aggregate_limit"]
    

def rating_gmm(hxd, options_dict, variables):
    cds = hxd.cds
    cyber_selection = cds.cyber_selection

    # Unpack variables
    currency_factor = variables["currency_factor"]
    gmm_class = variables["class"]
    base_premium = variables["base_premium"]
    non_option_coverages = variables["non_option_coverages"]
    size_discount_factor = variables["size_discount_factor"]
    venue_factor = variables["venue_factor"]
    policy_term = variables["policy_term"]
    total_schedule_mod_factor = variables["total_schedule_mod_factor"]
    surcharge_table = variables["surcharge_table"]
    us_international = variables["us_international"]
    inception_date = variables["inception_date"]
    
    tech_eo_primary_net_prem_usd = variables["tech_eo_primary_net_prem_usd"]
    tech_eo_base_net_prem_usd = variables["tech_eo_base_net_prem_usd"]
    tech_eo_retention_ratio_factor = variables["tech_eo_retention_ratio_factor"]
    tech_eo_eec_ilf = variables["tech_eo_eec_ilf"]
    tech_eo_agg_ilf_primary_factor = variables["tech_eo_agg_ilf_primary_factor"]

    stop_gap_additional_coverage_value = variables["stop_gap_additional_coverage_value"]
    tria_additional_coverage_value = variables["tria_additional_coverage_value"]
    punitive_damages_additional_coverage_value = variables["punitive_damages_additional_coverage_value"] 
    
    retro_table = variables["retro_table"]
    default_excess_retro_date = variables["default_excess_retro_date"]

    options = pd.DataFrame(options_dict) 
    timer.start("section 1")
    ###
    #----------------------------------------------------------------------------------------------#
    # Policy Agg/Weighted Sum Individual Agg Ratio
    #----------------------------------------------------------------------------------------------#
    #options = utils.pd_df_from_hx_list(cds.options)
    
    agg_limits = options.loc[:, agg_limit_cols(hxd, "gmm")]

    agg_limits["sum_of_individual_aggs"] = agg_limits.sum(axis=1)  
    
    # We need each coverage base premium to calculate coverage weight
    pl_base_premium = base_premium * non_option_coverages.loc[0,["additional_coverage"]].iloc[0] * non_option_coverages.loc[0,["retro_factor"]].iloc[0] * size_discount_factor * venue_factor * policy_term     
    gl_base_premium = base_premium * non_option_coverages.loc[1,["additional_coverage"]].iloc[0] * non_option_coverages.loc[1,["retro_factor"]].iloc[0] * size_discount_factor * venue_factor * policy_term 
    prodl_base_premium = base_premium * non_option_coverages.loc[2,["additional_coverage"]].iloc[0] * non_option_coverages.loc[2,["retro_factor"]].iloc[0] * size_discount_factor * venue_factor * policy_term 
    eo_base_premium = base_premium * non_option_coverages.loc[3,["additional_coverage"]].iloc[0] * non_option_coverages.loc[3,["retro_factor"]].iloc[0] * size_discount_factor * venue_factor * policy_term 
    ebl_base_premium = base_premium * non_option_coverages.loc[5,["additional_coverage"]].iloc[0] * non_option_coverages.loc[5,["retro_factor"]].iloc[0] * size_discount_factor * venue_factor * policy_term 
    el_base_premium = base_premium * non_option_coverages.loc[6,["additional_coverage"]].iloc[0] * non_option_coverages.loc[6,["retro_factor"]].iloc[0] * size_discount_factor * venue_factor * policy_term 
    techEO_base_premium = tech_eo_base_net_prem_usd.loc[0,["tech_eo_base_net_prem_usd"]].iloc[0] 
    
    # Calculate coverage weight
    pl_include_primary = non_option_coverages.loc[0,["include_primary"]].iloc[0] 

    gl_coverage_weight = np.where(pl_include_primary == True, 
                                  non_option_coverages[non_option_coverages["coverage"] == "general_liability"]["additional_coverage"].iloc[0], 
                                  gl_base_premium/techEO_base_premium)  
    
    prodl_coverage_weight = np.where(pl_include_primary == True, 
                                  non_option_coverages[non_option_coverages["coverage"] == "product_liability"]["additional_coverage"].iloc[0],
                                  prodl_base_premium/techEO_base_premium)  

    eo_coverage_weight = np.where(pl_include_primary == True, 
                                  non_option_coverages[non_option_coverages["coverage"] == "eo"]["additional_coverage"].iloc[0],
                                  eo_base_premium/techEO_base_premium) 

    ebl_coverage_weight = np.where(pl_include_primary == True, 
                                   non_option_coverages[non_option_coverages["coverage"] == "employee_benefits_liability"]["additional_coverage"].iloc[0],
                                   ebl_base_premium/techEO_base_premium)
    
    el_coverage_weight = np.where(pl_include_primary == True, 
                                   non_option_coverages[non_option_coverages["coverage"] == "employers_liability"]["additional_coverage"].iloc[0],
                                   el_base_premium/techEO_base_premium)    

    # Add on coverage weight into main table    
    non_option_coverages["additional_coverage"] = np.where(non_option_coverages["coverage"] == "general_liability", \
                                                           gl_coverage_weight, \
                                                           non_option_coverages["additional_coverage"])
        
    non_option_coverages["additional_coverage"] = np.where(non_option_coverages["coverage"] == "product_liability", \
                                                           prodl_coverage_weight, \
                                                           non_option_coverages["additional_coverage"])
                                
    non_option_coverages["additional_coverage"] = np.where(non_option_coverages["coverage"] == "eo", \
                                                           eo_coverage_weight, \
                                                           non_option_coverages["additional_coverage"])
            
    non_option_coverages["additional_coverage"] = np.where(non_option_coverages["coverage"] == "employee_benefits_liability", \
                                                           ebl_coverage_weight, \
                                                           non_option_coverages["additional_coverage"])        
         
    non_option_coverages["additional_coverage"] = np.where(non_option_coverages["coverage"] == "employers_liability", \
                                                           el_coverage_weight, \
                                                           non_option_coverages["additional_coverage"])        
    
    #The Tech EO coverage weight is recacluated at the Tech EO rating section
    non_option_coverages["coverage_weight"] = non_option_coverages["include_primary"] * non_option_coverages["additional_coverage"]
     
    for coverage in ["professional_liability","general_liability","product_liability","eo","employee_benefits_liability","employers_liability","tech_eo_products_media"]:
        additional_coverage_factor = non_option_coverages[non_option_coverages["coverage"] == coverage]["coverage_weight"].iloc[0]
        agg_limits[f"weighted_agg_{coverage}"] = agg_limits[f"coverages.{coverage}.aggregate_limit"] * additional_coverage_factor                                                                             
        agg_limits[f"contribution_to_sum_of_aggs_{coverage}"] = agg_limits[f"coverages.{coverage}.aggregate_limit"] / agg_limits["sum_of_individual_aggs"]
    
    weighted_agg_limits = agg_limits.loc[:,["weighted_agg_professional_liability",\
        "weighted_agg_general_liability",\
        "weighted_agg_product_liability",\
        "weighted_agg_eo",\
        "weighted_agg_employee_benefits_liability",\
        "weighted_agg_employers_liability",\
        "weighted_agg_tech_eo_products_media"]]

    policy_aggregate = options.loc[:,["agg_limit"]]
    policy_aggregate["weighted_sum_ind_aggs"] = weighted_agg_limits.sum(axis=1)

    policy_aggregate["policy_agg.weighted_sum"] = policy_aggregate["agg_limit"] / policy_aggregate["weighted_sum_ind_aggs"]
    policy_aggregate["policy_agg.weighted_sum"] = policy_aggregate["policy_agg.weighted_sum"].fillna(0)

    # Validations for agg limit
    limit_validation = options.loc[:,["agg_limit"]].fillna(0)
    if limit_validation["agg_limit"].sum()== 0:
        hx.errors.validation("No policy aggregate limit has been entered")

    #Overall policy agg factor
    agg_to_sum_of_aggs_table = hx.params.table_gmm_policy_agg 
    ratio_pol_agg_to_sum_individual =  agg_to_sum_of_aggs_table["ratio_pol_agg_to_sum_individual"].to_numpy()
    ratio_pol_agg_to_sum_individual_factor =  agg_to_sum_of_aggs_table["factor"].to_numpy()

    policy_aggregate["overall_policy_agg_factor"] = np.minimum(1 ,np.where((policy_aggregate["policy_agg.weighted_sum"]>1) | (policy_aggregate["agg_limit"].isna()),\
        1, np.interp(policy_aggregate["policy_agg.weighted_sum"], ratio_pol_agg_to_sum_individual, ratio_pol_agg_to_sum_individual_factor)))

    
    # Contribution to individual agg
    contribution_to_sum_of_aggs = agg_limits.loc[:,["contribution_to_sum_of_aggs_professional_liability",\
        "contribution_to_sum_of_aggs_general_liability",\
        "contribution_to_sum_of_aggs_product_liability",\
        "contribution_to_sum_of_aggs_eo",\
        "contribution_to_sum_of_aggs_employee_benefits_liability",\
        "contribution_to_sum_of_aggs_employers_liability",\
        "contribution_to_sum_of_aggs_tech_eo_products_media"]]

    contribution_to_sum_of_aggs = pd.concat([contribution_to_sum_of_aggs, policy_aggregate["overall_policy_agg_factor"]], axis=1)    

    for coverage in ["professional_liability","general_liability","product_liability","eo","employee_benefits_liability","employers_liability","tech_eo_products_media"]:
        contribution_to_sum_of_aggs[f"split_of_discount_{coverage}"] = 1 - ((1-policy_aggregate["overall_policy_agg_factor"])* contribution_to_sum_of_aggs[f"contribution_to_sum_of_aggs_{coverage}"])

    split_of_discount = contribution_to_sum_of_aggs.loc[:,["split_of_discount_professional_liability",\
        "split_of_discount_general_liability",\
        "split_of_discount_product_liability",\
        "split_of_discount_eo",\
        "split_of_discount_employee_benefits_liability",\
        "split_of_discount_employers_liability",\
        "split_of_discount_tech_eo_products_media"]] 

         
    timer.end("section 1") 
    timer.start("section 2")

    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary Premium Calculations Begin Here
    #--------------------------------------------------------------------------------------------------------------------------------#

    #Deductible parameters
    options_indemnity_only_dedctible = options.loc[:,["indemnity_only"]]
    indemnity_only_deductible_factor = hx.params.table_gmm_indemnity_ded_split["indemnity_defence_split"].iloc[0]
    deductible_credits = hx.params.table_gmm_deductible_credits
    deductible_size = deductible_credits["deductible"].to_numpy()
    deductible_factor = deductible_credits["factor"].to_numpy()
    
    #EEC ILF parameters
    ilf_table = hx.params.table_gmm_ilfs
    ilf_lev = ilf_table["lev"].to_numpy()
    ilf_factor = ilf_table["ilf"].to_numpy()

    #AGG ILF parameters
    agg_to_eec_table = hx.params.table_gmm_agg_to_eec
    agg_eec_ratio = agg_to_eec_table["agg_eec"].to_numpy()
    agg_eec_factor = agg_to_eec_table["factor"].to_numpy()

    basic_limit_pl = hx.params.table_gmm_base_limit_pl["basic_limit_pl"].iloc[0]

    

    timer.end("section 2") 
    timer.start("section 3")

    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary Premium: Professional liability calculated first - outside loop as we need it explicitly later on 
    #--------------------------------------------------------------------------------------------------------------------------------#
    total_primary_layer_per_coverage = pd.DataFrame()
    total_base_primary_layer_per_coverage = pd.DataFrame()
    
    # Professional Liability 
    pl_additional_coverage_factor = non_option_coverages[non_option_coverages["coverage"] == "professional_liability"]["additional_coverage"].iloc[0]
    pl_retro_factor = non_option_coverages[non_option_coverages["coverage"] == "professional_liability"]["retro_factor"].iloc[0]
    pl_table = options.loc[:,["coverages.professional_liability.retention","coverages.professional_liability.per_claim_limit","coverages.professional_liability.aggregate_limit"]]
    pl_table["converted_retention"] = pl_table["coverages.professional_liability.retention"] * currency_factor
    pl_table["converted_per_claim_limit"] = pl_table["coverages.professional_liability.per_claim_limit"] * currency_factor

    pl_table["base_premium"] = base_premium * pl_additional_coverage_factor * size_discount_factor * venue_factor * policy_term * pl_retro_factor

    pl_table["deductible_factor"] = np.where(options["indemnity_only"] == True,\
        np.interp(pl_table["converted_retention"], deductible_size, deductible_factor) * (1-indemnity_only_deductible_factor) + np.interp(0, deductible_size, deductible_factor) * indemnity_only_deductible_factor  ,\
            np.interp(pl_table["converted_retention"], deductible_size, deductible_factor))        

    pl_table["eel_ilf"] = np.interp(pl_table["converted_per_claim_limit"], ilf_lev, ilf_factor) / np.interp(basic_limit_pl, ilf_lev, ilf_factor)

    pl_table["agg_to_eec_ratio"] = pl_table["coverages.professional_liability.aggregate_limit"] / pl_table["coverages.professional_liability.per_claim_limit"] 
    pl_table["agg_ilf"] = np.interp(pl_table["agg_to_eec_ratio"], agg_eec_ratio, agg_eec_factor)
    pl_policy_agg_factor = pd.concat([split_of_discount["split_of_discount_professional_liability"], policy_aggregate["policy_agg.weighted_sum"], policy_aggregate["agg_limit"]],axis=1)         
    policy_aggregate["policy_agg_factor"] = np.minimum(1 ,np.where((pl_policy_agg_factor["policy_agg.weighted_sum"]>1) | (pl_policy_agg_factor["agg_limit"].isna()),\
        1, pl_policy_agg_factor["split_of_discount_professional_liability"]))

    pl_table = pd.concat([pl_table, policy_aggregate["policy_agg_factor"]], axis=1)

    pl_primary_layer = pl_table.loc[:,["base_premium","deductible_factor","eel_ilf","agg_ilf","policy_agg_factor"]]
    pl_primary_layer["primary_layer_net_premium"] = pl_primary_layer.prod(axis=1)

    total_primary_layer_per_coverage["primary_layer_net_premium_professional_liability_usd"] = pl_include_primary * pl_primary_layer["primary_layer_net_premium"] * total_schedule_mod_factor 
    total_base_primary_layer_per_coverage["primary_layer_base_premium_professional_liability_usd"] = pl_include_primary * pl_table["base_premium"] / pl_retro_factor


    timer.end("section 3") 
    timer.start("section 4")

    if pl_include_primary == False and cds.exposure.granular.gmm_product.product != "Virtual Care" :
        hx.errors.validation("Please check Professional Liability is selected for Primary")


    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary Premium: For the rest of the coverages, we can calculate these in a loop - EXCLUDING TECH E&O
    #--------------------------------------------------------------------------------------------------------------------------------#
    
    # Excluding Tech E&O
    for coverage in ["general_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability"]:

        include_in_primary_calc = non_option_coverages[non_option_coverages["coverage"] == coverage]["include_primary"].iloc[0] 

        if include_in_primary_calc == True :
            additional_coverage_factor = non_option_coverages[non_option_coverages["coverage"] == coverage]["additional_coverage"].iloc[0]
            retro_factor = non_option_coverages[non_option_coverages["coverage"] == coverage]["retro_factor"].iloc[0]
            options_coverage = options.loc[:,[f"coverages.{coverage}.retention",f"coverages.{coverage}.per_claim_limit",f"coverages.{coverage}.aggregate_limit"]]
            options_coverage["converted_retention"] = options_coverage[f"coverages.{coverage}.retention"] * currency_factor

            options_coverage["converted_per_claim_limit"] = options_coverage[f"coverages.{coverage}.per_claim_limit"] * currency_factor

            options_coverage["base_premium"] = np.where(options_coverage[f"coverages.{coverage}.per_claim_limit"].isna(),0 , base_premium * additional_coverage_factor * size_discount_factor * venue_factor * policy_term * retro_factor)

            options_coverage = pd.concat([options_coverage,options_indemnity_only_dedctible],axis=1)
            
            options_coverage["deductible_factor"] = np.where(options_coverage["indemnity_only"] == True,\
                np.interp(options_coverage["converted_retention"], deductible_size, deductible_factor) * (1-indemnity_only_deductible_factor) + np.interp(0, deductible_size, deductible_factor) * indemnity_only_deductible_factor  ,\
                    np.interp(options_coverage["converted_retention"], deductible_size, deductible_factor))

            options_coverage["eel_ilf"] = np.interp(options_coverage["converted_per_claim_limit"], ilf_lev, ilf_factor) / np.interp(basic_limit_pl, ilf_lev, ilf_factor)

            options_coverage["agg_to_eec_ratio"] = options_coverage[f"coverages.{coverage}.aggregate_limit"] / options_coverage[f"coverages.{coverage}.per_claim_limit"] 
            options_coverage["agg_ilf"] = np.interp(options_coverage["agg_to_eec_ratio"], agg_eec_ratio, agg_eec_factor)


            if coverage == "sexual_abuse":
                    policy_aggregate["policy_agg_factor"] = 1
            else:
                policy_agg_factor = pd.concat([split_of_discount[f"split_of_discount_{coverage}"], policy_aggregate["policy_agg.weighted_sum"], policy_aggregate["agg_limit"]],axis=1)         
                policy_aggregate["policy_agg_factor"] = np.minimum(1 ,np.where((policy_agg_factor["policy_agg.weighted_sum"]>1) | (policy_agg_factor["agg_limit"].isna()),\
                    1, policy_agg_factor[f"split_of_discount_{coverage}"]))


            options_coverage = pd.concat([options_coverage, policy_aggregate["policy_agg_factor"]], axis=1)

            primary_layer_per_coverage = options_coverage.loc[:,["base_premium","deductible_factor","eel_ilf","agg_ilf","policy_agg_factor"]]
            primary_layer_per_coverage["primary_layer_net_premium"] = primary_layer_per_coverage.prod(axis=1)

            total_primary_layer_per_coverage[f"primary_layer_net_premium_{coverage}_usd"] = primary_layer_per_coverage["primary_layer_net_premium"] * total_schedule_mod_factor
            total_base_primary_layer_per_coverage[f"primary_layer_base_premium_{coverage}_usd"] = options_coverage["base_premium"] / retro_factor
        
    total_primary_layer_per_coverage["primary_premium_exc_tech_eo_usd"] = total_primary_layer_per_coverage.sum(axis=1)         
    total_base_primary_layer_per_coverage["base_primary_premium_usd"] = total_base_primary_layer_per_coverage.sum(axis=1)        

    # Tech E&O        
    total_primary_layer_per_coverage["primary_premium_tech_eo_usd"] = tech_eo_primary_net_prem_usd["tech_eo_primary_net_prem_usd"] * split_of_discount["split_of_discount_tech_eo_products_media"]        
    total_base_primary_layer_per_coverage["primary_layer_base_premium_tech_eo_usd"] = tech_eo_base_net_prem_usd["tech_eo_base_net_prem_raw_usd"]

    # Total premium

    total_primary_layer_per_coverage["total_primary_premium_usd"] = total_primary_layer_per_coverage["primary_premium_exc_tech_eo_usd"] + total_primary_layer_per_coverage["primary_premium_tech_eo_usd"].fillna(0)
    total_base_primary_layer_per_coverage["total_primary_layer_base_premium_usd"] = total_base_primary_layer_per_coverage["base_primary_premium_usd"] + tech_eo_base_net_prem_usd["tech_eo_base_net_prem_raw_usd"]   


    timer.end("section 4") 
    timer.start("section 5")

    # GL Premium for Umbrella
    if cds.rating_factors.pricing.general_liability.include_primary == True:
        gl_primary_premium = total_primary_layer_per_coverage["primary_layer_net_premium_general_liability_usd"] / currency_factor
        gl_primary_premium = gl_primary_premium.fillna(0)
        if cds.rating_factors.pricing.general_liability.claims_basis == "Occurrence" and cds.rating_factors.pricing.general_liability.include_excess == True and cds.rating_factors.gmm.umbrella.general_liability.occurrence_cover == True:
            for index, option in enumerate(cds.options):
                setattr(getattr(option, "gmm_general_liability"),"premium_primary", gl_primary_premium[index])
        else: 
            for index, option in enumerate(cds.options):
                setattr(getattr(option, "gmm_general_liability"),"premium_primary", 0)
    else: 
            for index, option in enumerate(cds.options):
                setattr(getattr(option, "gmm_general_liability"),"premium_primary", 0)
    #----------------------------------------------------------------------------------------------#
    # Primary Premium: TECH E&O 
    #----------------------------------------------------------------------------------------------#        
    

    
    
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary Premium: Coverage Enhancments - note we have a "base" for each one, which is calculated on the base premium rather than the at limits premium. This is used for the excess layer pricing. 
    #--------------------------------------------------------------------------------------------------------------------------------#
    total_primary_layer_enhancements = pd.DataFrame()

    #Stop Gap
    stop_gap = options["include_stop_gap_primary"] * total_primary_layer_per_coverage["primary_premium_exc_tech_eo_usd"] * stop_gap_additional_coverage_value
    total_base_primary_layer_per_coverage["stop_gap_base"] = total_base_primary_layer_per_coverage["base_primary_premium_usd"] * stop_gap_additional_coverage_value
    total_primary_layer_enhancements["stop_gap_premium"] = np.where(stop_gap.isna() ,0 ,stop_gap)

    #TRIA
    tria_min = hx.params.table_gmm_tria_min["tria_min_prem"].iloc[0]
    tria = np.maximum(tria_min * options["include_tria_primary"], options["include_tria_primary"] * total_primary_layer_per_coverage["primary_premium_exc_tech_eo_usd"] * tria_additional_coverage_value)
    total_base_primary_layer_per_coverage["tria_base"] = np.maximum(tria_min, total_base_primary_layer_per_coverage["base_primary_premium_usd"]  * tria_additional_coverage_value)
    total_primary_layer_enhancements["tria_premium"] = np.where(tria.isna() ,0 ,tria)

    #Punitive Damages
    punitive_damages =  options["include_punitive_damages_primary"] * total_primary_layer_per_coverage["primary_premium_exc_tech_eo_usd"] * punitive_damages_additional_coverage_value
    punitive_damages_base = total_base_primary_layer_per_coverage["base_primary_premium_usd"] * punitive_damages_additional_coverage_value
    total_primary_layer_enhancements["punitive_damages_premium"] = np.where(punitive_damages.isna() ,0 ,punitive_damages)

    #Costs in Addition        
    costs_in_addition_table = hx.params.table_gmm_costs_in_addition
    costs_in_addition_selection = pd.DataFrame(options["costs_in_addition_selection"])
    costs_in_addition_primary = costs_in_addition_selection.merge(costs_in_addition_table, left_on = "costs_in_addition_selection", right_on = "costs_in_addition", how="left")
    
    costs_in_addition = options["include_costs_in_addition_primary"] * costs_in_addition_primary["debit"] * (total_primary_layer_per_coverage["primary_premium_exc_tech_eo_usd"] + total_primary_layer_per_coverage["primary_premium_tech_eo_usd"].fillna(0))
    total_base_primary_layer_per_coverage["costs_in_addition_base"] = costs_in_addition_primary["debit"] * total_base_primary_layer_per_coverage["base_primary_premium_usd"]
    total_primary_layer_enhancements["costs_in_addition_premium"] = np.where(costs_in_addition.isna() ,0 ,costs_in_addition)

    #Auto HNOA
    auto_hnoa_base_rate = hx.params.table_gmm_auto_hnoa_base_rate["auto_base_prem"].iloc[0]
    auto_selection = options.loc[:,["include_auto_primary","auto_measure","auto_amount"]]
    auto_selection["auto_amount"] = np.where(auto_selection["auto_amount"].isna(), 0, auto_selection["auto_amount"])

    auto_hnoa = np.where(auto_selection["auto_measure"] == "Mileage", auto_selection["auto_amount"]/10000, auto_selection["auto_amount"]) * auto_hnoa_base_rate * auto_selection["include_auto_primary"]
    total_base_primary_layer_per_coverage["auto_hnoa_base"] = np.where(auto_selection["auto_measure"] == "Mileage", auto_selection["auto_amount"]/10000, auto_selection["auto_amount"]) * auto_hnoa_base_rate
    total_primary_layer_enhancements["auto_premium"] = np.where(auto_hnoa.isna() ,0 ,auto_hnoa)

    #Sum up the total enhancments - gives the total primary premium layer
    total_primary_layer_premium = pd.DataFrame()
    total_primary_layer_premium["net_model_premium"] = total_primary_layer_per_coverage["total_primary_premium_usd"] \
        + total_primary_layer_enhancements["stop_gap_premium"] \
        + total_primary_layer_enhancements["tria_premium"] \
        + total_primary_layer_enhancements["punitive_damages_premium"] \
        + total_primary_layer_enhancements["costs_in_addition_premium"] \
        + total_primary_layer_enhancements["auto_premium"]
        
    
    timer.end("section 5") 
    timer.start("section 6")

    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary Premium: Minimum Premium Calculations
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Get tech EO parameters
    tech_eo_deductible_factor = tech_eo_retention_ratio_factor.loc[0,["tech_eo_retention_ratio_factor"]].iloc[0]
    tech_eo_eec_ilf = tech_eo_eec_ilf.loc[0,["tech_eo_eec_ilf"]].iloc[0]
    tech_eo_agg_ilf_primary_factor = tech_eo_agg_ilf_primary_factor.loc[0,["tech_eo_agg_ilf_primary_factor"]].iloc[0]
    
    # Minimum premium params
    minimum_premium_parameter_table = pl_table.loc[:,["deductible_factor","eel_ilf","agg_ilf"]]
    minimum_premium_parameter_table["deductible_factor"] = np.where(pl_include_primary == False, tech_eo_deductible_factor, minimum_premium_parameter_table["deductible_factor"])
    minimum_premium_parameter_table["eel_ilf"] = np.where(pl_include_primary == False, tech_eo_eec_ilf, minimum_premium_parameter_table["eel_ilf"])
    minimum_premium_parameter_table["agg_ilf"] = np.where(pl_include_primary == False, tech_eo_agg_ilf_primary_factor, minimum_premium_parameter_table["agg_ilf"])
    minimum_premim_options = minimum_premium_parameter_table.loc[:,["deductible_factor","eel_ilf","agg_ilf"]]
    minimum_premim_options["deductible_factor"] = np.maximum(1,minimum_premim_options["deductible_factor"])
    # minimum_premim_options = minimum_premim_options/currency_factor

    # Brokerage
    brokerage = options.loc[:,"brokerage_primary"].fillna(0) 

    spain_choice_of_law = cds.rating_factors.us_international_choice_of_law.choice_of_law == "Spain"
    # Need to add in brokerage here #DK added brokerage.. .only applies to Spain
    if spain_choice_of_law:
        spain_codes_minimum = hx.params.table_gmm_spanish_minimum_cob
        trimmed_cob = cds.exposure.granular.gmm_product.cob_code_description[:2] if cds.exposure.granular.gmm_product.cob_code_description else "DA"
        trimmed_cob_valid = spain_codes_minimum["code"].str.contains(trimmed_cob).any()

        if trimmed_cob_valid:
            spain_class_minimum = hx.params.table_gmm_spain_class
            spain_class_name = spain_class_minimum["spain_class"].iloc[0]
            product_class = cds.exposure.granular.gmm_product.cob_class

            if product_class == spain_class_name : 
                minimum_premim_options["minimum_premium_primary"] = spain_class_minimum["minimum"].iloc[0] / (1- brokerage)
            else:
                minimum_premim_options["minimum_premium_primary"] = spain_codes_minimum[spain_codes_minimum["code"] == trimmed_cob]["minimum"].iloc[0]
        else:
            minimum_premium_table = hx.params.table_gmm_minimum_premium
            trimmed_cob = cds.exposure.granular.gmm_product.cob_code_description[:2] if cds.exposure.granular.gmm_product.cob_code_description else None
            filtered_minimum_premium_table = minimum_premium_table[(minimum_premium_table["product"] == variables["product"]) & (minimum_premium_table["us_international"] == us_international) & (minimum_premium_table["cob_class"] == gmm_class) & (minimum_premium_table["cob_code"] == trimmed_cob)] if trimmed_cob else pd.DataFrame()
            if filtered_minimum_premium_table.shape[0]:
                minimum_prem_pre_adjustment = filtered_minimum_premium_table["minimum_premium"].iloc[0]
            else:
                minimum_prem_pre_adjustment = 0 
            minimum_premim_options["minimum_premium_primary"] = minimum_premim_options.prod(axis=1) * minimum_prem_pre_adjustment / currency_factor
    
    else:
        minimum_premium_table = hx.params.table_gmm_minimum_premium
        trimmed_cob = cds.exposure.granular.gmm_product.cob_code_description[:2] if cds.exposure.granular.gmm_product.cob_code_description else None
        filtered_minimum_premium_table = minimum_premium_table[(minimum_premium_table["product"] == variables["product"]) & (minimum_premium_table["us_international"] == us_international) & (minimum_premium_table["cob_class"] == gmm_class) & (minimum_premium_table["cob_code"] == trimmed_cob)] if trimmed_cob else pd.DataFrame()
        if filtered_minimum_premium_table.shape[0]:
            minimum_prem_pre_adjustment = filtered_minimum_premium_table["minimum_premium"].iloc[0]
        else:
            minimum_prem_pre_adjustment = 0 
        minimum_premim_options["minimum_premium_primary"] = minimum_premim_options.prod(axis=1) * minimum_prem_pre_adjustment / currency_factor

    # Concat on the pol_aggregate table to ensure that we only write to the node if there is a pol agg limit entered
    minimum_premim_options = pd.concat([minimum_premim_options, policy_aggregate["agg_limit"]], axis=1)
    minimum_premim_options["minimum_premium_primary"] = np.where(minimum_premim_options["agg_limit"] == 0 , 0 , minimum_premim_options["minimum_premium_primary"])
    utils.write_pd_to_hxd(minimum_premim_options,cds.options,["minimum_premium_primary"])

    
    timer.end("section 6") 
    timer.start("section 7")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary Gross Premium: Total Calculations
    #--------------------------------------------------------------------------------------------------------------------------------#          

 

    ###################
    # IR edit 22/12 ---

    # Pull in technical premium parameters from user library 
    tp_params = params.tp_parameters.df()

    # To stop the model erroring if the inception year defaults to a year not in the TP data
    yoa = hxd.hx_core.inception_date.year
    tp_year = yoa if yoa in tp_params["year"].values else tp_params["year"].max()

    # ML edit 07/09/26 ---
    # Business parameters --------       
    # Pull the right business class parameters
    if (us_international == "International"):
        if (tp_year <= 2025):
            bp_class = "Intl Misc Med (London)"
        else:
            bp_class = "Intl Misc Med & Life Sciences"
    else:
        bp_class = "US Misc Med"  
    # End of ML edit ---  

    tp_lookup_bool = (tp_params['business_plan_class'] == bp_class) & (tp_params['year'] == tp_year)
    tp_params_df = tp_params[tp_lookup_bool]

    # end of IR edit 22/12 ---
    #############
    
    # nmp_load
    nmp_load = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['nmp_load'].iloc[0]            

    total_gross_model_premium = pd.DataFrame()
    total_gross_model_premium["model_premium_primary"] = ((total_primary_layer_premium["net_model_premium"] / currency_factor) / (1-brokerage)) * (1 + nmp_load)

    #Include Cyber here
    if cyber_selection:
        total_gross_model_premium["model_premium_primary"]  = total_gross_model_premium["model_premium_primary"].fillna(0) + options["cyber_premium_primary"] * (1 + nmp_load)
        total_gross_model_premium["uplift_for_nmp_primary"] = total_gross_model_premium["model_premium_primary"] - options["cyber_premium_primary"] - ((total_primary_layer_premium["net_model_premium"] / currency_factor) / (1-brokerage))
    else:
       total_gross_model_premium["uplift_for_nmp_primary"] = total_gross_model_premium["model_premium_primary"] - ((total_primary_layer_premium["net_model_premium"] / currency_factor) / (1-brokerage))     

    # Concat on the pol_aggregate table to ensure that we only write to the node if there is a pol agg limit entered
    total_gross_model_premium = pd.concat([total_gross_model_premium, policy_aggregate["agg_limit"]], axis=1)
    total_gross_model_premium["model_premium_primary"] = np.where(total_gross_model_premium["agg_limit"] == 0 , 0 , total_gross_model_premium["model_premium_primary"])
    total_gross_model_premium["uplift_for_nmp_primary"] = np.where(total_gross_model_premium["agg_limit"] == 0 , 0 , total_gross_model_premium["uplift_for_nmp_primary"])

    if not total_gross_model_premium.empty:
        utils.write_pd_to_hxd(total_gross_model_premium,cds.options,["model_premium_primary","uplift_for_nmp_primary"])

    # Gross premium
    total_gross_model_premium["gross_premium_primary"] = np.maximum(total_gross_model_premium["model_premium_primary"], minimum_premim_options["minimum_premium_primary"])

    # write to cds        
    utils.write_pd_to_hxd(total_gross_model_premium,cds.options,["gross_premium_primary"])

    # Calculating benchmark premium and BPIs    
    priced_to_net_loss_ratio = hx.params.table_gmm_priced_to_net_lr.loc[:,"loss_ratio"].iloc[0]
    benchmark_loss_ratio = hx.params.table_benchmark_lr.loc[:,"loss_ratio"].iloc[0]

    # Total benchmark premium
    primary_benchmark_premium = total_gross_model_premium["gross_premium_primary"] * (priced_to_net_loss_ratio / benchmark_loss_ratio)

    primary_quoted_premium = options.loc[:,"quoted_premium_primary"]
    primary_quoted_premium = np.where(primary_quoted_premium.isna(), 0 , primary_quoted_premium)
    
    # try:
    
    total_gross_model_premium["bpi_primary"] = [q / b if b != 0 else 0 for q, b in zip(primary_quoted_premium, primary_benchmark_premium)] 
    total_gross_model_premium["bpi_primary"] = total_gross_model_premium["bpi_primary"].fillna(0)
    # except:
        # total_gross_model_premium["bpi_primary"] = [0] * len(options)

    utils.write_pd_to_hxd(total_gross_model_premium,cds.options,["bpi_primary"])

    
    timer.end("section 7") 
    timer.start("section 8")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Excess Layer Pricing 
    #--------------------------------------------------------------------------------------------------------------------------------#  
    for layer in range(1,11):
        setattr(cds.rating_factors.pricing, f"claims_basis_{layer}_excess", "Claims-Made")
        setattr(getattr(cds.rating_factors.pricing, f"retroactive_date_{layer}_excess"), "calculated", default_excess_retro_date)
    
    base_premiums_per_coverage = total_base_primary_layer_per_coverage.drop(columns=["base_primary_premium_usd"])

    excess_agg_to_eec = hx.params.table_gmm_excess_agg_to_eel
    excess_agg_eec_ratio = excess_agg_to_eec["agg_to_eel_ratio"].to_numpy()
    excess_agg_eec_factor = excess_agg_to_eec["factor"].to_numpy()

    coverages = ["professional_liability","general_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability","tech_eo_products_media"]
    include_excess = [getattr(getattr(cds.rating_factors.pricing , coverage),"include_excess") for coverage in coverages]
    # for coverage in ["professional_liability","general_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability","tech_eo_products_media"]:
    #     include_excess_value = getattr(getattr(cds.rating_factors.pricing , coverage),"include_excess")
    #     include_excess.append(include_excess_value)
            
    coverages_2 = ["stop_gap","tria","punitive_damages","costs_in_addition","auto"]
    include_excess_2 = [getattr(cds.rating_factors.pricing , f"include_{coverage}_excess") for coverage in coverages_2]

    include_excess = include_excess + include_excess_2
    
    excess_coverages = pd.DataFrame({"coverage": coverages + coverages_2, "include_excess": include_excess}) 
        

    # SA: list comprehensions are great
    excess_layers = ["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"]
    excess_retro_date = [getattr(getattr(cds.rating_factors.pricing , f"retroactive_date_{layer}"),"selected") for layer in excess_layers]
    excess_retro_years = [int(utils.policy_term(excess_retroactive_date, inception_date)) if excess_retroactive_date and utils.policy_term(excess_retroactive_date, inception_date) - int(utils.policy_term(excess_retroactive_date, inception_date)) < 0.01 else math.ceil(utils.policy_term(excess_retroactive_date, inception_date)) if excess_retroactive_date else None for excess_retroactive_date in excess_retro_date]
    # excess_retro_years = [math.ceil(utils.policy_term(excess_retroactive_date, inception_date)) if excess_retroactive_date else None for excess_retroactive_date in excess_retro_date]
    excess_retro_factor = [retro_table[retro_table["retro_years"] == excess_retroactive_years]["factor"].iloc[0] if not retro_table[retro_table["retro_years"] == excess_retroactive_years].empty else 1 for excess_retroactive_years in excess_retro_years]

    excess_layer_non_option = pd.DataFrame({"layer": excess_layers, "excess_retroactive_date": excess_retro_date, "excess_retroactive_years": excess_retro_years, "excess_retroactive_factor": excess_retro_factor})

    
    # Looping through all the layers to get the attachment, dettachment points and calculate the agg ILF for each point

    layers_table = options.loc[:,["coverages.professional_liability.per_claim_limit","coverages.professional_liability.retention",\
        "coverages.tech_eo_products_media.per_claim_limit","coverages.tech_eo_products_media.retention",\
        "per_claim_limit_1_excess","aggregate_limit_1_excess",\
        "per_claim_limit_2_excess","aggregate_limit_2_excess",\
        "per_claim_limit_3_excess","aggregate_limit_3_excess",\
        "per_claim_limit_4_excess","aggregate_limit_4_excess",\
        "per_claim_limit_5_excess","aggregate_limit_5_excess",\
        "per_claim_limit_6_excess","aggregate_limit_6_excess",\
        "per_claim_limit_7_excess","aggregate_limit_7_excess",\
        "per_claim_limit_8_excess","aggregate_limit_8_excess",\
        "per_claim_limit_9_excess","aggregate_limit_9_excess",\
        "per_claim_limit_10_excess","aggregate_limit_10_excess"]]

    excess_table = pd.DataFrame()
    #excess_table["attachment_1_excess"] = layers_table["coverages.professional_liability.per_claim_limit"]
    excess_table["attachment_1_excess"] = np.where(pl_include_primary == True, layers_table["coverages.professional_liability.per_claim_limit"], layers_table["coverages.tech_eo_products_media.per_claim_limit"])
    #excess_table["primary_retention"] = layers_table["coverages.professional_liability.retention"]
    excess_table["primary_retention"] = np.where(pl_include_primary == True, layers_table["coverages.professional_liability.retention"], layers_table["coverages.tech_eo_products_media.retention"])
    excess_table["dettachment_1_excess"] = excess_table["attachment_1_excess"] + layers_table["per_claim_limit_1_excess"]
    excess_table["dettachment_plus_retention_1_excess"] = (excess_table["primary_retention"] + excess_table["dettachment_1_excess"]) * currency_factor
    excess_table["attachment_plus_retention_1_excess"] = (excess_table["primary_retention"] + excess_table["attachment_1_excess"]) * currency_factor
    excess_table["unlimited_ilf_1_excess"] = (np.interp(excess_table["dettachment_plus_retention_1_excess"], ilf_lev, ilf_factor) - np.interp(excess_table["attachment_plus_retention_1_excess"], ilf_lev, ilf_factor)) / np.interp(basic_limit_pl, ilf_lev, ilf_factor)
    excess_table["agg_to_eel_ratio_1_excess"] = layers_table["aggregate_limit_1_excess"] / layers_table["per_claim_limit_1_excess"]
    excess_table["agg_ecc_factor_1_excess"] = np.interp(excess_table["agg_to_eel_ratio_1_excess"] , excess_agg_eec_ratio, excess_agg_eec_factor)
    excess_table["cumulative_agg_ecc_factor_1_excess"] = pl_table["agg_ilf"] 
    # try:
    excess_table["ilf_agg_1_excess"] = (excess_table["agg_ecc_factor_1_excess"] / excess_table["cumulative_agg_ecc_factor_1_excess"]) * excess_table["unlimited_ilf_1_excess"]
    excess_table["ilf_agg_1_excess"] = excess_table["ilf_agg_1_excess"].fillna(0)
    # except:
    #     excess_table["ilf_agg_1_excess"] =  0

    for layer in range(2,11) :
        excess_table[f"attachment_{layer}_excess"] = excess_table[f"attachment_{layer-1}_excess"] + layers_table[f"per_claim_limit_{layer-1}_excess"]
        excess_table[f"dettachment_{layer}_excess"] = excess_table[f"attachment_{layer}_excess"] + layers_table[f"per_claim_limit_{layer}_excess"]

        excess_table[f"dettachment_plus_retention_{layer}_excess"] = (excess_table["primary_retention"] + excess_table[f"dettachment_{layer}_excess"]) * currency_factor
        excess_table[f"attachment_plus_retention_{layer}_excess"] = (excess_table["primary_retention"] + excess_table[f"attachment_{layer}_excess"]) * currency_factor        

        
        excess_table[f"unlimited_ilf_{layer}_excess"] = (np.interp(excess_table[f"dettachment_plus_retention_{layer}_excess"], ilf_lev, ilf_factor) - np.interp(excess_table[f"attachment_plus_retention_{layer}_excess"], ilf_lev, ilf_factor)) / np.interp(basic_limit_pl, ilf_lev, ilf_factor)

        excess_table[f"agg_to_eel_ratio_{layer}_excess"] = layers_table[f"aggregate_limit_{layer}_excess"] / layers_table[f"per_claim_limit_{layer}_excess"]
        excess_table[f"agg_ecc_factor_{layer}_excess"] = np.interp(excess_table[f"agg_to_eel_ratio_{layer}_excess"] , excess_agg_eec_ratio, excess_agg_eec_factor)
        excess_table[f"cumulative_agg_ecc_factor_{layer}_excess"] = excess_table[f"cumulative_agg_ecc_factor_{layer-1}_excess"] * excess_table[f"agg_ecc_factor_{layer-1}_excess"]

        # try:
        excess_table[f"ilf_agg_{layer}_excess"] = (excess_table[f"agg_ecc_factor_{layer}_excess"] / excess_table[f"cumulative_agg_ecc_factor_{layer}_excess"]) * excess_table[f"unlimited_ilf_{layer}_excess"]
        excess_table[f"ilf_agg_{layer}_excess"] = excess_table[f"ilf_agg_{layer}_excess"].fillna(0)
        # except:
        #     excess_table[f"ilf_agg_{layer}_excess"] =  0

    excess_ilfs = excess_table.loc[:,["ilf_agg_1_excess","ilf_agg_2_excess","ilf_agg_3_excess","ilf_agg_4_excess","ilf_agg_5_excess","ilf_agg_6_excess","ilf_agg_7_excess","ilf_agg_8_excess","ilf_agg_9_excess","ilf_agg_10_excess"]]  

    excess_premium = pd.DataFrame()
    
    #Exclude the Tech E&O as this will be created from Tech E&O rating function
    # timer.start("old idea")
    # for test in ["professional_liability","general_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability"]:
    #     include_coverage_excess = excess_coverages[excess_coverages["coverage"] == test]["include_excess"].iloc[0]  # SA: make sure things that aren't dependant on a loop item aren't in a loop!
    #     for layer in range (1,11) : 
    #         if include_coverage_excess:                    
    #             retro_excess = excess_layer_non_option[excess_layer_non_option["layer"] == f"{layer}_excess"]["excess_retroactive_factor"].iloc[0]
    #             primary_base_premium_usd = base_premiums_per_coverage[f"primary_layer_base_premium_{test}_usd"]
    #             excess_ilf_factor = excess_ilfs[f"ilf_agg_{layer}_excess"]
    #             excess_premium[f"premium_{layer}_excess_{test}_usd"] = primary_base_premium_usd * excess_ilf_factor * retro_excess * total_schedule_mod_factor                       
    #         else:
    #             excess_premium[f"premium_{layer}_excess_{test}_usd"] = 0
    # timer.end("old idea")

    # timer.start("new idea")
    # Validatation error to show if including in excess but not primary
    primary_include = non_option_coverages[["coverage","include_primary"]]
    merged_includes = primary_include.merge(excess_coverages,how='left')
    merged_includes["error_catch"] = np.where((merged_includes["include_excess"] == True) & (merged_includes["include_primary"] == False), True, False )
    if merged_includes["error_catch"].sum() > 0:
        hx.errors.validation("Coverages must be included in primary to be included in excess")

    # SA: slightly faster to do access these things from lists rather than dataframes
    coverage_indexes = excess_coverages["coverage"].to_list()
    excess_coverages_list = excess_coverages["include_excess"].to_list()
    primary_coverage_list = non_option_coverages["include_primary"].to_list()
    for test in ["professional_liability","eo","general_liability","product_liability","sexual_abuse","employee_benefits_liability","employers_liability"]:
    
        index = coverage_indexes.index(test)
        include_coverage_excess = excess_coverages_list[index]  # SA: make sure things that aren't dependant on a loop item aren't in a loop!
        include_coverage_primary = primary_coverage_list[index]
        for layer in range (1,11):
            if include_coverage_excess:
                if include_coverage_primary:
                    retro_excess = excess_layer_non_option[excess_layer_non_option["layer"] == f"{layer}_excess"]["excess_retroactive_factor"].iloc[0]
                    primary_base_premium_usd = base_premiums_per_coverage[f"primary_layer_base_premium_{test}_usd"]
                    excess_ilf_factor = excess_ilfs[f"ilf_agg_{layer}_excess"]
                    excess_premium[f"premium_{layer}_excess_{test}_usd"] = primary_base_premium_usd * excess_ilf_factor * retro_excess * total_schedule_mod_factor
                else:
                    excess_premium[f"premium_{layer}_excess_{test}_usd"] = [0] * len(cds.options)                    
            else:            
                excess_premium[f"premium_{layer}_excess_{test}_usd"] = [0] * len(cds.options) 
    
    # timer.end("new idea")
        
    # To check
    # base_premiums_per_coverage["primary_layer_base_premium_tech_eo_products_media_usd"]
    # excess_ilfs["ilf_agg_1_excess"]
    # excess_layer_non_option[excess_layer_non_option["layer"] == "2_excess"]["excess_retroactive_factor"].iloc[0]
    
    # Tech EO excess Layer
    include_coverage_excess = excess_coverages[excess_coverages["coverage"] == "tech_eo_products_media"]["include_excess"].iloc[0]
    for layer in range (1, 11):
        if include_coverage_excess:
            options_list = [getattr(item, f"tech_eo_net_premium_usd_{layer}_excess") for index, item in enumerate(cds.options)]
            # for index, item in enumerate(cds.options):
            #     tech_eo_excess_temp.append(getattr(item,f"tech_eo_net_premium_usd_{layer}_excess" ))
            retro_excess = excess_layer_non_option[excess_layer_non_option["layer"] == f"{layer}_excess"]["excess_retroactive_factor"].iloc[0]
            # tech_eo_excess_temp = [x * retro_excess * policy_term * total_schedule_mod_factor for x in options_list]
            excess_premium[f"premium_{layer}_excess_tech_eo_products_media_usd"] = [x * retro_excess * policy_term * total_schedule_mod_factor for x in options_list]
        else:
            # tech_eo_excess_temp = [0]*len(cds.options)                
            excess_premium[f"premium_{layer}_excess_tech_eo_products_media_usd"] = [0]*len(cds.options) 
    


    #Gross total premiums excluding enhancments
    excess_premium_totals_excl_enhancments = pd.DataFrame()
    for layer in range (1,11):
        excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_excess_usd"] = excess_premium[f"premium_{layer}_excess_professional_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_general_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_product_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_eo_usd"] + \
            excess_premium[f"premium_{layer}_excess_sexual_abuse_usd"] + \
            excess_premium[f"premium_{layer}_excess_employee_benefits_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_employers_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_tech_eo_products_media_usd"]

        excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_exc_tech_eo_excess_usd"] = excess_premium[f"premium_{layer}_excess_professional_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_general_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_product_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_eo_usd"] + \
            excess_premium[f"premium_{layer}_excess_sexual_abuse_usd"] + \
            excess_premium[f"premium_{layer}_excess_employee_benefits_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_employers_liability_usd"]

    

    # Pricing Excess Coverage Enhancments
    include_stop_gap_excess = excess_coverages[excess_coverages["coverage"] == "stop_gap"]["include_excess"].iloc[0]
    include_tria_excess = excess_coverages[excess_coverages["coverage"] == "tria"]["include_excess"].iloc[0]
    include_punitive_damages_excess = excess_coverages[excess_coverages["coverage"] == "punitive_damages"]["include_excess"].iloc[0]
    include_costs_in_addition_excess = excess_coverages[excess_coverages["coverage"] == "costs_in_addition"]["include_excess"].iloc[0]
    include_auto_excess = excess_coverages[excess_coverages["coverage"] == "auto"]["include_excess"].iloc[0]
    coverage_enhancments_excess_premiums = pd.DataFrame()
    for layer in range (1,11):
        coverage_enhancments_excess_premiums[f"excess_{layer}_stop_gap_usd"] = include_stop_gap_excess * excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_exc_tech_eo_excess_usd"] * stop_gap_additional_coverage_value
        coverage_enhancments_excess_premiums[f"excess_{layer}_tria_usd"] = include_tria_excess * np.maximum(excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_exc_tech_eo_excess_usd"] * tria_additional_coverage_value , tria_min)
        coverage_enhancments_excess_premiums[f"excess_{layer}_punitive_damages_usd"] = include_punitive_damages_excess * excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_exc_tech_eo_excess_usd"] * punitive_damages_additional_coverage_value
        coverage_enhancments_excess_premiums[f"excess_{layer}_costs_in_addition_usd"] = include_costs_in_addition_excess * excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_excess_usd"] * costs_in_addition_primary["debit"]
        coverage_enhancments_excess_premiums[f"excess_{layer}_auto_usd"] = include_auto_excess * base_premiums_per_coverage["auto_hnoa_base"]   * excess_ilfs[f"ilf_agg_{layer}_excess"]

    # To check
    # excess_premium_totals_excl_enhancments["supported_excess_premium_2_excess"]
    # coverage_enhancments_excess_premiums["excess_2_stop_gap"]
    # coverage_enhancments_excess_premiums["excess_2_tria"]
    # coverage_enhancments_excess_premiums["excess_2_punitive_damages"]
    # coverage_enhancments_excess_premiums["excess_2_costs_in_addition"]
    # coverage_enhancments_excess_premiums["excess_2_auto"]

    excess_premium_totals_enhancments = pd.DataFrame()
    # for layer in range (1,11):
    #     excess_cols = [col for col in coverage_enhancments_excess_premiums.columns if col.startswith(f"excess_{layer}")]
    #     excess_premium_totals_enhancments[f"supported_excess_premium_{layer}_excess"] = coverage_enhancments_excess_premiums[excess_cols].sum(axis=1)  

    for layer in range(1,11):
        excess_premium_totals_enhancments[f"supported_excess_premium_{layer}_excess_usd"] = coverage_enhancments_excess_premiums[f"excess_{layer}_stop_gap_usd"] + \
        coverage_enhancments_excess_premiums[f"excess_{layer}_tria_usd"] + \
        coverage_enhancments_excess_premiums[f"excess_{layer}_punitive_damages_usd"] + \
        coverage_enhancments_excess_premiums[f"excess_{layer}_costs_in_addition_usd"] + \
        coverage_enhancments_excess_premiums[f"excess_{layer}_auto_usd"]
    
    # Convert to local currency
    support_excess_premium = excess_premium_totals_enhancments.add(excess_premium_totals_excl_enhancments,fill_value=0) / currency_factor     
    support_excess_premium.columns = support_excess_premium.columns.str.replace('_usd','')        
    support_excess_premium = support_excess_premium.fillna(0)

    # cyber excess premium and gross up the supported excess premium here
    cyber_excess_selection = cds.rating_factors.cyber.include_excess
    brokerage_excess = pd.DataFrame()
    if cyber_selection and cyber_excess_selection:
        cyber_options_df = pd.DataFrame([{
            f"model_premium_third_party_{layer}_excess": getattr(item, f"model_premium_third_party_{layer}_excess")
            for layer in range(1, 11)
        } for item in cds.cyber_options])

        # cyber_options_df = utils.pd_df_from_hx_list(cds.cyber_options)
        
        for layer in range(1,11):
            brokerage_excess[f"brokerage_{layer}_excess"] = options.loc[:,f"brokerage_{layer}_excess"].fillna(0) 
            support_excess_premium[f"supported_excess_premium_{layer}_excess"] = support_excess_premium[f"supported_excess_premium_{layer}_excess"] / (1 - brokerage_excess[f"brokerage_{layer}_excess"])+ \
                cyber_options_df[f"model_premium_third_party_{layer}_excess"]
    else:
        for layer in range(1,11):
            brokerage_excess[f"brokerage_{layer}_excess"] = options.loc[:,f"brokerage_{layer}_excess"].fillna(0) 
            support_excess_premium[f"supported_excess_premium_{layer}_excess"] = support_excess_premium[f"supported_excess_premium_{layer}_excess"] / (1 - brokerage_excess[f"brokerage_{layer}_excess"]) 
    
    # Set the GL premiums to the umbrella nodes

    # GL Premium for Umbrella
    gl_excess_premium = excess_premium.filter(like="general_liability") 
    gl_excess_premium.columns = gl_excess_premium.columns.str.replace("_usd","") 
    gl_excess_premium = gl_excess_premium / currency_factor

    if cds.rating_factors.pricing.general_liability.claims_basis == "Occurrence" and cds.rating_factors.pricing.general_liability.include_excess == True and cds.rating_factors.gmm.umbrella.general_liability.occurrence_cover == True:
        for index, option in enumerate(cds.options):
            for layer in range(1,11):
                setattr(getattr(option, "gmm_general_liability"),f"premium_{layer}_excess", gl_excess_premium[f"premium_{layer}_excess_general_liability"][index])
    else:
        for index, option in enumerate(cds.options):
            for layer in range(1,11):
                setattr(getattr(option, "gmm_general_liability"),f"premium_{layer}_excess", 0)



    timer.end("section 8") 
    timer.start("section 9")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Excess Premium: Minimum Premium Calculations
    #--------------------------------------------------------------------------------------------------------------------------------#
    
    # Minimum rate on line parameter table
    min_rol_xs_table = hx.params.table_minimum_excess_premium        

    # Turn to scalar variable
    min_rol_xs = min_rol_xs_table.iat[0,0]
    
    min_premium_xs = pd.DataFrame()

    for layer in range (1,11):
        min_premium_xs[f"minimum_premium_{layer}_excess"] = (excess_table[f"dettachment_{layer}_excess"] - excess_table[f"attachment_{layer}_excess"]).fillna(0) * min_rol_xs
    
    # write to cds
    utils.write_pd_to_hxd(min_premium_xs,cds.options,["minimum_premium_1_excess",\
        "minimum_premium_2_excess","minimum_premium_3_excess","minimum_premium_4_excess","minimum_premium_5_excess","minimum_premium_6_excess",\
        "minimum_premium_7_excess","minimum_premium_8_excess","minimum_premium_9_excess","minimum_premium_10_excess"])


        

    timer.end("section 9") 
    timer.start("section 10")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Excess Gross Premium: Total Calculations
    #--------------------------------------------------------------------------------------------------------------------------------#   

    # Rate Umbrella Excess here
    timer.start("section 10 rate umbrella")
    rate_umbrella(hxd) 
    timer.end("section 10 rate umbrella")

    #options_df_2 = utils.pd_df_from_hx_list(cds.options)
    #filter_col = [col for col in options_df_2 if col.startswith('umbrella_unsupported_net_premium')]
    #filter_col_brokerage = [col for col in options_df_2 if col.startswith('brokerage')]

    #options_umbrella_df = options_df_2[filter_col]
    #options_brokerage_df = options_df_2[filter_col_brokerage]

    options_umbrella_dict = [{
        "umbrella_unsupported_net_premium.premium_primary": item.umbrella_unsupported_net_premium.premium_primary,
        "umbrella_unsupported_net_premium.premium_1_excess": item.umbrella_unsupported_net_premium.premium_1_excess,
        "umbrella_unsupported_net_premium.premium_2_excess": item.umbrella_unsupported_net_premium.premium_2_excess,
        "umbrella_unsupported_net_premium.premium_3_excess": item.umbrella_unsupported_net_premium.premium_3_excess,
        "umbrella_unsupported_net_premium.premium_4_excess": item.umbrella_unsupported_net_premium.premium_4_excess,
        "umbrella_unsupported_net_premium.premium_5_excess": item.umbrella_unsupported_net_premium.premium_5_excess,
        "umbrella_unsupported_net_premium.premium_6_excess": item.umbrella_unsupported_net_premium.premium_6_excess,
        "umbrella_unsupported_net_premium.premium_7_excess": item.umbrella_unsupported_net_premium.premium_7_excess,
        "umbrella_unsupported_net_premium.premium_8_excess": item.umbrella_unsupported_net_premium.premium_8_excess,
        "umbrella_unsupported_net_premium.premium_9_excess": item.umbrella_unsupported_net_premium.premium_9_excess,
        "umbrella_unsupported_net_premium.premium_10_excess": item.umbrella_unsupported_net_premium.premium_10_excess
    } for item in cds.options]
    options_umbrella_df = pd.DataFrame(options_umbrella_dict) 

    options_brokerage_dict = [{
        "brokerage_primary": item.brokerage_primary,
        "brokerage_1_excess": item.brokerage_1_excess,
        "brokerage_2_excess": item.brokerage_2_excess,
        "brokerage_3_excess": item.brokerage_3_excess,
        "brokerage_4_excess": item.brokerage_4_excess,
        "brokerage_5_excess": item.brokerage_5_excess,
        "brokerage_6_excess": item.brokerage_6_excess,
        "brokerage_7_excess": item.brokerage_7_excess,
        "brokerage_8_excess": item.brokerage_8_excess,
        "brokerage_9_excess": item.brokerage_9_excess,
        "brokerage_10_excess": item.brokerage_10_excess
    } for item in cds.options]
    options_brokerage_df = pd.DataFrame(options_brokerage_dict)  

    options_brokerage_df = options_brokerage_df.fillna(0)
    options_brokerage_df = 1-options_brokerage_df

    options_umbrella_gross_prem = pd.DataFrame()
    gl_claims_made_flag = getattr(cds.rating_factors.pricing.general_liability,"claims_basis")

    for layer in range(1,11):
        general_liability_prem = excess_premium[f"premium_{layer}_excess_general_liability_usd"]
        umbrella_premium_pre_max = options_umbrella_df[f"umbrella_unsupported_net_premium.premium_{layer}_excess"]
        if gl_claims_made_flag == "Occurrence":
            options_umbrella_gross_prem[f"umbrella_premium_{layer}_excess"] = np.where(umbrella_premium_pre_max > 0, \
                (np.maximum((5000 - general_liability_prem) / currency_factor, umbrella_premium_pre_max)) / options_brokerage_df[f"brokerage_{layer}_excess"],0)
        else:
            options_umbrella_gross_prem[f"umbrella_premium_{layer}_excess"] = np.where(umbrella_premium_pre_max > 0, \
                (np.maximum(5000 / currency_factor, umbrella_premium_pre_max)) / options_brokerage_df[f"brokerage_{layer}_excess"],0)

    # gross the umbrella premium
    options_umbrella_gross_prem.fillna(0, inplace=True)  #IR: fix to avoid NaN errors
    utils.write_pd_to_hxd(options_umbrella_gross_prem,cds.options,["umbrella_premium_1_excess",\
        "umbrella_premium_2_excess","umbrella_premium_3_excess","umbrella_premium_4_excess","umbrella_premium_5_excess","umbrella_premium_6_excess",\
        "umbrella_premium_7_excess","umbrella_premium_8_excess","umbrella_premium_9_excess","umbrella_premium_10_excess"])
    # Rate Umbrella Excess + main coverage excess             

    # brokerage_excess = pd.DataFrame()
    total_gross_model_premium_excess = pd.DataFrame()    

    for layer in range (1,11):
        # Brokerage
        # brokerage_excess[f"brokerage_{layer}_excess"] = options.loc[:,f"brokerage_{layer}_excess"].fillna(0) 

        # Gross supported premium
        support_excess_premium[f"supported_excess_premium_{layer}_excess"] = support_excess_premium[f"supported_excess_premium_{layer}_excess"].fillna(0) 

        # total gross model premium excess (with nmp load)
        total_gross_model_premium_excess[f"model_premium_{layer}_excess"] = (support_excess_premium[f"supported_excess_premium_{layer}_excess"] + options_umbrella_gross_prem[f"umbrella_premium_{layer}_excess"]) * (1 + nmp_load)
        total_gross_model_premium_excess[f"uplift_for_nmp_{layer}_excess"] = total_gross_model_premium_excess[f"model_premium_{layer}_excess"] - ((support_excess_premium[f"supported_excess_premium_{layer}_excess"] + options_umbrella_gross_prem[f"umbrella_premium_{layer}_excess"]))
        
        # Gross premium = maximum of model premium and minimum premium
        total_gross_model_premium_excess[f"gross_premium_{layer}_excess"] = np.maximum(total_gross_model_premium_excess[f"model_premium_{layer}_excess"], min_premium_xs[f"minimum_premium_{layer}_excess"])                             
    
        total_gross_model_premium_excess[f"benchmark_premium_{layer}_excess"] = total_gross_model_premium_excess[f"gross_premium_{layer}_excess"].fillna(0) * (priced_to_net_loss_ratio / benchmark_loss_ratio)
        total_gross_model_premium_excess[f"quoted_premium_{layer}_excess"] = options.loc[:,f"quoted_premium_{layer}_excess"].fillna(0)            

        # For checking
        # total_gross_model_premium_excess["benchmark_premium_5_excess"]
        # total_gross_model_premium_excess["quoted_premium_5_excess"]
    
        # bpi calc
        total_gross_model_premium_excess[f"bpi_{layer}_excess"] = np.where(total_gross_model_premium_excess[f"quoted_premium_{layer}_excess"] == 0, \
            None, \
            (total_gross_model_premium_excess[f"quoted_premium_{layer}_excess"] / total_gross_model_premium_excess[f"benchmark_premium_{layer}_excess"]).fillna(0))

        # Setting values to zero where there is no per claim limit, to prevent outputs being displayed when there are no inputs...
        total_gross_model_premium_excess[f"model_premium_{layer}_excess"] = np.where(pd.isnull(layers_table[f"per_claim_limit_{layer}_excess"]), 0, total_gross_model_premium_excess[f"model_premium_{layer}_excess"])
        total_gross_model_premium_excess[f"uplift_for_nmp_{layer}_excess"] = np.where(pd.isnull(layers_table[f"per_claim_limit_{layer}_excess"]), 0, total_gross_model_premium_excess[f"uplift_for_nmp_{layer}_excess"]) 
        total_gross_model_premium_excess[f"gross_premium_{layer}_excess"] = np.where(pd.isnull(layers_table[f"per_claim_limit_{layer}_excess"]), 0, total_gross_model_premium_excess[f"gross_premium_{layer}_excess"])
        support_excess_premium[f"supported_excess_premium_{layer}_excess"] = np.where(pd.isnull(layers_table[f"per_claim_limit_{layer}_excess"]), 0, support_excess_premium[f"supported_excess_premium_{layer}_excess"])  
        
    total_gross_model_premium_excess = total_gross_model_premium_excess.fillna(0) 
    total_gross_model_premium_excess = total_gross_model_premium_excess.replace(np.inf, 0)       
    # write to cds                        
    # gross model premium
    utils.write_pd_to_hxd(total_gross_model_premium_excess, cds.options, ["model_premium_1_excess",\
        "model_premium_2_excess","model_premium_3_excess","model_premium_4_excess","model_premium_5_excess","model_premium_6_excess",\
        "model_premium_7_excess","model_premium_8_excess","model_premium_9_excess","model_premium_10_excess"])
    # nmp load
    utils.write_pd_to_hxd(total_gross_model_premium_excess, cds.options, ["uplift_for_nmp_1_excess",\
        "uplift_for_nmp_2_excess","uplift_for_nmp_3_excess","uplift_for_nmp_4_excess","uplift_for_nmp_5_excess","uplift_for_nmp_6_excess",\
        "uplift_for_nmp_7_excess","uplift_for_nmp_8_excess","uplift_for_nmp_9_excess","uplift_for_nmp_10_excess"])    
    # gross premium
    utils.write_pd_to_hxd(total_gross_model_premium_excess, cds.options, ["gross_premium_1_excess",\
        "gross_premium_2_excess","gross_premium_3_excess","gross_premium_4_excess","gross_premium_5_excess","gross_premium_6_excess",\
        "gross_premium_7_excess","gross_premium_8_excess","gross_premium_9_excess","gross_premium_10_excess"])
    # bpi
    utils.write_pd_to_hxd(total_gross_model_premium_excess, cds.options, ["bpi_1_excess",\
        "bpi_2_excess","bpi_3_excess","bpi_4_excess","bpi_5_excess","bpi_6_excess",\
        "bpi_7_excess","bpi_8_excess","bpi_9_excess","bpi_10_excess"])

    utils.write_pd_to_hxd(support_excess_premium,cds.options,["supported_excess_premium_1_excess","supported_excess_premium_2_excess",\
        "supported_excess_premium_3_excess","supported_excess_premium_4_excess","supported_excess_premium_5_excess","supported_excess_premium_6_excess",\
        "supported_excess_premium_7_excess","supported_excess_premium_8_excess","supported_excess_premium_9_excess","supported_excess_premium_10_excess"])    

    
    timer.end("section 10") 


def rating_glsn(hxd, options_dict, variables):
    cds = hxd.cds
    cyber_selection = cds.cyber_selection

    # Unpack variables
    currency_factor = variables["currency_factor"]
    base_premium = variables["base_premium"]
    non_option_coverages = variables["non_option_coverages"]
    venue_factor = variables["venue_factor"]
    policy_term = variables["policy_term"]
    total_schedule_mod_factor = variables["total_schedule_mod_factor"]
    surcharge_table = variables["surcharge_table"]
    us_international = variables["us_international"]
    inception_date = variables["inception_date"]
    
    stop_gap_additional_coverage_value = variables["stop_gap_additional_coverage_value"]
    tria_additional_coverage_value = variables["tria_additional_coverage_value"]
    punitive_damages_additional_coverage_value = variables["punitive_damages_additional_coverage_value"] 

    biosecure_product = variables["biosecure_product"]
    retro_factor = variables["retro_factor"]
    size_discount_factor = variables["size_discount_factor"]
    glsn_class_table = variables["glsn_class_table"]
    retro_table = variables["retro_table"]
    default_excess_retro_date = variables["default_excess_retro_date"]

    timer.start("section 1")
    #----------------------------------------------------------------------------------------------#
    # Number of significant coverages, Policy Aggregate Limits and Aggregate Retentions Agg/Weighted Sum Individual Agg Ratio
    #----------------------------------------------------------------------------------------------#
    #options = utils.pd_df_from_hx_list(cds.options)
    ### Get the relevant columns from the options node - too slow using utils.pd_df_from_hx_list function

    
    options = pd.DataFrame(options_dict) 

    block_eo = cds.rating_factors.glsn.form.selected == "WellTech"

    # Aggregate Limits

    agg_limits = options.loc[:, agg_limit_cols(hxd, "glsn")]

    agg_limits["sum_of_individual_aggs"] = agg_limits.sum(axis=1)

    # Aggregate retentions

    retentions = options.loc[:,["coverages.product_liability.retention",\
        "coverages.eo.retention",\
        "coverages.healthcare_professional_liability.retention",\
        "coverages.general_liability.retention",\
        "coverages.sexual_abuse.retention",\
        "coverages.employee_benefits_liability.retention",\
        "coverages.product_recall.retention",\
        "coverages.well_tech_eo_media.retention"]]   

    retentions["sum_of_individual_aggs"] = retentions.sum(axis=1)     

    # Significant Coverages ########################################################################

    product_liability_signficant_coverage = non_option_coverages[non_option_coverages["coverage"] == "product_liability"]["significant_coverage"].iloc[0]
    hpl_signficant_coverage = non_option_coverages[non_option_coverages["coverage"] == "healthcare_professional_liability"]["significant_coverage"].iloc[0]
    well_tech_eo_media_signficant_coverage = non_option_coverages[non_option_coverages["coverage"] == "well_tech_eo_media"]["significant_coverage"].iloc[0]
    eo_signficant_coverage = non_option_coverages[non_option_coverages["coverage"] == "eo"]["significant_coverage"].iloc[0]

    # Product Liability - contribute to number of significant coverages?
    if product_liability_signficant_coverage == "Significant" :
        product_liability_signficant_coverage_per_option = np.where((retentions["coverages.product_liability.retention"] + agg_limits["coverages.product_liability.aggregate_limit"]  + options["coverages.product_liability.per_claim_limit"]) != 0 , 1, 0)
    else:
        product_liability_signficant_coverage_per_option = [0] * len(options)

    # Healthcare Professional Liability - contribute to number of significant coverages?
    if hpl_signficant_coverage == "Significant" :
        hpl_signficant_coverage_per_option = np.where((retentions["coverages.healthcare_professional_liability.retention"] + agg_limits["coverages.healthcare_professional_liability.aggregate_limit"]  + options["coverages.healthcare_professional_liability.per_claim_limit"]) != 0 , 1, 0)
    else:
        hpl_signficant_coverage_per_option = [0] * len(options)

    # EO - contribute to number of significant coverages?
    if block_eo :           
        if well_tech_eo_media_signficant_coverage == "Significant":
            eo_signficant_coverage_per_option = np.where((retentions["coverages.well_tech_eo_media.retention"] + agg_limits["coverages.well_tech_eo_media.aggregate_limit"]  + options["coverages.well_tech_eo_media.per_claim_limit"]) != 0 , 1, 0) 
        else:
            eo_signficant_coverage_per_option = [0] * len(options)
    else :            
        if eo_signficant_coverage == "Significant":
            eo_signficant_coverage_per_option = np.where((retentions["coverages.eo.retention"] + agg_limits["coverages.eo.aggregate_limit"]  + options["coverages.eo.per_claim_limit"]) != 0 , 1, 0) 
        else:
            eo_signficant_coverage_per_option = [0] * len(options)

    
    # Number of significant coverages      
    number_significant_coverages = pd.DataFrame()
    number_significant_coverages["product_liability_signficant_coverage_per_option"] = pd.DataFrame({"product_liability_signficant_coverage_per_option":product_liability_signficant_coverage_per_option})
    number_significant_coverages["hpl_signficant_coverage_per_option"] = pd.DataFrame({"hpl_signficant_coverage_per_option":hpl_signficant_coverage_per_option})
    number_significant_coverages["eo_signficant_coverage_per_option"] = pd.DataFrame({"eo_signficant_coverage_per_option":eo_signficant_coverage_per_option})

    number_significant_coverages["number_significant_coverages"] = number_significant_coverages["product_liability_signficant_coverage_per_option"] + \
        number_significant_coverages["hpl_signficant_coverage_per_option"] + \
        number_significant_coverages["eo_signficant_coverage_per_option"]

    if max(number_significant_coverages["number_significant_coverages"]) == 0:
        hx.errors.validation("Please provide at least one Signficiant Coverage")

    # Significant coverages param table
    glsn_significant_coverage_table = hx.params.table_glsn_significant_coverage                

    # Significant coverages factor
    # Product liability
    if product_liability_signficant_coverage == None:
        number_significant_coverages["product_liability_sig_coverage_factor"] = 1
    else:    
        number_significant_coverages["product_liability_sig_coverage_factor"] = \
            np.where(number_significant_coverages["number_significant_coverages"] == 1, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == product_liability_signficant_coverage]["1"].iloc[0], \
                np.where(number_significant_coverages["number_significant_coverages"] == 2, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == product_liability_signficant_coverage]["2"].iloc[0], \
                    np.where(number_significant_coverages["number_significant_coverages"] == 3, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == product_liability_signficant_coverage]["3"].iloc[0], \
                        1)))

    # E&O
    if eo_signficant_coverage == None:
        number_significant_coverages["eo_sig_coverage_factor"] = 1
    else:
        number_significant_coverages["eo_sig_coverage_factor"] = \
            np.where(number_significant_coverages["number_significant_coverages"] == 1, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == eo_signficant_coverage]["1"].iloc[0], \
                np.where(number_significant_coverages["number_significant_coverages"] == 2, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == eo_signficant_coverage]["2"].iloc[0], \
                    np.where(number_significant_coverages["number_significant_coverages"] == 3, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == eo_signficant_coverage]["3"].iloc[0], \
                        1)))

    # HPL
    if hpl_signficant_coverage == None:
        number_significant_coverages["hpl_sig_coverage_factor"] = 1
    else:
        number_significant_coverages["hpl_sig_coverage_factor"] = \
            np.where(number_significant_coverages["number_significant_coverages"] == 1, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == hpl_signficant_coverage]["1"].iloc[0], \
                np.where(number_significant_coverages["number_significant_coverages"] == 2, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == hpl_signficant_coverage]["2"].iloc[0], \
                    np.where(number_significant_coverages["number_significant_coverages"] == 3, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == hpl_signficant_coverage]["3"].iloc[0], \
                        1)))

    # Tech E&O, Media     
    if well_tech_eo_media_signficant_coverage == None:
        number_significant_coverages["well_tech_eo_media_sig_coverage_factor"] = 1
    else:
        number_significant_coverages["well_tech_eo_media_sig_coverage_factor"] = \
            np.where(number_significant_coverages["number_significant_coverages"] == 1, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == well_tech_eo_media_signficant_coverage]["1"].iloc[0], \
                np.where(number_significant_coverages["number_significant_coverages"] == 2, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == well_tech_eo_media_signficant_coverage]["2"].iloc[0], \
                    np.where(number_significant_coverages["number_significant_coverages"] == 3, glsn_significant_coverage_table[glsn_significant_coverage_table["Level"] == well_tech_eo_media_signficant_coverage]["3"].iloc[0], \
                        1)))

    
    timer.end("section 1")
    timer.start("section 2")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary layer base premium and net premums for each option and coverage
    #--------------------------------------------------------------------------------------------------------------------------------#

    primary_layer_per_coverage = pd.DataFrame()
    total_primary_layer_per_coverage = pd.DataFrame()
    total_base_primary_layer_per_coverage = pd.DataFrame() #this excludes retro and schedule mods

    # No weighting given to EO if block E&O is true 
    non_option_coverages["block_eo_flag"] = np.where(non_option_coverages["coverage"] == "eo", block_eo, False)              

    # Coverage weights
    non_option_coverages["coverage_weight"] = non_option_coverages["include_primary"] * non_option_coverages["additional_coverage"] * ( 1- non_option_coverages["block_eo_flag"])

    # All coverages except well_tech_eo_media
    for coverage, retro in zip(["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall"],retro_factor):

        # additional coverage factor
        additional_coverage_factor = non_option_coverages[non_option_coverages["coverage"] == coverage]["coverage_weight"].iloc[0]                        
        
        # Base premium calc by coverage
        # product liability
        if coverage in ["product_liability"]:
            # Base premium
            primary_layer_per_coverage["primary_layer_base_premium"] = np.where( options[f"coverages.{coverage}.per_claim_limit"] != 0, base_premium * \
            additional_coverage_factor * \
            number_significant_coverages["product_liability_sig_coverage_factor"] * \
            size_discount_factor * \
            venue_factor * \
            retro * \
            policy_term   ,0)
            # Base premium ex retro
            primary_layer_per_coverage["primary_layer_base_premium_exc_retro"] = np.where( options[f"coverages.{coverage}.per_claim_limit"] != 0, base_premium * \
            additional_coverage_factor * \
            number_significant_coverages["product_liability_sig_coverage_factor"] * \
            size_discount_factor * \
            venue_factor * \
            policy_term   ,0)
        # eo
        elif coverage in ["eo"]:
            # Base premium
            primary_layer_per_coverage["primary_layer_base_premium"] = np.where( options[f"coverages.{coverage}.per_claim_limit"] != 0, base_premium * \
            additional_coverage_factor * \
            number_significant_coverages["eo_sig_coverage_factor"] * \
            size_discount_factor * \
            venue_factor * \
            retro * \
            policy_term   ,0)
            # Base premium ex retro
            primary_layer_per_coverage["primary_layer_base_premium_exc_retro"] = np.where( options[f"coverages.{coverage}.per_claim_limit"] != 0, base_premium * \
            additional_coverage_factor * \
            number_significant_coverages["eo_sig_coverage_factor"] * \
            size_discount_factor * \
            venue_factor * \
            policy_term   ,0)
        # hpl
        elif coverage in ["healthcare_professional_liability"]:
            # Base premium
            primary_layer_per_coverage["primary_layer_base_premium"] = np.where( options[f"coverages.{coverage}.per_claim_limit"] != 0, base_premium * \
            additional_coverage_factor * \
            number_significant_coverages["hpl_sig_coverage_factor"] * \
            size_discount_factor * \
            venue_factor * \
            retro * \
            policy_term   ,0)
            # Base premium ex retro
            primary_layer_per_coverage["primary_layer_base_premium_exc_retro"] = np.where( options[f"coverages.{coverage}.per_claim_limit"] != 0, base_premium * \
            additional_coverage_factor * \
            number_significant_coverages["hpl_sig_coverage_factor"] * \
            size_discount_factor * \
            venue_factor * \
            policy_term   ,0)            
        else:
            # Base premium
            primary_layer_per_coverage["primary_layer_base_premium"] = np.where( options[f"coverages.{coverage}.per_claim_limit"] != 0, base_premium * \
            additional_coverage_factor * \
            size_discount_factor * \
            venue_factor * \
            retro * \
            policy_term   ,0)
            # Base premium ex retro
            primary_layer_per_coverage["primary_layer_base_premium_exc_retro"] = np.where( options[f"coverages.{coverage}.per_claim_limit"] != 0, base_premium * \
            additional_coverage_factor * \
            size_discount_factor * \
            venue_factor * \
            policy_term   ,0)
                        
        # Base premium with retro, excluding schedule modes
        total_base_primary_layer_per_coverage[f"primary_layer_base_premium_{coverage}_usd"] = primary_layer_per_coverage["primary_layer_base_premium"]
        # Base premium excluding Retro and schedule mods
        total_base_primary_layer_per_coverage[f"primary_layer_base_premium_{coverage}_exc_retro_usd"] = primary_layer_per_coverage["primary_layer_base_premium_exc_retro"]

    # To be used in excess calcs, which does not include tech E&O, media        
    total_base_primary_layer_per_coverage["primary_base_premium_exc_retro_usd"] = total_base_primary_layer_per_coverage.sum(axis=1)


    timer.end("section 2")
    timer.start("section 3")
    # Well Tech EO Media ########################################################################

    # TECH EO's base premium is being used in the policy agg limits and retention calcs 
    non_option_tech_eo_filtered_temp = non_option_coverages[non_option_coverages["coverage"] == "well_tech_eo_media"]
    tech_eo_selection = non_option_tech_eo_filtered_temp["include_primary"].iloc[0]
    tech_eo_retro_factor = non_option_tech_eo_filtered_temp["retro_factor"].iloc[0]                

    rate_tech_eo(hxd)

    # tech_eo_selection = True
    tech_eo_primary_net_prem_usd = [0 for item in cds.options]
    tech_eo_base_net_prem_usd = [0 for item in cds.options]        
    for index,item in enumerate(cds.options):
        tech_eo_base_net_prem_usd[index] = cds.tech_eo_base_net_premium_usd
        tech_eo_primary_net_prem_usd[index] = item.tech_eo_primary_net_premium_usd     
                    
    # Convert to dataframe        
    tech_eo_primary_net_prem_usd = pd.DataFrame({"tech_eo_primary_net_prem_usd":tech_eo_primary_net_prem_usd})
    tech_eo_base_net_prem_usd = pd.DataFrame({"tech_eo_base_net_prem_usd" :tech_eo_base_net_prem_usd})        

    # Add on retro factor, policy term and schedule modifier (schedule modifier only for primary)
    tech_eo_base_net_prem_usd["tech_eo_base_net_prem_raw_usd"] = tech_eo_base_net_prem_usd["tech_eo_base_net_prem_usd"] * policy_term
    tech_eo_base_net_prem_usd["tech_eo_base_net_prem_usd"] = tech_eo_base_net_prem_usd["tech_eo_base_net_prem_usd"] * tech_eo_retro_factor * policy_term * number_significant_coverages["well_tech_eo_media_sig_coverage_factor"]
    tech_eo_primary_net_prem_usd["tech_eo_primary_net_prem_usd"] = tech_eo_primary_net_prem_usd["tech_eo_primary_net_prem_usd"] * tech_eo_retro_factor * policy_term * number_significant_coverages["well_tech_eo_media_sig_coverage_factor"]
    # Add to main dataframe where all the other cover's base premium are
    total_base_primary_layer_per_coverage["primary_layer_base_premium_well_tech_eo_media_usd"] = tech_eo_base_net_prem_usd["tech_eo_base_net_prem_usd"]

    # Calculate well_tech_eo_media coverage weighting
    tech_eo_coverage_weight = pd.DataFrame()

    # base premiums needed to calculate tech eo's coverage weighting
    tech_eo_coverage_weight["primary_layer_base_premium_product_liability_exc_sig_factor_usd"] = total_base_primary_layer_per_coverage["primary_layer_base_premium_product_liability_usd"]
    tech_eo_coverage_weight["primary_layer_base_premium_healthcare_professional_liability_exc_sig_factor_usd"] = total_base_primary_layer_per_coverage["primary_layer_base_premium_healthcare_professional_liability_usd"]
    
    tech_eo_coverage_weight["primary_layer_base_premium_well_tech_eo_media_exc_sig_factor_raw_usd"] = tech_eo_base_net_prem_usd["tech_eo_base_net_prem_raw_usd"]

    # Significant option chosen
    tech_eo_coverage_weight["product_liability_signficant_coverage_per_option"] = number_significant_coverages["product_liability_signficant_coverage_per_option"]
    tech_eo_coverage_weight["well_tech_eo_media_signficant_coverage_per_option"] = number_significant_coverages["eo_signficant_coverage_per_option"]
    tech_eo_coverage_weight["hpl_signficant_coverage_per_option"] = number_significant_coverages["hpl_signficant_coverage_per_option"]

    # Significant coverage factors needed to reverse out
    tech_eo_coverage_weight["product_liability_sig_coverage_factor"] = number_significant_coverages["product_liability_sig_coverage_factor"]
    
    # If block eo we use the tech_eo sig factor and primary base premium, else we use the standard eo version
    if block_eo == True:        
        tech_eo_coverage_weight["well_tech_eo_media_sig_coverage_factor"] = number_significant_coverages["well_tech_eo_media_sig_coverage_factor"]
        tech_eo_coverage_weight["primary_layer_base_premium_well_tech_eo_media_usd"] = tech_eo_base_net_prem_usd["tech_eo_base_net_prem_usd"]
    else:
        tech_eo_coverage_weight["well_tech_eo_media_sig_coverage_factor"] = number_significant_coverages["eo_sig_coverage_factor"]
        tech_eo_coverage_weight["primary_layer_base_premium_well_tech_eo_media_usd"] = total_base_primary_layer_per_coverage["primary_layer_base_premium_eo_usd"]
        if cds.rating_factors.pricing.well_tech_eo_media.significant_coverage is not None :
            hx.errors.validation("Cannot provide Well Tech EO and Media Signficant Coverage if Product is not WellTech")

    tech_eo_coverage_weight["hpl_sig_coverage_factor"] = number_significant_coverages["hpl_sig_coverage_factor"]

    # well tech eo media coverage weight
    tech_eo_coverage_weight["well_tech_eo_media_coverage_weight"] = np.where(
        tech_eo_coverage_weight["product_liability_signficant_coverage_per_option"] == 1,  tech_eo_coverage_weight["primary_layer_base_premium_well_tech_eo_media_exc_sig_factor_raw_usd"]  / (tech_eo_coverage_weight["primary_layer_base_premium_product_liability_exc_sig_factor_usd"] / tech_eo_coverage_weight["product_liability_sig_coverage_factor"]),
        np.where( tech_eo_coverage_weight["well_tech_eo_media_signficant_coverage_per_option"] == 1, tech_eo_coverage_weight["primary_layer_base_premium_well_tech_eo_media_exc_sig_factor_raw_usd"] / (tech_eo_coverage_weight["primary_layer_base_premium_well_tech_eo_media_usd"] /tech_eo_coverage_weight["well_tech_eo_media_sig_coverage_factor"]),
            np.where(tech_eo_coverage_weight["hpl_signficant_coverage_per_option"] == 1, tech_eo_coverage_weight["primary_layer_base_premium_well_tech_eo_media_exc_sig_factor_raw_usd"] / (tech_eo_coverage_weight["primary_layer_base_premium_healthcare_professional_liability_exc_sig_factor_usd"]/tech_eo_coverage_weight["hpl_sig_coverage_factor"])
                ,0)))      
    
            
    # well_tech_eo_coverage_weight
    well_tech_eo_coverage_weight = tech_eo_coverage_weight.loc[0,["well_tech_eo_media_coverage_weight"]].iloc[0]        

    # Join onto main table
    non_option_coverages["additional_coverage"] = np.where(non_option_coverages["coverage"] == "well_tech_eo_media", \
        well_tech_eo_coverage_weight , \
        non_option_coverages["additional_coverage"])  

    non_option_coverages["coverage_weight"] = np.where(non_option_coverages["coverage"] == "well_tech_eo_media", \
        well_tech_eo_coverage_weight , \
        non_option_coverages["coverage_weight"])  


    timer.end("section 3")
    timer.start("section 4")
    # Aggregate Limits ########################################################################

    for coverage in ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media"]:
        additional_coverage_factor = non_option_coverages[non_option_coverages["coverage"] == coverage]["coverage_weight"].iloc[0]
        agg_limits[f"weighted_agg_{coverage}"] = agg_limits[f"coverages.{coverage}.aggregate_limit"] * additional_coverage_factor
        agg_limits[f"contribution_to_sum_of_aggs_{coverage}"] = agg_limits[f"coverages.{coverage}.aggregate_limit"] / agg_limits["sum_of_individual_aggs"]
    
    weighted_agg_limits = agg_limits.loc[:,["weighted_agg_product_liability",\
        "weighted_agg_eo",\
        "weighted_agg_healthcare_professional_liability",\
        "weighted_agg_general_liability",\
        "weighted_agg_sexual_abuse",\
        "weighted_agg_employee_benefits_liability",\
        "weighted_agg_product_recall",\
        "weighted_agg_well_tech_eo_media"]]

    policy_aggregate = options.loc[:,["agg_limit"]]
    policy_aggregate["weighted_sum_ind_aggs"] = weighted_agg_limits.sum(axis=1)

    # try:
    policy_aggregate["policy_agg.weighted_sum"] = policy_aggregate["agg_limit"] / policy_aggregate["weighted_sum_ind_aggs"] 
    policy_aggregate["policy_agg.weighted_sum"] = policy_aggregate["policy_agg.weighted_sum"].fillna(0)
    # except:
    #     policy_aggregate["policy_agg.weighted_sum"] = 0

    #Overall policy agg factor
    agg_to_sum_of_aggs_table = hx.params.table_glsn_policy_agg 
    ratio_pol_agg_to_sum_individual =  agg_to_sum_of_aggs_table["ratio_pol_agg_to_sum_individual"].to_numpy()
    ratio_pol_agg_to_sum_individual_factor =  agg_to_sum_of_aggs_table["factor"].to_numpy()

    policy_aggregate["overall_policy_agg_factor"] = np.minimum(1 ,np.where((policy_aggregate["policy_agg.weighted_sum"]>1) | (policy_aggregate["agg_limit"].isna()),\
        1, np.interp(policy_aggregate["policy_agg.weighted_sum"], ratio_pol_agg_to_sum_individual, ratio_pol_agg_to_sum_individual_factor)))


    # Contribution to individual agg
    contribution_to_sum_of_aggs = agg_limits.loc[:,["contribution_to_sum_of_aggs_product_liability",\
        "contribution_to_sum_of_aggs_eo",\
        "contribution_to_sum_of_aggs_healthcare_professional_liability",\
        "contribution_to_sum_of_aggs_general_liability",\
        "contribution_to_sum_of_aggs_sexual_abuse",\
        "contribution_to_sum_of_aggs_employee_benefits_liability",\
        "contribution_to_sum_of_aggs_product_recall",\
        "contribution_to_sum_of_aggs_well_tech_eo_media"]]

    contribution_to_sum_of_aggs = pd.concat([contribution_to_sum_of_aggs, policy_aggregate["overall_policy_agg_factor"]], axis=1)    

    for coverage in ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media"]:
        contribution_to_sum_of_aggs[f"split_of_discount_{coverage}"] = 1 - ((1-policy_aggregate["overall_policy_agg_factor"])* contribution_to_sum_of_aggs[f"contribution_to_sum_of_aggs_{coverage}"])

    split_of_discount = contribution_to_sum_of_aggs.loc[:,["split_of_discount_product_liability",\
        "split_of_discount_eo",\
        "split_of_discount_healthcare_professional_liability",\
        "split_of_discount_general_liability",\
        "split_of_discount_sexual_abuse",\
        "split_of_discount_employee_benefits_liability",\
        "split_of_discount_product_recall",\
        "split_of_discount_well_tech_eo_media"]] 

    
    timer.end("section 4")
    timer.start("section 5")
    # Aggregate Retention ########################################################################

    retentions = options.loc[:,["coverages.product_liability.retention",\
        "coverages.eo.retention",\
        "coverages.healthcare_professional_liability.retention",\
        "coverages.general_liability.retention",\
        "coverages.sexual_abuse.retention",\
        "coverages.employee_benefits_liability.retention",\
        "coverages.product_recall.retention",\
        "coverages.well_tech_eo_media.retention"]] 

    max_retention_per_coverage = retentions.max(axis=1)    

    retentions["sum_of_individual_aggs"] = retentions.sum(axis=1)     

    for coverage in ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media"]:
        additional_coverage_factor = non_option_coverages[non_option_coverages["coverage"] == coverage]["coverage_weight"].iloc[0]
        retentions[f"weighted_agg_{coverage}"] = retentions[f"coverages.{coverage}.retention"] * additional_coverage_factor
        retentions[f"contribution_to_sum_of_aggs_{coverage}"] = np.where(retentions[f"coverages.{coverage}.retention"] > 0, 1, 0)

    weighted_retentions = retentions.loc[:,["weighted_agg_product_liability",\
        "weighted_agg_eo",\
        "weighted_agg_healthcare_professional_liability",\
        "weighted_agg_general_liability",\
        "weighted_agg_sexual_abuse",\
        "weighted_agg_employee_benefits_liability",\
        "weighted_agg_product_recall",\
        "weighted_agg_well_tech_eo_media"]]

    policy_aggregate_retention = options.loc[:,["agg_retention"]]
    policy_aggregate_retention["weighted_sum_ind_aggs"] = weighted_retentions.sum(axis=1)

    # Validations for agg limit
    limit_validation = options.loc[:,["agg_limit"]].fillna(0)
    if limit_validation["agg_limit"].sum()== 0:
        hx.errors.validation("No policy aggregate limit has been entered")
    
    # Validation for retentions
    retentions_validation = options.loc[:,["agg_retention"]]
    retentions_validation["max_retention_per_coverage"] = max_retention_per_coverage
    retentions_validation = retentions_validation.fillna(0)
    retentions_validation["validation"] = np.where((retentions_validation["max_retention_per_coverage"] > retentions_validation["agg_retention"])\
        & (retentions_validation["agg_retention"].notnull())\
        & (retentions_validation["agg_retention"] != 0), True, False)
    if retentions_validation["validation"].sum() > 0:
        hx.errors.validation("The Aggregate Retention must be greater than or equal to the largest product-level Retention. If there is no Aggregate Retention, leave this field empty.")

    # try:
    policy_aggregate_retention["policy_agg.weighted_sum"] = policy_aggregate_retention["agg_retention"] / policy_aggregate_retention["weighted_sum_ind_aggs"] 
    policy_aggregate_retention["policy_agg.weighted_sum"] = policy_aggregate_retention["policy_agg.weighted_sum"].fillna(0)
    # except:
    #     policy_aggregate_retention["policy_agg.weighted_sum"] = 0

    #Overall policy agg retention factor
    agg_retention_to_sum_of_agg_retention_table = hx.params.table_glsn_agg_retention 
    ratio_pol_retention_to_sum_individual =  agg_retention_to_sum_of_agg_retention_table["ratio_pol_agg_to_sum_individual"].to_numpy()
    ratio_pol_retention_to_sum_individual_factor_life_science =  agg_retention_to_sum_of_agg_retention_table["life_science"].to_numpy()    
    ratio_pol_retention_to_sum_individual_factor_nutra =  agg_retention_to_sum_of_agg_retention_table["nutra"].to_numpy() 

    # Determine which parameter column to use based on the form selected being BioSecure or NutraGuard. If neither of these, then base on the product selected. 
    if biosecure_product :
        policy_aggregate_retention["overall_policy_agg_factor"] = np.where(policy_aggregate_retention["agg_retention"].isna(),\
            1, np.interp(policy_aggregate_retention["policy_agg.weighted_sum"], ratio_pol_retention_to_sum_individual, ratio_pol_retention_to_sum_individual_factor_life_science))  
    else : 
        policy_aggregate_retention["overall_policy_agg_factor"] = np.where((policy_aggregate_retention["agg_retention"].isna()),\
            1, np.interp(policy_aggregate_retention["policy_agg.weighted_sum"], ratio_pol_retention_to_sum_individual, ratio_pol_retention_to_sum_individual_factor_nutra))


    contribution_to_sum_of_retentions = retentions.loc[:,["contribution_to_sum_of_aggs_product_liability",\
        "contribution_to_sum_of_aggs_eo",\
        "contribution_to_sum_of_aggs_healthcare_professional_liability",\
        "contribution_to_sum_of_aggs_general_liability",\
        "contribution_to_sum_of_aggs_sexual_abuse",\
        "contribution_to_sum_of_aggs_employee_benefits_liability",\
        "contribution_to_sum_of_aggs_product_recall",\
        "contribution_to_sum_of_aggs_well_tech_eo_media"]] 

    for coverage in ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media"]:
        contribution_to_sum_of_retentions[f"split_of_discount_{coverage}"] = 1 - ((1-policy_aggregate_retention["overall_policy_agg_factor"])* contribution_to_sum_of_retentions[f"contribution_to_sum_of_aggs_{coverage}"])

    split_of_discount_retentions = contribution_to_sum_of_retentions.loc[:,["split_of_discount_product_liability",\
        "split_of_discount_eo",\
        "split_of_discount_healthcare_professional_liability",\
        "split_of_discount_general_liability",\
        "split_of_discount_sexual_abuse",\
        "split_of_discount_employee_benefits_liability",\
        "split_of_discount_product_recall",\
        "split_of_discount_well_tech_eo_media"]]      


    timer.end("section 5")
    timer.start("section 6")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Set up ILF parameters 
    #--------------------------------------------------------------------------------------------------------------------------------#

    #Deductible parameters
    options_indemnity_only_dedctible = options.loc[:,["indemnity_only"]]
    indemnity_only_deductible_factor = hx.params.table_gmm_indemnity_ded_split["indemnity_defence_split"].iloc[0]
    
    #ILF parameters
    glsn_ilf_parameters = hx.params.table_glsn_parametric_ilfs
    if biosecure_product :
        a_1 = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "a1"]["biosecure"].iloc[0]
        b_1 = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "b1"]["biosecure"].iloc[0]
        threshold = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "threshold"]["biosecure"].iloc[0]
        a_2 = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "a2"]["biosecure"].iloc[0]
        b_2 = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "b2"]["biosecure"].iloc[0]
    else :
        a_1 = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "a1"]["nutraguard"].iloc[0]
        b_1 = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "b1"]["nutraguard"].iloc[0]
        threshold = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "threshold"]["nutraguard"].iloc[0]
        a_2 = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "a2"]["nutraguard"].iloc[0]
        b_2 = glsn_ilf_parameters[glsn_ilf_parameters["parameter"] == "b2"]["nutraguard"].iloc[0]
    
    #EEC ILF parameters
    ilf_table = hx.params.table_glsn_ilfs        
    ilf_lev = ilf_table["lev"].to_numpy()

    if biosecure_product:
        ilf_factor = ilf_table["biosecure"]
    else:
        ilf_factor = ilf_table["nutragard"]
    
    #AGG ILF parameters
    agg_to_eec_table = hx.params.table_glsn_agg_to_eec
    agg_eec_ratio = agg_to_eec_table["agg_eec"].to_numpy()
    agg_eec_factor_biosecure = agg_to_eec_table["biosecure"].to_numpy()
    agg_eec_factor_nutraguard = agg_to_eec_table["nutraguard"].to_numpy()      
    

    timer.end("section 6")
    timer.start("section 7")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # ILFs for each option and coverage
    #--------------------------------------------------------------------------------------------------------------------------------#

    # Primary
    # First for product liability
    primary_ilf_calcs = pd.DataFrame()    

    for coverage in ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media"]:
                
        # Workings for EEL ILF
        primary_ilf_calcs[f"{coverage}_attachment"] = np.where(retentions[f"coverages.{coverage}.retention"] * currency_factor <= threshold,\
            a_1 * (retentions[f"coverages.{coverage}.retention"] * currency_factor) ** b_1, \
            a_2 * (retentions[f"coverages.{coverage}.retention"] * currency_factor) ** b_2)

        primary_ilf_calcs[f"{coverage}_dettachment"] = np.where((retentions[f"coverages.{coverage}.retention"] + options[f"coverages.{coverage}.per_claim_limit"]) * currency_factor <= threshold,\
            a_1 * ((retentions[f"coverages.{coverage}.retention"] + options[f"coverages.{coverage}.per_claim_limit"]) * currency_factor) ** b_1, \
            a_2 * ((retentions[f"coverages.{coverage}.retention"] + options[f"coverages.{coverage}.per_claim_limit"]) * currency_factor) ** b_2)

        # Assuming always using parametric approach... which means the deductible factor never gets used
        # EEL ILF        
        primary_ilf_calcs[f"{coverage}_eec_ilf"] = primary_ilf_calcs[f"{coverage}_dettachment"] - primary_ilf_calcs[f"{coverage}_attachment"]

        # Workings for AGG ILF
        primary_ilf_calcs[f"{coverage}_agg_eec_ratio"] = options[f"coverages.{coverage}.aggregate_limit"] / options[f"coverages.{coverage}.per_claim_limit"]

        # AGG ILF
        if biosecure_product :
            primary_ilf_calcs[f"{coverage}_agg_ilf"] = np.interp(primary_ilf_calcs[f"{coverage}_agg_eec_ratio"], agg_eec_ratio, agg_eec_factor_biosecure)
        else:
            primary_ilf_calcs[f"{coverage}_agg_ilf"] = np.interp(primary_ilf_calcs[f"{coverage}_agg_eec_ratio"], agg_eec_ratio, agg_eec_factor_nutraguard)
    
    tech_eo_agg_limit_dict = [{
        "well_tech_eo_media_agg_ilf": item.tech_eo_agg_ilf_primary_factor,
    } for item in cds.options]   

    tech_eo_agg_limit_df = pd.DataFrame(tech_eo_agg_limit_dict) 
    primary_ilf_calcs["well_tech_eo_media_agg_ilf"] = tech_eo_agg_limit_df

    timer.end("section 7")
    timer.start("section 8")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary layer net premiums for each option and coverage
    #--------------------------------------------------------------------------------------------------------------------------------#

    for coverage in ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media"]:

        # Net premium calc by coverage         
        if (coverage == "well_tech_eo_media"):
            primary_layer_per_coverage["primary_layer_net_premium"] = tech_eo_primary_net_prem_usd["tech_eo_primary_net_prem_usd"] * \
                split_of_discount_retentions[f"split_of_discount_{coverage}"].fillna(1) * \
                split_of_discount[f"split_of_discount_{coverage}"].fillna(1)
        else:
            primary_layer_per_coverage["primary_layer_net_premium"] = total_base_primary_layer_per_coverage[f"primary_layer_base_premium_{coverage}_usd"] * \
                primary_ilf_calcs[f"{coverage}_eec_ilf"] * \
                primary_ilf_calcs[f"{coverage}_agg_ilf"] * \
                split_of_discount_retentions[f"split_of_discount_{coverage}"].fillna(1) * \
                split_of_discount[f"split_of_discount_{coverage}"].fillna(1)

        # check
        # total_base_primary_layer_per_coverage["primary_layer_base_premium_product_liability_usd"]
        # primary_ilf_calcs["product_liability_eec_ilf"]
        # primary_ilf_calcs["product_liability_agg_ilf"]
        # split_of_discount_retentions["split_of_discount_product_liability"].fillna(1)
        # split_of_discount["split_of_discount_product_liability"].fillna(1)

        # check
        # tech_eo_primary_net_prem_usd
        # split_of_discount_retentions["split_of_discount_well_tech_eo_media"].fillna(1)
        # split_of_discount["split_of_discount_well_tech_eo_media"].fillna(1)

        # Net premium including retro and schedule mods
        total_primary_layer_per_coverage[f"primary_layer_net_premium_{coverage}_usd"] = primary_layer_per_coverage["primary_layer_net_premium"] * total_schedule_mod_factor
        
    total_primary_layer_per_coverage["primary_premium_usd"] = total_primary_layer_per_coverage.sum(axis=1)                               


    # GL Premium for Umbrella
    if cds.rating_factors.pricing.general_liability.include_primary == True:
        gl_primary_premium = total_primary_layer_per_coverage["primary_layer_net_premium_general_liability_usd"] / currency_factor
        gl_primary_premium = gl_primary_premium.fillna(0)
        if cds.rating_factors.pricing.general_liability.claims_basis == "Occurrence" and cds.rating_factors.pricing.general_liability.include_excess == True and cds.rating_factors.glsn.umbrella.general_liability.occurrence_cover == True:
            for index, option in enumerate(cds.options):
                setattr(getattr(option, "glsn_general_liability"),"premium_primary", gl_primary_premium[index])
        else: 
            for index, option in enumerate(cds.options):
                setattr(getattr(option, "glsn_general_liability"),"premium_primary", 0)
    else: 
            for index, option in enumerate(cds.options):
                setattr(getattr(option, "glsn_general_liability"),"premium_primary", 0)

    timer.end("section 8")
    timer.start("section 9")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary Premium: Coverage Enhancments - note we have a "base" for each one, which is calculated on the base premium rather than the at limits premium. This is used for the excess layer pricing. 
    #--------------------------------------------------------------------------------------------------------------------------------#        
    total_primary_layer_enhancements = pd.DataFrame()        

    # Stop Gap        
    stop_gap = options["include_stop_gap_primary"] * total_primary_layer_per_coverage["primary_premium_usd"] * stop_gap_additional_coverage_value
    total_base_primary_layer_per_coverage["stop_gap_base"] = total_base_primary_layer_per_coverage["primary_base_premium_exc_retro_usd"] * stop_gap_additional_coverage_value
    total_primary_layer_enhancements["stop_gap_premium"] = np.where(stop_gap.isna() ,0 ,stop_gap)

    # TRIA
    tria_min = hx.params.table_glsn_tria_min["tria_min_prem"].iloc[0]
    tria = np.maximum(tria_min * options["include_tria_primary"], options["include_tria_primary"] * total_primary_layer_per_coverage["primary_premium_usd"] * tria_additional_coverage_value)
    total_base_primary_layer_per_coverage["tria_base"] = np.maximum(tria_min, total_base_primary_layer_per_coverage["primary_base_premium_exc_retro_usd"]  * tria_additional_coverage_value)
    total_primary_layer_enhancements["tria_premium"] = np.where(tria.isna() ,0 ,tria)


    # Punitive Damages
    punitive_damages =  options["include_punitive_damages_primary"] * total_primary_layer_per_coverage["primary_premium_usd"] * punitive_damages_additional_coverage_value
    punitive_damages_base = total_base_primary_layer_per_coverage["primary_base_premium_exc_retro_usd"] * punitive_damages_additional_coverage_value
    total_primary_layer_enhancements["punitive_damages_premium"] = np.where(punitive_damages.isna() ,0 ,punitive_damages)

    # Costs in Addition
    costs_in_addition_table = hx.params.table_gmm_costs_in_addition
    costs_in_addition_selection = pd.DataFrame(options["costs_in_addition_selection"])
    costs_in_addition_primary = costs_in_addition_selection.merge(costs_in_addition_table, left_on = "costs_in_addition_selection", right_on = "costs_in_addition", how="left")
    
    costs_in_addition = options["include_costs_in_addition_primary"] * costs_in_addition_primary["debit"] * total_primary_layer_per_coverage["primary_premium_usd"]
    total_base_primary_layer_per_coverage["costs_in_addition_base"] = costs_in_addition_primary["debit"] * total_base_primary_layer_per_coverage["primary_base_premium_exc_retro_usd"]
    total_primary_layer_enhancements["costs_in_addition_premium"] = np.where(costs_in_addition.isna() ,0 ,costs_in_addition)

    #Auto HNOA
    auto_hnoa_base_rate = hx.params.table_gmm_auto_hnoa_base_rate["auto_base_prem"].iloc[0]
    auto_selection = options.loc[:,["include_auto_primary","auto_measure","auto_amount"]]
    auto_selection["auto_amount"] = np.where(auto_selection["auto_amount"].isna(), 0, auto_selection["auto_amount"])

    auto_hnoa = np.where(auto_selection["auto_measure"] == "Mileage", auto_selection["auto_amount"]/10000, auto_selection["auto_amount"]) * auto_hnoa_base_rate * auto_selection["include_auto_primary"]
    total_base_primary_layer_per_coverage["auto_hnoa_base"] = np.where(auto_selection["auto_measure"] == "Mileage", auto_selection["auto_amount"]/10000, auto_selection["auto_amount"]) * auto_hnoa_base_rate
    total_primary_layer_enhancements["auto_premium"] = np.where(auto_hnoa.isna() ,0 ,auto_hnoa)

    #Sum up the total enhancments - gives the total primary premium layer
    total_primary_layer_premium = pd.DataFrame()
    total_primary_layer_premium["net_model_premium"] = total_primary_layer_per_coverage["primary_premium_usd"]\
        + total_primary_layer_enhancements["stop_gap_premium"] \
        + total_primary_layer_enhancements["tria_premium"] \
        + total_primary_layer_enhancements["punitive_damages_premium"] \
        + total_primary_layer_enhancements["costs_in_addition_premium"] \
        + total_primary_layer_enhancements["auto_premium"]


    timer.end("section 9")
    timer.start("section 10")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary Premium: Minimum Premium Calculations
    #--------------------------------------------------------------------------------------------------------------------------------#
    minimum_eel = pd.DataFrame()
    minimum_agg = pd.DataFrame()        
    minimum_prem = pd.DataFrame()

    glsn_minimum_prem_table = hx.params.table_glsn_minimum_premium
    
    # Extract EEL and AGG limits to be used in minimum premium calculations
    for coverage in ["product_liability","eo","healthcare_professional_liability", "well_tech_eo_media"]:
        # Extract EEL and AAL            
        minimum_eel[f"{coverage}"] = options[f"coverages.{coverage}.per_claim_limit"].fillna(0)
        minimum_agg[f"{coverage}"] = options[f"coverages.{coverage}.aggregate_limit"].fillna(0)
    
    # if block eo, choose well_tech_eo_media, otherwise choose eo
    if (block_eo == True):
        minimum_eel.drop("eo", axis = 1)
        minimum_agg.drop("eo", axis = 1)
    else:
        minimum_eel.drop("well_tech_eo_media", axis = 1)
        minimum_agg.drop("well_tech_eo_media", axis = 1)

    # Get the MAX EEL and AGG to be used for minimum premium calculations
    # Note that the max EEL determines which AGG limit to take, so we have to look up the coverage which the max EEL comes from and use that to work out the aggregate limit to use for min calcs
    minimum_prem["eel_for_min"] = minimum_eel.max(axis = 1) * currency_factor
    max_eel_coverage = minimum_eel.idxmax(axis=1)
    minimum_prem["agg_for_min"] = [minimum_agg.loc[index, max_eel_coverage[index]] for index in range(len(max_eel_coverage))] 
    minimum_prem["agg_for_min"] = minimum_prem["agg_for_min"] * currency_factor
    

    # Join on minimum premium parameters
    minimum_prem["AGGLimStep"] = glsn_minimum_prem_table[glsn_minimum_prem_table["Level"] == "MinimumPremiumAGGLimStep"]["Parameter"].iloc[0]
    minimum_prem["AGGMinStep"] = glsn_minimum_prem_table[glsn_minimum_prem_table["Level"] == "MinimumPremiumAGGMinStep"]["Parameter"].iloc[0]
    minimum_prem["Base"] = glsn_minimum_prem_table[glsn_minimum_prem_table["Level"] == "MinimumPremiumBase"]["Parameter"].iloc[0]
    minimum_prem["BaseAGGLim"] = glsn_minimum_prem_table[glsn_minimum_prem_table["Level"] == "MinimumPremiumBaseAGGLim"]["Parameter"].iloc[0]
    minimum_prem["BaseEELLim"] = glsn_minimum_prem_table[glsn_minimum_prem_table["Level"] == "MinimumPremiumBaseEECLim"]["Parameter"].iloc[0]
    minimum_prem["EELLimStep"] = glsn_minimum_prem_table[glsn_minimum_prem_table["Level"] == "MinimumPremiumEECLimStep"]["Parameter"].iloc[0]
    minimum_prem["EELMinStep"] = glsn_minimum_prem_table[glsn_minimum_prem_table["Level"] == "MinimumPremiumEECMinStep"]["Parameter"].iloc[0]

    # Work out minimum prem, which is based on a base + incremental step depending on EEL and AGG               
    minimum_prem["min_prem_usd"] = np.where(minimum_prem.sum(axis = 1) == 0, \
        0, \
            np.where(minimum_prem["eel_for_min"] <= minimum_prem["BaseEELLim"], \
                np.where(minimum_prem["agg_for_min"] <= minimum_prem["BaseAGGLim"], \
                    minimum_prem["Base"], \
                        minimum_prem["Base"] + ((minimum_prem["agg_for_min"] - minimum_prem["BaseAGGLim"]) / minimum_prem["AGGLimStep"])* minimum_prem["AGGMinStep"]), \
                            minimum_prem["Base"] + ((minimum_prem["eel_for_min"] - minimum_prem["BaseEELLim"]) / minimum_prem["EELLimStep"]) * minimum_prem["EELMinStep"] + \
                            ((minimum_prem["agg_for_min"] - minimum_prem["eel_for_min"]) / minimum_prem["AGGLimStep"]) * minimum_prem["AGGMinStep"]))

    
    # Minimum Premium
    if (np.sum(glsn_class_table["selection"]) < 1 or venue_factor == 0):
        minimum_prem["minimum_premium_primary"] = 0
    else:
        minimum_prem["minimum_premium_primary"] = minimum_prem["min_prem_usd"] / currency_factor

    # write to cds
    minimum_prem = minimum_prem.fillna(0)
    minimum_prem = pd.concat([minimum_prem, policy_aggregate["agg_limit"]], axis=1)
    minimum_prem["minimum_premium_primary"] = np.where(minimum_prem["agg_limit"] == 0 , 0 , minimum_prem["minimum_premium_primary"])
    utils.write_pd_to_hxd(minimum_prem,cds.options,["minimum_premium_primary"])

    
    timer.end("section 10")
    timer.start("section 11")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Primary Gross Premium: Total Calculations
    #--------------------------------------------------------------------------------------------------------------------------------#   
    
    ###################
    # IR edit 22/12 ---

    # Pull in technical premium parameters from user library 
    tp_params = params.tp_parameters.df()

    # To stop the model erroring if the inception year defaults to a year not in the TP data
    yoa = hxd.hx_core.inception_date.year
    tp_year = yoa if yoa in tp_params["year"].values else tp_params["year"].max()

    # ML edit 07/09/26 ---
    # Business parameters --------       
    # Pull the right business class parameters
    if (us_international == "International"):
        if (tp_year <= 2025):
            bp_class = "Intl Misc Med (London)"
        else:
            bp_class = "Intl Misc Med & Life Sciences"
    else:
        bp_class = "US Misc Med"  
    # End of ML edit --- 

    tp_lookup_bool = (tp_params['business_plan_class'] == bp_class) & (tp_params['year'] == tp_year)
    tp_params_df = tp_params[tp_lookup_bool]

    # end of IR edit 22/12 ---
    #############

    # nmp_load
    nmp_load = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['nmp_load'].iloc[0]            

    # Brokerage
    brokerage = options.loc[:,"brokerage_primary"].fillna(0) 

    # Total Gross Premium
    total_gross_model_premium = pd.DataFrame()        

    # Missing Cyber
    total_gross_model_premium["model_premium_primary_excl_NMP"] = (total_primary_layer_premium["net_model_premium"] / currency_factor) / (1-brokerage)

    # Cyber gross premium
    if cyber_selection:
        total_gross_model_premium["model_premium_primary_excl_NMP"]  = total_gross_model_premium["model_premium_primary_excl_NMP"] + options["cyber_premium_primary"]

    #  Add on NMP
    total_gross_model_premium["model_premium_primary"] = total_gross_model_premium["model_premium_primary_excl_NMP"] * (1 + nmp_load)
    total_gross_model_premium["uplift_for_nmp_primary"] = total_gross_model_premium["model_premium_primary"] - total_gross_model_premium["model_premium_primary_excl_NMP"]

    total_gross_model_premium["gross_premium_primary"] = np.maximum(total_gross_model_premium["model_premium_primary"], minimum_prem["minimum_premium_primary"])

    # write to cds
    #utils.write_pd_to_hxd(total_gross_model_premium,cds.options,["model_premium_primary","gross_premium_primary"])
    #utils.write_pd_to_hxd(total_gross_model_premium,cds.options,["gross_premium_primary"])


    # Calculating benchmark premium and BPIs    
    priced_to_net_loss_ratio = hx.params.table_glsn_priced_to_net_lr.loc[:,"loss_ratio"].iloc[0]
    benchmark_loss_ratio = hx.params.table_benchmark_lr.loc[:,"loss_ratio"].iloc[0]

    # Eventually this calc will need to change to the model premium including the cyber coverage
    primary_benchmark_premium = total_gross_model_premium["gross_premium_primary"] * (priced_to_net_loss_ratio / benchmark_loss_ratio)

    primary_quoted_premium = options.loc[:,"quoted_premium_primary"]
    primary_quoted_premium = np.where(primary_quoted_premium.isna(), 0 , primary_quoted_premium)
    
            
    # try:
    total_gross_model_premium["bpi_primary"] = [q / b if b != 0 else 0 for q, b in zip(primary_quoted_premium, primary_benchmark_premium)] 
    total_gross_model_premium["bpi_primary"] = total_gross_model_premium["bpi_primary"].fillna(0)
    # except:
    #     total_gross_model_premium["bpi_primary"] = [0] * len(options)
    total_gross_model_premium = total_gross_model_premium.fillna(0)
    utils.write_pd_to_hxd(total_gross_model_premium,cds.options,["model_premium_primary", "uplift_for_nmp_primary", "gross_premium_primary", "bpi_primary"])


    timer.end("section 11")
    timer.start("section 12")
    #--------------------------------------------------------------------------------------------------------------------------------#
    # Excess Layer Pricing 
    #--------------------------------------------------------------------------------------------------------------------------------#          
    for layer in range(1,11):
        setattr(cds.rating_factors.pricing, f"claims_basis_{layer}_excess", "Claims-Made")
        setattr(getattr(cds.rating_factors.pricing, f"retroactive_date_{layer}_excess"), "calculated", default_excess_retro_date)
    # Primary base premiums to be used in excess priicng
    base_premiums_per_coverage = total_base_primary_layer_per_coverage

    # AGG/EEC ratios and factors
    excess_agg_to_eec = hx.params.table_glsn_excess_agg_to_eec

    excess_agg_eec_ratio = excess_agg_to_eec["agg_eec"].to_numpy()
    if (biosecure_product == True):          
        excess_agg_eec_factor = excess_agg_to_eec["biosecure"].to_numpy()
    else:
        excess_agg_eec_factor = excess_agg_to_eec["nutraguard"].to_numpy()        

    # Include in excess flag
    include_excess = []

    for coverage in ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media"]:        
        include_excess_value = getattr(getattr(cds.rating_factors.pricing , coverage),"include_excess")
        include_excess.append(include_excess_value)
            
    for coverage in ["stop_gap","tria","punitive_damages","costs_in_addition","auto"]:
        include_excess_value = getattr(cds.rating_factors.pricing , f"include_{coverage}_excess")
        include_excess.append(include_excess_value)

    coverage_excess = pd.Series(["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media","stop_gap","tria","punitive_damages","costs_in_addition","auto"])
    include_excess= pd.Series(include_excess)
    excess_coverages = pd.DataFrame({"coverage": coverage_excess, "include_excess": include_excess}) 
        
    # Retro factor calcs
    excess_layers = ["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"]
    excess_retro_date = [getattr(getattr(cds.rating_factors.pricing , f"retroactive_date_{layer}"),"selected") for layer in excess_layers]
    excess_retro_years = [int(utils.policy_term(excess_retroactive_date, inception_date)) if excess_retroactive_date and utils.policy_term(excess_retroactive_date, inception_date) - int(utils.policy_term(excess_retroactive_date, inception_date)) < 0.01 else math.ceil(utils.policy_term(excess_retroactive_date, inception_date)) if excess_retroactive_date else None for excess_retroactive_date in excess_retro_date]
    excess_retro_factor = [retro_table[retro_table["retro_years"] == excess_retroactive_years]["factor"].iloc[0] if not retro_table[retro_table["retro_years"] == excess_retroactive_years].empty else 1 for excess_retroactive_years in excess_retro_years]


    excess_layer = pd.Series(["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])
    excess_retro_date = pd.Series(excess_retro_date)
    excess_retro_years = pd.Series(excess_retro_years)
    excess_retro_factor = pd.Series(excess_retro_factor)

    excess_layer_non_option = pd.DataFrame({"layer": excess_layer, "excess_retroactive_date": excess_retro_date, "excess_retroactive_years": excess_retro_years, "excess_retroactive_factor": excess_retro_factor})

    # Excess options
    excess_options = pd.DataFrame()

    # Significance weighting

    excess_options["product_liability_significant_weighting"] = pd.Series(product_liability_signficant_coverage_per_option)
    #EO signficant coverage per option defined earlier based on whether we block eo or not
    if block_eo : 
        excess_options["well_tech_eo_media_significant_weighting"] = pd.Series(eo_signficant_coverage_per_option)
    else:
        excess_options["eo_significant_weighting"] = pd.Series(eo_signficant_coverage_per_option)
    
    excess_options["healthcare_professional_liability_significant_weighting"] = pd.Series(hpl_signficant_coverage_per_option)        
    
    excess_options["number_of_significant_weighting"] = excess_options.sum(axis = 1)

    # Primary Limits, Retention and Aggregate Adjustments to be used in Excess calcs
    if block_eo:
        sig_coverages = ["product_liability","healthcare_professional_liability","well_tech_eo_media"]     
    else:
        sig_coverages = ["product_liability","eo","healthcare_professional_liability"]
    
    for coverage in sig_coverages:        

        excess_options[f"{coverage}_per_claim_limit"] = options[f"coverages.{coverage}.per_claim_limit"]
        excess_options[f"{coverage}_retention"] = retentions[f"coverages.{coverage}.retention"]
        excess_options[f"{coverage}_agg_ilf"] = primary_ilf_calcs[f"{coverage}_agg_ilf"]

        excess_options[f"{coverage}_per_claim_limit_weighted"] = excess_options[f"{coverage}_per_claim_limit"] * excess_options[f"{coverage}_significant_weighting"]
        excess_options[f"{coverage}_retention_weighted"] = excess_options[f"{coverage}_retention"] * excess_options[f"{coverage}_significant_weighting"]
        excess_options[f"{coverage}_agg_ilf_weighted"] = excess_options[f"{coverage}_agg_ilf"] * excess_options[f"{coverage}_significant_weighting"]

    if block_eo:
        excess_options = excess_options.rename(columns = {"well_tech_eo_media_per_claim_limit":"eo_per_claim_limit","well_tech_eo_media_retention":"eo_retention", "well_tech_eo_media_agg_ilf":"eo_agg_ilf", \
          "well_tech_eo_media_per_claim_limit_weighted":"eo_per_claim_limit_weighted","well_tech_eo_media_retention_weighted":"eo_retention_weighted", "well_tech_eo_media_agg_ilf_weighted":"eo_agg_ilf_weighted"  })

    # NANs introduced if one of the coverages above is not selected, so have to fill NAs with zero to prevent follow through errors 
    excess_options = excess_options.fillna(0)

    # per claim limit  x significant weighting for each option
    excess_options["total_per_claim_limit_weighted"] = excess_options["product_liability_per_claim_limit_weighted"] + \
        excess_options["eo_per_claim_limit_weighted"] + \
            excess_options["healthcare_professional_liability_per_claim_limit_weighted"]

    # retention x significant weighting for each option
    excess_options["total_retention_weighted"] = excess_options["product_liability_retention_weighted"] + \
        excess_options["eo_retention_weighted"] + \
            excess_options["healthcare_professional_liability_retention_weighted"]

    # agg ilf x significant weighting for each option
    excess_options["total_agg_ilf_weighted"] = excess_options["product_liability_agg_ilf_weighted"] + \
        excess_options["eo_agg_ilf_weighted"] + \
            excess_options["healthcare_professional_liability_agg_ilf_weighted"]
    
    # Primary limits, retention and aggregate adjustments used for excess

    # try:
    excess_options["primary_limit_for_xs"] = excess_options["total_per_claim_limit_weighted"] / excess_options["number_of_significant_weighting"]
    excess_options["primary_limit_for_xs"] = excess_options["primary_limit_for_xs"].fillna(0)
    # except:
    #     excess_options["primary_limit_for_xs"] = [0] * len(options)

    # try:
    excess_options["primary_retention_for_xs"] = excess_options["total_retention_weighted"] / excess_options["number_of_significant_weighting"]
    excess_options["primary_retention_for_xs"] = excess_options["primary_retention_for_xs"].fillna(0)
    # except:
    #     excess_options["primary_retention_for_xs"] = [0] * len(options)

    # try:
    excess_options["agg_ilf_for_xs"] = excess_options["total_agg_ilf_weighted"] / excess_options["number_of_significant_weighting"]
    excess_options["agg_ilf_for_xs"] = excess_options["agg_ilf_for_xs"].fillna(1)
    # except:
    #     excess_options["agg_ilf_for_xs"] = [1] * len(options)     
    
    # Looping through all the layers to get the attachment, dettachment points and calculate the agg ILF for each point
    layers_table = options.loc[:,["per_claim_limit_1_excess","aggregate_limit_1_excess",\
        "per_claim_limit_2_excess","aggregate_limit_2_excess",\
        "per_claim_limit_3_excess","aggregate_limit_3_excess",\
        "per_claim_limit_4_excess","aggregate_limit_4_excess",\
        "per_claim_limit_5_excess","aggregate_limit_5_excess",\
        "per_claim_limit_6_excess","aggregate_limit_6_excess",\
        "per_claim_limit_7_excess","aggregate_limit_7_excess",\
        "per_claim_limit_8_excess","aggregate_limit_8_excess",\
        "per_claim_limit_9_excess","aggregate_limit_9_excess",\
        "per_claim_limit_10_excess","aggregate_limit_10_excess"]]

    excess_table = pd.DataFrame()
    excess_table["attachment_1_excess"] = excess_options["primary_limit_for_xs"]
    excess_table["primary_retention"] = excess_options["primary_retention_for_xs"]
    excess_table["dettachment_1_excess"] = excess_table["attachment_1_excess"] + layers_table["per_claim_limit_1_excess"]
    excess_table["dettachment_plus_retention_1_excess"] = (excess_table["primary_retention"] + excess_table["dettachment_1_excess"]) 
    excess_table["attachment_plus_retention_1_excess"] = (excess_table["primary_retention"] + excess_table["attachment_1_excess"]) 

    # First excess layer
    excess_table["attachment_ilf_1_excess"] = np.where(excess_table["attachment_1_excess"] * currency_factor <= threshold,\
            a_1 * (excess_table["attachment_plus_retention_1_excess"] * currency_factor) ** b_1, \
            a_2 * (excess_table["attachment_plus_retention_1_excess"] * currency_factor) ** b_2)

    excess_table["dettachment_ilf_1_excess"] = np.where((excess_table["dettachment_1_excess"]) * currency_factor <= threshold,\
            a_1 * ((excess_table["dettachment_plus_retention_1_excess"]) * currency_factor) ** b_1, \
            a_2 * ((excess_table["dettachment_plus_retention_1_excess"]) * currency_factor) ** b_2)

    # always using parametric approach
    excess_table["unlimited_ilf_1_excess"] = excess_table["dettachment_ilf_1_excess"] - excess_table["attachment_ilf_1_excess"]
    excess_table["agg_to_eel_ratio_1_excess"] = layers_table["aggregate_limit_1_excess"] / layers_table["per_claim_limit_1_excess"]
    excess_table["agg_ecc_factor_1_excess"] = np.interp(excess_table["agg_to_eel_ratio_1_excess"] , excess_agg_eec_ratio, excess_agg_eec_factor)
    excess_table["cumulative_agg_ecc_factor_1_excess"] = excess_options["agg_ilf_for_xs"]

    # try:
    excess_table["ilf_agg_1_excess"] = (excess_table["agg_ecc_factor_1_excess"] / excess_table["cumulative_agg_ecc_factor_1_excess"]) * excess_table["unlimited_ilf_1_excess"]
    excess_table["ilf_agg_1_excess"] = excess_table["ilf_agg_1_excess"].fillna(0)
    # except:
    #     excess_table["ilf_agg_1_excess"] =  0

    for layer in range(2,11) :
        excess_table[f"attachment_{layer}_excess"] = excess_table[f"attachment_{layer-1}_excess"] + layers_table[f"per_claim_limit_{layer-1}_excess"]
        excess_table[f"dettachment_{layer}_excess"] = excess_table[f"attachment_{layer}_excess"] + layers_table[f"per_claim_limit_{layer}_excess"]

        excess_table[f"dettachment_plus_retention_{layer}_excess"] = (excess_table["primary_retention"] + excess_table[f"dettachment_{layer}_excess"]) 
        excess_table[f"attachment_plus_retention_{layer}_excess"] = (excess_table["primary_retention"] + excess_table[f"attachment_{layer}_excess"])        

        excess_table[f"attachment_ilf_{layer}_excess"] = np.where(excess_table[f"attachment_{layer}_excess"] * currency_factor <= threshold,\
            a_1 * (excess_table[f"attachment_plus_retention_{layer}_excess"] * currency_factor) ** b_1, \
            a_2 * (excess_table[f"attachment_plus_retention_{layer}_excess"] * currency_factor) ** b_2)

        excess_table[f"dettachment_ilf_{layer}_excess"] = np.where((excess_table[f"dettachment_{layer}_excess"]) * currency_factor <= threshold,\
            a_1 * ((excess_table[f"dettachment_plus_retention_{layer}_excess"]) * currency_factor) ** b_1, \
            a_2 * ((excess_table[f"dettachment_plus_retention_{layer}_excess"]) * currency_factor) ** b_2)

        excess_table[f"unlimited_ilf_{layer}_excess"] = excess_table[f"dettachment_ilf_{layer}_excess"] - excess_table[f"attachment_ilf_{layer}_excess"]

        excess_table[f"agg_to_eel_ratio_{layer}_excess"] = layers_table[f"aggregate_limit_{layer}_excess"] / layers_table[f"per_claim_limit_{layer}_excess"]
        excess_table[f"agg_ecc_factor_{layer}_excess"] = np.interp(excess_table[f"agg_to_eel_ratio_{layer}_excess"] , excess_agg_eec_ratio, excess_agg_eec_factor)
        excess_table[f"cumulative_agg_ecc_factor_{layer}_excess"] = excess_table[f"cumulative_agg_ecc_factor_{layer-1}_excess"] * excess_table[f"agg_ecc_factor_{layer-1}_excess"]

        # try:
        excess_table[f"ilf_agg_{layer}_excess"] = (excess_table[f"agg_ecc_factor_{layer}_excess"] / excess_table[f"cumulative_agg_ecc_factor_{layer}_excess"]) * excess_table[f"unlimited_ilf_{layer}_excess"]
        excess_table[f"ilf_agg_{layer}_excess"] = excess_table[f"ilf_agg_{layer}_excess"].fillna(0)
        # except:
        #     excess_table[f"ilf_agg_{layer}_excess"] =  0

    excess_ilfs = excess_table.loc[:,["ilf_agg_1_excess","ilf_agg_2_excess","ilf_agg_3_excess","ilf_agg_4_excess","ilf_agg_5_excess","ilf_agg_6_excess","ilf_agg_7_excess","ilf_agg_8_excess","ilf_agg_9_excess","ilf_agg_10_excess"]]  
    excess_ilfs = excess_ilfs.replace(np.inf, 0)

    check = excess_table.loc[:,["unlimited_ilf_1_excess", "unlimited_ilf_2_excess", "unlimited_ilf_3_excess", "ilf_agg_1_excess","ilf_agg_2_excess","ilf_agg_3_excess"]]
    excess_premium = pd.DataFrame()

    # Validatation error to show if including in excess but not primary
    primary_include = non_option_coverages[["coverage","include_primary"]]
    merged_includes = primary_include.merge(excess_coverages,how='left')
    merged_includes["error_catch"] = np.where((merged_includes["include_excess"] == True) & (merged_includes["include_primary"] == False), True, False )
    if merged_includes["error_catch"].sum() > 0:
        hx.errors.validation("Coverages must be included in primary to be included in excess")
    
    
    # Excess premium - exclude the Tech E&O as this will be created from Tech E&O rating function     
    for layer in range (1,11) : 
        for coverage in ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall"]:
            include_coverage_excess = excess_coverages[excess_coverages["coverage"] == coverage]["include_excess"].iloc[0]
            if include_coverage_excess:                   
                retro_excess = excess_layer_non_option[excess_layer_non_option["layer"] == f"{layer}_excess"]["excess_retroactive_factor"].iloc[0]
                primary_base_premium_usd = base_premiums_per_coverage[f"primary_layer_base_premium_{coverage}_exc_retro_usd"]
                excess_ilf_factor = excess_ilfs[f"ilf_agg_{layer}_excess"]
                excess_premium[f"premium_{layer}_excess_{coverage}_usd"] = primary_base_premium_usd * excess_ilf_factor * retro_excess * total_schedule_mod_factor   
            else:
                excess_premium[f"premium_{layer}_excess_{coverage}_usd"] = [0] * len(options)
                

    # Excess premium - Tech EO excess Layer
    for layer in range (1, 11):
        include_coverage_excess = excess_coverages[excess_coverages["coverage"] == "well_tech_eo_media"]["include_excess"].iloc[0]
        if include_coverage_excess:
            tech_eo_excess_temp = []
            for index, item in enumerate(cds.options):
                tech_eo_excess_temp.append(getattr(item,f"tech_eo_net_premium_usd_{layer}_excess" ))
            retro_excess = excess_layer_non_option[excess_layer_non_option["layer"] == f"{layer}_excess"]["excess_retroactive_factor"].iloc[0]
            tech_eo_excess_temp = [x * retro_excess * policy_term * number_significant_coverages["well_tech_eo_media_sig_coverage_factor"].iloc[0] * total_schedule_mod_factor for x in tech_eo_excess_temp]
            excess_premium[f"premium_{layer}_excess_well_tech_eo_media_usd"] = tech_eo_excess_temp
        else:                  
            excess_premium[f"premium_{layer}_excess_well_tech_eo_media_usd"] = [0] * len(options)


    #Gross total premiums excluding enhancments
    excess_premium_totals_excl_enhancments = pd.DataFrame()
    for layer in range (1,11):
        excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_excess_usd"] = excess_premium[f"premium_{layer}_excess_product_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_eo_usd"] + \
            excess_premium[f"premium_{layer}_excess_healthcare_professional_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_general_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_sexual_abuse_usd"] + \
            excess_premium[f"premium_{layer}_excess_employee_benefits_liability_usd"] + \
            excess_premium[f"premium_{layer}_excess_product_recall_usd"] + \
            excess_premium[f"premium_{layer}_excess_well_tech_eo_media_usd"]

    # For checking
    # excess_premium["premium_3_excess_product_liability_usd"]
    # excess_premium["premium_3_excess_eo_usd"]
    # excess_premium["premium_3_excess_healthcare_professional_liability_usd"] 
    # excess_premium["premium_3_excess_general_liability_usd"]
    # excess_premium["premium_3_excess_sexual_abuse_usd"]
    # excess_premium["premium_3_excess_employee_benefits_liability_usd"] 
    # excess_premium["premium_3_excess_product_recall_usd"]
    # excess_premium["premium_3_excess_well_tech_eo_media_usd"]        


    # Pricing Excess Coverage Enhancments
    include_stop_gap_excess = excess_coverages[excess_coverages["coverage"] == "stop_gap"]["include_excess"].iloc[0]
    include_tria_excess = excess_coverages[excess_coverages["coverage"] == "tria"]["include_excess"].iloc[0]
    include_punitive_damages_excess = excess_coverages[excess_coverages["coverage"] == "punitive_damages"]["include_excess"].iloc[0]
    include_costs_in_addition_excess = excess_coverages[excess_coverages["coverage"] == "costs_in_addition"]["include_excess"].iloc[0]
    include_auto_excess = excess_coverages[excess_coverages["coverage"] == "auto"]["include_excess"].iloc[0]
    coverage_enhancments_excess_premiums = pd.DataFrame()

    for layer in range (1,11):
        coverage_enhancments_excess_premiums[f"excess_{layer}_stop_gap_usd"] = include_stop_gap_excess * excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_excess_usd"] * stop_gap_additional_coverage_value
        coverage_enhancments_excess_premiums[f"excess_{layer}_tria_usd"] = include_tria_excess * np.maximum(excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_excess_usd"] * tria_additional_coverage_value , tria_min)
        coverage_enhancments_excess_premiums[f"excess_{layer}_punitive_damages_usd"] = include_punitive_damages_excess * excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_excess_usd"] * punitive_damages_additional_coverage_value
        coverage_enhancments_excess_premiums[f"excess_{layer}_costs_in_addition_usd"] = include_costs_in_addition_excess * excess_premium_totals_excl_enhancments[f"supported_excess_premium_{layer}_excess_usd"] * costs_in_addition_primary["debit"]
        coverage_enhancments_excess_premiums[f"excess_{layer}_auto_usd"] = include_auto_excess * base_premiums_per_coverage["auto_hnoa_base"]   * excess_ilfs[f"ilf_agg_{layer}_excess"]


    # For checking
    # coverage_enhancments_excess_premiums["excess_1_stop_gap"] = include_stop_gap_excess * excess_premium_totals_excl_enhancments["supported_excess_premium_1_excess"] * stop_gap_additional_coverage_value
    # coverage_enhancments_excess_premiums["excess_1_tria"] = include_tria_excess * np.maximum(excess_premium_totals_excl_enhancments["supported_excess_premium_1_excess"] * tria_additional_coverage_value , tria_min)
    # coverage_enhancments_excess_premiums["excess_1_punitive_damages"] = include_punitive_damages_excess * excess_premium_totals_excl_enhancments["supported_excess_premium_1_excess"] * punitive_damages_additional_coverage_value
    # coverage_enhancments_excess_premiums["excess_1_costs_in_addition"] = include_costs_in_addition_excess * excess_premium_totals_excl_enhancments["supported_excess_premium_1_excess"] * costs_in_addition_primary["debit"]
    # coverage_enhancments_excess_premiums["excess_1_auto"] = include_auto_excess * base_premiums_per_coverage["auto_hnoa_base"]   * excess_ilfs["ilf_agg_1_excess"]
    # coverage_enhancments_excess_premiums["excess_1_stop_gap"]
    # coverage_enhancments_excess_premiums["excess_1_tria"]
    # coverage_enhancments_excess_premiums["excess_1_punitive_damages"]
    # coverage_enhancments_excess_premiums["excess_1_costs_in_addition"]
    # coverage_enhancments_excess_premiums["excess_1_auto"]

    excess_premium_totals_enhancments = pd.DataFrame()
    for layer in range (1,11):            
        excess_premium_totals_enhancments[f"supported_excess_premium_{layer}_excess_usd"] = coverage_enhancments_excess_premiums[f"excess_{layer}_stop_gap_usd"] + \
            coverage_enhancments_excess_premiums[f"excess_{layer}_tria_usd"]  + \
            coverage_enhancments_excess_premiums[f"excess_{layer}_punitive_damages_usd"] + \
            coverage_enhancments_excess_premiums[f"excess_{layer}_costs_in_addition_usd"] + \
            coverage_enhancments_excess_premiums[f"excess_{layer}_auto_usd"]
                                
    # Convert to local currency
    support_excess_premium = excess_premium_totals_enhancments.add(excess_premium_totals_excl_enhancments,fill_value=0).fillna(0) / currency_factor                        
    support_excess_premium.columns = support_excess_premium.columns.str.replace('_usd','')             
    support_excess_premium = support_excess_premium.fillna(0)
    
    # cyber excess premium to add here and gross up the supported excess premium here
    cyber_excess_selection = cds.rating_factors.cyber.include_excess
    brokerage_excess = pd.DataFrame()
    if cyber_selection and cyber_excess_selection:
        cyber_options_df = utils.pd_df_from_hx_list(cds.cyber_options)
        for layer in range(1,11):
            # Brokerage
            brokerage_excess[f"brokerage_{layer}_excess"] = options.loc[:,f"brokerage_{layer}_excess"].fillna(0) 
            support_excess_premium[f"supported_excess_premium_{layer}_excess"] = support_excess_premium[f"supported_excess_premium_{layer}_excess"] / (1 - brokerage_excess[f"brokerage_{layer}_excess"]) + \
                cyber_options_df[f"model_premium_third_party_{layer}_excess"]
    else:
        for layer in range(1,11):
            brokerage_excess[f"brokerage_{layer}_excess"] = options.loc[:,f"brokerage_{layer}_excess"].fillna(0) 
            support_excess_premium[f"supported_excess_premium_{layer}_excess"] = support_excess_premium[f"supported_excess_premium_{layer}_excess"] / (1 - brokerage_excess[f"brokerage_{layer}_excess"]) 
            

    
    # GL Premium for Umbrella
    gl_excess_premium = excess_premium.filter(like="general_liability") 
    gl_excess_premium.columns = gl_excess_premium.columns.str.replace("_usd","") 
    gl_excess_premium = gl_excess_premium / currency_factor

    if cds.rating_factors.pricing.general_liability.claims_basis == "Occurrence" and cds.rating_factors.pricing.general_liability.include_excess == True and cds.rating_factors.glsn.umbrella.general_liability.occurrence_cover == True:
        for index, option in enumerate(cds.options):
            for layer in range(1,11):
                setattr(getattr(option, "glsn_general_liability"),f"premium_{layer}_excess", gl_excess_premium[f"premium_{layer}_excess_general_liability"][index])
    else:
        for index, option in enumerate(cds.options):
            for layer in range(1,11):
                setattr(getattr(option, "glsn_general_liability"),f"premium_{layer}_excess", 0)
    
    timer.end("section 12")
    timer.start("section 13")

    #--------------------------------------------------------------------------------------------------------------------------------#
    # Excess Premium: Minimum Premium Calculations
    #--------------------------------------------------------------------------------------------------------------------------------#
    
    # Minimum rate on line parameter table
    min_rol_xs_table = hx.params.table_minimum_excess_premium        

    # Turn to scalar variable
    min_rol_xs = min_rol_xs_table.iat[0,0]
    
    min_premium_xs = pd.DataFrame()

    for layer in range (1,11):
        min_premium_xs[f"minimum_premium_{layer}_excess"] = (excess_table[f"dettachment_{layer}_excess"] - excess_table[f"attachment_{layer}_excess"]).fillna(0) * min_rol_xs

        # write to cds
        utils.write_pd_to_hxd(min_premium_xs,cds.options,[f"minimum_premium_{layer}_excess"])

    #--------------------------------------------------------------------------------------------------------------------------------#
    # Excess Gross Premium: Total Calculations
    #--------------------------------------------------------------------------------------------------------------------------------#   

    # Rate Umbrella Excess here
    
    rate_umbrella(hxd) 
    options_umbrella_dict = [{
        "umbrella_unsupported_net_premium.premium_primary": item.umbrella_unsupported_net_premium.premium_primary,
        "umbrella_unsupported_net_premium.premium_1_excess": item.umbrella_unsupported_net_premium.premium_1_excess,
        "umbrella_unsupported_net_premium.premium_2_excess": item.umbrella_unsupported_net_premium.premium_2_excess,
        "umbrella_unsupported_net_premium.premium_3_excess": item.umbrella_unsupported_net_premium.premium_3_excess,
        "umbrella_unsupported_net_premium.premium_4_excess": item.umbrella_unsupported_net_premium.premium_4_excess,
        "umbrella_unsupported_net_premium.premium_5_excess": item.umbrella_unsupported_net_premium.premium_5_excess,
        "umbrella_unsupported_net_premium.premium_6_excess": item.umbrella_unsupported_net_premium.premium_6_excess,
        "umbrella_unsupported_net_premium.premium_7_excess": item.umbrella_unsupported_net_premium.premium_7_excess,
        "umbrella_unsupported_net_premium.premium_8_excess": item.umbrella_unsupported_net_premium.premium_8_excess,
        "umbrella_unsupported_net_premium.premium_9_excess": item.umbrella_unsupported_net_premium.premium_9_excess,
        "umbrella_unsupported_net_premium.premium_10_excess": item.umbrella_unsupported_net_premium.premium_10_excess
    } for item in cds.options]
    options_umbrella_df = pd.DataFrame(options_umbrella_dict) 

    options_brokerage_dict = [{
        "brokerage_primary": item.brokerage_primary,
        "brokerage_1_excess": item.brokerage_1_excess,
        "brokerage_2_excess": item.brokerage_2_excess,
        "brokerage_3_excess": item.brokerage_3_excess,
        "brokerage_4_excess": item.brokerage_4_excess,
        "brokerage_5_excess": item.brokerage_5_excess,
        "brokerage_6_excess": item.brokerage_6_excess,
        "brokerage_7_excess": item.brokerage_7_excess,
        "brokerage_8_excess": item.brokerage_8_excess,
        "brokerage_9_excess": item.brokerage_9_excess,
        "brokerage_10_excess": item.brokerage_10_excess
    } for item in cds.options]
    options_brokerage_df = pd.DataFrame(options_brokerage_dict)  

    options_brokerage_df = options_brokerage_df.fillna(0)
    options_brokerage_df = 1-options_brokerage_df

    options_umbrella_gross_prem = pd.DataFrame()
    # for layer in range(1,11):
    #     options_umbrella_gross_prem[f"premium_{layer}_excess"] = options_umbrella_df[f"umbrella_unsupported_net_premium/premium_{layer}_excess"] / \
    #         options_brokerage_df[f"brokerage_{layer}_excess"]

    excess_premium[[f"premium_{layer}_excess_general_liability_usd" for layer in range(1,11)]] = excess_premium[[f"premium_{layer}_excess_general_liability_usd" for layer in range(1,11)]].fillna(0)
    gl_claims_made_flag = getattr(cds.rating_factors.pricing.general_liability,"claims_basis")

    for layer in range(1,11):
        general_liability_prem = excess_premium[f"premium_{layer}_excess_general_liability_usd"]
        umbrella_premium_pre_max = options_umbrella_df[f"umbrella_unsupported_net_premium.premium_{layer}_excess"]

        if gl_claims_made_flag == "Occurrence" : 
            options_umbrella_gross_prem[f"premium_{layer}_excess"] = np.where(umbrella_premium_pre_max > 0, \
                (np.maximum((5000 - general_liability_prem) / currency_factor, umbrella_premium_pre_max)) / options_brokerage_df[f"brokerage_{layer}_excess"],0)   
        else:
           options_umbrella_gross_prem[f"premium_{layer}_excess"] = np.where(umbrella_premium_pre_max > 0, \
                (np.maximum(5000 / currency_factor, umbrella_premium_pre_max)) / options_brokerage_df[f"brokerage_{layer}_excess"],0)               

    # Gross the umbrella premium

    for layer_index in range(1,11):
        for option_index, option_item in enumerate(cds.options):
            setattr(option_item, f"umbrella_premium_{layer_index}_excess",options_umbrella_gross_prem[f"premium_{layer_index}_excess"][option_index])


    # Rate Umbrella Excess + main coverage excess             

    # brokerage_excess = pd.DataFrame()
    total_gross_model_premium_excess = pd.DataFrame()    

    for layer in range (1,11):

        # Gross supported premium
        support_excess_premium[f"supported_excess_premium_{layer}_excess"] = support_excess_premium[f"supported_excess_premium_{layer}_excess"].fillna(0) 

        # total gross model premium excess (with nmp load)
        total_gross_model_premium_excess[f"model_premium_{layer}_excess"] = (support_excess_premium[f"supported_excess_premium_{layer}_excess"] + options_umbrella_gross_prem[f"premium_{layer}_excess"]) * (1 + nmp_load)
        total_gross_model_premium_excess[f"uplift_for_nmp_{layer}_excess"] = total_gross_model_premium_excess[f"model_premium_{layer}_excess"] - ((support_excess_premium[f"supported_excess_premium_{layer}_excess"] + options_umbrella_gross_prem[f"premium_{layer}_excess"]))

        # Gross premium = maximum of model premium and minimum premium
        total_gross_model_premium_excess[f"gross_premium_{layer}_excess"] = np.maximum(total_gross_model_premium_excess[f"model_premium_{layer}_excess"], min_premium_xs[f"minimum_premium_{layer}_excess"])                             
    
        
        total_gross_model_premium_excess[f"benchmark_premium_{layer}_excess"] = total_gross_model_premium_excess[f"gross_premium_{layer}_excess"].fillna(0) * (priced_to_net_loss_ratio / benchmark_loss_ratio)
        total_gross_model_premium_excess[f"quoted_premium_{layer}_excess"] = options.loc[:,f"quoted_premium_{layer}_excess"].fillna(0)            

        # For checking
        # total_gross_model_premium_excess["benchmark_premium_5_excess"]
        # total_gross_model_premium_excess["quoted_premium_5_excess"]
    
        # bpi calc
        # total_gross_model_premium_excess[f"bpi_{layer}_excess"] = np.where(total_gross_model_premium_excess[f"quoted_premium_{layer}_excess"] == 0, \
        #     None, \
        #     (total_gross_model_premium_excess[f"quoted_premium_{layer}_excess"] / total_gross_model_premium_excess[f"benchmark_premium_{layer}_excess"]).fillna(0))

        total_gross_model_premium_excess[f"bpi_{layer}_excess"] = np.where((total_gross_model_premium_excess[f"quoted_premium_{layer}_excess"] > 0) & (total_gross_model_premium_excess[f"benchmark_premium_{layer}_excess"] > 0), \
            (total_gross_model_premium_excess[f"quoted_premium_{layer}_excess"] / total_gross_model_premium_excess[f"benchmark_premium_{layer}_excess"]).fillna(0), \
            None)
            
        total_gross_model_premium_excess = total_gross_model_premium_excess.fillna(0)    
        # write to cds                        
        # gross model premium
        utils.write_pd_to_hxd(total_gross_model_premium_excess,cds.options,[f"model_premium_{layer}_excess"])
        # nmp
        utils.write_pd_to_hxd(total_gross_model_premium_excess,cds.options,[f"uplift_for_nmp_{layer}_excess"])
        # gross premium
        utils.write_pd_to_hxd(total_gross_model_premium_excess,cds.options,[f"gross_premium_{layer}_excess"])
        # bpi
        utils.write_pd_to_hxd(total_gross_model_premium_excess,cds.options,[f"bpi_{layer}_excess"])
        
        utils.write_pd_to_hxd(support_excess_premium,cds.options,[f"supported_excess_premium_{layer}_excess"])

    
    timer.end("section 13")