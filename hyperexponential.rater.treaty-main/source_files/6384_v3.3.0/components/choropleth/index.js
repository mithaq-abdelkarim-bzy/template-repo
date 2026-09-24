import Plot from "react-plotly.js";

import * as HX from "hx-model-components";

const ChoroplethMap = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    title: HX.PropTypes.string,
    list: HX.PropTypes.path,
    text: HX.PropTypes.field,
    locations: HX.PropTypes.field,
    z: HX.PropTypes.field,
  },
  mapper: props => ({
    nodes: {
      points: {
        type: "list",
        path: props.list,
        nodes: {
          text: { type: "static", path: props.text },
          locations: { type: "static", path: props.locations },
          z: { type: "static", path: props.z },
        },
      },
    },
  }),
  render: (props, data, tools) => {
    const points = data.nodes.points.elements
      .map(element =>
        element
          ? {
            locations: element.nodes.locations.value,
            text: element.nodes.text.value,
            z: element.nodes.z.value,
          }
          : null
      )
      .filter(e => !!e);
    return (
      <Plot
        data={[
          {
            type: "choropleth",
            locationmode: "USA-states",
            locations: points.map(point => point.locations),
            z: points.map(point => point.z),
            text: points.map(point => point.text),
            autocolorscale: true,
          },
        ]}
        layout={{
          title: props.title,
          geo: {
            scope: "usa",
            countrycolor: "rgb(255, 255, 255)",
            showland: true,
            landcolor: "rgb(255, 255, 255)",
            showlakes: true,
          },
          margin: {
            l: 0,
            r: 0,
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
    );
  },
});
export default ChoroplethMap;