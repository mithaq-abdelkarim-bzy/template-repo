import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
        "rating_methodology": hx.Str(mode="input", default="Public D&O", options=["Public D&O", "Private D&O"], view={"label": "Public D&O / Private D&O"}),
        # Policy Tag error msg
        "policy_tag_error": hx.Str(mode="output",  async_output=["generate_tags_cuap", "generate_tags_twice"]),
        "is_policy_tag_error": hx.Bool(mode="output", async_output=["generate_tags_cuap", "generate_tags_twice"]),
                                
        # Broker Details
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),

        #additional coverage details 
        # "coverage_details": hx.Str(mode="input", default_index=0, options_table="form_options", options_column="form", view={"label": "Policy Form"}),                
        "coverage_details": hx.Str(mode="input", default="", optionality="optional", allow_custom_value=True, view={"label": "Policy Form"}),

        # Building the CapIQ output table
        "capiq_results" : hx.Str(mode="input", default=None, optionality="optional", async_output=["capiq_fetch_task"], view={"read_only": True, "label": "Results"}),
        "capiq_search_complete" : hx.Bool(mode="input", default=None, optionality="optional",  async_output=["capiq_fetch_task"]),
        "capiq_search": hx.Str(mode="input", default=None, async_input=["populate_capiq_data_task", "capiq_fetch_task", "rarc_task"], optionality="optional", view={"label": "Ticker Search"}),
        "capiq_selection" : hx.Int(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], view={"label": "Selected Row Number"}),
        "capiq_populate" : hx.Str(mode="input", default=None, optionality="optional", async_output=["populate_capiq_data_task"], view={"read_only": True, "label": "Status"}),
        "capiq": hx.List(mode="input", async_output=["capiq_fetch_task"], async_input=["populate_capiq_data_task"], children={
            "selection" : hx.Bool(mode="input", async_input=["populate_capiq_data_task"], default=False, optionality="required", view={"label": "Select One"}),
            "id" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"], view={"read_only": True, "label": "Company ID"}),
            "company_name" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"], view={"read_only": True, "label": "Company"}),
            "exchange" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"], view={"read_only": True, "label": "Exchange"}),
            "market_cap" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"], view={"read_only": True, "label": "Market Cap"}),
            "date_updated" : hx.Date(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"], view={"read_only": True, "label": "Date Updated"}),
            "sic_code" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "ipo_date" : hx.Date(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"], view={"read_only": True, "label": "Date Updated"}),
            "ticker" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "hq_state" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "incorporated_state" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "hq_city" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "minimum_trading_volume" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "volatility_of_trading" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "execs_under_age_50" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "year_founded" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "total_assets" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "ebit" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "current_assets" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "total_liabilities" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "current_liabilities" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "retained_earnings" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "net_sales" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "market_value_of_equity" : hx.Float(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "source" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
            "company_description" : hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], async_output=["capiq_fetch_task"]),
        }),
        "capiq_refresh_date": hx.Date(mode="input", default=None, optionality="optional", async_output=["populate_capiq_data_from_wb_task", "populate_capiq_data_task"], view={"label": "Refresh Date"}),
        # TODO: make an input to the landing page async task once the connection to Workbench is built
        "capiq_wb_id" : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Company ID"}, async_input=["populate_capiq_data_from_wb_task"]),

        # Trifocus dropdown is US surplus
        "trifocus_us_surplus": hx.Str(mode="input", default="BUSA D&O MM", optionality="required", options=["BESI D&O MM", "BUSA D&O MM"], view={"label": "Trifocus"}),

        # Mandatory fields
        "market_cap_mandatory": hx.Bool(mode="output"),
        "market_cap_complete": hx.Bool(mode="output"),
        "sector_mandatory": hx.Bool(mode="output"),
        "sector_complete": hx.Bool(mode="output"),
    })

     # private D&O fields 
    cds.extend_node_rater_defined("cds/exposure/aggregate",{
        "private_company_financials":hx.Structure(children={
            "long_term_debt" : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Long Term Debt", "format": utils.thousands_format(2)}),
            "equity" : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Equity", "format": utils.thousands_format(2)}),
            "revenue" : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Revenue", "format": utils.thousands_format(2)}),
            "cash" : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Cash", "format": utils.thousands_format(2)}),
            "net_income" : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Net Income", "format": utils.thousands_format(2)}),
            "free_cash_flow" : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Free Cash Flow", "format": utils.thousands_format(2)}),
            "latest_post_money_val" : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Latest Post Money Valuation", "format": utils.thousands_format(2)}),
            "date_of_latest_post_money_val" : hx.Date(mode="input", default=None, optionality="optional", view={"label": "Date ofLatest Post Money Valuation"}),
            })
        }),


    cds.extend_node_rater_defined("cds/key_industry", {
        "sic_mandatory": hx.Bool(mode="output"),
        "sic_complete": hx.Bool(mode="output"),
    }),

    # create node to determine how the rater is priced
    cds.extend_node_rater_defined("cds", {
        "review_type": hx.Structure(children={
            "rater_priced": hx.Bool(mode="output", async_input=["rarc_task"]),
            "private_priced": hx.Bool(mode="output", async_input=["rarc_task"]),
        })
    })


    # Defining boolean fields manually as default and optionality cannot be changed in the csv
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "ignore_ipo": hx.Bool(mode="input", default=False, view={"label": "Ignore IPO"}),
        "show_mcap_comment": hx.Bool(mode="input", default=False, view={"label": "Expand Market Cap Comment"}),
        "show_ipo_comment": hx.Bool(mode="input", default=False, view={"label": "Expand IPO Comment"}),
    })

    cds.extend_node_rater_defined("cds/exposure/aggregate", {"transaction_type": hx.Str(mode="input", default="Non Applicable", options=["Non Applicable", "SPAC", "De-SPAC", "Traditional IPO", "Reverse Merger"], view={"label": "Transaction Type"})})
    cds.extend_node_rater_defined("cds/exposure/aggregate", {"crypto_classification": hx.Str(mode="input", default="Non Crypto", options=["Non Crypto", "Crypto"], view={"label": "Crypto Classification"})})


    cds.extend_node_rater_defined("cds/key_industry", {
        "blended_sic": hx.Bool(mode="input", default=False, view={"label": "Blended SIC"}),
    })

    cds.extend_node_rater_defined("cds/key_industry", {
        "show_override_comment": hx.Bool(mode="input", default=False, view={"label": "Expand Override Comment"}),
        "show_override_comment_2": hx.Bool(mode="input", default=False, view={"label": "Expand Override Comment 2"}),
        "show_override_comment_3": hx.Bool(mode="input", default=False, view={"label": "Expand Override Comment 3"}),
    })

    cds.extend_node_rater_defined("cds",{
        "is_runoff": hx.Bool(mode="input", default=False, view={"label": "Is Runoff"}),
        "runoff_adjustment_info": hx.Str(mode="output", view={"label": "Divide the quoted premium by this figure to arrive at the Runoff Original Premium"})
    })

#### Override dropwown links ####
    cds.override_node_properties('cds/standard_fields/underwriter', {'options_table': "table_input_underwriters", 'options_column': "underwriter", "allow_custom_value": True, "optionality":"optional",'async_input':['generate_tags_cuap', 'generate_tags_twice']})
    cds.override_node_properties('cds/standard_fields/broker', {'options_data': "../../../non_cds/broker_dropdown", 'options_field': "Broker", "allow_custom_value": True}),
    cds.override_node_properties('cds/rw_broker', {'options_data': "../../non_cds/us_broker_dropdown", 'options_field': "Broker", "allow_custom_value": True}),
    cds.override_node_properties('cds/company_country', {'options_table': "dd_country", 'options_column': "Country", "default":"USA", 'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task']})
    cds.override_node_properties('cds/company_state', {
        'options_table': "dd_state", 
        'options_column': "State", 
        'async_output': ['populate_capiq_data_task','populate_capiq_data_from_wb_task'], 
        'async_input': ["reset_admitted_reasons_task",'set_admitted_to_max_task','set_admitted_to_min_task','set_admitted_to_midpoint_task']
    })
    cds.override_node_properties('cds/incorporated_state', {'options_table': "dd_incorporated_state", 'options_column': "State", 'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task']})
    cds.override_node_properties('cds/hq_state', {'options_table': "dd_state", 'options_column': "State", 'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task']}) 
    cds.override_node_properties('cds/coverage', {'options': ["ABC", "Side A", "Armour"], 'async_input':['rarc_task', 'rc_private_task', 'generate_tags_cuap', 'generate_tags_twice']})
    cds.override_node_properties("cds/key_industry/code", {"mode":"output", "view": {"label": "SIC Code"}, 'async_input':['generate_tags_cuap']})
    # cds.override_node_properties(
    #     'cds/key_industry/sector_name', 
    #     {
    #         'options_table': "ref_base_frequencies", 
    #         'options_column': "Sector_Desc", 
    #         "view": {"multiline": True, "options": {"mandatory": {"style_cell": "hx-bad"}}}, 
    #         'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task']
    #     }
    # )
    cds.override_node_properties("cds/key_industry/sector_name", {"mode":"output", "view":{"label": "Sector"}})
    cds.override_node_properties("cds/key_industry/sector_2", {"mode":"output", "view":{"label": "Sector 2"}})
    cds.override_node_properties("cds/key_industry/sector_3", {"mode":"output", "view":{"label": "Sector 3"}})
    cds.override_node_properties(
        'cds/key_industry/code_name', 
        {
            'options_data': "../../../non_cds/sic_dropdown", 
            'options_field': "SICCombined", 
            'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task'],
            "view": {"label":"SIC Description (Search SIC code here)", "multiline": True, "options": {"mandatory": {"style_cell": "hx-bad"}}}
        }
    )
    cds.override_node_properties('cds/key_industry/sic_description_2', {'options_data': "../../../non_cds/sic_dropdown_2", 'options_field': "SICCombined", "view": {"multiline": True}})
    cds.override_node_properties('cds/key_industry/sic_description_3', {'options_data': "../../../non_cds/sic_dropdown_3", 'options_field': "SICCombined", "view": {"multiline": True}})
    cds.override_node_properties('cds/exposure/aggregate/credit_rating', {'options_table': "ref_side_a_bankruptcy", 'options_column': "Bankruptcy Rating"})
    cds.override_node_properties('cds/exposure/aggregate/credit_rating_estimated', {"view": {"multiline": True}})
    cds.override_node_properties('cds/exposure/aggregate/credit_rating_override', {"view": {"multiline": True}})

        
    cds.override_node_properties('cds/coverage_details', {'options_data': "../../non_cds/policy_form_dropdown", 'options_field': "form", "allow_custom_value": True})

    
#### Override default values ####
    cds.override_node_properties('cds/currencies/source_currency', {'default': "USD"})
    cds.override_node_properties('hx_core/inception_date', {'default' : "2024-01-01"})
    cds.override_node_properties('hx_core/expiry_date', {'default' : "2024-12-31"}) 
    #cds.override_node_properties('hx_core/expiry_date', {'default' : "2024-12-31", "view": {"style_cell":"hx-bad"}}) TODO: show warning when inception and expiry not a year apart
    cds.override_node_properties('cds/exposure/aggregate/period', {'default' : 12, "view": {"format": {"mantissa": 0}}})

#### Override to output/override ####
    cds.override_node_properties("cds/standard_fields/benchmark_class", {"mode":"output"})
    cds.override_node_properties("cds/standard_fields/trifocus", {"mode":"output"})
    cds.override_node_properties("cds/standard_fields/is_admitted_or_surplus", {"mode":"override"})
    cds.override_node_properties("cds/standard_fields/is_free_trade_zone", {"mode":"output", "optionality":"optional"})
    # Doing this here rather than in the model variables spreadsheet as it won't add "output" the ther override, just the label
    cds.override_node_properties("cds/key_industry/code_type", {
        "mode":"output", "view": {"label": "SIC"},
    })

#### Override multiline ####
    cds.override_node_properties(f'cds/company_name',{'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task'], "view": {"multiline": True}})
    cds.override_node_properties(f'cds/key_industry/sector_uw_override_comment',{"view": {"multiline": True}})
    cds.override_node_properties(f'cds/key_industry/sector_uw_override_comment_2',{"view": {"multiline": True}})
    cds.override_node_properties(f'cds/key_industry/sector_uw_override_comment_3',{"view": {"multiline": True}})

#### Add remaining async tasks ####
    cds.override_node_properties('cds/layers/benchmark_premium',{'async_input':['rarc_task']})
    cds.override_node_properties('cds/layers/bpi',{'async_input':['rarc_task']})
    cds.override_node_properties('cds/layers/technical_premium',{'async_input':['rarc_task']})
    cds.override_node_properties('cds/layers/tpi',{'async_input':['rarc_task']})
    cds.override_node_properties('cds/layers/written_line',{"mode":"output",'async_input':['rarc_task']})

    ## Cap IQ tasks ##
    # Only need to set these for CapIQ fields when set_child_nodes_to_rarc_task_inputs is on
    cds.override_node_properties(f'cds/company_search',{'async_input':['populate_capiq_data_task','capiq_fetch_task']})
    cds.override_node_properties(f'cds/capiq_wb_id',{'async_input':['populate_capiq_data_from_wb_task']})
    cds.override_node_properties(f'cds/capiq_search',{'async_input':['populate_capiq_data_task','capiq_fetch_task']})

    capiq_fields = [
        "company_name", "sic_code", "ipo_date", "selection", "id", "date_updated", "exchange", "ticker", "hq_city", "hq_state", "incorporated_state",
        "minimum_trading_volume", "volatility_of_trading", "execs_under_age_50", "year_founded",
        "total_assets", "ebit", "current_assets", "total_liabilities", "current_liabilities", "retained_earnings", "net_sales", "market_value_of_equity", "source", "company_description"]
    for field in capiq_fields:
        cds.override_node_properties(f'cds/capiq/{field}',{'async_input':['populate_capiq_data_task','populate_capiq_data_from_wb_task']})

    cds.override_node_properties('cds/capiq_selection',{'async_input':['populate_capiq_data_task']})

    cds.override_node_properties('cds/capiq/market_cap',{'async_input':['populate_capiq_data_task','populate_capiq_data_from_wb_task'], "view": {"format": utils.thousands_format(0)}})

    # Populated rating fields
    cds_fields = ["ticker", "hq_city", "company_description"]
    for field in cds_fields:
        cds.override_node_properties(f'cds/{field}',{'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task']})

    # industry_fields = ["sector_name"]
    # for field in industry_fields:
    #     cds.override_node_properties(f'cds/key_industry/{field}',{'async_output':['populate_capiq_data_task']})
    
    exposure_fields = [
        "ipo_date","minimum_trading_volume", "volatility_of_trading", "execs_under_age_50", "source"
    ]
    for field in exposure_fields:
        cds.override_node_properties(f'cds/exposure/aggregate/{field}',{'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task']})

    exposure_fields_thousands = [
        "total_assets","ebit", "source", "net_sales", "market_value_of_equity", "total_liabilities", "current_assets", "current_liabilities", "retained_earnings"
    ]
    for field in exposure_fields_thousands:
        cds.override_node_properties(f'cds/exposure/aggregate/{field}',{'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task'], "view": {"format": utils.thousands_format(0)}})

    cds.override_node_properties("cds/exposure/aggregate/year_founded", {'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task'], "view": {"format": {"mantissa": 0}}})

    # Company description
    cds.override_node_properties(f'cds/company_description',{'async_output':[{'task':'populate_capiq_data_task', 'reset': False},{'task':'populate_capiq_data_from_wb_task', 'reset': False}],'async_input':['populate_capiq_data_task','populate_capiq_data_from_wb_task']})

    ## Rate Change tasks ##
    cds.override_node_properties('cds/key_industry/sector_id',{'async_input':['rarc_task']})
    cds.override_node_properties('cds/key_industry/sector_id_2',{'async_input':['rarc_task']})
    cds.override_node_properties('cds/key_industry/sector_id_3',{'async_input':['rarc_task']})

    # Set mandatory formatting
    cds.override_node_properties(f'cds/exposure/aggregate/market_cap',{'async_output':['populate_capiq_data_task','populate_capiq_data_from_wb_task'], "view": {"format": utils.thousands_format(0), "options": {"mandatory": {"style_cell": "hx-bad"}}}})

#### Override remaining formats ####
    ## Company Details ##
    cds.override_node_properties("cds/exposure/aggregate/insider_share", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/exposure/aggregate/revised_market_cap", {"view": {"format" : utils.thousands_format(0)}})
    cds.override_node_properties("cds/key_industry/sic_percentage", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/key_industry/sic_percentage_2", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/key_industry/sic_percentage_3", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/key_industry/sector_uw_override", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/key_industry/sector_uw_override_2", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/key_industry/sector_uw_override_3", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/key_industry/sector_unity_frequency", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/key_industry/sector_unity_frequency_2", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/key_industry/sector_unity_frequency_3", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/frequency/sca_model_freq", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/frequency/sca_freq_override", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/frequency/sca_used_freq", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/frequency/d_used_freq", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/frequency/ma_used_freq", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/frequency/total_freq", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    ## Company Financials
    cds.override_node_properties("cds/exposure/aggregate/dic_loading_factor", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/exposure/aggregate/z_score", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/exposure/aggregate/bankruptcy_score", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/exposure/aggregate/average_bankruptcy_score", {"view": {"format": {"output": "percent", "mantissa": 2}}})

    cds.override_node_properties("cds/key_industry/sector_message", {"view": {"style_cell":"hx-note"}})

def sch_private_priced(cds):

    # this creates nodes for private prcing cds/layers/coverages/abc/private_case_priced and cds/layers/coverages/side_a/private_case_priced
    cds.extend_node_rater_defined(
        "cds/layers/coverages",{"private_priced": hx.Structure(children={
                "benchmark_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Benchmark Premium", "format":  {"thousandSeparated": True, "mantissa": 0}}),
                "bpi": hx.Float(mode="output", view={"label": "BPI", "format":  {"output": "percent", "mantissa": 2}}),
                "technical_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Technical Premium", "format":  {"thousandSeparated": True, "mantissa": 0}}),
                "tpi": hx.Float(mode="output", view={"label": "TPI", "format":  {"output": "percent", "mantissa": 2}}),
            }),
        })
    

def sch_dropdowns():
    return  {
          "sic_dropdown" : hx.List(mode="output",children={
            "SICCombined" :hx.Str(mode="output", view={"label": "SIC Description"})
        }),      
        "policy_form_dropdown": hx.List(mode="output", children={
            "form": hx.Str(mode="output", view={"label": "Policy Form"})
        }),
         "sic_dropdown_2" : hx.List(mode="output",children={
            "SICCombined" :hx.Str(mode="output", view={"label": "SIC Description"})
        }),
         "sic_dropdown_3" : hx.List(mode="output",children={
            "SICCombined" :hx.Str(mode="output", view={"label": "SIC Description"})
        }),
        "broker_dropdown": hx.List(mode="output", children={
            "Broker": hx.Str(mode="output", view={"label": "Broker"})
        }),
        "us_broker_dropdown": hx.List(mode="output", children={
            "Broker": hx.Str(mode="output", view={"label": "Broker"})
        }),
            }
    


