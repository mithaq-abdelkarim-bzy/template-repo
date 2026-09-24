# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from algorithms.model_profiler.profiling_hxd_functions import time_me


from algorithms.rate_constants import max_layers, experience_rating_max_years, pareto_default_value, odf_default_value


@time_me
def rate_pricing_selection(hxd):
    """Pricing Selection for generic section like COB parameters, Other, and Final Selection"""
    ##############################
    ## Initialise variables
    ##############################

    cds = hxd.cds
    # cob_ref = cds.steer.risk_information.cob_reference
    cob_ref = cds.technical_price_assumptions.cob_reference
    cob_assumptions_df = hx.params.table_cob_code_assumptions

    # Default values
    pareto_p = cds.pricing_selection.pareto_parameters
    odf_p = cds.pricing_selection.odf_parameters

    cds_layers = cds.layers

    ms = hxd.model_state

    er = hxd.cds.steer.experience_rating

    is_rater_priced = cds.standard_fields.is_rater_priced
    
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

    ##############################
    ## Assign COB Parameters
    ##############################
    # Assign selected parameters
    pareto_p.default = get_parameter_from_df(cob_assumptions_df, cob_ref, "Pareto Parameter")
    odf_p.default = get_parameter_from_df(cob_assumptions_df, cob_ref, "Neg BI ODF")

    pareto_p.selected = pareto_p.overwrite if pareto_p.overwrite is not None else pareto_p.default
    odf_p.selected = odf_p.overwrite if odf_p.overwrite is not None else odf_p.default

    for layer_num, layer in enumerate(cds_layers):
        layer_name = f"layer_{layer_num+1:02d}"

    ##############################
    ## Assign Other Method
    ##############################
        other_method_pure_rate = layer.pricing_selection.other_method.pure_rate or 0
        layer.pricing_selection.other_method.pure_premium = 0
        layer.pricing_selection.other_method.pure_premium = other_method_pure_prem = layer.epi_100 * other_method_pure_rate if layer.epi_100 is not None and layer.epi_100 !=0 else 0
        layer.pricing_selection.other_method.pure_rol = 0
        layer.pricing_selection.other_method.pure_rol = other_method_pure_prem / layer.limit  if layer.limit is not None and layer.limit !=0 else 0


    ##############################
    ## Assign Final selection
    ##############################
        method_list = [
            "risk_profile_bdx",
            "limit_average_severity",
            "burning_cost",
            "clash",
            "healthcare_cat",
            "other_method",
        ]

        methods_to_remove = set()

        if ms.is_steer:
            methods_to_remove = {
                "clash",
                "healthcare_cat",
            }

        elif ms.is_clash:
            methods_to_remove = {
                "risk_profile_bdx",
                "limit_average_severity",
                "burning_cost",
                "healthcare_cat",
            }

        elif ms.is_healthcare_cat:
            methods_to_remove = {
                "risk_profile_bdx",
                "limit_average_severity",
                "burning_cost",
                "clash",
            }

        method_list = [
            method
            for method in method_list
            if method not in methods_to_remove
        ]


        total_weighting = 0
        total_pure_prem = 0
        for method in method_list:
            total_weighting = total_weighting + (getattr(layer.pricing_selection,method).weighting or 0)
            total_pure_prem = total_pure_prem + (getattr(layer.pricing_selection,method).weighting or 0) * (getattr(layer.pricing_selection,method).pure_premium or 0)

        layer.pricing_selection.final_selection.total_weighting = total_weighting
        layer.pricing_selection.final_selection.pure_premium = total_pure_prem
        layer.pricing_selection.final_selection.pure_rate = total_pure_prem / layer.epi_100 if layer.epi_100 is not None and layer.epi_100 !=0 else 0
        layer.pricing_selection.final_selection.pure_rol = total_pure_prem / layer.limit if layer.limit is not None and layer.limit!=0 else 0
        

        is_exposure_method = False
        exposure_method_list = [method for method in method_list if method != "burning_cost"]

        total_exposure_weighting = 0
        for method in exposure_method_list:
            total_exposure_weighting = total_exposure_weighting + (getattr(layer.pricing_selection,method).weighting or 0)
        
        total_experience_weighting = 0
        total_experience_weighting = layer.pricing_selection.burning_cost.weighting or 0
        
        is_exposure_method = (total_weighting == total_exposure_weighting) and (total_experience_weighting == 0)
        is_experience_method = (total_weighting == total_experience_weighting) and ( total_exposure_weighting== 0)
        
        if is_exposure_method:
            layer.pricing_selection.final_selection.plr_method = "Exposure"
        elif is_experience_method:
            layer.pricing_selection.final_selection.plr_method = "Burning Cost"
        else:
            layer.pricing_selection.final_selection.plr_method = "Blend"


    ##############################
    ## Set check and message if pure premium is calculated
    ##############################
    has_zero_pure_premium = True
    has_zero_pure_premium = any(layer.pricing_selection.final_selection.pure_premium == 0 for layer in cds_layers if layer.limit > 1)

    steer_bc_pattern_not_updated = (ms.is_steer_experience_rating and
        (er.is_not_experience_selected_updated))

    error_messages = []

    if has_zero_pure_premium and is_rater_priced:
        error_messages.append("Pricing Selection - ⚠️ Pure premium must be calculated for all layers before calculating Advanced Features. Review weighting.")

    if steer_bc_pattern_not_updated and is_rater_priced:
        error_messages.append("Burning Cost - ⚠️ Burning Cost Pattern must be updated")

    ms.pure_premium_error_message = "\n".join(error_messages)

    ms.is_pure_premium_calculated = not has_zero_pure_premium and not steer_bc_pattern_not_updated
    ms.is_pure_premium_not_calculated = has_zero_pure_premium or steer_bc_pattern_not_updated
    return

@time_me
def steer_rate_pricing_selection(hxd):
    """Pricing Selection for Steer like Burning Cost, Risk bdx and LAS bdx"""
    ##############################
    ## Initialise variables
    ##############################

    cds = hxd.cds
    cds_layers = cds.layers
    expe_r = cds.steer.experience_rating
    expo_r = cds.steer.exposure_rating

    for layer_num, layer in enumerate(cds_layers):
        layer_name = f"layer_{layer_num+1:02d}"

        ##############################
        ## Assign Risk Bdx 
        ##############################
        layer.pricing_selection.risk_profile_bdx.pure_rate = risk_bdx_pure_rate = layer.risk_profile_bdx.rate_on_npi or 0
        layer.pricing_selection.risk_profile_bdx.cedant_loss_ratio = layer.risk_profile_bdx.exposure_lr or 0
        layer.pricing_selection.risk_profile_bdx.pure_premium = 0
        layer.pricing_selection.risk_profile_bdx.pure_premium = risk_bdx_pure_prem = layer.epi_100 * risk_bdx_pure_rate if layer.epi_100 is not None and layer.epi_100 !=0 else 0
        layer.pricing_selection.risk_profile_bdx.pure_rol = 0
        layer.pricing_selection.risk_profile_bdx.pure_rol = risk_bdx_pure_prem / layer.limit  if layer.limit is not None and layer.limit !=0 else 0

        ##############################
        ## Assign LAS Bdx 
        ##############################
        layer.pricing_selection.limit_average_severity.pure_rate = las_bdx_pure_rate = getattr(expo_r.limit_average_severity.layers,layer_name).pure_rate or 0
        layer.pricing_selection.limit_average_severity.pure_premium = 0
        layer.pricing_selection.limit_average_severity.pure_premium = las_bdx_pure_prem = layer.epi_100 * las_bdx_pure_rate if layer.epi_100 is not None and layer.epi_100 !=0 else 0     
        layer.pricing_selection.limit_average_severity.pure_rol = 0
        layer.pricing_selection.limit_average_severity.pure_rol = las_bdx_pure_prem / layer.limit  if layer.limit is not None and layer.limit !=0 else 0


        ##############################
        ## Assign Burning Cost  
        ##############################
        layer.pricing_selection.burning_cost.pure_rate = bc_pure_rate = getattr(expe_r.layers,layer_name).selected_years_wa.rate_pct or 0
        layer.pricing_selection.burning_cost.ulr = getattr(expe_r.layers,layer_name).selected_years_wa.ulr or 0
        layer.pricing_selection.burning_cost.pure_premium = 0
        layer.pricing_selection.burning_cost.pure_premium = bc_pure_prem = layer.epi_100 * bc_pure_rate if layer.epi_100 is not None and layer.epi_100 !=0 else 0            
        layer.pricing_selection.burning_cost.pure_rol = 0
        layer.pricing_selection.burning_cost.pure_rol = bc_pure_prem / layer.limit  if layer.limit is not None and layer.limit !=0  else 0

    return

@time_me
def healthcare_rate_pricing_selection(hxd):
    """Pricing Selection for Steer like Burning Cost, Risk bdx and LAS bdx"""
    ##############################
    ## Initialise variables
    ##############################

    cds = hxd.cds
    cds_layers = cds.layers

    for layer_num, layer in enumerate(cds_layers):
        layer_name = f"layer_{layer_num+1:02d}"

        ##############################
        ## Assign Risk Bdx 
        ##############################
        layer.pricing_selection.healthcare_cat.pure_premium = healthcare_pure_prem = layer.healthcare_cat.expected_cost_in_layer_total or 0
        layer.pricing_selection.healthcare_cat.pure_rate = utils.ratio(healthcare_pure_prem , (layer.epi_100 or 0))
        layer.pricing_selection.healthcare_cat.pure_rol = utils.ratio(healthcare_pure_prem , (layer.limit or 0))

@time_me
def clash_rate_pricing_selection(hxd):
    """Pricing Selection for Steer like Burning Cost, Risk bdx and LAS bdx"""
    ##############################
    ## Initialise variables
    ##############################

    cds = hxd.cds
    cds_layers = cds.layers

    for layer_num, layer in enumerate(cds_layers):
        layer_name = f"layer_{layer_num+1:02d}"
        ##############################
        ## Assign Risk Bdx 
        ##############################
        layer.pricing_selection.clash.pure_rate = clash_pure_rate = 0 # TODO - To assign to clash once built
        layer.pricing_selection.clash.pure_premium = 0
        layer.pricing_selection.clash.pure_premium = clash_pure_prem = layer.epi_100 * clash_pure_rate if layer.epi_100 is not None and layer.epi_100 !=0 else 0
        layer.pricing_selection.clash.pure_rol = 0
        layer.pricing_selection.clash.pure_rol = clash_pure_prem / layer.limit  if layer.limit is not None and layer.limit !=0  else 0 