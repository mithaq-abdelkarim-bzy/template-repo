import Plot from "react-plotly.js";
import * as HX from "hx-model-components";
import {
  categoryPropTypes,
  getCategoryChartData,
  getCategoryNodes,
} from "../common/category";
import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
} from "../common/utilities";

const Waterfall_TP = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    ...categoryPropTypes,
    relativeOrAbsolute: HX.PropTypes.string.optional,
  },
  mapper: props => ({
    nodes: {
      ...getCommonNodes(props),
      waterfallNodes: getCategoryNodes(props),
    },
  }),
  render: (props, data, tools) => {
    const waterfallData = getCategoryChartData(data.nodes.waterfallNodes);
    return renderWithShownBy(
      data.nodes.shownBy,
      <Plot
        data={[
          {
            type: "waterfall",
            measure: [
              "absolute",
              "relative",
              "relative",
              "relative",
              "relative",
              "relative",
              "total",
              "absolute"
            ],
            x: waterfallData.map(entry => entry.label),
            y: waterfallData.map(entry => entry.value),
            textposition: props.textPosition,
            insidetextfont: { size: 11 },
            text: waterfallData.map(entry => entry.value),
            decreasing: { marker: { color: "#A8ADE1" } },
            increasing: { marker: { color: "#F49FD9" } },
            totals: { marker: { color: "#DC199B" } },
            hoverinfo: "y+delta",
            connector: {
              mode: "between",
              line: {
                width: 2,
                color: "Black",
                dash: 0,
              },
            },
          },
        ]}
        layout={{
          title: {
            text: props.title,
          },
          xaxis: {
            type: "category",
            title: props.xAxisLabel,
          },
          yaxis: {
            autorange: true,
            type: "linear",
            title: props.yAxisLabel,
          },
          autosize: true,
          showlegend: false,
        }}
      />
    );
  },
});
export default Waterfall_TP;