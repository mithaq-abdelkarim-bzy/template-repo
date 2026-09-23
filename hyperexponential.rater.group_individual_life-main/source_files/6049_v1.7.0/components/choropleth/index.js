import Plot from "react-plotly.js";
import * as HX from "hx-model-components";

const formatNumber = (num) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(num / 1000) + 'K';
};

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
      .map((element) =>
        element
          ? {
            locations: element.nodes.locations.value,
            text: element.nodes.text.value,
            z: element.nodes.z.value,
          }
          : null
      )
      .filter((e) => !!e);

    return (
      <Plot
        data={[
          {
            type: "choropleth",
            locationmode: "ISO-3",
            locations: points.map(point => point.locations),
            z: points.map(point => point.z),
            text: points.map(point => point.text),
            customdata: points.map(point => formatNumber(point.z)),
            autocolorscale: true,
            hovertemplate: '<b>%{text}</b><br>Sum Insured: %{customdata}<extra></extra>',
            colorbar: {
              orientation: 'h',
              x: 0.5,
              y: 0.9,
              len: 0.8,
              thickness: 20,
              xanchor: 'center',
              title: {
                text: 'Total Sum Insured',
                side: 'top',
                font: {
                  family: 'Arial, sans-serif',
                  size: 14,
                  color: 'black'
                }
              },
              tickfont: {
                family: 'Arial, sans-serif',
                size: 12,
                color: 'black'
              }
            }
          },
        ]}
        layout={{
          geo: {
            scope: "world",
            countrycolor: "rgb(255, 255, 255)",
            showland: true,
            landcolor: "rgb(217, 217, 217)",
            showlakes: false,
          },
          margin: {
            t: 20,  // Reduced top margin to minimize space
            b: 0,
            l: 0,
            r: 0
          }
        }}
        useResizeHandler={true}
        style={{ width: "100%", height: "100vh" }}
      />
    );
  },
});

export default ChoroplethMap;
