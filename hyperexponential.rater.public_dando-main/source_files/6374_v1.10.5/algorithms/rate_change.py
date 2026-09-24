import hx
import copy
import pandas as pd
import numpy as np
import time
import json
import itertools

from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.transient_hxd.transient_hxd import init_transient_hxd, DummyProgress, rgetattr, rsetattr, hx_internal_StructureNode, DataSchemaStaticParser
from algorithms.rating import rating_algorithm
from copy import deepcopy
from types import SimpleNamespace
from libraries.rate_change.algorithms.transient_hxd.transient_hxd import hx_internal_OverrideNode


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
        # Scalar case
        if np.isscalar(a) and np.isscalar(b):
            if a is None or b is None:
                return if_undefined

            try:
                if pd.isna(a) or pd.isna(b) or b == 0:
                    return if_undefined

                result = a / b

                if pd.isna(result) or not np.isfinite(result):
                    return if_undefined

                return result

            except Exception:
                return if_undefined

        # Series / array case
        a = pd.to_numeric(pd.Series(a), errors="coerce")
        b = pd.to_numeric(pd.Series(b), errors="coerce")

        valid = (
            a.notna()
            & b.notna()
            & (b != 0)
        )

        result = pd.Series(if_undefined, index=a.index, dtype="float64")
        result.loc[valid] = a.loc[valid] / b.loc[valid]

        result = result.replace([np.inf, -np.inf], if_undefined)
        result = result.fillna(if_undefined)

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

        lengths = []
        for node, exp_len in expiring_list_lengths.items():
            if not exp_len:
                continue
            ren_len = renewal_list_lengths.get(node)
            if ren_len:
                lengths.append(min(exp_len, ren_len))
            else:
                lengths.append(exp_len)
        
        list_item_combinations = [list(combo) for combo in itertools.product(*[range(length) for length in lengths])] if lengths else [[]]


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

                        

            if isinstance(hxd_val, hx_internal_OverrideNode):  # override node
                target_override = rgetattr(target, path, splitter="/", list_items=list_items, get_missing_indexes_from=get_from)
                if target_override is None:
                    placeholder = SimpleNamespace(
                        calculated=None,
                        override=None,
                        is_overridden=False,
                        selected=None,
                    )
                    rsetattr(target, path, placeholder, splitter="/", list_items=list_items)
                for override_child in override_children:
                    rsetattr(
                        target,
                        f"{path}/{override_child}",
                        getattr(hxd_val, override_child),
                        splitter="/",
                        list_items=list_items,
                    )
            
            # if dir(hxd_val) == override_children:  # override node
            #     for override_child in override_children:
            #         rsetattr(target, f"{path}/{override_child}", getattr(hxd_val, override_child), splitter="/", list_items=list_items)
            else:
                # if hxd_val != rgetattr(target, path, splitter="/"):
                # print(f"changing {path} from {rgetattr(target, path, list_items=list_items, splitter='/')} to {hxd_val} - item {list_items}")
                rsetattr(target, path, hxd_val, splitter="/", list_items=list_items)
                # print(self.rc_hxds['exposure'].cds.exposure.granular.gl_revenue[1].tier_input)
                
    def _inflate_override_nodes(self, payload, override_paths):
        override_tree: dict[str, dict | None] = {}
        for dot_path in override_paths:
            parts = dot_path.split(".")
            branch = override_tree
            for part in parts[:-1]:
                branch = branch.setdefault(part, {})
            branch.setdefault(parts[-1], None)
 
        def _apply(node, tree):
            if isinstance(node, list):
                for item in node:
                    _apply(item, tree)
                return
            if not isinstance(node, dict):
                return
            for key, subtree in tree.items():
                if key not in node:
                    continue
                child = node[key]
                if subtree is None:
                    if isinstance(child, hx_internal_OverrideNode):
                        continue
                    override_node = hx_internal_OverrideNode()
                    if isinstance(child, dict):
                        if "calculated" not in child and "override" not in child:
                            child = {"calculated": child}
                        for override_key, override_value in child.items():
                            if override_key in ("selected", "is_overridden"):
                                continue
                            if override_key in override_node._override_children:
                                setattr(override_node, override_key, override_value)
                    else:
                        override_node.calculated = child
                    node[key] = override_node
                else:
                    if isinstance(child, list):
                        for item in child:
                            _apply(item, subtree)
                    else:
                        _apply(child, subtree)
 
        def _inflate_exact_override_dicts(node):
            if isinstance(node, list):
                for item in node:
                    _inflate_exact_override_dicts(item)
                return
            if not isinstance(node, dict):
                return
            for key, value in list(node.items()):
                if isinstance(value, hx_internal_OverrideNode):
                    continue
                if isinstance(value, dict):
                    override_keys = {
                        "calculated",
                        "override",
                        "overridden_calculated",
                        "is_overridden",
                        "is_dirty",
                        "selected",
                    }
                    extra_keys = set(value.keys()) - override_keys
                    if not extra_keys:
                        override_node = hx_internal_OverrideNode()
                        for override_key, override_value in value.items():
                            if override_key in override_node._override_children:
                                setattr(override_node, override_key, override_value)
                        node[key] = override_node
                    else:
                        _inflate_exact_override_dicts(value)
                else:
                    _inflate_exact_override_dicts(value)
 
        _apply(payload, override_tree)
        _inflate_exact_override_dicts(payload)


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

        # Get expiring data
        expiring_policy_option = hx_renew_api.snapshots.get_snapshot(expiring_policy_option_id).json()["data"]
        expiring_policy_option.pop("bug_report", None)
        cds = expiring_policy_option.setdefault("cds", {})
        review_type = cds.setdefault("review_type", {})

        review_type.setdefault("rater_priced", True)
        review_type.setdefault("private_priced", False)


        if "bridge_override" in expiring_policy_option.get("cds", {}):
            for key in ["bridge_override", "bridge_premium"]:
                expiring_policy_option['cds'].pop(key, None)

        if "broker_dropdown" in expiring_policy_option.get("cds", {}):
            for key in ["broker_dropdown", "us_broker_dropdown"]:
                expiring_policy_option['cds'].pop(key, None)
            for key in ["sector_dropdown", "sic_dropdown", "sic_dropdown_2", "sic_dropdown_3"]:
                expiring_policy_option['cds']['key_industry'].pop(key, None)

        # Initialise list to store sequentially updated values
        updated_values = []
        ##############################
        data_schema_parser = DataSchemaStaticParser(data_schema_path=self.data_schema_static_path, files_path="transient_hxd_files")
        self._inflate_override_nodes(expiring_policy_option, data_schema_parser.get_overrides())
        ################################
        self.expiring_hxd = init_transient_hxd(expiring_policy_option, data_schema_static_path=self.data_schema_static_path)

        # Updating with everything not in buckets:
        # data_schema = DataSchemaStaticParser(data_schema_path=self.data_schema_static_path, files_path="transient_hxd_files")
        ################
        data_schema = data_schema_parser
        ###############
        inputs = data_schema.get_inputs() + data_schema.get_overrides()
        # sorted_paths = sorted(defaults.keys())
        sorted_paths = sorted([x.replace(".", "/") for x in inputs])

        # Exclude bucket items
        bucket_paths = [x for xs in [bucket[1] for bucket in self.buckets.items()] for x in xs]

        # Replace non-bucket items
        replace_paths = [x for x in sorted_paths if x not in bucket_paths]
        #for path in sorted_paths: #JD?: I changed this from "sorted_paths" to "replace_paths". Otherwise it was overwriting the fields in the buckets too
        for path in replace_paths:
            if not isinstance(rgetattr(self.expiring_hxd, path, splitter="/"), hx_internal_StructureNode):
                print(path)
                self._update_expiring_hxd(self.expiring_hxd, path)

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
                hxd_target = self.rc_hxds[bucket_name]

                        
                ######################
                
                EXPIRING_AGGREGATE_OVERRIDES = {
                    "cds/exposure/aggregate/market_cap": "market_cap",
                    "cds/exposure/aggregate/insider_share": "insider_share",
                    "cds/exposure/aggregate/revised_market_cap": "revised_market_cap",
                }


                active_cov = "side_a" if self.hxd.cds.is_side_a else "abc"

                EXPIRING_LAYER_OVERRIDES = {
                    f"cds/layers/coverages/{active_cov}/limit": "limit",
                    f"cds/layers/coverages/{active_cov}/deductible": "deductible",
                    f"cds/layers/coverages/{active_cov}/brokerage": "brokerage",
                }

                if self.hxd.cds.is_side_a:
                    EXPIRING_LAYER_OVERRIDES.update({
                        "cds/layers/coverages/side_a/excess": "side_a_excess",
                        "cds/layers/coverages/side_a/tower": "abc_tower",
                    })
                else:
                    EXPIRING_LAYER_OVERRIDES.update({
                        "cds/layers/coverages/abc/excess": "excess",
                    })


                # ---- PAD EXPIRING LAYERS (TARGET ONLY) ----
                renewal_len = len(self.hxd.cds.layers)
                exp_layers = hxd_target.cds.layers
                if len(exp_layers) < renewal_len:
                    exp_layers._pad_with_default(renewal_len - len(exp_layers))

                # ---- AGGREGATE OVERRIDES ----
                for hxd_path, rc_attr in EXPIRING_AGGREGATE_OVERRIDES.items():
                    selected_vals = {
                        getattr(layer.rate_change, rc_attr).expiring.selected
                        for layer in self.hxd.cds.layers
                    }

                    if len(selected_vals) > 1:
                        hx.errors.validation(f"Inconsistent selected values for {rc_attr}")

                    rsetattr(hxd_target, hxd_path, selected_vals.pop(), splitter="/")

                # ---- LAYER OVERRIDES ----
                for idx, layer in enumerate(self.hxd.cds.layers):
                    for hxd_path, rc_attr in EXPIRING_LAYER_OVERRIDES.items():
                        selected_val = getattr(layer.rate_change, rc_attr).expiring.selected
                        rsetattr(hxd_target, hxd_path, selected_val, splitter="/", list_items=[idx])

                ###################
            else:
                self.rc_hxds[bucket_name] = deepcopy(self.rc_hxds[previous_bucket])  # Start from previous bucket so changes are cumulative 

            for path in paths:
                self._update_expiring_hxd(self.rc_hxds[bucket_name], path)

            ### --- REPRICING
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
        if not self.current_actual_prem:
            current_actual_prem = self.expiring_actual_prem

        # Shorten names and get layers
        expiring_layers_list = rgetattr(self.expiring_hxd, self.layers_path, splitter="/")
        current_layers_list = rgetattr(self.hxd, self.layers_path, splitter="/")

        # Create DataFrame to calculate changes
        layers_list = [
            {
                "current_layer_id": idx + 1,
                "expiring_layer_id": layer.rate_change.expiring_layer,
                "current_actual": getattr(layer, current_actual_prem),
                "current_technical": getattr(layer, current_technical_prem)
            } 
            for idx, layer in enumerate(current_layers_list)
        ]
        rarc_df = pd.DataFrame(layers_list)

        # Add technical premiums to the df
        for bucket_name in self.buckets.keys():
            rc_layers_list = rgetattr(self.rc_hxds[bucket_name], self.layers_path, splitter="/")
            rc_premium_list = [getattr(layer, self.expiring_technical_prem) for idx, layer in enumerate(rc_layers_list)]
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
