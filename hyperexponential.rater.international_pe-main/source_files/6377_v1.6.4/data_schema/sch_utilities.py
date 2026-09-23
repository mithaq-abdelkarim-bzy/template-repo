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