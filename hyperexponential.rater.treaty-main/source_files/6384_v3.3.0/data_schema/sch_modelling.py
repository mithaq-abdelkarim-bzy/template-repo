import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_modelling(cds):
    cds.extend_node_rater_defined("cds/layers",
     {
        "model": hx.Structure(view={"label": "Model"}, children={
            "total_rms_nmp": hx.Structure(view={"label": "RMS + NMP"}, children={
                "gross_el": hx.Float(mode="output", optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "gross_sd": hx.Float(mode="output", optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0)}),
                "change_el": hx.Float(mode="output", optionality="optional", view={"label": "Change in EL", "format": {"output": "percent", "mantissa": 1}}),                
            }),
            "total_ivor_nmp": hx.Structure(view={"label": "IVOR + NMP"}, children={
                "gross_el": hx.Float(mode="output", optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "gross_sd": hx.Float(mode="output", optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0)}),
                "change_el": hx.Float(mode="output", optionality="optional", view={"label": "Change in EL", "format": {"output": "percent", "mantissa": 1}}),
            }),
            "total_air_nmp": hx.Structure(view={"label": "AIR + NMP"}, children={
                "gross_el": hx.Float(mode="output", optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "gross_sd": hx.Float(mode="output", optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0)}),
                "change_el": hx.Float(mode="output", optionality="optional", view={"label": "Change in EL", "format": {"output": "percent", "mantissa": 1}}),
            }),
            "rms": hx.Structure(view={"label": "Model"}, children={
                "gross_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "gross_sd": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Gross SD", "format": utils.thousands_format(0)}),
                "change_el": hx.Float(mode="output", optionality="optional", view={"label": "Change in RMS EL", "format": {"output": "percent", "mantissa": 1}}),

                "ws_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "WS EL", "format": utils.thousands_format(0)}),
                "eq_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "EQ EL", "format": utils.thousands_format(0)}),
                "scs_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "SCS EL", "format": utils.thousands_format(0)}),

                "eu_ws_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "EU WS EL", "format": utils.thousands_format(0)}),
                "jp_eq_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "JP EQ EL", "format": utils.thousands_format(0)}),
                "jp_ws_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "JP WS EL", "format": utils.thousands_format(0)}),
                "can_eq_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Canada EQ EL", "format": utils.thousands_format(0)}),
                "caribbean_ws_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Caribbean WS EL", "format": utils.thousands_format(0)}),

                "perc_us_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Percent US EL", "format": {"output": "percent", "mantissa": 1}}),
                "gross_el_for_ri_us_application_ccy": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
            }),
            "ivor": hx.Structure(view={"label": "Model"}, children={
                "gross_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "gross_sd": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Gross SD", "format": utils.thousands_format(0)}),
            }),
            "air": hx.Structure(view={"label": "Model"}, children={
                "gross_el": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "gross_sd": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Gross SD", "format": utils.thousands_format(0)}),
                "change_el": hx.Float(mode="output", optionality="optional", view={"label": "Change in RMS EL", "format": {"output": "percent", "mantissa": 1}}),
            }),
            "nmp": hx.Structure(view={"label": "Model"}, children={
                "gross_el_incl_rol": hx.Float(mode="output", optionality="optional", view={"label": "Gross EL incl. LOL", "format": utils.thousands_format(0)}),
                "gross_sd_incl_rol": hx.Float(mode="output", optionality="optional", view={"label": "Gross SD incl. LOL", "format": utils.thousands_format(0)}),
                "gross_el": hx.Float(mode="output", optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "gross_sd": hx.Float(mode="output", optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0)}),
                "additional_rol": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Additional LOL", "format": {"output": "percent", "mantissa": 1}}),
                "description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "NMP Description"}),              
            }),
        }),
        "model_prev": hx.Structure(view={"label": "Model"}, children={
            "total_rms_nmp": hx.Structure(view={"label": "RMS + NMP"}, children={
                "gross_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0), "read_only": True}),
                "gross_sd": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "total_ivor_nmp": hx.Structure(view={"label": "IVOR + NMP"}, children={
                "gross_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0), "read_only": True}),
                "gross_sd": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "total_air_nmp": hx.Structure(view={"label": "AIR + NMP"}, children={
                "gross_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0), "read_only": True}),
                "gross_sd": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "rms": hx.Structure(view={"label": "Model"}, children={
                "gross_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0), "read_only": True}),
                "gross_sd": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0), "read_only": True}),
                "ws_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "WS EL", "format": utils.thousands_format(0), "read_only": True}),
                "eq_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "EQ EL", "format": utils.thousands_format(0), "read_only": True}),
                "scs_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "SCS EL", "format": utils.thousands_format(0), "read_only": True}),

                "eu_ws_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "EU WS EL", "format": utils.thousands_format(0), "read_only": True}),
                "jp_eq_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "JP EQ EL", "format": utils.thousands_format(0), "read_only": True}),
                "jp_ws_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "JP WS EL", "format": utils.thousands_format(0), "read_only": True}),
                "can_eq_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Canada EQ EL", "format": utils.thousands_format(0), "read_only": True}),
                "caribbean_ws_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Caribbean WS EL", "format": utils.thousands_format(0), "read_only": True}),

                "perc_us_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Percent US EL", "format": {"output": "percent", "mantissa": 1}}),
            }),
            "ivor": hx.Structure(view={"label": "Model"}, children={
                "gross_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0), "read_only": True}),
                "gross_sd": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "air": hx.Structure(view={"label": "Model"}, children={
                "gross_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0), "read_only": True}),
                "gross_sd": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "nmp": hx.Structure(view={"label": "Model"}, children={
                "gross_el_incl_rol": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross EL incl. LOL", "format": utils.thousands_format(0), "read_only": True}),
                "gross_sd_incl_rol": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross SD incl. LOL", "format": utils.thousands_format(0), "read_only": True}),
                "gross_el": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0), "read_only": True}),
                "gross_sd": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0), "read_only": True}),
                "additional_rol": hx.Float(mode="input",default=None, optionality="optional", view={"label": "Additional LOL", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "description": hx.Str(mode="input",default=None, optionality="optional", view={"label": "NMP Description", "read_only": True}),              
            }),
        }),
    })

    ## RMS regional entries by RDS region, used for reinsurance calculation (this year and previous)
    cds.extend_node_rater_defined("cds/layers",
     {
        "rms_regional": hx.Structure(view={"label": "Model"}, children={
            "north_east": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "NE", "format": utils.percent_format(1)}),
            "mid_atlantic": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "MID ATLANTIC", "format": utils.percent_format(1)}),
            "carolinas": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "CARS", "format": utils.percent_format(1)}),
            "fl_se": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "FL SE", "format": utils.percent_format(1)}),
            "fl_non_se": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "FL NON SE", "format": utils.percent_format(1)}),
            "al_miss": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "AL + MISS", "format": utils.percent_format(1)}),
            "louisiana": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "LOUISIANA", "format": utils.percent_format(1)}),
            "tx_east": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "TX EAST", "format": utils.percent_format(1)}),
            "tx_west": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "TX WEST", "format": utils.percent_format(1)}),
            "cal_south": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "CAL SOUTH", "format": utils.percent_format(1)}),
            "cal_north": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "CAL NORTH", "format": utils.percent_format(1)}),
            "pnw": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "PNW", "format": utils.percent_format(1)}),
            "new_madrid": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "NM", "format": utils.percent_format(1)}),
            "hawaii": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "HAWAII", "format": utils.percent_format(1)}),
            # These don't impact the RI cost (but are needed for area codes)
            "mid_west_1": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "MID WEST 1", "format": utils.percent_format(1)}),
            "mid_west_2": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "MID WEST 2", "format": utils.percent_format(1)}),
            "second_event": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "2nd EVENT COVER", "format": utils.percent_format(1)}),
            "ca_wildfire": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "CA WILDFIRE", "format": utils.percent_format(1)}),
        }),
        
        "rms_regional_prev": hx.Structure(view={"label": "Model"}, children={
            "north_east": hx.Float(mode="input", default=None, optionality="optional", view={"label": "NE", "format": utils.percent_format(1), "read_only": True}),
            "mid_atlantic": hx.Float(mode="input", default=None, optionality="optional", view={"label": "MID ATLANTIC", "format": utils.percent_format(1), "read_only": True}),
            "carolinas": hx.Float(mode="input", default=None, optionality="optional", view={"label": "CARS", "format": utils.percent_format(1), "read_only": True}),
            "fl_se": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FL SE", "format": utils.percent_format(1), "read_only": True}),
            "fl_non_se": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FL NON SE", "format": utils.percent_format(1), "read_only": True}),
            "al_miss": hx.Float(mode="input", default=None, optionality="optional", view={"label": "AL + MISS", "format": utils.percent_format(1), "read_only": True}),
            "louisiana": hx.Float(mode="input", default=None, optionality="optional", view={"label": "LOUISIANA", "format": utils.percent_format(1), "read_only": True}),
            "tx_east": hx.Float(mode="input", default=None, optionality="optional", view={"label": "TX EAST", "format": utils.percent_format(1), "read_only": True}),
            "tx_west": hx.Float(mode="input", default=None, optionality="optional", view={"label": "TX WEST", "format": utils.percent_format(1), "read_only": True}),
            "cal_south": hx.Float(mode="input", default=None, optionality="optional", view={"label": "CAL SOUTH", "format": utils.percent_format(1), "read_only": True}),
            "cal_north": hx.Float(mode="input", default=None, optionality="optional", view={"label": "CAL NORTH", "format": utils.percent_format(1), "read_only": True}),
            "pnw": hx.Float(mode="input", default=None, optionality="optional", view={"label": "PNW", "format": utils.percent_format(1), "read_only": True}),
            "new_madrid": hx.Float(mode="input", default=None, optionality="optional", view={"label": "NM", "format": utils.percent_format(1), "read_only": True}),
            "hawaii": hx.Float(mode="input", default=None, optionality="optional", view={"label": "HAWAII", "format": utils.percent_format(1), "read_only": True}),
            # These don't impact the RI cost (but are needed for area codes)
            "mid_west_1": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "MID WEST 1", "format": utils.percent_format(1), "read_only": True}),
            "mid_west_2": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "MID WEST 2", "format": utils.percent_format(1), "read_only": True}),
            "second_event": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "2nd EVENT COVER", "format": utils.percent_format(1), "read_only": True}),
            "ca_wildfire": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "CA WILDFIRE", "format": utils.percent_format(1), "read_only": True}),
        }),
    })

    ## Add in marginal impacts
    cds.extend_node_rater_defined("cds/layers",
     {
        "marginal_impacts": hx.Structure(view={"label": "Marginal Impacts"}, children={
            **{f"{item}": hx.Structure(view={"label": "Model"}, children={
                "mi_250": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 250", "format": utils.percent_format(1)}),
                "mi_10": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 10", "format": utils.percent_format(1)}),
                }) for item in ["treaty_us","treaty_group","treaty_us_quake","treaty_intl"]
            },
        }),

        "marginal_impacts_prev": hx.Structure(view={"label": "Marginal Impacts"}, children={
            **{f"{item}": hx.Structure(view={"label": "Model"}, children={
                "mi_250": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 250", "format": utils.percent_format(1), "read_only": True}),
                "mi_10": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 10", "format": utils.percent_format(1), "read_only": True}),
                }) for item in ["treaty_us","treaty_group","treaty_us_quake","treaty_intl"]
            } ,
        }),
    })

    cds.extend_node_rater_defined("cds",
     {
        "modelling_account_level": hx.Structure(view={"label": "Modelling Account Level"}, children={
            "comments": hx.Str(mode="input",default="", optionality="optional", view={"label": "Comments"}),
            "ivor_nmp_selection": hx.Str(mode="input",default="Excludes NMP", options=["Excludes NMP", "Includes NMP"], view={"label": "IVOR NMP inclusion?"}),
            "rms_eq_curve_selection": hx.Int(mode="input",default=None,optionality="optional", options = [1,2,3,4,5,6,7,8,9], view={"label": "RMS EQ PML Curve Index"}),
            "rms_ws_curve_selection": hx.Int(mode="input",default=None,optionality="optional", options = [1,2,3,4,5,6,7,8,9],view={"label": "RMS WS PML Curve Index"}),
            "rms_scs_curve_selection": hx.Int(mode="input",default=None,optionality="optional", options = [1,2,3,4,5,6,7,8,9], view={"label": "RMS SCS PML Curve Index"}),

            "rms_eu_ws_curve_selection": hx.Int(mode="input",default=None,optionality="optional", options = [1,2,3,4,5,6,7,8,9], view={"label": "RMS EU WS PML Curve Index"}),
            "rms_jp_eq_curve_selection": hx.Int(mode="input",default=None,optionality="optional", options = [1,2,3,4,5,6,7,8,9], view={"label": "RMS Japan EQ PML Curve Index"}),
            "rms_jp_ws_curve_selection": hx.Int(mode="input",default=None,optionality="optional", options = [1,2,3,4,5,6,7,8,9], view={"label": "RMS Japan WS PML Curve Index"}),
            "rms_can_eq_curve_selection": hx.Int(mode="input",default=None,optionality="optional", options = [1,2,3,4,5,6,7,8,9], view={"label": "RMS Canada EQ PML Curve Index"}),
            "rms_caribbean_ws_curve_selection": hx.Int(mode="input",default=None,optionality="optional", options = [1,2,3,4,5,6,7,8,9], view={"label": "RMS Caribbean WS PML Curve Index"}),

            "rds_gross_loss": hx.Structure(view={"label": "Cedant RDS Gross Loss"}, children={

                **{f"{item}": hx.Structure(view={"label": label}, children={
                    "carolinas_ws": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Carolinas WS", "format": utils.thousands_format(0)}),
                    "miami_dade_ws": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Miami-Dade WS", "format": utils.thousands_format(0)}),
                    "gulf_ws": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Gulf WS", "format": utils.thousands_format(0)}),
                    "ne_ws": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "NE WS", "format": utils.thousands_format(0)}),
                    "fl_pinnelas_ws": hx.Float(mode="input",default=None, optionality="optional", view={"label": "FL Pinnelas", "format": utils.thousands_format(0)}),
                    "la_eq": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "LA EQ", "format": utils.thousands_format(0)}),
                    "nm_eq": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "NM EQ", "format": utils.thousands_format(0)}),
                    "nm_stress_eq": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "NM Stress EQ", "format": utils.thousands_format(0)}),
                    "sf_eq": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "SF EQ", "format": utils.thousands_format(0)}),     
                    }) for item, label in zip(["this_year"], ["This Year"]) 
                },

                **{f"{item}": hx.Structure(view={"label": label}, children={
                    "carolinas_ws": hx.Float(mode="input",default=None,  optionality="optional", view={"label": "Carolinas WS", "format": utils.thousands_format(0), "read_only": True}),
                    "miami_dade_ws": hx.Float(mode="input",default=None,  optionality="optional", view={"label": "Miami-Dade WS", "format": utils.thousands_format(0), "read_only": True}),
                    "gulf_ws": hx.Float(mode="input",default=None,  optionality="optional", view={"label": "Gulf WS", "format": utils.thousands_format(0), "read_only": True}),
                    "ne_ws": hx.Float(mode="input",default=None,  optionality="optional", view={"label": "NE WS", "format": utils.thousands_format(0), "read_only": True}),
                    "fl_pinnelas_ws": hx.Float(mode="input",default=None,  optionality="optional", view={"label": "FL Pinnelas", "format": utils.thousands_format(0), "read_only": True}),
                    "la_eq": hx.Float(mode="input",default=None,  optionality="optional", view={"label": "LA EQ", "format": utils.thousands_format(0), "read_only": True}),
                    "nm_eq": hx.Float(mode="input",default=None,  optionality="optional", view={"label": "NM EQ", "format": utils.thousands_format(0), "read_only": True}),
                    "nm_stress_eq": hx.Float(mode="input",default=None,  optionality="optional", view={"label": "NM Stress EQ", "format": utils.thousands_format(0), "read_only": True}),
                    "sf_eq": hx.Float(mode="input",default=None,  optionality="optional", view={"label": "SF EQ", "format": utils.thousands_format(0), "read_only": True}),     
                    }) for item, label in zip(["previous_year"], ["Previous Year"]) 
                },

                **{f"{item}": hx.Structure(view={"label": label}, children={
                    "carolinas_ws": hx.Float(mode="output", optionality="optional", view={"label": "Carolinas WS", "format": utils.percent_format(1)}),
                    "miami_dade_ws": hx.Float(mode="output", optionality="optional", view={"label": "Miami-Dade WS", "format": utils.percent_format(1)}),
                    "gulf_ws": hx.Float(mode="output", optionality="optional", view={"label": "Gulf WS", "format": utils.percent_format(1)}),
                    "ne_ws": hx.Float(mode="output", optionality="optional", view={"label": "NE WS", "format": utils.percent_format(1)}),
                    "fl_pinnelas_ws": hx.Float(mode="output", optionality="optional", view={"label": "FL Pinnelas", "format": utils.percent_format(1)}),
                    "la_eq": hx.Float(mode="output", optionality="optional", view={"label": "LA EQ", "format": utils.percent_format(1)}),
                    "nm_eq": hx.Float(mode="output", optionality="optional", view={"label": "NM EQ", "format": utils.percent_format(1)}),
                    "nm_stress_eq": hx.Float(mode="output", optionality="optional", view={"label": "NM Stress EQ", "format": utils.percent_format(1)}),
                    "sf_eq": hx.Float(mode="output", optionality="optional", view={"label": "SF EQ", "format": utils.percent_format(1)}),     
                    }) for item, label in zip(["yoy_growth"], ["YOY Growth"]) 
                },

            }),
        }),
    })