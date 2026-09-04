import Plot from "react-plotly.js";
import * as HX from "hx-model-components";



import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
  wrapWith,
  getNodeValue
} from "../common/utilities";


const coordPropTypesDualYAxis = {
  series: HX.PropTypes.arrayOfType(
    HX.PropTypes.objectOfType({
      yaxis: HX.PropTypes.string,
      label: HX.PropTypes.string,
      line_type: HX.PropTypes.string,
      colour: HX.PropTypes.string,

      points: HX.PropTypes.arrayOfType(
        HX.PropTypes.objectOfType({
          list: HX.PropTypes.path,
          x: HX.PropTypes.field,
          y: HX.PropTypes.field,
        })
      ),
    })
  ),
};


function getCoordNodesDualYAxis(props) {
  return props.series.map((seriesEntry) => ({
    yaxis: seriesEntry.yaxis ? { type: "const", value: seriesEntry.yaxis } : undefined,
    label: seriesEntry.label ? { type: "const", value: seriesEntry.label } : undefined,
    line_type: seriesEntry.line_type ? { type: "const", value: seriesEntry.line_type } : undefined,
    colour: seriesEntry.colour ? { type: "const", value: seriesEntry.colour } : undefined,
    points: seriesEntry.points.map((pointsEntry) => ({
      type: "list",
      path: pointsEntry.list,
      nodes: {
        x: { type: "static", path: pointsEntry.x },
        y: { type: "static", path: pointsEntry.y },
      },
    })),
  }));
}



export function getCoordChartData2(coordSeriesNodes) {
  return coordSeriesNodes.map((entry) => ({
    yaxis: getNodeValue(entry.yaxis),
    label: getNodeValue(entry.label),
    line_type: getNodeValue(entry.line_type),
    colour: getNodeValue(entry.colour),
    points: entry.points.map((pointsEntry) =>
      pointsEntry.type === "list"
        ? pointsEntry.elements
          .map((pointsElement) =>
            pointsElement
              ? {
                x: getNodeValue(pointsElement.nodes.x),
                y: getNodeValue(pointsElement.nodes.y),
              }
              : null
          )
          .filter((e) => !!e)
        : [
          {
            x: getNodeValue(pointsEntry.x),
            y: getNodeValue(pointsEntry.y),
          },
        ]
    ).flat(),
  }));
}


const TwoAxisLineChart = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    ...coordPropTypesDualYAxis,
    yAxis2Label: HX.PropTypes.string,
    height: HX.PropTypes.number.optional,
    width: HX.PropTypes.number.optional,
    line_thickness: HX.PropTypes.number.optional,
    legend_position: HX.PropTypes.string.optional,
  },
  mapper: (props, tools) => {

    // tools.log("Props received in mapper two lines:", props);


    const lineNodes = getCoordNodesDualYAxis(props);


    // tools.log("Mapped lineNodes two lines:", lineNodes);

    return {
      nodes: {
        ...getCommonNodes(props),
        lineNodes: lineNodes,
      }
    };
  },

  render: (props, data, tools) => {
    // tools.log("2 Linenodes", data.nodes.lineNodes)
    const lineData = getCoordChartData2(data.nodes.lineNodes);
    // tools.log("Two lines Data", lineData)
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
            ...lineData.map((series, index) => ({
              x: series.points.map((entry) => entry.x),
              y: series.points.map((entry) => entry.y),
              mode: "lines",
              type: "line",
              name: series.label,
              textposition: "top center",
              marker: { size: 12 },
              yaxis: series.yaxis,
              line: {
                color: series.colour,
                dash: series.line_type,
                width: props.line_thickness || 2
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

            },
            legend: {
              orientation: props.legend_position ? "v" : "h",  // Vertical if legend_position is given, horizontal otherwise
              xanchor: props.legend_position ? "right" : "center",  // Right side if legend_position, center otherwise
              x: props.legend_position ? 1.6 : 0.5,  // Move to the right of the graph if legend_position is given, center otherwise
              y: props.legend_position ? 0.9 : -0.15,  // Vertically centered if legend_position, below the graph otherwise
              yanchor: props.legend_position ? "middle" : "top",  // Center the legend vertically if legend_position, otherwise top-aligned
            },
            width: props.width || 900,
            height: props.height || 600,
            // font: { family: "Acid Grotesk", size: 12, color: "black" },
          }}
        />
      </div>
    );
  },
});
export default TwoAxisLineChart;

