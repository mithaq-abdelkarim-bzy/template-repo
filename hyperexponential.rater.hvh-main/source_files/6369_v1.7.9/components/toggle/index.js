import * as HX from "hx-model-components";
import { wrapWith, renderWithShownBy, getNodeValue } from "../common/utilities.js";
import styles from "../toggle/styles.js"

/*
  SimpleToggle
  -------------
  A minimal Boolean toggle switch.

  Props
  - boolNode (path): Path to the Boolean node which the switch controls.
  - shownBy (optional, path): Boolean node controlling visibility of the component.
  - with (optional, path): Common prefix path applied to all node paths.
  - label (optional, string): Static text label. Used when `labelBy` is not provided.
  - labelBy (optional, path): Path to a node providing the label text dynamically.

  Example Usage:
  <SimpleToggle bool="bool_node" label="Show Results"/>

  Possible future developments:
  - Improvements to styling (e.g. multiple labels, container sizing and placement).

*/

const SimpleToggle = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    boolNode: HX.PropTypes.path,
    shownBy: HX.PropTypes.path.optional,
    with: HX.PropTypes.path.optional,
    label: HX.PropTypes.string.optional,
    labelBy: HX.PropTypes.path.optional,
  },
  mapper: (props, tools) => ({
    nodes: {
      bool: { type: "static", path: wrapWith(props.boolNode, props.with) },
      label: props.labelBy
        ? { type: "static", path: wrapWith(props.labelBy, props.with) }
        : { type: "const", value: props.label ?? "Label Me!" },
      shownBy: props.shownBy
        ? { type: "static", path: wrapWith(props.shownBy, props.with) }
        : { type: "const", value: true },
    },
    state: {}
  }),

  render: (props, data, tools) => {
    const currentValue = data?.nodes?.bool?.value;
    const nodeId = data?.nodes?.bool?.nodeId;

    const onClickHandler = () => {
      tools.sendTransaction([
        { type: "UPDATE_VALUES", updates: { [nodeId]: !currentValue } }
      ]);
    };

    return (
      renderWithShownBy(
        data.nodes.shownBy,
        <div style={styles.container}>
          <span style={styles.label}>{getNodeValue(data.nodes.label)}</span>
          <label style={styles.outerSwitch}>
            <input type="checkbox" onChange={onClickHandler} style={styles.input} />
            <span style={currentValue ? styles.trackOn : styles.trackOff}>
              <span style={currentValue ? styles.knobOn : styles.knobOff} />
            </span>
          </label>
        </div>
      )
    );
  }
});

export default SimpleToggle;