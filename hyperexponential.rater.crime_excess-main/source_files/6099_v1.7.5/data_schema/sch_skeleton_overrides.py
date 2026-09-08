import hx

def sch_skeleton_overrides(cds):
    fields = {
        "cds/standard_fields/insured_country": {
           'mode':'output' 
        },
        "cds/admitted_excess/primary_limit/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/primary_retention/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/primary_premium/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/excess_limit/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/excess_attachment_point/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/no_of_policies_sharing_single_limit/value": {
           'mode':'output'            
        },
      "cds/admitted_excess/large_loss_potential/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/primary_rate_adequacy_correction/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/industry_sector_risk_level/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/industry_sector_factor/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/company_risk_level/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/company_factor/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/litigation_risk_level/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/litigation_factor/value": {
           'mode':'output'            
        },
        "cds/admitted_excess/fl_schedule_rating_factor/value": {
           'mode':'output'            
        }
    }

    for field, props in fields.items():
        cds.override_node_properties(field, props)

 

