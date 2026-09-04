import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Renewal"} shownBy={"cds/rate_change/show_layer_" + (n + 1)} >
        <HX.Pane flow="right" >
          <HX.Button task="rarc_task" title="Calculate Rate Change" />
          <HX.Pane />
        </HX.Pane>
        <HX.Notes with="cds/rate_change" field="rarc_run_again_message" shownBy="rarc_message_show" />

        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          {/* <HX.Collection fields={["rate_change/temp_storage/quoted_premium", "rate_change/temp_storage/benchmark_premium"]} /> */}
          <HX.Pane>
            {/* <HX.Collection fields={["rate_change/expiring_layer", null, null]} horizontal /> */}
            <HX.Table
              data={["premium/line_100pct/annualised", "premium/beazley_line/annualised", "written_line"]}
              fields={[{ field: "renewal", width: 150 }, { field: "expiring", width: 150 }, { field: "expiring_override", width: 200 }]}
              with="rate_change"
            />



          </HX.Pane>
          <HX.Pane shownBy="/cds/rate_change/rarc_calcs_show" >
            {/* <HX.Pane> */}
            <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
              data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                // "brokerage_change", # removed 
                "other_change",
                null,
                "rate_change"
              ]}
              fields={[{ field: "model_calculated", width: 140 }, { field: "uw_selected", width: 140 }, { field: "comments", width: 250 }]}
              with="rate_change"
              kb-interactive
            />
            <HX.Collection title="Final Rate Change"
              fields={[
                { field: "rate_change/risk_adjusted_rate_change", shownBy: "/cds/standard_fields/is_rater_priced" },

                // Used for checking gross rate change quickly
                // { field: "rate_change/risk_adjusted_rate_change_gross_for_reporting", shownBy: "/cds/standard_fields/is_rater_priced" },

                { field: "rate_change/risk_adjusted_rate_change_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
                null, null
              ]}
              horizontal
            />
          </HX.Pane>
        </HX.With>
      </HX.Section >
    );
  }

  return objects
}

function vw_rate_change() {
  return (
    <HX.Page title="Rate Change" viewScale={0.9} shownBy="cds/standard_fields/is_renewal" >
      <HX.Section title="Fetch Expiring Policy">
        <HX.Pane flow="right" >
          <HX.Collection fields={["cds/rate_change/expiring_policy_option_id"]} />
          <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" />
        </HX.Pane>
      </HX.Section>

      {vw_loop_rate_change_layer(max_layers())}

    </HX.Page >
  )
}
export { vw_rate_change };