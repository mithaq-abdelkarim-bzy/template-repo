import * as HX from "hx-model-components";
import Plot from "react-plotly.js";
import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
  wrapWith,
} from "../common/utilities";

const CollapsibleSchemaViewer = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    ...commonPropTypes,
    stringifiedJsonPath: HX.PropTypes.path.optional,
  },

  mapper: (props) => ({
    nodes: {
      ...getCommonNodes(props),
      stringifiedJsonPath: { type: "static", path: wrapWith(props.stringifiedJsonPath, props.with) },
      shownBy: props.shownBy
        ? { type: "static", path: wrapWith(props.shownBy, props.with) }
        : { type: "const", value: true },
    },
    state: {
      isOpen: false, // Initial type
    }
  }),

  render: (props, data, tools) => {
    // Extract the stringified JSON value from the provided data object
    const stringifiedValue = data.nodes.stringifiedJsonPath?.value;

    // Parse the JSON string into an object or default to an empty object if undefined
    const jsonObject = stringifiedValue ? JSON.parse(stringifiedValue) : {};

    // Helper function to dynamically initialize the `isOpen` state based on JSON structure
    const initializeState = (json, parentKey = "") => {
      const state = {};
      if (typeof json === "object" && json !== null) {
        // Iterate over each key in the JSON object
        Object.keys(json).forEach((key) => {
          const sectionKey = parentKey ? `${parentKey}.${key}` : key; // Create a unique key for nested objects
          state[sectionKey] = false; // Initialize the isOpen state for this key as false (collapsed)

          // Recursively initialize the state for nested objects
          if (typeof json[key] === "object" && json[key] !== null) {
            Object.assign(state, initializeState(json[key], sectionKey));
          }
        });
      }
      return state;
    };

    // Ensure the `data.state.isOpen` is initialized only if it hasn't been set already
    if (!data.state.isOpen) {
      data.state.isOpen = initializeState(jsonObject);
    }

    // Function to render the JSON recursively as collapsible sections
    const renderJSON = (json, parentKey = "") => {
      if (typeof json !== "object" || json === null) {
        // Directly render primitive values
        return <span>{JSON.stringify(json)}</span>;
      }

      // Render each key-value pair in the object as collapsible sections
      return (
        <div>
          {Object.entries(json).map(([key, value], index) => (
            <CollapsibleKey
              key={index}
              keyName={key}
              value={value}
              parentKey={parentKey} // Pass the parent key for nested structure
            />
          ))}
        </div>
      );
    };

    // Updated CollapsibleKey Component
    const CollapsibleKey = ({ keyName, value, parentKey }) => {
      // Generate a unique key for this section based on the parent key
      const sectionKey = parentKey ? `${parentKey}.${keyName}` : keyName;

      // Toggle the open/close state of this section
      const toggleOpen = () => {
        data.setState({
          ...data.state,
          isOpen: {
            ...data.state.isOpen,
            [sectionKey]: !data.state.isOpen[sectionKey], // Flip the current isOpen state
          },
        });
      };

      // Determine if this section is currently open
      const isOpen = data.state.isOpen[sectionKey];

      // Arrow to indicate open/close state (only for non-primitive types)
      const arrow = isOpen ? "▼" : "▶";

      return (
        <div style={{ marginLeft: "10px" }}>
          <div
            style={{
              cursor: typeof value === "object" && value !== null ? "pointer" : "default", // Pointer only for collapsible items
              userSelect: "none", // Prevents text selection on click
              display: "flex",
              alignItems: "center",
            }}
            onClick={typeof value === "object" && value !== null ? toggleOpen : undefined} // Toggle only for non-primitives
          >
            {/* Add a larger bullet for primitive types */}
            {typeof value !== "object" || value === null ? (
              <span
                style={{
                  marginRight: "5px",
                  color: "#000",
                  fontSize: "28px", // Match the size of the arrow
                  lineHeight: "16px", // Ensure alignment with text
                }}
              >
                ●
              </span>
            ) : (
              // Render arrow for non-primitives
              <span style={{ marginRight: "5px", color: "#0E124F" }}>{arrow}</span>
            )}
            <span style={{ color: "#326B9F" }}>{keyName}</span>
            {typeof value !== "object" || value === null ? (
              <span style={{ color: "#000" }}>: {JSON.stringify(value)}</span>
            ) : null}
          </div>
          {typeof value === "object" && value !== null && isOpen && (
            <div style={{ marginLeft: "20px" }}>
              {renderJSON(value, sectionKey)} {/* Recursively render nested objects */}
            </div>
          )}
        </div>
      );
    };

    // Function to download HTML
    // Function to download HTML
    const downloadJSON = () => {
      // Convert JSON object to a plain string with indentation
      const jsonContent = JSON.stringify(jsonObject, null, 2);

      // Create a Blob object for the plain JSON content
      const blob = new Blob([jsonContent], { type: "application/json" });

      // Generate a download link
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "data.json"; // File name for the downloaded file

      // Trigger the download
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    return (
      <div
        style={{
          border: "1px solid #0E124F", // Outer border for the viewer
          borderRadius: "8px", // Rounded corners
          padding: "15px", // Internal spacing
          margin: "20px 0", // Spacing around the viewer
          backgroundColor: "#F9F9F9", // Light background color
        }}
      >
        {renderWithShownBy(data.nodes.shownBy, renderJSON(jsonObject))}
        <button
          onClick={downloadJSON}
          style={{
            marginTop: "20px",
            padding: "10px 20px",
            fontSize: "16px",
            backgroundColor: "#0E124F",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Download JSON
        </button>
      </div>
    );

  }
});

export default CollapsibleSchemaViewer;
