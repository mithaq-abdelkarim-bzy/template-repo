# v0.5.0
import hx
import datetime
import pandas as pd
from dataclasses import dataclass
max_layers = 11
benchmark_lr = 0.7
attritional_cap = 5000000

@dataclass
class credibility_params:
    num_claims_full_cred: int
    num_years_experience: int
    cred_based_on_years_experience: float
    cred_based_on_years_experience_nil_claims: float
    dampening_factor: float
    decay_treshold: float

def get_credibility_params(num_years_experience: int) -> credibility_params:
    df_cred_factors = hx.params.ref_tbl_cred_fac_years
    cp = credibility_params
    cp.num_claims_full_cred = 25
    cp.num_years_experience = num_years_experience
    cp.cred_based_on_years_experience = df_cred_factors[df_cred_factors["num_years_experience"] <= max(1,num_years_experience)]["pure_experience_cred_factor"].iloc[-1]
    cp.cred_based_on_years_experience_nil_claims =  df_cred_factors[df_cred_factors["num_years_experience"] <= max(1,num_years_experience)]["pure_experience_nil_claims"].iloc[-1]
    cp.dampening_factor = 0.97
    cp.decay_treshold = 5000000

    return cp

@dataclass
class base_params:
    mu_base_uk: float
    mu_base: float
    sigma_uk: float
    sigma: float
    mc_date: datetime.date
    dcaf: float
    dcop: float
    dcp1: float
    base_freq: float
    base_power_value: float
    base_ncp: float
    odf: float

def get_base_params(profession) -> base_params:
    """ profession = "lpl" or "aec" """
    df_base_params = hx.params.ref_lpl_base_params if profession == "lpl" else hx.params.ref_ae_base_params
    bp = base_params

    bp.mu_base = float(df_base_params[df_base_params["Parameter Name"]=="mu_base"]["Weighting"].iloc[0])
    bp.mu_base_uk = bp.mu_base if profession == "aec" else float(df_base_params[df_base_params["Parameter Name"]=="mu_base_uk"]["Weighting"].iloc[0])
    bp.sigma = float(df_base_params[df_base_params["Parameter Name"]=="sigma"]["Weighting"].iloc[0])
    bp.sigma_uk = bp.sigma if profession == "aec" else float(df_base_params[df_base_params["Parameter Name"]=="sigma_uk"]["Weighting"].iloc[0])
    bp.mc_date = pd.to_datetime(df_base_params[df_base_params["Parameter Name"]=="MC_Date"]["Weighting"].iloc[0]).date()
    bp.dcaf = float(df_base_params[df_base_params["Parameter Name"]=="DefenseCostAvFactor"]["Weighting"].iloc[0])
    bp.dcop = float(df_base_params[df_base_params["Parameter Name"]=="DefenseCostOnlyProportion"]["Weighting"].iloc[0])
    bp.dcp1 = float(df_base_params[df_base_params["Parameter Name"]=="DC_p1"]["Weighting"].iloc[0])
    bp.base_freq = float(df_base_params[df_base_params["Parameter Name"]=="FREQ"]["Weighting"].iloc[0])
    bp.base_power_value = float(df_base_params[df_base_params["Parameter Name"]=="PowerValue"]["Weighting"].iloc[0])
    bp.base_ncp = float(df_base_params[df_base_params["Parameter Name"]=="NCP"]["Weighting"].iloc[0])
    bp.odf =float(df_base_params[df_base_params["Parameter Name"]=="ODF"]["Weighting"].iloc[0])

    return bp

@dataclass
class tech_params:
    target_lr: float
    che: float
    fixed_expense: float
    variable_expense: float
    investment_income: float
    ri_cost: float
    roc: float
    capital_cost: float

def get_tech_params() -> tech_params:
    df_tp = hx.params.ref_tech_params
    tp = tech_params
    tp.target_lr = float(df_tp[df_tp["Component"]=="Target LR"]["London Professions"].iloc[0])
    tp.che = float(df_tp[df_tp["Component"]=="CHE"]["London Professions"].iloc[0])
    tp.fixed_expense = float(df_tp[df_tp["Component"]=="Fixed Expense"]["London Professions"].iloc[0])
    tp.variable_expense = float(df_tp[df_tp["Component"]=="Variable Expense"]["London Professions"].iloc[0])
    tp.investment_income = float(df_tp[df_tp["Component"]=="Investment Income"]["London Professions"].iloc[0])
    tp.ri_cost = float(df_tp[df_tp["Component"]=="RI Cost"]["London Professions"].iloc[0])
    tp.roc = float(df_tp[df_tp["Component"]=="ROC"]["London Professions"].iloc[0])
    tp.capital_cost = float(df_tp[df_tp["Component"]=="Capital Cost"]["London Professions"].iloc[0])

    return tp

def get_nmp_load() -> float:
    df = hx.params.ref_nmp_load
    return df.iloc[0,0]     # only 1 value

def get_fx_rate(ccy) -> float:
    df = hx.params.ref_tbl_fx_rates
    df_filtered = df[df["Code"]==ccy]
    if df_filtered is None or len(df_filtered) == 0:
        return 1
    else:
        return df_filtered["ToUSD"].iloc[0]

def get_fx_rate_base(ccy) -> float:
    df = hx.params.ref_tbl_fx_rates_base
    df_filtered = df[df["Code"]==ccy]
    if df_filtered is None or len(df_filtered) == 0:
        return 1
    else:
        return df_filtered["ToUSD"].iloc[0]

exposure_details_notes=(
    "**For the last 5 years plus the estimate for the year quoted, "
    "we need the best guess exposure data including acquisitions** "
    "unless acquisitions have limited prior acts cover, in which case we need "
    "those acquisitions exposure data back to their retro date or for the last 5 years, "
    "whichever is the more recent) **but excluding divestments and excluded entities**. "
    "The last 5 years data will affect both exposure and experience (burning cost) rating."
    "\n"
    "\n"
    "**The exposure data prior to 5 years ago should be the sum of that year's "
    "exposure data for all covered entities whose claims data you have.** "
    "You don't need to provide exposure data for years earlier than 5 years prior to the "
    "Policy Year."
    "\n"
    "If for a certain entity(ies) you have data back to a more recent year than the "
    "Policy Year, you will need to include that entity(ies) "
    "exposure data for the years where you have their claims data AND for 5 years prior to that. "
    "These years data will only affect experience (burning cost) rating, so if only require to match claims "
    "data for these years other than anything else."
)

territory_notes = (
    "•  Enter revenue and fee information in Risk info CCY"
    "\n"
    "•  Only input country and state-splits in the Policy Years available."
)

claims_notes = (
    "**Claims data needs to align with exposure data.** "
    "Unless there is less than 5 years of prior retro cover for some/all entities (see Exposure Details tab for more info), "
    "that means **we need claims data for all entities, including acquisitions but excluding divestments and excluded entities, going back 5 policy years,**"
    "then **prior to that** you include **claims and exposuure data for entities only where you have claims information for that entity for that year** (clean or otherwise)." 
)

client_details_notes= (
    "- Enter fee information in Risk Info Currency.\n"
    "- Only input project and AOP splits in the Policy Years available."
)

experience_notes= (
    "**Limitations**\n"
    "1) Experience rating does not allow for the Round The Clock (RTC) arrangements."
    "For insureds with RTC towers, these insureds will be priced as aggregate placements.\n\n"
    "2) Experience Rating will price all layers as Defence Costs inclusive, regardless of which option is selected for ‘Defence Costs in Addition’ in the Structure & Pricing tab. (N.B. Experience Rating will, however, take account of whether you select Yes or No to ‘Also applies to defence cost?’ for the retention)\n\n"
    "3) ILF implied Gross Benchmark Premium is used for information only for the high XS layers which lack claims in the past."
    "The limitation is that ILF only allows AOC limit, which does not allow aggregate."
)

retention_split_notes = (
    "**Retention Instructions:**\n"
    "If this risk requires split retentions, specify which region each level of split retention applies to. "
    "Otherwise only complete the first row. Users can enter varying currencies based on region."
)

def get_individual_countries():
    df = hx.params.ref_region_country
    return df

def get_individual_countries_count() -> int:
    df = hx.params.ref_region_country
    return len(df)

def get_territory_groups():
    df = hx.params.ref_ae_territory_loading
    return df["Territory"].tolist()

def get_states_count() -> int:
    df = hx.params.ref_states
    return len(df)

def get_aop_lawyers_count() -> int:
    df = hx.params.ref_lpl_aop_loading
    return len(df)

def get_aop_ae_count() -> int:
    df = hx.params.ref_ae_aop_loading
    return len(df)

territory_labels = {
    "united_kingdom": "United Kingdom",
    "australia": "Australia",
    "canada": "Canada (excl Quebec)",
    "quebec": "Quebec",
    "ireland": "Ireland",
    "united_states": "United States",
    "asia_pac_south_africa":"Asia Pac (Developed) & South Africa",
    "europe": "Europe (high risk)",
    "middle_east": "Middle East (high risk)",
    "tax_haven": "Tax Haven",
    "rest_of_world": "Rest of World (low risk)"
}

def get_inflation_tables(hxd):
    # Get Future Inflation
    df_ref_inflation = hx.params.ref_inflation
    future_inflation_exposure = df_ref_inflation[df_ref_inflation["Year"]=="Future"]["Revenue"].iloc[0]
    future_inflation_AE_claims_I = df_ref_inflation[df_ref_inflation["Year"]=="Future"]["A&E Claims"].iloc[0]
    future_inflation_lawyers_claims_I = df_ref_inflation[df_ref_inflation["Year"]=="Future"]["Lawyers Indemnity"].iloc[0]
    future_inflation_claims_D = df_ref_inflation[df_ref_inflation["Year"]=="Future"]["Lawyers Defence"].iloc[0]

    # Get effective date
    incept_date = hxd.hx_core.inception_date
    incept_year = incept_date.year
    effective_date = datetime.date(incept_year, 7, 1)

    def calc_index(df: pd.DataFrame, incept_year, inflation) -> pd.DataFrame:
        df["Index"] = pow((1 + inflation),(incept_year - df["Year"]))
        return df

    #Create the data frame
    df_I_exp = pd.DataFrame({
        "Year": range(incept_year - 1, incept_year - 1 - 31, -1)
    })
    df_I_aec = df_I_exp.copy()
    df_I_lc = df_I_exp.copy()
    df_I_cd = df_I_exp.copy()

    df_I_exp = calc_index(df_I_exp, incept_year, future_inflation_exposure)
    df_I_aec = calc_index(df_I_aec, incept_year, future_inflation_AE_claims_I)
    df_I_lc = calc_index(df_I_lc, incept_year, future_inflation_lawyers_claims_I)
    df_I_cd = calc_index(df_I_cd, incept_year, future_inflation_claims_D)

    return {
        "df_I_exp": df_I_exp,
        "df_I_aec": df_I_aec,
        "df_I_lc": df_I_lc,
        "df_I_cd": df_I_cd
    }

def units_to_convert(hxd):
    utv = hxd.cds.experience_rating.units_to_view
    if utv == "Per Billion":
        x = 1e9
    elif utv == "Per Million":
        x = 1e6
    elif utv == "Per Thousand":
        x = 1e3
    else:
        x = 1

    return x


project_type_map = {
    "airport_runways":{"label":"Airport Runways", "type": "input", "parent": ""},
    "arenas_stadiums_convention_centers":{"label": "Arenas/Stadiums/Convention Centers", "type": "input", "parent": ""},
    "bridges_tunnels":{"label": "Bridges/Tunnels", "type": "input", "parent": ""},
    "chemical_pharmaceutical_plants":{"label": "Chemical/Pharmaceutical plants", "type": "input", "parent": ""},
    "dams_harbours_jetties_wetland_mitigation":{"label": "Dams, Harbours & Jetties/Wetland Mitigation", "type": "input", "parent": ""},
    "hospitals":{"label": "Hospitals", "type": "input", "parent": ""},
    "mining":{"label": "Mining", "type": "input", "parent": ""},
    "modular_buildings":{"label": "Modular Buildings (involving repetitive design)", "type": "input", "parent": ""},
    "oil_refineries_pipelines_powerplants":{"label": "Oil Refineries/Pipelines/Power Plants", "type": "input", "parent": ""},
    "parking_garages":{"label": "Parking Garages", "type": "input", "parent": ""},
    "processing_treatment":{"label": "Processing and treatment (Water/Sludge/Waste etc.)", "type": "input", "parent": ""},
    "residential_buildings_high_rise":{"label": "Residential Buildings (high rise - over 3 storeys)", "type": "input", "parent": ""},
    "warehouses_data_centres":{"label": "Warehouses/Data Centres", "type": "input", "parent": ""},
    "residential_buildings_low_rise":{"label": "Residential Buildings (low rise)", "type": "input", "parent": ""},
    "institutional_lower_risk_input":{"label": "Institutional (lower risk)", "type": "input", "parent": ""},
    "institutional_lower_risk_output":{"label": "Institutional (lower risk)", "type": "output", "parent": ""},
    #"institutional_lower_risk_output":{"label": "Institutional (lower risk)", "type": "input", "parent": ""},
    "churches":{"label": "Churches", "type": "input", "parent":  "institutional_lower_risk_output"},
    "colleges_universities_schools":{"label": "Colleges/Universities/Schools", "type": "input", "parent":  "institutional_lower_risk_output"},
    "convalescent_retirement_facilities":{"label": "Convalescent/Retirement Facilities", "type": "input", "parent":  "institutional_lower_risk_output"},
    "correctional_facilities_jails":{"label": "Correctional Facilities/Jails", "type": "input", "parent":  "institutional_lower_risk_output"},
    "courthouses":{"label": "Courthouses", "type": "input", "parent":  "institutional_lower_risk_output"},
    "institutional_other":{"label": "Institutional: Other", "type": "input", "parent":  "institutional_lower_risk_output"},
    "military":{"label": "Military", "type": "input", "parent":  "institutional_lower_risk_output"},
    "recreational_lower_risk_input":{"label": "Recreational (lower risk)", "type": "input", "parent":  ""},
    "recreational_lower_risk_output":{"label": "Recreational (lower risk)", "type": "output", "parent":  ""},
    #"recreational_lower_risk_output":{"label": "Recreational (lower risk)", "type": "input", "parent":  ""},
    "amusement_park":{"label": "Amusement Park", "type": "input", "parent":  "recreational_lower_risk_output"},
    "casinos":{"label": "Casinos", "type": "input", "parent":  "recreational_lower_risk_output"},
    "parks_playgrounds_pools":{"label": "Parks / Playgrounds / Pools", "type": "input", "parent":  "recreational_lower_risk_output"},
    "recreational_other":{"label": "Recreational: Other", "type": "input", "parent":  "recreational_lower_risk_output"},
    "sports_facilities":{"label": "Sports Facilities (EXCLUDING STADIUMS)", "type": "input", "parent":  "recreational_lower_risk_output"},
    "general_building_lower_risk_input":{"label": "General Building (lower risk)", "type": "input", "parent":  ""},
    "general_building_lower_risk_output":{"label": "General Building (lower risk)", "type": "output", "parent":  ""},
    #"general_building_lower_risk_output":{"label": "General Building (lower risk)", "type": "input", "parent":  ""},
    "airport_terminals":{"label": "Airport Terminals", "type": "input", "parent":  "general_building_lower_risk_output"},
    "general_building_other":{"label": "General Building (Other)", "type": "input", "parent":  "general_building_lower_risk_output"},
    "hotels_motels":{"label": "Hotels / Motels", "type": "input", "parent":  "general_building_lower_risk_output"},
    "libraries_museums":{"label": "Libraries / Museums", "type": "input", "parent":  "general_building_lower_risk_output"},
    "offices":{"label": "Offices (Low/High Rise/Other)", "type": "input", "parent":  "general_building_lower_risk_output"},
    "retail_malls_shopping_centers_restaurants":{"label": "Retail / Malls / Shopping Centers / restaurants", "type": "input", "parent":  "general_building_lower_risk_output"},
    "infrastructure_lower_risk_input":{"label": "Infrastructure (lower risk)", "type": "input", "parent":  ""},
    "infrastructure_lower_risk_output":{"label": "Infrastructure (lower risk)", "type": "output", "parent":  ""},
    #"infrastructure_lower_risk_output":{"label": "Infrastructure (lower risk)", "type": "input", "parent":  ""},
    "infrastructure_other":{"label": "Infrastructure: Other", "type": "input", "parent":  "infrastructure_lower_risk_output"},
    "rail":{"label": "Rail", "type": "input", "parent":  "infrastructure_lower_risk_output"},
    "roads":{"label": "Roads", "type": "input", "parent":  "infrastructure_lower_risk_output"},
    "utilities":{"label": "Utilities", "type": "input", "parent":  "infrastructure_lower_risk_output"},
    "industrial_lower_risk_input":{"label": "Industrial (lower risk)", "type": "input", "parent":  ""},
    "industrial_lower_risk_output":{"label": "Industrial (lower risk)", "type": "output", "parent":  ""},
    #"industrial_lower_risk_output":{"label": "Industrial (lower risk)", "type": "input", "parent":  ""},
    "industrial_other":{"label": "Industrial: Other", "type": "input", "parent":  "industrial_lower_risk_output"},
    "manufacturing_facilities":{"label": "Manufacturing Facilities", "type": "input", "parent":  "industrial_lower_risk_output"},
    "nuclear_facilities":{"label": "Nuclear Facilities", "type": "input", "parent":  "industrial_lower_risk_output"},
    "environmental_lower_risk_input":{"label": "Environmental (lower risk)", "type": "input", "parent":  ""},
    "environmental_lower_risk_output":{"label": "Environmental (lower risk)", "type": "output", "parent":  ""},
    #"environmental_lower_risk_output":{"label": "Environmental (lower risk)", "type": "input", "parent":  ""},
    "asbestos_abatement":{"label": "Asbestos Abatement", "type": "input", "parent":  "environmental_lower_risk_output"},
    "environmental_other":{"label": "Environmental Other", "type": "input", "parent":  "environmental_lower_risk_output"},
    "waste_brokering":{"label": "Waste Brokering", "type": "input", "parent":  "environmental_lower_risk_output"},
    "total": {"label": "Total", "type": "output", "parent": "Total"},
    #"total": {"label": "Total", "type": "input", "parent": "Total"},
}

project_type_parent_categories = [
    "residential_lower_risk",
    "residential_higher_risk",
    "institutional_lower_risk_output",
    "recreational_lower_risk_output",
    "general_building_lower_risk_output",
    "infrastructure_lower_risk_output",
    "industrial_lower_risk_output",
    "environmental_lower_risk_output"
    ]

def get_aop_aec_parent_categories(): 
    # df = hx.params.ref_ae_aop_loading
    # x = df["Area of Practice"].tolist()
    x = [
        "architecture",
        "architecture_interior_design",
        "civil",
        "construction_management",
        "environmental",
        "geotech",
        "mep",
        "other_low_risk",
        "process_engineering",
        "structural",
        "surveyor"
    ]
    return x

def get_aop_lpl_parent_categories(): 
    # df = hx.params.ref_lpl_aop_loading
    # x = df["Area of Practice"].tolist()
    x = [
        "banking_financial_institutions",
        "bankruptcy_insolvency_restructuring",
        "class_actions",
        "construction",
        "corporate_commercial",
        "criminal",
        "debt_collection",
        "dispute_resolution",
        "employment_labour",
        "entertainment",
        "environmental",
        "family_matrimonial_children",
        "government",
        "immigration",
        "insurance",
        "intellectual_property_copyright_patent_litigation",
        "intellectual_property_copyright_patent_prosecution",
        "ma",
        "management_risk_consultancy",
        "natural_resources_energy",
        "pensions",
        "personal_injury_workers_comp_product_liability",
        "real_estate_conveyancing_commercial",
        "real_estate_conveyancing_residential",
        "regulatory_competition_antitrust_law_lobbying",
        "securities",
        "taxation",
        "trust_probate_wills"
    ]
    return x

profession_dict = {
    "Lawyers": 0,
    "Architects and Engineers": 1,
    "Contractors": 2
}

incomplete_column = "\U0000274C"  # Red X
complete_column = "\U00002705"  # Green Check
column_labels_modifiers = "non_cds.modifier_labels"

environment_setup = {
    "DEV": {
        "Connection":"Driver={ODBC Driver 17 for SQL Server};Server=DBS-k34-TemplateRater01-DEV,12428;Database=TemplateRater01;Trusted_Connection=yes;MultiSubnetFailover=Yes;",
        "AD": "App.TemplateRater01.Admins.RW"
    },
    "SYSTEST": {
        "Connection": "Driver={ODBC Driver 17 for SQL Server};Server=DBS-68o-TemplateRater01-SYS;Database=TemplateRater01;Trusted_Connection=yes;MultiSubnetFailover=Yes;",
        "AD": "App.TemplateRater01.Admins.RW"
    },
    "UAT": {
        "Connection": "Driver={ODBC Driver 17 for SQL Server};Server=DBS-ank-TemplateRater01-UAT;Database=TemplateRater01;Trusted_Connection=yes;MultiSubnetFailover=Yes;",
        "AD":"App.TemplateRater01.Users.RW.TST"
    },
    "PROD": {
        "Connection": "Driver={ODBC Driver 17 for SQL Server};Server=DBS-p3t-TemplateRater01-PRD;Database=TemplateRater01;Trusted_Connection=yes;MultiSubnetFailover=Yes;",
        "AD":"App.TemplateRater01.Users.RW"
    }
}

def policy_structure_to_dataframe(hxd):
    rows = []
    for layer in hxd.cds.layers:
        rows.append({
            "include": layer.include,
            "limit_eec": layer.limit_eec,
            "limit_agg": layer.limit_agg,
            "excess_eec": layer.excess_eec,
            "excess_agg": layer.excess_agg,
            "rtc": layer.rtc,
            "rtc_agg": layer.rtc_agg,
            "defense_cost": layer.defense_cost,
            "wordings_adj": layer.wordings_adj,
            "uw_adj": layer.uw_adj,
            "brokerage": layer.brokerage,
        })
    return pd.DataFrame(rows)

def policy_addl_structure_to_dataframe(hxd):
    rows = []
    for layer in hxd.cds.layers_addl:
        rows.append({
            "include": layer.include,
            "limit_eec": layer.limit_eec,
            "limit_agg": layer.limit_agg,
            "excess_eec": layer.excess_eec,
            "excess_agg": layer.excess_agg,
            "rtc": layer.rtc,
            "rtc_agg": layer.rtc_agg,
            "defense_cost": layer.defense_cost,
            "wordings_adj": layer.wordings_adj,
            "uw_adj": layer.uw_adj,
            "brokerage": layer.brokerage,
        })
    return pd.DataFrame(rows)

def retention_to_dataframe(hxd):
    rows= []
    for item in hxd.cds.retention_split:
        rows.append({
            "class": "Not Specified" if item.region is None else item.region,              # sort the logic here - done
            "region": "Not Specified" if item.region is None else item.region, 
            "ccy": item.ccy,
            "eec": item.eec,
            "aggregate": item.aggregate,
            "retention_underlying": item.retention_underlying,
            "retention_residual": item.retention_residual,
            "defence_cost_bool": item.defence_cost_bool
        }) 

    return pd.DataFrame(rows)

def territory_to_dataframe(hxd):
    rows = []
    for key in get_territory_groups():
        group = getattr(hxd.cds.exposure.granular.territory.summary, key)
        rows.append({
            "territory": key,
            "year_0": group.year_0_pcnt,
            "year_1": group.year_1_pcnt,
            "year_2": group.year_2_pcnt,
            "year_3": group.year_3_pcnt,
            "year_4": group.year_4_pcnt,
            "year_5": group.year_5_pcnt,
            "weighted": group.weighted,
        })
    return pd.DataFrame(rows)

def client_details_lawyers_to_dataframe(hxd):
    rows = []
    for item in hxd.cds.exposure.granular.client_details_lawyers.areas_of_practice:
        rows.append({
            "areas_of_practice": item.areas_of_practice,
            "year_0_pcnt": item.year_0_pcnt,
            "year_0_value": item.year_0_value,
            "year_1_pcnt": item.year_1_pcnt,
            "year_1_value": item.year_1_value,
            "year_2_pcnt": item.year_2_pcnt,
            "year_2_value": item.year_2_value,
            "year_3_pcnt": item.year_3_pcnt,
            "year_3_value": item.year_3_value,
            "year_4_pcnt": item.year_4_pcnt,
            "year_4_value": item.year_4_value,
            "year_5_pcnt": item.year_5_pcnt,
            "year_5_value": item.year_5_value,
            "weighted": item.weighted,
        })
    return pd.DataFrame(rows)

def client_details_aec_to_dataframe(hxd):
    rows = []
    for item in hxd.cds.exposure.granular.client_details_AEC.areas_of_practice:
        rows.append({
            "areas_of_practice": item.areas_of_practice,
            "year_0_pcnt": item.year_0_pcnt,
            "year_0_value": item.year_0_value,
            "year_1_pcnt": item.year_1_pcnt,
            "year_1_value": item.year_1_value,
            "year_2_pcnt": item.year_2_pcnt,
            "year_2_value": item.year_2_value,
            "year_3_pcnt": item.year_3_pcnt,
            "year_3_value": item.year_3_value,
            "year_4_pcnt": item.year_4_pcnt,
            "year_4_value": item.year_4_value,
            "year_5_pcnt": item.year_5_pcnt,
            "year_5_value": item.year_5_value,
            "weighted": item.weighted,
        })
    return pd.DataFrame(rows)

def get_quotes_params(hxd):
    risk_fx_rate = get_fx_rate(hxd.cds.currencies.source_currency)
    df = policy_structure_to_dataframe(hxd)
    df = df[df["include"] == True]
    cols = ["limit_eec","limit_agg", "excess_eec", "excess_agg", "rtc", "rtc_agg"]
    df[cols] =  df[cols] / risk_fx_rate
    df.rename(columns={
        "limit_eec": "Leec",
        "limit_agg": "Lagg",
        "excess_eec": "Xeec",
        "excess_agg": "Xagg",
        "rtc": "RTC_Lim",
        "rtc_agg": "RTC_Agg",
        "defense_cost": "DCIA",
        "wordings_adj": "Wordings",
        "brokerage": "Brokerage"
    }, inplace=True)

    return df

def get_quotes_params_addl(hxd):
    risk_fx_rate = get_fx_rate(hxd.cds.currencies.source_currency)
    df = policy_addl_structure_to_dataframe(hxd)
    df = df[df["include"] == True]
    cols = ["limit_eec","limit_agg", "excess_eec", "excess_agg", "rtc", "rtc_agg"]
    df[cols] =  df[cols] / risk_fx_rate
    df.rename(columns={
        "limit_eec": "Leec",
        "limit_agg": "Lagg",
        "excess_eec": "Xeec",
        "excess_agg": "Xagg",
        "rtc": "RTC_Lim",
        "rtc_agg": "RTC_Agg",
        "defense_cost": "DCIA",
        "wordings_adj": "Wordings",
        "brokerage": "Brokerage"
    }, inplace=True)

    return df

layer_names = ["Primary", "1XS","2XS","3XS","4XS","5XS","6XS", "7XS", "8XS", "9XS", "10XS"]
layer_addl_names = ["Addl 1", "Addl 2", "Addl 3", "Addl 4", "Addl 5"]

def get_all_layer_names():
    return layer_names + layer_addl_names

def layer_order() -> pd.DataFrame:
    rows = [
        {"layer":"att_layer","order":0},
        {"layer":"Primary","order":1},
        {"layer":"1XS","order":2},
        {"layer":"2XS","order":3},
        {"layer":"3XS","order":4},
        {"layer":"4XS","order":5},
        {"layer":"5XS","order":6},
        {"layer":"6XS","order":7},
        {"layer":"7XS","order":8},
        {"layer":"8XS","order":9},
        {"layer":"9XS","order":10},
        {"layer":"10XS","order":11},       
        {"layer":"Addl 1","order":12},
        {"layer":"Addl 2","order":13},
        {"layer":"Addl 3","order":14},
        {"layer":"Addl 4","order":15},
        {"layer":"Addl 5","order":16},
    ]

    return pd.DataFrame(rows)

def exposure_change_list():
    exposure_change_path = [
        "cds/exposure/granular/exposure_expected_current_year",
    ]
    return(exposure_change_path)


def terms_and_conditions_change_list() :
    terms_and_conditions_change_path = [
        "cds/lawyers_num_attorneys_full", 
        "cds/lawyers_num_attorneys_fte",
        # "hx_core/expiry_date",
        # "hx_core/inception_date",
    ]
    return(terms_and_conditions_change_path)

def brokerage_change_list():
    brokerage_change_path = [
        "cds/layers/brokerage",
        "cds/layers_addl/brokerage"
    ]
    return(brokerage_change_path)

def risk_characteristics_change_list():
    risk_characteristics_change_path = [
        # Currency
        "cds/currencies/source_currency",
        # Territory
        "cds/exposure/granular/territory/summary/total/year_0_pcnt",
        "cds/exposure/granular/territory/summary/total/year_1_pcnt",
        "cds/exposure/granular/territory/summary/total/year_2_pcnt",
        "cds/exposure/granular/territory/summary/total/year_3_pcnt",
        "cds/exposure/granular/territory/summary/total/year_4_pcnt",
        "cds/exposure/granular/territory/summary/total/year_5_pcnt",
        "cds/exposure/granular/territory/summary/total/year_0_value",
        "cds/exposure/granular/territory/summary/total/year_1_value",
        "cds/exposure/granular/territory/summary/total/year_2_value",
        "cds/exposure/granular/territory/summary/total/year_3_value",
        "cds/exposure/granular/territory/summary/total/year_4_value",
        "cds/exposure/granular/territory/summary/total/year_5_value",
        "cds/exposure/granular/territory/summary/total/weighted",
        
        ##### AEC #######
        # Client Details
        "cds/exposure/granular/client_details_AEC/size_of_matters",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_0_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_1_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_2_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_3_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_4_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_5_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_0_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_1_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_2_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_3_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_4_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_5_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/weighted",

        # Individaul Project Types
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_0_pcnt",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_1_pcnt",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_2_pcnt",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_3_pcnt",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_4_pcnt",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_5_pcnt",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_0_value",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_1_value",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_2_value",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_3_value",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_4_value",
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/year_5_value",    
        "cds/exposure/granular/client_details_AEC/individual_project_types/total/weighted",     

        ####### Lawyers  ##########
        # Client Details
        "cds/exposure/granular/client_details_AEC/size_of_matters",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_0_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_1_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_2_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_3_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_4_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_5_pcnt",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_0_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_1_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_2_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_3_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_4_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_5_value",
        "cds/exposure/granular/client_details_AEC/areas_of_practice_total/weighted",
    ]

    return(risk_characteristics_change_path)

def deductible_change_list():
    deductible_change_path = [
        "cds/layers/excess_agg",
        "cds/layers/excess_eec",
        "cds/layers_addl/excess_agg",
        "cds/layers_addl/excess_eec",
        "cds/retention_split/eec",
        "cds/retention_split/aggregate",
        "cds/retention_split/retention_underlying",
        "cds/retention_split/retention_residual",
    ]
    return(deductible_change_path)    

def limit_change_list():
    limit_change_path = [
        "cds/layers/limit_eec",
        "cds/layers/limit_agg",
        "cds/layers_addl/limit_eec",
        "cds/layers_addl/limit_agg",
    ]
    return(limit_change_path)     

exposure_rate_per_million_revenue_aec = {
    "united_kingdom": 5962.267144,
    "australia": 7354.984192,
    "canada": 5962.267144,
    "quebec": 10075.23738,
    "ireland": 5962.267144,
    "united_states": 8290.69588,
    "asia_pac_south_africa": 5962.267144,
    "europe": 4681.100975,
    "middle_east": 5962.267144,
    "tax_haven": 5962.267144,
    "rest_of_world": 5962.267144,
}

exposure_rate_per_million_revenue_lpl = {
    "united_kingdom": 2657.413963,
    "australia": 2743.38002,
    "canada": 2551.507103,
    "quebec": 2551.507103,
    "ireland": 2551.507103,
    "united_states": 3359.548232,
    "asia_pac_south_africa": 2036.459459,
    "europe": 2036.459459,
    "middle_east": 2036.459459,
    "tax_haven": 2657.413963,
    "rest_of_world": 1478.307601,
}

chart_revenue_steps = [
    100_000_000,
    200_000_000,
    300_000_000,
    400_000_000,
    500_000_000,
    600_000_000,
    700_000_000,
    800_000_000,
    900_000_000,
    1000_000_000,
    1100_000_000,
    1200_000_000,
    1300_000_000,
    1400_000_000,
    1500_000_000,
    3000_000_000,
    4500_000_000,
    6000_000_000,
    7500_000_000,
    9000_000_000,
    10_500_000_000,
    12_000_000_000,
    13_500_000_000,
    15_000_000_000,
    16_500_000_000,
    18_000_000_000,
    19_500_000_000,
    21_000_000_000,
    22_500_000_000,
    24_000_000_000,
    25_500_000_000,
    27_000_000_000,
    28_500_000_000,
    30_000_000_000
]

hover_info = {
    "retention_underlying":"Underlying to EEC and Agg is fully eroded.",
    "retention_residual":"Residual retention after Agg is fully eroded.",
    "rtc":"For RTC deals, please keep Limit Agg and Excess Agg empty.",
    "wordings_adj":"0% means no adjustment applied.",
    "uw_adj":"0% means no adjustment applied.",
    "blended_model_net_rate":"Includes CAT load and NMP load.",
    "expected_loss_cost_net":" - Net of non loss cost provisions\n - Net of brokerage",
    "uw_experience_weighting":" - If Experience Rate is higher, then full credibility is given.\n - If Experience Rate is lower, then only 20% credibility is given.",
    "blended_uw_net_rate":"Includes:\n - Wordings Adjustment\n - UW Adjustment\n - CAT load and NMP load",
    "benchmark_premium_uw_view":" - Gross of brokerage\n - Benchmark LR 70%",
    "gross_rate_per_mill":"This is the gross rate based on the Bound Premium. It includes the non loss cost provisions.",
    "elevated_risk_year_load":"May include:\n - Increased economic risk\n - Recession\n - Higher than normal claims inflation.",         
    "gross_benchmark_premium":"Include 70% LR and Brokerage.",
    "ilf_gross_benchmark_premium":("ILF Implied Experience Rate is shown for imformation only.\n\n"
                                    "This approach provides a hybrid experience-exposure rate, whereby:\n"
                                    "1) Emprical losses are used to price up to the attritional cap (experience rating)\n"
                                    "2) The ILFs then used to extrapolate to the full policy limit (exposure rating)"),  
    "value_of_claims_data":"Accounts for exposure revaluing, exposure weighting and general IBNR.",
    "total_usd_inflated":"The claims post retention structure is fed into the experience rating.",
    "territory_policy_year":"Please leave blank unless you happend to have splits for the upcoming policy year.",         
    "inception_date":"Inception Date used to calulate the IBNR.",     
    "latest_policy_year": "Best guess for upcoming policy year, NOT the last completed policy year.",    
    "calculated_policy_year":"The earliest 5 years notional revenue is back calculated, based on the annual growth rate."                       
}