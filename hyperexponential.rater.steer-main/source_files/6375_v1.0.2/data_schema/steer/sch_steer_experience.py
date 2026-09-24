import hx_data_schema as hx
import data_schema.sch_utilities as utils # includes functions thousands_format, percent_format, integer_format)
from algorithms.rate_constants import max_layers, experience_rating_max_years, max_data_layout, reinstatement_max_number, raw_data_max_column
from data_schema.sch_utilities import create_node_from_list, add_year_suffix
from data_schema.sch_rate_change import rarc_task_name


def _steer_experience_on_levelling():
    return {
        "on_levelling": hx.Structure(view={"label": "On Levelling"}, children={
            "measure": hx.Str(mode="input", default="Premium", optionality="optional", options=["Premium","Headcount","Revenue"],view={"label": "Measure"}),
            # 16 years of information: uw_year, exposure, annual_rate_change, rate_change_index, exposure_on_level, exposure_adjusted_layer_{index} from 1 to 6
            ** _steer_experience_years(),
            "future_inflation": hx.Float(mode="input", default=0.0, optionality="optional",view={"label": "Future Inflation", "format": utils.percent_format(2)}),
            "raw_data_comment": hx.Str(mode="output",view={"label": "Raw Data Comment"}),
            # "raw_data": hx.File(mode="input", async_input=["steer_upload_raw_data","steer_validate_raw_data","steer_process_claims"],async_output=["steer_upload_raw_data","steer_validate_raw_data","steer_process_claims"],view={"label": "Raw data"}),
            # "raw_data_error": hx.File(mode="output",async_output=["steer_upload_raw_data","steer_validate_raw_data","steer_process_claims"], file_name="RawDataError.xlsx"),
        }),
    }


def _steer_experience_years():
    """
    Create a list with historical years. The key is as "year_<number>" and set in line with the model constant (experience_rating_max_years).   
    """
    years = {}

    year_node = hx.List(mode="input", async_input=[rarc_task_name,"steer_format_raw_data_task","start_renewal_task"],async_output=[ {"task": "start_renewal_task", "reset": False}], view={"label":"`exposure Assumptions`"},default_element_count=experience_rating_max_years, max_element_count=experience_rating_max_years, min_element_count=experience_rating_max_years, children={
        "display_yoa": hx.Str(mode="output", async_input=[rarc_task_name,"steer_format_raw_data_task","start_renewal_task"],view={"label": "YOA"}),
        "uw_year": hx.Int(mode="output", async_input=[rarc_task_name,"steer_format_raw_data_task","start_renewal_task"], view={"label": "UW Year"}),
        "exposure": hx.Float(mode="input", default=None, optionality="optional", async_input=[rarc_task_name,"steer_format_raw_data_task","start_renewal_task"],async_output=[ {"task": "start_renewal_task", "reset": False}], view={"label": "Exposure", "format": utils.thousands_format(0)}),
        "annual_rate_change": hx.Float(mode="input", default=None, optionality="optional", async_input=[rarc_task_name,"steer_format_raw_data_task","start_renewal_task"],async_output=["start_renewal_task"], view={"label": "Annual\nRate Change", "format": {"output": "percent", "mantissa": 2}}),
        "exposure_on_level": hx.Float(mode="output", async_input=[rarc_task_name,"steer_format_raw_data_task","start_renewal_task"], view={"label": "Exposure\nOn Level", "format": utils.thousands_format(0)}),
        "rate_change_index": hx.Float(mode="output",async_input=[rarc_task_name,"steer_format_raw_data_task","start_renewal_task"],  view={"label": "Rate Change\nIndex", "format": {"output": "percent", "mantissa": 2}}),
        "claims_inflation": hx.Float(mode="input", default=None, optionality="optional", async_input=[rarc_task_name,"steer_format_raw_data_task","start_renewal_task"],async_output=[ {"task": "start_renewal_task", "reset": False}], view={"label": "Claims Inflation", "format": {"output": "percent", "mantissa": 2}}),
        "inflation_index": hx.Float(mode="output", async_input=[rarc_task_name,"steer_format_raw_data_task","start_renewal_task"], view={"label": "Inflation\nIndex", "format": {"output": "percent", "mantissa": 2}}),
            
    })
    for i in range(1, max_layers+1):
        field_name = f"exposure_adjusted_layer_{i:02d}"
        year_node.children[field_name] = hx.Float(mode="input", default=None, optionality="optional", async_input=[rarc_task_name, "steer_format_raw_data_task","start_renewal_task"], async_output=[ {"task": "start_renewal_task", "reset": False}],view={"label": f"Exposure\nAdjusted\nLayer {i}", "format": utils.thousands_format(0)})
    
    years["exposure_assumptions"] = year_node
        
    return years

def _steer_raw_data():
    """
    Create a list of undefined numner of items with 109 colummns to capture the raw data 
    """
    return {
        "raw_data": hx.List(mode="input", async_input=["steer_format_raw_data_task",rarc_task_name],async_output=["steer_clear_raw_data_task",{"task":"steer_validate_raw_data_task","reset":False}],children={
            # f"column_{i}": hx.Str(mode="input", default="", optionality="optional",async_output=["steer_clear_raw_data_task",{"task":"steer_validate_raw_data_task","reset":False}], view={"label": f"Column\n{i}"})
            f"column_{i:02d}": hx.Str(mode="input", default="", optionality="optional",async_input=["steer_format_raw_data_task",rarc_task_name],async_output=["steer_clear_raw_data_task",{"task":"steer_validate_raw_data_task","reset":False}], view={"label": f"Column\n{i}"})
            
            for i in range(1, raw_data_max_column+1)
        })
    }

def _steer_data_format():
    """
    Create assumptions for data mapping and formatting
    """
    return {
        # Misc parameters
        "misc_parameters": hx.Structure(view={"label": "Data Mapping"}, children={
            "target_year": hx.Int(mode="output", async_input=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Target Year","format": {"thousandSeparated": False, "mantissa": 0}}),
            "target_year_info": hx.Str(mode="output", view={"label": "None"}),
            "closed_indicator": hx.Str(mode="input", async_input=["steer_validate_raw_data_task","steer_format_raw_data_task"],default="Closed", view={"label": "Closed Indicator"}),
            "closed_indicator_info": hx.Str(mode="output", view={"label": "None"}),
            "data_layout": hx.Int(mode="input", default=1, validation={"max_value": max_data_layout}, view={"label": "Data Layout"}),
            "data_layout_info": hx.Str(mode="output", view={"label": "None"}),
        }),        
        # data mapping
        "data_mapping": hx.Structure(view={"label": "Data Mapping"}, children={**_steer_data_format_mapping_table_children()
        }),
        # ** _steer_data_format_mapping_table(),

        # "raw_data_column_names": hx.Structure(view={"label": "Raw Data Column Names"}, children={
        #     f"column_{i:02d}": hx.Str(mode="output", view={"label": f"Column\n{i}"})
        #     for i in range(1, raw_data_max_column+1)
        # }),

        # Other fields
        "other_fields": hx.Structure(view={"label": "Other Fields"}, children={**_steer_data_format_other_field_children_nodes()}),


    }

def _steer_data_format_mapping_table_children():
    """
    Create the raw data mapping table children nodes
    """
    fields = [
        ("Reference"),
        ("Claimant"),
        ("Insured"),
        ("Status"),
        ("Incident date"),
        ("Report date"),
        ("Closed date"),
        ("Incident year"),
        ("Policy year"),
        ("Closed year"),
        ("Policy limit"),
        ("Policy excess"),
        ("Indemnity paid"),
        ("Indemnity inc"),
        ("Defense cost paid"),
        ("Defense cost inc"),
        ("Claim paid"),
        ("Claim inc"),
        ]

    raw_data_mapping = {
        f"field_{index+1:02d}": hx.Structure(view={"label": label}, children={**_steer_data_format_field_children_nodes()})
        for index, label in enumerate(fields)
    }
    return raw_data_mapping
    
def _steer_data_format_field_children_nodes():
    """
    Create the children of the structure for data_mapping
    """
    return {
        "field": hx.Str(mode="output", view={"label": "Field"}),
        "field_name": hx.Str(mode="output", async_input=["steer_validate_raw_data_task","steer_format_raw_data_task"],view={"label": "Field Name"}),
        "description": hx.Str(mode="output", async_input=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Description"}),
        "mandatory_column": hx.Str(mode="output", async_input=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Mandatory\nColumn"}),
        "specify_column": hx.Int(mode="input", async_input=["steer_validate_raw_data_task","steer_format_raw_data_task"], default=None, optionality="optional", view={"label": "Specify\nColumn"}),
        "accept_missing": hx.Str(mode="output", view={"label": "Accept\nMissing"}),
        "field_type": hx.Str(mode="output", view={"label": "Field\nType"}),
        "value_within_range": hx.Str(mode="output", view={"label": "Value\nWithin\nRange"}),
        "replace_missing_with_default": hx.Str(mode="output", view={"label": "Replace\nMissing\nWith\nDefault"})
    }

def _steer_data_format_other_field_children_nodes():
    return {
        "fvy": hx.Structure(view={"label": "First Year Of Data Valuation"},children={
            "description": hx.Str(mode="output", view={"label": "Description"}),
            "value": hx.Int(mode="input",default=None, async_input=[rarc_task_name,"steer_validate_raw_data_task","steer_format_raw_data_task","steer_populate_bc_patterns_task"],optionality="optional",validation={"max_value":9999},view={"label": "Value","format": {"thousandSeparated": False, "mantissa": 0}}),
        }),
        "lvy": hx.Structure(view={"label": "Last Year Of Data Valuation"},children={
            "description": hx.Str(mode="output", view={"label": "Description"}),
            "value": hx.Int(mode="output", async_input=["steer_validate_raw_data_task","steer_format_raw_data_task","steer_populate_bc_patterns_task"],optionality="optional",validation={ "max_value":9999},view={"label": "Value","format": {"thousandSeparated": False, "mantissa": 0}}),
        }),
        "coverage_basis": hx.Structure(view={"label": "Coverage Basis"},children={
            "description": hx.Str(mode="output", view={"label": "Description"}),
            "value": hx.Str(mode="input", default="Costs Inclusive", options=["Costs Inclusive", "Costs Exclusive","Costs Pro-Rata"], async_input=[rarc_task_name,"steer_format_raw_data_task"], view={"label": "Value"}),
        }),
        "bcost_measure": hx.Structure(view={"label": "Required for Bcost"},children={
            "description": hx.Str(mode="output", view={"label": "Description"}),
            "value": hx.Str(mode="output", view={"label": "Value"}),
        }),
        "data_as_at_date": hx.Structure(view={"label": "Data As At Date"},children={
            "description": hx.Str(mode="output", view={"label": "Description"}),
            "value": hx.Date(mode="input", default="2020-01-01", async_input=[rarc_task_name,"steer_validate_raw_data_task","steer_format_raw_data_task","steer_populate_bc_patterns_task"],optionality="optional",view={"label": "Value"}),
        }),
    }

def _steer_data_format_column_display():
    """
    Create the children of the structure for column display
    """
    fields = [
        ("reference", "Reference"),
        ("claimant", "Claimant"),
        ("insured", "Insured"),
        ("status", "Status"),
        ("incident_date", "Incident Date"),
        ("report_date", "Report Date"),
        ("closed_date", "Closed Date"),
        ("incident_year", "Incident Year"),
        ("policy_year", "Policy Year"),
        ("closed_year", "Closed Year"),
        ("policy_limit", "Policy Limit"),
        ("policy_excess", "Policy Excess"),
        ("paid", "Paid"),
        ("incurred", "Incurred"),
        ("paid_expenses", "Paid Expenses"),
        ("incurred_expenses", "Incurred Expenses"),
        ("paid_claim_ind", "Paid Claim Indemnity"),
        ("inc_claim_ind", "Incurred Claim Indemnity"),
    

        ("incurred_claims", "Incurred Claim"),
        ("inflated_claims", "Inflated Claim"),
        ("incurred_capped", "Incurred Capped"),

        ("trended_claim", "Trended Claim"),
        ("trended_expenses", "Trended Expenses"),

        ("ri_claim", "RI Claim"),
        ("ri_claim_on_levelled", "RI Claim On-levelled"),
        ("ri_claim_count", "RI Claim Count"),
        ("ri_claim_count_on_levelled", "RI Claim Count On-levelled"),
        # ("ri_claim_ind", "RI Claim Ind"),
        # ("ri_claim_ind_closed", "RI Claim Ind Closed"),
        ("claim_ranking", "Claim Ranking"),
        ("row_number", "Row Number"),
    ]
    
    structure = {
        field: hx.Structure(
            view={"label": label},
            children={
                "show": hx.Bool(mode="input", view={"label": "Show?"}, default=True),
            }
        )
        for field, label in fields
    }
    return structure


def _steer_raw_data_error():
    return {
        "raw_data_error": hx.Structure(view={"label": "Raw Data Error"},children={
            "pre_val_err_messages": hx.Str(mode="input", default=None,optionality="optional",async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Note", "options": {"warning": {"style_cell": "strong-validation", "read_only": True}}}),
            "show_pre_val_err_messages": hx.Bool(mode="output", async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"],view={"label": "Show Pre Validation Error Messages"}),
            "accepted_missing_value": hx.List(mode="output", async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Accepted Missing Value"},children={
                **_steer_raw_data_error_children_nodes(),
            }),
            "field_type": hx.List(mode="output", async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Field type"},children={
                **_steer_raw_data_error_children_nodes(),
            }),
            "value_within_range": hx.List(mode="output", async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Value Within Range"},children={
                **_steer_raw_data_error_children_nodes(),
            }),
        }),
    }
 
def _steer_raw_data_error_children_nodes():
    return {
        "requirement": hx.Str(mode="output", async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Requirement"}),
        "column_name": hx.Str(mode="output", async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Column Name"}),
        "cell_address": hx.Str(mode="output", async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Row"}),
        "value_found": hx.Str(mode="output", async_output=["steer_validate_raw_data_task","steer_format_raw_data_task"], view={"label": "Value Found"}),
    }


def _steer_processed_claims():
    """
    Create the children nodes of the list for processed claims
    """
    return {
        "processed_claims": hx.List(mode="output", async_input=["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task"], async_output=["steer_format_raw_data_task"], view={"label":"Processed Claims"}, children={
            **_steer_processed_claims_single_nodes(),
            **_steer_processed_claims_loop_year(experience_rating_max_years),
            **_steer_processed_claims_loop_layer(max_layers)
        })
    }

def _steer_processed_claims_single_nodes():
    node_info_list = [        
        ("Reference",hx.Str,"output",None,None,["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Claimant",hx.Str,"output",None,None,["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Insured",hx.Str,"output",None,None,["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Status",hx.Str,"output",None,None,["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Incident date",hx.Date,"output",None,None,["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Report date",hx.Date,"output",None,None,["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Closed date",hx.Date,"output",None,None,["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Incident year",hx.Int,"output",None,utils.integer_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Policy year",hx.Int,"output",None,utils.integer_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Closed year",hx.Int,"output",None,utils.integer_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Policy limit",hx.Str,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Policy excess",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),

        ("Incurred Claims",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Inflated Claims",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),

        ("Incurred Capped",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Trended Claim",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Trended Expenses",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),


        ("Claim Ranking",hx.Int,"output",None,utils.integer_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Row Number",hx.Int,"output",None,utils.integer_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),

    ]
    return create_node_from_list(node_info_list)

def _steer_processed_claims_loop_year(experience_rating_max_years):
    node_info_list=[
        ("Paid DY ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Incurred DY ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),


        ("Paid Expenses DY ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Incurred Expenses DY ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Paid Claim Indemnity DY ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Incurred Claim Indemnity DY ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Paid Claim Count DY ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("Incurred Claim Count DY ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),


    ]
    return create_node_from_list(add_year_suffix(node_info_list, experience_rating_max_years))
    
def _steer_processed_claims_loop_layer(max_layers):
    node_info_list=[

        ("RI Claim Layer ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("RI Claim On-Levelled Layer ",hx.Float,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("RI Claim Count Layer ",hx.Bool,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),
        ("RI Claim Count On-Levelled Layer ",hx.Bool,"output",None,utils.thousands_format(0),["steer_tri_exclusions_setup_task","steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"steer_format_raw_data_task"),

    ]
    return create_node_from_list(add_year_suffix(node_info_list, max_layers))

def _steer_claims_movements():
    """
    Create the claims movements table
    """
    return {
        "claim_movements": hx.List(mode="output", async_output=["steer_format_raw_data_task"],view={"label":"Claim Movements"}, children={
            **_steer_claims_movements_children()
            })
        }

def _steer_claims_movements_children():    
    node_info_list=[
        ("Claim Ranking",hx.Str,"output",None,None,None,"steer_format_raw_data_task"),
        ("Claim Reference",hx.Str,"output",None,None,None,"steer_format_raw_data_task"),
        ("YOA",hx.Int,"output",None,utils.integer_format(0),None,"steer_format_raw_data_task"),
        ("Status",hx.Str,"output",None,None,None,"steer_format_raw_data_task"),
        ("Last Year",hx.Float,"output",None,utils.thousands_format(0),None,"steer_format_raw_data_task"),
        ("This Year",hx.Float,"output",None,utils.thousands_format(0),None,"steer_format_raw_data_task"),
        ("Incurred Movement",hx.Float,"output",None,utils.thousands_format(0),None,"steer_format_raw_data_task"),
        ("Last Year On Levelled",hx.Float,"output",None,utils.thousands_format(0),None,"steer_format_raw_data_task"),
        ("This Year On Levelled",hx.Float,"output",None,utils.thousands_format(0),None,"steer_format_raw_data_task"),
        ("Incurred Movement On Levelled",hx.Float,"output",None,utils.thousands_format(0),None,"steer_format_raw_data_task"),

    ]
    return create_node_from_list(node_info_list)

def _steer_triangles_per_layer_children():
    return {
        "selected_average_option_input":    hx.Str(  mode="input",   default="all-year", optionality="required", options=["5-year", "7-year", "15-year", "all-year"], view={"label": "Selected Average Option Input"}),
        "override_triangle":                hx.Bool( mode="input",   view={"label": "Use Override Triangle?"},                   default=False, async_input=["steer_tri_exclusions_setup_task","steer_populate_bc_patterns_task"] ),
        "override_triangle_date":           hx.Date( mode="input",   view={"label": "Enter Date of Override Triangle:"},         default=None, optionality="optional", async_input=["steer_format_raw_data_task","steer_tri_override_setup_task"]),
        "override_triangle_date_used":      hx.Date( mode="input",  async_input=["steer_populate_bc_patterns_task"], async_output=["steer_tri_override_setup_task"], view={"label": "Date of Override Triangle used: "},         default=None, optionality="optional"),
        "override_triangle_years":          hx.Float(mode="input",   async_input=["steer_tri_override_setup_task","steer_populate_bc_patterns_task"], view={"label": "Enter Number of Years:"},                   default=5),
        "assign_override_triangle_status":  hx.Str(  mode="output",  view={"label": "Override Triangle Status"} ),
        "async_override_triangle_status":   hx.Str(  mode="output",  async_output=["steer_tri_override_setup_task"], view={"label": "Override Triangle Last Setup Status"} ),


        "tri_exclusions_setup_task_status": hx.Str(mode="output",   view={"label": "Exclusions Triangle Task Status"}, async_output=["steer_tri_exclusions_setup_task"] ),
        "tri_exclusions_dimensions_status": hx.Str(mode="output",   view={"label": "Exclusions Triangle Active?"} ),

        # TODO delete if not used in Steer
        "benchmark_name": hx.Structure(view={"label": "Benchmark Name"}, children={
        "default"           : hx.Str(mode="output",             view={"label": "Algorithmic"} ),
        "override"          : hx.Str(mode="input",              view={"label": "Override"},                                 default=None, optionality="optional",   options_table="lst_benchmarknames", options_column="Benchmark Class"),
        "selected"          : hx.Str(mode="output",             view={"label": "Selected"}),
        }),

        "experience_weight": hx.Structure(view={"label": "Experience Weight"}, children={
            "default"           : hx.Float(mode="output",           view={"label": "Algorithmic", "format":utils.percent_format(2)}),
            "override"          : hx.Float(mode="input",            view={"label": "Override",    "format":utils.percent_format(2)},  default=None, optionality="optional"),
            "selected"          : hx.Float(mode="output",           view={"label": "Selected",    "format":utils.percent_format(2)}),
        }),
        
        # TODO delete if not used in Steer
        "benchmark_use_occurrence": hx.Bool(mode="input",  default=False, view={"label": "Use Claims Occurrence pattern, not Claims Made "}),

        "tri_1_basis":    hx.Str(  mode="input",   default="Incurred", optionality="required", options=["Incurred", "Paid"],async_input=["steer_tri_exclusions_setup_task"], view={"label": "Selected Raw Data Triangle"}),
        # "has_populated_bc_patterns":    hx.Bool(  mode="output", async_input=["advanced_features_task"], async_output=["steer_populate_bc_patterns_task"]),
        "is_not_experience_selected_updated":    hx.Bool(  mode="output"),
        "update_pattern_message"     : hx.Str(  mode="output", view={"label": "Update Pattern Message"}),
        "tri_1_raw_data": hx.Triangle(mode="output", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}),
        "tri_1a_raw_data_incurred": hx.Triangle(mode="output", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}},async_input=["steer_tri_exclusions_setup_task"], async_output=[{"task":"steer_format_raw_data_task", "reset":False}]),
        "tri_1b_raw_data_paid": hx.Triangle(mode="output", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, async_input=["steer_tri_exclusions_setup_task"], async_output=[{"task":"steer_format_raw_data_task", "reset":False}]),
        "tri_2_manual_input": hx.Triangle(mode="input", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, async_input=["steer_tri_exclusions_setup_task"], async_output=["steer_tri_override_setup_task"]),
        "tri_3a_exclusions": hx.Triangle(mode="input", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, async_output=["steer_tri_exclusions_setup_task"]),
        "tri_3_selected": hx.Triangle(mode="output", averages={"vw_5": {"label": "5-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 5}, "vw_7": {"label": "7-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 7}, "vw_15": {"label": "15-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 15}, "vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, default_average="vw_all"),
        "tri_4_result": hx.Triangle(mode="output", averages={"vw_5": {"label": "5-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 5},"vw_7": {"label": "7-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 7}, "vw_15": {"label": "15-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 15}, "vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, default_average="vw_all"),
        

        "incremental_dev_factor": hx.List(mode="input", default_element_count=experience_rating_max_years, view={"label": "DF"}, children={
            "show_idf_row"          : hx.Bool( mode="output", view={"label": "Show Row"}),
            "development_qtr"       : hx.Float(mode="output", view={"label": "Development Qtr",             "format":utils.integer_format(0)}),
            "development_mth"       : hx.Float(mode="output", view={"label": "Development Mth",             "format":utils.integer_format(0)}),
            "development_label"     : hx.Str(  mode="output", view={"label": "Label"}),

            "experience_default"    : hx.Float(mode="output", view={"label": "Experience - Algorithmic",    "format":utils.thousands_format(3)}),
            "experience_override"   : hx.Float(mode="input",  view={"label": "Experience - Override",       "format":utils.thousands_format(3)}, default=None, optionality="optional" ),
            "experience_selected_set_in_task"   : hx.Float(mode="input", async_input=[rarc_task_name], async_output="steer_populate_bc_patterns_task",  view={"label": "Experience - Selected","format":utils.thousands_format(3)}, default=1, optionality="optional" ),
            
            "experience_selected"   : hx.Float(mode="output", view={"label": "Experience - Selected",       "format":utils.thousands_format(3)}),

            "benchmark_default"     : hx.Float(mode="output", view={"label": "Benchmark - Algorithmic",     "format":utils.thousands_format(3)}),
            "benchmark_override"    : hx.Float(mode="output", view={"label": "Benchmark - Override",        "format":utils.thousands_format(3)}),
            "benchmark_selected"    : hx.Float(mode="output", view={"label": "Benchmark - Selected",        "format":utils.thousands_format(3)}),

            "blended_default"       : hx.Float(mode="output", view={"label": "Blended - Algorithmic",       "format":utils.thousands_format(3)}),
            "blended_override"      : hx.Float(mode="output", view={"label": "Blended - Override",          "format":utils.thousands_format(3)}),
            "blended_selected"      : hx.Float(mode="output", view={"label": "Blended - Selected",          "format":utils.thousands_format(3)})
        }),


        "tail_factor": hx.Structure(view={"label": "Tail DF"}, children={
            "show_idf_row"          : hx.Bool( mode="output", view={"label": "Show Row"}),

            "experience_default"    : hx.Float(mode="output", view={"label": "Experience - Algorithmic",    "format":utils.thousands_format(3)}),
            "experience_override"   : hx.Float(mode="input",  view={"label": "Experience - Override",       "format":utils.thousands_format(3)}, default=None, optionality="optional" ),
            "experience_selected_set_in_task"   : hx.Float(mode="input", async_input=[rarc_task_name], async_output="steer_populate_bc_patterns_task",  view={"label": "Experience - Selected","format":utils.thousands_format(3)}, default=1, optionality="optional" ),
            
            "experience_selected"   : hx.Float(mode="output", view={"label": "Experience - Selected",       "format":utils.thousands_format(3)}),

            "benchmark_default"     : hx.Float(mode="output", view={"label": "Benchmark - Algorithmic",     "format":utils.thousands_format(3)}),
            "benchmark_override"    : hx.Float(mode="output", view={"label": "Benchmark - Override",        "format":utils.thousands_format(3)}),
            "benchmark_selected"    : hx.Float(mode="output", view={"label": "Benchmark - Selected",        "format":utils.thousands_format(3)}),

            "blended_default"       : hx.Float(mode="output", view={"label": "Blended - Algorithmic",       "format":utils.thousands_format(3)}),
            "blended_override"      : hx.Float(mode="output", view={"label": "Blended - Override",          "format":utils.thousands_format(3)}),
            "blended_selected"      : hx.Float(mode="output", view={"label": "Blended - Selected",          "format":utils.thousands_format(3)})

        }),


        "percents_ultimate": hx.List(mode="input", default_element_count=experience_rating_max_years, view={"label": "Incremental DF"}, children={
            "show_ult_row"          : hx.Bool( mode="output", view={"label": "Show Row"}),
            "development_qtr"       : hx.Float(mode="output", view={"label": "Development Qtr",                     "format":utils.integer_format(0)}),
            "development_mth"       : hx.Float(mode="output", view={"label": "Development Mth",                     "format":utils.integer_format(0)}),
            "percents_label"        : hx.Str(  mode="output", view={"label": "Label"}),

            "experience_default_perc_ult"    : hx.Float(mode="output", view={"label": "Experience - Algorithmic",   "format":utils.percent_format(2)}),
            "experience_override_perc_ult"   : hx.Float(mode="output", view={"label": "Experience - Override",      "format":utils.percent_format(2)}),
            "experience_selected_perc_ult"   : hx.Float(mode="output", view={"label": "Experience - Selected",      "format":utils.percent_format(2)}),

            "benchmark_default_perc_ult"     : hx.Float(mode="output", view={"label": "Benchmark - Algorithmic",    "format":utils.percent_format(2)}),
            "benchmark_override_perc_ult"    : hx.Float(mode="output", view={"label": "Benchmark - Override",       "format":utils.percent_format(2)}),
            "benchmark_selected_perc_ult"    : hx.Float(mode="output", view={"label": "Benchmark - Selected",       "format":utils.percent_format(2)}),

            "blended_default_perc_ult"       : hx.Float(mode="output", view={"label": "Blended - Algorithmic",      "format":utils.percent_format(2)}),
            "blended_override_perc_ult"      : hx.Float(mode="output", view={"label": "Blended - Override",         "format":utils.percent_format(2)}),
            "blended_selected_perc_ult"      : hx.Float(mode="output", view={"label": "Blended - Selected",         "format":utils.percent_format(2)})
        }),
    }


def _steer_claim_count_per_layer_children():
    return {
        "selected_average_option_input":    hx.Str(  mode="input",   default="all-year", optionality="required", options=["5-year", "7-year", "15-year", "all-year"], view={"label": "Selected Average Option Input"}),
        
        "override_triangle":                hx.Bool( mode="input",   view={"label": "Use Override Triangle?"},                   default=False, async_input=["steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"]),
        "override_triangle_date":           hx.Date( mode="input",   view={"label": "Enter Date of Override Triangle:"},         default=None, optionality="optional", async_input=["steer_format_raw_data_task","steer_tri_count_override_setup_task"],   async_output=["steer_tri_override_setup_task"]),
        "override_triangle_date_used":      hx.Date( mode="input",   async_output=["steer_tri_count_override_setup_task"], view={"label": "Date of Override Triangle used: "},         default=None, optionality="optional"),
        "override_triangle_years":          hx.Float(mode="input",   async_input=["steer_tri_count_override_setup_task","steer_populate_bc_patterns_task"],    async_output=["steer_tri_override_setup_task"],view={"label": "Enter Number of Years:"},                   default=5),
        "assign_override_triangle_status":  hx.Str(  mode="output",  view={"label": "Override Triangle Status"} ),
        "async_override_triangle_status":   hx.Str(  mode="output",  async_output=["steer_tri_count_override_setup_task"], view={"label": "Override Triangle Last Setup Status"} ),


        "tri_exclusions_setup_task_status": hx.Str(mode="output",   view={"label": "Exclusions Triangle Task Status"}, async_output=["steer_tri_count_exclusions_setup_task"] ),
        "tri_exclusions_dimensions_status": hx.Str(mode="output",   view={"label": "Exclusions Triangle Active?"} ),

        # TODO delete if not used in Steer
        "benchmark_name": hx.Structure(view={"label": "Benchmark Name"}, children={
        "default"           : hx.Str(mode="output",             view={"label": "Algorithmic"} ),
        "override"          : hx.Str(mode="input",              view={"label": "Override"},                                 default=None, optionality="optional",   options_table="lst_benchmarknames", options_column="Benchmark Class"),
        "selected"          : hx.Str(mode="output",             view={"label": "Selected"}),
        }),

        "experience_weight": hx.Structure(view={"label": "Experience Weight"}, children={
            "default"           : hx.Float(mode="output",           view={"label": "Algorithmic", "format":utils.percent_format(2)}),
            "override"          : hx.Float(mode="input",            view={"label": "Override",    "format":utils.percent_format(2)},  default=None, optionality="optional"),
            "selected"          : hx.Float(mode="output",           view={"label": "Selected",    "format":utils.percent_format(2)}),
        }),
        
        # TODO delete if not used in Steer
        "benchmark_use_occurrence": hx.Bool(mode="input",  default=False, view={"label": "Use Claims Occurrence pattern, not Claims Made "}),

        "tri_1_basis":    hx.Str(  mode="input",   default="Incurred", optionality="required", options=["Incurred", "Paid"], async_input=["steer_tri_count_exclusions_setup_task"], view={"label": "Selected Raw Data Triangle"}),
        # created here to allow display with selector 
        # "has_populated_bc_patterns":    hx.Bool(  mode="output", async_input=["advanced_features_task"],async_output=["steer_populate_bc_patterns_task"]),       
        "is_not_experience_selected_updated":    hx.Bool(  mode="output"),
        "update_pattern_message"     : hx.Str(  mode="output", view={"label": "Update Pattern Message"}),
        "tri_1_raw_data": hx.Triangle(mode="output", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}),
        "tri_1a_raw_data_incurred": hx.Triangle(mode="output", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, async_input=["steer_tri_count_exclusions_setup_task"], async_output=[{"task":"steer_format_raw_data_task", "reset":False}]),
        "tri_1b_raw_data_paid": hx.Triangle(mode="output", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, async_input=["steer_tri_count_exclusions_setup_task"], async_output=[{"task":"steer_format_raw_data_task", "reset":False}]),
        "tri_2_manual_input": hx.Triangle(mode="input", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, async_input=["steer_tri_count_exclusions_setup_task"], async_output=["steer_tri_count_override_setup_task"]),
        "tri_3_selected": hx.Triangle(mode="output", averages={"vw_5": {"label": "5-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 5}, "vw_7": {"label": "7-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 7}, "vw_15": {"label": "15-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 15}, "vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, default_average="vw_all"),
        "tri_4_result": hx.Triangle(mode="output", averages={"vw_5": {"label": "5-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 5},"vw_7": {"label": "7-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 7}, "vw_15": {"label": "15-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": 15}, "vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, default_average="vw_all"),
        "tri_3a_exclusions": hx.Triangle(mode="input", default_average="vw_all", averages={"vw_all": {"label": "all-year", "average_type": "column_sum", "latest_diagonal": "include", "last_n_origin_periods": None}}, async_output=["steer_tri_count_exclusions_setup_task"]),


        "incremental_dev_factor": hx.List(mode="input", default_element_count=experience_rating_max_years, view={"label": "DF"}, children={
            "show_idf_row"          : hx.Bool( mode="output", view={"label": "Show Row"}),
            "development_qtr"       : hx.Float(mode="output", view={"label": "Development Qtr",             "format":utils.integer_format(0)}),
            "development_mth"       : hx.Float(mode="output", view={"label": "Development Mth",             "format":utils.integer_format(0)}),
            "development_label"     : hx.Str(  mode="output", view={"label": "Label"}),

            "experience_default"    : hx.Float(mode="output", view={"label": "Experience - Algorithmic",    "format":utils.thousands_format(3)}),
            "experience_override"   : hx.Float(mode="input",  view={"label": "Experience - Override",       "format":utils.thousands_format(3)}, default=None, optionality="optional" ),
            "experience_selected_set_in_task"   : hx.Float(mode="input", async_input=[rarc_task_name], async_output="steer_populate_bc_patterns_task",  view={"label": "Experience - Selected","format":utils.thousands_format(3)}, default=1, optionality="optional" ),
            
            "experience_selected"   : hx.Float(mode="output", view={"label": "Experience - Selected",       "format":utils.thousands_format(3)}),

            "benchmark_default"     : hx.Float(mode="output", view={"label": "Benchmark - Algorithmic",     "format":utils.thousands_format(3)}),
            "benchmark_override"    : hx.Float(mode="output", view={"label": "Benchmark - Override",        "format":utils.thousands_format(3)}),
            "benchmark_selected"    : hx.Float(mode="output", view={"label": "Benchmark - Selected",        "format":utils.thousands_format(3)}),

            "blended_default"       : hx.Float(mode="output", view={"label": "Blended - Algorithmic",       "format":utils.thousands_format(3)}),
            "blended_override"      : hx.Float(mode="output", view={"label": "Blended - Override",          "format":utils.thousands_format(3)}),
            "blended_selected"      : hx.Float(mode="output", view={"label": "Blended - Selected",          "format":utils.thousands_format(3)})
        }),


        "tail_factor": hx.Structure(view={"label": "Tail DF"}, children={
            "show_idf_row"          : hx.Bool( mode="output", view={"label": "Show Row"}),

            "experience_default"    : hx.Float(mode="output", view={"label": "Experience - Algorithmic",    "format":utils.thousands_format(3)}),
            "experience_override"   : hx.Float(mode="input",  view={"label": "Experience - Override",       "format":utils.thousands_format(3)}, default=None, optionality="optional" ),
            "experience_selected_set_in_task"   : hx.Float(mode="input", async_input=[rarc_task_name], async_output="steer_populate_bc_patterns_task",  view={"label": "Experience - Selected","format":utils.thousands_format(3)}, default=1, optionality="optional" ),
            
            "experience_selected"   : hx.Float(mode="output", view={"label": "Experience - Selected",       "format":utils.thousands_format(3)}),

            "benchmark_default"     : hx.Float(mode="output", view={"label": "Benchmark - Algorithmic",     "format":utils.thousands_format(3)}),
            "benchmark_override"    : hx.Float(mode="output", view={"label": "Benchmark - Override",        "format":utils.thousands_format(3)}),
            "benchmark_selected"    : hx.Float(mode="output", view={"label": "Benchmark - Selected",        "format":utils.thousands_format(3)}),

            "blended_default"       : hx.Float(mode="output", view={"label": "Blended - Algorithmic",       "format":utils.thousands_format(3)}),
            "blended_override"      : hx.Float(mode="output", view={"label": "Blended - Override",          "format":utils.thousands_format(3)}),
            "blended_selected"      : hx.Float(mode="output", view={"label": "Blended - Selected",          "format":utils.thousands_format(3)})

        }),


        "percents_ultimate": hx.List(mode="input", default_element_count=experience_rating_max_years, view={"label": "Incremental DF"}, children={
            "show_ult_row"          : hx.Bool( mode="output", view={"label": "Show Row"}),
            "development_qtr"       : hx.Float(mode="output", view={"label": "Development Qtr",                     "format":utils.integer_format(0)}),
            "development_mth"       : hx.Float(mode="output", view={"label": "Development Mth",                     "format":utils.integer_format(0)}),
            "percents_label"        : hx.Str(  mode="output", view={"label": "Label"}),

            "experience_default_perc_ult"    : hx.Float(mode="output", view={"label": "Experience - Algorithmic",   "format":utils.percent_format(2)}),
            "experience_override_perc_ult"   : hx.Float(mode="output", view={"label": "Experience - Override",      "format":utils.percent_format(2)}),
            "experience_selected_perc_ult"   : hx.Float(mode="output", view={"label": "Experience - Selected",      "format":utils.percent_format(2)}),

            "benchmark_default_perc_ult"     : hx.Float(mode="output", view={"label": "Benchmark - Algorithmic",    "format":utils.percent_format(2)}),
            "benchmark_override_perc_ult"    : hx.Float(mode="output", view={"label": "Benchmark - Override",       "format":utils.percent_format(2)}),
            "benchmark_selected_perc_ult"    : hx.Float(mode="output", view={"label": "Benchmark - Selected",       "format":utils.percent_format(2)}),

            "blended_default_perc_ult"       : hx.Float(mode="output", view={"label": "Blended - Algorithmic",      "format":utils.percent_format(2)}),
            "blended_override_perc_ult"      : hx.Float(mode="output", view={"label": "Blended - Override",         "format":utils.percent_format(2)}),
            "blended_selected_perc_ult"      : hx.Float(mode="output", view={"label": "Blended - Selected",         "format":utils.percent_format(2)})
        }),

    # })
    }

def _steer_burning_cost_layer_summary_nodes():
    """
    Create Children nodes of selected_years_wa and all_years_wa. This will also be part of the burning_cost among other nodes.
    """

    node_info_list = [
        ("Frequency per m Exposure",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Average Cost Per Claim",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Loss Cost per m Exposure",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Rate Pct",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Expected Loss Cost",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("ULR",hx.Float,"output",None,utils.percent_format(2),None,None),
    ]
    return create_node_from_list(node_info_list)
    

def _steer_burning_cost_layer_year_nodes():
    """
    Create Children nodes of burning_cost 
    """

    node_info_list = [
        ("Policy Year Label",hx.Str,"output",None,None,[rarc_task_name,"start_renewal_task"],None),
        ("Policy Year",hx.Int,"output",None,utils.integer_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Weighting",hx.Float,"input",1,utils.thousands_format(2),[rarc_task_name,"start_renewal_task"],[rarc_task_name,{"task": "start_renewal_task", "reset": False}]),
        ("Onlevelled Exposure",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Incurred Claims",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Incurred No of Claims",hx.Int,"output",None,utils.integer_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Inflated Claims",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Inflated No of Claims",hx.Int,"output",None,utils.integer_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Ultimate Claims Developed",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Ultimate Claims Developed And Inflated",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("IBNR",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Ultimate No of Claims Developed",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Frequency per m Exposure",hx.Float,"output",None,utils.thousands_format(2),[rarc_task_name,"start_renewal_task"],None),
        ("Average Cost Per Claim",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Loss Cost per m Exposure",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Rate pct",hx.Float,"output",None,utils.percent_format(2),[rarc_task_name,"start_renewal_task"],None),
        ("Expected Loss Cost",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Premium",hx.Float,"input",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],[rarc_task_name,{"task": "start_renewal_task", "reset": False}],"optional"),
        ("ULR",hx.Float,"output",None,utils.percent_format(2),[rarc_task_name,"start_renewal_task"],None),
        ("Claim Dev pct",hx.Float,"output",None,utils.percent_format(2),[rarc_task_name,"start_renewal_task"],None),
        ("Claim Count Dev pct",hx.Float,"output",None,utils.percent_format(2),[rarc_task_name,"start_renewal_task"],None),
        ("Claim Dev Method",hx.Str,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Claim Count Dev Method",hx.Str,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("CL_Incurred Claims Developed",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("CL_Inflated Claims Developed",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("CL_Claim Count Developed",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("CL_Freq",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("CL_ACPC",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("CL_ACPC Inflated",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("BF_Claim Amount",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("BF_Claim Amount Inflated",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("BF_Claim Count",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),

        ("Average Expected Loss Cost",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),
        ("Average Freq per m Exposure",hx.Float,"output",None,utils.percent_format(2),[rarc_task_name,"start_renewal_task"],None),
        ("Average Loss Cost per m Exposure",hx.Float,"output",None,utils.thousands_format(0),[rarc_task_name,"start_renewal_task"],None),

    ]
    return create_node_from_list(node_info_list) 


def _steer_experience_rating_layers_children():
    """
    Create Children nodes of experience rating layers, including burning_cost, selected_years_wa, all_years_wa, triangle_projection and claim_count
    """
    return {
        # Burning Cost
        # **_steer_burning_cost_layer_nodes(),
        "burning_cost": hx.List(mode="input",async_input=[rarc_task_name,"start_renewal_task"],async_output=[{"task": "start_renewal_task", "reset": False}],view={"label":"`Burning Cost"},default_element_count=experience_rating_max_years, max_element_count=experience_rating_max_years, min_element_count=experience_rating_max_years, children={
            **_steer_burning_cost_layer_year_nodes(),}),
            "selected_years_wa": hx.Structure(view={"label": "Selected\nY\nWA"}, children={**_steer_burning_cost_layer_summary_nodes()}),
            "all_years_wa": hx.Structure(view={"label": "All Y\nWA"}, children={**_steer_burning_cost_layer_summary_nodes()}),
        # for burning cost summary
        "limit": hx.Float(mode="output", optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0)}),
        "excess": hx.Float(mode="output", optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0)}),
        "ulr": hx.Float(mode="output", optionality="optional", view={"label": "ULR", "format": utils.percent_format(2)}),
        "pure_rate": hx.Float(mode="output", optionality="optional", view={"label": "Pure Rate", "format": utils.percent_format(2)}),
        "pattern_type": hx.Str(mode="input", default = "FGU",async_input =["steer_populate_bc_patterns_task"],optionality="required", options=["FGU","Layer"],view={"label": "Selected\nClaim\nPattern"}),
        "bc_ulr_message": hx.Str(mode="output"),
        "bc_comment": hx.Str(mode="input",default=None, optionality="optional", view={"label": "Burning Cost Comment"}),
        
        # Triangles
        "triangle_projection": hx.Structure(children={**_steer_triangles_per_layer_children()}),
        # Claim count
        "claim_count": hx.Structure(children={**_steer_claim_count_per_layer_children()}),
        "bf_expected": hx.Structure(children={
            "incurred_claim":hx.Structure(view={"label": "Incurred\nClaim"},children={
                **_steer_experience_rating_layers_bf_children()
                }),
            "inflated_claim":hx.Structure(view={"label": "Inflated\nClaim"},children={
                **_steer_experience_rating_layers_bf_children()
                }),
            }),
    }

def _steer_experience_rating_layers_bf_children():
    node_info_list = [
    ("Frequency per m Exposure",hx.Float,"output",None,utils.percent_format(2),None,None),
    ("ACPC",hx.Float,"output",None,utils.thousands_format(0),None,None),
    ("Loss Cost per m Revenue",hx.Float,"output",None,utils.thousands_format(0),None,None),
    ("Offset rows",hx.Int,"output",None,utils.integer_format(0),None,None),

    ]
    return create_node_from_list(node_info_list)

def _steer_experience_rating_layers():
    """
    Create content for FGU and a fixed number of layers. 
    """
    layers = {}
    for layer_num in range(1, max_layers + 1):
        layer_key = f"layer_{layer_num:02d}"
        layers[layer_key] = hx.Structure(view={"label": f"Layer {layer_num}"}, children={
            **_steer_experience_rating_layers_children(),
            "layer_name": hx.Str(mode="input", default= f"Layer {layer_num}", view={"label": "Layer Name"}),
    
        })  

    # Add FGU layer
    layers["fgu"] = hx.Structure(view={"label": "FGU"}, children={
        **_steer_experience_rating_layers_children(),
        "layer_name": hx.Str(mode="input", default="FGU", view={"label": "Layer Name"}),
    })
    return {
        "layers": hx.Structure(children={**layers
        }),
        "is_not_experience_selected_updated": hx.Bool(mode="output",async_input=["advanced_features_task"]),
    }
