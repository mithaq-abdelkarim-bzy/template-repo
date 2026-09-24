overall_note = \
    """Requirement for anti-selection charge - Does the pricing warrant an anti-selection charge? i.e. do we expect anti-selection to be present within this account?

    By default this should yes as there are rare circumstances where this is not applied
    """


baseline_note = \
    """Base Line - Intended to capture the 'base line' fundamental anti-selection risk that is not captured by the other rating factors below
    
    Selection
    1. Niche Contract (Focused on locally placed business [rather than wholesale] in specific targeted domiciles and classes)
    2. Standard Contract (Contract writing one or two lines of business, that are well within Beazley appetite, e.g. US Property or Marine)
    3. Large Cross Class Facility (Contract has multiple and materially varying lines of business)"""


competing_portfolio_note = \
    """Overarching structure and optionality with regards to competing portfolios - Intended to capture the potential and incentives for the coverholder [or related entities] to place \"attractive\" business in competing portfolios or equivalently to use this facility as a mechanism to place business that is otherwise difficult to place in the Market)
        
        Selection
        1. MGA (or any related entity) DOES NOT underwrite a competing portfolio outside of this Market Facility
        2. MGA (or any related entity) DOES underwrite a competing portfolio outside of this Market Facility
        3. Consortium where a competing portfolio IS NOT also underwritten by the Lead Underwriter
        4. Consortium where a competing portfolio IS also underwritten by the Lead Underwriter
        5. Coverholder is a part of a Broker Group"""


delegation_scope_note = \
    """Scope and degree of delegation - Intended to capture the degree to which the coverholder can anti-select or underwrite business outside of \"agreed\" parameters (set based on our risk appetite or leveraging the coverholder's specialist expertise / infrastructure / relationships)
        
        Selection
        1. Very Limited Scope (e.g. MGA / Coverholder must submit all information prior to writing a risk)
        2. Limited Scope (e.g. Lead Underwriter has reviewed and agreed coverholder's rating model, tight scope / guidelines)
        3. Average Scope (e.g. Coverholder can underwrite within specified parameters such as agreed Lloyd's risk codes, territories, max line sizes, etc.)
        4. Extensive Scope (e.g. Freedom to underwrite to very broad parameters)"""


quantity_quality_note = \
    """Data quality / quantity provided in submission - Intended to identify the asymmetry of data [both in terms of quantity and quality] as a proxy for potentially actively masking potential anti-selection issues or adverse performance on or within the portfolio.
    
    Selection
    1. Poor - Low quality and quantity of both experience and exposure data available
    2. Average - Reasonable quality and quantity of both experience and exposure data available
    3. Good - High quality and quantity of both experience and exposure data available"""


cover_holder_alignment_note = \
    """Degree to which Terms align coverholder and our interests - Intended to capture the degree to which the Terms align the coverholder's and insured's interest over a market cycle. 
    Examples of aligned interests include where:
    (I) PC constitutes a material proportion of overall brokerage/commission 
    (ii) PC is calculated using insured's overall performance rather than at a per-binder/per-class level 
    (iii) meaningful PC is not paid at levels where insured is loss-making, PC has a meaningful multi-year deficit clause that enables clawback following adverse experience 
    (iv) Good indexation by class of business, risk domicile and key rating factor (i.e. where indexation measures the 'take-up' of the 'in-scope business) such that the overall mix of business is closely aligned with the anticipated mix at prior renewal)
    
    Selection
    1. Poor - Negligible/No profit commission feature and poor indexation (such that overall mix of business is significantly different to the anticipated mix at prior renewal)
    2. Average - Profit Commission is a non-negligible component of the overall brokerage or commission (with a muti-year deficit clause that enables some clawback following adverse loss experience) and/or indexation is within acceptable parameters (such that the overall mix of business is broadly consistent with the anticipated mix at prior renewal)
    3. Good - Profit Commission is a large component of the overall brokerage or commission (with a muti-year deficit clause that enables meaningful clawback following adverse loss experience) and/or good indexation (such that overall mix of business closely aligns with the anticipated mix at prior renewal)"""


participation_note = \
    """Degree of differential participations from risk-to-risk - Intended to capture the degree to which varying participations can be used to anti-select.
    
    Selection
    1. Broadly flat written participations across all underlying risks written
    2. Varying participations across underlying risks written, but within reasonable parameters
    3. Significantly differing participations across underlying risks written"""
