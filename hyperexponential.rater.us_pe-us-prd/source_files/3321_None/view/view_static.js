
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
        fullWidth={false}
        viewScale={1}>
        <HX.Section title="Optional Exposure"
          shownBy="cds/exposure/aggregate/med_mal/hide">
          <HX.With context={{
            "path": "cds/exposure/aggregate",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "/cds/key_industry/code_name",
                  "infoBy": "tooltips/occupation"
                },
                {
                  "field": "/cds/key_industry/sub_occupation/name",
                  "infoBy": "tooltips/sub_occupation"
                },
                {
                  "field": "state",
                  "infoBy": "tooltips/state"
                }
              ]}
                horizontal={true} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "loss_experience",
                  "infoBy": "tooltips/loss_experience"
                },
                {
                  "field": "longevity/years",
                  "infoBy": "tooltips/longevity",
                  "shownBy": "longevity/show"
                },
                {
                  "field": "professional_experience/years",
                  "infoBy": "tooltips/professional_experience",
                  "shownBy": "professional_experience/show"
                }
              ]}
                horizontal={true} />
              <HX.Pane shownBy="show_loss_experience_empty_panel" />
              <HX.Pane shownBy="show_loss_experience_empty_panel" />
            </HX.Pane>
            <HX.Pane flow="right"
              shownBy="business_with_written_contract/show">
              <HX.Collection with="business_with_written_contract"
                fields={[
                {
                  "field": "percentage",
                  "infoBy": "/cds/exposure/aggregate/tooltips/business_with_written_contract_percentage"
                },
                {
                  "field": "revenue",
                  "infoBy": "/cds/exposure/aggregate/tooltips/business_with_written_contract_revenue"
                }
              ]}
                horizontal={true} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "underwriter_judgement",
                  "infoBy": "tooltips/underwriter_judgement"
                },
                {
                  "field": "underwriter_judgement_justification",
                  "infoBy": "tooltips/underwriter_judgement_justification"
                }
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Revenue Tiers"
          shownBy="cds/exposure/aggregate/med_mal/hide">
          <HX.With context={{
            "path": "cds/exposure",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "aggregate/revenues"
                }
              ]}
                fields={[
                "hazard_tier/tier",
                "hazard_tier/business_description",
                "value",
                {
                  "field": "type",
                  "shownBy": "aggregate/staffing/hide"
                }
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "aggregate/total_revenue"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Optional Exposure"
          shownBy="cds/exposure/aggregate/med_mal/show">
          <HX.With context={{
            "path": "cds/exposure/aggregate",
            "type": "struct"
          }}>
            <HX.Pane flow="down">
              <HX.Collection fields={[
                {
                  "field": "state",
                  "infoBy": "tooltips/state"
                },
                {
                  "field": "loss_experience",
                  "infoBy": "tooltips/loss_experience"
                }
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                {
                  "field": "underwriter_judgement",
                  "infoBy": "tooltips/underwriter_judgement"
                },
                {
                  "field": "underwriter_judgement_justification",
                  "infoBy": "tooltips/underwriter_judgement_justification"
                }
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Med Mal"
          shownBy="cds/exposure/aggregate/med_mal/show">
          <HX.With context={{
            "path": "cds/exposure/aggregate",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection with="med_mal"
                fields={[
                "allied_medical/allied_medical",
                "social_services/social_services"
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
                "med_mal/total_credit_or_debit"
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
                "med_mal/total_endorsement"
              ]} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Staffing Risk Type"
          shownBy="cds/exposure/aggregate/staffing/show">
          <HX.With context={{
            "path": "cds/exposure/aggregate/staffing",
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
                  "total"
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
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
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
          <HX.Section title="Coverage Options">
            <HX.Pane flow="down">
              <HX.Table title="Quote Inputs"
                syncColumnWidthsKey="coverage_tables"
                data={[
                "/cds/layers"
              ]}
                fields={[
                "is_primary_excess",
                {
                  "field": "media_and_advertising",
                  "shownBy": "/cds/layers_options/show_tech_options"
                },
                {
                  "field": "cont_bi_pd",
                  "shownBy": "/cds/layers_options/show_tech_options"
                },
                {
                  "field": "first_party_privacy",
                  "shownBy": "/cds/layers_options/show_tech_options"
                },
                {
                  "field": "cyber_extortion_only",
                  "shownBy": "/cds/layers_options/show_tech_options"
                },
                {
                  "field": "general_liability/true_or_false",
                  "shownBy": "general_liability/show"
                },
                {
                  "field": null,
                  "shownBy": "general_liability/show"
                },
                "limit",
                {
                  "field": "product_liability_limits_AGG",
                  "shownBy": "show_product_liability_limits_AGG"
                },
                {
                  "field": "aggregate_limit",
                  "shownBy": "liability_limits_AGG/show"
                },
                {
                  "field": "aggregate_limit",
                  "labelBy": "staffing_liability_limits_AGG_label",
                  "shownBy": "general_liability/show_staffing_liability_limits_AGG"
                },
                {
                  "field": "aggregate_limit",
                  "labelBy": "general_liability_limits_AGG_products_label",
                  "shownBy": "show_product_liability_limits_AGG"
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