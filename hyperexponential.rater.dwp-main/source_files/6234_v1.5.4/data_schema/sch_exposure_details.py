import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

# Replace / remove examples with your models exposures

def sch_exposure_details(cds):
    cds.extend_node_rater_defined("cds/exposure/granular", {        
        "education": hx.List(mode="input",  async_input=["rarc_task"], children={
            "institution_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Name of\nInstitution"}, async_input=["rarc_task"]),
            "num_schools": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Number of\nSchools"}, validation={"min_value": 0}, async_input=["rarc_task"]),
            "country": hx.Str(mode="input", default=None, optionality="optional",options_table="country_rates", options_column="Country", view={"label": "Country"}, async_input=["rarc_task"]),
            "state_code": hx.Str(mode="input", options_table="lst_state_lookup", options_column="State Code", default=None, optionality="optional", view={"label": "State Code"}, async_input=["rarc_task"]),
            "state_name": hx.Str(mode="output", optionality="optional", view={"label": "State Name"}, async_input=["rarc_task"]),
            "city_risk": hx.Str(mode="input", options_table="city_risk_factor", options_column="City Risk", default=None, optionality="optional", view={"label": "City Risk"}, async_input=["rarc_task"]),
            "location": hx.Str(mode="input", options_table="location_factor", options_column="Field", default=None, optionality="optional", view={"label": "Location"}, async_input=["rarc_task"]),
            "school_grade": hx.Str(mode="input", options_table="school_grade_factor", options_column="Field", default=None, optionality="optional", view={"label": "School Grade"}, async_input=["rarc_task"]),
            "school_type": hx.Str(mode="input", options_table="school_type_factor", options_column="Field", default=None, optionality="optional", view={"label": "School Type"}, async_input=["rarc_task"]),
            "boarding_day": hx.Str(mode="input", options_table="boarding_day_factor", options_column="Field", default_index=0, optionality="optional", view={"label": "Boarding /\nDay"}, async_input=["rarc_task"]),
            "num_students": hx.Int(mode="input", default=None, optionality="optional", view={"label": "# Students"}, validation={"min_value": 0}, async_input=["rarc_task"]),
            "num_employees": hx.Int(mode="input", default=None, optionality="optional", view={"label": "# Employees"}, async_input=["rarc_task"]),
            "sex_of_school": hx.Str(mode="input", options_table="school_sex_factor", options_column="Field", default_index=0, optionality="optional", view={"label": "Sex of School"}, async_input=["rarc_task"]),
            "num_req_counselling": hx.Float(mode="output", optionality="optional", view={"label": "# Req'g\nCounselling", "format": integer_format(0)}, async_input=["rarc_task"]),
            "factor_city_risk": hx.Float(mode="output", optionality="optional", view={"label": "City Risk\nFactor"}, async_input=["rarc_task"]),
            "rate_multiplier": hx.Float(mode="output", optionality="optional", async_input=["rarc_task"]),
        }),
        "non_education": hx.List(mode="input",  async_input=["rarc_task"], children={
            "establishment_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Name of Est."}, async_input=["rarc_task"]),
            "sector": hx.Structure(view={"linked_options_selector": "hierarchical"}, linked_options_table="sector_subsector_rates", linked_options_columns=["Sector", "SubSector"], children={
                "sector": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Sector"}, async_input=["rarc_task"]),
                "sub_sector": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Sub-Sector"}, async_input=["rarc_task"]),
            }),            
            "num_of_est": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Number of Est."}, validation={"min_value": 0}, async_input=["rarc_task"]),
            "country": hx.Str(mode="input", default=None, optionality="optional",options_table="country_rates", options_column="Country", view={"label": "Country"}, async_input=["rarc_task"]),
            "state_code": hx.Str(mode="input", options_table="lst_state_lookup", options_column="State Code", default=None, optionality="optional", view={"label": "State Code"}, async_input=["rarc_task"]),
            "state_name": hx.Str(mode="output", optionality="optional", view={"label": "State Name"}, async_input=["rarc_task"]),
            "city_risk": hx.Str(mode="input", options_table="city_risk_factor", options_column="City Risk", default=None, optionality="optional", view={"label": "City Risk"}, async_input=["rarc_task"]),
            "location": hx.Str(mode="input", options_table="location_factor", options_column="Field", default=None, optionality="optional", view={"label": "Location"}, async_input=["rarc_task"]),
            "footfall_measure": hx.Str(mode="output", view={"label": "Footfall\nMeasure"}, async_input=["rarc_task"]),
            "num_of_staff_per_est": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Number of\nStaff Per Est."}, validation={"min_value": 0}, async_input=["rarc_task"]),
            "footfall_measure_per_est": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Footfall\nMeasure per\nEst. (NOT Staff)", "format": thousands_format(0)}, async_input=["rarc_task"]),
            "east_of_access": hx.Str(mode="input", options_table="ease_of_access", options_column="Ease of Access", default=None, optionality="optional", view={"label": "Ease of\naccess"}, async_input=["rarc_task"]),
            "enclosed_space": hx.Str(mode="input", options_table="enclosed_space_factor", options_column="Enclosed Space", default=None, optionality="optional", view={"label": "Enclosed\nspace"}, async_input=["rarc_task"]),
            "num_of_days": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Number of\ndays (events\nonly)"}, validation={"min_value": 0}, async_input=["rarc_task"]),
            "num_req_counselling": hx.Float(mode="output", optionality="optional", view={"label": "# Req'g Counselling\nPer Event\n(Observers)", "format": integer_format(0)}, async_input=["rarc_task"]),
            "footfall_band": hx.Str(mode="output", optionality="optional", view={"label": "Footfall\nBand"}, async_input=["rarc_task"]),
            "factor_city_risk": hx.Float(mode="output", optionality="optional", view={"label": "City Risk\nFactor"}, async_input=["rarc_task"]),
            "rate_multiplier": hx.Float(mode="output", optionality="optional", async_input=["rarc_task"]),
        })
    })

    cds.extend_node_rater_defined("cds/exposure/aggregate", {        
        "total_schools": hx.Float(mode="output", view={"label": "Total Schools"}),
        "total_non_ed_est": hx.Float(mode="output", view={"label": "Total Establishments (Non-Ed)"}),
    })
    

