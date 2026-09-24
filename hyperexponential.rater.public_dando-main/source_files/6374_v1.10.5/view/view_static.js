
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root keyFields={[
      {
        "field": "cds/technical_premium_1",
        "shownBy": "cds/show_tech_prem_1"
      },
      {
        "field": "cds/technical_premium_2",
        "shownBy": "cds/show_tech_prem_2"
      },
      {
        "field": "cds/technical_premium_3",
        "shownBy": "cds/show_tech_prem_3"
      },
      {
        "field": "cds/technical_premium_4",
        "shownBy": "cds/show_tech_prem_4"
      },
      {
        "field": "cds/technical_premium_5",
        "shownBy": "cds/show_tech_prem_5"
      },
      {
        "field": "cds/technical_premium_6",
        "shownBy": "cds/show_tech_prem_6"
      },
      {
        "field": "cds/admitted/bici/final_premium",
        "shownBy": "cds/admitted/is_bici"
      },
      {
        "field": "cds/admitted/baic/final_premium",
        "shownBy": "cds/admitted/is_baic"
      },
      {
        "field": "cds/admitted_excess/adm_exc_model_prem/value",
        "shownBy": "cds/admitted_excess/conditions_met"
      },
      {
        "field": "cds/admitted/quoted_premium",
        "shownBy": "cds/admitted/is_admitted"
      }
    ]}>
      <HX.Page title="Landing Page"
        shownBy="model_state/show_landing_page">
        <HX.Section title="Start Policy">
          <HX.Collection fields={[
            "cds/capiq_wb_id"
          ]} />
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Button task="populate_capiq_data_from_wb_task"
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
              "underwriter",
              "benchmark_class"
            ]}
              with="cds/standard_fields"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/insured_name"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/policy_reference",
              "cds/currencies/source_currency",
              "cds/standard_fields/is_renewal",
              "cds/is_runoff"
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
          <HX.Collection fields={[
            "cds/rw_broker",
            null
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_methodology"
            ]} />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage">
          <HX.Collection fields={[
            "cds/coverage",
            "cds/coverage_details"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="S&P CapIQ Search"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/company_search",
              "cds/capiq_search",
              null
            ]}
              numCols={3} />
            <HX.Button task="capiq_fetch_task"
              title="Search CapIQ" />
            <HX.Table data={[
              {
                "datum": "cds/capiq"
              }
            ]}
              fields={[
              "selection",
              "company_name",
              "exchange",
              "market_cap",
              "date_updated"
            ]}
              kb-interactive={true} />
            <HX.Collection fields={[
              "cds/capiq_results"
            ]} />
          </HX.Pane>
          <HX.Pane shownBy="cds/capiq_search_complete">
            <HX.Button task="populate_capiq_data_task"
              title="Populate Rater" />
            <HX.Collection fields={[
              "cds/capiq_populate"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Company Details">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "company_name",
              {
                "field": "ticker",
                "shownBy": "/cds/review_type/rater_priced"
              },
              "company_country",
              "company_state",
              "exposure/aggregate/total_assets",
              "exposure/aggregate/year_founded"
            ]}
              with="cds" />
            <HX.Pane flow="down">
              <HX.Collection fields={[
                "incorporated_state",
                "hq_state",
                "hq_city",
                "airport_city",
                "pipeline_premium",
                "exposure/aggregate/crypto_classification"
              ]}
                with="cds" />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="down">
            <CustomComponent textNode="cds/company_description"
              placeholderText="Enter company description here ..." />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Market Cap & IPO"
          shownBy="/cds/review_type/rater_priced">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection fields={[
                {
                  "field": "exposure/aggregate/market_cap",
                  "infoBy": "exposure/aggregate/market_cap_info",
                  "shownBy": "market_cap_complete"
                },
                {
                  "field": "exposure/aggregate/market_cap.mandatory",
                  "shownBy": "market_cap_mandatory"
                },
                {
                  "field": "exposure/aggregate/insider_share",
                  "infoBy": "exposure/aggregate/insider_share_info"
                },
                "exposure/aggregate/revised_market_cap"
              ]}
                with="cds" />
              <CustomComponent notesPath="cds/exposure/aggregate/revised_market_cap_comment"
                label="Market Cap Comment"
                printButton={true}
                autosave={true} />
            </HX.Pane>
            <HX.Pane flow="down">
              <HX.Collection fields={[
                "exposure/aggregate/transaction_type",
                "exposure/aggregate/ipo_date",
                "exposure/aggregate/ignore_ipo"
              ]}
                with="cds" />
              <CustomComponent notesPath="cds/exposure/aggregate/ipo_date_comment"
                label="IPO Comment"
                marginTop="75px"
                printButton={true}
                autosave={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Sector">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection fields={[
                {
                  "field": "key_industry/code_name",
                  "shownBy": "key_industry/sic_complete"
                },
                {
                  "field": "key_industry/code_name.mandatory",
                  "shownBy": "key_industry/sic_mandatory"
                },
                {
                  "field": "key_industry/sector_name",
                  "shownBy": "sector_complete"
                },
                {
                  "field": "key_industry/sector_name.mandatory",
                  "shownBy": "sector_mandatory"
                },
                "key_industry/code"
              ]}
                with="cds" />
              <HX.Collection fields={[
                "key_industry/blended_sic"
              ]}
                with="cds" />
            </HX.Pane>
            <HX.Pane flow="down">
              <HX.Collection fields={[
                "key_industry/sic_percentage",
                "key_industry/sector_unity_frequency",
                "key_industry/sector_uw_override"
              ]}
                with="cds" />
              <CustomComponent notesPath="cds/key_industry/sector_uw_override_comment"
                label="Underwriter Override Comment"
                marginTop="30px"
                autosave={true} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Notes title="Sector Message"
              field="cds/key_industry/sector_message" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane flow="down"
              shownBy="cds/key_industry/blended_sic">
              <HX.Collection fields={[
                "sic_description_2",
                {
                  "field": "sector_2",
                  "infoBy": "sector_message_2"
                },
                "sic_code_2",
                "sic_percentage_2",
                "sector_unity_frequency_2",
                "sector_uw_override_2"
              ]}
                with="cds/key_industry" />
              <CustomComponent notesPath="cds/key_industry/sector_uw_override_comment_2"
                label="Underwriter Override Comment 2"
                marginTop="30px" />
            </HX.Pane>
            <HX.Pane flow="down"
              shownBy="cds/key_industry/blended_sic">
              <HX.Collection fields={[
                "sic_description_3",
                {
                  "field": "sector_3",
                  "infoBy": "sector_message_3"
                },
                "sic_code_3",
                "sic_percentage_3",
                "sector_unity_frequency_3",
                "sector_uw_override_3"
              ]}
                with="cds/key_industry" />
              <CustomComponent notesPath="cds/key_industry/sector_uw_override_comment_3"
                label="Underwriter Override Comment 3"
                marginTop="30px" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Admitted Info"
          shownBy="cds/admitted/conditions_met">
          <HX.Collection fields={[
            "cds/standard_fields/is_admitted_or_surplus",
            null
          ]}
            numCols={2} />
          <HX.Collection fields={[
            "cds/admitted/insurer",
            "cds/admitted_excess/is_primary_excess"
          ]}
            numCols={2} />
        </HX.Section>
        <HX.Section title="Credit Rating"
          shownBy="cds/is_side_a">
          <HX.Collection fields={[
            "credit_rating",
            "credit_rating_estimated",
            "credit_rating_override"
          ]}
            numCols={3}
            with="cds/exposure/aggregate" />
        </HX.Section>
        <HX.Section title="Company Financials"
          shownBy="/cds/review_type/rater_priced">
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
        <HX.Section title="Company Financials"
          shownBy="/cds/review_type/private_priced">
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
      </HX.Page>
      <HX.Page title="Runoff Pricing"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/is_runoff">
        <HX.Section title="Runoff Adjustment">
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="sync_layers"
              data={[
              {
                "datum": "cds/layers",
                "maxWidth": 250,
                "minWidth": 175
              }
            ]}
              fields={[
              "coverages/side_a/premium",
              "runoff_adjustment",
              "runoff_original_premium"
            ]}
              rowHeaderSettings={{
              "width": 250
            }}
              transpose={true}
              shownBy="cds/is_side_a"
              kb-interactive={true} />
            <HX.Table syncColumnWidthsKey="sync_layers"
              data={[
              {
                "datum": "cds/layers",
                "maxWidth": 250,
                "minWidth": 175
              }
            ]}
              fields={[
              "coverages/abc/premium",
              "runoff_adjustment",
              "runoff_original_premium"
            ]}
              rowHeaderSettings={{
              "width": 250
            }}
              transpose={true}
              shownBy="cds/is_abc"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Pricing"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Modifiers"
          shownBy="/cds/review_type/rater_priced">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Table syncColumnWidthsKey="sync_modifiers"
                data={[
                {
                  "datum": "management_corp_gov",
                  "labelBy": "/non_cds/modifier_labels/management_corp_gov"
                },
                {
                  "datum": "business_financial_model_factors",
                  "labelBy": "/non_cds/modifier_labels/business_financial_model_factors"
                },
                {
                  "datum": "significant_event_factors",
                  "labelBy": "/non_cds/modifier_labels/significant_event_factors"
                },
                {
                  "datum": "stock_market_factors",
                  "labelBy": "/non_cds/modifier_labels/stock_market_factors"
                },
                {
                  "datum": "regulatory",
                  "labelBy": "/non_cds/modifier_labels/regulatory"
                },
                null,
                "freq_adj_factor",
                null,
                {
                  "datum": "obj_freq_adj_factor",
                  "infoBy": "obj_freq_adj_factor/info"
                },
                null,
                "total_freq_adj_factor"
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
                  "field": "comment_plain_text",
                  "width": 200
                }
              ]}
                rowHeaderSettings={{
                "width": 350
              }}
                with="cds/modifiers"
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="down">
              <CustomComponent notesPath="cds/modifiers/management_corp_gov/comment"
                plainTextPath="cds/modifiers/management_corp_gov/comment_plain_text"
                label="Management and Corporate Governance Comment"
                width="400px"
                marginTop="55px"
                marginBottom="4px"
                autosave={true} />
              <CustomComponent notesPath="cds/modifiers/business_financial_model_factors/comment"
                plainTextPath="cds/modifiers/business_financial_model_factors/comment_plain_text"
                label="Business / Financial Model Factors Comment"
                width="400px"
                marginTop="4px"
                marginBottom="4px"
                autosave={true} />
              <CustomComponent notesPath="cds/modifiers/significant_event_factors/comment"
                plainTextPath="cds/modifiers/significant_event_factors/comment_plain_text"
                label="Significant Event Factors Comment"
                width="400px"
                marginTop="4px"
                marginBottom="4px"
                autosave={true} />
              <CustomComponent notesPath="cds/modifiers/stock_market_factors/comment"
                plainTextPath="cds/modifiers/stock_market_factors/comment_plain_text"
                label="Stock Market Factors Comment"
                width="400px"
                marginTop="4px"
                marginBottom="4px"
                autosave={true} />
              <CustomComponent notesPath="cds/modifiers/regulatory/comment"
                plainTextPath="cds/modifiers/regulatory/comment_plain_text"
                label="Regulatory Comment"
                width="400px"
                marginTop="4px"
                marginBottom="4px"
                autosave={true} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane>
            <HX.Collection syncColumnWidthsKey="sync_modifiers"
              fields={[
              "sca_model_freq",
              "sca_freq_override",
              "sca_used_freq"
            ]}
              with="cds/frequency" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Table syncColumnWidthsKey="sync_modifiers"
                data={[
                {
                  "datum": "derivative",
                  "labelBy": "/non_cds/modifier_labels/derivative"
                },
                {
                  "datum": "ma",
                  "infoBy": "ma/info"
                }
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
                  "field": "comment_plain_text",
                  "width": 120
                }
              ]}
                with="cds/modifiers"
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane>
              <CustomComponent notesPath="cds/modifiers/derivative/comment"
                plainTextPath="cds/modifiers/derivative/comment_plain_text"
                label="Derivative Comment"
                width="400px"
                marginTop="55px"
                marginBottom="4px"
                autosave={true} />
              <CustomComponent notesPath="cds/modifiers/ma/comment"
                plainTextPath="cds/modifiers/ma/comment_plain_text"
                label="M&A Comment"
                width="400px"
                marginTop="4px"
                marginBottom="4px"
                autosave={true} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane>
            <HX.Collection syncColumnWidthsKey="sync_modifiers"
              fields={[
              "d_used_freq",
              "ma_used_freq",
              "total_freq"
            ]}
              with="cds/frequency" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage">
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="sync_layers"
              data={[
              {
                "datum": "cds/layers",
                "maxWidth": 250,
                "minWidth": 175
              }
            ]}
              fields={[
              "status"
            ]}
              rowHeaderSettings={{
              "width": 250
            }}
              transpose={true}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="sync_layers"
              data={[
              {
                "datum": "cds/layers",
                "maxWidth": 250,
                "minWidth": 175
              }
            ]}
              fields={[
              "coverages/abc/limit",
              "coverages/abc/excess",
              "coverages/abc/deductible",
              "coverages/abc/ma_retention",
              null,
              "coverages/abc/premium",
              "coverages/abc/written_line",
              "coverages/abc/quoted_market_share",
              "coverages/abc/brokerage",
              null,
              {
                "field": "coverages/abc/benchmark_premium",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/abc/elr",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/abc/bpi",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/abc/technical_premium",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/abc/tpi",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/abc/roc",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/abc/private_priced/benchmark_premium",
                "shownBy": "/cds/review_type/private_priced"
              },
              {
                "field": "coverages/abc/private_priced/bpi",
                "shownBy": "/cds/review_type/private_priced"
              },
              {
                "field": "coverages/abc/private_priced/technical_premium",
                "shownBy": "/cds/review_type/private_priced"
              },
              {
                "field": "coverages/abc/private_priced/tpi",
                "shownBy": "/cds/review_type/private_priced"
              },
              null,
              {
                "field": "coverages/abc/at_cost_75",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/abc/incl_dimissals_75",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/review_type/rater_priced"
              },
              "coverages/abc/selected"
            ]}
              title="Options"
              rowHeaderSettings={{
              "width": 250
            }}
              transpose={true}
              shownBy="cds/is_abc"
              kb-interactive={true} />
            <HX.Table syncColumnWidthsKey="sync_layers"
              data={[
              {
                "datum": "cds/layers",
                "maxWidth": 250,
                "minWidth": 175
              }
            ]}
              fields={[
              "coverages/side_a/limit",
              "coverages/side_a/excess",
              "coverages/side_a/tower",
              "coverages/side_a/total_excess",
              "coverages/side_a/deductible",
              "coverages/side_a/director_limit",
              null,
              "coverages/side_a/premium",
              "coverages/side_a/written_line",
              "coverages/side_a/quoted_market_share",
              "coverages/side_a/brokerage",
              "coverages/side_a/non_rescindable_coverage",
              null,
              {
                "field": "coverages/side_a/benchmark_premium",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/side_a/elr",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/side_a/bpi",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/side_a/technical_premium",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/side_a/tpi",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/side_a/roc",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/side_a/private_priced/benchmark_premium",
                "shownBy": "/cds/review_type/private_priced"
              },
              {
                "field": "coverages/side_a/private_priced/bpi",
                "shownBy": "/cds/review_type/private_priced"
              },
              {
                "field": "coverages/side_a/private_priced/technical_premium",
                "shownBy": "/cds/review_type/private_priced"
              },
              {
                "field": "coverages/side_a/private_priced/tpi",
                "shownBy": "/cds/review_type/private_priced"
              },
              null,
              {
                "field": "coverages/side_a/at_cost_75",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": "coverages/side_a/incl_dimissals_75",
                "shownBy": "/cds/review_type/rater_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/review_type/rater_priced"
              },
              "coverages/side_a/selected"
            ]}
              title="Options"
              rowHeaderSettings={{
              "width": 250
            }}
              transpose={true}
              shownBy="cds/is_side_a"
              kb-interactive={true} />
            <HX.Pane flow="right">
              <HX.Button task="generate_tags_cuap"
                title="Save Tags" />
              <HX.Collection fields={[
                null
              ]} />
              <HX.Collection fields={[
                null
              ]} />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "cds/policy_tag_error"
              ]}
                shownBy="cds/is_policy_tag_error"
                horizontal={true} />
              <HX.Collection fields={[
                null
              ]} />
              <HX.Collection fields={[
                null
              ]} />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
            <HX.Collection syncColumnWidthsKey="sync_layers"
              fields={[
              "cds/entity_investigation"
            ]} />
            <HX.Table syncColumnWidthsKey="sync_layers"
              data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "ei_limit",
              "ei_price"
            ]}
              transpose={true}
              shownBy="cds/entity_investigation"
              kb-interactive={true} />
            <HX.Collection syncColumnWidthsKey="sync_layers"
              fields={[
              "cds/bridge_countries"
            ]} />
            <HX.Table data={[
              {
                "datum": "cds/bridge_country"
              }
            ]}
              fields={[
              {
                "field": "country",
                "width": 200
              },
              {
                "field": "premium",
                "width": 200
              }
            ]}
              shownBy="cds/bridge_countries"
              kb-interactive={true} />
            <HX.Collection syncColumnWidthsKey="sync_layers"
              fields={[
              "cds/bridge_premium",
              "cds/bridge_comment"
            ]}
              shownBy="cds/bridge_countries" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Admitted"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/admitted/is_admitted">
        <HX.Section title="Select Option">
          <HX.Collection syncColumnWidthsKey="sync_admitted"
            fields={[
            "cds/admitted/selected_option"
          ]} />
        </HX.Section>
        <HX.Section title="Company Info">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "company",
              "total_assets",
              "state",
              "limit",
              "inception_date",
              "excess",
              null,
              "deductible"
            ]}
              with="cds/admitted"
              numCols={2} />
            <HX.Collection fields={[
              null
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Admitted Modifiers"
          shownBy="cds/admitted/is_bici">
          <HX.Pane flow="right">
            <HX.Button task="set_admitted_to_min_task"
              title="Set to Inputs to Minimum" />
            <HX.Button task="set_admitted_to_midpoint_task"
              title="Set to Inputs to Midpoint" />
            <HX.Button task="set_admitted_to_max_task"
              title="Set to Inputs to Maximum" />
            <HX.Button task="reset_admitted_reasons_task"
              title="Reset Reasons" />
          </HX.Pane>
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="sync_admitted"
              data={[
              {
                "datum": "step_1_bpm",
                "infoBy": "step_1_bpm/message"
              },
              {
                "datum": "step_2_im",
                "infoBy": "step_2_im/message"
              },
              {
                "datum": "step_3_mam",
                "infoBy": "step_3_mam/message"
              },
              {
                "datum": "step_4_pm",
                "infoBy": "step_4_pm/message"
              },
              {
                "datum": "step_5_qm",
                "infoBy": "step_5_qm/message"
              },
              {
                "datum": "step_6_cm",
                "infoBy": "step_6_cm/message"
              },
              {
                "datum": "step_7_fm",
                "infoBy": "step_7_fm/message"
              },
              {
                "datum": "step_8_em",
                "infoBy": "step_8_em/message"
              },
              {
                "datum": "step_9_om",
                "infoBy": "step_9_om/message"
              },
              {
                "datum": "step_10_lm",
                "infoBy": "step_10_lm/message"
              },
              {
                "datum": "step_11_chm",
                "infoBy": "step_11_chm/message"
              },
              {
                "datum": "step_12_sm",
                "infoBy": "step_12_sm/message"
              },
              {
                "datum": "step_13_edm",
                "infoBy": "step_13_edm/message"
              },
              {
                "datum": "step_14_spm",
                "infoBy": "step_14_spm/message"
              },
              {
                "datum": "step_15_rm",
                "infoBy": "step_15_rm/message"
              },
              {
                "datum": "step_16_pcm",
                "infoBy": "step_16_pcm/message"
              },
              {
                "datum": "step_17_icm",
                "infoBy": "step_17_icm/message"
              },
              {
                "datum": "step_18_llm",
                "infoBy": "step_18_llm/message"
              }
            ]}
              with="cds/admitted/bici"
              fields={[
              {
                "field": "selected",
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
                "field": "reason",
                "minWidth": 700
              }
            ]}
              rowHeaderSettings={{
              "width": 300
            }}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table shownBy="cds/admitted/bici/show_final_prem_factor"
              syncColumnWidthsKey="sync_admitted"
              data={[
              "cds/admitted/bici/step_18a_fcp"
            ]}
              fields={[
              {
                "field": "selected",
                "width": 100
              },
              {
                "field": "min",
                "width": 100
              },
              {
                "field": "max",
                "width": 100
              }
            ]}
              rowHeaderSettings={{
              "width": 300
            }}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Premium Info"
          shownBy="cds/admitted/is_bici">
          <HX.Collection fields={[
            "final_premium",
            null,
            "rounding_message",
            null,
            "rounded_premium",
            null
          ]}
            with="cds/admitted/bici"
            numCols={2} />
        </HX.Section>
        <HX.Section title="Admitted Modifiers"
          shownBy="cds/admitted/is_baic">
          <HX.Pane flow="right">
            <HX.Button task="set_admitted_to_min_task"
              title="Set to Inputs to Minimum" />
            <HX.Button task="set_admitted_to_midpoint_task"
              title="Set to Inputs to Midpoint" />
            <HX.Button task="set_admitted_to_max_task"
              title="Set to Inputs to Maximum" />
            <HX.Button task="reset_admitted_reasons_task"
              title="Reset Reasons" />
          </HX.Pane>
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="sync_admitted"
              data={[
              {
                "datum": "step_1_bpm",
                "infoBy": "step_1_bpm/message"
              },
              {
                "datum": "step_2_im",
                "infoBy": "step_2_im/message"
              },
              {
                "datum": "step_3_mam",
                "infoBy": "step_3_mam/message"
              },
              {
                "datum": "step_4_pm",
                "infoBy": "step_4_pm/message"
              },
              {
                "datum": "step_5_qm",
                "infoBy": "step_5_qm/message"
              },
              {
                "datum": "step_6_cm",
                "infoBy": "step_6_cm/message"
              },
              {
                "datum": "step_7_fm",
                "infoBy": "step_7_fm/message"
              },
              {
                "datum": "step_8_em",
                "infoBy": "step_8_em/message"
              },
              {
                "datum": "step_9_om",
                "infoBy": "step_9_om/message"
              },
              {
                "datum": "step_10_lm",
                "infoBy": "step_10_lm/message"
              },
              {
                "datum": "step_11_chm",
                "infoBy": "step_11_chm/message"
              },
              {
                "datum": "step_12_sm",
                "infoBy": "step_12_sm/message"
              },
              {
                "datum": "step_13_edm",
                "infoBy": "step_13_edm/message"
              },
              {
                "datum": "step_14_spm",
                "infoBy": "step_14_spm/message"
              },
              {
                "datum": "step_15_clrm",
                "infoBy": "step_15_clrm/message"
              },
              {
                "datum": "step_16_pcm",
                "infoBy": "step_16_pcm/message"
              },
              {
                "datum": "step_17_icm",
                "infoBy": "step_17_icm/message"
              },
              {
                "datum": "step_18_yo",
                "infoBy": "step_18_yo/message"
              },
              {
                "datum": "step_19_saf",
                "infoBy": "step_19_saf/message"
              }
            ]}
              fields={[
              {
                "field": "selected",
                "width": 120
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
                "field": "reason",
                "minWidth": 500
              }
            ]}
              with="cds/admitted/baic"
              rowHeaderSettings={{
              "width": 300
            }}
              shownBy="is_california_not"
              kb-interactive={true} />
            <HX.Table syncColumnWidthsKey="sync_admitted"
              data={[
              {
                "datum": "step_1_bpm",
                "infoBy": "step_1_bpm/message"
              },
              {
                "datum": "step_2_im",
                "infoBy": "step_2_im/message"
              },
              {
                "datum": "step_3_mam",
                "infoBy": "step_3_mam/message"
              },
              {
                "datum": "step_4_pm",
                "infoBy": "step_4_pm/message"
              },
              {
                "datum": "step_5_qm",
                "infoBy": "step_5_qm/message"
              },
              {
                "datum": "step_6_cm",
                "infoBy": "step_6_cm/message"
              },
              {
                "datum": "step_7_fm",
                "infoBy": "step_7_fm/message"
              },
              {
                "datum": "step_8_em",
                "infoBy": "step_8_em/message"
              },
              {
                "datum": "step_9_om",
                "infoBy": "step_9_om/message"
              },
              {
                "datum": "step_10_lm",
                "infoBy": "step_10_lm/message"
              },
              {
                "datum": "step_11_chm",
                "infoBy": "step_11_chm/message"
              },
              {
                "datum": "step_12_sm",
                "infoBy": "step_12_sm/message"
              },
              {
                "datum": "step_13_edm",
                "infoBy": "step_13_edm/message"
              },
              {
                "datum": "step_14_spm",
                "infoBy": "step_14_spm/message"
              },
              {
                "datum": "step_15_clrm",
                "infoBy": "step_15_clrm/message"
              },
              {
                "datum": "step_16_pcm",
                "infoBy": "step_16_pcm/message"
              },
              {
                "datum": "step_17_icm",
                "infoBy": "step_17_icm/message"
              },
              {
                "datum": "step_18_yo_ca",
                "infoBy": "step_18_yo_ca/message"
              },
              {
                "datum": "step_19_saf",
                "infoBy": "step_19_saf/message"
              },
              {
                "datum": "step_20a_fwic"
              },
              {
                "datum": "step_20b_iglp"
              },
              {
                "datum": "step_20c_rii"
              },
              {
                "datum": "step_20d_str"
              },
              {
                "datum": "step_20e_mcd"
              },
              {
                "datum": "step_20f_lre"
              },
              {
                "datum": "step_20_srf"
              }
            ]}
              fields={[
              {
                "field": "selected",
                "width": 120
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
                "field": "reason",
                "minWidth": 500
              }
            ]}
              with="cds/admitted/baic"
              rowHeaderSettings={{
              "width": 300
            }}
              shownBy="is_california"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table shownBy="cds/admitted/baic/show_final_prem_factor"
              syncColumnWidthsKey="sync_admitted"
              data={[
              "cds/admitted/baic/step_19a_fcp"
            ]}
              fields={[
              {
                "field": "selected",
                "width": 120
              },
              {
                "field": "min",
                "width": 100
              },
              {
                "field": "max",
                "width": 100
              }
            ]}
              rowHeaderSettings={{
              "width": 300
            }}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Premium Info"
          shownBy="cds/admitted/is_baic">
          <HX.Collection fields={[
            "final_premium",
            null,
            "rounding_message",
            null,
            "rounded_premium",
            null
          ]}
            with="cds/admitted/baic"
            numCols={2} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Admitted Excess"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/admitted_excess/conditions_met">
        <HX.Section title="Layer Information">
          <HX.Pane flow="right">
            <HX.Table data={[
              "exc_prim_limit",
              "exc_prim_retention",
              "exc_prim_premium",
              "exc_excess_limit",
              "exc_excess_attach",
              "exc_no_policies"
            ]}
              with="cds/admitted_excess"
              fields={[
              {
                "field": "value",
                "width": 150
              }
            ]}
              title=""
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Admitted Rating">
          <HX.Pane flow="right">
            <HX.Table data={[
              "exc_prim_rate_ade",
              "exc_large_loss",
              "exc_ind_risk_level",
              "exc_ind_sec_factor",
              "exc_comp_spe_risk_level",
              "exc_comp_spe_factor",
              "exc_liti_potential_risk_level",
              "exc_liti_potential_factor",
              "exc_fl_schedule_rating_factor",
              "adm_exc_model_prem",
              "adm_exc_max_round_down",
              "adm_exc_max_round_up",
              "adm_exc_round_prem"
            ]}
              with="cds/admitted_excess"
              fields={[
              {
                "field": "value",
                "width": 150
              },
              {
                "field": "min",
                "width": 150
              },
              {
                "field": "max",
                "width": 150
              }
            ]}
              title=""
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="TPI Calculations"
        fullWidth={true}
        viewScale={1}
        shownBy="/cds/review_type/rater_priced">
        <HX.Section title="Select Option"
          shownBy="model_state/show_after_landing_page">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/tpi_calculations/selected_option"
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="SCA Frequency">
          <HX.Table syncColumnWidthsKey="sync_calcs1"
            title="Risk Information"
            data={[
            "sca_base_frequency",
            "market_cap_factor",
            "ipo_factor"
          ]}
            fields={[
            {
              "field": "value",
              "width": 150
            },
            {
              "field": "book_average",
              "width": 150
            },
            {
              "field": "comment",
              "width": 600
            }
          ]}
            rowHeaderSettings={{
            "width": 400
          }}
            with="cds/tpi_calculations" />
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="sync_calcs1"
              title="CapIQ"
              data={[
              "minimum_trading_volume_factor",
              "volatility_of_trading_factor",
              "execs_under_age_50_factor",
              "years_in_business_factor",
              null,
              {
                "datum": "capiq_total_factor",
                "infoBy": "capiq_total_factor/info"
              },
              null,
              "freq_sca_after_capiq"
            ]}
              fields={[
              {
                "field": "value"
              },
              {
                "field": "book_average"
              }
            ]}
              with="cds/tpi_calculations" />
          </HX.Pane>
          <HX.Table syncColumnWidthsKey="sync_calcs1"
            title="Modifiers & Overrides"
            data={[
            "freq_sca_after_overrides",
            "freq_sca_after_modifiers"
          ]}
            fields={[
            {
              "field": "value"
            },
            {
              "field": "book_average"
            },
            {
              "field": "comment"
            }
          ]}
            with="cds/tpi_calculations" />
        </HX.Section>
        <HX.Section title="SCA Severity">
          <HX.Table syncColumnWidthsKey="sync_calcs2"
            data={[
            "ground_up_sca_dismissal",
            "sca_loss_to_layer"
          ]}
            fields={[
            {
              "field": "value",
              "width": 150
            },
            {
              "field": "comment",
              "width": 750
            }
          ]}
            rowHeaderSettings={{
            "width": 400
          }}
            with="cds/tpi_calculations" />
        </HX.Section>
        <HX.Section title="Technical Premium">
          <HX.Table syncColumnWidthsKey="sync_calcs2"
            title="Dismissal Rate"
            data={[
            "sca_dismissal_rate"
          ]}
            fields={[
            {
              "field": "value"
            },
            {
              "field": "comment"
            }
          ]}
            with="cds/tpi_calculations" />
          <HX.Table shownBy="is_abc"
            syncColumnWidthsKey="sync_calcs2"
            title="Loss Cost"
            data={[
            {
              "datum": "sca_loss_cost",
              "infoBy": "sca_loss_cost/info"
            },
            "non_sca_loss_cost",
            "cat_load",
            null,
            {
              "datum": "abc_loss_cost",
              "infoBy": "abc_loss_cost/info"
            }
          ]}
            fields={[
            {
              "field": "value"
            },
            {
              "field": "comment"
            }
          ]}
            with="cds/tpi_calculations" />
          <HX.Table shownBy="is_side_a"
            syncColumnWidthsKey="sync_calcs2"
            title="Loss Cost"
            data={[
            {
              "datum": "sca_loss_cost",
              "infoBy": "sca_loss_cost/info"
            },
            "non_sca_loss_cost",
            "cat_load"
          ]}
            fields={[
            {
              "field": "value"
            }
          ]}
            with="cds/tpi_calculations" />
          <HX.Table shownBy="is_side_a"
            syncColumnWidthsKey="sync_calcs1"
            title="Side A Factors"
            data={[
            "dic_adjustment",
            "bankruptcy_load"
          ]}
            fields={[
            {
              "field": "value"
            },
            {
              "field": "book_average"
            }
          ]}
            with="cds/tpi_calculations" />
          <HX.Table shownBy="is_side_a"
            syncColumnWidthsKey="sync_calcs2"
            title="Total Loss Cost"
            data={[
            {
              "datum": "side_a_loss_cost",
              "infoBy": "side_a_loss_cost/info"
            }
          ]}
            fields={[
            {
              "field": "value"
            },
            {
              "field": "comment"
            }
          ]}
            with="cds/tpi_calculations" />
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="sync_calcs2"
              title="TPI"
              data={[
              "net_premium",
              {
                "datum": "profit",
                "infoBy": "profit/info"
              },
              {
                "datum": "roc",
                "infoBy": "roc/info"
              },
              {
                "datum": "technical_premium",
                "infoBy": "technical_premium/info"
              },
              {
                "datum": "tpi",
                "infoBy": "tpi/info"
              }
            ]}
              fields={[
              {
                "field": "value"
              }
            ]}
              with="cds/tpi_calculations" />
            <HX.Pane flow="right">
              <HX.Notes field="cds/tpi_calculations/net_premium/comment" />
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Historic Freq"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Historical Frequencies">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/sector_display"
            ]}
              numCols={2} />
            <HX.Collection fields={[
              null
            ]} />
            <HX.Notes field="cds/linked_spreadsheet" />
          </HX.Pane>
          <HX.Table data={[
            {
              "datum": "cds/historical_freq",
              "elementLabelBy": "display_year"
            }
          ]}
            fields={[
            "claims",
            "exposure",
            "base_frequency",
            "mc_frequency"
          ]}
            transpose={true} />
          <HX.Notes field="cds/table_explained" />
          <HX.Pane>
            <CustomComponent title="Historic Frequencies"
              xAxisLabel="Year"
              yAxisLabel="Frequency"
              yAxis2Label=""
              series={[
              {
                "colour": "#000000",
                "label": "Base Frequency",
                "line_type": "lines+marker",
                "points": [
                  {
                    "list": "cds/historical_freq",
                    "x": "display_year",
                    "y": "base_frequency"
                  }
                ],
                "yaxis": "y"
              },
              {
                "colour": "#CA3397",
                "label": "Market Cap Frequency",
                "line_type": "lines",
                "points": [
                  {
                    "list": "cds/historical_freq",
                    "x": "display_year",
                    "y": "mc_frequency"
                  }
                ],
                "yaxis": "y"
              }
            ]} />
            <HX.Notes field="cds/graph_explained" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        shownBy="model_state/show_rate_change">
        <HX.Section title="Private Rate Change"
          shownBy="/cds/review_type/private_priced">
          <HX.Pane flow="right">
            <HX.Button task="rc_private_task"
              title="Calculate Private Rate Change" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Fetch Expiring Policy"
          shownBy="cds/standard_fields/is_rater_priced">
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
          }}
            shownBy="cds/is_abc">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
          }}
            shownBy="cds/is_side_a">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
              <HX.Table shownBy="/cds/review_type/rater_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
              <HX.Table shownBy="/cds/review_type/private_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "excess_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
                "rate_change/new_calculated_premium/uw_selected",
                "rate_change/new_premium/gross",
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/rate_change/show_rarc_table" />
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
          }}
            shownBy="cds/is_abc">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
          }}
            shownBy="cds/is_side_a">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
              <HX.Table shownBy="/cds/review_type/rater_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
              <HX.Table shownBy="/cds/review_type/private_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "excess_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
                "rate_change/new_calculated_premium/uw_selected",
                "rate_change/new_premium/gross",
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/rate_change/show_rarc_table" />
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
          }}
            shownBy="cds/is_abc">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
          }}
            shownBy="cds/is_side_a">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
              <HX.Table shownBy="/cds/review_type/rater_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
              <HX.Table shownBy="/cds/review_type/private_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "excess_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
                "rate_change/new_calculated_premium/uw_selected",
                "rate_change/new_premium/gross",
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/rate_change/show_rarc_table" />
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
          }}
            shownBy="cds/is_abc">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
          }}
            shownBy="cds/is_side_a">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
              <HX.Table shownBy="/cds/review_type/rater_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
              <HX.Table shownBy="/cds/review_type/private_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "excess_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
                "rate_change/new_calculated_premium/uw_selected",
                "rate_change/new_premium/gross",
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/rate_change/show_rarc_table" />
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
          }}
            shownBy="cds/is_abc">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
          }}
            shownBy="cds/is_side_a">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
              <HX.Table shownBy="/cds/review_type/rater_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
              <HX.Table shownBy="/cds/review_type/private_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "excess_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
                "rate_change/new_calculated_premium/uw_selected",
                "rate_change/new_premium/gross",
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/rate_change/show_rarc_table" />
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
          }}
            shownBy="cds/is_abc">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
          }}
            shownBy="cds/is_side_a">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "market_cap",
                "insider_share",
                "revised_market_cap",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/rater_priced"
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
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_annualized_100pct",
                "premium_annualized_beazley_share",
                "limit",
                "deductible",
                "side_a_excess",
                "abc_tower",
                "total_excess",
                "asset_size",
                "brokerage",
                "ei_offered"
              ]}
                shownBy="/cds/review_type/private_priced"
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "private_priced",
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
              <HX.Table shownBy="/cds/review_type/rater_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
              <HX.Table shownBy="/cds/review_type/private_priced"
                data={[
                "exposure_change_fixed",
                "risk_characteristics_change",
                "deductible_change_fixed",
                "limit_change_fixed",
                "excess_change_fixed",
                "terms_conditions_change",
                "other_change_fixed",
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
                "rate_change/new_calculated_premium/uw_selected",
                "rate_change/new_premium/gross",
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/rate_change/show_rarc_table" />
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
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Underwriter Rationale Comments">
          <CustomComponent textNode="cds/standard_fields/uw_rationale" />
        </HX.Section>
        <HX.Section title="General Comments">
          <CustomComponent textNode="cds/comment" />
        </HX.Section>
        <HX.Section title="Claims History Comments">
          <CustomComponent textNode="cds/claims_history" />
                  
        </HX.Section>
        <HX.Section title="T&C's Comments">
          <CustomComponent textNode="cds/t_and_c_comment" />
                 
        </HX.Section>
        <HX.Section title="File Uploads">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.File field="cds/file_upload_1" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_2" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_3" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_4" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_5" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_6" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_7" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_8" />
            </HX.Pane>
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