##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################
###
##############################################################################################################################


import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides
import algorithms.rate_constants as const
from operator import itemgetter

def rate_claim_summary(hxd):

    cds = hxd.cds
    bi = cds.bi_data


   
    ####################################################################################
    ### 1) Get Claims Listing, Fx convert, Rank & Export basic exhibits              ###
    ####################################################################################

    #converting i) edm = raw data extracted from exposure mgmt; ii) ep_curve = what we want to visualise;   to dataframes
    claims_df = pd_df_from_hx_list(bi.claims_listing)
    policy_df = pd_df_from_hx_list(bi.facility_detail)
    if claims_df.shape[0] == 0 or (claims_df.shape[0]==1 and claims_df.yoa.iat[0]==None): 
        return


   ####################################################################################
    ### 2) Prepare Cat Event Exhibit                                                 ###
    ####################################################################################

    #group cat claims listing by event excluding block claims
    #1) take copy of df excluding non-cat
    cat_df          = claims_df[( claims_df.loss_category=="CAT") ].copy(    )

    #2) group by event and sort in place

    groupby_columns = ['beazley_catcode']
    calcby_columns  = ['bi_paid',   'bi_os',   'bi_incurred',   'pre_peer_blend_incurred',   'pre_peer_most_likely_incurred']  
    cat_df          = cat_df[  groupby_columns + calcby_columns  ].groupby(  groupby_columns  ).sum().reset_index()

    #3) add rank
    rankby_columns  = ['bi_incurred']
    cat_df['cat_tot_rank']  = cat_df[  rankby_columns  ].rank(method="first", ascending=False)

    sortby_columns  = ['cat_tot_rank']
    cat_df.sort_values(by=sortby_columns, inplace=True)
    max_rank        = const.default_num_rows
    #cat_df          = cat_df[    cat_df.cat_tot_rank <= max_rank  ]
    cat_df['show_row'] = np.where(cat_df.cat_tot_rank <= max_rank,   True,   False)
    

    #4) export
    output_columns  = sortby_columns + groupby_columns + calcby_columns + ['show_row']
    cat_df          = cat_df[cat_df.columns.intersection(output_columns)]
    setattr(cds.claim_summary,   "top15_cat_events",   cat_df.to_dict("records"))


    ####################################################################################
    ### 3) Prepare Freq/Sev Exhibit                                                  ###
    ####################################################################################

    #a) setup new df and add yoa
    fs_df                    = pd.DataFrame()
    incept_yoa               = hxd.hx_core.inception_date.year

    fs_df['yoa']             = [(incept_yoa - const.default_num_years + x) for x in range(const.default_num_years)]
    fs_df['yoa_label']       = fs_df['yoa'].astype(str)


    #b) source premium by year in appropriate fx
    fs_df['premium']         = [ ( policy_df[(policy_df.yoa == x) & policy_df.include  ]['gross_100pct_premium_sett_fx'].sum()) for x in fs_df.yoa]
    
    #b) get claim count by year from top 100 - criteria for frequency was if in top 100 att/large claims - could also do a non-nil claim count
    fs_df['frequency']       = [ ( claims_df[(claims_df.yoa == x) & claims_df.show_large  ]['exposure_reference'].count()) for x in fs_df.yoa]
    
    #c) get total loss by year from top 100
    fs_df['total_incurred']  = [ ( claims_df[(claims_df.yoa == x) & claims_df.show_large  ]['bi_incurred'].sum()) for x in fs_df.yoa]

    #d) calc freq per mille
    fs_df['freq_per_million']= np.where(fs_df.premium ==0,   0,   fs_df.frequency / fs_df.premium * 1e6)

    #e) calc average sev
    fs_df['severity']        = np.where(fs_df.frequency ==0,   0,   fs_df.total_incurred / fs_df.frequency)

    #f) determine show_row
    fs_df['show_row']        = np.where((fs_df.premium ==0) & (fs_df.frequency ==0),   False,   True)

    #g) export

    output_columns  = ['show_row','yoa','yoa_label','premium','freq_per_million','severity'] 
    fs_df           = fs_df[fs_df.columns.intersection(output_columns)]
    setattr(cds.claim_summary,   "chart_freq_sev",   fs_df.to_dict("records"))

    pass