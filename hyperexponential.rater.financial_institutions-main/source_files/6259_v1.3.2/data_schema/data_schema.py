import hx_data_schema as hxd
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema

from data_schema.sch_cover_details import sch_cover_details_non_cds
from data_schema.sch_exposure_details import sch_exposure_details, sch_exposure_details_non_cds
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_factors import sch_rating_factors
from data_schema.sch_rating_summary import sch_rating_summary, sch_rating_summary_non_cds
from data_schema.sch_rationale import sch_rationale
from data_schema.sch_risk_assessment import sch_risk_assessment, sch_risk_assessment_non_cds
from data_schema.sch_risk_information import sch_risk_information, sch_risk_information_non_cds


def sch_common_data_schema():
    cds = CommonDataSchema()
    sch_risk_information(cds)
    sch_exposure_details(cds)
    sch_rating_factors(cds)
    sch_risk_assessment(cds)
    sch_rating_summary(cds)
    sch_rationale(cds)
    sch_rate_change(cds)

    return cds.get_data_schema()


# These are the data schema items used for formatting and don't go into the cds
def sch_non_cds_items():
    return {
        "non_cds": hxd.Structure(children={
            **sch_risk_information_non_cds(),
            **sch_exposure_details_non_cds(),
            **sch_cover_details_non_cds(),
            **sch_risk_assessment_non_cds(),
            **sch_rating_summary_non_cds()
        })
    }


def add_async_input(node, task_name="export_to_excel"):
    if isinstance(node, hxd.nodes.ListNode) and node.mode == 'output':
        return

    # Add to async_input if node supports it and is in the correct mode
    if hasattr(node, "async_input"):
        existing = node.async_input
        if isinstance(existing,hxd.nodes.Undefined) or existing is None:
            node.async_input = [task_name]
        elif isinstance(existing, list) and task_name not in existing:
            existing.append(task_name)
            node.async_input = existing  # explicitly reassign in case the list was copied

    # Recurse into children if it's a Structure or List
    if isinstance(node, (hxd.nodes.StructureNode, hxd.nodes.ListNode)):
        for child in node.children.values():
            add_async_input(child, task_name)


@hxd.data_schema
def data_schema():
    schema = hxd.Structure(children={
        "output_file": hxd.File(mode="output", async_output=["export_to_excel"], file_name="output_file.xlsx"),
        "excel_export_notes":hxd.Str(mode="input",default="To use this functionality on a FINAL policy: please move the policy back to DRAFT, run the ‘Export to Excel’ function and then move the policy back to FINAL.", view={"read_only": True}),
        **sch_common_data_schema(),
        **sch_model_state(),
        **sch_non_cds_items()
    })
    add_async_input(schema)
    return schema
