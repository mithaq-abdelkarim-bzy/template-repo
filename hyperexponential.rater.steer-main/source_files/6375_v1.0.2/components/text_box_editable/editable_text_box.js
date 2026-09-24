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
            const w = window.open("", "_blank");
            if (!w) return;

            const doc = w.document;
            doc.write(`
        <html>
          <head>
            <meta charset="utf-8" />
            <title>Printable PDF</title>
            <style>
              @page { margin: 16mm; }
              body {
                font-family: "Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
                font-size: 16px;
                padding: 40px;
                white-space: pre-wrap;
                color: #111;
              }
              img { max-width: 100%; height: auto; }
              a { color: #111; text-decoration: underline; }
            </style>
          </head>
          <body>
            ${data.state.inputValue}
          </body>
        </html>
      `);
            doc.close();

            // Ensure Acid Grotesk @font-face is available in the new window
            try {
                const base = doc.createElement("base");
                base.href = document.baseURI;
                doc.head.appendChild(base);
                document
                    .querySelectorAll('link[rel="stylesheet"], style')
                    .forEach((el) => doc.head.appendChild(el.cloneNode(true)));
            } catch (_) { }

            w.focus();
            w.print();
        };

        return (
            <div
                style={{
                    marginLeft: "11px",
                    marginRight: "11px",
                    fontFamily:
                        '"Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
                }}
            >
                <style>
                    {`
            [data-placeholder]:empty::before {
              content: attr(data-placeholder);
              color: #999;
              font-style: italic;
              font-family: "Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
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
                        fontFamily:
                            '"Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
                        overflowY: "auto",
                        resize: "vertical",
                        whiteSpace: "pre-wrap",
                    }}
                />
                <div style={{ marginTop: "10px", display: "flex", gap: "10px" }}>
                    {/* <button onClick={handleDownloadTxt} style={buttonStyle}>Download as .txt</button> */}
                    <button
                        onClick={handlePrint}
                        style={buttonStyle}
                    >
                        Print / Save as PDF
                    </button>
                </div>
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
    fontFamily:
        '"Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
};

export default EditableText;
