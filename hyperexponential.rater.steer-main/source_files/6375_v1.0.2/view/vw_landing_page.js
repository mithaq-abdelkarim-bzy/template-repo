// # v0.5.1
import * as HX from "hx-model-components";

function vw_landing_page(scale) {
  return (
    <HX.Page title="Landing Page" viewScale={scale} shownBy="model_state/show_landing_page">
      <HX.Section title="Start Policy">
        <HX.Pane flow="right">
          <HX.Pane ratio={2}>
            <HX.Notes field="model_state/landing_page_info" />
          </HX.Pane>
          <HX.Pane>
            <HX.Button task="start_renewal_task" title="Start Policy" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_landing_page };