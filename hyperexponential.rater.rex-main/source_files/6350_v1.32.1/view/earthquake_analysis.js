import * as HX from "hx-model-components";
import { render_adjustment_summary_table } from "view/results_tables";

function render_earthquake_rating_table() {
  return (
    <HX.Section title="Earthquake Rating" defaultCollapsed shownBy="non_layer_perils/quake/show_section">

      <HX.Selector data={["layers"]} dropdown="layer_label">
        <HX.Section title="Earthquake Simulation Summary">
          <HX.Table
            data={["risk_appetite_summary"]}
            fields={[
              "us_quake_aal", "us_quake_sd", "aep_impact_1_in_10", "oep_impact_1_in_250", "intl_quake_aal", "intl_quake_sd"
            ]}
            kb-interactive
          />
          <HX.Table
            title="Intl. AAL Summary"
            data={[{ datum: "risk_appetite_summary_intl_country", elementLabelBy: 'country' }]}
            fields={[{ field: "aal_eq", width: 200 }]}
            filter={["show_eq"]}
            kb-interactive
          />
        </HX.Section>

        <HX.Section title="Modifier Summary">
          <HX.Table
            data={["perils/quake/modifier_summary"]}
            fields={[
              "peril_name", "no_of_locs", "sum_tiv_total_usd", "occupancy", "construction",
              "year_built", "num_of_floors", "construction_quality", "plan_irregularity",
              "soft_story", "vertical_irregularity", "ornamentation", "equipment_bracing",
              "equipment_maintenance", "pounding", "catnet_score",
              "total_modifier_impact", "gu_tech_rate", "worth", "tech_rate",
              "uw_adj_tech_rate", "uw_adj_tech_prem"
            ]}
            kb-interactive
          />
        </HX.Section>
        <HX.Section title="Risk Factors Summary">
          <HX.Pane flow="right" reflow={true}>
            {render_adjustment_summary_table("perils/quake/cresta_summary", "CRESTA Zone")}
            {render_adjustment_summary_table("perils/quake/risk_category_summary", "Earthquake Risk Category")}
          </HX.Pane>
          <HX.Pane flow="right" reflow={true}>
            {render_adjustment_summary_table("perils/quake/occupancy_summary", "Occupancy Summary")}
            {render_adjustment_summary_table("perils/quake/construction_summary", "Construction Summary")}
          </HX.Pane>
        </HX.Section>
        <HX.Pane flow="right">
          <HX.Collection fields={["/policy_information/top_20_sort_by"]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Section title="Top 20 Largest Locations">
          <HX.Table
            data={["perils/quake/top_20_locations_summary"]}
            fields={[
              "country", "state", "county", "zip", "tiv_buildings", "tiv_contents_total", "tiv_bi",
              "tiv_total", "itv", "base_rate", "catnet_score", "occupancy", "construction", "year_built", "num_of_floors",
              "construction_quality", "plan_irregularity", "soft_story", "vertical_irregularity", "ornamentation",
              "equipment_bracing", "equipment_maintenance", "pounding",
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

export { render_earthquake_rating_table };
