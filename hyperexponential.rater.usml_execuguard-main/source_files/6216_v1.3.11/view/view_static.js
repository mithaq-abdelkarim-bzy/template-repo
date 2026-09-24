
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root keyFields={[
      null,
      "cds/final_premium_summary/tpi",
      "cds/final_premium_summary/bpi",
      {
        "field": "cds/final_premium_summary/final_admitted_term_premium",
        "labelBy": "/non_cds/premium_label"
      },
      null
    ]}>
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
              "underwriter"
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
              "cds/standard_fields/is_renewal"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/is_admitted_or_surplus"
            ]} />
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "is_primary_excess"
              ]} />
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
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Insured State, Information and Coverage Elections">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/state",
              "cds/reactive_zipcode/zipcode",
              "cds/county"
            ]}
              title="Insured State" />
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "brokerage"
              ]}
                title="Brokerage Information" />
            </HX.With>
            <HX.Collection fields={[
              "cds/coverage_elections/epl",
              "cds/coverage_elections/fid",
              "cds/coverage_elections/pcl"
            ]}
              title="Coverage Elections" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Industry Information">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/industry/naics_search"
            ]} />
            <HX.Collection fields={[
              "cds/industry/mapped_sic_code"
            ]} />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/industry/class_of_business"
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Notes field="cds/industry/alert" />
            <HX.Notes field="cds/industry/wh_status" />
            <HX.Notes field="cds/industry/wh_information" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Company Ownership, State Requirements and Package Information">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/company_ownership"
            ]}
              title="Company Ownership" />
            <HX.Collection fields={[
              "cds/state_requirements/retroactive_date",
              "cds/state_requirements/prior_knowledge_date"
            ]}
              title="State Requirements" />
            <HX.Collection fields={[
              "cds/package_information/combined_single_aggregate_limit",
              "cds/package_information/package_discount"
            ]}
              title="Package Information" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Employee Count"
        fullWidth={true}
        shownBy="/non_cds/coverage_elections/epl_pcl">
        <HX.Section title="Employee Types">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Table data={[
                "cds/us_states/Alabama",
                "cds/us_states/Alaska",
                "cds/us_states/Arizona",
                "cds/us_states/Arkansas",
                "cds/us_states/California",
                "cds/us_states/Colorado",
                "cds/us_states/Connecticut",
                "cds/us_states/Delaware",
                "cds/us_states/District_of_Columbia",
                "cds/us_states/Florida",
                "cds/us_states/Georgia",
                "cds/us_states/Hawaii",
                "cds/us_states/Idaho",
                "cds/us_states/Illinois",
                "cds/us_states/Indiana",
                "cds/us_states/Iowa",
                "cds/us_states/Kansas",
                "cds/us_states/Kentucky",
                "cds/us_states/Louisiana",
                "cds/us_states/Maine",
                "cds/us_states/Maryland",
                "cds/us_states/Massachusetts",
                "cds/us_states/Michigan",
                "cds/us_states/Minnesota",
                "cds/us_states/Mississippi",
                "cds/us_states/Missouri",
                "cds/us_states/Montana",
                "cds/us_states/Nebraska",
                "cds/us_states/Nevada",
                "cds/us_states/New_Hampshire",
                "cds/us_states/New_Jersey",
                "cds/us_states/New_Mexico",
                "cds/us_states/New_York_metro",
                "cds/us_states/New_York_non_metro",
                "cds/us_states/North_Carolina",
                "cds/us_states/North_Dakota",
                "cds/us_states/Ohio",
                "cds/us_states/Oklahoma",
                "cds/us_states/Oregon",
                "cds/us_states/Pennsylvania",
                "cds/us_states/Rhode_Island",
                "cds/us_states/South_Carolina",
                "cds/us_states/South_Dakota",
                "cds/us_states/Tennessee",
                "cds/us_states/Texas",
                "cds/us_states/Utah",
                "cds/us_states/Vermont",
                "cds/us_states/Virginia",
                "cds/us_states/Washington",
                "cds/us_states/West_Virginia",
                "cds/us_states/Wisconsin",
                "cds/us_states/Wyoming",
                "cds/us_states/Total"
              ]}
                fields={[
                "fte",
                "pte"
              ]}
                title="States"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
            <HX.Pane>
              <HX.Table data={[
                "cds/split/seasonal",
                "cds/split/independent_contractors",
                "cds/split/temporary",
                "cds/split/foreign"
              ]}
                fields={[
                "head_count"
              ]}
                title="Split"
                syncColumnWidthsKey="mySyncedTables1" />
              <HX.Table data={[
                "cds/weights/high",
                "cds/weights/above_average",
                "cds/weights/moderate",
                "cds/weights/average",
                "cds/weights/below_average"
              ]}
                fields={[
                "ftes",
                "weighted_risk"
              ]}
                title="Weights"
                syncColumnWidthsKey="mySyncedTables1" />
              <HX.Collection fields={[
                "cds/total_ftes"
              ]} />
              <HX.Collection fields={[
                "cds/total_state_factor"
              ]} />
              <HX.Notes field="cds/comments"
                title="Comments" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="USML EPL Inputs"
        fullWidth={true}
        shownBy="/non_cds/is_epl_inputs">
        <HX.Section title="Admitted Modifiers">
          <HX.Table data={[
            "reactive_admitted_modifiers/risk_characteristics",
            {
              "datum": "financial_stability",
              "labelBy": "/non_cds/required_epl_row_labels/financial_stability"
            },
            {
              "datum": "loss_prevention_and_mitigation",
              "labelBy": "/non_cds/required_epl_row_labels/loss_prevention_and_mitigation"
            },
            {
              "datum": "employment_policies",
              "labelBy": "/non_cds/required_epl_row_labels/employment_policies"
            },
            "reactive_cob/class_of_business",
            "sug_class_business",
            "unionized_employees",
            "stock_option_exposure"
          ]}
            with="cds/modifiers/epl/admitted_modifiers"
            fields={[
            "description",
            "factor_selection",
            "min",
            "max"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Endorsements">
          <HX.Table data={[
            "selection",
            "factor_selection",
            "min",
            "max"
          ]}
            with="cds/modifiers/epl/endorsements"
            fields={[
            {
              "field": "punitive_damages",
              "labelBy": "/non_cds/required_epl_row_labels/punitive_damages",
              "shownBy": "/non_cds/punitive_damages_acceptable"
            },
            {
              "field": "punitive_damages.mandatory",
              "labelBy": "/non_cds/required_epl_row_labels/punitive_damages",
              "shownBy": "/non_cds/punitive_damages_not_acceptable"
            },
            "reactive_third_party_liab/third_party_liability",
            "reactive_wage_and_hour/wage_and_hour",
            "client_coverage",
            {
              "field": "ahern",
              "shownBy": "/non_cds/is_state_ca"
            },
            {
              "field": "partnership_defense",
              "shownBy": "/non_cds/is_state_ca"
            },
            {
              "field": "leaders_preferred",
              "shownBy": "/non_cds/is_leader_preferred"
            }
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Coinsurance">
          <HX.Table data={[
            "per_self_ins"
          ]}
            with="cds/modifiers/epl"
            fields={[
            "selection",
            "max_credit"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Total Admitted Modifier">
          <HX.Collection fields={[
            "cds/modifiers/epl/total_admitted_modifier"
          ]}
            syncColumnWidthsKey="mySyncedTables1" />
        </HX.Section>
        <HX.Section title="Admitted Schedule Rating"
          shownBy="/non_cds/is_state_ne_hide">
          <HX.Table data={[
            "rationale",
            "factor_selection",
            "min",
            "max"
          ]}
            fields={[
            {
              "field": "prior_claim_activity",
              "shownBy": "/non_cds/is_state_ca_or_in_hide"
            },
            {
              "field": "turnover_rate",
              "shownBy": "/non_cds/is_state_ca_or_in_hide"
            },
            {
              "field": "financial_strength",
              "shownBy": "/non_cds/is_state_ca_or_in_hide"
            },
            {
              "field": "hr_policies",
              "labelBy": "/non_cds/hr_policies_label",
              "shownBy": "/non_cds/is_state_in_hide"
            },
            {
              "field": "demographic_metro"
            },
            {
              "field": "management",
              "shownBy": "/non_cds/is_state_ca_or_in"
            },
            {
              "field": "internal_controls",
              "shownBy": "/non_cds/is_state_ca_or_in"
            },
            {
              "field": "cooperation",
              "shownBy": "/non_cds/is_state_ca_or_in"
            },
            {
              "field": "experience",
              "shownBy": "/non_cds/is_state_ca_or_in"
            },
            {
              "field": "staffing_turnover",
              "shownBy": "/non_cds/is_state_ca_or_in"
            },
            {
              "field": "salary_structure",
              "shownBy": "/non_cds/is_state_ca_or_in"
            },
            {
              "field": "stability",
              "shownBy": "/non_cds/is_state_ca"
            },
            "tot_sch_rat"
          ]}
            with="cds/modifiers/epl/admitted_schedule_rating"
            syncColumnWidthsKey="mySyncedTables1"
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="NE Deviation Factor"
          shownBy="/non_cds/is_state_ne">
          <HX.Table data={[
            "ne_deviation_factor"
          ]}
            with="cds/modifiers/epl"
            fields={[
            "rationale",
            "factor_selection",
            "min",
            "max"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Surplus Deviation"
          shownBy="/non_cds/is_surplus">
          <HX.Collection fields={[
            "cds/modifiers/epl/surplus_deviation"
          ]}
            syncColumnWidthsKey="mySyncedTables1" />
        </HX.Section>
        <HX.Section title="Benchmark UW Modifiers"
          shownBy="/non_cds/is_epl_finished_rating">
          <HX.Table data={[
            "bnch_risk_characteristics",
            "bnch_pro_claim_activity",
            "bnch_hr_policies",
            "bnch_turnover_ma_layoffs",
            "bnch_financial_strength",
            "bnch_demographic"
          ]}
            with="cds/modifiers/epl/benchmark_uw_modifiers"
            fields={[
            "factor_selection",
            "min",
            "max"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive={true} />
        </HX.Section>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Quote Grid">
            <HX.Table title=""
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "coverages/epl/quote_grid/qg_options"
            ]}
              fields={[
              "aggregate_limit",
              "adl_limit",
              "event_loss_limit",
              "retention",
              null,
              "miniumum_retention",
              "guideline_retention",
              null,
              {
                "field": "admitted_premium",
                "labelBy": "/non_cds/epl_premium_label"
              },
              "internal_benchmark",
              "guideline_minimum_premium",
              null,
              "bpi",
              null,
              {
                "field": "option_selected",
                "labelBy": "/non_cds/required_epl_row_labels/option_selected"
              }
            ]}
              freezeLeft={0}
              transpose={true}
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Premium Modifer Summary (for selected option only)"
            defaultCollapsed={true}>
            <HX.Table title=""
              data={[
              "base_rate",
              "lim_adj",
              "modifier_adj",
              "state_adj",
              "ded_adj",
              "coinsurance_adj",
              "employment_event_adj",
              "adl_adj",
              "sch_rating_adj",
              "prior_acts_adj",
              "ne_deviation_adj",
              "surp_dev_adj"
            ]}
              fields={[
              "prem",
              "modifier"
            ]}
              with="coverages/epl/running_prem_sum"
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
        <HX.Section title="Multiple Selection"
          shownBy="/non_cds/is_multiple_epl_covers">
          <HX.Notes field="non_cds/multiple_epl_covers_message" />
        </HX.Section>
        <HX.Section title="Split Retention">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "bnch_split_retention_offered"
            ]}
              with="cds/modifiers/epl"
              syncColumnWidthsKey="mySyncedTables1" />
          </HX.Pane>
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Section>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Split Retentions"
            shownBy="/non_cds/is_split_retention">
            <HX.Collection fields={[
              "main_retention_selected"
            ]}
              with="coverages/epl"
              syncColumnWidthsKey="mySyncedTables1" />
            <HX.Table title="State Split"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "state_split_1",
              "state_split_2",
              "state_split_3",
              "state_split_4",
              "state_split_5"
            ]}
              fields={[
              "state",
              "retention",
              "proportion",
              "retention_factor",
              "weighted_factor"
            ]}
              with="coverages/epl/state_split"
              kb-interactive={true} />
            <HX.Table title="Other Split"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "option_split_1",
              "option_split_2"
            ]}
              fields={[
              "basis_for_split",
              "detail",
              "retention",
              "retention_modifier"
            ]}
              with="coverages/epl/option_split"
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="USML Fiduciary Inputs"
        fullWidth={true}
        shownBy="/non_cds/is_fid_inputs">
        <HX.Section title="Employer Type">
          <HX.Collection fields={[
            "employer_type"
          ]}
            with="cds/fid"
            syncColumnWidthsKey="mySyncedTables1" />
        </HX.Section>
        <HX.Section title="Base Premium">
          <HX.Table data={[
            "cds/fid/base_premium/bp_plans"
          ]}
            fields={[
            "assets_contributions",
            "total_employees_or_members",
            "additional_designated_fiduciaries",
            "plan_type",
            "reactive_employee_exposure/employee_exposure",
            "percent_of_active_participants"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Plan Sponsor">
          <HX.Pane flow="right">
            <HX.Table data={[
              "reactive_financial_condition/financial_condition",
              "merger_acquisition_activity",
              "industry_quality",
              "reactive_layoffs_downsizing_spinoffs/layoffs_downsizing_spinoffs",
              "type_of_union"
            ]}
              with="cds/fid/plan_sponsor"
              fields={[
              "selection",
              "factor_selection",
              "min",
              "max"
            ]}
              title=""
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Benefit Plans">
          <HX.Pane flow="right">
            <HX.Table data={[
              "reactive_financial_condition_bp/financial_condition_bp",
              "outside_professionals",
              "funding_level",
              "investments_expenses",
              "asset_performance",
              "benefits"
            ]}
              with="cds/fid/benefit_plans"
              fields={[
              "selection",
              "factor_selection",
              "min",
              "max"
            ]}
              title=""
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Litigation">
          <HX.Table data={[
            "reactive_litigation/litigation"
          ]}
            with="cds/fid"
            fields={[
            "selection"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Foreign Charge">
          <HX.Table data={[
            "number_of_plans_outside_us"
          ]}
            with="cds/fid"
            fields={[
            "number_of_plans_outside_us",
            "factor_selection",
            "min",
            "max"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive={true} />
        </HX.Section>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Admitted Schedule Rating">
            <HX.Table data={[
              "rationale",
              "factor_selection",
              "min",
              "max"
            ]}
              with="fid/admitted_schedule_rating"
              fields={[
              "sponsor",
              "benefit_plan",
              "litigation",
              "other",
              {
                "field": "expense_factor",
                "shownBy": "/non_cds/is_state_ga"
              },
              "total_schedule_rating_modifier"
            ]}
              title=""
              syncColumnWidthsKey="mySyncedTables1"
              transpose={true}
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="Expense Rating"
            shownBy="/non_cds/is_state_ga">
            <HX.Table data={[
              "expense_rating"
            ]}
              with="fid"
              fields={[
              "factor_selection",
              "min",
              "max"
            ]}
              title=""
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="NE Deviation Factor"
            shownBy="/non_cds/is_state_ne">
            <HX.Table data={[
              "ne_deviation_factor"
            ]}
              with="fid"
              fields={[
              "rationale",
              "credit_debit",
              "min",
              "max"
            ]}
              title=""
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="Surplus Deviation"
            shownBy="/non_cds/is_surplus">
            <HX.Collection fields={[
              "surplus_deviation"
            ]}
              with="fid"
              syncColumnWidthsKey="mySyncedTables1" />
          </HX.Section>
          <HX.Section title="Benchmark UW Modifiers"
            shownBy="/non_cds/is_fid_finished_rating">
            <HX.Table data={[
              "prior_claim_activity",
              "additional_risk_characteristics"
            ]}
              with="fid/benchmark_uw_modifiers"
              fields={[
              "factor_selection",
              "min",
              "max"
            ]}
              title=""
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Quote Grid">
            <HX.Table data={[
              "coverages/fid/quote_grid/qg_options"
            ]}
              fields={[
              "aggregate_limit",
              {
                "field": "per_occurrence_limit",
                "shownBy": "/non_cds/is_per_occurrence_limit"
              },
              "adl_limit",
              "retention",
              {
                "field": "voluntary_compliance_fees_and_defense",
                "shownBy": "/non_cds/is_state_oh"
              },
              null,
              {
                "field": "admitted_premium",
                "labelBy": "/non_cds/fid_premium_label"
              },
              "internal_benchmark",
              "miniumum_retention",
              null,
              "bpi",
              {
                "field": "option_selected",
                "labelBy": "/non_cds/required_fiduciary_row_labels/option_selected"
              }
            ]}
              title=""
              syncColumnWidthsKey="mySyncedTables1"
              transpose={true}
              kb-interactive={true} />
            <HX.Collection fields={[
              "minimum_admitted_agg_limit"
            ]}
              with="coverages/fid"
              syncColumnWidthsKey="mySyncedTables1" />
            <HX.Collection fields={[
              "internal_guideline_retention"
            ]}
              with="coverages/fid"
              syncColumnWidthsKey="mySyncedTables1" />
          </HX.Section>
        </HX.With>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Premium Modifer Summary (for selected option only)"
            defaultCollapsed={true}>
            <HX.Table title=""
              data={[
              "base_rate",
              "lim_adj",
              "retention_adj",
              "fl_adj",
              "risk_char_adj",
              "lim_compression_adj",
              "adl_adj",
              "fcf_adj",
              "exp_fac_adj",
              "prior_acts_adj",
              "sch_rating_adj"
            ]}
              fields={[
              "prem",
              "modifier"
            ]}
              with="coverages/fid/running_prem_sum"
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
        <HX.Section title="Multiple Selection"
          shownBy="/non_cds/is_multiple_fiduciary_covers">
          <HX.Notes field="non_cds/multiple_fiduciary_covers_message" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="USML PCL Inputs"
        fullWidth={true}
        shownBy="/non_cds/is_pcl_inputs">
        <HX.Section title="Base Rate">
          <HX.Collection fields={[
            "cds/exposure/granular/pcl/base_rate/asset_size",
            "cds/exposure/granular/pcl/base_rate/revenue",
            "cds/rating_factors/pcl/base_rate/admitted_minimum_premium",
            "cds/rating_factors/pcl/base_rate/admitted_minimum_limit"
          ]}
            syncColumnWidthsKey="mySyncedTables1" />
        </HX.Section>
        <HX.Section title="Modifiers">
          <HX.Table data={[
            "financial_condition",
            "mergers_and_acquisition_activity",
            "ownership",
            "length_of_time_in_business",
            "layoffs_downsizing_or_spinoffs",
            "profitability",
            "quality_of_management",
            "litigation",
            "reactive_removal_of_punitive_damages/removal_of_punitive_damages"
          ]}
            with="cds/modifiers/pcl/modifiers_table"
            fields={[
            "description",
            "factor_selection",
            "min",
            "max",
            "factor_selection_nm",
            "min_nm",
            "max_nm"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Class of Business">
          <HX.Collection fields={[
            "class_of_business"
          ]}
            with="cds/exposure/granular/pcl"
            syncColumnWidthsKey="mySyncedTables1" />
          <HX.Table fields={[
            {
              "field": "table_a",
              "maxWidth": 300
            },
            {
              "field": "table_b",
              "maxWidth": 300
            }
          ]}
            data={[
            "option_1",
            "option_2",
            "option_3",
            "option_4",
            "option_5"
          ]}
            with="cds/exposure/granular/pcl/class_of_business_table" />
        </HX.Section>
        <HX.Section title="Schedule Rating">
          <HX.Table data={[
            "prior_claim_activity",
            "financial_strength",
            "mergers_and_acquisitions",
            "quality_of_board",
            "length_of_time_in_business",
            "size_of_revenues_assets_employees",
            "layoffs_downsizing_spinoffs",
            "ownership_control",
            "total_schedule_rating_modifier"
          ]}
            fields={[
            "rationale",
            "factor_selection",
            "min",
            "max"
          ]}
            with="cds/modifiers/pcl/schedule_rating/table_cw"
            syncColumnWidthsKey="mySyncedTables1"
            shownBy="/non_cds/is_table_cw"
            kb-interactive={true} />
          <HX.Table data={[
            "classification_peculiarities",
            "significant_transactional_event",
            "regulatory_exposure",
            "board_of_directors",
            "management_practices",
            "experience",
            "total_schedule_rating_modifier"
          ]}
            fields={[
            "rationale",
            "factor_selection",
            "min",
            "max"
          ]}
            with="cds/modifiers/pcl/schedule_rating/table_ca"
            syncColumnWidthsKey="mySyncedTables1"
            shownBy="/non_cds/is_table_ca"
            kb-interactive={true} />
          <HX.Table data={[
            "prior_claim_activity",
            "financial_strength",
            "mergers_and_acquisitions",
            "quality_of_board",
            "length_of_time_in_business",
            "size_of_revenues_assets_employees",
            "layoffs_downsizing_spinoffs",
            "total_schedule_rating_modifier"
          ]}
            fields={[
            "rationale",
            "factor_selection",
            "min",
            "max"
          ]}
            with="cds/modifiers/pcl/schedule_rating/table_la"
            syncColumnWidthsKey="mySyncedTables1"
            shownBy="/non_cds/is_table_la"
            kb-interactive={true} />
          <HX.Table data={[
            "prior_claim_activity",
            "cash_position_stability",
            "diversification_strategy",
            "board_shareholders",
            "size_of_revenues_assets_employees",
            "total_schedule_rating_modifier"
          ]}
            fields={[
            "rationale",
            "factor_selection",
            "min",
            "max"
          ]}
            with="cds/modifiers/pcl/schedule_rating/table_mo"
            syncColumnWidthsKey="mySyncedTables1"
            shownBy="/non_cds/is_table_mo"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="NE Deviation Factor"
          shownBy="/non_cds/is_state_ne">
          <HX.Table data={[
            "ne_deviation_factor"
          ]}
            with="cds/modifiers/pcl"
            fields={[
            "rationale",
            "credit_debit",
            "min",
            "max"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Surplus Deviation"
          shownBy="/non_cds/is_surplus">
          <HX.Collection fields={[
            "surplus_deviation"
          ]}
            with="cds/modifiers/pcl"
            syncColumnWidthsKey="mySyncedTables1" />
        </HX.Section>
        <HX.Section title="UW Modifier"
          shownBy="/non_cds/is_pcl_finished_rating">
          <HX.Table data={[
            "bnch_prior_claim_activity_selection"
          ]}
            with="cds/modifiers/pcl"
            fields={[
            "factor_selection",
            "min",
            "max"
          ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive={true} />
        </HX.Section>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Quote Grid">
            <HX.Table title=""
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "coverages/pcl/quote_grid/qg_options"
            ]}
              fields={[
              "aggregate_limit",
              "retention",
              "limit_retention",
              null,
              {
                "field": "admitted_premium",
                "labelBy": "/non_cds/pcl_premium_label"
              },
              "internal_benchmark",
              "guideline_minimum_premium",
              "miniumum_retention",
              null,
              "bpi",
              {
                "field": "option_selected",
                "labelBy": "/non_cds/required_pcl_row_labels/option_selected"
              }
            ]}
              freezeLeft={0}
              transpose={true}
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Premium Modifer Summary (for selected option only)"
            defaultCollapsed={true}>
            <HX.Table title=""
              data={[
              "base_rate",
              "combined_retention_and_limit_adj",
              "risk_char_adj",
              "cob_adj",
              "punitive_damages_adj",
              "state_adj",
              "surp_dev_adj"
            ]}
              fields={[
              "",
              "modifier"
            ]}
              with="coverages/pcl/running_prem_sum"
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
        <HX.Section title="Multiple Selection"
          shownBy="/non_cds/is_multiple_pcl_covers">
          <HX.Notes field="non_cds/multiple_pcl_covers_message" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Excess Premium"
        viewScale={1}
        shownBy="/cds/conditions_met">
        <HX.Section title="Folder Selection">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "chosen_date"
            ]}
              with="cds" />
            <HX.Pane ratio={3} />
          </HX.Pane>
        </HX.Section>
        <HX.With context={{
          "path": "cds/admitted_excess",
          "type": "struct"
        }}>
          <HX.Section title="Coverages">
            <HX.Table data={[
              "primary_limit",
              "primary_retention",
              "primary_premium",
              "excess_limit",
              "excess_attachment_point",
              "no_of_policies_sharing_single_limit"
            ]}
              fields={[
              "value"
            ]}
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="Admitted Excess Specific Inputs">
            <HX.Table shownBy="/cds/is_excess_surplus"
              data={[
              "large_loss_potential",
              "primary_rate_adequacy_correction",
              "industry_sector_risk_level",
              "industry_sector_factor",
              "company_risk_level",
              "company_factor",
              "litigation_risk_level",
              "litigation_factor",
              "fl_schedule_rating_factor",
              "surplus_deviation",
              null,
              "model_premium",
              "max_round_down",
              "max_round_up",
              "rounded_premium"
            ]}
              fields={[
              "value",
              "rationale",
              "min",
              "max",
              "default"
            ]}
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
            <HX.Table shownBy="/cds/not_excess_surplus"
              data={[
              "large_loss_potential",
              "primary_rate_adequacy_correction",
              "industry_sector_risk_level",
              "industry_sector_factor",
              "company_risk_level",
              "company_factor",
              "litigation_risk_level",
              "litigation_factor",
              "fl_schedule_rating_factor",
              null,
              "model_premium",
              "max_round_down",
              "max_round_up",
              "rounded_premium"
            ]}
              fields={[
              "value",
              "rationale",
              "min",
              "max",
              "default"
            ]}
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology.read_only",
              null
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rater Status">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/package_information/finished_rating"
            ]} />
            <HX.Pane flow="right">
              <HX.Button task="word_documents_task"
                title="Generate Coverage Options" />
              <HX.File field="/cds/coverage_options" />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage Options">
          <HX.Table title="Priced Quotes (Beazley Share)"
            data={[
            {
              "datum": "cds/layers",
              "width": 250
            }
          ]}
            fields={[
            "status.input",
            "section_reference",
            "brokerage",
            "written_line",
            null,
            "quoted_premium",
            "technical_premium",
            {
              "field": "technical_premium_pre_uw_adj",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "benchmark_premium"
            },
            null,
            "tpi",
            {
              "field": "tpi_pre_uw_adj",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "bpi",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "bpi_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            null,
            "pflr",
            "roc",
            {
              "field": "uw_adj_impact",
              "shownBy": "cds/standard_fields/is_rater_priced"
            }
          ]}
            freezeLeft={0}
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Quote Grid Summary"
          shownBy="cds/admitted_excess_local/is_policy_primary">
          <HX.Table data={[
            "cds/quote_grid_summary/epl",
            "cds/quote_grid_summary/fid",
            "cds/quote_grid_summary/pcl"
          ]}
            fields={[
            "limit",
            "adl",
            "retention",
            "benchmark_premium",
            "pre_rounding_admitted_premium",
            "selected_premium",
            "post_rounding_admitted_premium",
            "final_term_premium",
            "bpi"
          ]}
            title="Quote Grid Summary"
            syncColumnWidthsKey="mySyncedTables1" />
        </HX.Section>
        <HX.Section title="Final Premium Summary"
          shownBy="cds/admitted_excess_local/is_policy_primary">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/final_premium_summary/benchmark_premium",
              "cds/final_premium_summary/pre_rounding_admitted_premium",
              "cds/final_premium_summary/post_rounding_admitted_premium"
            ]} />
            <HX.Collection fields={[
              "cds/final_premium_summary/benchmark_term_premium",
              "cds/final_premium_summary/technical_term_premium",
              "cds/final_premium_summary/final_admitted_term_premium"
            ]} />
            <HX.Collection fields={[
              "cds/final_premium_summary/bpi",
              "cds/final_premium_summary/tpi"
            ]} />
            <HX.Collection fields={[
              "cds/final_premium_summary/rounding_min",
              "cds/final_premium_summary/rounding_max"
            ]} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        shownBy="cds/rate_change/show_hide_rc"
        fullWidth={true}>
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
              task="rarc_task" />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
          </HX.Pane>
        </HX.Section>
        <HX.Section>
          <HX.With context={{
            "path": "cds/rate_change",
            "type": "struct"
          }}>
            <HX.Pane>
              <HX.Table rowHeaderSettings={{
                "width": 320
              }}
                data={[
                "premium_annualized_beazley_share"
              ]}
                fields={[
                {
                  "field": "epl/renewal",
                  "shownBy": "coverage_indicator/epl",
                  "width": 100
                },
                {
                  "field": "epl/expiring",
                  "shownBy": "coverage_indicator/epl",
                  "width": 100
                },
                {
                  "field": "fid/renewal",
                  "shownBy": "coverage_indicator/fid",
                  "width": 100
                },
                {
                  "field": "fid/expiring",
                  "shownBy": "coverage_indicator/fid",
                  "width": 100
                },
                {
                  "field": "pcl/renewal",
                  "shownBy": "coverage_indicator/pcl",
                  "width": 100
                },
                {
                  "field": "pcl/expiring",
                  "shownBy": "coverage_indicator/pcl",
                  "width": 100
                },
                null,
                {
                  "field": "execuguard/renewal",
                  "width": 100
                },
                {
                  "field": "execuguard/expiring",
                  "width": 100
                }
              ]} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "path": "cds/rate_change",
            "type": "struct"
          }}>
            <HX.Pane>
              <HX.Table rowHeaderSettings={{
                "width": 320
              }}
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "epl/model",
                  "shownBy": "coverage_indicator/epl",
                  "width": 100
                },
                {
                  "field": "epl/selected",
                  "shownBy": "coverage_indicator/epl",
                  "width": 100
                },
                {
                  "field": "fid/model",
                  "shownBy": "coverage_indicator/fid",
                  "width": 100
                },
                {
                  "field": "fid/selected",
                  "shownBy": "coverage_indicator/fid",
                  "width": 100
                },
                {
                  "field": "pcl/model",
                  "shownBy": "coverage_indicator/pcl",
                  "width": 100
                },
                {
                  "field": "pcl/selected",
                  "shownBy": "coverage_indicator/pcl",
                  "width": 100
                },
                null,
                {
                  "field": "execuguard/model",
                  "width": 100
                },
                {
                  "field": "execuguard/selected",
                  "width": 100
                }
              ]} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Coverage RC Details">
          <HX.With context={{
            "path": "cds/rate_change",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Table shownBy="coverage_indicator/epl"
                data={[
                "fte",
                "limit",
                "ded"
              ]}
                fields={[
                {
                  "field": "epl/expiry",
                  "width": 130
                },
                {
                  "field": "epl/renewal",
                  "width": 130
                },
                {
                  "field": "epl/rate_change",
                  "width": 130
                }
              ]} />
              <HX.Table shownBy="coverage_indicator/fid"
                data={[
                "assets",
                "participants",
                "limit",
                "ded"
              ]}
                fields={[
                {
                  "field": "fid/expiry",
                  "width": 130
                },
                {
                  "field": "fid/renewal",
                  "width": 130
                },
                {
                  "field": "fid/rate_change",
                  "width": 130
                }
              ]} />
              <HX.Table shownBy="execugard_package"
                data={[
                "assets",
                "limit",
                "ded"
              ]}
                fields={[
                {
                  "field": "pcl/expiry",
                  "width": 130
                },
                {
                  "field": "pcl/renewal",
                  "width": 130
                },
                {
                  "field": "pcl/rate_change",
                  "width": 130
                }
              ]} />
              <HX.Table shownBy="not_execugard_package"
                data={[
                "assets",
                "fte",
                "limit",
                "ded"
              ]}
                fields={[
                {
                  "field": "pcl/expiry",
                  "width": 130
                },
                {
                  "field": "pcl/renewal",
                  "width": 130
                },
                {
                  "field": "pcl/rate_change",
                  "width": 130
                }
              ]} />
            </HX.Pane>
            <HX.Collection title="Final Rate Change"
              fields={[
              "uw_selected_rarc",
              null,
              null,
              null
            ]}
              horizontal={true} />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        shownBy="cds/excess_rate_change/show_hide_excess_rc"
        fullWidth={true}>
        <HX.With context={{
          "path": "cds/excess_rate_change",
          "type": "struct"
        }}>
          <HX.Section title="Rate Change Individual Componets">
            <HX.Pane flow="right">
              <HX.Table title="Deductible, Limit, and Brokergae"
                data={[
                "deductible",
                "limit",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiry",
                  "width": 150
                },
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "rate_change",
                  "width": 150
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="mySyncedTables1" />
              <HX.Table title="Exposure Components"
                data={[
                "exposure/fte",
                "exposure/plan_assets",
                "exposure/plan_participants",
                "exposure/total_assets",
                null,
                "exposure/total_rate_change"
              ]}
                fields={[
                {
                  "field": "expiry",
                  "width": 150
                },
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "rate_change",
                  "width": 150
                },
                null,
                {
                  "field": "weights",
                  "width": 150
                }
              ]} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Rate Change">
            <HX.Pane flow="right">
              <HX.Table title="Rate Change Build-up"
                data={[
                "annualized_expiring_prem",
                null,
                "exposure/total_rate_change",
                "risk_char",
                "deductible",
                "limit",
                "terms_and_conditions",
                "brokerage",
                null,
                "expected_new_prem",
                "new_prem",
                null,
                "final_rc"
              ]}
                fields={[
                {
                  "field": "rate_change",
                  "width": 150
                }
              ]} />
              <HX.Notes field="comments"
                title="Comments" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Underwriter Rationale">
          <CustomComponent textNode="cds/standard_fields/uw_rationale" />
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
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "quoted_premium",
                "labelBy": "/non_cds/quoted_premium_case_priced_label",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
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