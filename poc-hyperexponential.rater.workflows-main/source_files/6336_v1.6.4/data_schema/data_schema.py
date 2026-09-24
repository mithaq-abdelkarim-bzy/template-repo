import hx_data_schema as hx


@hx.data_schema
def data_schema():
    return hx.Structure(
        children={
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
            "k": hx.Float(mode="input", default=0, view={"label": "Input j - v1.6.4"})
        }
    )
