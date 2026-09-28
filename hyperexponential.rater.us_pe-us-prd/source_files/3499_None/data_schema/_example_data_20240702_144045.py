import hx_data_schema as hx


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        "a": hx.Int(mode="input", default=0, view={"label": "A"}),
        "b": hx.Int(mode="input", default=0, view={"label": "B"}),
        "c": hx.Int(mode="input", default=0, view={"label": "C"}),
    })
