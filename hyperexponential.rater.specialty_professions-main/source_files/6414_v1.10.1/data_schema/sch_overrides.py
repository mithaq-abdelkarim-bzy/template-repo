# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers
from data_schema.sch_rate_change import rarc_task_name


"""
NOTE: The 'override_node_properties' method is not cumulative. If two overrides are added in seperate places 
to the same node in the script, the one added last will override all the others. 
"""

def sch_overrides(cds):

    
    # Override properties
    

    # Override values
    # cds.override_node_properties("cds/layers/limit", {"async_input": [rarc_task_name]})
    cds.override_node_properties("cds/layers/excess", {"async_input": [rarc_task_name]})
    # cds.override_node_properties("cds/layers/deductible", {"async_input": [rarc_task_name]})    
    cds.override_node_properties("cds/layers/brokerage", {"default": 0, "optionality": "required", "async_input": [rarc_task_name],"view": {"options": {"read_only": {"read_only": True, "label": "Brokerage (excl. PC's)"}}}})
    # cds.override_node_properties("cds/layers/quoted_premium", {"default": 0, "optionality": "required", "async_input": [rarc_task_name], "view": {"options": {"read_only": {"read_only": True}}}})
    # cds.override_node_properties("cds/layers/quoted_premium", {"mode":"output", "optionality": "optionality", "async_input": [rarc_task_name], "view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/section_reference", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/written_line", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": [rarc_task_name]})

    cds.override_node_properties("cds/layers/rate_change/other_change", {"view": {"label": "Other Change (incl. Brokerage)"}})




    

