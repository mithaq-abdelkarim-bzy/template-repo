import hx
import pandas as pd
import numpy as np
from operator import itemgetter

from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_exposure_input import rate_exposure_input
from algorithms.rate_fine_art import rate_fine_art
from algorithms.rate_jewellers_block import rate_jewellers_block
from algorithms.rate_general_specie import rate_general_specie
from algorithms.rate_cash_in_transit import rate_cash_in_transit
from algorithms.rate_experience_rating import rate_experience_rating_bi, rate_experience_rating_manual
from algorithms.rate_final_selections_and_summary import rate_final_selections_and_summary
from algorithms.rate_rationale import rate_rationale
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_model_state import rate_model_state
from algorithms.rate_populate_fields import rate_validation_error
from algorithms.rate_show_page import rate_show_page
from algorithms.bi_intelligence import bi_intelligence_fetch,query_beazley_intelligence_database
from algorithms.rate_view_data_mapping import rate_view_data_mapping_inputs, rate_view_data_mapping_outputs
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs

@hx.rating
def rating_algorithm(hxd):
    # hxd.uat_prod_indicator = "uat"
    rate_view_data_mapping_inputs(hxd)
    rate_risk_information(hxd)
    df = rate_exposure_input(hxd)
    rate_fine_art(hxd, df)
    rate_jewellers_block(hxd, df)
    rate_general_specie(hxd, df)
    rate_cash_in_transit(hxd, df)
    rate_experience_rating_bi(hxd, df)
    rate_experience_rating_manual(hxd, df)
    rate_final_selections_and_summary(hxd, df)
    rate_rate_change(hxd)
    rate_rationale(hxd, df)
    rate_model_state(hxd)
    rate_validation_error(hxd)
    rate_show_page(hxd)
    rate_view_data_mapping_outputs(hxd)
    provision_bug_report_inputs_outputs(hxd)

    pass

