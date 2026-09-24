# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_rate_change import rarc_task_name
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
from algorithms.rate_constants import get_aop_lawyers_count, get_aop_ae_count, project_type_map, project_type_parent_categories, get_aop_aec_parent_categories, get_aop_lpl_parent_categories
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST

# Replace / remove examples with your models exposures

def insured_asset_coverages():
    if RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE:
        return {
            # NOTE: Example of Insured Asset List with Coverages. Replace with your models insureds asset list
            f"{COVERAGES_LIST[0]}": hx.List(mode="input",  async_input=[rarc_task_name], async_output=[{"task": rarc_task_name, "reset": False}], children={
            "unique_id": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "unique_id"}),
            "country": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Country"}),
            "city": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "City"}),
            "type": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Type"}),
            "tiv": hx.Float(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "TIV", "format": utils.thousands_format(0)}),
            "currency": hx.Str(mode="input", default="USD", async_input=[rarc_task_name], optionality="required", options=["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], view={"label": "Currency"}),
            "limit": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0)}),
            "excess": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0)}),
            "deductible": hx.Float(mode="input", default=None,  async_input=[rarc_task_name], optionality="optional", view={"label": "Deductible", "format": utils.thousands_format(0)}),
            "brokerage": hx.Float(mode="output", async_input=[rarc_task_name, "run_simulation_task"], optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),
            "quoted_premium_100": hx.Float(mode="input", default=0, async_input=[rarc_task_name],  optionality="required", view={"label": "Quoted\nPremium", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only": {"read_only": True}},"group":"100% Gross Share"}),
            "quoted_premium_annual_100": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium_annual": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_net_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_net": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_pre_uw_adj_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expected_loss_cost_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expected_loss_cost_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expected_loss_cost_pre_uw_adj_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "bpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
            "bpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "bpi_case_priced": hx.Float(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": {"output": "percent", "mantissa": 1}}),
            "tpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
            "tpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "pflr": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio", "format": {"output": "percent", "mantissa": 1}}),
            "pflr_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "roc": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),
            "uw_adj_impact": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Impact of Underwriting Adjustments", "format": {"output": "percent", "mantissa": 1}}),
            "written_line": hx.Float(mode="input",  async_input=[rarc_task_name], default=0, optionality="optional", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}, "options": {"read_only": {"read_only": True}}}),
            "status": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], view={"label": "Status", "options": {"read_only": {"read_only": True}}}),
            "section_reference": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "Section Reference", "options": {"read_only": {"read_only": True}}}),
            "policy_term": hx.Float(mode="output"),
            "start_date": hx.Date(default="2018-01-01", mode="input", view={"label": "Start Date"}),
            "end_date": hx.Date(default="2018-12-31", mode="input", view={"label": "End Date"}),
            }
            ),
            # NOTE: Example of Insured Asset List with Coverages. Replace with your models insureds asset list
            f"{COVERAGES_LIST[1]}": hx.List(mode="input",  async_input=[rarc_task_name], async_output=[{"task": rarc_task_name, "reset": False}], children={
            "unique_id": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "unique_id"}),
            "country": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Country"}),
            "city": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "City"}),
            "type": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Type"}),
            "tiv": hx.Float(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "TIV", "format": utils.thousands_format(0)}),
            "currency": hx.Str(mode="input", default="USD", async_input=[rarc_task_name], optionality="required", options=["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], view={"label": "Currency"}),
            "limit": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0)}),
            "excess": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0)}),
            "deductible": hx.Float(mode="input", default=None,  async_input=[rarc_task_name], optionality="optional", view={"label": "Deductible", "format": utils.thousands_format(0)}),
            "brokerage": hx.Float(mode="output", async_input=[rarc_task_name, "run_simulation_task"], optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),
            "quoted_premium_100": hx.Float(mode="input", default=0, async_input=[rarc_task_name],  optionality="required", view={"label": "Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only": {"read_only": True}},"group":"100% Gross Share"}),
            "quoted_premium_annual_100": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium_annual": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_net_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_net": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_pre_uw_adj_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expected_loss_cost_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expected_loss_cost_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expected_loss_cost_pre_uw_adj_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "bpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
            "bpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "bpi_case_priced": hx.Float(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": {"output": "percent", "mantissa": 1}}),
            "tpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
            "tpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "pflr": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio", "format": {"output": "percent", "mantissa": 1}}),
            "pflr_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "roc": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),
            "uw_adj_impact": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Impact of Underwriting Adjustments", "format": {"output": "percent", "mantissa": 1}}),
            "written_line": hx.Float(mode="input",  async_input=[rarc_task_name], default=0, optionality="optional", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}, "options": {"read_only": {"read_only": True}}}),
            "status": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], view={"label": "Status", "options": {"read_only": {"read_only": True}}}),
            "section_reference": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "Section Reference", "options": {"read_only": {"read_only": True}}}),
            "policy_term": hx.Float(mode="output"),
            "start_date": hx.Date(default="2018-01-01", mode="input", view={"label": "Start Date"}),
            "end_date": hx.Date(default="2018-12-31", mode="input", view={"label": "End Date"}),
            }
            )
        }
    else:
        return {}

def exposure_details_rows():
    return hx.List(mode="input", async_input=["rarc_task"], children={
            "policy_year": hx.Str(mode="output", view={"label": "Policy Year"}),
            "professional_services_fee": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Professional Services\nFee"}),
            "epc_design_construct_values": hx.Float(mode="input", default=0, optionality="optional", view={"label": "EPC Design\n& Construct Values"}),
            "hard_fm_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Hard FM\nRevenues"}),
            "construct_pass_soft_fm_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Construct Only/\nPass Through Costs/\nSoft FM Revenues"}),
            "revenue_100_pcnt": hx.Float(mode="input", view={"label": "100%\nRevenues"}),
            "notional_revenue": hx.Float(mode="input", view={"label": "Notional\nRevenues"}),
            "revalued_notional_revenue": hx.Float(mode="input", view={"label": "Revalued\nNotional Revenues"}),
            # "revenue_100_pcnt": hx.Float(mode="output", view={"label": "100%\nRevenues"}),
            # "notional_revenue": hx.Float(mode="output", view={"label": "Notional\nRevenues"}),
            # "revalued_notional_revenue": hx.Float(mode="output", view={"label": "Revalued\nNotional Revenues"}),
            "weighting": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Weighting"})
        }),

def sch_exposure_details(cds):
    def weighting_node_def(key):
        node = hx.Float(mode="output", view={"label": "Weighting", "format": {"output": "percent", "mantissa": 1}})
        # if key < 6:
        #     node = hx.Float(mode="output", view={"label": "Weighting", "format": {"output": "percent", "mantissa": 1}})
        # else:
        #     node = hx.Float(mode="input", default=0, optionality="optional", view={"label": "Weighting", "format": {"output": "percent", "mantissa": 1}})
        return node

    def input_output_float_node(value, bool_is_pcnt, year_label):
        if value["type"] == "input":
            if bool_is_pcnt:
                node = hx.Float(mode="input",  async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": year_label,"format": {"output": "percent", "mantissa": 1}})
            else:
                node = hx.Float(mode="input",  async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": year_label,"format": {"thousandSeparated": True, "mantissa": 0}})
        else:
            if bool_is_pcnt:
                node = hx.Float(mode="output",  async_input=["run_simulation_task","rarc_task"], view={"label": year_label,"format": {"output": "percent", "mantissa": 1}})
            else:
                node = hx.Float(mode="output",  async_input=["run_simulation_task","rarc_task"], view={"label": year_label,"format": {"thousandSeparated": True, "mantissa": 0}})
        
        return node

    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        # PLACEHOLDER value used in experience rating, the experience rating should connect to the total exposure value of the model
        "example_aggregate_exposure": hx.Float(mode="input", default=0, view={"label": "Agg Exposure", "format": utils.thousands_format(0)}),
        
    })

    # For granular exposure lists e.g. aircrafts, hospitals etc, please add to the granular node
    cds.extend_node_rater_defined("cds/exposure/granular", {        
        # NOTE: Replace the below with your models exposures
        "chart_loss_cost_by_revenue": hx.Structure(
            children={
                        "data": hx.Structure(
                            children = {
                                "label_uk": hx.Str(mode="output", view={"label": "Year"}),
                                "label_eu": hx.Str(mode="output", view={"label": "Year"}),
                                "points_uk": hx.List(
                                    mode="input",
                                    default_element_count=35,
                                    children={
                                        "revenue": hx.Float(mode="output", view={"label": "Revenue/Fees", "format": utils.thousands_format(0)}),
                                        "loss_cost": hx.Float(mode="output", view={"format": utils.thousands_format(1), "chart": {"series_type": "pointline"}}),
                                    },
                                ),
                                "points_eu": hx.List(
                                    mode="input",
                                    default_element_count=35,
                                    children={
                                        "revenue": hx.Float(mode="output", view={"label": "Revenue/Fees", "format": utils.thousands_format(0)}),
                                        "loss_cost": hx.Float(mode="output", view={"format": utils.thousands_format(1), "chart": {"series_type": "pointline"}}),
                                    },
                                )
                            }
                        ),
                    },
        ),
        "example_exposure": hx.List(mode="input",  async_input=["rarc_task"], children={
            "country": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Country"}),
            "city": hx.Str(mode="input", default=None, optionality="optional", view={"label": "City"}),
            "type": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Type"}),
            "tiv": hx.Float(mode="input", default=None, optionality="optional", view={"label": "TIV", "format": utils.thousands_format(0)}),
        }),
        "exposure_expected_current_year": hx.Float(mode="output", async_input=["run_simulation_task", "rarc_task"], view={"label":"Expected Exposure - Current Year", "format": utils.thousands_format(0)}),
        "exposure_expected_current_year_label": hx.Str(mode="output"),
        "exposure_details_notes": hx.Str(mode="output", view={"label": "Notes For Exposure Data"}),
        "bool_show_inception_year_client_details_input": hx.Bool(mode="input", default=False, view={"label": "View Policy Inception Year"}),
        "bool_show_inception_year_client_details_output_pcnt": hx.Bool(mode="output"),
        "bool_show_inception_year_client_details_output_value": hx.Bool(mode="output"),       
        "client_details_lawyers": hx.Structure(children={
            "notes": hx.Str(mode="output", view={"label":"Notes" }),
            "size_of_matters": hx.Str(mode="input", async_input=["run_simulation_task","rarc_task"], options_table="ref_tbl_complexity", options_column="Complexity", default_index=0, view={"label":"Size of matters worked on"}),
            "uw_comments": hx.Str(mode="input", default=None, optionality="optional", view={"label":"Underwriter Comments"}),
            "bool_is_pcnt": hx.Bool(mode="input", default=True, view={"label": "Enter Split as Percentage"}),
            "bool_is_pcnt_not": hx.Bool(mode="output"),
            "areas_of_practice_chart": hx.Structure(children={
                **{f"{key}": hx.Structure(children={
                    "expected_loss_cost": hx.Float(mode="output", view={"label": "Expected Loss Cost", "format": {"thousandSeparated": True, "mantissa": 0}})
                    },
                )
                for key in get_aop_lpl_parent_categories()}, 
            }),
            "areas_of_practice": hx.List(mode="input", 
                default_element_count=get_aop_lawyers_count(), 
                fixed_element_count=get_aop_lawyers_count(), 
                children={
                    "areas_of_practice": hx.Str(mode="input", 
                                    view={"label": "Areas of Practice"}, 
                                    options_table="ref_lpl_aop_loading",
                                    options_column="Area of Practice",
                                    default_index = 0,
                                    fixed_values_column = "Area of Practice",
                                    fixed_values_table = "ref_lpl_aop_loading",
                                    async_input=["run_simulation_task"]
                                    ),
                    "year_0_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                    "year_0_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_1_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_1","format": {"output": "percent", "mantissa": 1}}),
                    "year_1_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}), 
                    "year_2_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_2","format": {"output": "percent", "mantissa": 1}}),
                    "year_2_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),
                    "year_3_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_3","format": {"output": "percent", "mantissa": 1}}),
                    "year_3_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),                    
                    "year_4_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_4","format": {"output": "percent", "mantissa": 1}}),
                    "year_4_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),                    
                    "year_5_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_5","format": {"output": "percent", "mantissa": 1}}),
                    "year_5_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),
                    "weighted": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],view={"label": "Weighted % Split","format": {"output": "percent", "mantissa": 1}}),
                    "frequency": hx.Float(mode="output",view={"label": "Frequency", "format":utils.percent_format(1), "group": "Loading"}),
                    "severity": hx.Float(mode="output", view={"label": "Severity", "format": utils.percent_format(1), "group": "Loading"})
                }
            ),
            "areas_of_practice_total": hx.Structure(
                        view={"label": "Total"},
                        children={
                            "year_0_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                            "year_0_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0","format":{"output": "percent", "mantissa": 1}}),
                            "year_1_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_1","format": {"output": "percent", "mantissa": 1}}),
                            "year_1_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                            "year_2_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_2","format": {"output": "percent", "mantissa": 1}}),
                            "year_2_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                            "year_3_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_3","format": {"output": "percent", "mantissa": 1}}),
                            "year_3_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),                 
                            "year_4_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_4","format": {"output": "percent", "mantissa": 1}}),
                            "year_4_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),                 
                            "year_5_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_5","format": {"output": "percent", "mantissa": 1}}),
                            "year_5_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                            "weighted": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "Weighted % Split","format": {"output": "percent", "mantissa": 1}}),
                            "frequency": hx.Float(mode="output",view={"label": "Lambda\n(Mean Freq)", "format": {"thousandSeparated": True, "mantissa": 3}, "group": "Adjusted"}),
                            "severity": hx.Float(mode="output", view={"label": "Mu\n(Severity Parameter)", "format": {"thousandSeparated": True, "mantissa": 3}, "group": "Adjusted"}),   
                        }
            ),
            "summary_year_total_aop_labels": hx.Structure(children={
                "year_0": hx.Str(mode="output"),
                "year_1": hx.Str(mode="output"),
                "year_2": hx.Str(mode="output"),
                "year_3": hx.Str(mode="output"),
                "year_4": hx.Str(mode="output"),
                "year_5": hx.Str(mode="output")
            }),
        }),
        "client_details_AEC": hx.Structure(children={
            "notes": hx.Str(mode="output", view={"label":"Notes" }),
            "size_of_matters": hx.Str(mode="input", async_input=["run_simulation_task","rarc_task"], options_table="ref_tbl_complexity", options_column="Complexity", default_index=0, view={"label":"Size of matters worked on"}),
            "uw_comments": hx.Str(mode="input", default=None, optionality="optional", view={"label":"Underwriter Comments"}),
            "bool_aop_is_pcnt": hx.Bool(mode="input", default=True, view={"label": "Enter Split as Percentage"}),
            "bool_aop_is_pcnt_not": hx.Bool(mode="output"),       
            "bool_ipt_is_pcnt": hx.Bool(mode="input", default=True, view={"label": "Enter Split as Percentage"}),
            "bool_ipt_is_pcnt_not": hx.Bool(mode="output"),   
            "bool_ipt_enter_at_level":hx.Bool(mode="input", default=True, view={"label": "Enter at Individual Project Level?"}),
            "bool_ipt_enter_at_level_not":hx.Bool(mode="output"),
            "weighted_pcnt_filter_value": hx.Float(mode="input", optionality="optional", default=0.0, view={"label": "Weighted % Filter Value", "format": {"output": "percent", "mantissa": 1}}),
            "areas_of_practice_chart": hx.Structure(children={
                **{f"{key}": hx.Structure(children={
                    "expected_loss_cost": hx.Float(mode="output", view={"label": "Expected Loss Cost", "format": {"thousandSeparated": True, "mantissa": 0}})
                    },
                )
                for key in get_aop_aec_parent_categories()}, 
            }),
            "areas_of_practice": hx.List(mode="input", 
                            default_element_count=get_aop_ae_count(), 
                            fixed_element_count=get_aop_ae_count(), 
                            children={
                                "areas_of_practice": hx.Str(mode="input", 
                                                view={"label": "Areas of Practice"}, 
                                                options_table="ref_ae_aop_loading",
                                                options_column="Area of Practice",
                                                default_index = 0,
                                                fixed_values_column = "Area of Practice",
                                                fixed_values_table = "ref_ae_aop_loading",
                                                async_input=["run_simulation_task"]
                                                ),
                                "year_0_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                                "year_0_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),
                                "year_1_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_1","format": {"output": "percent", "mantissa": 1}}),
                                "year_1_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}), 
                                "year_2_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_2","format": {"output": "percent", "mantissa": 1}}),
                                "year_2_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),
                                "year_3_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_3","format": {"output": "percent", "mantissa": 1}}),
                                "year_3_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),                    
                                "year_4_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_4","format": {"output": "percent", "mantissa": 1}}),
                                "year_4_value": hx.Float(mode="input",async_input=["run_simulation_task","rarc_task"], default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),                    
                                "year_5_pcnt": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_5","format": {"output": "percent", "mantissa": 1}}),
                                "year_5_value": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"],default=0, optionality="optional", view={"label": "year_0","format": {"thousandSeparated": True, "mantissa": 0}}),
                                "weighted": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],view={"label": "Weighted % Split","format": {"output": "percent", "mantissa": 1}}),
                                "frequency": hx.Float(mode="output",view={"label": "Frequency", "format":utils.percent_format(1), "group": "Loading"}),
                                "severity": hx.Float(mode="output", view={"label": "Severity", "format": utils.percent_format(1), "group": "Loading"})
                            }
            ),
            "areas_of_practice_total": hx.Structure(
                        view={"label": "Total"},
                        children={
                            "year_0_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                            "year_0_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"], view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                            "year_1_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_1","format": {"output": "percent", "mantissa": 1}}),
                            "year_1_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                            "year_2_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_2","format": {"output": "percent", "mantissa": 1}}),
                            "year_2_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                            "year_3_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_3","format": {"output": "percent", "mantissa": 1}}),
                            "year_3_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),                 
                            "year_4_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_4","format": {"output": "percent", "mantissa": 1}}),
                            "year_4_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),                    
                            "year_5_pcnt": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_5","format": {"output": "percent", "mantissa": 1}}),
                            "year_5_value": hx.Float(mode="output", async_input=["run_simulation_task","rarc_task"],  view={"label": "year_0","format": {"output": "percent", "mantissa": 1}}),
                            "weighted": hx.Float(mode="output", async_input=["run_simulation_task", "rarc_task"], view={"label": "Weighted % Split","format": {"output": "percent", "mantissa": 1}}),
                            "frequency": hx.Float(mode="output",view={"label": "Lambda\n(Mean Freq)", "format": {"thousandSeparated": True, "mantissa": 3}, "group": "Adjusted"}),
                            "severity": hx.Float(mode="output", view={"label": "Mu\n(Severity Parameter)", "format": {"thousandSeparated": True, "mantissa": 3}, "group": "Adjusted"})   
                        }
            ),
            "summary_year_total_aop_labels": hx.Structure(children={
                "year_0": hx.Str(mode="output"),
                "year_1": hx.Str(mode="output"),
                "year_2": hx.Str(mode="output"),
                "year_3": hx.Str(mode="output"),
                "year_4": hx.Str(mode="output"),
                "year_5": hx.Str(mode="output")
            }),
            "summary_year_total_ipt_labels": hx.Structure(children={
                "year_0": hx.Str(mode="output"),
                "year_1": hx.Str(mode="output"),
                "year_2": hx.Str(mode="output"),
                "year_3": hx.Str(mode="output"),
                "year_4": hx.Str(mode="output"),
                "year_5": hx.Str(mode="output")
            }),
            "individual_project_types_chart": hx.Structure(children={
                **{f"{key}": hx.Structure(children={
                    "expected_loss_cost": hx.Float(mode="output", view={"label": "Expected Loss Cost", "format": {"thousandSeparated": True, "mantissa": 0}})
                    },
                )
                for key in project_type_parent_categories},                
            }),
            "individual_project_types": hx.Structure(children={
                **{f"{key}":hx.Structure(children={
                    "year_0_pcnt": input_output_float_node(value, True, "year_0"),
                    "year_0_value": input_output_float_node(value, False if key != "total" else True, "year_0"),
                    "year_1_pcnt": input_output_float_node(value, True, "year_1"),
                    "year_1_value": input_output_float_node(value, False if key != "total" else True, "year_1"),
                    "year_2_pcnt": input_output_float_node(value, True, "year_2"),
                    "year_2_value": input_output_float_node(value, False if key != "total" else True, "year_2"),
                    "year_3_pcnt": input_output_float_node(value, True, "year_3"),
                    "year_3_value": input_output_float_node(value, False if key != "total" else True, "year_3"),
                    "year_4_pcnt": input_output_float_node(value, True, "year_4"),
                    "year_4_value": input_output_float_node(value, False if key != "total" else True, "year_4"),
                    "year_5_pcnt": input_output_float_node(value, True, "year_5"),
                    "year_5_value": input_output_float_node(value, False if key != "total" else True, "year_5"),
                    "weighted": hx.Float(mode="output", async_input=["run_simulation_task", "rarc_task"], view={"label": "Weighted % Split","format": {"output": "percent", "mantissa": 1}}),
                    "frequency": hx.Float(mode="output",view={"label": "Frequency" if key != "total" else "Lambda\n(Mean Freq)", 
                                                                "format":utils.percent_format(1) if key != "total" else {"thousandSeparated": True, "mantissa": 3}, 
                                                                "group": "Loading" if key != "total" else "Adjusted"}),
                    "severity": hx.Float(mode="output", view={"label": "Severity" if key!= "total" else "Mu\n(Severity Parameter)", 
                                                                "format": utils.percent_format(1) if key != "total" else {"thousandSeparated": True, "mantissa": 3}, 
                                                                "group": "Loading" if key != "total" else "Adjusted"}),
                    "parent_label": hx.Str(mode="output"), #fixed_values=value["parent"])
                    "filter": hx.Bool(mode="output"),
                    "expected_loss_cost": hx.Float(mode="output", view={"label": "Expected Loss Cost", "format": {"thousandSeparated": True, "mantissa": 0}})
                },view={"label":value["label"]})
                for key, value in project_type_map.items()}
            })
        }),
        "exposure_details": hx.Structure(children={
            **{f"year_{key}": hx.Structure(children={"policy_year": hx.Str(mode="output", view={"label": "Policy Year"}),
            "gross_fee": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Gross Fee"}) if key < 16 else hx.Float(mode="override", view={"label": "Gross Fee"}),
            "professional_services_fee": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Professional\nServices Fee"}) if key < 16 else hx.Float(mode="override", view={"label": "Professional\nServices Fee"}),
            "epc_design_construct_values": hx.Float(mode="input", default=0, optionality="optional", view={"label": "EPC Design\n& Construct Values"}) if key < 16 else hx.Float(mode="override", view={"label": "EPC Design\n& Construct Values"}),
            "hard_fm_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Hard FM\nRevenues"}) if key < 16 else hx.Float(mode="override", view={"label": "Hard FM\nRevenues"}),
            # "gross_fee": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Gross Fee"}),
            # "professional_services_fee": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Professional\nServices Fee"}),
            # "epc_design_construct_values": hx.Float(mode="input", default=0, optionality="optional", view={"label": "EPC Design\n& Construct Values"}),
            # "hard_fm_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Hard FM\nRevenues"}),
            "construct_pass_soft_fm_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Construct Only/\nPass Through Costs/\n Soft FM Revenues"}) if key < 16 else hx.Float(mode="override", view={"label": "Construct Only/\nPass Through Costs/\n Soft FM Revenues"}),
            #"construct_pass_soft_fm_revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Construct Only/\nPass Through Costs/\n Soft FM Revenues"}),
            "revenue_100_pcnt": hx.Float(mode="input", default=0, view={"label": "100%\nRevenues"}),
            "notional_revenue": hx.Float(mode="input", default=0, view={"label": "Notional\nRevenues"}),
            "revalued_notional_revenue": hx.Float(mode="input", default=0, view={"label": "Revalued\nNotional Revenues"}),
            "revalued_fee":hx.Float(mode="input", default=0, view={"label": "Revalued\nFee"}),
            # "revenue_100_pcnt": hx.Float(mode="output", view={"label": "100%\nRevenues"}),
            # "notional_revenue": hx.Float(mode="output", view={"label": "Notional\nRevenues"}),
            # "revalued_notional_revenue": hx.Float(mode="output", view={"label": "Revalued\nNotional Revenues"}),
            # "revalued_fee":hx.Float(mode="output", view={"label": "Revalued\nFee"}),
            "weighting": weighting_node_def(key)
            })
            for key in range(20, -1, -1)}
        }),
        "exposure_details_year_labels": hx.Structure(children={
            **{f"year_{key}": hx.Str(mode="output")
            for key in range(20, -1, -1)}
            }
        ),

        # NOTE: Example of Insured Asset List with Layer. Replace with your models insureds asset list
        "layers": hx.List(mode="input",  async_input=[rarc_task_name], async_output=[{"task": rarc_task_name, "reset": False}], children={
            "unique_id": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "unique_id"}),
            "country": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Country"}),
            "city": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "City"}),
            "type": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Type"}),
            "tiv": hx.Float(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "TIV", "format": utils.thousands_format(0)}),
            "currency": hx.Str(mode="input", default="USD", async_input=[rarc_task_name], optionality="required", options=["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], view={"label": "Currency"}),
            "limit": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0)}),
            "excess": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0)}),
            "deductible": hx.Float(mode="input", default=None,  async_input=[rarc_task_name], optionality="optional", view={"label": "Deductible", "format": utils.thousands_format(0)}),
            "brokerage": hx.Float(mode="output", async_input=[rarc_task_name, "run_simulation_task"], optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),
            "quoted_premium_100": hx.Float(mode="input", default=0, async_input=[rarc_task_name],  optionality="required", view={"label": "Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only": {"read_only": True}},"group":"100% Gross Share"}),
            "quoted_premium_annual_100": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium_annual": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "quoted_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_net_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_net": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_pre_uw_adj_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expected_loss_cost_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expected_loss_cost_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expected_loss_cost_pre_uw_adj_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "bpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
            "bpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "bpi_case_priced": hx.Float(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": {"output": "percent", "mantissa": 1}}),
            "tpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
            "tpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "pflr": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio", "format": {"output": "percent", "mantissa": 1}}),
            "pflr_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "roc": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),
            "uw_adj_impact": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Impact of Underwriting Adjustments", "format": {"output": "percent", "mantissa": 1}}),
            "written_line": hx.Float(mode="input",  async_input=[rarc_task_name], default=0, optionality="optional", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}, "options": {"read_only": {"read_only": True}}}),
            "status": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], view={"label": "Status", "options": {"read_only": {"read_only": True}}}),
            "section_reference": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "Section Reference", "options": {"read_only": {"read_only": True}}}),
            "policy_term": hx.Float(mode="output"),
            "start_date": hx.Date(default="2018-01-01", mode="input", view={"label": "Start Date"}),
            "end_date": hx.Date(default="2018-12-31", mode="input", view={"label": "End Date"}),
            }
        ),
        **insured_asset_coverages()
        # # NOTE: Example of Insured Asset List with Coverages. Replace with your models insureds asset list
        # f"{COVERAGES_LIST[0]}": hx.List(mode="input",  async_input=[rarc_task_name], async_output=[{"task": rarc_task_name, "reset": False}], children={
        #     "unique_id": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "unique_id"}),
        #     "country": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Country"}),
        #     "city": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "City"}),
        #     "type": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Type"}),
        #     "tiv": hx.Float(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "TIV", "format": utils.thousands_format(0)}),
        #     "currency": hx.Str(mode="input", default="USD", async_input=[rarc_task_name], optionality="required", options=["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], view={"label": "Currency"}),
        #     "limit": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0)}),
        #     "excess": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0)}),
        #     "deductible": hx.Float(mode="input", default=None,  async_input=[rarc_task_name], optionality="optional", view={"label": "Deductible", "format": utils.thousands_format(0)}),
        #     "brokerage": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),
        #     "quoted_premium_100": hx.Float(mode="input", default=0, async_input=[rarc_task_name],  optionality="required", view={"label": "Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only": {"read_only": True}}}),
        #     "quoted_premium_annual_100": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "quoted_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "quoted_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "quoted_premium_annual": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "quoted_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_net_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_net": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_pre_uw_adj_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "expected_loss_cost_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "expected_loss_cost_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "expected_loss_cost_pre_uw_adj_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "bpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
        #     "bpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
        #     "bpi_case_priced": hx.Float(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": {"output": "percent", "mantissa": 1}}),
        #     "tpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
        #     "tpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
        #     "pflr": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio", "format": {"output": "percent", "mantissa": 1}}),
        #     "pflr_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "roc": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),
        #     "uw_adj_impact": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Impact of Underwriting Adjustments", "format": {"output": "percent", "mantissa": 1}}),
        #     "written_line": hx.Float(mode="input",  async_input=[rarc_task_name], default=0, optionality="optional", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}, "options": {"read_only": {"read_only": True}}}),
        #     "status": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], view={"label": "Status", "options": {"read_only": {"read_only": True}}}),
        #     "section_reference": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "Section Reference", "options": {"read_only": {"read_only": True}}}),
        #     "policy_term": hx.Float(mode="output"),
        #     "start_date": hx.Date(default="2018-01-01", mode="input", view={"label": "Start Date"}),
        #     "end_date": hx.Date(default="2018-12-31", mode="input", view={"label": "End Date"}),
        #     }
        # ),
        # # NOTE: Example of Insured Asset List with Coverages. Replace with your models insureds asset list
        # f"{COVERAGES_LIST[1]}": hx.List(mode="input",  async_input=[rarc_task_name], async_output=[{"task": rarc_task_name, "reset": False}], children={
        #     "unique_id": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "unique_id"}),
        #     "country": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Country"}),
        #     "city": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "City"}),
        #     "type": hx.Str(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "Type"}),
        #     "tiv": hx.Float(mode="input", default=None, optionality="optional", async_input=[rarc_task_name], view={"label": "TIV", "format": utils.thousands_format(0)}),
        #     "currency": hx.Str(mode="input", default="USD", async_input=[rarc_task_name], optionality="required", options=["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], view={"label": "Currency"}),
        #     "limit": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0)}),
        #     "excess": hx.Float(mode="input", default=None, async_input=[rarc_task_name], optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0)}),
        #     "deductible": hx.Float(mode="input", default=None,  async_input=[rarc_task_name], optionality="optional", view={"label": "Deductible", "format": utils.thousands_format(0)}),
        #     "brokerage": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),
        #     "quoted_premium_100": hx.Float(mode="input", default=0, async_input=[rarc_task_name],  optionality="required", view={"label": "Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only": {"read_only": True}}}),
        #     "quoted_premium_annual_100": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "quoted_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "quoted_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "quoted_premium_annual": hx.Float(mode="output", async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "quoted_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Quoted Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_net_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_net": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Net Benchmark Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "benchmark_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_annual_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_net_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_annual": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Annualised Gross Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_net": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Net Technical Premium (AFB%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "technical_premium_pre_uw_adj_100": hx.Float(mode="output", async_input=[rarc_task_name],  optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "expected_loss_cost_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (100%)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "expected_loss_cost_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "expected_loss_cost_pre_uw_adj_100": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "bpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
        #     "bpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "BPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
        #     "bpi_case_priced": hx.Float(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": {"output": "percent", "mantissa": 1}}),
        #     "tpi": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
        #     "tpi_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "TPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
        #     "pflr": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio", "format": {"output": "percent", "mantissa": 1}}),
        #     "pflr_pre_uw_adj": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "roc": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),
        #     "uw_adj_impact": hx.Float(mode="output",  async_input=[rarc_task_name], optionality="optional", view={"label": "Impact of Underwriting Adjustments", "format": {"output": "percent", "mantissa": 1}}),
        #     "written_line": hx.Float(mode="input",  async_input=[rarc_task_name], default=0, optionality="optional", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}, "options": {"read_only": {"read_only": True}}}),
        #     "status": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], view={"label": "Status", "options": {"read_only": {"read_only": True}}}),
        #     "section_reference": hx.Str(mode="input",  async_input=[rarc_task_name], default=None, optionality="optional", view={"label": "Section Reference", "options": {"read_only": {"read_only": True}}}),
        #     "policy_term": hx.Float(mode="output"),
        #     "start_date": hx.Date(default="2018-01-01", mode="input", view={"label": "Start Date"}),
        #     "end_date": hx.Date(default="2018-12-31", mode="input", view={"label": "End Date"}),
        #     }
        # )
    })
