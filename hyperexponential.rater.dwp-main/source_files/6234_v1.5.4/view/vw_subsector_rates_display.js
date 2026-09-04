import * as HX from "hx-model-components";

function vw_subsector_rates_display(scale) {
  return (
    <HX.Page
      title="SubSector Rating Table"
      fullWidth
      viewScale={scale}
      shownBy="model_state/show_after_landing_page">
      <HX.Section title="Sector / SubSector Rating Table">
        <HX.Pane>
          <HX.Table
            data={["subsector_rates_display"]}
            fields={[
              { field: "Sector", width: 200 },
              { field: "SubSector", width: 400 },
              { field: "BaseRate", width: 200 },
              { field: "Relativity", width: 200 }
            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_subsector_rates_display };