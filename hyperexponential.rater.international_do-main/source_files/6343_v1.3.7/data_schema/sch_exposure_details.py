import hx_data_schema as hx
import data_schema.sch_utilities as utils

# Replace / remove examples with your models exposures

def sch_exposure_details(cds):   

    cds.extend_node_rater_defined("cds/key_industry", {
        "ticker": hx.Str(mode="input", default=None, optionality="optional", async_input=["populate_capiq_data_task", "rarc_task", "capiq_fetch_task"], view={"label": "Ticker", "info": "Please enter the ticker without the exchange prefix. E.g. enter TSCO, not LON:TSCO"}),
    })

    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.extend_node_rater_defined("cds/exposure/aggregate", {        
        "insider_shareholder_comment": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Insider Shareholder Comment"}),
        "ipo_comment": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "IPO Comment"}),                
        "market_cap_2_year_high": hx.Float(mode="input", default=None, validation={"min_value": 0}, optionality="optional",  async_input=["rarc_task"], view={"label": "Market Cap (2 Year High)","format": {"thousandSeparated": True, "mantissa": 0}, "options": {"input": {"label": "Market Cap (2 Year High)"}, "read_only": {"label": "Exposure", "read_only": True}}}),
        "current_market_cap": hx.Float(mode="input", default=None, validation={"min_value": 0}, optionality="optional", async_input=["rarc_task"], view={"label": "Current Market Cap","format": {"thousandSeparated": True, "mantissa": 0}}),
        "fifty_two_week_high": hx.Float(mode="input", default=None, validation={"min_value": 0}, optionality="optional", async_input=["rarc_task"], view={"label": "52 Week High","format": {"thousandSeparated": True, "mantissa": 0}}),
        "fifty_two_week_low": hx.Float(mode="input", default=None, validation={"min_value": 0}, optionality="optional", async_input=["rarc_task"], view={"label": "52 Week Low","format": {"thousandSeparated": True, "mantissa": 0}}),
        "main_exchange": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Main Exchange"}),
        "minimum_trading_volume": hx.Float(mode="output",  async_input=["rarc_task"], view={"label": "Minimum Trading Volume","format": {"thousandSeparated": True, "mantissa": 0}}),
        "volatility_trading_volume": hx.Float(mode="output",  async_input=["rarc_task"], view={"label": "Volatility Trading Volume Downturn","format": {"thousandSeparated": True, "mantissa": 0}}),
        "execs_under_fifty": hx.Float(mode="output",  async_input=["rarc_task"], view={"label": "Percentage of Executives Under 50", "format":utils.percent_format(0)}),
        "total_assets": hx.Float(mode="input",  default=None, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], view={"label": "Total Assets","format": {"thousandSeparated": True, "mantissa": 0}, "options": {"input": {"label": "Total Assets"}, "read_only": {"label": "Exposure", "read_only": True}}}),
        "ebit": hx.Float(mode="input", default=None,  optionality="optional", async_input=["rarc_task"], view={"label": "Earnings Before Interest & Taxes (EBIT)","format": {"thousandSeparated": True, "mantissa": 0}}),
        "ebitda": hx.Float(mode="input", default=None,  optionality="optional", async_input=["rarc_task"], view={"label": "Earnings Before Interest & Taxes (EBITDA)","format": {"thousandSeparated": True, "mantissa": 0}}),
        "net_sales": hx.Float(mode="input", default=None,  optionality="optional", async_input=["rarc_task"], view={"label": "Net Sales","format": {"thousandSeparated": True, "mantissa": 0}}),
        "net_profit": hx.Float(mode="input", default=None,  optionality="optional", async_input=["rarc_task"], view={"label": "Net Profit","format": {"thousandSeparated": True, "mantissa": 0}}),
        "total_liabilities": hx.Float(mode="input",  default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Total Liabilities","format": {"thousandSeparated": True, "mantissa": 0}}),
        "net_debt": hx.Float(mode="input",  default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Net Debt","format": {"thousandSeparated": True, "mantissa": 0}}),
        "operating_cashflow": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Operating Cashflow","format": {"thousandSeparated": True, "mantissa": 0}}),
        "current_assets": hx.Float(mode="input",  default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Current Assets","format": {"thousandSeparated": True, "mantissa": 0}}),
        "current_liabilities": hx.Float(mode="input",  default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Current Liabilities","format": {"thousandSeparated": True, "mantissa": 0}}),
        "equity": hx.Float(mode="input", default=None,  optionality="optional", async_input=["rarc_task"], view={"label": "Equity","format": {"thousandSeparated": True, "mantissa": 0}}),
        "retained_earnings": hx.Float(mode="input",  default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Retained Earnings","format": {"thousandSeparated": True, "mantissa": 0}}),
        "period_ended": hx.Date(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Period Ended"}),
        "period_data": hx.Float(mode="input", default=12, optionality="required", options_table="lst_period_data", options_column="Period Data", async_input=["rarc_task"], view={"label": "Period Data (Months)","format": {"mantissa": 0}}),
        "adr_level": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_adr", options_column="Platform", async_input=["rarc_task"], view={"label": "ADR Level"}),
        "sponsored": hx.Str(mode="input", default=None, optionality="optional", options=["Sponsored", "Non-sponsored"], async_input=["rarc_task"], view={"label": "Sponsored"}),
        "us_listing_share": hx.Float(mode="input", default=None, validation={"min_value": 0, "max_value": 1.0},  optionality="optional", async_input=["rarc_task"], view={"label": "US Listing % Share of Total", "format": utils.percent_format(1),"options": {"input": {"label": "US Listing % Share of Total"}, "read_only": {"label": "ADR %", "read_only": True}}}),
        "credit_score": hx.Str(mode="input", default=None, optionality="optional", options_table="lst_credit_rating", options_column="Platform", async_input=["rarc_task"], view={"label": "Credit Score"}),
        "insider_shareholder_share": hx.Float(mode="input", default=None, validation={"min_value": 0, "max_value": 1.0},  optionality="optional", async_input=["rarc_task"], view={"label": "Insider Shareholder Share", "format":utils.percent_format(1)}),
        "insider_shareholder_details": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Details of Insider Shareholder"}),
        "institutional_ownership_share": hx.Float(mode="input", default=None, validation={"min_value": 0, "max_value": 1.0},  optionality="optional", async_input=["rarc_task"], view={"label": "Institutional Ownership %", "format":utils.percent_format(1)}),
        "ipo_date": hx.Date(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "IPO Date (If Within 5 Years)"}),
        "ignore_ipo": hx.Str(mode="input", default="No", optionality="required", options_table="lst_yn", options_column="yesno", async_input=["rarc_task"], view={"label": "Ignore IPO for D&O Purposes"}),
        "exposure_currency": hx.Str(mode="input", default=None, async_input=["rarc_task", "populate_capiq_data_task"], optionality="optional", options=["USD", "EUR", "GBP", "CAD", "CHF", "AED", "AFN", "ALL", "AMD", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BTN", "BWP", "BZD",  "CDF",  "CLP", "CNY", "COP", "CRC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ETB",  "FJD",  "GEL", "GHS", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KHR", "KMF", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SCR", "SDG", "SEK", "SGD", "SHP", "SOS", "SYP", "SZL", "THB", "TND", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "UYU", "UZS", "VND", "VUV", "XAF", "XCD", "XOF", "XPF", "YER", "ZAR", "ZWD"], view={"label": "Exposure Currency", "options": {"input": {"label": "Exposure Currency"}, "read_only": {"label": "Exposure Currency", "read_only": True}}}),
        "company_search_info": hx.Str(mode="output", view={"label": "Info"}),
        "credit_score_info": hx.Str(mode="output", view={"label": "Info"}),
        "current_ratio": hx.Structure(view={"label": "Current Ratio"}, children={
            "value": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Value", "format":{"mantissa": 2}}),
            "rag_status": hx.Str(mode="output", async_input=["rarc_task"], view={"label": "RAG"})
        }),
        "accumulated_profitability": hx.Structure(view={"label": "Accumulated Profitability"}, children={
            "value": hx.Float(mode="output",  async_input=["rarc_task"], view={"label": "Value", "format":utils.percent_format(2)}),
            "rag_status": hx.Str(mode="output", async_input=["rarc_task"], view={"label": "RAG"})
        }),
        "return_on_assets": hx.Structure(view={"label": "Return on Assets"}, children={
            "value": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Value", "format":utils.percent_format(2)}),
            "rag_status": hx.Str(mode="output", async_input=["rarc_task"], view={"label": "RAG"})
        }),
        "book_value_liability_ratio": hx.Structure(view={"label": "Book Value to Liability Ratio"}, children={
            "value": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Value", "format":{"mantissa": 2}}),
            "rag_status": hx.Str(mode="output", async_input=["rarc_task"], view={"label": "RAG"})
        }),
        "asset_turnover": hx.Structure(view={"label": "Asset Turnover"}, children={
            "value": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Value", "format":{"mantissa": 2}}),
            "rag_status": hx.Str(mode="output", async_input=["rarc_task"], view={"label": "RAG"})
        }),
        "z_score": hx.Structure(view={"label": "Z Score"}, children={
            "value": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Value", "format":{"mantissa": 2}}),
            "rag_status": hx.Str(mode="output", async_input=["rarc_task"], view={"label": "RAG"})
        }),
        "roe": hx.Structure(view={"label": "ROE"}, children={
            "value": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Value", "format":utils.percent_format(2)}),
            "rag_status": hx.Str(mode="output", async_input=["rarc_task"], view={"label": "RAG"})
        }),
        "net_debt_equity_ratio": hx.Structure(view={"label": "Net Debt / Equity"}, children={
            "value": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Value", "format":utils.percent_format(2)}),
            "rag_status": hx.Str(mode="output", async_input=["rarc_task"], view={"label": "RAG"})
        }),
        "cash_conversion": hx.Structure(view={"label": "Cash Conversion"}, children={
            "value": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Value", "format":utils.percent_format(2)}),
            "rag_status": hx.Str(mode="output", async_input=["rarc_task"], view={"label": "RAG"})
        }),
        "us_ftes": hx.Float(mode="input", default=None, validation={"min_value": 0}, optionality="optional", async_input=["rarc_task"], view={"label": "US FTEs","format": {"thousandSeparated": True, "mantissa": 0}}),
        "row_ftes": hx.Float(mode="input", default=None, validation={"min_value": 0}, optionality="optional", async_input=["rarc_task"], view={"label": "Rest of World FTEs","format": {"thousandSeparated": True, "mantissa": 0}, "options": {"input": {"label": "Rest of World FTEs"}, "read_only": {"label": "Number of Employees", "read_only": True}}}),
    })

    # Override exposure/aggregate label
    cds.override_node_properties("cds/exposure/aggregate", {
        "view": {"label": ""}
        })
