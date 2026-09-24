import hx_data_schema as hx
from data_schema.sch_utilities import create_node


def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        "risk_information": hx.Structure(
            children={
                "deal_status":              hx.Str( mode="input", default="Quoted", options_column="deal_status", options_table="table_input_deal_status", view={"label": "Deal Status"}, async_input=["generate_excel_document_task", "generate_word_document_task"], async_output=["start_renewal_task"]  ),
                "facility_type":            hx.Str( mode="input", default=None, optionality="optional", options_column="facility_type", options_table="table_input_facility_type", view={"label": "Facility Type"}, 
                                                                                async_input=["generate_excel_document_task", "generate_word_document_task"], async_output =['fetch_bbt_task', "start_renewal_task"]),
                "expiring_option_id":       hx.Int( mode="input", default=None, optionality="optional", async_input=["start_renewal_task"], view={"label": "Expiring Option Id", "format": {"thousandSeparated": False, "mantissa": 0} }),
                "is_large_model_mode":      hx.Bool(mode="input", default=False, optionality="required", view={"label": "Large Model Mode"}, 
                                                                                async_input=["import_policy_data_from_csv_task", "import_claim_data_from_csv_task", "get_column_headers_from_policy_data_csv_task","get_column_headers_from_claim_data_csv_task","write_policy_claim_data_to_hxd_task"],
                                                                                async_output=["start_renewal_task"]),
                "follow_main_syndicate":    hx.Bool(mode="input", default=False, view={"label": "Follow Main Syndicate Pricing?"}, async_input=["fetch_bbt_task", "calculate_profit_commission_task", "generate_word_document_task"], async_output=["start_renewal_task"]),
                "bbt_option_id":            hx.Int( mode="input", default=None, optionality="optional", view={"label": "BBT Option ID", "format":{"thousandSeparated": False, "mantissa": 0}}, async_input=["fetch_bbt_task", "generate_word_document_task"]),
                "prem_data_available":      hx.Bool(mode="input", default=True, view={"label": "Premium Data available?"},async_output=["start_renewal_task"]),
                "is_profit_comission":      hx.Bool(mode="input", default=False, view={"label": "Is there a Profit Commission?"}, async_output =['fetch_bbt_task',"start_renewal_task"], async_input=["generate_word_document_task", "generate_excel_document_task"]),
                "insured_data_date":        hx.Date(mode="input", default=None,     optionality="optional", view={"label": "Insured Data as at Date"}, async_input=[]),
                "data_yoa_basis":           hx.Str( mode="input", default_index=0, options=["Calendar Year","Policy Year"], view={"label": "Data YOA Basis"}, async_input=[],async_output=["start_renewal_task"]),
                "det_claims_data_available":hx.Bool(mode="input", default=False,    view={"label": "Detailed Claims Data available?"},async_output=["start_renewal_task"]),
                "cat_modelling_available":  hx.Bool(mode="input", default=False,    view={"label": "CAT Modelling Available?"},async_output=["start_renewal_task"]),
                "broker_contact":           hx.Str( mode="input", default=None,     optionality="optional",allow_custom_value=True, options_column="broker_contact", options_table="table_input_broker_details", view={"label": "Broker Contact"}, async_output =['fetch_bbt_task',"start_renewal_task"]),
                "broker_email":             hx.Str( mode="override",                view={"label": "Broker Email"}),
                "broker_location":          hx.Str( mode="override",                    view={"label": "Broker Location"}),
                "show_refs":                hx.Bool(mode="input", default=False,        view={"label": "Show References"},async_output=["start_renewal_task"]),
                "priced_by":                hx.Str( mode="input", default="Underwriting", options=["Underwriting", "Actuarial"], optionality="required", view={"label": "Priced By"}, async_input=["generate_word_document_task"],async_output=["start_renewal_task"]),
                "actuary_reviewed":         hx.Str( mode="input", default_index=0, options=["Priya Bhalla", "Asa Euridge", "Yifei Zhao", "Rita Zannetou", "Joe Delaney", "Shathu Berinbarasah", "Freddie Shortland", "Ella Boateng"],  allow_custom_value=True, optionality="required", view={"label": "Actuary Reviewed"}),
                "bbt_last_fetch_time":      hx.Str(mode="output", async_output=["fetch_bbt_task"])
            }
        )
    })
