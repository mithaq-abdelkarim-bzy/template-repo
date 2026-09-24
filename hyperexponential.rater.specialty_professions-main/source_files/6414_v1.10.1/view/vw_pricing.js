// v0.3.0
import * as HX from "hx-model-components";

function vw_pricing(scale) {
  return (
    // <HX.Page title="Pricing" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
    <HX.Page title="Pricing" fullWidth={true} viewScale={scale} shownBy="model_state/layer_no_ia_use">
      <HX.Section title="Layer Options (Up to 6 layers)">
        <HX.Table
          data={[{ datum: "layers", width: 250 }]}
          fields={["currency", "limit", "excess", "deductible", "expected_loss_cost_100"]}
          title="Quoted Layers"
          with="cds"
          kb-interactive
          //dynamic // filter and sort
          transpose
        />
      </HX.Section>
      <HX.Section title="Layer Options (Only one layer)">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Collection
              fields={["currency", "limit", "excess", "deductible", "expected_loss_cost_100"]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.With>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_pricing };