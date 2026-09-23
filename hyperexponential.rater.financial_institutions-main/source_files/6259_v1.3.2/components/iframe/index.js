import * as HX from "hx-model-components"

const IFrame = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    title: HX.PropTypes.string.optional,
    src: HX.PropTypes.string,
    width: HX.PropTypes.string.optional,
    height: HX.PropTypes.string.optional,

  },
  mapper: () => ({}),
  render: props => {
    return (
      <div style={{ padding: "10px", textAlign: "center" }}>
        <h2>{props.title ?? ""}
        </h2>
        <iframe
          // style={{ overflow: "hidden" }}
          style={{ overflowX: "hidden", overflowY: "auto" }}
          scrolling="no"
          frameborder="0"
          allowTransparency="true"
          src={props.src}
          width={props.width ?? document.documentElement.clientWidth}
          // width={props.width ?? "100%"}
          height={props.height ?? "100%"}
          loading="lazy"
        ></iframe>
      </div>
    );
  }

});
export default IFrame;

