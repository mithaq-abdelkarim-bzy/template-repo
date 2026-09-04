import hx

def adjust_graph_strings(hxd):
    chart_path = hxd.cds.rating_summary.chart_premium_breakdown
    chart_path.technical.metric_string = "TPI"
    chart_path.benchmark.metric_string = "BPI"


    chart_path.title_string = f"Premium Breakdown - {chart_path.uw_adj_basis} - {chart_path.premium_basis}"