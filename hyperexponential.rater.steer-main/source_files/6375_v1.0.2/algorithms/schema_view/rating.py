import hx_data_schema as HX
import hx
import json
import datetime

def schema_view_rating(hxd: HX.Structure):
    """
    This function is to restrict the use in editing mode only, 
    when it is a test/live policy the compoent will be hidden.
    """
    hxd.schema_view.show_view = not hx.meta.policy_id
    if not hx.meta.policy_id:
        hxd.schema_view.stringified_json = hxd_to_json(hxd=hxd)

def hxd_to_json(hxd: hx.Hxd):
    """Entry to the recursive function."""

    def _hxd_to_json(hxd_dict: dict):
        """Main function that handles the conversion."""
        try:
            for key, value in list(hxd_dict.items()):
                # If standalone field then pass as already in the correct form
                if isinstance(value, (str, float, int, bool, datetime.date, type(None))): 
                    pass
                elif hasattr(value, "is_overridden"): # Override Nodes
                    hxd_dict[key] = {"calculated": value.calculated, "selected": value.selected}
                elif hasattr(value, "__len__") and hasattr(value, "append"): # List Nodes
                    hxd_dict[key] = [_hxd_to_json(dict(element)) for element in value]
                else:
                    try:
                        hxd_dict[key] = _hxd_to_json(dict(value)) # For Structure Node
                    except: # Triangle or File Node
                        del hxd_dict[key]
        except:
            hxd_dict = {}
        return hxd_dict

    hxd_dict = dict(hxd)
    formatted_hxd_dict = _hxd_to_json(hxd_dict=hxd_dict)
    return json.dumps(formatted_hxd_dict, default=str)