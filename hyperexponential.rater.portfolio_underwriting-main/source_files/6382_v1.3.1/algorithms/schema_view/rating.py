import hx_data_schema as HX
import hx
import json
import datetime


LIST_NODE_DIR = ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']

 
def schema_view_rating(hxd: HX.Structure):
    """
    This function is to restrict the use in editing mode only,
    when it is a test/live policy the compoent will be hidden.
    """
    hxd.schema_view.show_view = True
    hxd.schema_view.stringified_json = _hxd_to_json(hxd)
 

def _hxd_to_json(hxd):
    hxd_dict = _unpack_hxd_attrs(hxd)
    return json.dumps(hxd_dict, default=str)
 

def _unpack_hxd_attrs(node):
    """Safe conversion of hxd to json, skipping file/triangle nodes."""
    
    # Unpacking a list node
    if ("hx_internal" in str(type(node))) and (dir(node) == LIST_NODE_DIR):  
        return [_unpack_hxd_attrs(item) for item in node]

    # Otherwise unpack as a structure 
    node_dict = {}
    for attr in dir(node):
        if attr.startswith("__") and attr.endswith("__"):
            continue  # Skip magic attributes

        try:
            child = getattr(node, attr)
            if "hx_internal" in str(type(child)):  # Nested hx renew component - unpack further 
                node_dict[attr] = _unpack_hxd_attrs(child)
            else:      
                node_dict[attr] = child
        except:  # unreadable child (triangle or file)
            continue

    return node_dict