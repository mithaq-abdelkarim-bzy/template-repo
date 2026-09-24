# v0.5.0
import hx
from algorithms.rate_constants import max_layers, experience_rating_max_years
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict , max_coverages
from algorithms.model_profiler.profiling_hxd_functions import time_me

@time_me
def model_state(hxd):

    hxd.cds.risk_information.inception_year = hxd.hx_core.inception_date.year
    
    ms = hxd.model_state

    # save the record global variable in the snapshot for governance
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 56654 # For debugging in dev mode
    
    ms.coverage_use = RARC_COVERAGE_USE # Edit v0.3.0
    ms.insured_asset_use = RARC_INSURED_ASSET_USE # Edit v0.3.0

    ms.info_by_risk_bdx_exposure_prem = "Total Exposure per Layer is floored at 0"
    ms.info_by_include_swing_rates = "Must select only one of Swing Rates or Profit Commission"
    ms.info_by_include_pc = "Must select only one of Swing Rates or Profit Commission"

    
    # Controls which page to show and hide when the start renewal button is pressed
    # Only displays the landing page for policies which are a renewal
    if (expiring_policy_option_id is None) or (ms.pressed_start_renewal_task) or (ms.expiring_policy_option_id == expiring_policy_option_id):
        ms.show_landing_page = False
        ms.show_after_landing_page = True
        # NOTE USE the below for rate change
        # ms.show_rate_change = True

        ms.show_rate_change_layer_no_ia_use = hxd.cds.standard_fields.is_renewal and not RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE
        ms.show_rate_change_layer_ia_use = hxd.cds.standard_fields.is_renewal and not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE
        ms.show_rate_change_coverage_no_ia_use = hxd.cds.standard_fields.is_renewal and RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE
        ms.show_rate_change_coverage_ia_use = hxd.cds.standard_fields.is_renewal and RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE

    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False

        ms.show_rate_change = False
        
        ms.show_rate_change_layer_no_ia_use = False
        ms.show_rate_change_layer_ia_use = False
        ms.show_rate_change_coverage_no_ia_use = False
        ms.show_rate_change_coverage_ia_use = False


    if RARC_COVERAGE_USE: # EDIT v0.3.0
        num_coverages = len(coverages_dict)
        for cvg_index in range(1,max_coverages):
            setattr(hxd.cds.rate_change, f"show_coverage_{cvg_index}", True) if cvg_index <= num_coverages else False

    # set the shown_by value # Edit # v0.5.0
    ms.layer_no_ia_use = (RARC_COVERAGE_USE==False and RARC_INSURED_ASSET_USE == False)
    ms.layer_ia_use = (RARC_COVERAGE_USE==False and RARC_INSURED_ASSET_USE == True)
    ms.coverage_no_ia_use = (RARC_COVERAGE_USE==True and RARC_INSURED_ASSET_USE == False)
    ms.coverage_ia_use = (RARC_COVERAGE_USE==True and RARC_INSURED_ASSET_USE == True)


    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology != "Rater"

    # set the rater boolean for calculation
    ms.is_steer = hxd.cds.metadata.rater == "STEER"
    ms.is_clash = hxd.cds.metadata.rater == "Clash"
    ms.is_healthcare_cat = hxd.cds.metadata.rater == "Healthcare CAT"
    ms.is_not_clash = not ms.is_clash

    # set the rater boolean for ui display
    ms.show_steer = ms.is_steer and ms.show_after_landing_page and hxd.cds.standard_fields.rating_methodology == "Rater"
    ms.show_clash = ms.is_clash and ms.show_after_landing_page and hxd.cds.standard_fields.rating_methodology == "Rater"
    ms.show_healthcare_cat = ms.is_healthcare_cat and ms.show_after_landing_page and hxd.cds.standard_fields.rating_methodology == "Rater"
    ms.show_rater_priced = ms.show_after_landing_page and hxd.cds.standard_fields.is_rater_priced
    ms.show_case_priced = ms.show_after_landing_page and hxd.cds.standard_fields.is_case_priced

    if ms.is_steer:
        steer_model_state(hxd, ms)
    else:
        ms.show_steer_risk_bdx = False
        ms.show_steer_las_bdx = False
        ms.show_steer_experience_rating = False

    
    # Set bug report message (update rater name below, use dash for space)
    hxd.bug_report_email = """Please use the following email to report a bug or issue with the model and the support team will get back to you shortly.
    Please include the model name, a brief description of the issue, and the website link to the policy the issue relates to. 
    
    [RatingTeamDev@beazley](mailto:RatingTeamDev@beazley.com?subject=RATERNAME-Rater)"""
               

def steer_model_state(hxd, ms):

    ms.show_steer_experience_rating = ms.is_steer_experience_rating and ms.show_after_landing_page and hxd.cds.standard_fields.is_rater_priced
    ms.show_steer_risk_bdx = ms.is_steer_exposure_rating_risk_profil_bdx and ms.show_after_landing_page and hxd.cds.standard_fields.is_rater_priced
    ms.show_steer_las_bdx = ms.is_steer_exposure_rating_limit_average_severity = ms.show_steer_experience_rating and ms.show_steer_risk_bdx and hxd.cds.standard_fields.is_rater_priced

    hxd.cds.steer.experience_rating.on_levelling.raw_data_comment = "Upload data including the header. Please denote the policy year by 'Policy Year, 'Treaty Year', 'PY' or 'TY' in the header. If the column contains Date data format, please include 'Date' in the header description (e.g. Closed Date)"

    as_at_date = hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value
    fvy = hxd.cds.steer.experience_rating.other_fields.fvy.value
    lvy = hxd.cds.steer.experience_rating.other_fields.lvy.value
    
    lvy = as_at_date.year
    
    ms.is_steer_raw_data_not_validated = not ms.is_steer_raw_data_validated if ms.is_steer_raw_data_validated is not None else None

    hxd.cds.steer.experience_rating.other_fields.lvy.value = as_at_date.year
    
    # For layers not used in the pricing summary, the rate change and KPI Summary is hidden
    layers = hxd.cds.layers
    num_layers = len(layers)
    ms.show_layer_fgu = True
    for layer_index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{layer_index}", True) if layer_index <= num_layers else False
        setattr(ms, f"show_layer_{layer_index:02d}", True) if layer_index <= num_layers else False
    
    num_of_years = (lvy - fvy)+1 if lvy is not None and fvy is not None else 0

    if num_of_years >0:
        for dy_index in range(1,experience_rating_max_years+1):
            if dy_index >= (experience_rating_max_years + 1 - num_of_years):
                setattr(ms, f"show_data_year_{dy_index:02d}", True)  
            else:
                setattr(ms, f"show_data_year_{dy_index:02d}", False)  

    return


@time_me
def allow_policy_doc_download(hxd):
    layer = hxd.cds.layers[0]
    doc = hxd.policy_doc
        
    tp = layer.technical_premium_100 or 0
    bp = layer.benchmark_premium_100 or 0
    qp = layer.quoted_premium_100 or 0
    
    if bp <= 0:
        doc.premium_check = f"Benchmark Premium has not been calculated. Please fill in the relevant fields in to calculate premium."
        doc.show_premium_check = True
    elif tp <= 0:
        doc.premium_check = "Benchmark Premium has not been fully calculated. Please check the validation errors at the bottom right corner."
        doc.show_premium_check = True
    elif qp <= 0:
        doc.premium_check = "Quoted Premium should be greater than 0. Please input a valid number in Rating Summary."
        doc.show_premium_check = True
    else:
        doc.show_generate_button = True
            