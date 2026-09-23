# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 10

benchmark_lr = 0.7




STATUS_GREEN = "\U0001F4D7"
STATUS_AMBER = "\U0001F4D2"
STATUS_RED = "\U0001F4D5"

RAG_STATUS = {
    "green": STATUS_GREEN,
    "amber": STATUS_AMBER,
    "red": STATUS_RED
}

# Climate Litigation Document
climate_ind_dropdown_dict = {
    "Australia": ["Consumer Products", "Financial Institutions", "Mining", "All Other Sectors", "Transport"],
    "France": ["Consumer Products", "Financial Institutions", "All Other Sectors", "Oil & Gas"],
    "Germany": ["Consumer Products", "Financial Institutions", "All Other Sectors", "Oil & Gas", "Transport"],
    "The Netherlands": ["Consumer Products", "Financial Institutions", "All Other Sectors", "Oil & Gas", "Transport"],
    "United Kingdom": ["Consumer Products", "Financial Institutions", "All Other Sectors", "Oil & Gas"],
}

climate_endpoint = (
                "https://beazley.sharepoint.com/sites/ClimateRisk/"
                "Shared Documents/"
                "4. Underwriting and Pricing/"
                "7. Specialty ESG Group/"
                "Climate Litigation Spotlight/"
                "Spotlight Drafts"
            )

climate_country_dict = {
    "Australia": "/Australia/Litigation Spotlight AUS_",
    "France": "/France/Litigation Spotlight France_",
    "Germany": "/Germany/Litigation Spotlight Germany_",
    "The Netherlands": "/The Netherlands/Litigation Spotlight Nlds_",
    "United Kingdom": "/United Kingdom/Litigation Spotlight UK_",
}

climate_industry_dict = {
    "Consumer Products": "Consumer_Products.docx",
    "Financial Institutions": "FI.docx",
    "Mining": "Mining.docx",
    "All Other Sectors": "Misc_Sectors.docx",
    "Oil & Gas": "Oil_Gas.docx",
    "Transport": "Transport.docx"
}