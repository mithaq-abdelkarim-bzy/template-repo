import * as HX from "hx-model-components";

function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">
      <HX.Section title="Account Details">
        <HX.Pane >
          {/* NOTE  uncomment if rater requires databse_id to be displayed */}
          {/* <HX.Collection fields={["database_id"]} with="cds" horizontal /> */}
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["underwriter", "benchmark_class"]} with="cds/standard_fields" horizontal />
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          <HX.Collection fields={["cds/standard_fields/policy_reference", "cds/currencies/source_currency", "cds/standard_fields/is_renewal"]} horizontal />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section>
      <HX.Section title="S&P CapIQ Search">
        <HX.Pane>
          <HX.Collection fields={["cds/company_search", null, null]} numCols={3} />
          <HX.Button task="capiq_fetch_task" title="Search CapIQ" />
          <HX.Table
            data={[{ datum: "cds/capiq" }]}
            fields={[
              "selection",
              "company_name",
              "exchange",
              "market_cap",
              "date_updated"
            ]}
            kb-interactive
          />
          <HX.Collection
            fields={["cds/capiq_results"]}
          />
        </HX.Pane>
        <HX.Pane shownBy="cds/capiq_search_complete">
          <HX.Button task="populate_capiq_data_task" title="Populate Rater" />
          <HX.Collection
            fields={["cds/capiq_populate"]}
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Company Details">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "company_name",
            "ticker",
            { field: "exposure/aggregate/market_cap", infoBy: "exposure/aggregate/market_cap_info", shownBy: "market_cap_complete" }, { field: "exposure/aggregate/market_cap.mandatory", shownBy: "market_cap_mandatory" },
            { field: "exposure/aggregate/insider_share", infoBy: "exposure/aggregate/insider_share_info" },
            "exposure/aggregate/revised_market_cap",
            "exposure/aggregate/show_mcap_comment",
            "exposure/aggregate/total_assets",
            "exposure/aggregate/ipo_date",
            "exposure/aggregate/ignore_ipo",
            "exposure/aggregate/show_ipo_comment"
          ]}
            with="cds" />
          <HX.Collection fields={[
            "coverage",
            "company_country",
            "company_state",
            "incorporated_state",
            "hq_state",
            "hq_city",
            "airport_city",
            "pipeline_premium",
            "exposure/aggregate/year_founded"
          ]}
            with="cds" />
          <HX.Collection fields={[
            { field: "key_industry/sector_name", shownBy: "sector_complete" }, { field: "key_industry/sector_name.mandatory", shownBy: "sector_mandatory" },
            { field: "key_industry/code_name", shownBy: "key_industry/sic_complete" }, { field: "key_industry/code_name.mandatory", shownBy: "key_industry/sic_mandatory" },
            "key_industry/code",
            "key_industry/sic_percentage",
            "key_industry/sector_unity_frequency",
            "key_industry/sector_uw_override",
            "key_industry/sector_uw_override_comment",
            "key_industry/show_override_comment",
            "key_industry/blended_sic"
          ]}
            with="cds" />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes
            title="Market Cap Comment"
            field="cds/exposure/aggregate/revised_market_cap_comment"
            shownBy="cds/exposure/aggregate/show_mcap_comment"
          />
          <HX.Notes
            title="IPO Comment"
            field="cds/exposure/aggregate/ipo_date_comment"
            shownBy="cds/exposure/aggregate/show_ipo_comment"
          />
          <HX.Notes
            title="Underwriter Override Comment"
            field="cds/key_industry/sector_uw_override_comment"
            shownBy="cds/key_industry/show_override_comment"
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes
            title="Sector Message"
            field="cds/key_industry/sector_message"
          />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={[
            { field: "sector_2", infoBy: "sector_message_2" },
            "sic_description_2",
            "sic_code_2",
            "sic_percentage_2",
            "sector_unity_frequency_2",
            "sector_uw_override_2",
            "sector_uw_override_comment_2",
            "show_override_comment_2"
          ]}
            with="cds/key_industry"
            shownBy="blended_sic" />
          <HX.Collection fields={[
            { field: "sector_3", infoBy: "sector_message_3" },
            "sic_description_3",
            "sic_code_3",
            "sic_percentage_3",
            "sector_unity_frequency_3",
            "sector_uw_override_3",
            "sector_uw_override_comment_3",
            "show_override_comment_3"
          ]}
            with="cds/key_industry"
            shownBy="blended_sic" />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes
            title="Underwriter Override Comment 2"
            field="sector_uw_override_comment_2"
            shownBy="show_override_comment_2"
            with="cds/key_industry"
          />
          <HX.Notes
            title="Underwriter Override Comment 3"
            field="sector_uw_override_comment_3"
            shownBy="show_override_comment_3"
            with="cds/key_industry"
          />
        </HX.Pane>
        <HX.Notes
          title="Company Description"
          field="cds/company_description"
        />
      </HX.Section>
      <HX.Section title="Admitted Info" shownBy="cds/admitted/conditions_met">
        <HX.Collection fields={["cds/standard_fields/is_admitted_or_surplus", null]} numCols={2} />
        <HX.Collection fields={["cds/admitted/insurer", "cds/admitted_excess/is_primary_excess"]} numCols={2} shownBy="cds/admitted/is_admitted" />
        {/* <HX.Collection fields={["cds/trifocus_us_surplus", null]} numCols={2} shownBy="cds/admitted/is_not_admitted" /> Excluding as trifocus should be done in workbench and want to avoid the UWs double keying*/}
      </HX.Section>
      <HX.Section title="Credit Rating" shownBy="cds/is_side_a">
        <HX.Collection fields={["credit_rating", "credit_rating_estimated", "credit_rating_override"]} numCols={3}
          with="cds/exposure/aggregate"
        />
      </HX.Section>
      <HX.Section title="Company Financials">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "ebit",
            "total_assets_output",
            "net_sales",
            "market_value_of_equity",
            "total_liabilities",
            "current_assets",
            "current_liabilities",
            "retained_earnings"
          ]}
            with="cds/exposure/aggregate" />
          <HX.Collection fields={[
            "period",
            "source",
            null,
            null,
            null,
            "z_score",
            "bankruptcy_score",
            "average_bankruptcy_score"
          ]}
            with="cds/exposure/aggregate" />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };


