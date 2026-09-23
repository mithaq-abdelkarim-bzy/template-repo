import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_constants import climate_ind_dropdown_dict


def update_climate_industry_dropdown(hxd):
    country = hxd.cds.risk_information.climate_document_country
    industries = climate_ind_dropdown_dict.get(country, [])

    hxd.cds.risk_information.climate_document_industry_options = [{}] * len(industries)
    for option_node, industry in zip(hxd.cds.risk_information.climate_document_industry_options, industries):
        option_node.industry = industry

    current_selection = hxd.cds.risk_information.climate_document_industry
    if current_selection and current_selection not in industries:
        hx.errors.validation(
            "Selected industry no longer matches the available options for the chosen country."
        )

def populate_infoby(hxd):
    hxd.cds.risk_information.climate_document_industry_infoby = "Sectors shown are identified as higher-risk in the selected jurisdiction. If a relevant industry is not shown, please select All Other Sectors for a sector agnostic report"

def rate_dashboard(hxd):
    populate_infoby(hxd)
    update_climate_industry_dropdown(hxd)
