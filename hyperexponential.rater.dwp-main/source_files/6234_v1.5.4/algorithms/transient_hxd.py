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


from datetime import datetime
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

# operation_num = 0
# global_root_node = None

def init_transient_hxd(example_data=None, data_schema_static_path=None):
    if not data_schema_static_path:    
        data_schema_static_filename = "data_schema_static.py"
        data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

    data_schema = DataSchemaStaticParser(data_schema_path=data_schema_static_path)
    defaults = data_schema.get_defaults()
    sorted_paths = sorted(defaults.keys())

    root_hxd_node = _new_node({})

    # global global_root_node
    # global_root_node = root_hxd_node

    # Set up defaults
    for path in sorted_paths:
        list_item_combinations = _get_list_length_combinations(root_hxd_node, path)
        for list_items in list_item_combinations:
            rsetattr(root_hxd_node, path, defaults[path], list_items=list_items)

    sorted_paths.reverse()

    # Lock all nodes
    for path in sorted_paths:
        list_item_combinations = _get_list_length_combinations(root_hxd_node, path)
        for list_items in list_item_combinations:
            if isinstance(rgetattr(root_hxd_node, path, list_items=list_items), hx_internal_StructureNode):
                rgetattr(root_hxd_node, path, list_items=list_items)._lock()
            elif isinstance(rgetattr(root_hxd_node, path, list_items=list_items), hx_internal_ListNode):
                rgetattr(root_hxd_node, path, list_items=list_items)._lock()
    root_hxd_node._lock()

    # Populate nodes with example data
    if example_data:
        load_from_example_data(root_hxd_node, example_data, initial_load=True)

    return root_hxd_node

def load_from_example_data(hxd_obj, example_data, initial_load=False):
    example_data_paths = get_paths(example_data, expand_lists=True)
    example_data_paths = sorted(example_data_paths)

    # global operation_num
    # global root_node
    for path in example_data_paths:
        list_item_combinations = _get_list_length_combinations(hxd_obj, path)
        for list_items in list_item_combinations:
            # operation_num += 1
            # if operation_num in [1]:
            #     breakpoint()
            # print(f"{operation_num}: {'none'}") 
            if initial_load and isinstance(rgetattr(hxd_obj, path, list_items=list_items), hx_internal_OverrideNode):
                pass
                # print(f"skipping assignment of {rgetkey(example_data, path, list_items=list_items)} to {path} because it is a direct assignment to an hx_internal_OverrideNode")
            # elif initial_load and isinstance(rgetkey(example_data, path, list_items=list_items), dict) and len([x for x in example_data_paths if path in x and x != path]):
            #     print(f"skipping direct assignment to {path} as its children are directly assigned to")
            else:
                try:  # TODO: implement rcheckkey instead of relying on try except
                    rsetattr(hxd_obj, path, rgetkey(example_data, path, list_items=list_items), list_items=list_items)
                except KeyError:
                    print(f"unable to set {hxd_obj._path}.{path} with list_items {str(list_items)} as this does not exist in example data")
                # except:
                #     breakpoint()
                #     rsetattr(hxd_obj, path, rgetkey(example_data, path, list_items=list_items), list_items=list_items)

def _new_node(value, path="", default_element_count=None):
    if isinstance(value, dict):
        return hx_internal_StructureNode(value, path=path)
    elif isinstance(value, list):
        return hx_internal_ListNode(value, path=path, default_element_count=None)
    else:
        raise Exception("trying to create a new node without using a list or dict")

def get_paths_raw(data, current_path="", paths_found=[], expand_lists=False):
    if isinstance(data, dict):
        paths_found.extend([f"{current_path}.{key}" for key in data])
        for key in data:
            get_paths_raw(data[key], current_path=f"{current_path}.{key}", paths_found=paths_found, expand_lists=expand_lists)
    elif isinstance(data, list) and expand_lists:
        for index, item in enumerate(data):
            get_paths_raw(data[index], current_path=f"{current_path}", paths_found=paths_found, expand_lists=expand_lists)

    return paths_found

def get_paths(data, expand_lists=False):
    paths_found = get_paths_raw(data, paths_found=[], expand_lists=expand_lists)
    remove_leading_point = [x[1:] for x in paths_found]
    dedupe = list(set(remove_leading_point))
    return dedupe
    
def _clean_value(value):
    # Check if string should be interpreted as a date
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            pass

    # Convert Decimals to floats
    if isinstance(value, decimal.Decimal):
        value = float(value)

    if isinstance(value, np.generic):
        value = value.item()

    return value

class hx_internal_BaseNode():
    def __init__(self, path=""):
        self._locked = False
        self._path = path

    def keys(self):
        return self._children()

    def __iter__(self):
        self._iter = 0
        return self

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

        if not isinstance(contents, dict):
            raise Exception("hx_internal_StructureNode contents must be dict")
        
        for key, value in contents.items():
            # Handle where further recursion is needed
            if isinstance(value, dict):
                value = _new_node(value, path=f"{self._path}.{key}")
            elif isinstance(value, list):
                if all([isinstance(x, dict) for x in value]):
                    if value:
                        value = _new_node(value, path=f"{self._path}.{key}")

            setattr(self, key, value)

    def _lock(self):
        self._locked = True
        for child in self._children():
            child_obj = getattr(self, child)
            if isinstance(child_obj, hx_internal_StructureNode) or isinstance(child_obj, hx_internal_ListNode):
                child_obj._lock()

    def __setattr__(self, key, value):
        if key == "_iter":
            self.__dict__[key] = value
        elif "_locked" not in self.__dict__ and key == "_locked":
            self.__dict__[key] = value
        elif not self._locked:
            if isinstance(value, dict):
                self.__dict__[key] = hx_internal_StructureNode(value, path=f"{self._path}.{key}")
            elif isinstance(value, list):
                self.__dict__[key] = hx_internal_ListNode(value, path=f"{self._path}.{key}")
            else:
                self.__dict__[key] = _clean_value(value)
        elif self._locked and key in self.__dict__:
            # if isinstance(value, dict):
            #     # print(f"skipped {self._path}.{key}")
            #     pass
            if isinstance(self.__dict__[key], hx_internal_OverrideNode) and isinstance(value, dict):
                if not len(value):
                    pass
                elif [x for x in value if x not in self.__dict__[key]._override_children]:  # Nodes in value that are not valid override children
                    raise Exception(f"Can't assign {str([x for x in value if x not in self.__dict__[key]._override_children])} to hx_internal_OverrideNode object at {self._path}.{key}")
                else:
                    for x in value:
                        setattr(self.__dict__[key], x, value[x])
            elif isinstance(self.__dict__[key], hx_internal_OverrideNode): 
                raise Exception(f"Can't assign {type(value)} directly to hx_internal_OverrideNode object at {self._path}.{key}")  
            elif isinstance(self.__dict__[key], hx_internal_ListNode) and (isinstance(value, list) or isinstance(value, pd.Series) or isinstance(value, np.ndarray) or (("hx_internal." in str(type(value))) and (dir(value) == LIST_NODE_DIR))):
                # Setting a list node by assigning directly - want to completely replace it
                # Start by clearing the existing list
                self.__dict__[key]._list.clear()
                
                # Then set to the right length
                self.__dict__[key]._pad_with_default(num_items=len(value))
                for index, val in enumerate(value):
                    self.__dict__[key][index] = deepcopy(val) 
            elif isinstance(self.__dict__[key], hx_internal_ListNode):
                raise Exception("Can only assign list to a hx_internal_ListNode")  # TODO: match exact error message
            elif isinstance(self.__dict__[key], hx_internal_StructureNode) and isinstance(value, dict):
                for child_key, child_value in value.items():
                    setattr(self.__dict__[key], child_key, child_value)
            elif isinstance(self.__dict__[key], hx_internal_StructureNode) and ("hx_internal." in str(type(value))):
                for child_key, child_value in value:
                    setattr(self.__dict__[key], child_key, child_value)
            elif isinstance(self.__dict__[key], hx_internal_StructureNode):
                raise Exception(f"Can't assign variable of type {type(value)} to hx_internal_StructureNode object")  # TODO: match exact error message
            elif isinstance(self.__dict__[key], hx_internal_FileNode):
                pass  # TODO: prevent assignment
            elif isinstance(self.__dict__[key], hx_internal_TriangleNode):
                print("writing to hx_internal_TriangleNode not yet implimented")
                pass  
            else:
                self.__dict__[key] = _clean_value(value)
        else:
            raise Exception(f"Invalid Key - {key}")

    def __dir__(self):
        return [key for key in self.__dict__.keys() if "_" != key[0]]

    def __len__(self):
        return len(self._children())

    def _children(self):
        return [x for x in self.__dict__.keys() if "_" != x[0]]

    def __next__(self):
        if self._iter < self.__len__():
            i = self._children()[self._iter]
            val = self.__dict__[i]
            self._iter += 1

            return i, val
        else:
            raise StopIteration

    def __repr__(self):
        keys = [x for x in self.__dict__.keys() if "_" != x[0]]
        dictionary = {x: getattr(self, x) for x in keys}
        contents = str(dictionary)
        return contents


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

        self._list = [_new_node(x, path=f"{self._path}") for x in contents]
        self._mode = mode

    def _lock(self):
        # Ensure there are no overlapping list children in memory
        for i in range(len(self._list)):
            self._list[i] = deepcopy(self._list[i])

        if not self._locked:
            self._locked = True
            # print(f"locking {self._path}")
            self._default_child = deepcopy(self._list[0])
            self._default_child._lock()

            if self._mode == "output":
                # print(f"clearing {self._path}")
                self._list.clear()

        for child in self._list:
            child._lock()

    def __dir__(self):  # Match hxd. These are all valid list operations (but only a subset)
        return LIST_NODE_DIR

    def __len__(self):
        return len(self._list)

    def _children(self):
        return self._default_child._children()

    def __next__(self):
        if self._iter < self.__len__():
            val = self._list[self._iter]
            self._iter += 1
            
            return val
        else:
            raise StopIteration

    def __getitem__(self, item):
        return self._list[item]

        #(isinstance(value, list) or (("hx_internal." in str(type(value))) and (dir(value) == LIST_NODE_DIR)))

    def __setitem__(self, loc, value):
        while loc >= len(self._list):
            self._list.append(deepcopy(self._default_child))
        
        if isinstance(value, dict):
            load_from_example_data(self._list[loc], value)
        elif ("hx_internal." in str(type(value))) and (dir(value) == self._children()):  # Make sure valid node is being set
            load_from_example_data(self._list[loc], value)
        elif ("hx_internal." in str(type(value))):
            raise Exception("Invalid hxd list node children")
        elif isinstance(value, hx_internal_StructureNode):
            if (value._path == self._path) and (value._children() == self._children()):  # Make sure a valid node is being set
                self._list[loc] = value
            else:
                raise Exception("Invalid hx_internal_StructureNode passed to hx_internal_ListNode")
        elif len(self._children()) == 1:
            self._list[loc] = value
        else:
            raise Exception("Can't assign scalar values to hx_internal_ListNode because list has more than 1 child")

    def __delitem__(self, value):
        self._list.remove(value)

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
        self._list.append(*args, **kwargs)  # TODO: make sure this does what it normally would

    def count(self, *args, **kwargs):
        self._list.count(*args, **kwargs)

    def extend(self, *args, **kwargs):
        self._list.extend(*args, **kwargs)

    def index(self, *args, **kwargs):
        self._list.index(*args, **kwargs)

    def insert(self, *args, **kwargs):
        self._list.insert(*args, **kwargs)

    def remove(self, *args, **kwargs):
        self._list.remove(*args, **kwargs)



class hx_internal_OverrideNode(hx_internal_BaseNode):
    _override_children = ["calculated", "is_dirty", "overridden_calculated", "override", "selected", "is_overridden"]

    def __init__(self, *args, **kwargs):
        super(hx_internal_OverrideNode, self).__init__(*args, **kwargs)

        self.calculated = None
        self.is_dirty = None
        self.overridden_calculated = None
        self.override = None

    @property
    def selected(self):
        if self.override is not None:
            return self.override
        else:
            return self.calculated

    @property
    def is_overridden(self):
        if self.override:
            return True
        elif self.override is None and self.calculated is None:
            return None
        else:
            return False

    def __dir__(self):
        # Match hxd. Unclear why it's not _override_children but doesn't seem to be
        return ['calculated', 'is_overridden', 'override', 'selected']

    def __len__(self):
        raise Exception("override node doesn't have len implemented")

    def _children(self):
        return self._override_children

    def __next__(self):
        if self._iter < self.__len__():
            i = self._children()[self._iter]
            val = self.selected
            self._iter += 1
            return i, val
        else:
            raise StopIteration

    def __repr__(self):
        calculated_keys = ["selected", "is_overridden"]
        static_keys = [x for x in [y for y in self._override_children if y not in calculated_keys]]

        dictionary = {x: getattr(self, x) for x in static_keys}
        dictionary["selected"] = self.selected
        dictionary["is_overridden"] = self.is_overridden

        contents = str(dictionary)
        return contents

    def __setattr__(self, key, value):
        if "_" == key[0]:
            self.__dict__[key] = value
        elif key in self._override_children and not key in ["selected", "is_overridden"]:
            self.__dict__[key] = _clean_value(value)
        elif key in ["selected", "is_overridden"]:
            pass
        else:
            raise Exception(f"Invalid Key {key} for Override Node")


class hx_internal_FileNode(hx_internal_BaseNode):
    _file_children = ["exists", "file_name", "file_size", "file_extension", "created_at", "created_by_user_id"]

    def __init__(self, *args, files_path="/workspace/editing/algorithms/debug/transient_hxd_files/", **kwargs):
        super(hx_internal_FileNode, self).__init__(*args, **kwargs)

        if os.path.isdir(files_path):
            self._files_path = files_path
        else:
            self._files_path = None

    def __dir__(self):
        return self._file_children

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

    def _read_or_write(self):
        modes = self._modes_from_data_schema_static()

        if self._path[4:] in modes:
            return modes[self._path[4:]]
        else:
            raise Exception("mode not found for file node")

    # TODO: This is only approximate. Check actual behaviour for reading and writing
    def open(self, mode="t"):
        input_or_output = self._read_or_write()

        if (input_or_output == "input") and (mode == "t"):
            open_mode = "r+"
        elif (input_or_output == "input") and (mode == "b"):
            open_mode = "rb+"
        elif (input_or_output == "output") and (mode == "t"):
            open_mode = "r+"
        elif (input_or_output == "output") and (mode == "b"):
            open_mode = "rb+"
        else:
            raise Exception(f"Invalid open mode: input_or_output is {input_or_output} and mode is {mode}")

        f = open(f"{self._files_path}{self.file_name}", open_mode)
        return f

    @property
    def exists(self):
        if self._files_path:
            converted_path = self._path.replace(".", "-")
            files = os.listdir(self._files_path)
            filtered_files = [x for x in files if converted_path in x]
            return bool(len(filtered_files))
        else:
            return False

    # TODO: This is only approximate. Check actual output
    @property
    def file_name(self):
        converted_path = self._path.replace(".", "-")
        if self._files_path:
            files = os.listdir(self._files_path)
            filtered_files = [x for x in files if converted_path in x]
            if len(filtered_files) > 0:
                return filtered_files[0]
        return converted_path


    # TODO: This is only approximate. Check actual output
    @property
    def file_size(self):
        if self._files_path:
            return os.stat(f"{self._files_path}{self.file_name}").st_size
        else:
            return 0
        
    # TODO: This is only approximate. Check actual output
    @property
    def file_extension(self):
        return self.file_name.split(".")[-1]

    @property
    def created_at(self):
        if self._files_path:
            return os.stat(f"{self._files_path}{self.file_name}").st_birthtime
        else:
            return 0

    @property
    def created_by_user_id(self):
        if self._files_path:
            return os.stat(f"{self._files_path}{self.file_name}").st_uid
        else:
            return ""

    def __setattr__(self, key, value):
        if "_" == key[0]:
            self.__dict__[key] = value
        elif key in self._file_children:
            self.__dict__[key] = _clean_value(value)
        else:
            print(f"Skipping key {key} for hx_internal_FileNode")
            # raise Exception(f"Invalid Key {key} for File Node")


class hx_internal_TriangleBaseObj():
    def __init__(self):
        self._locked = False

    def _lock(self):
        self._locked = True

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
        self._locked = False

        super(hx_internal_TriangleNode, self).__init__(*args, **kwargs)

        for child in self._triangle_children_children:
            setattr(self, child, self._triangle_children_children[child])

        self._lock()

    def _lock(self):
        self._locked = True

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
    def __init__(self, data_schema_path="/workspace/editing/data_schema/data_schema_static.py"):
        self.__defaults = {}
        self.__modes = {}

        self.__inputs = []
        self.__outputs = []
        self.__overrides = []
        
        self.__module_name = "data_schema_static"
        self.__data_schema_static_path = data_schema_path
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

            self.__data_schema_static_module = module.data_schema()

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
            if parent_path == "":
                path = child_path
            else:
                path = parent_path + '.' + child_path

            child = parent_node.children[child_path]

            if child.type == "structure":
                default_val = hx_internal_StructureNode({}, path=path)
                mode = None
                self.__recurssive_fetch(path, child, fetch)
            elif child.type == "list":
                if isinstance(parent_node.children[child_path].default_element_count, int):
                    default_element_count = parent_node.children[child_path].default_element_count
                else:
                    default_element_count = None

                default_val = hx_internal_ListNode([{}], path=path, default_element_count=default_element_count, mode=child.__getattribute__("mode"))

                mode = None
                self.__recurssive_fetch(path, child, fetch)
            elif child.type == "file":
                default_val = hx_internal_FileNode()
                mode = child.__getattribute__("mode")
            elif child.type == "triangle":
                default_val = hx_internal_TriangleNode()
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
                    else:
                        raise Exception(f"default not found for {path}. Please check the data schema static copy is up to date")
                    self.__inputs.append(path)
                elif mode == "override":
                    default_val = hx_internal_OverrideNode()
                    self.__overrides.append(path)
                else:
                    default_val = None
                    self.__outputs.append(path)

                if isinstance(default_val, str):
                    if default_val.__contains__("Undefined"):
                        default_val = 'default_index=' + str(child.__getattribute__("default_index"))
            
            self.__defaults[path] = default_val
            self.__modes[path] = mode


class OfflineProgress:
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

def _rgetattr(obj, attr, list_items=[0], get_missing_indexes_from=None):
    list_items = _validate_list_items(list_items)
        
    # Check for list in offline/real hxd agnostic way
    if dir(obj) == LIST_NODE_DIR:
        list_item = list_items[0]
        list_items = list_items[1:]
        if get_missing_indexes_from is not None and len(obj) <= list_item:
            return getattr(get_missing_indexes_from._default_child, attr), list_items
        else:
            return getattr(obj[list_item], attr), list_items
    else:
        return getattr(obj, attr), list_items

def rgetattr(obj, attr, splitter=".", list_items=[0], get_missing_indexes_from=None):
    list_items = _validate_list_items(list_items)

    attrs = attr.split(splitter)
    for a in attrs:
        obj, list_items_new = _rgetattr(obj, a, list_items=list_items, get_missing_indexes_from=get_missing_indexes_from)
        if get_missing_indexes_from is not None:
            get_missing_indexes_from, _ = _rgetattr(get_missing_indexes_from, a, list_items=list_items)

        list_items = list_items_new  # Need to assign here as list_items is needed unmodified for both _rgetattr statements
    return obj
    # func = functools.partial(_rgetattr, list_items=list_items)
    # return functools.reduce(func, [obj] + attr.split(splitter))

def _rgetkey(obj, key, list_items=[0]):
    list_items = _validate_list_items(list_items)

    # Check for list in offline/real hxd agnostic way
    if dir(obj) == LIST_NODE_DIR or isinstance(obj, list):
        list_item = list_items[0]
        list_items = list_items[1:]
        return obj[list_item][key], list_items
    else:
        return obj[key], list_items

def rgetkey(obj, key, splitter=".", list_items=[0]):
    list_items = _validate_list_items(list_items)

    keys = key.split(splitter)
    for k in keys:
        obj, list_items = _rgetkey(obj, k, list_items=list_items)
    return obj

    # func = functools.partial(_rgetkey, list_items=list_item)
    # return functools.reduce(func, [obj] + key.split(splitter))

def _check_list_lengths(obj, path, splitter="."):
    lists = {}
    for i in range(len(path.split(splitter))):
        sub_path = splitter.join(path.split(splitter)[:i])
        lists[sub_path] = _list_length(obj, sub_path)
    return lists

def _list_length(obj, path, splitter="."):
    if path == "":
        return None
    else:
        if dir(rgetattr(obj, path, splitter=splitter)) == LIST_NODE_DIR:
            return len(rgetattr(obj, path, splitter=splitter))
        else:
            return None

def _get_list_length_combinations(obj, path, splitter="."):
    list_lengths = _check_list_lengths(obj, path, splitter=splitter)
    ranges = [val for node, val in list_lengths.items() if val]
    list_item_combinations = [list(y) for y in itertools.product(*[list(range(x)) for x in ranges])]
    return list_item_combinations

def _validate_list_items(list_items):
    if not isinstance(list_items, list):
        list_items = [list_items]
    if list_items == []:
        list_items = [0]

    return list_items