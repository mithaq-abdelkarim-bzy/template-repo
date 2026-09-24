import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format


def get_float_values():
    return [
        ("gross_premium", "Gross Premium"),
        ("net_premium", "Net Premium"),
        ("paid_attritional", "Paid Attritional"),
        ("paid_large", "Paid Large"),
        ("paid_cat", "Paid CAT"),
        ("paid_total", "Paid Total"),
        ("incurred_attritional", "Incurred Attritional"),
        ("incurred_large", "Incurred Large"),
        ("incurred_cat", "Incurred CAT"),
        ("incurred_total", "Incurred Total"),
        ("sum_insured_tiv", "Sum Insured/TIV"),
        ("limit", "Limit"),
        ("attachment", "Attachment")
    ]

def get_float_values_outputs():
    return[
        ("gross_premium_cnv", "Gross Premium CNV"),
        ("net_premium_cnv", "Net Premium CNV"),
        ("paid_attritional_cnv", "Paid Attritional CNV"),               
        ("paid_large_cnv", "Paid Large CNV"),
        ("paid_cat_cnv", "Paid CAT CNV"),
        ("paid_total_cnv", "Paid Total CNV"),
        ("incurred_attritional_cnv", "Incurred Attritional CNV"),
        ("incurred_large_cnv", "Incurred Large CNV"),
        ("incurred_cat_cnv", "Incurred CAT CNV"),
        ("incurred_total_cnv", "Incurred Total CNV"),
    ]

def get_int_values():
    return [
    ("yoa", "YOA"),
    ]

def get_string_values():
    return [
    ("umr", "UMR"),
    ("policy_reference", "Policy Reference"),
    ("account_name", "Account Name"),
    ("facility_lob", "Facility LoB"),    
    ("risk_code", "Risk Code"),    
    ("risk_location", "Risk Location"),
    ("industry_type", "Industry Type"),
    ("region", "Region"),
    ("occupancy_property", "Occupancy (Property Only)"),
    ("habitational", "Habitational/Non-Habitational/Mixed"),
    ("slip_leader", "Slip Leader"),
    ("naic_sic", "NAIC/SIC"),
    ("month_processed", "Month Processed"),
    ("inception_date", "Inception Date"),
    ("expiry_date", "Expiry Date"),
]


def get_date_values():
    return []


def sch_policy_level_data(cds):
    cds.extend_node_rater_defined(
        "cds", 
        {
            "policy_level_data_table": hx.Structure(
                view={"label":"Policy Level Data"},
                children={
                    "as_at_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "As At Date"}),
                    "req_fields":hx.Str(mode="output", view={"label": "Required Fields"}), 
                    "replacement_log": hx.Str(mode="output", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy"], async_input=["get_column_headers_from_policy_data_csv_task"],view={"label": "Replacement Log"}),
                    "show_importer": hx.Bool(mode="input", default=False, view={"label": "Show Data Importer"}),
                    "clear_table": hx.Bool(mode="output", async_output=["clear_policy_level_table_task"]),
                    "unformatted_sov_file": hx.File(mode="input", async_input=["get_column_headers_from_policy_data_csv_task", "import_policy_data_from_csv_task"], file_extension=["csv", "xlsx"], view={"label": "Unformatted File"}),
                    "renew_sov_column_dropdown": hx.List(mode="input", async_output=["get_column_headers_from_policy_data_csv_task"], children={
                        "renew_column": hx.Str(mode="input", optionality="optional", default=None, async_output=["get_column_headers_from_policy_data_csv_task"])
                    }),
                    "unformatted_file_column_mapping": hx.List(mode="input", async_input=["import_policy_data_from_csv_task"], async_output="get_column_headers_from_policy_data_csv_task", children={
                        "unformatted_column": hx.Str(mode="output", async_input=["import_policy_data_from_csv_task"], async_output="get_column_headers_from_policy_data_csv_task", view={"label": "File\nColumn"}),
                        "renew_column": hx.Str(mode="input", default=None, optionality="optional", options_data="../../../renew_sov_column_dropdown", options_field="renew_column", async_input=["import_policy_data_from_csv_task"], async_output="get_column_headers_from_policy_data_csv_task", view={"label": "Renew\nColumn"}),
                        "similarity_score": hx.Int(mode="output", view={"label": "Similarity\nScore"}, async_input=["import_policy_data_from_csv_task"])
                    }),

                    "policy_level_data": hx.List(
                        mode="input",
                        async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"],
                        async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"],
                        children={
                            **{
                                field: hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"], async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": label, "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}})
                                for field, label in get_float_values()
                            },
                            **{
                                field: hx.Int(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"], async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": label, "format": {"thousandSeparated": False, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}})
                                for field, label in get_int_values()
                            },
                            **{
                                field: hx.Str(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"], async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": label, "options": {"read_only_option": {"read_only": True}}})
                                for field, label in get_string_values()
                            },
                            **{
                                field: hx.Date(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"], async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": label, "options": {"read_only_option": {"read_only": True}}})
                                for field, label in get_date_values()
                            },
                            "order_per": hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"], async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Order %", "format": percent_format(2), "options": {"read_only_option": {"read_only": True}}}),
                            "risk_code": hx.Str(mode="input", default=None, async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"], optionality="optional", view={"label": "Risk Code", "options": {"read_only_option": {"read_only": True}}}),
                            "currency": hx.Str(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"], async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], options_column="ccy", options_table="table_currency", optionality='optional', default="USD", view={"label": "Currency", "options": {"read_only_option": {"read_only": True}}}),
                            "limit_attachment_currency": hx.Str(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"], async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], allow_custom_value=True, default=None, optionality="optional", options=["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], view={"label": "Limit and Attachment Currency", "options": {"read_only_option": {"read_only": True}}}),
                            "primary": hx.Str(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task"], async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], allow_custom_value=True, default=None, optionality="optional", options=["Yes", "No"], view={"label": "Primary", "options": {"read_only_option": {"read_only": True}}}),
                            "modelled": hx.Str(mode="output", async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], view={"label": "Modelled?"}),
                            "selected_lob": hx.Str(mode="output", 
                            async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], 
                            view={"label": "Selected LOB"}
                            ),
                            **{
                                field: hx.Float(mode="output", async_input=["pre_group_policy_data_task" ,"get_column_headers_from_policy_data_csv_task"], view={"label": label, "format": {"thousandSeparated": True, "mantissa": 0}})
                                for field, label in get_float_values_outputs()
                            }
                        }
                    ),
                    "use_policy_level_data_grouped": hx.Bool(mode="input", async_input=["get_column_headers_from_policy_data_csv_task"], async_output=["un_group_policy_data_task", "pre_group_policy_data_task", {"task": "import_policy_data_from_csv_task", "reset": False}, "clear_policy_level_table_task"], default=False),
                    "use_policy_level_data_ungrouped": hx.Bool(mode="output"),
                    "policy_level_data_grouped": hx.List(
                        mode="input",
                        async_output=["pre_group_policy_data_task", "import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task"],
                        async_input=["get_column_headers_from_policy_data_csv_task"],
                        children={
                            "account_name": hx.Str(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Account Name", "options": {"read_only_option": {"read_only": True}}}),
                            "facility_lob": hx.Str(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Facility LoB", "options": {"read_only_option": {"read_only": True}}}),
                            "yoa": hx.Int(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "YOA", "format": {"thousandSeparated": False, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "risk_code": hx.Str(mode="input", default=None, async_input=["get_column_headers_from_policy_data_csv_task"], async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], optionality="optional", view={"label": "Risk Code", "options": {"read_only_option": {"read_only": True}}}),
                            "currency": hx.Str(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], options_column="ccy", options_table="table_currency", optionality='optional', default="USD", view={"label": "Currency", "options": {"read_only_option": {"read_only": True}}}),
                            "gross_premium":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Gross Premium", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "net_premium":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Net Premium", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "paid_attritional":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Paid Attritional", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "paid_large":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Paid Large", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "paid_cat":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Paid CAT", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "paid_total":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Paid Total", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "incurred_attritional":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Incurred Attritional", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "incurred_large":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Incurred Large", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "incurred_cat":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Incurred CAT", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                            "incurred_total":  hx.Float(mode="input", async_output=["import_policy_data_from_csv_task", "resolve_sov_rows_task_policy", "clear_policy_level_table_task","un_group_policy_data_task", "pre_group_policy_data_task"], async_input=["get_column_headers_from_policy_data_csv_task"], default=None, optionality="optional", view={"label": "Incurred Total", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only_option": {"read_only": True}}}),
                        }
                    )
                }
            ),
        }
    ) 