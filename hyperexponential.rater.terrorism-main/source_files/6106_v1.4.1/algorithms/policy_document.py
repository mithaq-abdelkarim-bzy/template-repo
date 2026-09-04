import hx
import pandas as pd
import json
from datetime import datetime
from algorithms.rate_utilities import pd_df_from_hx_list


def dict_sclr_risk_info(hxd):
    cds  = hxd.cds
    layer= cds.layers[0]
    data = {
             "expiry_date":                                                       hxd.hx_core.expiry_date
            ,"inception_date":                                                    hxd.hx_core.inception_date

            ,"underwriter":                                                       cds.standard_fields.underwriter
            ,"insured_name":                                                      cds.standard_fields.insured_name
            ,"is_renewal":                                                        cds.standard_fields.is_renewal
            ,"broker_name":                                                       cds.standard_fields.broker

            ,"section_reference":                                                 layer.section_reference
            ,"written_line":                                                      layer.written_line
            ,"brokerage":                                                         layer.brokerage
            ,"status":                                                            layer.status

            ,"source_currency":                                                   cds.currencies.source_currency
            ,"broker_contact":                                                    cds.policy_info.broker_contact
            ,"source_system":                                                     cds.policy_info.source_system

            ,"written_line_basis":                                                layer.written_line_basis
            ,"order":                                                             layer.order
            ,"line_currency":                                                     layer.line
            ,"to_terrorism_only":                                                 cds.policy_info.terrorism_only
            ,"wl_war_on_land":                                                    cds.policy_info.war_on_land

            }
    return data   



def dict_sclr_exposure(hxd):
    cds  = hxd.cds
    layer= cds.layers[0]
    agg  = cds.exposure.aggregate
    adj  = cds.layers[0].risk_adjustments
    data = {
             "commentary_security":                                               adj.security.uw_rationale
            ,"commentary_industry":                                               adj.industry.uw_rationale
            ,"commentary_policy":                                                 adj.policy.uw_rationale
            ,"commentary_ihs":                                                    adj.ihs_score.uw_rationale
            ,"commentary_general":                                                adj.uw_general_comments
            ,"uw_ihs_adjustment":                                                 adj.uw_ihs_adjustment
            ,"total_adjustment_score":                                            adj.total_adj_score
            ,"underwriter_multiplier":                                            adj.uw_multiplier

            ,"total_sum_insured":                                                 agg.total_sum_insured
            ,"bi_sum_insured":                                                    agg.bi_sum_insured
            ,"pd_sum_insured":                                                    agg.pd_sum_insured
            ,"policy_limit":                                                      agg.policy_limit
            ,"policy_sub_limit":                                                  agg.policy_sublimit
            ,"policy_excess":                                                     agg.policy_excess
            ,"policy_deductible":                                                 agg.policy_deductible
            ,"number_of_locations":                                               agg.no_of_locations
            ,"agg_discount":                                                      agg.agg_discount
            ,"type_of_limit":                                                     agg.details.limit_type
            ,"bi_wait_period_days":                                               agg.details.bi_wait_period
            ,"bi_indemnity_periuod_months":                                       agg.details.bi_indemnity_period
            ,"contingent_bi":                                                     agg.details.contingent_bi
            ,"aggregate_usage":                                                   agg.details.aggregate_usage

            ,"construction_coverage":                                             layer.coverages.construction.is_covered
            }
    return data   



def dict_sclr_risk_sum(hxd):
    cds  = hxd.cds
    layer= cds.layers[0]
    data = {
             "commentary_uw_rationale":                                           cds.standard_fields.uw_rationale
            
            ,"gross_quoted_premium":                                              layer.quoted_premium
            ,"gross_benchmark_premium":                                           layer.benchmark_premium
            ,"tpi":                                                               layer.tpi
            ,"priced_for_loss_ratio":                                             layer.pflr
            ,"gross_quoted_rol":                                                  layer.coverages.total.policy_period.quoted_rol
            ,"gross_technical_premium":                                           layer.technical_premium
            ,"tpi_pre_uw_adjustment":                                             layer.tpi_pre_uw_adj
            ,"return_on_capital":                                                 layer.roc
            ,"gross_technical_premium_pre_uw_adjustment":                         layer.technical_premium_pre_uw_adj
            ,"bpi":                                                               layer.bpi
            ,"impact_of_underwriting_adjustments":                                layer.uw_adj_impact
            }
    return data   



def dict_sclr_other(hxd):
    cds  = hxd.cds
    con  = cds.layers[0].coverages.construction
    agg  = cds.exposure.aggregate
    data = {
             "commentary_perils":                                                 agg.peril_comments
            ,"task_confirm_limits_status":                                             agg.confirm_message
            ,"days_difference":                                                   con.days_difference
            }
    return data   


# converts to dictionary from list
def dict_tbl_countries(hxd):
    intended_cols    = [ "rated_country"        ,"country"              ,"proxy_rating_country"
                        ,"no_of_locations"      ,"pml"                  ,"coverage"
                        ,"limit"                ,"excess"               ,"subcoverage"          ,"sublimit"         ,"deductible"
                        ,"total_sum_insured"    ,"bi_sum_insured"       ,"pd_sum_insured"
                        ,"liability_risk"       ,"attritional_risk"     ,"geog_risk"            ,"location_cat_risk"
                        ,"political"            ,"terrorism_raw"        ,"labour_strikes"       ,"protests_riots"   ,"interstate_war"
                        ,"civil_war"            ,"civil_unrest"         ,"war"                  ,"terrorism"
                        ,"selected_sum_insured" ,"warning"]
    intended_lst     = hxd.cds.exposure.granular.countries
    return list_converter(intended_lst, col_order=intended_cols)   


# converts to dictionary from list
def dict_tbl_ihs_score(hxd):
    intended_cols    = [ "rated_country"        ,"leading_peril"        ,"selected_sum_insured_contribution"
                        ,"labour_strikes"       ,"protests_riots"       ,"civil_unrest"         ,"override_civil_unrest"    ,"selected_civil_unrest"    ,"civil_unrest_roe_selected"
                        ,"interstate_war"       ,"civil_war"            ,"war"                  ,"override_war"             ,"selected_war"             ,"war_roe_selected"       
                        ,"terrorism_raw"        ,"political"            ,"civil_unrest"         ,"war"                      
                        ,"terrorism"            ,"override_terrorism"   ,"selected_terrorism"   ,"terrorism_roe_selected"    ]
    intended_lst     = hxd.cds.exposure.granular.countries
    return list_converter(intended_lst, col_order=intended_cols)



# converts to dictionary from list
def dict_tbl_construction_premium_build_up(hxd):
    intended_cols    = [ "end_date"        
                        ,"build_up_calculated"      ,"build_up_override"    ,"build_up_selected"    ,"sum_insured" 
                        ,"total_cvg_nl_roe"         ,"total_subcvg_nl_roe"  ,"cvg_expo_curve"       ,"subcvg_expo_curve"       
                        ,"cvg_premium"              ,"subcvg_premium"       ,"total_premium"        
                        ,"model_premium_pre_uw_adj" ,"model_premium"        ,"benchmark_premium"    ,"model_premium_post_agg_adj"  ]
    intended_lst     = hxd.cds.layers[0].coverages.construction.years
    return list_converter(intended_lst, col_order=intended_cols)



# converts to dictionary from list - custom to error trap empty list
def dict_tbl_construction_default_approach(hxd):
    intended_cols    = ["third", "build_up", "end_date"]
    intended_lst     = hxd.cds.layers[0].coverages.construction.thirds
    empty_df_test    = pd.DataFrame(intended_lst).empty
    return [] if empty_df_test else list_converter(intended_lst, col_order=intended_cols)



# converts to dictionary from structure
def dict_tbl_construction_premium_totals(hxd):
    path_root        = hxd.cds.layers[0].coverages.construction
    data             = []
    for structure in ["years_total", "years_annual"]:
        path = getattr(path_root,structure)
        data.append({
            "cvg_premium":                  path.cvg_premium
            ,"subcvg_premium":              path.subcvg_premium
            ,"total_premium":               path.total_premium
            ,"model_premium_pre_uw_adj":    path.model_premium_pre_uw_adj
            ,"model_premium":               path.model_premium
            ,"benchmark_premium":           path.benchmark_premium
            ,"model_premium_post_agg_adj":  path.model_premium_post_agg_adj
        })
    return data   



# converts to dictionary from structure
def dict_tbl_uw_adjustments(hxd):
    path_root        = hxd.cds.layers[0].risk_adjustments
    data             = []
    for structure in ["security", "industry", "policy", "ihs_score", "ihs_score_expiring"]:
        path = getattr(path_root,structure)
        data.append({
            "level":                 path.level
            ,"calculated":           path.calculated
            ,"min":                  path.min
            ,"override":             path.override
            ,"max":                  path.max
            ,"selected":             path.selected
            ,"description":          path.description
        })
    return data   



# converts to dictionary from structure
def dict_tbl_perils_general(hxd):
    path_root        = hxd.cds.exposure.aggregate.perils
    data             = []
    for structure in [  "terrorism", "sabotage",    "rscc",         "damage",   "insurrection", "coup"
                      , "war",       "insurgency",  "liability",    "cyber",    "nrcb",         "looting"]:
        path = getattr(path_root,structure)
        data.append({
            "is_covered_calculated":    path.is_covered_calculated
            ,"is_covered_override":     path.is_covered_override
            ,"is_covered_selected":     path.is_covered_selected
            ,"limit_calculated":        path.limit_calculated
            ,"limit_override":          path.limit_override
            ,"limit_selected":          path.limit_selected
            ,"excess_calculated":       path.excess_calculated
            ,"excess_override":         path.excess_override
            ,"excess_selected":         path.excess_selected
            ,"deductible_calculated":   path.deductible_calculated
            ,"deductible_override":     path.deductible_override
            ,"deductible_selected":     path.deductible_selected
        })
    return data   


# converts to dictionary from structure
def dict_tbl_perils_cbi(hxd):
    path_root        = hxd.cds.exposure.aggregate.cbi_perils
    data             = []
    for structure in ["unnamed", "named", "interruption", "denial", "ingress", "authority"]:
        path = getattr(path_root,structure)
        data.append({
            "is_covered_selected":      path.is_covered_selected
            ,"limit_selected":          path.limit_selected
            ,"excess_selected":         path.excess_selected
            ,"deductible_selected":     path.deductible_selected
            ,"territory_covered":       path.territory_covered
            ,"distance_selected":       path.distance_selected
            ,"metric_selected":         path.metric_selected
        })
    return data   


# converts to dictionary from structure
def dict_tbl_rate_change_premiums(hxd):
    path_root        = hxd.cds.layers[0].rate_change
    path_root_prem   = hxd.cds.layers[0].rate_change.premium
    data             = []
    for structure in ["line_100pct", "beazley_line", "written_line"]:
        if structure != "written_line":
            path = getattr(path_root_prem,structure)
        data.append({
            "renewal":              path.annualised.renewal           if structure != "written_line" else path_root.written_line.renewal
            ,"blank1":              None
            ,"expiring":            path.annualised.expiring          if structure != "written_line" else path_root.written_line.expiring
            ,"blank2":              None
            ,"expiring_override":   path.annualised.expiring_override if structure == "line_100pct"  else None
        })
    return data  



# converts to dictionary from structure
def dict_tbl_rate_change_drivers(hxd):
    path_root        = hxd.cds.layers[0].rate_change
    data             = []
    for structure in [  "exposure_change",          "risk_characteristics_change",  "deductible_change", "limit_change"
                       ,"terms_conditions_change",  "other_change",                 "rate_change"]:        
        path = getattr(path_root,structure)
        data.append({
            "model_calculated":     path.model_calculated
            ,"blank1":              None
            ,"uw_selected":         path.uw_selected if structure == "rate_change" else path.uw_selected.selected
            ,"blank2":              None
            ,"comments":            path.comments
        })
    return data  



# converts to dictionary from structure - TRANSPOSED
def dict_tbl_uw_authority(hxd):
    path_root        = hxd.cds.layers[0].uw_authorities
    data             = []
    for node in ["nb_gross_line", "nb_net_premium", "ren_gross_line", "ren_net_premium", "term"]:
        data.append({
            "authority":    getattr(getattr(path_root,"authority"), node)
            ,"blank1":      None
            ,"policy":      getattr(getattr(path_root,"policy"),    node)
            ,"blank2":      None
            ,"warning":     getattr(getattr(path_root,"warning"),   node)
        })
    return data   




# converts to dictionary from structure COMPLEX - TRANSPOSED
def dict_tbl_rating_annual_after_uw_adj(hxd):
    path_root        = hxd.cds.layers[0].coverages
    data             = []
    for node in ["model_premium",   "model_rol",            "minimum_premium",  "minimum_rol",          "quoted_premium",   "quoted_rol"
                ,"quoted_roe",      "technical_premium",    "tpi",              "benchmark_premium",    "bpi",              "expected_loss_ratio"]:
        data.append({
            "total":        getattr(                getattr(path_root,"total"),                 node)
            ,"total_pd":    getattr(                getattr(path_root,"property"),              node)
            ,"bi":          getattr(    getattr(    getattr(path_root,"property"),     "bi"),   node)
            ,"pd":          getattr(    getattr(    getattr(path_root,"property"),     "pd"),   node)
            ,"liab":        getattr(                getattr(path_root,"liability"),             node)
            ,"const":       getattr(                getattr(path_root,"construction"),          node)
        })
    return data   



# converts to dictionary from structure COMPLEX - TRANSPOSED
def dict_tbl_rating_term_after_uw_adj(hxd):
    path_root        = hxd.cds.layers[0].coverages
    data             = []
    for node in ["model_premium",   "model_rol",            "minimum_premium",  "minimum_rol",          "quoted_premium",   "quoted_rol"
                ,"quoted_roe",      "technical_premium",    "tpi",              "benchmark_premium",    "bpi",              "expected_loss_ratio"]:
        data.append({
            "total":        getattr(                getattr(getattr(path_root,"total"),       "policy_period"),             node)
            ,"total_pd":    getattr(                getattr(getattr(path_root,"property"),    "policy_period"),             node)
            ,"bi":          getattr(    getattr(    getattr(getattr(path_root,"property"),    "policy_period"),     "bi"),  node)
            ,"pd":          getattr(    getattr(    getattr(getattr(path_root,"property"),    "policy_period"),     "pd"),  node)
            ,"liab":        getattr(                getattr(getattr(path_root,"liability"),   "policy_period"),             node)
            ,"const":       getattr(                getattr(getattr(path_root,"construction"),"policy_period"),             node)
        })
    return data   



# converts to dictionary from structure COMPLEX - TRANSPOSED
def dict_tbl_rating_annual_before_uw_adj(hxd):
    path_root        = hxd.cds.layers[0].coverages
    data             = []
    for node in [ "model_premium_pre_uw_adj",        "model_rol_pre_uw_adj", "technical_premium_pre_uw_adj",     "tpi_pre_uw_adj"
                 ,"benchmark_premium_pre_uw_adj",    "bpi_pre_uw_adj",       "expected_loss_ratio_pre_uw_adj"]:
        data.append({
            "total":        getattr(                getattr(path_root,"total"),                 node)
            ,"total_pd":    getattr(                getattr(path_root,"property"),              node)
            ,"bi":          getattr(    getattr(    getattr(path_root,"property"),     "bi"),   node)
            ,"pd":          getattr(    getattr(    getattr(path_root,"property"),     "pd"),   node)
            ,"liab":        getattr(                getattr(path_root,"liability"),             node)
            ,"const":       getattr(                getattr(path_root,"construction"),          node)
        })
    return data   



# converts to dictionary from structure COMPLEX - TRANSPOSED
def dict_tbl_rating_term_before_uw_adj(hxd):
    path_root        = hxd.cds.layers[0].coverages
    data             = []
    for node in [ "model_premium_pre_uw_adj",        "model_rol_pre_uw_adj", "technical_premium_pre_uw_adj",     "tpi_pre_uw_adj"
                 ,"benchmark_premium_pre_uw_adj",    "bpi_pre_uw_adj",       "expected_loss_ratio_pre_uw_adj"]:
        data.append({
            "total":        getattr(                getattr(getattr(path_root,"total"),       "policy_period"),             node)
            ,"total_pd":    getattr(                getattr(getattr(path_root,"property"),    "policy_period"),             node)
            ,"bi":          getattr(    getattr(    getattr(getattr(path_root,"property"),    "policy_period"),     "bi"),  node)
            ,"pd":          getattr(    getattr(    getattr(getattr(path_root,"property"),    "policy_period"),     "pd"),  node)
            ,"liab":        getattr(                getattr(getattr(path_root,"liability"),   "policy_period"),             node)
            ,"const":       getattr(                getattr(getattr(path_root,"construction"),"policy_period"),             node)
        })
    return data   



# Format data in dictionary for Excel
def clean_data_for_policy_doc(data):
    dates_lst = ["inception_date", "expiry_date", "end_date"]   # allow more generic specification of dates
    for key, value in data.items():
        if isinstance(value, list):                             # non-standard added such that algo pushes into list being passed and allows steps below then to apply
            for lst_value in value:                             # as above
                clean_data_for_policy_doc(lst_value)            # as above
        elif value is None:
            data[key] = ""
        elif value is True:
            data[key] = "Yes"
        elif value is False:
            data[key] = "No"
        elif key in dates_lst:
            date_str = str(value)
            data[key] = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    return data


# Convert hx_list to a dictionary of lists
def list_converter(hx_list, col_order = []):
    df = pd_df_from_hx_list(hx_list)
    if col_order:
        df = df[col_order]

    dict_of_lists = df.to_dict(orient='records')

    return dict_of_lists



# Create data dictionary to write to Excel file
def create_dict_for_excel(hxd):
    cds     = hxd.cds
    sf      = hxd.cds.standard_fields
    layer   = hxd.cds.layers[0]
    exp     = hxd.cds.exposure.granular
    
    ##########################################################################################
    ### customised code to push merged dictionaries and additional dataframes expressed as dictionary
    ##########################################################################################

    # Add scalar fields below
    data    = dict_sclr_risk_info(hxd)  |  dict_sclr_exposure(hxd)  |  dict_sclr_risk_sum(hxd)  |  dict_sclr_other(hxd)

    # Add table fields below
    data["tbl_countries"]                       = dict_tbl_countries(hxd)
    data["tbl_ihs_score"]                       = dict_tbl_ihs_score(hxd)
    data["tbl_uw_adjustments"]                  = dict_tbl_uw_adjustments(hxd)
    data["tbl_perils_general"]                  = dict_tbl_perils_general(hxd)
    data["tbl_perils_cbi"]                      = dict_tbl_perils_cbi(hxd)
    data["tbl_uw_authority"]                    = dict_tbl_uw_authority(hxd)

    data["tbl_rating_annual_after_uw_adj"]      = dict_tbl_rating_annual_after_uw_adj(hxd)
    data["tbl_rating_term_after_uw_adj"]        = dict_tbl_rating_term_after_uw_adj(hxd)
    data["tbl_rating_annual_before_uw_adj"]     = dict_tbl_rating_annual_before_uw_adj(hxd)
    data["tbl_rating_term_before_uw_adj"]       = dict_tbl_rating_term_before_uw_adj(hxd)

    data["tbl_rate_change_premiums"]            = dict_tbl_rate_change_premiums(hxd)
    data["tbl_rate_change_drivers"]             = dict_tbl_rate_change_drivers(hxd)
    
    data["tbl_construction_premium_build_up"]   = dict_tbl_construction_premium_build_up(hxd) 
    data["tbl_construction_premium_totals"]     = dict_tbl_construction_premium_totals(hxd)
    data["tbl_construction_default_approach"]   = dict_tbl_construction_default_approach(hxd)



    ##########################################################################################
    ### standard skeleton model code below here
    ##########################################################################################
    
    # Add URL of hx policy
    p_id    = hx.meta.policy_id
    po_id   = hx.meta.policy_option_id
    
    
    data["tst_policy_url"]  = f"https://www.beazley-tst.hxrenew.com/policies/{p_id}/options/{po_id}"
    data["dev_policy_url"]  = f"https://www.beazley-dev.hxrenew.com/policies/{p_id}/options/{po_id}"
    data["prd_policy_url"]  = f"https://www.beazley.hxrenew.com/policies/{p_id}/options/{po_id}"
    
    # policy_url = f"https://www.beazley.hxrenew.com/policies/{p_id}/options/{po_id}"
    # data["policy_url"] = policy_url

    # Format data
    formatted_data = clean_data_for_policy_doc(data)
    json_data = json.dumps(formatted_data)

    return json_data



# Push dictionary to hxd for storage
def store_policy_data(hxd):
    # If there are multiple layers you'll need to update
    layer = hxd.cds.layers[0]

    # Don't run if premium has not been input
    if not layer.quoted_premium:
        return

    data = create_dict_for_excel(hxd)
    hxd.policy_doc.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.policy_doc.task_data_dict
    hxd.policy_doc.show_download = True if data == task_data else False


