import hx_data_schema as hx
import data_schema.utilities as utils

def sch_exposure_change(cds):
    cds.extend_node_rater_defined("cds", {
        "exposure_change": hx.Structure(children={
            "employee_count": hx.Structure(view={"label": "Employee Count"}, children={
                "renewal": hx.Float(mode="input", default=0, view={"label": "Renewal"}),
                "expiry": hx.Float(mode="input", default=0, view={"label": "Expiry"})
            }),
            "location_count":hx.Structure(view={"label":"Location Count"},children={
                "renewal":hx.Float(mode="input", default=0, view={"label": "Renewal"}),
                "expiry": hx.Float(mode="input", default=0, view={"label": "Expiry"})
            })
        })
    }) 