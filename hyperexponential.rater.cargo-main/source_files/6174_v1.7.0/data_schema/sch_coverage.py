import hx_data_schema as hx
from data_schema.sch_utilities import *

def sch_coverage(cds):

    # Account details
    cds.override_node_properties(
        "cds/standard_fields/benchmark_class", {"default": "Cargo", "optionality": "required"}
    )

    # Excess fields
    cds.override_node_properties(
        "cds/layers/coverages/cargo_transit/excess", 
        {"async_input": ["rarc_task","load_cargo_input"], "view": {"label": "Excess Amount", "format": thousands_format(0)}, "validation": {"min_value": 0}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_storage/excess", 
        {"async_input": ["rarc_task","load_cargo_input"], "view": {"label": "Excess Amount", "format": thousands_format(0)}, "validation": {"min_value": 0}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_cyber_transit/excess", 
        {"async_input": ["rarc_task"], "async_output" : [{"task":"load_cargo_input", "reset": False}],"view": {"label": "Excess Amount", "format": thousands_format(0)}, "validation": {"min_value": 0}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_cyber_storage/excess", 
        {"async_input": ["rarc_task"], "async_output" : [{"task":"load_cargo_input", "reset": False}], "view": {"label": "Excess Amount", "format": thousands_format(0)}, "validation": {"min_value": 0}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/specie_transit/excess", 
        {"async_input": ["rarc_task"], "view": {"label": "Excess Amount", "format": thousands_format(0)}, "validation": {"min_value": 0}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/specie_storage/excess", 
        {"async_input": ["rarc_task"], "view": {"label": "Excess Amount", "format": thousands_format(0)}, "validation": {"min_value": 0}}
    )

    # Limit fields
    cds.override_node_properties(
        "cds/layers/coverages/conloss/limit", 
        {   
            "default": 0,
            "optionality": "required",
            "async_input": ["rarc_task"],
            "view": {"label": "Indemnity Limit", "format": thousands_format(0)},
            "validation": {"min_value": 0, "max_value": 1000000000000}
        }
    )

    # Premium fields
    cds.override_node_properties(
        "cds/layers/coverages/cargo_transit/quoted_premium", 
        {"view": {"label": "Transit Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_transit/technical_premium", 
        {"view": {"label": "Transit Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_storage/quoted_premium", 
        {"view": {"label": "Storage Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_storage/technical_premium", 
        {"view": {"label": "Storage Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_cyber_transit/quoted_premium", 
        {"view": {"label": "Transit Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_cyber_transit/technical_premium", 
        {"view": {"label": "Transit Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_cyber_storage/quoted_premium", 
        {"view": {"label": "Storage Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/cargo_cyber_storage/technical_premium", 
        {"view": {"label": "Storage Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/specie_transit/quoted_premium", 
        {"view": {"label": "Transit Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/specie_transit/technical_premium", 
        {"view": {"label": "Transit Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/specie_storage/quoted_premium", 
        {"view": {"label": "Storage Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/specie_storage/technical_premium", 
        {"view": {"label": "Storage Premium (Term)", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/conloss_transit/quoted_premium", 
        {"view": {"label": "Transit Premium", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/conloss_transit/technical_premium", 
        {"view": {"label": "Transit Premium", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/conloss/quoted_premium", 
        {"view": {"label": "Con Loss Premium", "format": thousands_format(0)}}
    )
    cds.override_node_properties(
        "cds/layers/coverages/conloss/technical_premium", 
        {"view": {"label": "Con Loss Premium", "format": thousands_format(0)}}
    )
    