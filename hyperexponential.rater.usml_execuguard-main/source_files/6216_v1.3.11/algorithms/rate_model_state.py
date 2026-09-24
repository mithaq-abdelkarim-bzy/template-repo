import hx
from algorithms import rate_constants as constants


def shownby_conditions_excess(hxd):
    # set out the conditional statements for the shownby tables in the view
    hxd.non_cds.coverage_elections.excess = (
        True
        if hxd.cds.layers[0].is_primary_excess
        == "Excess"
        else False
    )

    # set out the conditional statements for the shownby tables in the Rating Summary view
    if (
        (hxd.cds.layers[0].is_primary_excess == "Excess") # &
        # (hxd.cds.standard_fields.is_admitted_or_surplus == "Admitted") 
    ):
        hxd.cds.admitted_excess_local.is_policy_primary = False
    else: 
        hxd.cds.admitted_excess_local.is_policy_primary = True


#a validation function that catches some essential inputs to the model
def validation_functions_rating(hxd):
    validation_passed = True  # Flag to track validation status

    if hxd.cds.state is None:
        hx.errors.validation("No State has been chosen")
        validation_passed = False

    if hxd.cds.industry.naics_search is None:
        hx.errors.validation("No Industry has been chosen")
        validation_passed = False       

    return validation_passed  # Return False if validation failed, True otherwise


def set_dropdowns(hxd):
        #get the reactive state table
    reactive_zipcode_table = hx.params.table_zipcode
    #change the type of the ZIP column to a string for matching and display purposes
    reactive_zipcode_table['ZIP'] = reactive_zipcode_table['ZIP'].astype(str)

    #filter the reactive zipcode table to match the selected state 
    if hxd.cds.state:  # Check if hxd.cds.state is not empty
        filtered_reactive_zipcode = reactive_zipcode_table[
            reactive_zipcode_table["StateName"] == hxd.cds.state
        ]["ZIP"].values
    else:
        filtered_reactive_zipcode = []

    #populate the reactive zipcode list with the filtered values
    hxd.cds.reactive_zipcode.reactive_zipcode_list = [
        {"zipcode": item} for item in filtered_reactive_zipcode
    ]

    selected_zip_code = hxd.cds.reactive_zipcode.zipcode

    if selected_zip_code not in filtered_reactive_zipcode:
        hx.errors.validation("State selected does not belong to the selected zipcode")
    
    #set the county value based on the second dropdown
    matching_counties = reactive_zipcode_table[reactive_zipcode_table["ZIP"] == hxd.cds.reactive_zipcode.zipcode]["County"]
    if not matching_counties.empty:
        hxd.cds.county = matching_counties.iloc[0]
    else:
        hxd.cds.county = "No matching county found"    

    #get the reactive naics tables
    # new NAICS dropdown with descriptions, so need to set naics code back to just 6 digits
    naics_search = hxd.cds.industry.naics_search
    naics_key = naics_search[-6:] if naics_search else None
    hxd.cds.industry.naics_code = naics_key

    naics_table = hx.params.table_naics_master   
    filtered_naics_table = naics_table.loc[naics_table['NAICS Code'] == hxd.cds.industry.naics_code]
    
    if filtered_naics_table.empty:
        hxd.cds.industry.class_of_business = "No matching classification found"
        hxd.cds.industry.mapped_sic_code = "No SIC available"
    else:
        hxd.cds.industry.class_of_business = filtered_naics_table['tblBeazOccMap'].iloc[0]
        hxd.cds.industry.mapped_sic_code = filtered_naics_table['SIC_Code'].iloc[0]

    
    reactive_epl_industry_factors = hx.params.table_epl_industry_factors 
    filtered_epl_table = reactive_epl_industry_factors[reactive_epl_industry_factors["BeazleyOcc"] == hxd.cds.industry.class_of_business]

    if filtered_epl_table.empty:
        hxd.cds.industry.alert = "No matching classification found"
        hxd.cds.industry.wh_status = "No matching classification found"
        hxd.cds.industry.wh_information = "No matching classification found"
    else:
        hxd.cds.industry.alert = filtered_epl_table["Information"].iloc[0]
        hxd.cds.industry.wh_status = filtered_epl_table["WHStatus"].iloc[0]
        hxd.cds.industry.wh_information = filtered_epl_table["WHInformation"].iloc[0]

def model_state(hxd):

    ms = hxd.model_state
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    coverage_elections = hxd.cds.coverage_elections
    # expiring_policy_option_id = 56654 # For debugging in dev mode
    # setting the expiring policy ID for RC here
    if (hxd.cds.rate_change and hxd.cds.rate_change.expiring_policy_option_id):
        hxd.cds.rate_change.expiring_policy_option_id.calculated = ms.expiring_policy_option_id
    
    # Controls which page to show and hide when the start renewal button is pressed
    # Only displays the landing page for policies which are a renewal
    if (expiring_policy_option_id is None) or (ms.pressed_start_renewal_task) or (ms.expiring_policy_option_id == expiring_policy_option_id):
        ms.show_landing_page = False
        ms.show_after_landing_page = True
        ms.show_rate_change = hxd.cds.standard_fields.is_renewal
        hxd.non_cds.is_epl_inputs = coverage_elections.epl
        hxd.non_cds.is_pcl_inputs = coverage_elections.pcl
        hxd.non_cds.is_fid_inputs = coverage_elections.fid 
    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False
        ms.show_rate_change = False
        hxd.non_cds.is_epl_inputs = False
        hxd.non_cds.is_pcl_inputs = False
        hxd.non_cds.is_fid_inputs = False
        hxd.non_cds.coverage_elections.epl_pcl = False
        hxd.cds.conditions_met = False
    hxd.non_cds.quoted_premium_case_priced_label = "Gross Quoted Premium (Case Priced)"

    # For layers not used in the pricing summary, the rate change and KPI Summary is hidden
    # layers = hxd.cds.layers
    # num_layers = len(layers)
    # for index in range(1,constants.max_layers+1):
    #     setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False

        