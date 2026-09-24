# As per Dimitri's requirements, This notes are added as static strings
requirement_notes = \
    """Requirement for uncertainty loading - Does the pricing warrant an additional uncertainty loading? 

    Areas of consideration:
    - If the pricing is a renewal, was there an uncertainy load applied in last years pricing and if so, does the rationale for the uncertainty load apply to this years pricing
    - If the facility being priced follows the main syndicate 2623/623 pricing; and if so is BST's exposure materially different to the main syndicate?
    """


quantity_notes = \
    """Data Quantity - This is intended to capture the volume of historical policy and claims data available for the Class of business(es) being priced. 

        For short-tailed classes, 5 years of data is considered sufficient for pricing
        For longer tailed classes, a minimum of 7 years of data is considered sufficient for pricing. 

        Note: Development periods between lines of businesses can differ depending on the tail of the risk. For shorter tailed classes this could be between 1-3 years, 5-8 years for longer tailed classes and 8+ years of very long tailed lines. 

        Selection
        1. Low - No data provided/Less than the required volume of data available
        2. Average - Reasonable volume of data provided 
        3. High - Several years of data provided exceeding the minimum to be considered sufficent
        """


quality_notes = \
    """Data Quality - This is intended to capture the adequacy of the data provided which may include the following:

        - The data is considered to be reflective of the portfolio of risks being underwritten in the prospective pricing period i.e. the risk profile is consistent. If a remediation strategy is in place fo the upcoming pricing period, the historical data should be easily adjustable to show the 'AS-IF' position of the dataset.
        - Where the data provided shows an 'AS-IF'd position, it is clear what factors have been applied to the data in order to appropriately compare the non-'AS IF'd data against the 'AS-IF'd dataset.
        - Where applicable, the in-scoping parameters should be easily identifiable in the dataset.
        - Risk code information should be clearly identifiable within the data, either at the individual policy level or risk code composition is provided ast the aggregate level, where lines of busineses are clearly linked to risk codes. 
        - Policy and claims data is provided at a granular level with individual claims mapped onto the respective premium vs aggregate premiums and losses by Year of Account.
        - Where large losses are observed in the experience, commentary is provided 
        - If the Facility is exposed to CAT events, CAT modelling has been provided either internally from the exposure management mean or externally from the broker/coverholder
        - Where the Facility being priced is a renewal, the data provided is reconcilable to last year's data provided.
        - Historical view of rate change is provided where applicable. 
        - Line size information is provided in terms of maximum for the facility and Beazley share by Class of Business/Risk Code. 

        Some areas of uncertainty within data quality may include the following: 
        - Data provided are summary tables with hardcoded figures vs files with calclulations preserved where the raw data can easily be traced and validated. 

        Selection
        1. Low - Both experience and exposure data are of poor quality.
        2. Average - Data is of reasonable quality 
        3. High - Data is excellent quality 
        """


new_or_existing_facility_notes = \
    """New or Existing Facility - This is intended to capture the degree of uncertainty associated with new business facilities considering whether the facility new business to 5623 or is this the first year of operation for the facility. Newer facilities are considered to carry more uncertainty when compared to established exisiting facilities due to the following:

        - The anticipated mix of business differing to the actual mix of business.
        - The uncertainty with attaining the actual forecasted premium due to low take-up rates
        - Uncertainty associated with additional brokers being on boarded onto the facility throughout the policy period with submission data not reflecting this

        Selection
        1. Brand new facility - Exotic - Aims to reflect uncertainty in relation to facilities writing risks for LOBs 5623 has little to no exposure
        2. Brand new facility - Standard - Aims to reflect uncertainty in relation to new facilities writing risks similar to those already written within 5623
        3. New business to Syndicate 5623 - Facility is not yet well-established in the market and there is some uncertainty in relation to the performance of the facility
        4. New business to Syndicate 5623 - Facility is well-established in the market and achieves targets year-on-year
        5. Renewal business - Uncertainty in relation to portfolio composition and how this is expected to move within prospective pricing period when compared to historical years i.e. changes in line size, portfolio mix and risk profile
        6. Renewal business - Portfolio composition is expected to remain broadly in line with prior year, therefore less uncertainty associated with the facility
        """


perf_volatility_notes = \
    """Performance Volatility - This considers the level of uncertainty reflected in facilties exposed to low frequency, high severity claims experience. Consideration should be taken as to whether any large loss loading implicity captures any uncertainty in relation to these types of risk. 

        Selection
        1. High volatility in claims experience
        2. Moderate volatility in claims experience
        3. Low volatility in claims experience
        """


reliance_on_ext_modelling_notes = \
    """Reliance on external modelling - This captures the uncertainty when pricing views are reliant on external information provided by the coveholder i.e. outputs from exposure rating model including expected loss ratio views.

        Selection
        1. High volatility in claims experience
        2. Moderate volatility in claims experience
        3. Low volatility in claims experience
        """


add_subjectivity_notes = \
    """Additional Subjectivity - This category intends to capture any additional uncertainty above and beyond what the other categories have captured. This should only be used in very rare cases where there is material uncertainty around the future performance of the account and must be documented why an additional subjectivity load has been selected.
        """


perf_discount_notes = \
    """Performance Discount - Where an uncertainty loading has been placed previously on a renewing account, how does the actual performance compare against expected performance? Where the actual performance is better than expected for the prior years and the uncertainty matrix has been populated consistently upon renewal, a reduction can be applied to the uncertainty load. We recommend a 1% discount for every year the account is renewed. A higher discount may be given upon renewal, however this must be clearly documented.
    
    Please refer to the BST Portfolio Dashboard in order to assess actual performance versus the historical priced-for loss ratio.
        """
