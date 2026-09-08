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
const PieChart = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes, ...categoryPropTypes,
    ignoreLastRow: HX.PropTypes.boolean.optional,
  },
  mapper: props => ({
    nodes: { ...getCommonNodes(props), pieNodes: getCategoryNodes(props) },
  }),
  render: (props, data, tools) => {
    // Get pie chart data
    let pieData = getCategoryChartData(data.nodes.pieNodes);

    // Check if the last row should be ignored
    if (props.ignoreLastRow && pieData.length > 1) {
      pieData = pieData.slice(0, -1); // Exclude the last row
    }

    return renderWithShownBy(
      data.nodes.shownBy,
      <Plot
        data={[
          {
            type: "pie",
            labels: pieData.map(entry => entry.label),
            values: pieData.map(entry => entry.value),
            textInfo: props.textInfo,
            hole: props.hole,
            marker: {
              colors: ['#FCD8EF', '#993366'], // Set fixed colours for the first few slices
            },
          },
        ]}
        layout={{ title: props.title, width: 600, height: 400 }}
      />
    );
  },
});
export default PieChart;