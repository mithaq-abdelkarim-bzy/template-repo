import * as HX from "hx-model-components";
import { wrapWith, getNodeValue } from "./utilities";

export const categoryPropTypes = {
  // Depending on whether List or Structure nodes have been provided, the required objectOfType of the node will be different
  data: HX.PropTypes.arrayOfType(
    HX.PropTypes.oneOfType([
      HX.PropTypes.objectOfType({
        value: HX.PropTypes.path,
        label: HX.PropTypes.string.optional,
        labelBy: HX.PropTypes.path.optional,
      }),
      HX.PropTypes.objectOfType({
        list: HX.PropTypes.path,
        value: HX.PropTypes.field,
        labelBy: HX.PropTypes.field.optional,
      }),
    ])
  ),
  textInfo: HX.PropTypes.string.optional,
};

export function getCategoryNodes(props) {
  return props.data.map((entry) =>
    entry.list
      ? {
        type: "list",
        path: wrapWith(entry.list, props.with),
        nodes: {
          value: { type: "static", path: entry.value },
          label: { type: "static", path: entry.labelBy },
        },
      }
      : {
        value: { type: "static", path: wrapWith(entry.value, props.with) },
        label: entry.labelBy
          ? { type: "static", path: wrapWith(entry.labelBy, props.with) }
          : { type: "const", value: entry.label },
      }
  );
}

export function getCategoryChartData(categoryNodes) {
  return categoryNodes
    .map((entry, index) =>
      entry.type === "list"
        ? entry.elements.map(
          (element) => element
            ? ({
              value: getNodeValue(element?.nodes.value),
              label: getNodeValue(element?.nodes.label),
            })
            : null
        ).filter(e => !!e)
        : [
          {
            value: getNodeValue(entry.value),
            label:
              getNodeValue(entry.label) ??
              entry.value.metadata.view?.label ??
              `index_${index}`,
          },
        ]
    )
    .flat();
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
    })
  ),
  textInfo: HX.PropTypes.string.optional,
}

export function getMultiTraceCategoryNodes(props) {
  return props.data.map((entry) =>
    entry.list
      ? {
        type: "list",
        path: wrapWith(entry.list, props.with),
        nodes: {
          traces: props.traces.map(trace => ({
            type: "static",
            path: trace.field,
          })),
          label: { type: "static", path: entry.labelBy },
        }
      }
      : {
        traces: props.traces.map(trace => ({
          type: "static",
          path: wrapWith(trace.field, wrapWith(entry.structure, props.with)),
        })),
        label: entry.labelBy
          ? { type: "static", path: wrapWith(entry.labelBy, wrapWith(entry.structure, props.with)) }
          : { type: "const", value: entry.label },
      }
  )
}

export function getMultiTraceCategoryChartData(props, categoryNodes) {
  return props.traces.map((trace, traceIndex) => ({
    label: trace.label,
    data: categoryNodes.map((entry, index) =>
      entry.type === "list"
        ? entry.elements.map((element) => element
          ? ({
            value: getNodeValue(element.nodes.traces[traceIndex]),
            label: getNodeValue(element.nodes.label)
          })
          : null
        ).filter(e => !!e)
        : [
          {
            value: getNodeValue(entry.traces[traceIndex]),
            label: getNodeValue(entry.label) ?? `index_${index}`
          }
        ]
    ).flat(),
  }))
}