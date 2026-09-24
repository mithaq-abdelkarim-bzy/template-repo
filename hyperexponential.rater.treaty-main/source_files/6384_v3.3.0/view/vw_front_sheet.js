import * as HX from "hx-model-components";

function vw_front_sheet(scale) {
  return (
    <HX.Page title="Automatic Front Sheet" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Front Sheet">
        <HX.Pane>
          <HX.Collection
            numCols={2}
            fields={[
              { field: "synergy_upload/to_user_only" },
              null
            ]}
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Button task="synergy_send_front_sheet_task"
            title="Send Front Sheet" />
        </HX.Pane>

      </HX.Section>
    </HX.Page>
  )
}

export { vw_front_sheet };