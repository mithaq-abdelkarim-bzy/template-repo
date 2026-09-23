import hx_data_schema as hx
import libraries.common_data_schema.data_schema.utilities as utils
import algorithms.utils_global_lists as lst
from algorithms.utils_functions import create_title

def sch_rate_change(cds):
    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
        "expiring_insured_name": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Insured Name"}),
        "expiring_premium": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Premium (Beazley's share)", "format": utils.thousands_format(0)}),
        "bound_final": hx.Float(mode="output", view={"label": "Rate Change", "format": utils.percent_format(1)}),
        "expiring_policy_term": hx.Float(mode="input", default=12, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Policy Term (months)"}),
        "expiring_beazley_share": hx.Float(mode="input", default=1, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Beazley Share", "format": utils.percent_format(0)}),
    })

    cds.extend_node_rater_defined("cds/layers", {
        "new_calculated_premium": hx.Float(mode="output", view={"label": "New Calculated Premium", "format": utils.thousands_format(0)}),
        "new_selected_premium": hx.Float(mode="output", view={"label": "New Selected Premium", "format": utils.thousands_format(0)}),
        "show_all_covers_for_rate_change": hx.Bool(mode="input", default=False, view={"label": "Show all coverages?"}),
        "pflr_pre_uw_adj": hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
        "quoted_premium_case_priced" : hx.Float(mode="input", optionality="optional", default=None, view={"label": "Gross Quoted Premium", "format":utils.thousands_format(0)}),
        "bpi_case_priced": hx.Float(mode="input", default=0, optionality="required", view={"label": "BPI (Case Priced)", "format": {"output": "percent", "mantissa": 1}}),
        "tpi_case_priced": hx.Float(mode="output", optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
        "technical_premium_case_priced":  hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "benchmark_premium_case_priced": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "written_line_view": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}}),
        })

    for item in lst.rate_change_list_static:
        cds.override_node_properties(f"cds/layers/rate_change/{item}/uw_selected", {
            "view": {"label": "UW Selected %", "format": utils.percent_format(1)}
        })

def sch_rate_change_non_cds():
    return {
        "show_rate_change": hx.Bool(mode="output"),
        "expiring_policy_option_id": hx.Int(mode="output", async_input=["expiring_policy_fetch_task", "start_renewal_task"]),
        "rate_change": hx.Structure(children={
            # Section Rate Change
            "expiring_brokerage": hx.Float(mode="input", default=0.15, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Brokerage", "format": utils.percent_format(1)}),
            "expiring_premium_comment": hx.Str(mode="input", default="", view={"label": "Comment"}),
            "show_safe_deposit_policy_table": hx.Bool(mode="output"),
            "show_computer_crime_policy_table": hx.Bool(mode="output"),
            # Exposure table (JUST BASIC BOND). Need to split this out as it's an async input. 
             **{
                loop_cover_vbl: hx.Structure(view={"label": loop_cover_str}, children={
                    "available": hx.Bool(mode="output", view={"label": "Available?"}),
                    "include": hx.Bool(mode="input", default=False, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Include?"}),
                    "final_include": hx.Bool(mode="output", async_input=["copy_expiring_basic_bond_terms"]),

                    "coverage": hx.Float(mode="input", default=0, async_input=["copy_expiring_basic_bond_terms"], async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Coverage", "format":utils.thousands_format(0)}),
                    "deductible": hx.Float(mode="input", default=0, async_input=["copy_expiring_basic_bond_terms"], async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Deductible", "format":utils.thousands_format(0)}),
                    
                    "coverage_premium_current": hx.Float(mode="output", view={"label": "Update Exposure", "format":utils.thousands_format(0)}),
                    "expiring_premium_update_deductible_limit": hx.Float(mode="output", view={"label": "Update Limit", "format":utils.thousands_format(0)}),
                    "expiring_premium_update_deductible": hx.Float(mode="output", view={"label": "Update Deductible", "format":utils.thousands_format(0)}),
                    "expiring_premium": hx.Float(mode="output", view={"label": "Expiring Premium", "format":utils.thousands_format(0)}),
                })
                for loop_cover_vbl, loop_cover_str in zip(lst.cover_str_static[:1], lst.cover_names[:1])
            },
            # Exposure table - Rate change
            **{
                loop_cover_vbl: hx.Structure(view={"label": loop_cover_str}, children={
                    "available": hx.Bool(mode="output", view={"label": "Available?"}),
                    "include": hx.Bool(mode="input", default=False, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Include?"}),
                    "final_include": hx.Bool(mode="output", async_input=["copy_expiring_basic_bond_terms"]),

                    "coverage": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task","copy_expiring_basic_bond_terms"], view={"label": "Coverage", "format":utils.thousands_format(0)}),
                    "deductible": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task","copy_expiring_basic_bond_terms"], view={"label": "Deductible", "format":utils.thousands_format(0)}),
                    
                    "coverage_premium_current": hx.Float(mode="output", view={"label": "Update Exposure", "format":utils.thousands_format(0)}),
                    "expiring_premium_update_deductible_limit": hx.Float(mode="output", view={"label": "Update Limit", "format":utils.thousands_format(0)}),
                    "expiring_premium_update_deductible": hx.Float(mode="output", view={"label": "Update Deductible", "format":utils.thousands_format(0)}),
                    "expiring_premium": hx.Float(mode="output", view={"label": "Expiring Premium", "format":utils.thousands_format(0)}),
                })
                for loop_cover_vbl, loop_cover_str in zip(lst.cover_str_static[1:], lst.cover_names[1:])
            },

            # Additional Coverage
            "include_checking_accounts_coverage": hx.Bool(mode="input", default=False, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Include Checking Accounts Coverage?"}),
            "number_of_agents": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Agents"}),
            "loan_to_deposit_ratio": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Loan to Deposit Ratio", "format": utils.percent_format(0)}),
            "include_loan_participation_coverage": hx.Bool(mode="input", default=True, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Include Loan Participation Coverage"}),
            "num_data_processing_orgs": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Data Processing Organisations Covered"}),
            
            **{
                item: hx.Structure(view={"label": create_title(item)}, children={
                    "us": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "US"}),
                    "other": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Other"}),
                })
                for item in ["branch_offices_ex_per", "facilities_ex_per", "mobile_branch_units_ex_per","branch_offices_ex_prop", "facilities_ex_prop", "mobile_branch_units_ex_prop"]
            },
            
            "excluded_employees_persons": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Excluded Number of Officers and Employees"}),
            "excluded_employees_property": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Excluded Number of Officers and Employees"}),
            "number_of_issuers_of_register_checks": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Issuers of Register Checks or Personal Money Orders"}),
            "number_of_partners_or_members": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Partners or Members"}),
            "number_of_registered_reps": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Registered Reps"}),
            "number_of_servicing_contractors": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Servicing Contractors"}),
            "number_of_atms": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Covered Teller Machine Locations"}),

            "safe_deposit_box_coverage": hx.Structure(view={"label": "Inputs"}, children={
                "num_of_rented_boxes": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Rented Boxes, all locations", "format": utils.integer_format(0)}),
                "num_of_locations": hx.Int(mode="input", default=1, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Locations (including main location)", "format": utils.integer_format(0)}),
                "combined_limit": hx.Bool(mode="input", default=False, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Combined Single Limit?"}),
                "include_money_coverage": hx.Bool(mode="input", default=False, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Loss of Property and Damage: Include Money Coverage?"}),
            }),

            # Computer crime additional coverage
            **{
                f"{item}": hx.Structure(view={"label": lst.computer_crime_labels[item]}, children={
                    "include": hx.Bool(mode="input", default=False, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Y/N?"}),
                    "loss_cost": hx.Float(mode="output", view={"label": "Loss Cost"}),
                    "info": hx.Str(mode="output"),
                })
                for item in ['access_to_computer', 'does_include_clearing_houses', 'does_use_fed_wire', 'use_telex']
            },

            **{
                f"{item}": hx.Structure(view={"label": lst.computer_crime_labels[item]}, children={
                    "include": hx.Bool(mode="input", default=False, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Y/N?"}),
                    "how_many": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "How Many?"}),
                    "loss_cost": hx.Float(mode="output", view={"label": "Loss Cost"}),
                    "info": hx.Str(mode="output"),
                })
                for item in ['independent_software_contractors', 'atms_accessed_to_system', 'additional_computer_system', 'other_atm_systems']
            },

            "computer_crime_total": hx.Structure(view={"label": "Total"}, children={
                "loss_cost": hx.Float(mode="output", view={"label": "Loss Cost"}),
            }),

            **{
                item: hx.Structure(view={"label": create_title(item)}, children={
                    "us": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "US"}),
                    "other": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Other"}),
                })
                for item in ["facilities", "mobile_branch_units"]
            },

            # Exposure general details
            "financial_assets_june_rc": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Last June 30 Financial Statement Assets", "format":utils.thousands_format(0)}),
            "financial_assets_dec_rc": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Last December 31 Financial Statement Assets", "format":utils.thousands_format(0)}),
            "average_assets_rc": hx.Float(mode="output", view={"label": "Average Financial Assets", "format":utils.thousands_format(0)}),
            "number_of_employees_rc": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Number of Officers and Employees"}),
            **{
                item: hx.Structure(view={"label": create_title(item)}, children={
                    "us": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "US"}),
                    "other": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Other"}),
                })
                for item in ["branch_offices_rc"]
            },

            # YoY Exposure Changes
            "financial_assets_june_yoy": hx.Float(mode="output", view={"label": "YoY Change in June 30 Assets", "format":utils.percent_format(0)}),
            "financial_assets_dec_yoy": hx.Float(mode="output", view={"label": "YoY Change in December 31 Assets", "format":utils.percent_format(0)}),
            "average_assets_yoy": hx.Float(mode="output", view={"label": "YoY Change in Average Financial Assets", "format":utils.percent_format(0)}),
            "number_of_employees_yoy": hx.Float(mode="output", view={"label": "YoY Change in Number of Employees", "format":utils.percent_format(0)}),
            **{
            item: hx.Structure(view={"label": create_title(item)}, children={
                "us": hx.Float(mode="output", view={"label": "US", "format":utils.percent_format(0)}),
                "other": hx.Float(mode="output", view={"label": "Other", "format":utils.percent_format(0)}),
            })
            for item in ["branch_offices_yoy", "facilities_yoy", "mobile_branch_units_yoy"]
            },
        })
    }

    # hxd.override_node_properties(f"rate_change/{lst.cover_str_static[:1][0]}/coverage", {"async_input": ["copy_expiring_basic_bond_terms"], async_output: ["expiring_policy_fetch_task", "start_renewal_task"]})
    # hxd.override_node_properties(f"rate_change/{lst.cover_str_static[:1][0]}/deductible", {"async_input": ["copy_expiring_basic_bond_terms"], async_output: ["expiring_policy_fetch_task", "start_renewal_task"]})