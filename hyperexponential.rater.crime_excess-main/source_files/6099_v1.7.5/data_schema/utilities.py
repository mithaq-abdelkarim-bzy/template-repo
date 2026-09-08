import hx_data_schema as hx

def thousands_format(mantissa = 0):
    return {"thousandSeparated": True, "mantissa": mantissa}

def percent_format(mantissa = 0):
    return {"output": "percent", "mantissa": mantissa}

def integer_format(mantissa = 0):
    return {"thousandSeparated": False, "mantissa": mantissa}

