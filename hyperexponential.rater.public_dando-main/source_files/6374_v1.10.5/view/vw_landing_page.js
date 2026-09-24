import * as HX from "hx-model-components";

function vw_landing_page() {
  return (
    <HX.Page title="Landing Page" shownBy="model_state/show_landing_page">
      <HX.Section title="Start Policy">
        <HX.Collection
          fields={["cds/capiq_wb_id"]} // for testing
        />
        <HX.Pane flow="right">
          {/* <HX.Pane ratio={2}>
            <HX.Notes field="model_state/landing_page_info" />
          </HX.Pane> */}
          <HX.Pane>
            <HX.Button task="populate_capiq_data_from_wb_task" title="Start Policy" />
            {/*<HX.Button task="skip_capiq_task" title="Skip" />*/}
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_landing_page };