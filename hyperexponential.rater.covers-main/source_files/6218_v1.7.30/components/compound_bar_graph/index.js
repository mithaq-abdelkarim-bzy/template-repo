// import Plot from "react-plotly.js";
// import * as HX from "hx-model-components";

// import {
//   commonPropTypes,
//   getCommonNodes,
//   renderWithShownBy,
//   wrapWith,
//   getNodeValue
// } from "../common/utilities";



// // export function getCategoryChartData(categoryNodes) {
// //   return categoryNodes
// //     .map((entry, index) =>
// //       entry.type === "list"
// //         ? entry.elements.map(
// //           (element) => element
// //             ? ({
// //               value: getNodeValue(element?.nodes.value),
// //               label: getNodeValue(element?.nodes.label),
// //             })
// //             : null
// //         ).filter(e => !!e)
// //         : [
// //           {
// //             value: getNodeValue(entry.value),
// //             label:
// //               getNodeValue(entry.label) ??
// //               entry.value.metadata.view?.label ??
// //               `index_${index}`,
// //           },
// //         ]
// //     )
// //     .flat();
// // }

// export function getCategoryChartData(categoryNodes) {
//   return categoryNodes.map((entry, index) => {
//     if (entry.type === "list") {
//       return entry.elements.map((element) => ({
//         value: getNodeValue(element.nodes.value),
//         label: getNodeValue(element.nodes.labelBy),
//       })).filter(e => !!e);
//     } else {
//       return {
//         value: getNodeValue(entry.value),
//         label: getNodeValue(entry.label) ?? `index_${index}`,
//       };
//     }
//   }).flat();
// }

// export const multiTraceCategoryPropTypes = {
//   data: HX.PropTypes.arrayOfType(
//     HX.PropTypes.oneOfType([
//       HX.PropTypes.objectOfType({
//         structure: HX.PropTypes.path,
//         label: HX.PropTypes.string.optional,
//         labelBy: HX.PropTypes.path.optional,
//       }),
//       HX.PropTypes.objectOfType({
//         list: HX.PropTypes.path,
//         labelBy: HX.PropTypes.field.optional,
//       }),
//     ])
//   ),
//   traces: HX.PropTypes.arrayOfType(
//     HX.PropTypes.objectOfType({
//       field: HX.PropTypes.field,
//       label: HX.PropTypes.string,
//       color: HX.PropTypes.string.optional,
//     })
//   ),
//   textInfo: HX.PropTypes.string.optional,

// }

// export function getMultiTraceCategoryNodes(props) {
//   return props.data.map((entry) => ({
//     traces: props.traces.map((trace) => ({
//       type: "static",
//       path: wrapWith(trace.field, wrapWith(entry.list || entry.structure, props.with)),
//     })),
//     label: entry.list
//       ? { type: "static", path: wrapWith(entry.list, wrapWith(entry.labelBy, props.with)) }
//       : { type: "static", path: wrapWith(entry.structure, props.with) },
//   }));
// }


// // export function getMultiTraceCategoryChartData(props, categoryNodes) {
// //   return props.traces.map((trace, traceIndex) => ({
// //     label: trace.label,
// //     color: trace.color,
// //     data: categoryNodes.map((entry, index) =>
// //       entry.type === "list"
// //         ? entry.elements.map((element) => element
// //           ? ({
// //             value: getNodeValue(element.nodes.traces[traceIndex]),
// //             label: getNodeValue(element.nodes.label)
// //           })
// //           : null
// //         ).filter(e => !!e)
// //         : [
// //           {
// //             value: getNodeValue(entry.traces[traceIndex]),
// //             label: getNodeValue(entry.label) ?? `index_${index}`
// //           }
// //         ]
// //     ).flat(),
// //   }))
// // }

// export function getMultiTraceCategoryChartData(props, categoryNodes) {
//   return props.traces.map((trace, traceIndex) => ({
//     label: trace.label,
//     color: trace.color,
//     data: categoryNodes.map((entry, index) => {
//       if (entry.type === "list") {
//         return entry.elements.map((element) => ({
//           value: getNodeValue(element.nodes.traces[traceIndex]),
//           label: getNodeValue(element.nodes.label),
//         })).filter(e => !!e);
//       } else {
//         return {
//           value: getNodeValue(entry.traces[traceIndex]),
//           label: getNodeValue(entry.label) ?? `index_${index}`,
//         };
//       }
//     }).flat(),
//   }));
// }


// const Bar = HX.buildCustomComponent({
//   apiVersion: "1.0.0",
//   propTypes: {
//     ...commonPropTypes,
//     ...multiTraceCategoryPropTypes,
//     xAxisTickAngle: HX.PropTypes.number.optional,
//     gapBetweenBarsSize: HX.PropTypes.number.optional,
//     barMode: HX.PropTypes.string.optional,
//     dynamicTitle: HX.PropTypes.path,
//     tpiLabelString: HX.PropTypes.path.optional,
//     bpiLabelString: HX.PropTypes.path.optional,
//   },
//   mapper: (props, tools) => {
//     return {
//       nodes: {
//         ...getCommonNodes(props),
//         barNodes: getMultiTraceCategoryNodes(props),
//         dynamicTitle: props.dynamicTitle
//           ? { type: "static", path: props.dynamicTitle }
//           : { type: "const", value: props.title || "Default Title" },  // Fallback to const with a default title
//         tpiLabelString: props.tpiLabelString
//           ? { type: "static", path: props.tpiLabelString }
//           : { type: "const", value: "" },  // Provide an empty string if not present
//         bpiLabelString: props.bpiLabelString
//           ? { type: "static", path: props.bpiLabelString }
//           : { type: "const", value: "" },  // Provide an empty string if not present
//       },
//     };
//   },
//   render: (props, data, tools) => {
//     const barData = getMultiTraceCategoryChartData(props, data.nodes.barNodes);
//     const customTickLabels = [
//       ` ${data.nodes.tpiLabelString.value}`,
//       ` ${data.nodes.bpiLabelString.value}`,
//       `Client`
//     ]
//     const xValues = barData[0]?.data.map((entry) => `${entry.label}`) || [];

//     return renderWithShownBy(
//       data.nodes.shownBy,

//       <Plot
//         data={barData.map(trace => ({
//           type: "bar",
//           x: trace.data.map(entry => `${entry.label}`),
//           y: trace.data.map(entry => entry.value),
//           name: trace.label,
//           marker: { color: trace.color },
//         }))}
//         layout={{
//           title: data.nodes.dynamicTitle?.value || props.title,  // Use dynamic title if available, otherwise static
//           xaxis: {
//             tickangle: props.xAxisTickAngle,
//             title: props.xAxisLabel,
//             tickvals: xValues, // Add tickvals to match the data points
//             ticktext: customTickLabels.length > 0 ? customTickLabels : xValues, // Custom labels corresponding to tickvals, Fallback to xValues if no custom labels
//           },
//           yaxis: {
//             title: props.yAxisLabel,
//           },
//           bargap: props.gapBetweenBarsSize,
//           barmode: props.barMode,
//           bargroupgap: 0.1,
//         }}
//       />
//     );
//   },
// });
// export default Bar;

import Plot from "react-plotly.js";
import * as HX from "hx-model-components";

import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
  wrapWith,
  getNodeValue
} from "../common/utilities";

export function getCategoryChartData(categoryNodes) {
  return categoryNodes.map((entry, index) => {
    if (entry.type === "list") {
      return entry.elements.map((element) => ({
        value: getNodeValue(element.nodes.value),
        label: getNodeValue(element.nodes.labelBy),
      })).filter(e => !!e);
    } else {
      return {
        value: getNodeValue(entry.value),
        label: getNodeValue(entry.label) ?? `index_${index}`,
      };
    }
  }).flat();
}

export const multiTraceCategoryPropTypes = {
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
  traces: HX.PropTypes.arrayOfType(
    HX.PropTypes.objectOfType({
      field: HX.PropTypes.field,
      label: HX.PropTypes.string,
      color: HX.PropTypes.string.optional,
    })
  ),
  textInfo: HX.PropTypes.string.optional,
};

export function getMultiTraceCategoryNodes(props) {
  return props.data.map((entry) => ({
    traces: props.traces.map((trace) => ({
      type: "static",
      path: wrapWith(trace.field, wrapWith(entry.list || entry.structure, props.with)),
    })),
    label: entry.list
      ? { type: "static", path: wrapWith(entry.list, wrapWith(entry.labelBy, props.with)) }
      : { type: "static", path: wrapWith(entry.structure, props.with) },
  }));
}

export function getMultiTraceCategoryChartData(props, categoryNodes) {
  return props.traces.map((trace, traceIndex) => ({
    label: trace.label,
    color: trace.color,
    data: categoryNodes.map((entry, index) => {
      if (entry.type === "list") {
        return entry.elements.map((element) => ({
          value: getNodeValue(element.nodes.traces[traceIndex]),
          label: getNodeValue(element.nodes.label),
        })).filter(e => !!e);
      } else {
        return {
          value: getNodeValue(entry.traces[traceIndex]),
          label: getNodeValue(entry.label) ?? `index_${index}`,
        };
      }
    }).flat(),
  }));
}

const CompoundBar = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    ...multiTraceCategoryPropTypes,
    xAxisTickAngle: HX.PropTypes.number.optional,
    gapBetweenBarsSize: HX.PropTypes.number.optional,
    barMode: HX.PropTypes.string.optional,
    dynamicTitle: HX.PropTypes.path,
    tpiLabelString: HX.PropTypes.path.optional,
    bpiLabelString: HX.PropTypes.path.optional,
  },
  mapper: (props, tools) => {
    return {
      nodes: {
        ...getCommonNodes(props),
        barNodes: getMultiTraceCategoryNodes(props),
        dynamicTitle: props.dynamicTitle
          ? { type: "static", path: props.dynamicTitle }
          : { type: "const", value: props.title || "Default Title" },  // Fallback to const with a default title
        tpiLabelString: props.tpiLabelString
          ? { type: "static", path: props.tpiLabelString }
          : { type: "const", value: "" },  // Provide an empty string if not present
        bpiLabelString: props.bpiLabelString
          ? { type: "static", path: props.bpiLabelString }
          : { type: "const", value: "" },  // Provide an empty string if not present
      },
    };
  },
  render: (props, data, tools) => {
    const barData = getMultiTraceCategoryChartData(props, data.nodes.barNodes);

    const customTickLabels = [
      ` ${data.nodes.tpiLabelString.value}`,
      ` ${data.nodes.bpiLabelString.value}`,
      `Client`
    ]

    const xValues = barData[0]?.data.map((entry) => `${entry.label}`) || [];

    return renderWithShownBy(
      data.nodes.shownBy,

      <Plot
        data={barData.map(trace => ({
          type: "bar",
          x: trace.data.map(entry => `${entry.label}`),
          y: trace.data.map(entry => entry.value),
          name: trace.label,
          marker: { color: trace.color },
          text: trace.data.map(entry => entry.value !== null && entry.value !== undefined && !isNaN(entry.value)
            ? (entry.value).toFixed(0)
            : ''  // Fallback for null, undefined, or invalid numbers
          ),  // Show values as text
          textposition: 'inside',  // Position text inside the bars
          insidetextanchor: 'middle',  // Center the text vertically within the bar
        }))}
        layout={{
          title: data.nodes.dynamicTitle?.value || props.title,  // Use dynamic title if available, otherwise static
          xaxis: {
            tickangle: props.xAxisTickAngle,
            title: props.xAxisLabel,
            tickvals: xValues, // Add tickvals to match the data points
            ticktext: customTickLabels.length > 0 ? customTickLabels : xValues, // Custom labels corresponding to tickvals, Fallback to xValues if no custom labels
          },
          yaxis: {
            title: props.yAxisLabel,
          },
          bargap: props.gapBetweenBarsSize,
          barmode: props.barMode,
          bargroupgap: 0.1,
        }}
      />
    );
  },
});

export default CompoundBar;
