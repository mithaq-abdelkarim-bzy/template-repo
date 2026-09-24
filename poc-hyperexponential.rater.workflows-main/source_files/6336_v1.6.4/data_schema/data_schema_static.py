raise Exception("""This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your Data Schema that will allow easier debugging.
""")

import hx_data_schema as hx


@hx.data_schema
def hx_calculation_legacy_initial_premium():
    return hx.Structure(children={
        "a": hx.Float(mode="input", default=1, view={"label": "Input a"}),
        "b": hx.Float(mode="input", default=2, view={"label": "Input b"}),
        "c": hx.Float(mode="output", view={"label": "Output c"}),
        "d": hx.Float(mode="output", view={"label": "Output d"}),
        "e": hx.Float(mode="output", view={"label": "Output e"}),
        "f": hx.Float(mode="output", view={"label": "Output f"}),
        "g": hx.Float(mode="output", view={"label": "Output g"}),
        "h": hx.Float(mode="output", view={"label": "Output h"}),
        "i": hx.Float(mode="input", default=3, view={"label": "Input i "}),
        "j": hx.Float(mode="input", default=4, view={"label": "Input j - v1.3.11"}),
        "k": hx.Float(mode="input", default=0, view={"label": "Input j - v1.6.4"}),
        "hx_core": hx.Structure(children={
            "inception_date": hx.Date(default="2018-01-01", mode="input", view={"label": "Inception Date"}),
            "expiry_date": hx.Date(default="2018-12-31", mode="input", view={"label": "Expiry Date"}),
            "model_premium": hx.Float(mode="output", view={"label": "Model Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "charged_premium": hx.Float(mode="output", view={"label": "Charged Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "premium_currency": hx.Str(mode="output", view={"label": "Premium Currency"}),
            "ulr": hx.Float(mode="output", view={"label": "ULR", "format": {"output": "percent", "mantissa": 1}}),
            "class_code": hx.Str(mode="output", view={"label": "Class Code"}),
        }),
    })
