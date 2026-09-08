import * as HX from "hx-model-components";
import Plot from "react-plotly.js";
import {
  getCategoryNodes,
  getCategoryChartData,
  categoryPropTypes,
} from "../common/category";
import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
} from "../common/utilities";

const options = ["Relative", "Absolute"]

const Waterfall = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    ...categoryPropTypes,
    width: HX.PropTypes.number.optional,
    height: HX.PropTypes.number.optional,
    xAxisLabel: HX.PropTypes.string.optional,
    yAxisLabel: HX.PropTypes.string.optional,
    xLabelGap: HX.PropTypes.number.optional
  },
  mapper: (props) => ({
    nodes: {
      ...getCommonNodes(props),
      waterfallNodes: getCategoryNodes(props),
    },
    state: {
      selectedOption: options[0]
    }
  }),

  render: (props, data, tools) => {
    const waterfallData = getCategoryChartData(data.nodes.waterfallNodes);

    var connectorColor = "White";
    const relativeOrAbsolute = data.state.selectedOption.toLowerCase();
    if (relativeOrAbsolute == "relative") {
      connectorColor = "Black"
    }

    // Create correct colors by defining which bars are totals
    const barColors = Array(waterfallData.length).fill('relative'); // Relative bars coloured pink
    if (relativeOrAbsolute == "absolute") {
      barColors.fill('absolute')
    }
    if (barColors.length > 0) {
      barColors[0] = 'total';
      barColors[barColors.length - 1] = 'total'; // First and last bars are total; coloured purple
    }

    console.log('Bar Colors:', barColors); // Debugging

    return renderWithShownBy(
      data.nodes.shownBy,
      <div>
        <div>
          <select value={data.state.selectedOption} onChange={e => data.setState(s => ({ ...s, selectedOption: e.target.value }))}>
            {options.map(option => <option value={option}>{option}</option>)}
          </select>
        </div>
        <div>
          <Plot
            // https://plotly.com/javascript/waterfall-charts/
            data={[
              {
                type: "waterfall",
                // measure: [relativeOrAbsolute, relativeOrAbsolute, relativeOrAbsolute, relativeOrAbsolute],
                measure: Array(waterfallData.length).fill(relativeOrAbsolute),
                x: waterfallData.map((entry) => entry.label),
                y: waterfallData.map((entry) => entry.value),
                measure: barColors,
                textposition: "outside",
                text: waterfallData.map((entry) =>
                  entry.value !== null && entry.value !== undefined && !isNaN(entry.value)
                    ? (entry.value * 100).toFixed(2) + "%"
                    : ''  // Fallback for null, undefined, or invalid numbers
                ),  // Check if value is valid, then round to 2 decimal places and show as percentage
                // pink #E8A4D5 purple CA3397
                decreasing: { marker: { color: 'pink' } },
                increasing: { marker: { color: 'pink' } },
                totals: { marker: { color: 'purple' } },
                marker: {
                  color: barColors,
                },
                hoverinfo: "y+delta",
                connector: {
                  mode: "between",
                  line: {
                    width: 1,
                    color: connectorColor,
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
                title: {
                  text: props.xAxisLabel || 'X Axis',
                  standoff: props.xLabelGap || 25,
                },
                showline: true,
                type: "category",
                automargin: true,
              },
              yaxis: {
                title: props.yAxisLabel || 'Y Axis',
                type: "linear",
              },
              autosize: true,
              showlegend: false,
              width: props.width || 800,
              height: props.height || 600,
            }}
          />
        </div>
      </div>
    );
  },
});

export default Waterfall;