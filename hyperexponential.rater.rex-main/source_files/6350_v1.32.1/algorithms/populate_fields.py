import hx
import hashlib
import re
import functools
import pandas as pd
from operator import attrgetter
from algorithms.constant import MAX_OPTIONS
from algorithms.info import machinery_breakdown_msg, equipment_breakdown_msg, cyber_msg, remodelling_info_msg, deductible_info_msg


def populate_text(hxd):
    '''
    Function that populates the default text box in the model
    '''

    # Page Policy Info - Section Sublimit
    hxd.sublimit.sublimit_warning = "\* Not by Layer"

    # Page Deductibles
    
    for layer in hxd.layers:
        for peril in ["named_windstorm", "scs", "flood", "quake"]:
            for index in range(1, MAX_OPTIONS + 1):
                option = attrgetter(f"perils.{peril}.location_ded.option_{index}")(layer)
                if option.type == "Percentage with a $ minimum":
                    option.cell_to_fill = "% + Location Min/Max"
                elif option.type == "Fixed $ amount":
                    option.cell_to_fill = "Location Min/Max Only"
                elif option.type == "Percentage uncapped":
                    option.cell_to_fill = "% Only"
                elif option.type == "No deductible":
                    option.cell_to_fill = "None"
                elif option.type == "Percentage capped by $ amount":
                    option.cell_to_fill = "% + Location Min/Max"
                else:
                    option.cell_to_fill = "None"

    # Page schedule
    currency = hxd.policy_information.slip_currency

    # Names for Intl Peril Columns
    hxd.model_state.min_ded_label = f"Base / Minimum\nDeductible ({currency})"
    hxd.model_state.max_ded_label = f"Maximum\nDeductible ({currency})"
    hxd.model_state.sublimit_label = f"Sublimit ({currency})"

    if hxd.policy_information.large_schedule_model:
        large_workflow_structure = hxd.schedule.large_schedule_workflow
        large_workflow_structure.run_rater_information = ""
        if large_workflow_structure.load_from_em_database:
            large_workflow_structure.run_rater_information += f"{large_workflow_structure.num_of_locations} locations loaded from EM database \n"
        elif large_workflow_structure.load_from_schedule_file:
            large_workflow_structure.run_rater_information += f"{large_workflow_structure.num_of_locations} locations loaded from schedule file \n"
        else:
            large_workflow_structure.run_rater_information += f"Please load locations data from EM database/schedule file \n"
        
        if large_workflow_structure.spatial_key_updated:
            large_workflow_structure.run_rater_information += f"\U0001F7E2Spatial key result is aligned with the latest schedule \n"
        else:
            large_workflow_structure.run_rater_information += f"\U0001F534Please rerun spatial key with the latest schedule \n"
        
        if hxd.policy_information.accgrpid:
            if large_workflow_structure.simulation_updated:
                large_workflow_structure.run_rater_information += f"\U0001F7E2Simulation result is aligned with the latest schedule \n"
            else:
                large_workflow_structure.run_rater_information += f"\U0001F534Please rerun simulation with the latest schedule \n"
    else:
        small_workflow_structure = hxd.schedule.small_schedule_workflow
        small_workflow_structure.run_rater_information = ""

        small_workflow_structure.run_rater_information += f"{hxd.schedule.schedule_total.num_locs} locations loaded to schedule table \n"

        input_data = [{
            "LocID": row.loc_id,
            "BI TIV": row.tiv_bi,
            "Building TIV": row.tiv_buildings,
            "Contents TIV": row.tiv_contents,
            "Other TIV": row.tiv_other,
            "Total TIV": (row.tiv_bi or 0) + (row.tiv_buildings or 0) + (row.tiv_contents or 0) + (row.tiv_other or 0),
            "City": row.address_dropdown.city,
            "Country": row.address_dropdown.country,
            # "County": row.address_dropdown.county,
            # "StateCode": row.address_dropdown.state,
            "Constr Code": row.constr_code,
            "Sprinklered": row.sprinkler,
            "StreetName": row.street_name,
            "Occupancy": row.industry_occupancy_dropdown.occupancy
        } for row in hxd.schedule.schedule_table]

        schedule_df = pd.DataFrame(input_data)
        schedule_hash = hashlib.sha256(pd.util.hash_pandas_object(schedule_df, index=True).values).hexdigest()

        if schedule_hash == hxd.schedule.small_schedule_workflow.spatial_key_hash:
            small_workflow_structure.run_rater_information += f"\U0001F7E2Spatial key result is aligned with the latest schedule \n"
        else:
            small_workflow_structure.run_rater_information += f"\U0001F534Please rerun spatial key with the latest schedule \n"

        if hxd.policy_information.accgrpid:
            if small_workflow_structure.simulation_updated:
                small_workflow_structure.run_rater_information += f"\U0001F7E2Simulation result is aligned with the latest schedule \n"
            else:
                small_workflow_structure.run_rater_information += f"\U0001F534Please rerun simulation with the latest schedule \n"


    # Default fields (Placeholder)
    hxd.hx_core.model_premium = 0
    hxd.hx_core.charged_premium = 0
    hxd.hx_core.ulr = 0
    hxd.hx_core.premium_currency = ""

            

def populate_dropdown(hxd):
    '''
    Populates dynamic dropdown
    '''
    non_cat_table = hx.params.non_cat_base_rates

    # Page Policy Info - Equipment Breakdown
    hxd.non_layer_perils.equipment_breakdown.industry_dropdown = sorted(set(non_cat_table['Industry']))
    hxd.non_layer_perils.equipment_breakdown.occupancy_dropdown = non_cat_table[non_cat_table['Industry'] == hxd.non_layer_perils.equipment_breakdown.industry.selected]["Occupancy"]

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def validation_run_schedule_rater_error(hxd, run_rater_data, simulation_data = {"Available" : "No"}):
    
    # Run Schedule Rater & Simulation Input Validation:
    input_checks = dict()
    simulation_checks = dict()

    # Sublimit Checks
    input_checks["ws_sublimit_check"] = ((hxd.sublimit.ws_sublimit / (hxd.policy_information.exchange_rate or 1)) if hxd.sublimit.ws_sublimit else 0) == run_rater_data["ws_policy_sublimit_usd_layer1"]
    input_checks["scs_sublimit_check"] = ((hxd.sublimit.scs_sublimit / (hxd.policy_information.exchange_rate or 1)) if hxd.sublimit.scs_sublimit else 0) == run_rater_data["scs_policy_sublimit_usd_layer1"]
    input_checks["fl_sublimit_check"] = ((hxd.sublimit.fl_sublimit / (hxd.policy_information.exchange_rate or 1)) if hxd.sublimit.fl_sublimit else 0) == run_rater_data["fl_policy_sublimit_usd_layer1"]
    input_checks["eq_sublimit_check"] = ((hxd.sublimit.eq_sublimit / (hxd.policy_information.exchange_rate or 1)) if hxd.sublimit.eq_sublimit else 0) == run_rater_data["eq_policy_sublimit_usd_layer1"]

    # Layer Input Checks
    sim_required = False
    for index, layer in enumerate(hxd.layers, start=1):
        input_checks[f"excess_check_{index}"] = (layer.excess / (hxd.policy_information.exchange_rate or 1)) == run_rater_data.get(f"policy_excess_usd_layer{index}", 0)
        input_checks[f"limit_check_{index}"] = (layer.limit / (hxd.policy_information.exchange_rate or 1)) == run_rater_data.get(f"policy_limit_usd_layer{index}", 0)
        input_checks[f"fire_ded_check_{index}"] = ((layer.perils.fire.deductible / (hxd.policy_information.exchange_rate or 1)) if layer.perils.fire.deductible else 0) == run_rater_data.get(f"policy_fire_deductible_usd_layer{index}", 0)
        input_checks[f"achieved_premium_100_gg_check_{index}"] = ((layer.achieved_premium_100_gg / (hxd.policy_information.exchange_rate or 1)) if layer.achieved_premium_100_gg else 0) == run_rater_data.get(f"achieved_premium_100_gg_usd_layer{index}", 0)

        simulation_checks[f"excess_check_{index}"] = layer.excess == simulation_data.get(f"simulation_excess{index}", 0)
        simulation_checks[f"limit_check_{index}"] = layer.limit == simulation_data.get(f"simulation_limit{index}", 0)

        sim_required = (layer.risk_appetite_summary.us_wind_aal != 0) or (layer.risk_appetite_summary.us_quake_aal != 0) or (layer.risk_appetite_summary.intl_wind_aal != 0) or (layer.risk_appetite_summary.intl_quake_aal != 0) or sim_required

    # Schedule Rater Checks
    run_schedule_rate_check = all(input_checks.values())

    # Simulation Checks
    has_simulation_validation_data = (
        isinstance(simulation_data, dict)
        and any(key.startswith("simulation_") for key in simulation_data.keys())
    )

    run_simulation_check = (
        all(simulation_checks.values())
        if sim_required and has_simulation_validation_data
        else True
    )

    # Validation Messages
    if (not run_simulation_check):
        hx.errors.validation(f"Input values have been changed. Please run the simulations and then the schedule rater again.")
        hxd.policy_information.policy_level_validation = True
    elif (not run_schedule_rate_check):
        hx.errors.validation(f"Input values have been changed. Please run the schedule rater again.")
        hxd.policy_information.policy_level_validation = True

def validation_error(hxd):
    '''
    Populates validation error
    '''

    hxd.policy_information.policy_level_validation = False
                

    for peril in ["fire", "named_windstorm", "scs", "flood", "quake", "wildfire"]:
        total = (rgetattr(hxd.non_layer_perils, f"uw_adjustments.risk_man.{peril}")) + (rgetattr(hxd.non_layer_perils, f"uw_adjustments.experience.{peril}")) + (rgetattr(hxd.non_layer_perils, f"uw_adjustments.valuation.{peril}")) + (rgetattr(hxd.non_layer_perils, f"uw_adjustments.other.{peril}"))
        needs_validation = total < -0.5
        rsetattr(hxd.non_layer_perils.uw_adjustments.total, f"{peril}", total)
        rsetattr(hxd.policy_information.requires_validation, f"{peril}", needs_validation)
        rsetattr(hxd.policy_information.doesnt_require_validation, f"{peril}", not needs_validation)


    # Policy level validation error
    if not hxd.policy_information.insured:
        hx.errors.validation(f"An Insured (Policy Info Tab) must have been entered.")
        hxd.policy_information.policy_level_validation = True
    
    if not hxd.policy_information.underwriter:
        hx.errors.validation(f"An Underwriter (Policy Info Tab) must have been entered.")
        hxd.policy_information.policy_level_validation = True
    
    if not hxd.policy_information.slip_currency:
        hx.errors.validation(f"A Slip Currency (Policy Info Tab) must have been entered.")
        hxd.policy_information.policy_level_validation = True
    
    for index, layer in enumerate(hxd.layers, start=1):
        # Layer Validation Error
        if layer.limit <= 0:
            hx.errors.validation(f"Limit greater than 0 must have been entered for layer {index}")
            hxd.policy_information.policy_level_validation = True
        
        if layer.excess < 0:
            hx.errors.validation(f"Excess greater than or equal to 0 must have been entered for layer {index}")
            hxd.policy_information.policy_level_validation = True
        
        if layer.brokerage < 0:
            hx.errors.validation(f"Brokerage greater than or equal to 0% must have been entered for layer {index}")
            hxd.policy_information.policy_level_validation = True
        
        if not layer.status:
            hx.errors.validation(f"A Status must have been entered for layer {index}")
            hxd.policy_information.policy_level_validation = True

        if layer.status == "Bound":
            if not layer.achieved_premium_100_gg:
                hx.errors.validation(f"An Achieved Premium must have been entered for layer {index} when the status is Bound")
                hxd.policy_information.policy_level_validation = True
            
            if not layer.new_renewal:
                hx.errors.validation(f"New/Renewal must have been entered for layer {index} when the status is Bound")
                hxd.policy_information.policy_level_validation = True
    
            # Matches reference
            team_df = hx.params.team
            if underwriter := hxd.policy_information.underwriter:
                reference_format = team_df[team_df["Initials"] == underwriter]["Reference Format"].iloc[0]
                if reference_format != "":
                    # if reference_format == "......\d\d....\-\d\d":  # NACP old format
                    #     format_description = "6 chars of any type, 2 digits and 4 chars of any type, hyphen, 2 digits"
                    if reference_format == "......\d\d....\-\d\d": # NACP new format to align with WB, 6 chars of any type, 2 digits and 4 chars of any type
                        reference_format = "......\d\d...." # changing this here so we don't change the teams.csv
                        format_description = "6 chars of any type, 2 digits and 4 chars of any type"
                    elif reference_format == "......\d\d....":
                        format_description = "6 char of any type, 2 digits and 4 chars of any type"
                    elif reference_format == "\d\d\d\d\d\d\d\d":
                        format_description = "8 digits"
                    else:
                        break

                    if not re.fullmatch(reference_format, layer.reference):
                        hx.errors.validation(f"For layer {index} the reference must be in the format of {format_description}")
                        hxd.policy_information.policy_level_validation = True    

                    for i in range(1, 7):
                        if getattr(layer, f"additional_reference_{i}") is not None and not re.fullmatch(reference_format, getattr(layer, f"additional_reference_{i}")):
                            hx.errors.validation(f"For layer {index}, additional reference {i} must be in the format of {format_description}")
                            hxd.policy_information.policy_level_validation = True    
                            
        # Deductible Error check
        for peril_struct_name, peril_display_name in zip(["fire", "wildfire"], ["Fire", "Wildfire"]):
            deductible = getattr(getattr(layer.perils, peril_struct_name), "deductible")
            if deductible and deductible < 0:
                hx.errors.validation(f"{peril_display_name} Deductible must not be negative for layer {index}")
                hxd.policy_information.policy_level_validation = True  

        for peril_struct_name, peril_display_name in zip(
                    ["named_windstorm", "scs", "flood", "quake"], 
                    ["Named Windstorm", "Severe Convective Storm", "Flood", "Quake"]):
            # Per Occurance Deductible check
            per_occurrence_ded = getattr(getattr(layer.perils, peril_struct_name), "per_occurrence_ded")
            if per_occurrence_ded and per_occurrence_ded < 0:
                hx.errors.validation(f"{peril_display_name} Per Occurence Deductible must not be negative for layer {index}")
                hxd.policy_information.policy_level_validation = True  

            for option_index in range(1, MAX_OPTIONS + 1):
                option = attrgetter(f"perils.{peril_struct_name}.location_ded.option_{option_index}")(layer)
                # Option Percent validation
                if option.percent and option.percent < 0:
                    hx.errors.validation(f"{peril_display_name} % must not be negative for option {option_index} layer {index}")
                    hxd.policy_information.policy_level_validation = True
                # Option Location deductible validation
                if option.location_min_max and option.location_min_max < 0:
                    hx.errors.validation(f"{peril_display_name} location min/max must not be negative for option {option_index} layer {index}")
                    hxd.policy_information.policy_level_validation = True
                # Option sublimit validation
                if option.sublimit and option.sublimit < 0:
                    hx.errors.validation(f"{peril_display_name} sublimit must not be negative for option {option_index} layer {index}")
                    hxd.policy_information.policy_level_validation = True
    
    for peril_abbr, peril_display_name in zip(["ws", "scs", "fl", "eq"], ["Named Windstorm", "Severe Convective Storm", "Flood", "Quake"]):
        sublimit = getattr(hxd.sublimit, f"{peril_abbr}_sublimit")
        if sublimit and sublimit < 0:
            hx.errors.validation(f"{peril_display_name} sublimit must not be negative.")

    # Underwriter Adjustment validation error
    for peril in ["fire", "named_windstorm", "scs", "flood", "quake", "wildfire"]:
        if getattr(hxd.policy_information.requires_validation, f"{peril}"):
            hx.errors.validation(f"Underwriter Adjustments for {peril} exceeds -50%. Please review.")
            hxd.policy_information.policy_level_validation = True

    # Schedule table validation error
    for row in hxd.schedule.schedule_table:
        if row.loc_id and not (row.industry_occupancy_dropdown.industry and row.industry_occupancy_dropdown.occupancy):
            hx.errors.validation(f"Industry and Occupancy not entered for all locations.")
            hxd.policy_information.policy_level_validation = True
            # break as we only need to show the error once
            break

    if hxd.policy_information.large_schedule_model:
        if hxd.policy_information.policy_level_validation:
            hxd.schedule.large_schedule_workflow.run_rater_information += "\U0001F534Please clear all validation errors (X on the button right corner) before running the rater \n"
        else:
            hxd.schedule.large_schedule_workflow.run_rater_information += "\U0001F7E2No validation error \n"
    else:
        if hxd.policy_information.policy_level_validation:
            hxd.schedule.small_schedule_workflow.run_rater_information += "\U0001F534Please clear all validation errors (X on the button right corner) before running the rater \n"
        else:
            hxd.schedule.small_schedule_workflow.run_rater_information += "\U0001F7E2No validation error \n"

    if (hxd.experience_rating.experience_rating_run or False) == True and (hxd.experience_rating.run_rater_run or False) == False:
        hx.errors.validation("Please re-run rater after applying non-cat experience rating adjustments.")
        hxd.policy_information.policy_level_validation = True

        
def populate_notifications(hxd):

    # populate notification box for reminder to mark as final
    finalise_reminder = ""
    # populate notification box for UW rationale tab requirements
    prem_threshold = ""

    for index, layer in enumerate(hxd.layers, start=1):
        if layer.status == "Bound" and hxd.policy_information.policy_level_validation == False:
            finalise_reminder = "- Remember to change the status of this risk to FINAL before exiting the rater."

        writ_line = (layer.written_line_perc if layer.status in {'Bound', 'MTA', 'Cancellation'} else layer.quoted_line_perc) or None

        if not hxd.rationale.first_saved and layer.achieved_premium_100_gg != None and writ_line != None:
            if ((((layer.achieved_premium_100_gg * writ_line) / hxd.policy_information.exchange_rate) if hxd.policy_information.exchange_rate else (layer.achieved_premium_100_gg  * writ_line))  * (1 - layer.brokerage))>= 250000:
                prem_threshold += str(index) + ", "

            elif layer.new_renewal == "New" and ((((layer.achieved_premium_100_gg * writ_line) / hxd.policy_information.exchange_rate) if hxd.policy_information.exchange_rate else (layer.achieved_premium_100_gg  * writ_line))  * (1 - layer.brokerage))>= 100000:
                prem_threshold += str(index) + ", "

    if prem_threshold != "": 
        prem_threshold = prem_threshold.removesuffix(', ')
        if len(prem_threshold) > 1: 
            prem_threshold = prem_threshold[:-3] + " and " + prem_threshold[-1]


        prem_threshold = (f"- The rationale tab may need to be filled out for layer(s) {prem_threshold}. If needed, please complete it for the layer that will be bound.")


    complex_policy = ""
    if hxd.rationale.fill_rationale == True and not hxd.rationale.first_saved:
        complex_policy = "- You have indicated that this is a complex policy. Please make sure to fill out the rationale tab for the layer that will be bound"


 
    # populates notification for climate questions   
    climate_questions = ""
    for index, layer in enumerate(hxd.layers, start=1):
        if hxd.non_layer_summary.climate_metrics.weighted_climate_score != None:
            if layer.new_renewal == "Renewal" and hxd.non_layer_summary.climate_metrics.weighted_climate_score >= 4:
                climate_questions = "- If we are leading this account please fill out the climate section."



    # Sets each comment to a new line and combines them into one comment
    notifications = ""
    for notification in (finalise_reminder, prem_threshold, complex_policy, climate_questions):
        if notification != "":
            notifications += notification +  " \n"

    hxd.policy_information.notifications.notification_box = notifications
    
    # hide show/hide button when there are no notifications
    if notifications != "":
        hxd.policy_information.notifications.notifications_populated = True
    else:
        hxd.policy_information.notifications.notifications_populated = False


    # hide notifications when the show/hide button is pressed
    if hxd.policy_information.notifications.notification_box != "" and hxd.policy_information.notifications.show_hide == True:
        hxd.policy_information.notifications.show_notifications = True
    else:
        hxd.policy_information.notifications.show_notifications = False

def initial_quoted_inputs(hxd):
    bound_set = {'Bound', 'MTA', 'Cancellation'}
    statuses = [layer.status for layer in hxd.layers]
    bound_status = [status in bound_set for status in statuses]
    
    # Written line validation
    wrt_line = [layer.written_line_perc == 0 for layer in hxd.layers]
    wrt_line_val = [a and b for a, b in zip(bound_status, wrt_line)]
    if any(wrt_line_val):
        hxd.control.show_wrt_line = False
        hxd.control.show_wrt_line_validation = True
        for idx, s in enumerate(wrt_line_val):
            if s:
                hx.errors.validation(f'Input signed line for bound layer {idx+1}')
    elif any(bound_status):
        hxd.control.show_wrt_line = True
        hxd.control.show_wrt_line_validation = False
    else:
        hxd.control.show_wrt_line = True
        hxd.control.show_wrt_line_validation = False
    
    # Quoted line validation
    quoted_line = [layer.quoted_line_perc == 0 for layer in hxd.layers]
    quoted_line_val = [a and b for a, b in zip(bound_status, quoted_line)]
    for idx, s in enumerate(quoted_line_val):
        if s:
            hx.errors.validation(f'Input quoted line for bound layer {idx+1}')
            
def populate_info_boxes_text(hxd):
    hxd.info.equipment_breakdown_msg = equipment_breakdown_msg
    hxd.info.machinery_breakdown_msg = machinery_breakdown_msg
    hxd.info.remodelling_info_msg = remodelling_info_msg
    hxd.non_layer_perils.cyber.info_note = cyber_msg
    hxd.info.deductible_info = deductible_info_msg


def show_hide_notifications(hxd, progress):
    hxd.policy_information.notifications.show_hide = not hxd.policy_information.notifications.show_hide


def validate_hurricane(hxd):
    if hxd.non_layer_summary.climate_metrics.client_questions.risk_mitigation_measures.answer != None and hxd.non_layer_summary.climate_metrics.client_questions.risk_mitigation_measures.answer == "Yes":
        hxd.non_layer_summary.climate_metrics.client_questions.risk_mitigation_measures.show_risk_mitigation_measures = True

    if hxd.non_layer_summary.climate_metrics.client_questions.additional_risk_mitigation_practices.answer != None and hxd.non_layer_summary.climate_metrics.client_questions.additional_risk_mitigation_practices.answer == "Yes":
        hxd.non_layer_summary.climate_metrics.client_questions.additional_risk_mitigation_practices.show_additional_risk_mitigation_practices = True