import * as HX from "hx-model-components";

const EditableText = HX.buildCustomComponent({
  apiVersion: "1.0.0",

  propTypes: {
    textNode: HX.PropTypes.path,
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
      inputValue: "",
    },
  }),

  getDerivedStateFromData: (data, previousData) => {
    if (data.nodes.text.value !== previousData?.nodes.text.value) {
      return { inputValue: data.nodes.text.value };
    }
    return data.state;
  },

  render: (props, data, tools) => {
    const toPngDataUrl = async (fileOrBlob) => {
      const blob = fileOrBlob instanceof Blob ? fileOrBlob : new Blob([fileOrBlob]);
      const type = (blob.type || "").toLowerCase();
      const asDataURL = (b) =>
        new Promise((resolve, reject) => {
          const fr = new FileReader();
          fr.onload = () => resolve(fr.result);
          fr.onerror = reject;
          fr.readAsDataURL(b);
        });

      const needsCanvas =
        type.includes("svg") || type.includes("webp") || type.includes("avif");

      if (!needsCanvas && (type.includes("png") || type.includes("jpeg") || type.includes("jpg") || type.includes("gif") || type.includes("bmp"))) {
        return await asDataURL(blob);
      }

      const imgUrl = URL.createObjectURL(blob);
      try {
        const img = await new Promise((resolve, reject) => {
          const im = new Image();
          im.onload = () => resolve(im);
          im.onerror = reject;
          im.crossOrigin = "anonymous";
          im.src = imgUrl;
        });

        const w = img.naturalWidth || img.width || 800;
        const h = img.naturalHeight || img.height || 600;

        const canvas = document.createElement("canvas");
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        const dataUrl = canvas.toDataURL("image/png");
        return dataUrl;
      } finally {
        URL.revokeObjectURL(imgUrl);
      }
    };

    const insertImageAtCaret = async (editorEl, fileOrBlob) => {
      const dataUrl = await toPngDataUrl(fileOrBlob);
      const img = document.createElement("img");
      img.src = dataUrl;
      img.style.maxWidth = "100%";
      img.style.height = "auto";

      const sel = window.getSelection();
      if (sel && sel.rangeCount > 0) {
        const range = sel.getRangeAt(0);
        range.deleteContents();
        range.insertNode(img);
        range.setStartAfter(img);
        range.collapse(true);
        sel.removeAllRanges();
        sel.addRange(range);
      } else {
        editorEl.appendChild(img);
      }
    };

    const handlePaste = async (e) => {
      const editorEl = e.currentTarget;

      const items = e.clipboardData?.items || [];
      const imageItems = Array.from(items).filter((it) => it.kind === "file" && it.type.startsWith("image/"));
      if (imageItems.length > 0) {
        e.preventDefault();
        for (const it of imageItems) {
          const file = it.getAsFile();
          if (file) {
            await insertImageAtCaret(editorEl, file);
          }
        }
        data.setState({ inputValue: editorEl.innerHTML });
        return;
      }

      setTimeout(async () => {
        const imgs = Array.from(editorEl.querySelectorAll("img"));
        let changed = false;
        for (const img of imgs) {
          const src = img.getAttribute("src") || "";
          if (src.startsWith("blob:") || src.startsWith("http://") || src.startsWith("https://")) {
            try {
              const resp = await fetch(src);
              const blob = await resp.blob();
              const dataUrl = await toPngDataUrl(blob);
              img.setAttribute("src", dataUrl);
              changed = true;
            } catch {
              //
            }
          }
        }
        if (changed) {
          data.setState({ inputValue: editorEl.innerHTML });
        }
      }, 0);
    };

    const handleDrop = async (e) => {
      const editorEl = e.currentTarget;
      const files = Array.from(e.dataTransfer?.files || []);
      const imageFiles = files.filter((f) => f.type.startsWith("image/"));
      if (imageFiles.length === 0) return;
      e.preventDefault();
      for (const f of imageFiles) {
        await insertImageAtCaret(editorEl, f);
      }
      data.setState({ inputValue: editorEl.innerHTML });
    };

    const normalizeImagesBeforeSave = async (editorEl) => {
      const imgs = Array.from(editorEl.querySelectorAll("img"));
      let changed = false;
      for (const img of imgs) {
        const src = img.getAttribute("src") || "";
        if (src.startsWith("data:image/")) continue;
        try {
          const resp = await fetch(src);
          const blob = await resp.blob();
          const dataUrl = await toPngDataUrl(blob);
          img.setAttribute("src", dataUrl);
          changed = true;
        } catch {
          //
        }
      }
      if (changed) {
        data.setState({ inputValue: editorEl.innerHTML });
      }
    };

    let editorRef = null;

    return (
      <div style={{ marginLeft: "11px", marginRight: "11px" }}>
        <style>
          {`
            [data-placeholder]:empty::before {
              content: attr(data-placeholder);
              color: #999;
              font-style: italic;
            }
            [contenteditable] img { max-width: 100%; height: auto; }
          `}
        </style>
        <div
          contentEditable
          suppressContentEditableWarning
          spellCheck={true}
          ref={(ref) => {
            editorRef = ref;
            if (ref && ref.innerHTML !== data.state.inputValue) {
              ref.innerHTML = data.state.inputValue;
            }
          }}
          onPaste={handlePaste}
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          onInput={(e) => data.setState({ inputValue: e.currentTarget.innerHTML })}
          onBlur={async () => {
            if (editorRef) {
              await normalizeImagesBeforeSave(editorRef);
              tools.sendTransaction([
                {
                  type: "UPDATE_VALUES",
                  updates: {
                    [data.nodes.text.nodeId]: editorRef.innerHTML,
                  },
                },
              ]);
            }
          }}
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
        <div style={{ marginTop: "10px", display: "flex", gap: "10px" }}>
          <button
            onClick={() => {
              const w = window.open("", "_blank");
              if (!w) return;
              w.document.write(`<html><body>${data.state.inputValue}</body></html>`);
              w.document.close();
              w.focus();
              w.print();
            }}
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
};

export default EditableText;
