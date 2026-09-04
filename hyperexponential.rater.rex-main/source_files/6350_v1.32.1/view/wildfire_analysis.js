import * as HX from "hx-model-components";
import { render_adjustment_summary_table } from "view/results_tables";

function render_wildfire_rating_table() {
  return (
    <HX.Section title="Wildfire Rating" defaultCollapsed shownBy="non_layer_perils/wildfire/show_section">
      <HX.Selector data={["layers"]} dropdown="layer_label">
        <HX.Section title="Modifier Summary">
          <HX.Table
            data={["perils/wildfire/modifier_summary"]}
            fields={[
              "peril_name", "num_locs", "sum_tiv_total_usd", "occupancy", "construction", "pc_code",
              "catnet_score", "size_discount", "bi_waiting_period", "total_modifier_impact", "gu_tech_rate", "worth", "tech_rate",
              "uw_adj_tech_rate", "uw_adj_tech_prem"
            ]}
            kb-interactive
          />
        </HX.Section>
        <HX.Section title="Risk Factors Summary">
          <HX.Pane flow="right" reflow={true}>
            {render_adjustment_summary_table("perils/wildfire/risk_category_summary", "Risk Category")}
            {render_adjustment_summary_table("perils/wildfire/construction_summary", "Construction Summary")}
          </HX.Pane>
          <HX.Pane flow="right" reflow={true}>
            {render_adjustment_summary_table("perils/wildfire/occupancy_summary", "Occupancy Summary")}
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Pane flow="right">
          <HX.Collection fields={["/policy_information/top_20_sort_by"]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Section title="Top 20 Largest Locations">
          <HX.Table
            data={["perils/wildfire/top_20_locations_summary"]}
            fields={[
              "country", "state", "county", "zip", "tiv_buildings", "tiv_contents_total", "tiv_bi",
              "tiv_total", "itv", "base_rate", "occupancy", "construction", "pc_code", "catnet_score", "size_discount", "bi_waiting_period",
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

export { render_wildfire_rating_table };
