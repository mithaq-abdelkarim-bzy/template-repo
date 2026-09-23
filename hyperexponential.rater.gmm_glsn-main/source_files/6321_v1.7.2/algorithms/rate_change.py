import hx
import copy
import pandas as pd
import numpy as np
import time
import json
import itertools
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.transient_hxd.transient_hxd import init_transient_hxd, DummyProgress, rgetattr, rsetattr
from algorithms.rating import rating_algorithm
from copy import deepcopy


class RateChange:
    
    def __init__(
        self, 
        hxd, 
        progress, 
        buckets, 
        layers_path,
        expiring_actual_prem,
        expiring_technical_prem,
        current_actual_prem=None,
        current_technical_prem=None,
        async_tasks=[],
        data_schema_static_path=None
    ):
        self.hxd = hxd
        self.progress = progress
        self.buckets = buckets
        self.layers_path = layers_path
        self.expiring_actual_prem = expiring_actual_prem
        self.expiring_technical_prem = expiring_technical_prem
        self.current_actual_prem = current_actual_prem
        self.current_technical_prem = current_technical_prem
        self.async_tasks = async_tasks
        self.rc_hxds = {}
        self.data_schema_static_path = data_schema_static_path
    
    @staticmethod
    def _ratio(a, b, if_undefined=0):
        # Check if the inputs are scalar values
        if np.isscalar(a) and np.isscalar(b):
            return if_undefined if b == 0 else a / b

        # Convert inputs to pandas Series if they aren't already
        a = pd.Series(a)
        b = pd.Series(b)
        
        # Calculate the ratio, applying if_undefined where b is zero
        result = a.where(b != 0, if_undefined) / b.where(b != 0, 1)
        
        return result

    def _update_expiring_hxd(self, target, path):
        """
        Update a field in the target dictionary from the source dictionary based on a path string.
        """

        # if path=="cds/exposure/granular/lives/no_lives":
        #     breakpoint()

        renewal_list_lengths = self.check_list_lengths(path)
        expiring_list_lengths = self.check_list_lengths(path, target=target)

        # # Layers are handled separately
        # if "cds/layers" in renewal_list_lengths:  
        #     renewal_list_lengths.pop("cds/layers")
        # if "cds/layers" in expiring_list_lengths:  
        #     expiring_list_lengths.pop("cds/layers")

        list_differences = {}
        for listnode in renewal_list_lengths:
            if renewal_list_lengths[listnode] and expiring_list_lengths[listnode]:
                list_differences[listnode] = renewal_list_lengths[listnode] - expiring_list_lengths[listnode]
        
        # if list_differences:
        #     breakpoint()

        for listnode, val in list_differences.items():
            if val == 0:  # Lengths match - don't modify
                pass  
            elif val > 0:  # Renewal longer than expiry - pad expiry with default values
                rgetattr(target, listnode, splitter="/")._pad_with_default(num_items=val)
            else:
                pass

        # Reset this as it may have changed, but expiry should now always be strictly at least as big as renewal 
        expiring_list_lengths = self.check_list_lengths(path, target=target)  
        # if "cds/layers" in expiring_list_lengths:  
        #     expiring_list_lengths.pop("cds/layers")

        ranges = [val for node, val in expiring_list_lengths.items() if val]
        list_item_combinations = [list(y) for y in itertools.product(*[list(range(x)) for x in ranges])]


        # if "cds/layers/" == path[:11]:
        #     path_in_layer = path[11:]
        #     for index, layer in enumerate(self.hxd.cds.layers):
        #         target_layer = target.cds.layers[index]
        #         self._update_all_list_combinations(layer, path_in_layer, target, list_item_combinations)
        # else:
        self._update_all_list_combinations(self.hxd, path, target, list_item_combinations)


    def _update_all_list_combinations(self, get_from, path, target, list_item_combinations):
        override_children = ['calculated', 'is_overridden', 'override', 'selected']

        for list_items in list_item_combinations:
            hxd_val = rgetattr(get_from, path, splitter="/", list_items=list_items, get_missing_indexes_from=target)
            
            if dir(hxd_val) == override_children:  # override node
                for override_child in override_children:
                    rsetattr(target, f"{path}/{override_child}", getattr(hxd_val, override_child), splitter="/", list_items=list_items)
            else:
                # if hxd_val != rgetattr(target, path, splitter="/"):
                # print(f"changing {path} from {rgetattr(target, path, list_items=list_items, splitter='/')} to {hxd_val} - item {list_items}")
                rsetattr(target, path, hxd_val, splitter="/", list_items=list_items)
                # print(self.rc_hxds['exposure'].cds.exposure.granular.gl_revenue[1].tier_input)
                

    def _setup_expiring_layers(self, bucket_name):
        """
        Shuffles expiring layers to match the renewed layers, duplicating if necessary 
        (i.e. multiple renewed layers point to the same expiring layer) 
        """
        # required_layers = [layer.rate_change.expiring_layer - 1 for layer in self.hxd.cds.layers]
        # actual_layers = self.rc_hxds[bucket_name].cds.layers
        
        # self.rc_hxds[bucket_name].cds.layers = [deepcopy(actual_layers[required_layer]) for required_layer in required_layers]

        self._setup_expiring_custom(bucket_name, "cds/layers", "rate_change/expiring_layer")


    def _setup_expiring_custom(self, bucket_name, path_to_list, path_from_list_to_req_item):
        """
        Shuffles expiring layers to match the renewed layers, duplicating if necessary 
        (i.e. multiple renewed layers point to the same expiring layer) 
        """
        required_items = [rgetattr(item, path_from_list_to_req_item, splitter="/") - 1 for item in rgetattr(self.hxd, path_to_list, splitter="/")]
        actual_items = rgetattr(self.rc_hxds[bucket_name], path_to_list, splitter="/")
        
        rsetattr(self.rc_hxds[bucket_name], path_to_list, [deepcopy(actual_items[required_item]) for required_item in required_items], splitter="/")
    

    def check_list_lengths(self, path, target=None):
        lists = {}
        for i in range(len(path.split("/"))):
            sub_path = "/".join(path.split("/")[:i])
            lists[sub_path] = self.list_length(sub_path, target=target)
        return lists

    def list_length(self, path, target=None):
        if path == "":
            return None
        else:
            if not target:
                target = self.hxd

            if dir(rgetattr(target, path, splitter="/")) == ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']:
                return len(rgetattr(target, path, splitter="/"))
            else:
                return None

    def _validate_buckets_format(self, buckets):
        if not isinstance(buckets, dict):
            return False, "Input for RARC buckets must be a dictionary."
        
        for key, value in buckets.items():
            if not isinstance(value, list):
                return False, f"Value for key '{key}' is not a list in the RARC buckets dictionary."
            for item in value:
                if not isinstance(item, str):
                    return False, f"Item '{item}' in the list for key '{key}' is not a string in the RARC buckets dictionary."
        
        return True, "Format is correct."

    def _get_level(self, input_path, dictionary):
        """
        Retrieve the value at a specific level in a nested dictionary.
        """
        # Split the input string into keys
        keys = input_path.split('/')

        # Navigate through the nested dictionary using the keys
        current_level = dictionary
        for key in keys:
            current_level = current_level[key]

        return current_level

    def calculate_repriced_values(
        self,
        repriced_key_values=None,
        expiring_data=None,
        expiring_policy_option_id=None,
        policy_option_id=None,
        model_version_id=None,
        match_expiring_lists=[]
    ):
        # Validate the format of the 'buckets' input
        is_valid, message = self._validate_buckets_format(self.buckets)
        if not is_valid:
            raise ValueError(f"{message}")

        expiring_policy_option_id = self.hxd.cds.rate_change.expiring_policy_option_id.selected or expiring_policy_option_id
        policy_option_id = hx.meta.policy_option_id or policy_option_id

        # Initialise the hx_renew_api library
        hx_renew_api = init_hx_renew_api()

        # Initialise list to store sequentially updated values
        updated_values = []

        # Get expiring data and initialise transient hxd
        if not expiring_data:
            expiring_data = hx_renew_api.snapshots.get_snapshot(expiring_policy_option_id).json()["data"]

        self.expiring_hxd = init_transient_hxd(expiring_data, data_schema_static_path=self.data_schema_static_path)

        previous_bucket = None
        for i, dict_items in enumerate(self.buckets.items()):
            bucket_name, paths = dict_items

            # print(bucket_name)

            if not previous_bucket:
                self.rc_hxds[bucket_name] = deepcopy(self.expiring_hxd)
                self._setup_expiring_layers(bucket_name)
                for list_to_match in [x for x in match_expiring_lists if x]:
                    if list_to_match[0] != "cds/layers":
                        self._setup_expiring_custom(bucket_name, list_to_match[0], list_to_match[1])
            else:
                self.rc_hxds[bucket_name] = deepcopy(self.rc_hxds[previous_bucket])  # Start from previous bucket so changes are cumulative 

            for path in paths:
                self._update_expiring_hxd(self.rc_hxds[bucket_name], path)

            previous_bucket = bucket_name
        
        ### --- REPRICING
        for i, dict_items in enumerate(self.buckets.items()):
            bucket_name, paths = dict_items
            
            # Run the rating algorithm 
            rating_algorithm(self.rc_hxds[bucket_name])

            # Iterate through each async task name provided and start the task
            for task in self.async_tasks:
                task(self.rc_hxds[bucket_name], DummyProgress())
                rating_algorithm(self.rc_hxds[bucket_name])

            previous_bucket = bucket_name

    def calculate_rarc_by_layer(self):
        # Set current equal to expiring if not declared
        if not self.current_technical_prem:
            current_technical_prem = self.expiring_technical_prem
        else:
            current_technical_prem = self.current_technical_prem

        if not self.current_actual_prem:
            current_actual_prem = self.expiring_actual_prem
        else:
            current_actual_prem = self.current_actual_prem

        # Shorten names and get layers
        expiring_layers_list = rgetattr(self.expiring_hxd, self.layers_path, splitter="/")
        current_layers_list = rgetattr(self.hxd, self.layers_path, splitter="/")

        # Create DataFrame to calculate changes
        layers_list = [
            {
                "current_layer_id": idx + 1,
                "expiring_layer_id": layer.rate_change.expiring_layer,
                "current_actual": rgetattr(layer, current_actual_prem, splitter="/"),
                "current_technical": rgetattr(layer, current_technical_prem, splitter="/")
            } 
            for idx, layer in enumerate(current_layers_list)
        ]
        rarc_df = pd.DataFrame(layers_list)

        # Add technical premiums to the df
        for bucket_name in self.buckets.keys():
            rc_layers_list = rgetattr(self.rc_hxds[bucket_name], self.layers_path, splitter="/")
            rc_premium_list = [rgetattr(layer, self.expiring_technical_prem, splitter="/") for idx, layer in enumerate(rc_layers_list)]
            rarc_df[bucket_name] = rc_premium_list[:rarc_df.shape[0]]

        # Calculate the % change for each bucket
        buckets_list = list(self.buckets.keys())

        for idx, change in enumerate(buckets_list):
            # Exit when at the end of the list
            if len(buckets_list) == idx + 1:
                break
            
            current_bucket = buckets_list[idx+1]
            previous_bucket = buckets_list[idx]
            rarc_df[f"{current_bucket}_change"] = self._ratio(rarc_df[current_bucket], rarc_df[previous_bucket], 1)

        # Put the changes in a schema-compliant list
        changes_list = [f"{bucket}_change" for bucket in buckets_list[1:]]
        rarc_list = []

        rarc_df.sort_values("current_layer_id", inplace=True)

        for idx, layer in rarc_df.iterrows():
            rarc_dict = {
                "temp_storage": {
                    "quoted_premium": layer["current_actual"],
                    "benchmark_premium": layer["current_technical"]
                }
            }

            for change in changes_list:
                rarc_dict[change] = {
                    "model_calculated": layer[change],
                    "uw_selected": layer[change]
                }

            rarc_list.append(rarc_dict)

        return rarc_df, rarc_list
