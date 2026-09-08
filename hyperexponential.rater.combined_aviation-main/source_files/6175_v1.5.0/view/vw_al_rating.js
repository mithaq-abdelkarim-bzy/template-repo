import * as HX from "hx-model-components";


function vw_al_rating() {

  return (
    <HX.Page title="Airlines Rating" fullWidth viewScale={0.8} shownBy="cds/exposure/granular/show_al_pricing">
      <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>

        <HX.Section title="Hull, PAX & TPL Liability Modelling">
          {/* <HX.Notes field="/debug_str" /> */}
          <HX.Pane>
            <HX.Table
              title="Summary"
              data={["airlines_rating_summary"]}
              fields={[
                "fleet_size",
                "hull_loss_cost",
                "total_seats",
                "pax_loss_cost",
                "tpl_loss_cost",
                "hull_large_severity",
                "liab_large_severity"
              ]}
            />
            <HX.Table
              title="Aircrafts"
              data={["airlines_rating"]}
              fields={[
                "include",
                { field: "no_of_aircraft", width: 125 },
                "registration",
                "value_usd",
                "coverage",
                "attachment_date",
                "expiry_date",
                "usage",
                "market_class",
                "build_year",
                "aircraft_status",
                "previous12_months_hours",
                "operator_region",
                "russian_built",
                "total_seats",
                "operating_mtow_lb",
                null,
                "hull_f_base",
                "hull_f_status",
                "hull_f_operator_region",
                "hull_f_previous12_months_hours",
                "hull_f_market_class",
                "hull_f_build_year_group",
                "hull_f_build_year",
                "hull_f_usage",
                "hull_frequency",
                null,
                "hull_s_base",
                "hull_s_previous12_months_hours",
                "hull_s_market_class",
                "hull_s_russian_built",
                "hull_s_mtow",
                "hull_s_build_year_group",
                "hull_s_build_year",
                "hull_severity",
                null,
                "hull_low_value_load",
                "hull_fleet_adj",
                "hull_attr_uplift",
                "hull_loss_cost_gu_usd",
                "hull_limit_point",
                "hull_excess_point",
                "hull_limit_usd",
                "hull_excess_usd",
                "hull_loss_cost_usd",
                null,
                "pax_seats_in_service",
                "pax_base_freq_year_built",
                "pax_status",
                "pax_operator_region",
                "pax_12_months_hours",
                "pax_market_class",
                "pax_severity_per_seat_usd",
                "pax_attr_uplift",
                "pax_liability_per_seat",
                "pax_fleet_adj",
                "pax_loss_cost_gu_usd",
                "pax_limit_point",
                "pax_attachment_point",
                "liability_limit_usd",
                "liability_excess_usd",
                "pax_loss_cost_usd",
                null,
                "tpl_liab_limit_exposed",
                "tpl_usage",
                "tpl_rate_on_limit",
                "tpl_base_loss_cost_usd",
                "tpl_fleet_adj",
                "tpl_loss_cost_usd",
                null,
                "bm_term_adj",
                "bm_hull_large_loss_cost",
                "bm_hull_large_severity",
                "bm_liab_large_frequency",
                "bm_liab_large_loss_cost",
                "bm_liab_large_severity",
                "bm_hull_benchmark",
                "bm_hull_benchmark_rate",
                "bm_pax_liab_benchmark_cost",
                "bm_pax_liability_per_seat",
                "bm_tpl_benchmark",
                "bm_allocated_hull_premium",
                "bm_aircraft_in_expiry_fleet",
                "bm_total_liab_premium",
                "bm_allocated_liab_premium"
              ]}
              dynamic
              kb-interactive
              freezeLeft={1}
            />
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_al_rating };
