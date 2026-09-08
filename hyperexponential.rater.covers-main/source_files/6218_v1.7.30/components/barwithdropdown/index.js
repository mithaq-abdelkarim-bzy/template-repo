import Plot from "react-plotly.js";
import * as HX from "hx-model-components";
import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
  wrapWith,
  getNodeValue
} from "../common/utilities";


const BarWithDropdown = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    data: HX.PropTypes.arrayOfType(
      HX.PropTypes.oneOfType([
        HX.PropTypes.objectOfType({
          structure: HX.PropTypes.path,
          label: HX.PropTypes.string.optional,
          labelBy: HX.PropTypes.path.optional,
        }),
        HX.PropTypes.objectOfType({
          list: HX.PropTypes.path,
          labelBy: HX.PropTypes.field.optional,
        }),
      ])
    ),
    fields: HX.PropTypes.arrayOfType(HX.PropTypes.field), // Fields to display in the chart
    labels: HX.PropTypes.arrayOfType(HX.PropTypes.string), // Labels for the dropdown options
    colors: HX.PropTypes.arrayOfType(HX.PropTypes.string).optional, // Optional colors for the bars
    xAxisTickAngle: HX.PropTypes.number.optional, // Optional property for X-axis tick angle
    gapBetweenBarsSize: HX.PropTypes.number.optional, // Optional gap size between bars
    barMode: HX.PropTypes.string.optional, // Optional bar mode (e.g., grouped, stacked)
    ignoreLastRow: HX.PropTypes.boolean.optional, // Optional flag to ignore the last row in data
    percentFormat: HX.PropTypes.arrayOfType(HX.PropTypes.boolean).optional, // Optional formatting for percentage
  },

  // Mapper function takes props and turns them into data bindings that will allow data from the hxd to be displayed in the chart
  mapper: (props, tools) => {
    return {
      nodes: {
        ...getCommonNodes(props),
        barNodes: props.data.map((entry) => ({
          type: "list",
          path: wrapWith(entry.list, props.with),
          nodes: {
            traces: props.fields.map((field) => ({
              type: "static",
              path: field,
            })),
            label: { type: "static", path: entry.labelBy },
          },
        })),
      },
      state: {
        selectedOption: props.fields[0],  // Default selected option
      },
    };
  },


  // Render function displays the chart
  render: (props, data, tools) => {
    const dropdownOptions = props.labels // Dropdown options
    const selectedOption = data.state.selectedOption  // Default to the first field

    // Extract and process data dynamically based on selected option
    let barData = data.nodes.barNodes.map((node) => {
      const traceIndex = props.fields.indexOf(selectedOption);
      return node.elements.map((element) => {
        return {
          value: getNodeValue(element.nodes.traces[traceIndex]), // Data for selected trace
          label: getNodeValue(element.nodes.label), // Label for x-axis

        };
      })
    }).flat();


    if (props.ignoreLastRow) {
      barData = barData.slice(0, -1); // Remove the last entry
    }


    return renderWithShownBy(
      data.nodes.shownBy,
      <div>
        {/* Dropdown for selecting data field */}
        <p>Select data:</p>
        <select
          value={selectedOption}
          onChange={(e) => data.setState({ selectedOption: e.target.value })}
        >
          {dropdownOptions.map((label, idx) => (
            <option value={props.fields[idx]} key={props.fields[idx]}>
              {label}
            </option>
          ))}
        </select>

        <Plot
          data={[
            {
              type: "bar",
              x: barData.map(entry => `${entry.label}`),
              y: barData.map(entry => entry.value),
              name: selectedOption,
              marker: {
                color: props.colors ? props.colors[props.fields.indexOf(selectedOption)] : "#FCD8EF" // if colors array not specified, it'll default to #FCD8EF
              },
              hovertemplate:
                // Format the hover info: show as percentage is percentFormat array specified or number with thousand separator
                (props.percentFormat && props.percentFormat[props.fields.indexOf(selectedOption)])
                  ? "%{x}: %{y:.2%}<extra></extra>"
                  : "%{x}: %{y:,.0f}<extra></extra>",
            },
          ]}
          layout={{
            autosize: true,
            title: props.title,
            xaxis: {
              tickangle: props.xAxisTickAngle,
              title: props.xAxisLabel,
              type: "category",
            },
            yaxis: {
              title: props.yAxisLabel,
            },
            // showlegend: true,
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
export default BarWithDropdown;