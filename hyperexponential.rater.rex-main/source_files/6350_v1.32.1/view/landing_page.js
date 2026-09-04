import * as HX from "hx-model-components";

function landing_page() {
  return (
    <HX.Page title="Landing Page" shownBy="model_state/show_landing_page">
      <HX.Section title="Start Policy">
        <HX.Pane flow="right">
          <HX.Button task="start_renewal_task" title="Start Policy" />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { landing_page };