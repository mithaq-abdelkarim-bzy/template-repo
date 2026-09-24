import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from hx import params as hx_params
import data_schema.sch_utilities as utils

def sch_adjustments(cds):
    cds.extend_node_rater_defined("cds", {
        "modifiers" : hx.Structure(view = {"label": ""}, children = {
            # Longevity Factor
            "longevity_factor" : hx.Float(mode="output", view={"label":"Longevity Factor","format":utils.integer_format(2)}, async_input=["rarc_task"]),
            # Experience Factor
            "experience_factor" : hx.Structure(view = {"label":"Experience Factor"}, children={
                "response" : hx.Str(mode="input", default="No claim activity or claim activity with little severity or frequency", options=hx_params.tbl_experience_factor["experience"].tolist(), view={"label":"Response"}),
                "selected" : hx.Float(mode="input", optionality="optional", default=None, view={"label":"Factor","format":utils.integer_format(2)}),
                "min" : hx.Float(mode="output", view={"label":"Min","format":utils.integer_format(2)}),
                "max" : hx.Float(mode="output", view={"label":"Max","format":utils.integer_format(2)}),
                "output" : hx.Float(mode="output", async_input=["rarc_task"]) # Used in rating. Not shown in view.
            }),
            # Media Liability: Schedule Rating
            "media": hx.Structure(view = {"label" : "Schedule Rating"}, children={
                **{item: hx.Structure(view ={"label": label}, children = {
                "min":hx.Str(mode = "output", view = {"label": "Min","format":utils.percent_format(1)}),
                "max":hx.Str(mode = "output", view = {"label": "Max","format":utils.percent_format(1)}),
                "selected":hx.Float(mode = "input", default=0, view = {"label": "Selected","format":utils.percent_format(1)}, async_input=["rarc_task"]),
                })
                for item, label in zip(hx_params.table_media_schedule_mods["description_name"], hx_params.table_media_schedule_mods["description"])},       
            }),
            # Music Liability: Schedule Rating
            "music": hx.Structure(view = {"label" : "Schedule Rating"}, children={
                **{item: hx.Structure(view ={"label": label}, children = {
                "min":hx.Str(mode = "output", view = {"label": "Min","format":utils.percent_format(1)}),
                "max":hx.Str(mode = "output", view = {"label": "Max","format":utils.percent_format(1)}),
                "selected":hx.Float(mode = "input", default=0, view = {"label": "Selected","format":utils.percent_format(1)}, async_input=["rarc_task"]),
                })
                for item, label in zip(hx_params.table_music_schedule_mods["description_name"], hx_params.table_music_schedule_mods["description"])},       
            }),
            # TV & Film E&O: Schedule Rating
            "tvfilm": hx.Structure(view = {"label" : "Schedule Rating"}, children={
                **{item: hx.Structure(view ={"label": label}, children = {
                "min": hx.Str(mode = "output", view = {"label": "Min","format":utils.percent_format(1)}),
                "max": hx.Str(mode = "output", view = {"label": "Max","format":utils.percent_format(1)}),
                "selected": hx.Float(mode = "input", default=0, view = {"label": "Selected","format":utils.percent_format(1)}, async_input=["rarc_task"]),
                })
                for item, label in zip(hx_params.table_tvfilm_schedule_mods["description_name"], hx_params.table_tvfilm_schedule_mods["description"])},       
            }),
            # Total Schedule Rating Modification
            "total_schedule_mod": hx.Float(mode="output"),  # Used in rating. Not shown in view.
            # Optional Coverages (Info Sec Liability, Tech E&O and False Advertising)
            "optional_coverages": hx.Structure(view = {"label" : "Optional Coverages"}, children={
                **{item: hx.Structure(view ={"label": label}, children = {
                "min": hx.Str(mode = "output", view = {"label": "Min","format":utils.percent_format(1)}),
                "max": hx.Str(mode = "output", view = {"label": "Max","format":utils.percent_format(1)}),
                "selected": hx.Float(mode = "input", default=0, view = {"label": "Selected","format":utils.percent_format(1)}),
                "included": hx.Str(mode = "input", default="No", options=["Yes", "No"], view = {"label":"Included?"}, async_input=["rarc_task"]),
                "comment": hx.Str(mode = "input", optionality="optional", default=None, view = {"label":"Comment"}),
                "output": hx.Float(mode="output", async_input=["rarc_task"]) # Used in rating. Not shown in view.
                })
                for item, label in zip(hx_params.table_optional_coverages["description_name"], hx_params.table_optional_coverages["description"])},       
            }),
            # Extended Reporting Period
            "extended_reporting_period" : hx.Structure(view = {"label":"Extended Reporting Period"}, children={
                "length" : hx.Str(mode="input", optionality="optional", default=None, options=["30 to 60 days"], view={"label":"Length"}),
                "factor" : hx.Float(mode="output", view={"label":"Factor","format":utils.integer_format(2)}, async_input=["rarc_task"]),
            }),
        })
    })