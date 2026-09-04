import hx, math
import pandas as pd
import polars as pl
import numpy as np
from typing import Union, Sequence, Literal


# Exceedence Probability Curves
def exceedence_prob_curves(df, groupby_col, loss_col, agg_type, EP, sims):
    """Returns the exceedence probability curves (Polars version)."""
    
    if agg_type == "sum":
        df = df.groupby(groupby_col).agg(pl.col(loss_col).sum().alias(loss_col))
    elif agg_type == "max":
        df = df.groupby(groupby_col).agg(pl.col(loss_col).max().alias(loss_col))
    else:
        raise ValueError("agg_type must be 'sum' or 'max'")

    # Reindex to include all years from 1 to sims
    all_yrs = pl.DataFrame({groupby_col: list(range(1, sims + 1))})
    df = all_yrs.join(df, on=groupby_col, how='left').fill_null(0) 
   
    # Compute quantiles
    quantile_val = 1 - 1 / EP
    losses = df[loss_col].to_numpy()
    quant = np.quantile(losses, quantile_val)
    
    return pl.DataFrame({
        loss_col: quant,
        "EP": EP
    })



def calc_aal(df: pl.DataFrame, peril_code: str, sims: int) -> float:
    """ Returns the AAL for peril. """
    return (
        df.filter(pl.col("Peril") == peril_code)     # filter
          .select(pl.col("LayerLoss").sum())         # aggregate inside Polars
          .item()                                    # grab scalar result
          / sims                                     # divide in Python once
    )


def agg_losses(df: pl.DataFrame, groupby_col: str, loss_cols: Union[str, Sequence[str]], agg_type: Literal["sum", "max"]) -> pl.DataFrame:
    """ Aggregate one or more loss columns by a single group-by column.

    groupby_col: Column name to group by.
    loss_cols: One or more column names to aggregate. A single string is allowed.
    agg_type: Aggregation type either max or xum
    """
    if isinstance(loss_cols, str):
        cols = [loss_cols]
    else:
        cols = list(loss_cols)

    if len(cols) == 0:
        raise ValueError("loss_cols must contain at least one column name.")

    # Validate agg_type
    if agg_type not in ("sum", "max"):
        raise ValueError("agg_type must be either 'sum' or 'max'")

    # Build the aggregation expressions
    if agg_type == "sum":
        exprs = [pl.col(c).sum().alias(c) for c in cols]
    else:  # agg_type == "max"
        exprs = [pl.col(c).max().alias(c) for c in cols]

    # Perform the aggregation; maintain order if helpful in downstream ops
    return df.groupby(groupby_col, maintain_order=True).agg(exprs)



def marginal_impacts(df, loss_col, comb_loss_col, EP, sims):
    # Threshold for smoothing
    q = 0.05

    # Sort losses in descending order
    df = df.sort(loss_col, descending=True)

    losses = df[loss_col].to_numpy()
    comb_losses = df[comb_loss_col].to_numpy()

    # Create list to store marginal impacts
    out = []

    # Calculate marginal impacts
    for rp in EP:
        # Quantile threshold
        qloss = np.quantile(losses, 1 - 1 / rp)

        # Mask for smoothing window
        mask = (losses >= (1 - q) * qloss) & (losses <= (1 + q) * qloss)
        yrs = math.floor((np.sum(mask) - 1) / 2)

        start_pos = math.floor(sims / rp - yrs)
        end_pos = math.floor(sims / rp + yrs) + 1

        smooth_loss = np.sum(losses[start_pos:end_pos]) / (yrs * 2 + 1)
        c_smooth_loss = np.sum(comb_losses[start_pos:end_pos]) / (yrs * 2 + 1)

        m_impt = c_smooth_loss - smooth_loss

        lst = [rp, yrs, smooth_loss, c_smooth_loss, m_impt]
        out.append(lst)

    df = pd.DataFrame(out, columns=['EP', 'Yrs', 'Loss', 'CombLoss', 'MarginalImpact'])

    return df



# Calculate Standard Deviation
def calc_stddev(df, peril, AAL, n):
    """ Calculates standard deviation """
    # Optional peril filter
    if peril:
        df = df.filter(pl.col("Peril") == peril)

    # 2. aggregate annual loss
    annual = df.groupby("Yr").agg(pl.col('LayerLoss').sum().alias('LayerLoss'))

    # 3. make sure every simulated year 1…n is present (missing ⇒ 0)
    all_years = pl.DataFrame({"Yr": np.arange(1, n + 1, dtype=np.int64)})
    annual = all_years.join(annual, on="Yr", how="left").with_columns(pl.col('LayerLoss').fill_null(0))

    # Variance and standard deviation (same algebra as original)
    variance = (
        annual.select(((pl.col('LayerLoss') - AAL) ** 2).sum() / (n - 1))
              .item()
    )
    SDOut = variance ** 0.5
    return SDOut

