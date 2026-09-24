const layer_labels = [
  "Primary Layer",
  "Excess Layer 1",
  "Excess Layer 2",
  "Excess Layer 3",
  "Excess Layer 4",
  "Excess Layer 5"];

// If changing the max_layers below, you must also update in rate_constants to the same number
function max_layers() {
  return 6
}

function max_options() {
  return 4
}

export { layer_labels, max_layers, max_options };
