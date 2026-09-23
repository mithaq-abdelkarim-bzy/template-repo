import hx_data_schema as hx
import data_schema.sch_utilities as utils
# from data_schema.rate_risk_information import rate_risk_information

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "policy_option_id": hx.Int(mode="output", view={"label": "Policy Option ID", "format": {"thousandSeparated": False, "mantissa": 0}}),
        
        # Broker Details
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),

        "broker_sub_category": hx.Str(mode="input", default="", view={"label": "Broker Sub-Category"}),

        "is_policy_tag_error": hx.Bool(mode="output", async_output=["generate_tags"]),
        "policy_tag_msg": hx.Str(mode="output",  async_output=["generate_tags"], view={"label": "Policy Tags Feedback"}),
        "level_1_us_exp_msg": hx.Str(mode="output", view={"label": "Note"}),

        "level_1_us_exp_flag": hx.Bool(mode="output", view={"label": "Note"})

   })


    cds.extend_node_rater_defined("cds/key_industry", {
        # SIC dropdowns to change with sector
        "sic_dropdown" : hx.List(mode="output",children={
            "SICClass" :hx.Str(mode="output", view={"label": "SIC Description"})
        }),
    })


    # Override properties
    cds.override_node_properties('cds/standard_fields/underwriter', {'options_table': "tbl_underwriter", 'options_column': "Underwriters", "async_input": ['generate_tags', 'generate_uw_rationale_doc_task'], "view": {"options": {"notSupported": {"style_cell": "hx-neutral"}}}})
    cds.override_node_properties('cds/standard_fields/broker', {'options_table': "lst_broker", 'options_column': "Value", "async_input": ['generate_tags'], "view": {"options": {"notSupported": {"style_cell": "hx-neutral"}}}})


    cds.override_node_properties('cds/standard_fields/insured_name', {"options_table": "tbl_insured_name", "options_column": "FirmName", "allow_custom_value": True, "async_input": ["start_renewal_task",'capiq_fetch_task', 'save_uw_to_pas_reference', 'generate_tags', 'generate_uw_rationale_doc_task','generate_climate_doc_task'], 
        "async_output" : ["populate_capiq_data_task"], 
        "view": {"options": {
        "input": {"label": "Insured Name"},
        "read_only": {"label": "Insured Name", "read_only": True}}}})

    cds.override_node_properties('cds/standard_fields/is_renewal', {"async_input": ["start_renewal_task", "expiring_policy_fetch_task"], "async_output": ["start_renewal_task"], "view": {"options": {"input": {"label": "Is Renewal"}}}})
        
    cds.override_node_properties(
    'cds/currencies/source_currency',
    {
        'default': "USD",
        'async_input': ["rarc_task", "populate_capiq_data_task"],
        "optionality":"optional",
        'options': [
        'USD', 'EUR', 'GBP', 'CAD', 'CHF','AED', 'AFN', 'ALL', 'AMD', 'AOA', 'ARS', 'AUD', 'AWG', 
        'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 
        'BOB', 'BRL', 'BTN', 'BWP', 'BZD',  'CDF', 'CLP', 
        'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 
        'DZD', 'EGP', 'ETB', 'FJD', 'GEL', 'GHS', 'GMD', 
        'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HTG', 'HUF', 'IDR', 'ILS', 
        'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KHR', 
        'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 
        'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 
        'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NIO', 'NOK', 
        'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 
        'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SCR', 'SDG', 
        'SEK', 'SGD', 'SHP', 'SOS', 'SYP', 'SZL', 'THB', 'TND', 'TRY', 
        'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VND', 'VUV', 
        'XAF', 'XCD', 'XOF', 'XPF', 'YER', 'ZAR', 'ZWD'],
        "view": {"options": {
        "input": {"label": "Source Currency"},
        "read_only": {"label": "Source Currency", "read_only": True}}}})

    cds.override_node_properties('cds/key_industry/code_type', {'mode': "output"})
    cds.override_node_properties('cds/key_industry/code', {'mode': "output"})
    cds.override_node_properties('cds/key_industry/code_name', {'mode': "output"})


    #cds.override_node_properties('cds/core_account', {'options_table': "lst_core_account", 'options_column': "CoreAccount"})

    # Defining risk information that do not below in any buckets (e.g. rating factors or modifiers..;)
    cds.extend_node_rater_defined("cds", {
        "risk_information": hx.Structure(view ={ "label": "Risk Information"}, children = {
            "cips_policy": hx.Str(mode="input", default="No", optionality="required", options_table="lst_yn", options_column="yesno" ,view={"label": "CIPS Policy"}),
            "core_account": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_core_account", options_column="CoreAccount" ,view={"label": "Core Account"}),
            "platform": hx.Str(mode="input", default="Lloyd's", optionality="required", options_table="lst_platform", options_column="platform" ,view={"label": "Platform"}),
            "epl_sublimit": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "EPL Sub-Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "epl_sublimit_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "EPL Sub-Limit Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "afb_primary_wording_manuscript": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_yn", options_column="yesno" ,view={"label": "AFB Primary and Wording Manuscript"}),
            "long_term_agreement": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_yn", options_column="yesno" ,view={"label": "Long Term Agreement"}),
            "esg_syndicate": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_esg_status", options_column="esg syndicate status" ,view={"label": "ESG Syndicate Status"}),
            "direct_ri": hx.Str(mode="input", default="Direct", options_table="lst_direct_ri", options_column="directri" ,view={"label": "Direct/RI"}),
            "esg_net_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ESG Net Written Premium (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}, validation={"min_value": 0}),
            "cedant_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Cedant Name"}),
            "any_one_claim": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_yn", options_column="yesno" ,view={"label": "Any One Claim (AOC)"}),
            "company_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Company Description"}),
            "comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),                        
            "test_info": hx.Str(mode="output", view={"label": "Test Info"}),
            "pe_backer": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_pe_backer", options_column="value" ,view={"label": "PE Backer"}),
            "other_pe_backer": hx.Str(mode="input", default=None, optionality="optional", view={"label": "If Other Please Specify"}),
            "macquarie_flag": hx.Str(mode="input", default="No", optionality="required", options_table="lst_yn", options_column="yesno" ,view={"label": "Macquarie"}),                        
            "other_pe_backer_flag": hx.Bool(mode="output", view={"label": "Other PE Backer Flag"}),
            "public_flag": hx.Bool(mode="output", view={"label": "Public Flag"}),
            "private_flag": hx.Bool(mode="output", view={"label": "Private Flag"}),
            "public_us_flag": hx.Bool(mode="output", view={"label": "Public and US Flag"}),
            "adr_level_one_flag": hx.Bool(mode="output", view={"label": "ADR Level 1 Flag"}),
            "mmp_flag": hx.Bool(mode="input",default=False, async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Middle Market"}),
            "not_mmp_flag": hx.Bool(mode="output", view={"label": "Not Middle Market Private"}),
            "ri_flag": hx.Bool(mode="output", view={"label": "RI Flag"}),
            "beazley_branch": hx.Str(mode="output", view={"label": "Beazley Branch"}),
            "climate_litigation": hx.Str(mode="output", view={"label": "Climate Litigation Heatmap Dashboard"}),
            "underwriting_assistant": hx.Str(mode="input", default=None, optionality="optional",  options_table="lst_underwriting_assistant", options_column="Underwriter Assistant", view={"label": "Underwriting Assistant", "options": {"notSupported": {"style_cell": "hx-neutral"}}}),
            "date_validation": hx.Str(mode="output", view={"label": "Date Validation"}),
            "date_validation_flag": hx.Bool(mode="output", view={"label": "Date Validation Flag"}),
            #"climate_document": hx.File(mode="output", async_output=["generate_climate_doc_task"], file_name="climate_litigation_spotlight.docx", view={"label": "Document"}),
            "climate_document": hx.File(mode="output", async_output=["generate_climate_doc_task"], file_name="climate_litigation_spotlight.docx", view={"label": "Document"}),       
            "climate_document_country": hx.Str(mode="input", async_input=["generate_climate_doc_task"], optionality="required", options=["Australia", "France", "Germany", "The Netherlands", "United Kingdom"], default="Australia", view={"label": "Country"}),                               
            "climate_document_industry": hx.Str(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["generate_climate_doc_task"],
                options_data="../climate_document_industry_options",
                options_field="industry",
                view={"label": "Industry"},
            ),
            "climate_document_industry_options": hx.List(
                mode="output",
                children={
                    "industry": hx.Str(mode="output", view={"label": "Industry"}),
                },
            ),
            "climate_document_industry_infoby": hx.Str(mode="output")
        }) 
    })
    # Defining rating factors risk information 
    cds.extend_node_rater_defined("cds", {
        "rating_factors": hx.Structure(view ={ "label": "Risk Information"}, children = {            
            "risk_information": hx.Structure(view ={ "label": "Rating Factors"}, children = {            
                "ownership_type": hx.Str(mode="input", default="Public", optionality="required", options_table="lst_ownership", options_column="value", async_input=["rarc_task"], view={"label": "Ownership Type","options": {"input": {"label": "Ownership Type"}, "read_only": {"label": "Ownership Type", "read_only": True}}}),
                "us_adr_exposure": hx.Str(mode="input", default="No", optionality="required", options_table="lst_yn", options_column="yesno", async_input=["rarc_task"], view={"label": "US ADR Exposure"}),      
                "country_of_domicile": hx.Str(mode="input", default="UNITED KINGDOM", optionality="required", options_table="lst_country", options_column="country", async_input=["rarc_task"], view={"label": "Country of Domicile","options": {"input": {"label": "Country of Domicile"}, "read_only": {"label": "Country of Domicile", "read_only": True}}}),
                "main_operating_country": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_country", options_column="country", async_input=["rarc_task"], view={"label": "Main Operating Country","options": {"input": {"label": "Main Operating Countrye"}, "read_only": {"label": "Main Operating Country", "read_only": True}}}),
                "primary_listing_location": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_country", options_column="country", async_input=["rarc_task"], view={"label": "Primary Listing Location"}),
                "search_sic": hx.Str(mode="input", default="Class", optionality="required", async_input=["populate_capiq_data_task"], options=["Class", "SIC Code"],view={"label": "Search SIC By"}),                        
                "industry_class_sic_code": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=["populate_capiq_data_task"], view={"label": "Industry-Class-SIC Code", "options": {"input": {"label": "Industry-Class-SIC Code"}, "read_only": {"label": "Industry SIC Code", "read_only": True}}}),            
                "policy_term": hx.Float(mode="output"),
            }),
        })
    })


    cds.extend_node_rater_defined("cds", {
        "uw_rationale": hx.Structure(view ={ "label": "Risk Information"}, children = {        
            "broker_discussion": hx.Str(mode="input", default=None, optionality="optional", async_input=["generate_uw_rationale_doc_task"], view={"label": "1. Summary  of Programme Discussion with Broker"}),
            "unusual_coverage": hx.Str(mode="input",default=None, optionality="optional", async_input=["generate_uw_rationale_doc_task"], view={"label": "2. Wording and any Unusual Coverage"}),
            "other_factors": hx.Str(mode="input",default=None, optionality="optional", async_input=["generate_uw_rationale_doc_task"], view={"label": "3. Any Other Factors not Captured Elsewhere"}),
            "esg": hx.Str(mode="input",default=None, optionality="optional", async_input=["generate_uw_rationale_doc_task"], view={"label": "4. ESG"}),
            "esg_info": hx.Str(mode="output", async_input=["generate_uw_rationale_doc_task"]),
            "bpi_comment": hx.Str(mode="input",default=None, optionality="optional", async_input=["generate_uw_rationale_doc_task"], view={"label": "5. I am Writing this Because (including comments on BPI)"}),
            "bpi_comment_info": hx.Str(mode="output", async_input=["generate_uw_rationale_doc_task"]),
            "file_upload_1": hx.File(mode="input", async_input=["rarc_task"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
            "file_upload_2": hx.File(mode="input", async_input=["rarc_task"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
            "file_upload_3": hx.File(mode="input", async_input=["rarc_task"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
            "file_upload_4": hx.File(mode="input", async_input=["rarc_task"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
            "file_upload_5": hx.File(mode="input", async_input=["rarc_task"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
            "file_upload_6": hx.File(mode="input", async_input=["rarc_task"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
            "file_upload_7": hx.File(mode="input", async_input=["rarc_task"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
            "file_upload_8": hx.File(mode="input", async_input=["rarc_task"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
            "file_download_1": hx.File(mode="output", async_output=["generate_uw_rationale_doc_task"], file_name="uw_rationale_doc.docx", view={"label": "UW Rationale Document"}),
            "file_download_2": hx.File(mode="output", async_output=["generate_uw_rationale_doc_task"], file_name="unused2.docx", view={"label": "UW Rationale Document"}),
            "file_download_3": hx.File(mode="output", async_output=["generate_uw_rationale_doc_task"], file_name="unused3.docx", view={"label": "UW Rationale Document"}),
            "file_download_4": hx.File(mode="output", async_output=["generate_uw_rationale_doc_task"], file_name="unused4.docx", view={"label": "UW Rationale Document"}),
        }),
    })

    # Override dropdown links
    cds.override_node_properties(
        'cds/rating_factors/risk_information/industry_class_sic_code', 
        {"async_input": ["rarc_task"], 'options_data': "../../../key_industry/sic_dropdown", 'options_field': "SICClass", "view": {"label":"SIC Description", "multiline": True}}
        )
