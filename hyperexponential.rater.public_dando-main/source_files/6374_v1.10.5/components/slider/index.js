import * as HX from "hx-model-components";

const BaseStructure = HX.buildCustomComponent({

  /* 
  This component shows the minimal work required to display:
  - A prop with a constant value
  - A prop that paths to a single node
  - Data from a list
  */

  apiVersion: "1.0.0",
  propTypes: {
    // Define the arguments that are to be passed into the component

    // Constant node
    // A static string value
    "title": HX.PropTypes.string,

    // Structure Node
    // A string value that is a path to a leaf node 
    "field": HX.PropTypes.path,

    // List Node
    // A string value that is a path to a list node 
    // "myListNode": HX.PropTypes.path,
    // // An array of child nodes within the list
    // "myListFields": HX.PropTypes.arrayOfType(HX.PropTypes.field)

  },
  mapper: (props) => ({
    nodes: {
      // Type "const" will take the actual value passed to the component
      constant: { type: "const", value: props.title },

      // Type "static" will take the value from the path passed to the component 
      field: { type: "static", path: props.field },

      // Type "list" will take the data from the last node and the child nodes that are passed to the list
      // list: {
      //   type: "list",
      //   path: props.myListNode,
      //   nodes: props.myListFields.map((elt) => ({ type: "static", path: elt }))
      // }
    },
    state: {
      currentVal: 0
    }
  }),
  getDerivedStateFromData: (data, previousData) => {
    return data.state;
  },
  render: (props, data, tools) => {
    // Inspect the console to see the data format you are working with
    tools.log("Sample log")
    tools.log(data)

    let currentVal = data.state.currentVal

    return (
      // Display the data on the screen
      <div>
        <input
          type="range"
          min="0"
          max="100"
          // name={data.nodes.title}
          value={currentVal}
          onChange={(e) =>
            data.setState({
              ...data.state,
              currentVal: parseInt(e.target.value),
            })
          }
          onClick={() => tools.sendTransaction([
            {
              type: "UPDATE_VALUES",
              updates: {
                // this is JS shorthand for assigning a key-value pair into an object
                [data.nodes.field.nodeId]: currentVal
              }
            }
          ])}
          style={{
            flexGrow: "1", // Allow the slider to fill remaining space
            appearance: "none",
            height: "8px",
            backgroundColor: "#ddd",
            borderRadius: "5px",
            outline: "none",
            color: "#FF1493",
            marginRight: "10px", // Space between slider and button
          }}
        />
      </div>
    );
  },
});

export default BaseStructure;
