import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];
  const renewalVsExpiring_actuarial = ["premium_policy_term_100pct", "premium_policy_term_beazley_share", "written_line", null, { datum: "benchmark_premium_post_uw_adj", elementInfoBy: "/cds/rate_change/pre_nmp_calculation_msg" }, "benchmark_premium", "bpi"]
  const renewalVsExpiring_non_actuarial = ["premium_policy_term_100pct", "premium_policy_term_beazley_share", "written_line", null, "benchmark_premium", "bpi"]

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Renewal"} shownBy={"cds/rate_change/show_layer_" + (n + 1)} >
        <HX.Pane flow="right" >
          <HX.Button task="rarc_task" title="Calculate Rate Change" shownBy="/cds/standard_fields/is_rater_priced" />
          <HX.Pane />
        </HX.Pane>
        <HX.Notes with="cds/rate_change" field="reg_warning" shownBy="show_reg_warning" />
        <HX.Notes with="cds/rate_change" field="rarc_run_again_message" shownBy="rarc_message_show" />

        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          {/* <HX.Collection fields={["rate_change/temp_storage/quoted_premium", "rate_change/temp_storage/benchmark_premium"]} /> */}
          <HX.Pane flow="right">
            <HX.Table
              title="Hull"
              data={renewalVsExpiring_actuarial}
              fields={[{ field: "renewal", width: 150 }, { field: "expiring", width: 150 }]}
              with="rate_change/hull"
              shownBy="/cds/exposure/granular/show_aircraft_summary"
              kb-interactive
            />
            <HX.Table
              title="Liability"
              data={renewalVsExpiring_actuarial}
              fields={[{ field: "renewal", width: 150 }, { field: "expiring", width: 150 }]}
              with="rate_change/liability"
              shownBy="/cds/exposure/granular/show_aircraft_summary"
              kb-interactive
            />
            <HX.Table
              title="Hull"
              data={renewalVsExpiring_non_actuarial}
              fields={[{ field: "renewal", width: 150 }, { field: "expiring", width: 150 }]}
              with="rate_change/hull"
              shownBy="/cds/exposure/granular/hide_aircraft_summary"
              kb-interactive
            />
            <HX.Table
              title="Liability"
              data={renewalVsExpiring_non_actuarial}
              fields={[{ field: "renewal", width: 150 }, { field: "expiring", width: 150 }]}
              with="rate_change/liability"
              shownBy="/cds/exposure/granular/hide_aircraft_summary"
              kb-interactive
            />
          </HX.Pane>

          <HX.Pane shownBy="/cds/rate_change/rarc_calcs_show" flow="right">

            {/* Hull Rate Change */}
            <HX.Pane>
              <HX.Table
                title="Hull Rate Change"
                shownBy="/cds/standard_fields/is_rater_priced"
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
                fields={[{ field: "model_calculated", width: 125 }, { field: "uw_selected", width: 125 }, { field: "comments", width: 250 }]}
                with="rate_change/hull"
                kb-interactive
              />
              <HX.Collection title="Hull Final Rate Change (Gross Brokerage)" with="rate_change" fields={["hull/risk_adjusted_rate_change/uw_selected", null]} horizontal shownBy="/cds/standard_fields/is_rater_priced" />
            </HX.Pane>

            {/* Liability Rate Change */}
            <HX.Pane>
              <HX.Table
                title="Liability Rate Change"
                shownBy="/cds/standard_fields/is_rater_priced"
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
                fields={[{ field: "model_calculated", width: 125 }, { field: "uw_selected", width: 125 }, { field: "comments", width: 250 }]}
                with="rate_change/liability"
                kb-interactive
              />
              <HX.Collection title="Liability Final Rate Change (Gross Brokerage)" with="rate_change" fields={["liability/risk_adjusted_rate_change/uw_selected", null]} horizontal shownBy="/cds/standard_fields/is_rater_priced" />
            </HX.Pane>

          </HX.Pane>
        </HX.With>

      </HX.Section >
    );
  }

  return objects
}

function vw_rate_change() {
  return (
    <HX.Page title="Rate Change" fullWidth shownBy="cds/exposure/granular/show_rc_page" viewScale={0.9} >
      <HX.Section title="Fetch Expiring Policy" >
        {/* <HX.Collection fields={["debug_str"]} /> */}
        {/* <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection fields={["rate_change/rebased_expiring_premium"]} />
        </HX.With> */}
        < HX.Pane flow="right" >
          <HX.Collection fields={["cds/rate_change/expiring_policy_option_id"]} />
          <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
        </HX.Pane>
      </HX.Section>

      {vw_loop_rate_change_layer(max_layers())}

      <HX.Section title="Rate Change" shownBy="/cds/standard_fields/is_case_priced">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane >
            <HX.Collection title="Hull Final Rate Change (Gross Brokerage)" with="rate_change" fields={["hull/risk_adjusted_rate_change_case_priced/uw_selected", null]} horizontal />
            <HX.Collection title="Liability Final Rate Change (Gross Brokerage)" with="rate_change" fields={["liability/risk_adjusted_rate_change_case_priced/uw_selected", null]} horizontal />
            <HX.Collection title=" " fields={["rate_change/risk_adjusted_rate_change_case_priced/comments"]} />
          </HX.Pane>
        </HX.With>
      </HX.Section>

    </HX.Page >
  )
}
export { vw_rate_change };