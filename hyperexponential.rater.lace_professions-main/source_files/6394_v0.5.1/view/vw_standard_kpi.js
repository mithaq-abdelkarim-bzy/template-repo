// v0.3.0
import * as HX from "hx-model-components";
import StandardKpi from "components/standard_kpi";

function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs">
      <HX.Section title="Standard KPIs">
        <StandardKpi
          layersPath="cds/layers"
          additionalLayersPath="cds/layers_addl"
        />
      </HX.Section>
    </HX.Page>
  )
}


export { vw_standard_kpi };
