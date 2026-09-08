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
    ignoreLastRow: HX.PropTypes.boolean.optional,
  },
  mapper: (props, tools) => {
    return {
      nodes: {
        ...getCommonNodes(props),
        barNodes: getMultiTraceCategoryNodes(props),
      }
    };
  },
  render: (props, data, tools) => {

    let barData = getMultiTraceCategoryChartData(props, data.nodes.barNodes);

    // Check if the last row should be ignored
    if (props.ignoreLastRow) {
      barData = barData.map(trace => ({
        ...trace,
        data: trace.data.slice(0, -1), // Exclude the last row from each trace
      }));
    }

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
            hovertemplate: "%{x}: %{y:,.0f}<extra></extra>",
          }))}
          layout={{
            autosize: true,
            title: props.title,
            xaxis: {
              tickangle: props.xAxisTickAngle,
              title: props.xAxisLabel,
            },
            yaxis: {
              title: props.yAxisLabel,
            },
            showlegend: true,
            bargap: props.gapBetweenBarsSize,
            barmode: props.barMode,
            bargroupgap: 0.1,
            margin: {
              b: 250, // Increase bottom margin to make room for longer labels
            },

          }}

          style={{
            // contents of the style prop
            width: "100%",
            height: "100%",
          }}
          useResizeHandler
        />
      </div>
    );
  },
});
export default Bar;