import * as HX from "hx-model-components";

function vw_general_specie() {
  return (
    <HX.Page fullWidth={true} title="General Specie">
      <HX.Section title="Exposure Rate Summary">
        <HX.Pane flow="right">
          {/* <HX.Collection
            fields={["gs_class"]}
            stretch
          /> */}
          <HX.Table
            data={["gs_metals_summary", "gs_cash_summary", "gs_securities_summary"]}
            fields={["premium",
              "tsi",
              "ded",
              "ded_perc",
              { field: "credit", infoBy: "ded_input_metals_display" },
              "uw_adj_impact",
              "prem_post_ded",
              "implied_rate_post_ded",
              "prem_ly", "tsi_ly",
              "ded_credit_ly",
              "uw_adj_impact_ly",
              "prem_post_ded_ly"]}
            title="Summary"
          />
        </HX.Pane >
      </HX.Section >
      <HX.Section title="General Specie Specific">
        <HX.Pane flow="right">
          <HX.Collection
            fields={[null]}
          />
          <HX.Collection
            fields={["gs_transit_relativity"]}
          />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table
            data={[
              "gs_static_metals_region_usa",
              "gs_static_metals_region_europe",
              "gs_static_metals_region_asia",
              "gs_static_metals_region_africa",
              "gs_static_metals_region_oceania",
              "gs_static_metals_region_north_america",
              "gs_static_metals_region_south_america",
              null,
              "gs_static_metals_region_total"]}
            fields={["tsi", "rate", "premium"]}
            title="STATIC - Metal"
          />
          <HX.Table
            data={[
              "gs_transit_metals_region_usa",
              "gs_transit_metals_region_europe",
              "gs_transit_metals_region_asia",
              "gs_transit_metals_region_africa",
              "gs_transit_metals_region_oceania",
              "gs_transit_metals_region_north_america",
              "gs_transit_metals_region_south_america",
              null,
              "gs_transit_metals_region_total"]}
            fields={["tsi", "rate", "premium"]}
            title="TRANSIT - Metal"
          />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table
            data={[
              "gs_static_cash_region_usa",
              "gs_static_cash_region_europe",
              "gs_static_cash_region_asia",
              "gs_static_cash_region_africa",
              "gs_static_cash_region_oceania",
              "gs_static_cash_region_north_america",
              "gs_static_cash_region_south_america",
              null,
              "gs_static_cash_region_total"]}
            fields={["tsi", "rate", "premium"]}
            title="STATIC - Cash"
          />
          <HX.Table
            data={[
              "gs_transit_cash_region_usa",
              "gs_transit_cash_region_europe",
              "gs_transit_cash_region_asia",
              "gs_transit_cash_region_africa",
              "gs_transit_cash_region_oceania",
              "gs_transit_cash_region_north_america",
              "gs_transit_cash_region_south_america",
              null,
              "gs_transit_cash_region_total"]}
            fields={["tsi", "rate", "premium"]}
            title="TRANSIT - Cash"
          />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table
            data={[
              "gs_static_securities_region_usa",
              "gs_static_securities_region_europe",
              "gs_static_securities_region_asia",
              "gs_static_securities_region_africa",
              "gs_static_securities_region_oceania",
              "gs_static_securities_region_north_america",
              "gs_static_securities_region_south_america",
              null,
              "gs_static_securities_region_total"]}
            fields={["tsi", "rate", "premium"]}
            title="STATIC - Securities"
          />
          <HX.Table
            data={[
              "gs_transit_securities_region_usa",
              "gs_transit_securities_region_europe",
              "gs_transit_securities_region_asia",
              "gs_transit_securities_region_africa",
              "gs_transit_securities_region_oceania",
              "gs_transit_securities_region_north_america",
              "gs_transit_securities_region_south_america",
              null,
              "gs_transit_securities_region_total"]}
            fields={["tsi", "rate", "premium"]}
            title="TRANSIT - Securities"
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_general_specie };