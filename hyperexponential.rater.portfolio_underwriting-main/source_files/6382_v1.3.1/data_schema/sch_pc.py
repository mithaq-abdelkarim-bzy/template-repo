import hx_data_schema as hx
from data_schema.sch_utilities import percent_format, create_node, thousands_format
from algorithms import rate_constants as constants


def generate_matrix_common_nodes(label, options=[], has_selection=True):
    nodes = {
        "guideline_min":  create_node("Guideline Min",  "output",  format=percent_format(2), group="Uncertainty Load"),
        "guideline_max":  create_node("Guideline Max",  "output",  format=percent_format(2), group="Uncertainty Load"),
        "suggested":      create_node("Suggested",      "output",  format=percent_format(2), group="Uncertainty Load"),
        "final_selected": create_node("Final Selected", "override",format=percent_format(2), group="Uncertainty Load"),
        "comments":       create_node("Comments", type="str")
    }

    if has_selection:
        nodes["selection"] = create_node("Selection", type="str", options=options)

    return hx.Structure(view={"label": label}, children=nodes)


def generate_applied_charge_summary_nodes(is_model_weighting=False):
    common_nodes = {
        "own_performance":      create_node("Own Performance",      "output", format=percent_format(0)),
        "lloyds_performance":   create_node("Lloyds Performance",   "output", format=percent_format(0)),
        "beazley_performance":  create_node("Beazley Performance",  "output", format=percent_format(0)),
        "business_plan":        create_node("Business Plan",        "output", format=percent_format(0)),
        "case_pricing":         create_node("Case Pricing",         "output", format=percent_format(0)),
        "pricing_2623_623":     create_node("2623/623 Pricing",     "output", format=percent_format(0)),
    }
    if not is_model_weighting:
        common_nodes["selected_lob"] = create_node("Selected Lob",      "output",             type="str")
        common_nodes["load"]         = create_node("Uncertainty Load",  "override",  format=percent_format(2))

    return common_nodes


def generate_calculations_common_nodes(is_summary=False):
    as_i1    = ['calculate_profit_commission_task'] + ["sync_lob_lists_task"]
    mode     = "output" if is_summary else "input"

    children = {
        "gwp_5623":                 create_node("GWP 5623",              "output", format=thousands_format(0), async_input=as_i1),
        "deductions":               create_node("Total Deductions",      "output", format=percent_format(1),   async_input=as_i1),
        "nwp_5623":                 create_node("NWP 5623",              "output", format=thousands_format(0), async_input=as_i1),
        "best_estimate_pre_pc_adj": create_node(                    mode="output",                             async_input=as_i1),
        "attr_gg_ulr":              create_node("Attritional GG ULR %",  "output", format=percent_format(1),   async_input=as_i1),
        "large_gg_ulr":             create_node("Large GG ULR %",        "output", format=percent_format(1),   async_input=as_i1),
        "cat_gg_ulr":               create_node("CAT GG ULR %",          "output", format=percent_format(1),   async_input=as_i1),
        "total_gg_ulr":             create_node("Total GG ULR %",        "output", format=percent_format(1),   async_input=as_i1),
        "attr_cov":                 create_node("Attritional CoV",       "output", format=percent_format(1),   async_input=as_i1),
        "large_cov":                create_node("Large CoV",             "output", format=percent_format(1),   async_input=as_i1),
        "cat_cov":                  create_node("CAT CoV",               "output", format=percent_format(1),   async_input=as_i1),
        "attr_el":                  create_node("Attritional EL",        "output",                             async_input=as_i1),
        "large_el":                 create_node("Large EL",              "output",                             async_input=as_i1),
        "cat_non_weather_el":       create_node("CAT (Non-Weather) EL",  "output",                             async_input=as_i1),
        "cat_weather_el":           create_node("CAT (Weather) EL",      "output",                             async_input=as_i1),
        "attr_sd":                  create_node("Attritional SD",        "output",                             async_input=as_i1),
        "large_sd":                 create_node("Large SD",              "output",                             async_input=as_i1),
        "cat_non_weather_sd":       create_node("CAT (Non-Weather) SD",  "output",                             async_input=as_i1),
        "cat_weather_sd":           create_node("CAT (Weather) SD",      "output",                             async_input=as_i1)
    }

    if not is_summary:
        children["is_row_visible"]      = hx.Bool( mode='output', async_input=as_i1)
        children["bm_class_override"]   = hx.Str(  mode="input"
                                                 , view={"label": "Benchmark Class Override"}
                                                 , optionality="optional"
                                                 , default=None
                                                 , options_column="Business Plan Class"
                                                 , options_table="table_bbt_parameters"
                                                 , async_input=as_i1)
        children["selected_lob"]        = create_node("Line of Business",       "output",           type="str",                                         async_input=as_i1)
        children["bm_class_auto"]       = create_node("Benchmark Class Auto",   "output",           type="str",                                         async_input=as_i1)
        children["bm_class_applied"]    = create_node("Benchmark Class Applied","output", "output", type="str",                                         async_input=as_i1)
        children["cov_basis_attr"]      = create_node("CoV Basis: Attritional",  mode,              type="str", options=["BBT", "Experience"],          async_input=as_i1)
        children["cov_basis_large"]     = create_node("CoV Basis: Large",        mode,              type="str", options=["BBT", "Experience"],          async_input=as_i1)
        children["cov_basis_cat"]       = create_node("CoV Basis: CAT",          mode,              type="str", options=["BBT", "Experience", "RMS"],   async_input=as_i1)
        children["cov_basis_attr_bbt"]  = create_node("CoV Basis: Attritional",  mode,              type="str", options=["BBT"],                        async_input=as_i1)
        children["cov_basis_large_bbt"] = create_node("CoV Basis: Large",        mode,              type="str", options=["BBT"],                        async_input=as_i1)
        children["cov_basis_cat_bbt"]   = create_node("CoV Basis: CAT",          mode,              type="str", options=["BBT"],                        async_input=as_i1)

    return children


def generate_profit_commission_common_nodes(is_summary=False):
    children = {
        "selected_lob":             create_node("Line of Business",                  "output", type="str",               async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "gwp_5623":                 create_node("5623 GWP", "output",                                                    async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "deductions":               create_node("Total Deductions",                  "output",                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "nwp_5623":                 create_node("5623 NWP",                          "output",                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "total_losses":             create_node("Simulated Total Expected Losses $", "output",                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "uw_expense":               create_node("UW Expense $",                      'output',                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "dcf":                      create_node("Deficit Carry-forward",             "output",                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "expected_pl":              create_node("Expected P/L",                      'output',                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "pc_on_binders":            create_node("PC Payable on Underlying Binders",  'output',                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "pc_on_contract":           create_node("PC Payable on Contract",            'output',                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "nwp_after_pc":             create_node("5623 NWP After PC",                 "output",                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "total_gn_ulr_pre":         create_node("Total GN ULR (Pre PC)",             "output", format=percent_format(1), async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "total_gn_ulr_post":        create_node("Total GN ULR (Post PC)",            "output", format=percent_format(1), async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "best_estimate_pre_pc_adj": create_node(                                mode="output",                           async_output=['calculate_profit_commission_task',"fetch_bbt_task"]),
        "pc_impact":                create_node("PC impact on GN ULR",               "output", format=percent_format(2), async_output=['calculate_profit_commission_task',"fetch_bbt_task"])
    }

    if not is_summary:
        children["is_row_visible"] = hx.Bool(mode='output', async_output=['calculate_profit_commission_task',"fetch_bbt_task"])

    return children


def sch_pc(cds):
    as_i1 = ['calculate_profit_commission_task']
    as_o  = []
    cds.extend_node_rater_defined("cds",
        {"pc": hx.Structure( children={
            "pc_control": hx.Structure(children={
                "is_pc_interlocking":        hx.Bool(mode="input", default=True,  view={"label": "Is PC Interlocking?"},                                       async_input=as_i1),
                "allow_for_correlation":     hx.Bool(mode="input", default=True,  view={"label": "Allow for Correlation"},                                     async_input=as_i1),
                "show_details":              hx.Bool(mode="input", default=False, view={"label": "Show Details?"},                                             async_input=as_i1),
                "ul_binders_pc":             hx.Bool(mode="input", default=False, view={"label": "Is there a PC on Underlying Binders?"},                      async_input=as_i1),
                "ul_pc_as_expense":          hx.Bool(mode="input", default=False, view={"label": "Underlying PC treated as Expense on Contract PC"},           async_input=as_i1),
                "ul_pc_as_expense_pct": create_node("Proportion of Underlying Binders in Contract", format=percent_format(1),                                  async_input=as_i1),
                "no_of_simulations": create_node("Number of Simulations",        type="int",                                             default=1000000,      async_input=as_i1),
                "dcf_opt":           create_node("Deficit Carry forward Option", type="str", options=["None", "Experience", "$ Amount"], default="Experience", async_input=as_i1),
                "dcf_opt_bbt":       create_node("Deficit Carry forward Option", type="str", options=["None", "$ Amount"],                                     async_input=as_i1),
                "dcf_amount":        create_node("$ Amount",                     type="int",                                                                   async_input=as_i1),
                "dcf_amount_basis":  create_node("Basis",                        type="str", options=["Total Contract", "BST Share"],                          async_input=as_i1),
                "dcf_exper_num_yrs": create_node("Years",                        type="int",                                             default=3,            async_input=as_i1),
                "dcf_exper_exc_yrs": create_node("Excl X most recent years",     type="int", options=[0, 1, 2, 3, 4, 5],                 default=1,            async_input=as_i1),
                "dcf_exper_basis":   create_node("Basis",                        type="str", options=["Incurred", "Ultimate"],                                 async_input=as_i1),}),
            
            "pc_structure": hx.Structure(children={
                "table":        hx.List(mode="input", default_element_count=constants.DEFAULT_NUM_LOB,
                                        async_output=[{"task": "sync_lob_lists_task", "reset": False}], children={
                    "selected_lob":         create_node("Line of Business", mode="output", type="str",                              async_input=['calculate_profit_commission_task', 'generate_word_document_task', 'generate_excel_document_task']),
                    "total_fees":           create_node(                    mode="output",                                          async_input=['calculate_profit_commission_task', 'generate_word_document_task', 'generate_excel_document_task']),
                    "market_deductions":    create_node(                    mode="output",                                          async_input=['calculate_profit_commission_task', 'generate_word_document_task', 'generate_excel_document_task']),
                    "pc_type":              create_node("PC Type",          type="str", options=["Standard", "Sliding Scale"],      async_input=["sync_lob_lists_task", 'calculate_profit_commission_task', 'generate_word_document_task', 'generate_excel_document_task']),
                    "uw_expense":           create_node("UW Expense %",             format=percent_format(1),                       async_input=["sync_lob_lists_task", 'calculate_profit_commission_task', 'generate_word_document_task', 'generate_excel_document_task']),
                    "expense_basis":        create_node("UW Expense Basis", type="str", options=["Net Premium", "Gross Premium"],   async_input=["sync_lob_lists_task", 'calculate_profit_commission_task', 'generate_word_document_task', 'generate_excel_document_task']),
                    "std_pc_percent":       create_node("PC %",             format=percent_format(1),                               async_input=["sync_lob_lists_task", 'calculate_profit_commission_task', 'generate_word_document_task', 'generate_excel_document_task']),
                    "is_row_visible":       hx.Bool(mode="output",                                                                  async_input=['calculate_profit_commission_task', 'generate_word_document_task', 'generate_excel_document_task'])}),
                
                "table_sliding_scale": hx.List( mode="input", 
                                                default_element_count=constants.DEFAULT_NUM_LOB,
                                                async_output=[{"task": "sync_lob_lists_task", "reset": False}], 
                                                children={
                    "selected_lob":      create_node("Line of Business", mode="output", type="str",async_input=as_i1),
                    'scale':  hx.List(mode="input", default_element_count=constants.DEFAULT_NUM_LOB, children={                       
                        "gn_ulr_less_than": create_node("GN ULR Less than", format=percent_format(0), async_input=as_i1 + ["sync_lob_lists_task"]),
                        "pc":               create_node("PC %",             format=percent_format(0), async_input=as_i1 + ["sync_lob_lists_task"])})})}),

            "pc_calculations": hx.Structure(children={
                "details":           hx.List(      mode="input", default_element_count=constants.DEFAULT_NUM_LOB,         async_output=[{"task": "sync_lob_lists_task", "reset": False}],                   
                                                                                                                          children=generate_calculations_common_nodes(is_summary=False)),
                "summary":           hx.Structure(                        view={"label": "Total"},                        children=generate_calculations_common_nodes(is_summary=True ))}),
                "profit_commission": hx.Structure(children={
                    "details": hx.List(           mode="output",   async_output=['calculate_profit_commission_task',"fetch_bbt_task"],     children=generate_profit_commission_common_nodes(is_summary=False)),
                    "summary": hx.Structure(                              view={"label": "Total"},                        children=generate_profit_commission_common_nodes(is_summary=True ))}),

            "cm_calc": hx.List(mode="output", children={
                "selected_lob":      create_node("Line of Business", mode="output", type="str"),
                "cm_col": hx.List(mode="output", children={
                    "coeff": hx.Float(mode="output",view={"label": "co-efficient","format":percent_format(1)})})}),

            "cm_ovd": hx.List(mode="input", default_element_count=constants.DEFAULT_NUM_LOB, async_output=[{"task": "sync_lob_lists_task", "reset": False}], children={
                "selected_lob":      create_node("Line of Business", mode="output", type="str"),
                "cm_col": hx.List(mode="input", default_element_count=constants.DEFAULT_NUM_LOB, async_output=[{"task": "sync_lob_lists_task", "reset": False}], children={
                    "coeff": hx.Float(mode="input", optionality="optional", default=None,view={"label": "co-efficient","format":percent_format(1)})})}),

            "cm_sel": hx.List(mode="output", async_input=as_i1, async_output=as_o, children={
                "selected_lob":      create_node("Line of Business", async_input=as_i1, async_output=as_o, mode="output", type="str"),
                "cm_col": hx.List(mode="output", async_input=as_i1, async_output=as_o,   children={
                    "coeff": hx.Float(mode="output", async_input=as_i1, async_output=as_o, view={"label": "co-efficient","format":percent_format(1)})})}),
            })})
