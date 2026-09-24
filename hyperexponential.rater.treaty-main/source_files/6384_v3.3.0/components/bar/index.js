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
const Bar = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    ...multiTraceCategoryPropTypes,
    xAxisTickAngle: HX.PropTypes.number.optional,
    gapBetweenBarsSize: HX.PropTypes.number.optional,
    barMode: HX.PropTypes.string.optional,
  },
  mapper: (props, tools) => {
    return {
      nodes: {
        ...getCommonNodes(props),
        barNodes: getMultiTraceCategoryNodes(props),
      },
    };
  },
  render: (props, data, tools) => {
    const barData = getMultiTraceCategoryChartData(props, data.nodes.barNodes);
    return renderWithShownBy(
      data.nodes.shownBy,
      <div >

        <Plot
          data={barData.map(trace => ({
            type: "bar",
            x: trace.data.map(entry => `${entry.label}`),
            y: trace.data.map(entry => entry.value),
            name: trace.label,
            marker: { color: trace.color || '#000' },
          }))}
          layout={{
            title: props.title,
            xaxis: {
              tickangle: props.xAxisTickAngle,
              title: props.xAxisLabel,
            },
            yaxis: {
              title: props.yAxisLabel,
            },
            bargap: props.gapBetweenBarsSize,
            barmode: props.barMode,
            bargroupgap: 0.1,
          }}
        />
      </div>
    );
  },
});
export default Bar;