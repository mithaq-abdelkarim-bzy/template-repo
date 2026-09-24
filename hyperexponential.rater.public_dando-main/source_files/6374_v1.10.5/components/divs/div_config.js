import * as HX from "hx-model-components";

const DivConfig = HX.buildCustomComponent({
  apiVersion: "1.0.0",

  propTypes: {
    textNode: HX.PropTypes.path, // A path to a string node
    minHeight: HX.PropTypes.string.optional,
    maxHeight: HX.PropTypes.string.optional,
    minWidth: HX.PropTypes.string.optional,
    maxWidth: HX.PropTypes.string.optional,
    width: HX.PropTypes.string.optional,
    marginTop: HX.PropTypes.string.optional,
    marginBottom: HX.PropTypes.string.optional,
    marginLeft: HX.PropTypes.string.optional,
    marginRight: HX.PropTypes.string.optional,
  },

  mapper: (props) => ({
    nodes: {
      text: { type: "static", path: props.textNode },
    },
    state: {
      inputValue: "", // Local editable value
    },
  }),


  getDerivedStateFromData: (data, previousData) => {
    if (data.nodes.text.value !== previousData?.nodes.text.value) {
      return { inputValue: data.nodes.text.value };
    }
    return data.state;
  },

  render: (props) => {
    return (
      <div
        style={{
          //display: "inline-block", // Auto-fits content
          minHeight: props.minHeight ?? "auto",
          maxHeight: props.maxHeight ?? "none",
          minWidth: props.minWidth ?? "auto",
          maxWidth: props.maxWidth ?? "none",
          width: props.width ?? "fit-content", // Makes the div size adjust to its content
          marginTop: props.marginTop ?? "0px",
          marginBottom: props.marginBottom ?? "0px",
          marginLeft: props.marginLeft ?? "0px",
          marginRight: props.marginRight ?? "0px"
        }}
      >
        {props.children}
      </div>
    );
  }
});

export default DivConfig;