import * as HX from "hx-model-components";
import TwoAxisLineChart from "components/line";


function vw_historical_freq(scale) {
  return (
    <HX.Page title="Historic Freq" fullWidth shownBy="model_state/show_after_landing_page">
      <HX.Section title="Historical Frequencies">
        <HX.Pane flow="right">
          <HX.Collection
            fields={[
              "cds/sector_display"
            ]}
            numCols={2} />
          <HX.Collection fields={[null]} />
          <HX.Notes
            field="cds/linked_spreadsheet"
          />
        </HX.Pane>
        <HX.Table
          // wanted a dynamic title for the graph depending on sector. This wasn't possible in hx
          data={[{ datum: "cds/historical_freq", elementLabelBy: "display_year" }]}
          fields={["claims", "exposure", "base_frequency", "mc_frequency"]}
          transpose
        />
        <HX.Notes
          field="cds/table_explained"
        />
        <HX.Pane >
          <TwoAxisLineChart
            title="Historic Frequencies"
            xAxisLabel="Year"
            yAxisLabel="Frequency"
            yAxis2Label=""
            series={[
              {
                yaxis: "y",
                label: "Base Frequency",
                colour: "#000000",
                line_type: 'lines+marker',
                points: [
                  {
                    list: "cds/historical_freq",
                    x: "display_year",
                    y: "base_frequency",
                  },
                ],
              },
              {
                yaxis: "y",
                label: "Market Cap Frequency",
                colour: "#CA3397",
                line_type: 'lines',
                points: [
                  {
                    list: "cds/historical_freq",
                    x: "display_year",
                    y: "mc_frequency",
                  },
                ],
              },
            ]}
          />
          <HX.Notes
            field="cds/graph_explained"
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_historical_freq };