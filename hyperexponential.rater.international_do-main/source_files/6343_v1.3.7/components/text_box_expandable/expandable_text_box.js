import * as HX from "hx-model-components";

const HTML_TAG_REGEX = /<[A-Za-z][^>]*>/;
const AUTOSAVE_DEBOUNCE_MS = 750;

const NormalizeNodeValue = (value) => {
  if (value == null || value === "") {
    return "";
  }

  if (HTML_TAG_REGEX.test(value)) {
    return value;
  }

  return value.replace(/(\r\n|\n|\r)/g, "<br>");
};

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
      originalValue: "",
      isExpanded: false,
    },
  }),

  getDerivedStateFromData: (data, previousData) => {
    const rawNodeValue = data.nodes.text.value ?? "";
    const normalizedValue = NormalizeNodeValue(rawNodeValue);

    if (previousData === undefined || data.state.inputValue === undefined) {
      return {
        ...data.state,
        inputValue: normalizedValue,
        originalValue: normalizedValue,
      };
    }

    const previousRawValue = previousData.nodes.text.value ?? "";
    if (rawNodeValue !== previousRawValue && !data.state.isExpanded) {
      return {
        ...data.state,
        inputValue: normalizedValue,
        originalValue: normalizedValue,
      };
    }

    return data.state;
  },

  render: (props, data, tools) => {
    tools.lifecycle = tools.lifecycle ?? {};
    const lifecycle = tools.lifecycle;
    const editorRef = { current: null };

    const ClearAutoSave = () => {
      if (lifecycle.autosaveTimeout) {
        clearTimeout(lifecycle.autosaveTimeout);
        lifecycle.autosaveTimeout = null;
      }
      lifecycle.pendingValue = undefined;
    };

    const SaveValue = (updatedText) => {
      const currentValue = data.nodes.text.value ?? "";
      if (updatedText === currentValue) {
        return;
      }

      tools.sendTransaction([
        {
          type: "UPDATE_VALUES",
          updates: {
            [data.nodes.text.nodeId]: updatedText,
          },
        },
      ]);
    };

    const FlushPendingValue = (explicitValue) => {
      const pendingValue = lifecycle.pendingValue;
      const editorValue =
        explicitValue ??
        pendingValue ??
        (editorRef.current ? editorRef.current.innerHTML ?? "" : data.state.inputValue ?? "");

      ClearAutoSave();

      if (editorValue === undefined) {
        return;
      }

      SaveValue(editorValue);
    };

    const ScheduleAutoSave = (updatedText) => {
      if (lifecycle.autosaveTimeout) {
        clearTimeout(lifecycle.autosaveTimeout);
      }
      lifecycle.pendingValue = updatedText;
      lifecycle.autosaveTimeout = setTimeout(() => {
        lifecycle.autosaveTimeout = null;
        FlushPendingValue();
      }, AUTOSAVE_DEBOUNCE_MS);
    };

    const normalizePastedHtml = (rootEl) => {
      Array.from(rootEl.querySelectorAll("p")).forEach((p) => {
        p.style.margin = "0";
      });
      Array.from(rootEl.querySelectorAll("div")).forEach((d) => {
        d.style.margin = "0";
      });

      Array.from(rootEl.querySelectorAll("td")).forEach((cell) => {
        const lines = [];
        for (const child of Array.from(cell.childNodes)) {
          if (
            child.nodeType === Node.ELEMENT_NODE &&
            ["DIV", "P"].includes(child.nodeName)
          ) {
            child.style && (child.style.margin = "0");
            lines.push(child.innerHTML.trim());
          } else if (child.nodeType === Node.TEXT_NODE) {
            const text = (child.textContent || "").trim();
            if (text) lines.push(text);
          }
        }
        if (lines.length > 0) {
          cell.innerHTML = lines.join("<br>");
        }
      });

      Array.from(rootEl.querySelectorAll("p")).forEach((p) => {
        const text = (p.textContent || "").trim();

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
        } else if (/^\d+[.)]\s+/.test(text)) {
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

      Array.from(rootEl.querySelectorAll("p,div")).forEach((el) => {
        el.style.margin = "0";
      });
    };

    const handlePaste = (e) => {
      const clipboardData = e.clipboardData || window.clipboardData;
      if (!clipboardData) return;

      const htmlData = clipboardData.getData("text/html");
      const textData = clipboardData.getData("text/plain");

      if (htmlData) {
        const tmp = document.createElement("div");
        tmp.innerHTML = htmlData;

        normalizePastedHtml(tmp);

        e.preventDefault();
        document.execCommand("insertHTML", false, tmp.innerHTML);
        return;
      }

      if (textData) {
        e.preventDefault();
        document.execCommand("insertText", false, textData);
      }
    };

    const handleInput = (event) => {
      const updatedText = event.currentTarget.innerHTML ?? "";
      data.setState({
        ...data.state,
        inputValue: updatedText,
      });
      ScheduleAutoSave(updatedText);
    };

    const handleBlur = (event) => {
      const updatedText = event.currentTarget.innerHTML ?? "";
      FlushPendingValue(updatedText);
    };

    const handleOk = () => {
      const updatedText =
        (editorRef.current && editorRef.current.innerHTML) || "";
      FlushPendingValue(updatedText);
      data.setState({
        inputValue: updatedText,
        originalValue: updatedText,
        isExpanded: false,
      });
    };

    const handleCancel = () => {
      ClearAutoSave();
      const originalValue = data.state.originalValue ?? "";
      if (editorRef.current) {
        editorRef.current.innerHTML = originalValue;
      }
      data.setState({
        inputValue: originalValue,
        originalValue,
        isExpanded: false,
      });
      SaveValue(originalValue);
    };

    const normalizedCurrentValue = NormalizeNodeValue(
      data.nodes.text.value ?? ""
    );

    if (!data.state.isExpanded) {
      return (
        <button
          onClick={() => {
            ClearAutoSave();
            data.setState({
              inputValue: normalizedCurrentValue,
              originalValue: normalizedCurrentValue,
              isExpanded: true,
            });
          }}
          style={buttonStyle}
        >
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
          onInput={handleInput}
          onBlur={handleBlur}
          ref={(ref) => {
            editorRef.current = ref;
            if (ref && document.activeElement !== ref && ref.innerHTML !== data.state.inputValue) {
              ref.innerHTML = data.state.inputValue ?? "";
            }

            if (ref) {
              Array.from(ref.querySelectorAll("p,div")).forEach((el) => {
                el.style.margin = "0";
              });
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
            lineHeight: "1.35",
          }}
        />
        <div style={{ marginTop: "10px", display: "flex", gap: "10px" }}>
          <button onClick={handleOk} style={buttonStyle}>
            OK
          </button>
          <button onClick={handleCancel} style={buttonStyle}>
            Cancel
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
};

export default ExpandableEditableText;
