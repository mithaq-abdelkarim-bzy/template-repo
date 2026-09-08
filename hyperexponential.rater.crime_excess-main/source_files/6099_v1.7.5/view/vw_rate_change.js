import * as HX from "hx-model-components";

function vw_rate_change(scale) {
  return (
    <HX.Page title="Rate Change" fullWidth={false} viewScale={scale} shownBy="/show_rate_change">
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Rate Change">
          <HX.Pane flow="right">
            <HX.Collection fields={["rate_change/expiring_policy_option_id"]} horizontal />
            <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={["rate_change/expiring_insured_name"]} />
            <HX.Pane />
          </HX.Pane>
          <HX.Table kb-interactive
            data={["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "brokerage_change", "other_change"]}
            fields={["uw_selected", "comments"]}
            title="Impact Split"
            with="rate_change"
          />
          <HX.Pane >
            <HX.Collection with="rate_change" fields={["expiring_premium", "expiring_beazley_share", "rate_change/uw_selected"]} horizontal />
            <HX.Collection with="rate_change" fields={["expiring_policy_term", "expiring_limit", "expiring_brokerage"]} horizontal />
            <HX.Collection with="rate_change" fields={["expiring_policy_reference", "expiring_excess", null]} horizontal />
            {/* To add when switching to new benchmark calcs*/}
            <HX.Collection title="Company Information"
              with="rate_change" fields={["expiring_revenue", "expiring_assets", "expiring_employees", "expiring_locations"]} horizontal />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_rate_change };