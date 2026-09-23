import * as HX from "hx-model-components";

function vw_general_specie(scale) {
  return (
    <HX.Page fullWidth={true} viewScale={scale} title="General Specie" shownBy="cds/show_page/show_gs">
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
        <HX.Section title="Exposure Rate Summary">
          <HX.Pane flow="right">
            {/* <HX.Collection
            fields={["gs_class"]}
            stretch
          /> */}
            <HX.Table
              data={["gs_metals", "gs_cash", "gs_securities", "gs_additional"]}
              fields={["premium",
                "tsi",
                "deductible",
                "ded_perc",
                "credit",
                "uw_adj_impact",
                "prem_post_ded",
                "implied_rate_post_ded",
                "prem_ly", "tsi_ly",
                "ded_credit_ly",
                "uw_adj_impact_ly",
                "prem_post_ded_ly"]}
              title="Summary"
              with="coverages"
            />
          </HX.Pane >
        </HX.Section >
        <HX.Section title="General Specie Specific">
          <HX.Pane flow="right">
            <HX.Collection
              fields={[null]}
            />
            <HX.Collection
              fields={["/cds/gs_transit_relativity"]}
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table
              data={[
                "static_0",
                "static_1",
                "static_2",
                "static_3",
                "static_4",
                "static_5",
                "static_6",
                null,
                "static_subtotal"]}
              fields={["region", "tsi", "rate", "premium"]}
              title="STATIC - Metal"
              with="coverages/gs_metals"
            />
            <HX.Table
              data={[
                "transit_0",
                "transit_1",
                "transit_2",
                "transit_3",
                "transit_4",
                "transit_5",
                "transit_6",
                null,
                "transit_subtotal"]}
              fields={["region", "tsi", "rate", "premium"]}
              title="TRANSIT - Metal"
              with="coverages/gs_metals"
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table
              data={[
                "static_0",
                "static_1",
                "static_2",
                "static_3",
                "static_4",
                "static_5",
                "static_6",
                null,
                "static_subtotal"]}
              fields={["region", "tsi", "rate", "premium"]}
              title="STATIC - Cash"
              with="coverages/gs_cash"
            />
            <HX.Table
              data={[
                "transit_0",
                "transit_1",
                "transit_2",
                "transit_3",
                "transit_4",
                "transit_5",
                "transit_6",
                null,
                "transit_subtotal"]}
              fields={["region", "tsi", "rate", "premium"]}
              title="TRANSIT - Cash"
              with="coverages/gs_cash"
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table
              data={[
                "static_0",
                "static_1",
                "static_2",
                "static_3",
                "static_4",
                "static_5",
                "static_6",
                null,
                "static_subtotal"]}
              fields={["region", "tsi", "rate", "premium"]}
              title="STATIC - Securities"
              with="coverages/gs_securities"
            />
            <HX.Table
              data={[
                "transit_0",
                "transit_1",
                "transit_2",
                "transit_3",
                "transit_4",
                "transit_5",
                "transit_6",
                null,
                "transit_subtotal"]}
              fields={["region", "tsi", "rate", "premium"]}
              title="TRANSIT - Securities"
              with="coverages/gs_securities"
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table
              data={[
                "custom"
              ]}
              fields={["coverage", "tsi", "prem_rate_per_100_tsi", "premium"]}
              title="Additional"
              with="coverages/gs_additional"
            />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page >
  )
}

export { vw_general_specie };