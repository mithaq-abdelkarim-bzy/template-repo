import hx


def validate_exposure(hxd):
    # SA: If you do create a static variables doc I'd put these there too
    MIN_WRITTEN_CONTRACT = 0
    MAX_WRITTEN_CONTRACT = 1
    MIN_UNDERWRITER_JUDGEMENT = -0.5
    product_type = hxd.cds.account_details.product_type

    written_contract = hxd.cds.rating_factors.business_with_written_contract.percentage
    if written_contract is not None and (
        written_contract < MIN_WRITTEN_CONTRACT
        or written_contract > MAX_WRITTEN_CONTRACT
    ):
        hx.errors.validation(
            f"Invalid Input: Percentage of Written Contract must be between {MIN_WRITTEN_CONTRACT*100}% and {MAX_WRITTEN_CONTRACT*100}%"
        )

    underwriter_judgement = hxd.cds.rating_factors.underwriter_judgement
    if (
        underwriter_judgement is not None
        and underwriter_judgement < MIN_UNDERWRITER_JUDGEMENT
    ):
        hx.errors.validation(
            f"Invalid Risk Characteristics: Maximum credit is {MIN_UNDERWRITER_JUDGEMENT*100}%"
        )

    if product_type == "Staffing":
        staffing_total = hxd.cds.exposure.aggregate.staffing
        if staffing_total is not None and staffing_total != 1:
            hx.errors.validation("Staffing: Allocation does not sum to 100%")
