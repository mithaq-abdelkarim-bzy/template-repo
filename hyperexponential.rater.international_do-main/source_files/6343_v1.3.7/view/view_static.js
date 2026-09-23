
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
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/risk_information/date_validation",
              null
            ]}
              horizontal={true}
              shownBy="cds/risk_information/date_validation_flag" />
            <HX.Collection fields={[
              {
                "field": "cds/standard_fields/underwriter",
                "shownBy": "cds/validation/underwriter/valid"
              },
              {
                "field": "cds/standard_fields/underwriter.notSupported",
                "infoBy": "cds/validation/underwriter/info_text",
                "shownBy": "cds/validation/underwriter/invalid"
              },
              "cds/risk_information/beazley_branch"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              {
                "field": "cds/risk_information/underwriting_assistant",
                "shownBy": "cds/validation/underwriting_assistant/valid"
              },
              {
                "field": "cds/risk_information/underwriting_assistant.notSupported",
                "infoBy": "cds/validation/underwriting_assistant/info_text",
                "shownBy": "cds/validation/underwriting_assistant/invalid"
              },
              null
            ]}
              horizontal={true} />
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "cds/standard_fields/insured_name"
              ]} />
            </HX.Pane>
            <HX.Collection fields={[
              "currencies/source_currency",
              "standard_fields/is_renewal",
              "risk_information/cips_policy",
              null
            ]}
              with="cds"
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "rating_factors/risk_information/ownership_type",
              {
                "field": "risk_information/pe_backer",
                "shownBy": "risk_information/private_flag"
              }
            ]}
              with="cds" />
            <HX.Collection fields={[
              {
                "field": "rating_factors/risk_information/us_adr_exposure"
              },
              {
                "field": "risk_information/other_pe_backer",
                "shownBy": "risk_information/other_pe_backer_flag"
              }
            ]}
              syncColumnWidthsKey="Sync1"
              with="cds" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "mmp_flag"
            ]}
              horizontal={true}
              with="cds/risk_information" />
            <HX.Collection fields={[
              "macquarie_flag"
            ]}
              horizontal={true}
              with="cds/risk_information" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/risk_information/country_of_domicile",
              "cds/rating_factors/risk_information/main_operating_country",
              {
                "field": "cds/rating_factors/risk_information/primary_listing_location",
                "shownBy": "cds/risk_information/public_flag"
              }
            ]}
              syncColumnWidthsKey="Sync1" />
            <HX.Collection fields={[
              "cds/rating_factors/risk_information/search_sic",
              "cds/rating_factors/risk_information/industry_class_sic_code"
            ]}
              syncColumnWidthsKey="Sync1" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            {
              "field": "standard_fields/broker",
              "shownBy": "validation/broker/valid"
            },
            {
              "field": "standard_fields/broker.notSupported",
              "infoBy": "validation/broker/info_text",
              "shownBy": "validation/broker/invalid"
            },
            "broker_sub_category",
            "broker_contact"
          ]}
            with="cds"
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Policy Tags">
          <HX.Pane flow="right">
            <HX.Button task="generate_tags"
              title="Create Policy Tags" />
            <HX.Collection fields={[
              "policy_tag_msg"
            ]}
              with="cds" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Other Information">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "core_account",
                "afb_primary_wording_manuscript",
                "esg_syndicate",
                "esg_net_premium",
                {
                  "field": "any_one_claim",
                  "shownBy": "not_mmp_flag"
                }
              ]}
                with="cds/risk_information" />
              <HX.Collection fields={[
                "platform",
                "long_term_agreement",
                "direct_ri",
                {
                  "field": "cedant_name",
                  "shownBy": "ri_flag"
                },
                "epl_sublimit",
                "epl_sublimit_premium"
              ]}
                with="cds/risk_information" />
            </HX.Pane>
          </HX.Pane>
          <HX.Notes title="Company Description"
            field="cds/risk_information/company_description" />
        </HX.Section>
        <HX.Section title="Comments">
          <HX.Notes field="cds/risk_information/comments" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        viewScale={1}>
        <HX.Section title="S&P CapIQ Search"
          shownBy="cds/risk_information/public_flag">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/key_industry/ticker",
              {
                "field": "cds/company_search",
                "infoBy": "cds/exposure/aggregate/company_search_info"
              }
            ]}
              horizontal={true} />
            <HX.Pane flow="right">
              <HX.Button task="capiq_fetch_task"
                title="Search CapIQ" />
              <HX.Collection fields={[
                "cds/capiq_results"
              ]} />
            </HX.Pane>
            <HX.Table shownBy="cds/capiq_search_complete"
              data={[
              {
                "datum": "cds/capiq"
              }
            ]}
              fields={[
              "selection",
              "insured_name",
              "exchange",
              "market_cap_2_year_high",
              "currency",
              "date_updated"
            ]}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right"
            shownBy="cds/capiq_search_complete">
            <HX.Button task="populate_capiq_data_task"
              title="Populate Rater" />
            <HX.Collection fields={[
              "cds/capiq_populate"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Financials">
          <HX.Pane>
            <HX.Collection shownBy="cds/risk_information/private_flag"
              fields={[
              "cds/exposure/aggregate/exposure_currency",
              null,
              null,
              null
            ]}
              horizontal={true} />
            <HX.Collection shownBy="cds/risk_information/public_flag"
              fields={[
              "cds/currencies/source_currency.read_only",
              null,
              null,
              null
            ]}
              horizontal={true} />
            <HX.Table data={[
              {
                "datum": "cds/exposure/aggregate",
                "maxWidth": 250,
                "minWidth": 175
              }
            ]}
              fields={[
              {
                "field": "market_cap_2_year_high",
                "shownBy": "cds/risk_information/public_flag"
              },
              {
                "field": "current_market_cap",
                "shownBy": "cds/risk_information/public_flag"
              },
              {
                "field": "fifty_two_week_high",
                "shownBy": "cds/risk_information/public_flag"
              },
              {
                "field": "fifty_two_week_low",
                "shownBy": "cds/risk_information/public_flag"
              },
              {
                "field": "main_exchange",
                "shownBy": "cds/risk_information/public_flag"
              },
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
              "retained_earnings",
              null,
              {
                "field": "period_ended",
                "shownBy": "cds/risk_information/public_flag"
              },
              "period_data"
            ]}
              transpose={true}
              syncColumnWidthsKey="SyncExp"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="USA Exposure Details"
          shownBy="cds/risk_information/public_us_flag">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/exposure/aggregate",
                "maxWidth": 250,
                "minWidth": 175
              }
            ]}
              fields={[
              {
                "field": "adr_level",
                "shownBy": "cds/risk_information/public_us_flag"
              },
              {
                "field": "sponsored",
                "shownBy": "cds/risk_information/adr_level_one_flag"
              },
              {
                "field": "us_listing_share",
                "shownBy": "cds/risk_information/public_us_flag"
              }
            ]}
              transpose={true}
              syncColumnWidthsKey="SyncExp"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Collection shownBy="cds/level_1_us_exp_flag"
            fields={[
            "cds/level_1_us_exp_msg",
            null,
            null
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Additional Information"
          shownBy="cds/risk_information/public_flag">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/exposure/aggregate",
                "maxWidth": 250,
                "minWidth": 175
              }
            ]}
              fields={[
              {
                "field": "credit_score",
                "infoBy": "cds/exposure/aggregate/credit_score_info"
              },
              "insider_shareholder_share",
              "insider_shareholder_details",
              "institutional_ownership_share",
              "ipo_date",
              "ignore_ipo"
            ]}
              transpose={true}
              syncColumnWidthsKey="SyncExp"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "insider_shareholder_comment",
              null,
              "ipo_comment",
              null
            ]}
              with="cds/exposure/aggregate"
              numCols={2} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Financial Metrics">
          <HX.Pane>
            <HX.Table data={[
              "current_ratio",
              "accumulated_profitability",
              "return_on_assets",
              "book_value_liability_ratio",
              "asset_turnover",
              "z_score",
              "roe",
              "net_debt_equity_ratio",
              "cash_conversion"
            ]}
              fields={[
              {
                "field": "value",
                "width": 100
              },
              {
                "field": "rag_status",
                "width": 100
              }
            ]}
              with="cds/exposure/aggregate"
              syncColumnWidthsKey="SyncExp"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="EPL Inputs"
          shownBy="cds/risk_information/mmp_flag">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/exposure/aggregate",
                "maxWidth": 250,
                "minWidth": 175
              }
            ]}
              fields={[
              "us_ftes",
              "row_ftes"
            ]}
              transpose={true}
              syncColumnWidthsKey="SyncExp"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Assessment"
        viewScale={1}
        fullWidth={true}
        shownBy="cds/risk_information/not_mmp_flag">
        <HX.Section title="Sector Commentary">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Notes field="cds/modifiers/message"
                title="Message" />
              <HX.Pane>
                <HX.Collection fields={[
                  {
                    "field": "sca_freq_adj_factor",
                    "infoBy": "sca_freq_adj_factor_info"
                  },
                  null,
                  null,
                  null,
                  null,
                  null
                ]}
                  with="cds/modifiers"
                  horizontal={true} />
                <HX.Collection fields={[
                  "sca_freq_adj_factor_comment"
                ]}
                  with="cds/modifiers" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Underwriting Modifiers - AB/ABC">
          <HX.Pane flow="right">
            <HX.Table data={[
              "cds/modifiers/management_corp_gov_factors",
              "cds/modifiers/business_financial_model_factors",
              "cds/modifiers/significant_event_factors",
              "cds/modifiers/stock_market_factors",
              "cds/modifiers/sca_adj_factors"
            ]}
              fields={[
              {
                "field": "value",
                "width": 100
              },
              {
                "field": "min",
                "width": 100
              },
              {
                "field": "max",
                "width": 100
              },
              {
                "field": "comment",
                "maxWidth": 600
              }
            ]}
              rowHeaderSettings={{
              "width": 400
            }}
              shownBy="cds/risk_information/public_flag"
              kb-interactive={true} />
            <HX.Table data={[
              "cds/modifiers/management_corp_gov_factors",
              "cds/modifiers/business_financial_model_factors",
              "cds/modifiers/significant_event_factors",
              "cds/modifiers/sca_adj_factors"
            ]}
              fields={[
              {
                "field": "value",
                "width": 100
              },
              {
                "field": "min",
                "width": 100
              },
              {
                "field": "max",
                "width": 100
              },
              {
                "field": "comment",
                "maxWidth": 600
              }
            ]}
              rowHeaderSettings={{
              "width": 400
            }}
              shownBy="cds/risk_information/private_flag"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane />
          <HX.Pane flow="right">
            <HX.Table data={[
              "regulatory_factors",
              "mergers_and_acquisitions_factors",
              "territory_of_operation_factors",
              "total_factors"
            ]}
              fields={[
              {
                "field": "value",
                "width": 100
              },
              {
                "field": "min",
                "width": 100
              },
              {
                "field": "max",
                "width": 100
              },
              {
                "field": "comment",
                "maxWidth": 600
              }
            ]}
              rowHeaderSettings={{
              "width": 400
            }}
              with="cds/modifiers"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Underwriting Modifiers - Side A">
          <HX.Pane flow="right">
            <HX.Table data={[
              "cds/modifiers/management_corp_gov_factors_side_a",
              "cds/modifiers/business_financial_model_factors_side_a",
              "cds/modifiers/significant_event_factors_side_a",
              "cds/modifiers/stock_market_factors_side_a",
              "cds/modifiers/sca_adj_factors_side_a"
            ]}
              fields={[
              {
                "field": "value",
                "width": 100
              },
              {
                "field": "min",
                "width": 100
              },
              {
                "field": "max",
                "width": 100
              },
              {
                "field": "comment",
                "maxWidth": 600
              }
            ]}
              rowHeaderSettings={{
              "width": 400
            }}
              shownBy="cds/risk_information/public_flag"
              kb-interactive={true} />
            <HX.Table data={[
              "cds/modifiers/management_corp_gov_factors_side_a",
              "cds/modifiers/business_financial_model_factors_side_a",
              "cds/modifiers/significant_event_factors_side_a",
              "cds/modifiers/sca_adj_factors_side_a"
            ]}
              fields={[
              {
                "field": "value",
                "width": 100
              },
              {
                "field": "min",
                "width": 100
              },
              {
                "field": "max",
                "width": 100
              },
              {
                "field": "comment",
                "maxWidth": 600
              }
            ]}
              rowHeaderSettings={{
              "width": 400
            }}
              shownBy="cds/risk_information/private_flag"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table data={[
              "financial_stability_side_a_factors",
              "indemnification_side_a_factors",
              "total_factors_side_a"
            ]}
              fields={[
              {
                "field": "value",
                "width": 100
              },
              {
                "field": "min",
                "width": 100
              },
              {
                "field": "max",
                "width": 100
              },
              {
                "field": "comment",
                "maxWidth": 600
              }
            ]}
              rowHeaderSettings={{
              "width": 400
            }}
              with="cds/modifiers"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Side A Modification Commentary">
          <HX.Pane>
            <HX.Pane>
              <HX.Collection fields={[
                "suggested_factor",
                null,
                null,
                null,
                null,
                null
              ]}
                with="cds/modifiers"
                horizontal={true} />
            </HX.Pane>
            <HX.Pane>
              <HX.Notes field="cds/modifiers/suggested_factor_message"
                title="Message" />
              <HX.Notes field="cds/modifiers/suggested_factor_message_for_adj"
                title="Message for Adjustments" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/risk_information/not_mmp_flag">
        <HX.Section title="Risk Summary">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Table data={[
                {
                  "datum": "cds",
                  "width": 400
                }
              ]}
                fields={[
                "standard_fields/insured_name.read_only",
                {
                  "field": "currencies/source_currency.read_only"
                },
                {
                  "field": "exposure/aggregate/exposure_currency.read_only",
                  "shownBy": "cds/risk_information/private_flag"
                },
                {
                  "field": "exposure/aggregate/market_cap_2_year_high.read_only",
                  "shownBy": "cds/risk_information/public_flag"
                },
                {
                  "field": "exposure/aggregate/total_assets.read_only",
                  "shownBy": "cds/risk_information/private_flag"
                },
                "rating_factors/risk_information/industry_class_sic_code.read_only",
                "rating_factors/risk_information/ownership_type.read_only",
                "exposure/aggregate/us_listing_share.read_only",
                null,
                "rating_factors/risk_information/country_of_domicile.read_only",
                "rating_factors/risk_information/main_operating_country.read_only"
              ]}
                transpose={true}
                kb-interactive={true}
                rowHeaderSettings={{
                "width": 200
              }} />
            </HX.Pane>
            <HX.Pane>
              <HX.Pane>
                <HX.Table title="Side A"
                  data={[
                  "side_a_fifty_percentile",
                  "side_a_seventyfive_percentile"
                ]}
                  fields={[
                  {
                    "field": "inclusive_dismissals",
                    "width": 150
                  },
                  {
                    "field": "at_cost_only",
                    "width": 150
                  }
                ]}
                  rowHeaderSettings={{
                  "width": 150
                }}
                  with="cds/rating_summary"
                  kb-interactive={true}
                  syncColumnWidthsKey="SyncTable1" />
                <HX.Collection fields={[
                  "side_a_sca_freq"
                ]}
                  with="cds/rating_summary"
                  horizontal={true}
                  syncColumnWidthsKey="SyncTable1" />
              </HX.Pane>
              <HX.Pane>
                <HX.Table title="Side AB/ABC"
                  data={[
                  "side_abc_fifty_percentile",
                  "side_abc_seventyfive_percentile"
                ]}
                  fields={[
                  {
                    "field": "inclusive_dismissals",
                    "width": 150
                  },
                  {
                    "field": "at_cost_only",
                    "width": 150
                  }
                ]}
                  rowHeaderSettings={{
                  "width": 150
                }}
                  with="cds/rating_summary"
                  kb-interactive={true}
                  syncColumnWidthsKey="SyncTable1" />
                <HX.Collection fields={[
                  "side_abc_sca_freq"
                ]}
                  with="cds/rating_summary"
                  horizontal={true}
                  syncColumnWidthsKey="SyncTable1" />
              </HX.Pane>
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Layer Options">
          <HX.Table title="Programme Structure"
            data={[
            {
              "datum": "cds/large_cap/layers"
            }
          ]}
            fields={[
            {
              "field": "side_selection",
              "width": 150
            },
            {
              "field": "side_ab_discount",
              "width": 150
            },
            {
              "field": "uw_side_ab_discount_override",
              "infoBy": "cds/labels/uw_side_ab_discount_override_info",
              "width": 150
            },
            null,
            {
              "field": "limit",
              "width": 150
            },
            {
              "field": "excess",
              "width": 150
            },
            {
              "field": "deductible",
              "width": 150
            },
            null,
            {
              "field": "quoted_premium_100",
              "width": 150
            },
            {
              "field": "brokerage",
              "width": 150
            },
            null,
            {
              "field": "written_line",
              "infoBy": "cds/labels/beazley_market_share_info",
              "width": 150
            },
            {
              "field": "section_reference",
              "infoBy": "cds/labels/section_reference_info",
              "width": 150
            },
            {
              "field": "notes",
              "width": 150
            },
            {
              "field": "slip_leader",
              "shownBy": "/cds/validation/slip_leader/valid",
              "width": 150
            },
            {
              "field": "slip_leader.notSupported",
              "infoBy": "/cds/validation/slip_leader/info_text",
              "shownBy": "/cds/validation/slip_leader/invalid",
              "width": 150
            },
            {
              "field": "status",
              "width": 150
            },
            {
              "field": "cover_in_uw_authority",
              "width": 150
            },
            {
              "field": "signoff_obtained",
              "width": 150
            }
          ]}
            freezeLeft={0}
            syncColumnWidthsKey="TableSync"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Layer Results">
          <HX.Pane flow="right">
            <HX.Notes field="cds/labels/premium_and_costs_info" />
            <HX.Pane />
          </HX.Pane>
          <HX.Table title="Modelled Premium and Costs"
            data={[
            {
              "datum": "cds/large_cap/layers"
            }
          ]}
            fields={[
            "technical_premium",
            "technical_premium_pre_uw_adj",
            "benchmark_premium",
            null,
            "tpi",
            "tpi_pre_uw_adj",
            "bpi",
            null,
            "expected_loss_cost_att",
            "expected_loss_cost_cat",
            null,
            "adr_standalone",
            "contagion",
            "intl_standalone",
            "intl_large_company",
            "expected_loss_cost",
            "pflr",
            "roc"
          ]}
            freezeLeft={0}
            syncColumnWidthsKey="TableSync"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Premium Build-Up Graphs">
          <HX.Pane>
            <HX.Pane>
              <HX.Collection fields={[
                "cds/prem_build_up/selected_option",
                null
              ]}
                numCols={2} />
              <HX.CategoryChart data={[
                "technical_premium",
                "benchmark_premium",
                "bound_premium"
              ]}
                fields={[
                "gross_att_graph",
                "gross_cat_graph",
                "cost_ri_graph",
                "expenses_graph",
                "profit_load_graph",
                "brokerage_graph",
                "bound_premium_graph"
              ]}
                columnType="stack"
                title="Premium Build-Up"
                primaryAxis={{
                "label": "Premium Build-Up"
              }}
                with="cds/prem_build_up" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary MMP"
        fullWidth={true}
        shownBy="cds/risk_information/mmp_flag">
        <HX.Section title="Risk Summary">
          <HX.Pane flow="right">
            <HX.Table data={[
              {
                "datum": "cds",
                "width": 400
              }
            ]}
              fields={[
              "standard_fields/insured_name.read_only",
              {
                "field": "currencies/source_currency.read_only"
              },
              {
                "field": "exposure/aggregate/exposure_currency.read_only",
                "shownBy": "cds/risk_information/private_flag"
              },
              "exposure/aggregate/total_assets.read_only",
              "exposure/aggregate/row_ftes.read_only",
              null,
              "rating_factors/risk_information/country_of_domicile.read_only",
              "rating_factors/risk_information/main_operating_country.read_only"
            ]}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Pane>
              <HX.Notes field="cds/mmp/total/validation_note"
                title="Middle Market Private Notes" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Middle Market">
          <HX.Table title="Middle Market"
            data={[
            "dno",
            "epl",
            "cll",
            "total"
          ]}
            fields={[
            {
              "field": "coverage",
              "width": 150
            },
            {
              "field": "expiring_appetite_comment.read_only",
              "width": 150
            },
            {
              "field": "agg_aoc_limit",
              "width": 150
            },
            {
              "field": "appetite_comment",
              "width": 150
            },
            {
              "field": "limit",
              "width": 150
            },
            {
              "field": "excess",
              "width": 150
            },
            {
              "field": "deductible",
              "width": 150
            },
            null,
            {
              "field": "quoted_premium_100",
              "width": 150
            },
            {
              "field": "brokerage",
              "width": 150
            },
            {
              "field": "written_line",
              "width": 150
            },
            {
              "field": "technical_premium",
              "width": 150
            },
            {
              "field": "benchmark_premium",
              "width": 160
            },
            null,
            {
              "field": "status",
              "width": 150
            },
            {
              "field": "section_reference",
              "width": 150
            },
            {
              "field": "slip_leader",
              "shownBy": "/cds/validation/slip_leader/valid",
              "width": 150
            },
            {
              "field": "slip_leader.notSupported",
              "infoBy": "/cds/validation/slip_leader/info_text",
              "shownBy": "/cds/validation/slip_leader/invalid",
              "width": 150
            },
            {
              "field": "notes",
              "width": 150
            },
            null,
            {
              "field": "tpi",
              "width": 150
            },
            {
              "field": "bpi",
              "width": 150
            }
          ]}
            freezeLeft={0}
            with="cds/mmp"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Options Calculators - Agg Limit">
          <HX.Table title="D&O"
            data={[
            "cds/mmp/dno/option_1",
            "cds/mmp/dno/option_2",
            "cds/mmp/dno/option_3",
            "cds/mmp/dno/option_4"
          ]}
            fields={[
            {
              "field": "aggregate_limit"
            },
            {
              "field": "aggregate_excess"
            },
            {
              "field": "aggregate_deductible"
            },
            {
              "field": "technical_premium"
            }
          ]}
            transpose={true}
            kb-interactive={true} />
          <HX.Table title="EPL"
            data={[
            "cds/mmp/epl/option_1",
            "cds/mmp/epl/option_2",
            "cds/mmp/epl/option_3",
            "cds/mmp/epl/option_4"
          ]}
            fields={[
            {
              "field": "aggregate_limit"
            },
            {
              "field": "aggregate_excess"
            },
            {
              "field": "aggregate_deductible"
            },
            {
              "field": "technical_premium"
            }
          ]}
            transpose={true}
            kb-interactive={true} />
          <HX.Table title="CLL"
            data={[
            "cds/mmp/cll/option_1",
            "cds/mmp/cll/option_2",
            "cds/mmp/cll/option_3",
            "cds/mmp/cll/option_4"
          ]}
            fields={[
            {
              "field": "aggregate_limit"
            },
            {
              "field": "aggregate_excess"
            },
            {
              "field": "aggregate_deductible"
            },
            {
              "field": "technical_premium"
            }
          ]}
            transpose={true}
            kb-interactive={true} />
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
                "datum": "cds/large_cap/layers",
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status.read_only"
              }
            ]}
              kb-interactive={true}
              transpose={true}
              shownBy="cds/rate_change/show_layer_1" />
            <HX.Table title="Deal Status of Renewal"
              data={[
              {
                "datum": "cds/mmp/total",
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status.read_only"
              }
            ]}
              transpose={true}
              kb-interactive={true}
              shownBy="cds/risk_information/mmp_flag" />
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
          <HX.Section title="Rate Change Instructions and Key"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Notes field="cds/rate_change/instructions" />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Renewal Layer 1"
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal Layer 2"
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal Layer 3"
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal Layer 4"
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal Layer 5"
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal Layer 6"
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal Layer 7"
          shownBy="cds/rate_change/show_layer_7">
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal Layer 8"
          shownBy="cds/rate_change/show_layer_8">
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal Layer 9"
          shownBy="cds/rate_change/show_layer_9">
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal Layer 10"
          shownBy="cds/rate_change/show_layer_10">
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        <HX.Section title="Renewal MMP Total"
          shownBy="cds/risk_information/mmp_flag">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "total_assets",
                "insider_share",
                "mmp_flag",
                "number_employees",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
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
        viewScale={1}>
        <HX.Section title="1. Summary  of Programme Discussion with Broker"
          shownBy="cds/risk_information/not_mmp_flag">
          <CustomComponent textNode="cds/uw_rationale/broker_discussion" />
        </HX.Section>
        <HX.Section title="2. Wording and any Unusual Coverage"
          shownBy="cds/risk_information/not_mmp_flag">
          <CustomComponent textNode="cds/uw_rationale/unusual_coverage" />
        </HX.Section>
        <HX.Section title="3. Any Other Factors not Captured Elsewhere"
          shownBy="cds/risk_information/not_mmp_flag">
          <CustomComponent textNode="cds/uw_rationale/other_factors" />
        </HX.Section>
        <HX.Section title="4. ESG">
          <HX.Notes field="cds/uw_rationale/esg_info" />
          <CustomComponent textNode="cds/uw_rationale/esg" />
        </HX.Section>
        <HX.Section title="5. I am Writing this Because (including comments on BPI)">
          <HX.Notes field="cds/uw_rationale/bpi_comment_info" />
          <CustomComponent textNode="cds/uw_rationale/bpi_comment" />
        </HX.Section>
        <HX.Section title="File Uploads">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.File field="cds/uw_rationale/file_upload_1" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/uw_rationale/file_upload_2" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/uw_rationale/file_upload_3" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/uw_rationale/file_upload_4" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/uw_rationale/file_upload_5" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Download Rationale">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Button task="generate_uw_rationale_doc_task"
                title="Generate UW Rationale Document" />
              <HX.File field="cds/uw_rationale/file_download_1" />
            </HX.Pane>
            <HX.Pane />
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
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary Layer 2"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
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
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary Layer 3"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
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
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary Layer 4"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
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
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary Layer 5"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
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
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary Layer 6"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
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
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary Layer 7"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_7">
          <HX.With context={{
            "index": 6,
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
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary Layer 8"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_8">
          <HX.With context={{
            "index": 7,
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
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary Layer 9"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_9">
          <HX.With context={{
            "index": 8,
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
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary Layer 10"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_10">
          <HX.With context={{
            "index": 9,
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
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100"
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
        <HX.Section title="Summary MMP Total"
          shownBy="cds/risk_information/mmp_flag">
          <HX.Collection title="Risk Details"
            numCols={4}
            fields={[
            "cds/mmp/total/status.read_only",
            "cds/mmp/total/section_reference.read_only",
            "cds/mmp/total/brokerage",
            "cds/mmp/total/written_line"
          ]} />
          <HX.Collection title="Pricing"
            numCols={2}
            fields={[
            {
              "field": "cds/mmp/total/quoted_premium_100"
            },
            null,
            "cds/mmp/total/technical_premium",
            "cds/mmp/total/benchmark_premium",
            "cds/mmp/total/tpi",
            "cds/mmp/total/bpi"
          ]} />
          <HX.Collection title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_rater_priced"
            numCols={3}
            fields={[
            "cds/mmp/total/pflr",
            null,
            null
          ]} />
          <HX.Collection title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_case_priced"
            numCols={3}
            fields={[
            "cds/mmp/total/pflr",
            null,
            null
          ]} />
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
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
      <HX.Page title="Climate Litigation"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Climate Litigation Heatmap - Dashboard">
          <HX.Pane flow="right">
            <HX.Pane ratio={1} />
            <CustomComponent src="https://app.powerbi.com/reportEmbed?reportId=61c3c19e-fd8e-40ec-b41a-58600b833fff&appId=4b854f37-b63a-418b-904a-b507574e6797&autoAuth=true&ctid=9a50eba8-7568-447a-bcb9-27a0d464aa80"
              height="700" />
            <HX.Pane ratio={1} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Download Document">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={[
                "cds/risk_information/climate_document_country",
                {
                  "field": "cds/risk_information/climate_document_industry",
                  "infoBy": "cds/risk_information/climate_document_industry_infoby"
                }
              ]}
                horizontal={true} />
              <HX.Button task="generate_climate_doc_task"
                title="Generate Climate Litigation Spotlight Report" />
              <HX.File field="cds/risk_information/climate_document" />
            </HX.Pane>
            <HX.Pane />
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