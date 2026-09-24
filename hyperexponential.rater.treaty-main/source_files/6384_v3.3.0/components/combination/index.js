import Plot from "react-plotly.js";

import * as HX from "hx-model-components";

import {
  getMultiTraceCategoryChartData,
  getMultiTraceCategoryNodes,
  multiTraceCategoryPropTypes,
} from "../common/category";
import {
  coordPropTypes,
  getCoordChartData,
  getCoordNodes,
} from "../common/coord.js";
import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
} from "../common/utilities";

const CombinationChart = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    ...multiTraceCategoryPropTypes,
    ...coordPropTypes,
    xAxisTickAngle: HX.PropTypes.number.optional,
    gapBetweenBarsSize: HX.PropTypes.number.optional,
    barMode: HX.PropTypes.string.optional,
    yAxis2Label: HX.PropTypes.string.optional,
  },
  mapper: (props, tools) => {
    return {
      nodes: {
        ...getCommonNodes(props),
        barNodes: getMultiTraceCategoryNodes(props),
        lineNodes: getCoordNodes(props),
      },
    };
  },
  render: (props, data, tools) => {
    const lineData = getCoordChartData(data.nodes.lineNodes);
    const barData = getMultiTraceCategoryChartData(props, data.nodes.barNodes);
    return renderWithShownBy(
      data.nodes.shownBy,
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Plot
          data={[
            ...barData.map((trace, index) => ({
              type: "bar",
              x: trace.data.map(entry => `${entry.label}`),
              y: trace.data.map(entry => entry.value),
              name: trace.label,
              marker: {
                color: props.traces[index].color,
              },
            })),
            ...lineData.map((series, index) => ({
              x: series.points.map(entry => entry.x),
              y: series.points.map(entry => entry.y),
              mode: "lines+markers",
              type: "line",
              name: "Valuation",
              text: series.points.map(entry => entry.label),
              textposition: "top center",
              marker: { size: 12 },
              name: series.label,
              yaxis: "y2",
              line: {
                color: props.series[index].color,
              },
            })),
          ]}
          layout={{
            title: props.title,
            xaxis: {
              tickangle: props.xAxisTickAngle,
              title: props.xAxisLabel,
              tickmode: "linear",
            },
            yaxis: { title: props.yAxisLabel },
            yaxis2: {
              title: props.yAxis2Label,
              overlaying: "y",
              side: "right",
              tickformat: ".4%",
            },
            legend: { orientation: "h", xanchor: "center", x: 0.5, y: -0.15 },
            bargap: props.gapBetweenBarsSize,
            barmode: props.barMode,
            bargroupgap: 0.1,
            width: 900,
            height: 600,
            font: { family: "Acid Grotesk", size: 12, color: "black" },
          }}
        />
      </div>
    );
  },
});
export default CombinationChart;