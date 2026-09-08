import * as HX from "hx-model-components";

// 'with' prop that is implemented on existing HX components
export const wrapWith = (path, withProp) =>
  !path
    ? path
    : withProp && !path.startsWith("/")
      ? withProp + "/" + path
      : path;

// There are common PropTypes that exist on both 'XY' charts and 'Category' charts.
// To stop the duplication of code, we define them here, and then into them into the 'xy.js' and 'category.js' common files.
export const commonPropTypes = {
  title: HX.PropTypes.string,
  with: HX.PropTypes.path.optional,
  shownBy: HX.PropTypes.path.optional,
  xAxisLabel: HX.PropTypes.string.optional,
  yAxisLabel: HX.PropTypes.string.optional,
};

export const getCommonNodes = (props) => ({
  shownBy: props.shownBy
    ? { type: "static", path: props.shownBy }
    : { type: "const", value: true },
});

export const getNodeValue = (node) =>
  node.value && typeof node.value === "object" && "is_overridden" in node.value
    ? node.value.is_overridden
      ? node.value.override
      : node.value.calculated
    : node.value;

export const renderWithShownBy = (shownBy, content) =>
  getNodeValue(shownBy) ? content : null;