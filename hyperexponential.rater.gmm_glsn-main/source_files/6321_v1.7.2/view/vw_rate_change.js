import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];
  // start at n=2 as this equals the first excess layer, 0 is retention, 1 is primary (primary defined separately below)
  //  
  for (let n = 2; n < num_layers + 2; n++) {
    objects.push(
      <HX.Section title={"Renewal Excess Layer " + (n - 1)} defaultCollapsed shownBy={"cds/add_excess_" + (n - 1)} >
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane flow="right">
            <HX.Collection fields={["rate_change/expiring_layer_dropdown"]} />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Notes field="rate_change/renewal_premium_warning" shownBy="rate_change/renewal_premium_warning_show" />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
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
                // null,
                // "rate_change"
              ]}
              fields={[{ field: "model_calculated", width: 150 }, { field: "uw_selected", width: 150 }, { field: "comments", width: 150 }]}
              with="rate_change"
              syncColumnWidthsKey="mySyncedTables1"
              kb-interactive
            />
          </HX.Pane>
        </HX.With>

        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane>
            <HX.Table
              data={["premium_annualized_100pct"]}
              fields={[{ field: "expiring", width: 220 }, { field: "implied", width: 220 }, { field: "renewal", width: 220 }]}
              with="rate_change"
              syncColumnWidthsKey="mySyncedTables1"
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
    // <HX.Page title="Rate Change" fullWidth={true} shownBy="cds/standard_fields/is_renewal"  >
    <HX.Page title="Rate Change" fullWidth={true} shownBy="cds/is_real_renewal"  >
      <HX.Section title="Fetch Expiring Policy">
        <HX.Pane flow="right" >
          <HX.Collection fields={["cds/rate_change/expiring_policy_option_id", null]} horizontal />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            title=""
            data={[{ datum: "cds/layers", width: 200, elementLabelBy: "layer_label" }]}
            fields={[{ field: "status.read_only" }]}
            transpose
            filter={"show_row"}
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane flow="right" >
          <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" />
          <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
          <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
          <HX.Button title="Calculate Rate Change" task="rarc_task" shownBy="cds/standard_fields/is_rater_priced" />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes with="cds/rate_change" field="rarc_run_again_message" shownBy="rarc_message_show" />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Rate Change Instructions and Key" defaultCollapsed>
        <HX.Pane flow="right">
          <HX.Notes field="cds/rate_change/instructions" />
          {/* <HX.Pane></HX.Pane> */}
        </HX.Pane>
      </HX.Section >

      <HX.Section title={"Primary Layer"} >
        <HX.With context={{ type: "list", path: "cds/layers", index: 1 }}>
          <HX.Pane flow="right">
            <HX.Collection fields={["rate_change/expiring_layer_dropdown"]} />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Notes field="rate_change/renewal_premium_warning" shownBy="rate_change/renewal_premium_warning_show" />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
        </HX.With>


        <HX.With context={{ type: "list", path: "cds/layers", index: 1 }}>
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
                // null,
                // "rate_change"
              ]}
              fields={[{ field: "model_calculated", width: 150 }, { field: "uw_selected", width: 150 }, { field: "comments", width: 150 }]}
              with="rate_change"
              kb-interactive
              syncColumnWidthsKey="mySyncedTables1"
            />
          </HX.Pane>
        </HX.With>

        <HX.With context={{ type: "list", path: "cds/layers", index: 1 }}>
          <HX.Pane>
            <HX.Table
              data={["premium_annualized_100pct"]}
              fields={[{ field: "expiring", width: 220 }, { field: "implied", width: 220 }, { field: "renewal", width: 220 }]}
              with="rate_change"
              kb-interactive
              syncColumnWidthsKey="mySyncedTables1"
            />
          </HX.Pane>
        </HX.With>

        <HX.With context={{ type: "list", path: "cds/layers", index: 1 }}>
          <HX.Pane flow="right">
            <HX.Collection title="Final Rate Change (Gross Brokerage)" fields={["rate_change/risk_adjusted_rate_change/uw_selected"]} shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Collection title="Final Rate Change (Gross Brokerage)" fields={["rate_change/risk_adjusted_rate_change_case_priced/uw_selected"]} shownBy="/cds/standard_fields/is_case_priced" />
            <HX.Collection title=" " fields={["rate_change/risk_adjusted_rate_change_case_priced/comments"]} shownBy="/cds/standard_fields/is_case_priced" />
            < HX.Pane shownBy="/cds/standard_fields/is_rater_priced"></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
        </HX.With>

      </HX.Section >

      {vw_loop_rate_change_layer(max_layers())}

    </HX.Page >
  )
}
export { vw_rate_change };