import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_z_global_parameters as z_global_parameters
from operator import itemgetter

def rate_general_specie(hxd, df):
    
    # 0. DECLARE PARAMETERS -------------------------------------------------------------------------
    df = df # data frame created from exposure input
    layer.gs_transit_relativity = z_global_parameters.gs_transit_relativity
    table_rating_gs = hx.params.table_rating_gs
    table_rating_exposure_curves = hx.params.table_rating_exposure_curves

    def gs_calculate_rate(rel, param_a, param_b, tsi):
        rate = rel * param_a * math.exp(math.log(tsi) * param_b) 
        return rate


    # 1. CALCULATE TSI ------------------------------------------------------------------------------

    # Generate summaries by premise
    # tsi_summary_usa = df[df["region"] == "USA"]["tsi_cnv"].sum()
    # tsi_summary_europe = df[df["region"] == "Europe"]["tsi_cnv"].sum()
    # tsi_summary_asia = df[df["region"] == "Asia"]["tsi_cnv"].sum()
    # tsi_summary_africa = df[df["region"] == "Africa"]["tsi_cnv"].sum()
    # tsi_summary_oceania = df[df["region"] == "Oceania"]["tsi_cnv"].sum()
    # tsi_summary_north_america = df[df["region"] == "North America"]["tsi_cnv"].sum()
    # tsi_summary_south_america = df[df["region"] == "South America"]["tsi_cnv"].sum()
    
    # TSI - STATIC
    cov.gs_static_metals_region_usa.tsi = df[(df["region"] == "USA") & (df["type"] == "Metals")]["tsi_cnv"].sum()
    cov.gs_static_metals_region_europe.tsi = df[(df["region"] == "Europe") & (df["type"] == "Metals")]["tsi_cnv"].sum()
    cov.gs_static_metals_region_asia.tsi = df[(df["region"] == "Asia") & (df["type"] == "Metals")]["tsi_cnv"].sum()
    cov.gs_static_metals_region_africa.tsi = df[(df["region"] == "Africa") & (df["type"] == "Metals")]["tsi_cnv"].sum()
    cov.gs_static_metals_region_oceania.tsi = df[(df["region"] == "Oceania") & (df["type"] == "Metals")]["tsi_cnv"].sum()
    cov.gs_static_metals_region_north_america.tsi = df[(df["region"] == "North America") & (df["type"] == "Metals")]["tsi_cnv"].sum()
    cov.gs_static_metals_region_south_america.tsi = df[(df["region"] == "South America") & (df["type"] == "Metals")]["tsi_cnv"].sum()
    
    cov.gs_static_cash_region_usa.tsi = df[(df["region"] == "USA") & (df["type"] == "Cash")]["tsi_cnv"].sum()
    cov.gs_static_cash_region_europe.tsi = df[(df["region"] == "Europe") & (df["type"] == "Cash")]["tsi_cnv"].sum()
    cov.gs_static_cash_region_asia.tsi = df[(df["region"] == "Asia") & (df["type"] == "Cash")]["tsi_cnv"].sum()
    cov.gs_static_cash_region_africa.tsi = df[(df["region"] == "Africa") & (df["type"] == "Cash")]["tsi_cnv"].sum()
    cov.gs_static_cash_region_oceania.tsi = df[(df["region"] == "Oceania") & (df["type"] == "Cash")]["tsi_cnv"].sum()
    cov.gs_static_cash_region_north_america.tsi = df[(df["region"] == "North America") & (df["type"] == "Cash")]["tsi_cnv"].sum()
    cov.gs_static_cash_region_south_america.tsi = df[(df["region"] == "South America") & (df["type"] == "Cash")]["tsi_cnv"].sum()
 
    cov.gs_static_securities_region_usa.tsi = df[(df["region"] == "USA") & (df["type"] == "Securities")]["tsi_cnv"].sum()
    cov.gs_static_securities_region_europe.tsi = df[(df["region"] == "Europe") & (df["type"] == "Securities")]["tsi_cnv"].sum()
    cov.gs_static_securities_region_asia.tsi = df[(df["region"] == "Asia") & (df["type"] == "Securities")]["tsi_cnv"].sum()
    cov.gs_static_securities_region_africa.tsi = df[(df["region"] == "Africa") & (df["type"] == "Securities")]["tsi_cnv"].sum()
    cov.gs_static_securities_region_oceania.tsi = df[(df["region"] == "Oceania") & (df["type"] == "Securities")]["tsi_cnv"].sum()
    cov.gs_static_securities_region_north_america.tsi = df[(df["region"] == "North America") & (df["type"] == "Securities")]["tsi_cnv"].sum()
    cov.gs_static_securities_region_south_america.tsi = df[(df["region"] == "South America") & (df["type"] == "Securities")]["tsi_cnv"].sum()
    
    
    
    # 2. GENERAL SPECIE SPECIFIC ------------------------------------------------------------------------------
    

    # LOOK UP RATES START --------------------------
    # STATIC - METAL
    metals_static_usa_param_a = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "USA") & (table_rating_gs["country"] == "USA")]["param_a"].iloc[0]
    metals_static_usa_param_b = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "USA") & (table_rating_gs["country"] == "USA")]["param_b"].iloc[0]
    metals_static_usa_relativ = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "USA") & (table_rating_gs["country"] == "USA")]["relativity"].iloc[0]
    
    metals_static_europe_param_a = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Europe")]["param_a"].iloc[0]
    metals_static_europe_param_b = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Europe")]["param_b"].iloc[0]
    metals_static_europe_relativ = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Europe")]["relativity"].iloc[0]
    
    metals_static_asia_param_a = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Asia")]["param_a"].iloc[0]
    metals_static_asia_param_b = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Asia")]["param_b"].iloc[0]
    metals_static_asia_relativ = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Asia")]["relativity"].iloc[0]
    
    metals_static_africa_param_a = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Africa")]["param_a"].iloc[0]
    metals_static_africa_param_b = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Africa")]["param_b"].iloc[0]
    metals_static_africa_relativ = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Africa")]["relativity"].iloc[0]

    metals_static_oceania_param_a = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Oceania")]["param_a"].iloc[0]
    metals_static_oceania_param_b = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Oceania")]["param_b"].iloc[0]
    metals_static_oceania_relativ = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "Oceania")]["relativity"].iloc[0]
    
    metals_static_north_america_param_a = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "North America") & (table_rating_gs["country"] != "USA")]["param_a"].iloc[0]
    metals_static_north_america_param_b = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "North America") & (table_rating_gs["country"] != "USA")]["param_b"].iloc[0]
    metals_static_north_america_relativ = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "North America") & (table_rating_gs["country"] != "USA")]["relativity"].iloc[0]
    
    metals_static_south_america_param_a = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "South America")]["param_a"].iloc[0]
    metals_static_south_america_param_b = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "South America")]["param_b"].iloc[0]
    metals_static_south_america_relativ = table_rating_gs[(table_rating_gs["type"] == "Metals") & (table_rating_gs["region"] == "South America")]["relativity"].iloc[0]
    
    # STATIC - CASH
    cash_static_usa_param_a = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "USA") & (table_rating_gs["country"] == "USA")]["param_a"].iloc[0]
    cash_static_usa_param_b = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "USA") & (table_rating_gs["country"] == "USA")]["param_b"].iloc[0]
    cash_static_usa_relativ = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "USA") & (table_rating_gs["country"] == "USA")]["relativity"].iloc[0]
    
    cash_static_europe_param_a = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Europe")]["param_a"].iloc[0]
    cash_static_europe_param_b = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Europe")]["param_b"].iloc[0]
    cash_static_europe_relativ = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Europe")]["relativity"].iloc[0]
    
    cash_static_asia_param_a = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Asia")]["param_a"].iloc[0]
    cash_static_asia_param_b = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Asia")]["param_b"].iloc[0]
    cash_static_asia_relativ = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Asia")]["relativity"].iloc[0]
    
    cash_static_africa_param_a = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Africa")]["param_a"].iloc[0]
    cash_static_africa_param_b = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Africa")]["param_b"].iloc[0]
    cash_static_africa_relativ = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Africa")]["relativity"].iloc[0]

    cash_static_oceania_param_a = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Oceania")]["param_a"].iloc[0]
    cash_static_oceania_param_b = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Oceania")]["param_b"].iloc[0]
    cash_static_oceania_relativ = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "Oceania")]["relativity"].iloc[0]
    
    cash_static_north_america_param_a = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "North America") & (table_rating_gs["country"] != "USA")]["param_a"].iloc[0]
    cash_static_north_america_param_b = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "North America") & (table_rating_gs["country"] != "USA")]["param_b"].iloc[0]
    cash_static_north_america_relativ = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "North America") & (table_rating_gs["country"] != "USA")]["relativity"].iloc[0]
    
    cash_static_south_america_param_a = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "South America")]["param_a"].iloc[0]
    cash_static_south_america_param_b = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "South America")]["param_b"].iloc[0]
    cash_static_south_america_relativ = table_rating_gs[(table_rating_gs["type"] == "Cash") & (table_rating_gs["region"] == "South America")]["relativity"].iloc[0]
    
    # STATIC - SECURITIES
    securities_static_usa_param_a = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "USA") & (table_rating_gs["country"] == "USA")]["param_a"].iloc[0]
    securities_static_usa_param_b = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "USA") & (table_rating_gs["country"] == "USA")]["param_b"].iloc[0]
    securities_static_usa_relativ = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "USA") & (table_rating_gs["country"] == "USA")]["relativity"].iloc[0]
    
    securities_static_europe_param_a = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Europe")]["param_a"].iloc[0]
    securities_static_europe_param_b = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Europe")]["param_b"].iloc[0]
    securities_static_europe_relativ = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Europe")]["relativity"].iloc[0]
    
    securities_static_asia_param_a = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Asia")]["param_a"].iloc[0]
    securities_static_asia_param_b = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Asia")]["param_b"].iloc[0]
    securities_static_asia_relativ = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Asia")]["relativity"].iloc[0]
    
    securities_static_africa_param_a = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Africa")]["param_a"].iloc[0]
    securities_static_africa_param_b = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Africa")]["param_b"].iloc[0]
    securities_static_africa_relativ = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Africa")]["relativity"].iloc[0]

    securities_static_oceania_param_a = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Oceania")]["param_a"].iloc[0]
    securities_static_oceania_param_b = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Oceania")]["param_b"].iloc[0]
    securities_static_oceania_relativ = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "Oceania")]["relativity"].iloc[0]
    
    securities_static_north_america_param_a = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "North America") & (table_rating_gs["country"] != "USA")]["param_a"].iloc[0]
    securities_static_north_america_param_b = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "North America") & (table_rating_gs["country"] != "USA")]["param_b"].iloc[0]
    securities_static_north_america_relativ = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "North America") & (table_rating_gs["country"] != "USA")]["relativity"].iloc[0]
    
    securities_static_south_america_param_a = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "South America")]["param_a"].iloc[0]
    securities_static_south_america_param_b = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "South America")]["param_b"].iloc[0]
    securities_static_south_america_relativ = table_rating_gs[(table_rating_gs["type"] == "Securities") & (table_rating_gs["region"] == "South America")]["relativity"].iloc[0]
    # LOOK UP RATES END --------------------------
    


    # CALCULATE RATE - START----------------------
    # STATIC
    # METALS
    if cov.gs_static_metals_region_usa.tsi > 0:
        cov.gs_static_metals_region_usa.rate = metals_static_usa_relativ * metals_static_usa_param_a * math.exp(math.log(cov.gs_static_metals_region_usa.tsi) * metals_static_usa_param_b)
    else:
        cov.gs_static_metals_region_usa.rate = 0
    
    if cov.gs_static_metals_region_europe.tsi > 0:
        cov.gs_static_metals_region_europe.rate = metals_static_europe_relativ * metals_static_europe_param_a * math.exp(math.log(cov.gs_static_metals_region_europe.tsi) * metals_static_europe_param_b)
    else:
        cov.gs_static_metals_region_europe.rate = 0
    
    if cov.gs_static_metals_region_asia.tsi > 0:
        cov.gs_static_metals_region_asia.rate = metals_static_asia_relativ * metals_static_asia_param_a * math.exp(math.log(cov.gs_static_metals_region_asia.tsi) * metals_static_asia_param_b)
    else:
        cov.gs_static_metals_region_asia.rate = 0
    
    if cov.gs_static_metals_region_africa.tsi > 0:
        cov.gs_static_metals_region_africa.rate = metals_static_africa_relativ * metals_static_africa_param_a * math.exp(math.log(cov.gs_static_metals_region_africa.tsi) * metals_static_africa_param_b)
    else:
        cov.gs_static_metals_region_africa.rate = 0
    
    if cov.gs_static_metals_region_oceania.tsi > 0:
        cov.gs_static_metals_region_oceania.rate = metals_static_oceania_relativ * metals_static_oceania_param_a * math.exp(math.log(cov.gs_static_metals_region_oceania.tsi) * metals_static_oceania_param_b)
    else:
        cov.gs_static_metals_region_oceania.rate = 0
    
    if cov.gs_static_metals_region_north_america.tsi > 0:
        cov.gs_static_metals_region_north_america.rate = metals_static_north_america_relativ * metals_static_north_america_param_a * math.exp(math.log(cov.gs_static_metals_region_north_america.tsi) * metals_static_north_america_param_b)
    else:
        cov.gs_static_metals_region_north_america.rate = 0
    
    if cov.gs_static_metals_region_south_america.tsi > 0:
        cov.gs_static_metals_region_south_america.rate = metals_static_south_america_relativ * metals_static_south_america_param_a * math.exp(math.log(cov.gs_static_metals_region_south_america.tsi) * metals_static_south_america_param_b)
    else:
        cov.gs_static_metals_region_south_america.rate = 0
    
    # CASH
    if cov.gs_static_cash_region_usa.tsi > 0:
        cov.gs_static_cash_region_usa.rate = cash_static_usa_relativ * cash_static_usa_param_a * math.exp(math.log(cov.gs_static_cash_region_usa.tsi) * cash_static_usa_param_b)
    else:
        cov.gs_static_cash_region_usa.rate = 0
    
    if cov.gs_static_cash_region_europe.tsi > 0:
        cov.gs_static_cash_region_europe.rate = cash_static_europe_relativ * cash_static_europe_param_a * math.exp(math.log(cov.gs_static_cash_region_europe.tsi) * cash_static_europe_param_b)
    else:
        cov.gs_static_cash_region_europe.rate = 0
    
    if cov.gs_static_cash_region_asia.tsi > 0:
        cov.gs_static_cash_region_asia.rate = cash_static_asia_relativ * cash_static_asia_param_a * math.exp(math.log(cov.gs_static_cash_region_asia.tsi) * cash_static_asia_param_b)
    else:
        cov.gs_static_cash_region_asia.rate = 0
    
    if cov.gs_static_cash_region_africa.tsi > 0:
        cov.gs_static_cash_region_africa.rate = cash_static_africa_relativ * cash_static_africa_param_a * math.exp(math.log(cov.gs_static_cash_region_africa.tsi) * cash_static_africa_param_b)
    else:
        cov.gs_static_cash_region_africa.rate = 0
    
    if cov.gs_static_cash_region_oceania.tsi > 0:
        cov.gs_static_cash_region_oceania.rate = cash_static_oceania_relativ * cash_static_oceania_param_a * math.exp(math.log(cov.gs_static_cash_region_oceania.tsi) * cash_static_oceania_param_b)
    else:
        cov.gs_static_cash_region_oceania.rate = 0
    
    if cov.gs_static_cash_region_north_america.tsi > 0:
        cov.gs_static_cash_region_north_america.rate = cash_static_north_america_relativ * cash_static_north_america_param_a * math.exp(math.log(cov.gs_static_cash_region_north_america.tsi) * cash_static_north_america_param_b)
    else:
        cov.gs_static_cash_region_north_america.rate = 0
    
    if cov.gs_static_cash_region_south_america.tsi > 0:
        cov.gs_static_cash_region_south_america.rate = cash_static_south_america_relativ * cash_static_south_america_param_a * math.exp(math.log(cov.gs_static_cash_region_south_america.tsi) * cash_static_south_america_param_b)
    else:
        cov.gs_static_cash_region_south_america.rate = 0
    
    
    # SECURITIES
    if cov.gs_static_securities_region_usa.tsi > 0:
        cov.gs_static_securities_region_usa.rate = securities_static_usa_relativ * securities_static_usa_param_a * math.exp(math.log(cov.gs_static_securities_region_usa.tsi) * securities_static_usa_param_b)
    else:
        cov.gs_static_securities_region_usa.rate = 0
    
    if cov.gs_static_securities_region_europe.tsi > 0:
        cov.gs_static_securities_region_europe.rate = securities_static_europe_relativ * securities_static_europe_param_a * math.exp(math.log(cov.gs_static_securities_region_europe.tsi) * securities_static_europe_param_b)
    else:
        cov.gs_static_securities_region_europe.rate = 0
    
    if cov.gs_static_securities_region_asia.tsi > 0:
        cov.gs_static_securities_region_asia.rate = securities_static_asia_relativ * securities_static_asia_param_a * math.exp(math.log(cov.gs_static_securities_region_asia.tsi) * securities_static_asia_param_b)
    else:
        cov.gs_static_securities_region_asia.rate = 0
    
    if cov.gs_static_securities_region_africa.tsi > 0:
        cov.gs_static_securities_region_africa.rate = securities_static_africa_relativ * securities_static_africa_param_a * math.exp(math.log(cov.gs_static_securities_region_africa.tsi) * securities_static_africa_param_b)
    else:
        cov.gs_static_securities_region_africa.rate = 0
    
    if cov.gs_static_securities_region_oceania.tsi > 0:
        cov.gs_static_securities_region_oceania.rate = securities_static_oceania_relativ * securities_static_oceania_param_a * math.exp(math.log(cov.gs_static_securities_region_oceania.tsi) * securities_static_oceania_param_b)
    else:
        cov.gs_static_securities_region_oceania.rate = 0
    
    if cov.gs_static_securities_region_north_america.tsi > 0:
        cov.gs_static_securities_region_north_america.rate = securities_static_north_america_relativ * securities_static_north_america_param_a * math.exp(math.log(cov.gs_static_securities_region_north_america.tsi) * securities_static_north_america_param_b)
    else:
        cov.gs_static_securities_region_north_america.rate = 0
    
    if cov.gs_static_securities_region_south_america.tsi > 0:
        cov.gs_static_securities_region_south_america.rate = securities_static_south_america_relativ * securities_static_south_america_param_a * math.exp(math.log(cov.gs_static_securities_region_south_america.tsi) * securities_static_south_america_param_b)
    else:
        cov.gs_static_securities_region_south_america.rate = 0
    
    

    
    # TRANSIT
    # METALS
    if cov.gs_transit_metals_region_usa.tsi > 0:
        cov.gs_transit_metals_region_usa.rate = gs_calculate_rate(metals_static_usa_relativ, metals_static_usa_param_a, metals_static_usa_param_b, cov.gs_transit_metals_region_usa.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_metals_region_europe.tsi > 0:
        cov.gs_transit_metals_region_europe.rate = gs_calculate_rate(metals_static_europe_relativ, metals_static_europe_param_a, metals_static_europe_param_b, cov.gs_transit_metals_region_europe.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_metals_region_asia.tsi > 0:
        cov.gs_transit_metals_region_asia.rate = gs_calculate_rate(metals_static_asia_relativ, metals_static_asia_param_a, metals_static_asia_param_b, cov.gs_transit_metals_region_asia.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_metals_region_africa.tsi > 0:
        cov.gs_transit_metals_region_africa.rate = gs_calculate_rate(metals_static_africa_relativ, metals_static_africa_param_a, metals_static_africa_param_b, cov.gs_transit_metals_region_africa.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_metals_region_oceania.tsi > 0:
        cov.gs_transit_metals_region_oceania.rate = gs_calculate_rate(metals_static_oceania_relativ, metals_static_oceania_param_a, metals_static_oceania_param_b, cov.gs_transit_metals_region_oceania.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_metals_region_north_america.tsi > 0:
        cov.gs_transit_metals_region_north_america.rate = gs_calculate_rate(metals_static_north_america_relativ, metals_static_north_america_param_a, metals_static_north_america_param_b, cov.gs_transit_metals_region_north_america.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_metals_region_south_america.tsi > 0:
        cov.gs_transit_metals_region_south_america.rate = gs_calculate_rate(metals_static_south_america_relativ, metals_static_south_america_param_a, metals_static_south_america_param_b, cov.gs_transit_metals_region_south_america.tsi) * layer.gs_transit_relativity
    
    
    # CASH
    if cov.gs_transit_cash_region_usa.tsi > 0:
        cov.gs_transit_cash_region_usa.rate = gs_calculate_rate(cash_static_usa_relativ, cash_static_usa_param_a, cash_static_usa_param_b, cov.gs_transit_cash_region_usa.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_cash_region_europe.tsi > 0:
        cov.gs_transit_cash_region_europe.rate = gs_calculate_rate(cash_static_europe_relativ, cash_static_europe_param_a, cash_static_europe_param_b, cov.gs_transit_cash_region_europe.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_cash_region_asia.tsi > 0:
        cov.gs_transit_cash_region_asia.rate = gs_calculate_rate(cash_static_asia_relativ, cash_static_asia_param_a, cash_static_asia_param_b, cov.gs_transit_cash_region_asia.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_cash_region_africa.tsi > 0:
        cov.gs_transit_cash_region_africa.rate = gs_calculate_rate(cash_static_africa_relativ, cash_static_africa_param_a, cash_static_africa_param_b, cov.gs_transit_cash_region_africa.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_cash_region_oceania.tsi > 0:
        cov.gs_transit_cash_region_oceania.rate = gs_calculate_rate(cash_static_oceania_relativ, cash_static_oceania_param_a, cash_static_oceania_param_b, cov.gs_transit_cash_region_oceania.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_cash_region_north_america.tsi > 0:
        cov.gs_transit_cash_region_north_america.rate = gs_calculate_rate(cash_static_north_america_relativ, cash_static_north_america_param_a, cash_static_north_america_param_b, cov.gs_transit_cash_region_north_america.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_cash_region_south_america.tsi > 0:
        cov.gs_transit_cash_region_south_america.rate = gs_calculate_rate(cash_static_south_america_relativ, cash_static_south_america_param_a, cash_static_south_america_param_b, cov.gs_transit_cash_region_south_america.tsi) * layer.gs_transit_relativity
    
    
    # CASH
    if cov.gs_transit_securities_region_usa.tsi > 0:
        cov.gs_transit_securities_region_usa.rate = gs_calculate_rate(securities_static_usa_relativ, securities_static_usa_param_a, securities_static_usa_param_b, cov.gs_transit_securities_region_usa.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_securities_region_europe.tsi > 0:
        cov.gs_transit_securities_region_europe.rate = gs_calculate_rate(securities_static_europe_relativ, securities_static_europe_param_a, securities_static_europe_param_b, cov.gs_transit_securities_region_europe.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_securities_region_asia.tsi > 0:
        cov.gs_transit_securities_region_asia.rate = gs_calculate_rate(securities_static_asia_relativ, securities_static_asia_param_a, securities_static_asia_param_b, cov.gs_transit_securities_region_asia.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_securities_region_africa.tsi > 0:
        cov.gs_transit_securities_region_africa.rate = gs_calculate_rate(securities_static_africa_relativ, securities_static_africa_param_a, securities_static_africa_param_b, cov.gs_transit_securities_region_africa.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_securities_region_oceania.tsi > 0:
        cov.gs_transit_securities_region_oceania.rate = gs_calculate_rate(securities_static_oceania_relativ, securities_static_oceania_param_a, securities_static_oceania_param_b, cov.gs_transit_securities_region_oceania.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_securities_region_north_america.tsi > 0:
        cov.gs_transit_securities_region_north_america.rate = gs_calculate_rate(securities_static_north_america_relativ, securities_static_north_america_param_a, securities_static_north_america_param_b, cov.gs_transit_securities_region_north_america.tsi) * layer.gs_transit_relativity
    
    if cov.gs_transit_securities_region_south_america.tsi > 0:
        cov.gs_transit_securities_region_south_america.rate = gs_calculate_rate(securities_static_south_america_relativ, securities_static_south_america_param_a, securities_static_south_america_param_b, cov.gs_transit_securities_region_south_america.tsi) * layer.gs_transit_relativity
    
    # CALCULATE RATE - END ----------------------



    # CALCULATE PREMIUM - START -----------------
    # STATIC
    # METAL
    cov.gs_static_metals_region_usa.premium = cov.gs_static_metals_region_usa.rate * cov.gs_static_metals_region_usa.tsi
    cov.gs_static_metals_region_europe.premium = cov.gs_static_metals_region_europe.rate * cov.gs_static_metals_region_europe.tsi
    cov.gs_static_metals_region_asia.premium = cov.gs_static_metals_region_asia.rate * cov.gs_static_metals_region_asia.tsi
    cov.gs_static_metals_region_africa.premium = cov.gs_static_metals_region_africa.rate * cov.gs_static_metals_region_africa.tsi
    cov.gs_static_metals_region_oceania.premium = cov.gs_static_metals_region_oceania.rate * cov.gs_static_metals_region_oceania.tsi
    cov.gs_static_metals_region_north_america.premium = cov.gs_static_metals_region_north_america.rate * cov.gs_static_metals_region_north_america.tsi
    cov.gs_static_metals_region_south_america.premium = cov.gs_static_metals_region_south_america.rate * cov.gs_static_metals_region_south_america.tsi
    # CASH
    cov.gs_static_cash_region_usa.premium = cov.gs_static_cash_region_usa.rate * cov.gs_static_cash_region_usa.tsi
    cov.gs_static_cash_region_europe.premium = cov.gs_static_cash_region_europe.rate * cov.gs_static_cash_region_europe.tsi
    cov.gs_static_cash_region_asia.premium = cov.gs_static_cash_region_asia.rate * cov.gs_static_cash_region_asia.tsi
    cov.gs_static_cash_region_africa.premium = cov.gs_static_cash_region_africa.rate * cov.gs_static_cash_region_africa.tsi
    cov.gs_static_cash_region_oceania.premium = cov.gs_static_cash_region_oceania.rate * cov.gs_static_cash_region_oceania.tsi
    cov.gs_static_cash_region_north_america.premium = cov.gs_static_cash_region_north_america.rate * cov.gs_static_cash_region_north_america.tsi
    cov.gs_static_cash_region_south_america.premium = cov.gs_static_cash_region_south_america.rate * cov.gs_static_cash_region_south_america.tsi
    # SECURITIES
    cov.gs_static_securities_region_usa.premium = cov.gs_static_securities_region_usa.rate * cov.gs_static_securities_region_usa.tsi
    cov.gs_static_securities_region_europe.premium = cov.gs_static_securities_region_europe.rate * cov.gs_static_securities_region_europe.tsi
    cov.gs_static_securities_region_asia.premium = cov.gs_static_securities_region_asia.rate * cov.gs_static_securities_region_asia.tsi
    cov.gs_static_securities_region_africa.premium = cov.gs_static_securities_region_africa.rate * cov.gs_static_securities_region_africa.tsi
    cov.gs_static_securities_region_oceania.premium = cov.gs_static_securities_region_oceania.rate * cov.gs_static_securities_region_oceania.tsi
    cov.gs_static_securities_region_north_america.premium = cov.gs_static_securities_region_north_america.rate * cov.gs_static_securities_region_north_america.tsi
    cov.gs_static_securities_region_south_america.premium = cov.gs_static_securities_region_south_america.rate * cov.gs_static_securities_region_south_america.tsi

    # TRANSIT
    # METAL
    if cov.gs_transit_metals_region_usa.tsi > 0:
        cov.gs_transit_metals_region_usa.premium = cov.gs_transit_metals_region_usa.rate * cov.gs_transit_metals_region_usa.tsi

    if cov.gs_transit_metals_region_europe.tsi > 0:
        cov.gs_transit_metals_region_europe.premium = cov.gs_transit_metals_region_europe.rate * cov.gs_transit_metals_region_europe.tsi

    if cov.gs_transit_metals_region_asia.tsi > 0:
        cov.gs_transit_metals_region_asia.premium = cov.gs_transit_metals_region_asia.rate * cov.gs_transit_metals_region_asia.tsi

    if cov.gs_transit_metals_region_africa.tsi > 0:
        cov.gs_transit_metals_region_africa.premium = cov.gs_transit_metals_region_africa.rate * cov.gs_transit_metals_region_africa.tsi

    if cov.gs_transit_metals_region_oceania.tsi > 0:
        cov.gs_transit_metals_region_oceania.premium = cov.gs_transit_metals_region_oceania.rate * cov.gs_transit_metals_region_oceania.tsi
         
    if cov.gs_transit_metals_region_north_america.tsi > 0:
         cov.gs_transit_metals_region_north_america.premium = cov.gs_transit_metals_region_north_america.rate * cov.gs_transit_metals_region_north_america.tsi
     
    if cov.gs_transit_metals_region_south_america.tsi > 0:
         cov.gs_transit_metals_region_south_america.premium = cov.gs_transit_metals_region_south_america.rate * cov.gs_transit_metals_region_south_america.tsi
     
    # CASH
    if cov.gs_transit_cash_region_usa.tsi > 0:
        cov.gs_transit_cash_region_usa.premium = cov.gs_transit_cash_region_usa.rate * cov.gs_transit_cash_region_usa.tsi

    if cov.gs_transit_cash_region_europe.tsi > 0:
        cov.gs_transit_cash_region_europe.premium = cov.gs_transit_cash_region_europe.rate * cov.gs_transit_cash_region_europe.tsi

    if cov.gs_transit_cash_region_asia.tsi > 0:
        cov.gs_transit_cash_region_asia.premium = cov.gs_transit_cash_region_asia.rate * cov.gs_transit_cash_region_asia.tsi

    if cov.gs_transit_cash_region_africa.tsi > 0:
        cov.gs_transit_cash_region_africa.premium = cov.gs_transit_cash_region_africa.rate * cov.gs_transit_cash_region_africa.tsi

    if cov.gs_transit_cash_region_oceania.tsi > 0:
        cov.gs_transit_cash_region_oceania.premium = cov.gs_transit_cash_region_oceania.rate * cov.gs_transit_cash_region_oceania.tsi
         
    if cov.gs_transit_cash_region_north_america.tsi > 0:
         cov.gs_transit_cash_region_north_america.premium = cov.gs_transit_cash_region_north_america.rate * cov.gs_transit_cash_region_north_america.tsi
     
    if cov.gs_transit_cash_region_south_america.tsi > 0:
         cov.gs_transit_cash_region_south_america.premium = cov.gs_transit_cash_region_south_america.rate * cov.gs_transit_cash_region_south_america.tsi
     
    # SECURITIES
    if cov.gs_transit_securities_region_usa.tsi > 0:
        cov.gs_transit_securities_region_usa.premium = cov.gs_transit_securities_region_usa.rate * cov.gs_transit_securities_region_usa.tsi

    if cov.gs_transit_securities_region_europe.tsi > 0:
        cov.gs_transit_securities_region_europe.premium = cov.gs_transit_securities_region_europe.rate * cov.gs_transit_securities_region_europe.tsi

    if cov.gs_transit_securities_region_asia.tsi > 0:
        cov.gs_transit_securities_region_asia.premium = cov.gs_transit_securities_region_asia.rate * cov.gs_transit_securities_region_asia.tsi

    if cov.gs_transit_securities_region_africa.tsi > 0:
        cov.gs_transit_securities_region_africa.premium = cov.gs_transit_securities_region_africa.rate * cov.gs_transit_securities_region_africa.tsi

    if cov.gs_transit_securities_region_oceania.tsi > 0:
        cov.gs_transit_securities_region_oceania.premium = cov.gs_transit_securities_region_oceania.rate * cov.gs_transit_securities_region_oceania.tsi
         
    if cov.gs_transit_securities_region_north_america.tsi > 0:
         cov.gs_transit_securities_region_north_america.premium = cov.gs_transit_securities_region_north_america.rate * cov.gs_transit_securities_region_north_america.tsi
     
    if cov.gs_transit_securities_region_south_america.tsi > 0:
         cov.gs_transit_securities_region_south_america.premium = cov.gs_transit_securities_region_south_america.rate * cov.gs_transit_securities_region_south_america.tsi
     
    # CALCULATE PREMIUM - END ------------------------------------------------------
    
    # SUMMARISE REGION TABLE - START ------------------------------------------------------
    # STATIC
    # STATIC - METAL
    cov.gs_static_metals_region_total.tsi = (
        cov.gs_static_metals_region_usa.tsi + 
        cov.gs_static_metals_region_europe.tsi + 
        cov.gs_static_metals_region_asia.tsi + 
        cov.gs_static_metals_region_africa.tsi + 
        cov.gs_static_metals_region_oceania.tsi + 
        cov.gs_static_metals_region_north_america.tsi + 
        cov.gs_static_metals_region_south_america.tsi
    )

    cov.gs_static_metals_region_total.premium = (
        cov.gs_static_metals_region_usa.premium + 
        cov.gs_static_metals_region_europe.premium + 
        cov.gs_static_metals_region_asia.premium + 
        cov.gs_static_metals_region_africa.premium + 
        cov.gs_static_metals_region_oceania.premium + 
        cov.gs_static_metals_region_north_america.premium + 
        cov.gs_static_metals_region_south_america.premium
    )

    if cov.gs_static_metals_region_total.tsi > 0:
        cov.gs_static_metals_region_total.rate = cov.gs_static_metals_region_total.premium / cov.gs_static_metals_region_total.tsi
    else:
        cov.gs_static_metals_region_total.rate

    # STATIC - CASH
    cov.gs_static_cash_region_total.tsi = (
        cov.gs_static_cash_region_usa.tsi + 
        cov.gs_static_cash_region_europe.tsi + 
        cov.gs_static_cash_region_asia.tsi + 
        cov.gs_static_cash_region_africa.tsi + 
        cov.gs_static_cash_region_oceania.tsi + 
        cov.gs_static_cash_region_north_america.tsi + 
        cov.gs_static_cash_region_south_america.tsi
    )

    cov.gs_static_cash_region_total.premium = (
        cov.gs_static_cash_region_usa.premium + 
        cov.gs_static_cash_region_europe.premium + 
        cov.gs_static_cash_region_asia.premium + 
        cov.gs_static_cash_region_africa.premium + 
        cov.gs_static_cash_region_oceania.premium + 
        cov.gs_static_cash_region_north_america.premium + 
        cov.gs_static_cash_region_south_america.premium
    )
    if cov.gs_static_cash_region_total.tsi > 0:
        cov.gs_static_cash_region_total.rate = cov.gs_static_cash_region_total.premium / cov.gs_static_cash_region_total.tsi
    else:
        cov.gs_static_cash_region_total.rate

    # STATIC - CASH
    cov.gs_static_securities_region_total.tsi = (
        cov.gs_static_securities_region_usa.tsi + 
        cov.gs_static_securities_region_europe.tsi + 
        cov.gs_static_securities_region_asia.tsi + 
        cov.gs_static_securities_region_africa.tsi + 
        cov.gs_static_securities_region_oceania.tsi + 
        cov.gs_static_securities_region_north_america.tsi + 
        cov.gs_static_securities_region_south_america.tsi
    )

    cov.gs_static_securities_region_total.premium = (
        cov.gs_static_securities_region_usa.premium + 
        cov.gs_static_securities_region_europe.premium + 
        cov.gs_static_securities_region_asia.premium + 
        cov.gs_static_securities_region_africa.premium + 
        cov.gs_static_securities_region_oceania.premium + 
        cov.gs_static_securities_region_north_america.premium + 
        cov.gs_static_securities_region_south_america.premium
    )

    if cov.gs_static_securities_region_total.tsi > 0:
        cov.gs_static_securities_region_total.rate = cov.gs_static_securities_region_total.premium / cov.gs_static_securities_region_total.tsi
    else:
        cov.gs_static_securities_region_total.tsi = 0
    
    # TRANSIT   
    # TRANSIT - METAL
    cov.gs_transit_metals_region_total.tsi = (
        cov.gs_transit_metals_region_usa.tsi + 
        cov.gs_transit_metals_region_europe.tsi + 
        cov.gs_transit_metals_region_asia.tsi + 
        cov.gs_transit_metals_region_africa.tsi + 
        cov.gs_transit_metals_region_oceania.tsi + 
        cov.gs_transit_metals_region_north_america.tsi + 
        cov.gs_transit_metals_region_south_america.tsi
    )

    if cov.gs_transit_metals_region_usa.premium is None:
        gs_transit_metals_region_usa_prem = 0
    else:
        gs_transit_metals_region_usa_prem = cov.gs_transit_metals_region_usa.premium

    if cov.gs_transit_metals_region_europe.premium is None:
        gs_transit_metals_region_europe_prem = 0
    else:
        gs_transit_metals_region_europe_prem = cov.gs_transit_metals_region_europe.premium

    if cov.gs_transit_metals_region_asia.premium is None:
        gs_transit_metals_region_asia_prem = 0
    else:
        gs_transit_metals_region_asia_prem = cov.gs_transit_metals_region_asia.premium

    if cov.gs_transit_metals_region_africa.premium is None:
        gs_transit_metals_region_africa_prem = 0
    else:
        gs_transit_metals_region_africa_prem = cov.gs_transit_metals_region_africa.premium

    if cov.gs_transit_metals_region_oceania.premium is None:
        gs_transit_metals_region_oceania_prem = 0
    else:
        gs_transit_metals_region_oceania_prem = cov.gs_transit_metals_region_oceania.premium

    if cov.gs_transit_metals_region_north_america.premium is None:
        gs_transit_metals_region_north_america_prem = 0
    else:
        gs_transit_metals_region_north_america_prem = cov.gs_transit_metals_region_north_america.premium

    if cov.gs_transit_metals_region_south_america.premium is None:
        gs_transit_metals_region_south_america_prem = 0
    else:
        gs_transit_metals_region_south_america_prem = cov.gs_transit_metals_region_south_america.premium


    cov.gs_transit_metals_region_total.premium = (
        gs_transit_metals_region_usa_prem + 
        gs_transit_metals_region_europe_prem +
        gs_transit_metals_region_asia_prem +
        gs_transit_metals_region_africa_prem +
        gs_transit_metals_region_oceania_prem +
        gs_transit_metals_region_north_america_prem +
        gs_transit_metals_region_south_america_prem
    )

    if cov.gs_transit_metals_region_total.premium > 0:
        cov.gs_transit_metals_region_total.rate = cov.gs_transit_metals_region_total.premium / cov.gs_transit_metals_region_total.tsi

    
    # TRANSIT - CASH
    cov.gs_transit_cash_region_total.tsi = (
        cov.gs_transit_cash_region_usa.tsi + 
        cov.gs_transit_cash_region_europe.tsi + 
        cov.gs_transit_cash_region_asia.tsi + 
        cov.gs_transit_cash_region_africa.tsi + 
        cov.gs_transit_cash_region_oceania.tsi + 
        cov.gs_transit_cash_region_north_america.tsi + 
        cov.gs_transit_cash_region_south_america.tsi
    )

    if cov.gs_transit_cash_region_usa.premium is None:
        gs_transit_cash_region_usa_prem = 0
    else:
        gs_transit_cash_region_usa_prem = cov.gs_transit_cash_region_usa.premium

    if cov.gs_transit_cash_region_europe.premium is None:
        gs_transit_cash_region_europe_prem = 0
    else:
        gs_transit_cash_region_europe_prem = cov.gs_transit_cash_region_europe.premium

    if cov.gs_transit_cash_region_asia.premium is None:
        gs_transit_cash_region_asia_prem = 0
    else:
        gs_transit_cash_region_asia_prem = cov.gs_transit_cash_region_asia.premium

    if cov.gs_transit_cash_region_africa.premium is None:
        gs_transit_cash_region_africa_prem = 0
    else:
        gs_transit_cash_region_africa_prem = cov.gs_transit_cash_region_africa.premium

    if cov.gs_transit_cash_region_oceania.premium is None:
        gs_transit_cash_region_oceania_prem = 0
    else:
        gs_transit_cash_region_oceania_prem = cov.gs_transit_cash_region_oceania.premium

    if cov.gs_transit_cash_region_north_america.premium is None:
        gs_transit_cash_region_north_america_prem = 0
    else:
        gs_transit_cash_region_north_america_prem = cov.gs_transit_cash_region_north_america.premium

    if cov.gs_transit_cash_region_south_america.premium is None:
        gs_transit_cash_region_south_america_prem = 0
    else:
        gs_transit_cash_region_south_america_prem = cov.gs_transit_cash_region_south_america.premium


    cov.gs_transit_cash_region_total.premium = (
        gs_transit_cash_region_usa_prem + 
        gs_transit_cash_region_europe_prem +
        gs_transit_cash_region_asia_prem +
        gs_transit_cash_region_africa_prem +
        gs_transit_cash_region_oceania_prem +
        gs_transit_cash_region_north_america_prem +
        gs_transit_cash_region_south_america_prem
    )

    if cov.gs_transit_cash_region_total.premium > 0:
        cov.gs_transit_cash_region_total.rate = cov.gs_transit_cash_region_total.premium / cov.gs_transit_cash_region_total.tsi

    
    # TRANSIT - CASH
    cov.gs_transit_securities_region_total.tsi = (
        cov.gs_transit_securities_region_usa.tsi + 
        cov.gs_transit_securities_region_europe.tsi + 
        cov.gs_transit_securities_region_asia.tsi + 
        cov.gs_transit_securities_region_africa.tsi + 
        cov.gs_transit_securities_region_oceania.tsi + 
        cov.gs_transit_securities_region_north_america.tsi + 
        cov.gs_transit_securities_region_south_america.tsi
    )

    if cov.gs_transit_securities_region_usa.premium is None:
        gs_transit_securities_region_usa_prem = 0
    else:
        gs_transit_securities_region_usa_prem = cov.gs_transit_securities_region_usa.premium

    if cov.gs_transit_securities_region_europe.premium is None:
        gs_transit_securities_region_europe_prem = 0
    else:
        gs_transit_securities_region_europe_prem = cov.gs_transit_securities_region_europe.premium

    if cov.gs_transit_securities_region_asia.premium is None:
        gs_transit_securities_region_asia_prem = 0
    else:
        gs_transit_securities_region_asia_prem = cov.gs_transit_securities_region_asia.premium

    if cov.gs_transit_securities_region_africa.premium is None:
        gs_transit_securities_region_africa_prem = 0
    else:
        gs_transit_securities_region_africa_prem = cov.gs_transit_securities_region_africa.premium

    if cov.gs_transit_securities_region_oceania.premium is None:
        gs_transit_securities_region_oceania_prem = 0
    else:
        gs_transit_securities_region_oceania_prem = cov.gs_transit_securities_region_oceania.premium

    if cov.gs_transit_securities_region_north_america.premium is None:
        gs_transit_securities_region_north_america_prem = 0
    else:
        gs_transit_securities_region_north_america_prem = cov.gs_transit_securities_region_north_america.premium

    if cov.gs_transit_securities_region_south_america.premium is None:
        gs_transit_securities_region_south_america_prem = 0
    else:
        gs_transit_securities_region_south_america_prem = cov.gs_transit_securities_region_south_america.premium


    cov.gs_transit_securities_region_total.premium = (
        gs_transit_securities_region_usa_prem + 
        gs_transit_securities_region_europe_prem +
        gs_transit_securities_region_asia_prem +
        gs_transit_securities_region_africa_prem +
        gs_transit_securities_region_oceania_prem +
        gs_transit_securities_region_north_america_prem +
        gs_transit_securities_region_south_america_prem
    )

    if cov.gs_transit_securities_region_total.premium > 0:
        cov.gs_transit_securities_region_total.rate = cov.gs_transit_securities_region_total.premium / cov.gs_transit_securities_region_total.tsi

  

    # 3. GENERAL SPECIE SUMMARY ------------------------------------------------------------------------------

    # TSI & Premium
    cov.gs_metals_summary.premium = cov.gs_static_metals_region_total.premium + cov.gs_transit_metals_region_total.premium
    cov.gs_cash_summary.premium = cov.gs_static_cash_region_total.premium + cov.gs_transit_cash_region_total.premium
    cov.gs_securities_summary.premium = cov.gs_static_securities_region_total.premium + cov.gs_transit_securities_region_total.premium
    
    cov.gs_metals_summary.tsi = cov.gs_static_metals_region_total.tsi + cov.gs_transit_metals_region_total.tsi
    cov.gs_cash_summary.tsi = cov.gs_static_cash_region_total.tsi + cov.gs_transit_cash_region_total.tsi
    cov.gs_securities_summary.tsi = cov.gs_static_securities_region_total.tsi + cov.gs_transit_securities_region_total.tsi

    # Credit
    # Metals
    if cov.gs_metals_summary.tsi > 0:
        if cov.gs_metals_summary.ded is None or cov.gs_metals_summary.ded is 0:
            ded_input_metals = cov.gs_metals_summary.ded_perc
            hxd.ded_input_metals_display = "Using deductible percentage"
        else:
            ded_input_metals = cov.gs_metals_summary.ded / cov.gs_metals_summary.tsi
            hxd.ded_input_metals_display = "Using deductible $ amount"
    else:
        ded_input_metals = 0
        hxd.ded_input_metals_display = "Select either $ or percent ded"
    
    gs_metals_exposure_curve = table_rating_exposure_curves[table_rating_exposure_curves["limded"] <= ded_input_metals]["gsmetals"].iloc[-1]
    cov.gs_metals_summary.credit = gs_metals_exposure_curve

    # cash
    if cov.gs_cash_summary.tsi > 0:
        if cov.gs_cash_summary.ded is None or cov.gs_cash_summary.ded is 0:
            ded_input_cash = cov.gs_cash_summary.ded_perc
            hxd.ded_input_cash_display = "Using deductible percentage"
        else:
            ded_input_cash = cov.gs_cash_summary.ded / cov.gs_cash_summary.tsi
            hxd.ded_input_cash_display = "Using deductible $ amount"
    else:
        ded_input_cash = 0
        hxd.ded_input_cash_display = "Select either $ or percent ded"
    
    gs_cash_exposure_curve = table_rating_exposure_curves[table_rating_exposure_curves["limded"] <= ded_input_cash]["gscash"].iloc[-1]
    cov.gs_cash_summary.credit = gs_cash_exposure_curve

    # Securities
    if cov.gs_securities_summary.tsi > 0:
        if cov.gs_securities_summary.ded is None or cov.gs_securities_summary.ded is 0:
            ded_input_securities = cov.gs_securities_summary.ded_perc
            hxd.ded_input_securities_display = "Using deductible percentage"
        else:
            ded_input_securities = cov.gs_securities_summary.ded / cov.gs_securities_summary.tsi
            hxd.ded_input_securities_display = "Using deductible $ amount"
    else:
        ded_input_securities = 0
        hxd.ded_input_securities_display = "Select either $ or percent ded"
    
    gs_securities_exposure_curve = table_rating_exposure_curves[table_rating_exposure_curves["limded"] <= ded_input_securities]["gssecurities"].iloc[-1]
    cov.gs_securities_summary.credit = gs_securities_exposure_curve

    # PREMIUM AND RATE POST DEDUCTIBLE
    # METALS 
    if cov.gs_metals_summary.uw_adj_impact is not None and cov.gs_metals_summary.uw_adj_impact > 0:
        cov.gs_metals_summary.prem_post_ded = cov.gs_metals_summary.premium * (1 - cov.gs_metals_summary.uw_adj_impact)
    else:
        cov.gs_metals_summary.prem_post_ded = cov.gs_metals_summary.premium * (1 - cov.gs_metals_summary.credit)

    if cov.gs_metals_summary.tsi is not None and cov.gs_metals_summary.tsi > 0:
        cov.gs_metals_summary.implied_rate_post_ded = cov.gs_metals_summary.prem_post_ded / cov.gs_metals_summary.tsi


    # CASH 
    if cov.gs_cash_summary.uw_adj_impact is not None and cov.gs_cash_summary.uw_adj_impact > 0:
        cov.gs_cash_summary.prem_post_ded = cov.gs_cash_summary.premium * (1 - cov.gs_cash_summary.uw_adj_impact)
    else:
        cov.gs_cash_summary.prem_post_ded = cov.gs_cash_summary.premium * (1 - cov.gs_cash_summary.credit)

    if cov.gs_cash_summary.tsi is not None and cov.gs_cash_summary.tsi > 0:
        cov.gs_cash_summary.implied_rate_post_ded = cov.gs_cash_summary.prem_post_ded / cov.gs_cash_summary.tsi


    # SECURITIES 
    if cov.gs_securities_summary.uw_adj_impact is not None and cov.gs_securities_summary.uw_adj_impact > 0:
        cov.gs_securities_summary.prem_post_ded = cov.gs_securities_summary.premium * (1 - cov.gs_securities_summary.uw_adj_impact)
    else:
        cov.gs_securities_summary.prem_post_ded = cov.gs_securities_summary.premium * (1 - cov.gs_securities_summary.credit)

    if cov.gs_securities_summary.tsi is not None and cov.gs_securities_summary.tsi > 0:
        cov.gs_securities_summary.implied_rate_post_ded = cov.gs_securities_summary.prem_post_ded / cov.gs_securities_summary.tsi




    pass