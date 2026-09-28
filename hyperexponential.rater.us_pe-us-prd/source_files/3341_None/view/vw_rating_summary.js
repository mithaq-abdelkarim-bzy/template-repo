import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true}>
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection
              fields={["/cds/standard_fields/rating_methodology"]}
              syncColumnWidthsKey="coverage_tables"
            />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage Options">
          <HX.Pane flow="down">
            <HX.Table
              title="Quote Inputs"
              syncColumnWidthsKey="coverage_tables"
              data={["/cds/layers"]}
              fields={[
                "is_primary_excess",
                {
                  field: "media_and_advertising",
                  shownBy: "/cds/layers_options/show_tech_options",
                },
                {
                  field: "cont_bi_pd",
                  shownBy: "/cds/layers_options/show_tech_options",
                },
                {
                  field: "first_party_privacy",
                  shownBy: "/cds/layers_options/show_tech_options",
                },
                {
                  field: "cyber_extortion_only",
                  shownBy: "/cds/layers_options/show_tech_options",
                },
                {
                  field: "general_liability/value",
                  shownBy: "general_liability/show",
                },
                { field: null, shownBy: "general_liability/show" },
                "limit",
                {
                  field: "product_liability_limits_AGG",
                  shownBy: "show_product_liability_limits_AGG",
                },
                {
                  field: "aggregate_limit",
                  shownBy: "liability_limits_AGG/show",
                },
                {
                  field: "aggregate_limit",
                  shownBy:
                    "show_staffing_liability_limits_AGG",
                  labelBy: "staffing_liability_limits_AGG_label",
                },
                {
                  field: "general_liability/limit_staffing",
                  shownBy:
                    "general_liability/show_staffing",
                },
                {
                  field: "aggregate_limit",
                  shownBy: "show_product_liability_limits_AGG",
                  labelBy: "general_liability_limits_AGG_products_label",
                },
                {
                  field: "personal_advertising_liability_EEC/limit",
                  shownBy: "personal_advertising_liability_EEC/show",
                },
                {
                  field: "defence_outside_limits/limit",
                  shownBy: "defence_outside_limits/show",
                },
                "deductible",
                { field: "excess", shownBy: "show_excess" },
                "premium",
                "brokerage",
                "status",
                null,
                "model_premium",
                "benchmark_premium",
                "bpi",
                "technical_premium",
                "tpi",
                "effective_rate",
                "pflr",
              ]}
              transpose
            />

            <HX.Table
              title="COB Code Breakdown"
              syncColumnWidthsKey="coverage_tables"
              data={["/cds/layers"]}
              fields={[
                "cob/code_1",
                "cob/premium_1",
                "cob/code_2",
                "cob/premium_2",
                "cob/code_3",
                "cob/premium_3",
              ]}
              transpose
            />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_rating_summary };
