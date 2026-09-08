# show hide on tables must be contained within the respective lists & algorithms rather than here
# show hide on standard skeleton model characteristics is contained where they were coded


import hx
import pandas as pd
import numpy as np

def rate_show_hide(hxd):
    cds = hxd.cds

    ########################################################
    ### 1) Show Hide Defaults
    ########################################################
    cds.show_hide.page.show_exposure_detail         = False
    cds.show_hide.page.show_ihs                     = False
    cds.show_hide.page.show_rating_summary          = False
    cds.show_hide.page.show_rationale               = False
    cds.show_hide.page.show_actuarial               = False

    cds.show_hide.node.show_crcf                    = False
    cds.show_hide.node.show_cr_only                 = False
    cds.show_hide.node.show_political               = False
    cds.show_hide.node.show_pre_shipment_risk       = False
    cds.show_hide.node.show_pre_shipment_risk_not   = False
    cds.show_hide.node.show_hide_flat               = False 
    cds.show_hide.node.show_hide_flat_not           = False 
    cds.show_hide.node.show_hide_step               = False 

    ########################################################
    ### 2) Show Hide Rules - sheets
    ########################################################
    if hxd.model_state.show_after_landing_page:
        if cds.product !='':
            cds.show_hide.page.show_exposure_detail     = True
            cds.show_hide.page.show_ihs                 = True
            cds.show_hide.page.show_rating_summary      = True
            cds.show_hide.page.show_rationale           = True

            if (cds.rationale.actuarial_review in {'Yes'}):
                cds.show_hide.page.show_actuarial       = True


    ########################################################
    ### 2) Show Hide Rules - specific features
    ########################################################
    if (cds.product in {'Contract Frustration','Credit Risk'}):             cds.show_hide.node.show_crcf                    = True
    if (cds.product in {                       'Credit Risk'}):             cds.show_hide.node.show_cr_only                 = True
    if (cds.product in {'Political Risk'}):                                 cds.show_hide.node.show_political               = True
   
    if (cds.exposure.granular.crcf.pre_shipment_risk in {'Yes'}):           cds.show_hide.node.show_pre_shipment_risk       = True
    else:                                                                   cds.show_hide.node.show_pre_shipment_risk_not   = True
    
    if (cds.exposure.granular.crcf.load_amt_basis in {"Flat"}):             
        cds.show_hide.node.show_hide_flat               = True 
    else:
        cds.show_hide.node.show_hide_flat_not           = True 

    if (cds.exposure.granular.crcf.load_amt_basis in {"Step"}):             cds.show_hide.node.show_hide_step               = True 


    # if (crcf.load_show_hide==True and crcf.load_amt_basis == "Flat"):       cds.show_hide.node.show_hide_flat           = True 
    # if (crcf.load_show_hide==True and crcf.load_amt_basis == "Step")        cds.show_hide.node.show_hide_step           = True 

