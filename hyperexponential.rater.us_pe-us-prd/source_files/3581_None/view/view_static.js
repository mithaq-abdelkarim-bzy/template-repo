
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";

function HXModel(props) {
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
        fullWidth={false}
        viewScale={1}>
        <HX.With context={{
          "path": "cds",
          "type": "struct"
        }}>
          <HX.Section title="Account Details">
            <HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection with="/hx_core"
                  fields={[
                  "inception_date",
                  "expiry_date"
                ]}
                  horizontal={true} />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "standard_fields/underwriter"
                ]} />
                <HX.Pane />
              </HX.Pane>
              <HX.Collection fields={[
                "standard_fields/insured_name"
              ]} />
              <HX.Pane flow="right">
                <HX.Collection with="standard_fields"
                  fields={[
                  "policy_reference",
                  "is_renewal"
                ]}
                  horizontal={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Broker Details">
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "standard_fields/broker",
                "broker_contact"
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Coverage Selection">
            <HX.Pane>
              <HX.Collection with="account_details"
                fields={[
                "product_type",
                "retroactive_years/years"
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Optional Exposure"
          shownBy="cds/rating_factors/med_mal/hide">
          <HX.With context={{
            "path": "cds/rating_factors",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "/cds/key_industry/code_name",
                  "infoBy": "/cds/tooltips/occupation"
                },
                {
                  "field": "/cds/key_industry/sub_occupation/name",
                  "infoBy": "/cds/tooltips/sub_occupation"
                },
                {
                  "field": "/cds/standard_fields/insured_state_or_province",
                  "infoBy": "/cds/tooltips/state"
                }
              ]}
                horizontal={true} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "/cds/rating_factors/loss_experience",
                  "infoBy": "/cds/tooltips/loss_experience"
                },
                {
                  "field": "longevity/years",
                  "infoBy": "/cds/tooltips/longevity",
                  "shownBy": "longevity/show"
                },
                {
                  "field": "professional_experience/years",
                  "infoBy": "/cds/tooltips/professional_experience",
                  "shownBy": "professional_experience/show"
                }
              ]}
                horizontal={true} />
              <HX.Pane shownBy="show_loss_experience_empty_panel" />
              <HX.Pane shownBy="show_loss_experience_empty_panel" />
            </HX.Pane>
            <HX.Pane flow="right"
              shownBy="business_with_written_contract/show">
              <HX.Collection fields={[
                {
                  "field": "business_with_written_contract/percentage",
                  "infoBy": "/cds/tooltips/business_with_written_contract_percentage"
                },
                {
                  "field": "business_with_written_contract/revenue",
                  "infoBy": "/cds/tooltips/business_with_written_contract_revenue"
                }
              ]}
                horizontal={true} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "underwriter_judgement",
                  "infoBy": "/cds/tooltips/underwriter_judgement"
                },
                {
                  "field": "underwriter_judgement_justification",
                  "infoBy": "/cds/tooltips/underwriter_judgement_justification"
                }
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Revenue Tiers"
          shownBy="cds/rating_factors/med_mal/hide">
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "rating_factors/revenues"
                }
              ]}
                fields={[
                "hazard_tier/tier",
                "hazard_tier/business_description",
                "value",
                {
                  "field": "type",
                  "shownBy": "rating_factors/show_revenue_type"
                }
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "exposure/aggregate/total_revenue"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Optional Exposure"
          shownBy="cds/rating_factors/med_mal/show">
          <HX.With context={{
            "path": "cds/rating_factors",
            "type": "struct"
          }}>
            <HX.Pane flow="down">
              <HX.Collection fields={[
                {
                  "field": "/cds/standard_fields/insured_state_or_province",
                  "infoBy": "/cds/tooltips/state"
                },
                {
                  "field": "loss_experience",
                  "infoBy": "/cds/tooltips/loss_experience"
                }
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                {
                  "field": "underwriter_judgement",
                  "infoBy": "/cds/tooltips/underwriter_judgement"
                },
                {
                  "field": "underwriter_judgement_justification",
                  "infoBy": "/cds/tooltips/underwriter_judgement_justification"
                }
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Med Mal"
          shownBy="cds/rating_factors/med_mal/show">
          <HX.With context={{
            "path": "cds/rating_factors",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection with="med_mal"
                fields={[
                "allied_medical/allied_medical_type",
                "social_services/social_services_type"
              ]} />
              <HX.Collection with="med_mal"
                fields={[
                "allied_medical/exposure_measure",
                "social_services/exposure_measure"
              ]} />
              <HX.Collection with="med_mal"
                fields={[
                "allied_medical/exposure_type",
                "social_services/exposure_type"
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "professional_experience/years",
                  "labelBy": "professional_experience/med_mal_professional_experience_label"
                }
              ]} />
              <HX.Collection fields={[
                "professional_experience/factor"
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "longevity/years",
                  "labelBy": "longevity/med_mal_longevity_label"
                }
              ]} />
              <HX.Collection fields={[
                "longevity/factor"
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/cds/exposure/aggregate/med_mal/total_credit_or_debit"
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "med_mal/endorsements"
                }
              ]}
                fields={[
                "endorsement",
                "factor"
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/cds/exposure/aggregate/med_mal/total_endorsement"
              ]} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Staffing Risk Type"
          shownBy="cds/rating_factors/staffing/show">
          <HX.With context={{
            "path": "cds/rating_factors/staffing",
            "type": "struct"
          }}>
            <HX.Pane flow="down">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "permanent"
                ]} />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "peo"
                ]} />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "temporary"
                ]} />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "/cds/exposure/aggregate/staffing/total"
                ]} />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}>
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "/cds/standard_fields/rating_methodology"
            ]}
              syncColumnWidthsKey="coverage_tables" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rating Factors">
          <HX.Pane flow="right">
            <HX.Collection with="cds/rating_factors"
              fields={[
              {
                "field": "tech/media_and_advertising",
                "shownBy": "tech/show"
              },
              {
                "field": "tech/cont_bi_pd",
                "shownBy": "tech/show"
              },
              {
                "field": "tech/first_party_privacy",
                "shownBy": "tech/show"
              },
              {
                "field": "tech/cyber_extortion_only",
                "shownBy": "tech/show"
              },
              {
                "field": "general_liability/value",
                "shownBy": "general_liability/show"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Coverage Options">
            <HX.Pane flow="down">
              <HX.Table title="Quote Inputs"
                syncColumnWidthsKey="coverage_tables"
                data={[
                {
                  "datum": "/cds/layers",
                  "width": 250
                }
              ]}
                fields={[
                "is_primary_excess",
                null,
                "status",
                "limit",
                {
                  "field": "product_liability_limits_AGG",
                  "shownBy": "/cds/rating_factors/show_product_liability_limits_AGG"
                },
                {
                  "field": "aggregate_limit",
                  "shownBy": "liability_limits_AGG/show"
                },
                {
                  "field": "aggregate_limit",
                  "labelBy": "/cds/rating_factors/staffing_liability_limits_AGG_label",
                  "shownBy": "/cds/rating_factors/show_staffing_liability_limits_AGG"
                },
                {
                  "field": "general_liability/limit_staffing",
                  "shownBy": "/cds/rating_factors/general_liability/show_staffing"
                },
                {
                  "field": "aggregate_limit",
                  "labelBy": "/cds/rating_factors/general_liability_limits_AGG_products_label",
                  "shownBy": "/cds/rating_factors/show_product_liability_limits_AGG"
                },
                {
                  "field": "personal_advertising_liability_EEC/limit",
                  "shownBy": "personal_advertising_liability_EEC/show"
                },
                {
                  "field": "defence_outside_limits/limit",
                  "shownBy": "defence_outside_limits/show"
                },
                "deductible",
                {
                  "field": "excess",
                  "shownBy": "show_excess"
                },
                "brokerage",
                "written_line",
                null,
                "quoted_premium",
                {
                  "field": "model_premium",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                "technical_premium",
                {
                  "field": "technical_premium_pre_uw_adj",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "benchmark_premium"
                },
                null,
                "tpi",
                {
                  "field": "tpi_pre_uw_adj",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "bpi",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "bpi_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                "pflr",
                "roc",
                {
                  "field": "uw_adj_impact",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                }
              ]}
                transpose={true}
                freezeLeft={0} />
              <HX.Table title="COB Code Breakdown"
                syncColumnWidthsKey="coverage_tables"
                data={[
                "/cds/layers"
              ]}
                fields={[
                "cob/code_1",
                "cob/premium_1",
                "cob/code_2",
                "cob/premium_2",
                "cob/code_3",
                "cob/premium_3"
              ]}
                transpose={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
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
            <HX.Table title=""
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
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
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
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
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
        <HX.Section title="Renewal Layer 2"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 1,
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
          </HX.With>
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
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
        <HX.Section title="Renewal Layer 3"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 2,
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
          </HX.With>
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
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
        <HX.Section title="Renewal Layer 4"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 3,
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
          </HX.With>
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
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
        <HX.Section title="Renewal Layer 5"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 4,
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
          </HX.With>
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
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
        <HX.Section title="Renewal Layer 6"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 5,
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
          </HX.With>
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
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
        <HX.Section title="Renewal Layer 7"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_7">
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 6,
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
          </HX.With>
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
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
        <HX.Section title="Renewal Layer 8"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_8">
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 7,
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
          </HX.With>
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
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
        <HX.Section title="Renewal Layer 9"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_9">
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 8,
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
          </HX.With>
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
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
        <HX.Section title="Renewal Layer 10"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_10">
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 9,
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
          </HX.With>
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
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
                  "width": 130
                },
                {
                  "field": "uw_selected",
                  "width": 130
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
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
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}>
        <HX.With context={{
          "path": "cds/rationale",
          "type": "struct"
        }}>
          <HX.Section title="KNOWLEDGE OF INSURED">
            <HX.Notes field="knowledge_of_insured" />
          </HX.Section>
          <HX.Section title="PORTFOLIO FIT">
            <HX.Notes field="portfolio_fit" />
          </HX.Section>
          <HX.Section title="BASIS OF RISK SELECTION">
            <HX.Notes field="basis_of_risk_selection" />
          </HX.Section>
          <HX.Section title="UNUSUAL OR COMPLEX OPERATIONS">
            <HX.Notes field="unusual_or_complex_operations" />
          </HX.Section>
          <HX.Section title="FACTS AFFECTING DECISION">
            <HX.Notes field="facts_affecting_decision" />
          </HX.Section>
        </HX.With>
      </HX.Page>
    </HX.Root>
  );
}

export default HXModel;