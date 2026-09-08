#set all the unity prem valuess to 1/100%
import hx

def rate_unity_premium(hxd):
    hxd.cds.admitted_excess.primary_limit.value = hxd.cds.layers[0].limit
    hxd.cds.admitted_excess.primary_retention.value = hxd.cds.layers[0].excess
    hxd.cds.admitted_excess.primary_premium.value = hxd.cds.layers[0].premium
    hxd.cds.admitted_excess.excess_limit.value = hxd.cds.layers[hxd.beazley_layer_index].limit
    hxd.cds.admitted_excess.excess_attachment_point = hxd.cds.layers[hxd.beazley_layer_index].excess
    hxd.cds.admitted_excess.no_of_policies_sharing_single_limit.value = 1    


    hxd.cds.admitted_excess.large_loss_potential.value = "Average"
    hxd.cds.admitted_excess.primary_rate_adequacy_correction.value = 0  
    hxd.cds.admitted_excess.industry_sector_risk_level.value = "Normal Risk"  
    hxd.cds.admitted_excess.industry_sector_factor.value = 0
    hxd.cds.admitted_excess.company_risk_level.value = "Normal Risk"    
    hxd.cds.admitted_excess.company_factor.value = 0  
    hxd.cds.admitted_excess.litigation_risk_level.value = "Normal Risk"    
    hxd.cds.admitted_excess.litigation_factor.value = 0  
    hxd.cds.admitted_excess.fl_schedule_rating_factor.value = 0  

     
    

    # # testing purposes
    # hxd.cds.layers[0].unity_premium = 5e3 * hxd.cds.beazley_share
    # hxd.cds.layers[0].unity_premium_annual = 5e3

# "large_loss_potential",
# "primary_rate_adequacy_correction",
# "industry_sector_risk_level",
# "industry_sector_factor",
# "company_risk_level",
# "company_factor",
# "litigation_risk_level",
# "litigation_factor",
# "fl_schedule_rating_factor