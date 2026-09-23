import hx_data_schema as hx
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers

"""
NOTE: The 'override_node_properties' method is not cumulative. If two overrides are added in seperate places 
to the same node in the script, the one added last will override all the others. 
"""

def sch_overrides(cds):
    # Change labels for read only mode
    cds.override_node_properties("cds/layers/written_line", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/written_line_case_priced", {"view": {"options": {"read_only": {"read_only": True}}}})


    cds.override_node_properties("cds/layers/coverages/eo/status", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/coverages/mediatech/status", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/coverages/gl/status", {"view": {"options": {"read_only": {"read_only": True}}}})

