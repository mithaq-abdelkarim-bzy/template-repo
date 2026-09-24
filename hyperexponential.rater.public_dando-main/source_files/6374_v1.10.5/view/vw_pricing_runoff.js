import * as HX from "hx-model-components";

function vw_pricing_runoff(scale) {
  return (
    <HX.Page title="Runoff Pricing" fullWidth={true} viewScale={scale} shownBy="cds/is_runoff">
      <HX.Section title="Runoff Adjustment">
        <HX.Pane>
          <HX.Table
            syncColumnWidthsKey="sync_layers"
            data={[{ datum: "cds/layers", minWidth: 175, maxWidth: 250 }]}
            fields={[
              "coverages/side_a/premium",
              "runoff_adjustment",
              "runoff_original_premium"
            ]}
            rowHeaderSettings={{ width: 250 }}
            transpose
            shownBy="cds/is_side_a"
            kb-interactive
          />
          <HX.Table
            syncColumnWidthsKey="sync_layers"
            data={[{ datum: "cds/layers", minWidth: 175, maxWidth: 250 }]}
            fields={[
              "coverages/abc/premium",
              "runoff_adjustment",
              "runoff_original_premium"
            ]}
            rowHeaderSettings={{ width: 250 }}
            transpose
            shownBy="cds/is_abc"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_pricing_runoff };