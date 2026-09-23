
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page title="Landing Page"
        shownBy="model_state/show_landing_page"
        viewScale={1}>
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
        shownBy="model_state/show_after_landing_page"
        viewScale={1}>
        <HX.Section title="Account Details">
          <HX.Collection fields={[
            "inception_date",
            "expiry_date"
          ]}
            with="hx_core"
            horizontal={true} />
          <HX.Collection fields={[
            "standard_fields/underwriter",
            null
          ]}
            with="cds"
            horizontal={true} />
          <HX.Collection fields={[
            "standard_fields/insured_name"
          ]}
            with="cds" />
          <HX.Collection fields={[
            "risk_info/currency",
            "standard_fields/is_renewal"
          ]}
            with="cds"
            horizontal={true} />
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "risk_info/quote_details_search"
            ]}
              with="cds" />
            <HX.Button task="save_quote_details_to_pas_reference"
              title="Save Quote Details to PAS Reference" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "standard_fields/broker",
            "risk_info/broker_contact"
          ]}
            with="cds"
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Industry Details">
          <HX.Collection fields={[
            "rating_factors/risk_info/region",
            "standard_fields/insured_country"
          ]}
            with="cds"
            horizontal={true} />
          <HX.Collection fields={[
            "key_industry/code_name",
            "rating_factors/risk_info/sub_industry"
          ]}
            with="cds"
            horizontal={true} />
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "ownership_type"
            ]}
              with="cds/rating_factors/risk_info" />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Cover Required">
          <HX.Collection fields={[
            "crime_coverage_required",
            "pi_coverage_required",
            "do_coverage_required"
          ]}
            with="cds/rating_factors/risk_info"
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Other Information">
          <HX.Pane>
            <HX.Collection fields={[
              "platform",
              "eea_non_eea_indicator"
            ]}
              with="cds/risk_info"
              horizontal={true} />
            <HX.Collection fields={[
              "direct_ri",
              "cedant_name"
            ]}
              with="cds/risk_info"
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="generate_tags"
              title="Create Policy Tags" />
            <HX.Collection fields={[
              "policy_tag_msg"
            ]}
              with="cds" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Comments">
          <HX.Notes field="comments"
            with="cds/risk_info" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        shownBy="/non_cds/exposure_details/regions/show"
        viewScale={1}>
        <HX.Section title="Client Information"
          shownBy="/non_cds/exposure_details/client_info_show">
          <HX.Collection fields={[
            {
              "field": "no_of_locations",
              "shownBy": "/non_cds/exposure_details/no_of_locations_show"
            },
            {
              "field": "currency",
              "shownBy": "/non_cds/exposure_details/regions/show"
            },
            null
          ]}
            with="cds/rating_factors/exposure_details"
            horizontal={true}
            syncColumnWidthsKey="client_info" />
          <HX.Collection fields={[
            "main_listing",
            "ipo_date",
            "/cds/exposure/aggregate/market_cap",
            "us_listing",
            {
              "field": "/cds/exposure/aggregate/market_cap_us",
              "shownBy": "/non_cds/exposure_details/market_cap_us_show"
            }
          ]}
            shownBy="/non_cds/exposure_details/client_info_public_show"
            with="cds/rating_factors/exposure_details"
            numCols={3}
            syncColumnWidthsKey="client_info" />
        </HX.Section>
        <HX.Section title="Exposure Details"
          shownBy="non_cds/exposure_details/exposure_details_show">
          <HX.Collection fields={[
            "total_amounts/aum"
          ]}
            shownBy="/non_cds/exposure_details/total_aum_show"
            with="cds/exposure/aggregate"
            syncColumnWidthsKey="client_info" />
          <HX.Table data={[
            "aggregate/total_amounts",
            null,
            "granular/regions/splits_entered_as"
          ]}
            fields={[
            "employees",
            "revenues",
            "assets"
          ]}
            shownBy="/non_cds/exposure_details/regions/show"
            with="cds/exposure"
            title="Regions"
            syncColumnWidthsKey="exposure_details" />
          <HX.Table data={[
            "africa",
            "arab_states",
            "asia",
            "oceania",
            "europe",
            "former_soviet_republics",
            "usa",
            "canada",
            "south_latin_america",
            "caribbean",
            "row",
            null,
            "/non_cds/exposure_details/regions/check_on_totals"
          ]}
            fields={[
            {
              "field": "value/employees",
              "shownBy": "/non_cds/exposure_details/regions/is_value/employees"
            },
            {
              "field": "percent/employees",
              "shownBy": "/non_cds/exposure_details/regions/is_percent/employees"
            },
            {
              "field": "value/revenues",
              "shownBy": "/non_cds/exposure_details/regions/is_value/revenues"
            },
            {
              "field": "percent/revenues",
              "shownBy": "/non_cds/exposure_details/regions/is_percent/revenues"
            },
            {
              "field": "value/assets",
              "shownBy": "/non_cds/exposure_details/regions/is_value/assets"
            },
            {
              "field": "percent/assets",
              "shownBy": "/non_cds/exposure_details/regions/is_percent/assets"
            }
          ]}
            shownBy="/non_cds/exposure_details/regions/show"
            with="cds/exposure/granular/regions/regions_list"
            syncColumnWidthsKey="exposure_details"
            kb-interactive={true} />
          <HX.Collection fields={[
            "missing_amount_text.read_only_option",
            {
              "field": "value/employees",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/value/employees/hide_missing"
            },
            {
              "field": "percent/employees",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/employees/hide_missing"
            },
            {
              "field": "value/employees.missing_values",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/value/employees/show_missing"
            },
            {
              "field": "percent/employees.missing_values",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/employees/show_missing"
            },
            {
              "field": "value/revenues",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/value/revenues/hide_missing"
            },
            {
              "field": "percent/revenues",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/revenues/hide_missing"
            },
            {
              "field": "value/revenues.missing_values",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/value/revenues/show_missing"
            },
            {
              "field": "percent/revenues.missing_values",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/revenues/show_missing"
            },
            {
              "field": "value/assets",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/value/assets/hide_missing"
            },
            {
              "field": "percent/assets",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/assets/hide_missing"
            },
            {
              "field": "value/assets.missing_values",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/value/assets/show_missing"
            },
            {
              "field": "percent/assets.missing_values",
              "shownBy": "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/assets/show_missing"
            }
          ]}
            with="/non_cds/exposure_details/regions/missing_amounts"
            horizontal={true}
            syncColumnWidthsKey="exposure_details" />
          <HX.Collection fields={[
            "commited_capital",
            "invested_capital"
          ]}
            shownBy="/non_cds/exposure_details/capital_show"
            with="cds/exposure/granular"
            horizontal={true}
            syncColumnWidthsKey="client_info" />
          <HX.Collection fields={[
            "no_of_directorship"
          ]}
            shownBy="/non_cds/exposure_details/no_of_directorship_show"
            with="cds/exposure/granular"
            syncColumnWidthsKey="client_info" />
          <HX.Collection fields={[
            "transactions_av_value",
            "transactions_av_fee"
          ]}
            shownBy="/non_cds/exposure_details/transactions_av_show"
            with="cds/exposure/granular"
            horizontal={true}
            syncColumnWidthsKey="client_info" />
        </HX.Section>
        <HX.Section title="Investor Profile"
          shownBy="non_cds/exposure_details/investor_split/show">
          <HX.Pane flow="right">
            <HX.Table title="Type"
              data={[
              "investor_split_type/institutional",
              "investor_split_type/retail",
              "investor_split_type/other",
              "/non_cds/exposure_details/investor_split/type_total"
            ]}
              fields={[
              "percent"
            ]}
              with="cds/exposure/granular"
              kb-interactive={true} />
            <HX.Table title="Regions"
              data={[
              "investor_split_region/region_1",
              "investor_split_region/region_2",
              "investor_split_region/region_3",
              "/non_cds/exposure_details/investor_split/region_total"
            ]}
              fields={[
              "region",
              "percent"
            ]}
              with="cds/exposure/granular"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Credit Rating"
          shownBy="non_cds/exposure_details/credit_rating_show">
          <HX.Collection fields={[
            "cr_s_and_p",
            "cr_moodys",
            "cr_fitch"
          ]}
            with="cds/rating_factors/exposure_details"
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Revenue Split by Activity"
          shownBy="non_cds/exposure_details/revenue_split_admin/show">
          <HX.Table data={[
            "est_companies",
            "est_trusts",
            "outside_board",
            "legal_advice",
            "accountancy",
            "tax",
            "other",
            "/non_cds/exposure_details/revenue_split_admin/total"
          ]}
            fields={[
            "amount",
            "percent"
          ]}
            with="cds/exposure/granular/revenue_split_admin"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Revenue Split by Activity"
          shownBy="non_cds/exposure_details/revenue_split_banks/show">
          <HX.Table data={[
            "interest",
            "fee",
            "trading",
            "other",
            "/non_cds/exposure_details/revenue_split_banks/total"
          ]}
            fields={[
            "amount",
            "percent"
          ]}
            with="cds/exposure/granular/revenue_split_banks"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Premium Income split"
          shownBy="non_cds/exposure_details/premium_split/show">
          <HX.Table data={[
            "life",
            "pc",
            "personal",
            "commercial",
            "healthcare",
            "ripc",
            "other",
            "/non_cds/exposure_details/premium_split/total"
          ]}
            fields={[
            "amount",
            "percent"
          ]}
            with="cds/exposure/granular/premium_split"
            kb-interactive={true} />
          <HX.Collection fields={[
            "combined_ratio",
            "solvency_ratio"
          ]}
            with="cds/rating_factors/exposure_details"
            horizontal={true}
            syncColumnWidthsKey="client_info" />
          <HX.Collection fields={[
            "short_tail_pc",
            "direct_business_pc"
          ]}
            with="cds/rating_factors/exposure_details"
            horizontal={true}
            syncColumnWidthsKey="client_info" />
        </HX.Section>
        <HX.Section title="Revenue Split by Activity"
          shownBy="non_cds/exposure_details/revenue_split_brokers/show">
          <HX.Table data={[
            "institutional_advisory",
            "institutional_execution",
            "retail_advisory",
            "retail_execution",
            "retail_discretionary",
            "other",
            "/non_cds/exposure_details/revenue_split_brokers/total"
          ]}
            fields={[
            "amount",
            "percent"
          ]}
            with="cds/exposure/granular/revenue_split_brokers"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Revenue Split by Activity"
          shownBy="non_cds/exposure_details/revenue_split_exchanges/show">
          <HX.Table data={[
            "exchange",
            "listing",
            "clear_settlement",
            "depositary",
            "other",
            "/non_cds/exposure_details/revenue_split_exchanges/total"
          ]}
            fields={[
            "amount",
            "percent"
          ]}
            with="cds/exposure/granular/revenue_split_exchanges"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Revenue Split by Activity"
          shownBy="non_cds/exposure_details/revenue_split_investment/show">
          <HX.Table data={[
            "investment_management",
            "personal_services",
            "legal_advisory_services",
            "family_group_services",
            "other",
            "/non_cds/exposure_details/revenue_split_investment/total"
          ]}
            fields={[
            "amount",
            "percent"
          ]}
            with="cds/exposure/granular/revenue_split_investment"
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Assessment"
        shownBy="model_state/show_after_landing_page"
        viewScale={1}>
        <HX.Section title="Underwriting considerations">
          <HX.Table data={[
            "risk_category",
            "comment"
          ]}
            fields={[
            {
              "field": "policy_wording",
              "shownBy": "/non_cds/risk_assesment/any_any"
            },
            {
              "field": "claims_history_cpi",
              "shownBy": "/non_cds/risk_assesment/any_crime_pi"
            },
            {
              "field": "claims_history_do",
              "shownBy": "/non_cds/risk_assesment/any_do"
            },
            {
              "field": "risk_management",
              "shownBy": "/non_cds/risk_assesment/any_any"
            },
            {
              "field": "strength_of_financial",
              "shownBy": "/non_cds/risk_assesment/any_any"
            },
            {
              "field": "technological_infrastructure",
              "shownBy": "/non_cds/risk_assesment/any_any"
            },
            {
              "field": "quality_of_control",
              "shownBy": "/non_cds/risk_assesment/any_crime"
            },
            {
              "field": "agents_as_employees",
              "shownBy": "/non_cds/risk_assesment/notins_crime_pi"
            },
            {
              "field": "regulatory_risk",
              "shownBy": "/non_cds/risk_assesment/any_pi_do"
            },
            {
              "field": "quality_of_claims_handling",
              "shownBy": "/non_cds/risk_assesment/ins_pi"
            },
            {
              "field": "product_complexity",
              "shownBy": "/non_cds/risk_assesment/any_pi"
            },
            {
              "field": "quality_of_bcp",
              "shownBy": "/non_cds/risk_assesment/fin_pi"
            },
            {
              "field": "market_regulator",
              "shownBy": "/non_cds/risk_assesment/ban_fin_pi"
            },
            {
              "field": "extent_of_leveraged_gearing",
              "shownBy": "/non_cds/risk_assesment/inv_pi"
            },
            {
              "field": "quality_of_performance_non_pevc",
              "shownBy": "/non_cds/risk_assesment/inv_pi"
            },
            {
              "field": "redemption_gates",
              "shownBy": "/non_cds/risk_assesment/inv_pi"
            },
            {
              "field": "valuation_for_pevc",
              "shownBy": "/non_cds/risk_assesment/inv_PE_VC_RE_pi"
            },
            {
              "field": "loan_covenant",
              "shownBy": "/non_cds/risk_assesment/inv_PE_VC_RE_pi"
            },
            {
              "field": "dando_portfolio_companies",
              "shownBy": "/non_cds/risk_assesment/inv_PE_VC_do"
            },
            {
              "field": "data_centre",
              "shownBy": "/non_cds/risk_assesment/fin_any"
            },
            {
              "field": "tech_outsourcing",
              "shownBy": "/non_cds/risk_assesment/fin_any"
            },
            "uw_adj.input"
          ]}
            with="cds/modifiers"
            transpose={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Cover Details"
        shownBy="model_state/show_after_landing_page"
        viewScale={1}>
        <HX.Section title="Primary Layer">
          <HX.Collection fields={[
            {
              "field": "different_towers_manager_fund_warning.read_only_option",
              "shownBy": "show_different_towers_manager_fund_warning"
            }
          ]}
            with="/non_cds/cover_details" />
          <HX.Pane flow="right">
            <HX.Table data={[
              "towers_all_manager"
            ]}
              fields={[
              {
                "field": "crime",
                "shownBy": "/cds/rating_factors/risk_info/crime_coverage_required"
              },
              {
                "field": "pi",
                "shownBy": "/cds/rating_factors/risk_info/pi_coverage_required"
              },
              {
                "field": "do",
                "shownBy": "/cds/rating_factors/risk_info/do_coverage_required"
              }
            ]}
              shownBy="/non_cds/cover_details/all_manager_show"
              with="cds/rating_factors/cover_details/primary_layer"
              transpose={true}
              kb-interactive={true} />
            <HX.Table data={[
              "towers_all_manager.manager",
              "towers_fund"
            ]}
              fields={[
              {
                "field": "crime",
                "shownBy": "/cds/rating_factors/risk_info/crime_coverage_required"
              },
              {
                "field": "pi",
                "shownBy": "/cds/rating_factors/risk_info/pi_coverage_required"
              },
              {
                "field": "do",
                "shownBy": "/cds/rating_factors/risk_info/do_coverage_required"
              }
            ]}
              shownBy="/non_cds/cover_details/fund_show"
              with="cds/rating_factors/cover_details/primary_layer"
              transpose={true}
              kb-interactive={true} />
            <HX.Pane shownBy="/non_cds/cover_details/all_manager_show" />
            <HX.Table data={[
              "sir_all_manager"
            ]}
              fields={[
              {
                "field": "crime",
                "shownBy": "/cds/rating_factors/risk_info/crime_coverage_required"
              },
              {
                "field": "pi",
                "shownBy": "/cds/rating_factors/risk_info/pi_coverage_required"
              },
              {
                "field": "do",
                "shownBy": "/non_cds/cover_details/do_side_a_show"
              },
              {
                "field": "do.side_b",
                "shownBy": "/non_cds/cover_details/do_side_b_show"
              },
              {
                "field": "do_side_c",
                "shownBy": "/non_cds/cover_details/do_side_c_show"
              }
            ]}
              shownBy="/non_cds/cover_details/all_manager_show"
              with="cds/rating_factors/cover_details/primary_layer"
              transpose={true}
              kb-interactive={true} />
            <HX.Table data={[
              "sir_all_manager.manager",
              "sir_fund"
            ]}
              fields={[
              {
                "field": "crime",
                "shownBy": "/cds/rating_factors/risk_info/crime_coverage_required"
              },
              {
                "field": "pi",
                "shownBy": "/cds/rating_factors/risk_info/pi_coverage_required"
              },
              {
                "field": "do",
                "shownBy": "/non_cds/cover_details/do_side_a_show"
              },
              {
                "field": "do.side_b",
                "shownBy": "/non_cds/cover_details/do_side_b_show"
              },
              {
                "field": "do_side_c",
                "shownBy": "/non_cds/cover_details/do_side_c_show"
              }
            ]}
              shownBy="/non_cds/cover_details/fund_show"
              with="cds/rating_factors/cover_details/primary_layer"
              transpose={true}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Collection fields={[
            "do_type"
          ]}
            shownBy="/cds/rating_factors/risk_info/do_coverage_required"
            with="cds/rating_factors/cover_details/primary_layer"
            syncColumnWidthsKey="coverage_details" />
        </HX.Section>
        <HX.Section title="Coverage specifics">
          <HX.Collection fields={[
            "sublimits_req",
            "details_reinstatements",
            {
              "field": "reinst_rtc_program_limit",
              "shownBy": "/non_cds/cover_details/rtc_limit_show"
            },
            {
              "field": "no_direct_reinstatements",
              "shownBy": "/non_cds/cover_details/direct_reinstatements_show"
            }
          ]}
            with="cds/rating_factors/cover_details"
            numCols={3}
            syncColumnWidthsKey="coverage_details" />
          <HX.Collection fields={[
            {
              "field": "cover_details/crime_retroactive_date",
              "shownBy": "risk_info/crime_coverage_required"
            },
            {
              "field": "cover_details/pi_retroactive_date",
              "shownBy": "risk_info/pi_coverage_required"
            },
            {
              "field": "cover_details/do_retroactive_date",
              "shownBy": "risk_info/do_coverage_required"
            }
          ]}
            shownBy="/non_cds/risk_info/is_coverage_required"
            with="cds/rating_factors"
            horizontal={true}
            syncColumnWidthsKey="coverage_details" />
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "num_layers"
            ]}
              with="non_cds/cover_details"
              syncColumnWidthsKey="coverage_details" />
            <HX.Button task="num_layers_task"
              title="Apply Number of Layers" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Split of premium"
          shownBy="non_cds/cover_details/premium_split_show">
          <HX.Collection fields={[
            "eea",
            "non_eea"
          ]}
            shownBy="/cds/risk_info/eea_non_eea_indicator"
            with="cds/rating_factors/cover_details/premium_split_all_layers"
            horizontal={true}
            syncColumnWidthsKey="coverage_details" />
          <HX.Collection fields={[
            "is_premium_split_all_layers",
            null,
            null
          ]}
            shownBy="/non_cds/risk_info/is_coverage_required"
            with="non_cds/cover_details"
            horizontal={true} />
          <HX.Collection fields={[
            {
              "field": "cover_details/premium_split_all_layers/crime",
              "shownBy": "risk_info/crime_coverage_required"
            },
            {
              "field": "cover_details/premium_split_all_layers/pi",
              "shownBy": "risk_info/pi_coverage_required"
            },
            {
              "field": "cover_details/premium_split_all_layers/do",
              "shownBy": "risk_info/do_coverage_required"
            },
            {
              "field": "/non_cds/cover_details/premium_split_missing_amount",
              "shownBy": "/non_cds/cover_details/show_premium_split_missing_amount"
            },
            {
              "field": "/non_cds/cover_details/premium_split_missing_amount.bad",
              "shownBy": "/non_cds/cover_details/show_bad_premium_split_missing_amount"
            }
          ]}
            shownBy="/non_cds/cover_details/premium_split_coverages_show"
            with="cds/rating_factors"
            numCols={3}
            syncColumnWidthsKey="coverage_details" />
        </HX.Section>
        <HX.Section title="Brokerage & Discounts">
          <HX.Collection fields={[
            "is_brokerage_all_layers",
            null,
            null
          ]}
            with="non_cds/cover_details"
            horizontal={true} />
          <HX.Collection fields={[
            "brk.input",
            "ncb",
            "lta"
          ]}
            shownBy="/non_cds/cover_details/is_brokerage_all_layers"
            with="cds/rating_factors/cover_details/brokerage_all_layers"
            horizontal={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        shownBy="model_state/show_after_landing_page"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Program Structure">
          <HX.Collection fields={[
            "table1_label",
            null,
            null,
            null,
            null
          ]}
            with="non_cds/rating_summary"
            syncColumnWidthsKey="field"
            horizontal={true} />
          <HX.Table data={[
            {
              "datum": "cds/layers",
              "elementLabelBy": "label"
            }
          ]}
            fields={[
            {
              "field": "tower_1/coverage",
              "shownBy": "non_cds/rating_summary/tower_1/coverage_show"
            },
            {
              "field": "tower_2/coverage",
              "shownBy": "non_cds/rating_summary/tower_2/coverage_show"
            },
            {
              "field": "tower_3/coverage",
              "shownBy": "non_cds/rating_summary/tower_3/coverage_show"
            },
            {
              "field": "tower_4/coverage",
              "shownBy": "non_cds/rating_summary/tower_4/coverage_show"
            },
            {
              "field": "tower_5/coverage",
              "shownBy": "non_cds/rating_summary/tower_5/coverage_show"
            },
            {
              "field": "tower_6/coverage",
              "shownBy": "non_cds/rating_summary/tower_6/coverage_show"
            },
            null,
            {
              "field": "tower_1/limit",
              "shownBy": "non_cds/cover_details/tower_1_show"
            },
            {
              "field": "tower_2/limit",
              "shownBy": "non_cds/cover_details/tower_2_show"
            },
            {
              "field": "tower_3/limit",
              "shownBy": "non_cds/cover_details/tower_3_show"
            },
            {
              "field": "tower_4/limit",
              "shownBy": "non_cds/cover_details/tower_4_show"
            },
            {
              "field": "tower_5/limit",
              "shownBy": "non_cds/cover_details/tower_5_show"
            },
            {
              "field": "tower_6/limit",
              "shownBy": "non_cds/cover_details/tower_6_show"
            },
            null,
            {
              "field": "tower_1/excess_str",
              "shownBy": "non_cds/cover_details/tower_1_show"
            },
            {
              "field": "tower_2/excess_str",
              "shownBy": "non_cds/cover_details/tower_2_show"
            },
            {
              "field": "tower_3/excess_str",
              "shownBy": "non_cds/cover_details/tower_3_show"
            },
            {
              "field": "tower_4/excess_str",
              "shownBy": "non_cds/cover_details/tower_4_show"
            },
            {
              "field": "tower_5/excess_str",
              "shownBy": "non_cds/cover_details/tower_5_show"
            },
            {
              "field": "tower_6/excess_str",
              "shownBy": "non_cds/cover_details/tower_6_show"
            },
            null,
            {
              "field": "tower_1/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_1/direct_reinstatements_show"
            },
            {
              "field": "tower_2/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_2/direct_reinstatements_show"
            },
            {
              "field": "tower_3/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_3/direct_reinstatements_show"
            },
            {
              "field": "tower_4/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_4/direct_reinstatements_show"
            },
            {
              "field": "tower_5/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_5/direct_reinstatements_show"
            },
            {
              "field": "tower_6/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_6/direct_reinstatements_show"
            },
            null,
            {
              "field": "tower_1/rtc_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_1/rtc_reinstatements_show"
            },
            {
              "field": "tower_2/rtc_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_2/rtc_reinstatements_show"
            },
            {
              "field": "tower_3/rtc_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_3/rtc_reinstatements_show"
            },
            {
              "field": "tower_4/rtc_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_4/rtc_reinstatements_show"
            },
            {
              "field": "tower_5/rtc_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_5/rtc_reinstatements_show"
            },
            {
              "field": "tower_6/rtc_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_6/rtc_reinstatements_show"
            },
            null,
            {
              "field": "coverages/crime/all_manager/sublimit",
              "shownBy": "non_cds/rating_summary/crime/sublimit_show"
            },
            {
              "field": "coverages/pi/all_manager/sublimit",
              "shownBy": "non_cds/rating_summary/pi/sublimit_show"
            },
            {
              "field": "coverages/do/all_manager/sublimit",
              "shownBy": "non_cds/rating_summary/do/sublimit_show"
            },
            {
              "field": "coverages/crime/all_manager/sublimit.manager",
              "shownBy": "non_cds/rating_summary/crime/all_manager_sublimit_show"
            },
            {
              "field": "coverages/pi/all_manager/sublimit.manager",
              "shownBy": "non_cds/rating_summary/pi/all_manager_sublimit_show"
            },
            {
              "field": "coverages/do/all_manager/sublimit.manager",
              "shownBy": "non_cds/rating_summary/do/all_manager_sublimit_show"
            },
            {
              "field": "coverages/crime/fund/sublimit",
              "shownBy": "non_cds/rating_summary/crime/fund_sublimit_show"
            },
            {
              "field": "coverages/pi/fund/sublimit",
              "shownBy": "non_cds/rating_summary/pi/fund_sublimit_show"
            },
            {
              "field": "coverages/do/fund/sublimit",
              "shownBy": "non_cds/rating_summary/do/fund_sublimit_show"
            },
            null,
            "quoted_premium_pro_rata_100.input",
            {
              "field": "brokerage.input",
              "shownBy": "non_cds/rating_summary/is_brokerage_per_layer"
            },
            {
              "field": "ncb",
              "shownBy": "non_cds/rating_summary/is_brokerage_per_layer"
            },
            {
              "field": "lta",
              "shownBy": "non_cds/rating_summary/is_brokerage_per_layer"
            },
            "net_premium",
            {
              "field": "coverages/crime/premium_split",
              "shownBy": "non_cds/rating_summary/crime/premium_split_show"
            },
            {
              "field": "coverages/pi/premium_split",
              "shownBy": "non_cds/rating_summary/pi/premium_split_show"
            },
            {
              "field": "coverages/do/premium_split",
              "shownBy": "non_cds/rating_summary/do/premium_split_show"
            },
            null,
            {
              "field": "tower_1/beazley_line",
              "shownBy": "non_cds/cover_details/tower_1_show"
            },
            {
              "field": "tower_2/beazley_line",
              "shownBy": "non_cds/cover_details/tower_2_show"
            },
            {
              "field": "tower_3/beazley_line",
              "shownBy": "non_cds/cover_details/tower_3_show"
            },
            {
              "field": "tower_4/beazley_line",
              "shownBy": "non_cds/cover_details/tower_4_show"
            },
            {
              "field": "tower_5/beazley_line",
              "shownBy": "non_cds/cover_details/tower_5_show"
            },
            {
              "field": "tower_6/beazley_line",
              "shownBy": "non_cds/cover_details/tower_6_show"
            },
            null,
            "esg",
            null,
            "exposure",
            "afb_net_premium",
            "net_rol",
            "actual_ilf",
            null,
            "bpi",
            "benchmark_premium_annualised_100",
            "benchmark_premium_pro_rata_100",
            {
              "field": "coverages/crime/losses_split",
              "shownBy": "cds/rating_factors/risk_info/crime_coverage_required"
            },
            {
              "field": "coverages/pi/losses_split",
              "shownBy": "cds/rating_factors/risk_info/pi_coverage_required"
            },
            {
              "field": "coverages/do/losses_split",
              "shownBy": "cds/rating_factors/risk_info/do_coverage_required"
            },
            "model_ilf",
            null,
            "expected_loss_cost_att",
            "expected_loss_cost_cat",
            "tpi",
            "technical_premium_net",
            "technical_premium",
            null,
            "status.input",
            {
              "field": "coverages/crime/pol_ref",
              "minWidth": 200,
              "shownBy": "cds/rating_factors/risk_info/crime_coverage_required"
            },
            {
              "field": "coverages/pi/pol_ref",
              "minWidth": 200,
              "shownBy": "cds/rating_factors/risk_info/pi_coverage_required"
            },
            {
              "field": "coverages/do/pol_ref",
              "minWidth": 200,
              "shownBy": "cds/rating_factors/risk_info/do_coverage_required"
            },
            {
              "field": "coverages/crime/pol_ref_non_eea",
              "minWidth": 200,
              "shownBy": "non_cds/rating_summary/crime/pol_ref_non_eea_show"
            },
            {
              "field": "coverages/pi/pol_ref_non_eea",
              "minWidth": 200,
              "shownBy": "non_cds/rating_summary/pi/pol_ref_non_eea_show"
            },
            {
              "field": "coverages/do/pol_ref_non_eea",
              "minWidth": 200,
              "shownBy": "non_cds/rating_summary/do/pol_ref_non_eea_show"
            },
            "slip_lead"
          ]}
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Program Structure - USD"
          shownBy="non_cds/rating_summary/secondry_summary_show">
          <HX.Collection fields={[
            "authorities_fx"
          ]}
            with="cds/rating_summary"
            syncColumnWidthsKey="field"
            horizontal={true} />
          <HX.Table data={[
            {
              "datum": "cds/layers",
              "elementLabelBy": "label"
            }
          ]}
            fields={[
            {
              "field": "tower_1/coverage",
              "shownBy": "non_cds/cover_details/tower_1_show"
            },
            {
              "field": "tower_2/coverage",
              "shownBy": "non_cds/cover_details/tower_2_show"
            },
            {
              "field": "tower_3/coverage",
              "shownBy": "non_cds/cover_details/tower_3_show"
            },
            {
              "field": "tower_4/coverage",
              "shownBy": "non_cds/cover_details/tower_4_show"
            },
            {
              "field": "tower_5/coverage",
              "shownBy": "non_cds/cover_details/tower_5_show"
            },
            {
              "field": "tower_6/coverage",
              "shownBy": "non_cds/cover_details/tower_6_show"
            },
            null,
            {
              "field": "tower_1/limit_fx",
              "shownBy": "non_cds/cover_details/tower_1_show"
            },
            {
              "field": "tower_2/limit_fx",
              "shownBy": "non_cds/cover_details/tower_2_show"
            },
            {
              "field": "tower_3/limit_fx",
              "shownBy": "non_cds/cover_details/tower_3_show"
            },
            {
              "field": "tower_4/limit_fx",
              "shownBy": "non_cds/cover_details/tower_4_show"
            },
            {
              "field": "tower_5/limit_fx",
              "shownBy": "non_cds/cover_details/tower_5_show"
            },
            {
              "field": "tower_6/limit_fx",
              "shownBy": "non_cds/cover_details/tower_6_show"
            },
            null,
            {
              "field": "tower_1/excess_str_fx",
              "shownBy": "non_cds/cover_details/tower_1_show"
            },
            {
              "field": "tower_2/excess_str_fx",
              "shownBy": "non_cds/cover_details/tower_2_show"
            },
            {
              "field": "tower_3/excess_str_fx",
              "shownBy": "non_cds/cover_details/tower_3_show"
            },
            {
              "field": "tower_4/excess_str_fx",
              "shownBy": "non_cds/cover_details/tower_4_show"
            },
            {
              "field": "tower_5/excess_str_fx",
              "shownBy": "non_cds/cover_details/tower_5_show"
            },
            {
              "field": "tower_6/excess_str_fx",
              "shownBy": "non_cds/cover_details/tower_6_show"
            },
            null,
            {
              "field": "tower_1/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_1/direct_reinstatements_show"
            },
            {
              "field": "tower_2/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_2/direct_reinstatements_show"
            },
            {
              "field": "tower_3/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_3/direct_reinstatements_show"
            },
            {
              "field": "tower_4/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_4/direct_reinstatements_show"
            },
            {
              "field": "tower_5/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_5/direct_reinstatements_show"
            },
            {
              "field": "tower_6/direct_reinstatements",
              "shownBy": "non_cds/rating_summary/tower_6/direct_reinstatements_show"
            },
            null,
            {
              "field": "tower_1/rtc_reinstatements_fx",
              "shownBy": "non_cds/rating_summary/tower_1/rtc_reinstatements_show"
            },
            {
              "field": "tower_2/rtc_reinstatements_fx",
              "shownBy": "non_cds/rating_summary/tower_2/rtc_reinstatements_show"
            },
            {
              "field": "tower_3/rtc_reinstatements_fx",
              "shownBy": "non_cds/rating_summary/tower_3/rtc_reinstatements_show"
            },
            {
              "field": "tower_4/rtc_reinstatements_fx",
              "shownBy": "non_cds/rating_summary/tower_4/rtc_reinstatements_show"
            },
            {
              "field": "tower_5/rtc_reinstatements_fx",
              "shownBy": "non_cds/rating_summary/tower_5/rtc_reinstatements_show"
            },
            {
              "field": "tower_6/rtc_reinstatements_fx",
              "shownBy": "non_cds/rating_summary/tower_6/rtc_reinstatements_show"
            },
            null,
            {
              "field": "coverages/crime/all_manager/sublimit_fx",
              "shownBy": "non_cds/rating_summary/crime/sublimit_show"
            },
            {
              "field": "coverages/pi/all_manager/sublimit_fx",
              "shownBy": "non_cds/rating_summary/pi/sublimit_show"
            },
            {
              "field": "coverages/do/all_manager/sublimit_fx",
              "shownBy": "non_cds/rating_summary/do/sublimit_show"
            },
            {
              "field": "coverages/crime/all_manager/sublimit_fx.manager",
              "shownBy": "non_cds/rating_summary/crime/all_manager_sublimit_show"
            },
            {
              "field": "coverages/pi/all_manager/sublimit_fx.manager",
              "shownBy": "non_cds/rating_summary/pi/all_manager_sublimit_show"
            },
            {
              "field": "coverages/do/all_manager/sublimit_fx.manager",
              "shownBy": "non_cds/rating_summary/do/all_manager_sublimit_show"
            },
            {
              "field": "coverages/crime/fund/sublimit_fx",
              "shownBy": "non_cds/rating_summary/crime/fund_sublimit_show"
            },
            {
              "field": "coverages/pi/fund/sublimit_fx",
              "shownBy": "non_cds/rating_summary/pi/fund_sublimit_show"
            },
            {
              "field": "coverages/do/fund/sublimit_fx",
              "shownBy": "non_cds/rating_summary/do/fund_sublimit_show"
            },
            null,
            "quoted_premium_pro_rata_100_fx",
            {
              "field": "brokerage",
              "shownBy": "non_cds/rating_summary/is_brokerage_per_layer"
            },
            {
              "field": "ncb",
              "shownBy": "non_cds/rating_summary/is_brokerage_per_layer"
            },
            {
              "field": "lta",
              "shownBy": "non_cds/rating_summary/is_brokerage_per_layer"
            },
            "net_premium_fx",
            {
              "field": "coverages/crime/premium_split",
              "shownBy": "non_cds/rating_summary/crime/premium_split_show"
            },
            {
              "field": "coverages/pi/premium_split",
              "shownBy": "non_cds/rating_summary/pi/premium_split_show"
            },
            {
              "field": "coverages/do/premium_split",
              "shownBy": "non_cds/rating_summary/do/premium_split_show"
            },
            null,
            {
              "field": "tower_1/beazley_line",
              "shownBy": "non_cds/cover_details/tower_1_show"
            },
            {
              "field": "tower_2/beazley_line",
              "shownBy": "non_cds/cover_details/tower_2_show"
            },
            {
              "field": "tower_3/beazley_line",
              "shownBy": "non_cds/cover_details/tower_3_show"
            },
            {
              "field": "tower_4/beazley_line",
              "shownBy": "non_cds/cover_details/tower_4_show"
            },
            {
              "field": "tower_5/beazley_line",
              "shownBy": "non_cds/cover_details/tower_5_show"
            },
            {
              "field": "tower_6/beazley_line",
              "shownBy": "non_cds/cover_details/tower_6_show"
            },
            null,
            "esg",
            null,
            "exposure_fx",
            "afb_net_premium_fx",
            "net_rol",
            "actual_ilf",
            null,
            "bpi",
            "benchmark_premium_annualised_100_fx",
            "benchmark_premium_pro_rata_100_fx",
            {
              "field": "coverages/crime/losses_split",
              "shownBy": "cds/rating_factors/risk_info/crime_coverage_required"
            },
            {
              "field": "coverages/pi/losses_split",
              "shownBy": "cds/rating_factors/risk_info/pi_coverage_required"
            },
            {
              "field": "coverages/do/losses_split",
              "shownBy": "cds/rating_factors/risk_info/do_coverage_required"
            },
            "model_ilf",
            null,
            "expected_loss_cost_att",
            "expected_loss_cost_cat",
            "tpi",
            "technical_premium_net_fx",
            "technical_premium_fx",
            null,
            "status.input",
            {
              "field": "coverages/crime/pol_ref",
              "minWidth": 200,
              "shownBy": "cds/rating_factors/risk_info/crime_coverage_required"
            },
            {
              "field": "coverages/pi/pol_ref",
              "minWidth": 200,
              "shownBy": "cds/rating_factors/risk_info/pi_coverage_required"
            },
            {
              "field": "coverages/do/pol_ref",
              "minWidth": 200,
              "shownBy": "cds/rating_factors/risk_info/do_coverage_required"
            },
            {
              "field": "coverages/crime/pol_ref_non_eea",
              "minWidth": 200,
              "shownBy": "non_cds/rating_summary/crime/pol_ref_non_eea_show"
            },
            {
              "field": "coverages/pi/pol_ref_non_eea",
              "minWidth": 200,
              "shownBy": "non_cds/rating_summary/pi/pol_ref_non_eea_show"
            },
            {
              "field": "coverages/do/pol_ref_non_eea",
              "minWidth": 200,
              "shownBy": "non_cds/rating_summary/do/pol_ref_non_eea_show"
            },
            "slip_lead"
          ]}
            freezeLeft={0} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        shownBy="model_state/show_after_landing_page"
        viewScale={1}>
        <HX.Section title="1. Summary of Programme Discussion with Broker">
          <HX.Notes field="general_comments"
            with="cds/rationale" />
        </HX.Section>
        <HX.Section title="2. Comments on BPI and/or Rate Change">
          <HX.Notes field="bpi_comments"
            with="cds/rationale" />
        </HX.Section>
        <HX.Section title="3. Any other Factors not Captured Elsewhere">
          <HX.Notes field="other_factors_comments"
            with="cds/rationale" />
        </HX.Section>
        <HX.Section title="4. Comments on ESG">
          <HX.Notes field="esg_comments"
            with="cds/rationale" />
        </HX.Section>
        <HX.Section title="5. I am writing this risk because">
          <HX.Notes field="reason_comments"
            with="cds/rationale" />
        </HX.Section>
        <HX.Section title="6. Any other documents/attachments are stored at (including file name)">
          <HX.Notes field="additional_info_path"
            with="cds/rationale" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        shownBy="model_state/show_rate_change"
        viewScale={1}>
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
        <HX.Section title="Renewal Layer - Primary"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 1st Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 2nd Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 3rd Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 4th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 5th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 6th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_7">
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 7th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_8">
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 8th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_9">
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 9th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_10">
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 10th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_11">
          <HX.With context={{
            "index": 10,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 11th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_12">
          <HX.With context={{
            "index": 11,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 12th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_13">
          <HX.With context={{
            "index": 12,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 13th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_14">
          <HX.With context={{
            "index": 13,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 14th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_15">
          <HX.With context={{
            "index": 14,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
        <HX.Section title="Renewal Layer - 15th Excess"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_16">
          <HX.With context={{
            "index": 15,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer_label",
                null,
                null
              ]}
                horizontal={true} />
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
      <HX.Page title="Excel Export"
        shownBy="model_state/show_after_landing_page"
        viewScale={1}>
        <HX.Section title="Excel Export">
          <HX.Notes field="excel_export_notes" />
          <HX.Button task="export_to_excel"
            title="Export to Excel" />
          <HX.File field="output_file"
            title="Output File"
            stretch={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Climate Litigation"
        shownBy="cds/rating_factors/risk_info/do_coverage_required"
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
                "cds/climate_document_country"
              ]}
                horizontal={true} />
              <HX.Button task="generate_climate_doc_task"
                title="Generate Climate Litigation Spotlight Report" />
              <HX.File field="cds/climate_document" />
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
        <HX.Section title="Summary Layer 11"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_11">
          <HX.With context={{
            "index": 10,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
        <HX.Section title="Summary Layer 12"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_12">
          <HX.With context={{
            "index": 11,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
        <HX.Section title="Summary Layer 13"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_13">
          <HX.With context={{
            "index": 12,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
        <HX.Section title="Summary Layer 14"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_14">
          <HX.With context={{
            "index": 13,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
        <HX.Section title="Summary Layer 15"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_15">
          <HX.With context={{
            "index": 14,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
        <HX.Section title="Summary Layer 16"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_16">
          <HX.With context={{
            "index": 15,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference",
              {
                "field": "brokerage.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers_not"
              },
              {
                "field": "/cds/rating_factors/cover_details/brokerage_all_layers/brk.read_only",
                "shownBy": "/non_cds/cover_details/is_brokerage_all_layers"
              },
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_pro_rata_100.read_only"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_pro_rata_100",
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
              "/cds/modifiers/risk_category/uw_adj.read_only"
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
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};