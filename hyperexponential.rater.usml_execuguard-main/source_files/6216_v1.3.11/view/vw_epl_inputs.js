import * as HX from "hx-model-components";

function vw_epl_inputs() {
  return (
    <HX.Page title="USML EPL Inputs" fullWidth={true} shownBy="/non_cds/is_epl_inputs" >

      <HX.Section title="Admitted Modifiers">
        <HX.Table
          data={["reactive_admitted_modifiers/risk_characteristics",
            {
              datum: "financial_stability",
              labelBy: "/non_cds/required_epl_row_labels/financial_stability"
            },
            {
              datum: "loss_prevention_and_mitigation",
              labelBy: "/non_cds/required_epl_row_labels/loss_prevention_and_mitigation"
            },
            {
              datum: "employment_policies",
              labelBy: "/non_cds/required_epl_row_labels/employment_policies"
            },
            "reactive_cob/class_of_business", "sug_class_business", "unionized_employees", "stock_option_exposure"]} with="cds/modifiers/epl/admitted_modifiers"
          fields={["description", "factor_selection", "min", "max"]}
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Endorsements">
        <HX.Table
          data={[
            "selection",
            "factor_selection",
            "min",
            "max"]} with="cds/modifiers/epl/endorsements"
          fields={[
            {
              field: "punitive_damages",
              labelBy:
                "/non_cds/required_epl_row_labels/punitive_damages",
              shownBy: "/non_cds/punitive_damages_acceptable"
            },
            //put this back in when we get hxvalidation added to the theme
            {
              field: "punitive_damages.mandatory",
              labelBy:
                "/non_cds/required_epl_row_labels/punitive_damages",
              shownBy: "/non_cds/punitive_damages_not_acceptable"
            },
            "reactive_third_party_liab/third_party_liability",

            "reactive_wage_and_hour/wage_and_hour",
            "client_coverage",
            { field: "ahern", shownBy: "/non_cds/is_state_ca" },
            { field: "partnership_defense", shownBy: "/non_cds/is_state_ca" },
            { field: "leaders_preferred", shownBy: "/non_cds/is_leader_preferred" }
          ]}
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          transpose
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Coinsurance">
        <HX.Table
          data={["per_self_ins"]} with="cds/modifiers/epl"
          fields={["selection", "max_credit"]}
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Total Admitted Modifier" >
        <HX.Collection fields={["cds/modifiers/epl/total_admitted_modifier"]} syncColumnWidthsKey='mySyncedTables1' />
      </HX.Section>
      <HX.Section title="Admitted Schedule Rating" shownBy="/non_cds/is_state_ne_hide">
        <HX.Table
          data={["rationale", "factor_selection", "min", "max"]}
          fields={[
            { field: "prior_claim_activity", shownBy: '/non_cds/is_state_ca_or_in_hide' },
            { field: "turnover_rate", shownBy: '/non_cds/is_state_ca_or_in_hide' },
            { field: "financial_strength", shownBy: '/non_cds/is_state_ca_or_in_hide' },
            { field: "hr_policies", labelBy: '/non_cds/hr_policies_label', shownBy: '/non_cds/is_state_in_hide' },
            { field: "demographic_metro" },
            { field: "management", shownBy: '/non_cds/is_state_ca_or_in' },
            { field: "internal_controls", shownBy: '/non_cds/is_state_ca_or_in' },
            { field: "cooperation", shownBy: '/non_cds/is_state_ca_or_in' },
            { field: "experience", shownBy: '/non_cds/is_state_ca_or_in' },
            { field: "staffing_turnover", shownBy: '/non_cds/is_state_ca_or_in' },
            { field: "salary_structure", shownBy: '/non_cds/is_state_ca_or_in' },
            { field: "stability", shownBy: '/non_cds/is_state_ca' },
            "tot_sch_rat"
          ]}
          with="cds/modifiers/epl/admitted_schedule_rating"
          syncColumnWidthsKey="mySyncedTables1"
          transpose
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="NE Deviation Factor" shownBy="/non_cds/is_state_ne">
        <HX.Table
          data={["ne_deviation_factor"]} with="cds/modifiers/epl"
          fields={["rationale", "factor_selection", "min", "max"]}
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Surplus Deviation" shownBy="/non_cds/is_surplus">
        <HX.Collection fields={["cds/modifiers/epl/surplus_deviation"]} syncColumnWidthsKey='mySyncedTables1' />
      </HX.Section>
      <HX.Section title="Benchmark UW Modifiers" shownBy="/non_cds/is_epl_finished_rating">
        <HX.Table
          data={["bnch_risk_characteristics", "bnch_pro_claim_activity", "bnch_hr_policies", "bnch_turnover_ma_layoffs", "bnch_financial_strength", "bnch_demographic"]} with="cds/modifiers/epl/benchmark_uw_modifiers"
          fields={["factor_selection", "min", "max"]}
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          kb-interactive
        />
      </HX.Section>
      {/* </HX.With> */}
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Quote Grid">
          <HX.Table
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            data={["coverages/epl/quote_grid/qg_options"]}
            fields={[
              "aggregate_limit",
              "adl_limit",
              "event_loss_limit",
              "retention",
              null,
              "miniumum_retention",
              "guideline_retention",
              null,
              { field: "admitted_premium", labelBy: "/non_cds/epl_premium_label" },
              "internal_benchmark",
              "guideline_minimum_premium",
              null,
              "bpi",
              null,
              {
                field: "option_selected",
                labelBy:
                  "/non_cds/required_epl_row_labels/option_selected",
              },

            ]}
            freezeLeft={0}
            transpose
            kb-interactive
          />
        </HX.Section>
      </HX.With>
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Premium Modifer Summary (for selected option only)" defaultCollapsed={true}>
          <HX.Table
            title=""
            data={["base_rate", "lim_adj", "modifier_adj", "state_adj", "ded_adj", "coinsurance_adj", "employment_event_adj", "adl_adj", "sch_rating_adj", "prior_acts_adj", "ne_deviation_adj", "surp_dev_adj"]}
            fields={["prem", "modifier"]}
            with="coverages/epl/running_prem_sum"
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive
          />
        </HX.Section>
      </HX.With>

      <HX.Section title="Multiple Selection" shownBy="/non_cds/is_multiple_epl_covers">
        <HX.Notes field="non_cds/multiple_epl_covers_message" />
      </HX.Section>
      <HX.Section title="Split Retention">
        <HX.Pane flow="right">
          <HX.Collection fields={["bnch_split_retention_offered"]} with="cds/modifiers/epl" syncColumnWidthsKey='mySyncedTables1' />
        </HX.Pane>
        <HX.Pane />
        <HX.Pane />
        <HX.Pane />
        <HX.Pane />
      </HX.Section>
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Split Retentions" shownBy="/non_cds/is_split_retention">
          <HX.Collection fields={["main_retention_selected"]} with="coverages/epl" syncColumnWidthsKey='mySyncedTables1' />
          <HX.Table
            title="State Split"
            syncColumnWidthsKey="mySyncedTables1"
            data={["state_split_1", "state_split_2", "state_split_3", "state_split_4", "state_split_5"]}
            fields={[
              "state",
              "retention",
              "proportion",
              "retention_factor",
              "weighted_factor"
            ]}
            with="coverages/epl/state_split"
            kb-interactive
          />
          <HX.Table
            title="Other Split"
            syncColumnWidthsKey="mySyncedTables1"
            data={["option_split_1", "option_split_2"]}
            fields={[
              "basis_for_split",
              "detail",
              "retention",
              "retention_modifier"
            ]}
            with="coverages/epl/option_split"
            kb-interactive
          />
        </HX.Section>
      </HX.With>
    </HX.Page >
  )
}

export { vw_epl_inputs };