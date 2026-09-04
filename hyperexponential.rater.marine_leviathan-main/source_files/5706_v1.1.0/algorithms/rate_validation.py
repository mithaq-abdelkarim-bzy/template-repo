import hx
import pandas as pd
import numpy as np

def rate_validations(hxd):

    layer = hxd.cds.layers[0]

    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation(f"Insured name field must be completed.")

    # Validation check that brokerage is bound between 0 and 1
    if hxd.cds.brokerage < 0 :
        hx.errors.validation(f"Brokerage is negative")

    if hxd.cds.brokerage > 1 :
        hx.errors.validation(f"Brokerage above 100%")

    # Validation check that Beazley share is between between 0 and 1
    if hxd.cds.beazley_share < 0 :
        hx.errors.validation(f"Beazley share is negative")

    if hxd.cds.beazley_share > 1 :
        hx.errors.validation(f"Beazley share above 100%")
    
    # Validation to check how many layers are set as bound, also updates premium label for bound policies
    bound_count = 0
    for layer in hxd.cds.layers:
        if layer.status in ["Bound", "Post Bind Complete"]:
            bound_count += 1
            layer.premium_label = "Gross Bound Premium"
        else:
            layer.premium_label = "Gross Quoted Premium"
    
    if bound_count == 0:
        hx.errors.validation(f"Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final")
    elif bound_count > 1:
        hx.errors.validation(f"There must be only one bound policy")

    # If UW adjustment is applied then a comment must be added
    if hxd.cds.exposure.granular.uw_adjustment != 0 and hxd.cds.exposure.granular.uw_adjustment_rationale == "":
        hx.errors.validation(f"Please provide reason for Adjustment % in the Adjustment Rationale")

    # If Total Sum Insured entered by Number of Units zero
    if hxd.cds.exposure.granular.total_sum_insured.rov > 0 and hxd.cds.exposure.granular.number_of_units.rov == 0:
        hx.errors.validation(f"Number of units zero for ROV")

    if hxd.cds.exposure.granular.total_sum_insured.auv > 0 and hxd.cds.exposure.granular.number_of_units.auv == 0:
        hx.errors.validation(f"Number of units zero for AUV")
    
    if hxd.cds.exposure.granular.total_sum_insured.seismic_towed > 0 and hxd.cds.exposure.granular.number_of_units.seismic_towed == 0:
        hx.errors.validation(f"Number of units zero for Seismic-Towed")

    if hxd.cds.exposure.granular.total_sum_insured.seismic_ocean_bottom > 0 and hxd.cds.exposure.granular.number_of_units.seismic_ocean_bottom == 0:
        hx.errors.validation(f"Number of units zero for Seismic-Ocean Bottom")

    if hxd.cds.exposure.granular.total_sum_insured.diving_oceanographic > 0 and hxd.cds.exposure.granular.number_of_units.diving_oceanographic == 0:
        hx.errors.validation(f"Number of units zero for Diving & Oceanographic")

    if hxd.cds.exposure.granular.total_sum_insured.submersibles > 0 and hxd.cds.exposure.granular.number_of_units.submersibles == 0:
        hx.errors.validation(f"Number of units zero for Submersibles")

    if hxd.cds.exposure.granular.total_sum_insured.other > 0 and hxd.cds.exposure.granular.number_of_units.other == 0:
        hx.errors.validation(f"Number of units zero for Other")

    
    # If Number of Units entered but Total Sum Insured zero
    if hxd.cds.exposure.granular.number_of_units.rov > 0 and hxd.cds.exposure.granular.total_sum_insured.rov == 0:
        hx.errors.validation(f"Total Sum Insured zero for ROV")

    if hxd.cds.exposure.granular.number_of_units.auv > 0 and hxd.cds.exposure.granular.total_sum_insured.auv == 0:
        hx.errors.validation(f"Total Sum Insured zero for AUV")

    if hxd.cds.exposure.granular.number_of_units.seismic_towed > 0 and hxd.cds.exposure.granular.total_sum_insured.seismic_towed == 0:
        hx.errors.validation(f"Total Sum Insured zero for Seismic-Towed")

    if hxd.cds.exposure.granular.number_of_units.seismic_ocean_bottom > 0 and hxd.cds.exposure.granular.total_sum_insured.seismic_ocean_bottom == 0:
        hx.errors.validation(f"Total Sum Insured zero for Seismic-Ocean Bottom")

    if hxd.cds.exposure.granular.number_of_units.diving_oceanographic > 0 and hxd.cds.exposure.granular.total_sum_insured.diving_oceanographic == 0:
        hx.errors.validation(f"Total Sum Insured zero for Diving & Oceanographic")

    if hxd.cds.exposure.granular.number_of_units.submersibles > 0 and hxd.cds.exposure.granular.total_sum_insured.submersibles == 0:
        hx.errors.validation(f"Total Sum Insured zero for Submersibles")

    if hxd.cds.exposure.granular.number_of_units.other > 0 and hxd.cds.exposure.granular.total_sum_insured.other == 0:
        hx.errors.validation(f"Total Sum Insured zero for Other")

    # Validation if average sum insured is less than the excess
    if hxd.cds.exposure.granular.excess_per_loss.rov > hxd.cds.exposure.granular.average_sum_insured_per_unit.rov:
        hx.errors.validation(f"Excess per loss higher than the average sum insured for ROV")

    if (hxd.cds.exposure.granular.total_sum_insured.auv > 0 and hxd.cds.exposure.granular.excess_per_loss_auv.normal_ops > hxd.cds.exposure.granular.average_sum_insured_per_unit.auv) or (hxd.cds.exposure.granular.total_sum_insured.auv > 0 and hxd.cds.exposure.granular.excess_per_loss_auv.launch_recovery > hxd.cds.exposure.granular.average_sum_insured_per_unit.auv) :
        hx.errors.validation(f"Excess per loss higher than the average sum insured for AUV")
    
    if hxd.cds.exposure.granular.excess_per_loss.seismic_towed > hxd.cds.exposure.granular.average_sum_insured_per_unit.seismic_towed:
        hx.errors.validation(f"Excess per loss higher than the average sum insured for Seismic Towed")

    if hxd.cds.exposure.granular.excess_per_loss.seismic_ocean_bottom > hxd.cds.exposure.granular.average_sum_insured_per_unit.seismic_ocean_bottom:
        hx.errors.validation(f"Excess per loss higher than the average sum insured for Seismic Ocean Bottom") 

    if hxd.cds.exposure.granular.excess_per_loss.diving_oceanographic > hxd.cds.exposure.granular.average_sum_insured_per_unit.diving_oceanographic:
        hx.errors.validation(f"Excess per loss higher than the average sum insured for Diving & Oceanographic")   

    if hxd.cds.exposure.granular.excess_per_loss.submersibles > hxd.cds.exposure.granular.average_sum_insured_per_unit.submersibles:
        hx.errors.validation(f"Excess per loss higher than the average sum insured for Submersibles")

    if hxd.cds.exposure.granular.excess_per_loss.other > hxd.cds.exposure.granular.average_sum_insured_per_unit.other:
        hx.errors.validation(f"Excess per loss higher than the average sum insured for Other")  


    

    # If Status set to Bound but achieved premium is zero
    if hxd.cds.layers[0].status in ("Bound", "Post Bind Complete") and hxd.cds.layers[0].quoted_premium == 0:
        hx.errors.validation(f"Achieved Premium must be entered to mark a policy as final")

    #If Benchmark premium is negative
    if layer.benchmark_premium < 0 :
        hx.errors.validation(f"Benchmark premium is negative")
    
    #If Quoted premium is negative
    if layer.quoted_premium < 0 :
        hx.errors.validation(f"Quoted premium is negative")

    #If Quoted Case Premium premium is negative
    if layer.quoted_premium_net_case_priced < 0 :
        hx.errors.validation(f"Quoted premium is negative")
    
     #If BPI (Case Priced) is negative
    if layer.bpi < 0 :
        hx.errors.validation(f"BPI is negative") 

    #If Technical premium is negative
    if layer.technical_premium < 0:
         hx.errors.validation(f"Technical premium is negative")

