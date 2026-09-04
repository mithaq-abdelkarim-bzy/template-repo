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
} from "../common/coords";
import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
} from "../common/utilities";

const customTickFormat = (tickValue) => {
  const formattedValue = d3.format(",.3s")(tickValue); // Use D3 formatting
  if (formattedValue.endsWith("G")) {
    return formattedValue.replace("G", "B"); // Replace "G" with "B"
  }
  return formattedValue; // Return the formatted value as is
};


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
          width: "100%",
          height: "100%"
        }}
      > {(barData && barData[0].data[0]) ?
        (<Plot
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
              marker: { size: 10 },
              name: series.label,
              yaxis: "y2",
              line: {
                color: series.color,
              },
            })),
          ]}
          layout={{
            title: {
              text: props.title,
              x: 0,
              xanchor: 'left',
              yanchor: 'top',
              font: {
                family: 'Acid Grotesk',
                size: 18,
                color: lineData[0]?.color || "black"
              }
            },

            xaxis: {
              type: "category",
              categoryorder: "array",
              tickangle: barData[0].data.length > 100 ? -90 : props.xAxisTickAngle,
              title: props.xAxisLabel,
              tickmode: "linear",
              range: [-0.5, barData[0].data.length - 0.5],
              automargin: true,
              tickfont: { family: "Acid Grotesk", size: barData[0].data.length > 100 ? 7 : 12, color: "black" },

            },
            yaxis: {
              title: props.yAxisLabel,
              tickvals: null,
              tickformat: (tickVals) => tickVals.map(customTickFormat),
              showticksuffix: "all",
              showline: true
            },
            yaxis2: {
              title: props.yAxis2Label,
              overlaying: "y",
              side: "right",
              showline: true,
              showticksuffix: 'all',
              rangemode: 'tozero'
            },
            legend: { orientation: "h", xanchor: "right", yanchor: "top", x: 1, y: 1 },
            bargap: props.gapBetweenBarsSize,
            barmode: props.barMode,
            bargroupgap: 0.1,
            width: 1450,
            height: 1100,
            font: { family: "Acid Grotesk", size: 12, color: "black" },
          }}
        />) : <div>No Chart Data To Display</div>}
      </div>
    );
  },
});
export default CombinationChart;