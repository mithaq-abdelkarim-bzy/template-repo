import * as HX from "hx-model-components";
import Plot from "react-plotly.js";
import {
  wrapWith,
  getCommonNodes,
  getNodeValue,
  renderWithShownBy,
} from "../common/utilities";


const ChoroplethMap = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    title: HX.PropTypes.string,
    node_path: HX.PropTypes.path,
    zs: HX.PropTypes.arrayOfType(HX.PropTypes.field),
    options: HX.PropTypes.arrayOfType(HX.PropTypes.string),
    withMarkers: HX.PropTypes.boolean,
    text: HX.PropTypes.field.optional,
    shownBy: HX.PropTypes.path.optional,
    with: HX.PropTypes.path.optional,
    scope: HX.PropTypes.string.optional,
    percentFormat: HX.PropTypes.arrayOfType(HX.PropTypes.boolean).optional,
  },

  mapper: (props) => {
    const dropdownOptions = props.options  // Get options for the dropdown

    return {
      nodes: {
        data: { type: "static", path: props.node_path },
        ...getCommonNodes(props),
      },
      state: {
        selectedOption: dropdownOptions[0],  // Default selected option
      },
    };
  },


  render: (props, data, tools) => {
    const dropdownOptions = props.options
    const selectedOption = data.state.selectedOption

    let locations_data;

    if (data.nodes.data.value !== undefined && data.nodes.data.value !== null) {
      locations_data = JSON.parse(data.nodes.data.value);


      const dynamicOptionsMapper = dropdownOptions.reduce((acc, option, index) => {
        // Map each option to its corresponding z field (e.g., z1, z2)
        const zField = props.zs[index]; // Get the z field (e.g., z1, z2)
        if (zField) {
          acc[option] = props.zs[index]; // set the value: {Num of Locations: "num_locations"}
        }
        return acc;
      }, {});


      const points = locations_data
        .map((location) =>
          location && location.lat && location.lon && location[dynamicOptionsMapper[selectedOption]]
            ? {
              state: location.state,
              country: location.country,
              lat: location.lat,
              lon: location.lon,
              z: location[dynamicOptionsMapper[selectedOption]], // Use dynamically selected Z field
            }
            : null
        )
        .filter((e) => !!e);

      const percentFormatEnabled =
        props.percentFormat && props.percentFormat[props.options.indexOf(selectedOption)];

      const formatOptions = percentFormatEnabled
        ? {
          tickformat: '.3%',
          cmin: 0,
        }
        : {
          ticktext: function (value) {
            return Plotly.d3.format("~s")(value);
          },
          cmin: 0,
        };

      // Right Choropleth Chart
      if (props.withMarkers) {
        // Sorting in ascending so we have higher value markers show on top
        const sortedPoints = points.sort((a, b) => a.z - b.z);
        const onlyUsStates = sortedPoints.every(obj => obj.country === "United States");

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
                  type: "scattergeo",
                  mode: "markers",
                  lat: sortedPoints.map(p => Number(p.lat)),
                  lon: sortedPoints.map(p => Number(p.lon)),
                  customdata: sortedPoints.map(p => ({ "z": p.z, "text": p.country == "United States" ? p.state : p.country })),  // if it's US, we show the State, otherwise we show the Country
                  hovertemplate: percentFormatEnabled
                    ? "%{customdata.text}<br>Value: %{customdata.z:.3%}<extra></extra>" // Format as percentage
                    : "%{customdata.text}<br>Value: %{customdata.z:,.0f}<extra></extra>",
                  marker: {
                    size: 10,
                    color: sortedPoints.map(p => p.z),
                    colorscale: "YlOrRd",
                    colorbar: formatOptions,
                    reversescale: true,
                    showscale: true,
                    zmin: 0,
                    line: {
                      width: 1,
                      color: "black"
                    }
                  }
                }
              ]}
              layout={{
                title: props.title,
                geo: {
                  scope: onlyUsStates ? "usa" : "world",
                  fitbounds: "locations",
                  visible: true, // this field is required - sets the border to be visible
                  showcountries: true,
                  showland: true,
                  landcolor: "rgb(217, 217, 217)",
                  showlakes: true,
                  resolution: 50
                },
                margin: {
                  l: 20,
                  r: 20,
                  t: 50,
                  b: 0,
                  autoexpand: true
                }
              }}
              style={{
                width: "100%",
                height: "100%",
              }}
              useResizeHandler={true}
            />
          </div>
        )
      }
      // Left Choropleth Chart
      else {
        const countryMap = {};
        const usStateMap = {};

        points.forEach(({ country, state, z }) => {
          if (country === "United States") {
            if (!usStateMap[state]) {
              usStateMap[state] = { state, z: 0 };
            }
            usStateMap[state].z += z;
          } else {
            if (!countryMap[country]) {
              countryMap[country] = { country, z: 0 };
            }
            countryMap[country].z += z;
          }
        });

        const countryPoints = Object.values(countryMap);
        const usStatePoints = Object.values(usStateMap);

        const combinedZ = [...countryPoints.map(d => d.z), ...usStatePoints.map(d => d.z)];
        const zmax = Math.max(...combinedZ);

        const showUsScale = () => usStatePoints.length > 0 && countryPoints.length === 0;

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

            <Plot
              data={[
                {
                  type: "choropleth",
                  locationmode: "country names",
                  locations: countryPoints.map(p => p.country),
                  z: countryPoints.map(p => p.z),
                  zmin: 0,
                  zmax: zmax,
                  text: countryPoints.map(p => p.country),
                  colorscale: "YlOrRd",
                  colorbar: formatOptions,
                  reversescale: true,
                  showscale: true,
                  hovertemplate: percentFormatEnabled
                    ? "%{text}<br>Value: %{z:.3%}<extra></extra>"
                    : "%{text}<br>Value: %{z:,.0f}<extra></extra>",
                },
                {
                  type: "choropleth",
                  locationmode: "USA-states",
                  locations: usStatePoints.map(p => p.state),
                  z: usStatePoints.map(p => p.z),
                  zmin: 0,
                  zmax: zmax,
                  text: usStatePoints.map(p => p.state),
                  colorscale: "YlOrRd",
                  colorbar: formatOptions,
                  reversescale: true,
                  showscale: showUsScale(),
                  hovertemplate: percentFormatEnabled
                    ? "%{text}<br>Value: %{z:.3%}<extra></extra>"
                    : "%{text}<br>Value: %{z:,.0f}<extra></extra>",
                }
              ]}
              layout={{
                title: props.title,
                geo: {
                  showcountries: true,
                  showland: true,
                  landcolor: "rgb(217, 217, 217)",
                  showlakes: true,
                  resolution: 50
                },
                margin: {
                  l: 20,
                  r: 20,
                  t: 50,
                  b: 0,
                  autoexpand: true
                }
              }}
              style={{
                width: "100%",
                height: "100%",
              }}
              useResizeHandler={true}
            />
          </div>
        );
      }
    }
  }
})

export default ChoroplethMap;

