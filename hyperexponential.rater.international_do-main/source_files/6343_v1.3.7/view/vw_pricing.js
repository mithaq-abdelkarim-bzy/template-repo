import * as HX from "hx-model-components";

function vw_pricing(scale) {
  return (
    <HX.Page title="Pricing" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Coverage Options (Up to 6 layers)">
        <HX.Table
          data={[{ datum: "layers", width: 250 }]}
          fields={["limit", "excess", "deductible", "expected_loss_cost"]}
          title="Quoted Layers"
          with="cds"
          kb-interactive
          //dynamic // filter and sort
          transpose
        />
      </HX.Section>
      <HX.Section title="Coverage Options (Only one layer)">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Collection
              fields={["limit", "excess", "deductible", "expected_loss_cost"]} />
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