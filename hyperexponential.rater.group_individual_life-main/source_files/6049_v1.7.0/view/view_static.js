
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
        <HX.Section title="Rating Methodology">
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
              "insured_name"
            ]}
              with="cds/standard_fields"
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
        <HX.Section title="Policy Information">
          <HX.Pane shownBy="cds/is_group">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection title="Details"
                fields={[
                "written_line_input",
                {
                  "field": "brokerage",
                  "labelBy": "brokerage_label"
                },
                "/cds/policy_info/direct_ri"
              ]}
                horizontal={true} />
              <HX.Collection title="Aggregate Limits"
                fields={[
                "aggregate_limit",
                "aggregate_deductible"
              ]}
                horizontal={true} />
            </HX.With>
            <HX.Collection with="cds/policy_info"
              title="Profit Commission"
              fields={[
              "has_profit_commission",
              "pc_to_gross"
            ]}
              horizontal={true} />
            <HX.Collection with="cds/policy_info"
              fields={[
              "profit_commission",
              "pc_expenses",
              "pc_deficit"
            ]}
              horizontal={true} />
            <HX.Collection with="cds/policy_info"
              title="No Claims Bonus"
              fields={[
              "has_no_claims_bonus",
              "ncb_pct",
              "ncb_to_gross"
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane shownBy="cds/is_individual">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                {
                  "field": "brokerage",
                  "labelBy": "brokerage_label"
                },
                "brokerage_ri"
              ]}
                horizontal={true} />
            </HX.With>
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
      <HX.Page title="coverage"
        shownBy="model_state/show_group">
        <HX.Section title="Group Life - Benefits Covered">
          <HX.Pane flow="right">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection title="Death"
                with="coverages"
                fields={[
                "death/cover_type",
                "additional_death/is_covered",
                "death/accidental_death_adj",
                "death/sick_affluence",
                "death/sick_weight_to_nationality",
                "death/accidental_death_rate"
              ]}
                numCols={2} />
              <HX.Pane flow="right">
                <HX.Collection title="Terminal illness"
                  with="coverages/terminal_illness"
                  fields={[
                  "is_covered"
                ]}
                  numCols={2} />
                <HX.Pane />
              </HX.Pane>
              <HX.Collection title="Critical illness (covers 6 illnesses)"
                with="coverages/critical_illness"
                fields={[
                "is_covered",
                "benefit",
                {
                  "field": "benefit_amount_fixed",
                  "shownBy": "show_benefit_amount"
                },
                {
                  "field": "benefit_amount_pct",
                  "shownBy": "show_benefit_pct"
                },
                {
                  "field": "cap_amount",
                  "shownBy": "show_benefit_pct"
                },
                {
                  "field": "cap_pct",
                  "shownBy": "show_benefit_amount"
                }
              ]}
                numCols={2} />
              <HX.Collection title="Repatriation expenses"
                with="coverages/repat_exp"
                fields={[
                "is_covered",
                "limit"
              ]}
                numCols={2} />
            </HX.With>
            <HX.Collection title="Historical claims experience"
              with="cds/experience_rating"
              fields={[
              "claims_available",
              null
            ]}
              numCols={2} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Premium"
        fullWidth={true}
        viewScale={0.9}
        shownBy="model_state/show_premium_group">
        <HX.Section title="Premium Calculations">
          <HX.Pane flow="right" />
          <HX.Pane>
            <HX.With context={{
              "path": "cds/exposure/granular",
              "type": "struct"
            }}>
              <HX.Collection fields={[
                "show_check_cols",
                "show_exposure_map",
                null,
                null
              ]}
                horizontal={true}
                syncColumnWidthsKey="aboveTable" />
              <HX.Pane flow="right">
                <HX.Table data={[
                  "/cds/exposure/granular"
                ]}
                  fields={[
                  "data_check",
                  "region_warning",
                  "country_finder"
                ]}
                  kb-interactive={true}
                  rowHeaderSettings={{
                  "width": 50
                }} />
                <HX.Pane />
              </HX.Pane>
              <HX.Table data={[
                "lives"
              ]}
                fields={[
                {
                  "field": "no_lives",
                  "width": 100
                },
                {
                  "field": "no_lives_check",
                  "labelBy": "check_col_labels/no_lives_check_label",
                  "shownBy": "show_check_cols",
                  "width": 100
                },
                {
                  "field": "sex",
                  "width": 100
                },
                {
                  "field": "sex_check",
                  "labelBy": "check_col_labels/sex_check_label",
                  "shownBy": "show_check_cols",
                  "width": 100
                },
                {
                  "field": "age_attained",
                  "width": 110
                },
                {
                  "field": "age_attained_check",
                  "labelBy": "check_col_labels/age_attained_check_label",
                  "shownBy": "show_check_cols",
                  "width": 100
                },
                {
                  "field": "salary",
                  "width": 150
                },
                {
                  "field": "salary_check",
                  "labelBy": "check_col_labels/salary_check_label",
                  "shownBy": "show_check_cols",
                  "width": 100
                },
                {
                  "field": "salary_multiple",
                  "width": 100
                },
                {
                  "field": "salary_multiple_check",
                  "labelBy": "check_col_labels/salary_multiple_check_label",
                  "shownBy": "show_check_cols",
                  "width": 100
                },
                {
                  "field": "sum_insured",
                  "width": 150
                },
                {
                  "field": "sum_insured_check",
                  "labelBy": "check_col_labels/sum_insured_check_label",
                  "shownBy": "show_check_cols",
                  "width": 100
                },
                {
                  "field": "nationality",
                  "width": 200
                },
                {
                  "field": "nationality_check",
                  "labelBy": "check_col_labels/nationality_check_label",
                  "shownBy": "show_check_cols",
                  "width": 100
                },
                {
                  "field": "location",
                  "width": 200
                },
                {
                  "field": "location_check",
                  "labelBy": "check_col_labels/location_check_label",
                  "shownBy": "show_check_cols",
                  "width": 100
                },
                {
                  "field": "region",
                  "width": 200
                },
                {
                  "field": "region_check",
                  "labelBy": "check_col_labels/region_check_label",
                  "shownBy": "show_check_cols",
                  "width": 150
                },
                {
                  "field": "occupation_code",
                  "width": 130
                },
                {
                  "field": "occupation_code_check",
                  "labelBy": "check_col_labels/occupation_code_check_label",
                  "shownBy": "show_check_cols",
                  "width": 100
                },
                null,
                {
                  "field": "db_qx",
                  "width": 125
                },
                {
                  "field": "db_expected_loss_cost_pre_uw_adj",
                  "width": 125
                },
                {
                  "field": "db_technical_premium_pre_uw_adj",
                  "width": 125
                },
                {
                  "field": "db_expected_loss_cost",
                  "width": 125
                },
                {
                  "field": "db_technical_premium",
                  "width": 125
                },
                {
                  "field": null,
                  "shownBy": "show_adb"
                },
                {
                  "field": "adb_qx",
                  "shownBy": "show_adb",
                  "width": 125
                },
                {
                  "field": "adb_expected_loss_cost_pre_uw_adj",
                  "shownBy": "show_adb",
                  "width": 125
                },
                {
                  "field": "adb_technical_premium_pre_uw_adj",
                  "shownBy": "show_adb",
                  "width": 125
                },
                {
                  "field": "adb_expected_loss_cost",
                  "shownBy": "show_adb",
                  "width": 125
                },
                {
                  "field": "adb_technical_premium",
                  "shownBy": "show_adb",
                  "width": 125
                },
                {
                  "field": null,
                  "shownBy": "show_re"
                },
                {
                  "field": "re_rate",
                  "shownBy": "show_re",
                  "width": 125
                },
                {
                  "field": "re_expected_loss_cost_pre_uw_adj",
                  "shownBy": "show_re",
                  "width": 125
                },
                {
                  "field": "re_technical_premium_pre_uw_adj",
                  "shownBy": "show_re",
                  "width": 125
                },
                {
                  "field": "re_expected_loss_cost",
                  "shownBy": "show_re",
                  "width": 125
                },
                {
                  "field": "re_technical_premium",
                  "shownBy": "show_re",
                  "width": 125
                },
                {
                  "field": null,
                  "shownBy": "show_ci"
                },
                {
                  "field": "ci_cover",
                  "shownBy": "show_ci",
                  "width": 125
                },
                {
                  "field": "ci_rate",
                  "shownBy": "show_ci",
                  "width": 125
                },
                {
                  "field": "ci_sum_insured",
                  "shownBy": "show_ci",
                  "width": 125
                },
                {
                  "field": "ci_sum_insured_post_cap",
                  "shownBy": "show_ci",
                  "width": 125
                },
                {
                  "field": "ci_expected_loss_cost_pre_uw_adj",
                  "shownBy": "show_ci",
                  "width": 125
                },
                {
                  "field": "ci_technical_premium_pre_uw_adj",
                  "shownBy": "show_ci",
                  "width": 125
                },
                {
                  "field": "ci_expected_loss_cost",
                  "shownBy": "show_ci",
                  "width": 125
                },
                {
                  "field": "ci_technical_premium",
                  "shownBy": "show_ci",
                  "width": 125
                },
                {
                  "field": null,
                  "shownBy": "show_ti"
                },
                {
                  "field": "ti_cover",
                  "shownBy": "show_ti",
                  "width": 125
                },
                {
                  "field": "ti_proportion",
                  "shownBy": "show_ti",
                  "width": 125
                },
                {
                  "field": "ti_rate",
                  "shownBy": "show_ti",
                  "width": 125
                },
                {
                  "field": "ti_expected_loss_cost_pre_uw_adj",
                  "shownBy": "show_ti",
                  "width": 125
                },
                {
                  "field": "ti_technical_premium_pre_uw_adj",
                  "shownBy": "show_ti",
                  "width": 125
                },
                {
                  "field": "ti_expected_loss_cost",
                  "shownBy": "show_ti",
                  "width": 125
                },
                {
                  "field": "ti_technical_premium",
                  "shownBy": "show_ti",
                  "width": 125
                },
                null,
                {
                  "field": "no_claim_prob",
                  "width": 125
                }
              ]}
                dynamic={true}
                kb-interactive={true}
                maxListVisibleRows={20} />
            </HX.With>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Premium"
        shownBy="cds/is_individual">
        <HX.Section title="Life Details">
          <HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/exposure/granular/life",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "age_next_bday",
                "age_attained",
                "sum_insured",
                "coverage",
                "nationality",
                "location",
                "smoker_status",
                "term"
              ]}
                numCols={2} />
            </HX.With>
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "rga_load_mult",
                "rga_load_add"
              ]}
                horizontal={true} />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Premium Results">
          <HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/exposure/granular/life",
              "type": "list"
            }}>
              <HX.Collection title="Beazley to pay RGA"
                fields={[
                "rga_rate",
                "rga_premium"
              ]}
                horizontal={true} />
              <HX.Collection title="RI Brokerage"
                fields={[
                "brokerage_ri_amount",
                "gross_rga_premium"
              ]}
                horizontal={true} />
              <HX.Collection title="Beazley to charge"
                fields={[
                "bzl_rate",
                "bzl_premium"
              ]}
                horizontal={true} />
            </HX.With>
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection title="Actual quote"
                fields={[
                "quoted_rate",
                "quoted_premium_ind"
              ]}
                horizontal={true} />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rating Summary">
          <HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                {
                  "field": "expected_loss_cost",
                  "labelBy": "el_label"
                },
                "quoted_premium_net"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "benchmark_premium",
                "bpi"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "technical_premium",
                "tpi"
              ]}
                horizontal={true} />
            </HX.With>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="SI Map by Nationality"
        fullWidth={true}
        shownBy="cds/exposure/granular/show_exposure_map">
        <HX.Section title="Exposure by Nationality">
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Pane>
              <CustomComponent title="Total Sum Insured by Nationality"
                list="lives_by_nation"
                text="nationality"
                locations="country_iso3"
                z="total_sum_insured" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="SI Map by Location"
        fullWidth={true}
        shownBy="cds/exposure/granular/show_exposure_map">
        <HX.Section title="Exposure by Location">
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Pane>
              <CustomComponent title="Total Sum Insured by Location"
                list="lives_by_location"
                text="location"
                locations="country_iso3"
                z="total_sum_insured" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Experience Rating"
        fullWidth={true}
        shownBy="cds/experience_rating/claims_available">
        <HX.With context={{
          "path": "cds/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="Selections">
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection fields={[
                  "cut_off_date",
                  "death_or_all_risks"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "date_check"
                ]}
                  shownBy="date_check_show" />
              </HX.Pane>
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Claims">
            <HX.Table data={[
              "claims",
              null,
              "claims_totals"
            ]}
              fields={[
              "year",
              "no_lives",
              "sum_insured",
              "incurred",
              "number",
              "ibnr_factor",
              "time_adj",
              "burn",
              "burn_per_mille"
            ]}
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="Summary">
            <HX.Pane flow="right">
              <HX.Collection title="Credibility Metrics"
                fields={[
                "life_years",
                "cred_weight"
              ]} />
              <HX.Collection title="Z Values"
                fields={[
                "z_factor",
                "one_minus_z"
              ]} />
              <HX.Collection title="Burn Metrics"
                fields={[
                "claims_totals/burn",
                "burn_cost"
              ]} />
              <HX.Collection title="Discounts"
                fields={[
                "death_only_discount",
                "all_risk_discount"
              ]} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        shownBy="model_state/show_group">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Aggregate Limit and Deductible - Expected Loss"
            shownBy="/cds/cover_selection/are_agg_limits_full">
            <HX.Pane flow="right">
              <HX.Button title="Price for PC/NCB or (and) Agg"
                task="simulate_years_task" />
              <HX.Collection fields={[
                "temp/task_update_msg"
              ]}
                stretch={true} />
            </HX.Pane>
            <HX.Collection with="coverages/death"
              fields={[
              "el_cost_post_sim_pre_agg",
              "el_cost_post_sim",
              "agg_impact_on_el"
            ]}
              horizontal={true} />
          </HX.Section>
        </HX.With>
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
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Premium Summary"
            shownBy="/cds/standard_fields/is_rater_priced">
            <HX.Notes with="/cds/cover_selection"
              field="agg_limits_check_message"
              shownBy="agg_limits_check_show" />
            <HX.Table data={[
              {
                "datum": "coverages/death",
                "labelBy": "coverages/death/label"
              },
              "coverages/additional_death",
              "coverages/repat_exp",
              {
                "datum": "coverages/critical_illness",
                "infoBy": "coverages/critical_illness/age_info"
              },
              {
                "datum": "coverages/terminal_illness",
                "infoBy": "coverages/terminal_illness/age_info"
              },
              null,
              "totals/total_ex_pc_ncb",
              null,
              "totals/pc",
              "totals/ncb",
              null,
              "totals/total"
            ]}
              fields={[
              "el_cost_pre_uw_pre_exp",
              "el_rate_pre_uw_pre_exp",
              "uw_adj",
              "el_cost_post_uw_pre_exp",
              "el_rate_post_uw_pre_exp",
              "expected_loss_cost",
              null,
              "technical_premium",
              "technical_rate",
              "benchmark_premium",
              "benchmark_rate",
              null,
              "quoted_rate",
              "uw_adj_impact",
              "quoted_premium"
            ]}
              filter="is_covered"
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
          </HX.Section>
          <HX.Section title="Technical Summary"
            shownBy="/cds/standard_fields/is_rater_priced">
            <HX.Pane flow="right"
              shownBy="/cds/cover_selection/are_agg_limits_full">
              <HX.Button title="Price for PC/NCB or (and) Agg"
                task="simulate_years_task" />
              <HX.Notes with="/cds/cover_selection"
                field="agg_limits_check_message"
                shownBy="agg_limits_check_show"
                stretch={true} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/cds/quote/total_sum_insured",
                "total_no_lives"
              ]} />
              <HX.Collection fields={[
                "expected_pc",
                "expected_ncb"
              ]} />
              <HX.Collection fields={[
                {
                  "field": "bpi_pre_uw_adj",
                  "infoBy": "expe_adj_label"
                },
                {
                  "field": "bpi",
                  "infoBy": "expe_adj_label"
                }
              ]} />
              <HX.Collection fields={[
                {
                  "field": "tpi_pre_uw_adj",
                  "infoBy": "expe_adj_label"
                },
                {
                  "field": "tpi",
                  "infoBy": "expe_adj_label"
                }
              ]} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Summary Statistics"
            shownBy="/cds/standard_fields/is_rater_priced">
            <HX.Pane flow="right">
              <HX.Collection title="Age"
                fields={[
                "lives_wtd_avg_age",
                "si_wtd_avg_age",
                "max_age",
                "min_age"
              ]} />
              <HX.Collection title="Salary"
                fields={[
                "lives_wtd_avg_salary",
                "max_salary",
                "min_salary"
              ]} />
              <HX.Collection title="Sum Insured"
                fields={[
                "lives_wtd_avg_si",
                "max_si",
                "min_si"
              ]} />
              <HX.Collection title="Expected Values"
                fields={[
                "no_claim_prob",
                "exp_no_deaths_per_thousand",
                "exp_no_deaths",
                "avg_cost",
                "sd_cost"
              ]} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
        <HX.Section title="Technical Summary"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.Table title="Priced Quote"
            data={[
            {
              "datum": "cds/layers",
              "width": 250
            }
          ]}
            fields={[
            "status",
            "/cds/standard_fields/policy_reference",
            "brokerage",
            "written_line_input",
            null,
            "quoted_premium_case_priced",
            "technical_premium",
            "benchmark_premium",
            null,
            "tpi",
            "bpi_case_priced",
            null,
            "pflr",
            "roc"
          ]}
            freezeLeft={0}
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Notes">
          <HX.Pane flow="right">
            <HX.Notes title="Underwriter Rationale"
              field="cds/standard_fields/uw_rationale" />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Quote Summary"
        fullWidth={true}
        shownBy="model_state/show_group">
        <HX.Section title="Quote Details">
          <HX.Pane flow="right">
            <HX.Collection title="Policy Details"
              with="cds/quote"
              fields={[
              "reinsured_name",
              "insured_name",
              "cover",
              "term"
            ]} />
            <HX.Collection title="Risk Details"
              with="cds/quote"
              fields={[
              "max_age_attained",
              "no_lives",
              "sum_insured_basis",
              "max_aol_sum_insured"
            ]} />
            <HX.Collection title=" "
              with="cds/quote"
              fields={[
              "free_cover_limit",
              "total_sum_insured",
              "event_limit"
            ]} />
            <HX.Collection title="Financial Details"
              with="cds/quote"
              fields={[
              "deposit_premium",
              "adjustable_rate",
              "commission"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Terms & Conditions">
          <HX.Pane flow="right">
            <HX.Table data={[
              "cds/quote/exclusions"
            ]}
              fields={[
              {
                "field": "exclusion",
                "width": 600
              },
              {
                "field": "is_excluded",
                "width": 100
              }
            ]}
              kb-interactive={true} />
            <HX.Table data={[
              "cds/quote/conditions"
            ]}
              fields={[
              {
                "field": "condition",
                "width": 600
              },
              {
                "field": "is_included",
                "width": 100
              }
            ]}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Collection fields={[
            "cds/quote/valid_until_date",
            null,
            null
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Notes & Summary Document">
          <HX.Pane flow="right">
            <HX.Notes field="cds/quote/uw_notes" />
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
                title="Click on the icon below to download the quote summary document"
                shownBy="show_download" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        shownBy="cds/standard_fields/is_renewal">
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id"
            ]} />
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data" />
          </HX.Pane>
          <HX.Pane />
        </HX.Section>
        <HX.Section title="Renewal"
          shownBy="cds/rate_change/show_layer_1">
          <HX.Pane flow="right">
            <HX.Button task="rarc_task"
              title="Calculate Rate Change" />
            <HX.Pane />
          </HX.Pane>
          <HX.Notes with="cds/rate_change"
            field="rarc_run_again_message"
            shownBy="rarc_message_show" />
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line"
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
            <HX.Pane shownBy="/cds/rate_change/rarc_calcs_show">
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
                    "width": 125
                  },
                  {
                    "field": "uw_selected",
                    "width": 125
                  },
                  {
                    "field": "comments",
                    "width": 300
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
            </HX.Pane>
          </HX.With>
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
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]}
              shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]}
              shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_case_priced_view",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi_case_priced_view"
            ]}
              shownBy="/cds/standard_fields/is_case_priced" />
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