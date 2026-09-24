# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers 
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict , max_coverages, COVERAGES_LIST

from data_schema.rate_change.sch_rate_change_generic_structure import rarc_tasks_names, rarc_task_name, rc_quoted_premium , rc_expiring_info, rc_temp_storage, rc_show_coverages, rc_insured_asset_list, rc_expiring_and_renewal

### --- BUILD RATE CHANGE DATA SCHEMA FOR LAYERS --- ###
def sch_rate_change(cds):
    """
    BUILD RATE CHANGE DATA SCHEMA FOR LAYERS
    """
    rarc_changes = {
        "exposure_change": {"label": "Exposure Change"},
        "risk_characteristics_change": {"label": "Risk Characteristics Change"},
        "limit_change": {"label": "Limit Change"},
        "deductible_change": {"label": "Deductible Change"},
        "terms_conditions_change": {"label": "Terms & Conditions Change"},
        "other_change": {"label": "Other Change", "info": "Includes Brokerage Change"},
        "brokerage_change": {"label": "Brokerage Change"},
        "rate_change": {"label": "Risk Adjusted Rate Change"}
    }

    for change in rarc_changes.keys():
        # EDIT v0.3.0
        cds.override_node_properties(f"cds/layers/rate_change/{change}/model_calculated",{"view": {"label": "Model", "format": percent_format(1)},"async_output": [] if change == "rate_change" else [rarc_task_name]} )
        cds.override_node_properties(f"cds/layers/rate_change/{change}/uw_selected",{"view": {"label": "UW Selected", "format": percent_format(1)},"async_output": [] if change == "rate_change" else [{"task": rarc_task_name, "reset": False},"start_renewal_task"]} )  # added this to clear out the override on start of renewal but keep the selected value when Calculating Rate change again.
        cds.override_node_properties(f"cds/layers/rate_change/{change}/uw_override",{"view": {"label": "UW Override", "format": percent_format(1),"read_only": True} if change == "rate_change" else {"label": "UW Override", "format": percent_format(1)}})
        cds.override_node_properties(f"cds/layers/rate_change/{change}/final",{"view": {"label": "Final", "format": percent_format(1)}} )
        cds.override_node_properties(f"cds/layers/rate_change/{change}/comments",{"async_output": ["start_renewal_task"]} ) # added this to clear out the input on start of renewal.


    cds.override_node_properties(
        "cds/layers/rate_change/expiring_layer", 
        {  
            "async_input": rarc_tasks_names,
            "async_output": [{"task": "start_renewal_task", "reset": False}],
            "options": [*range(1,max_layers+1)],
    })

    cds.extend_node_rater_defined("cds/layers/rate_change", {
        # "risk_adjusted_rate_change": hx.Float(mode="output", view={"label": "Final Risk Adjusted Rate Change", "format": percent_format()}), # EDIT v0.3.0 removed since it has moved to CDS 1.3.0
        "risk_adjusted_rate_change_case_priced": hx.Float(mode="input", optionality='optional', default=None, view={"label": "Final Risk Adjusted Rate Change", "format": percent_format(), "options": {"read_only": {"read_only": True}}}),
        # "risk_adjusted_rate_change_gross_for_reporting": hx.Float(mode="output"), # EDIT v0.3.0 removed since it has moved to CDS 1.3.0
        **rc_quoted_premium(),
        **rc_expiring_and_renewal(),        
        "expiring_policy_info": hx.Structure(children={**rc_expiring_info()}),
        "error_message": hx.Str(mode="output"),
        "temp_storage": hx.Structure(children={**rc_temp_storage()}),
        # "new_layer": hx.Bool(mode="input", default=False, async_input= rarc_tasks_names, view={"label": "New Layer"}), # Edit Addition v0.3.0 
        "new_layer": hx.Bool(mode="output", view={"label": "New Layer"}), # Edit Addition v0.3.0 
        "renewing_layer": hx.Bool(mode="output",async_input= rarc_tasks_names), # Edit Addition v0.3.0 
        "show_expiring_revalued": hx.Bool(mode="output",async_input= rarc_tasks_names), # Edit Addition v0.3.0 - Amount converted in renewing currency use to handle change in currency at renewal.

    }) 

    ### --- MODIFIED RATE CHANGE DATA SCHEMA FOR LAYERS --- ### 
    cds.override_node_properties("cds/layers/quoted_premium_annual_100", {"async_input": [rarc_task_name]})
    cds.override_node_properties("cds/layers/benchmark_premium_annual_100", {"async_input": [rarc_task_name]})
    
    ### --- BUILD RATE CHANGE DATA SCHEMA FOR COVERAGES --- ### 
    if RARC_COVERAGE_USE:
        cds.extend_node_rater_defined("cds/layers/rate_change", {
        **{
            cvg: hx.Structure(view=cvg_view, children={
                **{change: hx.Structure(view=rc_view, children={
                    "model_calculated": hx.Float(mode="output", async_output=[] if change=="rate_change" else [rarc_task_name], view={"label": "Model", "format": percent_format(1)}),
                    "uw_selected": hx.Float(mode="output" if change=="rate_change" else "override", async_output=[{"task": rarc_task_name, "reset": False},"start_renewal_task"], view={"label": "UW Selected", "format": percent_format(1)}),
                    "uw_override": hx.Float(mode="input", default=None, optionality="optional", async_output=[{"task": rarc_task_name, "reset": False}, "start_renewal_task"],view={"label": "UW Override %", "format": {"output": "percent", "mantissa": 1}}),
                    "final": hx.Float(mode="output", view={"label": "Final %", "format": {"output": "percent", "mantissa": 1}}),
                    "comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}, async_output=[{"task": "start_renewal_task", "reset": False}])
                }) for change, rc_view in rarc_changes.items()},
                "rate_change": hx.Structure(view={"label": "Risk Adjusted Rate Change"}, children={
                    "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": {"output": "percent", "mantissa": 1}}),
                    "uw_selected": hx.Float(mode="output", view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 1}}),
                    "comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                    "lloyds_limit_attachment_point_change": hx.Float(mode="output", view={"label": "Lloyds's Limit Attachment Point Change", "format": {"output": "percent", "mantissa": 0}}),
                    "lloyds_breadth_of_cover_change": hx.Float(mode="output", view={"label": "Lloyds's Breadth of Cover Change", "format": {"output": "percent", "mantissa": 0}}),
                    "other_factors_change": hx.Float(mode="output", view={"label": "Other Factors Change", "format": {"output": "percent", "mantissa": 0}}),
                    "uw_override": hx.Float(mode="input", default=None, optionality="optional", view={"label": "UW Override", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                    "final": hx.Float(mode="output", view={"label": "Final", "format": {"output": "percent", "mantissa": 1}}),
                }),
                "risk_adjusted_rate_change": hx.Float(mode="output", view={"label": "Final Risk Adjusted Rate Change", "format": percent_format(1)}),
                "risk_adjusted_rate_change_case_priced": hx.Float(mode="input", optionality='optional', default=None, view={"label": "Final Risk Adjusted Rate Change", "format": percent_format(1), "options": {"read_only": {"read_only": True}}}),
                "risk_adjusted_rate_change_gross_for_reporting": hx.Float(mode="output", view={"label": "Risk Adjusted Rate Change (Gross For Reporting)", "format": percent_format(1)}),
                **rc_quoted_premium(),
                **rc_expiring_and_renewal(),
                "expiring_policy_info": hx.Structure(children={**rc_expiring_info()}),
                "error_message": hx.Str(mode="output"),
                "temp_storage": hx.Structure(children={**rc_temp_storage()}),
                "new_layer": hx.Bool(mode="input", default=False, async_input= rarc_tasks_names, view={"label": "New Layer"}), # Edit Addition v0.3.0 
                "renewing_layer": hx.Bool(mode="output",async_input= rarc_tasks_names), # Edit Addition v0.3.0 
                "show_expiring_revalued": hx.Bool(mode="output",async_input= rarc_tasks_names), # Edit Addition v0.3.0 - Amount converted in renewing currency use to handle change in currency at renewal.

            }) for cvg, cvg_view in coverages_dict.items()
        },  
        })
        ### --- MODIFIED RATE CHANGE DATA SCHEMA FOR COVERAGES --- ###
        
        [(
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/quoted_premium_annual_100", {"async_input": [rarc_task_name]}),
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/benchmark_premium_annual_100", {"async_input": [rarc_task_name]}),
        ) for cvg, cvg_view in coverages_dict.items()
        ]
    
    ### --- BUILD GENERAL RATE CHANGE SECTION DATA SCHEMA --- ###
    
    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            **{f"show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
            "expiring_policy_option_id": hx.Int(mode="override", async_input=rarc_tasks_names, async_output=["start_renewal_task"],view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "has_fetch_not_run": hx.Bool(mode="input", default=True, async_output=rarc_tasks_names),
            "has_fetch_run": hx.Bool(mode="output", async_output=rarc_tasks_names),
            "has_rarc_not_run": hx.Bool(mode="input", default=True, async_output=[rarc_task_name]),
            "has_rarc_run": hx.Bool(mode="output", async_output=[rarc_task_name]),
            "rarc_run_again_message": hx.Str(mode="output"),
            "rarc_message_show": hx.Bool(mode="output"),
            "layer_mapping": hx.Str(mode="output", async_output=rarc_tasks_names),
            # EDIT Addition v0.3.0
            "instructions": hx.Str(mode="input",view={"label": "Instructions", "read_only":True,"multiline":True},
                default="""The rate change tab calculates the change in premium associated with each component (detailed descriptions in the table below). The most appropriate method to obtain a rate change is to calculate the change on premium rather than the change in underlying factors as there are numerous interactions and products to consider.

                    To calculate the rate change, please follow the steps below:
                    1) The user should fist click 'Fetch Expiring Data' to initialise the rate change calculation.
                    2) Select mapping between renewing layers and expiry, this needs to be a 1-1 mapping. For new layers that do not have any link to expiring layer, set the expiring layer to the blank value.
                    3) If there have been any changes to the previous tabs (including the first instance of reaching this tab in any record/YOA), please press 'Calculate Rate Change'.
                    4) The rater will derive the rate changes to each component from the user input.
                    5) The user will be able to override the rate change values as appropriate in the 'UW Selected %' column.
                    6) To recalculate rate change following further changes, please press 'Calculate Rate Change' again.
                    7) Following the task running, the user will be able to override 'Expiring' and 'Renewal' fields with rate change automatically calculating WITHOUT having to run the task again. 

                    _Rate Change Components Include:_
                    _**Exposure Change**_: Driven by changes to base premium due to market cap, assets, country, industry, and ADR percentage
                    _**Risk Characteristics Change**_: Driven by changes to schedule modifiers
                    _**Deductible Change**_: Driven by changes to excesses, and deductibles
                    _**Limit Change**_: Driven by changes to limits 
                    _**Terms and Conditions Change**_: Driven by changes to coverages selected
                    _**Other Change**_: Driven by any other factors such as brokerage
                    """),
            "expiring_inception_date": hx.Date(mode="output", async_output=rarc_tasks_names),
            "expiring_expiry_date": hx.Date(mode="output", async_output=rarc_tasks_names),
            "rarc_coverage_use": hx.Bool(mode="output"),
            "rarc_insured_asset_use": hx.Bool(mode="output"),
            **rc_show_coverages(),
            **rc_insured_asset_list()
        })
    })

    cds.override_node_properties("cds/currencies/source_currency", {"async_input": [rarc_task_name,"run_simulation_task"],"async_output": [{"task": rarc_task_name, "reset": False}], "view":{"label": "Exposure, Structure & Premium Currency"}})
    
    
 
