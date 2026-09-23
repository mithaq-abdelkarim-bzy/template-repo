import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale}>
      <HX.Section title="Underwriter Rationale">
        <HX.Notes field="cds/standard_fields/uw_rationale" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rationale };