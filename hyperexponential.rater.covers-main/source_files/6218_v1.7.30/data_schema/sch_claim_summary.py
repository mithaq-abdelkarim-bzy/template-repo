########################################################################################################################
####################                        OUTSTANDING                                             ####################
########################################################################################################################

########################################################################################################################


import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_claim_summary(cds):
        
    # Extending cds nodes for RMS
    cds.extend_node_rater_defined("cds", {

        "claim_summary": hx.Structure(children={

            "top15_cat_events": hx.List(mode="output", view={"label": "Top 15 Cat Events - @100% in Settlement Fx"}, children={
                "show_row"          : hx.Bool(mode="output",    view={"label": "Show Hide"}),
                "cat_tot_rank"      : hx.Float(mode="output",   view={"label": "Cat Rank",                              "format":thousands_format(0)}),
                "beazley_catcode"   : hx.Str(mode="output",     view={"label": "Cat code"}),
                "bi_paid"           : hx.Float(mode="output",   view={"label": "BI Paid",                               "format":thousands_format(0)}),
                "bi_os"             : hx.Float(mode="output",   view={"label": "BI OS",                                 "format":thousands_format(0)}),
                "bi_incurred"       : hx.Float(mode="output",   view={"label": "BI Incurred",                           "format":thousands_format(0)}),
                "pre_peer_blend_incurred"       : hx.Float(mode="output", view={"label": "Pre Peer Blend Incurred",     "format":thousands_format(0)}),
                "pre_peer_most_likely_incurred" : hx.Float(mode="output", view={"label": "Pre Peer most likely Incurred","format":thousands_format(0)}),
            }),

            "chart_freq_sev": hx.List(mode="output", view={"label": "Large Loss Freq/Sev Trends @100% in Settlement Fx"}, children={
                "show_row"          : hx.Bool( mode="output", view={"label": "Show Hide"}),
                "yoa_label"         : hx.Str(  mode="output", view={"label": "YOA"}),
                "yoa"               : hx.Float(mode="output", view={"label": "YOA",                         "format":integer_format(0)}),
                "premium"           : hx.Float(mode="output", view={"label": "Premium",                     "format":thousands_format(0)}),
                "freq_per_million"  : hx.Float(mode="output", view={"label": "Freq per Million Premium",    "format":thousands_format(3)}),
                "severity"          : hx.Float(mode="output", view={"label": "Avg Severity",                "format":thousands_format(0)}),
            }),
        })
    })




