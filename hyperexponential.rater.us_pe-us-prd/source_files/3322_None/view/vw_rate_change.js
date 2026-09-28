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
              fields={[{ field: "renewal", width: 250 }, { field: "expiring", width: 250 }]}
              with="rate_change"
            />
          </HX.Pane>
        </HX.With>

        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane>
            <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
              data={["exposure_change", "risk_characteristics_change",
                "deductible_change", "limit_change", "terms_conditions_change", "brokerage_change",
                "other_change", null, "rate_change"]}
              fields={[{ field: "model_calculated", width: 250 }, { field: "uw_selected", width: 250 }, { field: "comments", width: 250 }]}
              with="rate_change"
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
    <HX.Page title="Rate Change" fullWidth={false} shownBy="cds/standard_fields/is_renewal" >
      <HX.Section title="Fetch Expiring Policy">
        <HX.Pane flow="right" >
          <HX.Collection fields={["cds/rate_change/expiring_policy_option_id"]} />
          <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            title=""
            data={[{ datum: "cds/layers", width: 250 }]}
            fields={[{ field: "status.read_only" }]}
            transpose
          />
        </HX.Pane>
      </HX.Section>

      {vw_loop_rate_change_layer(max_layers())}


    </HX.Page >
  )
}
export { vw_rate_change };