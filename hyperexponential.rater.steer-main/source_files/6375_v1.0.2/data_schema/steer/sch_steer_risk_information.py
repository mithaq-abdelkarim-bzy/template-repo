import hx_data_schema as hx
import data_schema.sch_utilities as utils # include thousands_format, percent_format, integer_format)
from algorithms.rate_constants import max_layers, experience_rating_max_years, max_data_layout, reinstatement_max_number


def _steer_risk_info():
    return {
        "database_id": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Database ID", "format": utils.integer_format(0)}),
        "application_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Application Date"}),
        # "select_class": hx.Str(mode="input", default="", optionality="optional", view={"label": "Select Class"}),
        # "cob_reference": hx.Str(mode="output", view={"label": "COB Reference"}),
        # "deal_status": hx.Str(mode="input", default="Rating", optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], view={"label": "Deal Status"}),
        "deal_status": hx.Str(mode="input", default="Submission", optionality="optional", options=["Submission"], view={"label": "Deal Status"}),
        "clearance_status": hx.Str(mode="input", default=None, optionality="optional", options=["Quotable","blocked"],view={"label": "Clearance Status"}),
        "basis": hx.Str(mode="input", default=None, optionality="optional", options=["CMD","LOD","RAD"], view={"label": "Basis"}),
        "new_replacement": hx.Str(mode="input", default="", optionality="optional", view={"label": "New/Replacement"}),   
    }