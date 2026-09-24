"""
rate_simulation_helpers.py
-------------------
Python port of key actuarial rating functions from RatingFunctions.r.

Matrix convention throughout:
    axis 0 (rows)    = claims / time steps
    axis 1 (columns) = simulations

R pmin/pmax  ->  np.minimum / np.maximum
apply(X, 2, cumsum)  ->  np.cumsum(X, axis=0)
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def n_sir_exhaustion(losses_q_agg: np.ndarray, la: float) -> np.ndarray:
    """
    For each simulation column, find the 0-based row index of the first claim
    where the cumulative qualified losses reach (or exceed) the aggregate limit
    ``la``.

    Parameters
    ----------
    losses_q_agg : ndarray, shape (n_claims, n_sims)
        Cumulative qualified losses per simulation.
    la : float
        Aggregate limit (Layer Aggregate). When 0, no limit applies.

    Returns
    -------
    nj : ndarray, shape (n_sims,), dtype float
        0-based row index of first exhaustion, or np.nan if exhaustion never
        occurs or ``la == 0``.

    Notes
    -----
    R's ``nSirExhaustion`` returns a 1-based index; this function returns a
    0-based index to match Python conventions.
    """
    n_sims = losses_q_agg.shape[1]
    nj = np.full(n_sims, np.nan, dtype=float)

    if la == 0:
        return nj

    for j in range(n_sims):
        col = losses_q_agg[:, j]
        hits = np.where(col >= la)[0]
        if hits.size > 0:
            nj[j] = hits[0]

    return nj


# ---------------------------------------------------------------------------
# RetentionApply3
# ---------------------------------------------------------------------------

def retention_apply3(
    clms: np.ndarray,
    ret: float,
    agg_ret: float = 0.0,
    maint_before: float = 0.0,
    maint_after: float = 0.0,
    clms_defence: np.ndarray | None = None,
) -> np.ndarray | tuple[np.ndarray, np.ndarray]:
    """
    Apply a per-claim retention and optional aggregate retention to a claims
    matrix, optionally with maintenance deductibles that switch before/after
    aggregate exhaustion.

    Port of ``RetentionApply3`` in RatingFunctions.r.

    Parameters
    ----------
    clms : ndarray, shape (n_claims, n_sims)
        Ground-up claims matrix (rows = claim ordinal, cols = simulations).
    ret : float
        Each-and-every-claim (EEC) retention.
    agg_ret : float, optional
        Aggregate retention cap. ``0`` means no aggregate limit (treated as
        ``Inf``). Default 0.
    maint_before : float, optional
        Maintenance deductible applied before aggregate is exhausted.
        Default 0.
    maint_after : float, optional
        Maintenance deductible applied after aggregate is exhausted.
        Default 0.
    clms_defence : ndarray or None, optional
        Defence costs matrix, same shape as ``clms``. When provided the
        function returns a tuple.

    Returns
    -------
    loss : ndarray or tuple of ndarray
        If ``clms_defence`` is None: ndarray of shape ``(n_claims, n_sims)``
        with the net losses above the combined retention + maintenance.

        If ``clms_defence`` is provided: tuple
        ``(indemnity_net, defence_net)`` where each element has shape
        ``(n_claims, n_sims)``.
    """
    # Edge case: empty claims matrix
    if clms.shape[0] == 0:
        return np.zeros_like(clms)

    # Normalise aggregate retention: 0 means no limit -> Inf
    if agg_ret == 0 or np.isnan(agg_ret):
        agg_ret = np.inf

    # Normalise maintenance deductibles
    if np.isnan(maint_before):
        maint_before = 0.0
    if np.isnan(maint_after):
        maint_after = 0.0

    n_claims, n_sims = clms.shape

    # Step 1: claims net of the maintenance deductible that applies before
    #         aggregate exhaustion
    clms_post_deductible = np.maximum(clms - maint_before, 0.0)

    # Step 2: per-claim contribution toward aggregate retention
    #         (capped at EEC retention)
    contribution_to_agg = np.minimum(clms_post_deductible, ret)

    # Step 3: cumulative contribution to aggregate (column-wise cumsum)
    #         then cap at aggregate retention
    contribution_to_agg_cum = np.cumsum(contribution_to_agg, axis=0)
    agg_ret_cum = np.minimum(contribution_to_agg_cum, agg_ret)

    # Step 4: build "agg_ret_cum at start of each claim row" by prepending a
    #         zeros row and dropping the last row (shift down by one)
    agg_ret_cum_start = np.vstack(
        [np.zeros((1, n_sims)), agg_ret_cum[:-1, :]]
    )

    # Step 5: per-claim retention = diff of capped cumulative sums
    #         Using prepend=zeros is equivalent to the R loop and matches the
    #         explicit Retention[1,] / Retention[i+1,] construction.
    retention = np.diff(agg_ret_cum, axis=0, prepend=np.zeros((1, n_sims)))

    # Step 6: maintenance deductible for each claim-row depends on whether
    #         the aggregate retention was already exhausted at the START of
    #         that claim.
    maintenance = np.where(agg_ret_cum_start < agg_ret, maint_before, maint_after)

    # Step 7: net loss = max(gross - (per-claim retention + maintenance), 0)
    loss_net_retention = np.maximum(clms - (retention + maintenance), 0.0)

    if clms_defence is not None:
        # Defence costs similarly net of retention + maintenance
        loss_defence = np.maximum(clms_defence - (retention + maintenance), 0.0)
        return loss_net_retention - loss_defence, loss_defence

    return loss_net_retention


# ---------------------------------------------------------------------------
# ApplyQuotes
# ---------------------------------------------------------------------------

def apply_quotes(
    ci_losses: np.ndarray,
    ind_losses: np.ndarray,
    def_costs: np.ndarray,
    le: float,
    xe: float = 0.0,
    xa: float = 0.0,
    la: float = 0.0,
    rtcl: float = 0.0,
    rtca: float = 0.0,
    dcia: str = "No",
) -> np.ndarray:
    """
    Apply a reinsurance/excess-of-loss quote structure to a claims matrix.

    Port of ``ApplyQuotes`` in RatingFunctions.r.

    Parameters
    ----------
    ci_losses : ndarray, shape (n_claims, n_sims)
        Combined-indemnity (CI) losses — used when ``dcia="No"``.
    ind_losses : ndarray, shape (n_claims, n_sims)
        Indemnity-only losses — used when ``dcia="Yes"``.
    def_costs : ndarray, shape (n_claims, n_sims)
        Defence cost losses — only relevant when ``dcia="Yes"``.
    le : float
        Layer limit (limit per each claim excess of ``xe``).
    xe : float, optional
        Per-claim excess / attachment. Default 0.
    xa : float, optional
        Aggregate excess / attachment. ``Inf`` is valid. Default 0.
    la : float, optional
        Layer aggregate limit. ``0`` means no aggregate limit. Default 0.
    rtcl : float, optional
        Reinstatement / RTC per-claim limit. ``0`` means non-RTC path.
        Default 0.
    rtca : float, optional
        Reinstatement / RTC aggregate. Default 0.
    dcia : str, optional
        "Yes" or "No". When "Yes", indemnity and defence are handled
        separately and merged with a proportional ratio. Default "No".

    Returns
    -------
    final_results : ndarray, shape (4, n_sims)
        Row 0 : indemnity loss count per simulation (or DCIA total count).
        Row 1 : total qualified losses per simulation.
        Row 2 : defence frequency per simulation (non-zero only when
                ``dcia="Yes"``).
        Row 3 : aggregate-exhaustion indicator (1 if exhausted, else 0).
    """
    # Select base losses depending on DCIA flag
    if dcia == "Yes":
        losses = ind_losses.copy()
    else:
        losses = ci_losses.copy()

    n_claims, n_sims = losses.shape

    # -----------------------------------------------------------------------
    # RTC cap on individual claims and cumulative tracking
    # -----------------------------------------------------------------------
    if rtcl != 0:
        losses = np.minimum(losses, rtcl)

    losses_agg_rtc = np.cumsum(losses, axis=0)

    # Effective RTCA is at least RTCL
    rtca_eff = max(rtcl, rtca)

    if rtcl == 0:
        losses_t = losses.copy()
    else:
        # Losses_t = Losses + RTCA - Losses_Agg_RTC, clipped at 0,
        # but reverting to original for rows where cumulative <= RTCA
        losses_t = losses + rtca_eff - losses_agg_rtc
        losses_t = np.maximum(losses_t, 0.0)
        mask_below = losses_agg_rtc <= rtca_eff
        losses_t[mask_below] = losses[mask_below]

    # -----------------------------------------------------------------------
    # Non-RTC path
    # -----------------------------------------------------------------------
    if rtcl == 0:
        # agg_xs_remaining tracks the remaining aggregate excess "bucket" as claims
        # are consumed.  Shape (n_claims+1, n_sims): row 0 is the initial
        # excess, rows 1..n_claims are residuals after each claim.

        # the agg_xs_remaining bucket requires a finite starting number - arithmetic can't be done on infinity.  
        # So when no aggregate excess is specified (xa = np.inf, meaning "unlimited"), the code substitutes 10_000 * xe as a stand in for "effectively infinite"
        # Each individual claim is capped at xe (the each-excess), so the maximum a single claim could consume from the agg bucket is xe
        # Multiplying by 10_000 means the bucket could absorb 10_000 full-sized claims before being exhausted - effectively infinity for our purposes.
        xa_init = (10_000 * xe) if xa == np.inf else xa
        agg_xs_remaining = np.zeros((n_claims + 1, n_sims))
        agg_xs_remaining[0, :] = xa_init

        losses_q = np.zeros_like(losses)

        for i in range(n_claims):
            # Consume per-claim loss from the aggregate excess bucket
            agg_xs_remaining[i + 1, :] = np.maximum(
                agg_xs_remaining[i, :] - np.minimum(losses[i, :], xe if xe > 0 else losses[i, :]),
                0.0,
            )
            losses_q[i, :] = losses_t[i, :] - (agg_xs_remaining[i, :] - agg_xs_remaining[i + 1, :])

        losses_q = np.maximum(losses_q, 0.0)
        losses_q = np.minimum(losses_q, le)

        losses_q_agg = np.cumsum(losses_q, axis=0)

    # -----------------------------------------------------------------------
    # RTC path
    # -----------------------------------------------------------------------
    else:
        no_of_shots = rtca_eff / rtcl
        remainder_no_of_shots = no_of_shots - np.floor(no_of_shots)
        losses_cum = np.cumsum(losses_t, axis=0)
        losses_temp = np.zeros_like(losses_t)
        rws = n_claims

        for j in range(n_sims):
            if losses_cum[-1, j] <= 0:
                continue

            index = 0  # will be set inside the loop

            for i in range(1, int(np.ceil(no_of_shots)) + 1):
                loop_attach = rtcl * (i - 1) + xe
                loop_detach = rtcl * (i - 1) + le + xe

                if i <= no_of_shots:
                    # Full reinstatement
                    losses_temp[0, j] += np.maximum(
                        np.minimum(losses_cum[0, j], loop_detach)
                        - np.maximum(0.0, loop_attach),
                        0.0,
                    )
                    if rws > 1:
                        losses_temp[1:rws, j] += np.maximum(
                            np.minimum(losses_cum[1:rws, j], loop_detach)
                            - np.maximum(losses_cum[0 : rws - 1, j], loop_attach),
                            0.0,
                        )
                else:
                    # Partial reinstatement (remainder fraction)
                    losses_temp[0, j] += np.maximum(
                        np.minimum(losses_cum[0, j], loop_detach)
                        - np.maximum(0.0, loop_attach),
                        0.0,
                    )

                    if index > 1 and rws > 1:
                        losses_temp[1 : index - 1, j] += np.maximum(
                            np.minimum(losses_cum[1 : index - 1, j], loop_detach)
                            - np.maximum(losses_cum[0 : index - 2, j], loop_attach),
                            0.0,
                        )
                    # bug fix here
                    start = max(index, 1)
                    if start < rws:
                        losses_temp[start:rws, j] += (
                            np.maximum(
                                np.minimum(losses_cum[start:rws, j], loop_detach)
                                - np.maximum(
                                    losses_cum[start - 1 : rws - 1, j], loop_attach
                                ),
                                0.0,
                            )
                            * remainder_no_of_shots
                        )

                #     if index < rws:
                #         losses_temp[index:rws, j] += (
                #             np.maximum(
                #                 np.minimum(losses_cum[index:rws, j], loop_detach)
                #                 - np.maximum(
                #                     losses_cum[index - 1 : rws - 1, j], loop_attach
                #                 ),
                #                 0.0,
                #             )
                #             * remainder_no_of_shots
                #         )

                # Find first zero entry to update index (R: which(Losses_Temp[,j]==0)[1])
                zero_rows = np.where(losses_temp[:, j] == 0)[0]
                index = int(zero_rows[0]) if zero_rows.size > 0 else rws

        losses_q = losses_temp
        losses_q = np.maximum(losses_q, 0.0)
        losses_q_agg = np.cumsum(losses_q, axis=0)

    # -----------------------------------------------------------------------
    # Aggregate limit (LA) application
    # -----------------------------------------------------------------------
    nj = n_sir_exhaustion(losses_q_agg, la)  # 0-based exhaustion row per sim

    if la > 0:
        nc = n_claims
        for i in range(n_sims):
            if not np.isnan(nj[i]):
                row = int(nj[i])
                # Trim the exhaustion-row loss so cumulative exactly equals LA
                losses_q[row, i] += la - losses_q_agg[row, i]

        # Recompute cumulative after adjustment
        losses_q_agg2 = np.cumsum(losses_q, axis=0)
        # Zero out anything above LA (with a rounding tolerance of 5)
        losses_q[losses_q_agg2 > (la + 5)] = 0.0

    # Indemnity count = number of positive loss entries per simulation
    ind_loss_count = np.sum(losses_q > 0, axis=0).astype(float)

    # -----------------------------------------------------------------------
    # DCIA: proportional allocation of defence costs
    # -----------------------------------------------------------------------
    if dcia == "Yes":
        # q_ratio = losses_q / losses; handle division by zero -> nan
        with np.errstate(divide="ignore", invalid="ignore"):
            q_ratio = np.where(losses != 0, losses_q / losses, np.nan)

        # Fill nan based on whether there is an excess
        if xe > 0 and rtcl == 0:
            q_ratio = np.where(np.isnan(q_ratio), 0.0, q_ratio)
        else:
            q_ratio = np.where(np.isnan(q_ratio), 1.0, q_ratio)

        # Zero out ratio for claims after aggregate exhaustion
        nc = n_claims
        for i in range(n_sims):
            if not np.isnan(nj[i]):
                row = int(nj[i])
                if row < nc - 1:
                    q_ratio[row + 1 : nc, i] = 0.0

        losses_q = losses_q + def_costs * q_ratio
        def_loss_count = np.sum(losses_q > 0, axis=0).astype(float)
    else:
        def_loss_count = np.zeros(n_sims, dtype=float)

    # -----------------------------------------------------------------------
    # Assemble final results matrix
    # -----------------------------------------------------------------------
    final_results = np.zeros((4, n_sims), dtype=float)
    final_results[0, :] = ind_loss_count
    final_results[1, :] = np.sum(losses_q, axis=0)
    final_results[2, :] = def_loss_count
    final_results[3, :] = (~np.isnan(nj)).astype(float)

    return final_results