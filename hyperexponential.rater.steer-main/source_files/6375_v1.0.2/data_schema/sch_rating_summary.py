# v0.5.0
import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format, create_node_from_list
# from data_schema.sch_utilities import percent_format
# from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers, reinstatement_max_number
import data_schema.sch_utilities as utils
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict
from data_schema.sch_rate_change import rarc_task_name

### --- DEFINE RATING NODES FOR LAYER --- ###
def sch_rating_summary(cds):
    cds.extend_node_rater_defined('cds/layers', {**additional_layer_nodes()})
    cds.override_node_properties("cds/layers/quoted_premium",{"mode":"output","optionality":"optional","async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (AFB)", "format": {"thousandSeparated": True, "mantissa": 0}},})
        
    if not RARC_INSURED_ASSET_USE: # Edit v0.5.0
        # EDIT v0.3.0 change quoted_premium_100 node type to input and quote_premium (Beazley) to output
        cds.override_node_properties("cds/layers/quoted_premium_100",{"mode":"input","default": 0,"optionality":"required","async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only": {"read_only": True}}},})
        cds.override_node_properties("cds/layers/currency", {"mode":"input", "default": "USD", "optionality": "required","async_input": [rarc_task_name],"options":["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], "view":{"label": "Currency"}})

    else:
        cds.override_node_properties("cds/layers/quoted_premium_100",{"mode":"output","optionality":"optional","async_input":[rarc_task_name],"view":{"label": "Gross Quoted Premium (100%)", "format": {"thousandSeparated": True, "mantissa": 0}},})
        cds.override_node_properties("cds/layers/currency",{"mode":"output", "optionality":"optional", "async_input": [rarc_task_name],"view":{"label": "Currency"},})
    
    cds.extend_node_rater_defined('cds', {**rating_summary_programme_nodes()})

def rating_summary_programme_nodes():
    return {
        "programme_all": hx.Structure(view={"label": "Programme\n(All)"}, children={
            **_total_children(),
        }),
        "programme_selected": hx.Structure(view={"label": "Programme\n(Selected)"}, children={
            **_total_children(),
        }), 
        "technical_price_assumptions": hx.Structure(view={"label": "Technical\nPrice\nAssumptions"}, children={
            **_technical_price_assumptions(),
        }),    
    }

### --- DEFINE GENERIC RATING NODES  --- ###
def additional_layer_nodes():
    return {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        'bpi_case_priced': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'BPI (Case Priced)', 'format': percent_format(1)}),
        # 'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}), # EDIT v0.3.0 removed since it has moved to CDS 1.3
        'premium_label': hx.Str(mode='output'),
        # EDIT v0.3.0 - Add 100 % premium for rating summary 
        'technical_premium_pre_uw_adj_100': hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        'technical_premium_annual_100': hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Technical Premium 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        'technical_premium_annual': hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Technical Premium AFB%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        'expected_loss_cost_pre_uw_adj_100':hx.Float(mode="output", optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment) 100%", "format": {"thousandSeparated": True, "mantissa": 0}}),
        'include_layer':hx.Bool(mode="input", default=True, view={"label": "Include?"}),
        "advanced_features_input": hx.Structure(view={"label": "Advanced\nFeatures"}, children={
            **_layers_advanced_features_input(),
        }), 
        "loss_corridor": hx.Structure(view={"label": "Loss\nCorridor"}, children={
            **_layers_loss_corridor(),
        }), 
        "swing_rates": hx.Structure(view={"label": "Swing\nRate"}, children={
            **_layers_swing_rates(),
        }), 
        **_layers_additional_nodes(),
        **_layers_advanced_features_summary(),
        **_layers_rating_summary(),
        "healthcare_cat": hx.Structure(view={"label": "Loss\nCorridor"}, children={
            **_healthcare_cat_layers(),
        }), 
        "glr": hx.Float(mode="output", optionality="optional", view={"label": "Gross Loss Ratio", "format": {"output": "percent", "mantissa": 2}}),
                

    }

def _layers_advanced_features_input():
    node_info_list = [
    ("AAD",hx.Float,"input",0,utils.thousands_format(0),["advanced_features_task"],None),

    ]
    return create_node_from_list(node_info_list) 

def _layers_loss_corridor():
    node_info_list = [
    ("Min Rate",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),
    ("Max Rate",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),
    ("Insured Participation",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),
    ]
    return create_node_from_list(node_info_list) 

def _layers_swing_rates():
    node_info_list = [
    ("Swing Brokerage",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),
    ("Use Swing Brokerage",hx.Bool,"input",False,None,["advanced_features_task"],None),
    ("Deposit Rate",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),
    ("Min Rate",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),
    ("Max Rate",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),
    ("Margin",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),
    ("Loading Factor",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),
    ("Claims Cap Pct",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None),

    ]
    return create_node_from_list(node_info_list) 

def _layers_additional_nodes():
    node_info_list = [
        ("EPI 100",hx.Float,"input",None,utils.thousands_format(0),["advanced_features_task"],None,"optional"),
        ("Rate",hx.Float,"input",None,utils.percent_format(2),["advanced_features_task"],None,"optional"),
        ("Ceding Commission",hx.Float,"input",0,utils.percent_format(2),["advanced_features_task"],None,"optional"),
        ("NCB",hx.Float,"input",None,utils.percent_format(2),["advanced_features_task"],None,"optional"),
        ("Profit Commission Rate",hx.Float,"input",None,utils.percent_format(2),["advanced_features_task"],None,"optional"),
        ("Expense Allowance",hx.Float,"input",None,utils.percent_format(2),["advanced_features_task"],None,"optional"),
        ("Bkg Gross or Net",hx.Str,"input",None,None,["advanced_features_task"],None,"optional"),
        ("Cap Gross Pct",hx.Float,"input",None,utils.percent_format(2),["advanced_features_task"],None,"optional"),
        ("Loss Cap Used",hx.Bool,"output",None,utils.percent_format(2),["advanced_features_task"],None,"optional"),
        ("No Reinstatement",hx.Str,"input","0",None,["advanced_features_task"],None,"optional"),
        ("BPI Case Priced 100",hx.Float,"input",0,utils.thousands_format(0),None,None),

    ] 

    result = create_node_from_list(node_info_list)

    for index in range(1,reinstatement_max_number+1):
        result[f"reinstatement_pct_{index}"]= hx.Float(mode="input",default=None, async_input=["advanced_features_task"],optionality="optional", view={"label": f"{index}", "format": {"output": "percent", "mantissa": 2}}) 
    return result


def _layers_advanced_features_summary():

    node_info_list = [

        ("Expected Loss",hx.Float,"output",None,utils.thousands_format(0),["advanced_features_task"],None),
        ("Expected AAD",hx.Float,"input",0,utils.thousands_format(0),None,["advanced_features_task",{"task": "start_renewal_task", "reset": True}]),
        ("Loss Corridor Loss Cost",hx.Float,"input",0,utils.thousands_format(0),None,["advanced_features_task",{"task": "start_renewal_task", "reset": True}]),
        ("Expected Losses After Loss Sensitive Features",hx.Float,"output",None,utils.thousands_format(0),None,None),

        ("Upfront Premium Gross 100",hx.Float,"output",None,utils.thousands_format(0),["advanced_features_task"],None),
        ("Upfront Premium Net 100",hx.Float,"output",None,utils.thousands_format(0),None,None),

        ("Expected Premium Paid Gross 100",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Expected Premium Paid Net 100",hx.Float,"output",None,utils.thousands_format(0),None,None),

        ("Expected Reinstatement Factor",hx.Float,"input",0,utils.percent_format(2),None,["advanced_features_task",{"task": "start_renewal_task", "reset": True}]),
        ("Expected NCB Pct",hx.Float,"input",0,utils.percent_format(2),None,["advanced_features_task",{"task": "start_renewal_task", "reset": True}]),
        ("Profit Commission",hx.Float,"input",0,utils.thousands_format(0),None,["advanced_features_task",{"task": "start_renewal_task", "reset": True}]),
        ("Swing Premium",hx.Float,"input",0,utils.thousands_format(0),None,["advanced_features_task",{"task": "start_renewal_task", "reset": True}]),


        ("Number of RIPS",hx.Int,"output",None,utils.thousands_format(0),["advanced_features_task"],None),
        ("Brokerage Inc Swing",hx.Float,"output",None,utils.percent_format(2),["advanced_features_task"],None),

    ]

    return create_node_from_list(node_info_list) 


def _layers_rating_summary():

    node_info_list = [
        ("Expected Loss inc NMP",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Pure Rate",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Line Size",hx.Float,"output",None,utils.thousands_format(0),None,None),
        
        ("Claim Frequency",hx.Float,"output",None,utils.thousands_format(2),None,["advanced_features_task"]),
        ("Average Cost per Claim",hx.Float,"output",None,utils.thousands_format(0),None,["advanced_features_task"]),
    
    ]
    return create_node_from_list(node_info_list) 

def _total_children():

    node_info_list = [
        ("Expected Loss",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Expected Losses After Loss Sensitive Features",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Expected Loss Inc NMP",hx.Float,"output",None,utils.thousands_format(0),None,None),
        
        # ("Upfront Premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Upfront Premium Gross 100",hx.Float,"output",None,utils.thousands_format(0),None,None),

        ("Upfront Premium Net 100",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Expected Premium Paid Gross 100",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Expected Premium Paid Net 100",hx.Float,"output",None,utils.thousands_format(0),None,None),
        
        ("Quoted Premium 100",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Benchmark Premium 100",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Technical Premium 100",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Quoted Premium Net 100",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Benchmark Premium Net 100",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Technical Premium Net 100",hx.Float,"output",None,utils.thousands_format(0),None,None),

        ("Quoted Premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Line Size",hx.Float,"output",None,utils.thousands_format(0),None,None),
        
        ("BPI",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("TPI",hx.Float,"output",None,utils.percent_format(2),None,None),
        
        ("PFLR",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("ROC",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("GLR",hx.Float,"output",None,utils.percent_format(2),None,None),

        
        ]
    return create_node_from_list(node_info_list) 

def _technical_price_assumptions():

    node_info_list = [

    ("Select Class",hx.Str,"input",None,None,None,None,"optional"),
    ("COB Reference",hx.Str,"output",None,None,None,None),


    ("Benchmark Loss Ratio",hx.Float,"output",None,utils.percent_format(2),None,None),
    ("Claims Handling Expenses",hx.Float,"output",None,utils.percent_format(2),None,None),
    ("Fixed Expenses",hx.Float,"output",None,utils.thousands_format(0),None,None),
    ("Variable Expenses",hx.Float,"output",None,utils.percent_format(2),None,None),
    ("Investment Income",hx.Float,"output",None,utils.percent_format(2),None,None),
    ("Cost of RI",hx.Float,"output",None,utils.percent_format(2),None,None),
    ("Return On Capital",hx.Float,"output",None,utils.percent_format(2),None,None),
    ("Capital Cost",hx.Float,"output",None,utils.percent_format(2),None,None),
    ("Non-Modelled Perils NMP",hx.Float,"output",None,utils.percent_format(2),None,None),
    ("RI Rec",hx.Float,"output",None,utils.percent_format(2),None,None),

    ]
    return create_node_from_list(node_info_list) 

def _healthcare_cat_layers():

    node_info_list = [
        ("Gross Portfolio Size",hx.Float,"input",0,utils.thousands_format(0),None,None),
        ("Detachment",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Expected Cost in Layer Total",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Expected Cost in Layer Beazley Share",hx.Float,"output",None,utils.thousands_format(0),None,None),


    ]
    return create_node_from_list(node_info_list) 




