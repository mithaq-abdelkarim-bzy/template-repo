import hx


def check_max_limit_at_100_per_value(max_limit_at_100_per, bst_share_line_size):
    mask_limit = max_limit_at_100_per.isna()
    mask_share = bst_share_line_size.isna()
    condition  = (mask_limit & mask_share).any()
    warning    = "Warning: ”Maximum Limit @ 100%” (Premium and Limit Profile Tab) is blank. Please provide a value or ensure that a manual override to “BST Share / Line Size” has been applied."
    if condition:
        hx.errors.validation(warning)


def check_max_limit_at_bst_share_value(max_limit_at_bst_share, bst_share_line_size):
    mask_limit = max_limit_at_bst_share.isna()
    mask_share = bst_share_line_size.isna()
    condition  = (mask_limit & mask_share).any()
    warning    = "Warning: ”Maximum Limit @ BST Share” (Premium and Limit Profile Tab) is blank. Please provide a value or ensure that a manual override to “BST Share / Line Size” has been applied."
    if condition:
        hx.errors.validation(warning)


def check_future_ultimate_gross_prem_value(future_ultimate_gross_prem_col, bst_share_line_size):
    mask_prem  = future_ultimate_gross_prem_col.isna()
    mask_share = bst_share_line_size.isna()
    condition     = (mask_prem & mask_share).any()
    warning       = "Warning: ”Future Ultimate Gross Premium @100%” (Premium and Limit Profile Tab) is blank. Please provide a value or ensure that a manual override to “BST Net Premium” has been applied"
    if condition:
        hx.errors.validation(warning)
