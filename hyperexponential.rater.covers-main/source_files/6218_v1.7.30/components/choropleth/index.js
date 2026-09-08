import * as HX from "hx-model-components";
import Plot from "react-plotly.js";
import {
  wrapWith,
  getCommonNodes,
  renderWithShownBy,
} from "../common/utilities";

const ChoroplethMap = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    title: HX.PropTypes.string,
    list: HX.PropTypes.path,
    text: HX.PropTypes.field,
    locations: HX.PropTypes.field,
    locationmode: HX.PropTypes.oneOfLiteral(
      ["ISO-3", "country names", "USA-states", "USA-counties"]
    ),
    shownBy: HX.PropTypes.path.optional,
    with: HX.PropTypes.path.optional,
    scope: HX.PropTypes.string.optional,
    ignoreLastRow: HX.PropTypes.boolean.optional,
    zs: HX.PropTypes.arrayOfType(HX.PropTypes.field),
    options: HX.PropTypes.arrayOfType(HX.PropTypes.string),
    percentFormat: HX.PropTypes.arrayOfType(HX.PropTypes.boolean).optional,
  },

  mapper: (props) => {
    const dropdownOptions = props.options  // Get options for the dropdown
    const zs = props.zs  // Get the z fields from the props

    // Dynamically generate nodes based on options and zs
    const dynamicNodes = dropdownOptions.reduce((acc, option, index) => {
      // Map each option to its corresponding z field (e.g., z1, z2)
      const zField = zs[index]; // Get the z field (e.g., z1, z2)
      if (zField) {
        acc[option] = { type: "static", path: zField };  // Set static for each option
      }
      return acc;
    }, {});

    return {
      nodes: {
        ...getCommonNodes(props),
        points: {
          type: "list",
          path: wrapWith(props.list, props.with),
          nodes: {
            text: { type: "static", path: props.text },
            locations: { type: "static", path: props.locations },
            ...dynamicNodes,  // Add dynamically generated nodes for z fields
          },
        },
      },
      state: {
        selectedOption: dropdownOptions[0],  // Default selected option
      },
    };
  },


  render: (props, data, tools) => {
    const dropdownOptions = props.options
    const selectedOption = data.state.selectedOption

    const elements = props.ignoreLastRow
      ? data.nodes.points.elements.slice(0, -1)
      : data.nodes.points.elements;

    const points = elements
      .map((element) =>
        element && element.nodes.text && element.nodes.locations && element.nodes[selectedOption]
          ? {
            locations: element.nodes.locations.value,
            text: element.nodes.text.value,
            z: element.nodes[selectedOption].value, // Use dynamically selected Z field
          }
          : null
      )
      .filter((e) => !!e);

    let mapscope;
    if (props.locationmode === "USA-states" || props.locationmode === "USA-counties") {
      mapscope = "usa";
    }

    return renderWithShownBy(
      data.nodes.shownBy,

      <div>
        {/* Dropdown for selecting Z value */}
        <p>Select data:</p>
        <select
          value={selectedOption}
          onChange={(e) => data.setState({ selectedOption: e.target.value })}
        >
          {dropdownOptions.map((option) => (
            <option value={option} key={option}>
              {option}
            </option>
          ))}
        </select>



        {/* Plotly Choropleth Map */}
        <Plot
          data={[
            {
              type: "choropleth",
              locationmode: props.locationmode,
              locations: points.map((point) => point.locations),
              z: points.map((point) => point.z),
              text: points.map((point) => point.text),
              colorscale: "YlOrRd",
              reversescale: true,
              hovertemplate: props.percentFormat && props.percentFormat[props.options.indexOf(selectedOption)]
                ? "%{text}<br>Value: %{z:.2%}<extra></extra>" // Format as percentage
                : "%{text}<br>Value: %{z:,.0f}<extra></extra>",
              geojson:
                "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json", // URL for county boundaries in geoJSON format
            },
          ]}
          layout={{
            title: props.title,
            autosize: true,
            geo: {
              scope: mapscope,
              countrycolor: "rgb(255, 255, 255)",
              showland: true,
              landcolor: "rgb(217, 217, 217)",
              showlakes: true,
            },
            margin: { t: 50, r: 0, b: 0, l: 0 },
          }}
          style={{
            width: "100%",
            height: "100%",
          }}
          useResizeHandler
        />
      </div>
    );
  },
});

export default ChoroplethMap;
