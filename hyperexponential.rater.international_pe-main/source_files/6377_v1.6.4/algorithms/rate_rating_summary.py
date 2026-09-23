import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import ratio
from operator import itemgetter

def rate_rating_summary(hxd):



       
    # Use a for loop if your model prices multiple layers 
    for layer in hxd.cds.layers:        
        '''
        # NOTE: calculate the impact of UW adjustment by using Expected Loss Cost and Expected Loss Cost Pre UW Adjustment. 
        # Please stick to this method and do NOT use TP and TP pre UW adjustment for the calculation.

        The following expected loss is assumed to be the Beazley share. If the model requires the 100% line then 
        update calc using layer.written_line. 

        Currency will also need to be considered.

        '''
        layer.expected_loss_cost = 10000 # PLACEHOLDER (Beaz Share)
        layer.expected_loss_cost_pre_uw_adj = 9000 # PLACEHOLDER
        layer.uw_adj_impact = ratio(layer.expected_loss_cost, layer.expected_loss_cost_pre_uw_adj) - 1


    '''
    If there is only ever one layer, use the following code to work with the first element of the layer list without having to loop
    '''
    layer = hxd.cds.layers[0]
    layer.expected_loss_cost = 10000 # PLACEHOLDER (Beaz share)



