'''
This file is a back-end file for the transient_hxd. It involves some quite complex python constructions 
and is NOT required to be understood for usage (i.e. it can be used as a "black box"). You are however
welcome to look through if you're interested! 

What is required for usage of the transient_hxd is:
- A copy of the data_schema_static.py file saved in the algorithms folder
    If this is not called data_schema_static.py and saved directly in algorithms this will need to be 
    specified by passing to data_schema_static_path when running init_transient_hxd

If you have any issues when using this script, please contact your contact in the hx model development 
team, or the support portal
'''


from datetime import datetime, date
import importlib
import os
import sys
import decimal
import functools
import numpy as np
from copy import deepcopy
from hx_data_schema.nodes import Undefined
import hx
import itertools
import pandas as pd

LIST_NODE_DIR = ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']
FILE_NODE_DIR = ['exists', 'file_extension', 'file_name', 'file_size', 'open']
OVERRIDE_NODE_DIR = ['calculated', 'is_overridden', 'override', 'selected']

# operation_num = 0
# global_root_node = None

def init_transient_hxd(example_data=None, data_schema_static_path="data_schema_static.py", files_path="transient_hxd_files", reset_outputs=True, skip_invalid_nodes=False):
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_path)
    files_path = os.path.join(os.path.dirname(__file__), files_path)

    loader = TransientHxdLoader(skip_invalid_nodes=skip_invalid_nodes)

    data_schema = DataSchemaStaticParser(data_schema_static_path, files_path, loader)
    defaults = data_schema.get_defaults()
    types = data_schema.get_types()
    optionalities = data_schema.get_optionalities()
    sorted_paths = sorted(defaults.keys())

    root_hxd_node = _new_node({}, loader)

    # global global_root_node
    # global_root_node = root_hxd_node
    # global operation_num

    # Set up defaults
    for path in sorted_paths:
        # operation_num += 1
        # print(f"{operation_num}: {path}") 
        # if operation_num in [24]:
        #     breakpoint()
        # if "benchmark_premium" in path:
        #     breakpoint()
        list_item_combinations = _get_list_length_combinations(root_hxd_node, path)
        if list_item_combinations:
            for list_items in list_item_combinations:
                _set_value_node_metadata(defaults, types, optionalities, root_hxd_node, path, list_items=list_items)
                rsetattr(root_hxd_node, path, defaults[path], list_items=list_items)
        else:
            _set_value_node_metadata(defaults, types, optionalities, root_hxd_node, path, list_items=[])
            rsetattr(root_hxd_node, path, defaults[path], list_items=[])

    sorted_paths.reverse()

    # Lock all nodes
    for path in sorted_paths:
        list_item_combinations = _get_list_length_combinations(root_hxd_node, path)
        if list_item_combinations:
            for list_items in list_item_combinations:
                if isinstance(rgetattr(root_hxd_node, path, list_items=list_items), hx_internal_StructureNode):
                    rgetattr(root_hxd_node, path, list_items=list_items)._lock()
                elif isinstance(rgetattr(root_hxd_node, path, list_items=list_items), hx_internal_ListNode):
                    rgetattr(root_hxd_node, path, list_items=list_items)._lock()
                elif isinstance(rgetattr(root_hxd_node, path, list_items=list_items), hx_internal_OverrideNode):
                    rgetattr(root_hxd_node, path, list_items=list_items)._lock()
                # EDIT IH
                # elif isinstance(rgetattr(root_hxd_node, path, list_items=list_items), hx_internal_TriangleOptions):
                #     rgetattr(root_hxd_node, path, list_items=list_items)._lock()
        else:
            if isinstance(rgetattr(root_hxd_node, path, list_items=[]), hx_internal_StructureNode):
                rgetattr(root_hxd_node, path, list_items=[])._lock()
            elif isinstance(rgetattr(root_hxd_node, path, list_items=[]), hx_internal_ListNode):
                rgetattr(root_hxd_node, path, list_items=[])._lock()
            elif isinstance(rgetattr(root_hxd_node, path, list_items=[]), hx_internal_OverrideNode):
                rgetattr(root_hxd_node, path, list_items=[])._lock()
            # EDIT IH
            # elif isinstance(rgetattr(root_hxd_node, path, list_items=[]), hx_internal_TriangleOptions):
            #     rgetattr(root_hxd_node, path, list_items=[])._lock()

    root_hxd_node._lock()

    # Populate nodes with example data
    if example_data:
        loader.load_from_dictionary(root_hxd_node, example_data)

    if reset_outputs:
        reset_node_outputs(root_hxd_node, loader=loader, data_schema_static_path=data_schema_static_path, files_path=files_path)

    loader.skip_invalid_nodes = False  # Even if this is allowed for this function, want to turn it off at the end

    return root_hxd_node

def _set_value_node_metadata(defaults, types, optionalities, root_hxd_node, path, list_items=[]):    
    # If it isn't a transient_hxd object, or is an override node, need to set type enforcement
    if ("hx_internal_" not in str(type(defaults[path]))) or (isinstance(defaults[path], hx_internal_OverrideNode)):  
        parent_structure, _, child_key = path.rpartition('.')
        if parent_structure:
            parent_node = rgetattr(root_hxd_node, parent_structure, list_items=list_items)
        else:
            parent_node = root_hxd_node

        if isinstance(parent_node, hx_internal_ListNode):
            for list_node_item in parent_node:
                list_node_item._child_types[child_key] = types[path]
                list_node_item._child_optionalities[child_key] = optionalities[path]
        else:
            parent_node._child_types[child_key] = types[path]
            parent_node._child_optionalities[child_key] = optionalities[path]

def transient_to_json(transient_obj):
    dictionary = transient_obj._get_node_dict()
    for key in dictionary:
        if isinstance(dictionary[key], hx_internal_StructureNode):
            dictionary[key] = transient_to_json(dictionary[key])
        if isinstance(dictionary[key], hx_internal_ListNode):
            list_items = []
            for i in range(len(dictionary[key])):
                list_items.append(transient_to_json(dictionary[key][i]))
            dictionary[key] = list_items
    return dictionary

class TransientHxdLoader:
    def __init__(self, skip_invalid_nodes=False):
        self.skip_invalid_nodes = skip_invalid_nodes
    
    def load_from_dictionary(self, hxd_obj, example_data):
        example_data_paths = get_paths(example_data, expand_lists=True)
        example_data_paths = sorted(example_data_paths)

        for path in example_data_paths:
            try:
                list_item_combinations = _get_list_length_combinations(hxd_obj, path)
            except AttributeError:
                if self.skip_invalid_nodes: 
                    continue
                raise

            if not list_item_combinations:
                list_item_combinations = [[]]

            for list_items in list_item_combinations:
                try:
                    if "hx_internal" in str(type(example_data)):
                        rsetattr(hxd_obj, path, rgetattr(example_data, path, list_items=list_items), list_items=list_items)
                    else:
                        try:
                            is_override_parent = isinstance(rgetkey(hxd_obj, path.rsplit('.', 1)[0], list_items=list_items), hx_internal_OverrideNode)
                        except AttributeError:
                            if self.skip_invalid_nodes: 
                                break
                            raise

                        if is_override_parent and '.' in path and path.rsplit('.', 1)[1] in hx_internal_OverrideNode._protected_override_children:
                            continue
                        if is_override_parent and '.' in path and path.rsplit('.', 1)[1] == "override" and not rgetkey(example_data, path.rsplit('.', 1)[0], list_items=list_items)["is_overridden"]:
                            continue

                        if self.skip_invalid_nodes:
                            try:
                                rgetattr(hxd_obj, path, list_items=list_items)
                            except AttributeError:
                                break
                            
                        try:
                            rsetattr(hxd_obj, path, rgetkey(example_data, path, list_items=list_items), list_items=list_items)
                        except SetInvalidStructureNodeKeyError:
                            if self.skip_invalid_nodes: 
                                break
                            raise
                        except:
                            rsetattr(hxd_obj, path, rgetkey(example_data, path, list_items=list_items), list_items=list_items)
      
                except KeyError:
                    print(f"unable to set {hxd_obj._path}.{path} with list_items {str(list_items)} as this does not exist in example data")
        

def reset_node_outputs(hxd_obj, loader=None, data_schema_static_path="data_schema_static.py", files_path="transient_hxd_files"):
    if loader is None:
        loader = TransientHxdLoader()  # If no loader provided, create a default one (skip_invalid_nodes=False)
    
    data_schema = DataSchemaStaticParser(data_schema_static_path, files_path, loader)
    modes = data_schema.get_modes()
    sorted_paths = sorted(modes.keys())
    
    # global operation_num
    # global root_node

    output_list_nodes = []

    for path in sorted_paths:
        # Check if we've already wiped it's parent output list
        if any(path.startswith(f"{output_list_node}.") for output_list_node in output_list_nodes):
            continue

        # if "airlines.countries" in path:
        #     breakpoint()
        list_item_combinations = _get_list_length_combinations(hxd_obj, path)
        if list_item_combinations:
            for list_items in list_item_combinations:
                # operation_num += 1
                # print(f"{operation_num}: {path}") 
                # if operation_num in [19]:
                #     breakpoint()
                
                if isinstance(rgetattr(hxd_obj, path, list_items=list_items), hx_internal_StructureNode):
                    rgetattr(hxd_obj, path, list_items=list_items)._reset_outputs(modes)
                elif isinstance(rgetattr(hxd_obj, path, list_items=list_items), hx_internal_ListNode):
                    rgetattr(hxd_obj, path, list_items=list_items)._reset_outputs(modes)

                    if modes[path] == "output":
                        output_list_nodes.append(path)

        else:
            if isinstance(rgetattr(hxd_obj, path, list_items=[]), hx_internal_StructureNode):
                rgetattr(hxd_obj, path, list_items=[])._reset_outputs(modes)
            elif isinstance(rgetattr(hxd_obj, path, list_items=[]), hx_internal_ListNode):
                rgetattr(hxd_obj, path, list_items=[])._reset_outputs(modes)

                if modes[path] == "output":
                    output_list_nodes.append(path)


    hxd_obj._reset_outputs(modes)

def _new_node(value, loader, path="", default_element_count=None):
    if isinstance(value, dict):
        return hx_internal_StructureNode(value, path=path, loader=loader)
    elif isinstance(value, list):
        return hx_internal_ListNode(value, path=path, default_element_count=None, loader=loader)
    else:
        raise Exception("trying to create a new node without using a list or dict")

def get_paths_raw(data, current_path="", paths_found=[], expand_lists=False):
    if (
            isinstance(data, list) or (("hx_internal" in str(type(data))) and (dir(data) == LIST_NODE_DIR))  # list or hx/transient list
        ) and expand_lists:

        for index, item in enumerate(data):
            get_paths_raw(data[index], current_path=f"{current_path}", paths_found=paths_found, expand_lists=expand_lists)

    elif isinstance(data, dict):  # python dict
        paths_found.extend([f"{current_path}.{key}" for key in data])
        for key in data:
            get_paths_raw(data[key], current_path=f"{current_path}.{key}", paths_found=paths_found, expand_lists=expand_lists)

    elif ("hx_internal" in str(type(data))) and (dir(data) != OVERRIDE_NODE_DIR) and (dir(data) != FILE_NODE_DIR):  # hx or transient node but not list
        paths_found.extend([f"{current_path}.{key}" for key, value in data])
        for key, value in data:
            get_paths_raw(value, current_path=f"{current_path}.{key}", paths_found=paths_found, expand_lists=expand_lists)
    
    return paths_found

def get_paths(data, expand_lists=False):
    paths_found = get_paths_raw(data, paths_found=[], expand_lists=expand_lists)
    remove_leading_point = [x[1:] for x in paths_found]
    dedupe = list(set(remove_leading_point))
    return dedupe
    
def _enforce_value(value, force_type, optional, path):
    try:
        if isinstance(value, hx_internal_OverrideNode):
            value._type = force_type
            return value
        elif optional and value is None:
            return None
        elif force_type == "int":
            if isinstance(value, np.generic):
                value = value.item()
            if value == "":  # Special case allowed by hxd
                return None
            return int(value)
        elif force_type == "float":
            if isinstance(value, np.generic):
                value = value.item()
            if value == "":  # Special case allowed by hxd
                return None
            return float(value)
        elif force_type == "str":
            return str(value)
        elif force_type == "bool":
            return bool(value)
        elif force_type == "date":
            if isinstance(value, str):
                value = datetime.strptime(value, "%Y-%m-%d").date()
            elif isinstance(value, datetime):
                value = value.date()

            if isinstance(value, date):
                return value
            else:
                raise Exception(f"No available date handling for {type(value)}")
        else:
            raise Exception(f"Invalid type - {force_type}")
    except Exception as e:
        raise Exception(f"failed to assign to Node {path}, value {value} is of type {type(value)}, not {force_type}: {e}")

class hx_internal_BaseNode():
    def __init__(self, path="", loader=None):
        self.__dict__['_locked'] = False
        self.__dict__['_path'] = path
        self.__dict__['_loader'] = loader

    def keys(self):
        return self._children()

    # def __iter__(self):
    #     self._iter = 0
    #     return self

    def __getitem__(self, item):
        if not isinstance(item, str):
            raise Exception(f"{item} not a valid attribute")
        return getattr(self, item)

    def __bool__(self):
        return bool([x for x in self.__dict__.keys() if "_" != x[0]])

    def __reversed__(self, item):
        raise Exception("reversing this node type is not possible")

    def __copy__(self):  # TODO: necessary?
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj


class hx_internal_StructureNode(hx_internal_BaseNode):
    def __init__(self, contents, *args, **kwargs):
        super(hx_internal_StructureNode, self).__init__(*args, **kwargs)

        self.__dict__['_child_types'] = {}
        self.__dict__['_child_optionalities'] = {}

        if not isinstance(contents, dict):
            raise Exception("hx_internal_StructureNode contents must be dict")
        
        for key, value in contents.items():
            # Handle where further recursion is needed
            if isinstance(value, dict):
                value = _new_node(value, self._loader, path=f"{self._path}.{key}")
            elif isinstance(value, list):
                if all([isinstance(x, dict) for x in value]):
                    if value:
                        value = _new_node(value, self._loader, path=f"{self._path}.{key}")

            setattr(self, key, value)

    def _lock(self):
        self.__dict__['_locked'] = True
        for child in self._children():
            child_obj = getattr(self, child)
            if isinstance(child_obj, hx_internal_StructureNode) or isinstance(child_obj, hx_internal_ListNode):
                child_obj._lock()

    def _reset_outputs(self, modes):
        for child in self._children():
            full_path = f"{self._path}.{child}" if self._path else child

            child_obj = getattr(self, child)
            if isinstance(child_obj, hx_internal_StructureNode) or isinstance(child_obj, hx_internal_ListNode):
                child_obj._reset_outputs(modes)
                
            elif modes[full_path] == "output":
                setattr(self, child, None)

            elif modes[full_path] == "override":
                getattr(self, child).calculated = None

    def __setattr__(self, key, value):
        if "_locked" not in self.__dict__ and key == "_locked":
            self.__dict__[key] = value
        elif not self._locked:
            if isinstance(value, dict):
                self.__dict__[key] = hx_internal_StructureNode(value, path=f"{self._path}.{key}")
            elif isinstance(value, list):
                self.__dict__[key] = hx_internal_ListNode(value, path=f"{self._path}.{key}")
            elif key in self._child_types:
                self.__dict__[key] = _enforce_value(value, self._child_types[key], self._child_optionalities[key], f"{self._path}.{key}")
            else:
                self.__dict__[key] = value
        elif self._locked and key in self.__dict__:
            # if isinstance(value, dict):
            #     # print(f"skipped {self._path}.{key}")
            #     pass
            if isinstance(self.__dict__[key], hx_internal_OverrideNode) and isinstance(value, dict):
                if [x for x in value if x not in self.__dict__[key]._override_children]:  # Nodes in value that are not valid override children
                    raise Exception(f"Can't assign {str([x for x in value if x not in self.__dict__[key]._override_children])} to hx_internal_OverrideNode object at {self._path}.{key}")
                else:
                    setattr(self.__dict__[key], "calculated", value.get("calculated", None))
                    if value.get("override", None) or value.get("is_overridden", False):  # Handles if override is actually None by also checking is_overridden
                        setattr(self.__dict__[key], "override", value.get("override", None))  # If is overridden, set the override (will handle the calculated fields)
            elif isinstance(self.__dict__[key], hx_internal_OverrideNode) and (("hx_internal" in str(type(value))) and (dir(value) == OVERRIDE_NODE_DIR)):
                setattr(self.__dict__[key], "calculated", value.calculated)
                if value.override or value.is_overridden:  # Handles if override is actually None by also checking is_overridden
                    setattr(self.__dict__[key], "override", value.override)  # If is overridden, set the override (will handle the calculated fields)

            elif isinstance(self.__dict__[key], hx_internal_OverrideNode): 
                raise Exception(f"Can't assign {type(value)} directly to hx_internal_OverrideNode object at {self._path}.{key}")  
            elif isinstance(self.__dict__[key], hx_internal_ListNode) and (isinstance(value, (list, pd.Series, np.ndarray, hx_internal_ListNode)) or (("hx_internal" in str(type(value))) and (dir(value) == LIST_NODE_DIR))):  # Works for real and transient_hxd
                # Setting a list node by assigning directly - want to completely replace it
                # Start by clearing the existing list
                self.__dict__[key]._list.clear()
                
                # Then set to the right length
                self.__dict__[key]._pad_with_default(num_items=len(value))
                for index, val in enumerate(value):
                    self.__dict__[key][index] = deepcopy(val) 
            elif isinstance(self.__dict__[key], hx_internal_ListNode):
                raise Exception(f"Can't assign variable of type {type(value)} to hx_internal_ListNode ({self._path})")  # TODO: match exact error message
            elif isinstance(self.__dict__[key], hx_internal_StructureNode) and isinstance(value, dict):
                for child_key, child_value in value.items():
                    setattr(self.__dict__[key], child_key, child_value)
            elif isinstance(self.__dict__[key], hx_internal_StructureNode) and ("hx_internal" in str(type(value))):  # Works for real hxd and transient_hxd
                for child_key, child_value in value:
                    setattr(self.__dict__[key], child_key, child_value)
            elif isinstance(self.__dict__[key], hx_internal_StructureNode):
                raise Exception(f"Can't assign variable of type {type(value)} to hx_internal_StructureNode object ({self._path})")  # TODO: match exact error message
            elif isinstance(self.__dict__[key], hx_internal_FileNode):
                pass  # TODO: prevent assignment
            elif isinstance(self.__dict__[key], hx_internal_TriangleNode):
                print("writing to hx_internal_TriangleNode not yet implimented")
                pass  
            else:
                self.__dict__[key] = _enforce_value(value, self._child_types[key], self._child_optionalities[key], f"{self._path}.{key}")
        else:
            raise SetInvalidStructureNodeKeyError(key, self._path)

    def __dir__(self):
        return [key for key in self.__dict__.keys() if "_" != key[0]]

    def __len__(self):
        return len(self._children())

    def _children(self):
        return [x for x in self.__dict__.keys() if "_" != x[0]]

    def __iter__(self):
        return hx_internal_StructureNodeIterator(self)

    def _get_node_dict(self):
        keys = [x for x in self.__dict__.keys() if "_" != x[0]]
        dictionary = {x: getattr(self, x) for x in keys}
        return dictionary

    def __repr__(self):
        dictionary = self._get_node_dict()
        contents = str(dictionary)
        return contents

    def __contains__(self, item):
        return item in self._children()

class hx_internal_StructureNodeIterator:
    def __init__(self, node):
        self._node = node
        self._keys = node._children()
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._keys):
            raise StopIteration
        key = self._keys[self._index]
        value = getattr(self._node, key)
        self._index += 1
        return key, value


class hx_internal_ListNode(hx_internal_BaseNode):
    def __init__(self, contents, *args, default_element_count=None, mode="input", **kwargs):
        super(hx_internal_ListNode, self).__init__(*args, **kwargs)

        if not isinstance(contents, list):
            raise Exception("hx_internal_ListNode contents must be list")
        if not contents:
            raise Exception("hx_internal_ListNode contents cannot be empty. Use [{}] for an empty list")

        if default_element_count and len(contents) > default_element_count:
            contents = contents[0:default_element_count]
        elif default_element_count and len(contents) < default_element_count:
            contents.extend([contents[0] for x in range(len(contents), default_element_count)])

        self._list = [_new_node(x, self._loader, path=f"{self._path}") for x in contents]
        self._mode = mode

    def _lock(self):
        # Ensure there are no overlapping list children in memory
        for i in range(len(self._list)):
            self._list[i] = deepcopy(self._list[i])

        if not self._locked:
            self.__dict__['_locked'] = True
            # print(f"locking {self._path}")
            self._default_child = deepcopy(self._list[0])
            self._default_child._lock()

            if self._mode == "output":
                # print(f"clearing {self._path}")
                self._list.clear()

        for child in self._list:
            child._lock()

    def _reset_outputs(self, modes):
        if modes[self._path] == "output": # If output list, reset list length
            if len(self._list) > 0:
                self._list = self._list[:0]

        for child in self._list:  
            child._reset_outputs(modes)

    def __dir__(self):  # Match hxd. These are all valid list operations (but only a subset)
        return LIST_NODE_DIR

    def __len__(self):
        return len(self._list)

    def _children(self):
        return self._default_child._children()

    def __iter__(self):
        return hx_internal_ListNodeIterator(self._list)

    def __getitem__(self, item):
        return self._list[item]

    def __bool__(self):
        return bool(self._list)

    def __setitem__(self, loc, value):
        while loc >= len(self._list) and not self._locked:
            self._list.append(deepcopy(self._default_child))

        if loc > len(self._list):
            raise Exception(f"list index {loc} out of range (transient list of length {len(self._list)})")
        
        self._convert_value_to_transient_list(loc, value)

    def _convert_value_to_transient_list(self, loc, value):
        # Setting from a dictionary - leverage how we do this elsewhere
        if isinstance(value, dict):
            self._loader.load_from_dictionary(self._list[loc], value)
        # Setting from a real hxd object - we can actually still use the dictionary load func, but need to validate the children
        elif ("hx_internal." in str(type(value))):
            if (dir(value) == self._children()):  # Make sure valid node is being set
                self._loader.load_from_dictionary(self._list[loc], value)
            else:
                raise Exception("Invalid hxd list node children")
        # Setting from another transient_hxd object - don't need to convert anything here, just check the metadata aligns
        elif isinstance(value, hx_internal_StructureNode):
            if value._children() == self._children():  # Make sure a valid node is being set
                self._list[loc] = value
            else:
                raise Exception(f"Invalid hx_internal_StructureNode (children: {value._children()}) passed to hx_internal_ListNode (children: {self._children()})")
        # Special assignment that real hxd supports
        elif len(self._children()) == 1:
            self._list[loc] = value
        else:
            raise Exception("Can't assign scalar values to hx_internal_ListNode because list has more than 1 child")

    def __delitem__(self, i):
        del self._list[i]

    def __setattr__(self, key, value):
        if "_" == key[0]:
            self.__dict__[key] = value
        elif not self._locked:
            [setattr(x, key, deepcopy(value)) for x in self._list]
        else:
            [setattr(x, key, deepcopy(value)) for x in self._list]

    def _pad_with_default(self, num_items=1):
        for i in range(num_items):
            self._list.append(deepcopy(self._default_child))

    def __repr__(self):
        contents = str(self._list)
        return contents

    def __reversed__(self):
        return reversed(self._list)

    def __contains__(self, item):
        return item in self._list

    def __iadd__(self, item):
        self._list += item

    def append(self, *args, **kwargs):
        self._list.append(deepcopy(self._default_child))
        
        self._convert_value_to_transient_list(-1, args[0])

    def count(self, *args, **kwargs):
        self._list.count(*args, **kwargs)

    def extend(self, *args, **kwargs):
        for item in args[0]:
            self.append(item)

    def index(self, *args, **kwargs):
        self._list.index(*args, **kwargs)

    def insert(self, *args, **kwargs):
        self._list.insert(*args, **kwargs)

    def remove(self, *args, **kwargs):
        self._list.remove(*args, **kwargs)


class hx_internal_ListNodeIterator:
    def __init__(self, node_list):
        self._list = node_list
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._list):
            raise StopIteration
        value = self._list[self._index]
        self._index += 1
        return value



class hx_internal_OverrideNode(hx_internal_BaseNode):
    _override_children = ["calculated", "is_dirty", "overridden_calculated", "override", "selected", "is_overridden"]
    _protected_override_children = ["is_dirty", "overridden_calculated", "selected", "is_overridden"]

    def __init__(self, *args, **kwargs):
        super(hx_internal_OverrideNode, self).__init__(*args, **kwargs)

        self._type = None

        # User inputs
        self.calculated = None
        self.override = None

        # Controlled values
        self.overridden_calculated = None
        self.is_overridden = None

    def _lock(self):
        self.__dict__['_locked'] = True

    @property
    def selected(self):
        if self.is_overridden:
            return self.override
        else:
            return self.calculated

    @property
    def is_dirty(self):
        if not self.is_overridden:
            return None  # TODO: check this behaviour
        elif self.calculated == self.overridden_calculated:
            return False
        else:
            return True

    def __dir__(self):
        # Match hxd. Unclear why it's not _override_children but doesn't seem to be
        return OVERRIDE_NODE_DIR

    def __len__(self):
        raise Exception("override node doesn't have len implemented")

    def _children(self):
        return self._override_children

    def __iter__(self):
        return hx_internal_OverrideNodeIterator(self)

    def __repr__(self):
        calculated_keys = ["selected", "is_overridden"]
        static_keys = [x for x in [y for y in self._override_children if y not in calculated_keys]]

        dictionary = {x: getattr(self, x) for x in static_keys}
        dictionary["selected"] = self.selected
        dictionary["is_overridden"] = self.is_overridden

        contents = str(dictionary)
        return contents

    def __setattr__(self, key, value):
        if "_" == key[0] and key != "_type":
            self.__dict__[key] = value
        elif key == "_type":
            if not self._locked:
                self.__dict__[key] = value
            else:
                raise Exception("trying to change type of a locked OverrideNode")
        elif key == "override":  # This can't usually be set to, but transient allows it for arbitrary paths so handle the same as if a user has set it in UI
            self.__dict__[key] = _enforce_value(value, self._type, True, self._path)
            if self._locked:
                self.__dict__["overridden_calculated"] = self.calculated
                self.__dict__["is_overridden"] = True
        elif key == "calculated":
            self.__dict__[key] = _enforce_value(value, self._type, True, self._path)
        elif key in self._override_children:  
            # ["is_dirty", "selected"] - always calculated 
            # ["overridden_calculated", "is_overridden"] - set while setting to override
            if not self._locked:
                self.__dict__[key] = value
            else:
                raise Exception(f"Can't write to {key} in an Override Node")
        else:
            raise Exception(f"Invalid Key {key} for Override Node")

class hx_internal_OverrideNodeIterator:
    def __init__(self, node):
        self._node = node
        self._keys = node._children()
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._keys):
            raise StopIteration
        key = self._keys[self._index]
        value = getattr(self._node, key)
        self._index += 1
        return key, value


class hx_internal_FileNode(hx_internal_BaseNode):
    _file_children = ["exists", "file_name", "file_size", "file_extension", "created_at", "created_by_user_id"]
    # TODO: work out if regular hxd actually supports created_at and created_by_user_id

    def __init__(self, files_path, mode, *args, **kwargs): 
        super(hx_internal_FileNode, self).__init__(*args, **kwargs)

        self._mode = mode

        if os.path.isdir(files_path):
            self._files_path = files_path
        else:
            print(f"WARNING: FileNode initialised but transient_hxd was not able to find {files_path}")
            self._files_path = None

    def __dir__(self):
        return FILE_NODE_DIR

    def __len__(self):
        raise Exception("file node doesn't have len implemented")

    def _children(self):
        return self._file_children  # TODO: Test

    def __next__(self):
        raise Exception("file node doesn't have next implemented")

    def __repr__(self):
        dictionary = {x: getattr(self, x) for x in self._file_children}
        contents = str(dictionary)
        return contents

    # TODO: This is only approximate. Check actual behaviour for reading and writing
    def open(self, mode="t"):
        input_or_output = self._mode

        if (input_or_output == "input") and (mode == "t"):
            open_mode = "r"
        elif (input_or_output == "input") and (mode == "b"):
            open_mode = "rb"
        elif (input_or_output == "output") and (mode == "t"):
            open_mode = "r+"
        elif (input_or_output == "output") and (mode == "b"):
            open_mode = "rb+"
        # if mode == "t":
        #     open_mode = "r+"
        # elif mode == "b":
        #     open_mode = "rb+"
        else:
            raise Exception(f"Invalid open mode: input_or_output is {input_or_output} and mode is {mode}")
            # raise Exception(f"Invalid open mode: mode is {mode} but must be either 't' or 'b'")

        f = open(f"{self._files_path}/{self.file_name}", open_mode)
        return f

    @property
    def exists(self):
        if self._files_path:
            converted_path = self._path.replace(".", "-")
            files = os.listdir(self._files_path)
            filtered_files = [x for x in files if os.path.splitext(x)[0] == converted_path]
            return bool(len(filtered_files))
        else:
            return False

    # TODO: This is only approximate. Check actual output
    @property
    def file_name(self):
        converted_path = self._path.replace(".", "-")
        if self._files_path:
            files = os.listdir(self._files_path)
            filtered_files = [x for x in files if os.path.splitext(x)[0] == converted_path]
            if len(filtered_files) > 0:
                return filtered_files[0]
        return converted_path


    # TODO: This is only approximate. Check actual output
    @property
    def file_size(self):
        if self._files_path:
            return os.stat(f"{self._files_path}/{self.file_name}").st_size
        else:
            return 0
        
    # TODO: This is only approximate. Check actual output
    @property
    def file_extension(self):
        return self.file_name.split(".")[-1]

    @property
    def created_at(self):
        if self._files_path:
            return os.stat(f"{self._files_path}/{self.file_name}").st_mtime  # NB: Actually gets time last modified
        else:
            return 0

    @property
    def created_by_user_id(self):
        if self._files_path:
            return os.stat(f"{self._files_path}/{self.file_name}").st_uid
        else:
            return ""

    def __setattr__(self, key, value):
        if "_" == key[0]:
            self.__dict__[key] = value
        elif key in self._file_children:
            self.__dict__[key] = value
        else:
            print(f"Skipping key {key} for hx_internal_FileNode")
            # raise Exception(f"Invalid Key {key} for File Node")


class hx_internal_TriangleBaseObj():
    def __init__(self):
        self.__dict__['_locked'] = False

    def _lock(self):
        self.__dict__['_locked'] = True

    def _reset_outputs(self, modes):
        pass

    def __setattr__(self, key, value):
        if "_locked" not in self.__dict__ and key == "_locked":
            self.__dict__[key] = value
        elif not self._locked:
            self.__dict__[key] = value
        else:
            print(f"hx_internal_TriangleBaseObj not implimented - skipping setting {key}")
            pass

class hx_internal_TriangleOptions(hx_internal_TriangleBaseObj):
    def __init__(self):
        super(hx_internal_TriangleOptions, self).__init__()
        self.n_wtd_avg = hx_internal_TriangleAveragesOptions()
        self.simple = hx_internal_TriangleAveragesOptions()
        self.wtd_avg = hx_internal_TriangleAveragesOptions()
        
        self._lock()

class hx_internal_TriangleAveragesOptions(hx_internal_TriangleBaseObj):
    def __init__(self):
        super(hx_internal_TriangleAveragesOptions, self).__init__()
        self.average_type = ""
        self.last_n_origin_periods = None
        self.latest_diagonal = ""
        
        self._lock()

class hx_internal_TriangleCount(hx_internal_TriangleBaseObj):
    def __init__(self):
        super(hx_internal_TriangleCount, self).__init__()
        self.count = None
        self.index = None
        
        self._lock()

class hx_internal_TriangleDimensions(hx_internal_TriangleBaseObj):
    def __init__(self):
        super(hx_internal_TriangleDimensions, self).__init__()
        self.height = None
        self.width = None
        
        self._lock()

class hx_internal_TrianglePeriod(hx_internal_TriangleBaseObj):
    def __init__(self):
        super(hx_internal_TrianglePeriod, self).__init__()
        self.as_integer_ratio = None
        self.bit_length = None
        self.conjugate = None
        self.denominator = None
        self.from_bytes = None
        self.imag = None
        self.numerator = None
        self.real = None
        self.to_bytes = None
        
        self._lock()

class hx_internal_TriangleIDFTableAdjustments(hx_internal_TriangleBaseObj):
    def __init__(self):
        super(hx_internal_TriangleIDFTableAdjustments, self).__init__()
        self.exclusions = None
        
        self._lock()

class hx_internal_TriangleSelectedAverageOption(hx_internal_TriangleBaseObj):
    def __init__(self):
        super(hx_internal_TriangleSelectedAverageOption, self).__init__()
        self.capitalize = None
        self.casefold = None
        self.center = None
        self.count = None
        self.encode = None
        self.endswith = None
        self.expandtabs = None
        self.find = None
        self.format = None
        self.format_map = None
        self.index = None
        self.isalnum = None
        self.isalpha = None
        self.isascii = None
        self.isdecimal = None
        self.isdigit = None
        self.isidentifier = None
        self.islower = None
        self.isnumeric = None
        self.isprintable = None
        self.isspace = None
        self.istitle = None
        self.isupper = None
        self.join = None
        self.ljust = None
        self.lower = None
        self.lstrip = None
        self.maketrans = None
        self.partition = None
        self.removeprefix = None
        self.removesuffix = None
        self.replace = None
        self.rfind = None
        self.rindex = None
        self.rjust = None
        self.rpartition = None
        self.rsplit = None
        self.rstrip = None
        self.split = None
        self.splitlines = None
        self.startswith = None
        self.strip = None
        self.swapcase = None
        self.title = None
        self.translate = None
        self.upper = None
        self.zfill = None
        
        self._lock()

class hx_internal_TriangleTailFactor(hx_internal_TriangleBaseObj):
    def __init__(self):
        super(hx_internal_TriangleTailFactor, self).__init__()
        self.as_integer_ratio = None
        self.conjugate = None
        self.fromhex = None
        self.hex = None
        self.imag = None
        self.is_integer = None
        self.real = None
        
        self._lock()


# TODO: Placeholder. Implement
class hx_internal_TriangleNode(hx_internal_BaseNode):
    _triangle_children_children = {
        'averages_options': hx_internal_TriangleOptions(), 
        'cdfs_calculated': hx_internal_TriangleCount(), 
        'cdfs_calculated_options': hx_internal_TriangleOptions(), 
        'cdfs_selected': hx_internal_TriangleCount(),
        'cumulative_data': hx_internal_TriangleDimensions(),
        'dev_period_count': hx_internal_TrianglePeriod(), 
        'dev_period_increment': hx_internal_TrianglePeriod(), 
        'dev_periods': hx_internal_TriangleCount(),
        'first_dev_period': hx_internal_TrianglePeriod(),
        'idf_overrides': hx_internal_TriangleCount(),
        'idf_table_adjustments': hx_internal_TriangleIDFTableAdjustments(),
        'idf_table_calculated': hx_internal_TriangleDimensions(),
        'idf_table_selected': hx_internal_TriangleDimensions(),
        'idfs_calculated': hx_internal_TriangleCount(),
        'idfs_calculated_options': hx_internal_TriangleOptions(),
        'idfs_selected': hx_internal_TriangleCount(),
        'incremental_data': hx_internal_TriangleDimensions(),
        'most_recent_cumulative_values': hx_internal_TriangleCount(),
        'most_recent_dev_period_indexes': hx_internal_TriangleCount(),
        'origin_period_count': hx_internal_TrianglePeriod(),
        'origin_periods': hx_internal_TriangleCount(),
        'pcts_developed_calculated': hx_internal_TriangleCount(),
        'pcts_developed_calculated_options': hx_internal_TriangleOptions(),
        'pcts_developed_selected': hx_internal_TriangleCount(),
        'projected_cumulative_data': hx_internal_TriangleDimensions(),
        'selected_average_option': hx_internal_TriangleSelectedAverageOption(),
        'tail_factor': hx_internal_TriangleTailFactor(),
        'ultimate_cumulative_values': hx_internal_TriangleCount() 
    }
    def __init__(self, *args, **kwargs):
        self.__dict__['_locked'] = False

        super(hx_internal_TriangleNode, self).__init__(*args, **kwargs)

        for child in self._triangle_children_children:
            setattr(self, child, self._triangle_children_children[child])

        self._lock()

    def _lock(self):
        self.__dict__['_locked'] = True

    def _reset_outputs(self, modes):
        pass

    def __setattr__(self, key, value):
        if "_locked" not in self.__dict__ and key == "_locked":
            self.__dict__[key] = value
        elif not self._locked:
            self.__dict__[key] = value
        else:
            print(f"hx_internal_TriangleNode not implimented - skipping setting {key}")
            pass

    # def __dir__(self):
    #     return []

    # def __len__(self):
    #     return 0

    # def __next__(self):
    #     pass

    # def __repr__(self):
    #     return ""

    # def __contains__(self):
    #     pass # cdfs_calculated

    # def __getitem__(self):
    #     pass # cdfs_calculated
 
    # def __iter__(self):
    #     pass # cdfs_calculated

    # def __reversed__(self):
    #     pass # cdfs_calculated



class DataSchemaStaticParser:
    def __init__(self, data_schema_path, files_path, loader):
        self.__defaults = {}
        self.__modes = {}
        self.__types = {}
        self.__optionalities = {}

        self.__inputs = []
        self.__outputs = []
        self.__overrides = []

        self.__async_outputs = {}
        
        self.__module_name = "data_schema_static"
        self.__data_schema_static_path = data_schema_path
        self.__files_path = files_path
        self.__loader = loader
        self.__remove_string = """raise Exception(\"""This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your Data Schema that will allow easier debugging.
\""")"""

        if os.path.exists(self.__data_schema_static_path):
            spec = importlib.util.spec_from_file_location(self.__module_name, self.__data_schema_static_path)
            if spec is None:
                raise ImportError(f"Could not load spec for module '{self.__module_name}' at: {self.__data_schema_static_path}")

            source = spec.loader.get_source(self.__module_name)
            new_source = source.replace(self.__remove_string, "")

            module = importlib.util.module_from_spec(spec)

            codeobj = compile(new_source, module.__spec__.origin, 'exec')
            exec(codeobj, module.__dict__)
            sys.modules[self.__module_name] = module
            
            data_schema_module_name = [name for name in dir(module) if not (name.startswith('__') and name.endswith('__')) and (name != "hx")][0]
            self.__data_schema_static_module = getattr(module, data_schema_module_name)()

            self.__recurssive_fetch("", self.__data_schema_static_module, "default")

            self._found_data_schema_static = True

        else:
            self._found_data_schema_static = False

            raise FileNotFoundError(f"Couldn't find data schema at {self.__data_schema_static_path}")

    def get_defaults(self):
        return self.__defaults

    def get_inputs(self):
        return self.__inputs

    def get_outputs(self):
        return self.__outputs

    def get_overrides(self):
        return self.__overrides

    def get_modes(self):
        return self.__modes

    def get_types(self):
        return self.__types
        
    def get_optionalities(self):
        return self.__optionalities

    def get_async_outputs(self):
        return self.__async_outputs

    def get_paths(self):
        return self.__defaults.keys()

    def get_list_paths(self):
        return [x for x in self.__defaults if isinstance(self.__defaults[x], hx_internal_ListNode)]

    def get_children(self, path):
        short_path = path[4:]
        full_paths = [k for k in self.__defaults if short_path in k]
        path_len = len(short_path) + 1 if path != "hxd" else 0
        full_child_paths = [x[path_len:] for x in full_paths]
        split_paths = [x.split(".") for x in full_child_paths if len(x) > 1]
        child_paths = [x[0] for x in split_paths]
        deduped_child_paths = list(set(child_paths))
        return deduped_child_paths

    def __recurssive_fetch(self, parent_path, parent_node, fetch):
        for child_path in parent_node.children:
            # global operation_num
            # operation_num += 1
            # print(f"{operation_num}") 
            # if operation_num in [6006]:
            #     breakpoint()
            if parent_path == "":
                path = child_path
            else:
                path = parent_path + '.' + child_path

            child = parent_node.children[child_path]

            if child.type == "structure":
                default_val = hx_internal_StructureNode({}, path=path, loader=self.__loader)
                mode = None
                self.__recurssive_fetch(path, child, fetch)
            elif child.type == "list":
                if isinstance(parent_node.children[child_path].default_element_count, int):
                    default_element_count = parent_node.children[child_path].default_element_count
                else:
                    default_element_count = None

                default_val = hx_internal_ListNode([{}], path=path, default_element_count=default_element_count, mode=child.__getattribute__("mode"), loader=self.__loader)

                mode = child.__getattribute__("mode")
                self.__recurssive_fetch(path, child, fetch)
            elif child.type == "file":
                mode = child.__getattribute__("mode")
                default_val = hx_internal_FileNode(self.__files_path, mode, path=path, loader=self.__loader)
            elif child.type == "triangle":
                default_val = hx_internal_TriangleNode(path=path, loader=self.__loader)
                mode = child.__getattribute__("mode")
            else:
                mode = child.__getattribute__("mode")
                if mode == "input":
                    if not isinstance(child.__getattribute__("default"), Undefined):
                        default_val = child.__getattribute__("default")
                    elif not isinstance(child.__getattribute__("options"), Undefined):
                        options = child.__getattribute__("options")
                        default_val = options[child.__getattribute__("default_index")]
                    elif not isinstance(child.__getattribute__("options_table"), Undefined):
                        param_df = getattr(hx.params, child.__getattribute__("options_table"))
                        options = list(param_df[child.__getattribute__("options_column")])
                        default_val = options[child.__getattribute__("default_index")]
                    elif not isinstance(parent_node.__getattribute__("linked_options_table"), Undefined):
                        param_df = getattr(hx.params, parent_node.__getattribute__("linked_options_table"))

                        options_cols = parent_node.__getattribute__("linked_options_columns")
                        matching_children = [x for x in parent_node.children]
                        col_index = matching_children.index(child_path)
                        option_col = options_cols[col_index]

                        options = list(param_df[option_col])
                        default_val = options[parent_node.__getattribute__("linked_default_index")]
                    elif not isinstance(parent_node.__getattribute__("linked_options_data"), Undefined) and child.__getattribute__("optionality"):
                        default_val = None
                    else:
                        raise Exception(f"default not found for {path}. Please check the data schema static copy is up to date")
                    self.__inputs.append(path)
                elif mode == "override":
                    default_val = hx_internal_OverrideNode(path=path, loader=self.__loader)
                    self.__overrides.append(path)
                else:
                    default_val = None
                    self.__outputs.append(path)

                if not isinstance(child.__getattribute__("async_output"), Undefined):
                    async_outputs = child.__getattribute__("async_output")
                    if async_outputs is None:  # None is a valid input - handle by doing nothing
                        pass
                    elif isinstance(async_outputs, str):  # A single string rather than a list is a valid input - handle by making it a list
                        self.__async_outputs.setdefault(async_outputs, []).append(path)
                    elif isinstance(async_outputs, dict):  # A single string rather than a list is a valid input - handle by making it a list
                        self.__async_outputs.setdefault(async_outputs["task"], []).append(path)
                    else:
                        for task in child.__getattribute__("async_output"):
                            if isinstance(task, dict):
                                self.__async_outputs.setdefault(task["task"], []).append(path)
                            else:
                                self.__async_outputs.setdefault(task, []).append(path)
                            

                if isinstance(default_val, str):
                    if default_val.__contains__("Undefined"):
                        default_val = 'default_index=' + str(child.__getattribute__("default_index"))
            
            self.__defaults[path] = default_val
            self.__modes[path] = mode
            self.__types[path] = child.type

            if child.type in ["structure", "list", "file", "triangle"]:
                self.__optionalities[path] = None  # These node types don't have optionality as a property
            elif mode in ["output", "override"]:
                self.__optionalities[path] = True
            else:
                self.__optionalities[path] = child.optionality == "optional"



class DummyProgress:
    def update(*args, **kwargs):
        pass


def rsetattr(obj, attr, val, splitter=".", list_items=[0]):
    list_items = _validate_list_items(list_items)

    pre, _, post = attr.rpartition(splitter)
    try:
        hxd_obj = rgetattr(obj, pre, splitter=splitter, list_items=list_items) if pre else obj

        if dir(hxd_obj) == LIST_NODE_DIR:
            return setattr(hxd_obj[list_items[-1]], post, val)
        else:
            return setattr(hxd_obj, post, val)
    except AttributeError as a:
        print(f"can't set attribute - {attr} to {str(val)}")
        setattr(hxd_obj, post, val)

def _rgetattr(obj, attr, list_items, get_missing_indexes_from=None):
    list_items = _validate_list_items(list_items)
        
    # Check for list in offline/real hxd agnostic way
    if dir(obj) == LIST_NODE_DIR and len(list_items) > 0:
        list_item = list_items[0]
        list_items = list_items[1:]
        if get_missing_indexes_from is not None and len(obj) <= list_item:
            return getattr(get_missing_indexes_from._default_child, attr), list_items
        else:
            return getattr(obj[list_item], attr), list_items
    elif dir(obj) == LIST_NODE_DIR and len(list_items) == 0:
        # breakpoint()
        # a=1
        raise Exception("trying to access a list with no list_items")
        # return None, list_items
    else:
        return getattr(obj, attr), list_items

def rgetattr(obj, attr, splitter=".", list_items=[], get_missing_indexes_from=None):
    list_items = _validate_list_items(list_items)

    attrs = attr.split(splitter)
    for a in attrs:
        obj, list_items_new = _rgetattr(obj, a, list_items, get_missing_indexes_from=get_missing_indexes_from)
        if get_missing_indexes_from is not None:
            get_missing_indexes_from, _ = _rgetattr(get_missing_indexes_from, a, list_items)

        list_items = list_items_new  # Need to assign here as list_items is needed unmodified for both _rgetattr statements
    return obj
    # func = functools.partial(_rgetattr, list_items=list_items)
    # return functools.reduce(func, [obj] + attr.split(splitter))

def _rgetkey(obj, key, list_items):
    list_items = _validate_list_items(list_items)

    # Check for list in offline/real hxd agnostic way
    if dir(obj) == LIST_NODE_DIR or isinstance(obj, list):
        list_item = list_items[0]
        list_items = list_items[1:]
        return obj[list_item][key], list_items
    else:
        # comment IH
        # return obj[key], list_items
        # EDIT IH
        if isinstance(obj[key], hx_internal_TriangleNode):
            pass
        else:
            return obj[key], list_items
        
        

def rgetkey(obj, key, splitter=".", list_items=[]):
    list_items = _validate_list_items(list_items)

    keys = key.split(splitter)
    for k in keys:
        # comment
        # obj, list_items = _rgetkey(obj, k, list_items)
        # edit IH
        if isinstance(obj[key], hx_internal_TriangleNode):
            pass
        else:
            obj, list_items = _rgetkey(obj, k, list_items)
    return obj

    # func = functools.partial(_rgetkey, list_items=list_item)
    # return functools.reduce(func, [obj] + key.split(splitter))

def _get_list_length_combinations(obj, path, splitter="."):
    # global operation_num
    lists = None
    for i in range(len(path.split(splitter))):
        # operation_num += 1
        # print(f"{operation_num}: {'none'}") 
        # if operation_num in [113]:
        #     breakpoint()
        sub_path = splitter.join(path.split(splitter)[:i])
        if lists is None:
            lists_to_add = _list_length(obj, sub_path, [])
            if lists_to_add is not None:
                lists = [[x] for x in lists_to_add]
        else:
            lists_to_add = []
            new_lists = []
            for combination_list in lists:
                lists_to_add = _list_length(obj, sub_path, combination_list)
                if lists_to_add is not None:
                    new_lists.extend([combination_list + [x] for x in lists_to_add])

            if new_lists:
                lists = new_lists

    return lists or []

def _list_length(obj, path, list_items, splitter="."):
    if path == "":
        return None
    else:
        if dir(rgetattr(obj, path, list_items=list_items, splitter=splitter)) == LIST_NODE_DIR:
            return list(range(len(rgetattr(obj, path, list_items=list_items, splitter=splitter))))
        else:
            return None

def _validate_list_items(list_items):
    if not isinstance(list_items, list):
        list_items = [list_items]
    # if list_items == []:
    #     list_items = [0]

    return list_items


class SetInvalidStructureNodeKeyError(Exception):
    """Raised when an invalid key is used in a StructureNode"""
    def __init__(self, key, path):
        super().__init__(f"Invalid Key '{key}' in StructureNode ({path})")