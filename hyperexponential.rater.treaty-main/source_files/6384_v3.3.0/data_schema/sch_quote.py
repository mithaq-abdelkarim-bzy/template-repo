import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params
from algorithms.rate_constants import rp_peril_options

def sch_quote(cds):
    cds.extend_node_rater_defined("cds",
    {
        "tp_comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),
        "quote_total_usd": hx.Structure(view={"label": "Total (USD)"}, children={
            "quote": hx.Structure(children={
                "rol_ty": hx.Structure(children={
                    "rol_quote": hx.Float(mode="output", optionality="optional", view={"label": "Quoted ROL", "format": utils.thousands_format(0)}),
                    "rol_fot": hx.Float(mode="output", optionality="optional", view={"label": "FOT ROL", "format": utils.thousands_format(0)}),
                    
                    "prem_full_line": hx.Float(mode="output", optionality="optional", view={"label": "Premium 100%", "format": utils.thousands_format(0)}),
                    "written_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format": utils.thousands_format(0)}),
                    "estimated_signing_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Estimated Signing", "format": utils.thousands_format(0)}),
                    "signed_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Signed Line", "format": utils.thousands_format(0)}),
                    "epi_written": hx.Float(mode="output", optionality="optional", view={"label": "Written EPI", "format": utils.thousands_format(0)}),
                    "epi_estimated": hx.Float(mode="output", optionality="optional", view={"label": "Estimated EPI", "format": utils.thousands_format(0)}),
                    "epi_signed": hx.Float(mode="output", optionality="optional", view={"label": "Signed EPI", "format": utils.thousands_format(0)}),                
                }),
                "rol_ly": hx.Structure(children={
                    "rol_quote": hx.Float(mode="output", optionality="optional", view={"label": "Quoted ROL", "format": utils.thousands_format(0)}),
                    "rol_fot": hx.Float(mode="output", optionality="optional", view={"label": "FOT ROL", "format": utils.thousands_format(0)}),

                    "prem_full_line": hx.Float(mode="output", optionality="optional", view={"label": "Premium 100%", "format": utils.thousands_format(0)}),
                    "written_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format": utils.thousands_format(0)}),
                    "estimated_signing_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Estimated Signing", "format": utils.thousands_format(0)}),
                    "signed_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Signed Line", "format": utils.thousands_format(0)}),
                    "epi_written": hx.Float(mode="output", optionality="optional", view={"label": "Written EPI", "format": utils.thousands_format(0)}),
                    "epi_estimated": hx.Float(mode="output", optionality="optional", view={"label": "Estimated EPI", "format": utils.thousands_format(0)}),
                    "epi_signed": hx.Float(mode="output", optionality="optional", view={"label": "Signed EPI", "format": utils.thousands_format(0)}),                   
                }),
            }),
        }),
        "quote": hx.Structure(children={
            "tp_calc_info": hx.Structure(children={
                "description": hx.Structure(view={"label": "Description"}, children={
                    "roc": hx.Str(mode="output", optionality="optional", view={"label": "ROC"}),
                    "lae": hx.Str(mode="output", optionality="optional", view={"label": "LAE"}),
                    "direct_expenses": hx.Str(mode="output", optionality="optional", view={"label": "Direct Expenses"}),
                    "indirect_expenses": hx.Str(mode="output", optionality="optional", view={"label": "Indirect Expenses"}),
                    "ri_cost": hx.Str(mode="output", optionality="optional", view={"label": "RI Cost"}),
                    "inv_income": hx.Str(mode="output", optionality="optional", view={"label": "Investment Income"}),
                    "capital_alloc": hx.Str(mode="output", optionality="optional", view={"label": "Capital Allocated"}),
                    "sd_load": hx.Str(mode="output", optionality="optional", view={"label": "SD Load"}),

                    "tp_calc_1": hx.Str(mode="output", optionality="optional", view={"label": "TP Calc 1"}),
                    "tp_calc_2": hx.Str(mode="output", optionality="optional", view={"label": "TP Calc 2"}),
                    "tp_calc_3": hx.Str(mode="output", optionality="optional", view={"label": "TP Calc 3"}),

                    "general_notes": hx.Str(mode="output", optionality="optional", view={"label": "General Notes"}),
                    "default_line": hx.Str(mode="output", optionality="optional", view={"label": "Default Line"}),
                }),
                "value": hx.Structure(view={"label": "Value"}, children={
                    "roc": hx.Str(mode="output", optionality="optional", view={"label": "ROC"}),
                    "lae": hx.Str(mode="output", optionality="optional", view={"label": "LAE"}),
                    "direct_expenses": hx.Str(mode="output", optionality="optional", view={"label": "Direct Expenses"}),
                    "indirect_expenses": hx.Str(mode="output", optionality="optional", view={"label": "Indirect Expenses"}),
                    "inv_income": hx.Str(mode="output", optionality="optional", view={"label": "Investment Income"}),
                    "sd_load": hx.Str(mode="output", optionality="optional", view={"label": "SD Load"})
                }),
                "value_ly": hx.Structure(view={"label": "LY Value"}, children={                    
                    "roc": hx.Str(mode="output", optionality="optional", view={"label": "ROC"}),
                    "lae": hx.Str(mode="output", optionality="optional", view={"label": "LAE"}),
                    "direct_expenses": hx.Str(mode="output", optionality="optional", view={"label": "Direct Expenses"}),
                    "indirect_expenses": hx.Str(mode="output", optionality="optional", view={"label": "Indirect Expenses"}),
                    "inv_income": hx.Str(mode="output", optionality="optional", view={"label": "Investment Income"}),
                    "sd_load": hx.Str(mode="output", optionality="optional", view={"label": "SD Load"})
                }),
                "ri_cost_ty": hx.Structure(view={"label": "This Year"}, children={
                    "north_east": hx.Float(mode="output",optionality="optional", view={"label": "NE", "format": utils.percent_format(1)}),
                    "mid_atlantic": hx.Float(mode="output",optionality="optional", view={"label": "MID ATLANTIC", "format": utils.percent_format(1)}),
                    "carolinas": hx.Float(mode="output",optionality="optional", view={"label": "CARS", "format": utils.percent_format(1)}),
                    "fl_se": hx.Float(mode="output",optionality="optional", view={"label": "FL SE", "format": utils.percent_format(1)}),
                    "fl_non_se": hx.Float(mode="output", optionality="optional", view={"label": "FL NON SE", "format": utils.percent_format(1)}),
                    "al_miss": hx.Float(mode="output", optionality="optional", view={"label": "AL + MISS", "format": utils.percent_format(1)}),
                    "louisiana": hx.Float(mode="output", optionality="optional", view={"label": "LOUISIANA", "format": utils.percent_format(1)}),
                    "tx_east": hx.Float(mode="output", optionality="optional", view={"label": "TX EAST", "format": utils.percent_format(1)}),
                    "tx_west": hx.Float(mode="output", optionality="optional", view={"label": "TX WEST", "format": utils.percent_format(1)}),
                    "cal_south": hx.Float(mode="output", optionality="optional", view={"label": "CAL SOUTH", "format": utils.percent_format(1)}),
                    "cal_north": hx.Float(mode="output", optionality="optional", view={"label": "CAL NORTH", "format": utils.percent_format(1)}),
                    "pnw": hx.Float(mode="output", optionality="optional", view={"label": "PNW", "format": utils.percent_format(1)}),
                    "new_madrid": hx.Float(mode="output", optionality="optional", view={"label": "NM", "format": utils.percent_format(1)}),
                    "hawaii": hx.Float(mode="output", optionality="optional", view={"label": "HAWAII", "format": utils.percent_format(1)}),
                    "us_wf": hx.Float(mode="output", optionality="optional", view={"label": "WILDFIRE", "format": utils.percent_format(1)}),
                    
                    "eu_ws": hx.Float(mode="output", optionality="optional", view={"label": "EU WS", "format": utils.percent_format(1)}),
                    "jp_eq": hx.Float(mode="output", optionality="optional", view={"label": "JP EQ", "format": utils.percent_format(1)}),
                    "jp_ws": hx.Float(mode="output", optionality="optional", view={"label": "JP WS", "format": utils.percent_format(1)}),
                    "can_eq": hx.Float(mode="output", optionality="optional", view={"label": "CAN EQ", "format": utils.percent_format(1)}),
                    "caribbean_ws": hx.Float(mode="output", optionality="optional", view={"label": "CARIBBEAN WS", "format": utils.percent_format(1)}),
                }),
                "ri_cost_ly": hx.Structure(view={"label": "Last Year"}, children={
                    "north_east": hx.Float(mode="output",optionality="optional", view={"label": "NE", "format": utils.percent_format(1)}),
                    "mid_atlantic": hx.Float(mode="output",optionality="optional", view={"label": "MID ATLANTIC", "format": utils.percent_format(1)}),
                    "carolinas": hx.Float(mode="output",optionality="optional", view={"label": "CARS", "format": utils.percent_format(1)}),
                    "fl_se": hx.Float(mode="output",optionality="optional", view={"label": "FL SE", "format": utils.percent_format(1)}),
                    "fl_non_se": hx.Float(mode="output", optionality="optional", view={"label": "FL NON SE", "format": utils.percent_format(1)}),
                    "al_miss": hx.Float(mode="output", optionality="optional", view={"label": "AL + MISS", "format": utils.percent_format(1)}),
                    "louisiana": hx.Float(mode="output", optionality="optional", view={"label": "LOUISIANA", "format": utils.percent_format(1)}),
                    "tx_east": hx.Float(mode="output", optionality="optional", view={"label": "TX EAST", "format": utils.percent_format(1)}),
                    "tx_west": hx.Float(mode="output", optionality="optional", view={"label": "TX WEST", "format": utils.percent_format(1)}),
                    "cal_south": hx.Float(mode="output", optionality="optional", view={"label": "CAL SOUTH", "format": utils.percent_format(1)}),
                    "cal_north": hx.Float(mode="output", optionality="optional", view={"label": "CAL NORTH", "format": utils.percent_format(1)}),
                    "pnw": hx.Float(mode="output", optionality="optional", view={"label": "PNW", "format": utils.percent_format(1)}),
                    "new_madrid": hx.Float(mode="output", optionality="optional", view={"label": "NM", "format": utils.percent_format(1)}),
                    "hawaii": hx.Float(mode="output", optionality="optional", view={"label": "HAWAII", "format": utils.percent_format(1)}),
                    "us_wf": hx.Float(mode="output", optionality="optional", view={"label": "WILDFIRE", "format": utils.percent_format(1)}),
                    
                    "eu_ws": hx.Float(mode="output", optionality="optional", view={"label": "EU WS", "format": utils.percent_format(1)}),
                    "jp_eq": hx.Float(mode="output", optionality="optional", view={"label": "JP EQ", "format": utils.percent_format(1)}),
                    "jp_ws": hx.Float(mode="output", optionality="optional", view={"label": "JP WS", "format": utils.percent_format(1)}),
                    "can_eq": hx.Float(mode="output", optionality="optional", view={"label": "CAN EQ", "format": utils.percent_format(1)}),
                    "caribbean_ws": hx.Float(mode="output", optionality="optional", view={"label": "CARIBBEAN WS", "format": utils.percent_format(1)}),
                }),
                "mvt": hx.Structure(view={"label": "Movement"}, children={
                    "north_east": hx.Float(mode="output",optionality="optional", view={"label": "NE", "format": utils.percent_format(1)}),
                    "mid_atlantic": hx.Float(mode="output",optionality="optional", view={"label": "MID ATLANTIC", "format": utils.percent_format(1)}),
                    "carolinas": hx.Float(mode="output",optionality="optional", view={"label": "CARS", "format": utils.percent_format(1)}),
                    "fl_se": hx.Float(mode="output",optionality="optional", view={"label": "FL SE", "format": utils.percent_format(1)}),
                    "fl_non_se": hx.Float(mode="output", optionality="optional", view={"label": "FL NON SE", "format": utils.percent_format(1)}),
                    "al_miss": hx.Float(mode="output", optionality="optional", view={"label": "AL + MISS", "format": utils.percent_format(1)}),
                    "louisiana": hx.Float(mode="output", optionality="optional", view={"label": "LOUISIANA", "format": utils.percent_format(1)}),
                    "tx_east": hx.Float(mode="output", optionality="optional", view={"label": "TX EAST", "format": utils.percent_format(1)}),
                    "tx_west": hx.Float(mode="output", optionality="optional", view={"label": "TX WEST", "format": utils.percent_format(1)}),
                    "cal_south": hx.Float(mode="output", optionality="optional", view={"label": "CAL SOUTH", "format": utils.percent_format(1)}),
                    "cal_north": hx.Float(mode="output", optionality="optional", view={"label": "CAL NORTH", "format": utils.percent_format(1)}),
                    "pnw": hx.Float(mode="output", optionality="optional", view={"label": "PNW", "format": utils.percent_format(1)}),
                    "new_madrid": hx.Float(mode="output", optionality="optional", view={"label": "NM", "format": utils.percent_format(1)}),
                    "hawaii": hx.Float(mode="output", optionality="optional", view={"label": "HAWAII", "format": utils.percent_format(1)}),
                    "us_wf": hx.Float(mode="output", optionality="optional", view={"label": "WILDFIRE", "format": utils.percent_format(1)}),
                    
                    "eu_ws": hx.Float(mode="output", optionality="optional", view={"label": "EU WS", "format": utils.percent_format(1)}),
                    "jp_eq": hx.Float(mode="output", optionality="optional", view={"label": "JP EQ", "format": utils.percent_format(1)}),
                    "jp_ws": hx.Float(mode="output", optionality="optional", view={"label": "JP WS", "format": utils.percent_format(1)}),
                    "can_eq": hx.Float(mode="output", optionality="optional", view={"label": "CAN EQ", "format": utils.percent_format(1)}),
                    "caribbean_ws": hx.Float(mode="output", optionality="optional", view={"label": "CARIBBEAN WS", "format": utils.percent_format(1)}),
                }),
                            
            }),
            "quote_reins_information": hx.Str(mode="input", default = """NB: Figures shown in this section are after application of; reinstatements, AAD and Black Swan load.""", view={"read_only": True}),
            "rms_tp_calc_reins_information": hx.Str(mode="input", default = """NB: The Net Expected Loss calculation below is as follows:\n
            1) 'Gross EL' is the RMS + NMP 100% EL before any application of; reinstatements, AAD or Black Swan loads (i.e. as entered in the Modelling tab which assumes unlimited free).\n
            2) 'Model Adj. Factor' (or override) converts the Gross EL from unlimited free and no AAD to limited free (depending on the number of reinstatements) and AAD adjusted. This is the 'Net EL (Free Reinstatements)' column.\n
            3) 'Expected Reinstatement Cost' converts the limited free EL to limited paid EL (depending on whether there are paid reinstatements). This is the 'Net EL' column.\n
            4) Finally, Black Swan load is added to the Net (of paid reinstatements and AAD) EL.\n\n 
            NB: If you have priced an account outside the rater already allowing for reinstatements, then set the 'Override Adj. Factor' to 100%.""", view={"read_only": True}),
            "rol_ty": hx.Structure(children={
                "ulr": hx.Float(mode="output", optionality="optional", view={"label": "ULR (GN)", "format": {"output": "percent", "mantissa": 1}}),
                "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
                "roc": hx.Float(mode="output", optionality="optional", view={"label": "ROC", "format": {"output": "percent", "mantissa": 1}}),

                "rol_quote": hx.Float(mode="output", optionality="optional", view={"label": "Quoted ROL", "format": utils.thousands_format(0)}),
                "rol_fot": hx.Float(mode="output", optionality="optional", view={"label": "FOT ROL", "format": utils.thousands_format(0)}),
                
                "quote_adequacy": hx.Float(mode="output", optionality="optional", view={"label": "Quote Adequacy", "format": {"output": "percent", "mantissa": 1}}),                
                "fot_adequacy": hx.Float(mode="output", optionality="optional", view={"label": "FOT Adequacy", "format": {"output": "percent", "mantissa": 1}}),
                "prem_full_line": hx.Float(mode="output", optionality="optional", view={"label": "Premium 100%", "format": utils.thousands_format(0)}),
                "written_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format": utils.thousands_format(0)}),
                "estimated_signing_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Estimated Signing", "format": utils.thousands_format(0)}),
                "signed_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Signed Line", "format": utils.thousands_format(0)}),
                "epi_written": hx.Float(mode="output", optionality="optional", view={"label": "Written EPI", "format": utils.thousands_format(0)}),
                "epi_estimated": hx.Float(mode="output", optionality="optional", view={"label": "Estimated EPI", "format": utils.thousands_format(0)}),
                "epi_signed": hx.Float(mode="output", optionality="optional", view={"label": "Signed EPI", "format": utils.thousands_format(0)}),                
            }),
            "rol_ly": hx.Structure(children={
                "ulr": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ULR (GN)", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "tpi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "bpi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "roc": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ROC", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),

                "rol_quote": hx.Float(mode="output", optionality="optional", view={"label": "Quoted ROL", "format": utils.thousands_format(0)}),
                "rol_fot": hx.Float(mode="output", optionality="optional", view={"label": "FOT ROL", "format": utils.thousands_format(0)}),

                "quote_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Quote Adequacy", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),                
                "fot_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT Adequacy", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "prem_full_line": hx.Float(mode="output", optionality="optional", view={"label": "Premium 100%", "format": utils.thousands_format(0)}),
                "written_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format": utils.thousands_format(0)}),
                "estimated_signing_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Estimated Signing", "format": utils.thousands_format(0)}),
                "signed_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Signed Line", "format": utils.thousands_format(0)}),
                "epi_written": hx.Float(mode="output", optionality="optional", view={"label": "Written EPI", "format": utils.thousands_format(0)}),
                "epi_estimated": hx.Float(mode="output", optionality="optional", view={"label": "Estimated EPI", "format": utils.thousands_format(0)}),
                "epi_signed": hx.Float(mode="output", optionality="optional", view={"label": "Signed EPI", "format": utils.thousands_format(0)}),                   
            }),
        }),
    })

    cds.extend_node_rater_defined("cds/layers",
     {
        "quote": hx.Structure(children={
            "rol_ty": hx.Structure(children={
                "rol_rms": hx.Float(mode="output", optionality="optional", view={"label": "RMS ROL (GG)", "format": {"output": "percent", "mantissa": 2}}),
                "rol_ivor": hx.Float(mode="output", optionality="optional", view={"label": "IVOR ROL (GG)", "format": {"output": "percent", "mantissa": 2}}),
                "rol_air": hx.Float(mode="output", optionality="optional", view={"label": "AIR ROL (GG)", "format": {"output": "percent", "mantissa": 2}}),
                "rol_burn": hx.Float(mode="output", optionality="optional", view={"label": "Burn ROL (GG)", "format": {"output": "percent", "mantissa": 2}}),
                "rol_burn_override": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Burn Override (GG)", "format": {"output": "percent", "mantissa": 2}}),

                "weighting_rms": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "RMS Weighting", "format": {"output": "percent", "mantissa": 1}}),
                "weighting_ivor": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "IVOR Weighting", "format": {"output": "percent", "mantissa": 1}}),
                "weighting_air": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "AIR Weighting", "format": {"output": "percent", "mantissa": 1}}),
                "weighting_burn": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Burn Weighting", "format": {"output": "percent", "mantissa": 1}}),

                ## these are all net
                "lol_rms": hx.Float(mode="output", optionality="optional", view={"label": "RMS LOL", "format": {"output": "percent", "mantissa": 1}}),
                "lol_ivor": hx.Float(mode="output", optionality="optional", view={"label": "IVOR LOL", "format": {"output": "percent", "mantissa": 1}}),
                "lol_air": hx.Float(mode="output", optionality="optional", view={"label": "AIR LOL", "format": {"output": "percent", "mantissa": 1}}),
                "lol_burn": hx.Float(mode="output", optionality="optional", view={"label": "Burn LOL", "format": {"output": "percent", "mantissa": 1}}),
                "lol_weighted": hx.Float(mode="output", optionality="optional", view={"label": "Weighted LOL", "format": {"output": "percent", "mantissa": 1}}),

                "weighted_el": hx.Float(mode="output", optionality="optional", view={"label": "Net EL", "format": utils.thousands_format(0)}),

                ## risk XL
                "risk_xl_rol_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Exposure ROL (GG)", "format": {"output": "percent", "mantissa": 2}}),
                "risk_xl_weighting_exposure": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Exposure Weighting", "format": {"output": "percent", "mantissa": 1}}),
                "risk_xl_lol_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Exposure LOL", "format": {"output": "percent", "mantissa": 1}}),

                "tp_calc_1_burn": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 1", "format": utils.thousands_format(0)}),
                "tp_calc_2_burn": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 2", "format": utils.thousands_format(0)}),
                "tp_calc_3_burn": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 3", "format": utils.thousands_format(0)}),
                "tp_final_burn": hx.Float(mode="output", optionality="optional", view={"label": "Final Technical Premium (GN)", "format": utils.thousands_format(0)}),

                "tp_calc_1_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 1", "format": utils.thousands_format(0)}),
                "tp_calc_2_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 2", "format": utils.thousands_format(0)}),
                "tp_calc_3_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 3", "format": utils.thousands_format(0)}),
                "tp_final_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Final Technical Premium (GN)", "format": utils.thousands_format(0)}),

                "layer_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Layer Exposure", "format": utils.thousands_format(0)}),
                "roev": hx.Float(mode="output", optionality="optional", view={"label": "ROEV", "format": utils.percent_format(4)}),

                # want weighted gross lol for rate change, assess impact of changes in reinstatements
                "gross_lol_weighted": hx.Float(mode="output", optionality="optional", view={"label": "Gross Weighted LOL", "format": {"output": "percent", "mantissa": 1}}),

                "rol_afb_tech": hx.Float(mode="output", optionality="optional", view={"label": "AFB Tech ROL (GG)", "format": {"output": "percent", "mantissa": 2}}),
                "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
                "roc": hx.Float(mode="output", optionality="optional", view={"label": "ROC", "format": {"output": "percent", "mantissa": 1}}),
                "ulr": hx.Float(mode="output", optionality="optional", view={"label": "ULR (GN)", "format": {"output": "percent", "mantissa": 1}}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),

                "rol_quote": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Quoted ROL", "format": {"output": "percent", "mantissa": 2}}),
                "rol_fot": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "FOT ROL", "format": {"output": "percent", "mantissa": 2}}),
                "quote_fot_ratio": hx.Float(mode="output", optionality="optional", view={"label": "FOT / Quote Comparison", "format": {"output": "percent", "mantissa": 1}}),
                
                "prem_full_line": hx.Float(mode="output", optionality="optional", view={"label": "Premium 100%", "format": utils.thousands_format(0)}),

                "quote_adequacy": hx.Float(mode="output", optionality="optional", view={"label": "Quote Adequacy", "format": {"output": "percent", "mantissa": 1}}),
                "fot_adequacy": hx.Float(mode="output", optionality="optional", view={"label": "FOT Adequacy", "format": {"output": "percent", "mantissa": 1}}),
                "rms_adequacy": hx.Float(mode="output", optionality="optional", view={"label": "RMS Adequacy", "format": {"output": "percent", "mantissa": 1}}),

                "written_line": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Written Line", "format": {"output": "percent", "mantissa": 2}}),
                "estimated_signing": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Estimated Signing", "format": {"output": "percent", "mantissa": 2}}),
                "signed_line": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Signed Line", "format": {"output": "percent", "mantissa": 2}}),
                "est_sign_written_ratio": hx.Float(mode="output", optionality="optional", view={"label": "Estimated Signing %", "format": {"output": "percent", "mantissa": 2}}),

                "written_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format": utils.thousands_format(0)}),
                "estimated_signing_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Estimated Signing", "format": utils.thousands_format(0)}),
                "signed_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Signed Line", "format": utils.thousands_format(0)}),

                "epi_written": hx.Float(mode="output", optionality="optional", view={"label": "Written EPI", "format": utils.thousands_format(0)}),
                "epi_estimated": hx.Float(mode="output", optionality="optional", view={"label": "Estimated EPI", "format": utils.thousands_format(0)}),
                "epi_signed": hx.Float(mode="output", optionality="optional", view={"label": "Signed EPI", "format": utils.thousands_format(0)}),

                "rp_quote_break_even": hx.Float(mode="output", optionality="optional", view={"label": "Quote Break Even", "format": utils.thousands_format(0)}),
                "rp_fot_break_even": hx.Float(mode="output", optionality="optional", view={"label": "FOT Break Even", "format": utils.thousands_format(0)}),

                # attach and exit points
                "curve_agg_rp_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "curve_agg_rp_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                ## rms ap
                "rms_ap_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "rms_ap_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                ## rms eq
                "rms_eq_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "rms_eq_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),  
                ## rms ws
                "rms_ws_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "rms_ws_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),  
                ## rms scs
                "rms_scs_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "rms_scs_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),  
                ## air ap
                "air_ap_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "air_ap_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),  
                ## air eq
                "air_eq_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "air_eq_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),  
                ## air ws
                "air_ws_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "air_ws_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),  
                ## air scs
                "air_scs_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "air_scs_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),  
                ## air winter
                "air_winter_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "air_winter_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),  
                ## air wf
                "air_wf_attach": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),
                "air_wf_exit": hx.Float(mode="input", default=None, optionality="optional", view = {"read_only": True}),  

                "rp_attach": hx.Float(mode="output", optionality="optional", view={"label": "RP Attach", "format": utils.thousands_format(0)}),
                "rp_exit": hx.Float(mode="output", optionality="optional", view={"label": "RP Exit", "format": utils.thousands_format(0)}),
                "rp_pml_selection": hx.Str(mode="input", default = "Curve Agg", options = rp_peril_options, view={"label": "PML Selection"}),

                "rp_attach_peak": hx.Float(mode="output", optionality="optional", view={"label": "RP Attach", "format": utils.thousands_format(0)}),
                "rp_exit_peak": hx.Float(mode="output", optionality="optional", view={"label": "RP Exit", "format": utils.thousands_format(0)}),
                "rp_pml_selection_peak": hx.Str(mode="input", default = "Curve Agg", options = rp_peril_options, view={"label": "PML Selection"}),

            }),
            "rol_ly": hx.Structure(children={
                "rol_rms": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RMS ROL (GG)", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "rol_ivor": hx.Float(mode="input", default=None, optionality="optional", view={"label": "IVOR ROL (GG)", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "rol_air": hx.Float(mode="input", default=None, optionality="optional", view={"label": "AIR ROL (GG)", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "rol_burn": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Burn ROL (GG)", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "rol_burn_override": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Burn Override (GG)", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),

                "weighting_rms": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RMS Weighting", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "weighting_ivor": hx.Float(mode="input", default=None, optionality="optional", view={"label": "IVOR Weighting", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "weighting_air": hx.Float(mode="input", default=None, optionality="optional", view={"label": "AIR Weighting", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "weighting_burn": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Burn Weighting", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),

                "lol_rms": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RMS LOL", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "lol_ivor": hx.Float(mode="input", default=None, optionality="optional", view={"label": "IVOR LOL", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "lol_air": hx.Float(mode="input", default=None, optionality="optional", view={"label": "AIR LOL", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "lol_burn": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Burn LOL", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "lol_weighted": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Weighted LOL", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),

                ## risk XL
                "risk_xl_rol_exposure": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Exposure ROL (GG)", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "risk_xl_weighting_exposure": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Exposure Weighting", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "risk_xl_lol_exposure": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Exposure LOL", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),

                "tp_calc_1_burn": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 1", "format": utils.thousands_format(0)}),
                "tp_calc_2_burn": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 2", "format": utils.thousands_format(0)}),
                "tp_calc_3_burn": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 3", "format": utils.thousands_format(0)}),
                "tp_final_burn": hx.Float(mode="output", optionality="optional", view={"label": "Final Technical Premium (GN)", "format": utils.thousands_format(0)}),

                "tp_calc_1_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 1", "format": utils.thousands_format(0)}),
                "tp_calc_2_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 2", "format": utils.thousands_format(0)}),
                "tp_calc_3_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 3", "format": utils.thousands_format(0)}),
                "tp_final_exposure": hx.Float(mode="output", optionality="optional", view={"label": "Final Technical Premium (GN)", "format": utils.thousands_format(0)}),

                "layer_exposure": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Layer Exposure", "format": utils.thousands_format(0), "read_only": True}),
                "roev": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ROEV", "format": utils.percent_format(4), "read_only": True}),
                

                # want weighted gross lol for rate change, assess impact of changes in reinstatements
                "gross_lol_weighted": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross Weighted LOL", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),

                "rol_afb_tech": hx.Float(mode="input", default=None, optionality="optional", view={"label": "AFB Tech ROL (GG)", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "tpi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "roc": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ROC", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "ulr": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ULR (GN)", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "bpi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),

                "rol_quote": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Quoted ROL", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "rol_fot": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT ROL", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "quote_fot_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT / Quote Comparison", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),

                "prem_full_line": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Premium 100%", "format": utils.thousands_format(0), "read_only": True}),

                "quote_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Quote Adequacy", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "fot_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT Adequacy", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "rms_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RMS Adequacy", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),

                "written_line": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "estimated_signing": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Estimated Signing", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),
                "signed_line": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Signed Line", "format": {"output": "percent", "mantissa": 2}, "read_only": True}),

                "written_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format": utils.thousands_format(0)}),
                "estimated_signing_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Estimated Signing", "format": utils.thousands_format(0)}),
                "signed_line_dollar": hx.Float(mode="output", optionality="optional", view={"label": "Signed Line", "format": utils.thousands_format(0)}),

                "epi_written": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Written EPI", "format": utils.thousands_format(0), "read_only": True}),
                "epi_estimated": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Estimated EPI", "format": utils.thousands_format(0), "read_only": True}),
                "epi_signed": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Signed EPI", "format": utils.thousands_format(0), "read_only": True}),

                "rp_quote_break_even": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Quote Break Even", "format": utils.thousands_format(0), "read_only": True}),
                "rp_fot_break_even": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT Break Even", "format": utils.thousands_format(0), "read_only": True}),

                "rp_attach": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RP Attach", "format": utils.thousands_format(0), "read_only": True}),
                "rp_exit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RP Exit", "format": utils.thousands_format(0), "read_only": True}),
                "rp_pml_selection": hx.Str(mode="input", default=None, optionality="optional", view={"label": "PML Selection", "read_only": True}),

                "rp_attach_peak": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RP Attach", "format": utils.thousands_format(0), "read_only": True}),
                "rp_exit_peak": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RP Exit", "format": utils.thousands_format(0), "read_only": True}),
                "rp_pml_selection_peak": hx.Str(mode="input", default=None, optionality="optional", view={"label": "PML Selection", "read_only": True}),     
            }),
            "rms_tp_calc": hx.Structure(children={
                "gross_lol": hx.Float(mode="output", optionality="optional", view={"label": "Gross LOL", "format": {"output": "percent", "mantissa": 1}}),
                "gross_el": hx.Float(mode="output", optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "gross_sd": hx.Float(mode="output", optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0)}),
                "model_limit_factor": hx.Float(mode="output", optionality="optional", view={"label": "Model Adj. Factor", "format": {"output": "percent", "mantissa": 1}}),
                "override_limit_factor": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Override Adj. Factor", "format": {"output": "percent", "mantissa": 1}}),
                "net_el_excl_reins_prem": hx.Float(mode="output", optionality="optional", view={"label": "Net EL (Free Reinstatements)", "format": utils.thousands_format(0)}),
                "no_expected_reins": hx.Float(mode="output", optionality="optional", view={"label": "Expected Reinstatement Cost", "format": {"thousandSeparated": True, "mantissa": 3}}),
                "net_el": hx.Float(mode="output", optionality="optional", view={"label": "Net EL", "format": utils.thousands_format(0)}),
                "net_sd": hx.Float(mode="output", optionality="optional", view={"label": "Net SD", "format": utils.thousands_format(0)}),
                "net_el_incl_bs": hx.Float(mode="output", optionality="optional", view={"label": "Net EL + Black Swan", "format": utils.thousands_format(0)}),
                "net_sd_incl_bs": hx.Float(mode="output", optionality="optional", view={"label": "Net SD + Black Swan", "format": utils.thousands_format(0)}),

                "afb_net_el": hx.Float(mode="output", optionality="optional", view={"label": "AFB Net EL", "format": utils.thousands_format(0)}),
                "afb_net_sd": hx.Float(mode="output", optionality="optional", view={"label": "AFB Net SD", "format": utils.thousands_format(0)}),

                "mi_250": hx.Float(mode="output", optionality="optional", view={"label": "Marginal Impact %", "format": {"output": "percent", "mantissa": 1}}),
                "marginal_impact": hx.Float(mode="output", optionality="optional", view={"label": "Marginal Impact", "format": utils.thousands_format(0)}),
                "capital_us": hx.Float(mode="output", optionality="optional", view={"label": "US Capital", "format": utils.thousands_format(0)}),
                "capital_intl": hx.Float(mode="output", optionality="optional", view={"label": "Intl. Capital", "format": utils.thousands_format(0)}),
                "attritional_capital": hx.Float(mode="output", optionality="optional", view={"label": "Attr. Capital", "format": utils.thousands_format(0)}),
                "total_capital": hx.Float(mode="output", optionality="optional", view={"label": "Total Capital", "format": utils.thousands_format(0)}),
                "total_coc": hx.Float(mode="output", optionality="optional", view={"label": "Total CoC", "format": utils.thousands_format(0)}),

                "ri_cost": hx.Float(mode="output", optionality="optional", view={"label": "Total Reinsurance Cost", "format": utils.thousands_format(0)}),

                "indirect_expenses": hx.Float(mode="output", optionality="optional", view={"label": "Indirect Expenses", "format": utils.thousands_format(0)}),
                "direct_expenses": hx.Float(mode="output", optionality="optional", view={"label": "Direct Expenses", "format": utils.thousands_format(0)}),
                "lae": hx.Float(mode="output", optionality="optional", view={"label": "LAE", "format": utils.thousands_format(0)}),
                "total_expenses": hx.Float(mode="output", optionality="optional", view={"label": "Total Expenses", "format": utils.thousands_format(0)}),

                "sd_load": hx.Float(mode="output", optionality="optional", view={"label": "SD Load", "format": utils.thousands_format(0)}),
                "calc_3_lr_load": hx.Float(mode="output", optionality="optional", view={"label": "LR Load", "format": utils.thousands_format(0)}),
                "expenses_less_inv_income": hx.Float(mode="output", optionality="optional", view={"label": "Expnenses less Investment Inc.", "format": utils.thousands_format(0)}),  

                "tp_calc_1": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 1", "format": utils.thousands_format(0)}),
                "tp_calc_2": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 2", "format": utils.thousands_format(0)}),
                "tp_calc_3": hx.Float(mode="output", optionality="optional", view={"label": "Calculation 3", "format": utils.thousands_format(0)}),
                "tp_max_calculation": hx.Str(mode="output", optionality="optional", view={"label": "Max Calculation"}),
                "tp_non_loss_cost": hx.Float(mode="output", optionality="optional", view={"label": "Non-Loss Cost Load", "format": utils.thousands_format(0)}),
                "tp_final": hx.Float(mode="output", optionality="optional", view={"label": "Final Technical Premium (GN)", "format": utils.thousands_format(0)}),
            }),
            "ivor_tp_calc": hx.Structure(children={
                "afb_net_el": hx.Float(mode="output", optionality="optional", view={"label": "AFB Net EL", "format": utils.thousands_format(0)}),
                "afb_net_sd": hx.Float(mode="output", optionality="optional", view={"label": "AFB Net SD", "format": utils.thousands_format(0)}),
                "tp_final": hx.Float(mode="output", optionality="optional", view={"label": "Final Technical Premium (GN)", "format": utils.thousands_format(0)}),
            }),
            "air_tp_calc": hx.Structure(children={
                "afb_net_el": hx.Float(mode="output", optionality="optional", view={"label": "AFB Net EL", "format": utils.thousands_format(0)}),
                "afb_net_sd": hx.Float(mode="output", optionality="optional", view={"label": "AFB Net SD", "format": utils.thousands_format(0)}),
                "tp_final": hx.Float(mode="output", optionality="optional", view={"label": "Final Technical Premium (GN)", "format": utils.thousands_format(0)}),
            }),
            "burn_tp_calc": hx.Structure(children={
                "afb_net_el": hx.Float(mode="output", optionality="optional", view={"label": "AFB Net EL", "format": utils.thousands_format(0)}),
                "afb_net_sd": hx.Float(mode="output", optionality="optional", view={"label": "AFB Net SD", "format": utils.thousands_format(0)}),
                "tp_final": hx.Float(mode="output", optionality="optional", view={"label": "Final Technical Premium (GN)", "format": utils.thousands_format(0)}),
            }),
        }),
    })