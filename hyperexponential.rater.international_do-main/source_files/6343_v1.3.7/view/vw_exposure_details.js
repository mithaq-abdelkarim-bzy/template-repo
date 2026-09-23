import * as HX from "hx-model-components";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" viewScale={scale} >
      <HX.Section title="S&P CapIQ Search" shownBy="cds/risk_information/public_flag">
        <HX.Pane>
          <HX.Collection fields={["cds/key_industry/ticker",
            { field: "cds/company_search", infoBy: "cds/exposure/aggregate/company_search_info" }]} horizontal />
          <HX.Pane flow="right">
            <HX.Button task="capiq_fetch_task" title="Search CapIQ" />
            <HX.Collection fields={["cds/capiq_results"]} />
          </HX.Pane>
          <HX.Table shownBy="cds/capiq_search_complete"
            data={[{ datum: "cds/capiq" }]}
            fields={[
              "selection",
              "insured_name",
              "exchange",
              "market_cap_2_year_high",
              "currency",
              "date_updated"
            ]}
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane flow="right" shownBy="cds/capiq_search_complete">
          <HX.Button task="populate_capiq_data_task" title="Populate Rater" />
          <HX.Collection fields={["cds/capiq_populate"]} />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Financials">

        {/* <HX.Pane flow="right">
          <HX.Collection fields={[
            { field: "cds/key_industry/ticker", shownBy: "cds/risk_information/public_flag" },
            null,
            null,
            null,
            null,
            null
          ]} horizontal
            syncColumnWidthsKey="SyncExp" />
        </HX.Pane> */}

        <HX.Pane>
          <HX.Collection shownBy="cds/risk_information/private_flag"
            fields={["cds/exposure/aggregate/exposure_currency", null, null, null]}
            horizontal
          />
          <HX.Collection shownBy="cds/risk_information/public_flag"
            fields={["cds/currencies/source_currency.read_only", null, null, null]}
            horizontal
          />

          <HX.Table
            data={[{ datum: "cds/exposure/aggregate", minWidth: 175, maxWidth: 250 }]}
            fields={[{ field: "market_cap_2_year_high", shownBy: "cds/risk_information/public_flag" },
            { field: "current_market_cap", shownBy: "cds/risk_information/public_flag" },
            { field: "fifty_two_week_high", shownBy: "cds/risk_information/public_flag" },
            { field: "fifty_two_week_low", shownBy: "cds/risk_information/public_flag" },
            { field: "main_exchange", shownBy: "cds/risk_information/public_flag" },
              // JC and UW decided to hide until further notice 04/25
              //{ field: "minimum_trading_volume", shownBy: "cds/risk_information/public_flag" },
              //{ field: "volatility_trading_volume", shownBy: "cds/risk_information/public_flag" },
              //{ field: "execs_under_fifty", shownBy: "cds/risk_information/public_flag" },
              "total_assets",
              null,
              "ebit",
              "ebitda",
              "net_sales",
              "net_profit",
              "total_liabilities",
              "net_debt",
              "operating_cashflow",
              "current_assets",
              "current_liabilities",
              "equity",
              // { field: "equity", shownBy: "cds/risk_information/public_flag" },
              "retained_earnings",
              null,
            { field: "period_ended", shownBy: "cds/risk_information/public_flag" },
              "period_data"]}
            transpose
            syncColumnWidthsKey="SyncExp"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="USA Exposure Details" shownBy="cds/risk_information/public_us_flag">
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/exposure/aggregate", minWidth: 175, maxWidth: 250 }]}
            fields={[{ field: "adr_level", shownBy: "cds/risk_information/public_us_flag" },
            { field: "sponsored", shownBy: "cds/risk_information/adr_level_one_flag" },
            { field: "us_listing_share", shownBy: "cds/risk_information/public_us_flag" }
            ]}
            transpose
            syncColumnWidthsKey="SyncExp"
            kb-interactive
          />
        </HX.Pane>
        <HX.Collection shownBy="cds/level_1_us_exp_flag"
          fields={["cds/level_1_us_exp_msg", null, null]}
          horizontal
        />
      </HX.Section>

      <HX.Section title="Additional Information" shownBy="cds/risk_information/public_flag" >
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/exposure/aggregate", minWidth: 175, maxWidth: 250 }]}
            fields={[{ field: "credit_score", infoBy: "cds/exposure/aggregate/credit_score_info" },
              "insider_shareholder_share",
              "insider_shareholder_details",
              "institutional_ownership_share",
              "ipo_date",
              "ignore_ipo"
            ]}
            transpose
            syncColumnWidthsKey="SyncExp"
            kb-interactive
          />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Collection fields={["insider_shareholder_comment", null, "ipo_comment", null,]}
            with="cds/exposure/aggregate"
            numCols={2}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Financial Metrics">
        <HX.Pane>
          <HX.Table
            //data={[{ datum: "cds/exposure/aggregate", minWidth: 175, maxWidth: 250 }]}
            data={[
              "current_ratio",
              "accumulated_profitability",
              "return_on_assets",
              "book_value_liability_ratio",
              "asset_turnover",
              "z_score",
              "roe",
              "net_debt_equity_ratio",
              "cash_conversion"
            ]
            }

            fields={[
              { field: "value", width: 100 },
              { field: "rag_status", width: 100 }
            ]}
            //transpose
            with="cds/exposure/aggregate"
            syncColumnWidthsKey="SyncExp"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="EPL Inputs" shownBy="cds/risk_information/mmp_flag">
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/exposure/aggregate", minWidth: 175, maxWidth: 250 }]}
            fields={["us_ftes",
              "row_ftes"]}
            transpose
            syncColumnWidthsKey="SyncExp"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>


    </HX.Page >
  )
}

export { vw_exposure_details };