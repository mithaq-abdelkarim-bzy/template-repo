import hx_data_schema as hx
import data_schema.sch_utilities as utils
import algorithms.rate_constants as const

def sch_admitted(cds):

#### BICI and BAIC structures ####
    cds.extend_node_rater_defined("cds", {
        "admitted": hx.Structure(children={
            "conditions_met": hx.Bool(mode="output", view={"label": "None"}),
            "is_admitted": hx.Bool(mode="output", view={"label": "None"}),
            "is_not_admitted": hx.Bool(mode="output", view={"label": "None"}),
            "is_bici": hx.Bool(mode="output", view={"label": "None"}),
            "is_baic": hx.Bool(mode="output", view={"label": "None"}),
            "insurer": hx.Str(mode="input", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task","reset_admitted_reasons_task"], default=None, optionality="optional", options=["BICI", "BAIC"], view={"label": "Insurer"}),
            "selected_option": hx.Int(mode="input", default=1, options=[*range(1,const.max_layers + 1)], view={"label": "Selected Option"}),
            "company": hx.Str(mode="output", view={"label": "Company"}),
            "state": hx.Str(mode="output", view={"label": "State"}),
            "inception_date": hx.Date(mode="output", view={"label": "Inception Date"}),
            "total_assets": hx.Float(mode="output", view={"label": "Total Assets", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "limit": hx.Float(mode="output", view={"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "excess": hx.Float(mode="output", view={"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "deductible": hx.Float(mode="output", view={"label": "Deductible / SIR (Minimum)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium": hx.Float(mode="output", view={"label": "Quoted Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "bici": hx.Structure(children={
                "final_premium": hx.Float(mode="output", view={"label": "Final Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "rounding_value": hx.Float(mode="output", view={"label": "Rounding Value"}),
                "rounding_message": hx.Str(mode="output", view={"label": "Rounding Message"}),
                "rounded_premium": hx.Float(mode="override", view={"label": "Rounded", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "show_final_prem_factor": hx.Bool(mode="output", view={"label": "None"}),
                "step_2_im": hx.Structure(view={"label": "Step 2 - Industry"}, children={
                    "selected": hx.Float(mode="input", async_output=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], default=None, optionality="optional", view={"label": "Selected", "format": {"mantissa": 4}}),
                    "reason": hx.Str(mode="output", view={"label": "Reason"}),
                    "min": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Min"}),
                    "max": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Max"}),
                    "message": hx.Str(mode="output", view={"label": "Message"}),
                }),
                "step_18a_fcp": hx.Structure(view={"label": "Step 18a - Final Calculated Premium Factor"}, children={
                    "selected": hx.Float(mode="input", async_output=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], default=None, optionality="optional", view={"label": "Selected"}),
                    "reason": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Reason"}),
                    "min": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Min"}),
                    "max": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Max"}),
                    "message": hx.Str(mode="output", view={"label": "Message"}),
                }),
                **{
                    step: hx.Structure(view={"label": label}, children={
                        "selected": hx.Float(mode="input", async_output=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], default=None, optionality="optional", view={"label": "Selected", "format": {"mantissa": 4}}),
                        "reason": hx.Str(mode="input", async_output=["reset_admitted_reasons_task"], default=None, optionality="optional", view={"label": "Reason"}),
                        "min": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Min"}),
                        "max": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Max"}),
                        "message": hx.Str(mode="output", view={"label": "Message"}),
                    })
                    for step, label in zip(const.bici_other_steps, const.bici_other_steps_labels)
                },
                **{
                    step: hx.Structure(view={"label": label}, children={
                        "selected": hx.Float(mode="output", view={"label": "Selected"}),
                        "message": hx.Str(mode="output", view={"label": "Message"}),
                    })
                    for step, label in zip(const.bici_calc_steps, const.bici_calc_steps_labels)
                },
                **{
                    dropdown : hx.List(mode="output",children={
                    "Activity" :hx.Str(mode="output", view={"label": "Reason"})
                    })
                    for dropdown in [step + "_bici_dropdown" for step in const.bici_other_steps]    
                },
            }),
            # TODO: make this a loop
            "baic": hx.Structure(children={
                "is_california": hx.Bool(mode="output", async_input=["reset_admitted_reasons_task","set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "None"}),
                "is_california_not": hx.Bool(mode="output", view={"label": "None"}),
                "final_premium": hx.Float(mode="output", view={"label": "Final Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "rounding_value": hx.Float(mode="output", view={"label": "Rounding Value"}),
                "rounding_message": hx.Str(mode="output", view={"label": "Rounding Message"}),
                "rounded_premium": hx.Float(mode="override", view={"label": "Rounded", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "show_final_prem_factor": hx.Bool(mode="output", view={"label": "None"}),
                "step_1_bpm": hx.Structure(view={"label": "Step 1 - Base Premium"}, children={
                    "selected": hx.Float(mode="output", view={"label": "Selected", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "message": hx.Str(mode="output", view={"label": "Message"}),
                }),
                "step_2_im": hx.Structure(view={"label": "Step 2 - Industry"}, children={
                    "selected": hx.Float(mode="input", async_output=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], default=None, optionality="optional", view={"label": "Selected"}),
                    "reason": hx.Str(mode="output", view={"label": "Reason"}),
                    "min": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Min"}),
                    "max": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Max"}),
                    "message": hx.Str(mode="output", view={"label": "Message"}),
                }),
                "step_15_clrm": hx.Structure(view={"label": "Step 15 - Combined Limit/Retention Factor"}, children={
                    "selected": hx.Float(mode="output", view={"label": "Selected"}),
                    "message": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Message"}),
                }),
                "step_19a_fcp": hx.Structure(view={"label": "Step 19a - Final Calculated Premium Factor"}, children={
                    "selected": hx.Float(mode="input", async_output=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], default=None, optionality="optional", view={"label": "Selected"}),
                    "reason": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Reason"}),
                    "min": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Min"}),
                    "max": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Max"}),
                    "message": hx.Str(mode="output", view={"label": "Message"}),
                }),
                **{
                    step: hx.Structure(view={"label": label}, children={
                        "selected": hx.Float(mode="input", async_output=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], default=None, optionality="optional", view={"label": "Selected", "format": {"mantissa": 4}}),
                        "reason": hx.Str(mode="input", async_output=["reset_admitted_reasons_task"], default=None, optionality="optional", view={"label": "Reason"}),
                        "min": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Min"}),
                        "max": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Max"}),
                        "message": hx.Str(mode="output", view={"label": "Message"}),
                    })
                    for step, label in zip(const.baic_other_steps, const.baic_other_steps_labels)
                },
                **{
                    step: hx.Structure(view={"label": label}, children={
                        "selected": hx.Float(mode="output", view={"label": "Selected"}),
                        "message": hx.Str(mode="output", view={"label": "Message"}),
                    })
                    for step, label in zip(const.baic_calc_steps, const.baic_calc_steps_labels)
                },
                "step_20_srf": hx.Structure(view={"label": "Step 20 - Schedule Rating Factor"}, children={
                        "selected": hx.Float(mode="output", view={"label": "Selected"}),
                        "message": hx.Str(mode="output", view={"label": "Message"}),
                        "min": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Min"}),
                        "max": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Max"})
                        }),
                **{
                    dropdown : hx.List(mode="output",children={
                    "Activity" :hx.Str(mode="output", view={"label": "Reason"})
                    })
                    for dropdown in [step + "_baic_dropdown" for step in const.baic_other_steps]    
                },
                **{
                    step: hx.Structure(view={"label": label}, children={
                        "selected": hx.Float(mode="input", async_output=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], default=None, optionality="optional", view={"label": "Selected", "format": {"mantissa": 4}}),
                        "min": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Min"}),
                        "max": hx.Float(mode="output", async_input=["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task"], view={"label": "Max"}),
                        "message": hx.Str(mode="output", view={"label": "Message"}),
                    })
                    for step, label in zip(const.baic_ca_input_steps, const.baic_ca_input_step_labels)
                },
            }),
        }),
    })

#### Step dropdowns ####

    ## BICI ##
    steps = const.bici_other_steps

    for step in (steps):
        path = step + "_bici_dropdown"

        # Override dropwown links
        step_path = 'cds/admitted/bici/' + step + '/reason'
        #path = "../../../../" + path
        path = "../../" + path
        cds.override_node_properties(step_path, {'options_data': path, 'options_field': "Activity", "view": {"label":"Reason", "multiline": True}})

    ## BAIC ##
    steps = const.baic_other_steps

    for step in (steps):
        path = step + "_baic_dropdown"

        # Override dropwown links
        step_path = 'cds/admitted/baic/' + step + '/reason'
        path = "../../" + path
        cds.override_node_properties(step_path, {'options_data': path, 'options_field': "Activity", "view": {"label":"Reason", "multiline": True}})
    
#### Updating async tasks ####

# This is only necessary because of set_child_nodes_to_rarc_task_inputs(cds.get_data_schema(), cds)
# All these updates are in the extend_node_rater_defined function above
# However, these get overrided with async_input=["rarc_task"] unless they are set again here
# JD?: Why is this the case? Can we fix this?

    cds.override_node_properties('cds/admitted/insurer',{'async_input':["set_admitted_to_min_task", "set_admitted_to_max_task", "set_admitted_to_midpoint_task", "reset_admitted_reasons_task"]})
