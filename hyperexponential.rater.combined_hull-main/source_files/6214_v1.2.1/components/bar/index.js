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
    xAxisRangeStart: HX.PropTypes.string.optional,
    xAxisRangeEnd: HX.PropTypes.string.optional,
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
    let min_value = 1000000;
    let max_value = 0;
    barData.forEach(trace => {
      trace.data.forEach(entry => {
        if (entry.value < min_value) {
          min_value = entry.value;
        }
        if (entry.value > max_value) {
          max_value = entry.value;
        }
      });
    });
    return renderWithShownBy(
      data.nodes.shownBy,
      <Plot
        data={barData.map(trace => ({
          type: "bar",
          x: trace.data.map(entry => `${Number(entry.value)}`),
          y: trace.data.map(entry => `${Number(entry.label)}`),
          name: trace.label,
          orientation: 'h'
        }))}
        layout={{
          title: props.title,
          xaxis: {
            tickangle: props.xAxisTickAngle,
            title: props.xAxisLabel,
            autorange: false,
            range: [min_value, max_value],
            tickformat: ',.2%',
          },
          yaxis: {
            title: props.yAxisLabel,
            visible: false
          },
          bargap: props.gapBetweenBarsSize,
          barmode: props.barMode,
          bargroupgap: 0.1,
          height: 230
        }}
      />
    );
  }
});

export default Bar;