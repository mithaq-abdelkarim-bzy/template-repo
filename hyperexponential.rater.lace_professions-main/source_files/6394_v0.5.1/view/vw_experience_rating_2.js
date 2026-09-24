// v0.3.0
import * as HX from "hx-model-components";
import { claims_summary_years_15, claims_summary_years_20 } from "view/vw_constants";

function vw_experience_rating_2(scale) {
  return (
    <HX.Page title="Experience Rating" fullWidth={true} viewScale={scale}>
      <HX.Section title="Instructions" defaultCollapsed={false}>
        <HX.Notes field="cds/experience_rating/experience_instructions" />
      </HX.Section>
      <HX.Section title="Historical Account Performance (in USD)" defaultCollapsed={false}>
        <HX.Collection fields={["units_to_view", "layer_to_view", null, null, null, null]} with="cds/experience_rating" horizontal />
        <HX.Table
          data={[
            { datum: "layer_to_view_summary" },
          ]}
          fields={[
            { field: "aoc_limit_usd", width: 170 },
            { field: "agg_limit_usd", width: 170 },
            { field: "aoc_attachment", width: 170 },
            { field: "agg_attachment", width: 170 },
          ]}
          rowHeaderSettings={{ width: 70 }}
          with="cds/experience_rating"
          dynamic
          kb-interactive
        />
        <HX.Table
          data={claims_summary_years_20()}
          fields={[
            { field: "revalued_notional_revenue", width: 170 },
            { field: "revalued_notional_revenue_weighted", maxWidth: 170 },
            { field: "pcnt_developed", width: 170 },
            { field: "gu_incurred", width: 170 },
            { field: "gu_inflated", width: 170 },
            null,
            { field: "ql_inflated_incurred", width: 200 }
          ]}
          rowHeaderSettings={{ width: 70 }}
          with="cds/experience_rating"
          dynamic
          kb-interactive
        />
        <HX.Pane flow="right">
          <HX.Table
            data={[
              { datum: "experience_rating/weighted_revalued_notional_revenue" },
              { datum: "experience_rating/developed_weighted_revalued_notional_revenue" },
              { datum: "experience_rating/value_of_claims_data", infoBy: "hover_info/value_of_claims_data" },
            ]}
            fields={[
              { field: "last_10_years", width: 168, labelBy: "experience_rating/last_x_year_labels/last_10_years" },
              { field: "last_15_years", width: 168, labelBy: "experience_rating/last_x_year_labels/last_15_years" },
              { field: "last_20_years", width: 168, labelBy: "experience_rating/last_x_year_labels/last_20_years" },
            ]}
            with="cds"
            rowHeaderSettings={{ width: 380 }}
            kb-interactive
          />
          <HX.Table
            data={[
              { datum: "inflated_incurred_to_quoted_layer" },
              { datum: "per_yr_of_claims_data_value" },
              { datum: "gross_benchmark_experience_rated_premium" },
            ]}
            fields={[
              { field: "last_10_years", width: 168, labelBy: "last_x_year_labels/last_10_years" },
              { field: "last_15_years", width: 168, labelBy: "last_x_year_labels/last_15_years" },
              { field: "last_20_years", width: 168, labelBy: "last_x_year_labels/last_20_years" },
            ]}
            with="cds/experience_rating"
            rowHeaderSettings={{ width: 380 }}
            kb-interactive
          />
          {/* <HX.Collection fields={[null]} with="hx_core" horizontal /> */}
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Pricing Summary By Layer (USD)" defaultCollapsed={false}>
        <HX.Table
          data={[
            {
              datum: "layers", elementLabelBy: "name"
            }
          ]}
          fields={[
            { field: "include", width: 100 },
            { field: "experience_rating_summary/aoc_limit", width: 220 },
            { field: "experience_rating_summary/agg_limit", width: 220 },
            { field: "experience_rating_summary/aoc_attachment", width: 220 },
            { field: "experience_rating_summary/agg_attachment", width: 220 },
            { field: "experience_rating_summary/gross_benchmark_premium", width: 240, infoBy: "hover_info/gross_benchmark_premium" },
            { field: "experience_rating_summary/ilf_gross_benchmark_premium", width: 240, infoBy: "hover_info/ilf_gross_benchmark_premium" },
          ]}
          with="cds"
          rowHeaderSettings={{ width: 100 }}
          kb-interactive
        />
        <HX.Table
          data={[
            {
              datum: "layers_addl", elementLabelBy: "name"
            }
          ]}
          fields={[
            { field: "include", width: 100 },
            { field: "experience_rating_summary/aoc_limit", width: 220 },
            { field: "experience_rating_summary/agg_limit", width: 220 },
            { field: "experience_rating_summary/aoc_attachment", width: 220 },
            { field: "experience_rating_summary/agg_attachment", width: 220 },
            { field: "experience_rating_summary/gross_benchmark_premium", width: 240, infoBy: "hover_info/gross_benchmark_premium" },
            { field: "experience_rating_summary/ilf_gross_benchmark_premium", width: 240, infoBy: "hover_info/ilf_gross_benchmark_premium" },
          ]}
          with="cds"
          rowHeaderSettings={{ width: 100 }}
          kb-interactive
        />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_experience_rating_2 };