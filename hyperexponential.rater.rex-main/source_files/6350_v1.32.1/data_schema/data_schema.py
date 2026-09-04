import hx_data_schema as hx
from data_schema.core import core
from data_schema.policy_information import policy_information
from data_schema.layers import layers_and_perils
from data_schema.perils import non_layer_perils
from data_schema.sublimit import sublimit
from data_schema.comments import comments
from data_schema.schedule import schedule
from data_schema.temp import temp_storage
from data_schema.exposure_management_api import exposure_management_api
from data_schema.summary import non_layer_summary
from data_schema.spatialkey import spatialkey
from data_schema.rate_change import rate_change
from data_schema.quote_documents import quote_documents
from data_schema.account_segmentation import account_segmentation
from data_schema.rationale import rationale
from data_schema.model_state import model_state
from data_schema.experience_rating import experience_rating
from data_schema.utilities import run_schedule_rater_async_tasks
from libraries.email_notification.data_schema.bug_report_schema import bug_report

@hx.data_schema
def data_schema():
    return hx.Structure(
        children={
            # Data schema related to policy info page input/output
            **policy_information(),
            **layers_and_perils(),
            **non_layer_perils(),
            **sublimit(),
            **comments(),
            **non_layer_summary(),

            # Schedule
            **spatialkey(),
            **schedule(),


            # temp storage storing fields that are reset in async tasks
            **temp_storage(),

            **exposure_management_api(),
            **account_segmentation(),
            **rate_change(),
            **rationale(),
            **quote_documents(),
            **core(),
            **model_state(),
            **experience_rating(),
            **bug_report()
        }
    )
