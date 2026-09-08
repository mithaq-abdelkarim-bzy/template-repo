import * as HX from "hx-model-components";

function vw_experience_rating() {
  return (
    <HX.Page title="Experience Rating" fullWidth viewScale={0.9} shownBy="cds/experience_rating/show_experience_rating">
      {/* <HX.Page title="Experience Rating" fullWidth viewScale={0.9}> */}
      <HX.With context={{ type: "struct", path: "cds/experience_rating" }}>

        <HX.Section title="Loss History">
          {/* <HX.Notes field="/debug_str" /> */}
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={["historic_premium_known", "no_of_years_history"]} horizontal syncColumnWidthsKey="date" />
              <HX.Collection fields={["as_at_date", { field: "as_at_date_message", shownBy: "show_date_message" }]} horizontal syncColumnWidthsKey="date" />
              <HX.Pane flow="right">
                <HX.Collection fields={["show_rc_calcs"]} syncColumnWidthsKey="date" />
                <HX.Button title="Autopopulate Premium" task="fill_historic_premium_task" />
              </HX.Pane>
            </HX.Pane>
            {/* <HX.Pane /> */}
            <HX.Notes field="expiring_claims_msg" stretch />
          </HX.Pane>
          <HX.Table
            data={["claims"]}
            fields={[
              "yoa",
              null,
              { field: "hull_portfolio_rc", shownBy: "show_rc_calcs" },
              { field: "liab_portfolio_rc", shownBy: "show_rc_calcs" },
              { field: "hull_rc_to_use", shownBy: "show_rc_calcs" },
              { field: "liab_rc_to_use", shownBy: "show_rc_calcs" },
              { field: "hull_cumul_rc", shownBy: "show_rc_calcs" },
              { field: "liab_cumul_rc", shownBy: "show_rc_calcs" },
              { field: "years_to_inception", shownBy: "show_rc_calcs" },
              { field: "hull_inflation", shownBy: "show_rc_calcs" },
              { field: "liab_inflation", shownBy: "show_rc_calcs" },
              { field: null, shownBy: "show_rc_calcs" },
              "hull_attr_claims",
              "hull_large_losses",
              "hull_gross_premium",
              "hull_exposure_adj",
              "hull_rate_change",
              "hull_as_if_premium",
              "hull_pct_developed",
              "hull_ult_attr_claims",
              "hull_ulr",
              "liab_attr_claims",
              "liab_large_losses",
              "liab_gross_premium",
              "liab_exposure_adj",
              "liab_rate_change",
              "liab_as_if_premium",
              "liab_pct_developed",
              "liab_ult_attr_claims",
              "liab_ulr"
            ]}
            kb-interactive
            freezeLeft={1}
          />
        </HX.Section>

        <HX.Section title="Results">
          <HX.Pane flow="right">
            <HX.Table
              title="Large Loss Loading"
              data={["hull", "liability"]}
              fields={[
                "max_insured_loss",
                "implied_lllr",
                "implied_rp",
                null,
                "large_loss_loading"
              ]}
              kb-interactive
              transpose
              syncColumnWidthsKey="experience"
            />
            <HX.Table
              title="Summary"
              data={["hull", "liability"]}
              fields={[
                "actual_no_of_years",
                null,
                "quoted_premium",
                "implied_attr_lr",
                { field: "large_loss_loading", labelBy: "hull/ll_loading_label" },
                null,
                "expected_lr",
                { field: "expected_claims", labelBy: "hull/expected_claims_label" },
                "credibility"
              ]}
              kb-interactive
              transpose
              syncColumnWidthsKey="experience"
            />
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}


export { vw_experience_rating };