import * as HX from "hx-model-components";
import { render_adjustment_summary_table } from "view/results_tables";

function render_hurricane_rating_table() {
  return (
    <HX.Section title="Windstorm Rating" defaultCollapsed shownBy="non_layer_perils/named_windstorm/show_section">
      <HX.Selector data={["layers"]} dropdown="layer_label">
        <HX.Section title="Windstorm Simulation Summary">
          <HX.Table
            data={["risk_appetite_summary"]}
            fields={[
              "us_wind_aal", "us_wind_sd", "aep_impact_1_in_10", "oep_impact_1_in_250", "intl_wind_aal", "intl_wind_sd"
            ]}
            kb-interactive
          />
          <HX.Table
            title="Intl. AAL Summary"
            data={[{ datum: "risk_appetite_summary_intl_country", elementLabelBy: 'country' }]}
            fields={[{ field: "aal_ws", width: 200 }]}
            filter={["show_ws"]}
            kb-interactive
          />
        </HX.Section>

        <HX.Section title="Modifier Summary">
          <HX.Table
            data={["perils/named_windstorm/modifier_summary"]}
            fields={[
              "peril_name", "no_of_locs", "sum_tiv_total_usd", "occupancy", "construction",
              "year_built", "floor_area", "num_of_floors", "roof_age", "roof_covering",
              "roof_geometry", "construction_quality", "roof_anchor", "roof_bracing", "roof_cladding",
              "frame_connection", "storm_surge", "catnet_score",
              "total_modifier_impact", "gu_tech_rate", "worth", "tech_rate",
              "uw_adj_tech_rate", "uw_adj_tech_prem"
            ]}
            kb-interactive
          />
        </HX.Section>
        <HX.Section title="Risk Factors Summary">
          <HX.Pane flow="right" reflow={true}>
            {render_adjustment_summary_table("perils/named_windstorm/gate_summary", "Windstorm Gate")}
            {render_adjustment_summary_table("perils/named_windstorm/risk_category_summary", "Windstorm Risk Category")}
          </HX.Pane>
          <HX.Pane flow="right" reflow={true}>
            {render_adjustment_summary_table("perils/named_windstorm/occupancy_summary", "Occupancy Summary")}
            {render_adjustment_summary_table("perils/named_windstorm/construction_summary", "Construction Summary")}
          </HX.Pane>
        </HX.Section>
        <HX.Pane flow="right">
          <HX.Collection fields={["/policy_information/top_20_sort_by"]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Section title="Top 20 Largest Locations">
          <HX.Table
            data={["perils/named_windstorm/top_20_locations_summary"]}
            fields={[
              "country", "state", "county", "zip", "tiv_buildings", "tiv_contents_total", "tiv_bi",
              "tiv_total", "itv", "base_rate", "catnet_score", "occupancy", "construction", "year_built", "floor_area", "num_of_floors",
              "roof_age", "roof_covering", "roof_geometry", "construction_quality", "roof_anchor", "roof_bracing",
              "roof_cladding", "frame_connection", "storm_surge",
              "total_modifier_impact", "gu_tech_rate", "worth", "tech_rate", "uw_adj_tech_rate", "uw_adj_tech_prem"
            ]}
            kb-interactive
            minListVisibleRows={30}
          />
        </HX.Section>
      </HX.Selector>
    </HX.Section>
  )
}

export { render_hurricane_rating_table };
