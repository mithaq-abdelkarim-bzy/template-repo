import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format


def get_float_values():
    return [        
        ("paid", "Paid"),
        ("outstanding", "Outstanding"),
        ("incurred", "Incurred")       
    ]

def get_float_values_outputs():
    return[     
        ("paid_cnv", "Paid CNV"),
        ("outstanding_cnv", "Outstanding CNV"),
        ("incurred_cnv", "Incurred CNV")      
    ]

def get_int_values():
    return [    
    ("yoa", "YOA"),    
    ]

def get_string_values():
    return [
    ("umr", "UMR"),
    ("policy_reference", "Policy Reference"),
    ("claim_reference", "Claim Reference"),
    ("account_name", "Account Name"),
    ("facility_lob", "Facility LoB"), 
    ("claim_status", "Claim Status"),   
    ("risk_code", "Risk Code"),
    ("claim_type", "Claim Type"), 
    ("cat_code", "Cat Code"),  
    ("month_processed", "Month Processed"),
    ("loss_date", "Loss Date"),
    ("claim_made_date", "Claim Made Date"),
    ("closed_date", "Closed Date")   
]

def get_date_values():
    return []


def sch_claim_level_data(cds):
    cds.extend_node_rater_defined(
        "cds", 
        {
            "claim_level_data_table": hx.Structure(
                view={"label":"Claim Level Data"},
                children={
                    "as_at_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "As At Date"}),
                    "req_fields":hx.Str(mode="output", view={"label": "Required Fields"}), 
                    "replacement_log": hx.Str(mode="output", async_output=["import_claim_data_from_csv_task", "resolve_sov_rows_task"], async_input=["get_column_headers_from_claim_data_csv_task"],view={"label": "Replacement Log"}),
                    "show_importer": hx.Bool(mode="input", default=False, view={"label": "Show Data Importer"}),
                    "clear_table": hx.Bool(mode="output", async_output=["clear_claim_level_table_task"]),
                    "unformatted_sov_file": hx.File(mode="input", async_input=["get_column_headers_from_claim_data_csv_task", "import_claim_data_from_csv_task"], file_extension=["csv", "xlsx"], view={"label": "Unformatted File"}),
                    "renew_sov_column_dropdown": hx.List(mode="input", async_output=["get_column_headers_from_claim_data_csv_task"], children={
                        "renew_column": hx.Str(mode="input", optionality="optional", default=None, async_output=["get_column_headers_from_claim_data_csv_task"])
                    }),
                    "unformatted_file_column_mapping": hx.List(mode="input", async_input=["import_claim_data_from_csv_task"], async_output="get_column_headers_from_claim_data_csv_task", children={
                        "unformatted_column": hx.Str(mode="output", async_input=["import_claim_data_from_csv_task"], async_output="get_column_headers_from_claim_data_csv_task", view={"label": "File\nColumn"}),
                        "renew_column": hx.Str(mode="input", default=None, optionality="optional", options_data="../../../renew_sov_column_dropdown", options_field="renew_column", async_input=["import_claim_data_from_csv_task"], async_output="get_column_headers_from_claim_data_csv_task", view={"label": "Renew\nColumn"}),
                        "similarity_score": hx.Int(mode="output", view={"label": "Similarity\nScore"}, async_input=["import_claim_data_from_csv_task"])
                    }),
                    "claim_level_data": hx.List(
                        mode="input", 
                        async_output=["import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task"], 
                        async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"],
                        view={"label": "Claim Level Data"},
                        children={
                            **{
                                field: hx.Float(mode="input", async_output=["import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task"], async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": label, "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}})
                                for field, label in get_float_values()
                            },
                            **{
                                field: hx.Float(mode="output", async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], view={"label": label, "format": {"thousandSeparated": True, "mantissa": 0}})
                                for field, label in get_float_values_outputs()
                            },
                            **{
                                f"{field}_input": hx.Float(mode="input", default=None, optionality="optional", async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], view={"label": label, "options": {"read_only_option": {"read_only": True}}})
                                for field, label in get_float_values_outputs()
                            },
                            **{
                                field: hx.Int(mode="input", async_output=["import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task"], async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": label, "format": {"thousandSeparated": False, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}})
                                for field, label in get_int_values()
                            },
                            **{
                                field: hx.Str(mode="input", async_output=["import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task"], async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": label, "options": {"read_only_option": {"read_only": True}}})
                                for field, label in get_string_values()
                            },
                            **{
                                field: hx.Date(mode="input", async_output=["import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task"], async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": label, "options": {"read_only_option": {"read_only": True}}})
                                for field, label in get_date_values()
                            },
                            "claim_type": hx.Str(mode="input", async_output=["import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task"], async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", options=["Attritional", "Large", "CAT"], view={"label": "Claim Type", "options": {"read_only_option": {"read_only": True}}}),
                            "currency": hx.Str(mode="input", async_output=["import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task"], async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], options_column="ccy", options_table="table_currency",  optionality='optional', default="USD", view={"label": "Currency", "options": {"read_only_option": {"read_only": True}}}),
                            "modelled": hx.Str(mode="output", async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], view={"label": "Modelled?"}),
                            "selected_lob": hx.Str(mode="output", async_input=["pre_group_claim_data_task", "get_column_headers_from_claim_data_csv_task"], view={"label": "Selected LOB"})
                        }
                    ),
                    "use_claim_level_data_grouped": hx.Bool(mode="input", async_input=["get_column_headers_from_claim_data_csv_task"], async_output=["un_group_claim_data_task", "pre_group_claim_data_task", {"task": "import_claim_data_from_csv_task", "reset": False}, "clear_claim_level_table_task"], default=False),
                    "use_claim_level_data_ungrouped": hx.Bool(mode="output"),
                    "claim_level_data_grouped": hx.List(
                        mode="input", 
                        async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], 
                        async_input=["get_column_headers_from_claim_data_csv_task"],
                        view={"label": "Claim Level Data"},
                        children={
                            "facility_lob": hx.Str(mode="input", async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": "Facility LoB", "options": {"read_only_option": {"read_only": True}} }),
                            "yoa": hx.Int(mode="input", async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": "YOA", "format": {"thousandSeparated": False, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "claim_status": hx.Str(mode="input", async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": "Claim Status", "options": {"read_only_option": {"read_only": True}}}),
                            "risk_code": hx.Str(mode="input", async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": "Risk Code", "options": {"read_only_option": {"read_only": True}}}),
                            "currency": hx.Str(mode="input", async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], options_column="ccy", options_table="table_currency",  optionality='optional', default="USD", view={"label": "Currency", "options": {"read_only_option": {"read_only": True}}}),
                            "claim_type": hx.Str(mode="input", async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", options=["Attritional", "Large", "CAT"], view={"label": "Claim Type", "options": {"read_only_option": {"read_only": True}}}),
                            "paid": hx.Float(mode="input", async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": "Paid", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "outstanding": hx.Float(mode="input", async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": "Outstanding", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "incurred": hx.Float(mode="input", async_output=["pre_group_claim_data_task", "import_claim_data_from_csv_task", "resolve_sov_rows_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], default=None, optionality="optional", view={"label": "Incurred", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "selected_lob": hx.Str(mode="input", default="", async_output=["pre_group_claim_data_task", "clear_claim_level_table_task", "un_group_claim_data_task"], async_input=["get_column_headers_from_claim_data_csv_task"], view={"label": "Selected LOB"})
                        }
                    ),
                }
            ),
        }
    ) 



