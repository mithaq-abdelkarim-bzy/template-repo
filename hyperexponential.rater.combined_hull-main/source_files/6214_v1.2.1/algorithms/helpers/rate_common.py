import hx
import math
import pandas as pd
import algorithms.rate_constants as constants


def calculate_technical_premium(premium, written_line, commission):
    # TODO ADD currency conversion
    try:
        if (
            (not written_line)
            or (written_line == 0)
            or (not commission)
            or (commission == 1)
        ):
            return 0

        # Currency conversion for fixed expense
        fixed_expense_converted = constants.hull_fixed_expense

        # Step 1: Calculate Adjusted Premium
        adjusted_premium = (
            premium * (1 - commission) * constants.benchmark_lr * written_line
        )

        # Step 2: Add Hull CHE
        adjusted_premium_with_che = adjusted_premium * (1 + constants.hull_che)

        # Step 3: Add Fixed Expense
        total_premium = adjusted_premium_with_che + fixed_expense_converted

        # Step 4: Calculate Denominator
        denominator = (
            1
            - constants.hull_variable_expense
            - constants.hull_ri_cost
            - (constants.hull_roc * constants.hull_cir)
            + constants.hull_inv_income
        )

        # Step 5: Divide Total Premium by Denominator
        premium_after_division = total_premium / denominator

        # Step 6: Divide by Written Line
        premium_per_written_line = premium_after_division / written_line

        # Step 7: Final Division by (1 - Commission)
        final_premium = premium_per_written_line / (1 - commission)

        return final_premium
    except Exception:
        return 0


def calculate_final_achieved_net_rate(df, criteria_column, coverage_factor_column):
    if df.empty or (criteria_column not in df.columns):
        return pd.Series(dtype=float)

    return df[criteria_column] * df[coverage_factor_column]


def MBBEFDG3(c, x):
    """
    Calculates the rate modelling for a given value of c and x.

    Parameters:
    c (float): The value of c.
    x (float): The value of x.

    Returns:
    float: The calculated rate modelling value, or None if an error occurs.
    """
    try:
        b = math.exp(3.1 - 0.15 * (1 + c) * c)
        g = math.exp((0.78 + 0.12 * c) * c)

        if g == 1:
            return x
        elif b == 1 and g > 1:
            return math.log(1 + (g - 1) * x) / math.log(g)
        elif b * g == 1 and g > 1:
            return (1 - b**x) / (1 - b)
        elif b > 0 and b != 1 and b * g != 1 and g > 1:
            return math.log(
                ((g - 1) * b + (1 - g * b) * (b**x)) / (1 - b)
            ) / math.log(g * b)
        else:
            return 0
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        hx.errors.validation(f"Error in MBBEFDG3 calculation: {e}")
        return 0
