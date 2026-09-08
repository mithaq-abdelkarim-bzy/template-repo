import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.With context={{ type: "list", path: "cds/layers", index: n }}>

        <HX.Section title="Renewal vs. Expiring" shownBy={"/cds/rate_change/show_layer_" + (n + 1)} >
          {/* <HX.Section title="Renewal vs. Expiring"> */}
          <HX.Pane>
            <HX.Table
              data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                "benchmark_premium",
                "bpi",
                null,
                "technical_premium",
                "tpi"
              ]}
              fields={[{ field: "renewal", width: 200 }, { field: "expiring", width: 200 }]}
              with="rate_change"
            />
          </HX.Pane>
        </HX.Section >

        <HX.Section title="Rate Change" shownBy="/cds/rate_change/has_expiring_data" defaultCollapsed>
          <HX.Pane flow="right" >
            <HX.Button task="rarc_task" title="Calculate Rate Change" />
            <HX.Pane />
          </HX.Pane>
          <HX.Notes with="/cds/rate_change" field="rarc_run_again_message" shownBy="rarc_message_show" />

          <HX.Pane shownBy="/cds/rate_change/rarc_calcs_show">
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={["exposure_change", "risk_characteristics_change",
                  "deductible_change", "limit_change", "terms_conditions_change", "brokerage_change",
                  "other_change", null, "rate_change"]}
                fields={[{ field: "model_calculated", width: 125 }, { field: "uw_selected", width: 125 }, { field: "comments", width: 250 }]}
                with="rate_change"
              />
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)" fields={["rate_change/risk_adjusted_rate_change/uw_selected"]} shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)" fields={["rate_change/risk_adjusted_rate_change_case_priced/uw_selected"]} shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" " fields={["rate_change/risk_adjusted_rate_change_case_priced/comments"]} shownBy="/cds/standard_fields/is_case_priced" />
              < HX.Pane shownBy="/cds/standard_fields/is_rater_priced"></HX.Pane>
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>

        </HX.Section>

      </HX.With>
    );
  }

  return objects
}

function vw_rate_change() {
  return (
    <HX.Page title="Rate Change" shownBy="cds/standard_fields/is_renewal" >

      {/* Moved this section to Risk Infromation as requested by UW */}
      {/* <HX.Section title="Fetch Expiring Policy">
        <HX.Pane flow="right" >
          <HX.Collection fields={["cds/rate_change/expiring_policy_option_id"]} />
          <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" />
        </HX.Pane>
      </HX.Section> */}

      {vw_loop_rate_change_layer(max_layers())}

    </HX.Page >
  )
}
export { vw_rate_change };