import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils
import data_schema.sch_params as sch_params


def sch_rating_summary(cds):
    cds.extend_node_rater_defined('cds/layers', {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        'bpi_case_priced': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'BPI (Case Priced)', 'format': percent_format(1)}),
        'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
        'premium_label': hx.Str(mode='output'),
        # Used for rate change calcs
        'quoted_premium_annualised': hx.Float(mode='output', async_input=["rarc_task"]),
        'benchmark_premium_annualised': hx.Float(mode='output', async_input=["rarc_task"]),
        "quoted_premium_case_priced": hx.Float(mode="input",default=0,view={"label":"Gross Quoted Premium","format":utils.thousands_format(0)})
    })

    