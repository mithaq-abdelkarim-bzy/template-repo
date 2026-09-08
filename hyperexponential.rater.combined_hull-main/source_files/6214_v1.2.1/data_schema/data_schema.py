import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import (
    CommonDataSchema,
)
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_vessels import sch_vessels
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_portfolio_analysis import sch_portfolio_analysis
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_non_cds import sch_non_cds_controllers
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_vessel_analysis import sch_vessel_analysis


def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_vessels(cds)
    sch_vessel_analysis(cds)
    sch_rate_change(cds)
    sch_exposure_details(cds)
    sch_portfolio_analysis(cds)
    sch_rating_summary(cds)
    sch_experience_rating(cds)

    return cds.get_data_schema()


# These are the data schema items used for formatting and don't go into the cds
def sch_non_cds_items():
    return {
        "non_cds": hx.Structure(
            children={
                **sch_non_cds_controllers(),
            }
        )
    }


@hx.data_schema
def data_schema():
    schema = hx.Structure(
        children={
            **sch_common_data_schema(),
            **sch_model_state(),
            **sch_non_cds_items(),
            "hx_core": hx.Structure(
                children={
                    "inception_date": hx.Date(
                        default="2018-01-01",
                        mode="input",
                        async_input=["rarc_task", "start_renewal_task","generate_rating_summary_xlsx_task"],
                        view={"label": "Inception Date"},
                    ),
                    "expiry_date": hx.Date(
                        default="2018-12-31",
                        mode="input",
                        async_input=["rarc_task", "start_renewal_task","generate_rating_summary_xlsx_task"],
                        view={"label": "Expiry Date"},
                    ),
                },
                view={"label": "Hx Core"},
            ),
            "rate_change": hx.Structure(
                children={
                    "hull_vessels": hx.Str(mode="output", async_input=["rarc_task"]),
                    "loh_vessels": hx.Str(mode="output", async_input=["rarc_task"]),
                    "shipbuilders_vessels": hx.Str(
                        mode="output", async_input=["rarc_task"]
                    ),
                    "expiring_hull_vessels": hx.Str(
                        mode="output", async_output=["start_renewal_task"]
                    ),
                }
            ),
        }
    )

    def add_async_output(node, task={"task": "start_renewal_task", "reset": False}):

        if isinstance(node, hx.nodes.StructureNode):
            for child in node.children.values():
                add_async_output(child, task)
            return

        if (
            isinstance(node, hx.nodes.ListNode) and node.mode == "output"
        ) or node.mode != "input":
            return

        # Add to async_output if node supports it and is in the correct mode
        if hasattr(node, "async_output"):
            existing = node.async_output
            if isinstance(existing, hx.nodes.Undefined) or existing is None:
                node.async_output = [task]
            elif isinstance(existing, list) and task not in existing:
                existing.append(task)
                node.async_output = (
                    existing  # explicitly reassign in case the list was copied
                )

        # Recurse into children if it's a Structure or List
        if isinstance(node, hx.nodes.ListNode):
            for child in node.children.values():
                add_async_output(child, task)

    add_async_output(schema)
    return schema
