import pandas as pd
import algorithms.rate_utilities as utils


def build_risk_codes_str(final_composition_df):
    parts = []
    for _, row in final_composition_df.iterrows():
        if pd.notna(row["risk_code"]) and pd.notna(row["composition"]):
            parts.append(f'{row["risk_code"]} ({float(row["composition"]):.1%})')
    if parts:
        return " ".join(parts) + "; See RC section for details"
    else:
        return "; See RC section for details"


def build_trifocus_string(prem_limit_df):
    return prem_limit_df.loc[prem_limit_df['portfolio_composition'].idxmax(), 'assigned_trifocus']


def build_key_lob_str(prem_limit_df):
    lobs = prem_limit_df["selected_lob"]

    return ", ".join(lobs.dropna().astype(str))


def _format_value(val: float):
    if val < 1_000_000:
        return f"{val/1_000:,.2f}k"
    else:
        return f"{val/1_000_000:,.2f}m"


def build_prem_average_limit_str(hxd):
    currency = hxd.cds.currencies.source_currency
    max_limit_at_100_per = hxd.cds.prem_limit_profile.summary.max_limit_at_100_per or 0
    avg_limit_at_100_per = hxd.cds.prem_limit_profile.summary.avg_limit_at_100_per or 0

    return f"{currency} {_format_value(max_limit_at_100_per)} / {currency} {_format_value(avg_limit_at_100_per)}"


def build_gn_prem(hxd):
    currency = hxd.cds.currencies.source_currency
    bst_net_premium = hxd.cds.prem_limit_profile.summary.bst_net_premium or 0
    bst_share_ultimate_gross_premium = hxd.cds.prem_limit_profile.summary.bst_share_ultimate_gross_premium or 0 
       
    def format_value(val: float, suffix: str) -> str:
        if val < 1_000_000:
            return f"{val/1_000:,.2f}k {suffix}"
        else:
            return f"{val/1_000_000:,.2f}m {suffix}"

    return f"{currency} {format_value(bst_share_ultimate_gross_premium, 'GROSS')} / {currency} {format_value(bst_net_premium, 'NET')}"


def build_deduction_strings(hxd, rater):
    deductions_df = rater["deductions_df"]
    prem_limit_df = rater["prem_limit_df"]

    filtered_prem_limit_df = prem_limit_df[["selected_lob", "bst_net_premium"]]

    cols = [
        {"field": "market_deductions", "label": "Market Deductions"},
        {"field": "facility_brokerage", "label": "Facility Brokerage"},
        {"field": "leaders_fee", "label": "Learders Fee"},
        {"field": "service_fee", "label": "Service Fee"},
        {"field": "other", "label": "Other"},
        {"field": "selected_effective_deductions", "label": "Total Deductions"}
    ]

    combined_df = filtered_prem_limit_df.merge(
        deductions_df[["selected_lob"] + [c["field"] for c in cols]],
        on="selected_lob",
        how="left"
    )

    deductions = {}

    for index, col in enumerate(cols, start=1): 
        deductions[col["field"]] = (
            (combined_df[col["field"]] * combined_df["bst_net_premium"]).sum()
            / combined_df["bst_net_premium"].sum()
        )
        deductions[f"ded_str_{index}"] = f"{deductions[col['field']] * 100:.2f}% - {col['label']}"

    return deductions


def generate_profit_commission_description(hxd):
    pc_structure_df = utils.pd_df_from_hx_list_v2(
        hxd.cds.pc.pc_structure.table)

    profit_commission_description = ""

    if hxd.cds.risk_information.is_profit_comission:
        pc_structure_df = pc_structure_df[pc_structure_df["selected_lob"].notna(
        )]
        standard_bool = (pc_structure_df["pc_type"] == "Standard").any()
        sliding_scale_bool = (
            pc_structure_df["pc_type"] == "Sliding Scale").any()
        if standard_bool and sliding_scale_bool:
            profit_commission_description = "PC varies by class of business, refer to profit commission section below"
        else:
            uw_expense = pc_structure_df["uw_expense"].values[0]
            expense_basis = pc_structure_df["expense_basis"].values[0]
            if standard_bool:
                standard_df = utils.pd_df_from_hx_list_v2(
                    hxd.cds.pc.pc_structure.for_standard)
                pc_percent = standard_df["pc_percent"].values[0]
                profit_commission_description = f"{pc_percent * 100:.5f}% after {uw_expense * 100}% Underwriting expenses on {expense_basis}"
            else:
                profit_commission_description = f"Sliding Scale PC after {uw_expense * 100}% Underwriting expenses on {expense_basis}"
    else:
        profit_commission_description = "Not Applicable"

    return profit_commission_description


def build_anti_selection_uncertainty_str(hxd):
    loading_summary = hxd.cds.rating_summary.additional_loadings.summary

    anti_selection = loading_summary.anti_selection_charge
    uncertainty = loading_summary.uncertainty_charge

    return f"{anti_selection * 100:.2f} / {uncertainty * 100:.2f}"

