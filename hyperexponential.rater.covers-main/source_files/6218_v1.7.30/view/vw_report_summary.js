import * as HX from "hx-model-components";
import Bar from "components/bar";
import BarWithDropdown from "components/barwithdropdown";
import PieChart from "components/pie";
import ChoroplethMap from "components/choropleth";

commonFields = ["tiv", "share_lim", "perc_share_limit", "gn_prem", "ws_aal", "eq_aal", "aop_el", "rate_received", "ws_aal_rate", "eq_aal_rate", "aop_el_rate", "prem_as_perc_of_aal"]
chartLabels = ["TIV", "Share Limit", "Share Limit %", "GN Premium", "WS AAL", "EQ AAL", "AOP EL", "GN Rate", "WS AAL Rate", "EQ AAL Rate", "AOP EL Rate", "Premium as a % of AAL"]
chartPercFormat = [false, false, true, false, false, false, false, true, true, true, true, true]
chartColors = ["#FCD8EF", "#FCD8EF", "#993366", "#FCD8EF", "#FCD8EF", "#FCD8EF", "#FCD8EF", "#993366", "#993366", "#993366", "#993366", "#993366"]


const createBarComponent = ({
  title,
  data,
  xAxisLabel,
  shownBy
}) => {
  return (
    <BarWithDropdown
      title={title}
      data={data}
      fields={commonFields}
      labels={chartLabels}
      percentFormat={chartPercFormat}
      colors={chartColors}
      xAxisTickAngle={-45}
      gapBetweenBarsSize={0.05}
      xAxisLabel={xAxisLabel}
      yAxisLabel="Value"
      ignoreLastRow
      shownBy={shownBy}
    />
  );
};


function vw_report_summary(scale) {
  return (
    <HX.Page title="Report Summary" fullWidth viewScale={0.9} shownBy="cds/show_hide/page/show_sov">
      <HX.With context={{ type: "struct", path: "cds/exposure/aggregate" }}>

        <HX.Section title="TIV Summary">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Table
                fields={["coverage", "value", "percentage"]}
                data={["tiv_summary", null, "tiv_summary_total"]}
                filter="show_row"
                kb-interactive
              />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={["show_coverage_chart"]} />
              <PieChart
                title="Coverage Breakdown"
                textInfo="value"
                data={[{ list: "tiv_summary", value: "value", labelBy: "coverage" }]}
                ignoreLastRow
                shownBy="show_coverage_chart"
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Construction Summary">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Table
                fields={["iso_constr", ...commonFields]}
                data={["construction_summary", null, "construction_summary_total"]}
                kb-interactive
                filter="show_row"
                freezeLeft={1}
                syncColumnWidthsKey="table_sync"
              />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={["show_construction_chart"]} />
              {createBarComponent({
                data: [{ "labelBy": "iso_constr", "list": "construction_summary" }],
                title: "Construction Summary",
                xAxisLabel: "Construction",
                shownBy: "show_construction_chart"
              })}
              <Bar title="Construction Classification"
                data={[{ "labelBy": "iso_constr", "list": "construction_summary" }]}
                traces={[
                  { "field": "ws_aal", "label": "WS AAL", "color": "#FCD8EF" },
                  { "field": "aop_el", "label": "AOP EL", "color": "#993366" }
                ]}
                xAxisTickAngle={-45}
                gapBetweenBarsSize={0.05}
                xAxisLabel="Construction"
                yAxisLabel="Value"
                ignoreLastRow
                shownBy="show_construction_chart"
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Year Built Summary">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Table
                fields={["year_built", ...commonFields]}
                data={["year_built_summary", null, "year_built_summary_total"]}
                kb-interactive
                filter="show_row"
                freezeLeft={1}
                syncColumnWidthsKey="table_sync"
              />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={["show_year_built_chart"]} />
              {createBarComponent({
                data: [{ "labelBy": "year_built", "list": "year_built_summary" }],
                title: "Year Built Summary",
                xAxisLabel: "Year Built",
                shownBy: "show_year_built_chart"
              })}
            </HX.Pane>
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Occupancy Summary">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Table
                fields={["occupancy", ...commonFields]}
                data={["occupancy_summary", null, "occupancy_summary_total"]}
                kb-interactive
                filter="show_row"
                freezeLeft={1}
                syncColumnWidthsKey="table_sync"
              />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={["show_occupancy_chart"]} />
              {createBarComponent({
                data: [{ "labelBy": "occupancy", "list": "occupancy_summary" }],
                title: "Occupancy Summary",
                xAxisLabel: "Occupancy",
                shownBy: "show_occupancy_chart"
              })}
            </HX.Pane>
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Number of Floors Summary">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Table
                fields={["num_floors", ...commonFields]}
                data={["num_floors_summary", null, "num_floors_summary_total"]}
                kb-interactive
                filter="show_row"
                syncColumnWidthsKey="table_sync"
              />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={["show_num_floors_chart"]} />
              {createBarComponent({
                data: [{ "labelBy": "num_floors", "list": "num_floors_summary" }],
                title: "Number of Floors Summary",
                xAxisLabel: "Number of Floors",
                shownBy: "show_num_floors_chart"
              })}
            </HX.Pane>
          </HX.Pane>
        </HX.Section>

        <HX.Section title="State Summary">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Table
                fields={["state", ...commonFields]}
                data={["state_summary", null, "state_summary_total"]}
                kb-interactive
                filter="show_row"
                freezeLeft={1}
                syncColumnWidthsKey="table_sync"
              />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={["show_state_chart"]} />
              {createBarComponent({
                data: [{ "labelBy": "state", "list": "state_summary" }],
                title: "State Summary",
                xAxisLabel: "State",
                shownBy: "show_state_chart"
              })}
              <ChoroplethMap
                title="USA States"
                list="state_summary"
                text="label"
                locations="state"
                locationmode="USA-states"
                zs={commonFields}
                options={chartLabels}
                percentFormat={chartPercFormat}
                shownBy="show_state_chart"
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_report_summary };