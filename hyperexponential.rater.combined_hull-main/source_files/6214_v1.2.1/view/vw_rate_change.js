import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];
  const renewalVsExpiring = [
    "premium_policy_term_100pct",
    "premium_policy_term_beazley_share",
    "written_line",
    null,
    "benchmark_premium",
    "bpi",
  ];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section
        title={"Renewal"}
        shownBy={"cds/rate_change/show_layer_" + (n + 1)}
      >
        <HX.Pane flow="right">
          <HX.Button
            task="rarc_task"
            title="Calculate Rate Change"
            shownBy="/cds/standard_fields/is_rater_priced"
          />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Notes
            with="cds/rate_change"
            field="rarc_note_for_uw"
            shownBy="/non_cds/show_hide_toggles/rate_change/show_rarc_note_for_uw"
          />
          <HX.Notes
            with="cds/rate_change"
            field="rarc_run_again_message"
            shownBy="rarc_message_show"
          />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          {/* <HX.Collection fields={["rate_change/temp_storage/quoted_premium", "rate_change/temp_storage/benchmark_premium"]} /> */}
          <HX.Pane flow="right">
            <HX.Table
              title="Hull"
              data={renewalVsExpiring}
              fields={[
                { field: "renewal", width: 150 },
                { field: "expiring", width: 150 },
              ]}
              with="rate_change/hull"
              shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage"
              kb-interactive
            />
            <HX.Table
              title="Iv"
              data={renewalVsExpiring}
              fields={[
                { field: "renewal", width: 150 },
                { field: "expiring", width: 150 },
              ]}
              with="rate_change/iv"
              shownBy="/non_cds/show_hide_toggles/iv/show_iv_coverage"
              kb-interactive
            />
            <HX.Table
              title="War"
              data={renewalVsExpiring}
              fields={[
                { field: "renewal", width: 150 },
                { field: "expiring", width: 150 },
              ]}
              with="rate_change/war"
              shownBy="/non_cds/show_hide_toggles/war/show_war_coverage"
              kb-interactive
            />
            <HX.Table
              title="Loss of Hire (LOH)"
              data={renewalVsExpiring}
              fields={[
                { field: "renewal", width: 150 },
                { field: "expiring", width: 150 },
              ]}
              with="rate_change/loh"
              shownBy="/non_cds/show_hide_toggles/loh/show_loh_coverage"
              kb-interactive
            />
            <HX.Table
              title="Shipbuilders"
              data={renewalVsExpiring}
              fields={[
                { field: "renewal", width: 150 },
                { field: "expiring", width: 150 },
              ]}
              with="rate_change/ship_building"
              shownBy="/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
              kb-interactive
            />
          </HX.Pane>

          <HX.Pane flow="right">
            {/* Hull Rate Change */}
            <HX.Pane shownBy="rate_change/hull/rarc_calcs_show">
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
                  "rate_change",
                ]}
                fields={[
                  { field: "model_calculated", width: 125 },
                  { field: "uw_selected", width: 125 },
                  { field: "comments", width: 250 },
                ]}
                with="rate_change/hull"
                kb-interactive
              />
              <HX.Collection
                title="Hull Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={["hull/risk_adjusted_rate_change_uw_selected/uw_selected", null]}
                horizontal
                shownBy="/cds/standard_fields/is_rater_priced"
              />
            </HX.Pane>

            {/* IV Rate Change */}
            <HX.Pane shownBy="rate_change/iv/rarc_calcs_show">
              <HX.Table
                title="IV Rate Change"
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
                  "rate_change",
                ]}
                fields={[
                  { field: "model_calculated", width: 125 },
                  { field: "uw_selected", width: 125 },
                  { field: "comments", width: 250 },
                ]}
                with="rate_change/iv"
                kb-interactive
              />
              <HX.Collection
                title="IV Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={["iv/risk_adjusted_rate_change_uw_selected/uw_selected", null]}
                horizontal
                shownBy="/cds/standard_fields/is_rater_priced"
              />
            </HX.Pane>

            {/* War Rate Change */}
            <HX.Pane shownBy="rate_change/war/rarc_calcs_show">
              <HX.Table
                title="War Rate Change"
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
                  "rate_change",
                ]}
                fields={[
                  { field: "model_calculated", width: 125 },
                  { field: "uw_selected", width: 125 },
                  { field: "comments", width: 250 },
                ]}
                with="rate_change/war"
                kb-interactive
              />
              <HX.Collection
                title="War Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={["war/risk_adjusted_rate_change_uw_selected/uw_selected", null]}
                horizontal
                shownBy="/cds/standard_fields/is_rater_priced"
              />
            </HX.Pane>

            {/* LOH Rate Change */}
            <HX.Pane shownBy="rate_change/loh/rarc_calcs_show">
              <HX.Table
                title="Loss of Hire (LOH) Rate Change"
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
                  "rate_change",
                ]}
                fields={[
                  { field: "model_calculated", width: 125 },
                  { field: "uw_selected", width: 125 },
                  { field: "comments", width: 250 },
                ]}
                with="rate_change/loh"
                kb-interactive
              />
              <HX.Collection
                title="LOH Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={["loh/risk_adjusted_rate_change_uw_selected/uw_selected", null]}
                horizontal
                shownBy="/cds/standard_fields/is_rater_priced"
              />
            </HX.Pane>

            {/* Shipbuilders Rate Change */}
            <HX.Pane shownBy="rate_change/ship_building/rarc_calcs_show">
              <HX.Table
                title="Shipbuilders Rate Change"
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
                  "rate_change",
                ]}
                fields={[
                  { field: "model_calculated", width: 125 },
                  { field: "uw_selected", width: 125 },
                  { field: "comments", width: 250 },
                ]}
                with="rate_change/ship_building"
                kb-interactive
              />
              <HX.Collection
                title="Shipbuilders Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={[
                  "ship_building/risk_adjusted_rate_change_uw_selected/uw_selected",
                  null,
                ]}
                horizontal
                shownBy="/cds/standard_fields/is_rater_priced"
              />
            </HX.Pane>
          </HX.Pane>
        </HX.With>
      </HX.Section>
    );
  }

  return objects;
}

function vw_rate_change() {
  return (
    <HX.Page
      title="Rate Change"
      fullWidth
      shownBy="cds/standard_fields/is_renewal"
      viewScale={0.9}
    >
      <HX.Section title="Fetch Expiring Policy">
        {/* <HX.Collection fields={["debug_str"]} /> */}
        {/* <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection fields={["rate_change/rebased_expiring_premium"]} />
        </HX.With> */}
        <HX.Pane flow="right">
          <HX.Collection
            fields={["cds/rate_change/expiring_policy_option_id"]}
          />
          <HX.Button
            task="expiring_policy_fetch_task"
            title="Fetch Expiring Data"
          />
          {/* <HX.Button
            task="policy_json_download_task"
            title="Download JSON Data"
          />
          <HX.File field="cds/rate_change/output_json_example_data" /> */}
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane></HX.Pane>
      </HX.Section>

      {vw_loop_rate_change_layer(max_layers())}

      <HX.Section
        title="Rate Change"
        shownBy="/cds/standard_fields/is_case_priced"
      >
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane>
            <HX.Collection
              title="Hull Final Rate Change (Gross Brokerage)"
              with="rate_change"
              fields={[
                "hull/risk_adjusted_rate_change_case_priced/uw_selected",
                null,
              ]}
              shownBy="hull/rarc_calcs_show"
              horizontal
            />
            <HX.Collection
              title="IV Final Rate Change (Gross Brokerage)"
              with="rate_change"
              fields={[
                "iv/risk_adjusted_rate_change_case_priced/uw_selected",
                null,
              ]}
              shownBy="iv/rarc_calcs_show"
              horizontal
            />
            <HX.Collection
              title="War Final Rate Change (Gross Brokerage)"
              with="rate_change"
              fields={[
                "war/risk_adjusted_rate_change_case_priced/uw_selected",
                null,
              ]}
              shownBy="war/rarc_calcs_show"
              horizontal
            />
            <HX.Collection
              title="LOH Final Rate Change (Gross Brokerage)"
              with="rate_change"
              fields={[
                "loh/risk_adjusted_rate_change_case_priced/uw_selected",
                null,
              ]}
              shownBy="loh/rarc_calcs_show"
              horizontal
            />
            <HX.Collection
              title="Shipbuilders Final Rate Change (Gross Brokerage)"
              with="rate_change"
              fields={[
                "ship_building/risk_adjusted_rate_change_case_priced/uw_selected",
                null,
              ]}
              shownBy="ship_building/rarc_calcs_show"
              horizontal
            />
            <HX.Collection
              title=" "
              fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments",
              ]}
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>
      <HX.Section title="Export to Excel" shownBy="/non_cds/show_hide_toggles/rate_change/show_generate_output_summary_button">
        <HX.Pane flow="right">
          <HX.Button
            title="Generate Output Summary"
            task="generate_rating_summary_xlsx_task"
          />
          <HX.File
            field="cds/exposure/granular/vessels/hull_rating/output_summary_xlsx"
            shownBy="/non_cds/show_hide_toggles/hull/show_generated_output_summary_xlsx"
          />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  );
}
export { vw_rate_change };
