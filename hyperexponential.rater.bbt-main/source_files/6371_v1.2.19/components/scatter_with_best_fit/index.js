import * as HX from "hx-model-components";
import Plot from "react-plotly.js";

import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
  wrapWith,
  getNodeValue
} from "../common/utilities";

const coordPropTypes = {
  series: HX.PropTypes.arrayOfType(
    HX.PropTypes.objectOfType({
      label: HX.PropTypes.string,
      marker_type: HX.PropTypes.string,
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

function getCoordNodesBestFit(props) {
  return props.series.map((seriesEntry) => ({
    label: seriesEntry.label ? { type: "const", value: seriesEntry.label } : undefined,
    marker_type: seriesEntry.marker_type ? { type: "const", value: seriesEntry.marker_type } : undefined,
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





export function getCoordBestFitChartData(coordSeriesNodes) {
  return coordSeriesNodes.map((entry) => ({
    label: getNodeValue(entry.label),
    marker_type: getNodeValue(entry.marker_type),
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


export function linearRegression(x, y) {
  const n = x.length;
  const sumX = x.reduce((a, b) => a + b, 0);
  const sumY = y.reduce((a, b) => a + b, 0);
  const sumXY = x.map((xi, i) => xi * y[i]).reduce((a, b) => a + b, 0);
  const sumXX = x.map((xi) => xi * xi).reduce((a, b) => a + b, 0);

  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;

  return { slope, intercept };
}

const ScatterBestFit = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    ...coordPropTypes,

  },
  mapper: (props, tools) => {
    // tools.log("Props received in mapper:", props);

    const lineNodes = getCoordNodesBestFit(props);

    // tools.log("Mapped lineNodes:", lineNodes);

    return {
      nodes: {
        ...getCommonNodes(props),
        lineNodes: lineNodes,
      }
    };
  },

  render: (props, data, tools) => {
    // tools.log("Scatter", data.nodes.lineNodes)
    const lineData = getCoordBestFitChartData(data.nodes.lineNodes);
    // tools.log("This Line Data")
    // tools.log("Scatter Line Data", lineData)
    const xValues = lineData.flatMap((series) => series.points.map((entry) => entry.x));
    const yValues = lineData.flatMap((series) => series.points.map((entry) => entry.y));

    const { slope, intercept } = linearRegression(xValues, yValues);


    const bestFitYValues = xValues.map(x => slope * x + intercept);

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
          data={
            lineData.map((series, index) => ({
              x: series.points.map((entry) => entry.x),
              y: series.points.map((entry) => entry.y),
              mode: "markers",
              type: "scatter",
              name: series.label,
              marker: {
                size: 12,
                color: series.colour,
                dash: series.marker_type,
              },
            }))

              .concat([
                {
                  x: xValues,
                  y: bestFitYValues,
                  mode: "lines",
                  type: "scatter",
                  name: `Best Fit`,
                  line: {
                    color: lineData.colour || 'red',
                    dash: 'solid',
                  },
                },
              ])
          }
          layout={{
            title: props.title,
            xaxis: {
              tickangle: props.xAxisTickAngle,
              title: props.xAxisLabel,
              tickmode: "linear",
            },
            yaxis: { title: props.yAxisLabel },
            legend: { orientation: "h", xanchor: "center", x: 0.5, y: -0.15 },
            width: 900,
            height: 600,
            // font: { family: "Acid Grotesk", size: 12, color: "black" },
          }}
        />

      </div>
    );
  },
});
export default ScatterBestFit;
