import hx
import json
from datetime import datetime
from algorithms.rate_utilities import pd_df_from_hx_list


# The following dictionaries were derived in this file - if major updates are needed it maybe worth looking at how that was built
# \\bfl.local\UK\Groups\Finance\Actuarial\Pricing\01 - Property\JB\cpr\7_policy_document_template\example_document_template _after_names_formularemoved_v4.xlsm 
# real code begins around line 240

def dict_risk_info_all(hxd):
    cds = hxd.cds
    data = {
             "product":                                                           cds.product
            ,"underwriter":                                                       cds.standard_fields.underwriter
            ,"insured_name":                                                      cds.standard_fields.insured_name
            ,"section_reference":                                                 cds.layers[0].section_reference
            ,"source_currency":                                                   cds.currencies.source_currency
            ,"is_renewal":                                                        cds.standard_fields.is_renewal
            ,"expiry_date":                                                       hxd.hx_core.expiry_date
            ,"inception_date":                                                    hxd.hx_core.inception_date
            ,"broker_contact":                                                    cds.broker_contact
            ,"broker_name":                                                       cds.standard_fields.broker
            ,"written_line":                                                      cds.layers[0].written_line
            ,"excess":                                                            cds.layers[0].excess
            ,"limit":                                                             cds.layers[0].limit
            ,"brokerage":                                                         cds.layers[0].brokerage
            ,"status":                                                            cds.layers[0].status
            }
    return data   


def dict_risk_info_crcf(hxd):
    cds = hxd.cds
    data = {
             "crcf_country":                                                      cds.risk_info.crcf_country
            ,"crcf_obligor":                                                      cds.risk_info.crcf_obligor
            ,"crcf_industry":                                                     cds.risk_info.crcf_industry
            ,"crcf_industry_group":                                               cds.risk_info.crcf_industry_group
            }
    return data   


def dict_exposure_crcf(hxd):
    cds = hxd.cds
    data = {
            "crcf.commentary.security_lgd":                                       cds.modifiers.crcf.lgd_commentary
            ,"crcf.commentary.underwriter_adjustments":                           cds.modifiers.crcf.uw_adj_commentary
            ,"crcf.commentary.credit_rating_source":                              cds.modifiers.crcf.rating_commentary
            ,"crcf.commentary.obligor_risk_drivers":                              cds.modifiers.crcf.obligor_commentary
            ,"crcf.source_of_rating":                                             cds.modifiers.crcf.rating_source
            ,"crcf.corporate_credit_rating":                                      cds.modifiers.crcf.rating_corporate
            ,"crcf.economic_outlook":                                             cds.modifiers.crcf.economic_outlook
            ,"crcf.gross_sum_insured":                                            cds.exposure.granular.crcf.sum_insured
            ,"crcf.indemnity":                                                    cds.exposure.granular.crcf.indemnity
            ,"crcf.waiting_period_d":                                             cds.exposure.granular.crcf.waiting_period
            ,"crcf.post_shipment_percent":                                        cds.exposure.granular.crcf.pst_shipment_amt
            ,"crcf.pre_shipment_percent":                                         cds.exposure.granular.crcf.pre_shipment_amt
            ,"crcf.pre_shipment_risk":                                            cds.exposure.granular.crcf.pre_shipment_risk
            ,"crcf.country_credit_rating":                                        cds.modifiers.crcf.rating_country
            ,"crcf.default.grade":                                                cds.modifiers.crcf.default.grade
            ,"crcf.max.grade":                                                    cds.modifiers.crcf.override_max.grade
            ,"crcf.min.grade":                                                    cds.modifiers.crcf.override_min.grade
            ,"crcf.override.grade":                                               cds.modifiers.crcf.override.grade
            ,"crcf.selected.grade":                                               cds.modifiers.crcf.selected.grade
            ,"crcf.default.probability_of_default":                               cds.modifiers.crcf.default.pod
            ,"crcf.max.probability_of_default":                                   cds.modifiers.crcf.override_max.pod
            ,"crcf.min.probability_of_default":                                   cds.modifiers.crcf.override_min.pod
            ,"crcf.override.probability_of_default":                              cds.modifiers.crcf.override.pod
            ,"crcf.selected.probability_of_default":                              cds.modifiers.crcf.selected.pod
            ,"crcf.default.loss_given_default":                                   cds.modifiers.crcf.default.lgd
            ,"crcf.max.loss_given_default":                                       cds.modifiers.crcf.override_max.lgd
            ,"crcf.min.loss_given_default":                                       cds.modifiers.crcf.override_min.lgd
            ,"crcf.override.loss_given_default":                                  cds.modifiers.crcf.override.lgd
            ,"crcf.selected.loss_given_default":                                  cds.modifiers.crcf.selected.lgd
            ,"crcf.default.underwriter_adjustment":                               cds.modifiers.crcf.default.uw_adj
            ,"crcf.max.underwriter_adjustment":                                   cds.modifiers.crcf.override_max.uw_adj
            ,"crcf.min.underwriter_adjustment":                                   cds.modifiers.crcf.override_min.uw_adj
            ,"crcf.override.underwriter_adjustment":                              cds.modifiers.crcf.override.uw_adj
            ,"crcf.selected.underwriter_adjustment":                              cds.modifiers.crcf.selected.uw_adj
            }
    return data


def dict_exposure_pol(hxd):
    cds = hxd.cds
    data = {
             "pol.commentary.underwriter_adjustments":                            cds.modifiers.political.uw_adj_commentary
            ,"pol.exposure_curve":                                                cds.exposure.granular.political.exposure_curve
            ,"pol.number_of_sims":                                                cds.exposure.granular.political.simulation.num_sims
            ,"pol.tenor_mths":                                                    cds.exposure.granular.political.tenor
            ,"pol.tenor_rate":                                                    cds.exposure.granular.political.key_summary_outputs.tenor_rate
            ,"pol.fixed_assets.government_action_intervention":                   cds.exposure.granular.political.coverage_matrix.fixed_assets.gov_action
            ,"pol.lenders_interest.government_action_intervention":               cds.exposure.granular.political.coverage_matrix.lenders_interest.gov_action
            ,"pol.mobile_assets.government_action_intervention":                  cds.exposure.granular.political.coverage_matrix.mobile_assets.gov_action
            ,"pol.deductible.political_violence":                                 cds.exposure.granular.political.coverage_matrix.deductible.pol_violence
            ,"pol.fixed_assets.political_violence":                               cds.exposure.granular.political.coverage_matrix.fixed_assets.pol_violence
            ,"pol.lenders_interest.political_violence":                           cds.exposure.granular.political.coverage_matrix.lenders_interest.pol_violence
            ,"pol.mobile_assets.political_violence":                              cds.exposure.granular.political.coverage_matrix.mobile_assets.pol_violence
            ,"pol.sublimit.political_violence":                                   cds.exposure.granular.political.coverage_matrix.sublimit.pol_violence
            ,"pol.fixed_assets.currency_inconvertibility":                        cds.exposure.granular.political.coverage_matrix.fixed_assets.cur_inconvertibility
            ,"pol.lenders_interest.currency_inconvertibility":                    cds.exposure.granular.political.coverage_matrix.lenders_interest.cur_inconvertibility
            ,"pol.mobile_assets.currency_inconvertibility":                       cds.exposure.granular.political.coverage_matrix.mobile_assets.cur_inconvertibility
            ,"pol.sublimit.currency_inconvertibility":                            cds.exposure.granular.political.coverage_matrix.sublimit.cur_inconvertibility
            ,"pol.fixed_assets.contractual_relationship_with_government":         cds.exposure.granular.political.coverage_matrix.fixed_assets.cont_relation_govt
            ,"pol.lenders_interest.contractual_relationship_with_government":     cds.exposure.granular.political.coverage_matrix.lenders_interest.cont_relation_govt
            ,"pol.mobile_assets.contractual_relationship_with_government":        cds.exposure.granular.political.coverage_matrix.mobile_assets.cont_relation_govt
            ,"pol.override.total":                                                cds.modifiers.political.override.total
            ,"pol.max.total":                                                     cds.modifiers.political.override_max.total
            ,"pol.min.total":                                                     cds.modifiers.political.override_min.total
            ,"pol.selected.total":                                                cds.modifiers.political.selected.total
            ,"pol.override.uw_adjustment_1_industry":                             cds.modifiers.political.override.industry
            ,"pol.max.uw_adjustment_1_industry":                                  cds.modifiers.political.override_max.industry
            ,"pol.min.uw_adjustment_1_industry":                                  cds.modifiers.political.override_min.industry
            ,"pol.selected.uw_adjustment_1_industry":                             cds.modifiers.political.selected.industry
            ,"pol.override.uw_adjustment_2_quality_of_insured":                   cds.modifiers.political.override.insured_quality
            ,"pol.max.uw_adjustment_2_quality_of_insured":                        cds.modifiers.political.override_max.insured_quality
            ,"pol.min.uw_adjustment_2_quality_of_insured":                        cds.modifiers.political.override_min.insured_quality
            ,"pol.selected.uw_adjustment_2_quality_of_insured":                   cds.modifiers.political.selected.insured_quality
            ,"pol.override.uw_adjustment_3_asset_composition":                    cds.modifiers.political.override.asset_composition
            ,"pol.max.uw_adjustment_3_asset_composition":                         cds.modifiers.political.override_max.asset_composition
            ,"pol.min.uw_adjustment_3_asset_composition":                         cds.modifiers.political.override_min.asset_composition
            ,"pol.selected.uw_adjustment_3_asset_composition":                    cds.modifiers.political.selected.asset_composition
            }
    return data        


def dict_risk_sum_all(hxd):
    cds = hxd.cds
    data = {
             "all.impact_of_underwriting_adjustments":                            cds.layers[0].uw_adj_impact
            ,"all.return_on_capital":                                             cds.layers[0].roc
            ,"all.gross_model_premium":                                           cds.layers[0].model_premium
            ,"all.gross_quoted_premium":                                          cds.layers[0].quoted_premium
            ,"all.gross_technical_premium":                                       cds.layers[0].technical_premium
            ,"all.gross_technical_premium_pre_uw_adjustment":                     cds.layers[0].technical_premium_pre_uw_adj
            ,"all.gross_benchmark_premium":                                       cds.layers[0].benchmark_premium
            ,"all.tpi":                                                           cds.layers[0].tpi
            ,"all.tpi_pre_uw_adjustment":                                         cds.layers[0].tpi_pre_uw_adj
            ,"all.bpi":                                                           cds.layers[0].bpi
            ,"all.priced_for_loss_ratio":                                         cds.layers[0].pflr
            ,"all.bpi_pre_uw_adjustment":                                         cds.layers[0].bpi_pre_uw_adj
            ,"all.priced_for_loss_ratio_pre_uw_adjustment":                       cds.layers[0].pflr_pre_uw_adj
            ,"all.rate_chg.prem_expiring.annualized_100_share":                   cds.layers[0].rate_change.premium.line_100pct.annualised.expiring
            ,"all.rate_chg.prem_renewal.annualized_100_share":                    cds.layers[0].rate_change.premium.line_100pct.annualised.renewal
            ,"all.rate_chg.prem_expiring.annualized_beazley_share":               cds.layers[0].rate_change.premium.beazley_line.annualised.expiring
            ,"all.rate_chg.prem_renewal.annualized_beazley_share":                cds.layers[0].rate_change.premium.beazley_line.annualised.renewal
            ,"all.rate_chg.pct_comment.exposure_change":                          cds.layers[0].rate_change.exposure_change.comments
            ,"all.rate_chg.pct_model.exposure_change":                            cds.layers[0].rate_change.exposure_change.model_calculated
            ,"all.rate_chg.pct_selected.exposure_change":                         cds.layers[0].rate_change.exposure_change.uw_selected.selected
            ,"all.rate_chg.pct_comment.risk_characteristics_change":              cds.layers[0].rate_change.risk_characteristics_change.comments
            ,"all.rate_chg.pct_model.risk_characteristics_change":                cds.layers[0].rate_change.risk_characteristics_change.model_calculated
            ,"all.rate_chg.pct_selected.risk_characteristics_change":             cds.layers[0].rate_change.risk_characteristics_change.uw_selected.selected
            ,"all.rate_chg.pct_comment.deductible_change":                        cds.layers[0].rate_change.deductible_change.comments
            ,"all.rate_chg.pct_model.deductible_change":                          cds.layers[0].rate_change.deductible_change.model_calculated
            ,"all.rate_chg.pct_selected.deductible_change":                       cds.layers[0].rate_change.deductible_change.uw_selected.selected
            ,"all.rate_chg.pct_comment.limit_change":                             cds.layers[0].rate_change.limit_change.comments
            ,"all.rate_chg.pct_model.limit_change":                               cds.layers[0].rate_change.limit_change.model_calculated
            ,"all.rate_chg.pct_selected.limit_change":                            cds.layers[0].rate_change.limit_change.uw_selected.selected
            ,"all.rate_chg.pct_comment.terms_conditions_change":                  cds.layers[0].rate_change.terms_conditions_change.comments
            ,"all.rate_chg.pct_model.terms_conditions_change":                    cds.layers[0].rate_change.terms_conditions_change.model_calculated
            ,"all.rate_chg.pct_selected.terms_conditions_change":                 cds.layers[0].rate_change.terms_conditions_change.uw_selected.selected
            ,"all.rate_chg.pct_comment.other_change":                             cds.layers[0].rate_change.other_change.comments
            ,"all.rate_chg.pct_model.other_change":                               cds.layers[0].rate_change.other_change.model_calculated
            ,"all.rate_chg.pct_selected.other_change":                            cds.layers[0].rate_change.other_change.uw_selected.selected
            ,"all.rate_chg.pct_comment.risk_adjusted_rate_change":                cds.layers[0].rate_change.rate_change.comments
            ,"all.rate_chg.pct_model.risk_adjusted_rate_change":                  cds.layers[0].rate_change.rate_change.model_calculated
            ,"all.rate_chg.pct_selected.risk_adjusted_rate_change":               cds.layers[0].rate_change.rate_change.uw_selected
            ,"all.commentary.underwriter_rationale":                              cds.standard_fields.uw_rationale
            }
    return data   


def dict_risk_sum_crcf(hxd):
    cds = hxd.cds
    data = {
             "crcf.pre_uwadj_annual.rate_on_exposure_offered":                    cds.layers[0].crcf.metrics_summary_pre_uwadj_annual.roe_offered
            ,"crcf.pre_uwadj_term.rate_on_exposure_offered":                      cds.layers[0].crcf.metrics_summary_pre_uwadj_term.roe_offered
            ,"crcf.pst_uwadj_annual.rate_on_exposure_offered":                    cds.layers[0].crcf.metrics_summary_pst_uwadj_annual.roe_offered
            ,"crcf.pst_uwadj_term.rate_on_exposure_offered":                      cds.layers[0].crcf.metrics_summary_pst_uwadj_term.roe_offered
            ,"crcf.pre_uwadj_annual.rate_on_exposure_plan":                       cds.layers[0].crcf.metrics_summary_pre_uwadj_annual.roe_plan
            ,"crcf.pre_uwadj_term.rate_on_exposure_plan":                         cds.layers[0].crcf.metrics_summary_pre_uwadj_term.roe_plan
            ,"crcf.pst_uwadj_annual.rate_on_exposure_plan":                       cds.layers[0].crcf.metrics_summary_pst_uwadj_annual.roe_plan
            ,"crcf.pst_uwadj_term.rate_on_exposure_plan":                         cds.layers[0].crcf.metrics_summary_pst_uwadj_term.roe_plan
            ,"crcf.pre_uwadj_annual.rate_on_exposure_technical":                  cds.layers[0].crcf.metrics_summary_pre_uwadj_annual.roe_technical
            ,"crcf.pre_uwadj_term.rate_on_exposure_technical":                    cds.layers[0].crcf.metrics_summary_pre_uwadj_term.roe_technical
            ,"crcf.pst_uwadj_annual.rate_on_exposure_technical":                  cds.layers[0].crcf.metrics_summary_pst_uwadj_annual.roe_technical
            ,"crcf.pst_uwadj_term.rate_on_exposure_technical":                    cds.layers[0].crcf.metrics_summary_pst_uwadj_term.roe_technical
            ,"crcf.pre_uwadj_annual.rate_on_exposure_benchmark":                  cds.layers[0].crcf.metrics_summary_pre_uwadj_annual.roe_benchmark
            ,"crcf.pre_uwadj_term.rate_on_exposure_benchmark":                    cds.layers[0].crcf.metrics_summary_pre_uwadj_term.roe_benchmark
            ,"crcf.pst_uwadj_annual.rate_on_exposure_benchmark":                  cds.layers[0].crcf.metrics_summary_pst_uwadj_annual.roe_benchmark
            ,"crcf.pst_uwadj_term.rate_on_exposure_benchmark":                    cds.layers[0].crcf.metrics_summary_pst_uwadj_term.roe_benchmark
            ,"crcf.pre_uwadj_term.bpi":                                           cds.layers[0].crcf.metrics_summary_pre_uwadj_term.bpi
            ,"crcf.pst_uwadj_term.bpi":                                           cds.layers[0].crcf.metrics_summary_pst_uwadj_term.bpi
            ,"crcf.pre_uwadj_term.tpi":                                           cds.layers[0].crcf.metrics_summary_pre_uwadj_term.tpi
            ,"crcf.pst_uwadj_term.tpi":                                           cds.layers[0].crcf.metrics_summary_pst_uwadj_term.tpi
            ,"crcf.pre_uwadj_term.priced_to_plan":                                cds.layers[0].crcf.metrics_summary_pre_uwadj_term.priced_to_plan
            ,"crcf.pst_uwadj_term.priced_to_plan":                                cds.layers[0].crcf.metrics_summary_pst_uwadj_term.priced_to_plan
            ,"crcf.pre_uwadj_term.priced_loss_ratio_gross_gross":                 cds.layers[0].crcf.metrics_summary_pre_uwadj_term.priced_gglr
            ,"crcf.pst_uwadj_term.priced_loss_ratio_gross_gross":                 cds.layers[0].crcf.metrics_summary_pst_uwadj_term.priced_gglr
            ,"crcf.pre_uwadj_term.priced_loss_ratio_gross_net":                   cds.layers[0].crcf.metrics_summary_pre_uwadj_term.priced_gnlr
            ,"crcf.pst_uwadj_term.priced_loss_ratio_gross_net":                   cds.layers[0].crcf.metrics_summary_pst_uwadj_term.priced_gnlr
            ,"crcf.pst_uwadj_term.bound_lgd_implied":                             cds.layers[0].crcf.metrics_summary_pst_uwadj_term.lgd_bound
            ,"crcf.pst_uwadj_term.bound_grade_implied":                           cds.layers[0].crcf.metrics_summary_pst_uwadj_term.credit_rating_bound
            }
    return data   


def dict_risk_sum_pol(hxd):
    cds = hxd.cds
    data = {
             "pol.pre_uwadj.rate_on_line_offered":                                cds.layers[0].political.metrics_summary_pre_uwadj.rol_offered
            ,"pol.pst_uwadj.rate_on_line_offered":                                cds.layers[0].political.metrics_summary_pst_uwadj.rol_offered
            ,"pol.pre_uwadj.rate_on_line_model":                                  cds.layers[0].political.metrics_summary_pre_uwadj.rol_model
            ,"pol.pst_uwadj.rate_on_line_model":                                  cds.layers[0].political.metrics_summary_pst_uwadj.rol_model
            ,"pol.pre_uwadj.rate_on_line_technical":                              cds.layers[0].political.metrics_summary_pre_uwadj.rol_technical
            ,"pol.pst_uwadj.rate_on_line_technical":                              cds.layers[0].political.metrics_summary_pst_uwadj.rol_technical
            ,"pol.pre_uwadj.rate_on_line_benchmark":                              cds.layers[0].political.metrics_summary_pre_uwadj.rol_benchmark
            ,"pol.pst_uwadj.rate_on_line_benchmark":                              cds.layers[0].political.metrics_summary_pst_uwadj.rol_benchmark
            ,"pol.pre_uwadj.bpi":                                                 cds.layers[0].political.metrics_summary_pre_uwadj.bpi
            ,"pol.pst_uwadj.bpi":                                                 cds.layers[0].political.metrics_summary_pst_uwadj.bpi
            ,"pol.pre_uwadj.tpi":                                                 cds.layers[0].political.metrics_summary_pre_uwadj.tpi
            ,"pol.pst_uwadj.tpi":                                                 cds.layers[0].political.metrics_summary_pst_uwadj.tpi
            ,"pol.pre_uwadj.priced_to_plan":                                      cds.layers[0].political.metrics_summary_pre_uwadj.priced_to_plan
            ,"pol.pst_uwadj.priced_to_plan":                                      cds.layers[0].political.metrics_summary_pst_uwadj.priced_to_plan
            ,"pol.pre_uwadj.priced_loss_ratio_gross_gross":                       cds.layers[0].political.metrics_summary_pre_uwadj.priced_gglr
            ,"pol.pst_uwadj.priced_loss_ratio_gross_gross":                       cds.layers[0].political.metrics_summary_pst_uwadj.priced_gglr
            ,"pol.pre_uwadj.priced_loss_ratio_gross_net":                         cds.layers[0].political.metrics_summary_pre_uwadj.priced_gnlr
            ,"pol.pst_uwadj.priced_loss_ratio_gross_net":                         cds.layers[0].political.metrics_summary_pst_uwadj.priced_gnlr
            }
    return data   



# Format data in dictionary for Excel
def clean_data_for_policy_doc(data):
    for key, value in data.items():
        if value is None:
            data[key] = ""
        elif value is True:
            data[key] = "Yes"
        elif value is False:
            data[key] = "No"
        elif key in ["inception_date", "expiry_date"]:
            date_str = str(value)
            data[key] = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

    return data


def list_converter(hx_list, col_order = []):
    df = pd_df_from_hx_list(hx_list)
    if col_order:
        df = df[col_order]

    dict_of_lists = df.to_dict(orient='records')

    return dict_of_lists


# Create data dictionary to write to Excel file
def create_dict_for_excel(hxd):
    cds = hxd.cds
    sf = hxd.cds.standard_fields
    rf = hxd.cds.rating_factors
    layer = hxd.cds.layers[0]
    exp = hxd.cds.exposure.granular
    
    ##########################################################################################
    ### customised code to push merged dictionaries and additional dataframes expressed as dictionary
    ##########################################################################################

    if (cds.product in {'Contract Frustration','Credit Risk'}): 
        # Add scalr fields below
        data          = dict_risk_info_all(hxd)   |   dict_risk_info_crcf(hxd)  |  dict_exposure_crcf(hxd)  |  dict_risk_sum_all(hxd)  |  dict_risk_sum_crcf(hxd)


        # Add data tables here, need to convert to a dictionary for storate in the data dictionary using 'list_converter'
        exposure_cols = ["month_1", "month_2", "month_3", "month_4", "month_5", "month_6","month_7", "month_8", "month_9", "month_10","month_11","month_12"]
        exposure_lst  = list_converter(exp.crcf.exposure_profile, col_order=exposure_cols)
        data["crcf.exposure_profile"] = exposure_lst

    elif (cds.product in {'Political Risk'}): 
        # Add scalr fields below
        data          = dict_risk_info_all(hxd)   |                                dict_exposure_pol(hxd)   |  dict_risk_sum_all(hxd)  |  dict_risk_sum_pol(hxd)
        # Add data tables here, need to convert to a dictionary for storate in the data dictionary using 'list_converter'
        exposure_cols = ["country", "sum_insured", "excess", "limit", "check", "country_2dig"]
        exposure_lst  = list_converter(exp.political.country_exposure, col_order=exposure_cols)
        data["pol.country_details"] = exposure_lst

    else:
        # Add scalr fields below
        data =    dict_risk_info_all(hxd)



    ##########################################################################################
    ### standard skeleton model code below here
    ##########################################################################################
    
    # Add URL of hx policy
    p_id = hx.meta.policy_id
    po_id = hx.meta.policy_option_id
    
    
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


