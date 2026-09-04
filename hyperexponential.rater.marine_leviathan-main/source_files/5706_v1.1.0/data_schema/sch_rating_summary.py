import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils

def thousands_format(mantissa=0):
    return{"thousandSeparated": True, "mantissa":mantissa}


def percent_format(mantissa=0):
    return{"output": "percent", "mantissa":mantissa}


def sch_rating_summary(cds):
    cds.extend_node_rater_defined('cds/layers', {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        'bpi_case_priced': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'BPI (Case Priced)', 'format': percent_format(1)}),
        'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
        'premium_label': hx.Str(mode='output'),
        # Used for rate change calcs
        'quoted_premium_annualised': hx.Float(mode='output', async_input=["rarc_task"]),
        'benchmark_premium_annualised': hx.Float(mode='output', async_input=["rarc_task"]),
        
        "benchmark_premium_net": hx.Float(mode="output", optionality="optional", view={"label": "Net Benchmark Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "prem_rate_benchmark_net": hx.Float(mode="output", view={"label": "Prem Rate (Net)", "format":{"output": "percent", "mantissa":3}}),
        "prem_rate_benchmark_gross": hx.Float(mode="output", view={"label": "Prem Rate (Gross)", "format":{"output": "percent", "mantissa":3}}),
        
        "quoted_premium_net": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Net brokerage", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "prem_rate_net": hx.Float(mode="output", view={"label": "Prem Rate (Net)", "format":{"output": "percent", "mantissa":3}}),
        "prem_rate_gross": hx.Float(mode="output", view={"label": "Prem Rate (Gross)", "format":{"output": "percent", "mantissa":3}}),
        "technical_premium_pre_uw_adj_net": hx.Float(mode="output", view={"label": "Net brokerage", "format": {"thousandSeparated": True, "mantissa": 0}}),
        
        "bpi_case_priced": hx.Float(mode="input", default=0, view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
        "quoted_premium_case_priced": hx.Float(mode="output",  view={"label": "Gross Achieved Premium (Case Priced)", "format": thousands_format()}),
        "quoted_premium_net_case_priced": hx.Float(mode="input", default=0, view={"label": "Net Achieved Premium (Case Priced)", "format": thousands_format()}),
        


        "net_kpi": hx.Structure(view={"label": "Net"}, children={

            "benchmark_premium": hx.Float(mode="output", view ={"label": "Benchmark Premium", "format": thousands_format(0)}),
            "benchmark_rate": hx.Float(mode="output", view ={"label": "Benchmark Rate", "format": {"output": "percent", "mantissa":3}}),

            "achieved_premium": hx.Float(mode="input", default=0, view ={"label": "Achieved Premium", "format": thousands_format(0)}),
            "achieved_rate": hx.Float(mode="output", view ={"label": "Achieved Rate", "format": {"output": "percent", "mantissa":3}}),
            
            "bpi_pre_uw_adj": hx.Float(mode="output", view ={"label": "BPI Pre UW Adj", "format": {"output": "percent", "mantissa":2}}),
            "bpi_post_uw_adj": hx.Float(mode="output", view ={"label": "BPI Post UW Adj", "format": {"output": "percent", "mantissa":2}}),
            "pflr": hx.Float(mode="output", view ={"label": "PFLR (Net)", "format": {"output": "percent", "mantissa":2}}), 

            "technical_premium": hx.Float(mode="output", view ={"label": "Technical Premium", "format": thousands_format(0)}),
            "tpi_pre_uw_adj": hx.Float(mode="output", view ={"label": "TPI Pre UW Adj", "format": {"output": "percent", "mantissa":2}}), 
            "tpi_post_uw_adj": hx.Float(mode="output", view ={"label": "TPI Post UW Adj", "format": {"output": "percent", "mantissa":2}}),          

            
    }),            

        "gross_kpi": hx.Structure(view={"label": "Gross"}, children={

            "benchmark_premium": hx.Float(mode="output", view ={"label": "Benchmark Premium", "format": thousands_format(0)}),
            "benchmark_rate": hx.Float(mode="output", view ={"label": "Benchmark Rate", "format": {"output": "percent", "mantissa":3}}),

            "achieved_premium": hx.Float(mode="output", view ={"label": "Achieved Premium", "format": thousands_format(0)}),
            "achieved_rate": hx.Float(mode="output", view ={"label": "Achieved Rate", "format": {"output": "percent", "mantissa":3}}),
            
            #"bpi_pre_uw_adj": hx.Float(mode="output", view ={"label": "BPI Pre UW Adj", "format": {"output": "percent", "mantissa":1}}),
            #"bpi_post_uw_adj": hx.Float(mode="output", view ={"label": "BPI Post UW Adj", "format": {"output": "percent", "mantissa":1}}),
            #"pflr": hx.Float(mode="output", view ={"label": "PFLR", "format": {"output": "percent", "mantissa":3}}), 

            #"technical_premium": hx.Float(mode="output", view ={"label": "Technical Premium", "format": thousands_format(0)}),
            #"tpi_pre_uw_adj": hx.Float(mode="output", view ={"label": "TPI Pre UW Adj", "format": {"output": "percent", "mantissa":1}}), 
            #"tpi_post_uw_adj": hx.Float(mode="output", view ={"label": "TPI Post UW Adj", "format": {"output": "percent", "mantissa":1}}),          

            
    }),                
       
    })


    