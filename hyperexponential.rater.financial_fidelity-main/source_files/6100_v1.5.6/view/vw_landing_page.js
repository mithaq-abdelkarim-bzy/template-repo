import * as HX from "hx-model-components";

function vw_landing_page() {
  return (
    <HX.Page title="Landing Page" shownBy="model_state/show_landing_page">
      <HX.Section title="Start Policy">
        <HX.Pane flow="right">
          <HX.Button task="start_renewal_task" title="Press on 'Import Expiring Policy Data' at the top right corner then click here" />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_landing_page };