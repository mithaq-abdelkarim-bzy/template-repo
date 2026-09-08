import * as HX from "hx-model-components";
import { get_inputs_section } from "view/common";

function vw_ship_building(scale) {
  const PREFIX = "ship_building_";
  const PRICING_PREFIX = "ship_building_pricing_";
  const RATING_SUMMARY_PREFIX = "coverages/ship_building/ship_building_";
  let pricing_fields = [
    "overall_process_base_rate",
    "base_rate_steel_cutting_keel_laying",
    "base_rate_keel_laying_launch",
    "base_rate_launch_delivery",
    "base_rate_non_war",
    "vessel_type",
    "country",
    "survey_grade",
    "deductible",
    "non_war_premium_net_rate",
    "war_premium_net_rate",
    "total_exposure_net_rate_pre_fleet",
    "fleet_discount",
    "total_exposure_net_rate",
    "exposure_net_premium",
  ].map((field) => PRICING_PREFIX + field);

  return (
    <HX.Page
      title="Shipbuilders - Exposure Rating"
      shownBy="/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
      fullWidth
    >
      <HX.With
        context={{
          type: "list",
          index: 0,
          path: "/cds/layers",
        }}
      >
        {get_inputs_section("ship_building")}
        <HX.Section title="Shipbuilders Vessels">
          <HX.Pane flow="down">
            <HX.Pane flow="right">
              <HX.Collection
                fields={[RATING_SUMMARY_PREFIX + "policy_details"]}
                horizontal
                syncColumnWidthsKey="key_1"
              />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection
                fields={[
                  {
                    field:
                      "/non_cds/labels/shipbuilders/shipbuilders_vessels_number_greater_than_one_warning",
                    shownBy:
                      "/non_cds/show_hide_toggles/ship_building/show_number_of_vessels_warning",
                  },
                ]}
                horizontal
              />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table
              data={[
                "/cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list",
              ]}
              fields={[
                PREFIX + "vessel_type",
                {
                  field: PREFIX + "number_of_vessels",
                  infoBy: "/non_cds/tooltips/shipbuilders/number_of_vessels",
                },
                PREFIX + "vessel_name",
                PREFIX + "attachment_date",
                PREFIX + "delivery_date",
                {
                  field: PREFIX + "total_months_steel_cutting_keel_laying",
                  shownBy:
                    RATING_SUMMARY_PREFIX + "show_production_stages_time",
                },
                {
                  field: PREFIX + "total_months_keel_laying_launch",
                  shownBy:
                    RATING_SUMMARY_PREFIX + "show_production_stages_time",
                },
                {
                  field: PREFIX + "total_months_launch_delivery",
                  shownBy:
                    RATING_SUMMARY_PREFIX + "show_production_stages_time",
                },
                {
                  field: PREFIX + "total_months_all_stages",
                  shownBy: RATING_SUMMARY_PREFIX + "show_overall_time",
                },
                PREFIX + "country",
                PREFIX + "survey_grade",
                PREFIX + "deductible",
                PREFIX + "sum_insured",
                PREFIX + "benchmark_rate",
              ]}
              title=""
              kb-interactive
              dynamic
              maxListVisibleRows={20}
            />
            <HX.Table
              title="Actuarial Pricing"
              kb-interactive
              dynamic
              maxListVisibleRows={20}
              data={[
                "/cds/exposure/granular/vessels/ship_building_rating/ship_building_pricing_vessels_list",
              ]}
              shownBy="/non_cds/show_hide_toggles/ship_building/show_ship_builders_actuarial_pricing"
              fields={pricing_fields}
            />
            <HX.Pane flow="right">
              <HX.Collection
                fields={[
                  {
                    field: RATING_SUMMARY_PREFIX + "achieved_premium",
                    labelBy: "/non_cds/labels/ship_building/achieved_premium",
                  },
                  {
                    field:
                      "coverages/ship_building/ship_building_net_benchmark_premium_pre_uw_adj",
                    labelBy:
                      "/non_cds/labels/ship_building/exposure_benchmark_premium",
                  },
                  {
                    field: RATING_SUMMARY_PREFIX + "experience_premium",
                    labelBy:
                      "/non_cds/labels/ship_building/experience_benchmark_premium",
                    infoBy: "/non_cds/tooltips/shipbuilders/experience_premium",
                  },
                  {
                    field: RATING_SUMMARY_PREFIX + "experience_weighting",
                    labelBy:
                      "/non_cds/labels/ship_building/weight_to_experience",
                    infoBy: "/non_cds/tooltips/shipbuilders/credibility",
                  },
                  {
                    field:
                      "coverages/ship_building/ship_building_blended_benchmark_premium_pre_uw_adj",
                    labelBy:
                      "/non_cds/labels/ship_building/blended_premium_pre_adj",
                  },
                  RATING_SUMMARY_PREFIX + "uw_adjustment",
                  {
                    field:
                      "coverages/ship_building/ship_building_blended_benchmark_premium_post_uw_adj",
                    labelBy:
                      "/non_cds/labels/ship_building/blended_premium_post_adj",
                  },
                ]}
                syncColumnWidthsKey="key_1"
              />
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_ship_building };
