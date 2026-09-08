import hx
import copy
import pandas as pd
import numpy as np
import time
import json
import itertools
import warnings
from collections import Counter
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.transient_hxd.transient_hxd import init_transient_hxd, DummyProgress, rgetattr, rsetattr
from algorithms.rating import rating_algorithm
from copy import deepcopy
from algorithms.timer import timer


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

    def _update_expiring_hxd(self, target, path, list_excluded_from_padding=None, matching_key=None, common_items=None):
        """
        Synchronise the structure of the target data with the source data (`self.hxd`) by adjusting list lengths 
        and optionally filtering elements based on a key.

        This function:
        - Compares list lengths between `self.hxd` (renewal data) and `target` (expiring data).
        - Updates values in `target` based on `self.hxd`.
        - Pads lists in `target` if they are shorter than in `self.hxd`.
        - Ensures that a specific list (if specified via `list_excluded_from_padding`) only contains common elements
        based on a matching key.
        """

        renewal_list_lengths = self.check_list_lengths(path)
        expiring_list_lengths = self.check_list_lengths(path, target=target)

        list_differences = {}
        for listnode in renewal_list_lengths:
            if renewal_list_lengths[listnode] and expiring_list_lengths[listnode]:
                list_differences[listnode] = renewal_list_lengths[listnode] - expiring_list_lengths[listnode]
        
        # if list_differences:
        #     breakpoint()

        for listnode, val in list_differences.items():
            if (list_excluded_from_padding is not None) and (list_excluded_from_padding == listnode):
                continue
            if val == 0:  # Lengths match - don't modify
                pass  
            elif val > 0:  # Renewal longer than expiry - pad expiry with default values
                rgetattr(target, listnode, splitter="/")._pad_with_default(num_items=val)
            else:
                pass

        # Reset this as it may have changed, but expiry should now always be strictly at least as big as renewal 
        expiring_list_lengths = self.check_list_lengths(path, target=target)  
        ranges = [val for node, val in expiring_list_lengths.items() if val]
        list_item_combinations = [list(y) for y in itertools.product(*[list(range(x)) for x in ranges])]

        # Filter hxd (renewal data) so that the specially treated list only contains common items
        filtered_hxd = deepcopy(self.hxd)

        if list_excluded_from_padding and matching_key and common_items:    
            attr_list = rgetattr(filtered_hxd, list_excluded_from_padding, splitter="/")

            # Iterate backwards to avoid index shifting issues
            for i in range(len(attr_list) - 1, -1, -1):
                if getattr(attr_list[i], matching_key) not in common_items:
                    del attr_list[i]  # Remove item from the list     

        self._update_all_list_combinations(filtered_hxd, path, target, list_item_combinations)


    def _update_all_list_combinations(self, get_from, path, target, list_item_combinations):
        override_children = ['calculated', 'is_overridden', 'override', 'selected']

        for list_items in list_item_combinations:
            hxd_val = rgetattr(get_from, path, splitter="/", list_items=list_items, get_missing_indexes_from=target)
            
            if dir(hxd_val) == override_children:  # override node
                for override_child in override_children:
                    rsetattr(target, f"{path}/{override_child}", getattr(hxd_val, override_child), splitter="/", list_items=list_items)
            else:
                rsetattr(target, path, hxd_val, splitter="/", list_items=list_items)
                

    def _setup_expiring_layers(self, bucket_name):
        """
        Shuffles expiring layers to match the renewed layers, duplicating if necessary 
        (i.e. multiple renewed layers point to the same expiring layer) 
        """
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

    def _validate_split_list_inputs(
        self,
        custom_expiring_data,
        split_list_path,
        matching_key,
        additional_items_bucket
    ):
        valid = True
        inputs = {
            "custom_expiring_data": custom_expiring_data,
            "split_list_path": split_list_path,
            "matching_key": matching_key,
            "additional_items_bucket": additional_items_bucket
        }

        # Check if some inputs are None while others are not
        none_inputs = [key for key, value in inputs.items() if value is None]
        non_none_inputs = [key for key, value in inputs.items() if value is not None]

        if none_inputs and non_none_inputs:
            warnings.warn(
                f"Some inputs are provided, but the following inputs are missing: {', '.join(none_inputs)}. Skipping this step."
            )
            return False

        # Proceed with validation only if all inputs are provided
        if all(value is not None for value in inputs.values()):
            errors = []

            if not (isinstance(custom_expiring_data, list) and len(custom_expiring_data) == 4):
                errors.append("custom_expiring_data must be a list of exactly 4 elements: \n\
                    1. Original expiring data (ED)\n2. ED with common items\n3. ED with additional renewal items\n4. ED with dropped items")

            if not (isinstance(split_list_path, str) and split_list_path.startswith("cds/")):
                errors.append("split_list_path must be a string and start with 'cds/'")

            if not isinstance(matching_key, str):
                errors.append("matching_key must be a string")

            if not (isinstance(additional_items_bucket, str) and additional_items_bucket in self.buckets.keys()):
                errors.append("additional_items_bucket must be a string and belong to the 'buckets' dictionary")

            if errors:
                warnings.warn(
                    "It looks like you're trying to use custom_expiring_data, split_list_path, matching_key and additional_items_bucket, "
                    "but some inputs are invalid. Skipping this step. Errors:\n" + "\n".join(f"- {e}" for e in errors)
                )
                valid = False

        return valid
    
    def _get_split_list_items(
        self,
        custom_expiring_data,
        split_list_path,
        matching_key
    ):  
        # Get common items
        expiring_data_common = custom_expiring_data[1]
        list_common = self._get_level(split_list_path, expiring_data_common)
        common_items = [item[matching_key] for item in list_common]

        # Get other items
        expiring_data_others = custom_expiring_data[2]
        list_others = self._get_level(split_list_path, expiring_data_others)
        other_items = [item[matching_key] for item in list_others]  

        # Get dropped items
        expiring_data_dropped = custom_expiring_data[3]
        list_dropped = self._get_level(split_list_path, expiring_data_dropped)
        dropped_items = [item[matching_key] for item in list_dropped]

        return common_items, other_items, dropped_items

    def _remove_dropped_elements(
        self,
        custom_expiring_data,
        dropped_items,
        bucket_name,
        split_list_path,
        matching_key,
        additional_items_bucket
    ):
        # Check inputs
        are_inputs_valid = self._validate_split_list_inputs(custom_expiring_data, split_list_path, matching_key, additional_items_bucket)
        if not are_inputs_valid:
            return

        # Remove items that have dropped by creating new list of remaining items
        print(f"Removing dropped items for: {bucket_name}")
        hxd_list = rgetattr(self.rc_hxds[bucket_name], split_list_path, splitter="/")
        list_renewal = [item for i, item in enumerate(hxd_list) if getattr(hxd_list[i], matching_key) not in dropped_items]
        rsetattr(self.rc_hxds[bucket_name], split_list_path, list_renewal, splitter="/")

    
    def _append_renewal_elements(
        self,
        custom_expiring_data,
        split_list_path,
        matching_key,
        additional_items_bucket
    ):
        # Check inputs
        are_inputs_valid = self._validate_split_list_inputs(custom_expiring_data, split_list_path, matching_key, additional_items_bucket)
        if not are_inputs_valid:
            return
                
        # Check specified list is not empty
        expiring_data_others = custom_expiring_data[2]
        if len(self._get_level(split_list_path, expiring_data_others)) == 0:
            print("List of additional renewal elements is empty. Appending will be skipped.")
            return

        expiring_hxd_others = init_transient_hxd(expiring_data_others, data_schema_static_path=self.data_schema_static_path)

        start_appending = False
        for i, (bucket_name, paths) in enumerate(self.buckets.items()):
            # Only append the additional items from the selected bucket onwards
            if bucket_name == additional_items_bucket:
                start_appending = True
            if not start_appending:
                continue
            
            print(f"Appending additional items for: {bucket_name}")
            split_list_common = rgetattr(self.rc_hxds[bucket_name], split_list_path, splitter="/")
            split_list_others = rgetattr(expiring_hxd_others, split_list_path, splitter="/")
            split_list_common.extend(split_list_others)


    def calculate_repriced_values(
        self,
        repriced_key_values=None,
        custom_expiring_data=None,
        split_list_path=None,
        matching_key=None,
        additional_items_bucket=None,
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

        # Get expiring data and initialise transient hxd
        if not custom_expiring_data:
            expiring_data = hx_renew_api.snapshots.get_snapshot(expiring_policy_option_id).json()["data"]
        elif isinstance(custom_expiring_data, list): # For cases when a specific list in expiring data needs to be split between common and other items
            expiring_data = custom_expiring_data[0]

        self.expiring_hxd = init_transient_hxd(expiring_data, data_schema_static_path=self.data_schema_static_path)

        # Get slip list items
        common_items, other_items, dropped_items = self._get_split_list_items(custom_expiring_data, split_list_path, matching_key)

        # Create different hxds for each bucket
        previous_bucket = None
        start_removing = False

        for i, dict_items in enumerate(self.buckets.items()):
            bucket_name, paths = dict_items
            print(f"Creating hxd for: {bucket_name}")

            if not previous_bucket:
                self.rc_hxds[bucket_name] = deepcopy(self.expiring_hxd)
                self._setup_expiring_layers(bucket_name)
                for list_to_match in [x for x in match_expiring_lists if x]:
                    if list_to_match[0] != "cds/layers":
                        self._setup_expiring_custom(bucket_name, list_to_match[0], list_to_match[1])
            else:
                self.rc_hxds[bucket_name] = deepcopy(self.rc_hxds[previous_bucket])  # Start from previous bucket so changes are cumulative
                
            # Remove items that have dropped in specified list from expiry to renewal
            if bucket_name == additional_items_bucket:
                start_removing = True
            if start_removing:
                self._remove_dropped_elements(custom_expiring_data, dropped_items, bucket_name, split_list_path, matching_key, additional_items_bucket)
            
            # Sequentially update nodes for each bucket
            print(f"Updating inputs for: {bucket_name}")
            for path in paths:
                # Only update elements of list if there is at least one common item
                if path.startswith(split_list_path) and (len(common_items) == 0):
                    continue

                self._update_expiring_hxd(
                    self.rc_hxds[bucket_name], 
                    path, 
                    list_excluded_from_padding=split_list_path,
                    matching_key=matching_key,
                    common_items=common_items
                )

            previous_bucket = bucket_name

        # Append additional items to specified list
        self._append_renewal_elements(custom_expiring_data, split_list_path, matching_key, additional_items_bucket)
        
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
                rarc_dict[change] = {"model_calculated": layer[change]}

            rarc_list.append(rarc_dict)

        return rarc_df, rarc_list
