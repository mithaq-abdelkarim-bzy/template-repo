import hx
from fuzzywuzzy import fuzz, process
import pandas as pd

def search_firm(hxd):
    '''
    Search firm with the given Firm Name input, uses contained search and return up to 10 results
    '''
    if not hxd.policy_information.insured_search.firmid_input and not hxd.policy_information.insured_search.firmname_input:
        return

    full_company_list = list(hx.params.firm.itertuples(index=False, name=None))

    search_result = []

    for firm in full_company_list:
        if len(search_result) == 10:
            break

        if hxd.policy_information.insured_search.firmname_input.upper() in firm[1].upper():
            search_result.append({"firm_id": firm[0], "firm_name": firm[1]})
    
    hxd.policy_information.insured_search.search_result = search_result


def import_firm(hxd):
    '''
    Import firm with the selected Insured Name, custom firmname will be imported instead if that exists
    '''

    # Import custom firm name if exist
    if custom_name := hxd.policy_information.insured_search.custom_firmname:
        hxd.policy_information.insured = custom_name
        return

    # Check only one firm name is selected
    if selected_count := (sum([result.selected for result in hxd.policy_information.insured_search.search_result]) != 1):
        hx.errors.fatal("Please select exactly 1 firm to import, or by overrding with custom firm name")
    else:
        firm_name = [result.firm_name for result in hxd.policy_information.insured_search.search_result if result.selected][0]
        hxd.policy_information.insured = firm_name