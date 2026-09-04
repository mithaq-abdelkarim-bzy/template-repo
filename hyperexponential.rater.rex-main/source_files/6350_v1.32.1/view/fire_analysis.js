import * as HX from "hx-model-components";
import { render_adjustment_summary_table } from "view/results_tables";

function render_fire_rating_table() {
  return (
    <HX.Section title="Fire Rating" defaultCollapsed shownBy="non_layer_perils/fire/show_section">
      <HX.Selector data={["layers"]} dropdown="layer_label">
        <HX.Section title="Modifier Summary">
          <HX.Table
            data={["perils/fire/modifier_summary"]}
            fields={[
              "peril_name", "no_of_locs", "sum_tiv_total_usd", "occupancy", "construction",
              "pc_code", "sprinkler", "bi_waiting_period", "bi_indemnity_period", "cbi", "fire_size_discount",
              "total_modifier_impact", "gu_tech_rate", "worth", "tech_rate",
              "uw_adj_tech_rate", "uw_adj_tech_prem"
            ]}
            kb-interactive
          />
        </HX.Section>
        <HX.Section title="Risk Factors Summary">
          <HX.Pane flow="right" reflow={true}>
            {render_adjustment_summary_table("perils/fire/occupancy_summary", "Occupancy Summary")}
            {render_adjustment_summary_table("perils/fire/construction_summary", "Construction Summary")}
          </HX.Pane>
          <HX.Pane flow="right" reflow={true}>
            {render_adjustment_summary_table("perils/fire/sprinkler_summary", "Sprinkler Summary")}
            <HX.Table
              title="Machinery Breakdown Summary"
              data={["perils/fire/machinery_breakdown_summary"]}
              fields={[
                { field: "name", width: 200 },
                { field: "num_locations", width: 100 },
                { field: "tiv", width: 150 },
                { field: "fire_mb_proportion", width: 150 },
                { field: "gu_tech_rate", width: 150 },
                { field: "worth", width: 100 },
                { field: "tech_rate", width: 120 },
                { field: "uw_adj_tech_rate", width: 150 },
                { field: "uw_adj_tech_prem", width: 150 },
              ]}
              kb-interactive
            />
          </HX.Pane>
        </HX.Section>
        <HX.Pane flow="right">
          <HX.Collection fields={["/policy_information/top_20_sort_by"]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Section title="Top 20 Largest Locations">
          <HX.Table
            data={["perils/fire/top_20_locations_summary"]}
            fields={[
              "country", "state", "county", "zip", "tiv_buildings", "tiv_contents_total", "tiv_bi",
              "tiv_total", "itv", "base_rate", "occupancy", "construction", "pc_code", "sprinkler", "bi_waiting_period", "bi_indemnity_period", "cbi", "fire_size_discount",
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

export { render_fire_rating_table };
