import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils

def sch_rating_summary(cds):
    cds.extend_node_rater_defined("cds/layers", {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        "bpi_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
        'premium_label': hx.Str(mode='output'),
        "side_selection": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_cover_type", options_column="Value",view={"label": "Side Selection", "multiline":True}, async_input=["rarc_task"]),
        "side_ab_discount": hx.Float(mode="output",view={"label": "Model Side \n AB Discount", "format":utils.percent_format(1)}),
        "uw_side_ab_discount_override": hx.Float(mode="input", default=None, optionality="optional",view={"label": "UW Side AB \n Discount \n Override", "format": percent_format(1)}, async_input=["rarc_task"]),
        "notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Notes"}),
        "slip_leader": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_slip_lead", options_column="Markets",view={"label": "Slip Leader"}),
        "cover_in_uw_authority": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_yn", options_column="yesno",view={"label": "Cover Within \n UW Authority"}),
        "signoff_obtained": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_ynna", options_column="YesNo",view={"label": "Sign-off \n Obtained"}),
        "expected_loss_cost_att": hx.Float(mode="output",view={"label": "Total Attritional \n Loss","format": {"thousandSeparated": True, "mantissa": 0}}),
        "expected_loss_cost_cat": hx.Float(mode="output",view={"label": "Total Cat Loss","format": {"thousandSeparated": True, "mantissa": 0}}),
        "adr_standalone": hx.Float(mode="output",view={"label": "ADR Standalone","format": {"thousandSeparated": True, "mantissa": 0}}),
        "contagion": hx.Float(mode="output",view={"label": "Contagion","format": {"thousandSeparated": True, "mantissa": 0}}),
        "intl_standalone": hx.Float(mode="output",view={"label": "Intl Standalone","format": {"thousandSeparated": True, "mantissa": 0}}),
        "intl_large_company": hx.Float(mode="output",view={"label": "Intl Large \n Company","format": {"thousandSeparated": True, "mantissa": 0}}),
        "implied_ilf": hx.Float(mode="output",view={"label": "Implied ILF \n for Layer","format": {"thousandSeparated": True, "mantissa": 0}}),
        # 'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Achieved Loss Ratio (excl. UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
        # 'limit_for_rc_view': hx.Float(mode='output', optionality='optional', view={'label': 'Brokerage', 'format': {"thousandSeparated": True, "mantissa": 0}}),
        # 'excess_for_rc_view': hx.Float(mode='output', optionality='optional', view={'label': 'Brokerage', 'format': {"thousandSeparated": True, "mantissa": 0}}),
        # 'deductible_for_rc_view': hx.Float(mode='output', optionality='optional', view={'label': 'Brokerage', 'format': {"thousandSeparated": True, "mantissa": 0}}),
        'brokerage_for_rc_view': hx.Float(mode='output', optionality='optional', view={'label': 'Brokerage', 'format': {'output': 'percent', 'mantissa': 1}}),
        'technical_premium_pre_uw_adj_100': hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        'expected_loss_cost_pre_uw_adj_100':hx.Float(mode="output", optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "market_cap": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Market Cap","format": {"thousandSeparated": True, "mantissa": 0}}),
        "total_assets": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Total Assets","format": {"thousandSeparated": True, "mantissa": 0}}),
        "insider_share": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Market Cap","format": percent_format(1)}),
        "mmp_flag": hx.Bool(mode="output", async_input=["rarc_task"], view={"label": "Middle Market"}),
        "number_employees": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Number of Employees","format": {"thousandSeparated": True, "mantissa": 0}}),
        # "option_label": hx.Str(mode="output", view={"label": "Option"})
    })

    cds.extend_node_rater_defined("cds", {
        "large_cap": hx.Structure(view ={"label": ""}, children = {
            "layers": hx.List(mode="input", default_element_count=1, max_element_count=10, view={"label": "Layers"}, children={
                "limit": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "excess": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "deductible": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Deductible / \n SIR", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "aggregate_limit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "aggregate_deductible": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "currency": hx.Str(mode="input", default=None, optionality="optional", options=["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], view={"label": "Currency"}),
                "section_reference": hx.Str(mode="input", default=None, async_output=["start_renewal_task"], optionality="optional", view={"label": "Section \n Reference", "options": {"read_only": {"read_only": True}}}),
                "brokerage": hx.Float(mode="input", default=0, async_input=["rarc_task"], optionality="required", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}, "options": {"read_only": {"read_only": True, "label": "Brokerage (excl. PC's)"}}}),
                "written_line": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1.0}, view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}, "options": {"input": {"label": "Beazley \n Market Share"}, "read_only": {"read_only": True}}}),
                "premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross Bound Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "status": hx.Str(mode="input", default=None, async_output=["start_renewal_task"], optionality="optional", options_column="DealStatus", options_table="lst_deal_status", view={"label": "Status", "options": {"input": {"label": "Status"}, "read_only": {"label": "Deal Status by Renewal Layers", "read_only": True}}}),
                "is_primary_excess": hx.Str(mode="input", default=None, optionality="optional", options=["Primary", "Excess"], view={"label": "Primary or Excess"}),
                "benchmark_premium": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Gross \n Benchmark \n Premium \n (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI % \n (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "bpi_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "BPI % \n (excl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "model_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Model Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "unity_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Unity Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "quoted_premium": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Gross Quoted Premium", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"input": {"label": "Quoted Premium"}}}),
                "technical_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical \n Premium \n (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "technical_premium_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical \n Premium \n (excl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "technical_premium_net": hx.Float(mode="output", optionality="optional", view={"label": "Net Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI % \n (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "tpi_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "TPI % \n (excl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "pflr_att": hx.Float(mode="output", optionality="optional", view={"label": "Priced-for Loss Ratio (Att)", "format": {"output": "percent", "mantissa": 1}}),
                "pflr_cat": hx.Float(mode="output", optionality="optional", view={"label": "Priced-for Loss Ratio (Cat)", "format": {"output": "percent", "mantissa": 1}}),
                "pflr": hx.Float(mode="output", optionality="optional", view={"label": "Achieved Loss \n Ratio", "format": {"output": "percent", "mantissa": 1}}),
                "roc": hx.Float(mode="output", optionality="optional", view={"label": "RoC", "format": {"output": "percent", "mantissa": 1}}),
                "uw_adj_impact": hx.Float(mode="output", optionality="optional", view={"label": "Impact of Underwriting Adjustments", "format": {"output": "percent", "mantissa": 1}}),
                "trifocus": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Trifocus"}),
                "expected_loss_cost": hx.Float(mode="output", optionality="optional", view={"label": "Total Expected \n Losses", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expected_loss_cost_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expected_loss_cost_100": hx.Float(mode="output", optionality="optional", view={"label": "Expected Loss Cost (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "quoted_premium_net": hx.Float(mode="output", optionality="optional", view={"label": "Net Quoted Premium (AFB)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "quoted_premium_net_100": hx.Float(mode="output", optionality="optional", view={"label": "Net Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "quoted_premium_100": hx.Float(mode="input", default=0, optionality="optional", view={"label": "100% Gross \n Premium", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"input": {"label": "100% Gross \n Premium"}, "read_only": {"label": "100% Gross Premium", "read_only": True}}}),
                "quoted_premium_annual": hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Quoted Premium (AFB)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "quoted_premium_annual_100": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "benchmark_premium_net": hx.Float(mode="output", optionality="optional", view={"label": "Net Benchmark Premium (AFB)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "benchmark_premium_net_100": hx.Float(mode="output", optionality="optional", view={"label": "Net Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "benchmark_premium_100": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "benchmark_premium_annual": hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Benchmark Premium (AFB)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "benchmark_premium_annual_100": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Annualised Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "benchmark_premium_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "technical_premium_100": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "technical_premium_net_100": hx.Float(mode="output", optionality="optional", view={"label": "Net Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "pflr_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"output": "percent", "mantissa": 1}}),
                "bpi_case_priced": hx.Float(mode="input", default=0, optionality="required", view={"label": "BPI (Case Priced)", "format": {"output": "percent", "mantissa": 1}}),
                "premium_label": hx.Str(mode="output"),
                "side_selection": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", options_column="Value", options_table="lst_cover_type", view={"label": "Side Selection", "multiline": True}),
                "side_ab_discount": hx.Float(mode="output", view={"label": "Model Side \n AB Discount", "format": {"output": "percent", "mantissa": 1}}),
                "uw_side_ab_discount_override": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "UW Side AB \n Discount \n Override", "format": {"output": "percent", "mantissa": 1}}),
                "notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Notes"}),
                "slip_leader": hx.Str(mode="input", default=None, optionality="optional", options_column="Markets", options_table="lst_slip_lead", view={"label": "Slip Leader", "options": {"notSupported": {"style_cell": "hx-neutral"}}}),
                "cover_in_uw_authority": hx.Str(mode="input", default=None, optionality="optional", options_column="yesno", options_table="lst_yn", view={"label": "Cover Within \n UW Authority"}),
                "signoff_obtained": hx.Str(mode="input", default=None, optionality="optional", options_column="YesNo", options_table="lst_ynna", view={"label": "Sign-off \n Obtained"}),
                "expected_loss_cost_att": hx.Float(mode="output", view={"label": "Total Attritional \n Loss", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expected_loss_cost_cat": hx.Float(mode="output", view={"label": "Total Cat Loss", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "adr_standalone": hx.Float(mode="output", view={"label": "ADR Standalone", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "contagion": hx.Float(mode="output", view={"label": "Contagion", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "intl_standalone": hx.Float(mode="output", view={"label": "Intl Standalone", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "intl_large_company": hx.Float(mode="output", view={"label": "Intl Large \n Company", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "implied_ilf": hx.Float(mode="output", view={"label": "Implied ILF \n for Layer", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "limit_for_rc_view": hx.Float(mode="output", optionality="optional", view={"label": "Brokerage", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "excess_for_rc_view": hx.Float(mode="output", optionality="optional", view={"label": "Brokerage", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "deductible_for_rc_view": hx.Float(mode="output", optionality="optional", view={"label": "Brokerage", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "brokerage_for_rc_view": hx.Float(mode="output", optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),
                "technical_premium_pre_uw_adj_100": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expected_loss_cost_pre_uw_adj_100": hx.Float(mode="output", optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
            })
        })
    })

    cds.extend_node_rater_defined("cds", {
        "labels": hx.Structure(view ={"label": "Labels"}, children = {
            "uw_side_ab_discount_override_info": hx.Str(mode="output",view={"label": "UW Side AB Discount Override Info"}),
            "beazley_market_share_info": hx.Str(mode="output",view={"label": "Beazley Market Share Info"}),
            "section_reference_info": hx.Str(mode="output",view={"label": "Section Reference Info"}),
            "premium_and_costs_info": hx.Str(mode="output",view={"label": "Modelled Premium and Costs Info"}),
        }) 
    })

    cds.extend_node_rater_defined("cds", {
        "prem_build_up": hx.Structure(view ={"label": ""}, children = {
            "selected_option": hx.Str(mode="input", default="1", optionality="optional", view={"label": "Selected Layer"}),
            "options_list" : hx.List(mode="output",children={
                "option" :hx.Str(mode="output", view={"label": "List"})
        }),                 
            "technical_premium": hx.Structure(view={"label": "Technical"}, children={
                "gross_att_graph": hx.Float(mode='output', view={'label': 'Gross Attritional',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "gross_cat_graph": hx.Float(mode='output', view={'label': 'Gross Cat',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "cost_ri_graph": hx.Float(mode='output', view={'label': 'Cost of RI',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "expenses_graph": hx.Float(mode='output', view={'label': 'Expenses',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "profit_load_graph": hx.Float(mode='output', view={'label': 'Profit Load',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "brokerage_graph": hx.Float(mode='output', view={'label': 'Brokerage',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "bound_premium_graph": hx.Float(mode='output', view={'label': 'Bound Premium',"format": {"thousandSeparated": True, "mantissa": 0}}),
        }),
            "benchmark_premium": hx.Structure(view={"label": "Benchmark"}, children={
                "gross_att_graph": hx.Float(mode='output', view={'label': 'Gross Attritional',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "gross_cat_graph": hx.Float(mode='output', view={'label': 'Gross Cat',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "cost_ri_graph": hx.Float(mode='output', view={'label': 'Cost of RI',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "expenses_graph": hx.Float(mode='output', view={'label': 'Expenses',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "profit_load_graph": hx.Float(mode='output', view={'label': 'Profit Load',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "brokerage_graph": hx.Float(mode='output', view={'label': 'Brokerage',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "bound_premium_graph": hx.Float(mode='output', view={'label': 'Bound Premium',"format": {"thousandSeparated": True, "mantissa": 0}}),
        }),
            "bound_premium": hx.Structure(view={"label": "Bound"}, children={
                "gross_att_graph": hx.Float(mode='output', view={'label': 'Gross Attritional',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "gross_cat_graph": hx.Float(mode='output', view={'label': 'Gross Cat',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "cost_ri_graph": hx.Float(mode='output', view={'label': 'Cost of RI',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "expenses_graph": hx.Float(mode='output', view={'label': 'Expenses',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "profit_load_graph": hx.Float(mode='output', view={'label': 'Profit Load',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "brokerage_graph": hx.Float(mode='output', view={'label': 'Brokerage',"format": {"thousandSeparated": True, "mantissa": 0}}),
                "bound_premium_graph": hx.Float(mode='output', view={'label': 'Bound Premium',"format": {"thousandSeparated": True, "mantissa": 0}}),
        })}),
    })

    cds.extend_node_rater_defined("cds", {
        "rating_summary": hx.Structure(view ={"label": ""}, children = {                        
            "side_a_fifty_percentile": hx.Structure(view={"label": "50th %tile"}, children={
                "inclusive_dismissals": hx.Float(mode="output", view={"label": "Inclusive \n of Dismissals","format": {"thousandSeparated": True, "mantissa": 0}}),
                "at_cost_only": hx.Float(mode="output", view={"label": "At Cost Only","format": {"thousandSeparated": True, "mantissa": 0}}),
            }),
            "side_a_seventyfive_percentile": hx.Structure(view={"label": "75th %tile"}, children={
            "inclusive_dismissals": hx.Float(mode="output", view={"label": "Inclusive \n of Dismissals","format": {"thousandSeparated": True, "mantissa": 0}}),          
            "at_cost_only": hx.Float(mode="output", view={"label": "At Cost Only","format": {"thousandSeparated": True, "mantissa": 0}}),
            }),  
            "side_abc_fifty_percentile": hx.Structure(view={"label": "50th %tile"}, children={
                "inclusive_dismissals": hx.Float(mode="output", view={"label": "Inclusive \n of Dismissals","format": {"thousandSeparated": True, "mantissa": 0}}),
                "at_cost_only": hx.Float(mode="output", view={"label": "At Cost Only","format": {"thousandSeparated": True, "mantissa": 0}}),
            }),
            "side_abc_seventyfive_percentile": hx.Structure(view={"label": "75th %tile"}, children={
            "inclusive_dismissals": hx.Float(mode="output", view={"label": "Inclusive \n of Dismissals","format": {"thousandSeparated": True, "mantissa": 0}}),          
            "at_cost_only": hx.Float(mode="output", view={"label": "At Cost Only", "format": {"thousandSeparated": True, "mantissa": 0}}),
            }),
            "side_a_sca_freq": hx.Float(mode="output",view={"label": "Wtd. SCA Freq", "format": percent_format(2)}),  
            "side_abc_sca_freq": hx.Float(mode="output",view={"label": "Wtd. SCA Freq", "format": percent_format(2)}),    
        }),        
    })

    
    # Override values
    cds.override_node_properties("cds/standard_fields/benchmark_class", {"mode": "output"})

    cds.override_node_properties("cds/layers", {"default_element_count":10, "max_element_count": 10})

    cds.override_node_properties("cds/layers/status", {"mode": "output", "options_column":"DealStatus", "options_table":"lst_deal_status",})

    cds.override_node_properties("cds/layers/section_reference", {"mode": "output"})

    cds.override_node_properties("cds/layers/quoted_premium_100", {"mode": "output","view": {"label": "100% Gross \n Premium"}})

    cds.override_node_properties("cds/layers/written_line", {"mode": "output", "validation":{"min_value": 0, "max_value": 1.0}})

    cds.override_node_properties("cds/layers/technical_premium", {"view": {"label": "Gross Technical \n Premium \n (incl. UW adj)"}})

    cds.override_node_properties("cds/layers/technical_premium_pre_uw_adj", {"view": {"label": "Gross Technical \n Premium \n (excl. UW adj)"}})

    cds.override_node_properties("cds/layers/brokerage", {"mode": "output", "async_input": ["rarc_task"]})

    cds.override_node_properties("cds/layers/tpi", {"view": {"label": "TPI % \n (incl. UW adj)"}})

    cds.override_node_properties("cds/layers/tpi_pre_uw_adj", {"view": {"label": "TPI % \n (excl. UW adj)"}})

    cds.override_node_properties("cds/layers/roc", {"view": {"label": "RoC"}})

    cds.override_node_properties("cds/layers/bpi", {"view": {"label": "BPI % \n (incl. UW adj)"}})

    cds.override_node_properties("cds/layers/bpi_pre_uw_adj", {"view": {"label": "BPI % \n (excl. UW adj)"}})

    cds.override_node_properties("cds/layers/expected_loss_cost", {"view": {"label": "Total Expected \n Losses"}})

    cds.override_node_properties("cds/layers/pflr", {"view": {"label": "Achieved Loss \n Ratio"}})

    cds.override_node_properties("cds/layers/pflr_pre_uw_adj", {"view" : {"format": {"output": "percent", "mantissa": 1}}})

    cds.override_node_properties("cds", {"view": {"label": ""}})

    cds.override_node_properties("cds/layers/currency", {"mode": "output", "async_input": ["rarc_task"]})

    # cds.override_node_properties("cds/currencies/source_currency", {"default": "USD", "async_input": ["rarc_task", "populate_capiq_data_task"]})

    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})
    
    # Add nodes to async_inputs for rarc_task
    cds.override_node_properties("cds/layers/limit", {"mode": "output","async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/excess", {"mode": "output","async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/deductible", {"mode": "output","async_input": ["rarc_task"],"view": {"label": "Deductible / \n SIR"}})
    cds.override_node_properties("cds/layers/quoted_premium", {"mode": "output", "async_input": ["rarc_task"], "view": {"options": {"input" : {"label": "Quoted Premium"}}}})    
    # cds.override_node_properties("cds/layers/quoted_premium", {"default": 0, "optionality": "required", "async_input": ["rarc_task"], "view": {"options": {"input" : {"label": "Quoted Premium"}, "read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"],"view": {"label": "Gross \n Benchmark \n Premium \n (incl. UW adj)"}})
    

    # Override dropdown links
    cds.override_node_properties(
        'cds/prem_build_up/selected_option', 
        {'options_data': "../options_list", 'options_field': "option", "view": {"label":"Selected Layer", "multiline": True}}
        )
  
