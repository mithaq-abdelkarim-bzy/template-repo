import hx
import pandas as pd
import numpy as np
from scipy.stats import norm

_ILF_TABLE_CACHE: dict[int, dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]] = {}
 
 
def _prepare_ilf_table(ilf_table: pd.DataFrame) -> dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    cache_id = id(ilf_table)
    cached = _ILF_TABLE_CACHE.get(cache_id)
    if cached is not None:
        return cached
 
    table = ilf_table.copy()
    table["curve"] = table["curve"].astype(str).str.strip()
 
    prepared: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = {}
    for curve_name, group in table.groupby("curve", sort=False):
        group_sorted = group.sort_values("LimitLow").reset_index(drop=True)
        limit_low = group_sorted["LimitLow"].to_numpy(dtype=float)
        limit_high = group_sorted["LimitHigh"].to_numpy(dtype=float)
        ilf = group_sorted["Ilf"].to_numpy(dtype=float)
        next_ilf = np.concatenate([ilf[1:], ilf[-1:]])
        prepared[curve_name] = (limit_low, limit_high, ilf, next_ilf)
 
    _ILF_TABLE_CACHE[cache_id] = prepared
    return prepared

def ilfa(
        x: pd.Series,
        c_type: pd.Series,
        p1: pd.Series,
        p2: pd.Series,
        p3: pd.Series,
        p4: pd.Series,
    ) -> pd.Series:
    """
    Vectorized ILFA calculation for pandas Series (DataFrame columns).

    Args:
        x: Input Series (must be >= 0.01)
        c_type: Series of curve types (e.g., "MMF", "Rational", etc.)
        p1, p2, p3, p4: Parameter Series for the curve
    Returns:
        ILFA Series
    """
    
    
    x = pd.Series(x)
    # x = x.clip(min=0.01)
    x = x.clip(lower=0.01)
    x_norm = x / 1_000_000  # Normalize by 1,000,000

    result = pd.Series(np.nan, index=x.index)

    # MMF
    mmf_mask = c_type == "MMF"
    if mmf_mask.any():
        result.loc[mmf_mask] = (p1[mmf_mask] + p2[mmf_mask] * (x_norm[mmf_mask] ** p3[mmf_mask])) / (p4[mmf_mask] + (x_norm[mmf_mask] ** p3[mmf_mask]))

    # Rational
    rational_mask = c_type == "Rational"
    if rational_mask.any():
        result.loc[rational_mask] = (p1[rational_mask] + p2[rational_mask] * x_norm[rational_mask]) / (
            1 + p3[rational_mask] * x_norm[rational_mask] + p4[rational_mask] * (x_norm[rational_mask] ** 2)
        )

    # Vapour pressure
    vapour_mask = c_type == "Vapour pressure"
    if vapour_mask.any():
        result.loc[vapour_mask] = np.exp(p1[vapour_mask] + p2[vapour_mask] / x_norm[vapour_mask] + p3[vapour_mask] * np.log(x_norm[vapour_mask]))

    # Weibull
    weibull_mask = c_type == "Weibull"
    if weibull_mask.any():
        result.loc[weibull_mask] = p1[weibull_mask] + p2[weibull_mask] * np.exp(p3[weibull_mask] * (x_norm[weibull_mask] ** p4[weibull_mask]))

    # LogNormal_Extended
    lognorm_ext_mask = c_type == "LogNormal_Extended"
    if lognorm_ext_mask.any():
        mu = p1[lognorm_ext_mask] + p2[lognorm_ext_mask] * np.log(p4[lognorm_ext_mask]) - 0.5 * p3[lognorm_ext_mask]**2 + np.log(1.2)
        si = p3[lognorm_ext_mask]
        result.loc[lognorm_ext_mask] = (
            np.exp(mu + 0.5 * si**2) * norm.cdf(np.log(x[lognorm_ext_mask]), loc=mu + si**2, scale=si) +
            x[lognorm_ext_mask] * (1 - norm.cdf(np.log(x[lognorm_ext_mask]), loc=mu, scale=si))
        )

    # LogNormal
    lognorm_mask = c_type == "LogNormal"
    if lognorm_mask.any():
        mu, si = p1[lognorm_mask], p2[lognorm_mask]
        result.loc[lognorm_mask] = (
            np.exp(mu + 0.5 * si**2) * norm.cdf(np.log(x[lognorm_mask]), loc=mu + si**2, scale=si) +
            x[lognorm_mask] * (1 - norm.cdf(np.log(x[lognorm_mask]), loc=mu, scale=si))
        )

    mbbefd_mask = c_type == "MBBEFD"
    if mbbefd_mask.any():
        g, b = p1[mbbefd_mask], p2[mbbefd_mask]
        x_clip = x[mbbefd_mask].clip(upper=1)

        # All masks are now relative to the mbbefd_mask subset
        mask_g1 = g == 1
        mask_b1_g1 = (b == 1) & (g > 1)
        mask_bg1_g1 = (b * g == 1) & (g > 1)
        mask_other = (b > 0) & (b != 1) & (b * g != 1) & (g > 1)

        # Create a copy of the subset for assignment
        result_subset = result[mbbefd_mask].copy()

        # Assign values to the subset
        result_subset[mask_g1] = x_clip[mask_g1]
        result_subset[mask_b1_g1] = np.log(1 + (g[mask_b1_g1] - 1) * x_clip[mask_b1_g1]) / np.log(g[mask_b1_g1])
        result_subset[mask_bg1_g1] = (1 - b[mask_bg1_g1]**x_clip[mask_bg1_g1]) / (1 - b[mask_bg1_g1])
        result_subset[mask_other] = (
            np.log(
                ((g[mask_other] - 1) * b[mask_other] +
                (1 - g[mask_other] * b[mask_other]) *
                (b[mask_other]**x_clip[mask_other])) /
                (1 - b[mask_other])
            ) / np.log(g[mask_other] * b[mask_other])
        )
        result_subset[~(mask_g1 | mask_b1_g1 | mask_bg1_g1 | mask_other)] = -1  # Error

        # Assign the subset back to the result
        result.loc[mbbefd_mask] = result_subset


    # Power
    power_mask = c_type == "Power"
    if power_mask.any():
        y, power = p1[power_mask], p2[power_mask]
        alpha = np.log(power) / np.log(2)
        l, r = 1_000_000, 100_000
        k = x[power_mask] / y
        k0 = l / r
        k1 = y / r
        result.loc[power_mask] = k1**alpha * ((1 + k)**alpha - 1) / ((1 + k0)**alpha - 1)

    # Restricted Benktander
    benktander_mask = c_type == "Restricted Benktander"
    if benktander_mask.any():
        s, a, k = p1[benktander_mask], p2[benktander_mask], p3[benktander_mask]
        result.loc[benktander_mask] = k + s / np.sqrt(a) * (1 - np.exp(-2 * np.sqrt(a) * (np.sqrt(1 + (x[benktander_mask] - k) / s) - 1)))

    # Check for unknown curve types
    if result.isna().any():
        unknown_mask = result.isna()
        unknown_c_types = c_type[unknown_mask].unique()
        raise ValueError(f"Unknown curve type(s): {unknown_c_types}")

    return result


def ilftab2_old(
        x: pd.Series,
        curve: pd.Series,
        ilf_table: pd.DataFrame,
    ) -> pd.Series:
    """
    Vectorized ILF table lookup and interpolation for pandas Series.

    Args:
        x: Input Series (limit values)
        curve: Series of curve names (must match values in the 'curve' column of the table)
        ilf_table: DataFrame containing the ILF table (columns: 'LimitLow', 'LimitHigh', 'curve', 'Ilf')
    Returns:
        Interpolated ILF Series
    """
    x = pd.Series(x)
    x = x.clip(lower=0.01)  # avoid errors if excess = 0
    result = pd.Series(index=x.index, dtype=float)

    for i, (val, curve_name) in enumerate(zip(x, curve)):
        # Find the band where LimitLow <= val <= LimitHigh for the given curve
        if curve_name is not None and curve_name != "":
        
            curve_mask = ilf_table["curve"].astype(str).str.strip() == curve_name
 
            if not curve_mask.any():
                hx.errors.fatal(f"ILF curve '{curve_name}' not found in table_ilf_tabular.")
            
            band_mask = curve_mask & (
                (ilf_table["LimitLow"] <= val) & (ilf_table["LimitHigh"] >= val)
            )
            
            # if not band_mask.any():
            #     hx.errors.validation(
            #         f"No ILF band for curve '{curve_name}' covering limit {val}."
            #     )

            band = ilf_table[
                (ilf_table['curve'] == curve_name) &
                (ilf_table['LimitLow'] <= val) &
                (ilf_table['LimitHigh'] >= val)
            ]
            
            if band.empty:
                # If no band is found, use the last band for the curve
                band = ilf_table[ilf_table['curve'] == curve_name].iloc[[-1]] # get the highest band   

            limit_low = band['LimitLow'].values[0]
            limit_high = band['LimitHigh'].values[0]

            # Get the Ilf values for the band
            ilf_low = band['Ilf'].values[0]
            try:
                ilf_high = ilf_table[
                    (ilf_table['curve'] == curve_name) &
                    (ilf_table['LimitLow'] == band['LimitHigh'].values[0])
                ]['Ilf'].values[0]
            except:
                ilf_high = ilf_table[(ilf_table['curve'] == curve_name)]['Ilf'].values[-1]

            # Linear interpolation
            # m = (val - limit_low) / (limit_high - limit_low)
            # result.iloc[i] = (1 - m) * ilf_low + m * ilf_high

            if val == 0:
                result.iloc[i] = 0
            else:
                m = (val - limit_low) / (limit_high - limit_low)
                result.iloc[i] = (1 - m) * ilf_low + m * ilf_high

        else:
            result.iloc[i] = 1

    return result

def ilftab2(
        x: pd.Series,
        curve: pd.Series,
        ilf_table: pd.DataFrame,
    ) -> pd.Series:
    """
    Vectorised ILF table lookup using pre-filtered per-curve tables.
    """
    if len(x) == 0:
        return pd.Series(dtype=float)
 
    table_map = _prepare_ilf_table(ilf_table)
 
    raw_x_series = pd.Series(x).astype(float)
    zero_mask = raw_x_series == 0
    x_series = raw_x_series.clip(lower=0.01)
    curve_series = (
        pd.Series(curve)
        .fillna("")
        .astype(str)
        .str.strip()
        .replace({"None": "", "nan": ""})
    )
 
    result = pd.Series(index=x_series.index, dtype=float)
 
    blank_mask = curve_series == ""
    if blank_mask.any():
        result.loc[curve_series.index[blank_mask]] = 1.0
 
    non_blank = curve_series[~blank_mask]
 
    for curve_name, idx_series in non_blank.groupby(non_blank):
        curve_data = table_map.get(curve_name)
        if curve_data is None:
            hx.errors.fatal(f"ILF curve '{curve_name}' not found in table_ilf_tabular.")
 
        limit_low, limit_high, ilf_low, ilf_high = curve_data
        x_values = x_series.loc[idx_series.index].to_numpy(dtype=float)
 
        positions = np.searchsorted(limit_low, x_values, side="right") - 1
        positions = np.clip(positions, 0, len(limit_low) - 1)
 
        lower = limit_low[positions]
        upper = limit_high[positions]
 
        out_of_range = (x_values < lower) | (x_values > upper)
        # if out_of_range.any():
        #     offending = float(x_values[out_of_range][0])
        #     hx.errors.validation(
        #         f"No ILF band for curve '{curve_name}' covering limit {offending}."
        #     )
 
        denom = upper - lower
        ratios = np.zeros_like(x_values, dtype=float)
        positive_span = denom > 0
        ratios[positive_span] = (x_values[positive_span] - lower[positive_span]) / denom[positive_span]
        ratios = np.clip(ratios, 0.0, 1.0)
 
        interpolated = (1 - ratios) * ilf_low[positions] + ratios * ilf_high[positions]

        curve_zero_mask = zero_mask.loc[idx_series.index].to_numpy(dtype=bool)
        if curve_zero_mask.any():
            interpolated = np.where(curve_zero_mask, 0.0, interpolated)

        result.loc[idx_series.index] = interpolated
 
    return result
