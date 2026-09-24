# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio, usd, to_ccy, look_up
from operator import itemgetter

from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST

from algorithms import parameter_tables_schema as params

# NOTE: Define Global Variable for storing Renewing Insured Asset List
def define_insured_asset_list_variable(hxd):
    # This is only define when RARC_INSURED_ASSET_USE == True    
    HXD_INSURED_ASSET_LIST = {} 
    if RARC_INSURED_ASSET_USE and RARC_COVERAGE_USE:
        HXD_INSURED_ASSET_LIST = {
            f"{COVERAGES_LIST[0]}": hxd.cds.rate_change.insured_asset_list.example_coverage_1,
            f"{COVERAGES_LIST[1]}": hxd.cds.rate_change.insured_asset_list.example_coverage_2,
        }
    elif RARC_INSURED_ASSET_USE and not RARC_COVERAGE_USE:
        HXD_INSURED_ASSET_LIST = {
            "layers": hxd.cds.rate_change.insured_asset_list.layers,
        }
        print(HXD_INSURED_ASSET_LIST)
    return HXD_INSURED_ASSET_LIST

def save_insured_asset_list_for_rate_change(hxd):
    """
    This function is used when the calculation is done at an insured asset level. 
    It saves the insured asset list to a string node under cds/rate_change/insured_asset_list for future data manipulation in the rate change process. 
    """
    # Export insured asset list
    if RARC_COVERAGE_USE:
        for cvg in COVERAGES_LIST:
            hxd_cvg_insured_asset_list = getattr(hxd.cds.exposure.granular,cvg)
            exported_cvg_insured_asset_list = [
                {
                    "unique_id": ia.unique_id, 
                    "country": ia.country, 
                    "city": ia.city, 
                    "type": ia.type, 
                    "tiv": ia.tiv, 
                    "currency": ia.currency, 
                    "limit": ia.limit, 
                    "excess": ia.excess, 
                    "deductible": ia.deductible, 
                    "brokerage": ia.brokerage, 
                    "quoted_premium_net_100": ia.quoted_premium_net_100, 
                    "quoted_premium_100": ia.quoted_premium_100, 
                    "quoted_premium_annual_100": ia.quoted_premium_annual_100, 
                    "benchmark_premium_100": ia.benchmark_premium_100,
                    "benchmark_premium_pre_uw_adj": ia.benchmark_premium_pre_uw_adj, 
                    "benchmark_premium_annual_100": ia.benchmark_premium_annual_100, 
                    "technical_premium_100": ia.technical_premium_100,
                    "technical_premium_net_100": ia.technical_premium_net_100, 
                    "technical_premium_pre_uw_adj": ia.technical_premium_pre_uw_adj, 
                    "technical_premium_pre_uw_adj_100": ia.technical_premium_pre_uw_adj_100, 
                    "expected_loss_cost_100": ia.expected_loss_cost_100, 
                    "expected_loss_cost_pre_uw_adj": ia.expected_loss_cost_pre_uw_adj, 
                    "expected_loss_cost_pre_uw_adj_100": ia.expected_loss_cost_pre_uw_adj_100, 
                    "bpi": ia.bpi, 
                    "bpi_pre_uw_adj": ia.bpi_pre_uw_adj, 
                    "bpi_case_priced": ia.bpi_case_priced, 
                    "tpi": ia.tpi, 
                    "tpi_pre_uw_adj": ia.tpi_pre_uw_adj, 
                    "pflr": ia.pflr, 
                    "pflr_pre_uw_adj": ia.pflr_pre_uw_adj, 
                    "roc": ia.roc, 
                    "uw_adj_impact": ia.uw_adj_impact, 
                    "written_line": ia.written_line, 
                    "status": ia.status, 
                    ###### ----- Example for override ----- #####
                    # 
                    # "override_node": {
                    #     "calculated": ia.override_node.calculated,
                    #     "is_overridden": True,
                    #     "selected": ia.override_node.selected,
                    # },
                    ###### ----- Example for nested node ----- #####
                    # "nested_node": {"level_2": ia.level2.nested_node}, 
                    ###### ----- Exampl for date ----- #####
                    # "inception_date": date_to_string(ia.inception_date),
                }
                for ia in hxd_cvg_insured_asset_list
            ]
            # save the insured asset list in the Data Schema for future data transformation
            setattr(hxd.cds.rate_change.insured_asset_list,cvg,json.dumps(exported_cvg_insured_asset_list))
    else:
        hxd_insured_asset_list = hxd.cds.exposure.granular.layers

        exported_insured_asset_list = [
            {
                "unique_id": ia.unique_id, 
                "country": ia.country, 
                "city": ia.city, 
                "type": ia.type, 
                "tiv": ia.tiv, 
                "currency": ia.currency, 
                "limit": ia.limit, 
                "excess": ia.excess, 
                "deductible": ia.deductible, 
                "brokerage": ia.brokerage, 
                "quoted_premium_net_100": ia.quoted_premium_net_100, 
                "quoted_premium_100": ia.quoted_premium_100, 
                "quoted_premium_annual_100": ia.quoted_premium_annual_100, 
                "benchmark_premium_100": ia.benchmark_premium_100,
                "benchmark_premium_pre_uw_adj": ia.benchmark_premium_pre_uw_adj, 
                "benchmark_premium_annual_100": ia.benchmark_premium_annual_100, 
                "technical_premium_100": ia.technical_premium_100,
                "technical_premium_net_100": ia.technical_premium_net_100, 
                "technical_premium_pre_uw_adj": ia.technical_premium_pre_uw_adj, 
                "technical_premium_pre_uw_adj_100": ia.technical_premium_pre_uw_adj_100, 
                "expected_loss_cost_100": ia.expected_loss_cost_100, 
                "expected_loss_cost_pre_uw_adj": ia.expected_loss_cost_pre_uw_adj, 
                "expected_loss_cost_pre_uw_adj_100": ia.expected_loss_cost_pre_uw_adj_100, 
                "bpi": ia.bpi, 
                "bpi_pre_uw_adj": ia.bpi_pre_uw_adj, 
                "bpi_case_priced": ia.bpi_case_priced, 
                "tpi": ia.tpi, 
                "tpi_pre_uw_adj": ia.tpi_pre_uw_adj, 
                "pflr": ia.pflr, 
                "pflr_pre_uw_adj": ia.pflr_pre_uw_adj, 
                "roc": ia.roc, 
                "uw_adj_impact": ia.uw_adj_impact, 
                "written_line": ia.written_line, 
                "status": ia.status, 
                ###### ----- Example for override ----- #####
                # 
                # "override_node": {
                #     "calculated": ia.override_node.calculated,
                #     "is_overridden": True,
                #     "selected": ia.override_node.selected,
                # },
                ###### ----- Example for nested node ----- #####
                # "nested_node": {"level_2": ia.level2.nested_node}, 
                ###### ----- Exampl for date ----- #####
                    # "inception_date": date_to_string(ia.inception_date),
            } for ia in hxd_insured_asset_list
        ]
            # save the insured asset list in the Data Schema for future data transformation
        hxd.cds.rate_change.insured_asset_list.layers=json.dumps(exported_insured_asset_list)
