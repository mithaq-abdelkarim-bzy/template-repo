// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers, max_raw_data_columns } from "view/vw_constants";


function vw_healthcare_cat_pricing_calculation(scale) {
  return (
    <HX.Page title="Pricing Calculation" fullWidth={true} viewScale={scale} shownBy="model_state/show_healthcare_cat">
      <HX.With context={{ type: "struct", path: "cds/healthcare_cat" }}>
        {/* <HX.Section title="Pricing Specifics">
          <HX.Pane>
            <HX.Table
              with="pricing"
              data={[
                "territory_adjustment",
                "trial_history_adjustment",
                "type_of_business_adjustment",
                "high_low_adjustment",
                "social_inflation_impact",
                "total_risk_adjustment",
              ]}
              fields={[

                { field: "value", width: 150 },
                { field: "select", width: 150 },
              ]}
              kb-interactive

              rowHeaderSettings={{ width: 350 }}
            />
          </HX.Pane>
        </HX.Section> */}
        <HX.Section title="Expected Cost Per Layer">
          <HX.Pane>
            <HX.Table
              data={[
                { datum: "/cds/layers", width: 150 }
              ]}
              fields={[
                "healthcare_cat/expected_cost_in_layer_total",
                "healthcare_cat/expected_cost_in_layer_beazley_share",

              ]}
              kb-interactive
              transpose
              // syncColumnWidthsKey="total_risk_adjustment"
              rowHeaderSettings={{ width: 350 }}
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Pricing Calculation">
          <HX.Pane>
            <HX.Table
              title="Loss distribution"
              data={[
                "/healthcare_cat/pricing_calc/loss_distribution_calculation"
              ]}
              fields={[
                { field: "band_size", width: 150 },
                { field: "loss_percentile", width: 150 },
                { field: "ulr", width: 150 },
                null,
                { field: "fgu_expected_cat_loss_01", width: 150 },
                { field: "expected_loss_in_layer_01", width: 150 },
                { field: "expected_loss_x_prob_of_loss_01", width: 150 },
                null,
                { field: "fgu_expected_cat_loss_02", width: 150 },
                { field: "expected_loss_in_layer_02", width: 150 },
                { field: "expected_loss_x_prob_of_loss_02", width: 150 },
                null,
                { field: "fgu_expected_cat_loss_03", width: 150 },
                { field: "expected_loss_in_layer_03", width: 150 },
                { field: "expected_loss_x_prob_of_loss_03", width: 150 },
                null,
                { field: "fgu_expected_cat_loss_04", width: 150 },
                { field: "expected_loss_in_layer_04", width: 150 },
                { field: "expected_loss_x_prob_of_loss_04", width: 150 },
                null,
                { field: "fgu_expected_cat_loss_05", width: 150 },
                { field: "expected_loss_in_layer_05", width: 150 },
                { field: "expected_loss_x_prob_of_loss_05", width: 150 }

              ]}
              kb-interactive
            />

          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_healthcare_cat_pricing_calculation };