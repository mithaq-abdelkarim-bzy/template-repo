import hx_data_schema as hx

def schema_view():
    return {
        "schema_view": hx.Structure(children={
            "stringified_json": hx.Str(mode="output"),
            "show_view": hx.Bool(mode="output")
        })
    }