import hx

VALIDATIONS = []

TABLE_UNDERWRITER_OPTIONS = list(hx.params.tbl_underwriter["Underwriters"])
TABLE_UNDERWRITING_ASSISTANT_OPTIONS = list(hx.params.lst_underwriting_assistant["Underwriter Assistant"])
TABLE_BROKER_OPTIONS = list(hx.params.lst_broker["Value"])
TABLE_SLIP_LEADER_OPTIONS = list(hx.params.lst_slip_lead["Markets"])


def set_valid(hxd, field):
    setattr(getattr(hxd.cds.validation, field), "valid", True)
    setattr(getattr(hxd.cds.validation, field), "invalid", False)

def set_invalid(hxd, field, error_msg):
    setattr(getattr(hxd.cds.validation, field), "valid", False)
    setattr(getattr(hxd.cds.validation, field), "invalid", True)
    setattr(getattr(hxd.cds.validation, field), "info_text", error_msg)
    hx.errors.validation(error_msg)

def validation(fn):
    VALIDATIONS.append(fn)

    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


@validation
def validate_underwriter(hxd):
    supported_values = TABLE_UNDERWRITER_OPTIONS
    value = hxd.cds.standard_fields.underwriter

    if value and value not in supported_values:
        set_invalid(hxd, "underwriter", "Risk Information: The selected Underwriter is inactive. Choose an alternative.")
    else:
        set_valid(hxd, "underwriter")


@validation
def validate_underwriting_assistant(hxd):
    supported_values = TABLE_UNDERWRITING_ASSISTANT_OPTIONS
    value = hxd.cds.risk_information.underwriting_assistant

    if value and value not in supported_values:
        set_invalid(hxd, "underwriting_assistant", "Risk Information: The selected UA is inactive. Choose an alternative.")
    else:
        set_valid(hxd, "underwriting_assistant")


@validation
def validate_broker(hxd):
    supported_values = TABLE_BROKER_OPTIONS[:225]
    value = hxd.cds.standard_fields.broker

    if value and value not in supported_values:
        set_invalid(hxd, "broker", "Risk Information: The selected Broker Name is inactive. Choose an alternative.")
    else:
        set_valid(hxd, "broker")


@validation
def validate_slip_leader(hxd):
    supported_values = TABLE_SLIP_LEADER_OPTIONS[:68]
    invalid_options = list()

    if hxd.cds.risk_information.mmp_flag:
        value = hxd.cds.mmp.total.slip_leader

        if value and value not in supported_values:
            set_invalid(hxd, "slip_leader", "Rating Summary MMP: The selected slip leader is inactive. Choose an alternative")
        else:
            set_valid(hxd, "slip_leader")

    else:
        set_valid(hxd, "slip_leader")
    
        for i, layer in enumerate(hxd.cds.large_cap.layers):
            value = layer.slip_leader
            if value and value not in supported_values:
                invalid_options.append(str(i+1))
            
        if invalid_options:
            set_invalid(hxd, "slip_leader", "Rating Summary: A selected slip leader is inactive. Choose an alternative")


def run_validation(hxd):
    for validate in VALIDATIONS:
        validate(hxd)