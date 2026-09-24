import hx_data_schema as hx
from data_schema.sch_utilities import percent_format


def modifiers_selection():
    return {
        "rationale": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Rationale"},
        ),
        "factor_selection": hx.Float(
            mode="override",            
            optionality="optional",
            view={"label": "Factor Selection", "format": percent_format(0)},
        ),
        "min": hx.Float(
            mode="output",
            view={"label": "Min", "format": {"output": "percent", "mantissa": 0}},
        ),
        "max": hx.Float(
            mode="output",
            view={"label": "Max", "format": {"output": "percent", "mantissa": 0}},
        ),
    }

def modifiers_selection_inputs():
    return {
        "rationale": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Rationale"},
        ),
        "factor_selection": hx.Float(
            mode="input",
            default=None,            
            optionality="optional",
            view={"label": "Factor Selection", "format": percent_format(0)},
        ),
        "min": hx.Float(
            mode="output",
            view={"label": "Min", "format": {"output": "percent", "mantissa": 0}},
        ),
        "max": hx.Float(
            mode="output",
            view={"label": "Max", "format": {"output": "percent", "mantissa": 0}},
        ),
    }    


def modifiers_factor_selection():
    return {
        "factor_selection_nm": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={
                "label": "Factor Selection",
                "group": "Non-Admitted",
                "format": percent_format(0),
            },
        ),
        "min_nm": hx.Float(
            mode="output",
            view={"label": "Min", "group": "Non-Admitted", "format": percent_format(0)},
        ),
        "max_nm": hx.Float(
            mode="output",
            view={"label": "Max", "group": "Non-Admitted", "format": percent_format(0)},
        ),
    }

def factor_selection():
    return {
        "rationale": hx.Str(mode="output", view={"label": "Rationale"}),
        "factor_selection": hx.Float(
            mode="override",
            optionality="optional",            
            view={
                "label": "Factor Selection",
                "format": {"output": "percent", "mantissa": 0},
            },
        ),
        "min": hx.Float(
            mode="output",
            view={"label": "Min", "format": {"output": "percent", "mantissa": 0}},
        ),
        "max": hx.Float(
            mode="output",
            view={"label": "Max", "format": {"output": "percent", "mantissa": 0}},
        ),
        "out_of_range": hx.Str(mode="output", view={"label": "Out of Range"}),
    }

def coinsurance():
    return {
        "selection": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Selection", "format": {"output": "percent", "mantissa": 0}},
        ),
        "max_credit": hx.Float(
            mode="output",           
            view={
                "label": "Max Credit",
                "format": {"output": "percent", "mantissa": 0},
            },
        ),
    }    