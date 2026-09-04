import * as HX from "hx-model-components";

function vw_rate_change() {
  return (
    <HX.Page title="Rate Change" fullWidth={false} shownBy="model_state/show_rate_change" >

      <HX.Section title="Fetch Expiring Policy">
        <HX.Pane flow="right" >
          <HX.Collection fields={["cds/rate_change/expiring_policy_option_id", null]} horizontal />
        </HX.Pane>
        <HX.Pane flow="right" >
          <HX.Button title="Calculate Rate Change" task="rarc_task" shownBy="cds/standard_fields/is_rater_priced" />
          <HX.Button title="Import Expiring Premium" task="case_priced_expiry_import" shownBy="cds/standard_fields/is_case_priced" />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes with="cds/rate_change" field="rarc_run_again_message" shownBy="rarc_message_show" />
        </HX.Pane>
      </HX.Section>

      <HX.Section title={"Rate Change"} >
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane>
            <HX.Table
              data={["premium_annualized_100pct", "premium_annualized_beazley_share"]}
              fields={[{ field: "renewal", width: 200 }, { field: "expiring", width: 200 }]}
              with="rate_change"
            />
          </HX.Pane>
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
              fields={[{ field: "model_calculated", width: 135 }, { field: "uw_selected", width: 135 }, { field: "comments", width: 250 }]}
              with="rate_change"
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection
              title="Final Rate Change (Gross Brokerage)"
              fields={["rate_change/risk_adjusted_rate_change/uw_selected"]}
              shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Collection
              title="Final Rate Change (Gross Brokerage)"
              fields={["rate_change/risk_adjusted_rate_change_case_priced/uw_selected"]}
              shownBy="/cds/standard_fields/is_case_priced" />
            <HX.Collection
              title=" "
              fields={["rate_change/risk_adjusted_rate_change_case_priced/comments"]}
              shownBy="/cds/standard_fields/is_case_priced" />
            < HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Pane />
          </HX.Pane>
        </HX.With>
      </HX.Section >
    </HX.Page >
  )
}
export { vw_rate_change };