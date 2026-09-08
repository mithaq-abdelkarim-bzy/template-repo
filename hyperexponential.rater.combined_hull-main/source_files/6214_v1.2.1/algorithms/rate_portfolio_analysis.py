import hx


def rate_portfolio_analysis(hxd):
    currency = hxd.cds.portfolio_analysis.hull_rating.filter_options.currency
    hxd.non_cds.labels.portfolio_analysis_labels.currency_avg_agreed_value = (
        f"Avg. Agreed Value ({currency})" if currency else "Avg. Agreed Value"
    )
    hxd.non_cds.labels.portfolio_analysis_labels.currency_agreed_value_converted = (
        f"Agreed Value Converted ({currency})" if currency else "Agreed Value Converted"
    )
