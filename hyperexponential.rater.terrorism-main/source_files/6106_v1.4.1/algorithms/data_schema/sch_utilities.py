import hx_data_schema as hx

# Get node function from existing node
def hx_node(existing_node):
    # Map from the class type to the corresponding hx function
    node_type_map = {
        "BoolNode": hx.Bool,
        "FloatNode": hx.Float,
        "IntNode": hx.Int,
        "StrNode": hx.Str,
        "DateNode": hx.Date
    }

    # Get the type name of the existing node
    node_type_name = type(existing_node).__name__
    
    # Map to the hx function
    hx_function = node_type_map.get(node_type_name)

    return hx_function

def get_existing_attributes(obj, node_names):
    return {
        node_name: getattr(obj, node_name)
        for node_name in node_names if hasattr(obj, node_name)
    }

### --- Standard utilities
def thousands_format(mantissa=0, trimMantissa=False):
    return {"thousandSeparated": True, "mantissa": mantissa, "trimMantissa": trimMantissa}

def percent_format(mantissa=0):
    return {"output": "percent", "mantissa": mantissa}

def integer_format(mantissa=0):
    return {"thousandSeparated": False, "mantissa": mantissa}


def clean_string(string):
    string = ''.join(letter for letter in string if letter.isalnum())
    string = string.lower()

    return string 
    
def remove_spaces_string(string):
    string = string.replace(" ", "_")
    string = string.replace("-", "_")
    string = string.lower()

    return string

def clean_string_heading(string):
    string = ' '.join(letter for letter in string if letter.isalnum())
    string = string.title()

    return string
 
def title_rc(string):
    string = string.replace("_and_"," & ")
    string = string.replace("_"," ")
    string = string.title()

    return string