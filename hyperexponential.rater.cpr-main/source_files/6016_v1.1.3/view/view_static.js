
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
            <HX.Pane ratio={2}>
              <HX.Notes field="model_state/landing_page_info" />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
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
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/underwriter",
              "cds/product"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/insured_name"
            ]}
              horizontal={true} />
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "section_reference",
                "/cds/currencies/source_currency",
                "/cds/standard_fields/is_renewal"
              ]}
                horizontal={true} />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Load Policy Data from Beazley Intelligence"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Collection fields={[
              "last_run_status",
              "check_run_consistent",
              "calc_run_value"
            ]}
              with="cds/bi"
              title="Enter Policy Section Reference then press button here to load latest Beazley Intelligence information." />
            <HX.Button title="Load from BI"
              task="task_sql_bi_data"
              stretch={true} />
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
                "limit",
                "excess"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "brokerage",
                "status",
                null
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
        <HX.Section title="Credit Risk & Contract Frustration - additional fields"
          shownBy="/cds/show_hide/node/show_crcf">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection fields={[
                "crcf_obligor",
                "crcf_country",
                "crcf_industry_group",
                "crcf_industry"
              ]}
                with="cds/risk_info" />
            </HX.Pane>
            <HX.Pane flow="down"
              stretch={true}>
              <HX.Collection fields={[
                "last_run_status",
                "check_run_consistent",
                "calc_run_value"
              ]}
                with="cds/ihs"
                title="Select country then press button here to load latest IHS information." />
              <HX.Button title="Load IHS Data"
                task="task_api_ihs_data"
                stretch={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={false}
        viewScale={1}
        shownBy="cds/show_hide/page/show_exposure_detail">
        <HX.Section title="Exposure Details - CRCF"
          shownBy="/cds/show_hide/node/show_crcf">
          <HX.Pane flow="right"
            reflow={true}>
            <HX.Collection title="Cover Details"
              fields={[
              "sum_insured",
              "indemnity",
              "waiting_period",
              null,
              null
            ]}
              horizontal={true}
              with="cds/exposure/granular/crcf"
              syncColumnWidthsKey="exposure_details_crcf" />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={true}>
            <HX.Collection title="Pre Shipment Risk"
              fields={[
              "pre_shipment_risk"
            ]}
              with="cds/exposure/granular/crcf"
              shownBy="/cds/show_hide/node/show_pre_shipment_risk_not"
              horizontal={true}
              syncColumnWidthsKey="exposure_details_crcf" />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={true}>
            <HX.Collection title="Pre Shipment Risk"
              fields={[
              "pre_shipment_risk",
              "pre_shipment_amt",
              "pst_shipment_amt"
            ]}
              with="cds/exposure/granular/crcf"
              shownBy="/cds/show_hide/node/show_pre_shipment_risk"
              horizontal={true}
              syncColumnWidthsKey="exposure_details_crcf" />
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Pane flow="right"
              reflow={true}>
              <HX.Collection title="Amount at Risk"
                fields={[
                "load_amt_basis"
              ]}
                with="cds/exposure/granular/crcf"
                shownBy="/cds/show_hide/node/show_hide_flat_not"
                horizontal={true}
                syncColumnWidthsKey="exposure_details_crcf" />
              <HX.Collection title="Amount at Risk"
                fields={[
                "load_amt_basis",
                "load_amt_flat"
              ]}
                with="cds/exposure/granular/crcf"
                shownBy="/cds/show_hide/node/show_hide_flat"
                horizontal={true}
                syncColumnWidthsKey="exposure_details_crcf" />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={true}>
              <HX.Collection fields={[
                "load_amt_step_opening_si",
                "load_amt_step_grace_period",
                "load_amt_step_instal_freq"
              ]}
                with="cds/exposure/granular/crcf"
                shownBy="/cds/show_hide/node/show_hide_step"
                horizontal={true}
                syncColumnWidthsKey="exposure_details_crcf" />
              <HX.Collection fields={[
                "load_amt_step_instal_amt",
                "load_amt_step_term"
              ]}
                with="cds/exposure/granular/crcf"
                shownBy="/cds/show_hide/node/show_hide_step"
                horizontal={true}
                syncColumnWidthsKey="exposure_details_crcf" />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={true}>
              <HX.Button title="Populate Automatic Exposure Profile"
                task="task_fill_exposure_profile" />
              <HX.Collection fields={[
                "last_run_status"
              ]}
                with="cds/exposure/granular/crcf"
                horizontal={true} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table title="Exposure Profile"
              data={[
              {
                "datum": "exposure_profile",
                "elementLabelBy": "year_label"
              }
            ]}
              fields={[
              {
                "field": "month_1",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_1",
                "maxWidth": 140
              },
              {
                "field": "month_2",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_2",
                "maxWidth": 140
              },
              {
                "field": "month_3",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_3",
                "maxWidth": 140
              },
              {
                "field": "month_4",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_4",
                "maxWidth": 140
              },
              {
                "field": "month_5",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_5",
                "maxWidth": 140
              },
              {
                "field": "month_6",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_6",
                "maxWidth": 140
              },
              {
                "field": "month_7",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_7",
                "maxWidth": 140
              },
              {
                "field": "month_8",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_8",
                "maxWidth": 140
              },
              {
                "field": "month_9",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_9",
                "maxWidth": 140
              },
              {
                "field": "month_10",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_10",
                "maxWidth": 140
              },
              {
                "field": "month_11",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_11",
                "maxWidth": 140
              },
              {
                "field": "month_12",
                "labelBy": "/cds/exposure/granular/crcf/exposure_profile_label_months/month_12",
                "maxWidth": 140
              }
            ]}
              with="cds/exposure/granular/crcf"
              filter="year_show_hide"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Credit Rating - CRCF"
          shownBy="/cds/show_hide/node/show_crcf">
          <HX.Pane flow="down">
            <HX.Table data={[
              {
                "datum": "crcf",
                "maxWidth": 350
              }
            ]}
              fields={[
              {
                "field": "rating_source",
                "shownBy": "/cds/show_hide/node/show_cr_only"
              },
              {
                "field": "rating_corporate",
                "shownBy": "/cds/show_hide/node/show_cr_only"
              },
              "rating_country",
              "economic_outlook"
            ]}
              with="cds/modifiers"
              transpose={true}
              title="Rating & Outlook" />
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Table data={[
              null,
              {
                "datum": "default",
                "maxWidth": 140
              },
              null,
              {
                "datum": "override_min",
                "maxWidth": 140
              },
              {
                "datum": "override",
                "maxWidth": 140
              },
              {
                "datum": "override_max",
                "maxWidth": 140
              },
              null,
              {
                "datum": "selected",
                "maxWidth": 140
              }
            ]}
              fields={[
              "grade",
              "pod",
              "lgd",
              "uw_adj"
            ]}
              with="cds/modifiers/crcf"
              transpose={true}
              title="Underwriter Adjustments"
              syncColumnWidthsKey="credit_rating_crcf" />
            <HX.Notes field="cds/modifiers/crcf/rating_commentary"
              title="Please provide detail on the source of the credit rating." />
            <HX.Notes field="cds/modifiers/crcf/obligor_commentary"
              title="Please provide detail on the Obligor Risk Drivers" />
            <HX.Notes field="cds/modifiers/crcf/lgd_commentary"
              title="Please provide detail on the Security & its Impact on Average LGD" />
            <HX.Notes field="cds/modifiers/crcf/uw_adj_commentary"
              title="Please provide detail on the Underwriter Adjustments" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Details - Political Risk"
          shownBy="/cds/show_hide/node/show_political">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/exposure/granular/political/tenor",
              "cds/exposure/granular/political/key_summary_outputs/tenor_rate",
              "cds/exposure/granular/political/simulation/num_sims",
              "cds/exposure/granular/political/exposure_curve",
              null
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Table data={[
              {
                "datum": "mobile_assets",
                "maxWidth": 140
              },
              {
                "datum": "fixed_assets",
                "maxWidth": 140
              },
              {
                "datum": "lenders_interest",
                "maxWidth": 140
              },
              {
                "datum": "sublimit",
                "maxWidth": 140
              },
              {
                "datum": "deductible",
                "maxWidth": 140
              }
            ]}
              fields={[
              "gov_action",
              "pol_violence",
              "cur_inconvertibility",
              "cont_relation_govt"
            ]}
              with="cds/exposure/granular/political/coverage_matrix"
              transpose={true}
              title="Coverage Matrix" />
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Table data={[
              null,
              {
                "datum": "override_min",
                "maxWidth": 140
              },
              {
                "datum": "override",
                "maxWidth": 140
              },
              {
                "datum": "override_max",
                "maxWidth": 140
              },
              null,
              {
                "datum": "selected",
                "maxWidth": 140
              }
            ]}
              fields={[
              null,
              "total",
              null,
              "industry",
              "insured_quality",
              "asset_composition"
            ]}
              with="cds/modifiers/political"
              transpose={true}
              title="Underwriter Adjustments" />
            <HX.Notes field="cds/modifiers/political/uw_adj_commentary"
              title="Please provide information on the Underwriter Adjustments" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Profile - Political Risk"
          shownBy="/cds/show_hide/node/show_political">
          <HX.Table title="Country Details"
            data={[
            "cds/exposure/granular/political/country_exposure"
          ]}
            fields={[
            "country",
            "sum_insured",
            "excess",
            "limit",
            "check",
            "country_2dig"
          ]}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Settings"
          shownBy="/cds/show_hide/node/show_political">
          <HX.Pane flow="right">
            <HX.Pane flow="down"
              stretch={true}>
              <HX.Collection fields={[
                "last_run_status",
                "check_run_consistent",
                "calc_run_value"
              ]}
                with="cds/ihs"
                title="Enter country details in sections below then press button to load IHS info." />
              <HX.Button title="Load IHS Data"
                task="task_api_ihs_data" />
            </HX.Pane>
            <HX.Pane flow="down"
              shownBy="/cds/show_hide/node/show_political">
              <HX.Collection fields={[
                "last_run_status",
                "check_run_consistent",
                "calc_run_value"
              ]}
                with="cds/exposure/granular/political/simulation"
                title="Enter all details in sections below then press button here to run simulation." />
              <HX.Button task="task_sim_political"
                title="Simulate Losses" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="IHS Information"
        fullWidth={true}
        shownBy="cds/show_hide/page/show_ihs">
        <HX.Section title="IHS Dataframe">
          <HX.Collection fields={[
            "last_run_status",
            "last_run_date",
            "last_run_value",
            "calc_run_value",
            "check_run_consistent"
          ]}
            with="cds/ihs"
            horizontal={true} />
          <HX.Button title="Load IHS Data"
            task="task_api_ihs_data" />
          <HX.Pane flow="right">
            <HX.Table title="IHS Outlook"
              data={[
              "cds/ihs/ihs_outlook"
            ]}
              fields={[
              {
                "field": "country",
                "maxWidth": 100
              },
              {
                "field": "risk_name",
                "maxWidth": 250
              },
              {
                "field": "outlook",
                "maxWidth": 120
              },
              {
                "field": "outlook_description",
                "maxWidth": 500
              },
              {
                "field": "last_updated_date",
                "maxWidth": 200
              },
              {
                "field": "last_updated_value",
                "maxWidth": 200
              }
            ]}
              maxListVisibleRows={15}
              kb-interactive={true}
              dynamic={true} />
            <HX.Table title="IHS Historic Values"
              data={[
              "cds/ihs/ihs_detail"
            ]}
              fields={[
              {
                "field": "country",
                "maxWidth": 100
              },
              {
                "field": "risk_name",
                "maxWidth": 250
              },
              {
                "field": "historic_updated_date",
                "maxWidth": 200
              },
              {
                "field": "historic_updated_value",
                "maxWidth": 200
              }
            ]}
              maxListVisibleRows={15}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        shownBy="cds/show_hide/page/show_rating_summary">
        <HX.Section title="Summary @ Share & Policy Period">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}
            shownBy="cds/standard_fields/is_rater_priced">
            <HX.Collection title="Priced Quotes"
              numCols={2}
              fields={[
              "quoted_premium",
              "model_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj",
              "benchmark_premium"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "tpi",
              "pflr",
              "bpi",
              "tpi_pre_uw_adj",
              "pflr_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Other Metrics"
              numCols={2}
              fields={[
              "roc",
              "uw_adj_impact"
            ]} />
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}
            shownBy="cds/standard_fields/is_case_priced">
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
        <HX.Section title="Summary Metrics @100% & Annual - Political Risks"
          shownBy="/cds/show_hide/node/show_political">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right"
              reflow={false}>
              <HX.Table title="Rate-on-Line & Kpis"
                data={[
                null,
                {
                  "datum": "metrics_summary_pre_uwadj",
                  "maxWidth": 140
                },
                {
                  "datum": "metrics_summary_pst_uwadj",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "rol_offered",
                "rol_model",
                "rol_technical",
                "rol_benchmark",
                null,
                "bpi",
                "tpi",
                "priced_to_plan",
                "priced_gglr",
                "priced_gnlr"
              ]}
                with="political"
                transpose={true}
                removeHorizontalScroll={true} />
              <HX.Table title="Premium Analysis by Peril - AFTER Underwriter Adjustment"
                data={[
                null,
                {
                  "datum": "total",
                  "maxWidth": 140
                },
                null,
                {
                  "datum": "gov_action",
                  "maxWidth": 140
                },
                {
                  "datum": "pol_violence",
                  "maxWidth": 140
                },
                {
                  "datum": "cur_inconvertibility",
                  "maxWidth": 140
                },
                {
                  "datum": "cont_relation_govt",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "premium_bound",
                "premium_benchmark",
                "premium_model",
                null,
                "premium_technical",
                "expected_loss",
                "che",
                "fixed_expenses",
                "variable_expenses",
                "investment_income",
                "cost_of_reinsurance",
                "capital",
                "brokerage"
              ]}
                with="political/premium_composition_pst_uwadj"
                transpose={true}
                removeHorizontalScroll={true} />
              <HX.Table title="Premium Analysis by Peril - BEFORE Underwriter Adjustment"
                data={[
                null,
                {
                  "datum": "total",
                  "maxWidth": 140
                },
                null,
                {
                  "datum": "gov_action",
                  "maxWidth": 140
                },
                {
                  "datum": "pol_violence",
                  "maxWidth": 140
                },
                {
                  "datum": "cur_inconvertibility",
                  "maxWidth": 140
                },
                {
                  "datum": "cont_relation_govt",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "premium_bound",
                "premium_benchmark",
                "premium_model",
                null,
                "premium_technical",
                "expected_loss",
                "che",
                "fixed_expenses",
                "variable_expenses",
                "investment_income",
                "cost_of_reinsurance",
                "capital",
                "brokerage"
              ]}
                with="political/premium_composition_pre_uwadj"
                transpose={true}
                removeHorizontalScroll={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Metrics @100% - CRCF"
          shownBy="/cds/show_hide/node/show_crcf">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right"
              reflow={false}>
              <HX.Table title="Rate-on-Exposure & KPI's"
                data={[
                null,
                {
                  "datum": "metrics_summary_pre_uwadj_annual",
                  "maxWidth": 140
                },
                {
                  "datum": "metrics_summary_pre_uwadj_term",
                  "maxWidth": 140
                },
                null,
                {
                  "datum": "metrics_summary_pst_uwadj_annual",
                  "maxWidth": 140
                },
                {
                  "datum": "metrics_summary_pst_uwadj_term",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "roe_offered",
                "roe_plan",
                "roe_technical",
                "roe_benchmark",
                null,
                "bpi",
                "tpi",
                "priced_to_plan",
                "priced_gglr",
                "priced_gnlr",
                "lgd_bound",
                "credit_rating_bound"
              ]}
                with="crcf"
                transpose={true}
                removeHorizontalScroll={true} />
              <HX.Table title="Loss Composition"
                data={[
                null,
                {
                  "datum": "loss_composition_pre_uwadj_term",
                  "maxWidth": 140
                },
                {
                  "datum": "loss_composition_pst_uwadj_term",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "exposure",
                "credit_rating",
                "pod",
                "tenor_load",
                "lgd",
                "recovery_discounted",
                "limit_discount",
                "term",
                "other",
                "expected_loss"
              ]}
                with="crcf"
                transpose={true}
                removeHorizontalScroll={true} />
              <HX.Table title="Premium Analysis"
                data={[
                null,
                {
                  "datum": "premium_composition_pre_uwadj_annual",
                  "maxWidth": 140
                },
                {
                  "datum": "premium_composition_pre_uwadj_term",
                  "maxWidth": 140
                },
                null,
                {
                  "datum": "premium_composition_pst_uwadj_annual",
                  "maxWidth": 140
                },
                {
                  "datum": "premium_composition_pst_uwadj_term",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "premium_bound",
                "premium_benchmark",
                "premium_plan",
                null,
                "premium_technical",
                "expected_loss",
                "che",
                "fixed_expenses",
                "variable_expenses",
                "investment_income",
                "cost_of_reinsurance",
                "capital",
                "brokerage"
              ]}
                with="crcf"
                transpose={true}
                removeHorizontalScroll={true} />
            </HX.Pane>
          </HX.With>
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
          <HX.Pane>
            <HX.Table title="Deal Status by Renewal Layers"
              data={[
              {
                "datum": "cds/layers",
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status.read_only"
              }
            ]}
              transpose={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data"
              shownBy="cds/rate_change/has_rarc_not_run" />
            <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
            <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
            <HX.Button title="Calculate Rate Change"
              task="rarc_task"
              shownBy="cds/standard_fields/is_rater_priced" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Renewal Layer 1"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "line_100pct/annualised",
                "beazley_line/annualised"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 150
                },
                {
                  "field": "renewal",
                  "width": 150
                }
              ]}
                with="rate_change/premium" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_selected",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}
        shownBy="cds/show_hide/page/show_rationale">
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
        <HX.Section title="Actuarial Commentary"
          defaultCollapsed={true}>
          <HX.Collection fields={[
            "cds/rationale/actuarial_review"
          ]} />
          <HX.Notes field="cds/rationale/actuarial_notes" />
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
        <HX.Section title="Useful Information">
          <HX.Pane flow="right">
            <HX.Notes field="cds/rationale/help_file" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs">
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Actuarial Info (typically hidden)"
        fullWidth={true}
        shownBy="cds/show_hide/page/show_actuarial">
        <HX.Section title="IHS Dataframe"
          defaultCollapsed={true}>
          <HX.Collection fields={[
            "last_run_status",
            "last_run_date",
            "last_run_value",
            "calc_run_value",
            "check_run_consistent"
          ]}
            with="cds/ihs"
            horizontal={true} />
          <HX.Button title="Load IHS Data"
            task="task_api_ihs_data" />
          <HX.Pane flow="right">
            <HX.Table title="IHS Outlook"
              data={[
              "cds/ihs/ihs_outlook"
            ]}
              fields={[
              {
                "field": "country",
                "maxWidth": 100
              },
              {
                "field": "risk_name",
                "maxWidth": 250
              },
              {
                "field": "outlook",
                "maxWidth": 120
              },
              {
                "field": "outlook_description",
                "maxWidth": 500
              },
              {
                "field": "last_updated_date",
                "maxWidth": 200
              },
              {
                "field": "last_updated_value",
                "maxWidth": 200
              }
            ]}
              maxListVisibleRows={15}
              kb-interactive={true}
              dynamic={true} />
            <HX.Table title="IHS Historic Values"
              data={[
              "cds/ihs/ihs_detail"
            ]}
              fields={[
              {
                "field": "country",
                "maxWidth": 100
              },
              {
                "field": "risk_name",
                "maxWidth": 250
              },
              {
                "field": "historic_updated_date",
                "maxWidth": 200
              },
              {
                "field": "historic_updated_value",
                "maxWidth": 200
              }
            ]}
              maxListVisibleRows={15}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Simulation"
          defaultCollapsed={true}>
          <HX.Collection fields={[
            "total_sim_loss_uncapped",
            "total_sim_loss_capped",
            "total_det_loss_uncapped",
            "total_det_loss_capped",
            "total_det_loss_scaled"
          ]}
            with="cds/exposure/granular/political/simulation"
            horizontal={true} />
          <HX.Collection fields={[
            "last_run_status",
            "last_run_date",
            "last_run_value",
            "calc_run_value",
            "check_run_consistent"
          ]}
            with="cds/exposure/granular/political/simulation"
            horizontal={true} />
          <HX.Button title="Simulate loss"
            task="task_sim_political" />
        </HX.Section>
        <HX.Section title="Load from Beazley Intelligence"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Collection fields={[
              "last_run_status",
              "last_run_date",
              "last_run_value",
              "calc_run_value",
              "check_run_consistent"
            ]}
              with="cds/bi"
              title="Enter Policy Section Reference then press button here to load latest Beazley Intelligence information." />
            <HX.Button title="Load from BI"
              task="task_sql_bi_data"
              stretch={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Rating Dataframe - CRCF"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Complete List"
              data={[
              "cds/exposure/granular/crcf/exposure_profile"
            ]}
              fields={[
              "year",
              "year_label",
              "year_show_hide",
              "month_1",
              "month_2",
              "month_3",
              "month_4",
              "month_5",
              "month_6",
              "month_7",
              "month_8",
              "month_9",
              "month_10",
              "month_11",
              "month_12",
              "average_default_month",
              "average_default_year_month",
              "average_exposure",
              "average_recovery_time",
              "expected_recovery_pct",
              "term_adj",
              "pre_uw_adj_tenor_load",
              "pre_uw_adj_pod_adj_inc",
              "pre_uw_adj_pod_adj_inc_allow_prior",
              "pre_uw_adj_average_severity",
              "pre_uw_adj_average_loss",
              "pre_uw_adj_average_loss_adj_lim_xs",
              "pre_uw_adj_premium_benchmark",
              "pre_uw_adj_premium_achieved",
              "pre_uw_adj_premium_achieved_adj_pod",
              "pst_uw_adj_tenor_load",
              "pst_uw_adj_pod_adj_inc",
              "pst_uw_adj_pod_adj_inc_allow_prior",
              "pst_uw_adj_average_severity",
              "pst_uw_adj_average_loss",
              "pst_uw_adj_average_loss_adj_lim_xs",
              "pst_uw_adj_premium_benchmark",
              "pst_uw_adj_premium_achieved",
              "pst_uw_adj_premium_achieved_adj_pod",
              "implied_lgd_average_loss_adj_lim_xs",
              "implied_lgd_average_loss",
              "implied_lgd_average_severity",
              "implied_lgd",
              "implied_grade_average_loss_adj_lim_xs",
              "implied_grade_average_loss",
              "implied_grade_pod_adj_inc_allow_prior",
              "implied_grade_pod_adj_inc",
              "implied_grade_pod_inc"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Rating Dataframe - Political Risk"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Complete List"
              data={[
              "cds/exposure/granular/political/country_exposure"
            ]}
              fields={[
              "id",
              "country",
              "sum_insured",
              "excess",
              "limit",
              "check",
              "country_2dig",
              "sublimit_pv",
              "deductible_pv",
              "sublimit_ci",
              "ihs_political",
              "ihs_violence",
              "ihs_ci",
              "prem_roe_gai",
              "prem_roe_pv",
              "prem_roe_ci",
              "prem_roe_crg",
              "prem_roe_tot",
              "loss_roe_gai",
              "loss_roe_pv",
              "loss_roe_ci",
              "loss_roe_crg",
              "loss_roe_tot",
              "struc_adj_gai",
              "struc_adj_pv",
              "struc_adj_ci",
              "struc_adj_crg",
              "net_rol_gai",
              "net_rol_pv",
              "net_rol_ci",
              "net_rol_crg",
              "net_rol_tot",
              "gross_rol_tot"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Metrics - Political Risks"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table title="Rate-on-Line & Kpis"
                data={[
                null,
                {
                  "datum": "metrics_summary_pre_uwadj",
                  "maxWidth": 140
                },
                {
                  "datum": "metrics_summary_pst_uwadj",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "rol_offered",
                "rol_model",
                "rol_technical",
                "rol_benchmark",
                null,
                "bpi",
                "priced_to_plan",
                "tpi",
                "priced_gglr",
                "priced_gnlr"
              ]}
                with="political"
                transpose={true}
                syncColumnWidthsKey="metrics_1" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Premium Details - Political Risks"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table title="Premium Analysis by Peril - BEFORE Underwriter Adjustment"
                data={[
                null,
                {
                  "datum": "gov_action",
                  "maxWidth": 140
                },
                {
                  "datum": "pol_violence",
                  "maxWidth": 140
                },
                {
                  "datum": "cur_inconvertibility",
                  "maxWidth": 140
                },
                {
                  "datum": "cont_relation_govt",
                  "maxWidth": 140
                },
                {
                  "datum": "total",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "premium_bound",
                "premium_benchmark",
                "premium_model",
                null,
                "premium_technical",
                "expected_loss",
                "che",
                "fixed_expenses",
                "variable_expenses",
                "investment_income",
                "cost_of_reinsurance",
                "capital",
                "brokerage"
              ]}
                with="political/premium_composition_pre_uwadj"
                transpose={true}
                syncColumnWidthsKey="xxxxxxxxxxxxxxxxxxxxx" />
              <HX.Table title="Premium Analysis by Peril - AFTER Underwriter Adjustment"
                data={[
                null,
                {
                  "datum": "gov_action",
                  "maxWidth": 140
                },
                {
                  "datum": "pol_violence",
                  "maxWidth": 140
                },
                {
                  "datum": "cur_inconvertibility",
                  "maxWidth": 140
                },
                {
                  "datum": "cont_relation_govt",
                  "maxWidth": 140
                },
                {
                  "datum": "total",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "premium_bound",
                "premium_benchmark",
                "premium_model",
                null,
                "premium_technical",
                "expected_loss",
                "che",
                "fixed_expenses",
                "variable_expenses",
                "investment_income",
                "cost_of_reinsurance",
                "capital",
                "brokerage"
              ]}
                with="political/premium_composition_pst_uwadj"
                transpose={true}
                syncColumnWidthsKey="xxxxxxxxxxxxxxxxxxxxx" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Mapping to standard fields"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Table title="hx - standard fields"
                data={[
                "hx_core"
              ]}
                fields={[
                "inception_date",
                "expiry_date",
                "model_premium",
                "charged_premium",
                "premium_currency",
                "ulr",
                "class_code"
              ]}
                transpose={true} />
              <HX.Table title="cds - currencies"
                data={[
                "cds/currencies"
              ]}
                fields={[
                "target_currency",
                "source_currency",
                "multi_currency_support"
              ]}
                transpose={true} />
              <HX.Table title="cds - experience rating"
                data={[
                "cds/experience_rating"
              ]}
                fields={[
                "claims_available",
                "claims_fgu",
                "claims_net_of_deductible"
              ]}
                transpose={true} />
              <HX.Table title="cds"
                data={[
                "cds"
              ]}
                fields={[
                "database_id",
                "broker_contact",
                "product"
              ]}
                transpose={true} />
            </HX.Pane>
            <HX.Table title="cds - standard fields"
              data={[
              "cds/standard_fields"
            ]}
              fields={[
              "insured_name",
              "broker",
              "expiry_date",
              "inception_date",
              "insured_country",
              "insured_postal_code",
              "insured_state_or_province",
              "is_admitted_or_surplus",
              "is_free_trade_zone",
              "is_renewal",
              "underwriter",
              "policy_reference",
              "facility_reference",
              "benchmark_class",
              "uw_rationale",
              "trifocus",
              "rating_methodology",
              "is_case_priced",
              "is_rater_priced"
            ]}
              transpose={true} />
            <HX.Table title="cds - standard layer fields"
              data={[
              "cds/layers"
            ]}
              fields={[
              "limit",
              "excess",
              "deductible",
              "aggregate_limit",
              "aggregate_excess",
              "aggregate_deductible",
              "currency",
              "section_reference",
              "brokerage",
              "written_line",
              "premium",
              "status",
              "is_primary_excess",
              "benchmark_premium",
              "bpi",
              "bpi_pre_uw_adj",
              "model_premium",
              "unity_premium",
              "quoted_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj",
              "technical_premium_net",
              "tpi",
              "tpi_pre_uw_adj",
              "pflr_att",
              "pflr_cat",
              "pflr",
              "roc",
              "uw_adj_impact",
              "trifocus",
              "expected_loss_cost",
              "expected_loss_cost_pre_uw_adj",
              "bpi_case_priced",
              "pflr_pre_uw_adj",
              "premium_label"
            ]}
              transpose={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};