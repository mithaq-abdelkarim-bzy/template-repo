import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_pricing as rate
from algorithms import parameter_tables_schema as params

def historical_freq(hxd):
    ind = hxd.cds.key_industry
    sector = ind.sector_name
    mcap = 375e6 if hxd.cds.exposure.aggregate.revised_market_cap is None else hxd.cds.exposure.aggregate.revised_market_cap

    hxd.cds.sector_display = sector

    hxd.cds.linked_spreadsheet = "[Open Model Review Spreadsheet](https://beazley.sharepoint.com/:x:/r/sites/FSUPublicDO/_layouts/15/Doc.aspx?sourcedoc=%7BD6F6CF0E-4866-4EC6-A18B-B97D00996457%7D&file=Frequencies.xlsm&action=default&mobileredirect=true)"
    hxd.cds.table_explained = (
        "Base frequency is based on trends for companies with market capitalisation between $250-$500m\n" +
        "Market Cap (MC) frequency is based on frequency trends for the size of revised market cap on the ABC screen\n\n" +
        "The frequency numbers above may differ from the frequency shown on the ABC screen for the sector. Historic frequency is actual claims numbers, while the frequency pick may factor in projected future trends."
    )
    hxd.cds.graph_explained = "Number of Exposure and Claims for U.S. public listings, excluding ADR Listings at Level II and III, Chinese exposure, and IPOs filed in the last 3 years."

    # This filters the parameter table and converts it into the form to be written to the hxd
    if sector is not None:
        # Creating the Market Cap frequency adjustment
        mc_freq_adj = rate.calc_mcap_factor(
            "sca", 
            hx.params.ref_sca_freq_modifiers, 
            min(max(1, mcap), 999e9)
        )

        # Creating table
        df_hist_freq = hx.params.historical_freq
        df_hist_freq = df_hist_freq[df_hist_freq["GroupItem"] == sector] 
        
        # Extracting years from column headings
        years = list(df_hist_freq.columns.values)
        years = years[2:]

        # Splitting into a table for each group type
        df_claims = df_hist_freq[df_hist_freq["GroupType"] == "Claims"]
        df_exposure = df_hist_freq[df_hist_freq["GroupType"] == "Exposure"]
        df_base_freq = df_hist_freq[df_hist_freq["GroupType"] == "Base Frequency"]

        # Converts each table into a list
        claims = df_claims.values.flatten().tolist()
        claims = claims[2:]
        exposures = df_exposure.values.flatten().tolist()
        exposures = exposures[2:]
        base_freqs = df_base_freq.values.flatten().tolist()
        base_freqs = base_freqs[2:]

        # Calculates the market cap frequencies by applying the adjustment
        mc_freqs = [i * mc_freq_adj for i in base_freqs]

        # Combines the list into one dataframe and writes this into the hxd
        hist_freq_data = pd.DataFrame({
            "display_year": years, 
            "claims": claims,
            "exposure": exposures,
            "base_frequency" : base_freqs,
            "mc_frequency" : mc_freqs})

        utils.write_pd_to_hxd(
            hist_freq_data,
            hxd.cds.historical_freq,
            ["display_year", "claims", "exposure", "base_frequency", "mc_frequency"]
        )
