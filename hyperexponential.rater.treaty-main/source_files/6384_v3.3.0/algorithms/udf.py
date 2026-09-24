import hx
import pandas as pd
import numpy as np
import math as math
from scipy.stats import nbinom, poisson
import scipy.special as sc
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves
from ast import literal_eval
from io import BytesIO
import pyodbc
from scipy.optimize import brentq

def list_to_numpy(input_list: list, data_type) -> np.array:

    if data_type == str:
        output = np.array(input_list, dtype = str)
        return output

    output = np.array(input_list, dtype = float)
    output = np.nan_to_num(output, nan=0.0)

    if data_type == int:
        output = output.astype(int)

    return output

def duplicate_ylt(ylt, no_sims):
    ## adjustment in-case no_sims > ylt max year ~~~
    ylt_max_year = ylt["YEAR"].max()
    ylt_max_year = math.ceil(ylt_max_year / 1e3) * 1e3 # sometimes max year e.g 9987, round to nearest 1000
    duplications = int(utils.ratio(no_sims, ylt_max_year)) - 1

    if duplications > 0:
        duplicate_list = [None] * duplications
        for i in range(duplications):
            duplicate_temp = ylt.copy()
            duplicate_temp["YEAR"] = duplicate_temp["YEAR"] + (ylt_max_year * (i+1))
            duplicate_list[i] = duplicate_temp

        final_ylt = pd.concat([ylt] + duplicate_list, ignore_index = True)
    else:
        final_ylt = ylt.copy()
    
    return final_ylt


def generate_ymlt(df: pd.DataFrame, sims: int) -> pd.DataFrame:
    """
    Args:
        df (pd.DataFrame): DataFrame of format [rp, cedant_loss]
        sims (int): 

    Returns:
        pd.DataFrame: 
    """
    df["percentile"] = 1 - (1 / df["rp"])
    df = df.sort_values("percentile",ascending = True).reset_index(drop = True)

    sim_table = pd.DataFrame(data = {"percentile": range(1, sims + 1)})
    sim_table["percentile"] = sim_table["percentile"] / sims

    sim_table = pd.merge_asof(sim_table, df, on = "percentile", direction = "backward")#.fillna(0)
    sim_table["rp"] = sim_table["rp"].fillna(0)
    sim_table["cedant_loss"] = sim_table["cedant_loss"].fillna(0)

    sim_table = sim_table.rename(columns = {"rp": "rp_below", "cedant_loss": "cedant_loss_below"})
    sim_table["rp_below"] = np.where(sim_table["rp_below"] == 0, 1, sim_table["rp_below"])

    sim_table = pd.merge_asof(sim_table, df, on = "percentile", direction="forward")
    sim_table["rp"] = sim_table["rp"].fillna(np.max(sim_table["rp"]))
    sim_table["cedant_loss"] = sim_table["cedant_loss"].fillna(np.max(sim_table["cedant_loss"]))

    sim_table = sim_table.rename(columns = {"rp": "rp_above", "cedant_loss": "cedant_loss_above"})
    sim_table["rp"] = np.where(sim_table["percentile"] < 1, 1 / (1 - sim_table["percentile"]), sim_table["rp_above"])

    sim_table["cedant_loss"] = np.where(sim_table["rp_above"] == sim_table["rp_below"],
                                sim_table["cedant_loss_above"],
                                sim_table["cedant_loss_below"] 
                                + (sim_table["cedant_loss_above"] - sim_table["cedant_loss_below"]) 
                                * (sim_table["rp"] - sim_table["rp_below"]) 
                                / (sim_table["rp_above"] - sim_table["rp_below"]))               

    # randomly sort simulated losses
    sim_table = (sim_table
            .drop(columns = ["percentile", "rp_below", "cedant_loss_below", "rp_above", "cedant_loss_above", "rp"])
            .sample(frac = 1)
    )

    sim_table = sim_table.assign(year = range(1, sims + 1)).reset_index(drop = True)

    sim_table = sim_table[["year","cedant_loss"]]

    return sim_table


def generate_oep(df: pd.DataFrame, loss_column: str, sims: int, rp_array: np.array, curve_type: str = "OEP", attr_losses = 0) -> pd.DataFrame:
    """
    Args:
        df (pd.DataFrame): DataFrame of format ["rp", loss_column]
        sims (int): 
        loss_column (str):
        rp_array (np.array):

    Returns:
        pd.DataFrame: 
    """
    year_table = pd.DataFrame(data = {"year": range(1,sims+1)})

    df.columns = df.columns.str.lower()

    if curve_type == "OEP":
        df = (df
            .groupby("year")
            .agg(loss = pd.NamedAgg(f"{loss_column}", "max"))
        )
        year_table = pd.merge(year_table, df, on = "year", how = "left").fillna(0)
    else:
        df = (df
            .groupby("year")
            .agg(loss = pd.NamedAgg(f"{loss_column}", "sum"))
        )
        year_table = pd.merge(year_table, df, on = "year", how = "left").fillna(0)
        year_table["loss"] += attr_losses

    oep_curve = pd.DataFrame(data = {"rp": rp_array, "loss": np.quantile(year_table["loss"], 1 - 1 / rp_array)})

    return oep_curve


def layer_loss(df: pd.DataFrame,
               limit: pd.Series,
               excess: pd.Series,
               no_reins: int,
               aad: float = 0,
               ded_type: str = "Conventional") -> pd.Series:

    """
    Args:
        df (pd.DataFrame): DataFrame of format ["year", "loss"]

    Returns:
        pd.Series: 
    """
    
    if ded_type not in ["Conventional", "Franchise"] :
        raise ValueError("ded_type must either be Conventional or Franchise")
    else:
        df.columns = ["year", "loss"]
        if ded_type == "Conventional":
            df["net_loss_unlim"] = np.minimum(limit, np.maximum(df["loss"] - excess, 0))
        elif ded_type == "Franchise":
            df["net_loss_unlim"] = np.where(df["loss"] > excess, np.minimum(df["loss"], limit), 0)
        
        df["cum_net_loss_unlim"] = df.groupby("year")["net_loss_unlim"].transform("cumsum")
        df["cum_net_loss_lim"] = np.maximum(0, np.minimum(df["cum_net_loss_unlim"] - aad, limit * (1 + no_reins)))
        df["cum_net_loss_lim_shift"] = df.groupby("year")["cum_net_loss_lim"].shift(1).fillna(0)
        df["subject_loss"] = df["cum_net_loss_lim"] - df["cum_net_loss_lim_shift"]

    return df["subject_loss"]


def kpi_calc(df: pd.DataFrame, loss_column: str, sims: int, attr_losses = 0) -> dict:
    """
    kpi entry "el" or "sd".
    """
    year_table = pd.DataFrame(data = {"YEAR": range(1, sims+1)})

    df = df.rename(columns = {"year": "YEAR"})
    df = (df
          .groupby("YEAR")[f"{loss_column}"]
          .sum()
        )

    year_table = pd.merge(year_table, df, on = "YEAR", how = "left").fillna(0)

    year_table[f"{loss_column}"] += attr_losses

    el = year_table[f"{loss_column}"].mean()
    sd = year_table[f"{loss_column}"].std()

    return {"el": el, "sd": sd}


def agg_std_dev(x: pd.Series):
    return np.sqrt(np.sum(x**2))


def create_index(column: pd.Series) -> pd.Series: 
    reversed_column = column[::-1] + 1
    cumprod_reversed = reversed_column.cumprod()[::-1]
    shifted_index = cumprod_reversed.shift(-1).fillna(1)
    return shifted_index


def reins_calc(df: pd.DataFrame,
               loss_column: str,
               limit: int,
               no_reins: int,
               reins_perc: list,
               sims: int) -> float:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        loss_column (str): _description_
        limit (int): _description_
        no_reins (int): _description_
        reins_perc (list): _description_
        sims (int): _description_

    Raises:
        ValueError: reins_perc list needs to be length no_reins.

    Returns:
        float: net of paid reinstatements loss
    """

    if no_reins != len(reins_perc):
        raise ValueError("reins_perc list needs to be length no_reins.")
    else:    
        year_table = pd.DataFrame(data = {"YEAR": range(1, sims + 1)})

        df = df.rename(columns = {"year":"YEAR"})
        df = (df
            .groupby("YEAR")[f"{loss_column}"]
            .sum()
            )
        
        year_table = pd.merge(year_table, df, on = "YEAR", how = "left").fillna(0)

        el = year_table[f"{loss_column}"].mean()

        if no_reins > 0:
            reins_fac_list = [None] * no_reins
            reins_fac_list = pd.Series(reins_fac_list)

            for i in range(no_reins):
                year_table = year_table.assign(reins_temp = np.minimum(limit, np.maximum(0, year_table[f"{loss_column}"] - ((i + 1) - 1) * limit)))
                reins_fac = year_table["reins_temp"].mean()
                reins_fac = reins_fac * (reins_perc[i] / limit)
                reins_fac_list[i] = reins_fac

            reins_fac = reins_fac_list.sum()

            # net paid reinstatements
            net_loss = el / (1 + reins_fac)
        else:
            net_loss = el
    
        return net_loss



def reins_calc_burn(df: pd.DataFrame,
                    loss_column: str,
                    limit: int,
                    no_reins: int,
                    reins_perc: list,
                    super_cat_el: float,
                    super_cat_sd: float) -> float:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        loss_column (str): _description_
        limit (int): _description_
        no_reins (int): _description_
        reins_perc (list): _description_

    Raises:
        ValueError: reins_perc list needs to be length no_reins.

    Returns:
        float: net of paid reinstatements loss
    """
   
    el = df[f"{loss_column}"].mean() + super_cat_el
    sd = np.sqrt(df[f"{loss_column}"].std()**2 + super_cat_el**2)

    if no_reins > 0:
        reins_fac_list = [None] * no_reins
        reins_fac_list = pd.Series(reins_fac_list)

        for i in range(min(no_reins, len(reins_perc))):
            df = df.assign(reins_temp = np.minimum(limit, np.maximum(0, df[f"{loss_column}"] - ((i + 1) - 1) * limit)))
            reins_fac = df["reins_temp"].mean()
            reins_fac = reins_fac * (reins_perc[i] / limit)
            reins_fac_list[i] = reins_fac

        reins_fac = reins_fac_list.sum()

        # net paid reinstatements
        net_loss = el / (1 + reins_fac)
        net_sd = sd / (1 + reins_fac)
    else:
        net_loss = el
        net_sd = sd

    return [net_loss, net_sd]



def reins_approx(lol: float, 
                 cov: float, 
                 limit: float, 
                 aad: float, 
                 no_reins: int,
                 reins_perc: list,
                 show_cat_work_comp_input: bool) -> list:

    if lol == 0:
        result_list = [0, 0, 0, 0, 0]
    elif show_cat_work_comp_input:
        if cov == "poisson":
                df = pd.DataFrame(data = {"limit_exhaustions": range(0, 50),
                            "prob": poisson.pmf(np.array(range(0, 50)), lol)})
        else:
            cov = float(cov)
            n = lol**2 / ( (lol * cov)**2 - lol)
            p = lol / (lol * cov)**2

            df = pd.DataFrame(data = {"limit_exhaustions": range(0,50),
                                    "prob": nbinom.pmf(np.array(range(0, 50)), n, p)})

        df["gross_loss"] = df["limit_exhaustions"] * limit
        df["loss_net_aad"] = np.maximum((df["limit_exhaustions"] * limit) - aad, 0)
        df["loss_cap_reins"] = np.minimum(df["loss_net_aad"], limit * (1 + no_reins))
        df["total_reins_fac"] = 0

        for i in range(min(no_reins, len(reins_perc))):
            df["reins_fac_temp"] = np.where(df["limit_exhaustions"] > 0,
                                            np.minimum(limit, np.maximum(0, df["loss_cap_reins"] - ((i + 1) - 1) * limit)) * reins_perc[i] / limit,
                                            0)
            df["total_reins_fac"] = df["total_reins_fac"] + df["reins_fac_temp"]

        gross_el = (df["prob"] * df["gross_loss"]).sum()
        gross_var_approx = (df["prob"] * df["gross_loss"]**2).sum() - gross_el**2
        gross_sd_approx = np.sqrt(gross_var_approx)

        net_el_excl_reins_prem = (df["prob"] * df["loss_cap_reins"]).sum()
        net_var_approx = (df["prob"] * df["loss_cap_reins"]**2).sum()
        net_sd_approx = np.sqrt(net_var_approx)

        reins_factor = (df["prob"] * df["total_reins_fac"]).sum()

        net_sd_factor_excl_reins_prem = utils.ratio(net_sd_approx, gross_sd_approx)

        ## bermuda second loss probability
        second_loss_probability = 1 - df.loc[df["limit_exhaustions"] == 0]["prob"].iloc[0]

        result_list = [gross_el, net_el_excl_reins_prem, reins_factor, net_sd_factor_excl_reins_prem, second_loss_probability]

    else:
        result_list = [lol * limit, lol * limit, 0, 1, 0]

    return result_list


def sim_elt_calc(elt: pd.DataFrame, sims: int) -> pd.DataFrame:
        
    # 1) assign parameters
    event_count = elt["RATE"].sum()
    elt["occ_prop"] = elt["RATE"] / event_count
    elt["alpha"] =  (
        ((elt["PERSPVALUE"] / (elt["STDDEVC"] + elt["STDDEVI"])) ** 2 
        * (1 - elt["PERSPVALUE"] / elt["EXPVALUE"]))
        - (elt["PERSPVALUE"] / elt["EXPVALUE"])
    )

    elt.loc[elt["alpha"].isna(), "alpha"] = 0

    elt["beta"] = elt["alpha"] * (elt["EXPVALUE"] / elt["PERSPVALUE"] - 1)
    elt = elt.rename(columns = {"PERSPVALUE": "PERSPVALUE_COMB"})

    # 2) generate number of losses per year
    year_list = np.random.poisson(event_count, sims)
    year_list = np.repeat(range(1, sims + 1), year_list)

    # 3) assign events to year losses
    event_samples = np.random.choice(elt["EVENTID"], size = len(year_list), replace = True, p = elt["occ_prop"])
    uniform_sample = np.random.uniform(size = len(year_list))
    
    # 4) create YLT
    ylt = pd.DataFrame({"YEAR": year_list,                        
                        "EVENTID": event_samples,
                        "percentile": uniform_sample})
    
    ylt = pd.merge(ylt, elt, how = "left", on = "EVENTID")

    ylt["LOSS"] = ylt["EXPVALUE"] * sc.betaincinv(ylt["alpha"], ylt["beta"], ylt["percentile"])
    ## adjust for inf and NA, set to mean loss
    ylt["LOSS"] = np.where(np.isinf(ylt["LOSS"]) | ylt["LOSS"].isna(), ylt["PERSPVALUE_COMB"], ylt["LOSS"])

    ylt = ylt[["YEAR", "EVENTID", "LOSS", "PERSPVALUE_COMB"]]  

    return ylt


def sim_elt_all(elt: pd.DataFrame, sims: int) -> pd.DataFrame:
    """_summary_

    Args:
        elt (pd.DataFrame): ELT Input
        sims (int): 

    Returns:
        pd.DataFrame: YLT
    """

    elt = elt.rename(columns=str.upper) 

    col_names_expected = ["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "TABLE_INDEX"]

    if "PERSPCODE" in elt.columns.values:
        elt = elt.drop(columns = "PERSPCODE")

    col_names = elt.columns.values

    col_names_expected_sort = sorted(col_names_expected)
    col_names_sort = sorted(col_names)

    if col_names_expected_sort != col_names_sort:
        raise ValueError("Check Format of ELT columns")
    else:                   
        elt = elt[col_names_expected]

        event_list = set(elt["EVENTID"])
        base_elt = (
            elt[["EVENTID", "TABLE_INDEX", "PERSPVALUE"]]
            .drop_duplicates()
            .reset_index(drop = True)
        )

        # check for duplicate EVENTIDs, if so group otherwise continue
        if len(elt["EVENTID"]) != len(event_list):      
            elt = (elt
                .groupby("EVENTID", as_index = False)
                .agg({
                    "RATE": "mean",
                    "PERSPVALUE" : "sum",
                    "STDDEVC": "sum",
                    "STDDEVI": agg_std_dev,
                    "EXPVALUE": "sum"
                })
                .reset_index())
            
        ylt = sim_elt_calc(elt, sims)
        ylt = pd.merge(ylt, base_elt, how = "left", on = "EVENTID")
        ylt["LOSS"] = ylt["LOSS"] * ylt["PERSPVALUE"] / ylt["PERSPVALUE_COMB"]
        ylt = ylt[["YEAR", "EVENTID", "LOSS", "TABLE_INDEX"]]

    return ylt


def fhcf_recoveries(year: pd.Series,
                    indemnity_loss: pd.Series,
                    fhcf_limit: float, 
                    fhcf_excess: float,                                         
                    fhcf_participation: float,                     
                    lae_actual: float = 0, 
                    lae_cap: float = 0) -> pd.Series:
    
    df = pd.DataFrame({"year": year,
                    "loss": indemnity_loss})
    
    lae_final = min(lae_actual, lae_cap)

    # The largest two losses are subject to the standard excess level, all subsequent losses subject to an excess reduction of two thirds
    df = df.sort_values(["year", "loss"], ascending=[True, False])
    largest_two_index = df.groupby("year").head(2).index
    df["fhcf_excess"] = fhcf_excess / 3
    df.loc[largest_two_index, "fhcf_excess"] = fhcf_excess

    # lae cap applies to losses in excess of retention, not fgu
    df["loss_excess_retention"] = np.maximum(0, df["loss"] - fhcf_excess)
    df["unl"] = df["loss_excess_retention"] * (1 + lae_final)
    df["fhcf_loss"] = layer_loss(df[["year", "unl"]], fhcf_limit, excess = 0, no_reins = 0) * fhcf_participation
    df = df.sort_index()

    return df["fhcf_loss"]


def ccy_conversion(ccy_column: pd.Series,
                   target_ccy: str,
                   ccy_table: pd.DataFrame) -> pd.Series:

    to_usd_dict = ccy_table.set_index("currency")["to_usd"].to_dict()
    ccy_column = pd.Series(ccy_column)

    original_to_usd = ccy_column.map(to_usd_dict).to_numpy()
    usd_to_target = to_usd_dict[target_ccy]

    exchange_rate_multiplicative = utils.ratio(usd_to_target, original_to_usd)
    exchange_rate_multiplicative = np.where(np.isnan(original_to_usd) | np.isnan(usd_to_target), 1, exchange_rate_multiplicative)

    return exchange_rate_multiplicative


def net_el_func(method_rms, method_el, method_sd, limit_cnv, aad_cnv, number_reins, reins_perc, reins_cov_table, override_limit_factor, bs_load, afb_line, show_cat_work_comp_input):

    gross_lol_results = [None] * len(method_el)
    model_limit_factor_results = [None] * len(method_el)
    net_el_excl_reins_prem_results = [None] * len(method_el)
    exp_reins_cost_results = [None] * len(method_el)
    net_el_results = [None] * len(method_el)
    net_sd_results = [None] * len(method_el)
    net_el_incl_bs_results = [None] * len(method_el)
    net_sd_incl_bs_results = [None] * len(method_el)
    afb_net_el_results = [None] * len(method_el)
    afb_net_sd_results = [None] * len(method_el)

    second_loss_probability_results = [None] * len(method_el)

    a = reins_cov_table.at["a", "value"]
    b = reins_cov_table.at["b", "value"]

    for i, el in enumerate(method_el):

        gross_el = method_el[i]
        gross_sd = method_sd[i]

        lol = utils.ratio(gross_el, limit_cnv)

        ## calc cov to use
        power_cov = a * (lol ** b)
        poisson_cov = 1 / np.sqrt(lol)

        cov = np.where(lol == 0, 0, 
                np.where(power_cov < poisson_cov , "poisson",
                    power_cov))

        reins_list = [None] * len(limit_cnv)
        net_results = [reins_approx(lol[i], cov[i], limit_cnv[i], aad_cnv[i], number_reins[i], reins_perc[i], show_cat_work_comp_input) for i in range(len(limit_cnv))]

        model_net_el_excl_reins_prem = [x[1] for x in net_results]
        exp_reins_cost = [x[2] for x in net_results]
        model_net_sd_factor_excl_reins_prem = [x[3] for x in net_results]
        second_loss_probability = [x[4] for x in net_results]

        model_net_el_excl_reins_prem = np.array(model_net_el_excl_reins_prem)
        exp_reins_cost = np.array(exp_reins_cost)
        model_net_sd_factor_excl_reins_prem = np.array(model_net_sd_factor_excl_reins_prem)
        second_loss_probability = np.array(second_loss_probability)

        model_limit_factor = utils.ratio(model_net_el_excl_reins_prem, gross_el)
        selected_limit_factor = np.where(override_limit_factor, override_limit_factor, model_limit_factor)
        selected_limit_factor = selected_limit_factor.astype(float)

        net_el_excl_reins_prem = gross_el * selected_limit_factor
        net_el = net_el_excl_reins_prem / (1 + exp_reins_cost)

        net_sd_factor = np.where(aad_cnv > 0, model_net_sd_factor_excl_reins_prem, selected_limit_factor)
        net_sd_excl_reins_prem = gross_sd * net_sd_factor
        net_sd = net_sd_excl_reins_prem / (1 + exp_reins_cost)

        net_el_incl_bs = net_el * (1 + bs_load)
        net_sd_incl_bs = net_sd * (1 + bs_load)

        afb_net_el = net_el_incl_bs * afb_line
        afb_net_sd = net_sd_incl_bs * afb_line

        gross_lol_results[i] = lol
        model_limit_factor_results[i] = model_limit_factor
        net_el_excl_reins_prem_results[i] = net_el_excl_reins_prem
        exp_reins_cost_results[i] = exp_reins_cost
        net_el_results[i] = net_el
        net_sd_results[i] = net_sd
        net_el_incl_bs_results[i] = net_el_incl_bs
        net_sd_incl_bs_results[i] = net_sd_incl_bs
        afb_net_el_results[i] = afb_net_el
        afb_net_sd_results[i] = afb_net_sd

        second_loss_probability_results[i] = second_loss_probability

    if method_rms:
        return([gross_lol_results, model_limit_factor_results, net_el_excl_reins_prem_results, exp_reins_cost_results, net_el_results, net_sd_results, net_el_incl_bs_results, net_sd_incl_bs_results, afb_net_el_results, afb_net_sd_results, second_loss_probability_results])
    else:
        return([afb_net_el_results, afb_net_sd_results])


def query_bi_database(query, columns):
    # Set up connection details
    # print("starting " + str(datetime.datetime.now()))
    print(str(query))
    
    is_dev = (hx.secrets.environment_name == 'beazley-dev' or hx.secrets.environment_name == 'beazley-tst')

    database_name   = "BeazleyIntelligenceDataSets"

    host = hx.secrets.beazleyintelligencedatasets_host_uat if is_dev else hx.secrets.beazleyintelligencedatasets_host_prd       ### UAT: hx.secrets.beazleyintelligencedatasets_host_uat;        Prod:   hx.secrets.beazleyintelligencedatasets_host_prd
    user = hx.secrets.beazleyintelligencedataSets_login_uat if is_dev else hx.secrets.beazleyintelligencedataSets_login_prd      ### UAT: hx.secrets.beazleyintelligencedataSets_login_uat;       Prod:   hx.secrets.beazleyintelligencedataSets_login_prd
    password = hx.secrets.beazleyintelligencedataSets_password_uat if is_dev else hx.secrets.beazleyintelligencedataSets_password_prd   ### UAT: hx.secrets.beazleyintelligencedataSets_password_uat;    Prod:   hx.secrets.beazleyintelligencedataSets_password_prd

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER={' + host + '};DATABASE={' + database_name + '};UID={' + user + '};PWD={' + password + '}', timeout=30)

    # Setting up a cursor is the idiomatic way of maintaining the connection
    cursor = cnxn.cursor()

    # Fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    #print("ending " + str(datetime.datetime.now()))
    return pd.DataFrame.from_records(rows, columns=columns)


def mbbefd_fls(b: float,
               g: float,
               tiv_perc: float) -> float:
    """
    returns the worth % for a given MBBEFD curve with parameter c
    """

    fls_result = np.where((b > 0) & (g > 0), utils.ratio(np.log(utils.ratio(((g - 1) * b + (1 - g * b) * b ** tiv_perc), 1 - b)), np.log(g * b)), 0)

    return fls_result

def mbbefd_expected_value(b: float,
                          g: float) -> float:

    return utils.ratio((np.log(b * g) * (1 - b)) , (np.log(b) * (1 - b * g)))

def mbbefd_pdf(b: float,
               g: float,
               x: float) -> float:
    
    return 1 - utils.ratio(1 - b, (g - 1) * b**(1-x) + (1 - g*b))


def mbbefd_inv_pdf(b, g, y):
    return brentq(lambda x: mbbefd_pdf(b, g, x) - y, -0.1, 0.1)



def mbbefd_inverse(b: float,
                   g: float,
                   U: float) -> float:

    F_1 = mbbefd_pdf(b, g, 1)

    num = b * (g - 1) * (1 - U)
    den = b * (g - 1) + U * (1 - b * g)

    x = np.where(U > F_1, 1, (np.log(num) - np.log(den)) / np.log(b))

    return x






