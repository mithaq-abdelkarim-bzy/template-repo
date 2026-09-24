"""
rate_simulation.py
-------------
Python port of R Code — Monte Carlo simulation of professional
liability losses with split retentions, multi-quote tower structures, and
Defence Costs In Addition (DCIA) support.

Matrix convention throughout:
    axis 0 (rows)    = claim ordinal within a simulated year
    axis 1 (columns) = simulations

Inputs are plain Python / NumPy / pandas objects; no R or Excel dependencies.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import nbinom

from algorithms.rate_simulation_helpers import apply_quotes, retention_apply3


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_simulation(
    ded_params: pd.DataFrame,
    model_params: pd.DataFrame,
    quotes_params: pd.DataFrame,
    add_quotes_params: pd.DataFrame,
    revenue: float,
    r_scalar_input_odf: float,
    num_sims: int = 10_000,
    seed: int = 1,
) -> dict:
    """
    Run the Professions liability simulation.

    Parameters
    ----------
    ded_params : DataFrame
        Retention / deductible parameters per retention class.
        Required columns:
            Class               : str  — retention class identifier
            EEC                 : float — each-and-every-claim retention
            aggRet              : float — aggregate retention (NaN = none)
            InitialMaintenance  : float — maintenance deductible before agg
            MaintenanceThereafter : float — maintenance deductible after agg
            AppliesDefence      : str  — "Yes"/"No" — defence in retention?

    model_params : DataFrame
        Territory / severity model parameters.
        Required columns:
            Area   : str   — territory identifier
            Class  : str   — retention class for this territory
            En     : float — expected number of claims (freq mean)
            mu     : float — lognormal mean (log scale)
            sigma  : float — lognormal sigma (log scale)
            DCp1   : float — defence cost proportion (0–1)

    quotes_params : DataFrame
        Tower quote layers (first row is a dummy/burn layer and is ignored).
        Required columns: Leec, Lagg, Xeec, Xagg, RTC_Lim, RTC_Agg, DCIA

    add_quotes_params : DataFrame
        Additional (off-tower) quote layers (first row is a dummy and is
        ignored).  Same columns as quotes_params.

    revenue : float
        Total revenue / fees for the risk (used to compute rate per £/$ of
        revenue).

    r_scalar_input_odf : float
        Overdispersion factor for the negative binomial frequency model.
        theta = En / (ODF - 1).

    num_sims : int, optional
        Number of Monte Carlo simulations. Default 10 000.

    seed : int, optional
        Random seed for reproducibility. Default 1.

    Returns
    -------
    tuple of (model_outputs, add_model_outputs) : each a pd.DataFrame

        Each row corresponds to one active quote layer (dummy row excluded).
        Column names match the R comments in simulation.r:

            BookRate          : exposure premium per unit of revenue / 1e6
            FreqPer1000       : indemnity frequency per 1 000 revenue units
            DefFreqFGUPer1000 : defence FGU frequency per 1 000 revenue units
            ExhaustionProb    : mean exhaustion probability across simulations
    """
    rng = np.random.default_rng(seed)

    # ------------------------------------------------------------------
    # Unpack retention parameters
    # ------------------------------------------------------------------
    each_retention = ded_params["EEC"].to_numpy(dtype=float)
    agg_retention = ded_params["aggRet"].to_numpy(dtype=float)
    initial_deductible = ded_params["InitialMaintenance"].to_numpy(dtype=float)
    post_agg_deductible = ded_params["MaintenanceThereafter"].to_numpy(dtype=float)
    def_costs_in_retention = ded_params["AppliesDefence"].tolist()

    def _col(df, name, fill=0.0):
        """Extract a numeric column, treating missing values as ``fill``."""
        return np.nan_to_num(df[name].to_numpy(dtype=float), nan=fill)

    # ------------------------------------------------------------------
    # Unpack tower quote parameters
    # ------------------------------------------------------------------
    each_limit = _col(quotes_params, "Leec")
    agg_limit = _col(quotes_params, "Lagg")
    each_excess = _col(quotes_params, "Xeec")
    agg_excess = _col(quotes_params, "Xagg")
    rtc_limit = _col(quotes_params, "RTC_Lim")
    rtc_agg_limit = _col(quotes_params, "RTC_Agg")
    dcia_flag = quotes_params["DCIA"].tolist()

    # RTC_agg cannot be smaller than RTC_limit
    rtc_agg_limit = np.maximum(rtc_agg_limit, rtc_limit)

    # ------------------------------------------------------------------
    # Unpack additional quote parameters
    # ------------------------------------------------------------------
    if add_quotes_params is None or add_quotes_params.empty:
        add_each_limit = np.array([])
        add_agg_limit = np.array([])
        add_each_excess = np.array([])
        add_agg_excess = np.array([])
        add_rtc_limit = np.array([])
        add_rtc_agg_limit = np.array([])
        add_rtc_agg_limit = np.array([])
        add_dcia_flag = np.array([])
    else:
        add_each_limit = _col(add_quotes_params, "Leec")
        add_agg_limit = _col(add_quotes_params, "Lagg")
        add_each_excess = _col(add_quotes_params, "Xeec")
        add_agg_excess = _col(add_quotes_params, "Xagg")
        add_rtc_limit = _col(add_quotes_params, "RTC_Lim")
        add_rtc_agg_limit = _col(add_quotes_params, "RTC_Agg")
        add_rtc_agg_limit = np.maximum(add_rtc_agg_limit, add_rtc_limit)
        add_dcia_flag = add_quotes_params["DCIA"].tolist()


    num_quotes = len(quotes_params)
    num_add_quotes = 0 if add_quotes_params is None else len(add_quotes_params)

    territories = model_params["Area"].unique().tolist()
    retention_classes = model_params["Class"].unique().tolist()
    num_retention_classes = len(retention_classes)

    # ------------------------------------------------------------------
    # PHASE 1 — Simulate FGU losses per territory
    # ------------------------------------------------------------------
    # Store as dict: territory_name -> (indemnity_matrix, defence_matrix, freq_vector)
    territory_indemnity: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    territory_defence: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    for territory in territories:
        tp = model_params[model_params["Area"] == territory].iloc[0]

        mu = float(tp["En"])
        theta = float(mu / (r_scalar_input_odf - 1))  # NegBin dispersion
        mu_sev = float(tp["mu"])
        sigma = float(tp["sigma"])
        dc_prop = float(tp["DCp1"])

        # Simulate claim counts (Negative Binomial)
        # scipy nbinom(n, p): mean = n*(1-p)/p, so p = theta/(mu+theta)
        frequency = nbinom.rvs(
            n=theta,
            p=theta / (mu + theta),
            size=num_sims,
            random_state=rng,
        )

        max_freq = int(frequency.max()) if frequency.max() > 0 else 1
        individual_claims = np.zeros((max_freq, num_sims), dtype=float)

        for j in range(num_sims):
            n_j = frequency[j]
            if n_j > 0:
                individual_claims[:n_j, j] = rng.lognormal(
                    mean=mu_sev, sigma=sigma, size=n_j
                )

        # Split into indemnity and defence
        indemnity_matrix = individual_claims * (1.0 - dc_prop)
        defence_matrix = individual_claims * dc_prop

        territory_indemnity[territory] = (indemnity_matrix, frequency)
        territory_defence[territory] = (defence_matrix, frequency)

    # ------------------------------------------------------------------
    # PHASE 2 — Combine territories into retention classes
    # ------------------------------------------------------------------
    # lvI[rc] = (indemnity_matrix, freq_vector)
    # lvD[rc] = (defence_matrix,   freq_vector)
    lvI: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    lvD: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    for rc in retention_classes:
        rc_territories = model_params[model_params["Class"] == rc]["Area"].tolist()

        combined_ind_mat: np.ndarray | None = None
        combined_def_mat: np.ndarray | None = None
        combined_freq: np.ndarray | None = None

        for i, terr in enumerate(rc_territories):
            ind_mat, freq = territory_indemnity[terr]
            def_mat, _ = territory_defence[terr]

            if i == 0:
                combined_ind_mat = ind_mat.copy()
                combined_def_mat = def_mat.copy()
                combined_freq = freq.copy()
            else:
                # Stack claims rows; frequencies are additive
                combined_ind_mat = np.vstack([combined_ind_mat, ind_mat])
                combined_def_mat = np.vstack([combined_def_mat, def_mat])
                combined_freq = combined_freq + freq

        # Sort all rows so non-zero claims are at the top (order by defence
        # descending so both ind and def stay aligned)
        n_rows, _ = combined_def_mat.shape
        for k in range(num_sims):
            order = np.argsort(combined_def_mat[:, k])[::-1]  # descending
            combined_def_mat[:, k] = combined_def_mat[order, k]
            combined_ind_mat[:, k] = combined_ind_mat[order, k]

        # Randomly shuffle the non-zero claims within each simulation
        # (so the order isn't just "largest first")
        for k in range(num_sims):
            n = int(combined_freq[k])
            if n > 0:
                perm = rng.permutation(n)
                combined_def_mat[:n, k] = combined_def_mat[perm, k]
                combined_ind_mat[:n, k] = combined_ind_mat[perm, k]

        # Truncate to max rows actually needed
        max_n = int(combined_freq.max()) if combined_freq.max() > 0 else 1
        combined_def_mat = combined_def_mat[:max_n, :]
        combined_ind_mat = combined_ind_mat[:max_n, :]

        # Combined = indemnity + defence
        combined_mat = combined_def_mat + combined_ind_mat

        lvI[rc] = (combined_ind_mat, combined_freq)
        lvD[rc] = (combined_def_mat, combined_freq)
        # Store combined under the same key structure
        lvI[rc + "__combined"] = (combined_mat, combined_freq)

    # ------------------------------------------------------------------
    # PHASE 3 — Apply retentions
    # ------------------------------------------------------------------
    # We need two full loss matrices:
    #   costsinc_matrix  — for "Costs inclusive" quotes (DCIA="No")
    #   indemnity_matrix / defence_matrix — for DCIA quotes

    costsinc_parts: list[np.ndarray] = []
    indemnity_parts: list[np.ndarray] = []
    defence_parts: list[np.ndarray] = []
    defence_freq_total: np.ndarray | None = None

    for i, rc in enumerate(retention_classes):
        fgu_c, freq_vec = lvI[rc + "__combined"]
        fgu_i, _ = lvI[rc]
        fgu_d, _ = lvD[rc]

        # Ensure no NaNs
        fgu_c = np.nan_to_num(fgu_c, nan=0.0)
        fgu_i = np.nan_to_num(fgu_i, nan=0.0)
        fgu_d = np.nan_to_num(fgu_d, nan=0.0)

        # Identify the matching row in DedParams
        k = ded_params.index[ded_params["Class"] == rc][0]
        eec = float(each_retention[k])
        agg = float(agg_retention[k])
        maint_b = float(initial_deductible[k])
        maint_a = float(post_agg_deductible[k])
        def_in_ret = def_costs_in_retention[k]

        # --- Costs-inclusive matrix ---
        if def_in_ret == "Yes":
            loss_ci = retention_apply3(fgu_c, eec, agg, maint_b, maint_a)
        else:
            loss_ci = retention_apply3(fgu_i, eec, agg, maint_b, maint_a) + fgu_d
        costsinc_parts.append(loss_ci)

        # --- Indemnity / defence split matrix (for DCIA) ---
        if def_in_ret == "Yes":
            result = retention_apply3(fgu_c, eec, agg, maint_b, maint_a, clms_defence=fgu_d)
            loss_i, loss_d = result
        else:
            loss_i = retention_apply3(fgu_i, eec, agg, maint_b, maint_a)
            loss_d = fgu_d

        indemnity_parts.append(loss_i)
        defence_parts.append(loss_d)

        if defence_freq_total is None:
            defence_freq_total = freq_vec.copy()
        else:
            defence_freq_total = defence_freq_total + freq_vec

    # Stack retention-class parts vertically
    costsinc_matrix = np.vstack(costsinc_parts)
    indemnity_matrix = np.vstack(indemnity_parts)
    defence_matrix_raw = np.vstack([lvD[rc][0] for rc in retention_classes])

    # Fix: defence_matrix in the DCIA path should be the raw (pre-retention)
    # defence costs — matching R's `defense_matrix <- rbind(defense_matrix, lvD[[2*i-1]])`
    # for i > 1 in the DCIA loop.  indemnity_parts already has retention applied.
    defence_matrix = defence_matrix_raw

    # ------------------------------------------------------------------
    # PHASE 4 — Re-order rows so non-zero losses are at the top
    #           (using defence as the sort key, matching R logic)
    # ------------------------------------------------------------------
    if num_retention_classes > 1:
        end_row = defence_matrix.shape[0]
        for j in range(num_sims):
            nonzero_mask = defence_matrix[:, j] > 0
            nz_ind = indemnity_matrix[nonzero_mask, j]
            nz_ci = costsinc_matrix[nonzero_mask, j]
            nz_def = defence_matrix[nonzero_mask, j]
            nz_count = int(nonzero_mask.sum())

            indemnity_matrix[:end_row, j] = np.concatenate(
                [nz_ind, np.zeros(end_row - nz_count)]
            )
            costsinc_matrix[:end_row, j] = np.concatenate(
                [nz_ci, np.zeros(end_row - nz_count)]
            )
            defence_matrix[:end_row, j] = np.concatenate(
                [nz_def, np.zeros(end_row - nz_count)]
            )

    # Randomise order of non-zero losses per simulation
    for k in range(num_sims):
        n = int(defence_freq_total[k])
        if n > 0:
            perm = rng.permutation(n)
            defence_matrix[:n, k] = defence_matrix[perm, k]
            indemnity_matrix[:n, k] = indemnity_matrix[perm, k]
            costsinc_matrix[:n, k] = costsinc_matrix[perm, k]

    # Trim to max rows needed
    max_def = int(defence_freq_total.max()) if defence_freq_total.max() > 0 else 1
    defence_matrix = defence_matrix[:max_def, :]
    indemnity_matrix = indemnity_matrix[:max_def, :]
    costsinc_matrix = costsinc_matrix[:max_def, :]

    # ------------------------------------------------------------------
    # PHASE 5 — Apply quote structures
    # ------------------------------------------------------------------
    results_each_quote: list[np.ndarray] = []  # shape (4, num_sims) each
    results_each_add_quote: list[np.ndarray] = []

    for q in range(num_quotes):
        res = apply_quotes(
            ci_losses=costsinc_matrix,
            ind_losses=indemnity_matrix,
            def_costs=defence_matrix,
            le=float(each_limit[q]),
            xe=float(each_excess[q]),
            xa=float(agg_excess[q]),
            la=float(agg_limit[q]),
            rtcl=float(rtc_limit[q]),
            rtca=float(rtc_agg_limit[q]),
            dcia=str(dcia_flag[q]),
        )
        results_each_quote.append(res.T)  # transpose to (num_sims, 4)

    for q in range(num_add_quotes):
        res = apply_quotes(
            ci_losses=costsinc_matrix,
            ind_losses=indemnity_matrix,
            def_costs=defence_matrix,
            le=float(add_each_limit[q]),
            xe=float(add_each_excess[q]),
            xa=float(add_agg_excess[q]),
            la=float(add_agg_limit[q]),
            rtcl=float(add_rtc_limit[q]),
            rtca=float(add_rtc_agg_limit[q]),
            dcia=str(add_dcia_flag[q]),
        )
        results_each_add_quote.append(res.T)

    # ------------------------------------------------------------------
    # PHASE 6 — Aggregate outputs
    # ------------------------------------------------------------------
    # outputs[q] row: [mean_losses, mean_ind_freq, mean_def_freq, mean_exhaustion]
    # R indexing: col1=mean losses, col2=ind freq, col3=def freq, col4=exhaustion
    # results_each_quote[q] shape: (num_sims, 4)
    #   col 0 = ind count, col 1 = total losses, col 2 = def count, col 3 = exhaustion

    n_tower = len(results_each_quote)
    outputs = np.zeros((n_tower, 4))
    for q, res in enumerate(results_each_quote):
        outputs[q, 0] = res[:, 1].mean()   # mean total losses (book rate numerator)
        outputs[q, 1] = res[:, 0].mean()   # mean indemnity freq
        outputs[q, 2] = res[:, 2].mean()   # mean defence freq
        outputs[q, 3] = res[:, 3].mean()   # mean exhaustion probability

    n_add = len(results_each_add_quote)
    add_outputs = np.zeros((n_add, 4))
    for q, res in enumerate(results_each_add_quote):
        add_outputs[q, 0] = res[:, 1].mean()
        add_outputs[q, 1] = res[:, 0].mean()
        add_outputs[q, 2] = res[:, 2].mean()
        add_outputs[q, 3] = res[:, 3].mean()

    # Book rate = mean losses / (revenue / 1e6)
    book_rate = outputs[:, 0] / (revenue / 1e6)

    model_outputs = np.zeros((n_tower, 4))
    model_outputs[:, 0] = book_rate
    model_outputs[:, 1] = (outputs[:, 1] / revenue) * 1_000_000
    model_outputs[:, 2] = (outputs[:, 2] / revenue) * 1_000_000
    model_outputs[:, 3] = outputs[:, 3]

    add_model_outputs = np.zeros((n_add, 4))
    if n_add > 0:
        add_book_rate = add_outputs[:, 0] / (revenue / 1e6)
        add_model_outputs[:, 0] = add_book_rate
        add_model_outputs[:, 1] = (add_outputs[:, 1] / revenue) * 1_000_000
        add_model_outputs[:, 2] = (add_outputs[:, 2] / revenue) * 1_000_000
        add_model_outputs[:, 3] = add_outputs[:, 3]

    # Column names match R comments in simulation.r:
    #   col1 = exposure premium per lawyer  -> BookRate
    #   col2 = freq per 1000                -> FreqPer1000
    #   col3 = freq per 1000 (defense fgu)  -> DefFreqFGUPer1000
    #   col4 = exhaustion probability       -> ExhaustionProb
    _cols = ["BookRate", "FreqPer1000", "DefFreqFGUPer1000", "ExhaustionProb"]

    return (
        pd.DataFrame(model_outputs, columns=_cols),
        pd.DataFrame(add_model_outputs, columns=_cols),
    )


# ---------------------------------------------------------------------------
# Input helpers — build the expected DataFrames from dicts for convenience
# ---------------------------------------------------------------------------

def make_ded_params(rows: list[dict]) -> pd.DataFrame:
    """
    Construct a DedParams DataFrame from a list of dicts.

    Each dict must have keys: Class, EEC, aggRet, InitialMaintenance,
    MaintenanceThereafter, AppliesDefence.
    """
    df = pd.DataFrame(rows)
    df["EEC"] = pd.to_numeric(df["EEC"])
    df["aggRet"] = pd.to_numeric(df["aggRet"])
    df["InitialMaintenance"] = pd.to_numeric(df["InitialMaintenance"])
    df["MaintenanceThereafter"] = pd.to_numeric(df["MaintenanceThereafter"])
    return df.reset_index(drop=True)


def make_model_params(rows: list[dict]) -> pd.DataFrame:
    """
    Construct a ModelParams DataFrame from a list of dicts.

    Each dict must have keys: Area, Class, En, mu, sigma, DCp1.
    """
    df = pd.DataFrame(rows)
    for col in ["En", "mu", "sigma", "DCp1"]:
        df[col] = pd.to_numeric(df[col])
    return df.reset_index(drop=True)


def make_quotes_params(rows: list[dict]) -> pd.DataFrame:
    """
    Construct a QuotesParams DataFrame from a list of dicts.

    Each dict must have keys: Leec, Lagg, Xeec, Xagg, RTC_Lim, RTC_Agg, DCIA.
    Pass an empty list to indicate no quote layers.
    """
    cols = ["Leec", "Lagg", "Xeec", "Xagg", "RTC_Lim", "RTC_Agg", "DCIA"]
    if not rows:
        return pd.DataFrame(columns=cols)
    df = pd.DataFrame(rows)
    for col in ["Leec", "Lagg", "Xeec", "Xagg", "RTC_Lim", "RTC_Agg"]:
        df[col] = pd.to_numeric(df[col])
    return df.reset_index(drop=True)