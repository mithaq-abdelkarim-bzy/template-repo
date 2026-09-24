import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter


def rate_risk_information(hxd):
    # Extracts database id for the risk information tab
    hxd.cds.database_id = hx.meta.policy_option_id
    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"
    
    #set these parameters for the admitted excess library
    #this been overriden in the sch_overrides file
    hxd.cds.standard_fields.insured_country = "USA"

    if hxd.cds.state is not None:        
        hxd.cds.standard_fields.insured_state_or_province = hxd.cds.state

    #turn off the coverages if the rater is set to Excess
    coverage = hxd.cds.coverage_elections
    if hxd.cds.layers[0].is_primary_excess == "Excess":
        hxd.non_cds.is_epl_inputs = False
        hxd.non_cds.is_pcl_inputs = False
        hxd.non_cds.is_fid_inputs = False

    #set the premium label for the top level premium
    if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus":
        hxd.non_cds.premium_label = "Surplus Premium"
    else:
        hxd.non_cds.premium_label = "Admitted Premium"     

        

     
    

    
    