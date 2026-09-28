import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Renewal Layer " + (n + 1)} defaultCollapsed shownBy={"cds/rate_change/show_layer_" + (n + 1)} >
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane flow="right">
            <HX.Collection fields={["rate_change/expiring_layer"]} />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
        </HX.With>

        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane>
            <HX.Table
              data={["premium_annualized_100pct", "premium_annualized_beazley_share"]}
              fields={[{ field: "renewal", width: 200 }, { field: "expiring", width: 200 }]}
              with="rate_change"
            />
          </HX.Pane>
        </HX.With>

        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane>
            <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
              data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change",
                null,
                "rate_change"
              ]}
              fields={[{ field: "model_calculated", width: 130 }, { field: "uw_selected", width: 130 }, { field: "comments", width: 250 }]}
              with="rate_change"
              kb-interactive
            />
          </HX.Pane>
        </HX.With>
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane flow="right">
            <HX.Collection title="Final Rate Change (Gross Brokerage)" fields={["rate_change/risk_adjusted_rate_change/uw_selected"]} shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Collection title="Final Rate Change (Gross Brokerage)" fields={["rate_change/risk_adjusted_rate_change_case_priced/uw_selected"]} shownBy="/cds/standard_fields/is_case_priced" />
            <HX.Collection title=" " fields={["rate_change/risk_adjusted_rate_change_case_priced/comments"]} shownBy="/cds/standard_fields/is_case_priced" />
            < HX.Pane shownBy="/cds/standard_fields/is_rater_priced"></HX.Pane>
            <HX.Pane></HX.Pane>
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
            title=""
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