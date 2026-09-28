import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true}>
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
      <HX.Section title="Rating Factors">
        <HX.Pane flow="right">
          <HX.Collection
            with="cds/rating_factors"
            fields={[
              {
                field: "tech/media_and_advertising",
                shownBy: "tech/show",
              },
              {
                field: "tech/cont_bi_pd",
                shownBy: "tech/show",
              },
              {
                field: "tech/first_party_privacy",
                shownBy: "tech/show",
              },
              {
                field: "tech/cyber_extortion_only",
                shownBy: "tech/show",
              },
              {
                field: "general_liability/value",
                shownBy: "general_liability/show",
              },
            ]}
          />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Coverage Options">
          <HX.Pane flow="down">
            <HX.Table
              title="Quote Inputs"
              syncColumnWidthsKey="coverage_tables"
              data={[{ datum: "/cds/layers", width: 250 }]}
              fields={[
                "is_primary_excess",
                null,
                "status",
                "limit",
                {
                  field: "product_liability_limits_AGG",
                  shownBy:
                    "/cds/rating_factors/show_product_liability_limits_AGG",
                },
                {
                  field: "aggregate_limit",
                  shownBy: "liability_limits_AGG/show",
                },
                {
                  field: "aggregate_limit",
                  shownBy:
                    "/cds/rating_factors/show_staffing_liability_limits_AGG",
                  labelBy:
                    "/cds/rating_factors/staffing_liability_limits_AGG_label",
                },
                {
                  field: "general_liability/limit_staffing",
                  shownBy:
                    "/cds/rating_factors/general_liability/show_staffing",
                },
                {
                  field: "aggregate_limit",
                  shownBy:
                    "/cds/rating_factors/show_product_liability_limits_AGG",
                  labelBy:
                    "/cds/rating_factors/general_liability_limits_AGG_products_label",
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
                "brokerage",
                "written_line",
                null,
                "premium",
                "quoted_premium",
                {
                  field: "model_premium",
                  shownBy: "/cds/standard_fields/is_rater_priced",
                },
                "technical_premium",
                {
                  field: "technical_premium_pre_uw_adj",
                  shownBy: "/cds/standard_fields/is_rater_priced",
                },
                { field: "benchmark_premium" },
                null,
                "tpi",
                {
                  field: "tpi_pre_uw_adj",
                  shownBy: "/cds/standard_fields/is_rater_priced",
                },
                {
                  field: "bpi",
                  shownBy: "/cds/standard_fields/is_rater_priced",
                },
                {
                  field: "bpi_case_priced",
                  shownBy: "/cds/standard_fields/is_case_priced",
                },
                null,
                "pflr",
                "roc",
                {
                  field: "uw_adj_impact",
                  shownBy: "/cds/standard_fields/is_rater_priced",
                },
              ]}
              transpose
              freezeLeft={0}
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
