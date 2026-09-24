# v0.5.0
import hx
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, remove_before_separator, shift_dataframe_columns
import algorithms.rate_constants as const
def task_start_renewal(hxd, progress):
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    
    ##############################
    ## Initialise variables
    ##############################

    ms = hxd.model_state
    sf = hxd.cds.standard_fields
    steer_er = hxd.cds.steer.experience_rating

    inception_date = hxd.hx_core.inception_date

    expo_ass_df = pd_df_from_hx_list(steer_er.on_levelling.exposure_assumptions)

    hc_trial_history_df = pd_df_from_hx_list(hxd.cds.healthcare_cat.trial_history.trial)

    hc_expo_p_year_df = pd_df_from_hx_list(hxd.cds.healthcare_cat.exposure_territory.overall_exposure_per_year)


    ##############################
    ## Landing Page and expiry poi assignements
    ##############################

    if not hxd.cds.standard_fields.insured_name:
        ms.landing_page_info = "❗**FAILED**: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner.❗"
    else:
        ms.pressed_start_renewal_task = True
        ms.expiring_policy_option_id = expiring_policy_option_id = hx.meta.expiring_policy_option_id
        sf.is_renewal = True
        # Add tasks which must be done before starting a policy here >>
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id # Assigning this node in this tasks allows to clear the override at the creation of a renewal

    ##############################
    ## Input aging - Get aging step
    ##############################
    # get expiry inception date

    # For debug
    # expiring_policy_option_id = 1726411
    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]

    expiry_inception_date = expiring_data["hx_core"]["inception_date"]
    expiring_year = int(expiring_data["hx_core"]["inception_date"][:4])
    # calculate aging_year

    aging_step = max(0, inception_date.year - int(expiring_data["hx_core"]["inception_date"][:4]))

    # For debug
    # aging_step=2

    ##############################
    ## STEER
    ##############################

    if ms.is_steer == True:

    ##############################
    ## Input aging STEER: On LEVELLED
    ##############################
        expo_ass_columns_to_shift=[
                "exposure",
                "annual_rate_change",
                "claims_inflation",
                "exposure_adjusted_layer_01",
                "exposure_adjusted_layer_02",
                "exposure_adjusted_layer_03",
                "exposure_adjusted_layer_04",
                "exposure_adjusted_layer_05",
            ]
        
        expo_ass_df = shift_dataframe_columns(
            expo_ass_df,
            columns_to_shift=expo_ass_columns_to_shift,
            aging_step=aging_step,
            
        )
        
        expo_ass_df[expo_ass_columns_to_shift ] = expo_ass_df[expo_ass_columns_to_shift ].fillna(0)
        # write to hxd
        write_pd_to_hxd(expo_ass_df,  steer_er.on_levelling.exposure_assumptions,  expo_ass_columns_to_shift )


    ##############################
    ## Input aging STEER: BURNING COST
    ##############################

        # fgu
        bc_columns_to_shift_with_default=[
            {"column_name":"weighting","default_value":1},
            {"column_name":"premium","default_value":0}
        ]

        bc_columns_to_shift = [item["column_name"] for item in bc_columns_to_shift_with_default]
        
        bc_fgu_df = pd_df_from_hx_list(steer_er.layers.fgu.burning_cost)
        bc_fgu_df = shift_dataframe_columns(
            bc_fgu_df,
            columns_to_shift=bc_columns_to_shift_with_default,
            aging_step=aging_step,
        )
        
        bc_fgu_df[bc_columns_to_shift ] = bc_fgu_df[bc_columns_to_shift ].fillna(0)
        # write to hxd
        write_pd_to_hxd(bc_fgu_df,  steer_er.layers.fgu.burning_cost ,  bc_columns_to_shift )


        # layers
        for layer_index in range(const.max_layers):
            layer_suffix=f"{layer_index+1:02d}"
            layer_name = f"layer_{layer_suffix}"
            bc_layer_df = pd_df_from_hx_list(getattr(steer_er.layers,layer_name).burning_cost)

            bc_layer_df = shift_dataframe_columns(
                bc_layer_df,
                columns_to_shift=bc_columns_to_shift_with_default,
                aging_step=aging_step,
            )
            
            bc_layer_df[bc_columns_to_shift ] = bc_layer_df[bc_columns_to_shift ].fillna(0)
            # write to hxd
            write_pd_to_hxd(bc_layer_df,  getattr(steer_er.layers,layer_name).burning_cost,  bc_columns_to_shift )


    ##############################
    ## Healthcare CAT
    ##############################
        
    elif ms.is_healthcare_cat == True:
    ##############################
    ## Input aging Healthcare CAT: TRIAL HISTORY
    ##############################

        hc_trial_history_columns_to_shift=[
            "taken_to_trial",
            "wins",
            "losses",
            "mistrials",

        ]
        
        hc_trial_history_df = shift_dataframe_columns(
            hc_trial_history_df,
            columns_to_shift=hc_trial_history_columns_to_shift,
            aging_step=aging_step,
            
        )
        
        hc_trial_history_df[hc_trial_history_columns_to_shift ] = hc_trial_history_df[hc_trial_history_columns_to_shift ].fillna(0)
        # write to hxd
        write_pd_to_hxd(hc_trial_history_df,  hxd.cds.healthcare_cat.trial_history.trial,  hc_trial_history_columns_to_shift )

        ##############################
        ## Input aging Healthcare CAT: EXPOSURE TERRITORY
        ##############################
        # hc_expo_p_year_df
        hc_expo_p_year_columns_to_shift=[
            "physicians",
            "professional_associations",
            "ambulatory_surgery_centres",
            "hospitals",
            "ltc_facilities",
            "other_facilities",
            "dentists",
            "others",
        ]
        
        hc_expo_p_year_df = shift_dataframe_columns(
            hc_expo_p_year_df,
            columns_to_shift=hc_expo_p_year_columns_to_shift,
            aging_step=aging_step,
        )
        
        hc_expo_p_year_df[hc_expo_p_year_columns_to_shift ] = hc_expo_p_year_df[hc_expo_p_year_columns_to_shift ].fillna(0)
        # write to hxd
        write_pd_to_hxd(hc_expo_p_year_df,  hxd.cds.healthcare_cat.exposure_territory.overall_exposure_per_year,  hc_expo_p_year_columns_to_shift )

    else:
        pass

    ##############################
    ## Input removal: ADVANCED FEATURES as resetting async_output 
    ##############################
    
    # Check from Debug console
    # hxd.cds.layers[0].expected_aad
    # hxd.cds.layers[0].loss_corridor_loss_cost
    # hxd.cds.layers[0].expected_reinstatement_factor
    # hxd.cds.layers[0].expected_ncb_pct
    # hxd.cds.layers[0].profit_commission
    # hxd.cds.layers[0].swing_premium



    ##############################
    ## Input removal: Rating Summary References as resetting async_output 
    ##############################
    # Check from Debug console
    # hxd.cds.layers[0].section_reference


    ##############################
    ## Input removal: RATE cHANGE
    ##############################

    # hxd.cds.layers[0].rate_change.exposure_change.uw_override
    # hxd.cds.layers[0].rate_change.exposure_change.uw_override
    # hxd.cds.layers[0].rate_change.risk_characteristics_change.uw_override
    # hxd.cds.layers[0].rate_change.limit_change.uw_override
    # hxd.cds.layers[0].rate_change.deductible_change.uw_override
    # hxd.cds.layers[0].rate_change.terms_conditions_change.uw_override
    # hxd.cds.layers[0].rate_change.other_change.uw_override
    # hxd.cds.layers[0].rate_change.brokerage_change.uw_override
    # hxd.cds.layers[0].rate_change.uw_override.uw_override



