# v0.5.0
import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers, new_column
import data_schema.sch_utilities as utils
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict
from data_schema.sch_rate_change import rarc_task_name

### --- DEFINE GENERIC RATING NODES  --- ###
rating_summary_new_nodes_dict = {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        'bpi_case_priced': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'BPI (Case Priced)', 'format': percent_format(1)}),
        # 'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}), # EDIT v0.3.0 removed since it has moved to CDS 1.3
        'premium_label': hx.Str(mode='output'),
        # EDIT v0.3.0 - Add 100 % premium for rating summary 
        'technical_premium_pre_uw_adj_100': hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        'technical_premium_annual_100': hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Technical Premium 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        'technical_premium_annual': hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Technical Premium AFB%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        'expected_loss_cost_pre_uw_adj_100':hx.Float(mode="output", optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),

}
### --- DEFINE RATING NODES FOR LAYER --- ###
def sch_rating_summary(cds):
    cds.extend_node_rater_defined('cds/layers', {**rating_summary_new_nodes_dict})
    cds.override_node_properties("cds/layers/quoted_premium",{"mode":"output","optionality":"optional","async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (AFB)", "format": {"thousandSeparated": True, "mantissa": 0}},})

    # Previous definition in data_schema/sch_pricing.py kept for reference:
    # "experience_weighting": hx.Float(mode="output", view={"label": "Experience\nWeighting",  "format": {"output": "percent", "mantissa": 1}}),
    # cds.override_node_properties(
    #     "cds/layers/experience_weighting",
    #     {
    #         "mode": "override",
    #         "view": {"label": new_column+"Experience\nWeighting", "format": {"output": "percent", "mantissa": 1}},
    #     },
    # )
    # Previous definition in data_schema/sch_pricing.py kept for reference:
    # "experience_weighting": hx.Float(mode="output", view={"label": "Experience\nWeighting",  "format": {"output": "percent", "mantissa": 1}}),
    # cds.override_node_properties(
    #     "cds/layers_addl/experience_weighting",
    #     {
    #         "mode": "override",
    #         "view": {"label": new_column+"Experience\nWeighting", "format": {"output": "percent", "mantissa": 1}},
    #     },
    # )
        
    if not RARC_INSURED_ASSET_USE: # Edit v0.5.0
        # EDIT v0.3.0 change quoted_premium_100 node type to input and quote_premium (Beazley) to output
        cds.override_node_properties("cds/layers/quoted_premium_100",{"mode":"input","default": 0,"optionality":"required","async_input":[rarc_task_name],"view":{"label": "Quoted\nPremium", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only": {"read_only": True}},"group":"100% Gross Share"},})
        cds.override_node_properties("cds/layers/currency", {"mode":"input", "default": "USD", "optionality": "required","async_input": [rarc_task_name],"options":["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], "view":{"label": "Currency"}})

    else:
        cds.override_node_properties("cds/layers/quoted_premium_100",{"mode":"output","optionality":"optional","async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}},})
        cds.override_node_properties("cds/layers/currency",{"mode":"output", "optionality":"optional", "async_input": [rarc_task_name],"view":{"label": "Currency"},})
    
### --- DEFINE RATING NODES FOR COVERAGES --- ###
def sch_rating_summary_coverages(cds):
    cds.extend_node_rater_defined('cds/layers/coverages', {**rating_summary_new_nodes_dict})
    # EDIT v0.3.0 change quoted_premium_100 node type to input and quote_premium (Beazley) to output
    for cvg in coverages_dict.keys():
        if not RARC_INSURED_ASSET_USE:
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/quoted_premium_100",{"mode":"input","default": 0,"async_input":[rarc_task_name],"optionality":"required","view":{"label": "Quoted Premium", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only": {"read_only": True}},"group":"100% Gross Share"},})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/currency",{"mode":"input", "default":"USD", "optionality":"optional", "async_input":[rarc_task_name],"options":["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], "view":{"label": "Currency"}})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/brokerage",{"mode":"input", "default":0, "optionality":"optional", "async_input":[rarc_task_name],"view":{"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/limit",{"mode":"input", "default":0, "optionality":"optional", "async_input":[rarc_task_name],"view":{"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/excess",{"mode":"input", "default":0, "optionality":"optional", "async_input":[rarc_task_name],"view":{"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}})
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/deductible",{"mode":"input", "default":0, "optionality":"optional", "async_input":[rarc_task_name],"view":{"label": "Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}})
        
        else:
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/brokerage",{"mode":"input", "async_input":[rarc_task_name], "default":0, "optionality":"optional", "async_input":[rarc_task_name],"view":{"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}})
            
            cds.override_node_properties(f"cds/layers/coverages/{cvg}/currency",{"mode":"output","optionality":"optional", "async_input":[rarc_task_name],"options":["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], "view":{"label": "Currency"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/quoted_premium",{"mode":"output", "async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (AFB)", "format": {"thousandSeparated": True, "mantissa": 0}},})
