import hx, re
from dateutil.relativedelta import relativedelta

def check_deal_status_value(status):
    if status != "Bound":
        hx.errors.validation("Deal Status (Risk Information Tab) must be set to Bound prior to Finalising.")


def check_expiry_date_value(inception_date, expiry_date):
    if inception_date < expiry_date:
        hx.errors.validation("Expiry Date must not be prior to Inception Date")


def check_underwriter_value(underwriter):
    if underwriter is None:
        hx.errors.validation("An Underwriter (Risk Information Tab) must be entered.")


def check_facility_type_value(facility_type):
    if facility_type is None:
        hx.errors.validation("A Facility Type (Risk Information Tab) must be entered.")


def check_insured_name_value(insured_name):
    if insured_name is None:
        hx.errors.validation("An Insured Name (Risk Information Tab) must be entered.")


def check_currency_value(currency):
    if currency is None:
        hx.errors.validation("A Currency (Risk Information Tab) must be entered.")


def check_insured_data_as_at_date_value(insured_date_as_at_date, inception_date, hxd):
    is_empty      = insured_date_as_at_date is None
    is_less_9mth  = True if is_empty else inception_date - relativedelta(months=9) > insured_date_as_at_date
    is_grt_incept = True if is_empty else inception_date                           < insured_date_as_at_date

    if is_empty:
        hx.errors.validation("An Insured Data as at Date (Risk Information Tab) must be entered - value temporarily defaulted to 9mth prior to Inception Date.")

    # if outside 0-9mth from incept additionally trigger a non-blocking global warning
    if is_empty or is_less_9mth or is_grt_incept:
        hxd.non_cds.global_fields.is_projections_msg_shown = True


def _is_valid_policy_reference(ref):
    pattern = r'^[A-Za-z0-9]{6}\d{2}$'
    return bool(re.match(pattern, ref))


def check_policy_reference_value(policy_reference):
    if policy_reference is None or not _is_valid_policy_reference(policy_reference):
        hx.errors.validation("The Policy Reference (Risk Information Tab) must be in the format of 6 char of any type and 2 digits")

def check_broker_name(broker_name):
    if broker_name is None:
        hx.errors.validation("A Broker Name (Risk Information Tab) must be entered.")
