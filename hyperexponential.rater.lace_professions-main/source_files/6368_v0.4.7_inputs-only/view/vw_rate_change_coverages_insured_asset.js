// v0.3.0
// USE FOR COVERAGES
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer_coverages_insured_asset(num_layers, num_coverages) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Renewal Layer " + (n + 1)} shownBy={"cds/rate_change/show_layer_" + (n + 1)} >
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane>
            <HX.Collection fields={["rate_change/expiring_layer", null, null]} horizontal />
            <HX.Pane flow="right" >
              {/* Coverage 1 */}
              <HX.Pane >
                <HX.Table
                  data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised",

                  ]}
                  fields={[{ field: "expiring", width: 130 }, { field: "expiring_revalued", width: 130, shownBy: "example_coverage_1/show_expiring_revalued" }, { field: "renewal", width: 130 }]}
                  with="rate_change"
                />
                <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                  data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    // "example_coverage_1/brokerage_change", # removed 
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                  fields={[{ field: "model_calculated", width: 100 },
                  //{ field: "uw_selected", width: 140 }, // Edit v0.3.0
                  { field: "uw_override", width: 100 }, // Edit v0.3.0
                  { field: "final", width: 100 }, // Edit v0.3.0
                  { field: "comments", width: 150 }]} // Edit v0.3.0
                  with="rate_change"
                  syncColumnWidthsKey="syncRateChange"
                  kb-interactive
                />
                <HX.Collection title="Final Rate Change"
                  fields={[
                    { field: "rate_change/example_coverage_1/risk_adjusted_rate_change", shownBy: "/cds/standard_fields/is_rater_priced" },
                    { field: "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
                    null, null
                  ]}
                  horizontal
                />
              </HX.Pane>
              {/* Coverage 2 */}
              <HX.Pane>
                {/* <HX.Collection fields={["rate_change/expiring_layer", null, null]} horizontal /> */}
                <HX.Table
                  data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised",

                  ]}
                  fields={[{ field: "expiring", width: 130 }, { field: "expiring_revalued", width: 130, shownBy: "example_coverage_2/show_expiring_revalued" }, { field: "renewal", width: 130 }]}
                  with="rate_change"
                />
                <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                  data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    // "example_coverage_2/brokerage_change", # removed 
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                  fields={[{ field: "model_calculated", width: 140 },
                  //{ field: "uw_selected", width: 140 }, // Edit v0.3.0
                  { field: "uw_override", width: 140 },// Edit v0.3.0
                  { field: "final", width: 140 },// Edit v0.3.0
                  { field: "comments", width: 250 }]} // Edit v0.3.0
                  with="rate_change"
                  syncColumnWidthsKey="syncRateChange"
                  kb-interactive
                />
                <HX.Collection title="Final Rate Change"
                  fields={[
                    { field: "rate_change/example_coverage_2/risk_adjusted_rate_change", shownBy: "/cds/standard_fields/is_rater_priced" },
                    { field: "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
                    null, null
                  ]}
                  horizontal
                />
              </HX.Pane>
            </HX.Pane>
          </HX.Pane>
        </HX.With>
      </HX.Section >
    );
  }

  return objects
}

function vw_rate_change_coverages_insured_asset() {
  return (
    <HX.Page title="Rate Change Coverages Insured Assets" fullWidth viewScale={1} shownBy="model_state/show_rate_change_coverage_ia_use">
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
          <HX.Button task="expiring_policy_fetch_coverages_task" title="Fetch Expiring Data" shownBy="cds/rate_change/has_rarc_not_run" />
          <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
          <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
          <HX.Button title="Calculate Rate Change" task="rarc_task_coverages_insured_asset" shownBy="cds/standard_fields/is_rater_priced" />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes with="cds/rate_change" field="rarc_run_again_message" shownBy="rarc_message_show" />
        </HX.Pane>
        {/* // EDIT v0.3.0  */}
        <HX.Section title="Rate Change Instructions and Key" defaultCollapsed>
          <HX.Pane flow="right">
            <HX.Notes field="cds/rate_change/instructions" />
          </HX.Pane>
        </HX.Section >
      </HX.Section>

      {vw_loop_rate_change_layer_coverages_insured_asset(max_layers())}

    </HX.Page >
  )
}
export { vw_rate_change_coverages_insured_asset };