
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";

function HXModel(props) {
  return (
    <HX.Root>
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
                  "/cds/exposure/aggregate/total"
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
                "/cds/layers"
              ]}
                fields={[
                "is_primary_excess",
                null,
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
                "premium",
                "brokerage",
                "status",
                null,
                "model_premium",
                "benchmark_premium",
                "bpi",
                "technical_premium",
                "tpi",
                "effective_rate",
                "pflr"
              ]}
                transpose={true} />
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