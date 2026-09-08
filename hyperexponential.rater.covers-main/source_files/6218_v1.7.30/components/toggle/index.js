
import * as HX from "hx-model-components";
import {
  getCommonNodes,
  renderWithShownBy,
} from "../common/utilities";
import { outerDiv, captionClass, outerSwitch, switchOn, switchOff, inputClass, switchThumbOn, switchThumbOff, touchRipple, trackOn, trackOff } from "./styles.js"


const SimpleToggle = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    falseLabel: HX.PropTypes.string.optional,
    trueLabel: HX.PropTypes.string.optional,
    boolNode: HX.PropTypes.path,
    shownBy: HX.PropTypes.path.optional
  },
  mapper: (props) => ({
    nodes: {
      ...getCommonNodes(props),
      boolNode: { type: "static", path: props.boolNode }
    }
  }),
  render: (props, data, tools) => {
    return renderWithShownBy(
      data.nodes.shownBy,
      <div style={outerDiv}>
        <span style={captionClass}>{props.falseLabel ?? "False"}</span>
        <span style={outerSwitch}>
          <span style={data.nodes.boolNode.value ? switchOn : switchOff}>
            <input style={inputClass} tabindex="-1" type="checkbox"
              onChange={() => tools.sendTransaction([
                {
                  type: "UPDATE_VALUES",
                  updates: { [data.nodes.boolNode.nodeId]: !data.nodes.boolNode.value }
                }
              ])}
            />
            <span style={data.nodes.boolNode.value ? switchThumbOn : switchThumbOff}></span>
            <span style={touchRipple}></span>
          </span>
          <span style={data.nodes.boolNode.value ? trackOn : trackOff}></span>
        </span>
        <span style={captionClass}>{props.trueLabel ?? "True"}</span>
      </div>
    );
  },
});
export default SimpleToggle;

