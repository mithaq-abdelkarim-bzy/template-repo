import hx_data_schema as hx
from collections import ChainMap
from itertools import chain

def thousands_format(mantissa=0):
    return {"thousandSeparated": True, "mantissa": mantissa}

def percent_format(mantissa=0):
    return {"output": "percent", "mantissa": mantissa}

def integer_format(mantissa = 0):
    return {"thousandSeparated": False, "mantissa": mantissa}

def merge_dicts(l):
    """
    merge multiple dictionaries into one
    """
    return dict(ChainMap(*reversed(list(l))))

# Helper functions to set properties in multiple data schema nodes.
def _type_of(value):
    return value.__class__.__name__


def _nth(number):
    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number, 'th')
    return f'{number}{suffix}'


def _str_type_check(iterable, iterable_name):
    """
    Check that every item in the iterable is a string
    iterable_name is included so a nice error message can be raised
    """
    for i, path in enumerate(iterable, start=1):
        if not isinstance(path, str):
            raise TypeError(
                f'`{iterable_name}` is expected to be an iterable of `str`s, '
                f'but the {_nth(i)} object is: {_type_of(path)}')


def set_node_properties(hxd_node, node_paths, *, async_input=None, async_output=None, mode=None):
    """
    Set properties for each node within in a list of nodes
    
    Arguments:
    hxd_node: Can be any structural node but will generally be the full data schema
    node_paths: A list of paths to nodes in the hxd_node, with the path to a child node of a Structure and List represented by "/"
    async_input: A list of async inputs
    async_output: An async output
    mode: An item node
    """
    
    # Validation
    # Keyword validation
    if not any([async_input, async_output, mode]):
        raise ValueError("At least one keyword argument must be supplied: `async_input`, `async_output`, or `mode`")
    
    # Type validation
    if not isinstance(node_paths, list):
        raise TypeError(f"`node_paths` must be of type `list`, but is of type `{_type_of(node_paths)}`")
    _str_type_check(node_paths, "node_paths")

    if not isinstance(hxd_node, hx.Structure):
        raise TypeError(f"`hxd_node` must be a Structure Node, but is a `{_type_of(hxd_node)}`")

    if async_input:
        if not isinstance(async_input, list):
            raise TypeError(f"`async_input` must be of type `list`, but is of type `{_type_of(async_input)}`")
        _str_type_check(async_input, "async_input")

    if async_output:
        if not (isinstance(async_output, list) or isinstance(async_output, str)):
            raise TypeError(f"`async_output` must be one of type `list` or `str`, but is of type `{_type_of(async_output)}`")
        _str_type_check(async_output, "async_output")

    if mode and mode != "output":
        raise TypeError(f"If `mode` is set, it must have the value 'output'")
   
    # Iterate through each path in node_paths
    for node_path in node_paths:

        # Set new reference to hxd_node so it can be reused for the next node_path
        data_schema_node = hxd_node

        for node in filter(bool, node_path.split('/')):
            # Access each successive child node
            # When the for loop has finished, the node on which the property is to be set has been reached
            data_schema_node = data_schema_node[node]

        # Set async_input property
        if async_input is not None:
            if isinstance(data_schema_node.async_input, hx.nodes.Undefined):
                data_schema_node.async_input = async_input
            else:
                data_schema_node.async_input = list(set(chain(async_input, data_schema_node.async_input)))

        # Set async_output property
        # Sanitise value to a list if it is a string
        async_output_list = [async_output] if isinstance(async_output, str) else async_output

        if async_output is not None:
            # No existing async output
            if isinstance(data_schema_node.async_output, hx.nodes.Undefined):
                data_schema_node.async_output = async_output
            # Append to existing async outputs while removing duplicate tasks
            else:
                existing_outputs = [data_schema_node.async_output] if isinstance(data_schema_node.async_output, str) else data_schema_node.async_output
                data_schema_node.async_output = list(set(chain(async_output_list, existing_outputs)))

        # Set mode property to "output"
        if mode is not None:
            
            data_schema_node.mode = mode

            if not isinstance(data_schema_node, hx.List):                
                # If mode is changed to output, `read_only` is not a valid key
                if not isinstance(data_schema_node.view, hx.nodes.Undefined):

                    # Outside a view option
                    data_schema_node.view.pop("read_only", None)
                        
                    # Inside a view option
                    for key in data_schema_node.view.get("options", {}):
                        data_schema_node.view["options"][key].pop("read_only", None)

                if not isinstance(data_schema_node, hx.nodes.DateNode):
                    data_schema_node.options = hx.nodes.UNDEFINED
                    data_schema_node.options_column = hx.nodes.UNDEFINED
                    data_schema_node.options_table = hx.nodes.UNDEFINED
                    data_schema_node.default_index = hx.nodes.UNDEFINED
                    data_schema_node.default = hx.nodes.UNDEFINED

def run_schedule_rater_async_tasks(async_input = True):
    '''
    Tasks which require to run the run_schedule_rater_task async task.
    Grouped together to make data schema more readable
    '''
    if async_input: 
        return ["run_schedule_rater_task", "remove_experience_adjustment_task", "fill_intl_ded_countries_task", "save_case_pricing_results_task", "machinery_breakdown_industry_task", "check_remodel_task", "generate_flood_climate_metrics_task"]
    else:
        return ["run_schedule_rater_task", "remove_experience_adjustment_task", {"task":"fill_intl_ded_countries_task", "reset": False}, {"task":"save_case_pricing_results_task", "reset": False}, {"task":"machinery_breakdown_industry_task", "reset": False},{"task": "check_remodel_task", "reset": False}, {"task":"generate_flood_climate_metrics_task","reset":False}]