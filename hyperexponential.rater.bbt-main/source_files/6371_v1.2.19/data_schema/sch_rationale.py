##############################################################################################################################
################                             NOTES                                                            ################ 
##############################################################################################################################


import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format

def sch_rationale(cds):

    cds.extend_node_rater_defined("cds", {
        "rationale": hx.Structure(children={
            "actuarial_review"              : hx.Str(mode="input", default="No",                         view={"label": "Actuarial Reviewed?"},       options_table="lst_yn", options_column="YesNo"),
            "actuarial_notes"               : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Actuarial Commentary"}),
            "actuarial_view"                : hx.Bool(mode="input", default=False,                       view={"label": "Keep Actuarial view active:"}),
            "help_file"                     : hx.Str(mode="output",                                      view={"label": "Help file"}),
        })
    })
 
