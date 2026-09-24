# v0.5.0
import hx
from algorithms.rate_constants import max_layers, experience_rating_max_years, pareto_default_value, odf_default_value
# import algorithms.rate_constants as const
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict , max_coverages
from algorithms.model_profiler.profiling_hxd_functions import time_me
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, remove_before_separator, ratio
from algorithms import parameter_tables_schema as params

@time_me
def model_state_all_inputs(hxd):

    hxd.cds.risk_information.inception_year = hxd.hx_core.inception_date.year
    
    ms = hxd.model_state

    # save the record global variable in the snapshot for governance
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 56654 # For debugging in dev mode
    
    ms.coverage_use = RARC_COVERAGE_USE # Edit v0.3.0
    ms.insured_asset_use = RARC_INSURED_ASSET_USE # Edit v0.3.0

    ms.info_by_risk_bdx_exposure_prem = "Total Exposure per Layer is floored at 0"
    ms.info_by_include_swing_rates = "Must select only one of Swing Rates or Profit Commission"
    ms.info_by_include_pc = "Must select only one of Swing Rates or Profit Commission"

    
    # Controls which page to show and hide when the start renewal button is pressed
    # Only displays the landing page for policies which are a renewal
    # if (expiring_policy_option_id is None) or (ms.pressed_start_renewal_task) or (ms.expiring_policy_option_id == expiring_policy_option_id):
    if True:
        ms.show_landing_page = False
        ms.show_after_landing_page = True
        # NOTE USE the below for 
        # ms.show_rate_change = True

        ms.show_rate_change_layer_no_ia_use = hxd.cds.standard_fields.is_renewal and not RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE
        ms.show_rate_change_layer_ia_use = hxd.cds.standard_fields.is_renewal and not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE
        ms.show_rate_change_coverage_no_ia_use = hxd.cds.standard_fields.is_renewal and RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE
        ms.show_rate_change_coverage_ia_use = hxd.cds.standard_fields.is_renewal and RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE

    # else:
    #     ms.show_landing_page = True
    #     ms.show_after_landing_page = False

    #     ms.show_rate_change = False
        
    #     ms.show_rate_change_layer_no_ia_use = False
    #     ms.show_rate_change_layer_ia_use = False
    #     ms.show_rate_change_coverage_no_ia_use = False
    #     ms.show_rate_change_coverage_ia_use = False


    if RARC_COVERAGE_USE: # EDIT v0.3.0
        num_coverages = len(coverages_dict)
        for cvg_index in range(1,max_coverages):
            setattr(hxd.cds.rate_change, f"show_coverage_{cvg_index}", True) if cvg_index <= num_coverages else False

    # set the shown_by value # Edit # v0.5.0
    ms.layer_no_ia_use = (RARC_COVERAGE_USE==False and RARC_INSURED_ASSET_USE == False)
    ms.layer_ia_use = (RARC_COVERAGE_USE==False and RARC_INSURED_ASSET_USE == True)
    ms.coverage_no_ia_use = (RARC_COVERAGE_USE==True and RARC_INSURED_ASSET_USE == False)
    ms.coverage_ia_use = (RARC_COVERAGE_USE==True and RARC_INSURED_ASSET_USE == True)


    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology != "Rater"

    # set the rater boolean for calculation
    ms.is_steer = hxd.cds.metadata.rater == "STEER"
    ms.is_clash = hxd.cds.metadata.rater == "Clash"
    ms.is_healthcare_cat = hxd.cds.metadata.rater == "Healthcare CAT"
    ms.is_not_clash = not ms.is_clash

    # set the rater boolean for ui display
    ms.show_steer = ms.is_steer and ms.show_after_landing_page and hxd.cds.standard_fields.rating_methodology == "Rater"
    ms.show_clash = ms.is_clash and ms.show_after_landing_page and hxd.cds.standard_fields.rating_methodology == "Rater"
    ms.show_healthcare_cat = ms.is_healthcare_cat and ms.show_after_landing_page and hxd.cds.standard_fields.rating_methodology == "Rater"
    ms.show_rater_priced = ms.show_after_landing_page and hxd.cds.standard_fields.is_rater_priced
    ms.show_case_priced = ms.show_after_landing_page and hxd.cds.standard_fields.is_case_priced


    if ms.is_steer:
        steer_model_state(hxd, ms)
    else:
        ms.show_steer_risk_bdx = False
        ms.show_steer_las_bdx = False
        ms.show_steer_experience_rating = False

    
    # Set bug report message (update rater name below, use dash for space)
    hxd.bug_report_email = """Please use the following email to report a bug or issue with the model and the support team will get back to you shortly.
    Please include the model name, a brief description of the issue, and the website link to the policy the issue relates to. 
    
    [RatingTeamDev@beazley](mailto:RatingTeamDev@beazley.com?subject=RATERNAME-Rater)"""
               

def steer_model_state(hxd, ms):
    ms.show_steer_experience_rating = ms.is_steer_experience_rating and ms.show_after_landing_page and hxd.cds.standard_fields.is_rater_priced
    ms.show_steer_risk_bdx = ms.is_steer_exposure_rating_risk_profil_bdx and ms.show_after_landing_page and hxd.cds.standard_fields.is_rater_priced
    ms.show_steer_las_bdx = ms.is_steer_exposure_rating_limit_average_severity = ms.show_steer_experience_rating and ms.show_steer_risk_bdx and hxd.cds.standard_fields.is_rater_priced


    # hxd.cds.steer.experience_rating.on_levelling.raw_data_comment = "Upload data including the header. Please denote the policy year by 'Policy Year, 'Treaty Year', 'PY' or 'TY' in the header. If the column contains Date data format, please include 'Date' in the header description (e.g. Closed Date)"

    as_at_date = hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value
    fvy = hxd.cds.steer.experience_rating.other_fields.fvy.value
    lvy = hxd.cds.steer.experience_rating.other_fields.lvy.value
    
    lvy = as_at_date.year
    
    ms.is_steer_raw_data_not_validated = not ms.is_steer_raw_data_validated if ms.is_steer_raw_data_validated is not None else None

    # hxd.cds.steer.experience_rating.other_fields.lvy.value = as_at_date.year
    
    # # For layers not used in the pricing summary, the rate change and KPI Summary is hidden
    # layers = hxd.cds.layers
    # num_layers = len(layers)
    # ms.show_layer_fgu = True
    # for layer_index in range(1,max_layers+1):
    #     setattr(hxd.cds.rate_change, f"show_layer_{layer_index}", True) if layer_index <= num_layers else False
    #     setattr(ms, f"show_layer_{layer_index:02d}", True) if layer_index <= num_layers else False
    
    # num_of_years = (lvy - fvy)+1 if lvy is not None and fvy is not None else 0

    # if num_of_years >0:
    #     for dy_index in range(1,experience_rating_max_years+1):
    #         if dy_index >= (experience_rating_max_years + 1 - num_of_years):
    #             setattr(ms, f"show_data_year_{dy_index:02d}", True)  
    #         else:
    #             setattr(ms, f"show_data_year_{dy_index:02d}", False)  
   ############################################################
    ## Page On levelling
    ############################################################
    cy_yoa = hxd.cds.risk_information.inception_year
    ol= hxd.cds.steer.experience_rating.on_levelling
    num_years = len(ol.exposure_assumptions)
    expo_ass_df = pd_df_from_hx_list(ol.exposure_assumptions)

    expo_ass_df["uw_year"] = [(cy_yoa - num_years + x) for x in range(1,num_years +1)] 
    expo_ass_df["display_yoa"] = expo_ass_df.uw_year.astype(int).astype(str) 

    #  Write to hxd
    expo_assump_output_columns_str = [
        "display_yoa"
    ]
    expo_assumnmp_output_columns_flt = [
        "uw_year"
        # ,"exposure_on_level"
        # ,"rate_change_index"
        # ,"inflation_index"
    ]
    # clean data before writing it hxd
    expo_ass_df[expo_assump_output_columns_str ] = expo_ass_df[expo_assump_output_columns_str ].fillna('')
    expo_ass_df[expo_assumnmp_output_columns_flt ] = expo_ass_df[expo_assumnmp_output_columns_flt ].fillna(0)

    write_pd_to_hxd(expo_ass_df,  hxd.cds.steer.experience_rating.on_levelling.exposure_assumptions,  expo_assump_output_columns_str + expo_assumnmp_output_columns_flt )

    
    ############################################################
    ## Page Data Format
    ############################################################
    #     
    data_map = hxd.cds.steer.experience_rating.data_mapping
    tbl_data_mapping = hx.params.table_steer_expe_data_mapping
    coverage_basis = hxd.cds.steer.experience_rating.other_fields.coverage_basis.value

    # Data Mapping: assign field and field name and other column
    for index, item in enumerate(data_map):
        item[1].field = remove_before_separator(item[0],"_")
        item[1].field_name = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Field Name"].iloc[0]
        item[1].description = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Description"].iloc[0]
        # item[1].mandatory_column = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Mandatory Column"].iloc[0]
        item[1].mandatory_column = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]][f"Mandatory Column {coverage_basis}"].iloc[0]
        item[1].accept_missing = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Accept Missing Values"].iloc[0]
        item[1].field_type = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Field Type"].iloc[0]
        item[1].value_within_range = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Value Within Range"].iloc[0]
        item[1].replace_missing_with_default = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Replace Missing with Default Value"].iloc[0]

    ############################################################
    ## Page Burning Cost - GET CLAIM INFO FROM PROCESSED DATA AND TRIANGLES (incurred claims, inflated claims, incurred_no_of_claims, dev pettern claim and count)
    ############################################################
    inception_date = hxd.hx_core.inception_date
    start_year = inception_date.year - experience_rating_max_years + 1
    end_year = inception_date.year

    ##############################
    ## START Helper functions ##
    ##############################
    def assign_yoa_labels(er_layers, inception_date, max_years,max_layers):
        """Assign policy_year and policy_year_label for all layers."""
        for yoa_index in range(max_years):
            policy_year = inception_date.year - max_years + yoa_index + 1
            policy_year_label = str(policy_year) if policy_year else ""

            # Assign to FGU layer
            er_layers.fgu.burning_cost[yoa_index].policy_year = policy_year
            er_layers.fgu.burning_cost[yoa_index].policy_year_label = policy_year_label

            # Assign to all RI layers
            for layer_index in range(max_layers):
                layer_name = f'layer_{layer_index+1:02d}'
                layer_bc = getattr(er_layers, layer_name).burning_cost[yoa_index]
                setattr(layer_bc, "policy_year", policy_year)
                setattr(layer_bc, "policy_year_label", policy_year_label)

    ##############################
    ## Start Initialise Variables and lists
    ##############################
    # er_layers = hxd.cds.steer.experience_rating.layers
    # Assign YOA labels columns in the burning cost node
    assign_yoa_labels(hxd.cds.steer.experience_rating.layers, inception_date, experience_rating_max_years, max_layers)

    # write_pd_to_hxd(er_fgu_bc_df, er_layers.fgu.burning_cost, bc_output_columns)


    return


@time_me
def allow_policy_doc_download(hxd):
    layer = hxd.cds.layers[0]
    doc = hxd.policy_doc
        
    tp = layer.technical_premium_100 or 0
    bp = layer.benchmark_premium_100 or 0
    qp = layer.quoted_premium_100 or 0
    
    if bp <= 0:
        doc.premium_check = f"Benchmark Premium has not been calculated. Please fill in the relevant fields in to calculate premium."
        doc.show_premium_check = True
    elif tp <= 0:
        doc.premium_check = "Benchmark Premium has not been fully calculated. Please check the validation errors at the bottom right corner."
        doc.show_premium_check = True
    elif qp <= 0:
        doc.premium_check = "Quoted Premium should be greater than 0. Please input a valid number in Rating Summary."
        doc.show_premium_check = True
    else:
        doc.show_generate_button = True

@time_me
def back_populate_generic_pages(hxd):

    cds_layers = hxd.cds.layers
    tp_params_df = params.tp_parameters.df()

    cds = hxd.cds
    cob_ref = cds.technical_price_assumptions.cob_reference
    cob_assumptions_df = hx.params.table_cob_code_assumptions

    # Default values
    pareto_p = cds.pricing_selection.pareto_parameters
    odf_p = cds.pricing_selection.odf_parameters
    # Assign technical price assumptions
    yoa = hxd.hx_core.inception_date.year

    if yoa in list(set(tp_params_df[(tp_params_df["business_plan_class"]=="Specialty Reinsurance") | (tp_params_df["business_plan_class"]=="Specialty (PT)") | (tp_params_df["business_plan_class"]=="Specialty Surety")]['year'])):
        tp_year = yoa
    else:
        tp_year = tp_params_df['year'].max()

    if cob_ref == "TQ":
        hxd.cds.standard_fields.benchmark_class = business_plan_class = "Specialty Surety"
    elif tp_year < 2026:
        hxd.cds.standard_fields.benchmark_class = business_plan_class = "Specialty (PT)"
    else:
        hxd.cds.standard_fields.benchmark_class = business_plan_class =  "Specialty Reinsurance"

    tpa_df = tp_params_df[(tp_params_df["year"]==tp_year) & (tp_params_df["business_plan_class"]==business_plan_class) ]
    nmp_load =  tpa_df["nmp_load"].item()


    method_list = [
            "risk_profile_bdx",
            "limit_average_severity",
            "burning_cost",
            "clash",
            "healthcare_cat",
            "other_method",
        ]



    ##############################
    ## Assign COB Parameters
    ##############################



    ##############################
    ## Helper functions
    ##############################

    # Helper function to fetch parameter from DataFrame or return None
    def get_parameter_from_df(df, cob_ref, column_name):
        if cob_ref == "" or  cob_ref is None:
            if column_name == "Pareto Parameter":
                return pareto_default_value 
            else:
                return odf_default_value
        matching_rows = df.loc[df['Class of Business Code'] == cob_ref, column_name]
        return matching_rows.values[0] if not matching_rows.empty else None


    # Assign selected parameters
    pareto_p.default = get_parameter_from_df(cob_assumptions_df, cob_ref, "Pareto Parameter")
    odf_p.default = get_parameter_from_df(cob_assumptions_df, cob_ref, "Neg BI ODF")

    pareto_p.selected = pareto_p.overwrite if pareto_p.overwrite is not None else pareto_p.default
    odf_p.selected = odf_p.overwrite if odf_p.overwrite is not None else odf_p.default


    for layer_index, layer in enumerate(cds_layers):
        ##############################
        ## Rating Summary
        ##############################

        brokerage = layer.swing_rates.swing_brokerage if layer.swing_rates.use_swing_brokerage == True else layer.brokerage
        ceding_commission = layer.ceding_commission or 0
        # define brokerage netting down factor
        if layer.bkg_gross_or_net == "Gross":
            bkg_netting_down_factor = 1 - brokerage - ceding_commission
        else:
            bkg_netting_down_factor = (1 - brokerage) * (1 - ceding_commission)

        layer.brokerage_inc_swing = brokerage
        layer.quoted_premium_net_100 = ratio(layer.quoted_premium_100 or 0 , bkg_netting_down_factor)
        layer.benchmark_premium_net_100 = ratio(layer.benchmark_premium_100 or 0 , bkg_netting_down_factor)
        layer.technical_premium_net_100 = ratio(layer.technical_premium_100 or 0 , bkg_netting_down_factor)
        layer.expected_loss_inc_nmp = (layer.expected_losses_after_loss_sensitive_features or 0) * (1 + nmp_load)
        layer.line_size = (layer.written_line or 0) * (layer.upfront_premium_gross_100 or 0)

        ##############################
        ## Pricing Selection
        ##############################

        layer.pricing_selection.risk_profile_bdx.pure_premium = pure_premium_risk_bdx =  (layer.pricing_selection.risk_profile_bdx.pure_rate or 0) * (layer.epi_100 or 0)
        layer.pricing_selection.risk_profile_bdx.pure_rol = ratio(pure_premium_risk_bdx,layer.limit or 0)

        layer.pricing_selection.limit_average_severity.pure_premium = pure_premium_las =  (layer.pricing_selection.limit_average_severity.pure_rate or 0) *  (layer.epi_100 or 0) 
        layer.pricing_selection.limit_average_severity.pure_rol = ratio(pure_premium_las,layer.limit or 0)

        layer.pricing_selection.burning_cost.pure_premium = pure_premium_bc =  (layer.pricing_selection.burning_cost.pure_rate or 0) *  (layer.epi_100 or 0) 
        layer.pricing_selection.burning_cost.pure_rol = ratio(pure_premium_bc,layer.limit or 0)

        # layer.pricing_selection.clash.pure_premium = pure_premium_clash =  (layer.pricing_selection.clash.pure_rate or 0) *  (layer.epi_100 or 0) 
        # layer.pricing_selection.clash.pure_rol = ratio(pure_premium_clash,layer.limit or 0)

        layer.pricing_selection.healthcare_cat.pure_premium = pure_premium_hc =  (layer.pricing_selection.healthcare_cat.pure_rate or 0) *  (layer.epi_100 or 0) 
        layer.pricing_selection.healthcare_cat.pure_rol = ratio(pure_premium_hc,layer.limit or 0)

        layer.pricing_selection.other_method.pure_premium = pure_premium_other =  (layer.pricing_selection.other_method.pure_rate or 0) *  (layer.epi_100 or 0) 
        layer.pricing_selection.other_method.pure_rol = ratio(pure_premium_other,layer.limit or 0)

        layer.pricing_selection.final_selection.pure_rate = layer.pure_rate or 0
        layer.pricing_selection.final_selection.pure_premium =  layer.pricing_selection.final_selection.pure_rate * (layer.epi_100 or 0)
        layer.pricing_selection.final_selection.pure_rol = ratio(layer.pricing_selection.final_selection.pure_premium,layer.limit)
        layer.pricing_selection.final_selection.total_weighting = (layer.pricing_selection.risk_profile_bdx.weighting or 0) + (layer.pricing_selection.limit_average_severity.weighting or 0) + (layer.pricing_selection.burning_cost.weighting or 0) + (layer.pricing_selection.healthcare_cat.weighting or 0) + (layer.pricing_selection.other_method.weighting or 0)
    
    
    
    return
            