// If changing the max_layers below, you must also update in rate_constants to the same number
function max_layers() {
  return 20
}

function number_curves() {
  return 30
}

function max_curves() {
  return 30
}

// RMS is added in pml curves view file
const pml_types = ["air_curves", "nmp_curves", "other_curves"]
const pml_titles = ["AIR Curves", "NMP Curves", "Other Curves"]


const peril_references = ["el_eq", "el_ws", "el_scs", "el_wf", "el_winter", "el_fl", "el_other"]
const peril_titles = ["EQ", "WS", "SCS", "WF", "Winter", "FL", "Other"]


export { max_layers, number_curves, max_curves, pml_types, pml_titles, peril_references, peril_titles };