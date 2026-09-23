import hx
from algorithms.rate_constants import deductible_type_mapping

VALIDATIONS = []

TABLE_BROKER_OPTIONS = list(hx.params.table_broker["Broker"])
TABLE_UNDERWRITER_OPTIONS = list(hx.params.table_input_underwriters["underwriter"])
TABLE_AOP_DEDUCTIBLE_OPTIONS = list(hx.params.table_aop_deductible_options['AOP Deductible'])
TABLE_WS_DEDUCTIBLE_OPTIONS = list(hx.params.table_ws_deductible_options["WS Deductible"])
SUBLIMITS_MAPPING = {
    "animal": {
        "label": "Animal Liability Limitation",
        "invalid_options": []
    },
    "diving_board_and_pool": {
        "label": "Diving Board & Pool Slide Liability Limitiation",
        "invalid_options": []
    },
    "trampoline": {
        "label": "Trampoline Liability Limitation",
        "invalid_options": []
    },
    "swimming_pool": {
        "label": "Swimming Pool Liability Limitation",
        "invalid_options": []
    },
}

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

# @validation
# def validate_underwriter(hxd):
#     # PLACEHOLDER: Currently, set to first 30 names... meaning validation errors do not apply.
#     supported_values = TABLE_UNDERWRITER_OPTIONS[:30]
#     value = hxd.cds.standard_fields.underwriter

#     if value not in supported_values:
#         set_invalid(hxd, "underwriter", "The selected Underwriter Name is inactive. Please choose an appropriate replacement.")
#     else:
#         set_valid(hxd, "underwriter")


@validation
def validate_broker(hxd):
    supported_values = TABLE_BROKER_OPTIONS[:49]
    value = hxd.cds.standard_fields.broker

    if value not in supported_values:
        set_invalid(hxd, "broker", "The selected Broker Name is inactive. Please choose an appropriate replacement.")
    else:
        set_valid(hxd, "broker")

# @validation
# def validate_city(hxd):
#     zip_code = hxd.cds.rating_factors.zip
#     zip_city_state_mappings = hx.params.table_zip_code_city_state_mappings
#     zip_match = zip_city_state_mappings[zip_city_state_mappings['Risk Zip'] == zip_code]
#     supported_values = list(zip_match['Risk City'])
#     # supported_values = zip_match['Risk City']
#     value = hxd.cds.rating_factors.city
    
#     # using supported_values is a Series

#     if not supported_values:
#         if not value:
#             set_valid(hxd, "city")
#         else:
#             set_invalid(hxd, "city", "The selected City is inactive. Please choose an appropriate replacement.")
#     else:
#         if value and value not in supported_values:
#             set_invalid(hxd, "city", "The selected City is inactive. Please choose an appropriate replacement.")
#         else:
#             set_valid(hxd, "city")

@validation
def validate_construction_type(hxd):
    unsupported_values = ["Joisted Masonry", None]
    value = hxd.cds.rating_factors.construction_type

    if value in unsupported_values:
        set_invalid(hxd, "construction_type", "The selected Construction Type is inactive. Please choose an appropriate replacement.")
    else:
        set_valid(hxd, "construction_type")

@validation
def validate_roof_shape(hxd):
    unsupported_values = ["Gable roof low pitch", "Gable Roof unknown pitch"]
    value = hxd.cds.rating_factors.roof_shape

    if value in unsupported_values:
        set_invalid(hxd, "roof_shape", "The selected Roof Shape is inactive. Please choose an appropriate replacement.")
    else:
        set_valid(hxd, "roof_shape")

@validation
def validate_number_of_units(hxd):
    unsupported_values = ["Quadplex"]
    value = hxd.cds.rating_factors.number_of_units

    if value in unsupported_values:
        set_invalid(hxd, "number_of_units", "The selected Number of Units is inactive. Please choose an appropriate replacement.")
    else:
        set_valid(hxd, "number_of_units")

# @validation
# def validate_insured_occupation(hxd):
#     unsupported_values = ["Other"]
#     value = hxd.cds.rating_factors.insured_occupation

#     if value in unsupported_values:
#         set_invalid(hxd, "insured_occupation", "The selected Insured Occupation is inactive. Please choose an appropriate replacement.")
#     else:
#         set_valid(hxd, "insured_occupation")

@validation
def validate_aop_deductible(hxd):
    if hxd.cds.show_aop_options == False or hxd.cds.show_aop_option == False:
        return 

    set_valid(hxd, "aop_deductible")
    aop_deductible_invalid_options = list()

    for i, layer in enumerate(hxd.cds.layers):
        if i >= hxd.cds.number_of_options:
            break

        # check AOP Deductible validity
        if layer.coverages.aop.deductible not in TABLE_AOP_DEDUCTIBLE_OPTIONS[1:]:
            aop_deductible_invalid_options.append(str(i+1))

    if aop_deductible_invalid_options:
        aop_deductible_error_msg = f"The selected value(s) in AOP Deductible for Options ({','.join(aop_deductible_invalid_options)}) are not supported. Please choose appropriate supported values."
        set_invalid(hxd, "aop_deductible", aop_deductible_error_msg)


@validation
def validate_ws_deductible(hxd):
    # Skip validation entirely if Excess Wind & Hail is selected
    if hxd.cds.excess_wind_hail_selected:
        return

    if hxd.cds.show_ws_options == False or hxd.cds.show_ws_option == False:
        return 

    set_valid(hxd, "ws_deductible")
    ws_deductible_invalid_options = list()

    # show this row in the table only if All Perils isn't selected 
    if not hxd.cds.ws_deductible_is_not_all_perils:
        hxd.cds.validation.ws_deductible.valid = False
        hxd.cds.validation.ws_deductible.invalid = False
        return  # better than pass, stops further checks

    for i, layer in enumerate(hxd.cds.layers):
        if i >= hxd.cds.number_of_options:
            break
     
        if (
            layer.coverages.ws.deductible not in TABLE_WS_DEDUCTIBLE_OPTIONS
            and layer.coverages.ws.include_peril.value
        ):
            ws_deductible_invalid_options.append(str(i + 1))

    if ws_deductible_invalid_options:
        ws_deductible_error_msg = (
            f"The selected value(s) in WS Deductible for Options "
            f"({','.join(ws_deductible_invalid_options)}) are not supported. "
            f"Please choose appropriate supported values."
        )
        set_invalid(hxd, "ws_deductible", ws_deductible_error_msg)
        
@validation
def validate_wildfire_deductible_type(hxd):

    set_valid(hxd, "wildfire_deductible_type")
    wildfire_deductible_type_invalid_options = list()

    for i, layer in enumerate(hxd.cds.layers):
        if i >= hxd.cds.number_of_options:
            break
        
        if hxd.cds.show_wildfire_options:
            if (not layer.coverages.wildfire.include_peril.value and not layer.coverages.wildfire.deductible_type == "Excluded"):
                wildfire_deductible_type_invalid_options.append(str(i+1))
            elif layer.coverages.wildfire.include_peril.value and layer.coverages.wildfire.deductible_type == "Excluded":
                wildfire_deductible_type_invalid_options.append(str(i+1))

        

    if wildfire_deductible_type_invalid_options:
        wildfire_deductible_type_error_msg = f"Wildfire Deductible Type value(s) for Options ({','.join(wildfire_deductible_type_invalid_options)}) are not supported when Wildfire Coverage is disabled. Please choose appropriate supported values."
        set_invalid(hxd, "wildfire_deductible_type", wildfire_deductible_type_error_msg)

@validation
def validate_wildfire_deductible(hxd):

    set_valid(hxd, "wildfire_deductible")
    wildfire_deductible_invalid_options = list()

    for i, layer in enumerate(hxd.cds.layers):
        if i >= hxd.cds.number_of_options:
            break
            
        if hxd.cds.show_wildfire_options:
            valid_values = deductible_type_mapping.get(layer.coverages.wildfire.deductible_type, [])

            if layer.coverages.wildfire.deductible_type == "AOP":
                valid_values = [layer.coverages.aop.deductible]

            # Check Wildfire Deductible validity
            if layer.coverages.wildfire.deductible_type == "Excluded":
                if layer.coverages.wildfire.deductible:
                    wildfire_deductible_invalid_options.append(str(i+1))
            else:
                if layer.coverages.wildfire.deductible not in valid_values:
                    wildfire_deductible_invalid_options.append(str(i+1))

    if wildfire_deductible_invalid_options:
        wildfire_deductible_error_msg = f"The selected value(s) in Wildfire Deductible for Options ({','.join(wildfire_deductible_invalid_options)}) are not supported. Please choose appropriate supported values."
        set_invalid(hxd, "wildfire_deductible", wildfire_deductible_error_msg)

@validation
def validate_coverage_m(hxd):
    set_valid(hxd, "coverage_m_med_pay_limit")
    coverage_m_invalid_options = list()

    for i, layer in enumerate(hxd.cds.layers):
        if i >= hxd.cds.number_of_options:
            break

        # Check Coverage M Med Pay validity
        if layer.coverage_m_med_pay_limit not in [0, 1000, 5000, 10000]:
            coverage_m_invalid_options.append(str(i+1))
        
    if coverage_m_invalid_options:
        coverage_m_error_msg = f"The selected value(s) in Coverage M - Med Pay for Options ({','.join(coverage_m_invalid_options)}) are not supported. Please choose appropriate supported values."
        set_invalid(hxd, "coverage_m_med_pay_limit", coverage_m_error_msg)

@validation
def validate_status(hxd):
    set_valid(hxd, "status")
    status_invalid_options = list()

    for i, layer in enumerate(hxd.cds.layers):
        if i >= hxd.cds.number_of_options:
            break

        # Status validity
        if layer.status == "Post Bind Complete":
            status_invalid_options.append(str(i+1))

    if status_invalid_options:
        status_error_msg = f"The selected Status for Options ({','.join(status_invalid_options)}) is not supported. Please choose an appropriate status."
        set_invalid(hxd, "status", status_error_msg)

@validation
def validate_sub_limits(hxd):

    # Prepare the mapper and reset it between executions
    for i, layer in enumerate(hxd.cds.layers):
        if i >= hxd.cds.number_of_options:
            break

        for sub_limit in SUBLIMITS_MAPPING:
            set_valid(hxd, sub_limit)
            SUBLIMITS_MAPPING[sub_limit]["invalid_options"] = list() # resetting to an empty list

    # Validate
    for i, layer in enumerate(hxd.cds.layers):
        if i >= hxd.cds.number_of_options:
            break
        
        dropdown_options = list()
        coverage_l_values = layer.coverage_l_liability_limit.selected
    
        # Check Sub Limits validity
        for sub_limit in SUBLIMITS_MAPPING:
            if getattr(layer.sublimits, f"{sub_limit}_included"):
                if coverage_l_values and coverage_l_values > 0:
                    dropdown_options = [25000, coverage_l_values]
                else:
                    dropdown_options = [None] # value can be None so we're adding it
            else:
                dropdown_options = [None]
            
            if getattr(layer.sublimits, sub_limit) not in dropdown_options:
                SUBLIMITS_MAPPING[sub_limit]["invalid_options"].append(str(i+1))

    # Set the flags and the error messages for each sub limit
    for sub_limit in SUBLIMITS_MAPPING:
        invalid_options = SUBLIMITS_MAPPING[sub_limit]["invalid_options"]

        if invalid_options:
            error_msg = f"The selected value(s) for {SUBLIMITS_MAPPING[sub_limit]['label']} for Options ({','.join(invalid_options)}) is not supported. Please choose an appropriate supported value."
            set_invalid(hxd, sub_limit, error_msg)


def run_validation(hxd):
    for validate in VALIDATIONS:
        validate(hxd)