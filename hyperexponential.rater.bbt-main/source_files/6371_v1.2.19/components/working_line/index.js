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
    yAxis2Label: HX.PropTypes.string.optional, // Optional label for the second y-axis
    yAxis2Title: HX.PropTypes.string.optional, // Optional title for the second y-axis
    yAxis2Show: HX.PropTypes.boolean.optional,    // Flag to show the second y-axis
  },
  mapper: (props, tools) => ({
    nodes: {
      ...getCommonNodes(props),
      lineNodes: getCoordNodes(props),
    },
  }),
  render: (props, data, tools) => {
    tools.log("Hello")
    const lineData = getCoordChartData(data.nodes.lineNodes);

    return renderWithShownBy(
      data.nodes.shownBy,
      <Plot
        data={lineData.map((series) => ({
          x: series.points.map((entry) => entry.x),
          y: series.points.map((entry) => entry.y),
          mode: series.mode,
          type: "scatter",
          name: "Valuation",
          text: series.points.map((entry) => entry.label),
          textposition: "top center",
          marker: {
            size: 12,
            color: series.color,  // Set color for the markers (points)
          },
          line: {
            color: series.color,  // Set color for the line
            dash: series.lineType,
            width: 4,
          },
          name: series.label,
          yaxis: series.yAxis || 'y',
        }))}
        layout={{
          title: props.title,
          xaxis: { title: props.xAxisLabel },
          yaxis: { title: props.yAxisLabel },
          yaxis2: props.yAxis2Show ? {
            title: props.yAxis2Title,
            overlaying: 'y',
            side: 'right',
          } : undefined,
        }}
      />
    );
  },
});
export default Line;