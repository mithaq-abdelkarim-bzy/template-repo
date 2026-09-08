import * as HX from "hx-model-components";

function vw_landing_page(scale) {
  return (
    <HX.Page title="Landing Page" shownBy="model_state/show_landing_page" >
      <HX.Section title="Start Policy">
        <HX.Pane flow="right">
          <HX.Button task="start_renewal_task" title="Start Policy" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="NB:" collapsible={false}>
        <HX.Notes field="model_state/landing_page_info" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_landing_page };