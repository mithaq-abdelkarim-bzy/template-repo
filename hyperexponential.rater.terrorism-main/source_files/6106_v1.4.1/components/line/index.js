import * as HX from "hx-model-components";
import Plot from "react-plotly.js";
import {
  getCoordNodes,
  getCoordChartData,
  coordPropTypes,
} from "../common/coord";
import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
} from "../common/utilities";

const Line = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    ...coordPropTypes,
  },
  mapper: (props, tools) => ({
    nodes: {
      ...getCommonNodes(props),
      lineNodes: getCoordNodes(props),
    },
  }),
  render: (props, data, tools) => {
    const lineData = getCoordChartData(data.nodes.lineNodes);

    return renderWithShownBy(
      data.nodes.shownBy,
      <Plot
        data={lineData.map((series) => ({
          x: series.points.map((entry) => entry.x),
          y: series.points.map((entry) => entry.y),
          mode: "lines+markers",
          type: "scatter",
          name: "Valuation",
          text: series.points.map((entry) => entry.label),
          textposition: "top center",
          marker: { size: 12 },
          name: series.label,
        }))}
        layout={{
          title: props.title,
          xaxis: { title: props.xAxisLabel },
          yaxis: { title: props.yAxisLabel },
          legend: {
            orientation: "h", // Set the legend to horizontal
            x: 0, // Align the legend to the bottom-left
            y: -0.2, // Position the legend below the chart
          },
        }}
      />
    );
  },
});
export default Line;