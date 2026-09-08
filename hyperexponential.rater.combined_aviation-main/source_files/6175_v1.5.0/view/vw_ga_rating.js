import * as HX from "hx-model-components";

function vw_ga_rating(pageType) {
  const renderPage = () => {
    switch (pageType) {
      case "total_loss_freq":
        return (
          <HX.Page title="Total & Partial Loss Freq" fullWidth viewScale={0.8} shownBy="cds/exposure/granular/show_ga_pricing">
            <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
              <HX.Section title="Total Loss Frequency Calculation">
                <HX.Pane>
                  <HX.Table
                    title="Aircrafts"
                    data={["ga_rating"]}
                    fields={[
                      "include",
                      "aircraft_class",
                      "base_rate",
                      { field: "no_of_aircraft", width: 125 },
                      "base_freq_all_aircraft",
                      "hull_value_usd",
                      "hull_value_adjuster",
                      "time_in_service",
                      "status_adjuster",
                      "build_location",
                      "build_location_adjuster",
                      "freq_region",
                      "use",
                      "use_adjuster",
                      "region_adjuster",
                      "fleet_size",
                      "fleet_size_adjuster",
                      "exp_total_losses",
                      "exp_partial_losses"
                    ]}
                    dynamic
                    kb-interactive
                    freezeLeft={1}
                  />
                </HX.Pane>
              </HX.Section>
            </HX.With>
          </HX.Page>
        );

      case "hull_rating":
        return (
          <HX.Page title="Hull Rating" fullWidth viewScale={0.8} shownBy="cds/exposure/granular/show_ga_pricing">
            <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
              <HX.Section title="Hull Rating Calculation">
                <HX.Pane>
                  <HX.Table
                    title="Aircrafts"
                    data={["ga_rating"]}
                    fields={[
                      "include",
                      "exp_total_losses",
                      "exp_partial_losses",
                      "hull_value_usd",
                      "hull_per_occ_deductible_usd",
                      "hull_severity",
                      "hull_partial_base_severity",
                      "hull_partial_engine_adjuster",
                      "hull_partial_build_year_adjuster",
                      "hull_total_loss_unadjusted",
                      "hull_partial_loss_unadjusted",
                      "hull_expected_loss_unadjusted",
                      "hull_attritional_adjuster",
                      "bm_term_adj",
                      "hull_expected_loss",
                      "hull_benchmark_cost",
                      "hull_net_rate",
                      "hull_benchmark_rate"
                    ]}
                    dynamic
                    kb-interactive
                    freezeLeft={1}
                  />
                </HX.Pane>
              </HX.Section>
            </HX.With>
          </HX.Page>
        );

      case "pax_rating":
        return (
          <HX.Page title="PAX Rating" fullWidth viewScale={0.8} shownBy="cds/exposure/granular/show_ga_pricing">
            <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
              <HX.Section title="PAX Liability Rating Calculation">
                <HX.Pane>
                  <HX.Table
                    title="Aircrafts"
                    data={["ga_rating"]}
                    fields={[
                      "include",
                      "pax_exp_total_losses",
                      "total_seats_all_aircraft",
                      "total_seats",
                      "seat_occupancy",
                      "fatality",
                      "exp_no_of_deaths",
                      "operator_region",
                      "pax_award_usd",
                      "pax_limit_usd",
                      "apply_pax_limit",
                      "gu_pax_losses",
                      "max_pax_losses",
                      "pax_per_occ_limit_usd",
                      "pax_apply_occ_limit_ded",
                      "pax_apply_occ_limit_ded_to_max_loss",
                      "pax_exp_loss_from_total_losses",
                      "pax_attritional_adjuster",
                      "bm_term_adj",
                      "pax_expected_loss",
                      "pax_benchmark_cost",
                      "pax_benchmark_per_seat"
                    ]}
                    dynamic
                    kb-interactive
                    freezeLeft={1}
                  />
                </HX.Pane>
              </HX.Section>
            </HX.With>
          </HX.Page>
        );

      case "tpl_rating":
        return (
          <HX.Page title="TPL Rating" fullWidth viewScale={0.8} shownBy="cds/exposure/granular/show_ga_pricing">
            <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
              <HX.Section title="TP Liability Rating Calculation">
                <HX.Pane>
                  <HX.Table
                    title="Aircrafts"
                    data={["ga_rating"]}
                    fields={[
                      "include",
                      "no_of_aircraft",
                      "tpl_limit_usd",
                      "tpl_limit_exposed",
                      "tpl_net_rol_exposed",
                      "tpl_net_rol_unexposed",
                      "tpl_expected_loss_unadjusted",
                      "fleet_size",
                      "fleet_size_adjuster",
                      "bm_term_adj",
                      "tpl_expected_loss",
                      "tpl_benchmark_cost",
                      "tpl_net_rate",
                      "tpl_gross_rate"
                    ]}
                    dynamic
                    kb-interactive
                    freezeLeft={1}
                  />
                </HX.Pane>
              </HX.Section>
            </HX.With>
          </HX.Page>
        );
    }
  };

  return renderPage();
}

export { vw_ga_rating };
