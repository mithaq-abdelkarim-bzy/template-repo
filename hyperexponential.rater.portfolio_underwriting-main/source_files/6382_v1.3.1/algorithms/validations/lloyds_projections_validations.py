import hx


def check_summary_checked_value(checked_col):
    if (checked_col == False).any():
        hx.errors.validation("Warning: All Risk Codes (Lloyds Projections Tab) must be reviewed and marked as “Checked” before submission")

