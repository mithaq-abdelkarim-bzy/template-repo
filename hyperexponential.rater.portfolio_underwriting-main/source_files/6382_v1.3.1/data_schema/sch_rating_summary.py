import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, create_node
import algorithms.rate_constants as constants


def get_common_row_metadata(async_input=[]):
    return {
        "selected_lob": create_node("Selected Line of Business", "output", type="str"),
        "is_row_visible": hx.Bool(mode="output")
    }


def generate_projected_gn_ulr_nodes(is_summary=False):
    mode = "output" if is_summary else "input"
    as_i = [ "generate_word_document_task", "generate_excel_document_task"] + ["sync_lob_lists_task"]
    as_o = []
    children = {
        "gn_premium":           create_node("GN Premium",                       "output", async_input=as_i),
        "portfolio_percent":    create_node("% of Portfolio",                   "output", async_input=as_i,                    format=percent_format(1)),
        "total_deductions":     create_node("Total Deductions",                 "output", async_input=as_i,                    format=percent_format(1)),
        "own_exp_gn_ulr":       create_node("Own Experience GN ULR %",          "output", async_input=as_i,                    format=percent_format(1)),
        "lloyds_gn_ulr":        create_node("Lloyd's Projected GN ULR %",       "output", async_input=as_i,                    format=percent_format(1)),
        "beazley_gn_ulr":       create_node("Beazley Projected GN ULR %",       "output", async_input=as_i,                    format=percent_format(1)),
        "bp_gn_ulr":            create_node("BP Projected GN ULR %",            "output", async_input=as_i,                    format=percent_format(1)),
        "case_pricing":         create_node("Case Pricing GN ULR %",             mode,    async_input=as_i,                    format=percent_format(1)),
        
        "own_exp_gn_ulr_ly":    create_node("Own Experience GN ULR % (LY)",     "input",  async_input=as_i, async_output=as_o, format=percent_format(1)),
        "lloyds_gn_ulr_ly":     create_node("Lloyd's Projected GN ULR % (LY)",  "input",  async_input=as_i, async_output=as_o, format=percent_format(1)),
        "beazley_gn_ulr_ly":    create_node("Beazley Projected GN ULR % (LY)",  "input",  async_input=as_i, async_output=as_o, format=percent_format(1)),
        "bp_gn_ulr_ly":         create_node("BP Projected GN ULR % (LY)",       "input",  async_input=as_i, async_output=as_o, format=percent_format(1)),
        "case_pricing_ly":      create_node("Case Pricing GN ULR % (LY)",       "input",  async_input=as_i, async_output=as_o, format=percent_format(1))
    }

    if not is_summary:
        additional_fields={
            "tracker_class":    create_node("Tracker Class",                    "output", async_input=as_i, type="str"),
            "policy_ref_by_lob":create_node("Policy Section Reference",         "input",  async_input=as_i, type="str"),
            "selected_lob":     create_node("Selected Line of Business",        "output", async_input=as_i, type="str"),
            "is_row_visible":   hx.Bool(                                   mode="output", async_input=as_i)
        }
        children.update(additional_fields)

    return children


def generate_model_weights_nodes(is_summary=False):
    mode = "output" if is_summary else "input"
    as_i = ["generate_word_document_task", "generate_excel_document_task"]+ ["sync_lob_lists_task"]
    as_o = []
    children = {
        "own_experience":   create_node("Own Experience Weighting",         mode, default=0.5, format=percent_format(1), async_input=as_i),
        "lloyds_proj":      create_node("Lloyd's Projection Weighting",     mode, default=0.5, format=percent_format(1), async_input=as_i),
        "beazley_proj":     create_node("Beazley Projection Weighting",     mode, default=0,   format=percent_format(1), async_input=as_i),
        "bp_proj":          create_node("BP Projection Weighting",          mode, default=0,   format=percent_format(1), async_input=as_i),
        "case_pricing":     create_node("Case Pricing Weighting",           mode, default=0,   format=percent_format(1), async_input=as_i),
        "weighting_check":  create_node("Weighting Check",                  "output", type='str',                        async_input=as_i),

        "own_experience_ly":create_node("Own Experience Weighting (LY)",    "input", format=percent_format(1), async_input=as_i, async_output=as_o),
        "lloyds_proj_ly":   create_node("Lloyd's Projection Weighting (LY)","input", format=percent_format(1), async_input=as_i, async_output=as_o),
        "beazley_proj_ly":  create_node("Beazley Projection Weighting (LY)","input", format=percent_format(1), async_input=as_i, async_output=as_o),
        "bp_proj_ly":       create_node("BP Projection Weighting (LY)",     "input", format=percent_format(1), async_input=as_i, async_output=as_o),
        "case_pricing_ly":  create_node("Case Pricing Weighting (LY)",      "input", format=percent_format(1), async_input=as_i, async_output=as_o),

        "model_estimate":   create_node("Model Estimate GN ULR %",          "output",format=percent_format(1), async_input=as_i                   ),
        "model_estimate_ly":create_node("Model Estimate GN ULR % (LY)",     "input", format=percent_format(1), async_input=as_i, async_output=as_o)
    }

    if not is_summary:
        additional_fields = {
            "selected_lob": create_node("Selected Line of Business", "output", async_input=as_i, type="str"),
            "is_row_visible": hx.Bool(mode="output", async_input=as_i)
        }
        children.update(additional_fields)

    return children


def generate_cat_loading_nodes(is_summary=False):
    mode = "override" if not is_summary else "output"
    as_i = ["generate_word_document_task", "generate_excel_document_task"]+ ["sync_lob_lists_task"]
    children = {
        "attr_and_lrg_exp":     create_node("Attritional & Large %: Own Experience", "output", async_input=as_i, format=percent_format(1)),
        "cat_exp":              create_node("CAT %: Own Experience",                 "output", async_input=as_i, format=percent_format(1)),
        "attr_and_lrg_bp":      create_node("Attritional & Large %: Business Plan",  "output", async_input=as_i, format=percent_format(1)),
        "cat_bp":               create_node("CAT %: Business Plan",                  "output", async_input=as_i, format=percent_format(1)),
        "attr_and_lrg":         create_node("Attritional & Large %",                 "output", async_input=as_i, format=percent_format(1)),
        "cat":                  create_node("CAT %",                                  mode,    async_input=as_i, format=percent_format(1)),
        "climate_change_load":  create_node("Climate Change Loading %",              "output", async_input=as_i, format=percent_format(1)),
        "nmp_load_general":     create_node("NMP Loading (General) %",               "output", async_input=as_i, format=percent_format(1)),
        "nmp_load_weather":     create_node("NMP Loading (All Other) %",             "output", async_input=as_i, format=percent_format(1))
    }

    if not is_summary:
        children.update({
            "selected_lob":     create_node("Selected Line of Business",             "output", async_input=as_i, type="str"),
            "is_row_visible":   hx.Bool(                                        mode="output", async_input=as_i)
        })

    return children


def generate_pricing_outputs_nodes(is_summary=False):
    as_o1 = [{"task":"fetch_bbt_task", "reset": False}]
    as_o2 = ["fetch_bbt_task"]
    as_i1 = ["generate_word_document_task"]
    children = {
        "bbt_gn_ulr":          create_node("BBT GN ULR % (before PC)",      "override", format=percent_format(1),                           async_output=as_o1),
        "bbt_gn_cat_ulr":      create_node("BBT GN CAT ULR % (before PC)",  "override", format=percent_format(1),                           async_output=as_o1),
        "bbt_pc":              create_node("BBT PC",                        "override", format=percent_format(1),  is_read_only=True),
        "attr_and_large":      create_node("Attritional & Large %",         "override", format=percent_format(1)),
        "cat":                 create_node("CAT %",                         "override", format=percent_format(1)),
        "deductions_623_2623": create_node("623 / 2623 Total Deductions %", "override", format=percent_format(1),                           async_output=as_o1,                 async_input=as_i1),
        "cat_gn_ulr_final":    create_node("CAT GN Final ULR %",            "output",   format=percent_format(1),                           async_output=as_o1),
        "deductions_5623":     create_node("5623 Total Deductions %",                   format=percent_format(1), default=0,                async_output=as_o2),
        "bbt_class":           create_node("BBT Class",                     "override", type='str',                                         async_output=as_o1,                 async_input=as_i1,  
                                                                            options="table_business_plan/business_plan_class", 
                                                                            allow_custom_value=True),
        "tracker_class":       create_node("Assigned Tracker Class",        type='str', options="table_trifocus_list/Trifocus List",                                            async_input=as_i1),
        "section_ref_5623":    create_node("5623 Policy Section Reference", type='str',                                                                                         async_input=as_i1),
        "gn_ulr_5623":         create_node("5623 GN ULR %",                 "output",   format=percent_format(1)),
        "gn_ulr_5623_ly":      create_node("5623 GN ULR % (LY)",            "input",    format=percent_format(1),                           async_output=[]),
        "afb_api":             create_node("5623 EPI (Net of Aqn, Gross of PC)",                                  default=0),
        "line_size":           create_node("Written Line Size",                         format=percent_format(1), default=0),
    }

    return children


def generate_pricing_loadings_nodes(is_summary=False):
    mode = "output" if is_summary else "input"
    as_i = ["generate_word_document_task", "generate_excel_document_task"]+ ["sync_lob_lists_task"]
    children = {
        "anti_selection_charge": create_node("Anti-Selection Charge %", "output", async_input=as_i, format=percent_format(2)),
        "uncertainty_charge":    create_node("Uncertainty Charge %",    "output", async_input=as_i, format=percent_format(2)),
        "additional_charge":     create_node("Additional Charge %",     mode,     async_input=as_i, format=percent_format(1))
    }

    if not is_summary:
        children.update({
            "selected_lob":     create_node("Selected Line of Business", "output", async_input=as_i, type="str"),
            "is_row_visible":   hx.Bool(                            mode="output", async_input=as_i)
        })
    else:
        children.update(
            {"additional_charge_bbt": create_node("Additional Charge %", default=0, async_input=as_i, format=percent_format(1))}
        )

    return children


def generate_pricing_adequacy_nodes(is_summary=False, is_actuarial_basis=False):
    as_i = ["generate_word_document_task", "generate_excel_document_task"] if is_summary else []
    
    children = {
        "best_estimate_pre_pc_adj": create_node("Best Estimate GN ULR % (Pre PC Adj)",  "output", async_input=as_i, format=percent_format(1)),
        "pc_impact":                create_node("PC % Impact on GN ULR",                "output", async_input=as_i, format=percent_format(1)),
        "best_estimate":            create_node("Best Estimate GN ULR %",               "output", async_input=as_i, format=percent_format(1)),
        "bpi":                      create_node("BPI",                                  "output", async_input=as_i, format=percent_format(1)),
        "tpi":                      create_node("TPI",                                  "output", async_input=as_i, format=percent_format(1)),
        "roc":                      create_node("RoC",                                  "output", async_input=as_i, format=percent_format(1))
    }

    if not is_summary:
        if not is_actuarial_basis:
            children.update(get_common_row_metadata())
        else:
            children.update({
                "selected_lob":     create_node("Selected Line of Business", "output", async_input=as_i, type="str"),
                "is_row_visible":   hx.Bool(                            mode="output", async_input=as_i)
            })

    return children


def generate_final_pricing_basis_nodes(is_summary=False):
    mode = "output" if is_summary else "input"
    as_i1 = ["generate_word_document_task", "generate_excel_document_task"]+ ["sync_lob_lists_task"]
    as_o1 = ["generate_word_document_task", "generate_excel_document_task"]
    as_i2 = ["sync_lob_lists_task"]
    as_o2 = []
    children = {
        "uw_adj":               create_node("UW Adjustment (-10% to +10%)",                 mode=mode,format=percent_format(1), async_input=as_i1,  default=0),
        "best_estimate_gn":     create_node("Best Estimate GN ULR % (Post UW Adj.)",        "output", format=percent_format(1), async_input=as_i1),
        "best_estimate_gg":     create_node("Best Estimate GG ULR % (Post UW Adj.)",        "output", format=percent_format(1), async_input=as_i1),
        "bpi":                  create_node("BPI",                                          "output", format=percent_format(1), async_input=as_i1),
        "tpi":                  create_node("TPI",                                          "output", format=percent_format(1), async_input=as_i1),
        "roc":                  create_node("RoC",                                          "output", format=percent_format(1), async_input=as_i1),
        "best_estimate_gn_ly":  create_node("Best Estimate GN ULR % (Post UW Adj.) (LY)",   "input",  format=percent_format(1), async_input=as_i1,  async_output=as_o2),
        "best_estimate_gg_ly":  create_node("Best Estimate GG ULR % (Post UW Adj.) (LY)",   "input",  format=percent_format(1), async_input=as_i1,  async_output=as_o2),
        "bpi_ly":               create_node("BPI (LY)",                                     "input",  format=percent_format(1), async_input=as_i2,  async_output=as_o1),
        "tpi_ly":               create_node("TPI (LY)",                                     "input",  format=percent_format(1), async_input=as_i2,  async_output=as_o1),
        "roc_ly":               create_node("RoC (LY)",                                     "input",  format=percent_format(1), async_input=as_i2,  async_output=as_o1),
    }

    if not is_summary:
        additional_fields = {
            "selected_lob": create_node("Selected Line of Business", "output", async_input=["generate_word_document_task", "generate_excel_document_task"], type="str"),
            "is_row_visible": hx.Bool(mode="output", async_input=["generate_word_document_task", "generate_excel_document_task"])
        }
        children.update(additional_fields)
    else:
        children.update({"uw_adj_bbt": create_node("UW Adjustment (-10% to +10%)", default=0, format=percent_format(1), async_output=["fetch_bbt_task"])})

    return children


def generate_premium_build_up_nodes(is_summary=False):
    children = {
        "el_pre_adj":       create_node("EL (Pre Anti-Selection & Uncertainty)",        "output"),
        "el_actuarial":     create_node("EL (Actuarial Basis)",                         "output"),
        "el_final":         create_node("EL (Final Pricing Basis)",                     "output"),
        "net_expense":      create_node("Net Expense / GN Premium",                     "output", format=percent_format(1)),
        "inv_income":       hx.Float(mode="output", view={"label": "Investment Income / GN Premium", "format": percent_format(1), "info": "2025 & prior this is NN" }),
        "ri_premium":       create_node("RI Premium / GN Premium",                      "output", format=percent_format(1)),
        "ri_recoveries":    create_node("RI Recoveries / GN Premium",                   "output", format=percent_format(1)),
        "capital_required": hx.Float(mode="output", view={"label": "Capital Required / GN Premium", "format": percent_format(1), "info": "2025 & prior this is NN" }),
        "target_roc":       create_node("Target RoC",                                   "output", format=percent_format(1)),
        "tp_pre_adj":       create_node("TP (Pre Anti-Selection & Uncertainty)",        "output"),
        "tp_actuarial":     create_node("TP (Actuarial Basis)",                         "output"),
        "tp_final":         create_node("TP (Final Pricing Basis)",                     "output"),
        "gg_tp_final":      create_node("GG TP (Final Pricing Basis)",                  "output"),
        "gg_bm_final":      create_node("GG Benchmark Premium (Final Pricing Basis)",   "output"),
    }

    if not is_summary:
        additional_fields = {
            "selected_lob": create_node("Selected Line of Business", "output", type="str"),
            "is_row_visible": hx.Bool(mode="output"),
        }
        children.update(additional_fields)

    return children


def generate_cat_ulr_summary_nodes(is_summary=False):
    children = {
        "gn_cat_ulr_excl_loads": create_node("GN CAT ULR % (excl. Loads)", "output", format=percent_format(1)),
        "gn_cat_ulr_inc_loads":  create_node("GN CAT ULR % (incl. Loads)", "output", format=percent_format(1))
    }

    if not is_summary:
        children.update(get_common_row_metadata())

    return children


def generate_trifocus_summary_structure(label):
    children = {
        "tracker_property": create_node("Tracker Property", "output", format=percent_format(1)),
        "tracker_sr":       create_node("Tracker SR",       "output", format=percent_format(1)),
        "tracker_marine":   create_node("Tracker Marine",   "output", format=percent_format(1)),
        "tracker_pac":      create_node("Tracker PAC",      "output", format=percent_format(1)),
        "tracker_cyber":    create_node("Tracker Cyber",    "output", format=percent_format(1)),
        "summary":          create_node("Total",            "output", format=percent_format(1)),
    }

    return hx.Structure(
        view={"label": label},
        children=children
    )


def sch_rating_summary(cds):
    num_lob = constants.DEFAULT_NUM_LOB
    num_refs= constants.NUMBER_SECTION_REFERENCES
    sec_ref_opt = [i for i in range(1,21)]
    cds.extend_node_rater_defined(
        "cds",
        {
            "rating_summary": hx.Structure(children={
                "model_gn_ulr": hx.Structure(children={
                    "projected_gn_ulr": hx.Structure(children={
                        "table":            hx.List(        mode="input", 
                                                            default_element_count=num_lob,
                                                            async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                            children=generate_projected_gn_ulr_nodes()),
                        "summary":          hx.Structure(           view={"label": "Total"},            children=generate_projected_gn_ulr_nodes(is_summary=True))}),
                    
                    "model_weights": hx.Structure(children={
                        "table":            hx.List(        mode="input",
                                                            default_element_count=num_lob,
                                                            async_output=[{"task": "sync_lob_lists_task", "reset": False}], 
                                                            children=generate_model_weights_nodes()),
                        "summary":          hx.Structure(           view={"label": "Total"},            children=generate_model_weights_nodes(is_summary=True))})}),
                
                "cat_loadings": hx.Structure(children={
                    "show_details":         hx.Bool(        mode="input", default=False, view={"label": "Show Details"}),
                    "cat_allocation":       hx.List(        mode="input",
                                                            default_element_count=num_lob,
                                                            async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                            children=generate_cat_loading_nodes()),
                    "summary":              hx.Structure(           view={"label": "Total"},            children=generate_cat_loading_nodes(is_summary=True))}),
                
                "pricing_outputs":          hx.Structure(           view={"label": "Total"},            children=generate_pricing_outputs_nodes(is_summary=True)),
                
                "additional_loadings": hx.Structure(children={
                    "additional_pricing_loads": hx.List(    mode="input",
                                                            default_element_count=num_lob,
                                                            async_output=[{"task": "sync_lob_lists_task", "reset": False}], 
                                                            children=generate_pricing_loadings_nodes()),
                    "summary":              hx.Structure(           view={"label": "Total"},            children=generate_pricing_loadings_nodes(is_summary=True))}),
                
                "pricing_adequacy_metrics": hx.Structure(children={
                    "pricing_adequacy_pre_adj": hx.Structure(children={
                        "table":            hx.List(        mode="output",                              children=generate_pricing_adequacy_nodes()),
                        "summary":          hx.Structure(           view={"label": "Total"},            children=generate_pricing_adequacy_nodes(is_summary=True))}),
                
                    "pricing_adequacy_actuarial_basis": hx.Structure(children={
                        "table":            hx.List(        mode="output",                              children=generate_pricing_adequacy_nodes()),
                        "summary":          hx.Structure(           view={"label": "Total"},            children=generate_pricing_adequacy_nodes(is_summary=True))}),
                
                    "pricing_adequacy_final_pricing": hx.Structure(children={
                        "table":            hx.List(        mode="input",
                                                            default_element_count=num_lob,
                                                            async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                            children=generate_final_pricing_basis_nodes()),
                        "summary":          hx.Structure(           view={"label": "Total"},children=generate_final_pricing_basis_nodes(is_summary=True))})}),
                
                "cat_ulr_summary": hx.Structure(children={
                    "details":              hx.List(        mode="output",                              children=generate_cat_ulr_summary_nodes()),
                    "summary":              hx.Structure(           view={"label": "Total"},            children=generate_cat_ulr_summary_nodes(is_summary=True))}),
                
                "technical_premium_build_up": hx.Structure(children={
                    "tpi_year":             hx.Int(         mode="override", options_data="../tpi_year_dropdown", options_field="year_0", 
                                                            optionality="optional", async_input=["generate_word_document_task"], 
                                                            view={"label": "TPI Year", "format":{"thousandSeparated": False, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}} }),
                    "tpi_year_dropdown":    hx.List(        mode="output", children={"year_0": hx.Int(mode="output")}),
                    "technical_premium":    hx.List(        mode="output",                              children=generate_premium_build_up_nodes()),
                    "summary":              hx.Structure(           view={"label": "Total"},            children=generate_premium_build_up_nodes(is_summary=True))}),
                
                "trifocus_summary": hx.Structure(children={
                    "model_estimate":       generate_trifocus_summary_structure("Model Estimate GN ULR %"),
                    "be_before_loads":      generate_trifocus_summary_structure("Best Estimate GN ULR % (Before Loads)"),
                    "anti_selection":       generate_trifocus_summary_structure("Anti-Selection Charge %"),
                    "uncertainty":          generate_trifocus_summary_structure("Uncertainty Charge %"),
                    "additional_charge":    generate_trifocus_summary_structure("Additional Charge %"),
                    "pc_impact":            generate_trifocus_summary_structure("PC % Impact on GN ULR"),
                    "be_after_pc":          generate_trifocus_summary_structure("Best Estimate GN ULR %"),
                    "uw_adj":               generate_trifocus_summary_structure("UW Adjustment (-10% to +10%)"),
                    "be_post_uw":           generate_trifocus_summary_structure("Best Estimate GN ULR % (Post UW Adj.)"),
                    "bpi":                  generate_trifocus_summary_structure("BPI"),
                    "tpi":                  generate_trifocus_summary_structure("TPI"),
                    "roc":                  generate_trifocus_summary_structure("RoC"),
                    "show_tracker_property":hx.Bool(mode="output"),
                    "show_tracker_sr":      hx.Bool(mode="output"),
                    "show_tracker_marine":  hx.Bool(mode="output"),
                    "show_tracker_pac":     hx.Bool(mode="output"),
                    "show_tracker_cyber":   hx.Bool(mode="output")}),

                "case_pricing": hx.Structure(children={
                    "brokerage":            hx.Float(mode="input", optionality="optional", default=None, view={"label": "Brokerage (excl. PC's)", "format": {"output": "percent", "mantissa": 2}}),
                    "written_line":         hx.Float(mode="input", optionality="optional", default=None, view={"label": "Written Line", "format": {"output": "percent", "mantissa": 2}}),
                    "bpi":                  hx.Float(mode="input", optionality="optional", default=None, view={"label": "BPI", "format": {"output": "percent", "mantissa": 2}}),
                    "tpi":                  hx.Float(mode="output",                                      view={"label": "TPI", "format": {"output": "percent", "mantissa": 2}}),
                    "tpi_override":         hx.Float(mode="override",                                    view={"label": "TPI", "format": {"output": "percent", "mantissa": 2}}), # added later hence separate from tpi field above
                    "roc":                  hx.Float(mode="output",                                      view={"label": "ROC", "format": {"output": "percent", "mantissa": 2}}),
                    "roc_override":         hx.Float(mode="override",                                    view={"label": "ROC", "format": {"output": "percent", "mantissa": 2}}), # added later hence separate from roc field above
                    "gn_ulr":               hx.Float(mode="output",                                      view={"label": "GN ULR", "format": {"output": "percent", "mantissa": 2}}),
                    "gg_ulr":               hx.Float(mode="output",                                      view={"label": "GG ULR", "format": {"output": "percent", "mantissa": 2}}),
                    "quoted_premium_100":   hx.Float(mode="input", optionality="optional", default=None, view={"label": "Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "case_pricing_analysis_location": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Case Pricing Analysis Filepath"}),
                    "tracker_class":        hx.Str(mode="input", default=None, optionality="optional", view={"label": "Tracker Class"}, options_column="Trifocus List", options_table="table_trifocus_list")}),


                "section_ref_allocation": hx.Structure(children={
                
                    "num_ref":    hx.Int(     mode="input", default=5, optionality="required", view={"label": "Number of Section References"}, options=sec_ref_opt), 

                    # this is the main table
                    "table_pcts": hx.List(    mode="input", default_element_count=num_lob, async_output=[{"task": "sync_lob_lists_task", "reset": False}], children={
                        "label":            hx.Str(  mode="output",                                      view={"label": "Selected LOB"                            }),
                        "is_row_visible":   hx.Bool( mode="output"),
                        **{f"ref_{i:02}":   hx.Float(mode="input", default=None, optionality="optional", view={"label": f"Reference {i}", "format": percent_format(2)})   for i in range(1,num_refs+1)} }),

                    # these are the columns to the left and right
                    "section_ref":hx.Structure(view={"label": "Section Reference"}, children={
                        **{f"ref_{i:02}":   hx.Str(  mode="input", default=None, optionality="optional", view={"label": f"Reference {i}"                             })   for i in range(1,num_refs+1)} }),

                    "trifocus":   hx.Structure(view={"label": "TriFocus Group"}, children={
                        **{f"ref_{i:02}":   hx.Str(  mode="input", default=None, optionality="optional", view={"label": f"Reference {i}"}, options_column="Trifocus List", options_table="table_trifocus_list")   for i in range(1,num_refs+1)} }),

                    "total_pcts_by_ref": hx.Structure(view={"label": "Total"}, children={                                                                                                                         # TODO: REMOVE THIS LINE
                        **{f"ref_{i:02}":   hx.Float(mode="output", view={"label": f"Reference {i}", "format": percent_format(2)})                                        for i in range(1,num_refs+1)} }),       # TODO: REMOVE THIS LINE

                    "check":      hx.Structure(view={"label": "Check"}, children={                                                                                                                                # TODO: REMOVE THIS LINE
                        **{f"ref_{i:02}":   hx.Str(  mode="output",                                        view={"label": f"Reference {i}"})                                for i in range(1,num_refs+1)} }),     # TODO: REMOVE THIS LINE
    
                    # these are the totals at the bottom
                    "total_section_ref":hx.Structure(view={"label": "Section Reference"}, children={}),
                    "total_trifocus":   hx.Structure(view={"label": "TriFocus Group"}, children={}),

                    "total_pcts_by_lob":hx.List(mode="output",  view={"label": "Total"}, children={
                        "label":            hx.Str(  mode="output", view={"label": "Selected LOB"                      }),
                        "check":            hx.Str(  mode="output", view={"label": "Check"                             }),
                        "is_row_visible":   hx.Bool( mode="output"                                                      ),
                        "total":            hx.Float(mode="output", view={"label": "Total", "format": percent_format(2)})}),

                    "total_total_pcts": hx.Structure(view={"label": "Total"}, children={                                              #TODO: REMOVE THIS LINE
                        "total":            hx.Float(mode="output", view={"label": "Total", "format": percent_format(2)})}),          #TODO: REMOVE THIS LINE

                    "total_check":      hx.Structure(view={"label": "Check"}, children={                                              #TODO: REMOVE THIS LINE
                        "total":            hx.Str(  mode="output", view={"label": "Total"})}),                                       #TODO: REMOVE THIS LINE

                    "premium_by_lob": hx.List(mode="output",  view={"label": "BST Share GN EPI"}, children={                                              #TODO: REMOVE THIS LINE
                        "label":            hx.Str(  mode="output", view={"label": "Selected LOB"                      }),  
                        "is_row_visible":   hx.Bool( mode="output"                                                      ),                      
                        "total":            hx.Float(mode="output", view={"label": "BST Share GN EPI", "format": thousands_format(0)}),
                        }),                    

                    "metrics_by_ref":   hx.List(mode="output",  view={"label": "Metrics by Section Reference"}, children={
                        # "show_hide":                        hx.Bool( mode="output", view={"label": "Show"}),
                        "section_ref":                      hx.Str(  mode="output", view={"label": "Section Reference"}),
                        "trifocus":                         hx.Str(  mode="output", view={"label": "TriFocus"}),
                        "status":                           hx.Str(  mode="output", view={"label": "Status"}),
                        
                        "market_deductions":                hx.Float(mode="output", view={"label": "Market Deductions",                 "format": percent_format(2)  }),
                        "mga_fee":                          hx.Float(mode="output", view={"label": "Consortium Managers fee / MGA fee", "format": percent_format(2)  }),
                        "facility_brokerage":               hx.Float(mode="output", view={"label": "Facility Brokerage",                "format": percent_format(2)  }),
                        "leaders_fee":                      hx.Float(mode="output", view={"label": "Leaders Fee",                       "format": percent_format(2)  }), 
                        "service_fee":                      hx.Float(mode="output", view={"label": "Service Fee",                       "format": percent_format(2)  }),
                        "other":                            hx.Float(mode="output", view={"label": "Other",                             "format": percent_format(2)  }),
                        "selected_effective_deductions":    hx.Float(mode="output", view={"label": "Selected Effective Deductions",     "format": percent_format(2)  }),

                        "pc_impact":                        hx.Float(mode="output", view={"label": "PC Impact on Loss Ratio",           "format": percent_format(2)  }),
                        "written_line":                     hx.Float(mode="output", view={"label": "Written Line",                      "format": percent_format(2)  }),
                        "quoted_premium_gg_bst":            hx.Float(mode="output", view={"label": "BST Share Gross EPI",               "format": thousands_format(0)}),
                        "technical_premium_gg_bst":         hx.Float(mode="output", view={"label": "BST Share Gross Technical Premium", "format": thousands_format(0)}),
                        "benchmark_premium_gg_bst":         hx.Float(mode="output", view={"label": "BST Share Gross Benchmark Premium", "format": thousands_format(0)}),
                        "technical_premium_gg_bst_pre":     hx.Float(mode="output", view={"label": "BST Share Gross Technical Premium (Pre UW Adj)", "format": thousands_format(0)}),
                        "benchmark_premium_gg_bst_pre":     hx.Float(mode="output", view={"label": "BST Share Gross Benchmark Premium (Pre UW Adj)", "format": thousands_format(0)}),

                        "quoted_premium_gn_bst":            hx.Float(mode="output", view={"label": "BST Share Net EPI",                 "format": thousands_format(0)}),
                        "technical_premium_gn_bst":         hx.Float(mode="output", view={"label": "BST Share Net Technical Premium",   "format": thousands_format(0)}),
                        "benchmark_premium_gn_bst":         hx.Float(mode="output", view={"label": "BST Share Net Benchmark Premium",   "format": thousands_format(0)}),
                        "technical_premium_gn_bst_pre":     hx.Float(mode="output", view={"label": "BST Share Net Technical Premium (Pre UW Adj)",   "format": thousands_format(0)}),
                        "benchmark_premium_gn_bst_pre":     hx.Float(mode="output", view={"label": "BST Share Net Benchmark Premium (Pre UW Adj)",   "format": thousands_format(0)}),

                        "tpi":                              hx.Float(mode="output", view={"label": "TPI",                               "format": percent_format(2)  }),
                        "bpi":                              hx.Float(mode="output", view={"label": "BPI",                               "format": percent_format(2)  }),
                        "pflr":                             hx.Float(mode="output", view={"label": "Priced-for Loss Ratio",             "format": percent_format(2)  }),
                        "roc":                              hx.Float(mode="output", view={"label": "ROC",                               "format": percent_format(2)  }),
                        "rarc":                             hx.Float(mode="output", view={"label": "Rate Change",                               "format": percent_format(2)  }),

                        "tpi_pre_uw_adj":                   hx.Float(mode="output", view={"label": "TPI (Pre UW Adj)",                  "format": percent_format(2)  }),
                        "bpi_pre_uw_adj":                   hx.Float(mode="output", view={"label": "BPI (Pre UW Adj)",                  "format": percent_format(2)  }),
                        "pflr_pre_uw_adj":                  hx.Float(mode="output", view={"label": "Priced-for Loss Ratio (Pre UW Adj)","format": percent_format(2)  }),
                        "roc_pre_uw_adj":                   hx.Float(mode="output", view={"label": "ROC (Pre UW Adj)",                  "format": percent_format(2)  }),

                        "uw_adj_impact":                    hx.Float(mode="output", view={"label": "Impact of Underwriting Adjustment", "format": percent_format(2)  })  }),

                    "metrics_summary":   hx.Structure(view={"label": "Total"}, children={
                        # "show_hide":                        hx.Bool( mode="output", view={"label": "Show"}),
                        # "section_ref":                      hx.Str(  mode="output", view={"label": "Section Reference"}),
                        # "trifocus":                         hx.Str(  mode="output", view={"label": "TriFocus"}),
                        # "status":                           hx.Str(  mode="output", view={"label": "Status"}),
                        
                        "market_deductions":                hx.Float(mode="output", view={"label": "Market Deductions",                 "format": percent_format(2)  }),
                        "mga_fee":                          hx.Float(mode="output", view={"label": "Consortium Managers fee / MGA fee", "format": percent_format(2)  }),
                        "facility_brokerage":               hx.Float(mode="output", view={"label": "Facility Brokerage",                "format": percent_format(2)  }),
                        "leaders_fee":                      hx.Float(mode="output", view={"label": "Leaders Fee",                       "format": percent_format(2)  }), 
                        "service_fee":                      hx.Float(mode="output", view={"label": "Service Fee",                       "format": percent_format(2)  }),
                        "other":                            hx.Float(mode="output", view={"label": "Other",                             "format": percent_format(2)  }),
                        "selected_effective_deductions":    hx.Float(mode="output", view={"label": "Selected Effective Deductions",     "format": percent_format(2)  }),

                        "pc_impact":                        hx.Float(mode="output", view={"label": "PC Impact on Loss Ratio",           "format": percent_format(2)  }),
                        "written_line":                     hx.Float(mode="output", view={"label": "Written Line",                      "format": percent_format(2)  }),
                        "quoted_premium_gg_bst":            hx.Float(mode="output", view={"label": "BST Share Gross EPI",               "format": thousands_format(0)}),
                        "technical_premium_gg_bst":         hx.Float(mode="output", view={"label": "BST Share Gross Technical Premium", "format": thousands_format(0)}),
                        "benchmark_premium_gg_bst":         hx.Float(mode="output", view={"label": "BST Share Gross Benchmark Premium", "format": thousands_format(0)}),
                        "technical_premium_gg_bst_pre":     hx.Float(mode="output", view={"label": "BST Share Gross Technical Premium (Pre UW Adj)", "format": thousands_format(0)}),
                        "benchmark_premium_gg_bst_pre":     hx.Float(mode="output", view={"label": "BST Share Gross Benchmark Premium (Pre UW Adj)", "format": thousands_format(0)}),

                        "quoted_premium_gn_bst":            hx.Float(mode="output", view={"label": "BST Share Net EPI",                 "format": thousands_format(0)}),
                        "technical_premium_gn_bst":         hx.Float(mode="output", view={"label": "BST Share Net Technical Premium",   "format": thousands_format(0)}),
                        "benchmark_premium_gn_bst":         hx.Float(mode="output", view={"label": "BST Share Net Benchmark Premium",   "format": thousands_format(0)}),
                        "technical_premium_gn_bst_pre":     hx.Float(mode="output", view={"label": "BST Share Net Technical Premium (Pre UW Adj)",   "format": thousands_format(0)}),
                        "benchmark_premium_gn_bst_pre":     hx.Float(mode="output", view={"label": "BST Share Net Benchmark Premium (Pre UW Adj)",   "format": thousands_format(0)}),

                        "tpi":                              hx.Float(mode="output", view={"label": "TPI",                               "format": percent_format(2)  }),
                        "bpi":                              hx.Float(mode="output", view={"label": "BPI",                               "format": percent_format(2)  }),
                        "pflr":                             hx.Float(mode="output", view={"label": "Priced-for Loss Ratio",             "format": percent_format(2)  }),
                        "roc":                              hx.Float(mode="output", view={"label": "ROC",                               "format": percent_format(2)  }),
                        "rarc":                             hx.Float(mode="output", view={"label": "Rate Change",                               "format": percent_format(2)  }),

                        "tpi_pre_uw_adj":                   hx.Float(mode="output", view={"label": "TPI (Pre UW Adj)",                  "format": percent_format(2)  }),
                        "bpi_pre_uw_adj":                   hx.Float(mode="output", view={"label": "BPI (Pre UW Adj)",                  "format": percent_format(2)  }),
                        "pflr_pre_uw_adj":                  hx.Float(mode="output", view={"label": "Priced-for Loss Ratio (Pre UW Adj)","format": percent_format(2)  }),
                        "roc_pre_uw_adj":                   hx.Float(mode="output", view={"label": "ROC (Pre UW Adj)",                  "format": percent_format(2)  }),

                        "uw_adj_impact":                    hx.Float(mode="output", view={"label": "Impact of Underwriting Adjustment", "format": percent_format(2)  })  })
                })
            })
        })
                    
