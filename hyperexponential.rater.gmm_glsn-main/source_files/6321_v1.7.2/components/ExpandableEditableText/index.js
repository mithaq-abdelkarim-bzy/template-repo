import * as HX from "hx-model-components";

const ExpandableEditableText = HX.buildCustomComponent({
  apiVersion: "1.0.0",

  propTypes: {
    textNode: HX.PropTypes.path,
    label: HX.PropTypes.string.optional,
    minHeight: HX.PropTypes.string.optional,
    maxHeight: HX.PropTypes.string.optional,
    width: HX.PropTypes.string.optional,
  },

  mapper: (props) => ({
    nodes: {
      text: { type: "static", path: props.textNode },
    },
    state: {
      inputValue: "",
      isExpanded: false,
    },
  }),

  getDerivedStateFromData: (data, previousData) => {
    const nodeVal = data.nodes.text.value ?? "";
    if (
      data.state.inputValue === undefined ||
      previousData === undefined
    ) {
      return { ...data.state, inputValue: nodeVal };
    }
    if (nodeVal !== previousData.nodes.text.value) {
      return { ...data.state, inputValue: nodeVal };
    }
    return data.state;
  },

  render: (props, data, tools) => {
    const editorRef = { current: null };

    const handlePaste = (e) => {
      const clipboardData = e.clipboardData || window.clipboardData;
      if (!clipboardData) return;
      const htmlData = clipboardData.getData("text/html");
      const textData = clipboardData.getData("text/plain");

      if (htmlData) {
        const tmp = document.createElement("div");
        tmp.innerHTML = htmlData;

        Array.from(tmp.querySelectorAll("td")).forEach((cell) => {
          const lines = [];
          for (const child of Array.from(cell.childNodes)) {
            if (child.nodeType === Node.ELEMENT_NODE && ["DIV", "P"].includes(child.nodeName)) {
              lines.push(child.innerHTML.trim());
            } else if (child.nodeType === Node.TEXT_NODE) {
              const text = child.textContent.trim();
              if (text) lines.push(text);
            }
          }
          if (lines.length > 0) {
            cell.innerHTML = lines.join("<br>");
          }
        });

        Array.from(tmp.querySelectorAll("p")).forEach((p) => {
          const text = p.textContent.trim();

          if (/^[•·\-*]\s+/.test(text)) {
            const li = document.createElement("li");
            li.innerHTML = text.replace(/^[•·\-*]\s+/, "");
            let ul = p.previousElementSibling;
            if (!ul || ul.tagName !== "UL") {
              ul = document.createElement("ul");
              p.parentNode.insertBefore(ul, p);
            }
            ul.appendChild(li);
            p.remove();
          }

          else if (/^\d+[.)]\s+/.test(text)) {
            const li = document.createElement("li");
            li.innerHTML = text.replace(/^\d+[.)]\s+/, "");
            let ol = p.previousElementSibling;
            if (!ol || ol.tagName !== "OL") {
              ol = document.createElement("ol");
              p.parentNode.insertBefore(ol, p);
            }
            ol.appendChild(li);
            p.remove();
          }
        });

        e.preventDefault();
        document.execCommand("insertHTML", false, tmp.innerHTML);
        return;
      }

      if (textData) {
        e.preventDefault();
        document.execCommand("insertText", false, textData);
        return;
      }
    };

    const handleDownloadTxt = () => {
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
      const printWindow = window.open("", "_blank");
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
              }
              table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                padding: 4px;
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

    const handleOk = () => {
      const updatedText = editorRef.current?.innerHTML ?? "";
      tools.sendTransaction([
        {
          type: "UPDATE_VALUES",
          updates: {
            [data.nodes.text.nodeId]: updatedText,
          },
        },
      ]);
      data.setState({
        inputValue: updatedText,
        isExpanded: false,
      });
    };

    const handleCancel = () => {
      if (editorRef.current) {
        editorRef.current.innerHTML = data.state.inputValue;
      }
      data.setState({ isExpanded: false });
    };

    if (!data.state.isExpanded) {
      return (
        <button onClick={() => data.setState({ isExpanded: true })} style={buttonStyle}>
          {props.label ?? "Edit Text"}
        </button>
      );
    }

    return (
      <div>
        <div
          contentEditable
          suppressContentEditableWarning
          spellCheck={true}
          onPaste={handlePaste}
          ref={(ref) => {
            editorRef.current = ref;
            if (ref && ref.innerHTML !== data.state.inputValue) {
              ref.innerHTML = data.state.inputValue;
            }
          }}
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
          }}
        />
        <div style={{ marginTop: "10px", display: "flex", gap: "10px" }}>
          <button onClick={handleOk} style={buttonStyle}>OK</button>
          <button onClick={handleCancel} style={buttonStyle}>Cancel</button>
          <button onClick={handleDownloadTxt} style={buttonStyle}>Download as .txt</button>
          <button onClick={handlePrint} style={buttonStyle}>Print / Save as PDF</button>
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
};


export default ExpandableEditableText;

