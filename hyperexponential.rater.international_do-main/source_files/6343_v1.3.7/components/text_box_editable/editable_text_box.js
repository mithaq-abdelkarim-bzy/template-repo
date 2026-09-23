import * as HX from "hx-model-components";

const EditableText = HX.buildCustomComponent({
  apiVersion: "1.0.0",

  propTypes: {
    textNode: HX.PropTypes.path, // A path to a string node
    placeholderText: HX.PropTypes.string.optional,
    minHeight: HX.PropTypes.string.optional,
    maxHeight: HX.PropTypes.string.optional,
    width: HX.PropTypes.string.optional,
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

  render: (props, data, tools) => {
    const handleDownloadTxt = () => {
      // Strip HTML tags to get plain text
      const plainText = new DOMParser()
        .parseFromString(data.state.inputValue, "text/html")
        .body.textContent || "";

      const blob = new Blob([plainText], { type: "text/plain" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "editable_text.txt";
      link.click();
    };

    const handlePrint = () => {
      const printWindow = window.open('', '_blank');
      if (!printWindow) return;

      printWindow.document.write(`
        <html>
          <head>
            <title>Printable PDF</title>
            <style>
              body {
                font-family: inherit;
                font-size: 16px;
                padding: 40px;
                white-space: pre-wrap;
              }
            </style>
          </head>
          <body>
            ${data.state.inputValue}
          </body>
        </html>
      `);

      printWindow.document.close();
      printWindow.focus();
      printWindow.print();
    };

    return (
      <div style={{ marginLeft: "11px", marginRight: "11px" }}>
        <style>
          {`
            [data-placeholder]:empty::before {
              content: attr(data-placeholder);
              color: #999;
              font-style: italic;
            }
          `}
        </style>
        <div
          contentEditable
          suppressContentEditableWarning
          spellCheck={true}
          ref={(ref) => {
            if (ref && ref.innerHTML !== data.state.inputValue) {
              ref.innerHTML = data.state.inputValue;
            }
          }}
          onInput={(e) =>
            data.setState({ inputValue: e.currentTarget.innerHTML })
          }
          onBlur={() =>
            tools.sendTransaction([
              {
                type: "UPDATE_VALUES",
                updates: {
                  [data.nodes.text.nodeId]: data.state.inputValue,
                },
              },
            ])
          }
          data-placeholder={props.placeholderText || ""}
          style={{
            minHeight: props.minHeight ?? 120,
            maxHeight: props.maxHeight ?? 600,
            width: props.width ?? undefined,
            border: "1px solid #ccc",
            borderRadius: "4px",
            padding: "8px",
            fontSize: "16px",
            fontFamily: "inherit",
            overflowY: "auto",
            resize: "vertical",
            whiteSpace: "pre-wrap",
          }}
        />
      </div>
    );
  },
});

const buttonStyle = {
  padding: "8px 16px",
  fontSize: "14px",
  borderRadius: "4px",
  border: "1px solid #ccc",
  backgroundColor: "#0E124F",
  color: "white",
  cursor: "pointer",
};

export default EditableText;
