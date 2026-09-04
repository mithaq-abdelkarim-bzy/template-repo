import * as HX from "hx-model-components";

const InfoBox = HX.buildCustomComponent({
  apiVersion: "1.0.0",

  propTypes: {
    // Markdown text stored in a node
    textNode: HX.PropTypes.path,
    // Optional UI bits
    label: HX.PropTypes.string.optional, // defaults to "i"
    width: HX.PropTypes.string.optional, // size of the round button (both width/height)
  },

  mapper: (props) => ({
    nodes: {
      text: { type: "static", path: props.textNode },
    },
    state: {
      isOpen: false,
    },
  }),

  getDerivedStateFromData: (data) => data.state,

  render: (props, data, tools) => {
    const open = () => data.setState({ isOpen: true });
    const close = () => data.setState({ isOpen: false });
    const markdown = data?.nodes?.text?.value ?? "";
    const html = markdownToHtml(markdown);

    return (
      <div>
        <button
          onClick={open}
          aria-label={props.label ?? "Show info"}
          title={props.label ?? "Info"}
          style={infoButtonStyle(props.width)}
        >
          {props.label ?? "i"}
        </button>

        {data.state.isOpen && (
          <div
            onClick={close}
            style={overlayStyle}
            role="dialog"
            aria-modal="true"
          >
            <div
              onClick={(e) => e.stopPropagation()}
              style={modalStyle}
            >
              <div
                style={contentStyle}
                // Non-editable; renders markdown as HTML
                dangerouslySetInnerHTML={{ __html: html }}
              />
            </div>
          </div>
        )}
      </div>
    );
  },
});

// ——— styles ———

const infoButtonStyle = (size) => ({
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  width: size || "36px",
  height: size || "36px",
  borderRadius: "50%",
  border: "1px solid #ccc",
  backgroundColor: "#5E2C5E",
  color: "white",
  fontWeight: 700,
  fontFamily: "Georgia",
  fontSize: "32px",
  cursor: "pointer",
  lineHeight: 1,
});

const overlayStyle = {
  position: "fixed",
  inset: 0,
  backgroundColor: "rgba(0,0,0,0.4)",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  padding: "16px",
  zIndex: 9999,
};

const modalStyle = {
  backgroundColor: "#fff",
  borderRadius: "8px",
  border: "1px solid #ddd",
  maxWidth: "720px",
  width: "100%",
  maxHeight: "80vh",
  padding: "16px",
  overflow: "auto",
  boxShadow: "0 8px 24px rgba(0,0,0,0.2)",
  fontFamily: "inherit",
  fontSize: "16px",
};

const headerStyle = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  marginBottom: "8px",
};

const closeButtonStyle = {
  background: "transparent",
  border: "none",
  fontSize: "20px",
  cursor: "pointer",
  lineHeight: 1,
};

const contentStyle = { whiteSpace: "pre-wrap" };

// ——— minimal markdown renderer (kept simple) ———

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function markdownToHtml(md) {
  const escaped = escapeHtml(md || "");

  // Links: [text](url)
  let html = escaped.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener noreferrer" ' +
    'style="color:#005bbb;text-decoration:underline;cursor:pointer;">$1</a>'
  );


  // Bold **text**
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

  // Italic *text*
  html = html.replace(
    /(^|[\s(])\*([^*\n]+)\*(?=[\s).,!?:;]|$)/g,
    "$1<em>$2</em>"
  );

  // Inline code `code`
  html = html.replace(
    /`([^`]+)`/g,
    '<code style="background:#f6f8fa;padding:2px 4px;border-radius:4px;">$1</code>'
  );

  // Headings
  html = html
    .replace(/^### (.*)$/gm, "<h3>$1</h3>")
    .replace(/^## (.*)$/gm, "<h2>$1</h2>")
    .replace(/^# (.*)$/gm, '<h1 style="font-size:1.4em;margin:0.2em 0;">$1</h1>');

  // Unordered list blocks
  html = html.replace(/(^|\n)([-*] .*(\n[-*] .*)*)(\n|$)/g, (match) => {
    const items = match
      .trim()
      .split("\n")
      .map((line) => line.replace(/^[-*] (.*)$/, "<li>$1</li>"))
      .join("");
    return `<ul style="padding-left:1.2em;margin:0.5em 0;">${items}</ul>`;
  });

  // Paragraphs (split on blank lines); preserve single line breaks
  html = html
    .split(/\n{2,}/)
    .map((block) => {
      if (/^<h\d|^<ul|^<p|^<pre|^<blockquote/.test(block)) return block;
      const withBr = block.replace(/\n/g, "<br/>");
      return `<p style="margin:0.5em 0;">${withBr}</p>`;
    })
    .join("");

  return html;
}

export default InfoBox;
