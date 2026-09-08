import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Underwriter Rationale">
        <HX.Notes field="cds/standard_fields/uw_rationale" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rationale };