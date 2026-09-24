import hx
import pandas as pd
from algorithms import rate_constants as constants  
from algorithms.rate_utilities import ratio, look_up


def rate_rating_summary(hxd):
    # State calculations
    state = hxd.cds.state or ""
    state_code = look_up(state, "State Name", "Abbreviation", hx.params.table_reference_state, if_not_found=None)
    if state_code is None:
        return

    # Date calculations
    inception_date = hxd.hx_core.inception_date or pd.Timestamp.now().date()  # Dummy date if no inception date
    one_year_from_inception = (inception_date + pd.DateOffset(years=1)).date()
    expiry_date = hxd.hx_core.expiry_date or one_year_from_inception
    pro_rata_factor = 1 + (
        (expiry_date - one_year_from_inception) / pd.Timedelta(days=365)
    )

    state_allows_rounding = look_up(state_code, "state", "allows_rounding", hx.params.table_pkg_admitted_applicabilities, if_not_found=None)
    if state_allows_rounding is None:
        return
    allow_epl_rounding = state_allows_rounding == "True"

    coverage_elections = hxd.cds.coverage_elections

    number_of_coverages = coverage_elections.pcl + coverage_elections.epl + coverage_elections.fid

    if number_of_coverages > 1:
        if hxd.cds.package_information.combined_single_aggregate_limit:
            package_discount = 0.9
        else:
            package_discount = 0.95
    else:
        package_discount = 1  # Default Value 

    #bring out the package discount to the front end
    hxd.cds.package_information.package_discount = package_discount

    # Store totals as we go as we'll have to access all the variables anyway
    total_pre_rounding_admitted_premium = 0
    total_post_rounding_admitted_premium = 0
    total_final_term_premium = 0
    total_benchmark_premium = 0
    total_benchmark_premium_pre_uw_adj = 0
    
    layer = hxd.cds.layers[0]

    #set the written line for the rate change calc
    #layer.written_line = constants.beazley_share

    # Defaults to be potentially overridden if conditions are met
    rounding_lower_bound = -1
    rounding_upper_bound = 1

    # Fid, EPL and USML
    for coverage_struct in layer.coverages:
        coverage_name = coverage_struct[0]
        coverage = coverage_struct[1]
        is_coverage_selected = getattr(hxd.cds.coverage_elections, coverage_name)
        if not is_coverage_selected:
            continue

        # Populate Coverage Quote Grid
        # Using a loop as the number of options isn't expected to become large
        coverage_qg_options = coverage.quote_grid.qg_options
        for option in coverage_qg_options:
            if not option.option_selected:
                continue

            coverage_quote_grid = getattr(hxd.cds.quote_grid_summary, coverage_name)

            coverage_quote_grid.limit = option.aggregate_limit or 0
            coverage_quote_grid.adl = 0 if coverage_name == "pcl" else (option.adl_limit or 0)
            coverage_quote_grid.retention = option.retention or 0

            benchmark_premium = (option.internal_benchmark or 0) * package_discount
            benchmark_premium_pre_uw_adj = (option.internal_benchmark_pre_uw_adj or 0) * package_discount
            coverage_quote_grid.benchmark_premium = benchmark_premium
            total_benchmark_premium += benchmark_premium
            total_benchmark_premium_pre_uw_adj += benchmark_premium_pre_uw_adj

            pre_rounding_admitted_premium = (option.admitted_premium or 0) * package_discount
            coverage_quote_grid.pre_rounding_admitted_premium = pre_rounding_admitted_premium
            total_pre_rounding_admitted_premium += pre_rounding_admitted_premium

            selected_premium = coverage_quote_grid.selected_premium or 0
            post_rounding_admitted_premium = selected_premium if selected_premium > 0 else pre_rounding_admitted_premium
            coverage_quote_grid.post_rounding_admitted_premium = post_rounding_admitted_premium
            total_post_rounding_admitted_premium += post_rounding_admitted_premium

            final_term_premium = post_rounding_admitted_premium * pro_rata_factor
            coverage_quote_grid.final_term_premium = final_term_premium
            total_final_term_premium += final_term_premium
        
            coverage_quote_grid.bpi = 0 if benchmark_premium == 0 else final_term_premium/benchmark_premium * pro_rata_factor    

            if coverage_name == "epl" and allow_epl_rounding:
                table_rounding_rules = hx.params.table_rounding_rules  # Only applies for the selected option and epl, so only importing once despite loop

                table_rounding_rules_rows = table_rounding_rules.loc[
                    (
                        (
                            table_rounding_rules["lower_bound"]
                            <= pre_rounding_admitted_premium
                        )
                        & (
                            pre_rounding_admitted_premium
                            <= table_rounding_rules["upper_bound"]
                        )
                    ),
                    ("round_down", "round_up"),
                ]
                if not table_rounding_rules_rows.empty:
                    rounding_lower_bound, rounding_upper_bound = (
                        table_rounding_rules_rows.iloc[0]
                    )

    final_premium_summary = hxd.cds.final_premium_summary
    final_premium_summary.rounding_min = rounding_lower_bound
    final_premium_summary.rounding_max = rounding_upper_bound
    
    final_premium_summary.benchmark_premium = total_benchmark_premium   
    final_premium_summary.benchmark_premium_pre_uw_adj = total_benchmark_premium_pre_uw_adj
    final_premium_summary.pre_rounding_admitted_premium = total_pre_rounding_admitted_premium
    final_premium_summary.post_rounding_admitted_premium = total_post_rounding_admitted_premium
    final_premium_summary.final_admitted_term_premium = total_final_term_premium

    benchmark_term_premium = total_benchmark_premium * pro_rata_factor
    final_premium_summary.benchmark_term_premium = benchmark_term_premium
    benchmark_term_premium_pre_uw_adj = total_benchmark_premium_pre_uw_adj * pro_rata_factor
    final_premium_summary.benchmark_term_premium_pre_uw_adj = benchmark_term_premium_pre_uw_adj
    
    final_premium_summary.bpi = 0 if benchmark_term_premium == 0 else total_final_term_premium / benchmark_term_premium

    #adding a validation error around the sum of the selected premium and pre rounded premium
    if (hxd.cds.standard_fields.is_admitted_or_surplus == "Admitted" and hxd.cds.layers[0].is_primary_excess != "Excess"):
        if (
            total_post_rounding_admitted_premium < total_pre_rounding_admitted_premium + rounding_lower_bound or
            total_post_rounding_admitted_premium > total_pre_rounding_admitted_premium + rounding_upper_bound
        ):
            hx.errors.validation(f"The sum of the post rounded premium is outside the allowed rounding")
