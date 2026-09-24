import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict
from data_schema.sch_rate_change import rarc_task_name


def sch_clash(cds):
    cds.extend_node_rater_defined("cds", { 
        "clash": hx.Structure(children={
            "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
            "application_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Application Date"}),
            "select_class": hx.Str(mode="input", default="", optionality="optional", view={"label": "Select Class"}),
            "deal_status": hx.Str(mode="input", default="Rating", optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], view={"label": "Deal Status"}),
            "clearance_status": hx.Str(mode="output", view={"label": "Clearance Status"}),
            "basis": hx.Str(mode="input", default="", optionality="optional", view={"label": "Basis"}),
            "new_replacement": hx.Str(mode="input", default="", optionality="optional", view={"label": "New/Replacement"}),
            "include_aad": hx.Bool(mode="input", default=False, view={"label": "Include AAD"}),
            "include_loss_corridor": hx.Bool(mode="input", default=False, view={"label": "Include Loss Corridor"}),
            "include_swing_rates": hx.Bool(mode="input", default=False, view={"label": "Include Swing Rates"}),
        }),

        
    })



