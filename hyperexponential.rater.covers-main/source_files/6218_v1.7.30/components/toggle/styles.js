const outerDiv = {
  "color": "rgb(0, 0, 0)",
  "box-sizing": "inherit",
  "outline": "none",
  "height": "100%",
  "width": "100%",
  "grid-area": "1 / 1 / auto / 7",
  "border-style": "solid",
  "border-color": "rgb(50, 107, 159)",
  "border-radius": "0px",
  "border-width": "0px",
  "display": "flex",
  "flex-direction": "row",
  "align-items": "center",
  "justify-content": "flex-start",
  "padding": "10px"
}

const captionClass = {
  "box-sizing": "inherit",
  "margin": "0px",
  "font-size": "0.875rem",
  "line-height": "1.5rem",
  "font-weight": "400",
  "color": "rgb(97, 98, 99)",
  "letter-spacing": "0px",
}

const outerSwitch = {
  "color": "rgb(0, 0, 0)",
  "display": "inline-flex",
  "overflow": "hidden",
  "box-sizing": "border-box",
  "position": "relative",
  "flex-shrink": "0",
  "z-index": "0",
  "vertical-align": "middle",
  "width": "58px",
  "height": "38px",
  "padding": "12px",
  "transition": "box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1)"
}

const switchCommon = {
  "display": "inline-flex",
  "-webkit-box-align": "center",
  "align-items": "center",
  "-webkit-box-pack": "center",
  "justify-content": "center",
  "box-sizing": "border-box",
  "-webkit-tap-highlight-color": "transparent",
  "cursor": "pointer",
  "user-select": "none",
  "vertical-align": "middle",
  "appearance": "none",
  "position": "absolute",
  "top": "0px",
  "left": "0px",
  "z-index": "1",
  "outline": "0px",
  "border-width": "0px",
  "border-style": "initial",
  "border-color": "initial",
  "border-image": "initial",
  "margin": "0px",
  "text-decoration": "none",
  "border-radius": "50%",
  "transition": "left 150ms cubic-bezier(0.4, 0, 0.2, 1), transform 150ms cubic-bezier(0.4, 0, 0.2, 1)",
  "padding": "9px",
}

const switchOff = {
  ...switchCommon,
  "background-color": "transparent",
  "color": "rgb(255, 255, 255)",
}

const switchOn = {
  ...switchCommon,
  "background-color": "rgba(14, 18, 79, 0)",
  "color": "rgb(14, 18, 79)",
  "transform": "matrix(1, 0, 0, 1, 19.8596, 0)",
}

const inputClass = {
  "user-select": "none",
  "box-sizing": "inherit",
  "cursor": "inherit",
  "position": "absolute",
  "opacity": "0",
  "height": "100%",
  "top": "0px",
  "margin": "0px",
  "padding": "0px",
  "z-index": "1",
  "left": "-100%",
  "width": "300%",
}

const switchThumbCommon = {
  "-webkit-tap-highlight-color": "transparent",
  "cursor": "pointer",
  "user-select": "none",
  "box-sizing": "inherit",
  "box-shadow": "none",
  "background-color": "currentcolor",
  "border-radius": "50%",
  "border-width": "1px",
  "border-style": "solid",
  "width": "20px",
  "height": "20px",
}

const switchThumbOn = {
  ...switchThumbCommon,
  "color": "rgb(14, 18, 79)",
  "border-color": "currentcolor",
}

const switchThumbOff = {
  ...switchThumbCommon,
  "color": "rgb(255, 255, 255)",
  "border-color": "rgb(50, 107, 159)",
}

const touchRipple = {
  "-webkit-tap-highlight-color": "transparent",
  "cursor": "pointer",
  "user-select": "none",
  "color": "rgb(14, 18, 79)",
  "box-sizing": "inherit",
  "overflow": "hidden",
  "pointer-events": "none",
  "position": "absolute",
  "z-index": "0",
  "inset": "0px",
  "border-radius": "inherit",
}

const trackCommon = {
  "color": "rgb(0, 0, 0)",
  "box-sizing": "inherit",
  "height": "100%",
  "width": "100%",
  "z-index": "-1",
  "border-radius": "7px",
  "transition": "opacity 150ms cubic-bezier(0.4, 0, 0.2, 1), background-color 150ms cubic-bezier(0.4, 0, 0.2, 1)",
}

const trackOn = {
  ...trackCommon,
  "opacity": "0.5",
  "background-color": "rgb(14, 18, 79)",
}

const trackOff = {
  ...trackCommon,
  "background-color": "rgb(0, 0, 0)",
  "opacity": "0.38",
}


export { outerDiv, captionClass, outerSwitch, switchOn, switchOff, inputClass, switchThumbOn, switchThumbOff, touchRipple, trackOn, trackOff }