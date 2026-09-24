import hx
import copy
import pandas as pd
import numpy as np
import time
import json
import itertools
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
# from libraries.rate_change.algorithms.transient_hxd.transient_hxd import init_transient_hxd, DummyProgress, rgetattr, rsetattr, reset_node_outputs
from algorithms.rate_change.algorithms.transient_hxd.transient_hxd import init_transient_hxd, DummyProgress, rgetattr, rsetattr, reset_node_outputs

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
        expiring_currency=None,
        current_actual_prem=None,
        current_technical_prem=None,
        current_currency=None,
        async_tasks=[],
        data_schema_static_path=None
    ):
        self.hxd = hxd
        self.progress = progress
        self.buckets = buckets
        self.layers_path = layers_path
        self.expiring_actual_prem = expiring_actual_prem
        self.expiring_technical_prem = expiring_technical_prem
        self.expiring_currency = expiring_currency
        self.current_actual_prem = current_actual_prem
        self.current_technical_prem = current_technical_prem
        self.current_currency = current_currency
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

    def _update_expiring_hxd(self, target, path, override, source_from_expiring):
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
                rgetattr(target, listnode, list_items=[0], splitter="/")._pad_with_default(num_items=val)
            else:
                pass

        # Reset this as it may have changed, but expiry should now always be strictly at least as big as renewal 
        expiring_list_lengths = self.check_list_lengths(path, target=target)  

        ranges = [val for node, val in expiring_list_lengths.items() if val]
        list_item_combinations = [list(y) for y in itertools.product(*[list(range(x)) for x in ranges])]

        if source_from_expiring:
            get_from = self.expiring_hxd
        else:
            get_from = self.hxd

        self._update_all_list_combinations(get_from, path, target, list_item_combinations, override)


    def _update_all_list_combinations(self, get_from, path, target, list_item_combinations, override):
        override_children = ['calculated', 'is_overridden', 'override', 'selected']

        for list_items in list_item_combinations:
            hxd_val = rgetattr(get_from, path, splitter="/", list_items=list_items, get_missing_indexes_from=target)
            
            if dir(hxd_val) == override_children and override:  # handle explicit overriding differently
                rsetattr(target, f"{path}/calculated", getattr(hxd_val, "selected"), splitter="/", list_items=list_items)
                rsetattr(target, f"{path}/override", getattr(hxd_val, "selected"), splitter="/", list_items=list_items)
            elif dir(hxd_val) == override_children:  # override node
                for override_child in override_children:
                    rsetattr(target, f"{path}/{override_child}", getattr(hxd_val, override_child), splitter="/", list_items=list_items)
            else:
                # if hxd_val != rgetattr(target, path, splitter="/"):
                # print(f"changing {path} from {rgetattr(target, path, list_items=list_items, splitter='/')} to {hxd_val} - item {list_items}")
                rsetattr(target, path, hxd_val, splitter="/", list_items=list_items)
                # print(self.rc_hxds['exposure'].cds.exposure.granular.gl_revenue[1].tier_input)


    def _setup_expiring_custom(self, bucket_name, path_to_list, path_from_list_to_req_item):
        """
        Shuffles expiring layers to match the renewed layers, duplicating if necessary 
        (i.e. multiple renewed layers point to the same expiring layer) 
        """
        # list of layer expiry_index to renew
        required_items = [(rgetattr(item, path_from_list_to_req_item, list_items=[0], splitter="/") or 0) - 1 for item in rgetattr(self.hxd, path_to_list, splitter="/")]
        actual_items = rgetattr(self.rc_hxds[bucket_name], path_to_list, list_items=[0], splitter="/")
        
        rsetattr(self.rc_hxds[bucket_name], path_to_list, [deepcopy(actual_items[required_item]) for required_item in required_items], splitter="/")


    # Edit 1.50
    def _setup_expiring_custom_order(self, path_to_list, path_from_list_to_req_item):
        """
        Shuffles expiring layers to match the renewed layers, duplicating if necessary 
        (i.e. multiple renewed layers point to the same expiring layer) 
        """
        # list of layer expiry_index to renew
        required_items = [(rgetattr(item, path_from_list_to_req_item, list_items=[0], splitter="/") or 0) - 1 for item in rgetattr(self.hxd, path_to_list, splitter="/")]

        # get list of source value
        actual_items = rgetattr(self.expiring_hxd, path_to_list, list_items=[0], splitter="/")

        # delete current items
        for item in rgetattr(self.expiring_hxd, path_to_list, list_items=[0], splitter="/"):
            rgetattr(self.expiring_hxd, path_to_list, list_items=[0], splitter="/").remove

        # set new items
        rsetattr(self.expiring_hxd, path_to_list, [deepcopy(actual_items[required_item]) for required_item in required_items], splitter="/")

    def _setup_expiring_bucket_custom_order(self, bucket_name, path_to_list, path_from_list_to_req_item):
        """
        Shuffles expiring layers to match the renewed layers, duplicating if necessary 
        (i.e. multiple renewed layers point to the same expiring layer) 
        """
        # list of layer expiry_index to renew
        required_items = [(rgetattr(item, path_from_list_to_req_item, list_items=[0], splitter="/") or 0) - 1 for item in rgetattr(self.hxd, path_to_list, splitter="/")]
        actual_items = rgetattr(self.rc_hxds[bucket_name], path_to_list, list_items=[0], splitter="/")
        rgetattr(self.rc_hxds[bucket_name], path_to_list, list_items=[0], splitter="/").clear()
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

            if dir(rgetattr(target, path, list_items=[0], splitter="/")) == ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']:
                return len(rgetattr(target, path, list_items=[0], splitter="/"))
            else:
                return None

    def _validate_buckets_format(self, buckets):
        if not isinstance(buckets, dict):
            return False, "Input for RARC buckets must be a dictionary."
        
        for key, value in buckets.items():
            if not isinstance(value, list):
                return False, f"Value for key '{key}' is not a list in the RARC buckets dictionary."
            for item in value:
                if not isinstance(item, (str, dict)):
                    return False, f"Item '{item}' in the list for key '{key}' is not a string or dict in the RARC buckets dictionary."
                if isinstance(item, dict) and "node" not in item:
                    return False, f"Item '{item}' in the list for key '{key}' is a dict but does not contain key 'node' in the RARC buckets dictionary."
        
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

    def _validate_expiring_inputs_in_ccy(self, expiring_inputs_in_ccy):
        """
        Validates that the input is a list of tuples, where each tuple contains exactly two strings.

        Args:
            expiring_inputs_in_ccy (list): The list of tuples to validate.

        Returns:
            bool: True if the input is valid, False otherwise.

        Raises:
            ValueError: If the input is not a list, or if any tuple does not meet the criteria.
        """
        # Check if the input is a list
        if not isinstance(expiring_inputs_in_ccy, list):
            raise ValueError("Input must be a list.")

        # Check each item in the list
        for item in expiring_inputs_in_ccy:
            # Check if the item is a tuple
            if not isinstance(item, tuple):
                raise ValueError(f"Each item in the list must be a tuple. Found: {type(item)}")

            # Check if the tuple has exactly 2 items
            if len(item) != 2:
                raise ValueError(f"Each tuple must contain exactly 2 items. Found: {len(item)} items in {item}")

            # Check if both items in the tuple are strings
            if not all(isinstance(i, str) for i in item):
                raise ValueError(f"Both items in the tuple must be strings. Found: {item}")

        # If all checks pass
        return True

        # Prepare fx data to ensure the column names are the same
    def _validate_fx_data(self, df, ccy="ccy", fx_rate="fx_rate"):
        """
        Validates a DataFrame containing currency and FX rate data. Confirm to the of the fx_rates library.

        Args:
            df (pd.DataFrame): Input DataFrame.
            ccy (str): Name of the currency column. Defaults to "ccy".
            fx_rate (str): Name of the FX rate column. Defaults to "fx_rate".

        Returns:
            pd.DataFrame: Validated DataFrame with standardized column names.

        Raises:
            TypeError: If input is not a DataFrame.
            ValueError: If columns are missing, or data is invalid.
        """
        # Validate df is a DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        # Change the name of the columns
        df = df.rename(columns={
            df.columns[0]: ccy,
            df.columns[1]: fx_rate
        })

        # Validate the data format in columns
        if ccy not in df.columns or fx_rate not in df.columns:
            raise ValueError(f"DataFrame must contain columns named '{ccy}' and '{fx_rate}'.")

        # Check if all items in column ccy are strings of 3 letters
        if not df[ccy].apply(lambda x: isinstance(x, str) and len(x) == 3).all():
            raise ValueError(f"All items in column '{ccy}' must be 3-letter strings.")

        # Check if all items in column fx_rate are non-zero positive floats
        try:
            df[fx_rate] = pd.to_numeric(df[fx_rate], errors='raise')
        except ValueError:
            raise ValueError(f"All items in column '{fx_rate}' must be numeric.")

        if not (df[fx_rate] > 0).all():
            raise ValueError(f"All items in column '{fx_rate}' must be positive and non-zero.")

        return df

    def _get_fx_to_usd(self,df, lookup_value, lookup_col="ccy", return_col="fx_rate", if_not_found=1):
        """
        Look up a value in a DataFrame and return the corresponding value from another column.
        If the value is not found, return if_not_found.

        Args:
            df (pd.DataFrame): DataFrame containing the lookup table.
            lookup_value (str): Value to look up in the lookup_col.
            lookup_col (str): Name of the column to search for the lookup_value. Defaults to "ccy".
            return_col (str): Name of the column to return the value from. Defaults to "fx_rate".
            if_not_found (float): Value to return if lookup_value is not found. Defaults to 1.

        Returns:
            float: The corresponding value from return_col, or if_not_found if not found.
        """
        result = df.loc[df[lookup_col] == lookup_value, return_col]
        if result.empty:
            return if_not_found
        return result.iloc[0]

    def _fx_ratio(self,comparison_fx, target_fx, default=1):
        """
        Calculate the conversion ratio: target_fx / comparison_fx.
        If comparison_fx is zero, return default.

        Args:
            comparison_fx (float): FX rate of the comparison currency.
            target_fx (float): FX rate of the target currency.
            default (float): Default value to return if comparison_fx is zero. Defaults to 1.

        Returns:
            float: The conversion ratio.
        """
        if comparison_fx == 0:
            return default
        return target_fx / comparison_fx

    def _convert_selected_inputs(self, expiring_inputs_in_ccy, fx_table):
        """
        Convert selected inputs from one currency to another using FX rates.

        Args:
            expiring_inputs_in_ccy (list): List of tuples (target_attr, comparison_attr).
            fx_table (pd.DataFrame): DataFrame containing FX rates (must have columns "ccy" and "fx_rate").

        Returns:
            None: Modifies self.expiring_hxd in place.
        """
        # validate format
        self._validate_expiring_inputs_in_ccy(expiring_inputs_in_ccy)
        # validate format and values and reassign column names of the dataframe
        fx_table = self._validate_fx_data(fx_table, ccy="ccy", fx_rate="fx_rate")

        exp_layers_list = rgetattr(self.expiring_hxd, self.layers_path, list_items=[0], splitter="/")
        for idx,layer in enumerate(exp_layers_list):
            for item in expiring_inputs_in_ccy:
                
                target_item = rgetattr(self.expiring_hxd, item[1], list_items=[idx], splitter="/")
                comparison_item = rgetattr(self.hxd, item[1], list_items=[idx], splitter="/")

                if target_item == comparison_item:
                    continue
                else:
                    target_fx_to_usd = self._get_fx_to_usd(
                        df=fx_table,
                        lookup_value=target_item,
                        lookup_col="ccy",
                        return_col="fx_rate",
                        if_not_found=1
                    )
                    comparison_fx_to_usd = self._get_fx_to_usd(
                        df=fx_table,
                        lookup_value=comparison_item,
                        lookup_col="ccy",
                        return_col="fx_rate",
                        if_not_found=1
                    )
                    revaluing_factor = self._fx_ratio(target_fx_to_usd,comparison_fx_to_usd, 1)
                    # Convert the value
                    current_value = rgetattr(self.expiring_hxd, item[0], list_items=[idx], splitter="/")
                    converted_value = (current_value or 0) * revaluing_factor
                    rsetattr(self.expiring_hxd, item[0], converted_value, splitter="/", list_items=[idx])

        return

    def calculate_repriced_values(
        self,
        repriced_key_values=None,
        expiring_data=None,
        expiring_policy_option_id=None,
        policy_option_id=None,
        model_version_id=None,
        match_expiring_lists=[],
        expiring_inputs_in_ccy = None,
        fx_table=None

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
        # updated_values = []

        # Get expiring data and initialise transient hxd
        if not expiring_data:
            expiring_data = hx_renew_api.snapshots.get_snapshot(expiring_policy_option_id).json()["data"]
       
        self.expiring_hxd = init_transient_hxd(expiring_data, data_schema_static_path=self.data_schema_static_path, reset_outputs=False, skip_invalid_nodes=True)


        # Makes sure that the model state can be set as required. This is used to bypass rating sections that relate to hx.meta
        # such as the model state checking if hx.meta.expiring_policy_option_id is None (which will use the hx.meta of the current
        # policy not of the expiring one)
        if hasattr(self.expiring_hxd.model_state, "is_expiring_policy"): 
            self.expiring_hxd.model_state.is_expiring_policy = True  

        # Rearrange lists to match pairings
        self._setup_expiring_custom_order(path_to_list="cds/layers", path_from_list_to_req_item="rate_change/expiring_layer")

        # validate input
        if expiring_inputs_in_ccy is None or expiring_inputs_in_ccy == [] or fx_table is None:
            pass
        else:
            # revalue expiring input node in case of change in currency
            self._convert_selected_inputs(expiring_inputs_in_ccy=expiring_inputs_in_ccy, fx_table=fx_table)

        previous_bucket = None
        for i, dict_items in enumerate(self.buckets.items()):
            bucket_name, paths = dict_items

            print(f"setup {bucket_name}")

            if not previous_bucket:
                self.rc_hxds[bucket_name] = deepcopy(self.expiring_hxd)
            else:
                self.rc_hxds[bucket_name] = deepcopy(self.rc_hxds[previous_bucket])  # Start from previous bucket so changes are cumulative 

            for entry in paths:
                if isinstance(entry, dict):
                    path = entry["node"]
                    override = entry.get("override", False)
                    source_from_expiring = entry.get("source_from_expiring", False)  # Note rating algorithm hasn't run yet, so if sourcing any data from expiring (even in reshuffled layers) this is still exactly as was in expiring
                else:
                    path = entry
                    override = False
                    source_from_expiring = False

                self._update_expiring_hxd(self.rc_hxds[bucket_name], path, override, source_from_expiring)

            previous_bucket = bucket_name
        
        ### --- REPRICING
        for i, dict_items in enumerate(self.buckets.items()):
            bucket_name, paths = dict_items
            
            # Run the rating algorithm 
            print(f"rating {bucket_name}")
            
            # Reset node outputs before starting as they would be in the real hxd workflow
            reset_node_outputs(self.rc_hxds[bucket_name], data_schema_static_path=self.data_schema_static_path)
            rating_algorithm(self.rc_hxds[bucket_name])

            # Iterate through each async task name provided and start the task
            for task in self.async_tasks:
                task(self.rc_hxds[bucket_name], DummyProgress())
                rating_algorithm(self.rc_hxds[bucket_name])

            previous_bucket = bucket_name
        
        for list_to_match in [x for x in match_expiring_lists if x]:
            if list_to_match[0] != "cds/layers":
                self._setup_expiring_custom(bucket_name, list_to_match[0], list_to_match[1]) 

        pass

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

        if not self.current_currency:
            current_currency = self.expiring_currency
        else:
            current_currency = self.current_currency

        # Shorten names and get layers
        expiring_layers_list = rgetattr(self.expiring_hxd, self.layers_path, list_items=[0], splitter="/")
        current_layers_list = rgetattr(self.hxd, self.layers_path, list_items=[0], splitter="/")

        # Create DataFrame to calculate changes
        layers_list = [
            {
                "current_layer_id": idx + 1,
                "expiring_layer_id": layer.rate_change.expiring_layer,
                "current_actual": rgetattr(layer, current_actual_prem, list_items=[0], splitter="/"),
                "current_technical": rgetattr(layer, current_technical_prem, list_items=[0], splitter="/"),
                "currency": rgetattr(layer, current_currency, list_items=[0], splitter="/")
            } 
            for idx, layer in enumerate(current_layers_list)
        ]
        rarc_df = pd.DataFrame(layers_list)

        # Edit 1.46 Pad rarc_df if expiring_layers_list is longer
        if len(expiring_layers_list) > rarc_df.shape[0]:
            num_to_add = len(expiring_layers_list) - rarc_df.shape[0]
            padding_rows = pd.DataFrame([{
                "current_layer_id": None,
                "expiring_layer_id": None,
                "current_actual": None,
                "current_technical": None
            }] * num_to_add)
            rarc_df = pd.concat([rarc_df, padding_rows], ignore_index=True)

        # Pad expiring columns with None if expiring_layers_list is shorter
        padding_length = rarc_df.shape[0] - len(expiring_layers_list)

        rarc_df["expiring_actual"] = (
            [rgetattr(layer, current_actual_prem, list_items=[0], splitter="/") for layer in expiring_layers_list]
            + [None] * padding_length
        )

        rarc_df["expiring_technical"] = (
            [rgetattr(layer, current_technical_prem, list_items=[0], splitter="/") for layer in expiring_layers_list]
            + [None] * padding_length
        )

        # Edit 1.46 Add technical premiums to the df
        for bucket_name in self.buckets.keys():
            rc_layers_list = rgetattr(self.rc_hxds[bucket_name], self.layers_path, list_items=[0], splitter="/")
            rc_premium_list = [
                rgetattr(layer, self.expiring_technical_prem, list_items=[0], splitter="/") 
                for layer in rc_layers_list
            ]

            # Edit 1.46 Pad rc_premium_list if needed
            if len(rc_premium_list) < rarc_df.shape[0]:
                rc_premium_list += [None] * (rarc_df.shape[0] - len(rc_premium_list))
            elif len(rc_premium_list) > rarc_df.shape[0]:
                rc_premium_list = rc_premium_list[:rarc_df.shape[0]]

            rarc_df[bucket_name] = rc_premium_list
            # pd.set_option('display.max_columns', None)
            # print(rarc_df)

        # Calculate the % change for each bucket
        buckets_list = list(self.buckets.keys())

        rarc_df[f"model_actual_change"] = self._ratio(rarc_df["model"], rarc_df["expiring_actual"], 1)
        rarc_df[f"model_technical_change"] = self._ratio(rarc_df["model"], rarc_df["expiring_technical"], 1)

        for idx, change in enumerate(buckets_list):
            # Exit when at the end of the list
            if len(buckets_list) == idx + 1:
                break
            current_bucket = buckets_list[idx+1]
            previous_bucket = buckets_list[idx]

            rarc_df[f"{current_bucket}_change"] = self._ratio(rarc_df[current_bucket], rarc_df[previous_bucket], 1)

        rarc_df[f"balancing_actual_change"] = self._ratio(rarc_df["current_actual"], rarc_df["other"], 1)
        rarc_df[f"balancing_technical_change"] = self._ratio(rarc_df["current_technical"], rarc_df["other"], 1)

        # Put the changes in a schema-compliant list
        changes_list = [f"{bucket}_change" for bucket in buckets_list[1:]]
        rarc_list = []
        # Edit 1.46, sort last
        rarc_df.sort_values("current_layer_id", inplace=True, na_position='last')

        for idx, layer in rarc_df.iterrows():
            rarc_dict = {
                "temp_storage": {
                    "quoted_premium": layer["current_actual"],
                    "benchmark_premium": layer["current_technical"],
                    "currency": layer["currency"]
                }
            }

            for change in changes_list:
                rarc_dict[change] = {"model_calculated": layer[change]}

            rarc_list.append(rarc_dict)

        return rarc_df, rarc_list
