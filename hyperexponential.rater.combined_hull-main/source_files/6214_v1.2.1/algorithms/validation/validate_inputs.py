import hx


def validate_rating_summary_inputs(coverage):
    MIN_WRITTEN_LINE = 0
    MAX_WRITTEN_LINE = 1
    MIN_BROKERAGE = 0
    MAX_BROKERAGE = 1
    coverage_name = coverage[0]
    coverage_data = coverage[1]
    coverage_brokerage = (
        coverage_data.brokerage.selected or 0
        if (coverage_name == "iv") or (coverage_name == "war")
        else coverage_data.brokerage or 0
    )
    coverage_written_line = (
        coverage_data.written_line.selected or 0
        if (coverage_name == "iv") or (coverage_name == "war")
        else coverage_data.written_line or 0
    )
    if (coverage_written_line < MIN_WRITTEN_LINE) or (
        coverage_written_line > MAX_WRITTEN_LINE
    ):
        hx.errors.validation(
            f"{coverage_name}: Written line should be between 0 and 100"
        )

    # if (coverage_brokerage < MIN_BROKERAGE) or (coverage_brokerage > MAX_BROKERAGE):
    #     hx.errors.validation(f"{coverage_name}: Brokerage should be between 0 and 100")


def validate_inputs(hxd):
    for coverage in hxd.cds.layers[0].coverages:
        validate_rating_summary_inputs(coverage)
