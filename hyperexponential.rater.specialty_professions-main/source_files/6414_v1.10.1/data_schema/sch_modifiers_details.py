import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_modifiers_details(cds):
    
    cds.extend_node_rater_defined("cds", {
        "modifiers": hx.Structure(children={
            # this is an overriddeable figure which contributes to an underwriter adjustment
            "exp_mod": hx.Structure(view= {"label":"In the last 5 years, enter Insured's:"}, children={
                "incurred_loss": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Total incurred loss"}),
                "number_of_claims": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Number of claims"}),
                "number_of_incidents": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Number of incidents"}),
                "written_premium": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Total written premium"}),
                "incurred_lr": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Total incurred loss ratio", "format": utils.percent_format(0)}),
                "exp_mod_factor": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Experience Modification Factor \n (Suggested Range: 0.80 - 2.00)"}),
                "uw_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Underwriter Commentary"}),
                "incurred_lr_info_label": hx.Str(mode="output", view={"label": "Incurred LR Label"}),
                "exp_mod_factor_info_label": hx.Str(mode="output", view={"label": "Experience Modification Label"}),

            }),            
            "schedule_rating_factor": hx.Structure(view = {"label": "Schedule Rating Factor"}, children = {
                "qual_of_staff": hx.Structure(view={"label":"1. Qualifications of Staff"}, children={
                    "min": hx.Float(mode="output", view={"label": "Min", "format": utils.percent_format(0)}),
                    "max": hx.Float(mode="output", view={"label": "Max", "format": utils.percent_format(0)}),
                    "factor": hx.Float(mode="input", async_input=["rarc_task"], default=0.0, view={"label": "Schedule Factor", "format": utils.percent_format(0)}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "rm_attendance": hx.Structure(view={"label":"2. Attendance at Risk Management Seminars"}, children={
                    "min": hx.Float(mode="output", view={"label": "Min", "format": utils.percent_format(0)}),
                    "max": hx.Float(mode="output", view={"label": "Max", "format": utils.percent_format(0)}),
                    "factor": hx.Float(mode="input", async_input=["rarc_task"], default=0.0, view={"label": "Schedule Factor", "format": utils.percent_format(0)}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "foreign_work": hx.Structure(view={"label":"3. Foreign Work"}, children={
                    "min": hx.Float(mode="output", view={"label": "Min", "format": utils.percent_format(0)}),
                    "max": hx.Float(mode="output", view={"label": "Max", "format": utils.percent_format(0)}),
                    "factor": hx.Float(mode="input", async_input=["rarc_task"], default=0.0, view={"label": "Schedule Factor", "format": utils.percent_format(0)}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),

                "loss_prev": hx.Structure(view={"label":"4. Internal Loss Prevention"}, children={
                    "min": hx.Float(mode="output", view={"label": "Min", "format": utils.percent_format(0)}),
                    "max": hx.Float(mode="output", view={"label": "Max", "format": utils.percent_format(0)}),
                    "factor": hx.Float(mode="input", async_input=["rarc_task"], default=0.0, view={"label": "Schedule Factor", "format": utils.percent_format(0)}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "client_type": hx.Structure(view={"label":"5. Type of Client/Project Owner"}, children={
                    "min": hx.Float(mode="output", view={"label": "Min", "format": utils.percent_format(0)}),
                    "max": hx.Float(mode="output", view={"label": "Max", "format": utils.percent_format(0)}),
                    "factor": hx.Float(mode="input", async_input=["rarc_task"], default=0.0, view={"label": "Schedule Factor", "format": utils.percent_format(0)}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "contractual_practices": hx.Structure(view={"label":"6. Contractual Practices"}, children={
                    "min": hx.Float(mode="output", view={"label": "Min", "format": utils.percent_format(0)}),
                    "max": hx.Float(mode="output", view={"label": "Max", "format": utils.percent_format(0)}),
                    "factor": hx.Float(mode="input", async_input=["rarc_task"], default=0.0, view={"label": "Schedule Factor", "format": utils.percent_format(0)}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "engi_procure_construct": hx.Structure(view={"label":"7. Engineer, Procure and Construct"}, children={
                    "min": hx.Float(mode="output", view={"label": "Min", "format": utils.percent_format(0)}),
                    "max": hx.Float(mode="output", view={"label": "Max", "format": utils.percent_format(0)}),
                    "factor": hx.Float(mode="input", async_input=["rarc_task"], default=0.0, view={"label": "Schedule Factor", "format": utils.percent_format(0)}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "peer_review": hx.Structure(view={"label":"8. Peer Review"}, children={
                    "min": hx.Float(mode="output", view={"label": "Min", "format": utils.percent_format(0)}),
                    "max": hx.Float(mode="output", view={"label": "Max", "format": utils.percent_format(0)}),
                    "factor": hx.Float(mode="input", async_input=["rarc_task"], default=0.0, view={"label": "Schedule Factor", "format": utils.percent_format(0)}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "total": hx.Structure(view={"label":"Overall Schedule Rating Factor"}, children={
                    "min": hx.Float(mode="output", view={"label": "Min", "format": utils.percent_format(0)}),
                    "max": hx.Float(mode="output", view={"label": "Max", "format": utils.percent_format(0)}),
                    "factor": hx.Float(mode="output", view={"label": "Schedule Factor", "format": utils.percent_format(0)}),

                }),            
            }),            
        }),
    })

    pass