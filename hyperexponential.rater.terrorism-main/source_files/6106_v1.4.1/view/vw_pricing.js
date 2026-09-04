import * as HX from "hx-model-components";


function vw_pricing(pageType) {
  const renderPage = () => {
    switch (pageType) {
      case "roeCalcs":
        return (
          <HX.Page title="ROE Calcs" fullWidth viewScale={0.8} shownBy="cds/exposure/granular/show_pricing">
            <HX.Section title="ROE Calculations">
              <HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection title="BI and Countries" with="cds/exposure/granular" fields={["bi_multiplier", "no_of_countries"]} />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Collection title="Weighted Avg Min ROL" with="cds/exposure/granular" fields={["wa_nl_min_rol", "wa_liab_min_rol"]} />
                </HX.Pane>
                <HX.Table
                  with="cds/exposure/granular"
                  data={["roe"]}
                  fields={[
                    "country",
                    "attritional_risk",
                    "geog_risk",
                    "location_cat_risk",
                    "total_sum_insured",
                    "bi_sum_insured",
                    "pd_sum_insured",
                    "civil_unrest",
                    "war",
                    "terrorism",
                    "coverage",
                    "coverage_code",
                    "subcoverage",
                    "subcoverage_code",
                    "selected_sum_insured",
                    "risk_multiplier",
                    "bi_terrorism_c",
                    "bi_terrorism_b",
                    "bi_civil_unrest_c",
                    "bi_civil_unrest_b",
                    "bi_war_c",
                    "bi_war_b",
                    "bi_terrorism_roe",
                    "bi_civil_unrest_roe",
                    "bi_war_roe",
                    "pd_terrorism_c",
                    "pd_terrorism_b",
                    "pd_civil_unrest_c",
                    "pd_civil_unrest_b",
                    "pd_war_c",
                    "pd_war_b",
                    "pd_terrorism_roe",
                    "pd_civil_unrest_roe",
                    "pd_war_roe",
                    "selected_terrorism_roe",
                    "selected_civil_unrest_roe",
                    "selected_war_roe",
                    "cvg_terrorism",
                    "cvg_civil_unrest",
                    "cvg_war",
                    "cvg_loading",
                    "subcvg_terrorism",
                    "subcvg_civil_unrest",
                    "subcvg_war",
                    "subcvg_loading",
                    "ihs_average_default",
                    "bi_cvg_nl_roe",
                    "pd_cvg_nl_roe",
                    "total_cvg_nl_roe",
                    "bi_subcvg_nl_roe",
                    "pd_subcvg_nl_roe",
                    "total_subcvg_nl_roe",
                    "cvg_multiplier",
                    "subcvg_multiplier",
                    "nl_min_rol",
                    "liab_min_rol"
                  ]}
                  dynamic
                  kb-interactive
                />
              </HX.Pane>
            </HX.Section >
          </HX.Page >
        );

      case "expandedCalcs":
        return (
          <HX.Page title="Expanded Calcs" fullWidth viewScale={0.8} shownBy="cds/exposure/granular/show_pricing">
            <HX.Section title="Expanded Calculations">
              <HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection title="Countries and FX" with="cds/exposure/granular" fields={["no_of_countries", "fx_to_usd"]} />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Collection title="Summary" with="cds/exposure/granular" fields={["trapped_exposure", "limit_ded_difference", "expo_limit_ratio"]} />
                </HX.Pane>
                <HX.Table
                  with="cds/exposure/granular"
                  data={["curves"]}
                  fields={[
                    "location_number",
                    "country",
                    "country_number",
                    "no_of_locations",
                    "pml",
                    "coverage",
                    "limit",
                    "excess",
                    "subcoverage",
                    "sublimit",
                    "deductible",
                    "total_sum_insured",
                    "bi_sum_insured",
                    "pd_sum_insured",
                    "selected_sum_insured",
                    "band",
                    "kth_smallest",
                    "decile",
                    "category",
                    "no_in_category",
                    "si_unscaled",
                    "si_scaled",
                    "si_scaled_2",
                    "liability_risk",
                    "attritional_risk",
                    "geog_risk",
                    "location_cat_risk",
                    "bi_cvg_nl_roe",
                    "bi_subcvg_nl_roe",
                    "pd_cvg_nl_roe",
                    "pd_subcvg_nl_roe",
                    "cvg_bi_rate_si",
                    "cvg_pd_rate_si",
                    "cvg_bi_mbbefd",
                    "cvg_pd_mbbefd",
                    "cvg_bi_base_premium",
                    "cvg_pd_base_premium",
                    "cvg_limit_usd",
                    "cvg_excess_usd",
                    "cvg_ilf_upper",
                    "cvg_ilf_lower",
                    "cvg_liab_base_premium",
                    "subcvg_bi_rate_si",
                    "subcvg_pd_rate_si",
                    "subcvg_bi_mbbefd",
                    "subcvg_pd_mbbefd",
                    "subcvg_bi_base_premium",
                    "subcvg_pd_base_premium",
                    "subcvg_sublimit_usd",
                    "subcvg_ilf_upper",
                    "subcvg_liab_base_premium",
                    "trapped_exposure"
                  ]}
                  maxListVisibleRows={25}
                  dynamic
                  kb-interactive
                  freezeLeft={2}
                />
              </HX.Pane>
            </HX.Section>
          </HX.Page>
        );
    }
  };

  return renderPage();
}

export { vw_pricing };
