
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page title="Landing Page"
        shownBy="model_state/show_landing_page">
        <HX.Section title="Start Policy">
          <HX.Pane flow="right">
            <HX.Button task="start_renewal_task"
              title="Press on 'Import Expiring Policy Data' at the top right corner then click here" />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_after_landing_page">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Account Details">
            <HX.Pane>
              <HX.Pane ratio={1}>
                <HX.Collection fields={[
                  "/hx_core/inception_date",
                  "/hx_core/expiry_date"
                ]}
                  horizontal={true} />
              </HX.Pane>
              <HX.Pane>
                <HX.Collection fields={[
                  "/cds/standard_fields/underwriter",
                  "status"
                ]}
                  horizontal={true} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection fields={[
                  "/cds/standard_fields/insured_name",
                  "/cds/standard_fields/policy_reference"
                ]}
                  horizontal={true} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={[
                "/cds/standard_fields/is_admitted_or_surplus",
                "is_primary_excess",
                "brokerage"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "/hx_core/premium_currency",
                "/cds/standard_fields/is_renewal",
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Broker Details">
            <HX.Collection fields={[
              "/cds/standard_fields/broker",
              "/cds/broker_contact"
            ]}
              horizontal={true} />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="General Inputs">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/standard_fields/insured_state_or_province",
              "cds/rating_factors/claim_basis",
              null
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "code",
              "industry_group",
              "industry"
            ]}
              horizontal={true}
              with="/cds/key_industry" />
            <HX.Collection fields={[
              null,
              "entity_type",
              "excess_factor"
            ]}
              horizontal={true}
              with="/cds" />
            <HX.Collection fields={[
              "revenue",
              "assets",
              "employees",
              "locations"
            ]}
              with="/cds/exposure/aggregate"
              horizontal={true}
              title="Company Information" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Program Schedule">
          <HX.Pane>
            <HX.Table kb-interactive={true}
              fields={[
              "limit",
              "excess",
              "lead_underwriter",
              "participating_cosurety",
              "premium",
              "lead_percentage",
              "rate_per_m",
              "percent_underlying_rate"
            ]}
              data={[
              {
                "datum": "cds/retention"
              },
              {
                "datum": "cds/layers",
                "elementLabelBy": "layer_label"
              }
            ]}
              freezeLeft={1} />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection title="Selected Layer"
              fields={[
              "beazley_layer",
              "beazley_share",
              "is_follow"
            ]}
              with="cds"
              horizontal={true} />
            <HX.Collection fields={[
              "total_layer_limit",
              "beazley_limit",
              "beazley_pre_layer"
            ]}
              with="cds"
              horizontal={true} />
            <HX.Collection fields={[
              "underlying_layer_limit",
              "underlying_premium",
              "underlying_rate_per_m"
            ]}
              with="cds"
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Term Adjustment">
          <HX.Pane>
            <HX.Collection fields={[
              {
                "field": "cds/underlying_inception_date",
                "infoBy": "info_date"
              },
              {
                "field": "cds/underlying_expiry_date",
                "infoBy": "info_date"
              },
              "cds/term_adjustment_underlying"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Excess Social Engineering">
          <HX.Pane>
            <HX.Collection fields={[
              "social_engineering_sublimit",
              "social_engineering_limit",
              "social_engineering_allocation"
            ]}
              with="cds"
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        shownBy="/show_rate_change">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Rate Change">
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_policy_option_id"
              ]}
                horizontal={true} />
              <HX.Button task="expiring_policy_fetch_task"
                title="Fetch Expiring Data" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_insured_name"
              ]} />
              <HX.Pane />
            </HX.Pane>
            <HX.Table kb-interactive={true}
              data={[
              "exposure_change",
              "risk_characteristics_change",
              "deductible_change",
              "limit_change",
              "terms_conditions_change",
              "brokerage_change",
              "other_change"
            ]}
              fields={[
              "uw_selected",
              "comments"
            ]}
              title="Impact Split"
              with="rate_change" />
            <HX.Pane>
              <HX.Collection with="rate_change"
                fields={[
                "expiring_premium",
                "expiring_beazley_share",
                "rate_change/uw_selected"
              ]}
                horizontal={true} />
              <HX.Collection with="rate_change"
                fields={[
                "expiring_policy_term",
                "expiring_limit",
                "expiring_brokerage"
              ]}
                horizontal={true} />
              <HX.Collection with="rate_change"
                fields={[
                "expiring_policy_reference",
                "expiring_excess",
                null
              ]}
                horizontal={true} />
              <HX.Collection title="Company Information"
                with="rate_change"
                fields={[
                "expiring_revenue",
                "expiring_assets",
                "expiring_employees",
                "expiring_locations"
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section shownBy="/cds/standard_fields/is_rater_priced">
          <HX.Section title="Individual Risk Rating">
            <HX.Table kb-interactive={true}
              data={[
              "classification_peculiarities",
              "management",
              "personnel",
              "location",
              "response_to_losses",
              "endorsements",
              "expense_modification",
              null,
              {
                "datum": "total_modifiers"
              }
            ]}
              fields={[
              {
                "field": "minimum_state",
                "width": 200
              },
              {
                "field": "maximum_state",
                "width": 200
              },
              {
                "field": "selected",
                "width": 200
              },
              {
                "field": "comment"
              }
            ]}
              filter="available"
              with="cds" />
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "mod_factor",
                "eligibility_min_before",
                "eligibility_min_after"
              ]}
                with="cds"
                horizontal={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Expense Modification"
            shownBy="cds/expense_mod_flag">
            <HX.Table kb-interactive={true}
              data={[
              "expense_modification"
            ]}
              fields={[
              {
                "field": "minimum_state",
                "width": 200
              },
              {
                "field": "maximum_state",
                "width": 200
              },
              {
                "field": "selected",
                "width": 200
              },
              {
                "field": "comment"
              }
            ]}
              with="cds" />
          </HX.Section>
          <HX.Section title="Rating Summary">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Pane>
                <HX.Collection fields={[
                  "/cds/standard_fields/is_admitted_or_surplus",
                  {
                    "field": "/cds/surplus_deviation_factor",
                    "shownBy": "/cds/is_surplus"
                  },
                  "brokerage"
                ]}
                  horizontal={true}
                  syncColumnWidthsKey="Summary" />
                <HX.Pane flow="right">
                  <HX.Collection title="Premium"
                    fields={[
                    "final_premium",
                    "final_premium_annual",
                    "status"
                  ]}
                    horizontal={true}
                    syncColumnWidthsKey="Summary" />
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection title="Benchmark Pricing"
                  fields={[
                  "benchmark_premium",
                  "bpi"
                ]} />
                <HX.Collection title="Technical Pricing"
                  fields={[
                  "technical_premium",
                  "tpi"
                ]} />
                <HX.Collection title="Other Metrics"
                  fields={[
                  "/hx_core/ulr",
                  "/cds/term_adjustment",
                  {
                    "field": "rate_change/rate_change/uw_selected",
                    "shownBy": "/cds/standard_fields/is_renewal"
                  }
                ]} />
              </HX.Pane>
            </HX.With>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Technical Summary"
          shownBy="/cds/standard_fields/is_case_priced">
          <HX.Table title="Priced Quote"
            data={[
            {
              "datum": "cds/options",
              "width": 250
            }
          ]}
            fields={[
            "status",
            "section_reference",
            "brokerage",
            "written_line",
            null,
            "quoted_premium",
            "technical_premium",
            "benchmark_premium",
            null,
            "tpi",
            "bpi",
            null,
            "pflr",
            "roc"
          ]}
            freezeLeft={0}
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="General Comments">
          <HX.Notes field="cds/general_comments" />
        </HX.Section>
        <HX.Section title="Underwriting Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs"
        shownBy="cds/standard_fields/is_rater_priced">
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status_view",
              "/cds/standard_fields/policy_reference.read_only",
              "brokerage.read_only",
              "written_line_view"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs"
        shownBy="cds/standard_fields/is_case_priced">
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_option_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status_view",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium.read_only",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi.read_only"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Something is Broken">
        <HX.With context={{
          "path": "bug_report",
          "type": "struct"
        }}>
          <HX.Section title="Log a New Incident">
            <HX.Notes field="helper_text" />
            <HX.Pane>
              <HX.Button task="new_bug_report_task"
                title="Log a New Incident" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Incident Details"
            shownBy="commenced_flag">
            <HX.Pane>
              <HX.Collection fields={[
                "summary"
              ]}
                title="Summary" />
              <HX.Notes field="email_body"
                title="Details" />
              <HX.Pane flow="right"
                ratio={2}>
                <HX.Pane shownBy="inputs_outputs_file_show">
                  <HX.File field="inputs_outputs_file"
                    title="Inputs/Outputs Attachment" />
                  <HX.Button task="generate_bug_report_task"
                    title="Generate Inputs/Outputs" />
                </HX.Pane>
                <HX.With context={{
                  "path": "screenshot_files",
                  "type": "struct"
                }}>
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f1/show_text" />
                  <HX.File field="f1/file"
                    title="Screenshot Attachment"
                    shownBy="f1/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f2/show_text" />
                  <HX.File field="f2/file"
                    title="Screenshot Attachment 2"
                    shownBy="f2/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f3/show_text" />
                  <HX.File field="f3/file"
                    title="Screenshot Attachment 3"
                    shownBy="f3/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f4/show_text" />
                  <HX.File field="f4/file"
                    title="Screenshot Attachment 4"
                    shownBy="f4/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f5/show_text" />
                  <HX.File field="f5/file"
                    title="Screenshot Attachment 5"
                    shownBy="f5/show_file" />
                </HX.With>
              </HX.Pane>
              <HX.Button task="add_additional_file_task"
                title="Upload Additional Screenshots" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="send_bug_report_task"
                title="Send Incident" />
              <HX.Button task="cancel_bug_report_task"
                title="Cancel Incident" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};