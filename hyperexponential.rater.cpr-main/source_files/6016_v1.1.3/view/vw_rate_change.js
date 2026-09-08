import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Renewal Layer " + (n + 1)} defaultCollapsed shownBy={"cds/rate_change/show_layer_" + (n + 1)} >
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane>
            {/* <HX.Collection fields={["rate_change/expiring_layer", null, null]} horizontal /> */}
            <HX.Table
              data={["line_100pct/annualised", "beazley_line/annualised"]}
              fields={[{ field: "expiring", width: 150 }, { field: "renewal", width: 150 }]}
              with="rate_change/premium"
            />
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
    <HX.Page title="Rate Change" fullWidth={false} shownBy="model_state/show_rate_change" >
      <HX.Section title="Fetch Expiring Policy">
        <HX.Pane flow="right" >
          <HX.Collection fields={["cds/rate_change/expiring_policy_option_id", null]} horizontal />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            title="Deal Status by Renewal Layers"
            data={[{ datum: "cds/layers", width: 200 }]}
            fields={[{ field: "status.read_only" }]}
            transpose
          />
        </HX.Pane>
        <HX.Pane flow="right" >
          <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" shownBy="cds/rate_change/has_rarc_not_run" />
          <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
          <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
          <HX.Button title="Calculate Rate Change" task="rarc_task" shownBy="cds/standard_fields/is_rater_priced" />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes with="cds/rate_change" field="rarc_run_again_message" shownBy="rarc_message_show" />
        </HX.Pane>
      </HX.Section>

      {vw_loop_rate_change_layer(max_layers())}

    </HX.Page >
  )
}
export { vw_rate_change };