import * as HX from "hx-model-components";

function vw_fiduciary_inputs() {
  return (
    <HX.Page title="USML Fiduciary Inputs" fullWidth={true} shownBy="/non_cds/is_fid_inputs">

      <HX.Section title="Employer Type">
        <HX.Collection fields={["employer_type"]} with="cds/fid" syncColumnWidthsKey='mySyncedTables1' />
      </HX.Section>

      <HX.Section title="Base Premium">
        <HX.Table
          data={["cds/fid/base_premium/bp_plans"]}
          fields={["assets_contributions", "total_employees_or_members", "additional_designated_fiduciaries", "plan_type", "reactive_employee_exposure/employee_exposure", "percent_of_active_participants"]}//"reactive_employee_exposure/employee_exposure",
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          transpose
          kb-interactive
        />

      </HX.Section>
      <HX.Section title="Plan Sponsor">
        <HX.Pane flow="right">
          <HX.Table
            data={["reactive_financial_condition/financial_condition", "merger_acquisition_activity", "industry_quality", "reactive_layoffs_downsizing_spinoffs/layoffs_downsizing_spinoffs", "type_of_union"]} with="cds/fid/plan_sponsor"
            fields={["selection", "factor_selection", "min", "max"]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive
          />

        </HX.Pane>
      </HX.Section>
      <HX.Section title="Benefit Plans">
        <HX.Pane flow="right">
          <HX.Table
            data={["reactive_financial_condition_bp/financial_condition_bp", "outside_professionals", "funding_level", "investments_expenses", "asset_performance", "benefits"]} with="cds/fid/benefit_plans"
            fields={["selection", "factor_selection", "min", "max"]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive
          />

        </HX.Pane>
      </HX.Section>
      <HX.Section title="Litigation">
        <HX.Table
          data={["reactive_litigation/litigation"]} with="cds/fid"
          fields={["selection"]}
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Foreign Charge">
        <HX.Table
          data={["number_of_plans_outside_us"]} with="cds/fid"
          fields={["number_of_plans_outside_us", "factor_selection", "min", "max"]}
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          kb-interactive
        />
      </HX.Section>
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Admitted Schedule Rating">
          <HX.Table
            data={["rationale", "factor_selection", "min", "max"]} with="fid/admitted_schedule_rating"
            fields={["sponsor",
              "benefit_plan",
              "litigation",
              "other",
              { field: "expense_factor", shownBy: "/non_cds/is_state_ga" },
              'total_schedule_rating_modifier'
            ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            transpose
            kb-interactive
          />

        </HX.Section>
        <HX.Section title="Expense Rating" shownBy="/non_cds/is_state_ga">
          <HX.Table
            data={["expense_rating"]} with="fid"
            fields={["factor_selection", "min", "max"]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive
          />
        </HX.Section>
        <HX.Section title="NE Deviation Factor" shownBy="/non_cds/is_state_ne">
          <HX.Table
            data={["ne_deviation_factor"]} with="fid"
            fields={["rationale", "credit_debit", "min", "max"]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive
          />
        </HX.Section>
        <HX.Section title="Surplus Deviation" shownBy="/non_cds/is_surplus">
          <HX.Collection fields={["surplus_deviation"]} with="fid" syncColumnWidthsKey='mySyncedTables1' />
        </HX.Section>
        <HX.Section title="Benchmark UW Modifiers" shownBy="/non_cds/is_fid_finished_rating">
          <HX.Table
            data={["prior_claim_activity", "additional_risk_characteristics"]} with="fid/benchmark_uw_modifiers"
            fields={["factor_selection", "min", "max"]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive
          />
        </HX.Section>
      </HX.With>
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Quote Grid">
          <HX.Table
            data={["coverages/fid/quote_grid/qg_options"]}
            fields={["aggregate_limit",
              { field: "per_occurrence_limit", shownBy: "/non_cds/is_per_occurrence_limit" },
              "adl_limit",
              "retention",
              { field: "voluntary_compliance_fees_and_defense", shownBy: "/non_cds/is_state_oh" },
              null,
              { field: "admitted_premium", labelBy: "/non_cds/fid_premium_label" },
              "internal_benchmark",
              "miniumum_retention",
              null,
              'bpi',
              {
                field: "option_selected",
                labelBy:
                  "/non_cds/required_fiduciary_row_labels/option_selected",
              },
            ]}
            title=""
            syncColumnWidthsKey="mySyncedTables1"
            transpose
            kb-interactive
          />
          <HX.Collection fields={["minimum_admitted_agg_limit"]} with="coverages/fid" syncColumnWidthsKey='mySyncedTables1' />
          <HX.Collection fields={["internal_guideline_retention"]} with="coverages/fid" syncColumnWidthsKey='mySyncedTables1' />
        </HX.Section>
      </HX.With>
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Premium Modifer Summary (for selected option only)" defaultCollapsed={true}>
          <HX.Table
            title=""
            data={["base_rate", "lim_adj", "retention_adj", "fl_adj", "risk_char_adj", "lim_compression_adj", "adl_adj", "fcf_adj", "exp_fac_adj", "prior_acts_adj", "sch_rating_adj"]}
            fields={["prem", "modifier"]}
            with="coverages/fid/running_prem_sum"
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive
          />
        </HX.Section>
      </HX.With>
      <HX.Section title="Multiple Selection" shownBy="/non_cds/is_multiple_fiduciary_covers">
        <HX.Notes field="non_cds/multiple_fiduciary_covers_message" />
      </HX.Section>

    </HX.Page>
  )
}

export { vw_fiduciary_inputs };