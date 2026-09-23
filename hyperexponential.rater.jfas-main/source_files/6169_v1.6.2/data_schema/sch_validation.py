import hx_data_schema as hx
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_validation(cds):
    cds.extend_node_rater_defined("cds", {
        # Validations - for conditional formatting
        "validation": hx.Structure(children={            
            "status": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),                
            }),
            "limit": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),                
            }),
            "excess": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),                
            }),
            "brokerage": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),                
            }),
            "quoted_premium": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),                
            }),
            "sel_exp_weight": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),                
            }),
            "signed_line": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),                
            }),
        }),              
    })
