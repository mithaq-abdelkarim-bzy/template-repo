import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params



def sch_triage(cds):
    
        
    #----------------------------------------------------------------------------------------------#
    # Structure housing granular exposure details 
    #----------------------------------------------------------------------------------------------#

    cds.extend_node_rater_defined("cds/exposure/granular", {
        
        #This list sets out the triage details
        "triage_doctors_residents": hx.List(mode="input", default_element_count=154,children={
            "specialty": hx.Str(mode="output", view={"label":"Specialty"},async_input=["generate_email_task","generate_referral_email_task"]),
            "iso_code": hx.Str(mode="output", view={"label": "ISO Code"}),
            "iso_class": hx.Str(mode="output", view={"label": "Class"}),
            "obe_per_doctor": hx.Float(mode="output", view={"label": "OBE Per Doctor","format":utils.integer_format(1)},async_input=["generate_email_task","generate_referral_email_task"]),
            "doc_four_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Employed Doctors \nFour Years Ago","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000}),
            "doc_three_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Employed Doctors \nThree Years Ago","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000}),
            "doc_two_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Employed Doctors \nTwo Years Ago","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000}),
            "doc_one_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Employed Doctors \nPrevious Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000}),
            "doc_current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model","generate_email_task","generate_referral_email_task"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Employed Doctors \nCurrent Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000}),
            "obe_per_resident": hx.Float(mode="output", view={"label": "OBE Per Resident","format":utils.integer_format(1)},async_input=["generate_email_task","generate_referral_email_task"]),
            "resident_four_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Residents \nFour Years Ago","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
            "resident_three_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Residents \nThree Years Ago","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
            "resident_two_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Residents \nTwo Years Ago","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
            "resident_one_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Residents \nPrevious Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
            "resident_current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model","generate_email_task","generate_referral_email_task"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Residents \nCurrent Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
         }),

        #This list sets out the triage details
        

        "triage_procedures": hx.List(mode="input", default_element_count=18,children={
            "category": hx.Str(mode="output", view={"label":"Category"},async_input=["generate_email_task","generate_referral_email_task"]),
            "exposure_measure": hx.Str(mode="output", view={"label": "Exposure"},async_input=["generate_email_task","generate_referral_email_task"]),
            "obe_or_fte": hx.Float(mode="output", view={"label": "OBE Per","format":utils.integer_format(5)},async_input=["generate_email_task","generate_referral_email_task"]),
            "formatted_obe_or_fte": hx.Str(mode="output", view={"label": "OBE or FTE Relativity"}),
            "four_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Four Years Ago","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
            "three_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Three Years Ago","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
            "two_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Two Years Ago","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
            "one_years_ago": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Previous Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
            "current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model","generate_email_task","generate_referral_email_task"], async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="required", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),
         }),

         "triage_historical_obe": hx.List(mode="input", default_element_count=36,children={
            "category": hx.Str(mode="output", view={"label":"Category"}),
            "exposure_measure": hx.Str(mode="output", view={"label": "Exposure"}),
            "obe_or_fte": hx.Float(mode="output", view={"label": "OBE or FTE Relativity","format":utils.integer_format(2)}),
            "formatted_obe_or_fte": hx.Str(mode="output", view={"label": "OBE or FTE Relativity"}),
            "obe_equivalent": hx.Float(mode="output", view={"label": "OBE Equivalent","format":utils.integer_format(2)}),
            "overall_obe": hx.Float(mode="output", view={"label": "Overall OBE","format":utils.integer_format(2)}),
            "four_years_ago": hx.Float(mode="output", view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            "three_years_ago": hx.Float(mode="output", view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            "two_years_ago": hx.Float(mode="output", view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            "one_years_ago": hx.Float(mode="output", view={"label": "Previous Year","format":utils.thousands_format(0)}),
            "current_year": hx.Float(mode="output", view={"label": "Current Year","format":utils.thousands_format(0)}),
         }),
    })

    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "triage_running_total_obe": hx.List(mode="input", fixed_element_count=1,children={
            "four_years_ago": hx.Float(mode="output", view={"label": "Total OBE: \nFour Years Ago","format":utils.thousands_format(0)}),
            "three_years_ago": hx.Float(mode="output", view={"label": "Total OBE: \nThree Years Ago","format":utils.thousands_format(0)}),
            "two_years_ago": hx.Float(mode="output", view={"label": "Total OBE: \nTwo Years Ago","format":utils.thousands_format(0)}), 
            "one_years_ago": hx.Float(mode="output", view={"label": "Total OBE: \nPrevious Year","format":utils.thousands_format(0)}),
            "current_year": hx.Float(mode="output",async_input=["generate_email_task","generate_referral_email_task"], view={"label": "Total OBE: \nCurrent Year","format":utils.thousands_format(0)}),
        }),
    })
    
        