import * as HX from "hx-model-components";


function vw_perils(shownBy) {
  return (
    <HX.Page title="Peril Sheet" shownBy={shownBy} fullWidth viewScale={0.9}>

      <HX.Section title="Policy Summary">
        <HX.Pane flow="right">
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["/cds/standard_fields/insured_name", "section_reference"]} />
          </HX.With>
          <HX.Collection with="cds/exposure/aggregate" fields={["no_of_locations", "total_sum_insured", "details/limit_type"]} />
        </HX.Pane>
      </HX.Section>

      <HX.With context={{ type: "struct", path: "cds/exposure/aggregate" }}>
        <HX.Section title="Summary of Perils">
          <HX.Pane flow="right">
            <HX.Button task="task_confirm_limits" title="Confirm limits" />
            <HX.Notes field="confirm_message" />
          </HX.Pane>

          <HX.Notes field="peril_comments" title="Comments" />

          <HX.Pane>
            <HX.Table
              title="Perils"
              with="perils"
              data={[
                "terrorism"
                , "sabotage"
                , "rscc"
                , "damage"
                , "insurrection"
                , "coup"
                , "war"
                , "insurgency"
                , "liability"
                , "cyber"
                , "nrcb"
                , "looting"
              ]}
              fields={[
                null
                , { "field": "is_covered_calculated", "maxWidth": 140 }
                , { "field": "is_covered_override", "maxWidth": 140 }
                , { "field": "is_covered_selected", "maxWidth": 140 }
                , null
                , { "field": "limit_calculated", "maxWidth": 140 }
                , { "field": "limit_override", "maxWidth": 140 }
                , { "field": "limit_selected", "maxWidth": 140 }
                , null
                , { "field": "excess_calculated", "maxWidth": 140 }
                , { "field": "excess_override", "maxWidth": 140 }
                , { "field": "excess_selected", "maxWidth": 140 }
                , null
                , { "field": "deductible_calculated", "maxWidth": 140 }
                , { "field": "deductible_override", "maxWidth": 140 }
                , { "field": "deductible_selected", "maxWidth": 140 }

              ]}
              kb-interactive
              freezeLeft={1}
            // syncColumnWidthsKey="perils"
            />
            <HX.Table
              title="CBI Perils"
              with="cbi_perils"
              data={[
                "unnamed"
                , "named"
                , "interruption"
                , "denial"
                , "ingress"
                , "authority"
              ]}
              fields={[
                null
                , { "field": "is_covered_selected", "maxWidth": 140 }
                , { "field": "limit_selected", "maxWidth": 140 }
                , { "field": "excess_selected", "maxWidth": 140 }
                , { "field": "deductible_selected", "maxWidth": 140 }
                , null
                , { "field": "territory_covered", "maxWidth": 140, "shownBy": "/cds/exposure/aggregate/cbi_peril_territory_covered_show" }
                , { "field": "distance_selected", "maxWidth": 140 }
                , { "field": "metric_selected", "maxWidth": 140 }

              ]}
              kb-interactive
              freezeLeft={1}
              syncColumnWidthsKey="perils"
            />

          </HX.Pane>

        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_perils };
