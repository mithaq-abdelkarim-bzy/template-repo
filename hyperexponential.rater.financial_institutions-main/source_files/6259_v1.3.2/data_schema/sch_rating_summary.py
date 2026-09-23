import hx_data_schema as hxd
from libraries.common_data_schema.data_schema.utilities import integer_format, percent_format, thousands_format

from algorithms.rate_constants import coverages, max_layers, max_towers
from algorithms.rate_utilities import get_field_options


def sch_rating_summary(cds):
    # Add coverages
    cds.extend_node_items("cds/layers/coverages", {
        "crime": {"label": "Crime"},
        "pi": {"label": "PI"},
        "do": {"label": "D&O"},
    })

    # Layers fields
    cds.extend_node_rater_defined("cds/layers", {
        "label": hxd.Str(mode="output", view={"label": "Layer"}),

        # Used for rate change calcs
        'quoted_premium_annualised': hxd.Float(mode='output', async_input=["rarc_task"]),
        "quoted_premium_pro_rata_100": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=[{"task": "num_layers_task", "reset": False}], view={"options":{"input":{"label": "100% Gross\nPremium"},
                                                                                                                                                                                                            "read_only": {"label": "Gross Quoted Premium", "read_only": True, "format": {"thousandSeparated": True, "mantissa": 0}}}}),              
        "benchmark_premium_annualised_100": hxd.Float(mode="output", async_input=["rarc_task"], view={"label": "Annual Gross\nBenchmark\nPremium (100%)", "format": thousands_format()}),
        "benchmark_premium_pro_rata_100": hxd.Float(mode="output", async_input=["rarc_task"], view={"label": "Pro Rata Gross\nBenchmark\nPremium (100%)", "format": thousands_format()}),
        "technical_premium_100": hxd.Float(mode="output", async_input=["rarc_task"], view={"label": "Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),

        **build_towers(),

        "ncb": hxd.Float(mode="input", default=None, optionality="optional", async_output=[{"task": "num_layers_task", "reset": False}], async_input=["rarc_task"], view={"label": "NCB", "group": "Brokerage & Discounts", "format": percent_format(mantissa=2)}),
        "lta": hxd.Float(mode="input", default=None, optionality="optional", async_output=[{"task": "num_layers_task", "reset": False}], async_input=["rarc_task"], view={"label": "LTA", "group": "Brokerage & Discounts", "format": percent_format(mantissa=2)}),
        "net_premium": hxd.Float(mode="output", view={"label": "100% Net\nPremium", "format": {"thousandSeparated": True, "mantissa": 0}}),

        "esg": hxd.Bool(mode="input", default=False, async_output=[{"task": "num_layers_task", "reset": False}], view={"label": "ESG add'l\ncapacity"}),

        "exposure": hxd.Float(mode="output", view={"label": "Beazley\nExposure", "format": thousands_format()}),
        "afb_net_premium": hxd.Float(mode="output", view={"label": "AFB Net Prem", "format": thousands_format()}),
        "net_rol": hxd.Float(mode="output", view={"label": "Net ROL", "format": percent_format(mantissa=3)}),
        "actual_ilf": hxd.Float(mode="output", view={"label": "Actual ILF", "format": percent_format(mantissa=1)}),        
        "slip_lead": hxd.Str(mode="input", default="", options_table="table_slip_lead", options_column="market", allow_custom_value=True, async_output=[{"task": "num_layers_task", "reset": False}], view={"label": "Slip Leader"}),

        "net_lol": hxd.Float(mode="output", view={"label": "Net LOL", "format": percent_format(mantissa=1)}),
        "model_ilf": hxd.Float(mode="output", view={"label": "Model ILF", "format": percent_format(mantissa=1)}),
        "expected_loss_cost_att": hxd.Float(mode="output", view={"label": "Att", "group": "Proportion of Expected Losses", "format": percent_format(mantissa=1)}),
        "expected_loss_cost_cat": hxd.Float(mode="output", view={"label": "Cat", "group": "Proportion of Expected Losses", "format": percent_format(mantissa=1)}),
        "expected_loss_cost_annualised": hxd.Float(mode='output'),
        "pflr_pre_uw_adj": hxd.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"output": "percent", "mantissa": 1}}),

        # Secondry rating summary table (different currency)
        "net_premium_fx": hxd.Float(mode="output", view={"label": "100% Net\nPremium", "format": thousands_format()}),
        "exposure_fx": hxd.Float(mode="output", view={"label": "Beazley\nExposure", "format": thousands_format()}),
        "afb_net_premium_fx": hxd.Float(mode="output", view={"label": "AFB Net Prem", "format": thousands_format()}),
        "quoted_premium_pro_rata_100_fx": hxd.Float(mode="output", view={"label": "100% Gross\nPremium", "format": thousands_format()}),
        "benchmark_premium_pro_rata_100_fx": hxd.Float(mode="output", view={"label": "Pro Rata Gross\nBenchmark\nPremium (100%)", "format": thousands_format()}),
        "benchmark_premium_annualised_100_fx": hxd.Float(mode="output", view={"label": "Annual Gross\nBenchmark\nPremium (100%)", "format": thousands_format()}),
        "technical_premium_fx": hxd.Float(mode="output", view={"label": "Pro-Rata Gross\nTechnical\nPremium (AFB)", "format": thousands_format()}),
        "technical_premium_net_fx": hxd.Float(mode="output", view={"label": "Annual Gross\nTechnical\nPremium (AFB)", "format": thousands_format()}),
    })

    # Coverages fields
    cds.extend_node_rater_defined("cds/layers/coverages", {
        "premium_split": hxd.Float(mode="input", default=None, optionality="optional", async_output=[{"task": "num_layers_task", "reset": False}], async_input=["rarc_task"], view={"group": "Split of Premium", "format": percent_format(mantissa=2)}),
        "losses_split": hxd.Float(mode="output", view={"group": "Split of Model Losses", "format": percent_format(mantissa=1)}),
        "pol_ref": hxd.Str(mode="input", default="", async_output=[{"task": "num_layers_task", "reset": False}], view={"group": "Policy Reference"}),
        "pol_ref_non_eea": hxd.Str(mode="input", default="", optionality="optional", async_output=[{"task": "num_layers_task", "reset": False}], view={"group": "Policy Reference - Non EEA"}),
        "all_manager": hxd.Structure(children={
            "sublimit": hxd.Float(mode="input", default=None, optionality="optional", async_output=[{"task": "num_layers_task", "reset": False}], async_input=["rarc_task"], view={"group": "Sublimits", "format": thousands_format()}),
            "sublimit_fx": hxd.Float(mode="output", view={"group": "Sublimits", "format": thousands_format()})
        }),
        "fund": hxd.Structure(children={
            "sublimit": hxd.Float(mode="input", default=None, optionality="optional", async_output=[{"task": "num_layers_task", "reset": False}], async_input=["rarc_task"], view={"group": "Sublimits", "format": thousands_format()}),
            "sublimit_fx": hxd.Float(mode="output", view={"group": "Sublimits", "format": thousands_format()}),
        }),
    })

    # Override values
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers, "async_output": [{"task": "num_layers_task", "reset": False}]})
    cds.override_node_properties("cds/layers/currency", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/brokerage", {
        "default": None,
        "optionality": "optional",
        "async_input": ["rarc_task"],
        "async_output": [{"task": "num_layers_task", "reset": False}],
        "view": {"options": {
            "input": {"label": "Brokerage", "group": "Brokerage & Discounts", "format": percent_format(mantissa=2)},
            "read_only": {"label": "Brokerage", "format": percent_format(mantissa=1), "read_only": True}
        }}
    })
    cds.override_node_properties("cds/layers/written_line", {"mode": "output"})
    cds.override_node_properties(f"cds/layers/quoted_premium", {"mode": "output", "async_input": ["rarc_task"]})            
    cds.override_node_properties(f"cds/layers/benchmark_premium", {"mode": "output", "async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/technical_premium", {"view": {"label": "Pro-Rata Gross\nTechnical\nPremium (AFB)"}})
    cds.override_node_properties("cds/layers/technical_premium_net", {"view": {"label": "Annual Gross\nTechnical\nPremium (AFB)"}})
    cds.override_node_properties("cds/layers/status", {
        "default": "None",
        "optionality": "required",
        "options": get_field_options("rating_summary", "status"),
        "async_output": [{"task": "num_layers_task", "reset": False}],
        "view": {"options": {
            "input": {"label": "Status"},
            "read_only": {"read_only": True}
        }}
    })
    cds.override_node_properties("cds/layers/section_reference", {
        "mode":"output", "async_input":["export_to_excel"], "view":{"label": "Section Reference"}
    })

    # Coverages
    for coverage, label in coverages:
        cds.override_node_properties(f"cds/layers/coverages/{coverage}/premium_split", {"view": {"label": f"{label}"}})
        cds.override_node_properties(f"cds/layers/coverages/{coverage}/losses_split", {"view": {"label": f"{label}"}})
        cds.override_node_properties(f"cds/layers/coverages/{coverage}/pol_ref", {"view": {"label": f"{label}"}})
        cds.override_node_properties(f"cds/layers/coverages/{coverage}/pol_ref_non_eea", {"view": {"label": f"{label}"}})
        cds.override_node_properties(f"cds/layers/coverages/{coverage}/all_manager/sublimit", {
            "view": {
                "label": f"{label}",
                "options": {"manager": {"label": f"{label}\n(Manager)"}}
            }
        })
        cds.override_node_properties(f"cds/layers/coverages/{coverage}/all_manager/sublimit_fx", {
            "view": {
                "label": f"{label}",
                "options": {"manager": {"label": f"{label}\n(Manager)"}}
            }
        })
        cds.override_node_properties(f"cds/layers/coverages/{coverage}/fund/sublimit", {"view": {"label": f"{label}\n(Fund)"}})
        cds.override_node_properties(f"cds/layers/coverages/{coverage}/fund/sublimit_fx", {"view": {"label": f"{label}\n(Fund)"}})

    # Currency Rate for secondary table
    cds.extend_node_rater_defined("cds", {
        "rating_summary": hxd.Structure(children={
            "authorities_fx": hxd.Float(mode="override", optionality="optional", view={"label": "Exchange Rate"})
        })
    })


def sch_rating_summary_non_cds():
    return {
        "rating_summary": hxd.Structure(children={
            **build_towers_non_cds(),
            **build_coverages_non_cds(),
            "table1_label": hxd.Str(mode="output", view={"label": "Values Shown in"}),
            "is_brokerage_per_layer": hxd.Bool(mode="output"),
            "secondry_summary_show": hxd.Bool(mode="output"),
        })
    }


def build_towers():
    towers = {}
    for i in range(1, max_towers+1):
        towers[f"tower_{i}"] = hxd.Structure(children={
            "coverage": hxd.Str(mode="override", optionality="optional", options_table="table_coverages", options_column="cover", allow_custom_value=True, view={"label": f"Tower {i}", "group": "Coverage"}),
            "limit": hxd.Float(mode="input", default=None, optionality="optional", async_output=[{"task": "num_layers_task", "reset": False}], async_input=["rarc_task"], view={"label": f"Tower {i}", "group": "Limit", "format": thousands_format()}),
            "excess": hxd.Float(mode="override", optionality="optional", async_input=["rarc_task"], view={"label": f"Tower {i}", "group": "Excess", "format": thousands_format(), "options":{"read_only": {"read_only": True}}}),
            "excess_str": hxd.Str(mode="output", view={"label": f"Tower {i}", "group": "Excess"}),
            "direct_reinstatements": hxd.Int(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 10000}, async_output=[{"task": "num_layers_task", "reset": False}], async_input=["rarc_task"], view={"label": f"Tower {i}", "group": "Direct Reinstatements"}),
            "rtc_reinstatements": hxd.Float(mode="input", default=None, optionality="optional", async_output=[{"task": "num_layers_task", "reset": False}], async_input=["rarc_task"], view={"label": f"Tower {i}", "group": "RTC Reinstatements", "format": integer_format(1)}),
            "beazley_line": hxd.Float(mode="input", default=None, optionality="optional", async_output=[{"task": "num_layers_task", "reset": False}], view={"label": f"Tower {i}", "group": "AFB Line", "format": percent_format(mantissa=2)}),

            # Different currency
            "limit_fx": hxd.Float(mode="output", view={"label": f"Tower {i}", "group": "Limit", "format": thousands_format()}),
            "excess_fx": hxd.Float(mode="output", view={"label": f"Tower {i}", "group": "Excess", "format": thousands_format()}),
            "excess_str_fx": hxd.Str(mode="output", view={"label": f"Tower {i}", "group": "Excess"}),
            "rtc_reinstatements_fx": hxd.Float(mode="output", view={"label": f"Tower {i}", "group": "RTC Reinstatements", "format": integer_format(1)})
        })
    return towers


def build_towers_non_cds():
    towers = {}
    for i in range(1, max_towers+1):
        towers[f"tower_{i}"] = hxd.Structure(children={
            "direct_reinstatements_show": hxd.Bool(mode="output"),
            "rtc_reinstatements_show": hxd.Bool(mode="output"),
            "coverage_show": hxd.Bool(mode="output"),
        })
    return towers


def build_coverages_non_cds():
    covers = {}

    for c, _ in coverages:
        covers[c] = hxd.Structure(children={
            "sublimit_show": hxd.Bool(mode="output"),
            "all_manager_sublimit_show": hxd.Bool(mode="output"),
            "fund_sublimit_show": hxd.Bool(mode="output"),
            "premium_split_show": hxd.Bool(mode="output"),
            "pol_ref_non_eea_show": hxd.Bool(mode="output"),
        })
    return covers
