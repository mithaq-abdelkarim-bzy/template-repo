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



def create_node(label='', mode='input', format=thousands_format(0), type='float', default=None, group=None, options=[], async_input=[], async_output=[], is_read_only=False, allow_custom_value=None, hx_calc=False):
    node = {'mode': mode, 'view': {"label": label, "format": format}}
    if is_read_only:
        node['view']["options"] = {"read_only_option": {"read_only": True}}

    if hx_calc:
        node['view']["style_column"] = "hx-calculation"


    if allow_custom_value:
        node["allow_custom_value"] = allow_custom_value


    if len(async_input):
        node['async_input'] = async_input
    if len(async_output):
        node['async_output'] = async_output

    if type == 'bool':
        node['mode'] = mode
        if mode == 'input':
            node['default'] = default
        if group is not None:
            node['view']['group'] = group
        return hx.Bool(**node)

    if mode == 'input' or mode == 'override':
        if len(options) == 0 and mode == 'input':
            node['optionality'] = 'optional'
            if default is not None:
                node['default'] = default
            else:
                node['default'] = None
        elif len(options):
            if mode == 'input':
                if default:
                    node['default'] = default
                else:
                    node['default_index'] = 0
            if '/' in options:
                options_table,  options_column = options.split('/')
                node['options_table'] = options_table
                node['options_column'] = options_column
            else:
                node['options'] = options

    if group is not None:
        node['view']['group'] = group

    if type == 'float':
        return hx.Float(**node)
    if type == 'int':
        return hx.Int(**node)
    elif type == 'str':
        node['view']['format'] = {"thousandSeparated": False, "mantissa": 0}
        return hx.Str(**node)