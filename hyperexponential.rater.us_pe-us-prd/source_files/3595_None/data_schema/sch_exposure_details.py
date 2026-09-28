import hx_data_schema as hx
import data_schema.sch_utilities as utils
import hx as HX


# Function to return a list of product types from the revenue bands table
def product_types():
    revenue_bands_table = HX.params.table_input_revenue_bands
    return sorted(list(set(revenue_bands_table["product"])), key=lambda x: x.lower())


def loss_experience():
    loss_experience_table = HX.params.table_input_loss_experience
    return sorted(list(set(loss_experience_table["number_of_claims_in_years"])))


def revenue_tier_types():
    revenue_types_table = HX.params.table_revenue_types_factors
    return sorted(list(set(revenue_types_table["revenue_type"])))


def business_with_written_contract_client_revenue():
    mpl_client_revenue_table = HX.params.table_input_mpl_client_revenue
    return sorted(list(set(mpl_client_revenue_table["average_revenue"])))


def sch_rating_factors_non_cds():
    return {
        "rating_factors": hx.Structure(
            children={
                "retroactive_years_list": hx.List(
                    mode="output",
                    children={"years": hx.Str(mode="output")},  # Retroactive years list
                )
            }
        )
    }


def sch_exposure_details(cds):

    cds.extend_node_rater_defined(
        "cds",
        {
            "tooltips": hx.Structure(
                children={
                    "occupation": hx.Str(
                        mode="input",
                        default="Enter the occupation code which best describes the insured",
                    ),
                    "sub_occupation": hx.Str(
                        mode="input",
                        default="Enter the sub occupation code which best describes the insured",
                    ),
                    "state": hx.Str(mode="input", default="State or region of the US"),
                    "loss_experience": hx.Str(
                        mode="input", default="History of Claims"
                    ),
                    "underwriter_judgement": hx.Str(
                        mode="input",
                        default="Enter any risk based adjustments here",
                    ),
                    "underwriter_judgement_justification": hx.Str(
                        mode="input",
                        default="If you have entered anything other than 0 for UW Judgement then please justify it here",
                    ),
                    "longevity": hx.Str(
                        mode="input",
                        default="Length of time the insured has been in business",
                    ),
                    "professional_experience": hx.Str(
                        mode="input",
                        default="Average professional experience of the insured's staff",
                    ),
                    "business_with_written_contract_percentage": hx.Str(
                        mode="input",
                        default="Enter the percentage of business with written contracts",
                    ),
                    "business_with_written_contract_revenue": hx.Str(
                        mode="input",
                        default="What level of revenue do the insured's clients have",
                    ),
                }
            ),
        },
    )

    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.override_node_properties(
        "cds/key_industry/code_name",
        {
            "default_index": 0,
            "optionality": "required",
            "options_table": "table_input_occupations",
            "options_column": "occupation_name",
            "view": {"label": "Occupation"},
        },
    ),

    cds.override_node_properties(
        "cds/standard_fields/insured_state_or_province",
        {
            "default_index": 0,
            "optionality": "required",
            "options_table": "table_input_states",
            "options_column": "state_code",
            "view": {"label": "State"},
        },
    ),

    cds.extend_node_rater_defined(
        "cds/key_industry",
        {
            "sub_occupation": hx.Structure(
                children={
                    "group": hx.Int(mode="output"),
                    "list": hx.List(
                        mode="output", children={"name": hx.Str(mode="output")}
                    ),
                    "name": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                        options_data="../list",
                        options_field="name",
                        view={"label": "Sub Occupation"},
                    ),
                }
            )
        },
    ),

    cds.extend_node_rater_defined(
        "cds",
        {
            "rating_factors": hx.Structure(
                children={
                    # Product Type
                    "product_type": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                        async_input=["rarc_task"],
                        options=product_types(),  # Product type field with options from product_types function
                        view={"label": "Product Type"},
                    ),
                    "retroactive_years": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                        options_data="../../../non_cds/rating_factors/retroactive_years_list",  # Options data from retroactive years list
                        options_field="years",
                        async_input=["rarc_task"],
                        view={"label": "Retroactive Years"},
                    ),
                    "show_loss_experience_empty_panel": hx.Bool(mode="output"),
                    "show_revenue_type": hx.Bool(mode="output"),
                    "loss_experience": hx.Str(
                        mode="input",
                        view={"label": "Loss Experience"},
                        optionality="optional",
                        default=None,
                        options=loss_experience(),
                        async_input=["rarc_task"],
                    ),
                    "underwriter_judgement": hx.Float(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={
                            "label": "UW Judgement (Risk Based)",
                            "format": utils.percent_format(0),
                        },
                    ),
                    "underwriter_judgement_justification": hx.Str(
                        mode="input",
                        view={
                            "label": "Underwriter Comment",
                        },
                        default=None,
                        optionality="optional",
                    ),
                    "longevity": hx.Structure(
                        children={
                            "show": hx.Bool(mode="output"),
                            "years_list": hx.List(
                                mode="output", children={"years": hx.Str(mode="output")}
                            ),
                            "years": hx.Str(
                                mode="input",
                                async_input=["rarc_task"],
                                default=None,
                                optionality="optional",
                                options_data="../years_list",
                                options_field="years",
                                view={"label": "Longevity Factor"},
                            ),
                            "factor": hx.Float(
                                mode="output",
                                view={
                                    "label": "Credit/Debit",
                                    "format": utils.percent_format(0),
                                },
                            ),
                            # Just for the use of label by in the view
                            "med_mal_longevity_label": hx.Str(
                                mode="input", default="Age of business up to"
                            ),
                        },
                    ),
                    "professional_experience": hx.Structure(
                        children={
                            "show": hx.Bool(mode="output"),
                            "years_list": hx.List(
                                mode="output", children={"years": hx.Str(mode="output")}
                            ),
                            "years": hx.Str(
                                async_input=["rarc_task"],
                                mode="input",
                                default=None,
                                optionality="optional",
                                options_data="../years_list",
                                options_field="years",
                                view={"label": "Professional Experience"},
                            ),
                            "factor": hx.Float(
                                mode="output",
                                view={
                                    "label": "Credit/Debit",
                                    "format": utils.percent_format(0),
                                },
                            ),
                            # Just for the use of label by in the view
                            "med_mal_professional_experience_label": hx.Str(
                                mode="input", default="Professional Experience up to"
                            ),
                        },
                    ),
                    "business_with_written_contract": hx.Structure(
                        children={
                            "show": hx.Bool(mode="output"),
                            "percentage": hx.Float(
                                mode="input",
                                async_input=["rarc_task"],
                                default=None,
                                optionality="optional",
                                view={
                                    "label": "Business with Written Contract",
                                    "format": utils.percent_format(0),
                                },
                            ),
                            "revenue": hx.Str(
                                mode="input",
                                async_input=["rarc_task"],
                                default=None,
                                optionality="optional",
                                options=business_with_written_contract_client_revenue(),
                                view={"label": "Revenue of Insured's Clients"},
                            ),
                        },
                    ),
                    "tiers_list": hx.List(
                        mode="output",
                        children={
                            "tier": hx.Int(mode="output"),
                            "business_description": hx.Str(mode="output"),
                        },
                    ),
                    "types_list": hx.List(
                        mode="output",
                        children={"type": hx.Str(mode="output")},
                    ),
                    "revenues": hx.List(
                        mode="input",
                        children={
                            "hazard_tier": hx.Structure(
                                linked_options_data="../../../tiers_list",
                                linked_options_fields=["tier", "business_description"],
                                children={
                                    "tier": hx.Int(
                                        async_input=["rarc_task"],
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={"label": "Tier"},
                                    ),
                                    "business_description": hx.Str(
                                        mode="input",
                                        async_input=["rarc_task"],
                                        default=None,
                                        optionality="optional",
                                        view={"label": "Business Description"},
                                    ),
                                },
                            ),
                            "value": hx.Int(
                                mode="input",
                                async_input=["rarc_task"],
                                default=None,
                                view={
                                    "label": "Value",
                                    "format": utils.thousands_format(0),
                                },
                                optionality="optional",
                            ),
                            "factor": hx.Float(
                                mode="output",
                            ),
                            "type": hx.Str(
                                mode="input",
                                async_input=["rarc_task"],
                                default=None,
                                optionality="optional",
                                options_data="../../../types_list",
                                options_field="type",
                                view={"label": "Type"},
                            ),
                        },
                        default_element_count=3,
                    ),
                    "med_mal": hx.Structure(
                        children={
                            "show": hx.Bool(mode="output"),
                            "hide": hx.Bool(mode="output"),
                            "allied_medical": hx.Structure(
                                children={
                                    "allied_medical_type": hx.Str(
                                        mode="input",
                                        async_input=["rarc_task"],
                                        default=None,
                                        optionality="optional",
                                        options_table="table_allied_medical",
                                        options_column="allied_medical",
                                        view={"label": "Allied Medical Type"},
                                    ),
                                    "exposure_type": hx.Str(
                                        mode="output",
                                        optionality="optional",
                                        view={"label": "Exposure Type"},
                                    ),
                                    "exposure_measure": hx.Float(
                                        mode="input",
                                        async_input=["rarc_task"],
                                        default=None,
                                        optionality="optional",
                                        view={"label": "Exposure Measure"},
                                    ),
                                    "exposure_factor": hx.Float(
                                        mode="output",
                                        optionality="optional",
                                        view={"label": "Exposure Factor"},
                                    ),
                                },
                            ),
                            "social_services": hx.Structure(
                                children={
                                    "social_services_type": hx.Str(
                                        mode="input",
                                        async_input=["rarc_task"],
                                        default=None,
                                        optionality="optional",
                                        options_table="table_input_social_services",
                                        options_column="social_services",
                                        view={"label": "Social Services Type"},
                                    ),
                                    "exposure_type": hx.Str(
                                        mode="output",
                                        optionality="optional",
                                        view={"label": "Exposure Type"},
                                    ),
                                    "exposure_measure": hx.Float(
                                        mode="input",
                                        async_input=["rarc_task"],
                                        default=None,
                                        optionality="optional",
                                        view={"label": "Exposure Measure"},
                                    ),
                                    "exposure_factor": hx.Float(
                                        mode="output",
                                        optionality="optional",
                                        view={"label": "Exposure Factor"},
                                    ),
                                },
                            ),
                            "endorsements": hx.List(
                                mode="input",
                                children={
                                    "endorsement": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        options_table="table_input_endorsements",
                                        options_column="endorsement",
                                        view={"label": "Endorsement"},
                                    ),
                                    "factor": hx.Float(
                                        mode="output",
                                        optionality="optional",
                                        view={
                                            "label": "Exposure Factor",
                                            "format": utils.percent_format(0),
                                        },
                                    ),
                                },
                                default_element_count=6,
                            ),
                            "total_credit_or_debit": hx.Float(
                                mode="output",
                                view={
                                    "label": "Total Credit/Debit",
                                    "format": utils.percent_format(0),
                                },
                            ),
                            "total_endorsement": hx.Float(
                                mode="output",
                                view={
                                    "label": "Endorsement Total Credit/Debit",
                                    "format": utils.percent_format(0),
                                },
                            ),
                        }
                    ),
                    "staffing": hx.Structure(
                        children={
                            "show": hx.Bool(mode="output"),
                            "permanent": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={
                                    "label": "Permanent Staffing",
                                    "format": utils.percent_format(0),
                                },
                            ),
                            "peo": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={
                                    "label": "PEO's",
                                    "format": utils.percent_format(0),
                                },
                            ),
                            "temporary": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={
                                    "label": "Temporary Staffing",
                                    "format": utils.percent_format(0),
                                },
                            ),
                            "total": hx.Float(
                                mode="output",
                                optionality="optional",
                                view={
                                    "label": "Total",
                                    "format": utils.percent_format(0),
                                },
                            ),
                        }
                    ),
                    "tech": hx.Structure(
                        children={
                            "show": hx.Bool(mode="output"),
                            "media_and_advertising": hx.Bool(
                                async_input=["rarc_task"],
                                mode="input",
                                default=False,
                                optionality="required",
                                view={"label": "Media & Advertising"},
                            ),
                            "cont_bi_pd": hx.Bool(
                                async_input=["rarc_task"],
                                mode="input",
                                default=False,
                                optionality="required",
                                view={"label": "Cont BI/PD"},
                            ),
                            "first_party_privacy": hx.Bool(
                                async_input=["rarc_task"],
                                mode="input",
                                default=False,
                                optionality="required",
                                view={"label": "First Party Privacy"},
                            ),
                            "cyber_extortion_only": hx.Bool(
                                async_input=["rarc_task"],
                                mode="input",
                                default=False,
                                optionality="required",
                                view={"label": "Cyber Extortion Only"},
                            ),
                        }
                    ),
                    "general_liability": hx.Structure(
                        children={
                            "show": hx.Bool(mode="output"),
                            "value": hx.Bool(
                                async_input=["rarc_task"],
                                mode="input",
                                default=False,
                                optionality="required",
                                view={"label": "General Liability"},
                            ),
                            "show_staffing": hx.Bool(mode="output"),
                        }
                    ),
                    "show_staffing_liability_limits_AGG": hx.Bool(mode="output"),
                    "show_product_liability_limits_AGG": hx.Bool(mode="output"),
                    "staffing_liability_limits_AGG_label": hx.Str(
                        mode="input",
                        default="Staffing Liability Limits AGG",
                    ),
                    "general_liability_limits_AGG_products_label": hx.Str(
                        mode="input", default="General Liability Limits AGG"
                    ),
                }
            )
        },
    )

    cds.extend_node_rater_defined(
        "cds/exposure/aggregate",
        {
            "total_revenue": hx.Int(
                mode="output",
                view={"label": "Total Revenue", "format": utils.thousands_format(0)},
            )
        },
    )
