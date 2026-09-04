
import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_rms(cds):
        
    # Extending cds nodes for RMS
    cds.extend_node_rater_defined("cds", {
        "rms": hx.Structure(children={

            "edm_reference_requested"   : hx.Str( mode="output",  view={"label": "EDM Reference Requested"}),
            "use_override"              : hx.Bool( mode="input",  view={"label": "Override EDM Output"}, default=False),
            "rms_uplift_ws"             : hx.Float(mode="output", view={"label": "RMS Uplift WindStorm"}),
            "rms_uplift_eq"             : hx.Float(mode="output", view={"label": "RMS Uplift Earthquake"}),


            "edm_reference_lookup"  : hx.List(mode="input", view={"label": "EDM Reference Lookup"},       children={
                "portnum"               : hx.Str(mode="input", default=None, optionality="optional", view={"label": "PortNum"} ),
            }),

           
            
            "fetch_edm_data_reference_lookup_task_status"   : hx.Str(mode="output", view={"label": "EDM Data Lookup Status"} ),
            "fetch_edm_data_task_status"                    : hx.Str(mode="output", view={"label": "EDM Data Status"}        ),
            
            #lookup table 
            "edm_reference_selected": hx.Str(mode="input",  default=None, optionality="optional", view={"label": "EDM Reference Selected"}, options_data = "../edm_reference_lookup", options_field = "portnum" ),


            # Building the EDM table
            "edm": hx.List(mode="input", children={
                "return_period"     : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Return Period"}),
                "probability"       : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Probability"}),
                "portnum"           : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "PortNum"}),
                "ws_loss_amount"    : hx.Float(mode="input", default=None, optionality="optional", view={"label": "WS 100% contract AEP",   "format":thousands_format(0)}),
                "ws_premium"        : hx.Float(mode="input", default=None, optionality="optional", view={"label": "WS Premium",             "format":thousands_format(0)}),
                "ws_currency"       : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "WS Currency"}),
                "ws_fxrate"         : hx.Float(mode="input", default=None, optionality="optional", view={"label": "WS FX Rate",             "format":thousands_format(3)}),
                "eq_loss_amount"    : hx.Float(mode="input", default=None, optionality="optional", view={"label": "EQ 100% contract AEP",   "format":thousands_format(0)}),
                "eq_premium"        : hx.Float(mode="input", default=None, optionality="optional", view={"label": "EQ Premium",             "format":thousands_format(0)}),
                "eq_currency"       : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "EQ Currency"}),
                "eq_fxrate"         : hx.Float(mode="input", default=None, optionality="optional", view={"label": "EQ FX Rate",             "format":thousands_format(3)}),
            }),

            "edm_summary": hx.Structure(children={

                # tried a loop as follows, but failed ... for name_ in ["ws", "eq", "all_peril_calc_at_edm_fx", "all_peril_calc_at_acc_fx", "all_peril_selected_at_acc_fx"]:
                "ws_loss_amount": hx.Structure(view={"label": "WindStorm"}, children={
                    "fx"            : hx.Str(  mode="output", view={"label": "Currency"}),
                    "fxrate"        : hx.Float(mode="output", view={"label": "Currency Conversion Rate",                                    "format":thousands_format(3)}),
                    "aal"           : hx.Float(mode="output", view={"label": "AAL ",                                                        "format":thousands_format(0)}),
                    "std_dev"       : hx.Float(mode="output", view={"label": "Standard Deviation",                                          "format":thousands_format(0)}),
                    "prem"          : hx.Float(mode="output", view={"label": "Associated Premium",                                          "format":thousands_format(0)}),
                    "coeff_var"     : hx.Float(mode="output", view={"label": "Coefficient of Variation",                                    "format":percent_format(1)}),
                    "gross_lr"      : hx.Float(mode="output", view={"label": "Gross Loss Ratio",                                            "format":percent_format(1)}),
                }),
  
                "eq_loss_amount": hx.Structure(view={"label": "Earthquake"}, children={
                    "fx"            : hx.Str(  mode="output", view={"label": "Currency"}),
                    "fxrate"        : hx.Float(mode="output", view={"label": "Currency Conversion Rate",                                    "format":thousands_format(3)}),
                    "aal"           : hx.Float(mode="output", view={"label": "AAL ",                                                        "format":thousands_format(0)}),
                    "std_dev"       : hx.Float(mode="output", view={"label": "Standard Deviation",                                          "format":thousands_format(0)}),
                    "prem"          : hx.Float(mode="output", view={"label": "Associated Premium",                                          "format":thousands_format(0)}),
                    "coeff_var"     : hx.Float(mode="output", view={"label": "Coefficient of Variation",                                    "format":percent_format(1)}),
                    "gross_lr"      : hx.Float(mode="output", view={"label": "Gross Loss Ratio",                                            "format":percent_format(1)}),
                }),

                "all_peril_calc_at_edm_fx": hx.Structure(view={"label": "All Peril - Calc - EDM Fx"}, children={
                    "fx"            : hx.Str(  mode="output", view={"label": "Currency"}),
                    "fxrate"        : hx.Float(mode="output", view={"label": "Currency Conversion Rate",                                    "format":thousands_format(3)}),
                    "aal"           : hx.Float(mode="output", view={"label": "AAL ",                                                        "format":thousands_format(0)}),
                    "std_dev"       : hx.Float(mode="output", view={"label": "Standard Deviation",                                          "format":thousands_format(0)}),
                    "prem"          : hx.Float(mode="output", view={"label": "Associated Premium",                                          "format":thousands_format(0)}),
                    "coeff_var"     : hx.Float(mode="output", view={"label": "Coefficient of Variation",                                    "format":percent_format(1)}),
                    "gross_lr"      : hx.Float(mode="output", view={"label": "Gross Loss Ratio",                                            "format":percent_format(1)}),
                }),

                "all_peril_calc_at_acc_fx": hx.Structure(view={"label": "All Peril - Calc - Account Fx"}, children={
                    "fx"            : hx.Str(  mode="output", view={"label": "Currency"}),
                    "fxrate"        : hx.Float(mode="output", view={"label": "Currency Conversion Rate",                                    "format":thousands_format(3)}),
                    "aal"           : hx.Float(mode="output", view={"label": "AAL ",                                                        "format":thousands_format(0)}),
                    "std_dev"       : hx.Float(mode="output", view={"label": "Standard Deviation",                                          "format":thousands_format(0)}),
                    "prem"          : hx.Float(mode="output", view={"label": "Associated Premium",                                          "format":thousands_format(0)}),
                    "coeff_var"     : hx.Float(mode="output", view={"label": "Coefficient of Variation",                                    "format":percent_format(1)}),
                    "gross_lr"      : hx.Float(mode="output", view={"label": "Gross Loss Ratio",                                            "format":percent_format(1)}),
                }),

                "all_peril_selected_at_acc_fx": hx.Structure(view={"label": "All Peril - Selected - Account Fx"}, children={
                    "fx"            : hx.Str(  mode="output", view={"label": "Currency"}),
                    "fxrate"        : hx.Float(mode="output", view={"label": "Currency Conversion Rate",                                    "format":thousands_format(3)}),
                    "aal"           : hx.Float(mode="output", view={"label": "AAL ",                                                        "format":thousands_format(0)}),
                    "std_dev"       : hx.Float(mode="output", view={"label": "Standard Deviation",                                          "format":thousands_format(0)}),
                    "prem"          : hx.Float(mode="output", view={"label": "Associated Premium",                                          "format":thousands_format(0)}),
                    "coeff_var"     : hx.Float(mode="output", view={"label": "Coefficient of Variation",                                    "format":percent_format(1)}),
                    "gross_lr"      : hx.Float(mode="output", view={"label": "Gross Loss Ratio",                                            "format":percent_format(1)}),
                }),

                "all_peril_override_at_acc_fx": hx.Structure(view={"label": "All Peril - Override - Account Fx"}, children={
                    "fx"            : hx.Str(  mode="output", view={"label": "Currency"}),
                    "fxrate"        : hx.Float(mode="output", view={"label": "Currency Conversion Rate",                                    "format":thousands_format(3)}),
                    "aal"           : hx.Float(mode="input", view={"label": "AAL ",                                                         "format":thousands_format(0)}, default=None, optionality="optional"),
                    "std_dev"       : hx.Float(mode="input", view={"label": "Standard Deviation",                                           "format":thousands_format(0)}, default=None, optionality="optional"),
                    "prem"          : hx.Float(mode="input", view={"label": "Associated Premium",                                           "format":thousands_format(0)}, default=None, optionality="optional"),
                    "coeff_var"     : hx.Float(mode="output", view={"label": "Coefficient of Variation",                                    "format":percent_format(1)}),
                    "gross_lr"      : hx.Float(mode="output", view={"label": "Gross Loss Ratio",                                            "format":percent_format(1)}),
                }),
            }),


            "edm_epcurve": hx.List(mode="input", default_element_count=12, children={
                "return_period_label"           : hx.Str(  mode="output", view={"label": "Return Period"}),
                "return_period"                 : hx.Float(mode="output", view={"label": "Return Period",                                   "format":thousands_format(0)}),
                "probability"                   : hx.Float(mode="output", view={"label": "Probability"}),
                "ws_loss_amount"                : hx.Float(mode="output", view={"label": "WindStorm",                                       "format":thousands_format(0)}),
                "eq_loss_amount"                : hx.Float(mode="output", view={"label": "Earthquake",                                      "format":thousands_format(0)}),
                "all_peril_calc_at_edm_fx"      : hx.Float(mode="output", view={"label": "All Peril - Calc - EDM Fx",                       "format":thousands_format(0)}),
                "all_peril_calc_at_acc_fx"      : hx.Float(mode="output", view={"label": "All Peril - Calc - Account Fx",                   "format":thousands_format(0)}),
                "all_peril_selected_at_acc_fx"  : hx.Float(mode="output", view={"label": "All Peril - Selected - Account Fx",               "format":thousands_format(0)}),
                "all_peril_override_at_acc_fx"  : hx.Float(mode="input",  view={"label": "All Peril - Override - Account Fx",               "format":thousands_format(0)},  default=None, optionality="optional"),
            }),




        })
    })
