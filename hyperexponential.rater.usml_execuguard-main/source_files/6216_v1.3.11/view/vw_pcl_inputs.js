import * as HX from "hx-model-components";

function vw_pcl_inputs() {
  return (
    <HX.Page title="USML PCL Inputs" fullWidth={true} shownBy="/non_cds/is_pcl_inputs" >

      <HX.Section title="Base Rate">
        <HX.Collection fields={["cds/exposure/granular/pcl/base_rate/asset_size", "cds/exposure/granular/pcl/base_rate/revenue", "cds/rating_factors/pcl/base_rate/admitted_minimum_premium", "cds/rating_factors/pcl/base_rate/admitted_minimum_limit"]} syncColumnWidthsKey='mySyncedTables1' />
      </HX.Section>
      <HX.Section title="Modifiers">
        <HX.Table
          data={[
            "financial_condition",
            "mergers_and_acquisition_activity",
            "ownership",
            "length_of_time_in_business",
            "layoffs_downsizing_or_spinoffs",
            "profitability",
            "quality_of_management",
            "litigation",
            "reactive_removal_of_punitive_damages/removal_of_punitive_damages"]} with="cds/modifiers/pcl/modifiers_table"
          fields={["description", "factor_selection", "min", "max", 'factor_selection_nm', 'min_nm', 'max_nm']}
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Class of Business">
        <HX.Collection fields={["class_of_business"]} with="cds/exposure/granular/pcl" syncColumnWidthsKey='mySyncedTables1' />
        <HX.Table
          fields={[
            { field: "table_a", maxWidth: 300 },
            { field: "table_b", maxWidth: 300 }]}
          data={[
            "option_1",
            "option_2",
            "option_3",
            "option_4",
            "option_5"]}
          with="cds/exposure/granular/pcl/class_of_business_table"
        >

        </HX.Table>
      </HX.Section>
      <HX.Section title="Schedule Rating">
        <HX.Table data={["prior_claim_activity",
          "financial_strength",
          "mergers_and_acquisitions",
          "quality_of_board",
          "length_of_time_in_business",
          "size_of_revenues_assets_employees",
          "layoffs_downsizing_spinoffs",
          "ownership_control",
          "total_schedule_rating_modifier"]}
          fields={["rationale", "factor_selection", "min", "max",
          ]}
          with="cds/modifiers/pcl/schedule_rating/table_cw" syncColumnWidthsKey='mySyncedTables1' shownBy="/non_cds/is_table_cw" kb-interactive />
        <HX.Table
          data={[
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
          syncColumnWidthsKey='mySyncedTables1'
          shownBy="/non_cds/is_table_ca"
          kb-interactive
        />
        <HX.Table
          data={[
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
          syncColumnWidthsKey='mySyncedTables1'
          shownBy="/non_cds/is_table_la"
          kb-interactive
        />
        <HX.Table
          data={[
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
          syncColumnWidthsKey='mySyncedTables1'
          shownBy="/non_cds/is_table_mo"
          kb-interactive
        />

      </HX.Section>
      <HX.Section title="NE Deviation Factor" shownBy="/non_cds/is_state_ne">
        <HX.Table
          data={["ne_deviation_factor"]} with="cds/modifiers/pcl"
          fields={["rationale", "credit_debit", "min", "max"]}
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Surplus Deviation" shownBy="/non_cds/is_surplus">
        <HX.Collection fields={["surplus_deviation"]} with="cds/modifiers/pcl" syncColumnWidthsKey='mySyncedTables1' />
      </HX.Section>
      <HX.Section title="UW Modifier" shownBy="/non_cds/is_pcl_finished_rating">
        <HX.Table
          data={["bnch_prior_claim_activity_selection"]} with="cds/modifiers/pcl"
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
            data={["coverages/pcl/quote_grid/qg_options"]}
            fields={[
              "aggregate_limit",
              "retention",
              "limit_retention",
              null,
              { field: "admitted_premium", labelBy: "/non_cds/pcl_premium_label" },
              "internal_benchmark",
              "guideline_minimum_premium",
              "miniumum_retention",
              null,
              "bpi",
              {
                field: "option_selected",
                labelBy:
                  "/non_cds/required_pcl_row_labels/option_selected",
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
            data={["base_rate", "combined_retention_and_limit_adj", "risk_char_adj", "cob_adj", "punitive_damages_adj", "state_adj", "surp_dev_adj"]}
            fields={["", "modifier"]}
            with="coverages/pcl/running_prem_sum"
            syncColumnWidthsKey="mySyncedTables1"
            kb-interactive
          />
        </HX.Section>
      </HX.With>
      <HX.Section title="Multiple Selection" shownBy="/non_cds/is_multiple_pcl_covers">
        <HX.Notes field="non_cds/multiple_pcl_covers_message" />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_pcl_inputs };