# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_rate_change import rarc_task_name
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
from algorithms.rate_constants import get_territory_groups_2, get_individual_countries, get_individual_countries_count, get_states_count
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST


def sch_territory(cds):
    cds.extend_node_rater_defined("cds/exposure/granular", {        
        # "exposure_details": hx.Structure(children={
        #     **{f"year_{key}": hx.Structure(children={"policy_year": hx.Int(mode="output", view={"label": "Policy Year"}),
        #     "professional_services_fee": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Professional Services Fee"}),
        #     "epc_design_construct_values": hx.Float(mode="input", default=0, optionality="optional", view={"label": "EPC Design & Construct Values"}),
        #     "hard_fm_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Hard FM Revenues"}),
        #     "construct_pass_soft_fm_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Construct Only/ Pass Through Costs/ Soft FM Revenues"}),
        #     "revenue_100_pcnt": hx.Float(mode="output", view={"label": "100% Revenues"}),
        #     "notional_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Notional Revenues"}),
        #     "revalued_notional_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Revalued Notional Revenues"}),
        #     "weighting": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Weighting"})})
        #     for key in range(19, -1, -1)}
        # }),
        "territory": hx.Structure(children={
            "instructions": hx.Str(mode="output", view={"label": "How to use:"}),
            "bool_individual_country_level": hx.Bool(mode="input", async_input=["run_simulation_task", "rarc_task"], default=False, optionality="required", view={"label":"Enter at Individual Country Level?"}),
            "bool_individual_state_level": hx.Bool(mode="input", async_input=["run_simulation_task","rarc_task"], default=False, optionality="required", view={"label":"Enter at Individual State Level?"}),
            "bool_table_1": hx.Bool(mode="output"),
            "bool_table_2": hx.Bool(mode="output"),
            "bool_table_3": hx.Bool(mode="output"),
            "bool_table_4": hx.Bool(mode="output"),
            "split_option": hx.Str(mode="input", optionality="required", default_index=0,options=["Percentage", "Actual"], view={"label":"Enter split as:"}),
            "is_percentage_bool": hx.Bool(mode="input", optionality="required", default=True, view={"label": "Enter as Percentage?"}),
            "is_percentage_bool_not": hx.Bool(mode="output"),
            "bool_incept_year_pcnt": hx.Bool(mode="output"),
            "bool_incept_year_value": hx.Bool(mode="output"),
            "summary_label": hx.Str(mode="output"),
            "summary": hx.Structure(children={
                 **{f"{key}_reporting": hx.Structure(children={
                    "year_0_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0", "format": utils.percent_format(1)}),
                    "year_1_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_1", "format": utils.percent_format(1)}),
                    "year_2_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_2", "format": utils.percent_format(1)}),
                    "year_3_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_3", "format": utils.percent_format(1)}),
                    "year_4_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_4", "format": utils.percent_format(1)}),
                    "year_5_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_5", "format": utils.percent_format(1)}),
                    "year_0_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_1_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_1", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_2_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_2", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_3_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_3", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_4_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_4", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_5_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_5", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "weighted": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "Weighted % Split", "format": utils.percent_format(1)}),
                    "frequency": hx.Float(mode="output",view={"label": "Frequency", "format":utils.percent_format(1), "group": "Loading"}),
                    "severity": hx.Float(mode="output", view={"label": "Severity", "format": utils.percent_format(1), "group": "Loading"}),
                    "expected_loss_cost": hx.Float(mode="output", view={"label": "Expected Loss (FGU)", "format": {"thousandSeparated": True, "mantissa": 0}})
                    },
                )
                for key in get_territory_groups_2()},               
                **{f"{key}": hx.Structure(children={
                    "year_0_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_0", "format": utils.percent_format(1)}),
                    "year_1_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_1", "format": utils.percent_format(1)}),
                    "year_2_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_2", "format": utils.percent_format(1)}),
                    "year_3_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_3", "format": utils.percent_format(1)}),
                    "year_4_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_4", "format": utils.percent_format(1)}),
                    "year_5_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_5", "format": utils.percent_format(1)}),
                    "year_0_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_0", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_1_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_1", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_2_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_2", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_3_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_3", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_4_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_4", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_5_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_5", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "weighted": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "Weighted % Split", "format": utils.percent_format(1)}),
                    "frequency": hx.Float(mode="output",view={"label": "Frequency", "format":utils.percent_format(1), "group": "Loading"}),
                    "severity": hx.Float(mode="output", view={"label": "Severity", "format": utils.percent_format(1), "group": "Loading"}),
                    "expected_loss_cost": hx.Float(mode="output", view={"label": "Expected Loss (FGU)", "format": {"thousandSeparated": True, "mantissa": 0}})
                    },
                )
                for key in get_territory_groups_2()},
                **{f"{key}_country_sum": hx.Structure(children={
                    "year_0_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0", "format": utils.percent_format(1)}),
                    "year_1_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_1", "format": utils.percent_format(1)}),
                    "year_2_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_2", "format": utils.percent_format(1)}),
                    "year_3_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_3", "format": utils.percent_format(1)}),
                    "year_4_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_4", "format": utils.percent_format(1)}),
                    "year_5_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_5", "format": utils.percent_format(1)}),
                    "year_0_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_1_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_1", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_2_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_2", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_3_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_3", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_4_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_4", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_5_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_5", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "weighted": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "Weighted % Split", "format": utils.percent_format(1)}),
                    "frequency": hx.Float(mode="output",view={"label": "Frequency", "format":utils.percent_format(1), "group": "Adjusted"}),
                    "severity": hx.Float(mode="output", view={"label": "Severity", "format": utils.percent_format(1), "group": "Adjusted"})
                    },
                )
                for key in get_territory_groups_2()},
                **{f"{key}_state_sum": hx.Structure(children={
                    "year_0_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0", "format": utils.percent_format(1)}),
                    "year_1_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_1", "format": utils.percent_format(1)}),
                    "year_2_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_2", "format": utils.percent_format(1)}),
                    "year_3_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_3", "format": utils.percent_format(1)}),
                    "year_4_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_4", "format": utils.percent_format(1)}),
                    "year_5_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_5", "format": utils.percent_format(1)}),
                    "year_0_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_1_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_1", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_2_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_2", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_3_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_3", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_4_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_4", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_5_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_5", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "weighted": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "Weighted % Split", "format": utils.percent_format(1)}),
                    "frequency": hx.Float(mode="output",view={"label": "Frequency", "format":utils.percent_format(1), "group": "Loading"}),
                    "severity": hx.Float(mode="output", view={"label": "Severity", "format": utils.percent_format(1), "group": "Loading"})
                    },
                )
                for key in get_territory_groups_2()},
                "total": hx.Structure(children={
                    "year_0_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0", "format": utils.percent_format(1)}),
                    "year_1_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_1", "format": utils.percent_format(1)}),
                    "year_2_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_2", "format": utils.percent_format(1)}),
                    "year_3_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_3", "format": utils.percent_format(1)}),
                    "year_4_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_4", "format": utils.percent_format(1)}),
                    "year_5_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_5", "format": utils.percent_format(1)}),
                    "year_0_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0", "format": utils.percent_format(1)}),
                    "year_1_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_1", "format": utils.percent_format(1)}),
                    "year_2_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_2", "format": utils.percent_format(1)}),
                    "year_3_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_3", "format": utils.percent_format(1)}),
                    "year_4_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_4", "format": utils.percent_format(1)}),
                    "year_5_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_5", "format": utils.percent_format(1)}),
                    "weighted": hx.Float(mode="output", async_input=["run_simulation_task", "rarc_task"], view={"label": "Weighted % Split", "format": utils.percent_format(1)}),
                    "elc": hx.Float(mode="output",view={"label": "Expected Loss (FGU)", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "Total"}),   
                    "frequency": hx.Float(mode="output",view={"label": "Lambda\n(Mean Freq)", "format": {"thousandSeparated": True, "mantissa": 3}, "group": "Adjusted"}),
                    "severity": hx.Float(mode="output", view={"label": "Mu\n(Severity Parameter)", "format": {"thousandSeparated": True, "mantissa": 3}, "group": "Adjusted"})                      
                    }, 
                    view={"label": "Total"}),                
            }),
            "summary_modifier_labels": hx.Structure(children={
                **{f"{key}": hx.Str(mode="output")
                for key in get_territory_groups_2()},
                "not_specified": hx.Str(mode="output")        
            }),
            "summary_year_labels": hx.Structure(children={
                "year_0": hx.Str(mode="output"),
                "year_1": hx.Str(mode="output"),
                "year_2": hx.Str(mode="output"),
                "year_3": hx.Str(mode="output"),
                "year_4": hx.Str(mode="output"),
                "year_5": hx.Str(mode="output")
            }),
            "summary_year_total_labels": hx.Structure(children={
                "year_0": hx.Str(mode="output"),
                "year_1": hx.Str(mode="output"),
                "year_2": hx.Str(mode="output"),
                "year_3": hx.Str(mode="output"),
                "year_4": hx.Str(mode="output"),
                "year_5": hx.Str(mode="output"),
            }),
            "individual_countries": hx.List(
                mode="input", 
                async_input=["run_simulation_task", "rarc_task"],
                default_element_count=get_individual_countries_count(), 
                fixed_element_count=get_individual_countries_count(), 
                children={
                    "region": hx.Str(mode="input",
                                    async_input=["run_simulation_task", "rarc_task"],
                                    view={"label": "Region"}, 
                                    options_table="ref_region_country",
                                    options_column="region",
                                    default_index = 0,
                                    fixed_values_column = "region",
                                    fixed_values_table = "ref_region_country",
                                    ),
                    "country": hx.Str(mode="input",
                                    async_input=["run_simulation_task", "rarc_task"],
                                    view={"label": "Country"}, 
                                    options_table="ref_region_country",
                                    options_column="country",
                                    default_index=0,
                                    fixed_values_column = "country",       
                                    fixed_values_table = "ref_region_country",                       
                                    ),
                    "year_0_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_0", "format": utils.percent_format(1)}),
                    "year_1_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_1", "format": utils.percent_format(1)}),
                    "year_2_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_2", "format": utils.percent_format(1)}),
                    "year_3_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_3", "format": utils.percent_format(1)}),
                    "year_4_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_4", "format": utils.percent_format(1)}),
                    "year_5_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_5", "format": utils.percent_format(1)}),
                    "year_0_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_0", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_1_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_1", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_2_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_2", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_3_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_3", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_4_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_4", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_5_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_5", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    
                }),
            "state": hx.List(mode="input", 
                async_input=["run_simulation_task", "rarc_task"],
                default_element_count=get_states_count(), 
                fixed_element_count=get_states_count(), 
                children={
                    "state": hx.Str(mode="input", 
                                    async_input=["run_simulation_task", "rarc_task"],
                                    view={"label": "Region"}, 
                                    options_table="ref_states",
                                    options_column="state",
                                    default_index = 0,
                                    fixed_values_column = "state",
                                    fixed_values_table = "ref_states",
                                    ),
                    "year_0_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_0", "format": utils.percent_format(1)}),
                    "year_1_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_1", "format": utils.percent_format(1)}),
                    "year_2_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_2", "format": utils.percent_format(1)}),
                    "year_3_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_3", "format": utils.percent_format(1)}),
                    "year_4_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_4", "format": utils.percent_format(1)}),
                    "year_5_pcnt": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_5", "format": utils.percent_format(1)}),
                    "year_0_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_0", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_1_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_1", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_2_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_2", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_3_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_3", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_4_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_4", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_5_value": hx.Float(mode="input", async_input=["run_simulation_task", "rarc_task"], default=0, optionality="optional", view={"label": "year_5", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }
            )
        })
    }
    ),