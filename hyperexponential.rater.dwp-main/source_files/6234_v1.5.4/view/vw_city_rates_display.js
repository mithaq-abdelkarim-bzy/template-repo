import * as HX from "hx-model-components";

function vw_city_rates_display(scale) {
  return (
    <HX.Page
      title="City Rating Table"
      fullWidth
      viewScale={scale}
      shownBy="model_state/show_after_landing_page">
      <HX.Section title="City Lookup Table">
        <HX.Pane>
          <HX.Table
            data={["city_rates_display"]}
            fields={[
              { field: "State", width: 200 },
              { field: "City", width: 350 },
              { field: "Population", width: 150 },
              { field: "ViolentCrime", width: 120 },
              { field: "VCRate", width: 120 },
              { field: "Relativity", width: 150 },
              { field: "CityRisk", width: 120 },
            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_city_rates_display };