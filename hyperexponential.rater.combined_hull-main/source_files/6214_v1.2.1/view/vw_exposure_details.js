import * as HX from "hx-model-components";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Exposure Details">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "cds/exposure/aggregate/exposure"
          ]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_exposure_details };