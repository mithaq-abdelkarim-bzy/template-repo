import * as HX from "hx-model-components";

function vw_bp_projections(scale) {
  common_fields = [
    "tracker_class",
    "selected_lob",
    "bp_class",
    "risk_code",
    "composition",
    "acc_aquisition_costs",
    null,
    "attr_base_gn_ulr",
    "attr_inflation_1_year",
    "attr_rate_change",
    "attr_rarc_margin",
    "attr_portfolio_change",
    "cat_base_gn_ulr",
    "cat_inflation_1_year",
    "cat_rate_change",
    "cat_rarc_margin",
    "cat_climate_change",
    "cat_nmp_general",
    "cat_nmp_all_other",
    "rate_change_override",
    "selected_attr_gn_ulr",
    "selected_cat_gn_ulr",
    "total_gn_ulr",
    "bp_acquisition_costs",
    "adj_attr_gn_ulr",
    "adj_cat_gn_ulr",
    "adj_total_gn_ulr",
  ]

  return (
    <HX.Page title="BP Projections" fullWidth={true} viewScale={scale} shownBy="model_state/show_bp_proj">
      <HX.Section title="Business Plan Pricing" collapsible={false}>
        {/* <HX.Section title="BP Projections by Tracker Class">
          <HX.Table
            data={["cds/bp_projections/table_1"]}
            fields={common_fields}
            kb-interactive
          />
        </HX.Section> */}
        <HX.Section title="BP Projections by Selected LoB">
          <HX.Table
            data={["cds/bp_projections/bp_summary_by_lob"]}
            fields={common_fields}
            filter={"is_row_visible"}
            kb-interactive
          />
        </HX.Section>
        <HX.Section title="BP Projections by Selected LoB and Risk Code">
          <HX.Table
            data={["cds/bp_projections/bp_details"]}
            fields={[...common_fields]}
            filter={"is_row_visible"}
            kb-interactive
          />
        </HX.Section>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_bp_projections };