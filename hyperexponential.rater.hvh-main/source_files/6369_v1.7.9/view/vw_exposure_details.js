import * as HX from "hx-model-components";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} viewScale={scale}>
      <HX.Section title="Exposure Details">
        <HX.Pane>
          <HX.Collection fields={["cds/exposure/aggregate/example_aggregate_exposure", null, null, null, null]} horizontal />
          <HX.Table
            title="Granular Exposure (Example)"
            data={["cds/exposure/granular/example_exposure"]}
            fields={["country", "city", "type", "tiv"]}
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_exposure_details };