import hx_data_schema as hx
import libraries.common_data_schema.data_schema.utilities as utils
import algorithms.utils_global_lists as lst
from algorithms.utils_functions import create_title

def sch_exposure_details(cds):
    cds.extend_node_rater_defined("cds", {
        # Exposure general details
        "type_of_insured": hx.Str(mode="input", default_index=0, options_table="InstitutionTypes", options_column="institution_type", view={"label": "Type Of Insured"}),
        "policy_form_used": hx.Str(mode="output", view={"label": "Form Used"}),
    })

    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        # Exposure general details
        "assets_june": hx.Float(mode="input", default=0, view={"label": "Last June 30 Financial Statement Assets", "format": utils.thousands_format(0)}),
        "assets_december": hx.Float(mode="input", default=0, view={"label": "Last December 31 Financial Statement Assets", "format": utils.thousands_format(0)}),
        "number_of_employees": hx.Int(mode="input", default=0, view={"label": "Number of Officers and Employees"}),
        "basic_unit_of_coverage": hx.Float(mode="output", view={"label": "Basic Unit of Coverage", "format": utils.thousands_format(0)}),
        "average_assets": hx.Float(mode="output", view={"label": "Average Financial Assets", "format": utils.thousands_format(0)}),

        **{
            item: hx.Structure(view={"label": create_title(item)}, children={
                "us": hx.Int(mode="input", default=0, view={"label": "US"}),
                "other": hx.Int(mode="input", default=0, view={"label": "Other"}),
            })
            for item in ["branch_offices", "facilities", "mobile_branch_units"]
        },

        # Additional Coverage
        "number_of_agents": hx.Int(mode="input", default=0, view={"label": "Number of Agents"}),
        "loan_to_deposit_ratio": hx.Float(mode="input", default=0, view={"label": "Loan to Deposit Ratio", "format": utils.percent_format(0)}),
        **{
            item: hx.Structure(view={"label": create_title(item)}, children={
                "us": hx.Int(mode="input", default=0, view={"label": "US"}),
                "other": hx.Int(mode="input", default=0, view={"label": "Other"}),
            })
            for item in ["branch_offices_ex_per", "facilities_ex_per", "mobile_branch_units_ex_per","branch_offices_ex_prop", "facilities_ex_prop", "mobile_branch_units_ex_prop"]
        },
        "excluded_employees_persons": hx.Int(mode="input", default=0, view={"label": "Excluded Number of Officers and Employees"}),
        "excluded_employees_property": hx.Int(mode="input", default=0, view={"label": "Excluded Number of Officers and Employees"}),
        "number_of_issuers_of_register_checks": hx.Int(mode="input", default=0, view={"label": "Number of Issuers of Register Checks or Personal Money Orders"}),
        "number_of_partners_or_members": hx.Int(mode="input", default=0, view={"label": "Number of Partners or Members"}),
        "number_of_registered_reps": hx.Int(mode="input", default=0, view={"label": "Number of Registered Reps"}),
        "number_of_servicing_contractors": hx.Int(mode="input", default=0, view={"label": "Number of Servicing Contractors"}),
        "number_of_atms": hx.Int(mode="input", default=0, view={"label": "Number of Covered Teller Machine Locations"}),

        "safe_deposit_box_coverage": hx.Structure(view={"label": "Inputs"}, children={
            "num_of_rented_boxes": hx.Int(mode="input", default=0, view={"label": "Number of Rented Boxes, all locations", "format": utils.integer_format(0)}),
            "num_of_locations": hx.Int(mode="input", default=1, view={"label": "Number of Locations (including main location)", "format": utils.integer_format(0)}),
            "combined_limit": hx.Bool(mode="input", default=False, view={"label": "Combined Single Limit?"}),
            "include_money_coverage": hx.Bool(mode="input", default=False, view={"label": "Loss of Property and Damage: Include Money Coverage?"}),
        }),
        **{
            item: hx.Structure(view={"label": lst.computer_crime_labels[item]}, children={
                "include": hx.Bool(mode="input", default=False, view={"label": "Y/N?"}),
                "how_many": hx.Int(mode="input", default=0, view={"label": "How Many?"}),
                "loss_cost": hx.Float(mode="output", view={"label": "Loss Cost"}),
                "info": hx.Str(mode="output"),
            })
            for item in ['independent_software_contractors', 'atms_accessed_to_system', 'additional_computer_system', 'other_atm_systems']
        },
        **{
            item: hx.Structure(view={"label": lst.computer_crime_labels[item]}, children={
                "include": hx.Bool(mode="input", default=False, view={"label": "Y/N?"}),
                "loss_cost": hx.Float(mode="output", view={"label": "Loss Cost"}),
                "info": hx.Str(mode="output"),
            })
            for item in ['access_to_computer', 'does_include_clearing_houses', 'does_use_fed_wire', 'use_telex']
        },
    })

    cds.extend_node_rater_defined("cds/layers", {
        # Exposure general details
        "rating_note": hx.Str(mode="output", view={"label": "Rating Note"}),
        
        # Additional Coverage
        "include_loan_participation_coverage": hx.Bool(mode="input", default=True, view={"label": "Include Loan Participation Coverage"}),
        "num_data_processing_orgs": hx.Int(mode="input", default=0, view={"label": "Number of Data Processing Organisations Covered"}),
        "include_checking_accounts_coverage": hx.Bool(mode="input", default=False, view={"label": "Include Checking Accounts Coverage?"}),
        
        "include_safe_deposit_box": hx.Bool(mode="output"),  
        "include_computer_crime": hx.Bool(mode="output"), 

        "computer_crime_total": hx.Structure(view={"label": "Total"}, children={
            "loss_cost": hx.Float(mode="output", view={"label": "Loss Cost"}),
        }),
    })

    cds.extend_node_items("cds/layers/coverages", {
        "cover_1_basic_bond": {"label": "Basic Bond"},
        **{
            loop_cover_vbl: {"label": loop_cover_str}
            for loop_cover_vbl, loop_cover_str in zip(lst.cover_str_static, lst.cover_names)
        }
    })

    cds.extend_node_rater_defined("cds/layers/coverages", {
        "available": hx.Bool(mode="output", view={"label": "Available?"}),
        "include": hx.Bool(mode="input", default=False, view={"label": "Include?"}),
        "final_include": hx.Bool(mode="output", async_input=["copy_basic_bond_terms"]),
        "min_coverage": hx.Float(mode="output", view={"label": "Minimum Coverage", "format":utils.thousands_format(0)}),
        "max_coverage": hx.Float(mode="output", view={"label": "Maximum Coverage", "format":utils.thousands_format(0)}),
        "min_deductible": hx.Float(mode="output", view={"label": "Minimum Deductible", "format":utils.thousands_format(0)}),
        "max_deductible": hx.Float(mode="output", view={"label": "Maximum Deductible", "format":utils.thousands_format(0)}),
        "coverage": hx.Float(mode="input", async_output="copy_basic_bond_terms", default=0, view={"label": "Coverage", "format":utils.thousands_format(0)}),
        "coverage_manual": hx.Float(mode="output"),
        "deductible_manual": hx.Float(mode="output"),
        "coverage_premium": hx.Float(mode="output", view={"label": "Unity Premium (excl. experience)", "format":utils.thousands_format(0)}),
        "coverage_premium_post_experience": hx.Float(mode="output", view={"label": "Unity Premium", "format":utils.thousands_format(0)}),
        "coverage_premium_post_schedule": hx.Float(mode="output", view={"label": "Premium Post Schedule Rating", "format":utils.thousands_format(0)}),
        "coverage_premium_post_a_rating": hx.Float(mode="output", view={"label": "Final Premium", "format":utils.thousands_format(0)}),
        "coverage_premium_post_a_rating_annual": hx.Float(mode="output", view={"label": "Annualized Premium", "format":utils.thousands_format(0)}),
        "manual_premium": hx.Float(mode="output", view={"label": "Manual Premium", "format":utils.thousands_format(0)}),
        "info": hx.Str(mode="output", view={"label": "Info"}),
    })

    for cover_str in lst.cover_str_static[1:]:
        cds.override_node_properties(f"cds/layers/coverages/{cover_str}/deductible", {
            "async_output": ["copy_basic_bond_terms"],
            "default": 0,
            "optionality": "required"
            })

    # Exposure table (JUST BASIC BOND). Need to adjust some properties as it's an async input. 
    cds.override_node_properties(f"cds/layers/coverages/{lst.cover_str_static[:1][0]}/include", {"default": True})
    cds.override_node_properties(f"cds/layers/coverages/{lst.cover_str_static[:1][0]}/final_include", {"async_input": []})
    cds.override_node_properties(f"cds/layers/coverages/{lst.cover_str_static[:1][0]}/coverage", {"async_input": ["copy_basic_bond_terms"], "async_output": []})
    cds.override_node_properties(f"cds/layers/coverages/{lst.cover_str_static[:1][0]}/deductible", {"async_input": ["copy_basic_bond_terms"], "async_output": [], "default": 0, "optionality": "required"})

    cds.override_node_properties("cds/standard_fields/insured_state_or_province", {
        "default": None, 
        "options_table": "StateLookup", 
        "options_column": "State", 
        "view": {"label": "State"},
    })


def sch_exposure_details_non_cds():
    return {
        "checking_accounts_info": hx.Str(mode="output"),
        "loan_to_deposit_ratio_info": hx.Str(mode="output"),
    }
        