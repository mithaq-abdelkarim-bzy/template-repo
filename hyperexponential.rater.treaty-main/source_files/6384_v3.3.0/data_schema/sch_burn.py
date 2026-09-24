import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params
from algorithms.rate_constants import max_layers, max_exposure_years

def sch_burn(cds):

    # claims_available, claims_fgu, claims_net_of_deductible are standard fields; ignore

    # Add burn coverages node, by layer select which perils are included
    cds.extend_node_rater_defined("cds/layers",
     { "burn": hx.Structure(children={
            "burn_coverage": hx.Structure(children={
                **{f"coverage_{i}": hx.Bool(mode="input", default=True, view={"label": f"Coverage {i}"})
                for i in range(1,9)
                } ,
            }),
            "burn_result": hx.Structure(children={
                "avg_3_year": hx.Float(mode="output", optionality="optional", view = {"label": "3 Year Average", "format": utils.thousands_format(0)}),
                "avg_5_year": hx.Float(mode="output", optionality="optional", view = {"label": "5 Year Average", "format": utils.thousands_format(0)}),
                "avg_7_year": hx.Float(mode="output", optionality="optional", view = {"label": "7 Year Average", "format": utils.thousands_format(0)}),
                "avg_all_year": hx.Float(mode="output", optionality="optional", view = {"label": "All Year Average", "format": utils.thousands_format(0)}),
                "selection": hx.Str(mode="input", default="All Years", options=["3 Year", "5 Year", "7 Year", "All Years"], view={"label": "Base Period"}),
                "gross_burn_el": hx.Float(mode="output", optionality="optional", view = {"label": "Gross Burn EL", "format": utils.thousands_format(0)}),
                "gross_burn_sd": hx.Float(mode="output", optionality="optional", view = {"label": "Gross Burn SD", "format": utils.thousands_format(0)}),
                "gross_burn_lol": hx.Float(mode="output", optionality="optional", view = {"label": "Gross Burn LOL", "format": utils.percent_format(1)}),
                "gross_burn_sd_rol": hx.Float(mode="output", optionality="optional", view = {"label": "Gross Burn SD ROL", "format": utils.percent_format(1)}),

                "net_burn_el": hx.Float(mode="output", optionality="optional", view = {"label": "Net Burn EL", "format": utils.thousands_format(0)}),
                "net_burn_sd": hx.Float(mode="output", optionality="optional", view = {"label": "Net Burn SD", "format": utils.thousands_format(0)}),
                "net_burn_lol": hx.Float(mode="output", optionality="optional", view = {"label": "Net Burn LOL", "format": utils.percent_format(1)}),
                "net_burn_sd_rol": hx.Float(mode="output", optionality="optional", view = {"label": "Net Burn SD ROL", "format": utils.percent_format(1)}),

                "risk_xl_non_cat_burn_gross_el": hx.Float(mode="output", optionality="optional", view = {"label": "Non-Cat Burn Gross EL", "format": utils.thousands_format(0)}),
                "risk_xl_cat_burn_gross_el": hx.Float(mode="output", optionality="optional", view = {"label": "Cat Burn Gross EL", "format": utils.thousands_format(0)}),

                "risk_xl_rms_gross_el": hx.Float(mode="output", optionality="optional", view = {"label": "RMS Cat Gross EL", "format": utils.thousands_format(0)}),                            
            })
        })
    })

    # Add exposure and claims information into experience rating
    cds.extend_node_rater_defined("cds/experience_rating",
     {   
        "coverage": hx.Structure(children={
            **{f"coverage_{i}": hx.Str(mode="input", default="", view={"label": f"Coverage {i}"})
                for i in range(1,9)
             }
        }),
        "exposure": hx.Structure(children={
            "exposure_input_information": hx.Str(mode="input", default = """NB: Exposure for the year under consideration must be entered.
            If you do not have this information please enter a placeholder, for example roll forward last year's exposure.

            NB: Rate Change must be marked as 'Inclusive of Inflation' (Gross Rate Change) or 'Exclusive of Inflation' (Net Rate Change).
            """, view={"read_only": True}),           

            "exposure_start_year": hx.Int(mode="input", default=2010, options_column="year", options_table="table_years", view={"label": "Exposure Start Year (For Listing)", "format": {"thousandSeparated": False}}),
            "burn_start_year": hx.Int(mode="input", default=2018, options_column="year", options_table="table_years", view={"label": "Burn Start Year (For Calculation)", "format": {"thousandSeparated": False}}),
            "comments": hx.Str(mode="input", default="", view={"label": "Comments"}),
            "last_eight": hx.List(mode = "input", default_element_count=8,  children= {
                "year": hx.Float(mode = "output", view={"label": "Year", "format": {"thousandSeparated": False}}),
                "gnepi_actual": hx.Float(mode="output", validation={"min_value": 0}, view={"label": f"GNEPI (Actual)", "format": utils.thousands_format(0)}),
                "gnepi_projected": hx.Float(mode="output", validation={"min_value": 0}, view={"label": f"GNEPI (Projected)", "format": utils.thousands_format(0)}),
             }),
            "gnepi_exposure_segment" : hx.Structure(view={"label": "GNEPI Exposure"}, children={
                "allow_for_rc": hx.Bool(mode="input", default=True, view={"label": "Allow for RC?"}),
                "allow_for_other_changes": hx.Bool(mode="input", default=True, view={"label": "Allow for other changes?"}),
                "inflation_option": hx.Int(mode="input", default=1, options=[1, 2], view={"label": "Inflation Option"}),
                }),
            **{f"exposure_segment_{index}" : hx.Structure(view={"label": f"Exposure Segment {index}"}, children={
                "segment_name": hx.Str(mode="input", default="",optionality="optional", view={"label": "Segment Name"}),
                "segment_type": hx.Str(mode="input", default=None, optionality="optional", options_column="type", options_table="table_exposure_type", view={"label": "Segment Type"}),
                "allow_for_rc": hx.Bool(mode="input", default=False, view={"label": "Allow for RC?"}),
                "allow_for_other_changes": hx.Bool(mode="input", default=False, view={"label": "Allow for other changes?"}),
                "inflation_option": hx.Int(mode="input", default=1, options=[1, 2], view={"label": "Inflation Option"}),
                f"exposure_label": hx.Str(mode="output", optionality="optional"),
                f"exposure_change_label": hx.Str(mode="output", optionality="optional"),
                f"exposure_index_label": hx.Str(mode="output", optionality="optional"),
                f"total_index_label": hx.Str(mode="output", optionality="optional"),
                }) for index in range(1,4)
            },
            "rate_change_gross_net" : hx.Structure( children={
                "rate_change": hx.Str(mode="input", default="Inclusive of Inflation", options=["Inclusive of Inflation", "Exclusive of Inflation"], view={"label": "Rate Change", "style_cell": "hx-input"})
                }),
            "exposure_listing": hx.List(mode="input", default_element_count = max_exposure_years, children={
                "show_row_exposure": hx.Bool(mode="output", optionality = "optional"),
                "year": hx.Int(mode = "output", optionality = "optional", view={"label": "Year", "format": {"thousandSeparated": False}}),
                "pif": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": f"PIF", "format": utils.thousands_format(0)}),
                "gnepi_actual": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": f"GNEPI (Actual)", "format": utils.thousands_format(0)}),
                "gnepi_projected": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": f"GNEPI (Projected)", "format": utils.thousands_format(0)}),

                "rate_change": hx.Float(mode="input", default = None, optionality="optional", view={"label": "Rate Change", "format": {"output": "percent", "mantissa": 1}}),
                "inflation_option_1": hx.Float(mode="input", default = None, optionality="optional", view={"label": "Inflation Option 1", "format": {"output": "percent", "mantissa": 1}}),
                "inflation_option_2": hx.Float(mode="input", default = None, optionality="optional", view={"label": "Inflation Option 2", "format": {"output": "percent", "mantissa": 1}}),
                "other_changes": hx.Float(mode="input", default = None, optionality="optional", view={"label": "Other Changes", "format": {"output": "percent", "mantissa": 1}}),

                "gnepi_exposure_change": hx.Float(mode="output", optionality="optional", view={"label": "GNEPI Exposure Change"}),
                "gnepi_exposure_index": hx.Float(mode="output", optionality="optional", view={"label": "GNEPI Exposure Index"}),
                "gnepi_total_index": hx.Float(mode="output", optionality="optional", view={"label": "GNEPI Total Index"}),

                "risk_frequency_index": hx.Float(mode="output", optionality="optional", view={"label": "Frequency Index"}),
                "risk_avg_exposure_index": hx.Float(mode="output", optionality="optional", view={"label": "Average Exposure Index"}), 
                "risk_inflation_index": hx.Float(mode="output", optionality="optional", view={"label": "Inflation Index"}), 
                "risk_severity_index": hx.Float(mode="output", optionality="optional", view={"label": "Severity Index"}),                   

                **{f"exposure_value_{index}": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": f"Exposure Segment {index}", "format": utils.thousands_format(0)})
                    for index in range(1,4)
                },
                **{f"exposure_change_{index}": hx.Float(mode="output", optionality="optional", view={"label": f"Exposure Change {index}"})
                    for index in range(1,4)
                },
                **{f"exposure_index_{index}": hx.Float(mode="output", optionality="optional", view={"label": f"Exposure Index {index}"})
                    for index in range(1,4)
                },
                **{f"total_index_{index}": hx.Float(mode="output", optionality="optional", view={"label": f"Total Index {index}"})
                    for index in range(1,4)
                },                               
            })
        }),
        "claims_other": hx.Structure(children={
            "ten_largest": hx.List(mode = "output", children= {
                "year": hx.Float(mode = "output", view={"label": "Year", "format": {"thousandSeparated": False}}),
                "description": hx.Str(mode = "output", view={"label": "Description"}),
                "previous_year_total": hx.Float(mode = "output", view={"label": "Last Year Losses", "format": utils.thousands_format(0)}),
                "this_year_total": hx.Float(mode = "output", view={"label": "This Year Losses", "format": utils.thousands_format(0)}),
                "on_levelled_loss": hx.Float(mode = "output", view={"label": "Trended Losses", "format": utils.thousands_format(0)})
             }),
            "net_or_gross_reins_calc": hx.Str(mode="input", default="Gross", options = ["Gross", "Net"] , view={"label": "Gross or Net (of reinstatements) Calculation", "style_cell": "hx-input"}),
            "risk_xl_use_rms_cat": hx.Bool(mode="input", default=False, view={"label": "Use RMS Cat", "style_cell": "hx-input"}),
            "show_gross_fields": hx.Bool(mode="output"),
            "show_net_fields": hx.Bool(mode="output"),
            "comments": hx.Str(mode="input", default="", view={"label": "Comments"}),
            "burn_output_comments": hx.Str(mode="input", default="", view={"label": "Comments"}),
            **{f"loss_segment_label_{index}": hx.Str(mode="output", optionality="optional")
                    for index in range(1, 4)
                },
            **{f"show_loss_layer_{index}": hx.Bool(mode="output", optionality="optional")
                    for index in range(1, max_layers + 1)
            },
             "coverage_options": hx.List(mode = "output", children= {
                "option": hx.Str(mode = "output")
             }),
            "burn_year_result": hx.List(mode="input", default_element_count = max_exposure_years, children={
                "show_row": hx.Bool(mode="output", optionality = "optional"),
                "year": hx.Int(mode = "output", optionality = "optional", view={"label": "Year", "format": {"thousandSeparated": False}}),
                "non_zero_claim_count": hx.Int(mode = "output", optionality = "optional", view={"label": "Claim Count", "format": {"thousandSeparated": False}}),
                "freq_per_m_prem": hx.Float(mode = "output", optionality = "optional", view={"label": "Frequency per CCYm Premium", "format": {"thousandSeparated": False}}),
                "nominal_loss": hx.Float(mode = "output", optionality = "optional", view={"label": "Nominal Loss", "format": {"thousandSeparated": False}}),
                "on_levelled_loss": hx.Float(mode = "output", optionality = "optional", view={"label": "OL Loss", "format": utils.thousands_format(0)}),
                "severity": hx.Float(mode = "output", optionality = "optional", view={"label": "Severity", "format": utils.thousands_format(0)}),

                # show layer losses for each loss
                **{f"loss_layer_{index}": hx.Float(mode="output", optionality="optional", view={"label": f"Layer {index}", "format": utils.thousands_format(0)})
                    for index in range(1, max_layers + 1)
                },
            }), 
        }),
        "claims": hx.List(mode="input",default_element_count = 6, children={
            "year": hx.Int(mode = "input",default = None, optionality = "optional", view={"label": "Year", "format": {"thousandSeparated": False}}),
            "currency": hx.Str(mode="input", default=None, optionality="optional", options_column="currency", options_table="table_currency", view={"label": "Loss Currency"}),
            "description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Description"}),
            "large_loss": hx.Str(mode="input", default=None, optionality="optional", options_table="table_large_loss_event", options_column="event", view={"label": "Large Loss Event"}),
            "coverage": hx.Str(mode="input", default=None, optionality="optional", options_data = "../../../claims_other/coverage_options", options_field = "option", view={"label": "Coverage"}),

            "cat_non_cat": hx.Str(mode="input", default=None, optionality="optional", options = ["Cat", "Non-Cat"], view={"label": "Cat/Non-Cat"}),
            "cat_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Cat Name"}),

            "gnepi_loss": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": f"GNEPI Loss", "format": utils.thousands_format(0)}),
            
            **{f"loss_segment_{index}": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": f"Loss Segment {index}", "format": utils.thousands_format(0)})
                for index in range(1, 4)
            },

            "this_year_total": hx.Float(mode="output", optionality="optional", view = {"label": "This Year Total", "format": utils.thousands_format(0)}),
            "previous_year_total": hx.Float(mode="input", default = None, optionality="optional", view = {"label": "Previous Year Total", "format": utils.thousands_format(0)}),
            "movement": hx.Float(mode="output", optionality="optional", view = {"label": "Movement", "format": utils.thousands_format(0)}),
            "loss_type": hx.Str(mode="input", default = "Nominal", options = ["Nominal", "SuperCat", "As-If", "SuperCat As-If"], view = {"label": "Loss Type"}),                
            "as_if_loss": hx.Float(mode="input", default=None, optionality="optional", view = {"label": "As-If Loss", "format": utils.thousands_format(0)}),
            "on_levelled_loss": hx.Float(mode="output", optionality="optional", view = {"label": "On-Levelled Loss", "format": utils.thousands_format(0)}),
            "return_period": hx.Int(mode="input", default=None, optionality="optional", view = {"label": "Return Period"}),
            "comment": hx.Str(mode="input", default="", view={"label": "Comment"}),

            # show layer losses for each loss
            **{f"loss_layer_{index}": hx.Float(mode="output", optionality="optional", view={"label": f"Loss Layer {index}", "format": utils.thousands_format(0)})
                for index in range(1, max_layers + 1)
            },           
        }), 
    })