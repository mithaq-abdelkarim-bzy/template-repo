
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root keyFields={[
      {
        "field": "model_state/inconsistent_product_msg",
        "shownBy": "model_state/is_product_inconsistent"
      }
    ]}>
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
        <HX.Section title="Rating Model">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology",
              "cds/rater"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "inception_date",
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/insured_name"
            ]}
              horizontal={true} />
            <HX.Collection with="cds"
              fields={[
              "policy_info/application_date",
              "standard_fields/underwriter"
            ]}
              horizontal={true} />
            <HX.Collection with="cds"
              fields={[
              "currencies/source_currency",
              "standard_fields/is_renewal"
            ]}
              horizontal={true} />
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "/cds/standard_fields/policy_reference",
                "status"
              ]}
                horizontal={true} />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Cover Options">
          <HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Table data={[
                "coverages/hull",
                null,
                "coverages/liability"
              ]}
                fields={[
                "section_reference",
                "quoted_premium",
                "quoted_premium_net",
                null,
                "brokerage",
                "profit_commission",
                "ncb_pct",
                null,
                {
                  "field": "coverage",
                  "shownBy": "/cds/is_airlines"
                },
                "written_line",
                {
                  "field": "rate_change",
                  "labelBy": "coverages/hull/rate_change_label"
                },
                null,
                "limit",
                "excess",
                "currency"
              ]}
                transpose={true}
                kb-interactive={true}
                syncColumnWidthsKey="cover" />
            </HX.With>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "cds/experience_rating/claims_available"
              ]} />
              <HX.Pane shownBy="cds/is_neither" />
              <HX.Button title="Start Airlines"
                task="show_airlines_task"
                shownBy="cds/is_airlines" />
              <HX.Button title="Start General Aviation"
                task="show_ga_task"
                shownBy="cds/is_ga" />
            </HX.Pane>
            <HX.Collection fields={[
              null,
              "model_state/sql_failure_msg"
            ]}
              horizontal={true}
              shownBy="model_state/has_sql_conn_failed" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details - Optional">
          <HX.Collection with="cds"
            fields={[
            "standard_fields/broker",
            "policy_info/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Experience Rating"
        fullWidth={true}
        viewScale={0.9}
        shownBy="cds/experience_rating/show_experience_rating">
        <HX.With context={{
          "path": "cds/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="Loss History">
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection fields={[
                  "historic_premium_known",
                  "no_of_years_history"
                ]}
                  horizontal={true}
                  syncColumnWidthsKey="date" />
                <HX.Collection fields={[
                  "as_at_date",
                  {
                    "field": "as_at_date_message",
                    "shownBy": "show_date_message"
                  }
                ]}
                  horizontal={true}
                  syncColumnWidthsKey="date" />
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    "show_rc_calcs"
                  ]}
                    syncColumnWidthsKey="date" />
                  <HX.Button title="Autopopulate Premium"
                    task="fill_historic_premium_task" />
                </HX.Pane>
              </HX.Pane>
              <HX.Notes field="expiring_claims_msg"
                stretch={true} />
            </HX.Pane>
            <HX.Table data={[
              "claims"
            ]}
              fields={[
              "yoa",
              null,
              {
                "field": "hull_portfolio_rc",
                "shownBy": "show_rc_calcs"
              },
              {
                "field": "liab_portfolio_rc",
                "shownBy": "show_rc_calcs"
              },
              {
                "field": "hull_rc_to_use",
                "shownBy": "show_rc_calcs"
              },
              {
                "field": "liab_rc_to_use",
                "shownBy": "show_rc_calcs"
              },
              {
                "field": "hull_cumul_rc",
                "shownBy": "show_rc_calcs"
              },
              {
                "field": "liab_cumul_rc",
                "shownBy": "show_rc_calcs"
              },
              {
                "field": "years_to_inception",
                "shownBy": "show_rc_calcs"
              },
              {
                "field": "hull_inflation",
                "shownBy": "show_rc_calcs"
              },
              {
                "field": "liab_inflation",
                "shownBy": "show_rc_calcs"
              },
              {
                "field": null,
                "shownBy": "show_rc_calcs"
              },
              "hull_attr_claims",
              "hull_large_losses",
              "hull_gross_premium",
              "hull_exposure_adj",
              "hull_rate_change",
              "hull_as_if_premium",
              "hull_pct_developed",
              "hull_ult_attr_claims",
              "hull_ulr",
              "liab_attr_claims",
              "liab_large_losses",
              "liab_gross_premium",
              "liab_exposure_adj",
              "liab_rate_change",
              "liab_as_if_premium",
              "liab_pct_developed",
              "liab_ult_attr_claims",
              "liab_ulr"
            ]}
              kb-interactive={true}
              freezeLeft={1} />
          </HX.Section>
          <HX.Section title="Results">
            <HX.Pane flow="right">
              <HX.Table title="Large Loss Loading"
                data={[
                "hull",
                "liability"
              ]}
                fields={[
                "max_insured_loss",
                "implied_lllr",
                "implied_rp",
                null,
                "large_loss_loading"
              ]}
                kb-interactive={true}
                transpose={true}
                syncColumnWidthsKey="experience" />
              <HX.Table title="Summary"
                data={[
                "hull",
                "liability"
              ]}
                fields={[
                "actual_no_of_years",
                null,
                "quoted_premium",
                "implied_attr_lr",
                {
                  "field": "large_loss_loading",
                  "labelBy": "hull/ll_loading_label"
                },
                null,
                "expected_lr",
                {
                  "field": "expected_claims",
                  "labelBy": "hull/expected_claims_label"
                },
                "credibility"
              ]}
                kb-interactive={true}
                transpose={true}
                syncColumnWidthsKey="experience" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Airlines Details"
        shownBy="model_state/show_airlines"
        fullWidth={true}
        viewScale={0.8}>
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="Operator Details">
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    "operator_search"
                  ]} />
                  <HX.Button title="Search for Operator"
                    task="search_for_operator_task" />
                  <HX.Notes field="operators_msg"
                    shownBy="are_operators_fetched" />
                </HX.Pane>
                <HX.Table data={[
                  "operators"
                ]}
                  fields={[
                  "operator",
                  "operator_class"
                ]}
                  kb-interactive={true} />
                <HX.Collection fields={[
                  "fleet_size",
                  "selected_operator_class"
                ]}
                  horizontal={true} />
              </HX.Pane>
              <HX.Pane>
                <HX.Table data={[
                  "status_split"
                ]}
                  fields={[
                  "in_service",
                  "storage",
                  "other"
                ]}
                  kb-interactive={true}
                  transpose={true} />
                <HX.Collection fields={[
                  "status_split_msg"
                ]}
                  shownBy="show_status_split_msg" />
                <HX.Collection fields={[
                  "show_al_pricing"
                ]} />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Default Values">
            <HX.Table data={[
              "airlines_default"
            ]}
              fields={[
              {
                "field": "include",
                "width": 120
              },
              {
                "field": "no_of_aircraft",
                "width": 120
              },
              "operator",
              "aircraft_master_series",
              "registration",
              "aircraft_status",
              "coverage",
              "attachment_date",
              "expiry_date",
              "time_in_service",
              "build_year",
              "usage",
              "primary_usage",
              "market_class",
              "russian_built",
              "operator_country",
              "operator_region",
              "total_seats",
              "previous12_months_hours",
              "operating_mtow_lb",
              "value",
              "hull_limit",
              "hull_excess",
              "hull_ccy",
              "liability_limit",
              "liability_excess",
              "liability_ccy"
            ]}
              dynamic={true}
              kb-interactive={true}
              freezeLeft={0} />
          </HX.Section>
          <HX.Section title="Airlines Details">
            <HX.Pane>
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Button task="fill_with_defaults_task"
                    title="Autopopulate Default Values"
                    shownBy="/sql_db/are_regs_selected" />
                  <HX.Button task="fetch_by_operator_task"
                    title="Autopopulate from Cirium by Above Selected Operator"
                    shownBy="/sql_db/are_regs_selected" />
                  <HX.Button task="fetch_by_registration_task"
                    title="Autopopulate from Cirium by Registration"
                    shownBy="/sql_db/are_regs_selected" />
                  <HX.Button task="clear_table_task"
                    title="Clear Below"
                    shownBy="/sql_db/are_regs_selected" />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    {
                      "datum": "hull_premium",
                      "infoBy": "hull_premium/difference_msg"
                    }
                  ]}
                    fields={[
                    {
                      "field": "from_slip",
                      "width": 150
                    },
                    {
                      "field": "from_rate",
                      "shownBy": "hull_premium/are_premiums_equal",
                      "width": 150
                    },
                    {
                      "field": "from_rate.red",
                      "shownBy": "hull_premium/are_premiums_different",
                      "width": 150
                    }
                  ]}
                    kb-interactive={true}
                    shownBy="/sql_db/are_regs_selected" />
                  <HX.Collection fields={[
                    "show_check_cols",
                    "data_check"
                  ]}
                    shownBy="/sql_db/are_regs_selected"
                    horizontal={true} />
                  <HX.Notes field="has_duplicate_regs_msg"
                    shownBy="has_duplicate_regs" />
                  <HX.Notes field="has_missing_regs_msg"
                    shownBy="has_missing_regs" />
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Notes field="/sql_db/duplicate_regs_msg"
                  shownBy="/sql_db/has_duplicate_regs" />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table shownBy="/sql_db/has_duplicate_regs"
                data={[
                "/sql_db/duplicate_regs"
              ]}
                fields={[
                {
                  "field": "is_selected",
                  "width": 100
                },
                {
                  "field": "registration",
                  "width": 200
                },
                {
                  "field": "aircraft_family",
                  "width": 300
                },
                {
                  "field": "operator",
                  "width": 300
                },
                {
                  "field": "serial_number",
                  "width": 200
                }
              ]}
                dynamic={true}
                kb-interactive={true} />
              <HX.Pane flow="right">
                <HX.Button task="get_selected_regs_task"
                  title="Keep selected"
                  shownBy="/sql_db/is_at_least_one_reg_selected" />
                <HX.Notes field="/sql_db/duplicate_regs_selected_msg"
                  shownBy="/sql_db/are_duplicate_regs_selected" />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table shownBy="show_full_table"
                data={[
                "airlines"
              ]}
                fields={[
                {
                  "field": "include",
                  "width": 120
                },
                {
                  "field": "no_of_aircraft",
                  "width": 120
                },
                "operator",
                "aircraft_master_series",
                "registration",
                "aircraft_status",
                "coverage",
                "attachment_date",
                "expiry_date",
                "time_in_service",
                "build_year",
                "usage",
                "primary_usage",
                "market_class",
                "russian_built",
                "operator_country",
                "operator_region",
                "total_seats",
                "previous12_months_hours",
                "operating_mtow_lb",
                "value",
                "hull_limit",
                "hull_excess",
                "hull_ccy",
                "liability_limit",
                "liability_excess",
                "liability_ccy",
                {
                  "field": "pll_award",
                  "width": 135
                },
                {
                  "field": "tpl_limit_exposed",
                  "width": 120
                },
                {
                  "field": "achieved_hull_rate",
                  "width": 120
                }
              ]}
                dynamic={true}
                kb-interactive={true}
                maxListVisibleRows={20}
                freezeLeft={1} />
              <HX.Table title="Only rows with invalid entries are shown. Click on 'Validate Data' again to return to the full table."
                shownBy="show_validation_table"
                data={[
                "airlines"
              ]}
                fields={[
                {
                  "field": "include",
                  "width": 120
                },
                {
                  "field": "no_of_aircraft",
                  "width": 120
                },
                {
                  "field": "no_of_aircraft_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/no_of_aircraft_check_label"
                },
                "operator",
                "aircraft_master_series",
                "registration",
                "aircraft_status",
                "coverage",
                "attachment_date",
                {
                  "field": "attachment_date_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/attachment_date_check_label"
                },
                "expiry_date",
                {
                  "field": "expiry_date_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/expiry_date_check_label"
                },
                "time_in_service",
                {
                  "field": "time_in_service_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/time_in_service_check_label"
                },
                "build_year",
                {
                  "field": "build_year_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/build_year_check_label"
                },
                "usage",
                "primary_usage",
                "market_class",
                "russian_built",
                "operator_country",
                "operator_region",
                "total_seats",
                {
                  "field": "total_seats_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/total_seats_check_label"
                },
                "previous12_months_hours",
                {
                  "field": "previous12_months_hours_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/previous12_months_hours_check_label"
                },
                "operating_mtow_lb",
                {
                  "field": "operating_mtow_lb_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/operating_mtow_lb_check_label"
                },
                "value",
                {
                  "field": "value_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/value_check_label"
                },
                "hull_limit",
                {
                  "field": "hull_limit_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/hull_limit_check_label"
                },
                "hull_excess",
                {
                  "field": "hull_excess_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/hull_excess_check_label"
                },
                "hull_ccy",
                "liability_limit",
                {
                  "field": "liability_limit_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/liability_limit_check_label"
                },
                "liability_excess",
                {
                  "field": "liability_excess_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/liability_excess_check_label"
                },
                "liability_ccy",
                {
                  "field": "pll_award",
                  "width": 135
                },
                {
                  "field": "pll_award_check",
                  "labelBy": "/cds/exposure/granular/airlines_check_col_labels/pll_award_check_label"
                },
                {
                  "field": "tpl_limit_exposed",
                  "width": 120
                },
                {
                  "field": "achieved_hull_rate",
                  "width": 120
                }
              ]}
                dynamic={true}
                kb-interactive={true}
                maxListVisibleRows={20}
                freezeLeft={1}
                filter="has_error" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Aircraft Details"
        shownBy="model_state/show_ga"
        fullWidth={true}
        viewScale={0.8}>
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="Operator Details">
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    "operator_search"
                  ]} />
                  <HX.Button title="Search for Operator"
                    task="search_for_operator_task" />
                  <HX.Notes field="operators_msg"
                    shownBy="are_operators_fetched" />
                </HX.Pane>
                <HX.Table data={[
                  "operators"
                ]}
                  fields={[
                  "operator"
                ]}
                  kb-interactive={true} />
                <HX.Collection fields={[
                  "fleet_size",
                  "show_ga_pricing"
                ]}
                  horizontal={true} />
              </HX.Pane>
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Default Values and Totals">
            <HX.Table data={[
              "aircrafts_default"
            ]}
              fields={[
              "include",
              "aircraft_class",
              "number_of_engines",
              "operator",
              "aircraft_master_series",
              "no_of_aircraft",
              "registration",
              "value",
              "hull_ccy",
              "attachment_date",
              "expiry_date",
              "time_in_service",
              "build_location",
              "build_year",
              "operator_country",
              "operator_region",
              "use",
              "per_occ_deductible_pct",
              "per_occ_deductible",
              "pax_net_worth",
              "total_seats",
              "crew_seats",
              "seat_occupancy",
              "fatality",
              "per_pax_liab_limit",
              "combined_single_limit",
              "liability_ccy",
              "tpl_limit_exposed",
              "achieved_hull_rate",
              null,
              "hull_benchmark_rate",
              "pax_liab_benchmark_per_seat",
              "tpl_benchmark",
              "total_hull_benchmark",
              "total_liab_benchmark",
              null,
              "renewing_aircraft",
              "bm_allocated_hull_premium",
              "bm_allocated_liab_premium"
            ]}
              dynamic={true}
              kb-interactive={true}
              freezeLeft={0} />
          </HX.Section>
          <HX.Section title="Aircraft Details">
            <HX.Pane>
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Button task="fill_with_defaults_task"
                    title="Autopopulate Default Values"
                    shownBy="/sql_db/are_regs_selected" />
                  <HX.Button task="fetch_by_operator_task"
                    title="Autopopulate from Cirium by Above Selected Operator"
                    shownBy="/sql_db/are_regs_selected" />
                  <HX.Button task="fetch_by_registration_task"
                    title="Autopopulate from Cirium by Registration"
                    shownBy="/sql_db/are_regs_selected" />
                  <HX.Button task="fill_pax_limit_implied"
                    title="Autopopulate PAX Liability Limit If Time in Service is 0%"
                    shownBy="/sql_db/are_regs_selected" />
                  <HX.Button task="clear_table_task"
                    title="Clear Below"
                    shownBy="/sql_db/are_regs_selected" />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    {
                      "datum": "hull_premium",
                      "infoBy": "hull_premium/difference_msg"
                    }
                  ]}
                    fields={[
                    {
                      "field": "from_slip",
                      "width": 150
                    },
                    {
                      "field": "from_rate",
                      "shownBy": "hull_premium/are_premiums_equal",
                      "width": 150
                    },
                    {
                      "field": "from_rate.red",
                      "shownBy": "hull_premium/are_premiums_different",
                      "width": 150
                    }
                  ]}
                    kb-interactive={true}
                    shownBy="/sql_db/are_regs_selected" />
                  <HX.Collection fields={[
                    "show_check_cols",
                    "data_check"
                  ]}
                    shownBy="/sql_db/are_regs_selected"
                    horizontal={true} />
                  <HX.Notes field="has_duplicate_regs_msg"
                    shownBy="has_duplicate_regs" />
                  <HX.Notes field="has_missing_regs_msg"
                    shownBy="has_missing_regs" />
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Notes field="/sql_db/duplicate_regs_msg"
                  shownBy="/sql_db/has_duplicate_regs" />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table shownBy="/sql_db/has_duplicate_regs"
                data={[
                "/sql_db/duplicate_regs"
              ]}
                fields={[
                {
                  "field": "is_selected",
                  "width": 100
                },
                {
                  "field": "registration",
                  "width": 200
                },
                {
                  "field": "aircraft_family",
                  "width": 300
                },
                {
                  "field": "operator",
                  "width": 300
                },
                {
                  "field": "serial_number",
                  "width": 200
                }
              ]}
                dynamic={true}
                kb-interactive={true} />
              <HX.Pane flow="right">
                <HX.Button task="get_selected_regs_task"
                  title="Keep selected"
                  shownBy="/sql_db/is_at_least_one_reg_selected" />
                <HX.Notes field="/sql_db/duplicate_regs_selected_msg"
                  shownBy="/sql_db/are_duplicate_regs_selected" />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table shownBy="show_full_table"
                data={[
                "aircrafts"
              ]}
                fields={[
                "include",
                "aircraft_class",
                "number_of_engines",
                "operator",
                "aircraft_master_series",
                "no_of_aircraft",
                "registration",
                "value",
                "hull_ccy",
                "attachment_date",
                "expiry_date",
                "time_in_service",
                "build_location",
                "build_year",
                "operator_country",
                "operator_region",
                "use",
                "per_occ_deductible_pct",
                "per_occ_deductible",
                "pax_net_worth",
                "total_seats",
                "crew_seats",
                "seat_occupancy",
                "fatality",
                "per_pax_liab_limit",
                "combined_single_limit",
                "liability_ccy",
                "tpl_limit_exposed",
                "achieved_hull_rate",
                null,
                "hull_benchmark_rate",
                "pax_liab_benchmark_per_seat",
                "tpl_benchmark",
                "total_hull_benchmark",
                "total_liab_benchmark",
                null,
                "renewing_aircraft",
                "bm_allocated_hull_premium",
                "bm_allocated_liab_premium"
              ]}
                dynamic={true}
                kb-interactive={true}
                maxListVisibleRows={20}
                freezeLeft={1} />
              <HX.Table title="Only rows with invalid entries are shown. Click on 'Validate Data' again to return to the full table."
                shownBy="show_validation_table"
                data={[
                "aircrafts"
              ]}
                fields={[
                "include",
                "aircraft_class",
                {
                  "field": "aircraft_class_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/aircraft_class_check_label"
                },
                "number_of_engines",
                "operator",
                "aircraft_master_series",
                "no_of_aircraft",
                {
                  "field": "no_of_aircraft_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/no_of_aircraft_check_label"
                },
                "registration",
                "value",
                {
                  "field": "value_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/value_check_label"
                },
                "hull_ccy",
                "attachment_date",
                {
                  "field": "attachment_date_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/attachment_date_check_label"
                },
                "expiry_date",
                {
                  "field": "expiry_date_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/expiry_date_check_label"
                },
                "time_in_service",
                {
                  "field": "time_in_service_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/time_in_service_check_label"
                },
                "build_location",
                "build_year",
                {
                  "field": "build_year_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/build_year_check_label"
                },
                "operator_country",
                {
                  "field": "operator_country_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/operator_country_check_label"
                },
                "operator_region",
                "use",
                {
                  "field": "use_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/use_check_label"
                },
                "per_occ_deductible_pct",
                {
                  "field": "per_occ_deductible_pct_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/per_occ_deductible_pct_check_label"
                },
                "per_occ_deductible",
                {
                  "field": "per_occ_deductible_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/per_occ_deductible_check_label"
                },
                "pax_net_worth",
                "total_seats",
                {
                  "field": "total_seats_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/total_seats_check_label"
                },
                "crew_seats",
                {
                  "field": "crew_seats_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/crew_seats_check_label"
                },
                "seat_occupancy",
                "fatality",
                "per_pax_liab_limit",
                {
                  "field": "per_pax_liab_limit_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/per_pax_liab_limit_check_label"
                },
                "combined_single_limit",
                {
                  "field": "combined_single_limit_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/combined_single_limit_check_label"
                },
                "liability_ccy",
                "tpl_limit_exposed",
                {
                  "field": "tpl_limit_exposed_check",
                  "labelBy": "/cds/exposure/granular/ga_check_col_labels/tpl_limit_exposed_check_label"
                },
                "achieved_hull_rate",
                null,
                "hull_benchmark_rate",
                "pax_liab_benchmark_per_seat",
                "tpl_benchmark",
                "total_hull_benchmark",
                "total_liab_benchmark",
                null,
                "renewing_aircraft",
                "bm_allocated_hull_premium",
                "bm_allocated_liab_premium"
              ]}
                dynamic={true}
                kb-interactive={true}
                maxListVisibleRows={20}
                freezeLeft={1}
                filter="has_error" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Airlines Rating"
        fullWidth={true}
        viewScale={0.8}
        shownBy="cds/exposure/granular/show_al_pricing">
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="Hull, PAX & TPL Liability Modelling">
            <HX.Pane>
              <HX.Table title="Summary"
                data={[
                "airlines_rating_summary"
              ]}
                fields={[
                "fleet_size",
                "hull_loss_cost",
                "total_seats",
                "pax_loss_cost",
                "tpl_loss_cost",
                "hull_large_severity",
                "liab_large_severity"
              ]} />
              <HX.Table title="Aircrafts"
                data={[
                "airlines_rating"
              ]}
                fields={[
                "include",
                {
                  "field": "no_of_aircraft",
                  "width": 125
                },
                "registration",
                "value_usd",
                "coverage",
                "attachment_date",
                "expiry_date",
                "usage",
                "market_class",
                "build_year",
                "aircraft_status",
                "previous12_months_hours",
                "operator_region",
                "russian_built",
                "total_seats",
                "operating_mtow_lb",
                null,
                "hull_f_base",
                "hull_f_status",
                "hull_f_operator_region",
                "hull_f_previous12_months_hours",
                "hull_f_market_class",
                "hull_f_build_year_group",
                "hull_f_build_year",
                "hull_f_usage",
                "hull_frequency",
                null,
                "hull_s_base",
                "hull_s_previous12_months_hours",
                "hull_s_market_class",
                "hull_s_russian_built",
                "hull_s_mtow",
                "hull_s_build_year_group",
                "hull_s_build_year",
                "hull_severity",
                null,
                "hull_low_value_load",
                "hull_fleet_adj",
                "hull_attr_uplift",
                "hull_loss_cost_gu_usd",
                "hull_limit_point",
                "hull_excess_point",
                "hull_limit_usd",
                "hull_excess_usd",
                "hull_loss_cost_usd",
                null,
                "pax_seats_in_service",
                "pax_base_freq_year_built",
                "pax_status",
                "pax_operator_region",
                "pax_12_months_hours",
                "pax_market_class",
                "pax_severity_per_seat_usd",
                "pax_attr_uplift",
                "pax_liability_per_seat",
                "pax_fleet_adj",
                "pax_loss_cost_gu_usd",
                "pax_limit_point",
                "pax_attachment_point",
                "liability_limit_usd",
                "liability_excess_usd",
                "pax_loss_cost_usd",
                null,
                "tpl_liab_limit_exposed",
                "tpl_usage",
                "tpl_rate_on_limit",
                "tpl_base_loss_cost_usd",
                "tpl_fleet_adj",
                "tpl_loss_cost_usd",
                null,
                "bm_term_adj",
                "bm_hull_large_loss_cost",
                "bm_hull_large_severity",
                "bm_liab_large_frequency",
                "bm_liab_large_loss_cost",
                "bm_liab_large_severity",
                "bm_hull_benchmark",
                "bm_hull_benchmark_rate",
                "bm_pax_liab_benchmark_cost",
                "bm_pax_liability_per_seat",
                "bm_tpl_benchmark",
                "bm_allocated_hull_premium",
                "bm_aircraft_in_expiry_fleet",
                "bm_total_liab_premium",
                "bm_allocated_liab_premium"
              ]}
                dynamic={true}
                kb-interactive={true}
                freezeLeft={1} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Total & Partial Loss Freq"
        fullWidth={true}
        viewScale={0.8}
        shownBy="cds/exposure/granular/show_ga_pricing">
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="Total Loss Frequency Calculation">
            <HX.Pane>
              <HX.Table title="Aircrafts"
                data={[
                "ga_rating"
              ]}
                fields={[
                "include",
                "aircraft_class",
                "base_rate",
                {
                  "field": "no_of_aircraft",
                  "width": 125
                },
                "base_freq_all_aircraft",
                "hull_value_usd",
                "hull_value_adjuster",
                "time_in_service",
                "status_adjuster",
                "build_location",
                "build_location_adjuster",
                "freq_region",
                "use",
                "use_adjuster",
                "region_adjuster",
                "fleet_size",
                "fleet_size_adjuster",
                "exp_total_losses",
                "exp_partial_losses"
              ]}
                dynamic={true}
                kb-interactive={true}
                freezeLeft={1} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Hull Rating"
        fullWidth={true}
        viewScale={0.8}
        shownBy="cds/exposure/granular/show_ga_pricing">
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="Hull Rating Calculation">
            <HX.Pane>
              <HX.Table title="Aircrafts"
                data={[
                "ga_rating"
              ]}
                fields={[
                "include",
                "exp_total_losses",
                "exp_partial_losses",
                "hull_value_usd",
                "hull_per_occ_deductible_usd",
                "hull_severity",
                "hull_partial_base_severity",
                "hull_partial_engine_adjuster",
                "hull_partial_build_year_adjuster",
                "hull_total_loss_unadjusted",
                "hull_partial_loss_unadjusted",
                "hull_expected_loss_unadjusted",
                "hull_attritional_adjuster",
                "bm_term_adj",
                "hull_expected_loss",
                "hull_benchmark_cost",
                "hull_net_rate",
                "hull_benchmark_rate"
              ]}
                dynamic={true}
                kb-interactive={true}
                freezeLeft={1} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="PAX Rating"
        fullWidth={true}
        viewScale={0.8}
        shownBy="cds/exposure/granular/show_ga_pricing">
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="PAX Liability Rating Calculation">
            <HX.Pane>
              <HX.Table title="Aircrafts"
                data={[
                "ga_rating"
              ]}
                fields={[
                "include",
                "pax_exp_total_losses",
                "total_seats_all_aircraft",
                "total_seats",
                "seat_occupancy",
                "fatality",
                "exp_no_of_deaths",
                "operator_region",
                "pax_award_usd",
                "pax_limit_usd",
                "apply_pax_limit",
                "gu_pax_losses",
                "max_pax_losses",
                "pax_per_occ_limit_usd",
                "pax_apply_occ_limit_ded",
                "pax_apply_occ_limit_ded_to_max_loss",
                "pax_exp_loss_from_total_losses",
                "pax_attritional_adjuster",
                "bm_term_adj",
                "pax_expected_loss",
                "pax_benchmark_cost",
                "pax_benchmark_per_seat"
              ]}
                dynamic={true}
                kb-interactive={true}
                freezeLeft={1} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="TPL Rating"
        fullWidth={true}
        viewScale={0.8}
        shownBy="cds/exposure/granular/show_ga_pricing">
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="TP Liability Rating Calculation">
            <HX.Pane>
              <HX.Table title="Aircrafts"
                data={[
                "ga_rating"
              ]}
                fields={[
                "include",
                "no_of_aircraft",
                "tpl_limit_usd",
                "tpl_limit_exposed",
                "tpl_net_rol_exposed",
                "tpl_net_rol_unexposed",
                "tpl_expected_loss_unadjusted",
                "fleet_size",
                "fleet_size_adjuster",
                "bm_term_adj",
                "tpl_expected_loss",
                "tpl_benchmark_cost",
                "tpl_net_rate",
                "tpl_gross_rate"
              ]}
                dynamic={true}
                kb-interactive={true}
                freezeLeft={1} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Aircraft Summary"
        fullWidth={true}
        viewScale={0.8}
        shownBy="cds/exposure/granular/show_aircraft_summary">
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="Rating Summary by Aircraft">
            <HX.Pane>
              <HX.Table data={[
                "aircraft_summary_total",
                null,
                "aircraft_summary"
              ]}
                fields={[
                {
                  "field": "include",
                  "width": 120
                },
                {
                  "field": "no_of_aircraft",
                  "width": 120
                },
                {
                  "field": "market_class",
                  "shownBy": "/cds/is_airlines",
                  "width": 225
                },
                {
                  "field": "aircraft_class",
                  "shownBy": "/cds/is_ga",
                  "width": 225
                },
                {
                  "field": "registration",
                  "width": 175
                },
                {
                  "field": "hull_value",
                  "width": 125
                },
                {
                  "field": "hull_benchmark",
                  "width": 125
                },
                {
                  "field": "hull_benchmark_rate",
                  "width": 125
                },
                {
                  "field": "pax_limit",
                  "width": 125
                },
                {
                  "field": "pax_liab_benchmark",
                  "width": 125
                },
                {
                  "field": "pax_liab_benchmark_per_seat",
                  "width": 125
                },
                {
                  "field": "tpl_benchmark",
                  "width": 125
                },
                {
                  "field": "total_hull_benchmark",
                  "width": 125
                },
                {
                  "field": "total_liab_benchmark",
                  "width": 125
                },
                {
                  "field": "total_benchmark",
                  "width": 125
                }
              ]}
                dynamic={true}
                kb-interactive={true}
                freezeLeft={1} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rating Summary"
        shownBy="cds/exposure/granular/all_fields_valid">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Section title="Cover">
            <HX.Table with="coverages"
              data={[
              "hull",
              "liability/pax",
              "liability/tpl"
            ]}
              fields={[
              "benchmark_premium_pre_exp",
              "benchmark_rate_pre_exp"
            ]}
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
          <HX.Section title="Experience Rating">
            <HX.Table with="coverages"
              data={[
              "hull",
              "liability"
            ]}
              fields={[
              "benchmark_premium_exp",
              "exp_credibility",
              {
                "field": "benchmark_premium_pre_uw_adj",
                "infoBy": "liability/min_rate_info"
              }
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="pre-adj" />
          </HX.Section>
          <HX.Section title="Underwriter Adjustments">
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "pilot_uw_adj",
                "coverages/hull/uw_adj",
                "coverages/liability/uw_adj"
              ]} />
              <HX.Notes title="UW Rationale"
                field="/cds/standard_fields/uw_rationale"
                stretch={true} />
            </HX.Pane>
            <HX.Table with="coverages"
              data={[
              "hull",
              "liability"
            ]}
              fields={[
              "benchmark_premium_post_uw_adj",
              "uw_adj_impact"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="pre-adj" />
          </HX.Section>
          <HX.Section title="BPI - Premium for Policy Term">
            <HX.Table data={[
              "coverages/hull",
              "coverages/liability",
              "totals"
            ]}
              fields={[
              "benchmark_premium",
              "quoted_premium",
              null,
              "pflr",
              "pflr_net",
              "bpi",
              null,
              "business_plan_bpi",
              "roc_bpi"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="summary" />
          </HX.Section>
          <HX.Section title="TPI - Premium for Policy Term">
            <HX.Table data={[
              "coverages/hull",
              "coverages/liability",
              "totals"
            ]}
              fields={[
              "technical_premium",
              "technical_premium_pre_uw_adj",
              null,
              "tpi",
              "tpi_pre_uw_adj"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="summary" />
          </HX.Section>
        </HX.With>
        <HX.Section title="Overall Summary">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "section_reference",
              "status",
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
              "benchmark_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "tpi",
              "tpi_pre_uw_adj",
              "bpi",
              "pflr",
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
              "quoted_premium_case_priced",
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
        <HX.Section title="Summary Document">
          <HX.Pane>
            <HX.Collection with="policy_doc"
              fields={[
              "premium_check"
            ]}
              shownBy="show_premium_check" />
            <HX.Button title="Generate Quote Summary"
              task="quote_to_excel_task"
              shownBy="policy_doc/show_generate_button" />
            <HX.File with="policy_doc"
              field="output_file"
              title="Click on the icon below to download the summary document"
              shownBy="show_download" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={true}
        shownBy="cds/exposure/granular/show_rc_page"
        viewScale={0.9}>
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id"
            ]} />
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane />
        </HX.Section>
        <HX.Section title="Renewal"
          shownBy="cds/rate_change/show_layer_1">
          <HX.Pane flow="right">
            <HX.Button task="rarc_task"
              title="Calculate Rate Change"
              shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Pane />
          </HX.Pane>
          <HX.Notes with="cds/rate_change"
            field="reg_warning"
            shownBy="show_reg_warning" />
          <HX.Notes with="cds/rate_change"
            field="rarc_run_again_message"
            shownBy="rarc_message_show" />
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table title="Hull"
                data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                {
                  "datum": "benchmark_premium_post_uw_adj",
                  "elementInfoBy": "/cds/rate_change/pre_nmp_calculation_msg"
                },
                "benchmark_premium",
                "bpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                }
              ]}
                with="rate_change/hull"
                shownBy="/cds/exposure/granular/show_aircraft_summary"
                kb-interactive={true} />
              <HX.Table title="Liability"
                data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                {
                  "datum": "benchmark_premium_post_uw_adj",
                  "elementInfoBy": "/cds/rate_change/pre_nmp_calculation_msg"
                },
                "benchmark_premium",
                "bpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                }
              ]}
                with="rate_change/liability"
                shownBy="/cds/exposure/granular/show_aircraft_summary"
                kb-interactive={true} />
              <HX.Table title="Hull"
                data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                "benchmark_premium",
                "bpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                }
              ]}
                with="rate_change/hull"
                shownBy="/cds/exposure/granular/hide_aircraft_summary"
                kb-interactive={true} />
              <HX.Table title="Liability"
                data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                "benchmark_premium",
                "bpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                }
              ]}
                with="rate_change/liability"
                shownBy="/cds/exposure/granular/hide_aircraft_summary"
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/rate_change/rarc_calcs_show"
              flow="right">
              <HX.Pane>
                <HX.Table title="Hull Rate Change"
                  shownBy="/cds/standard_fields/is_rater_priced"
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
                    "width": 125
                  },
                  {
                    "field": "uw_selected",
                    "width": 125
                  },
                  {
                    "field": "comments",
                    "width": 250
                  }
                ]}
                  with="rate_change/hull"
                  kb-interactive={true} />
                <HX.Collection title="Hull Final Rate Change (Gross Brokerage)"
                  with="rate_change"
                  fields={[
                  "hull/risk_adjusted_rate_change/uw_selected",
                  null
                ]}
                  horizontal={true}
                  shownBy="/cds/standard_fields/is_rater_priced" />
              </HX.Pane>
              <HX.Pane>
                <HX.Table title="Liability Rate Change"
                  shownBy="/cds/standard_fields/is_rater_priced"
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
                    "width": 125
                  },
                  {
                    "field": "uw_selected",
                    "width": 125
                  },
                  {
                    "field": "comments",
                    "width": 250
                  }
                ]}
                  with="rate_change/liability"
                  kb-interactive={true} />
                <HX.Collection title="Liability Final Rate Change (Gross Brokerage)"
                  with="rate_change"
                  fields={[
                  "liability/risk_adjusted_rate_change/uw_selected",
                  null
                ]}
                  horizontal={true}
                  shownBy="/cds/standard_fields/is_rater_priced" />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Rate Change"
          shownBy="/cds/standard_fields/is_case_priced">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection title="Hull Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={[
                "hull/risk_adjusted_rate_change_case_priced/uw_selected",
                null
              ]}
                horizontal={true} />
              <HX.Collection title="Liability Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={[
                "liability/risk_adjusted_rate_change_case_priced/uw_selected",
                null
              ]}
                horizontal={true} />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]} />
            </HX.Pane>
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