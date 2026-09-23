import hx_data_schema as hx
import data_schema.sch_utilities as utils
# from data_schema.rate_risk_information import rate_risk_information

def sch_async_capiq(cds):
    cds.extend_node_rater_defined("cds", {
        # Building the CapIQ output table
        "capiq_results" : hx.Str(mode="output", async_output=["capiq_fetch_task", "populate_capiq_data_task"], view={"label": "Results"}),
        "company_search": hx.Str(mode="input", default=None, async_input=["populate_capiq_data_task", "capiq_fetch_task", "rarc_task"], optionality="optional", view={"label": "Company Search"}),
        "capiq_search_complete" : hx.Bool(mode="output",  async_output=["capiq_fetch_task", "start_renewal_task"]),
        "capiq_selection" : hx.Int(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task"], view={"label": "Selected Row Number"}),
        "capiq_populate" : hx.Str(mode="output", async_output=["populate_capiq_data_task"], view={"label": "Status"}),
        "capiq": hx.List(mode="input", async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], async_input=["populate_capiq_data_task"], children={
            "selection" : hx.Bool(mode="input", async_input=["populate_capiq_data_task"], async_output=[{"task": "populate_capiq_data_task", "reset": False}], default=False, optionality="required", view={"label": "Select One"}),
            "id" : hx.Str(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], view={"label": "Company ID"}),
            "insured_name" : hx.Str(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], view={"label": "Company"}),
            "exchange" : hx.Str(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], view={"label": "Exchange"}),
            "market_cap_2_year_high" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], view={"label": "Market Cap"}),
            "date_updated" : hx.Date(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], view={"label": "Date Updated"}),
            "sic_code" : hx.Str(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "ipo_date" : hx.Date(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], view={"label": "Date Updated"}),
            "ticker" : hx.Str(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "minimum_trading_volume" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "volatility_trading_volume" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "execs_under_fifty" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "total_assets" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "ebit" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "current_assets" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "total_liabilities" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "current_liabilities" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "retained_earnings" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "net_sales" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "current_market_cap" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "source" : hx.Str(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "company_description" : hx.Str(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "currency" : hx.Str(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], view={"label": "Currency"}),
            "period_ended" : hx.Date(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], view={"label": "Period Ended"}),
            "fifty_two_week_high" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "fifty_two_week_low" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "institutional_ownership_share" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "insider_shareholder_share" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}]),
            "equity" : hx.Float(mode="output", async_input=["populate_capiq_data_task"], async_output=[{"task": "capiq_fetch_task", "reset": False}, {"task": "populate_capiq_data_task", "reset": False}], view={"label": "Equity"}),


        }),
        "capiq_refresh_date": hx.Date(mode="output", async_output=["capiq_fetch_task", "populate_capiq_data_task"], view={"label": "Refresh Date"}),
        # TODO: make an input to the landing page async task once the connection to Workbench is built
        "capiq_wb_id" : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Company ID"})
    })

    ## Cap IQ tasks ##
    # Only need to set these for CapIQ fields when set_child_nodes_to_rarc_task_inputs is on

    capiq_fields = [
        "insured_name", "sic_code", "ipo_date", "selection", "id", "date_updated", "exchange", "ticker", "minimum_trading_volume", 
        "volatility_trading_volume", "execs_under_fifty", "total_assets", "ebit", 
        "current_assets", "total_liabilities", "current_liabilities", "retained_earnings", "net_sales", "current_market_cap", "source", "company_description", "equity", "fifty_two_week_high", "fifty_two_week_low","institutional_ownership_share", "insider_shareholder_share"]
    for field in capiq_fields:
        cds.override_node_properties(f'cds/capiq/{field}',{'async_input':['populate_capiq_data_task']})

    cds.override_node_properties('cds/capiq_selection',{'async_input':['populate_capiq_data_task']})

    cds.override_node_properties('cds/capiq/market_cap_2_year_high',{'async_input':['populate_capiq_data_task'], "view": {"format": utils.thousands_format(0)}})


    exposure_fields = [
        "ipo_date","minimum_trading_volume", "volatility_trading_volume", "execs_under_fifty", "main_exchange", "period_ended","institutional_ownership_share", "insider_shareholder_share"# "source"
    ]
    for field in exposure_fields:
        cds.override_node_properties(f'cds/exposure/aggregate/{field}',{'async_output':['populate_capiq_data_task']})

    exposure_fields_thousands = [
        "market_cap_2_year_high", "total_assets","ebit", "net_sales", "current_market_cap", "total_liabilities", "current_assets", "current_liabilities", "retained_earnings", "fifty_two_week_high", "fifty_two_week_low", "equity" #, "source"
    ]
    for field in exposure_fields_thousands:
        cds.override_node_properties(f'cds/exposure/aggregate/{field}',{'async_output':['populate_capiq_data_task'], "view": {"format": utils.thousands_format(0)}})



    # Populated rating fields
    cds.override_node_properties('cds/risk_information/company_description',{'async_output':['populate_capiq_data_task']})
    cds.override_node_properties('cds/key_industry/ticker',{'async_output':['populate_capiq_data_task']})
