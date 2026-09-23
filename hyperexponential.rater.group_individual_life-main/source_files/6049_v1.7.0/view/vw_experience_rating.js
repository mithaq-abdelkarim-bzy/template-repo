import * as HX from "hx-model-components";

function vw_experience_rating() {
  return (
    <HX.Page title="Experience Rating" fullWidth shownBy="cds/experience_rating/claims_available">
      <HX.With context={{ type: "struct", path: "cds/experience_rating" }}>
        <HX.Section title="Selections">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={["cut_off_date", "death_or_all_risks"]} horizontal />
              <HX.Collection fields={["date_check"]} shownBy="date_check_show" />
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Claims">
          <HX.Table
            data={["claims", null, "claims_totals"]}
            fields={[
              "year",
              "no_lives",
              "sum_insured",
              "incurred",
              "number",
              "ibnr_factor",
              "time_adj",
              "burn",
              "burn_per_mille"
            ]}
            kb-interactive
          />
        </HX.Section>
        <HX.Section title="Summary">
          <HX.Pane flow="right">
            <HX.Collection title="Credibility Metrics" fields={["life_years", "cred_weight"]} />
            <HX.Collection title="Z Values" fields={["z_factor", "one_minus_z"]} />
            <HX.Collection title="Burn Metrics" fields={["claims_totals/burn", "burn_cost",]} />
            <HX.Collection title="Discounts" fields={["death_only_discount", "all_risk_discount"]} />
          </HX.Pane>
          {/* <HX.Collection title="debug" fields={["/debug_str"]} /> */}
        </HX.Section>
      </HX.With>
    </HX.Page >
  )
}


export { vw_experience_rating };