import * as HX from "hx-model-components";


function vw_coverage(scale, shownBy = null) {

  return (
    <HX.Page title="coverage" shownBy={shownBy}>
      <HX.Section title="Group Life - Benefits Covered">
        <HX.Pane flow="right">
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection
              title="Death"
              with="coverages"
              fields={[
                "death/cover_type",
                "additional_death/is_covered",
                "death/accidental_death_adj",
                "death/sick_affluence",
                "death/sick_weight_to_nationality",
                "death/accidental_death_rate"
              ]}
              numCols={2}
            />
            <HX.Pane flow="right">
              <HX.Collection
                title="Terminal illness"
                with="coverages/terminal_illness"
                fields={["is_covered"]}
                numCols={2}
              />
              <HX.Pane />
            </HX.Pane>
            <HX.Collection
              title="Critical illness (covers 6 illnesses)"
              with="coverages/critical_illness"
              fields={[
                "is_covered",
                "benefit",
                { field: "benefit_amount_fixed", shownBy: "show_benefit_amount" },
                { field: "benefit_amount_pct", shownBy: "show_benefit_pct" },
                { field: "cap_amount", shownBy: "show_benefit_pct" },
                { field: "cap_pct", shownBy: "show_benefit_amount" }
              ]}
              numCols={2}
            />
            <HX.Collection
              title="Repatriation expenses"
              with="coverages/repat_exp"
              fields={["is_covered", "limit"]}
              numCols={2}
            />
          </HX.With>
          <HX.Collection
            title="Historical claims experience"
            with="cds/experience_rating"
            fields={["claims_available", null]}
            numCols={2}
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_coverage };
