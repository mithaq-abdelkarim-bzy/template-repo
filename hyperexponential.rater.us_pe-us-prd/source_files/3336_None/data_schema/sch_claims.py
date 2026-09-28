import hx_data_schema as hx


def sch_claims(cds):

    cds.extend_node_rater_defined(
        "cds",
        {
            "claims": hx.Structure(
                children={
                    "as_at_date": hx.Date(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={"label": "As At Date"},
                    ),
                    "threshold": hx.Int(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={"label": "Threshold"},
                    ),
                    "claims_net_of_retentions": hx.Bool(
                        mode="input",
                        default=False,
                        view={"label": "Claims Net of Retentions?"},
                    ),
                    "list": hx.List(
                        mode="input",
                        default_element_count=10,
                        children={
                            "claimant_name": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Claimant Name"},
                            ),
                            "claim_description": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Claim Description"},
                            ),
                            "date_claim_made": hx.Date(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Date Claim Made"},
                            ),
                            "date_claim_closed": hx.Date(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Date Claim Closed"},
                            ),
                            "current_status": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Current Status"},
                                options=["Open", "Closed"],
                            ),
                            "paid_defense": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Paid Defense"},
                            ),
                            "outstanding_defense": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Outstanding Defense"},
                            ),
                            "paid_indemnity": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Paid Indemnity"},
                            ),
                            "outstanding_indemnity": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Outstanding Indemnity"},
                            ),
                            "attachment": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Attachment"},
                            ),
                            "limit": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Limit"},
                            ),
                            "currency": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                options_table="table_input_currency",
                                options_column="ccy",
                                view={"label": "Currency"},
                            ),
                            "claim_type": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Claim Type"},
                            ),
                            "claim_location": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Claim Location"},
                            ),
                            "proc_code": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Proc Code"},
                            ),
                            "loss_date": hx.Date(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Loss Date"},
                            ),
                            "credit": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Credit"},
                            ),
                            "reviewed_indemnity_os": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Reviewed Indemnity OS"},
                            ),
                            "comments": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Comments"},
                            ),
                            "claimant_type": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Claimant Type"},
                            ),
                            "claimant_status": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Claimant Status"},
                            ),
                            "cause_of_loss": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Cause of Loss"},
                            ),
                            "area_of_practice": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Area of Practice"},
                            ),
                        },
                    ),
                }
            ),
        },
    )
