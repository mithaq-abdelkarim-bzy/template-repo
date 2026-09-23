import hx_data_schema as hx
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_final_selections_and_summary(cds):
    # Overrides of base properties
    cds.override_node_properties(f"cds/currencies/source_currency", {
        "default": "USD",
        "options_column": "ccy", 
        "options_table": "table_input_currency",
        "optionality": "required",
        "view": {"label": "Currency"}
    })

    # Case Priced BPI
    cds.extend_node_rater_defined("cds/layers", {
        "bpi_case_priced": hx.Float(mode="input", default=0, optionality="required", view={"label": "BPI (Case Priced)", "format": {"output": "percent", "mantissa": 1}}),
        "bench_prem_case_priced" : hx.Float(mode="output", view={"label":"Gross Benchmark Premium", "format":thousands_format()}),
        "technical_prem_case_priced" : hx.Float(mode="output", view={"label":"Gross Technical Premium", "format":thousands_format()}),
        "quoted_prem_kpi_summary" : hx.Float(mode="input", optionality="optional", default=None, view={"label": "Gross Quoted Premium", "format":thousands_format()}),
        "implied_roc_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),
        "tpi_case_priced": hx.Float(mode="output", optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
    })

    cds.override_node_properties(f"cds/layers/written_line", {"async_input": ["generate_rationale_doc_task"]})
    cds.override_node_properties(
        "cds/layers/tpi_pre_uw_adj", {
            "view": {
                "options": {
                    "kpi_summary_option": {
                        "label": "TPI",
                    }
                }
            }
        }
    )
    
    # Policy Information ~~~
    cds.extend_node_rater_defined(f"cds", {
        "final_selection": hx.Structure(children={
            "policy_ref" : hx.Str(mode="output", view={"label":"Policy Reference"}),
            "start_date" : hx.Date(mode="output", view={"label": "Start Date"}),
            "end_date" : hx.Date(mode="output", view={"label":"End Date"}),
            "policy_class" : hx.Str(mode="output", view={"label": "Class"}), 
            "currency" : hx.Str(mode="output", view={"label":"Currency"}),

            # Risk Quality Scoring ~~~
            "quality_score" : hx.Int(mode="output",view={"label":"Risk Quality Score (Out of 100)"}),
        })
    })

    ## Jewellers Block
    cds.extend_node_rater_defined(f"cds/layers", {
        "jb_final_selection": hx.List(mode="input", children={  
            "high_level_q1" : hx.Bool(mode="input", default=False, view={"label":"Established insurance pedigree"}),
            "high_level_q2" : hx.Bool(mode="input", default=False, view={"label":"Proven claims record"}),
            "high_level_q3" : hx.Bool(mode="input", default=False, view={"label":"Territory within appetite (UWR knowledge/prior exp."}),
            "high_level_q4" : hx.Bool(mode="input", default=False, view={"label":"Survery program with recommendations in last 3 years"}),
            "high_level_q5" : hx.Bool(mode="input", default=False, view={"label":"Central Station Alarm, min Grade 4 signalling (or equiv.)"}),
            "high_level_q6" : hx.Bool(mode="input", default=False, view={"label":"CCTV with remote monitoring"}),
            "high_level_q7" : hx.Bool(mode="input", default=False, view={"label":"Safe (positioned against 3rd party wall)"}),
            "high_level_q8" : hx.Bool(mode="input", default=False, view={"label":"Opening / Closing procedures"}),
            "high_level_q9" : hx.Bool(mode="input", default=False, view={"label":"No High End Luxury Watches within inventory"}),
            "high_level_q10" : hx.Bool(mode="input", default=False, view={"label":"References"}),     

            "specific_q1" : hx.Str(mode="input",default="Low", view={"label":"Stock limit v last recorded inventory"}, options_table="table_input_low_high", options_column="Answer"),
            "specific_q2" : hx.Bool(mode="input",default=False, view={"label":"Balance of operating sub-limits"}),
            "specific_q3" : hx.Str(mode="input",default="Long Term", view={"label":"Increased self retention level"}, options_table="table_input_term", options_column="Answer"),
            "specific_q4" :hx.Bool(mode="input",default=False, view={"label":"Enhanced security / protections"}),
            "specific_q5" :hx.Bool(mode="input",default=False, view={"label":"Basis of Settlements"}),
            "specific_q6" :hx.Bool(mode="input",default=False, view={"label":"Any ancilliary coverage requests"})
        })
    }),

    ## Fine Art NA

    ## General Specie NA

    ## Cash In Transit
    cds.extend_node_rater_defined(f"cds/layers", {
        "cit_final_selection": hx.List(mode="input", children={ 
            "high_level_q1" : hx.Bool(mode="input", default=False, view={"label":"Established insurance pedigree"}),
            "high_level_q2" : hx.Bool(mode="input", default=False, view={"label":"Proven claims record"}),
            "high_level_q3" : hx.Bool(mode="input", default=False, view={"label":"Terriroty within appetite (UWR knowledge/prior exp."}),
            "high_level_q4" : hx.Bool(mode="input", default=False, view={"label":"Survery program with recommendations in last 3 years"}),
            "high_level_q5" : hx.Bool(mode="input", default=False, view={"label":"Central Station Alarm, min Grade 4 signalling (or equiv.)"}),
            "high_level_q6" : hx.Bool(mode="input", default=False, view={"label":"CCTV with remote monitoring"}),
            "high_level_q7" : hx.Bool(mode="input", default=False, view={"label":"Vault / Safe rating with Dual opening procedures"}),
            "high_level_q8" : hx.Bool(mode="input", default=False, view={"label":"Opening / Closing procedures"}),
            "high_level_q9" : hx.Bool(mode="input", default=False, view={"label":"Armoured car specifications"}),
            "high_level_q10" : hx.Bool(mode="input", default=False, view={"label":"References"}),

            "specific_q1" : hx.Str(mode="input",default="Low", view={"label":"Static Limit, Transit limit, Pavement limit"}, options_table="table_input_low_high", options_column="Answer"),
            "specific_q2" : hx.Bool(mode="input",default=False, view={"label":"Balance of operating sub-limits"}),
            "specific_q3" : hx.Str(mode="input",default="Long Term", view={"label":"Increased self retention level"}, options_table="table_input_term", options_column="Answer"),
            "specific_q4" :hx.Bool(mode="input",default=False, view={"label":"Enhanced security / protections"}),
            "specific_q5" :hx.Bool(mode="input",default=False, view={"label":"Employee background checks / tests"}),
            "specific_q6" :hx.Bool(mode="input",default=False, view={"label":"Annual Carrying splits (Secure / retail / ATM) & revenues"})
        })
    }),


    # Claims Summary ~~~
    for sub_group in ["premises", "travel", "additional"]:
        ## Jewellers Block
        cds.extend_node_rater_defined(f"cds/layers/coverages/jb_{sub_group}", { 
            "final_summary_tsi" : hx.Float(mode="output",view={"label":"TSI (cnv)", "format":thousands_format()}),
            "final_summary_prem_post_ded" : hx.Float(mode="output",view={"label":"Prem Post Ded", "format":thousands_format()}),
            "final_summary_loss_cost_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Final Loss Cost\nLast Year", "format":thousands_format()}),
            "final_summary_final_loss_cost" : hx.Float(mode="output",view={"label":"Final Loss Cost\nThis Year", "format":thousands_format()})
        })

        cds.override_node_properties(f"cds/layers/coverages/jb_{sub_group}", {"view": {"label": f"{sub_group}".capitalize()}})

        ## Fine Art
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_{sub_group}", {
            "final_summary_tsi" : hx.Float(mode="output",view={"label":"TSI (cnv)", "format":thousands_format()}),
            "final_summary_prem_post_ded" : hx.Float(mode="output",view={"label":"Prem Post Ded", "format":thousands_format()}),
            "final_summary_loss_cost_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Final Loss Cost\nLast Year", "format":thousands_format()}),
            "final_summary_final_loss_cost" : hx.Float(mode="output",view={"label":"Final Loss Cost\nThis Year", "format":thousands_format()})
        })

        cds.override_node_properties(f"cds/layers/coverages/fa_{sub_group}", {"view": {"label": f"{sub_group}".capitalize()}})

    for sub_group in ["metals", "cash", "securities", "additional"]:
        ## General Specie
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_{sub_group}", {
            "final_summary_tsi" : hx.Float(mode="output",view={"label":"TSI (cnv)", "format":thousands_format()}),
            "final_summary_prem_post_ded" : hx.Float(mode="output",view={"label":"Prem Post Ded", "format":thousands_format()}),
            "final_summary_loss_cost_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Final Loss Cost\nLast Year", "format":thousands_format()}),
            "final_summary_final_loss_cost" : hx.Float(mode="output",view={"label":"Final Loss Cost\nThis Year", "format":thousands_format()})
        })

        cds.override_node_properties(f"cds/layers/coverages/gs_{sub_group}", {"view": {"label": f"{sub_group}".capitalize()}})

    for sub_group in ["premises", "additional"]:
        ## Cash in Transit
        cds.extend_node_rater_defined(f"cds/layers/coverages/cit_{sub_group}", {
            "final_summary_tsi" : hx.Float(mode="output",view={"label":"TSI (cnv)", "format":thousands_format()}),
            "final_summary_prem_post_ded" : hx.Float(mode="output",view={"label":"Prem Post Ded", "format":thousands_format()}),
            "final_summary_loss_cost_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Final Loss Cost\nLast Year", "format":thousands_format()}),
            "final_summary_final_loss_cost" : hx.Float(mode="output",view={"label":"Final Loss Cost\nThis Year", "format":thousands_format()})
        }),

        cds.override_node_properties(f"cds/layers/coverages/cit_{sub_group}", {"view": {"label": f"{sub_group}".capitalize()}})


    cds.extend_node_rater_defined(f"cds", {
        ## Final totals table
        "final_claims_summary_table" : hx.Structure(children={
            "tsi" : hx.Float(mode="output",view = {"label":"TSI (cnv)", "format":thousands_format()}),
            "exp_prem_post_ded" : hx.Float(mode="output",view = {"label":"Exposure Premium Post Ded", "format":thousands_format()}),
            "assumed_comms" : hx.Float(mode="output",view = {"label":"Assumed Comms", "format":percent_format(2)}),
            "assumed_lr_gn" : hx.Float(mode="output",view = {"label":"Assumed Loss Ratio (GN)", "format":percent_format(2)}),
            "exposure_loss_cost_length_adj" : hx.Float(mode="output",view = {"label":"Exposure Loss Cost\n(Policy Length Adj)", "format":thousands_format()}),
            "experience_loss_cost_length_adj" : hx.Float(mode="output",view = {"label":"Experience Loss Cost\n(Policy Length Adj)", "format":thousands_format()}),
            "rec_exp_weight" : hx.Float(mode="output",view = {"label":"Recommended Experience Weight", "format":percent_format(2)}),
            "sel_exp_weight" : hx.Float(mode="input",view = {"label":"Selected Experience Weight", "format":percent_format(2)}, default=0.0),
            "loss_cost_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view = {"label":"Final Loss Cost LY (cnv)", "format":thousands_format()}),
            "final_loss_cost" : hx.Float(mode="output", view = {"label":"Final Loss Cost (cnv)", "format":thousands_format()}),
            "perc_cat_bp" : hx.Float(mode="output", view = {"label":"% Cat BP", "format":percent_format(2)}),
            "perc_cat_data" : hx.Float(mode="output", view = {"label":"% Cat Data", "format":percent_format(2)}),
            "perc_cat_sel" : hx.Float(mode="input", view = {"label":"% Cat Selected", "format":percent_format(2)}, default=0.0)
        }),
        
        ## Final totals table
        "final_claims_prioryear_table" : hx.Structure(children={
            "tsi" : hx.Float(mode="output",view = {"label":"TSI (cnv)"}),
            "exp_prem_post_ded" : hx.Float(mode="output",view = {"label":"Exposure Premium Post Ded", "format":thousands_format()}),
            "assumed_comms" : hx.Float(mode="output",view = {"label":"Assumed Comms", "format":percent_format(2)}),
            "assumed_lr_gn" : hx.Float(mode="output",view = {"label":"Assumed Loss Ratio (GN)", "format":percent_format(2)}),
            "exposure_loss_cost_length_adj" : hx.Float(mode="output",view = {"label":"Exposure Loss Cost\n(Policy Length Adj)", "format":thousands_format()}),
            "experience_loss_cost_length_adj" : hx.Float(mode="output",view = {"label":"Experience Loss Cost\n(Policy Length Adj)", "format":thousands_format()}),
            "rec_exp_weight" : hx.Float(mode="output",view = {"label":"Recommended Experience Weight", "format":percent_format(2)}),
            "sel_exp_weight" : hx.Float(mode="output",view = {"options": { "invalid": {"style_cell": "hx-neutral"}}, "label":"Selected Experience Weight", "format":percent_format(2)}),
            "loss_cost_ly" : hx.Float(mode="output", view = {"label":"Final Loss Cost LY (cnv)", "format":thousands_format()}),
            "final_loss_cost" : hx.Float(mode="output", view = {"label":"Final Loss Cost (cnv)", "format":thousands_format()}),
            "perc_cat_bp" : hx.Float(mode="output", view = {"label":"% Cat BP", "format":percent_format(2)}),
            "perc_cat_data" : hx.Float(mode="output", view = {"label":"% Cat Data", "format":percent_format(2)}),
            "perc_cat_sel" : hx.Float(mode="output", view = {"label":"% Cat Selected", "format":percent_format(2)})
        }),

        # Premium Summary ~~~
        "final_prem_summary_limit_table" : hx.Structure(children = {
            "limit" : hx.Float(mode="input",view={"options": { "invalid": {"style_cell": "hx-neutral"}}, "label":"Limit/Line Size", "format":thousands_format()}, default=0.0),
            "excess" : hx.Float(mode="input",view={"options": { "invalid": {"style_cell": "hx-neutral"}}, "label":"Excess", "format":thousands_format()}, default=0.0),
            "uw_auth_limit" : hx.Float(mode="output",view={"label":"Underwriting Authority Limit/Line Size", "format":thousands_format()}),
            "uw_auth_flag" : hx.Str(mode="output",view={"label":"Underwriting Authority Flag"})
        }),

        "final_premium_summary_table" : hx.Structure(view = {"label":"Current Year"},children = {
            "loss_cost" : hx.Float(mode="output",view={"label":"Loss Cost (cnv)", "format":thousands_format()}),
            "tech_prem" : hx.Float(mode="output",view={"label":"Tech Prem (Pre UW Adj)", "format":thousands_format()}),
            "bench_prem" : hx.Float(mode="output",view={"label":"Bench Prem (Pre UW Adj)", "format":thousands_format()}),
            "uw_credit" : hx.Float(mode="input",view={"label":"UW Credit","format":percent_format(2)}, default=0.0),
            "client_credit" : hx.Float(mode="input",view={"label":"Client Credit","format":percent_format(2)}, default=0.0),
            "risk_score_credit" : hx.Float(mode="input",view={"label":"Risk Score Credit","format":percent_format(2)}, default=0.0),
            "total_credit" : hx.Float(mode="output",view={"label":"Total Credit","format":percent_format(2)}),
            "tech_prem_adj" : hx.Float(mode="output",view={"label":"Tech Prem (Post UW Adj)", "format":thousands_format()}),
            "bench_prem_adj" : hx.Float(mode="output",view={"label":"Bench Prem (Post UW Adj)", "format":thousands_format()}),
            "quoted_premium_slip_curr" : hx.Float(mode="input",view={"options": { "invalid": {"style_cell": "hx-neutral"}}, "label":"Quote Premium (Slip Currency)"}, default=0.0),
            "quoted_premium" : hx.Float(mode="output",view={"label":"Quote Premium (USD)"}),
            "acq_cost" : hx.Float(mode="input",view={"label":"Acq Costs","format":percent_format(2)}, default=0.0),
            "signed_line" : hx.Float(mode="input",view={"label":"Signed Line","format":percent_format(2)}, default=0.0),
            "written_line" : hx.Float(mode="output",view={"label":"Written Line","format":percent_format(2)}),
            "tech_prem_adj" : hx.Float(mode="output",view={"label":"Tech Prem (Post UW Adj)","format":thousands_format()}),
            "bench_prem_adj" : hx.Float(mode="output",view={"label":"Bench Prem (Post UW Adj)","format":thousands_format()}),
            "tpi_pre_uw_adj" : hx.Float(mode="output",view={"label":"TPI (Pre UW Adj)","format":percent_format(2)}),
            "bpi_pre_uw_adj" : hx.Float(mode="output",view={"label":"BPI (Pre UW Adj)","format":percent_format(2)}),
            "tpi" : hx.Float(mode="output",view={"label":"TPI (Post UW Adj)","format":percent_format(2)}),
            "bpi" : hx.Float(mode="output",view={"label":"BPI (Post UW Adj)","format":percent_format(2)}),
            "implied_roc_pre_uw_adj" : hx.Float(mode="output",view={"label":"Implied RoC (Pre UW Adj)","format":percent_format(2)}),
            "expected_profit_pre_uw_adj" : hx.Float(mode="output",view={"label":"Expected Profit (Pre UW Adj)", "format":thousands_format()}),
            "implied_roc" : hx.Float(mode="output",view={"label":"Implied RoC (Post UW Adj)","format":percent_format(2)}),
            "expected_profit" : hx.Float(mode="output",view={"label":"Expected Profit (Post UW Adj)", "format":thousands_format()}),
            "gg_achieved_rate" : hx.Float(mode="output", view = {"label":"GG Achieved Rate", "format":percent_format(2)}),
            "gn_achieved_rate" : hx.Float(mode="output", view = {"label":"GN Achieved Rate", "format":percent_format(2)})
        })
    })


    for sub_group in ["premises", "travel", "additional"]:
        ### Jewellers Block
        cds.extend_node_rater_defined(f"cds/layers/coverages/jb_{sub_group}", {
            "final_premium_summary_tsi" : hx.Float(mode="output",view={"label":"TSI (cnv)", "format":thousands_format()}),
            "final_premium_summary_tech_rate" : hx.Float(mode="output",view={"label":"Technical Rate","format":percent_format(2)}),
            "final_premium_summary_ach_rate" : hx.Float(mode="output",view={"label":"Achieved Rate","format":percent_format(2)}),
            "final_premium_summary_tsi_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year TSI (cnv)", "format":thousands_format()}),
            "final_premium_summary_tech_rate_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year Technical Rate","format":percent_format(2)}),
            "final_premium_summary_ach_rate_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year Achieved Rate","format":percent_format(2)})
        }),   

        ### Fine Art
        cds.extend_node_rater_defined(f"cds/layers/coverages/fa_{sub_group}", {
            "final_premium_summary_tsi" : hx.Float(mode="output",view={"label":"TSI (cnv)", "format":thousands_format()}),
            "final_premium_summary_tech_rate" : hx.Float(mode="output",view={"label":"Technical Rate","format":percent_format(2)}),
            "final_premium_summary_ach_rate" : hx.Float(mode="output",view={"label":"Achieved Rate","format":percent_format(2)}),
            "final_premium_summary_tsi_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year TSI (cnv)", "format":thousands_format()}),
            "final_premium_summary_tech_rate_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year Technical Rate","format":percent_format(2)}),
            "final_premium_summary_ach_rate_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year Achieved Rate","format":percent_format(2)})
        })
    
    for sub_group in ["metals", "cash", "securities", "additional"]:
        ### General Specie
        cds.extend_node_rater_defined(f"cds/layers/coverages/gs_{sub_group}", {
            "final_premium_summary_tsi" : hx.Float(mode="output",view={"label":"TSI (cnv)", "format":thousands_format()}),
            "final_premium_summary_tech_rate" : hx.Float(mode="output",view={"label":"Technical Rate","format":percent_format(2)}),
            "final_premium_summary_ach_rate" : hx.Float(mode="output",view={"label":"Achieved Rate","format":percent_format(2)}),
            "final_premium_summary_tsi_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year TSI (cnv)", "format":thousands_format()}),
            "final_premium_summary_tech_rate_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year Technical Rate","format":percent_format(2)}),
            "final_premium_summary_ach_rate_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year Achieved Rate","format":percent_format(2)})
        })

    for sub_group in ["premises", "additional"]:
        ### Cash in Transit 
        cds.extend_node_rater_defined(f"cds/layers/coverages/cit_{sub_group}", {
            "final_premium_summary_tsi" : hx.Float(mode="output",view={"label":"TSI (cnv)", "format":thousands_format()}),
            "final_premium_summary_tech_rate" : hx.Float(mode="output",view={"label":"Technical Rate","format":percent_format(2)}),
            "final_premium_summary_ach_rate" : hx.Float(mode="output",view={"label":"Achieved Rate","format":percent_format(2)}),
            "final_premium_summary_tsi_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year TSI (cnv)", "format":thousands_format()}),
            "final_premium_summary_tech_rate_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year Technical Rate","format":percent_format(2)}),
            "final_premium_summary_ach_rate_ly" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Prior Year Achieved Rate","format":percent_format(2)})
        })  


    cds.extend_node_rater_defined(f"cds", {
        ## Prior year metrics
        "final_prem_prioryear_table" : hx.Structure(view = {"label":"Prior Year"},children = {
            "loss_cost" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Loss Cost (cnv)", "format":thousands_format()}),
            "tech_prem" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Technical Premium", "format":thousands_format()}),
            "bench_prem" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Benchmark Premium", "format":thousands_format()}),
            "uw_credit" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"UW Credit","format":percent_format(2)}),
            "client_credit" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Client Credit","format":percent_format(2)}),
            "risk_score_credit" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Risk Score Credit","format":percent_format(2)}),
            "total_credit" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Total Credit","format":percent_format(2)}),
            "tech_prem_adj" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Tech Prem Adj", "format":thousands_format()}),
            "bench_prem_adj" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Bench Prem Adj", "format":thousands_format()}),
            "quoted_premium_slip_curr" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"options": { "invalid": {"style_cell": "hx-output"}},"label":"Quote Premium (Slip Currency)", "format":thousands_format()}),
            "quoted_premium" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Quote Premium (USD)", "format":thousands_format()}),
            "acq_cost" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"options": { "invalid": {"style_cell": "hx-output"}}, "label":"Acq Costs","format":percent_format(2)}),
            "signed_line" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"options": { "invalid": {"style_cell": "hx-output"}}, "label":"Signed Line","format":percent_format(2)}), #make this NA / blank
            "written_line" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Written Line","format":percent_format(2)}), #make this NA / blank
            "tpi_pre_uw_adj" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"TPI (Pre UW Adj)","format":percent_format(2)}),
            "bpi_pre_uw_adj" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"BPI (Pre UW Adj)","format":percent_format(2)}),
            "tpi" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"TPI (Post UW Adj)","format":percent_format(2)}),
            "bpi" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"BPI (Post UW Adj)","format":percent_format(2)}),
            "implied_roc_pre_uw_adj" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Implied RoC (Pre UW Adj)","format":percent_format(2)}),
            "expected_profit_pre_uw_adj" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Expected Profit (Pre UW Adj)", "format":thousands_format()}),
            "implied_roc" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Implied RoC (Post UW Adj)","format":percent_format(2)}),
            "expected_profit" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Expected Profit (Post UW Adj)", "format":thousands_format()}),
            "gg_achieved_rate" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view = {"label":"GG Achieved Rate", "format":percent_format(2)}),
            "gn_achieved_rate" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view = {"label":"GN Achieved Rate", "format":percent_format(2)})
        }),
          
        ## Technical premium breakdown table
        "final_prem_summary_tp_table" : hx.Structure(view = {"label":"Pre UW Adj"},children = {
            "loss_cost" : hx.Float(mode="output",view={"label":"Loss Cost", "format":thousands_format()}),
            "var_exp" : hx.Float(mode="output",view={"label":"Variable Expenses", "format":thousands_format()}),
            "fixed_exp" : hx.Float(mode="output",view={"label":"Fixed Expenses", "format":thousands_format()}),
            "inv_income" : hx.Float(mode="output",view={"label":"Investment Income", "format":thousands_format()}),
            "reins" : hx.Float(mode="output",view={"label":"Reinsurance", "format":thousands_format()}),
            "acq_cost" : hx.Float(mode="output",view={"label":"Acq Costs","format":percent_format(2)}),
            "cap_load" : hx.Float(mode="output",view={"label":"Capital Load", "format":thousands_format()}),
            "tech_prem" : hx.Float(mode="output",view={"label":"Technical Premium", "format":thousands_format()}),
            "allocated_capital" : hx.Float(mode="output",view={"label":"All. Capital", "format":thousands_format()})
        }),

        "final_prem_summary_tp_postuwadj_table" : hx.Structure(view = {"label":"Post UW Adj"},children = {
            "loss_cost" : hx.Float(mode="output",view={"label":"Loss Cost", "format":thousands_format()}),
            "var_exp" : hx.Float(mode="output",view={"label":"Variable Expenses", "format":thousands_format()}),
            "fixed_exp" : hx.Float(mode="output",view={"label":"Fixed Expenses", "format":thousands_format()}),
            "inv_income" : hx.Float(mode="output",view={"label":"Investment Income", "format":thousands_format()}),
            "reins" : hx.Float(mode="output",view={"label":"Reinsurance", "format":thousands_format()}),
            "acq_cost" : hx.Float(mode="output",view={"label":"Acq Costs","format":percent_format(2)}),
            "cap_load" : hx.Float(mode="output",view={"label":"Capital Load", "format":thousands_format()}),
            "tech_prem" : hx.Float(mode="output",view={"label":"Technical Premium", "format":thousands_format()}),
            "allocated_capital" : hx.Float(mode="output",view={"label":"All. Capital", "format":thousands_format()})
        })
    })


    # Rate Change Summary ~~~
    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "risk_adj_premium": hx.Structure(view={"label": "Risk Adj Prem"}, children={
            "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": thousands_format()}),
            "uw_selected": hx.Float(mode="override", view={"label": "UW Selected %", "format": thousands_format()}),
            "comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
        }),
        # "risk_adj_premium_override": hx.Float(mode="input", view={"label":"Risk Adj Prem", "format":thousands_format()}, default=0.0),
        "rate_change_calculated_pryr": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"RARC Last Year","format":percent_format(2)}),
        "rate_change_uw_selected_pryr": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"RARC Last Year","format":percent_format(2)}),
    
        # For displaying rate change summaries
        # SA: Moved here so that it works with view
        "expiry_premium": hx.Structure(view={"label":"Expiring Premium"}, children={
            "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": thousands_format()}, async_output=["expiring_policy_fetch_task", "start_renewal_task"]),
            "uw_selected": hx.Float(mode="override", view={"label": "UW Selected %", "format": thousands_format()}, async_output=["expiring_policy_fetch_task", "start_renewal_task"]),
            "comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}, async_output=["expiring_policy_fetch_task", "start_renewal_task"]),
        }),
        "quoted_premium": hx.Float(mode="output",view={"label":"Quoted Prem", "format": thousands_format()}),

        # SA: The below might be duplication - could another item in the rate_change structure handle these? The mapping table
        # placed them pointing outside of rate_change which doesn't work for the view
        "pure_rc": hx.Float(mode="output",view={"label":"Pure RC","format":percent_format(2)}),
        "business": hx.Float(mode="output",view={"label":"Business","format":percent_format(2)}),
    })

    cds.override_node_properties("cds/layers/rate_change", {"view": {"label": "UW Adj"}})
            
    cds.extend_node_rater_defined("cds", {
        # "final_rc_total_summary" : hx.Structure(view = {"label":"Total"}, children = {
        #     "expiry_premium" : hx.Float(mode="override", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Expiring Premium", "format":thousands_format()}),
        #     "quoted_premium" : hx.Float(mode="output",view={"label":"Quoted Prem", "format":thousands_format()})
        # }),
        "final_rc_uwadj_summary" : hx.Structure(view = {"label":"UW Adj"}, children = {
            "expiry_premium" : hx.Float(mode="override", async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label":"Expiring Premium", "format":thousands_format()}),
            "quoted_premium" : hx.Float(mode="output",view={"label":"Quoted Prem", "format":thousands_format()})
        }),
        # "final_rc_total_summary2" : hx.Structure(view = {"label":"Total"}, children = {
        #     "pure_rc" : hx.Float(mode="output",view={"label":"Pure RC","format":percent_format(2)}),
        #     "business" : hx.Float(mode="output",view={"label":"Business","format":percent_format(2)}),
        # }),
        "final_rc_uwadj_summary2" : hx.Structure(view = {"label":"UW Adj"}, children = {
            "pure_rc_uw_adj" : hx.Float(mode="output",view={"label":"Pure RC","format":percent_format(2)}),
            "business_uw_adj" : hx.Float(mode="output",view={"label":"Business","format":percent_format(2)}),
        }),

        # Waterfall ~~~
        "final_rc_waterfall": hx.Structure(view = {"label":"Waterfall"}, children = {
            "exp_prem" : hx.Float(mode="output",view={"label":"Expiring Premium", "format":thousands_format()}),
            "exposure" : hx.Float(mode="output",view={"label":"Exposure", "format":thousands_format()}),
            "deduct" : hx.Float(mode="output",view={"label":"Deductibles", "format":thousands_format()}),
            "limit" : hx.Float(mode="output",view={"label":"Limits", "format":thousands_format()}),
            "risk" : hx.Float(mode="output",view={"label":"Risk", "format":thousands_format()}),
            "t_and_cs" : hx.Float(mode="output",view={"label":"T&Cs", "format":thousands_format()}),
            "risk_adj_premium" : hx.Float(mode="output",view={"label":"Risk Adj Prem", "format":thousands_format()}),
            "quoted_premium" : hx.Float(mode="output",view={"label":"Quote Premium", "format":thousands_format()})
        }),

        # Waterfall - TP ~~~
        "final_tp_waterfall": hx.Structure(view = {"label":"Waterfall"}, children = {
            "loss_cost" : hx.Float(mode="output",view={"label":"Loss Cost", "format":thousands_format()}),
            "var_expense" : hx.Float(mode="output",view={"label":"Variable Expenses", "format":thousands_format()}),
            "fixed_expense" : hx.Float(mode="output",view={"label":"Fixed Expenses", "format":thousands_format()}),
            "tot_expense" : hx.Float(mode="output",view={"label":"Variable Expenses", "format":thousands_format()}),
            "inv_income" : hx.Float(mode="output",view={"label":"Investment Income", "format":thousands_format()}),
            "ri" : hx.Float(mode="output",view={"label":"Reinsurance", "format":thousands_format()}),
            "capital" : hx.Float(mode="output",view={"label":"Capital Charge", "format":thousands_format()}),
            "brokerage" : hx.Float(mode="output",view={"label":"Brokerage", "format":thousands_format()}),
            "tech_prem" : hx.Float(mode="output",view={"label":"Technical Premium", "format":thousands_format()}),
            "quoted_premium" : hx.Float(mode="output",view={"label":"Quote Premium", "format":thousands_format()})
        }),

        # Waterfall - TP UWADJ ~~~
        "final_tp_uwadj_waterfall": hx.Structure(view = {"label":"Waterfall"}, children = {
            "loss_cost" : hx.Float(mode="output",view={"label":"Loss Cost", "format":thousands_format()}),
            "var_expense" : hx.Float(mode="output",view={"label":"Variable Expenses", "format":thousands_format()}),
            "tot_expense" : hx.Float(mode="output",view={"label":"Variable Expenses", "format":thousands_format()}),
            "fixed_expense" : hx.Float(mode="output",view={"label":"Fixed Expenses", "format":thousands_format()}),
            "inv_income" : hx.Float(mode="output",view={"label":"Investment Income", "format":thousands_format()}),
            "ri" : hx.Float(mode="output",view={"label":"Reinsurance", "format":thousands_format()}),
            "capital" : hx.Float(mode="output",view={"label":"Capital Charge", "format":thousands_format()}),
            "brokerage" : hx.Float(mode="output",view={"label":"Brokerage", "format":thousands_format()}),
            "tech_prem" : hx.Float(mode="output",view={"label":"Technical Premium", "format":thousands_format()}),
            "quoted_premium" : hx.Float(mode="output",view={"label":"Quote Premium", "format":thousands_format()})
        })
    })

    cds.override_node_properties("cds/layers/limit", {"mode": "output"})
    cds.override_node_properties("cds/layers/excess", {"mode": "output"})
    cds.override_node_properties("cds/layers/quoted_premium", {"mode": "output"})

    cds.override_node_properties("cds/layers/rate_change/rate_change/uw_selected", {"mode": "input", "default": 0, "view": {"format": percent_format(2)}})
    cds.override_node_properties("cds/final_premium_summary_table/acq_cost", {
        "view": {
            "options": {
                "invalid": {"style_cell": "hx-neutral"},
                "read_only": {"label": "Brokerage (excl. PC's)", "read_only": True}, 
                "kpi_summary_option": {
                    "label": "Brokerage (excl. PC's)",
                },
                "short_label_option": {
                    "label": "Brokerage",
                }
            }
        }
    })
    cds.override_node_properties("cds/final_premium_summary_table/signed_line", {
        "view": {
            "options": {
                "invalid": {"style_cell": "hx-neutral"},
                "read_only": {"label": "Written Line", "read_only": True}, 
                "kpi_summary_option": {
                    "label": "Written Line",
                }
            }
        }
    })
    cds.override_node_properties("cds/final_premium_summary_table/tech_prem_adj", {
        "view": {
            "options": {
                "kpi_summary_option": {
                    "label": "Gross Technical Premium",
                }
            }
        }
    })
    cds.override_node_properties("cds/final_premium_summary_table/bench_prem_adj", {
        "view": {
            "options": {
                "kpi_summary_option": {
                    "label": "Gross Benchmark Premium",
                }
            }
        }
    })

    cds.override_node_properties("cds/layers/quoted_prem_kpi_summary", {
        "view": {
            "options": {
                "read_only": {"read_only": True}, 
            }
        }
    })
    cds.override_node_properties("cds/layers/bpi_case_priced", {
        "view": {
            "options": {
                "read_only": {"read_only": True}, 
            }
        }
    })
