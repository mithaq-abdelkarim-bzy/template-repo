##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

###############################################################################################################################




import hx
import pandas as pd
import numpy as np
import math as math
import datetime
import algorithms.rate_utilities as utils
from operator import itemgetter


def rate_risk_information(hxd):
    # Extracts database id for the risk information tab
    hxd.cds.database_id = hx.meta.policy_option_id
    
    cds = hxd.cds
    
    # Determine which if any trifocus is valid
    tfg_df                       = hx.params.tb_tfgmappings
    cds.risk_info.trifocus_valid = (tfg_df[tfg_df["Trifocus"] == cds.standard_fields.trifocus].empty == False) or pd.isnull(cds.standard_fields.trifocus)
    selected_trifocus_str        = cds.risk_info.proxy_trifocus     if (cds.risk_info.trifocus_valid == False) else cds.standard_fields.trifocus

    
    # Mapping Department, BPMI, IBNR Group, Benchmark Class
    if selected_trifocus_str:
        trifocus_df_row                      = tfg_df[tfg_df["Trifocus"] == selected_trifocus_str]
        cds.risk_info.division               = trifocus_df_row["Division"].iloc[0]
        cds.risk_info.department             = trifocus_df_row["Department"].iloc[0]
        cds.risk_info.business_plan_mi_group = trifocus_df_row["Business Plan MI Group"].iloc[0]
        cds.risk_info.ibnr_group             = trifocus_df_row["Reserving Class"].iloc[0]
        cds.standard_fields.benchmark_class  = trifocus_df_row["Benchmark Class"].iloc[0]
        cds.risk_info.st_or_lt               = trifocus_df_row["ST/LT"].iloc[0]


    layer = hxd.cds.layers[0]
    
    # Calculating total deductions
    layer.total_deductions =(layer.ipt or 0) + (layer.commission or 0) + (layer.brokerage or 0)

    # Calculating AFB EPI (Net of Aqn, Gross of PC)
    if layer.quoted_premium_100pct and layer.total_deductions and layer.written_line:
        layer.quoted_premium = layer.quoted_premium_100pct * (1-layer.total_deductions) * layer.written_line

    # populating triangle_data_asat where available otherwise now()
    if (   (cds.triangle_projection.override_triangle) & (cds.triangle_projection.override_triangle_date is not None) ): 
        cds.risk_info.final_data_asat =  cds.triangle_projection.override_triangle_date
    elif (cds.risk_info.bic_data_asat): 
        cds.risk_info.final_data_asat =  cds.risk_info.bic_data_asat
    else:    
        cds.risk_info.final_data_asat =  hxd.hx_core.inception_date                 #JB PLACEHOLDER - ideally this would be the date the rating was started and fixed     



    pass
