import * as HX from "hx-model-components";
import { render_notifications } from "view/results_tables";
import ChoroplethMap from "components/choropleth";
import CombinationChart from "components/exposure_segmentation";

function account_segmentation() {
  return (
    <HX.Page title="Account Segmentation" fullWidth={true} shownBy="model_state/show_after_landing_page">
      {render_notifications()}
      <HX.Section title="Visualisation ">
        <HX.Pane flow="right">
          <HX.Pane>
            <ChoroplethMap title="Countries"
              node_path="pricing_layer_segmentation/state_country_choropleth_data"
              zs={["tiv", "num_locations", "gu_loss", "gu_tech_rate"]}
              options={["TIV", "Num of locations", "GU Loss", "GU Tech Rate"]}
              percentFormat={[false, false, false, true]}
              withMarkers={false}
            />
          </HX.Pane>
          <HX.Pane>
            <ChoroplethMap title="States"
              node_path="pricing_layer_segmentation/state_country_choropleth_data"
              zs={["tiv", "num_locations", "gu_loss", "gu_tech_rate"]}
              options={["TIV", "Num of locations", "GU Loss", "GU Tech Rate"]}
              percentFormat={[false, false, false, true]}
              withMarkers={true}
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Account Segmentation by Layer">
        <HX.Selector data={["layers"]} dropdown="layer_label">
          <HX.Section title="Exposure Segmentation">
            <HX.Pane flow="right">
              <HX.Pane ratio={1}>
                <HX.Collection fields={["segmentation_tables/table_selector"]} />
              </HX.Pane>
              <HX.Pane ratio={4}>
                <CombinationChart
                  title="TIV and Location Segmentation"
                  data={[{ list: "other_segmentations/state_summary", labelBy: "name" }]}
                  traces={[
                    { field: "tiv", label: "TIV", color: "#dc1998" },
                  ]}
                  series={[
                    {
                      seriesLabel: "No of Locs",
                      seriesColor: "#4b0050",
                      points: [
                        {
                          list: "other_segmentations/state_summary",
                          x: "name",
                          y: "num_locations",
                        },
                      ],
                    },
                  ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="State"
                  yAxisLabel="TIV"
                  yAxis2Label="No of Locs"
                  shownBy="segmentation_tables/show_segmentation_tables/state"
                />
                <CombinationChart
                  title="TIV and Location Segmentation"
                  data={[{ list: "perils/fire/occupancy_summary", labelBy: "name" }]}
                  traces={[
                    { field: "tiv", label: "TIV", color: "#dc1998" },
                  ]}
                  series={[
                    {
                      seriesLabel: "No of Locs",
                      seriesColor: "#4b0050",
                      points: [
                        {
                          list: "perils/fire/occupancy_summary",
                          x: "name",
                          y: "num_locations",
                        },
                      ],
                    },
                  ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Occupancy"
                  yAxisLabel="TIV"
                  yAxis2Label="No of Locs"
                  shownBy="segmentation_tables/show_segmentation_tables/fire_occupancy"
                />
                <CombinationChart
                  title="TIV and Location Segmentation"
                  data={[{ list: "perils/fire/construction_summary", labelBy: "name" }]}
                  traces={[
                    { field: "tiv", label: "TIV", color: "#dc1998" },
                  ]}
                  series={[
                    {
                      seriesLabel: "No of Locs",
                      seriesColor: "#4b0050",
                      points: [
                        {
                          list: "perils/fire/construction_summary",
                          x: "name",
                          y: "num_locations",
                        },
                      ],
                    },
                  ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Construction"
                  yAxisLabel="TIV"
                  yAxis2Label="No of Locs"
                  shownBy="segmentation_tables/show_segmentation_tables/fire_construction"
                />
                <CombinationChart
                  title="TIV and Location Segmentation"
                  data={[{ list: "perils/named_windstorm/ws_zone_summary", labelBy: "name" }]}
                  traces={[
                    { field: "tiv", label: "TIV", color: "#dc1998" },
                  ]}
                  series={[
                    {
                      seriesLabel: "No of Locs",
                      seriesColor: "#4b0050",
                      points: [
                        {
                          list: "perils/named_windstorm/ws_zone_summary",
                          x: "name",
                          y: "num_locations",
                        },
                      ],
                    },
                  ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="WS Zone"
                  yAxisLabel="TIV"
                  yAxis2Label="No of Locs"
                  shownBy="segmentation_tables/show_segmentation_tables/ws_zone"
                />
                <CombinationChart
                  title="TIV and Location Segmentation"
                  data={[{ list: "perils/named_windstorm/distance_from_coast_summary", labelBy: "name" }]}
                  traces={[
                    { field: "tiv", label: "TIV", color: "#dc1998" },
                  ]}
                  series={[
                    {
                      seriesLabel: "No of Locs",
                      seriesColor: "#4b0050",
                      points: [
                        {
                          list: "perils/named_windstorm/distance_from_coast_summary",
                          x: "name",
                          y: "num_locations",
                        },
                      ],
                    },
                  ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="DTC"
                  yAxisLabel="TIV"
                  yAxis2Label="No of Locs"
                  shownBy="segmentation_tables/show_segmentation_tables/dtc"
                />
                <CombinationChart
                  title="TIV and Location Segmentation"
                  data={[{ list: "perils/quake/eq_zone_summary", labelBy: "name" }]}
                  traces={[
                    { field: "tiv", label: "TIV", color: "#dc1998" },
                  ]}
                  series={[
                    {
                      seriesLabel: "No of Locs",
                      seriesColor: "#4b0050",
                      points: [
                        {
                          list: "perils/quake/eq_zone_summary",
                          x: "name",
                          y: "num_locations",
                        },
                      ],
                    },
                  ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Quake Zone"
                  yAxisLabel="TIV"
                  yAxis2Label="No of Locs"
                  shownBy="segmentation_tables/show_segmentation_tables/eq_zone"
                />
              </HX.Pane>
            </HX.Pane>
            <HX.Button task="produce_heatmap_task" title="Generate Exposure Map" />
            <HX.Section title="Exposure Map" shownBy="/pricing_layer_segmentation/show_file_component">
              <HX.File field="/pricing_layer_segmentation/heatmap_file" />
            </HX.Section>
          </HX.Section>
          <HX.Section title="Exposure Segmentation (detailed)">
            <HX.Pane flow="right">
              <HX.Pane>
                {render_adjustment_summary_table("perils/fire/occupancy_summary", "Occupancy Summary", false)}
                {render_adjustment_summary_table("perils/fire/sprinkler_summary", "Sprinkler Summary", false)}
                {render_adjustment_summary_table("perils/fire/construction_summary", "Construction Summary", false)}
                {render_adjustment_summary_table("perils/quake/eq_zone_summary", "EQ Zone", false)}
              </HX.Pane>
              <HX.Pane>
                {render_adjustment_summary_table("perils/named_windstorm/ws_zone_summary", "WS Zone", false)}
                {render_adjustment_summary_table("perils/named_windstorm/distance_from_coast_summary", "DTC", false)}
                {render_adjustment_summary_table("perils/named_windstorm/year_built_summary", "Construction Summary", false)}
                {render_adjustment_summary_table("other_segmentations/state_summary", "State Summary", true)}
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.Selector>
      </HX.Section >

      <HX.Section title="Pricing Layer Segmentation">
        <HX.Section title="Marginal Impact Summary">
          <HX.Table
            with="pricing_layer_segmentation/marginal_impact_summary"
            data={["mi_1_in_10_aep_pt", "mi_1_in_250_oep_pt"]}
            fields={["layer1", "layer2", "layer3", "layer4", "layer5", "layer6"]}
          />
        </HX.Section>
        <HX.Section title="Global Summary" >
          {render_pricing_layer_segmentation_table("pricing_layer_segmentation/country")}
          <HX.Selector data={["pricing_layer_segmentation/state_country_outer"]} dropdown="country">
            {render_pricing_layer_segmentation_table("country_list", title_string = "Country Drilldown")}
          </HX.Selector>
        </HX.Section>
        <HX.Section title="Peril Summaries">
          {render_pricing_layer_segmentation_table("pricing_layer_segmentation/fire_occupancy")}
          {render_pricing_layer_segmentation_table("pricing_layer_segmentation/ws_zone")}
          {render_pricing_layer_segmentation_table("pricing_layer_segmentation/eq_zone")}
          {render_pricing_layer_segmentation_table("pricing_layer_segmentation/fl_risk_category")}
          {render_pricing_layer_segmentation_table("pricing_layer_segmentation/wf_risk_category")}
          {render_pricing_layer_segmentation_table("pricing_layer_segmentation/scs_risk_category")}
        </HX.Section>
      </HX.Section>
    </HX.Page >
  )
}

function render_adjustment_summary_table(path, table_title, skip_peril_gu_rate) {
  if (skip_peril_gu_rate) {
    return (
      <HX.Table
        data={[path]}
        fields={[
          { field: "name", width: 400 },
          "tiv",
          "itv",
          "num_locations",
          "total_gu_tech_rate"
        ]}
        title={table_title}
        kb-interactive
        dynamic={true}
      />
    )
  } else {
    return (
      <HX.Table
        data={[path]}
        fields={[
          { field: "name", width: 400 },
          "tiv",
          "itv",
          "num_locations",
          "gu_tech_rate",
          "total_gu_tech_rate"
        ]}
        title={table_title}
        kb-interactive
        dynamic={true}
      />
    )
  }
}

function render_pricing_layer_segmentation_table(path, title_string = "", use_filter = false) {
  if (use_filter) {
    return <HX.Table
      title={title_string}
      data={[path]}
      fields={[
        { field: "name", width: 400 },
        "tiv",
        "num_locations",
        "gu_loss",
        "gu_tech_rate",
        "gu_prem",
        "tech_prem_layer1",
        "tech_prem_layer2",
        "tech_prem_layer3",
        "tech_prem_layer4",
        "tech_prem_layer5",
        "tech_prem_layer6",
        "uw_adj_tech_prem_layer1",
        "uw_adj_tech_prem_layer2",
        "uw_adj_tech_prem_layer3",
        "uw_adj_tech_prem_layer4",
        "uw_adj_tech_prem_layer5",
        "uw_adj_tech_prem_layer6",
      ]}
      freezeLeft={1}
      filter={"name_populated"}
      kb-interactive
    />
  } else {
    return <HX.Table
      title={title_string}
      data={[path]}
      fields={[
        { field: "name", width: 400 },
        "tiv",
        "num_locations",
        "gu_loss",
        "gu_tech_rate",
        "gu_prem",
        "tech_prem_layer1",
        "tech_prem_layer2",
        "tech_prem_layer3",
        "tech_prem_layer4",
        "tech_prem_layer5",
        "tech_prem_layer6",
        "uw_adj_tech_prem_layer1",
        "uw_adj_tech_prem_layer2",
        "uw_adj_tech_prem_layer3",
        "uw_adj_tech_prem_layer4",
        "uw_adj_tech_prem_layer5",
        "uw_adj_tech_prem_layer6",
      ]}
      freezeLeft={1}
      kb-interactive
    />
  }
}

export { account_segmentation };
