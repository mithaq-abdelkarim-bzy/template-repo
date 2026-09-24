import hx
import pandas as pd
import numpy as np
import math
import algorithms.rate_utilities as utils
from operator import itemgetter

def rate_risk_information(hxd):
    # Extracts database id for the risk information tab
    hxd.cds.database_id = hx.meta.policy_option_id

#### Benchmark Class ####
    df_uw_location = hx.params.table_input_underwriters

    # Pulls the location of the underwriter, which impacts the plan metrics
    if hxd.cds.standard_fields.underwriter is not None:
        uw_location = utils.look_up(hxd.cds.standard_fields.underwriter, "underwriter", "team", df_uw_location, "UK")
    else:
        uw_location = "UK"
        hx.errors.validation("Must select an Underwriter")
    hxd.cds.uw_location = uw_location

    # Sets the Benchmark Class for reporting
    if hxd.cds.standard_fields.underwriter is not None:
        if uw_location == "UK":
            hxd.cds.standard_fields.benchmark_class = "London D&O"
        else:
            hxd.cds.standard_fields.benchmark_class = "US D&O"

#### Broker dropdown ####
    # Broker dropdown changes whether UW is in London or US
    df_broker = hx.params.dd_broker
    location = "UK" if hxd.cds.uw_location == "London" else "US"

    filtered_df = df_broker[df_broker["BrokerLocation"] == uw_location]
    filtered_dict = filtered_df[["Broker"]].to_dict("records")

    broker_dropdown = sorted(filtered_dict, key=lambda x: itemgetter("Broker")(x).casefold())
    setattr(hxd.non_cds, "broker_dropdown", broker_dropdown)

    # Using the dropdown for US brokers as the Retail/Wholesale Broker dropdown ####
    us_filtered_df = df_broker[df_broker["BrokerLocation"] == "US"]
    us_filtered_dict = us_filtered_df[["Broker"]].to_dict("records")
    us_broker_dropdown = sorted(us_filtered_dict, key=lambda x: itemgetter("Broker")(x).casefold())
    setattr(hxd.non_cds, "us_broker_dropdown", us_broker_dropdown)

#### Coverage Selection ####
    # Sets booleans for displaying selected coverage
    is_abc = hxd.cds.coverage in ["ABC", None]
    hxd.cds.is_abc = is_abc
    hxd.cds.is_side_a = not is_abc

    # helps identify which type of rating methodology the rater is using. 
    methodology = hxd.cds.rating_methodology
    
    methodology_map = {
        "Public D&O": (True, False),
        "Private D&O": (False, True),
    }
    
    rp, pp = methodology_map.get(methodology, (False, False))
    hxd.cds.review_type.rater_priced = rp
    hxd.cds.review_type.private_priced = pp
    hxd.cds.standard_fields.is_rater_priced = rp
    
    if methodology == "Public D&O":
        hxd.cds.standard_fields.rating_methodology = "Rater"
    else:
        hxd.cds.standard_fields.rating_methodology = "Private D&O"
                
    
    # validaion to ensure the user put in market cap, assets, or rev
    agg_exposure = hxd.cds.exposure.aggregate
    exposure_values = (agg_exposure.market_cap, agg_exposure.total_assets, agg_exposure.net_sales)

    if all(value is None for value in exposure_values):
        hx.errors.validation("Enter at least one of Market Cap, Total Assets, or Revenue")

    #### Policy Form Dropdown ####
    df_forms = hx.params.coverage_form_options

    selected_coverage = hxd.cds.coverage

    if selected_coverage == "Side A":
        filtered_forms = df_forms[df_forms["type"] == "Side A"]
    else:
        filtered_forms = df_forms[df_forms["type"] != "Side A"]

    forms_dict = filtered_forms[["form"]].drop_duplicates().to_dict("records")

    policy_form_dropdown = sorted(forms_dict, key=itemgetter("form"))

    setattr(hxd.non_cds, "policy_form_dropdown", policy_form_dropdown)


#### Market Cap ####
    # Conditional formatting for mandatory field
    if hxd.cds.exposure.aggregate.market_cap is None:
        hxd.cds.market_cap_mandatory = True
        hx.errors.validation("Must enter the market cap")
    else:
        hxd.cds.market_cap_complete = True

    # Calculates the revised market cap
    # Handles the hovertext and validation
    setup_revised_market_cap(hxd.cds.exposure.aggregate)

#### Sectors ####
    ind = hxd.cds.key_industry
    dd_path = hxd.non_cds

    df_base_freq = hx.params.ref_base_frequencies
    df_sic = hx.params.ref_sic

    # The first sector is the main sector and is treated differently. Only this sector:
    #   1) Is used in admitted pricing
    #   2) Has a sector message displayed in a field rather than as hovertext
    #   3) Feeds into common fields in the cds

    # For the main sector, sets the SIC dropdown, calculates the base frequency, and sets the UW Message
    setup_sector(ind, dd_path, df_sic, df_base_freq, 1, ind.code_name)
    if ind.code_name is None:
        hxd.cds.sector_complete = False
    else:
        hxd.cds.sector_complete = True

    # Sets the SIC dropdown and calculates the base frequency for the other sectors
    # "Blended SIC" must be set to true
    if ind.blended_sic:
        setup_sector(ind, dd_path, df_sic, df_base_freq, 2, ind.sic_description_2)
        setup_sector(ind, dd_path, df_sic, df_base_freq, 3, ind.sic_description_3)
    
    # Sector validations
    if ind.blended_sic: 
        sector_percentages = [ind.sic_percentage, ind.sic_percentage_2, ind.sic_percentage_3]
        sic_desc = [ind.code_name, ind.sic_description_2, ind.sic_description_3]
    else:
        sector_percentages = [ind.sic_percentage]
        sic_desc = [ind.code_name]
    
    if not math.isclose(sum([perc for perc in sector_percentages if perc is not None]), 1, rel_tol=0.0001):
        hx.errors.validation("Sector allocations must sum to 1")
    if not all(perc is None for perc in sector_percentages):
        if (min([perc for perc in sector_percentages if perc is not None]) < 0) or (max([perc for perc in sector_percentages if perc is not None]) > 1):
                hx.errors.validation("Sector percentages must be between 0 and 1")  

    for perc, desc in zip(sector_percentages, sic_desc):
        if perc is not None and perc > 0 and desc is None:
            hx.errors.validation("Add sector description for sectors with percentage > 0")

#### Admitted Insurer ####
    hxd.cds.admitted.baic.is_california = True if hxd.cds.company_state == "California" else False

    hxd.cds.admitted.baic.is_california_not = not hxd.cds.admitted.baic.is_california



def setup_revised_market_cap(hxd_path):
    """
    Performs validations and checks on the market cap and insider share
    If okay, calculates the revised market cap in the hxd
    """
    # Setting info for TPI calc screen
    hxd_path.market_cap_info = "2 year market cap high, review live stock ticker as needed"
    hxd_path.insider_share_info = "Validate insider share % via an external resource. Ensure the total insider share is captured, not ONLY significant share holdings by directors and officers"
    
    if hxd_path.market_cap is not None:
        df_sca_freq_mod = hx.params.ref_sca_freq_modifiers

        # Market cap validation
        if hxd_path.market_cap < 1e6:
            hx.errors.validation("Market Cap must be greater than $1m")  
        else:
            if hxd_path.insider_share is not None:
                # Insider share validation  
                if (hxd_path.insider_share < 0) or (hxd_path.insider_share > 1):
                    hx.errors.validation("Insider Share must be between 0 and 1") 

                # Pulling revised market cap parameters
                insider_share_min = utils.look_up("InsiderShareMin", "ParameterName", "Value", df_sca_freq_mod, 0)
                insuder_share_rate = utils.look_up("InsiderShareRate", "ParameterName", "Value", df_sca_freq_mod, 0) 
                
                #Calculates revised market cap
                if hxd_path.insider_share >= insider_share_min:
                    hxd_path.revised_market_cap = hxd_path.market_cap*(1 - insuder_share_rate * hxd_path.insider_share)
                else: 
                    hxd_path.revised_market_cap = hxd_path.market_cap 

    # Setting total assets for display
    hxd_path.total_assets_output = hxd_path.total_assets
         


def setup_sector(hxd_path, hxd_dropdown, sic_dataframe, freq_dataframe, sector, sic):
    """
    Function that creates the SIC dropdown and looks up the base frequency
    Code is different for the first sector, as this in the main sector
    Looks up and displays the sector message for the main sector
    Adds the sector message as info for the other sectors
    """
    # Main sector
    if sector == 1:
        # SICs in dropdown depend on the sector
        # Sets the SIC dropdown
        hxd_dropdown.sic_dropdown = create_sic_dropdown(sic_dataframe)
        sector_name = get_sector_name(sic_dataframe, sic)
        hxd_path.sector_name = sector_name

        # Calculates base frequency
        hxd_path.sector_base_frequency = utils.look_up(sector_name, "Sector_Desc", "f5Adj", freq_dataframe, 0)

        # Sets sector id
        # This is used as an index for the sector in other functions
        hxd_path.sector_id = utils.look_up(sector_name, "Sector_Desc", "Sector", freq_dataframe, None) 

        # Looks up SIC Code from SIC description
        if sic is not None:
            hxd_path.code = utils.look_up(sic , "SICCombined", "SICCode", sic_dataframe, 0) 
            # Sets the sector message
            hxd_path.sector_message = utils.look_up(int(hxd_path.code), "SICCode", "UWMessage", sic_dataframe, "Not Found")
            hxd_path.sic_complete = True
        else: 
            hxd_path.sic_mandatory = True

    # All other sectors
    else:
        path = f"_{sector}"
        # Sets the SIC dropdown
        sic_dropdown = create_sic_dropdown(sic_dataframe)
        setattr(hxd_dropdown, "sic_dropdown" + path, sic_dropdown)

        #Sector name
        sector_name = get_sector_name(sic_dataframe, sic)
        setattr(hxd_path, "sector" + path, sector_name)

        # Calculates base frequency
        base_freq = utils.look_up(sector_name, "Sector_Desc", "f5Adj", freq_dataframe, 0)
        setattr(hxd_path, "sector_base_frequency" + path, base_freq)

        # Sets sector id
        sector_id = utils.look_up(sector_name, "Sector_Desc", "Sector", freq_dataframe, None)
        setattr(hxd_path, "sector_id" + path, sector_id)

        # Looks up SIC Code from SIC description
        if sic is not None:
            sic_code = utils.look_up(sic , "SICCombined", "SICCode", sic_dataframe, 0) 
            setattr(hxd_path, "sic_code" + path, sic_code)
            # Sets the sector message to be shown as hovertext
            sector_message = utils.look_up(int(sic_code), "SICCode", "UWMessage", sic_dataframe, "Not Found")
            setattr(hxd_path, "sector_message" + path, sector_message)



def create_sic_dropdown(sic_dataframe : pd.DataFrame):
    """
    Filters the SIC table by sector and returns the sorted list
    Table must have columns "SectorName" and "SICCombined"
    """
    filtered_df = sic_dataframe    

    filtered_dict = filtered_df[["SICCombined"]].to_dict("records")
    return sorted(filtered_dict, key=itemgetter("SICCombined"))

def get_sector_name(sic_dataframe, sic_combined):
    if sic_combined is None:
        return None
    else:
        filtered_df = sic_dataframe[sic_dataframe["SICCombined"] == sic_combined]
        sectorName = filtered_df["SectorName"].iloc[0]
        return sectorName


