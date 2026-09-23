import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
import datetime as date
from operator import itemgetter
from algorithms.rate_tech_eo import rate_tech_eo
from scipy.stats import gamma, poisson, lognorm, norm
from algorithms.rate_umbrella import rate_umbrella
from algorithms.timer import timer
from algorithms.rate_pricing_helpers import *

def rate_pricing(hxd):
    cds=hxd.cds
    fx_rates = params.fx_rates.df()

    show_hides_and_labels(hxd)
    
    # Schedule Mod Calclations
    if cds.gmm_masking == True:    
        variables = basic_inputs(hxd, "gmm")  
        schedule_mod_calculations(hxd, "gmm", variables)
    if cds.glsn_masking == True:
        variables = basic_inputs(hxd, "glsn") 
        schedule_mod_calculations(hxd, "glsn", variables)

    # Size Discount Calculation
    if cds.gmm_masking == True:
        size_discount_gmm(hxd, variables)
    if cds.glsn_masking == True:
        #glsn_size_discount = cds.rating_factors.glsn.size_discount_selection
        size_discount_glsn(hxd, variables)

    # Venue Factor
    variables["venue_factor"] = cds.exposure.aggregate.total_venue_factor

    # Ground Up Base Premium
    if cds.gmm_masking == True:
        gu_base_prem_gmm(hxd, variables)
    if cds.glsn_masking == True:
        gu_base_prem_glsn(hxd, variables)   

    for coverage in ["professional_liability","healthcare_professional_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability","product_recall","tech_eo_products_media","well_tech_eo_media"]:
        setattr(getattr(cds.rating_factors.pricing , coverage),"claims_basis","Claims-Made")
    
    # Premium Calculations (in USD)
    if cds.gmm_masking : 
        coverages = ["professional_liability","general_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability","tech_eo_products_media"]
        primary_layer_prem_calcs(hxd, "gmm", coverages, variables)
        primary_layer_prem_calcs_gmm(hxd, coverages, variables)
        options_dict = options_dict_gmm(hxd)
        rating_gmm(hxd, options_dict, variables)

    if cds.glsn_masking : 
        coverages = ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media"]
        primary_layer_prem_calcs(hxd, "glsn", coverages, variables)
        primary_layer_prem_calcs_glsn(hxd, variables)
        options_dict = options_dict_glsn(hxd)
        rating_glsn(hxd, options_dict, variables)

        
        
        