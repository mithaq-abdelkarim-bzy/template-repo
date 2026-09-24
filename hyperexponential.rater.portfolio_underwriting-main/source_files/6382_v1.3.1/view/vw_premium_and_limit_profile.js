import * as HX from "hx-model-components";


function vw_premium_and_limit_profile(scale) {
  return (
    <HX.Page title="Premium and Limit Profile" fullWidth={true} viewScale={scale} shownBy="model_state/show_premium_limit_prof">
      <HX.Section title="Premium and Limit Profile" collapsible={false}>
        <HX.Pane>
          <HX.Table
            title="Premium and Limit Profile Table"
            data={['cds/prem_limit_profile/table', null, 'cds/prem_limit_profile/summary']}
            fields={[
              "lob",
              "selected_lob",
              "assigned_trifocus",
              "max_limit_at_100_per",
              "avg_limit_at_100_per",
              "avg_attachment_point",
              "primary",
              "max_limit_at_bst_share",
              null,
              "future_ultimate_gross_prem",
              "bst_share_line_size",
              "bst_share_ultimate_gross_premium",
              "bst_deductions",
              "bst_net_premium",
              "portfolio_composition"
            ]}
            filter={"is_row_visible"}
            syncColumnWidthsKey="table_1"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Commentary" collapsible={false}>
        <HX.Notes field="cds/rationale/prem_limit_notes" title="Please note any rationale for selection below, and any use of overrides:" />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_premium_and_limit_profile };