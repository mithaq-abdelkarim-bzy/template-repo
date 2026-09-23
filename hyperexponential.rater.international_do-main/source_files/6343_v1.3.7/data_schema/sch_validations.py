import hx_data_schema as hx

def sch_validations(cds):
    """
    These nodes are validation nodes for the different dropdowns that are getting updated. If a dropdown value is not supported anymore (going to be removed in the future), 
    the field will be marked in a warning color and an appropriate info text will be displayed. 
    """
    cds.extend_node_rater_defined('cds', {
        "validation":hx.Structure(children={
            # Underwriter name dropdown in Risk Information
            "underwriter": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Underwriting assistant name dropdown in Risk Information
            "underwriting_assistant": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),
            
            # PE backer dropdown in Risk Information
            "pe_backer": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Broker name dropdown in Risk Information
            "broker": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Slip leader in Rating Summary
            "slip_leader": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Status in Rating Summary
            "status": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),
        })
    })
