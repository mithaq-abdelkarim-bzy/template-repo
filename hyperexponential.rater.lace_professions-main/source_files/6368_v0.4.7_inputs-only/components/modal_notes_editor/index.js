import * as HX from "hx-model-components";

const ModalNotesEditor = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    notesPath: HX.PropTypes.path.required,
    plainTextPath: HX.PropTypes.path.optional,
    printButton: HX.PropTypes.boolean.optional,
    label: HX.PropTypes.string.optional,
    width: HX.PropTypes.string.optional,
    marginTop: HX.PropTypes.string.optional,
    marginBottom: HX.PropTypes.string.optional,
    autosave: HX.PropTypes.boolean.optional,          // enable/disable autosave
    // NOTE: Avoid "input" while actively typing — it will fire a transaction
    // on every input event and can hit transaction limits. Prefer "keystrokes"
    // (default) or "blur" for typical usage.
    autosaveMode: HX.PropTypes.string.optional,       // "blur" | "input" | "keystrokes" (default "keystrokes")
    autosaveKeystrokes: HX.PropTypes.number.optional, // threshold for keystrokes mode (default 20)
  },
  mapper: (props) => ({
    nodes: {
      notes: { type: "static", path: props.notesPath },
      plainText: props.plainTextPath
        ? { type: "static", path: props.plainTextPath }
        : { type: "const", value: null },
    },
    state: { editingHtml: "" },
  }),
  getDerivedStateFromData: (data, prev) => {
    if (data.nodes.notes.value !== prev?.nodes?.notes?.value) {
      return { editingHtml: data.nodes.notes.value || "" };
    }
    return data.state;
  },
  render: (props, data, tools) => {
    tools.lifecycle = tools.lifecycle || {};
    const { editingHtml } = data.state;
    const htmlNodeId = data.nodes.notes.nodeId;
    const plainNodeId = data.nodes.plainText?.nodeId;
    const showPrint = !!props.printButton;
    const launchLabel =
      typeof props.label === "string" && props.label.trim() ? props.label : "Open Notes Editor";
    const ROOT = "modal-notes-editor-root";

    // Inject/overwrite styles (ensures old padding on container is removed)
    {
      const STYLE_ID = "modal-notes-editor-styles";
      let style = document.getElementById(STYLE_ID);
      if (!style) {
        style = document.createElement("style");
        style.id = STYLE_ID;
        document.head.appendChild(style);
      }
      style.textContent = `
        /* Container: no extra spacing */
        .${ROOT}.notes-editor-container { display: block; margin: 0 !important; padding: 0 !important; }

        /* Launcher button */
        .${ROOT} .notes-editor-button {
          padding: 8px 16px;
          font-size: 14px;
          border-radius: 4px;
          border: 1px solid #ccc;
          background-color: #0e124f;
          color: #fff;
          cursor: pointer;
          font-weight: 400; /* regular */
          font-family: "Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
          transition: background 0.2s, box-shadow 0.2s, transform 0.05s;
        }
        .${ROOT} .notes-editor-button:hover { background-color: #1a2080; }
        .${ROOT} .notes-editor-button:active { transform: translateY(1px); }
        .${ROOT} .notes-editor-button:focus-visible { outline: 2px solid #1a2080; outline-offset: 2px; }

        /* Overlay lets clicks through except the modal itself */
        .modal-overlay {
          position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
          background: transparent; z-index: 1000; pointer-events: none;
        }

        /* Modal root — Acid Grotesk everywhere inside */
        .modal-content {
          position: absolute; top: 15vh; left: 20vw; width: 60vw; height: 60vh;
          background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.3);
          display: flex; flex-direction: column; resize: both; overflow: auto; pointer-events: auto; z-index: 1001;
          font-family: "Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
        }

        .modal-toolbar {
          background: #fafafa; padding: 8px; user-select: none;
          display: flex; gap: 6px; border-bottom: 1px solid #ddd; align-items: center;
          cursor: move;
        }

        .modal-editor {
          flex: 1; padding: 16px; overflow: auto; white-space: pre-wrap;
          font-family: "Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
          font-size: 14px; color: #111;
        }

        /* ======= Shared button system (toolbar + confirms) ======= */
        .cuic-btn {
          appearance: none; -webkit-appearance: none;
          padding: 8px 12px; height: 32px;
          font-size: 13px; line-height: 1; font-weight: 500;
          border-radius: 8px; border: 1px solid #cfcfcf;
          background: #f8f8f8; color: #111;
          display: inline-flex; align-items: center; justify-content: center; gap: 6px;
          cursor: pointer;
          transition: background 120ms ease, border-color 120ms ease, box-shadow 120ms ease, transform 60ms ease, opacity 120ms ease;
          font-family: "Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
        }
        .cuic-btn:hover { background: #f1f1f1; }
        .cuic-btn:active { transform: translateY(1px); }
        .cuic-btn:focus-visible { outline: 2px solid #000; outline-offset: 2px; }
        .cuic-btn[disabled] { opacity: 0.55; cursor: not-allowed; }

        .cuic-btn-primary { background: #111; color: #fff; border-color: #111; }
        .cuic-btn-primary:hover { background: #000; }

        .cuic-btn-danger { background: #fff; color: #d32f2f; border-color: #d32f2f; }
        .cuic-btn-danger:hover { background: #fef2f2; }

        .cuic-btn-ghost { background: transparent; border-color: #ddd; }
        .cuic-btn-ghost:hover { background: #f6f6f6; }

        .cuic-btn-icon { width: 32px; padding: 0; }

        /* ======= Confirm overlay & card ======= */
        @keyframes cuicConfirmFade { from { opacity: 0; } to { opacity: 1; } }
        @keyframes cuicConfirmPop  { from { opacity: 0; transform: translateY(4px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }

        .confirm-overlay {
          position: absolute; inset: 0;
          background: rgba(0,0,0,0.25);
          display: flex; align-items: center; justify-content: center;
          z-index: 2000; animation: cuicConfirmFade 120ms ease-out;
        }
        .confirm-card {
          background: #fff; border-radius: 12px; box-shadow: 0 8px 28px rgba(0,0,0,0.25);
          width: 420px; max-width: calc(100% - 32px);
          padding: 20px 24px; display: flex; flex-direction: column; gap: 16px;
          animation: cuicConfirmPop 140ms ease-out;
          font-family: "Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
        }
        .confirm-title { font-weight: 600; font-size: 18px; line-height: 1.3; color: #111; margin: 0; }
        .confirm-subtext { font-size: 14px; line-height: 1.45; color: #555; margin: 0; }
        .confirm-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 4px; }
      `;
    }

    // Plain text for Display String: single \n breaks, EM-space indent,
    // no extra blank line before lists, and always indent the 1st bullet/number.
    const getPlainText = (rootEl) => {
      const LS = "\n";
      const IND = "\u2003"; // EM space (non-collapsing) used for indent

      const inlineText = (el) =>
        (el.innerText ?? el.textContent ?? "")
          .replace(/\u00a0/g, " ")
          .replace(/\s+/g, " ")
          .trim();

      const walk = (node, depth = 0) => {
        if (!node) return "";
        if (node.nodeType === 3) return node.nodeValue || "";
        if (node.nodeType !== 1) return "";

        const tag = node.tagName;

        if (tag === "BR") return LS;

        if (tag === "UL" || tag === "OL") {
          const isOL = tag === "OL";
          let out = "";
          let i = 1;

          Array.from(node.children).forEach((li) => {
            if (li.tagName !== "LI") return;

            // head text only (ignore nested lists)
            const clone = li.cloneNode(true);
            clone.querySelectorAll(":scope > ul, :scope > ol").forEach((n) => n.remove());
            const head = inlineText(clone);

            const indent = IND.repeat(depth + 1);
            const marker = isOL ? `${i}. ` : "• ";

            out += indent + marker + head + LS;

            // nested lists
            li.querySelectorAll(":scope > ul, :scope > ol").forEach((childList) => {
              out += walk(childList, depth + 1);
            });

            i++;
          });

          return out;
        }

        // Other elements
        let out = "";
        node.childNodes.forEach((child) => {
          out += walk(child, depth);
        });

        if ((tag === "P" || tag === "DIV" || /^H[1-6]$/.test(tag)) && !out.endsWith(LS)) {
          out += LS;
        }

        return out;
      };

      // Build raw text
      let s = walk(rootEl)
        .replace(/\r\n?/g, LS)
        .replace(/\u2029/g, LS)
        .replace(/[ \t]+\n/g, LS)
        .trim();

      // --- Fixups ---

      // 1) If a bullet/number appears mid-line, split onto a new line
      s = s
        .replace(/([^\n])(\u2003*• )/g, `$1${LS}$2`)
        .replace(/([^\n])(\u2003*\d+\. )/g, `$1${LS}$2`);

      // 2) Ensure EVERY bullet/number line starts with at least one EM-space indent
      s = s.replace(
        new RegExp(`(^|${LS})\\u2003*(?=(?:• |\\d+\\. ))`, "g"),
        `$1${IND}`
      );

      // 3) Remove whitespace-only lines *between* consecutive list items
      {
        // A line that starts with optional normal spaces + EM-spaces, then a bullet or number.
        const listHead = /^(?: |\u2003)*(?:• |\d+\. )/;

        const lines = s.split("\n");
        const out = [];
        for (let i = 0; i < lines.length; i++) {
          const prev = out.length ? out[out.length - 1] : "";
          const cur = lines[i];
          const next = i + 1 < lines.length ? lines[i + 1] : "";

          const curIsBlank = cur.trim() === ""; // trims EM-spaces too
          if (curIsBlank && listHead.test(prev) && listHead.test(next)) {
            continue; // drop the spacer line between two list items
          }
          out.push(cur);
        }
        s = out.join("\n");
      }

      // 4) Remove a whitespace-only line directly ABOVE a list block (• or 1.)
      {
        const listHead = /^(?: |\u2003)*(?:• |\d+\. )/;
        const lines = s.split("\n");
        const out = [];
        for (let i = 0; i < lines.length; i++) {
          const cur = lines[i];
          // If the current line starts a list and the previous output line is blank, drop that blank.
          if (listHead.test(cur) && out.length && out[out.length - 1].trim() === "") {
            out.pop();
          }
          out.push(cur);
        }
        s = out.join("\n");
      }

      // 5) Never allow a blank *gap* before a list (collapse to exactly one line)
      s = s
        .replace(new RegExp(`${LS}{2,}(?=${IND}(?:• |\\d+\\. ))`, "g"), LS) // before list
        .replace(/\n{3,}/g, "\n\n") // anywhere else cap to one empty line
        .trim();

      return s;
    };

    // Imperative modal creation so it stays mounted outside CUIC tree
    const openModal = () => {
      if (tools.lifecycle.open) return;

      const overlay = document.createElement("div");
      overlay.className = "modal-overlay";
      document.body.appendChild(overlay);

      const modal = document.createElement("div");
      modal.className = "modal-content";
      const printBtnHtml = showPrint ? `<button class="cuic-btn" data-action="print">Print</button>` : "";
      modal.innerHTML = `
        <div class="modal-toolbar">
          <button class="cuic-btn cuic-btn-icon cuic-btn-ghost" data-action="bold" aria-label="Bold"><b>B</b></button>
          <button class="cuic-btn cuic-btn-icon cuic-btn-ghost" data-action="italic" aria-label="Italic"><i>I</i></button>
          <button class="cuic-btn cuic-btn-icon cuic-btn-ghost" data-action="ul" aria-label="Bulleted list">&bull;</button>
          <button class="cuic-btn cuic-btn-icon cuic-btn-ghost" data-action="ol" aria-label="Numbered list">1.</button>
          <button class="cuic-btn" data-action="link">Link</button>
          <button class="cuic-btn" data-action="image">Image</button>
          ${printBtnHtml}
          <div style="flex:1"></div>
          <button class="cuic-btn cuic-btn-primary" data-action="save">Save</button>
          <button class="cuic-btn cuic-btn-danger" data-action="close">Close</button>
          <input type="file" accept="image/*" style="display:none" />
        </div>
        <div class="modal-editor" contenteditable="true">${editingHtml}</div>
      `;
      document.body.appendChild(modal);

      tools.lifecycle.overlay = overlay;
      tools.lifecycle.modalEl = modal;
      tools.lifecycle.open = true;

      const toolbar = modal.querySelector(".modal-toolbar");
      const editor = modal.querySelector(".modal-editor");
      const saveBtn = toolbar.querySelector('button[data-action="save"]');

      // -------- PASTE NORMALIZER: bullets/numbers → proper <ul>/<ol>/<li> ----------
      (function attachPasteNormalizer(ed) {
        const esc = (s) =>
          (s || "").replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

        // Convert plain text lines to lists / paragraphs
        const textToHtml = (txt) => {
          const lines = (txt || "").replace(/\r\n?/g, "\n").split("\n");
          const chunks = []; // [{type:'ul'|'ol'|'p', items:[...]}]
          let cur = null;

          const pushPara = (s) => {
            if (s.trim() === "") return;
            chunks.push({ type: "p", items: [esc(s.trim())] });
          };

          const startList = (kind) => (cur = { type: kind, items: [] });
          const finishList = () => { if (cur) { chunks.push(cur); cur = null; } };

          const bulletRx = /^\s*[•\-–—*]\s+(.*)$/;         // •, -, –, —, *
          const numRx = /^\s*(\d+)[\.\)]\s+(.*)$/;       // 1.  2)  etc.

          for (let i = 0; i < lines.length; i++) {
            const raw = lines[i];
            const mBullet = raw.match(bulletRx);
            const mNum = raw.match(numRx);

            if (mBullet) {
              if (!cur || cur.type !== "ul") { finishList(); startList("ul"); }
              cur.items.push(esc(mBullet[1]));
              continue;
            }
            if (mNum) {
              if (!cur || cur.type !== "ol") { finishList(); startList("ol"); }
              cur.items.push(esc(mNum[2]));
              continue;
            }

            // blank between list items? ignore; between paragraphs? fall through
            if (raw.trim() === "") { finishList(); continue; }
            finishList();
            pushPara(raw);
          }
          finishList();

          // Render
          return chunks.map(ch => {
            if (ch.type === "p") return `<p>${ch.items[0]}</p>`;
            const tag = ch.type;
            return `<${tag}>${ch.items.map(it => `<li>${it}</li>`).join("")}</${tag}>`;
          }).join("");
        };

        // Sanitize & pass-through HTML that already has list tags
        const sanitizeHtmlWithLists = (html) => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");
          const walk = (node) => {
            if (node.nodeType === 3) return esc(node.nodeValue);
            if (node.nodeType !== 1) return "";
            const tag = node.tagName;

            const allow = { UL: 1, OL: 1, LI: 1, P: 1, BR: 1, B: 1, STRONG: 1, I: 1, EM: 1, A: 1 };
            if (!allow[tag]) {
              // unwrap unknown tags (span, div, etc.)
              let out = "";
              node.childNodes.forEach(c => out += walk(c));
              return out;
            }
            if (tag === "A") {
              const href = node.getAttribute("href") || "";
              return `<a href="${esc(href)}">${Array.from(node.childNodes).map(walk).join("")}</a>`;
            }
            let inner = "";
            node.childNodes.forEach(c => inner += walk(c));
            return `<${tag.toLowerCase()}>${inner}</${tag.toLowerCase()}>`;
          };

          // Word/Outlook paste often isn’t real lists; if we detect that, bail to text route
          if (/MsoListParagraph|mso-list/i.test(html)) {
            return textToHtml(doc.body.innerText || doc.body.textContent || "");
          }

          const hasRealLists = !!doc.querySelector("ul,ol,li");
          if (!hasRealLists) {
            // Not real lists? Convert from the visible text
            return textToHtml(doc.body.innerText || doc.body.textContent || "");
          }

          // Real lists: sanitize allowed tags only
          let out = "";
          doc.body.childNodes.forEach(n => out += walk(n));
          return out;
        };

        ed.addEventListener("paste", (e) => {
          e.preventDefault();
          const html = e.clipboardData?.getData("text/html") || "";
          const text = e.clipboardData?.getData("text/plain") || "";

          let toInsert = "";
          if (html) {
            toInsert = sanitizeHtmlWithLists(html);
          }
          if (!toInsert) {
            toInsert = textToHtml(text);
          }

          // Insert at caret; falls back to append
          if (document.queryCommandSupported && document.queryCommandSupported("insertHTML")) {
            document.execCommand("insertHTML", false, toInsert);
          } else {
            // minimal fallback
            const tmp = document.createElement("div");
            tmp.innerHTML = toInsert;
            while (tmp.firstChild) ed.appendChild(tmp.firstChild);
          }
        }, false);
      })(editor);

      // drag the modal (ignore when starting on a button)
      toolbar.onmousedown = (e) => {
        if (e.target && (e.target.tagName === "BUTTON" || e.target.closest("button"))) return;
        let startX = e.clientX, startY = e.clientY;
        const rect = modal.getBoundingClientRect();
        const onMouseMove = (ev) => {
          modal.style.left = rect.left + (ev.clientX - startX) + "px";
          modal.style.top = rect.top + (ev.clientY - startY) + "px";
        };
        const onMouseUp = () => {
          document.removeEventListener("mousemove", onMouseMove);
          document.removeEventListener("mouseup", onMouseUp);
        };
        document.addEventListener("mousemove", onMouseMove);
        document.addEventListener("mouseup", onMouseUp, { once: true });
        e.preventDefault();
      };

      // baseline for dirty checks
      tools.lifecycle.lastSavedHtml = editingHtml;

      const normalize = (s) => (s || "").replace(/\s+/g, " ").trim();
      const currentBaseline = () => tools.lifecycle.lastSavedHtml ?? editingHtml;
      const isDirty = () => normalize(editor.innerHTML) !== normalize(currentBaseline());
      const updateSaveEnabled = () => { if (saveBtn) saveBtn.disabled = !isDirty(); };

      const saveValues = () => {
        modal.querySelectorAll("span").forEach((s) => {
          s.style.width = s.offsetWidth + "px";
          s.style.height = s.offsetHeight + "px";
        });
        const htmlContent = editor.innerHTML;
        const plainText = getPlainText(editor);
        const updates = { [htmlNodeId]: htmlContent };
        // if (plainNodeId) updates[plainNodeId] = plainText;
        tools.sendTransaction([{ type: "UPDATE_VALUES", updates }]);
        tools.lifecycle.lastSavedHtml = htmlContent;
        updateSaveEnabled();
      };

      // init save state and listeners
      updateSaveEnabled();
      editor.addEventListener("input", updateSaveEnabled);

      // --- AUTOSAVE SETUP (no timers) ---
      const autosaveEnabled = !!props.autosave;
      const mode = (props.autosaveMode || "keystrokes").toLowerCase();
      const ksThreshold = (typeof props.autosaveKeystrokes === "number" && props.autosaveKeystrokes > 0)
        ? props.autosaveKeystrokes
        : 20;

      const saveIfDirty = () => { if (isDirty()) saveValues(); };

      // clear previous listeners if modal was reopened
      if (tools.lifecycle.autosaveCleanup) {
        try { tools.lifecycle.autosaveCleanup(); } catch (_) { }
      }

      const cleanups = [];

      if (autosaveEnabled) {
        if (mode === "input") {
          const onInputAuto = () => saveIfDirty();
          editor.addEventListener("input", onInputAuto);
          cleanups.push(() => editor.removeEventListener("input", onInputAuto));
        } else if (mode === "keystrokes") {
          tools.lifecycle.ksCount = 0;
          const onInputCount = () => {
            tools.lifecycle.ksCount = (tools.lifecycle.ksCount || 0) + 1;
            if (tools.lifecycle.ksCount >= ksThreshold) {
              tools.lifecycle.ksCount = 0;
              saveIfDirty();
            }
          };
          editor.addEventListener("input", onInputCount);
          cleanups.push(() => editor.removeEventListener("input", onInputCount));
        } else {
          // default: blur
          const onBlurAuto = () => saveIfDirty();
          // capture phase so it triggers even when focus moves to toolbar buttons
          editor.addEventListener("blur", onBlurAuto, true);
          cleanups.push(() => editor.removeEventListener("blur", onBlurAuto, true));
        }

        // also save when tab is hidden (switching tabs/windows)
        const onVis = () => { if (document.hidden) saveIfDirty(); };
        document.addEventListener("visibilitychange", onVis);
        cleanups.push(() => document.removeEventListener("visibilitychange", onVis));
      }

      // remember how to clean up next close
      tools.lifecycle.autosaveCleanup = () => {
        cleanups.forEach(fn => { try { fn(); } catch (_) { } });
      };

      const saveAndClose = () => { saveValues(); closeModal(); };

      const showCloseConfirm = () => {
        if (modal.querySelector(".confirm-overlay")) return;
        const co = document.createElement("div");
        co.className = "confirm-overlay";
        co.innerHTML = `
          <div class="confirm-card">
            <div class="confirm-title">Close without saving?</div>
            <div class="confirm-subtext">If you close now, your changes will be lost.</div>
            <div class="confirm-actions">
              <button class="cuic-btn cuic-btn-danger" data-act="discard">Close without saving</button>
              <button class="cuic-btn cuic-btn-ghost" data-act="cancel">Cancel</button>
              <button class="cuic-btn cuic-btn-primary" data-act="save">Save & Close</button>
            </div>
          </div>
        `;
        modal.appendChild(co);
        co.addEventListener("click", (ev) => {
          const act = ev.target?.getAttribute?.("data-act");
          if (!act) return;
          if (act === "save") { modal.removeChild(co); saveAndClose(); }
          if (act === "discard") { modal.removeChild(co); closeModal(); }
          if (act === "cancel") { modal.removeChild(co); }
        });
      };

      const printEditor = () => {
        // Print just the editor content in a clean document, with Acid Grotesk
        const w = window.open("", "_blank");
        if (!w) return;
        const doc = w.document;

        doc.open();
        doc.write(`<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Notes</title>
  <style>
    @page { margin: 16mm; }
    body {
      font-family: "Acid Grotesk", -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
      font-size: 12pt; color: #111;
    }
    .content { white-space: pre-wrap; }
    .content img { max-width: 100%; height: auto; }
    .content a { color: #111; text-decoration: underline; }
  </style>
</head>
<body>
  <div class="content">${editor.innerHTML}</div>
</body>
</html>`);
        doc.close();

        // Inherit parent styles so the Acid Grotesk @font-face is available
        try {
          const base = doc.createElement("base");
          base.href = document.baseURI;
          doc.head.appendChild(base);
          document.querySelectorAll('link[rel="stylesheet"], style').forEach((el) => {
            doc.head.appendChild(el.cloneNode(true));
          });
        } catch (_) { }

        w.focus();
        w.onafterprint = () => { try { w.close(); } catch (_) { } };
        w.print();
      };

      toolbar.querySelectorAll("button").forEach((btn) => {
        const action = btn.getAttribute("data-action");
        if (!action) return;
        btn.onclick = () => {
          editor.focus();

          if (action === "bold" || action === "italic") {
            document.execCommand(action);
            updateSaveEnabled();
            return;
          }

          if (action === "ul") {
            document.execCommand("insertUnorderedList");
            updateSaveEnabled();
            return;
          }

          if (action === "ol") {
            document.execCommand("insertOrderedList");
            updateSaveEnabled();
            return;
          }

          if (action === "link") {
            const url = prompt("Enter URL", "https://");
            if (url) document.execCommand("createLink", false, url);
            updateSaveEnabled();
          } else if (action === "image") {
            const fileInput = toolbar.querySelector('input[type=file]');
            fileInput.click();
          } else if (action === "print") {
            printEditor();
          } else if (action === "save") {
            // Save but DO NOT close
            saveValues();
          } else if (action === "close") {
            if (isDirty()) { showCloseConfirm(); } else { closeModal(); }
          }
        };
      });

      toolbar.querySelector('input[type=file]').onchange = (e) => {
        const file = e.target.files?.[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (ev) => {
          const span = document.createElement("span");
          span.contentEditable = "false";
          Object.assign(span.style, { display: "inline-block", resize: "both", overflow: "auto", border: "1px dashed #888" });
          const img = document.createElement("img");
          img.src = ev.target.result; img.style.width = img.style.height = "100%";
          span.appendChild(img);
          const sel = window.getSelection();
          if (sel && sel.rangeCount) {
            const range = sel.getRangeAt(0);
            range.collapse(false);
            range.insertNode(span);
            range.setStartAfter(span);
            sel.removeAllRanges(); sel.addRange(range);
          } else {
            editor.appendChild(span);
          }
          updateSaveEnabled();
        };
        reader.readAsDataURL(file);
        e.target.value = "";
      };
    };

    const closeModal = () => {
      if (!tools.lifecycle.open) return;

      if (tools.lifecycle.autosaveCleanup) {
        try { tools.lifecycle.autosaveCleanup(); } catch (_) { }
        tools.lifecycle.autosaveCleanup = null;
      }

      document.body.removeChild(tools.lifecycle.overlay);
      document.body.removeChild(tools.lifecycle.modalEl);
      tools.lifecycle.overlay = null;
      tools.lifecycle.modalEl = null;
      tools.lifecycle.open = false;
    };


    const launchStyle = {
      width: props.width || "auto",
      marginTop: props.marginTop ?? "14px",
      marginBottom: props.marginBottom ?? "4px",
      marginLeft: "11px",
    };

    return (
      <div className={`notes-editor-container ${ROOT}`}>
        <button
          className="notes-editor-button"
          style={launchStyle}
          onClick={openModal}
          aria-label={launchLabel}
        >
          {launchLabel}
        </button>
      </div>
    );
  },
});

export default ModalNotesEditor;
