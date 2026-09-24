import hx_data_schema as hx

def sch_validations():
    """
    These nodes are validation nodes for the different percentage that are getting updated. If a percentage value is not supported anymore, 
    the field will be marked in a warning color and an appropriate info text will be displayed. 
    """
    return {
        "validation":hx.Structure(children={
            "location_percentage": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),
            "engineering_disp_percentage": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),
            "contractor_disp_percentage": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),
            "fee_percentage": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),
        })
    }
    
