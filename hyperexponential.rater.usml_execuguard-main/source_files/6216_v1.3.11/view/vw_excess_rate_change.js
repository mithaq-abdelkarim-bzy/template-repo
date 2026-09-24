import * as HX from "hx-model-components";

function vw_excess_rate_change(scale) {
  return (
    <HX.Page title="Rate Change" shownBy="cds/excess_rate_change/show_hide_excess_rc" viewScale={scale} fullWidth={true}>
      <HX.With context={{ type: "struct", path: "cds/excess_rate_change" }}>
        <HX.Section title="Rate Change Individual Componets">
          <HX.Pane flow="right">
            <HX.Table
              title="Deductible, Limit, and Brokergae"
              data={["deductible", "limit", "brokerage"]}
              fields={[
                { field: "expiry", width: 150 },
                { field: "renewal", width: 150 },
                { field: "rate_change", width: 150 }
              ]}
              kb-interactive
              syncColumnWidthsKey="mySyncedTables1"
            />
            <HX.Table
              title="Exposure Components"
              data={["exposure/fte", "exposure/plan_assets", "exposure/plan_participants", "exposure/total_assets", null, "exposure/total_rate_change"]}
              fields={[
                { field: "expiry", width: 150 },
                { field: "renewal", width: 150 },
                { field: "rate_change", width: 150 },
                null,
                { field: "weights", width: 150 }
              ]}
            />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Rate Change">
          <HX.Pane flow="right">
            <HX.Table
              title="Rate Change Build-up"
              data={["annualized_expiring_prem", null, "exposure/total_rate_change", "risk_char", "deductible", "limit", "terms_and_conditions", "brokerage", null, "expected_new_prem", "new_prem", null, "final_rc"]}
              fields={[{ field: "rate_change", width: 150 }]}
            />
            <HX.Notes field="comments" title="Comments" />
          </HX.Pane>
        </HX.Section>
      </HX.With>

    </HX.Page>
  )
}
export { vw_excess_rate_change };