import * as HX from "hx-model-components";

function vw_landing_page() {
  return (
    <HX.Page title="Landing Page" shownBy="model_state/show_landing_page">
      <HX.Section title="Start Policy">
        <HX.Pane>
          <HX.Notes field="model_state/landing_page_info" />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Button task="start_renewal_task" title="Start Policy" />
            {/* <HX.Button task="sync_expiring_ids" title="Sync Expiring IDs" /> */}
          </HX.Pane>
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_landing_page };