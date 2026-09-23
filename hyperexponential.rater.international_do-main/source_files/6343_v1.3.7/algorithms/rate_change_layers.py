import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio, usd, to_ccy, look_up
from operator import itemgetter
from algorithms.rate_constants import max_layers
from algorithms import parameter_tables_schema as params

def rate_change_layers(hxd):

    market_cap_2_year_high = hxd.cds.exposure.aggregate.market_cap_2_year_high or 0
    current_market_cap = hxd.cds.exposure.aggregate.current_market_cap or 0

    if hxd.cds.risk_information.mmp_flag is False:
        for i, layer in enumerate(hxd.cds.large_cap.layers):
            hxd.cds.layers[i].quoted_premium_100 = layer.quoted_premium_100 or 0
            hxd.cds.layers[i].quoted_premium_annual_100 = layer.quoted_premium_annual_100 or 0
            hxd.cds.layers[i].benchmark_premium_annual_100 = layer.benchmark_premium_annual_100 or 0
            hxd.cds.layers[i].limit = layer.limit or 0
            hxd.cds.layers[i].excess = layer.excess or 0
            hxd.cds.layers[i].deductible = layer.deductible or 0
            hxd.cds.layers[i].brokerage = layer.brokerage or 0
            hxd.cds.layers[i].written_line = layer.written_line or 0
            hxd.cds.layers[i].market_cap = max(market_cap_2_year_high, current_market_cap)
            hxd.cds.layers[i].total_assets = hxd.cds.exposure.aggregate.total_assets or 0
            hxd.cds.layers[i].insider_share = hxd.cds.exposure.aggregate.insider_shareholder_share or 0
            hxd.cds.layers[i].mmp_flag = hxd.cds.risk_information.mmp_flag
            hxd.cds.layers[i].currency = hxd.cds.currencies.source_currency or "USD"
            hxd.cds.layers[i].status = layer.status or None
            hxd.cds.layers[i].section_reference = layer.section_reference or None
            hxd.cds.layers[i].technical_premium = layer.technical_premium or 0
            hxd.cds.layers[i].benchmark_premium = layer.benchmark_premium or 0
            hxd.cds.layers[i].tpi = layer.tpi or 0
            hxd.cds.layers[i].bpi = layer.bpi or 0
            hxd.cds.layers[i].tpi_pre_uw_adj = layer.tpi_pre_uw_adj or 0
            hxd.cds.layers[i].bpi_pre_uw_adj = layer.bpi_pre_uw_adj or 0
            hxd.cds.layers[i].pflr = layer.pflr or 0
            hxd.cds.layers[i].pflr_pre_uw_adj = layer.pflr_pre_uw_adj or 0
            hxd.cds.layers[i].uw_adj_impact = layer.uw_adj_impact or 0
    else:
        hxd.cds.layers[0].quoted_premium_100 = hxd.cds.mmp.total.quoted_premium_100 or 0
        hxd.cds.layers[0].quoted_premium_annual_100 = hxd.cds.mmp.total.quoted_premium_annual_100 or 0
        hxd.cds.layers[0].benchmark_premium_annual_100 = hxd.cds.mmp.total.benchmark_premium_annual_100 or 0
        hxd.cds.layers[0].limit = hxd.cds.mmp.dno.limit or 0
        hxd.cds.layers[0].excess = hxd.cds.mmp.dno.excess or 0
        hxd.cds.layers[0].deductible = hxd.cds.mmp.dno.deductible or 0
        hxd.cds.layers[0].brokerage = hxd.cds.mmp.total.brokerage or 0
        hxd.cds.layers[0].written_line = hxd.cds.mmp.total.written_line or 0
        hxd.cds.layers[0].market_cap = max(market_cap_2_year_high, current_market_cap)
        hxd.cds.layers[0].total_assets = hxd.cds.exposure.aggregate.total_assets or 0
        hxd.cds.layers[0].insider_share = hxd.cds.exposure.aggregate.insider_shareholder_share or 0
        hxd.cds.layers[0].mmp_flag = hxd.cds.risk_information.mmp_flag
        hxd.cds.layers[0].number_employees = hxd.cds.exposure.aggregate.row_ftes or 0
        hxd.cds.layers[0].currency = hxd.cds.currencies.source_currency or "USD"
        hxd.cds.layers[0].status = hxd.cds.mmp.total.status or None
        hxd.cds.layers[0].section_reference = hxd.cds.mmp.total.section_reference or None
        hxd.cds.layers[0].technical_premium = hxd.cds.mmp.total.technical_premium or 0
        hxd.cds.layers[0].benchmark_premium = hxd.cds.mmp.total.benchmark_premium or 0
        hxd.cds.layers[0].tpi = hxd.cds.mmp.total.tpi or 0
        hxd.cds.layers[0].bpi = hxd.cds.mmp.total.bpi or 0



    return

