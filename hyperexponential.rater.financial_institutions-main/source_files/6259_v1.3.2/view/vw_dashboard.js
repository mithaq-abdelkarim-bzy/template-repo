import * as HX from "hx-model-components"
import IFrame from "components/iframe"

function vw_dashboard(scale) {
  return (
    <HX.Page title="Climate Litigation" shownBy="cds/rating_factors/risk_info/do_coverage_required" fullWidth={true} viewScale={scale}>
      <HX.Section title="Climate Litigation Heatmap - Dashboard">
        <HX.Pane flow="right">
          <HX.Pane ratio={1} />
          <IFrame
            src="https://app.powerbi.com/reportEmbed?reportId=61c3c19e-fd8e-40ec-b41a-58600b833fff&appId=4b854f37-b63a-418b-904a-b507574e6797&autoAuth=true&ctid=9a50eba8-7568-447a-bcb9-27a0d464aa80"
            height="700"
          />
          <HX.Pane ratio={1} />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Download Document">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Collection fields={["cds/climate_document_country"]} horizontal />
            <HX.Button task="generate_climate_doc_task" title="Generate Climate Litigation Spotlight Report" />
            <HX.File field="cds/climate_document" />
          </HX.Pane>
          <HX.Pane>

          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  );
}

export { vw_dashboard };