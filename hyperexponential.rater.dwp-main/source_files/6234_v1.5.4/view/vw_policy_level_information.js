import * as HX from "hx-model-components";

function vw_policy_level_information(scale) {
  return (
    <HX.Page
      title="Policy Level Information"
      fullWidth={false}
      viewScale={scale}
      shownBy="model_state/show_after_landing_page">
      <HX.Section title="Policy Level Rating Information">
        <HX.Notes field="messages/policy_info_note" />
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection fields={["quoted_premium.read_only", null]} numCols={2} />
        </HX.With >
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
              <HX.Collection
                title="Policy Details"
                fields={[
                  "limit",
                  "aggregate_limit",
                  "type",
                  { field: "deductible", shownBy: "/flags/deductible_flag" },
                  { field: "excess", shownBy: "/flags/excess_flag" }
                ]}
              />
            </HX.With>
          </HX.Pane>
          <HX.Pane>
            <HX.Collection
              title="Terms & Conditions"
              fields={[
                "bi_and_ee_cover",
                "seperate_bi_ee_agg_limits",
                "bi_tiv",
                "extensions_covered",
                { field: "/cds/uw_rationale/extensions_comment", shownBy: "/flags/extensions_comment_flag" },
                "liability_covered"
              ]}
              with="cds/rating_factors"
            />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Collection
              title="Preparedness Factors"
              fields={[
                "risk_preparedness",
                "security",
                "crisis_management",
                "social_media",
                "high_profile_event"
              ]}
              with="cds/rating_factors"
            />
            <HX.Notes field="messages/crime_website" />
          </HX.Pane>
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}
export { vw_policy_level_information };