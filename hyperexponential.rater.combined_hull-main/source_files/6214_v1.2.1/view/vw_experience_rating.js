import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_experience_rating() {
  return (
    <HX.Page
      title="Shipbuilders - Experience Rating"
      fullWidth={true}
      with="cds/exposure/granular/vessels"
      shownBy="/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
    >
      <HX.With
        context={{
          type: "struct",
          path: "cds/experience_rating/ship_building",
        }}
      >
        <HX.Section title="Data Input">
          <HX.Pane flow="down">
            <HX.Pane flow="right">
              <HX.Collection fields={["claims_date"]} />
              <HX.Button title="Populate BI Data" task="populate_bi_data" />
              <HX.Collection
                fields={[
                  "claims_currency",
                  {
                    field: "claims_fx_rate",
                    labelBy:
                      "/non_cds/labels/ship_building/experience_rating/currency_experience_exchange_rate_label",
                  },
                ]}
              />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection
                shownBy="/non_cds/show_hide_toggles/ship_building/show_experience_rating_warning"
                fields={[
                  {
                    field:
                      "/non_cds/labels/shipbuilders/experience_signed_line_warning.read_only_option",
                    shownBy:
                      "/non_cds/show_hide_toggles/ship_building/show_experience_signed_line_warning",
                  },
                  {
                    field:
                      "/non_cds/labels/shipbuilders/number_of_vessels_warning.read_only_option",
                    shownBy:
                      "/non_cds/show_hide_toggles/ship_building/show_experience_number_of_vessels_warning",
                  },
                ]}
              />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table
              freezeLeft={1}
              data={["data_input_experience_table"]}
              fields={[
                "yoa",
                "previous_insurer",
                "number_of_vessels",
                {
                  field: "premium",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_gross_premium_label",
                },
                "acquisition_cost",
                {
                  field: "net_premium_shared_line",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_net_premium_shared_line_label",
                },
                {
                  field: "total_incurred_shared_line",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_total_incurred_label",
                },
                {
                  field: "att_incurred_shared_line",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_att_incurred_label",
                },
                {
                  field: "large_incurred_shared_line",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_large_incurred_label",
                },
                "signed_line",
                "rate_change",
                "is_include_year",
              ]}
              kb-interactive
              freezeRight={1}
              dynamic
            />
            <HX.Pane flow="right">
              <HX.Collection
                fields={[
                  {
                    field: "current_year_rate_change",
                    labelBy:
                      "/non_cds/labels/ship_building/experience_rating/current_year_experience_rating_rate_change_label",
                  },
                ]}
              />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="ULR Projection" defaultCollapsed>
          <HX.Pane flow="down">
            <HX.Table
              freezeLeft={1}
              data={["ulr_projection_experience_table"]}
              fields={[
                "yoa",
                {
                  field: "premium",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_net_premium_label",
                },
                {
                  field: "att_incurred_shared_line",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_att_incurred_label",
                },
                {
                  field: "large_incurred_shared_line",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_large_incurred_label",
                },
                "rate_change",
                "rate_change_cumulative",
                {
                  field: "on_levelled_premium",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_on_levelled_net_premium_label",
                },
                "claims_inflation_yoy",
                "claims_inflation_cumulative",
                {
                  field: "on_levelled_att_incurred_shared_line",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_on_levelled_att_incurred_label",
                },
                "on_levelled_att_incurred_lr",
                {
                  field: "on_levelled_large_incurred_shared_line",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_on_levelled_large_claims_label",
                },
                "on_levelled_large_incurred_lr",
                "development_month",
                "development_percent",
                "attritional_ulr",
                "is_include_year",
              ]}
              kb-interactive
              dynamic
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Large Load Selection">
          <HX.With context={{ type: "struct", path: "large_load_selection" }}>
            <HX.Pane flow="right">
              <HX.Collection
                fields={["average_on_levelled_net_large_lr"]}
                title="From Experience"
              />
              <HX.Collection
                fields={[
                  "user_selected/user_number_of_years_expected_large_loss",
                  "user_selected/user_average_net_lr_of_large_loss",
                  "user_selected/selected_large_load",
                ]}
                title="User Selected"
              />
              <HX.Collection
                fields={[
                  "portfolio_load_guidance/guidance_number_of_years_expected_large_loss",
                  "portfolio_load_guidance/guidance_average_net_lr_of_large_loss",
                  "portfolio_load_guidance/portfolio_large_load",
                ]}
                title="Portfolio Load - Guidance"
              />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Experience Pricing Results 100% Share">
          <HX.Pane flow="right">
            <HX.Collection
              with={"experience_pricing_results"}
              fields={[
                "average_attritional_ulr",
                "large_load",
                "total_ulr",
                {
                  field: "experience_claims_cost",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_claims_cost_label",
                },
                {
                  field: "net_benchmark_premium_pure_experience",
                  labelBy:
                    "/non_cds/labels/ship_building/experience_rating/currency_experience_claims_net_benchmark_premium_pure_experience",
                },
              ]}
            />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Experience Pricing Weighting Calculation">
          <HX.Pane flow="right">
            <HX.Collection
              with={"experience_weighting_calculation"}
              fields={["total_number_of_vessels", "experience_weighting"]}
            />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_experience_rating };
