import hx_data_schema as hx
from data_schema.sch_utilities import percent_format, thousands_format, integer_format

def sch_rating_factors_details(cds):
    
    cds.extend_node_rater_defined("cds", {
        "rating_factors": hx.Structure(children={            
            "location": hx.Structure(children={
                "state": hx.Str(mode="output", async_input = ["rarc_task"], view={"label": "State"}),
                "percentage": hx.Float(mode="output", view={"label": "Percentage", "format": percent_format(0),"options": {"notSupported": {"style_cell": "hx-neutral"}}}),
                "risk_group": hx.Str(mode="output", view={"label": "Risk Group"}),
                "state_factor_selected": hx.Float(mode="output", view={"label": "State Factor"}),
                "states": hx.List(mode="input", async_input = ["rarc_task"], children={
                    "state": hx.Str(mode="input", default="Alabama", options_table="tbl_state", options_column="State", async_input = ["rarc_task"], view={"label": "State"}),
                    "percentage": hx.Float(mode="input", default=1.0, optionality="optional", async_input = ["rarc_task"], view={"label": "Percentage", "format": percent_format(0),"options": {"notSupported": {"style_cell": "hx-neutral"}}}),
                    "risk_group": hx.Str(mode="output", async_input = ["rarc_task"], view={"label": "Risk Group"}),
                    "state_factor_selected": hx.Float(mode="output", async_input = ["rarc_task"], view={"label": "State Factor"})
                }),
            }),            
            "written_contracts": hx.Structure(view= {"label":"Enter Insured's:"}, children={
                "percentage": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Percent of projects that use written contracts", "format": percent_format(0)}),
                "written_contracts_factor": hx.Float(mode="input", async_input=["rarc_task"], default=1.0, view={"label": "Use of Written Contracts Factor (Suggested Range: 0.95 - 1.05)"}),
            
            }),
            "longevity_with_carrier": hx.Structure(view= {"label":"Enter Insured's:"}, children={
                "yrs_insured": hx.Float(mode="input", async_input=["rarc_task"], default=1, optionality="optional", view={"label": "Number of years insured with the Company including this renewal","format": {"mantissa": 0}}),
                "lr": hx.Bool(mode="input", async_input=["rarc_task"], default=True, view={"label": "Loss ratio less than 50% whilst with the Company (calculated up to 5 years with the Company)?", "format": percent_format(0)}),
                "longevity_with_carrier_factor": hx.Float(mode="output", view={"label": "Longevity with Carrier Factor"}),

            }),
            "longevity": hx.Structure(view= {"label":"Enter Insured's:"}, children={
                "yr_start": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Business start year", "format": {"mantissa": 0}}),
                "yrs_in_business": hx.Float(mode="output", view={"label": "Years in business","format": {"mantissa": 0}}),
                "longevity_factor": hx.Float(mode="output", view={"label": "Longevity Factor"}),

            }),
            "erp": hx.Structure(view= {"label":"Enter Insured's:"}, children={
                "erp": hx.Str(mode="input", async_input=["rarc_task"], default_index=0, options_table="tbl_erp", options_column = "Extended Reporting Period", view={"label": "Extended Reporting Period"}),
                "erp_factor": hx.Float(mode="output", view={"label": "ERP Factor"}),

            }),
            "resi": hx.Structure(view= {"label":"Yes or No?"}, children={
                "resi_proj": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Residential Project?"}),                
                "multiple_units": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Multiple Units - Over 25?"}),
                "high_value": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "High Value - Largest Projects over $500k?"}),
                "condos": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Condos"}),
                "resi_proj_factor": hx.Float(mode="output", view={"label": "Residential Project Factor"}),
                "multiple_units_factor": hx.Float(mode="output", view={"label": "Multiple Units Factor"}),
                "high_value_factor": hx.Float(mode="output", view={"label": "High Value Factor"}),
                "condos_factor": hx.Float(mode="output", view={"label": "Condos Factor"}),

            }),
            "opt_coverages": hx.Structure(view= {"label":"Enter Insured's:"}, children={
                "full_prior_act": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Full Prior Acts Coverage"}),
                "full_prior_act_date": hx.Date(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Enter Retroactive Date"}),
                "cpl": hx.Bool(mode="input", async_input=["rarc_task"], default=True, view={"label": "CPL Coverage"}),                
                "tech": hx.Bool(mode="input", async_input=["rarc_task"], default=True, view={"label": "Tech Coverage"}),
                "non_contributary": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Primary NoN Contributary"}),                                
                "retro_factor": hx.Float(mode="output", view={"label": "Retro Step Factor"}),
                "cpl_factor": hx.Float(mode="output", view={"label": "CPL Coverage Factor"}),
                # tech coverage discount factor depends on whether cpl coverage is taken out
                "tech_cpl_factor": hx.Float(mode="output", view={"label": "Tech Coverage Factor"}),
                "non_contributary_factor": hx.Float(mode="output", view={"label": "Primary NoN Contributary Factor"}),

            }),          
            
        }),
    })

    pass