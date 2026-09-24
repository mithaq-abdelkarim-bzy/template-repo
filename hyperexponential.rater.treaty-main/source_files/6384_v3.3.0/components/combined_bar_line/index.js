import Plot from "react-plotly.js";
import * as HX from "hx-model-components";
import {
  getMultiTraceCategoryChartData,
  getMultiTraceCategoryNodes,
  multiTraceCategoryPropTypes,
} from "../common/category";
import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
} from "../common/utilities";
import {
  coordPropTypes,
  getCoordChartData,
  getCoordNodes
} from "../common/coord.js";

const LineBar = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    ...multiTraceCategoryPropTypes,
    ...coordPropTypes,
    xAxisTickAngle: HX.PropTypes.number.optional,
    gapBetweenBarsSize: HX.PropTypes.number.optional,
    barMode: HX.PropTypes.string.optional,
    width: HX.PropTypes.number.optional,
    height: HX.PropTypes.number.optional,
    y2SeparateAxis: HX.PropTypes.boolean,
    yAxis2Label: HX.PropTypes.string.optional
  },

  mapper: (props, tools) => {
    return {
      nodes: {
        ...getCommonNodes(props),
        barNodes: getMultiTraceCategoryNodes(props),
        lineNodes: getCoordNodes(props)
      },
    };
  },
  render: (props, data, tools) => {
    const barData = getMultiTraceCategoryChartData(props, data.nodes.barNodes);
    const lineData = getCoordChartData(data.nodes.lineNodes);

    // Extract x values from bar data for x-axis ticks
    const xValues = barData.flatMap(trace => trace.data.map(entry => entry.label));
    const uniqueXValues = [...new Set(xValues)]; // Ensure uniqueness

    // Set lists for indexing
    const colors = ["#CA3397", "#4FADC7"]; // Add your custom colors here
    const lineTypes = ["dash", "solid"]
    const lineModes = ['lines+markers', 'lines']

    // Calculate ymax for the primary y-axis (bar data)
    const barYValues = barData.flatMap(trace => trace.data.map(entry => entry.value));
    const barYmax = Math.max(0, ...barYValues); // Ensure barYmax is non-negative

    // Calculate ymax for the secondary y-axis (line data)
    const lineYValues = lineData.flatMap(series => series.points.map(entry => entry.y));
    const lineYmax = Math.max(0, ...lineYValues); // Ensure lineYmax is non-negative



    return renderWithShownBy(
      data.nodes.shownBy,
      <Plot
        data={[
          ...barData.map(trace => ({
            type: "bar",
            x: trace.data.map(entry => `${entry.label}`),
            y: trace.data.map(entry => entry.value),
            name: trace.label,
            marker: { color: trace.color || '#000' }, // Default color if not provided
          })),
          ...lineData.map((series, index) => ({
            x: series.points.map((entry) => entry.x),
            y: series.points.map((entry) => entry.y),
            mode: series.mode,
            line: {
              dash: series.mode,  // Set the line style to dashed
              color: series.color, // Apply color from the custom color
            },
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
            },
            name: series.label,
            yaxis: props.y2SeparateAxis === true ? "y2" : "y",
          }))
        ]}
        layout={{
          title: props.title || 'Default Title',
          xaxis: {
            tickangle: props.xAxisTickAngle,
            title: props.xAxisLabel || 'X Axis',
            tickvals: uniqueXValues, // Set x-axis ticks to match x values
            ticktext: uniqueXValues, // Set tick labels to match x values
          },
          yaxis: {
            title: props.yAxisLabel || 'Y Axis',
            zeroline: true,
            range: [0, barYmax * 1.1],
          },
          yaxis2: {
            title: props.yAxis2Label,
            overlaying: 'y',
            side: "right",
            zeroline: true,
            range: [0, lineYmax * 1.1],
          },
          bargap: props.gapBetweenBarsSize,
          barmode: props.barMode,
          bargroupgap: 0.1,
          width: props.width || 800,
          height: props.height || 500,
        }}
      />
    );
  },
});
export default LineBar;