
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
          <HX.Pane>
            <HX.Notes field="model_state/landing_page_info" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "inception_date",
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "underwriter",
              "benchmark_class"
            ]}
              with="cds/standard_fields"
              horizontal={true} />
            <HX.Notes field="underwriter_warning"
              shownBy="show_underwriter_warning"
              with="uw_validation" />
            <HX.Collection fields={[
              "cds/standard_fields/insured_name"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/policy_reference",
              "cds/currencies/source_currency",
              "cds/standard_fields/is_renewal"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Policy Information">
          <HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "written_line",
                "brokerage",
                "status"
              ]}
                horizontal={true} />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Policy Document">
          <HX.Button task="policy_to_excel_task"
            title="Generate Policy Document"
            shownBy="policy_doc/show_generate_button" />
          <HX.Notes field="policy_doc/premium_check"
            shownBy="policy_doc/show_premium_check" />
          <HX.File with="policy_doc"
            field="output_file"
            title="Click on the icon below to download the policy document"
            shownBy="show_download" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Policy Level Information"
        fullWidth={false}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Policy Level Rating Information">
          <HX.Notes field="messages/policy_info_note" />
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection fields={[
              "quoted_premium.read_only",
              null
            ]}
              numCols={2} />
          </HX.With>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Collection title="Policy Details"
                  fields={[
                  "limit",
                  "aggregate_limit",
                  "type",
                  {
                    "field": "deductible",
                    "shownBy": "/flags/deductible_flag"
                  },
                  {
                    "field": "excess",
                    "shownBy": "/flags/excess_flag"
                  }
                ]} />
              </HX.With>
            </HX.Pane>
            <HX.Pane>
              <HX.Collection title="Terms & Conditions"
                fields={[
                "bi_and_ee_cover",
                "seperate_bi_ee_agg_limits",
                "bi_tiv",
                "extensions_covered",
                {
                  "field": "/cds/uw_rationale/extensions_comment",
                  "shownBy": "/flags/extensions_comment_flag"
                },
                "liability_covered"
              ]}
                with="cds/rating_factors" />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection title="Preparedness Factors"
                fields={[
                "risk_preparedness",
                "security",
                "crisis_management",
                "social_media",
                "high_profile_event"
              ]}
                with="cds/rating_factors" />
              <HX.Notes field="messages/crime_website" />
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Education"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Education">
          <HX.Pane>
            <HX.Table data={[
              "cds/exposure/granular/education"
            ]}
              fields={[
              "institution_name",
              "num_schools",
              "country",
              "state_code",
              "state_name",
              "city_risk",
              "location",
              "school_grade",
              "school_type",
              "boarding_day",
              "num_students",
              "num_employees",
              "sex_of_school",
              "num_req_counselling",
              "factor_city_risk"
            ]}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Non Education"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Non Education">
          <HX.Pane>
            <HX.Table data={[
              "cds/exposure/granular/non_education"
            ]}
              fields={[
              "establishment_name",
              "sector/sector",
              "sector/sub_sector",
              "num_of_est",
              "country",
              "state_code",
              "state_name",
              "city_risk",
              "location",
              "footfall_measure",
              "num_of_staff_per_est",
              "footfall_measure_per_est",
              "east_of_access",
              "enclosed_space",
              "num_of_days",
              "num_req_counselling",
              "footfall_band",
              "factor_city_risk"
            ]}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Experience Rating"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Control">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/experience_rating/data_source"
            ]} />
            <HX.Button task="sql_bi_fetch_task"
              title="Fetch BI Data"
              shownBy="flags/er_source_bi" />
            <HX.Button task="sql_bi_clear"
              title="Clear BI Data"
              shownBy="flags/er_source_bi" />
            <HX.Collection fields={[
              "flags/show_bi_claims"
            ]}
              shownBy="flags/er_source_bi" />
            <HX.Collection fields={[
              "cds/experience_rating/experience_data"
            ]}
              shownBy="flags/er_source_user" />
            <HX.Pane shownBy="flags/er_source_user" />
            <HX.Pane shownBy="flags/er_source_user" />
            <HX.Pane shownBy="flags/er_source_user" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "messages/fetch_bi_task_status"
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Experience Rating Summary">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/experience_rating/exposure_trend"
            ]} />
            <HX.Button task="backfill_exposure"
              title="Backfill with Current Exposure" />
            <HX.Collection fields={[
              {
                "field": "final_burning_cost",
                "infoBy": "/messages/experience_rating_note"
              },
              "cat_rms_or_bp"
            ]}
              with="cds/experience_rating"
              numCols={2} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table data={[
              {
                "datum": "er_calcs",
                "elementLabelBy": "yoa_label"
              },
              {
                "datum": "curr_yr",
                "elementLabelBy": "yoa_label"
              },
              null,
              {
                "datum": "er_totals",
                "labelBy": "er_totals/yoa"
              }
            ]}
              fields={[
              {
                "field": "exp_non_ed",
                "width": 150
              },
              {
                "field": "exp_ed",
                "width": 120
              },
              {
                "field": "sel_exp_base",
                "width": 120
              },
              {
                "field": "ultimate_claims",
                "width": 100
              },
              {
                "field": "sel_infl_index",
                "width": 120
              },
              {
                "field": "inf_ultimate",
                "width": 120
              },
              {
                "field": "include",
                "width": 100
              }
            ]}
              with="cds/experience_rating"
              kb-interactive={true} />
            <CustomComponent title="Projected on-levelled ULR by YOA"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/experience_rating/er_calcs"
              }
            ]}
              traces={[
              {
                "field": "attrition_on_level_ulr",
                "label": "Attritional ULR"
              },
              {
                "field": "large_ulr",
                "label": "Large ULR"
              },
              {
                "field": "cat_ulr",
                "label": "Cat ULR"
              }
            ]}
              xAxisTickAngle={-45}
              gapBetweenBarsSize={0.1}
              xAxisLabel="YOA"
              yAxisLabel="ULR"
              barMode="stack" />
            <CustomComponent title="Percentage Change in Exposure Relative to Prior Year"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/experience_rating/er_chart_data"
              }
            ]}
              traces={[
              {
                "field": "exp_non_ed_perc",
                "label": "Non-Education"
              },
              {
                "field": "exp_ed_perc",
                "label": "Education"
              },
              {
                "field": "gnwp_perc",
                "label": "Original GNWP"
              }
            ]}
              xAxisTickAngle={-45}
              gapBetweenBarsSize={0.2}
              xAxisLabel="YOA"
              yAxisLabel="% Change" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Experience Rating Calculations"
          shownBy="flags/er_experience_data">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/experience_rating/cat_event"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table data={[
            {
              "datum": "er_calcs",
              "elementLabelBy": "yoa_label"
            },
            {
              "datum": "curr_yr",
              "elementLabelBy": "yoa_label"
            },
            null,
            {
              "datum": "er_totals",
              "labelBy": "er_totals/yoa"
            }
          ]}
            fields={[
            {
              "field": "gnwp",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "rate_change",
              "shownBy": "/flags/er_source_bi",
              "width": 120
            },
            {
              "field": "user_input_gnwp",
              "shownBy": "/flags/er_source_user",
              "width": 100
            },
            {
              "field": "user_input_rate_change",
              "shownBy": "/flags/er_source_user",
              "width": 120
            },
            {
              "field": "rate_change_index",
              "width": 120
            },
            {
              "field": "on_level_premium",
              "width": 120
            },
            {
              "field": "user_input_att_ll_total",
              "shownBy": "/flags/er_source_user",
              "width": 230
            },
            null,
            {
              "field": "attrition_incurred",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "attrition_dev_factor",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "attrition_ielr",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "attrition_ult_claims",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "attrition_on_level_ulr",
              "shownBy": "/flags/er_source_bi",
              "width": 120
            },
            null,
            {
              "field": "large_incurred",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "large_avg_lr",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "large_ll_assumption",
              "shownBy": "/flags/er_source_bi",
              "width": 120
            },
            {
              "field": "large_weighted_ll",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "large_ult_claims",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "large_ulr",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            null,
            {
              "field": "cat_incurred",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "cat_avg",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "cat_rms_or_bp",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "cat_ult_claims",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            {
              "field": "cat_ulr",
              "shownBy": "/flags/er_source_bi",
              "width": 100
            },
            null,
            {
              "field": "total_att_ll_dev_factor",
              "width": 100
            },
            {
              "field": "total_att_ll_ielr",
              "width": 100
            },
            {
              "field": "attrition_ll_ult_claims",
              "width": 100
            },
            {
              "field": "cat_bp",
              "width": 100
            },
            {
              "field": "total_ult_claims",
              "width": 100
            },
            {
              "field": "total_on_level_ulr",
              "width": 120
            }
          ]}
            with="cds/experience_rating"
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Experience Rating Frequency"
          shownBy="flags/er_experience_data_no">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/experience_rating/actual_incurred"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table data={[
            {
              "datum": "er_calcs",
              "elementLabelBy": "yoa_label"
            },
            {
              "datum": "curr_yr",
              "elementLabelBy": "yoa_label"
            },
            null,
            {
              "datum": "er_totals",
              "labelBy": "er_totals/yoa"
            }
          ]}
            fields={[
            {
              "field": "user_input_num_incidents",
              "width": 100
            },
            {
              "field": "user_input_num_deaths",
              "width": 100
            },
            {
              "field": "user_input_num_injuries",
              "width": 100
            },
            {
              "field": "user_input_incurred_total",
              "shownBy": "/flags/er_actual_incurred",
              "width": 230
            },
            {
              "field": "frequency_ult_claims",
              "width": 100
            },
            {
              "field": "frequency_infl_index",
              "width": 100
            },
            {
              "field": "frequency_inf_ultimate",
              "width": 120
            }
          ]}
            with="cds/experience_rating"
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
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
        <HX.Section title="Summary"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Notes field="messages/rating_summary_note"
                title=" " />
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Collection numCols={2}
                  fields={[
                  {
                    "field": "quoted_premium",
                    "labelBy": "/messages/epi_heading"
                  },
                  "/cds/modifiers/underwriter_adjustment",
                  "model_premium",
                  {
                    "field": "/messages/min_premium_note",
                    "shownBy": "min_premium/flag"
                  }
                ]} />
              </HX.With>
            </HX.Pane>
            <HX.Pane>
              <HX.Notes field="cds/uw_rationale/comments"
                title="Comments" />
            </HX.Pane>
          </HX.Pane>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Pricing - Expected Loss"
                fields={[
                "expected_loss/exposure_rated",
                "expected_loss/experience_rated",
                "expected_loss/experience_weight",
                "expected_loss/blended"
              ]} />
              <HX.Collection title="Technical Pricing - Targets 15% RoC"
                fields={[
                "technical_premium",
                "tpi",
                "roc"
              ]} />
              <HX.Collection title="Benchmark Pricing - Targets 70% NLR"
                fields={[
                "benchmark_premium",
                "bpi",
                "pflr"
              ]} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Alternate Scenarios"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Table data={[
            {
              "datum": "cds/layers",
              "elementLabelBy": "label"
            }
          ]}
            syncColumnWidthsKey="mySyncedTables1"
            fields={[
            "alt_limit",
            "alt_agg_limit",
            null,
            "suggested_epi",
            null,
            "model_premium"
          ]}
            transpose={true}
            filter="filter" />
        </HX.Section>
        <HX.Section title="Summary"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.Notes field="messages/policy_info_note" />
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Priced Quotes"
              numCols={2}
              fields={[
              "quoted_premium",
              "bpi_case_priced",
              "technical_premium",
              "benchmark_premium"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "tpi",
              "pflr",
              "roc"
            ]} />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}
        shownBy="cds/uw_rationale/is_rationale_required">
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/uw_rationale/knowledge_of_insured"
            title="Knowledge of the Insured" />
          <HX.Notes field="cds/uw_rationale/portfolio_fit"
            title="Portfolio Fit" />
          <HX.Notes field="cds/uw_rationale/basis_of_risk_selection"
            title="Basis of Risk Selection" />
          <HX.Notes field="cds/uw_rationale/complex_considerations"
            title="Any Unusual or Complex Considerations" />
          <HX.Notes field="cds/uw_rationale/facts_affecting_decision"
            title="Any facts which affect Underwriter's decision?" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        shownBy="model_state/show_rate_change">
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id",
              null
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button title="Calculate Rate Change"
              task="rarc_task"
              shownBy="cds/standard_fields/is_rater_priced" />
            <HX.Button title="Import Expiring Premium"
              task="case_priced_expiry_import"
              shownBy="cds/standard_fields/is_case_priced" />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rate Change">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct",
                "premium_annualized_beazley_share"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "expiring",
                  "width": 200
                }
              ]}
                with="rate_change" />
            </HX.Pane>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 135
                },
                {
                  "field": "uw_selected",
                  "width": 135
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="BI Data"
        fullWidth={true}
        viewScale={1}
        shownBy="flags/show_bi_claims">
        <HX.Section title="Policy Data">
          <HX.Pane>
            <HX.Table data={[
              "cds/experience_rating/bi_policy_data"
            ]}
              fields={[
              "PolicyReference",
              "SectionReference",
              "TriFocusName",
              "ClassOfBusinessCode",
              "StatsCode",
              "YOA",
              "SettlementCurrency",
              "ExternalAcquisitionCostMultiplier",
              "WrittenOrEstimatedPremium",
              "RateChangeDivisor",
              "BenchmarkPremium",
              "TotalWrittenIfNotSignedMultiplier"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Claim Data">
          <HX.Pane>
            <HX.Table data={[
              "cds/experience_rating/bi_claim_data"
            ]}
              fields={[
              "PolicyReference",
              "SectionReference",
              "TriFocusName",
              "YOA",
              "ClaimReference",
              "MarketCatCode",
              "BeazleyShareTotalPaidInUSD",
              "BeazleyShareTotalOutstandingInUSD",
              "BeazleyShareTotalIncurredInUSD",
              "SettlementCurrency",
              "SlipOrderTotalIncurred",
              "SignedLineMultiplier"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs">
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status_view",
              "section_reference_view",
              "brokerage_view",
              "written_line_view"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_view",
              null,
              "technical_premium",
              "benchmark_premium_view",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]}
              shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_view",
              null,
              "technical_premium",
              "benchmark_premium_view",
              "tpi",
              "bpi_case_priced_view"
            ]}
              shownBy="/cds/standard_fields/is_case_priced" />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]}
              shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]}
              shownBy="/cds/standard_fields/is_case_priced" />
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