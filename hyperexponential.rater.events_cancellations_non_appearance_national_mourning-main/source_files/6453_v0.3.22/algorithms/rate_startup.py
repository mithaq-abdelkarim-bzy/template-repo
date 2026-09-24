# v0.5.0
import hx
import pandas as pd
import numpy as np
from operator import itemgetter, attrgetter
from datetime import timedelta, datetime
from typing   import List, Optional, Iterable
from algorithms import parameter_tables_schema as params
import math


from algorithms.data_schema.data_schema_static_copy import hx_calculation_legacy_initial_premium 
DS_ROOT = hx_calculation_legacy_initial_premium()



# to do
def generic_ds_code(path):
    nodes                   = ds_get_mode_type(  path  )
    cols                    = [node for node,mode,hxtype,label in nodes if mode == "input"]
    cols                   += [node for node,mode,hxtype,label in nodes if mode == "override"]
    return cols



def ds_get_mode_type(path):
    
    def get_node_by_path(structure, path):
        parts = path.split(".")
        node = structure
        for part in parts:
            node = node.children.get(part)
            if node is None:
                raise ValueError(f"Path '{path}' not found.")
        return node

    root        = DS_ROOT
    clean_path  = path[4:] if path.startswith("hxd.") else path
    node_target = get_node_by_path(root, clean_path)
    results     = []

    if hasattr(node_target, "children"):
        for name, obj in node_target.children.items():
            if not hasattr(obj, "children"):
                mode = getattr(obj, "mode", None)
                field_type = obj.__class__.__name__
                view_label = obj.view.get("label") if hasattr(obj, "view") else None
                results.append((name, mode, field_type, view_label))
    return results
