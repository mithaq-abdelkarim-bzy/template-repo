
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
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Notes field="model_state/landing_page_info" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "inception_date",
              "expiry_date",
              "/cds/term"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "underwriter",
              "benchmark_class"
            ]}
              with="cds/standard_fields"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/insured_name",
              "cds/currencies/source_currency"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={false}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="General Details">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "project_name",
              "target_name",
              "transaction_value",
              "total_limit",
              "total_limit_percentage",
              "brokerage"
            ]}
              with="cds/policy_info" />
            <HX.Collection fields={[
              "policyholder",
              "buyer_name",
              "buyer_lawyer",
              "seller_name",
              "seller_lawyer"
            ]}
              with="cds/policy_info" />
            <HX.Collection fields={[
              "uw_expenses_flag",
              "uw_expenses",
              "distressed_business_flag"
            ]}
              with="cds/policy_info" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Frequency Selections">
          <HX.Pane>
            <HX.Table kb-interactive={true}
              transpose={true}
              data={[
              "cds/rating_factors/freq/target",
              "cds/rating_factors/freq/buyer"
            ]}
              fields={[
              "jurisdiction",
              "industry",
              "business_nature"
            ]} />
            <HX.Collection fields={[
              "default_score",
              "freq_adjustment",
              "freq_adjusted"
            ]}
              with="cds/rating_factors/freq"
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Severity Selections">
          <HX.Pane>
            <HX.Table kb-interactive={true}
              with="cds/rating_factors/sev"
              data={[
              "due_diligence",
              "disclosure",
              "general_warranties",
              "tax_warranties"
            ]}
              fields={[
              "coverage_flag",
              "severity_assessment",
              "adjustment",
              "term",
              "term_modifier",
              "comment"
            ]} />
            <HX.Collection fields={[
              "modified_score",
              "div_flag",
              "volatility",
              "multiple"
            ]}
              with="cds/rating_factors/sev"
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Fundamental Top Up Coverage">
          <HX.Collection fields={[
            "cds/policy_info/fundamental_top_up_flag"
          ]} />
          <HX.Pane>
            <HX.Table with="cds/rating_factors"
              data={[
              "fun_top_up"
            ]}
              fields={[
              "base_rate",
              "adjustment",
              "term",
              "comment"
            ]}
              shownBy="/cds/policy_info/fundamental_top_up_flag"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Coverage Options">
          <HX.Table title="Priced Quotes (Beazley Share)"
            data={[
            {
              "datum": "cds/layers",
              "width": 250
            }
          ]}
            fields={[
            "section_reference",
            {
              "field": "is_fun_top_up_coverage",
              "shownBy": "cds/policy_info/fundamental_top_up_flag"
            },
            "is_primary_excess",
            "option_name",
            "status.input",
            "written_line",
            null,
            "limit",
            "limit_pct",
            "excess",
            "excess_pct",
            "indicated",
            null,
            "quoted_premium",
            {
              "field": "model_premium",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            "technical_premium",
            {
              "field": "benchmark_premium"
            },
            "model_rol",
            "warnings",
            "expected_loss_cost",
            null,
            "tpi",
            {
              "field": "bpi",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "bpi_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            null,
            "pflr",
            "roc",
            {
              "field": "uw_adj_impact",
              "shownBy": "cds/standard_fields/is_rater_priced"
            }
          ]}
            freezeLeft={0}
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Blend Quotes">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection fields={[
                "cds/blend_option/instruction"
              ]} />
              <HX.Table title="Blend Options"
                data={[
                "cds/blend_option/option_1",
                "cds/blend_option/option_2",
                "cds/blend_option/option_3"
              ]}
                fields={[
                "option_name",
                "weight",
                "weight_excess",
                "model_rol"
              ]}
                freezeLeft={0}
                transpose={true}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane>
              <HX.Table title="Blended Quote"
                data={[
                {
                  "datum": "cds/blend_option"
                }
              ]}
                fields={[
                "option_name",
                "limit",
                "limit_pct",
                "excess",
                "excess_pct",
                "indicated",
                "date"
              ]}
                freezeLeft={0}
                transpose={true}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="ESO"
        fullWidth={false}
        shownBy="model_state/show_after_landing_page">
        <HX.With context={{
          "path": "cds/eso",
          "type": "struct"
        }}>
          <HX.Section title="">
            <HX.Collection horizontal={true}
              fields={[
              "/cds/standard_fields/underwriter.read_only",
              "/cds/currencies/source_currency.read_only"
            ]} />
            <HX.Table data={[
              {
                "datum": "coverage",
                "labelBy": "coverage/label"
              },
              {
                "datum": "include_option",
                "labelBy": "include_option/label"
              }
            ]}
              fields={[
              {
                "field": "option_0",
                "shownBy": "show_hide/option_0"
              },
              {
                "field": "option_1",
                "shownBy": "show_hide/option_1"
              },
              {
                "field": "option_2",
                "shownBy": "show_hide/option_2"
              },
              {
                "field": "option_3",
                "shownBy": "show_hide/option_3"
              },
              {
                "field": "option_4",
                "shownBy": "show_hide/option_4"
              },
              {
                "field": "option_5",
                "shownBy": "show_hide/option_5"
              },
              {
                "field": "option_6",
                "shownBy": "show_hide/option_6"
              },
              {
                "field": "option_7",
                "shownBy": "show_hide/option_7"
              },
              {
                "field": "option_8",
                "shownBy": "show_hide/option_8"
              },
              {
                "field": "option_9",
                "shownBy": "show_hide/option_9"
              }
            ]}
              with="options"
              transpose={true} />
          </HX.Section>
          <HX.Section title="">
            <HX.Pane flow="right">
              <HX.Notes field="section_references"
                title="Selected Policy References" />
              <HX.Collection horizontal={true}
                fields={[
                "bind_date"
              ]} />
            </HX.Pane>
            <HX.Table data={[
              {
                "datum": "/cds/eso",
                "labelBy": "/cds/eso/label"
              }
            ]}
              fields={[
              "premium_total",
              "limit_total",
              "term",
              "over_lining",
              "cob"
            ]}
              transpose={true}
              kb-interactive={true} />
            <CustomComponent textNode="additional_term_info"
              label="Additional Term details if needed" />
          </HX.Section>
          <HX.Section title="Amount Authorising/Further Comments">
            <HX.Pane>
              <CustomComponent textNode="authorising_comments" />
              <HX.Notes field="authorising_comments_info" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Sign Off">
            <HX.Pane>
              <HX.Collection title="Exception (Include all elements over authority)"
                horizontal={true}
                fields={[
                "approving_uw",
                "authorisation_date"
              ]} />
              <HX.Notes field="info" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Transaction Description and Summary of Target">
          <CustomComponent textNode="cds/rationale/transaction_description" />
        </HX.Section>
        <HX.Section title="Knowledge of the Insured - List of DD Reports">
          <CustomComponent textNode="cds/rationale/knowledge_of_insured" />
        </HX.Section>
        <HX.Section title="Reasons for writing the Risk">
          <CustomComponent textNode="cds/rationale/reasons_for_writing_risk" />
        </HX.Section>
        <HX.Section title="Unusual Or Complex Aspects of the Risk">
          <CustomComponent textNode="cds/rationale/complex_considerations" />
        </HX.Section>
        <HX.Section title="Exclusions and Carve Outs">
          <CustomComponent textNode="cds/rationale/exclusions_and_carve_outs" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Generate UW Doc"
        fullWidth={false}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Policy Document">
          <HX.Pane flow="right">
            <HX.Button task="generate_uw_doc"
              title="Generate Policy Document in Word"
              shownBy="policy_doc/show_generate_button" />
            <HX.Notes field="/policy_doc/premium_check"
              shownBy="/policy_doc/show_premium_check" />
            <HX.File with="/policy_doc"
              field="output_file_doc"
              title="Click on the icon below to download the policy document" />
          </HX.Pane>
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