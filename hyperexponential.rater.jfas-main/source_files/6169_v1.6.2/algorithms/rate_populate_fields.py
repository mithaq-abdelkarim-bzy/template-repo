import hx
import re

# SA: Should this file be called rate_validation_error?

def rate_validation_error(hxd):
    cds = hxd.cds
    layer = cds.layers[0]
    '''
    Populates validation error
    '''

    #hxd.policy_information.policy_level_validation = False
                

    # Policy level validation error
    if not cds.risk_info.insured_name_final:
        hx.errors.validation(f"Risk Information tab: Insured Name must be entered.")        
        hxd.cds.insured_name_selected = False
        hxd.cds.insured_name_not_selected = True
    else:
        hxd.cds.insured_name_selected = True
        hxd.cds.insured_name_not_selected = False
       
    if not cds.standard_fields.underwriter:
        hx.errors.validation(f"Risk Information tab: Underwriter must be entered.")
        hxd.cds.underwriter_selected = False
        hxd.cds.underwriter_not_selected = True
    else:
        hxd.cds.underwriter_selected = True
        hxd.cds.underwriter_not_selected = False

    if not cds.standard_fields.benchmark_class:
        hx.errors.validation(f"Risk Information tab: Class must be entered.")
        hxd.cds.risk_class_selected = False
        hxd.cds.risk_class_not_selected = True
    else:
        hxd.cds.risk_class_selected = True
        hxd.cds.risk_class_not_selected = False

    if layer.limit <= 0:
        hx.errors.validation(f"Final Selections tab: Limit must be greater than 0.")    
        hxd.cds.validation.limit.valid = False
        hxd.cds.validation.limit.invalid = True
    else:
        hxd.cds.validation.limit.valid = True
        hxd.cds.validation.limit.invalid = False
    
    if layer.excess < 0:
        hx.errors.validation(f"Final Selections tab: Excess cannot be below 0.")
        hxd.cds.validation.excess.valid = False
        hxd.cds.validation.excess.invalid = True        
    else:
        hxd.cds.validation.excess.valid = True
        hxd.cds.validation.excess.invalid = False


    if cds.final_premium_summary_table.acq_cost < 0:
        hx.errors.validation(f"Final Selections tab: Brokerage cannot be below zero.")
        hxd.cds.validation.brokerage.valid = False
        hxd.cds.validation.brokerage.invalid = True        
    else:
        hxd.cds.validation.brokerage.valid = True
        hxd.cds.validation.brokerage.invalid = False        

    if layer.quoted_premium < 0:
        hx.errors.validation(f"Final Selections tab: Quote premium cannot be below zero.")
        hxd.cds.validation.quoted_premium.valid = False
        hxd.cds.validation.quoted_premium.invalid = True        
    else:
        hxd.cds.validation.quoted_premium.valid = True
        hxd.cds.validation.quoted_premium.invalid = False        

    if cds.final_claims_summary_table.sel_exp_weight < 0:
        hx.errors.validation(f"Final Selections tab: Selected Experience Weight cannot be below zero.")
        hxd.cds.validation.sel_exp_weight.valid = False
        hxd.cds.validation.sel_exp_weight.invalid = True        
    else:
        hxd.cds.validation.sel_exp_weight.valid = True
        hxd.cds.validation.sel_exp_weight.invalid = False        

    
    if layer.quoted_premium == 0:
        hx.errors.validation(f"Final Selections tab: Quote premium must be entered.")
        hxd.cds.validation.quoted_premium.valid = False
        hxd.cds.validation.quoted_premium.invalid = True        
    else:
        hxd.cds.validation.quoted_premium.valid = True
        hxd.cds.validation.quoted_premium.invalid = False        

    if cds.final_premium_summary_table.signed_line == 0:
        hx.errors.validation(f"Final Selections tab: Signed line must be entered.")
        hxd.cds.validation.signed_line.valid = False
        hxd.cds.validation.signed_line.invalid = True        
    else:
        hxd.cds.validation.signed_line.valid = True
        hxd.cds.validation.signed_line.invalid = False    

    if layer.status != "Bound":
        hx.errors.validation(f"Risk Information tab: Deal Status must be set to bound to finalise policy.")
        hxd.cds.validation.status.valid = False
        hxd.cds.validation.status.invalid = True
    else:
        hxd.cds.validation.status.valid = True
        hxd.cds.validation.status.invalid = False

    # Matches reference
    reference_format = "......\d\d...."
    format_description = "6 char of any type, 2 digits and 4 chars of any type"

    if not re.fullmatch(reference_format, cds.standard_fields.policy_reference):
        hx.errors.validation(f"Risk Information tab: Reference must be in the format of {format_description}")
        hxd.cds.policy_reference_filled = False
        hxd.cds.policy_reference_not_filled = True
    else:
        hxd.cds.policy_reference_filled = True
        hxd.cds.policy_reference_not_filled = False
        #hxd.policy_information.policy_level_validation = True 

    # Assign value to written line to align with other raters
    cds.final_premium_summary_table.written_line = cds.final_premium_summary_table.signed_line   
        


    
