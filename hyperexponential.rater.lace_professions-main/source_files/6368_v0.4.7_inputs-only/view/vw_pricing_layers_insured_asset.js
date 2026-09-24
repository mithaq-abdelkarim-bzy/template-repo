// v0.3.0
// USE FOR COVERAGES
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_pricing_layers_insured_asset(num_layers) {
  const objects = [];

  // for (let n = 0; n < num_layers; n++) {
  n = 0 // NOTE: Using only one layer with insured interest. Sperate list of insured asset can be used if coverages are mutually exclusive.
  objects.push(
    <HX.Section title={"Coverage Options Layer " + (n + 1)} shownBy={"cds/rate_change/show_layer_" + (n + 1)}>
      <HX.Pane>
        <HX.Table
          title="Layer info"
          data={[{ datum: "cds/layers", width: 250 }]}
          fields={[

            "brokerage",

          ]}
          freezeLeft={0}
          transpose
          kb-interactive
        />

      </HX.Pane>

      <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
        <HX.Pane flow="right">
          <HX.Table
            data={["layers"]}
            fields={
              [
                "unique_id",
                "currency",
                "limit",
                "excess",
                "deductible",
                "quoted_premium_100",
                "brokerage",
                "status",
                "written_line",
                "section_reference",
                "expected_loss_cost_100",
                "quoted_premium",
                "quoted_premium_annual",
              ]
            }
            title="Insured Assets"
            kb-interactive
            freezeRight={1}
            dynamic
          />
        </HX.Pane>
      </HX.With>
    </HX.Section>
  );
  // }
  return objects
}

function vw_pricing_layers_insured_asset(scale) {
  return (
    // <HX.Page title="Pricing Layer Insured Asset" fullWidth={true} viewScale={scale} shownBy="model_state/coverage_use">
    <HX.Page title="Pricing Layer Insured Asset" fullWidth={true} viewScale={scale} shownBy="model_state/layer_ia_use">
      {vw_loop_pricing_layers_insured_asset(max_layers())}
    </HX.Page>
  )
}

export { vw_pricing_layers_insured_asset };