import * as HX from "hx-model-components";


function vw_aggregates(scale) {
  return (
    <HX.Page title="Aggregates" fullWidth={true} viewScale={scale} shownBy="cds/show_non_risk_xl">
      <HX.Section title="Mandatory Details">

        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={3}>
            <HX.Pane flow="right" reflow={false}>
              <HX.Pane ratio={1} >
                <HX.Collection
                  fields={["cds/exposure/aggregate/exposure_measure",
                  ]}
                />
              </HX.Pane>
              <HX.Pane ratio={3}>
                <HX.Notes stretch={true}
                  field="cds/exposure/aggregate/exposure_comments"
                  title="Comments" />
              </HX.Pane>
            </HX.Pane>
          </HX.Pane>
          <HX.Pane ratio={4}>
            <HX.Table
              with="cds/exposure/aggregate"
              data={["ly_aggregates", "ty_aggregates", null, "value_change", "perc_change"]}
              fields={[
                { field: "exposure_total" },
                { field: "bespoke_total" },
                { field: "key_zone_total" },
              ]}
              kb-interactive
              freezeLeft={0}
              transpose
            />
          </HX.Pane>
        </HX.Pane>

      </HX.Section>
      <HX.Section title="Aggregate Entry">
        <HX.Pane>
          <HX.Table
            data={["cds/exposure/granular/exposures"]}
            fields={[
              { field: "peril" },
              { field: "address_dropdown/country" },
              { field: "address_dropdown/state" },
              { field: "address_dropdown/county" },
              { field: "description" },
              { field: "ly_aggregate" },
              { field: "ty_aggregate" },
              { field: "key_zone_selector" },
              null
              , { field: "value_change" }
              , { field: "perc_change" }

            ]}
            kb-interactive
            freezeLeft={0}
          />
        </HX.Pane>
      </HX.Section>

    </HX.Page >
  )
}

export { vw_aggregates };


