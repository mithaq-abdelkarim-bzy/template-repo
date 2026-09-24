# v0.5.0
import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format

from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
from data_schema.sch_rate_change import rarc_task_name


coverages_dict= {"all_risks"                : {"label": "All Risks"},
                    "adverse_weather"          : {"label": "Adverse Weather"},
                    "earthquake"               : {"label": "Earthquake"},
                    "windstorm"                : {"label": "Windstorm"},
                    "wildfire"                 : {"label": "Wildfire"},
                    "terrorism"                : {"label": "Terrorism"},
                    "cyber"                    : {"label": "Cyber"},
                    "national_mourning"        : {"label": "National Mourning"},
                    "riots_and_civil_commotion": {"label": "Riots and Civil Commotion"},
                    "strike"                   : {"label": "Strike"},
                    "war"                      : {"label": "War"},
                    "catastrophic_non_app"     : {"label": "Catastrophic Non-App"},
                    "ec_total"                 : {"label": "Event Cancellation Total"},
                    "na_total"                 : {"label": "Non-Appearance Total"}}             


### --- DEFINE GENERIC RATING NODES  --- ###
rating_summary_new_nodes_dict = {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        'bpi_case_priced':                  hx.Float(mode='input', default=None, optionality='optional', view={'label': 'BPI (Case Priced)',                         'format': percent_format(1)}),
        "quoted_premium_100_case_priced":   hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross Quoted Premium (100%) - Case Priced", "format": thousands_format(0)}),
        
        # 'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}), # EDIT v0.3.0 removed since it has moved to CDS 1.3
        'premium_label': hx.Str(mode='output'),
        'rat_sum_label': hx.Str(mode='output'),
        # EDIT v0.3.0 - Add 100 % premium for rating summary 
        'technical_premium_pre_uw_adj_100': hx.Float(mode="output",      view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": thousands_format(0)}),
        'technical_premium_annual_100':     hx.Float(mode="output",      view={"label": "Annualised Gross Technical Premium 100%",          "format": thousands_format(0)}),
        'technical_premium_annual':         hx.Float(mode="output",      view={"label": "Annualised Gross Technical Premium AFB%",          "format": thousands_format(0)}),
        'expected_loss_cost_pre_uw_adj_100':hx.Float(mode="output",      view={"label": "Expected Loss Cost (Pre-UW Adjustment) 100%",      "format": thousands_format(0)}),

        "plan_premium_100": hx.Float(mode="output", view={"label": "Gross Plan Premium 100%",   "format": thousands_format(0)}),
        # "quoted_premium_100": hx.Float(mode="output", view={"label": "Gross Quoted Premium (100%)"}),
        # "technical_premium_100": hx.Float(mode="output", view={"label": "Gross Technical Premium (100%)"}),
        # "benchmark_premium_100": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (100%)"}),
        "plan_rol":         hx.Float(mode="output", view={"label": "Gross Plan Rate-on-Line",   'format': percent_format(3)}), 
        "quoted_rol":       hx.Float(mode="output", view={"label": "Offered Rate-on-Line",      'format': percent_format(3)}),
        "quoted_roe":       hx.Float(mode="output", view={"label": "Offered Rate-on-Exposure",  'format': percent_format(3)}),    

        "benchmark_rol":    hx.Float(mode="output", view={"label": "Benchmark Rate-on-Line",    'format': percent_format(3)}),
        "technical_rol":    hx.Float(mode="output", view={"label": "Technical Rate-on-Line",    'format': percent_format(3)}),

        "benchmark_rol_pre_uw_adj":    hx.Float(mode="output", view={"label": "Benchmark (Pre-UW Adjustment) Rate-on-Line",    'format': percent_format(3)}),
        "technical_rol_pre_uw_adj":    hx.Float(mode="output", view={"label": "Technical (Pre-UW Adjustment) Rate-on-Line",    'format': percent_format(3)}),

        "plan_premium_pre_uw_adj_100":      hx.Float(mode="output", view={"label": "Gross Plan Premium (Pre-UW Adjustment) 100%", "format": thousands_format(0)}),
        # "quoted_premium_pre_uw_adj_100":    hx.Float(mode="output", view={"label": "Gross Quoted Premium (Pre-UW Adjustment) 100%"}),
        # "technical_premium_pre_uw_adj_100": hx.Float(mode="output", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%"}), 
        "benchmark_premium_pre_uw_adj_100": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment) 100%", "format": thousands_format(0)}),
        "plan_rol_pre_uw_adj":              hx.Float(mode="output", view={"label": "Gross Plan (Pre-UW Adjustment) Rate-on-Line",  'format': percent_format(3)}),
        "quoted_rol_pre_uw_adj":            hx.Float(mode="output", view={"label": "Offered (Pre-UW Adjustment) Rate-on-Line",  'format': percent_format(3)}),
        # "quoted_roe": hx.Float(mode="output", view={"label": "Offered Rate-on-Exposure"}),    # not needed pre-uw-adj

}

ec_blend_e_e_dict = {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        # 'loss_cost_fgu':                hx.Float(mode='output', view={'label': 'Exposure\nLoss Cost',               'format': thousands_format(0), "group": "Exposure Rating - FGU"}),
        # 'layer_adjustment':             hx.Float(mode='output', view={'label': 'Layer\nAdjustment',                 'format': percent_format(0),   "group": "Exposure Rating - Adjusting for Layer"}),
        'loss_cost_layer_adj':          hx.Float(mode='output', view={'label': 'Exposure\nLoss Cost',               'format': thousands_format(0), "group": "Exposure Rating - Adjusting for Layer"}),
        'agg_adjustment':               hx.Float(mode='output', view={'label': 'Aggregate\nAdjustment',             'format': percent_format(3),   "group": "Exposure Rating - Adjusting for Aggregate"}),
        'loss_cost_layer_agg_adj':      hx.Float(mode='output', view={'label': 'Exposure\nLoss Cost',               'format': thousands_format(0), "group": "Exposure Rating - Adjusting for Aggregate"}),
        'uw_adjustment':                hx.Float(mode='output', view={'label': 'Underwriter\nAdjustment',           'format': percent_format(3),   "group": "Exposure Rating - Adjusting for Underwriter"}),
        'loss_cost_layer_agg_uw_adj':   hx.Float(mode='output', view={'label': 'Exposure\nLoss Cost',               'format': thousands_format(0), "group": "Exposure Rating - Adjusting for Underwriter"}),

        'experience_weight':            hx.Float(mode="output", view={'label': 'Experience\nWeight',                'format': percent_format(3),   "group": "Experience Rating"}),
        'experience_loss_cost':         hx.Float(mode="output", view={'label': 'Experience\nLoss Cost',             'format': thousands_format(0), "group": "Experience Rating"}), 

        'blended_loss_cost_no_uw_adj':  hx.Float(mode='output', view={'label': 'Blended\nLoss Cost\nno Uw Adj',     'format': thousands_format(0), "group": "Blended Rating"}),
        'blended_loss_cost':            hx.Float(mode='output', view={'label': 'Blended\nLoss Cost\nwith Uw Adj',   'format': thousands_format(0), "group": "Blended Rating"}),
}


na_dict = {
        "description":          hx.Str(  mode="output", view={"label": "Description"}),                                                 
        "fgu_pct":              hx.Float(mode="output", view={"label": "Proportion of\nFGU Loss to\nthe Layer",  "format": percent_format(2)}),
        "el_fgu_mod":           hx.Float(mode="output", view={"label": "Expected Loss\nModified",                "format": thousands_format(0)}),
        "el_fgu_mod_adj":       hx.Float(mode="output", view={"label": "Expected Loss\nModified &\nUW Adjusted", "format": thousands_format(0)})
}

ec_dict = {
        "excess_use":       hx.Bool( mode="input", default=False, optionality="required", view={"label": "Use Excess (not deductible)"}, async_input=['rarc_task'],)
}





### --- DEFINE RATING NODES FOR LAYER --- ###
def sch_rating_summary(cds): 
    cds.extend_node_rater_defined('cds/layers', {**rating_summary_new_nodes_dict})
    cds.override_node_properties("cds/layers/quoted_premium",    {"mode":"output", "async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (AFB)",  "format": thousands_format(0)}}),
    cds.override_node_properties("cds/layers/quoted_premium_100",{"mode":"output", "async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (100%)", "format": thousands_format(0)}}),
    cds.override_node_properties("cds/layers/currency",          {"mode":"output", "async_input":[rarc_task_name],"view":{"label": "Currency"},})
    cds.override_node_properties("cds/layers/pflr_pre_uw_adj",   {                                                                                           "view":{"label": "Priced-for Loss Ratio (Gross Net Pre-UW Adj.)", "format": percent_format(1)}})
    cds.override_node_properties("cds/layers/pflr",              {                                                                                           "view":{"label": "Priced-for Loss Ratio (Gross Net)",             "format": percent_format(1)}})

    cds.extend_node_items(        "cds/layers/coverages",           {**coverages_dict})                 ### --- Adding coverages to the list of layers --- NOTE this code duplicates all the common fields from layer to each coverage.
    cds.extend_node_rater_defined("cds/layers/coverages",           {**rating_summary_new_nodes_dict})  ### --- Adding rated-defined STANDARD  field to ALL coverages --- ####
    cds.extend_node_rater_defined("cds/layers/coverages",           {**ec_blend_e_e_dict})              ### --- Adding rated-defined LOSS COST field to ALL coverages     ####

    cds.extend_node_rater_defined("cds/layers/coverages/na_total",  {**na_dict})                        ### --- Adding rated-defined LOSS COST field to NA  coverage      ####
    cds.extend_node_rater_defined("cds/layers/coverages/ec_total",  {**ec_dict})                        ### --- Adding xyz
    cds.extend_node_rater_defined('cds/layers',                     {**na_dict})                        ### --- Adding rated-defined LOSS COST field to Overall - note these were needed at this level for view to work ####
    cds.extend_node_rater_defined('cds/layers',                     {**ec_blend_e_e_dict})              ### --- Adding rated-defined LOSS COST field to Overall - note these were needed at this level for view to work ####





    # ### --- Adding a rated-defined field to a specifc coverage --- #### 
    for cvg in coverages_dict.keys():

        cds.override_node_properties(f"cds/layers/coverages/{cvg}/quoted_premium",      {"mode":"output", "async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (AFB)",  "format": thousands_format(0)}}),
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/quoted_premium_100",  {"mode":"input",  "optionality":"optional", "default": None, "async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (100%)", "format": thousands_format(0), "options": {"read_only": {"read_only": True}}}}),
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/currency",            {"mode":"output", "async_input":[rarc_task_name],"view":{"label": "Currency"},})
  
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/brokerage",           {"mode":"output"})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/written_line",        {"mode":"output"})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/premium",             {"mode":"output"})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/status",              {"mode":"output"})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/trifocus",            {"mode":"output"})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/bpi_case_priced",     {"mode":"output"})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/pflr_pre_uw_adj",     {"view":{"label": "Priced-for Loss Ratio (Gross Net Pre-UW Adj.)", "format": percent_format(1)}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/pflr",                 {"view":{"label": "Priced-for Loss Ratio (Gross Net)",             "format": percent_format(1)}})

        if cvg not in ['ec_total','na_total']:
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/limit",               {"mode":"output"})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/excess",              {"mode":"output"})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/deductible",          {"mode":"output"})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/aggregate_limit",     {"mode":"output"})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/aggregate_excess",    {"mode":"output"})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/aggregate_deductible",{"mode":"output"})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/section_reference",   {"mode":"output", "async_input": ["task_sql_bi_data"]
            })      
        elif cvg=="ec_total":
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/section_reference",   {
                  "view":        {"label": "Section Reference - Event Cancellation", "options": {"read_only": {"read_only": True}}}
                , "async_input": ["task_sql_bi_data", "task_simulation", "task_fetch_ihs_data", "task_start_renewal", "expiring_policy_fetch_task", "expiring_policy_fetch_coverages_task", "rarc_task", "rarc_task_coverages", "rarc_task_coverages_insured_asset", "policy_to_excel_task","sync_expiring_ids"]
                , "async_output":["task_start_renewal"]
            })
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/limit",               {"async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/excess",              {"async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/deductible",          {"async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/aggregate_limit",     {"async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/aggregate_excess",    {"async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/aggregate_deductible",{"async_input":["rarc_task"]})
        elif cvg=="na_total":
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/section_reference",   {
                  "mode":        "override"             # requested by YZ/AC 19 Aug 26
                , "view":        {"label": "Section Reference - Non-Appearance", "options": {"read_only": {"read_only": True}}}
                , "async_input": ["task_sql_bi_data"]
                # , "async_output":["task_start_renewal"] # requested by YZ/AC 19 Aug 26
            })     
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/limit",               {"mode":"output", "async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/excess",              {"mode":"output", "async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/deductible",          {"mode":"output", "async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/aggregate_limit",     {"mode":"output", "async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/aggregate_excess",    {"mode":"output", "async_input":["rarc_task"]})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/aggregate_deductible",{"mode":"output", "async_input":["rarc_task"]})



