// v0.3.0
// USE FOR COVERAGES
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_pricing_coverages(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Coverage Options Layer " + (n + 1)} shownBy={"cds/rate_change/show_layer_" + (n + 1)}>
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane flow="right">
            <HX.Collection
              title="Coverage 1"
              fields={[
                "coverages/example_coverage_1/currency",
                "coverages/example_coverage_1/limit",
                "coverages/example_coverage_1/excess",
                "coverages/example_coverage_1/deductible",
                "coverages/example_coverage_1/expected_loss_cost_100"
              ]} />
            <HX.Collection
              title="Coverage 2"
              fields={[
                "coverages/example_coverage_2/currency",
                "coverages/example_coverage_2/limit",
                "coverages/example_coverage_2/excess",
                "coverages/example_coverage_2/deductible",
                "coverages/example_coverage_2/expected_loss_cost_100"
              ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.With>
      </HX.Section>
    );
  }
  return objects
}

function vw_pricing_coverages(scale) {
  return (
    <HX.Page title="Pricing Coverages" fullWidth={true} viewScale={scale} shownBy="model_state/coverage_no_ia_use">
      {vw_loop_pricing_coverages(max_layers())}
    </HX.Page>
  )
}

export { vw_pricing_coverages };