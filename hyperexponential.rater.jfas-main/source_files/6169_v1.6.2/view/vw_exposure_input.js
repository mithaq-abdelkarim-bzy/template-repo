import * as HX from "hx-model-components";

function vw_exposure_input(scale) {
  return (
    <HX.Page title="Exposure Input" fullWidth={true} viewScale={scale} shownBy="cds/show_page/show_other">
      <HX.Section title="Clear Exposure Information">
        <HX.Pane flow="right">
          <HX.Button task="clear_exposure_input_task" title="Clear Exposure Details Schedule" />
          <HX.Collection fields={[
            null,
          ]} />
          <HX.Collection fields={[
            null,
          ]} />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Exposure Details">
        <HX.Pane>
          <HX.Table
            data={["cds/schedule"]}
            fields={["risk_class", "region", "country", "currency", "type", "tsi", "tsi_cnv", "sanctioned_country", "tsi_band_1", "tsi_band_2", "tsi_band_3", "tsi_band_4", "tsi_band_5", "tsi_band_6", "tsi_band_7", "tsi_band_8", "tsi_band_9", "tsi_band_10"]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Prior Year Exposure (Renewal Risks Only)" shownBy="cds/standard_fields/is_renewal" defaultCollapsed>
        <HX.Pane>
          <HX.Table
            data={["cds/schedule_prior"]}
            fields={["risk_class", "region", "country", "currency", "type", "tsi", "tsi_cnv", "sanctioned_country", "tsi_band_1", "tsi_band_2", "tsi_band_3", "tsi_band_4", "tsi_band_5", "tsi_band_6", "tsi_band_7", "tsi_band_8", "tsi_band_9", "tsi_band_10"]}

          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_exposure_input };