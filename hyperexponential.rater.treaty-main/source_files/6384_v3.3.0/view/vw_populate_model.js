import * as HX from "hx-model-components";

function vw_populate_model(scale) {
  return (
    <HX.Page title="Populate Model" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Populate Model (Bermuda Focus)">
        <HX.Pane>
          <HX.Collection
            numCols={2}
            fields={[
              "cds/populate_model/policy_option_id",
              null
            ]}
          />
          <HX.Button task="populate_model_task"
            title="Populate Model" />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_populate_model };