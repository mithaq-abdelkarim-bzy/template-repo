// v0.3.0
// If changing the max_layers below, you must also update in rate_constants to the same number
function max_layers() {
  return 6
}


export { max_layers };


export const EC_COVERAGES = [
  "all_risks",
  "adverse_weather",
  "earthquake",
  "windstorm",
  "wildfire",
  "terrorism",
  "cyber",
  "national_mourning",
  "riots_and_civil_commotion",
  "strike",
  "war",
  "catastrophic_non_app",
];