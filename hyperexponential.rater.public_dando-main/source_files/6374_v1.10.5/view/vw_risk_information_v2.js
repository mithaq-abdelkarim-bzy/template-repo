import * as HX from "hx-model-components";
import ExpandableEditableText from "components/text_box_expandable";
import EditableText from "components/text_box_editable";
import ModalNotesEditor from "components/modal_notes_editor";

function vw_risk_information_v2(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">
      <HX.Section title="Account Details">
        <HX.Pane >
          {/* NOTE  uncomment if rater requires databse_id to be displayed */}
          {/* <HX.Collection fields={["database_id"]} with="cds" horizontal /> */}
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["underwriter", "benchmark_class"]} with="cds/standard_fields" horizontal />
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          <HX.Collection fields={["cds/standard_fields/policy_reference", "cds/currencies/source_currency", "cds/standard_fields/is_renewal", "cds/is_runoff"]} horizontal />
          {/* <HX.Pane flow="right">
            <HX.Button task="generate_tags_quickquote_add" title="Set as Quick Quote" />
            <HX.Button task="generate_tags_cuap" title="Save Coverage, UW and attachment" />
          </HX.Pane> */}
          {/* <HX.Collection fields={["cds/policy_tag_error"]} shownBy="cds/is_policy_tag_error" horizontal /> */}
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
        <HX.Collection fields={["cds/rw_broker", null]} horizontal />
      </HX.Section>
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/rating_methodology"]} />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Coverage">
        <HX.Collection fields={["cds/coverage", "cds/coverage_details"]} horizontal />
      </HX.Section>
      <HX.Section title="S&P CapIQ Search" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Pane>
          <HX.Collection fields={["cds/company_search", "cds/capiq_search", null]} numCols={3} />
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
            { field: "ticker", shownBy: "/cds/review_type/rater_priced" },
            "company_country",
            "company_state",
            "exposure/aggregate/total_assets",
            "exposure/aggregate/year_founded",
          ]}
            with="cds" />
          <HX.Pane flow="down">
            <HX.Collection fields={[
              "incorporated_state",
              "hq_state",
              "hq_city",
              "airport_city",
              "pipeline_premium",
              "exposure/aggregate/crypto_classification",
            ]}
              with="cds" />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow='down'>
          <EditableText
            textNode="cds/company_description"
            placeholderText="Enter company description here ..."
          />
        </HX.Pane>
        {/* <HX.Notes
          title="Company Description"
          field="cds/company_description"
        /> */}
      </HX.Section>
      <HX.Section title="Market Cap & IPO" shownBy="/cds/review_type/rater_priced" >
        <HX.Pane flow='right'>
          <HX.Pane flow="down">
            <HX.Collection fields={[
              { field: "exposure/aggregate/market_cap", infoBy: "exposure/aggregate/market_cap_info", shownBy: "market_cap_complete" }, { field: "exposure/aggregate/market_cap.mandatory", shownBy: "market_cap_mandatory" },
              { field: "exposure/aggregate/insider_share", infoBy: "exposure/aggregate/insider_share_info" },
              "exposure/aggregate/revised_market_cap"
            ]}
              with="cds" />
            <ModalNotesEditor
              notesPath="cds/exposure/aggregate/revised_market_cap_comment"
              label="Market Cap Comment"
              printButton={true}
              autosave={true}
            />
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Collection fields={[
              "exposure/aggregate/transaction_type",
              "exposure/aggregate/ipo_date",
              "exposure/aggregate/ignore_ipo",
            ]}
              with="cds" />
            <ModalNotesEditor
              notesPath="cds/exposure/aggregate/ipo_date_comment"
              label="IPO Comment"
              marginTop="75px"
              printButton={true}
              autosave={true}
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Sector">
        <HX.Pane flow="right">
          <HX.Pane flow='down'>
            <HX.Collection fields={[

              { field: "key_industry/code_name", shownBy: "key_industry/sic_complete" }, { field: "key_industry/code_name.mandatory", shownBy: "key_industry/sic_mandatory" },
              { field: "key_industry/sector_name", shownBy: "sector_complete" }, { field: "key_industry/sector_name.mandatory", shownBy: "sector_mandatory" },
              "key_industry/code"
            ]}
              with="cds" />
            <HX.Collection fields={[
              "key_industry/blended_sic"
            ]}
              with="cds" />
          </HX.Pane>
          <HX.Pane flow='down'>
            <HX.Collection fields={[
              "key_industry/sic_percentage",
              "key_industry/sector_unity_frequency",
              "key_industry/sector_uw_override"
            ]}
              with="cds" />
            <ModalNotesEditor
              notesPath="cds/key_industry/sector_uw_override_comment"
              label="Underwriter Override Comment"
              marginTop="30px"
              autosave={true}
            />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="down">
          <HX.Notes
            title="Sector Message"
            field="cds/key_industry/sector_message"
          />
        </HX.Pane>
        <HX.Pane flow='right'>
          <HX.Pane flow='down' shownBy="cds/key_industry/blended_sic">
            <HX.Collection fields={[
              "sic_description_2",
              { field: "sector_2", infoBy: "sector_message_2" },
              "sic_code_2",
              "sic_percentage_2",
              "sector_unity_frequency_2",
              "sector_uw_override_2",
            ]}
              with="cds/key_industry" />
            <ModalNotesEditor
              notesPath="cds/key_industry/sector_uw_override_comment_2"
              label="Underwriter Override Comment 2"
              marginTop="30px"
            />
          </HX.Pane>
          <HX.Pane flow='down' shownBy="cds/key_industry/blended_sic">
            <HX.Collection fields={[

              "sic_description_3",
              { field: "sector_3", infoBy: "sector_message_3" },
              "sic_code_3",
              "sic_percentage_3",
              "sector_unity_frequency_3",
              "sector_uw_override_3",
            ]}
              with="cds/key_industry" />
            <ModalNotesEditor
              notesPath="cds/key_industry/sector_uw_override_comment_3"
              label="Underwriter Override Comment 3"
              marginTop="30px"
            />
          </HX.Pane>
        </HX.Pane>

      </HX.Section>
      <HX.Section title="Admitted Info" shownBy="cds/admitted/conditions_met">
        <HX.Collection fields={["cds/standard_fields/is_admitted_or_surplus", null]} numCols={2} />
        <HX.Collection fields={["cds/admitted/insurer", "cds/admitted_excess/is_primary_excess"]} numCols={2} />
        {/* <HX.Collection fields={["cds/trifocus_us_surplus", null]} numCols={2} shownBy="cds/admitted/is_not_admitted" /> Excluding as trifocus should be done in workbench and want to avoid the UWs double keying*/}
      </HX.Section>
      <HX.Section title="Credit Rating" shownBy="cds/is_side_a">
        <HX.Collection fields={["credit_rating", "credit_rating_estimated", "credit_rating_override"]} numCols={3}
          with="cds/exposure/aggregate"
        />
      </HX.Section>
      <HX.Section title="Company Financials" shownBy="/cds/review_type/rater_priced">
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
      <HX.Section title="Company Financials" shownBy="/cds/review_type/private_priced">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "total_assets_output",
            "current_assets",
            "total_liabilities",
            "current_liabilities",
            "private_company_financials/long_term_debt",
            "private_company_financials/equity",
            "retained_earnings"
          ]}
            with="cds/exposure/aggregate" />
          <HX.Collection fields={[
            "private_company_financials/revenue",
            "private_company_financials/cash",
            "private_company_financials/net_income",
            "private_company_financials/free_cash_flow",
            "private_company_financials/latest_post_money_val",
            "private_company_financials/date_of_latest_post_money_val"
          ]}
            with="cds/exposure/aggregate" />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information_v2 };


