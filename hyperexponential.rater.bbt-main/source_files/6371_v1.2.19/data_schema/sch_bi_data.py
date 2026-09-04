########################################################################################################################
####################                        OUTSTANDING                                             ####################
########################################################################################################################
###                                                                                                                  ###
###                                                                                                                  ###
###                                                                                                                  ###
########################################################################################################################


import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format


def sch_bi_data(cds):
        
    # Extending cds nodes for RMS
    cds.extend_node_rater_defined("cds", {

        "bi_data": hx.Structure(children={
            "fetch_clm_and_mvmt_detail_task_status"     : hx.Str(mode="output", view={"label": "Status - Load Historic Claims"}),
            "fetch_facility_detail_task_status"         : hx.Str(mode="output", view={"label": "Status - Load Historic Binders"}),
            "include_all_facility_references"           : hx.Bool(mode="input", default=True,  view={"label": "Include all binder references?"}),
            "triangles_loaded"                          : hx.Bool(mode="output", view={"label": "Triangles Loaded"}),

            # listing of individual facilities (technically section references)
            "facility_detail": hx.List(mode="input", children={
                "include"                               : hx.Bool(mode="input", default=False, view={"label": "Include?"}),
                "date_extracted"                        : hx.Date(mode="input", default=None,   optionality="optional", view={"label": "CreatedTimeStamp"}),
                "section_reference"                     : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Section Reference"}),
                "insured_party"                         : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Insured Party"}),
                "inception_date"                        : hx.Date(mode="input", default=None,   optionality="optional", view={"label": "Inception Date"}),
                "expiry_date"                           : hx.Date(mode="input", default=None,   optionality="optional", view={"label": "Expiry Date"}),
                "underwriter_name"                      : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Underwriter Name"}),
                "settlement_currency"                   : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Settlement Currency"}),
                "section_is_renewal"                    : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Section Is Renewal"}),
                "division"                              : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Division"}),
                "written_or_estimated_signed_line"      : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Written Or Estimated Signed Line",          "format":percent_format(2)}),
                "trifocus_name"                         : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Trifocus Name"}),
                "external_acquisition_cost_multiplier"  : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "External Acquisition Cost Multiplier",      "format":percent_format(2)}),
                "profit_commission_multiplier"          : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Profit Commission Multiplier",              "format":percent_format(2)}),
                "placing_brokername"                    : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Placing Brokername"}),
                "risk_class_code"                       : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Risk Class Code"}),
                "yoa"                                   : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Year of Account",                           "format":integer_format(0)}),
                "written_or_estimated_premium"          : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "AFB Net Premium",                           "format":thousands_format(0)}),
                "rate_change_divisor"                   : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Rate Change Multiplier",                    "format":percent_format(2)}),            
                "spot_rate_usd_to_sett"                 : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Spot Rate USD to Settlement Fx",            "format":integer_format(3)}),
                "net_beazley_premium_sett_fx"           : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Net Beazley Premium @ Settlement Fx",       "format":thousands_format(0)}),
                "net_100pct_premium_sett_fx"            : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Net 100pct Premium @ Settlement Fx",        "format":thousands_format(0)}),
                "gross_100pct_premium_sett_fx"          : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Gross 100pct Premium @ Settlement Fx",      "format":thousands_format(0)}),
                "net_100pct_premium_adjexp_sett_fx"     : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Net 100pct Adjusted Expiring Premium @ Settlement Fx",  "format":thousands_format(0)}),
            }),

 
            # listing of individual claims (technically exposure references) for all selected facilities
            "claims_listing"            : hx.List(mode="input", children={
                    'date_extracted'                    : hx.Date(mode="input",  default=None,   optionality="optional", view={"label": "Date Extracted"}),
                    'section_reference'                 : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Section Reference"}),
                    'claim_reference'                   : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Claim Reference"}),
                    'exposure_reference'                : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Exposure Reference"}),
                    'yoa'                               : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "YOA",                              "format":integer_format(0)}),
                    'beazley_catcode'                   : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Beazley CatCode"}),
                    'market_catcode'                    : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Market CatCode"}),
                    'trifocus_name'                     : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "TriFocus Name"}),
                    'settlement_currency'               : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Settlement Currency"}),
                    'block_indicator'                   : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Block Indicator"}),
                    'date_of_loss'                      : hx.Date(mode="input",  default=None,   optionality="optional", view={"label": "Date Of Loss"}),
                    'claim_made_date'                   : hx.Date(mode="input",  default=None,   optionality="optional", view={"label": "Claim Made Date"}),
                    'claim_or_circumstance'             : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Claim Or Circumstance"}),
                    'beazley_share_total_incurred'      : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Beazley Share Total Incurred",     "format":thousands_format(0)}),
                    'slip_order_total_incurred'         : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Slip Order Total Incurred",        "format":thousands_format(0)}),
                    'slip_order_total_paid'             : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Slip Order Total Paid",            "format":thousands_format(0)}),
                    'beazley_share_pre_peer_blend'      : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Beazley Share Pre Peer Blend",     "format":thousands_format(0)}),
                    'beazley_share_pre_peer_most_likely': hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Beazley Share Pre Peer Most Likely","format":thousands_format(0)}),
                    'loss_category'                     : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Loss Category"}),
                    'bi_paid'                           : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "BI Paid",                          "format":thousands_format(0)}),
                    'bi_os'                             : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "BI OS",                            "format":thousands_format(0)}),
                    'bi_incurred'                       : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "BI Incurred",                      "format":thousands_format(0)}),
                    'pre_peer_blend_incurred'           : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Pre Peer Blend Incurred",          "format":thousands_format(0)}),
                    'pre_peer_most_likely_incurred'     : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Pre Peer most likely Incurred",    "format":thousands_format(0)}),
                    'show_cat'                          : hx.Bool(mode="input",  default=None,   optionality="optional", view={"label": "Show Cat"}),
                    'show_large'                        : hx.Bool(mode="input",  default=None,   optionality="optional", view={"label": "Show Large"}),
                    'class_rank'                        : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Rank",                             "format":thousands_format(0)}),
            }),



            # listing of individual claims movements (technically exposure references) for all selected facilities
            "claims_movements": hx.List(mode="input", children={
                    'date_extracted'            : hx.Date(mode="input",  default=None,   optionality="optional", view={"label": "Date Extracted"}),
                    'loss_category'             : hx.Str(mode="input",   default=None,   optionality="optional", view={"label": "Loss Category"}),
                    'yoa'                       : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "YOA",                                      "format":integer_format(0)}),
                    'mvmt_yr'                   : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Movement Year",                            "format":integer_format(0)}),
                    'incurredmvmt_100_sett_fx'  : hx.Float(mode="input", default=None,   optionality="optional", view={"label": "Incurred Movement",                        "format":thousands_format(0)}),
            }),

        })
    })





