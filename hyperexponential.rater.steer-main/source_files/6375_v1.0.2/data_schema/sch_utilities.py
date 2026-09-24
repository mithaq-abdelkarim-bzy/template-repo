# v0.5.0
import hx_data_schema as hx


def thousands_format(mantissa = 0):
    return {"thousandSeparated": True, "mantissa": mantissa}

def percent_format(mantissa = 0):
    return {"output": "percent", "mantissa": mantissa}

def integer_format(mantissa = 0):
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

def create_node_from_list(node_info_list):
    """
    Assist the creation of hx node from node_info_list, a list of tuples.
    Tuple input order:
    - field_name - string
    - hx.type - not a string. In line with the type of node in hx.
    - default=None if no default provided or mode = "output". Must be provided if mode = "input"
    - format=None if no format provided
    - async_input - string or list of strings
    - async_output - string or list of strings
    - optionality (optional) - if provided "optional" as the last item of the tuple. This adds the "optionality" key to the kwargs
    """
    result_dict = {}

    for item in node_info_list:
        if len(item) == 7:
            (field_name, hx_type, mode, default, format, async_input, async_output) = item
        elif len(item) == 8:
            (field_name, hx_type, mode, default, format, async_input, async_output, optionality) = item

        formatted_field_name, label_name = format_field_name_label_name(field_name)

        # Build the view dictionary
        view = {"label": label_name}
        # view = {"label": field_name}

        if format is not None:
            view["format"] = format

        # Build the kwargs for hx_type
        kwargs = {"mode": mode, "view": view}
        if mode == "input":
            kwargs["default"] = default

        # Handle async_input: convert string to list if necessary
        if async_input is not None:
            if isinstance(async_input, str):
                kwargs["async_input"] = [async_input]
            else:
                kwargs["async_input"] = async_input

        # Handle async_output: convert string to list if necessary
        if async_output is not None:
            if isinstance(async_output, str):
                kwargs["async_output"] = [async_output]
            else:
                kwargs["async_output"] = async_output

        if len(item) == 8 and optionality is not None:
            kwargs["optionality"] = optionality

        # Assign to result_dict
        result_dict[formatted_field_name] = hx_type(**kwargs)

    return result_dict

def format_field_name_label_name(field_name):
    """
    provide field name and label name
    label name will go to the next line if the word exceed 12 characters
    """

    # Convert field_name to snake_case
    formatted_field_name = field_name.lower().replace(" ", "_").replace("-", "_").replace(".", "")
    formatted_field_name_with_capital = field_name.replace(" ", "_").replace("-", "_").replace(".", "")
    
    # convert field_name to Label name
    formatted = formatted_field_name_with_capital.replace('_', ' ')
    for i in range(1, len(formatted)):
        if formatted[i].isupper() and formatted[i-1].islower():
            formatted = formatted[:i] + ' ' + formatted[i:]
    # Capitalize each word and return
    # label_name = ' '.join(word.capitalize() for word in formatted.split())
    label_name = ' '.join(word for word in formatted.split())

    # Split into lines of up to 12 characters, without breaking words
    words = label_name.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) <= 12:
            current_line.append(word)
            current_length += len(word) + 1  # +1 for the space
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)

    if current_line:  # Add the last line if it's not empty
        lines.append(' '.join(current_line))

    formatted_label_name = '\n'.join(lines)

    return formatted_field_name, formatted_label_name
    
def add_year_suffix(node_info_list, experience_rating_max_years):
    result = []
    for item in node_info_list:
        base_name = item[0]
        for year in range(1, experience_rating_max_years + 1):
            new_name = f"{base_name}{year:02d}"
            new_item = (new_name,) + item[1:]
            result.append(new_item)
    return result
