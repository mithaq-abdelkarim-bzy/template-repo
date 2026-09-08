import * as HX from "hx-model-components";


function vw_aircraft_summary() {
  const aircraft_summary_fields = [
    { field: "hull_value", width: 125 },
    { field: "hull_benchmark", width: 125 },
    { field: "hull_benchmark_rate", width: 125 },
    { field: "pax_limit", width: 125 },
    { field: "pax_liab_benchmark", width: 125 },
    { field: "pax_liab_benchmark_per_seat", width: 125 },
    { field: "tpl_benchmark", width: 125 },
    { field: "total_hull_benchmark", width: 125 },
    { field: "total_liab_benchmark", width: 125 },
    { field: "total_benchmark", width: 125 }
  ]
  return (
    <HX.Page title="Aircraft Summary" fullWidth viewScale={0.8} shownBy="cds/exposure/granular/show_aircraft_summary">
      <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>

        <HX.Section title="Rating Summary by Aircraft">
          {/* <HX.Notes field="/debug_str" /> */}
          <HX.Pane>
            <HX.Table
              data={["aircraft_summary_total", null, "aircraft_summary"]}
              fields={[
                { field: "include", width: 120 },
                { field: "no_of_aircraft", width: 120 },
                { field: "market_class", width: 225, shownBy: "/cds/is_airlines" },
                { field: "aircraft_class", width: 225, shownBy: "/cds/is_ga" },
                { field: "registration", width: 175 },
                ...aircraft_summary_fields
              ]}
              dynamic
              kb-interactive
              freezeLeft={1}
            />
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_aircraft_summary };
