import hx_data_schema as hx

def sch_validations(cds):
    """
    These nodes are validation nodes for the different dropdowns that are getting updated. If a dropdown value is not supported anymore (going to be removed in the future), 
    the field will be marked in a warning color and an appropriate info text will be displayed. 
    """
    cds.extend_node_rater_defined('cds', {
        "validation":hx.Structure(children={
            # Broker Name dropdown in Risk Information
            "underwriter": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Broker Name dropdown in Risk Information
            "broker": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # City dropdown in Risk Information
            "city": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Construction Type dropdown in Risk Characteristics
            "construction_type": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),
            
            # Number of units dropdown in Risk Characteristics
            "number_of_units": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Insured Occupation dropdown in Pricing page
            "insured_occupation": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),          

            # Roof Shape dropdown in Risk Characteristics
            "roof_shape": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # AOP Deductible row in Pricing section in Pricing
            "aop_deductible": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # WS Deductible row in Pricing section in Pricing
            "ws_deductible": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),
            
            # Wildfire Deductible Type row in Pricing section in Pricing
            "wildfire_deductible_type": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Wildfire Deductible row in Pricing section in Pricing
            "wildfire_deductible": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Animal row in Sub-Limits section in Pricing
            "animal": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Diving board row in Sub-Limits section in Pricing
            "diving_board_and_pool": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Trampoline row in Sub-Limits section in Pricing
            "trampoline": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Swimming Pool row in Sub-Limits section in Pricing
            "swimming_pool": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Swimming Pool row in Sub-Limits section in Pricing
            "coverage_m_med_pay_limit": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),

            # Status in Total section in Pricing
            "status": hx.Structure(children={
                "valid": hx.Bool(mode="output"),
                "invalid": hx.Bool(mode="output"),
                "info_text": hx.Str(mode="output"),
            }),
        })
    })
