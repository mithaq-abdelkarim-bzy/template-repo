
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page title="Landing Page"
        shownBy="model_state/show_landing_page">
        <HX.Section title="Start Policy">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Notes field="model_state/landing_page_info" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "inception_date",
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "underwriter",
              "insured_name",
              {
                "field": "/cds/name_on_yard",
                "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
              }
            ]}
              with="cds/standard_fields"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/currencies/source_currency",
              "cds/standard_fields/is_renewal"
            ]}
              horizontal={true}
              syncColumnWidthsKey="coverage_type_key" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Coverage">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/coverage_type",
              {
                "field": "/non_cds/show_hide_toggles/hull/show_hull_coverage",
                "shownBy": "/non_cds/show_hide_toggles/hull/show_hull_coverage"
              },
              {
                "field": "cds/is_iv_coverage",
                "shownBy": "/non_cds/show_hide_toggles/hull/show_hull_coverage"
              },
              {
                "field": "cds/is_war_coverage",
                "shownBy": "/non_cds/show_hide_toggles/hull/show_hull_coverage"
              }
            ]}
              horizontal={true}
              syncColumnWidthsKey="coverage_type_key" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Vessels"
        fullWidth={true}
        shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage">
        <HX.With context={{
          "index": 0,
          "path": "/cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Inputs">
            <HX.Pane flow="down">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "coverages/hull/section_reference",
                  "coverages/hull/brokerage",
                  "coverages/hull/written_line",
                  "coverages/hull/hull_lead_follow",
                  "/cds/exposure/granular/vessels/hull_rating/operator_domicile",
                  "/cds/exposure/granular/vessels/hull_rating/is_modelling"
                ]}
                  horizontal={true} />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  {
                    "field": "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                    "shownBy": "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                  }
                ]} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Button task="upsert_hx_meta_policy_references_task"
                  title="Pass Policy Reference to PAS" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
        <HX.Section title="Fleet Soft Factors">
          <HX.With context={{
            "path": "cds/exposure/granular/vessels/hull_rating/fleet_soft_factors",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "fleet_casualty_history",
                "owner_quality"
              ]}
                horizontal={true} />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Vessels Defaults">
          <HX.Pane shownBy="/non_cds/show_hide_toggles/loh/show_loh_coverage">
            <HX.Collection fields={[
              "/non_cds/show_hide_toggles/loh/show_defaults"
            ]}
              syncColumnWidthsKey="key_1" />
          </HX.Pane>
          <HX.Pane shownBy={null}
            flow="right"
            reflow={false}>
            <HX.Pane flow="down">
              <HX.Collection fields={[
                "/cds/exposure/granular/vessels/vessels_defaults/hull/inception_date",
                "/cds/exposure/granular/vessels/vessels_defaults/hull/expiry_date"
              ]}
                syncColumnWidthsKey="key_1" />
              <HX.Pane flow="right">
                <HX.Button task="set_vessels_defaults_task"
                  title="Set Vessels Defaults" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane flow="down">
              <HX.Collection fields={[
                "/cds/exposure/granular/vessels/vessels_defaults/hull/coverage",
                "/cds/exposure/granular/vessels/vessels_defaults/hull/deductible",
                "/cds/exposure/granular/vessels/vessels_defaults/hull/order_percent"
              ]}
                syncColumnWidthsKey="key_1" />
            </HX.Pane>
            <HX.Pane flow="down"
              shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage">
              <HX.Collection fields={[
                "/cds/exposure/granular/vessels/vessels_defaults/hull/freight_conditions",
                "/cds/exposure/granular/vessels/vessels_defaults/hull/vessel_quality",
                "/cds/exposure/granular/vessels/vessels_defaults/hull/area_of_operation"
              ]}
                syncColumnWidthsKey="key_1" />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Vessels">
          <HX.Pane flow="down">
            <HX.Pane flow="right"
              reflow={false}>
              <HX.Pane flow="down"
                ratio={3}>
                <HX.Button task="clear_vessels_task"
                  title="Clear Vessels Table" />
                <HX.Collection fields={[
                  "/non_cds/show_hide_toggles/hull/show_vessels_details",
                  "cds/exposure/granular/vessels/hull_rating/fleet_size"
                ]} />
              </HX.Pane>
              <HX.Pane flow="down"
                ratio={3}>
                <HX.Button task="lookup_imos_task"
                  title="Lookup IMOs" />
                <HX.Collection fields={[
                  "/non_cds/show_hide_toggles/hull/filter_by_errors"
                ]} />
              </HX.Pane>
              <HX.Pane flow="down"
                ratio={4}>
                <HX.With context={{
                  "index": 0,
                  "path": "/cds/layers",
                  "type": "list"
                }}>
                  <HX.Collection fields={[
                    "coverages/hull/total_quoted_premium"
                  ]} />
                </HX.With>
                <HX.Collection fields={[
                  "/non_cds/labels/hull/validation_error_message",
                  {
                    "field": "/non_cds/labels/hull/data_mart_warning_message.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/hull/show_data_mart_warning"
                  },
                  {
                    "field": "/non_cds/labels/hull/duplicate_imo_and_name_message.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/hull/show_duplicate_vessel_warning"
                  }
                ]} />
              </HX.Pane>
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/exposure/granular/vessels/hull_rating/vessels_list",
              "type": "list"
            }}>
              <HX.Table maxListVisibleRows={30}
                filter="has_error"
                data={[
                "/cds/exposure/granular/vessels/hull_rating/vessels_list"
              ]}
                fields={[
                "vessel_details/imo",
                {
                  "field": "vessel_details/name",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/name"
                },
                {
                  "field": "error_validation_columns/validation_name",
                  "labelBy": "/non_cds/labels/hull/validation_name",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "inception_date",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/inception_date"
                },
                {
                  "field": "error_validation_columns/validation_inception_date",
                  "labelBy": "/non_cds/labels/hull/validation_inception_date",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "expiry_date",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/expiry_date"
                },
                {
                  "field": "error_validation_columns/validation_expiry_date",
                  "labelBy": "/non_cds/labels/hull/validation_expiry_date",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "coverage",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/coverage"
                },
                {
                  "field": "error_validation_columns/validation_coverage",
                  "labelBy": "/non_cds/labels/hull/validation_coverage",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_type",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/vessel_type"
                },
                {
                  "field": "error_validation_columns/validation_vessel_type",
                  "labelBy": "/non_cds/labels/hull/validation_vessel_type",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "agreed_value",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/agreed_value"
                },
                {
                  "field": "error_validation_columns/validation_agreed_value",
                  "labelBy": "/non_cds/labels/hull/validation_agreed_value",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/gross_tonnage",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/gross_tonnage"
                },
                {
                  "field": "error_validation_columns/validation_gross_tonnage",
                  "labelBy": "/non_cds/labels/hull/validation_gross_tonnage",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "dwt",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/dwt"
                },
                {
                  "field": "error_validation_columns/validation_dwt",
                  "labelBy": "/non_cds/labels/hull/validation_dwt",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "year_built",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/year_built"
                },
                {
                  "field": "error_validation_columns/validation_year_built",
                  "labelBy": "/non_cds/labels/hull/validation_year_built",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "flag",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/flag"
                },
                {
                  "field": "error_validation_columns/validation_flag",
                  "labelBy": "/non_cds/labels/hull/validation_flag",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/vessel_class",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/vessel_class"
                },
                {
                  "field": "error_validation_columns/validation_vessel_class",
                  "labelBy": "/non_cds/labels/hull/validation_vessel_class",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "deductible",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/deductible"
                },
                {
                  "field": "error_validation_columns/validation_deductible",
                  "labelBy": "/non_cds/labels/hull/validation_deductible",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/order_percent",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/order_percent"
                },
                {
                  "field": "error_validation_columns/validation_order_percent",
                  "labelBy": "/non_cds/labels/hull/validation_order_percent",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/freight_conditions",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/freight_conditions"
                },
                {
                  "field": "error_validation_columns/validation_freight_conditions",
                  "labelBy": "/non_cds/labels/hull/validation_freight_conditions",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/vessel_quality",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/vessel_quality"
                },
                {
                  "field": "error_validation_columns/validation_vessel_quality",
                  "labelBy": "/non_cds/labels/hull/validation_vessel_quality",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/area_of_operation",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/area_of_operation"
                },
                {
                  "field": "error_validation_columns/validation_area_of_operation",
                  "labelBy": "/non_cds/labels/hull/validation_area_of_operation",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                "behavioural_model_rate",
                {
                  "field": "behavioural_benchmark_premium",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/behavioural_benchmark_premium"
                },
                "static_model_rate",
                {
                  "field": "static_benchmark_premium",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/static_benchmark_premium"
                },
                {
                  "field": "achieved_rate",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/achieved_rate"
                },
                {
                  "field": "error_validation_columns/validation_achieved_rate",
                  "labelBy": "/non_cds/labels/hull/validation_achieved_rate",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "achieved_premium",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/achieved_premium"
                },
                {
                  "field": "average_achieved_rate",
                  "shownBy": "/cds/exposure/granular/vessels/hull_rating/is_modelling"
                },
                "uw_adjustment",
                {
                  "field": "number_of_port_visits",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "number_of_unique_port_visits",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "age",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_antarctica",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_australia_and_new_zealand",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_eastern_asia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_eastern_europe",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_high_seas",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_latin_america_and_caribbean",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_melanesia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_micronesia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_northern_africa",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_northern_america",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_northern_europe",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_polynesia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_south_eastern_asia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_southern_asia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_southern_europe",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_sub_saharan_africa",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_western_asia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_western_europe",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "change_in_fleet",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_class_changes_5yr",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "model_dwt",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "model_flag",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "model_gross_tonnage",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "max_distance_ratio",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "net_sum_insured",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "num_journeys_cut",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "num_port_visits_cut",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "perc_time_eez",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "perc_time_hrz",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "perc_time_seca",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "powerkwmax",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "ratio_anchored",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "ratio_moored",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "ratio_moving",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "total_unique_imos_owner",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "unique_journey_ratio",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "unique_port_ratio",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "ship_type",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "current_flag",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "model_ship_name",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "raw_deadweight",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "year_of_build",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "raw_grosstonnage",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "raw_ship_type",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_behavioural_data",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "mapped_vessel_type",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                }
              ]}
                kb-interactive={true}
                freezeLeft={2}
                shownBy="/non_cds/show_hide_toggles/hull/filter_by_errors" />
              <HX.Table maxListVisibleRows={30}
                data={[
                "/cds/exposure/granular/vessels/hull_rating/vessels_list"
              ]}
                fields={[
                "vessel_details/imo",
                {
                  "field": "vessel_details/name",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/name"
                },
                {
                  "field": "error_validation_columns/validation_name",
                  "labelBy": "/non_cds/labels/hull/validation_name",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "inception_date",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/inception_date"
                },
                {
                  "field": "error_validation_columns/validation_inception_date",
                  "labelBy": "/non_cds/labels/hull/validation_inception_date",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "expiry_date",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/expiry_date"
                },
                {
                  "field": "error_validation_columns/validation_expiry_date",
                  "labelBy": "/non_cds/labels/hull/validation_expiry_date",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "coverage",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/coverage"
                },
                {
                  "field": "error_validation_columns/validation_coverage",
                  "labelBy": "/non_cds/labels/hull/validation_coverage",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_type",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/vessel_type"
                },
                {
                  "field": "error_validation_columns/validation_vessel_type",
                  "labelBy": "/non_cds/labels/hull/validation_vessel_type",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "agreed_value",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/agreed_value"
                },
                {
                  "field": "error_validation_columns/validation_agreed_value",
                  "labelBy": "/non_cds/labels/hull/validation_agreed_value",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/gross_tonnage",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/gross_tonnage"
                },
                {
                  "field": "error_validation_columns/validation_gross_tonnage",
                  "labelBy": "/non_cds/labels/hull/validation_gross_tonnage",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "dwt",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/dwt"
                },
                {
                  "field": "error_validation_columns/validation_dwt",
                  "labelBy": "/non_cds/labels/hull/validation_dwt",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "year_built",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/year_built"
                },
                {
                  "field": "error_validation_columns/validation_year_built",
                  "labelBy": "/non_cds/labels/hull/validation_year_built",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "flag",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/flag"
                },
                {
                  "field": "error_validation_columns/validation_flag",
                  "labelBy": "/non_cds/labels/hull/validation_flag",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/vessel_class",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/vessel_class"
                },
                {
                  "field": "error_validation_columns/validation_vessel_class",
                  "labelBy": "/non_cds/labels/hull/validation_vessel_class",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "deductible",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/deductible"
                },
                {
                  "field": "error_validation_columns/validation_deductible",
                  "labelBy": "/non_cds/labels/hull/validation_deductible",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/order_percent",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/order_percent"
                },
                {
                  "field": "error_validation_columns/validation_order_percent",
                  "labelBy": "/non_cds/labels/hull/validation_order_percent",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/freight_conditions",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/freight_conditions"
                },
                {
                  "field": "error_validation_columns/validation_freight_conditions",
                  "labelBy": "/non_cds/labels/hull/validation_freight_conditions",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/vessel_quality",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/vessel_quality"
                },
                {
                  "field": "error_validation_columns/validation_vessel_quality",
                  "labelBy": "/non_cds/labels/hull/validation_vessel_quality",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "vessel_details/area_of_operation",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/area_of_operation"
                },
                {
                  "field": "error_validation_columns/validation_area_of_operation",
                  "labelBy": "/non_cds/labels/hull/validation_area_of_operation",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                "behavioural_model_rate",
                {
                  "field": "behavioural_benchmark_premium",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/behavioural_benchmark_premium"
                },
                "static_model_rate",
                {
                  "field": "static_benchmark_premium",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/static_benchmark_premium"
                },
                {
                  "field": "achieved_rate",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/achieved_rate"
                },
                {
                  "field": "error_validation_columns/validation_achieved_rate",
                  "labelBy": "/non_cds/labels/hull/validation_achieved_rate",
                  "shownBy": "/non_cds/show_hide_toggles/hull/filter_by_errors"
                },
                {
                  "field": "achieved_premium",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/achieved_premium"
                },
                {
                  "field": "average_achieved_rate",
                  "shownBy": "/cds/exposure/granular/vessels/hull_rating/is_modelling"
                },
                "uw_adjustment",
                {
                  "field": "number_of_port_visits",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "number_of_unique_port_visits",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "age",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_antarctica",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_australia_and_new_zealand",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_eastern_asia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_eastern_europe",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_high_seas",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_latin_america_and_caribbean",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_melanesia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_micronesia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_northern_africa",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_northern_america",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_northern_europe",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_polynesia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_south_eastern_asia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_southern_asia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_southern_europe",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_sub_saharan_africa",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_western_asia",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_aths_western_europe",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "change_in_fleet",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_class_changes_5yr",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "model_dwt",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "model_flag",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "model_gross_tonnage",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "max_distance_ratio",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "net_sum_insured",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "num_journeys_cut",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "num_port_visits_cut",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "perc_time_eez",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "perc_time_hrz",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "perc_time_seca",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "powerkwmax",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "ratio_anchored",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "ratio_moored",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "ratio_moving",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "total_unique_imos_owner",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "unique_journey_ratio",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "unique_port_ratio",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "ship_type",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "current_flag",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "model_ship_name",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "raw_deadweight",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "year_of_build",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "raw_grosstonnage",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "raw_ship_type",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "is_behavioural_data",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                },
                {
                  "field": "mapped_vessel_type",
                  "shownBy": "/non_cds/show_hide_toggles/hull/show_vessels_details"
                }
              ]}
                kb-interactive={true}
                freezeLeft={2}
                shownBy="/non_cds/show_hide_toggles/hull/not_filter_by_errors" />
            </HX.With>
            <HX.Pane>
              <HX.Collection fields={[
                {
                  "field": "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                  "shownBy": "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                }
              ]} />
            </HX.Pane>
            <HX.Pane flow="right"
              shownBy="/non_cds/show_hide_toggles/show_powersearch">
              <HX.Button task="generate_vessels_xlsx_task"
                title="Generate Vessels Excel" />
              <HX.File field="/cds/exposure/granular/vessels/hull_rating/vessels_xlsx"
                shownBy="/non_cds/show_hide_toggles/hull/show_generated_vessels_xlsx" />
              <HX.Button task="push_vessels_to_datamart_task"
                title="Push to Powersearch" />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="IV"
        fullWidth={true}
        shownBy="/non_cds/show_hide_toggles/iv/show_iv_coverage">
        <HX.With context={{
          "path": "cds/exposure/granular/vessels/hull_rating",
          "type": "struct"
        }}>
          <HX.Section title="IV Coverage">
            <HX.With context={{
              "index": 0,
              "path": "/cds/layers",
              "type": "list"
            }}>
              <HX.Section title="Inputs">
                <HX.Pane flow="down">
                  <HX.Pane flow="right">
                    <HX.Collection fields={[
                      "coverages/iv/section_reference",
                      "coverages/iv/brokerage",
                      "coverages/iv/written_line",
                      "coverages/iv/iv_lead_follow"
                    ]}
                      horizontal={true} />
                    <HX.Pane />
                  </HX.Pane>
                  <HX.Pane flow="right">
                    <HX.Collection fields={[
                      {
                        "field": "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                        "shownBy": "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                      }
                    ]} />
                    <HX.Pane />
                    <HX.Pane />
                    <HX.Pane />
                  </HX.Pane>
                  <HX.Pane flow="right">
                    <HX.Button task="upsert_hx_meta_policy_references_task"
                      title="Pass Policy Reference to PAS" />
                    <HX.Pane />
                    <HX.Pane />
                    <HX.Pane />
                    <HX.Pane />
                  </HX.Pane>
                </HX.Pane>
              </HX.Section>
            </HX.With>
            <HX.Section title="IV Vessels List">
              <HX.Pane flow="down">
                <HX.Pane flow="right">
                  <HX.With context={{
                    "index": 0,
                    "path": "/cds/layers",
                    "type": "list"
                  }}>
                    <HX.Collection fields={[
                      "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
                      "coverages/iv/iv_perc_of_h_and_m_value",
                      "coverages/iv/total_quoted_premium"
                    ]}
                      syncColumnWidthsKey="key_1"
                      horizontal={true} />
                  </HX.With>
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    "/non_cds/show_hide_toggles/iv/iv_filter_by_errors",
                    "/non_cds/labels/iv/validation_iv_error_message",
                    {
                      "field": "/non_cds/labels/hull/data_mart_warning_message.read_only_option",
                      "shownBy": "/non_cds/show_hide_toggles/hull/show_data_mart_warning"
                    }
                  ]}
                    syncColumnWidthsKey="key_1"
                    horizontal={true} />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
                <HX.Table data={[
                  "vessels_list"
                ]}
                  fields={[
                  "vessel_details/imo.read_only_option",
                  "vessel_details/name.read_only_option",
                  {
                    "field": "inception_date.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "expiry_date.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  "iv/iv_coverage",
                  {
                    "field": "iv/iv_error_validation_columns/validation_iv_coverage",
                    "labelBy": "/non_cds/labels/iv/validation_iv_coverage",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_filter_by_errors"
                  },
                  "vessel_type.read_only_option",
                  {
                    "field": "iv/iv_agreed_value",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/agreed_value"
                  },
                  {
                    "field": "iv/iv_error_validation_columns/validation_iv_agreed_value",
                    "labelBy": "/non_cds/labels/iv/validation_iv_agreed_value",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_filter_by_errors"
                  },
                  "vessel_details/gross_tonnage.read_only_option",
                  "dwt.read_only_option",
                  "year_built.read_only_option",
                  {
                    "field": "flag.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/vessel_class.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_deductible",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/deductible"
                  },
                  {
                    "field": "vessel_details/order_percent.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/freight_conditions.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/vessel_quality.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/area_of_operation.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_behavioural_model_rate",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_behavioural_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/behavioural_benchmark_premium",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_static_model_rate",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_static_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/static_benchmark_premium",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  "iv/iv_achieved_rate",
                  {
                    "field": "iv/iv_error_validation_columns/validation_iv_achieved_rate",
                    "labelBy": "/non_cds/labels/iv/validation_iv_achieved_rate",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_filter_by_errors"
                  },
                  {
                    "field": "iv/iv_achieved_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/achieved_premium"
                  },
                  "iv/iv_uw_adjustment",
                  {
                    "field": "iv/iv_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/iv_benchmark_premium"
                  },
                  "iv/iv_is_include_vessel"
                ]}
                  kb-interactive={true}
                  freezeRight={1}
                  dynamic={true}
                  shownBy="/non_cds/show_hide_toggles/iv/iv_not_filter_by_errors" />
                <HX.Table data={[
                  "vessels_list"
                ]}
                  fields={[
                  "vessel_details/imo.read_only_option",
                  "vessel_details/name.read_only_option",
                  {
                    "field": "inception_date.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "expiry_date.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  "iv/iv_coverage",
                  {
                    "field": "iv/iv_error_validation_columns/validation_iv_coverage",
                    "labelBy": "/non_cds/labels/iv/validation_iv_coverage",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_filter_by_errors"
                  },
                  "vessel_type.read_only_option",
                  {
                    "field": "iv/iv_agreed_value",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/agreed_value"
                  },
                  {
                    "field": "iv/iv_error_validation_columns/validation_iv_agreed_value",
                    "labelBy": "/non_cds/labels/iv/validation_iv_agreed_value",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_filter_by_errors"
                  },
                  "vessel_details/gross_tonnage.read_only_option",
                  "dwt.read_only_option",
                  "year_built.read_only_option",
                  {
                    "field": "flag.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/vessel_class.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_deductible",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/deductible"
                  },
                  {
                    "field": "vessel_details/order_percent.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/freight_conditions.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/vessel_quality.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/area_of_operation.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_behavioural_model_rate",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_behavioural_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/behavioural_benchmark_premium",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_static_model_rate",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "iv/iv_static_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/static_benchmark_premium",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  "iv/iv_achieved_rate",
                  {
                    "field": "iv/iv_error_validation_columns/validation_iv_achieved_rate",
                    "labelBy": "/non_cds/labels/iv/validation_iv_achieved_rate",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_filter_by_errors"
                  },
                  {
                    "field": "iv/iv_achieved_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/achieved_premium"
                  },
                  "iv/iv_uw_adjustment",
                  {
                    "field": "iv/iv_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/iv_benchmark_premium"
                  },
                  "iv/iv_is_include_vessel"
                ]}
                  kb-interactive={true}
                  freezeRight={1}
                  dynamic={true}
                  shownBy="/non_cds/show_hide_toggles/iv/iv_filter_by_errors"
                  filter="iv/iv_has_error" />
                <HX.Pane>
                  <HX.Collection fields={[
                    {
                      "field": "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                      "shownBy": "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                    }
                  ]} />
                </HX.Pane>
                <HX.Pane flow="right"
                  shownBy="/non_cds/show_hide_toggles/show_powersearch">
                  <HX.Button task="push_vessels_to_datamart_task"
                    title="Push to Powersearch" />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
              </HX.Pane>
            </HX.Section>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="War"
        fullWidth={true}
        shownBy="/non_cds/show_hide_toggles/war/show_war_coverage">
        <HX.With context={{
          "path": "cds/exposure/granular/vessels/hull_rating",
          "type": "struct"
        }}>
          <HX.Section title="War Coverage">
            <HX.With context={{
              "index": 0,
              "path": "/cds/layers",
              "type": "list"
            }}>
              <HX.Section title="Inputs">
                <HX.Pane flow="down">
                  <HX.Pane flow="right">
                    <HX.Collection fields={[
                      "coverages/war/section_reference",
                      "coverages/war/brokerage",
                      "coverages/war/written_line",
                      "coverages/war/war_lead_follow"
                    ]}
                      horizontal={true} />
                    <HX.Pane />
                  </HX.Pane>
                  <HX.Pane flow="right">
                    <HX.Collection fields={[
                      {
                        "field": "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                        "shownBy": "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                      }
                    ]} />
                    <HX.Pane />
                    <HX.Pane />
                    <HX.Pane />
                  </HX.Pane>
                  <HX.Pane flow="right">
                    <HX.Button task="upsert_hx_meta_policy_references_task"
                      title="Pass Policy Reference to PAS" />
                    <HX.Pane />
                    <HX.Pane />
                    <HX.Pane />
                    <HX.Pane />
                  </HX.Pane>
                </HX.Pane>
              </HX.Section>
            </HX.With>
            <HX.Section title="War Vessels List">
              <HX.Pane flow="down">
                <HX.Pane flow="right">
                  <HX.With context={{
                    "index": 0,
                    "path": "/cds/layers",
                    "type": "list"
                  }}>
                    <HX.Collection fields={[
                      "/non_cds/show_hide_toggles/war/war_show_vessel_details",
                      "coverages/war/total_quoted_premium"
                    ]}
                      horizontal={true} />
                  </HX.With>
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    "/non_cds/show_hide_toggles/war/war_filter_by_errors",
                    "/non_cds/labels/war/validation_war_error_message",
                    {
                      "field": "/non_cds/labels/hull/data_mart_warning_message.read_only_option",
                      "shownBy": "/non_cds/show_hide_toggles/hull/show_data_mart_warning"
                    }
                  ]}
                    horizontal={true} />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
                <HX.Table data={[
                  "vessels_list"
                ]}
                  fields={[
                  "vessel_details/imo.read_only_option",
                  "vessel_details/name.read_only_option",
                  {
                    "field": "inception_date.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "expiry_date.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  "war/war_coverage",
                  {
                    "field": "war/war_error_validation_columns/validation_war_coverage",
                    "labelBy": "/non_cds/labels/war/validation_war_coverage",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_filter_by_errors"
                  },
                  "vessel_type.read_only_option",
                  {
                    "field": "war/war_agreed_value",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/agreed_value"
                  },
                  {
                    "field": "war/war_error_validation_columns/validation_war_agreed_value",
                    "labelBy": "/non_cds/labels/war/validation_war_agreed_value",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_filter_by_errors"
                  },
                  "vessel_details/gross_tonnage.read_only_option",
                  "dwt.read_only_option",
                  "year_built.read_only_option",
                  {
                    "field": "flag.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/vessel_class.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/order_percent.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/freight_conditions.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/vessel_quality.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/area_of_operation.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "war/war_behavioural_model_rate",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "war/war_behavioural_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/behavioural_benchmark_premium",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "war/war_static_model_rate",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "war/war_static_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/static_benchmark_premium",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  "war/war_achieved_rate",
                  {
                    "field": "war/war_error_validation_columns/validation_war_achieved_rate",
                    "labelBy": "/non_cds/labels/war/validation_war_achieved_rate",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_filter_by_errors"
                  },
                  {
                    "field": "war/war_achieved_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/achieved_premium"
                  },
                  "war/war_uw_adjustment",
                  {
                    "field": "war/war_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/war_benchmark_premium"
                  },
                  "war/war_is_include_vessel"
                ]}
                  title="Vessels"
                  kb-interactive={true}
                  freezeRight={1}
                  dynamic={true}
                  shownBy="/non_cds/show_hide_toggles/war/war_not_filter_by_errors" />
                <HX.Table data={[
                  "vessels_list"
                ]}
                  fields={[
                  "vessel_details/imo.read_only_option",
                  "vessel_details/name.read_only_option",
                  {
                    "field": "inception_date.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "expiry_date.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  "war/war_coverage",
                  {
                    "field": "war/war_error_validation_columns/validation_war_coverage",
                    "labelBy": "/non_cds/labels/war/validation_war_coverage",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_filter_by_errors"
                  },
                  "vessel_type.read_only_option",
                  {
                    "field": "war/war_agreed_value",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/agreed_value"
                  },
                  {
                    "field": "war/war_error_validation_columns/validation_war_agreed_value",
                    "labelBy": "/non_cds/labels/war/validation_war_agreed_value",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_filter_by_errors"
                  },
                  "vessel_details/gross_tonnage.read_only_option",
                  "dwt.read_only_option",
                  "year_built.read_only_option",
                  {
                    "field": "flag.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/vessel_class.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/order_percent.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/freight_conditions.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/vessel_quality.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "vessel_details/area_of_operation.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "war/war_behavioural_model_rate",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "war/war_behavioural_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/behavioural_benchmark_premium",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  {
                    "field": "war/war_static_model_rate",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_show_vessel_details"
                  },
                  {
                    "field": "war/war_static_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/static_benchmark_premium",
                    "shownBy": "/non_cds/show_hide_toggles/iv/iv_show_vessel_details"
                  },
                  "war/war_achieved_rate",
                  {
                    "field": "war/war_error_validation_columns/validation_war_achieved_rate",
                    "labelBy": "/non_cds/labels/war/validation_war_achieved_rate",
                    "shownBy": "/non_cds/show_hide_toggles/war/war_filter_by_errors"
                  },
                  {
                    "field": "war/war_achieved_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/achieved_premium"
                  },
                  "war/war_uw_adjustment",
                  {
                    "field": "war/war_benchmark_premium",
                    "labelBy": "/non_cds/labels/required_vessels_columns_labels/war_benchmark_premium"
                  },
                  "war/war_is_include_vessel"
                ]}
                  title="Vessels"
                  kb-interactive={true}
                  freezeRight={1}
                  dynamic={true}
                  shownBy="/non_cds/show_hide_toggles/war/war_filter_by_errors"
                  filter="war/war_has_error" />
                <HX.Pane>
                  <HX.Collection fields={[
                    {
                      "field": "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                      "shownBy": "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                    }
                  ]} />
                </HX.Pane>
                <HX.Pane flow="right"
                  shownBy="/non_cds/show_hide_toggles/show_powersearch">
                  <HX.Button task="push_vessels_to_datamart_task"
                    title="Push to Powersearch" />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
              </HX.Pane>
            </HX.Section>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Loss of Hire (LOH)"
        shownBy="/non_cds/show_hide_toggles/loh/show_loh_coverage"
        fullWidth={true}>
        <HX.With context={{
          "path": "cds/exposure/granular/vessels",
          "type": "struct"
        }}>
          <HX.With context={{
            "index": 0,
            "path": "/cds/layers",
            "type": "list"
          }}>
            <HX.Section title="Inputs">
              <HX.Pane flow="down">
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    "coverages/loh/section_reference",
                    "coverages/loh/brokerage",
                    {
                      "field": "coverages/loh/other_deductions",
                      "infoBy": "/non_cds/tooltips/shipbuilders/other_deductions",
                      "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                    },
                    "coverages/loh/written_line",
                    {
                      "field": "coverages/loh/loh_is_war_cover",
                      "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                    },
                    {
                      "field": "/non_cds/show_hide_toggles/ship_building/show_ship_builders_actuarial_pricing",
                      "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                    },
                    {
                      "field": "coverages/loh/loh_achieved_premium",
                      "labelBy": "/non_cds/labels/loh/achieved_premium_label",
                      "shownBy": "/non_cds/show_hide_toggles/loh/show_loh_coverage"
                    }
                  ]}
                    horizontal={true} />
                  <HX.Pane />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    {
                      "field": "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                      "shownBy": "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                    }
                  ]} />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Button task="upsert_hx_meta_policy_references_task"
                    title="Pass Policy Reference to PAS" />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.Section title="Vessels Defaults">
            <HX.Pane shownBy="/non_cds/show_hide_toggles/loh/show_loh_coverage">
              <HX.Collection fields={[
                "/non_cds/show_hide_toggles/loh/show_defaults"
              ]}
                syncColumnWidthsKey="key_1" />
            </HX.Pane>
            <HX.Pane shownBy="/non_cds/show_hide_toggles/loh/show_defaults"
              flow="right"
              reflow={false}>
              <HX.Pane flow="down">
                <HX.Collection fields={[
                  {
                    "field": "/cds/exposure/granular/vessels/vessels_defaults/loh/loh_daily_rate",
                    "labelBy": "/non_cds/labels/currency_loh_daily_rate_label"
                  },
                  "/cds/exposure/granular/vessels/vessels_defaults/loh/loh_uw_adjustment"
                ]}
                  syncColumnWidthsKey="key_1" />
                <HX.Pane flow="right">
                  <HX.Button task="set_loh_vessels_defaults_task"
                    title="Set Vessels Defaults" />
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="down">
                <HX.Collection fields={[
                  "/cds/exposure/granular/vessels/vessels_defaults/loh/loh_xs_days",
                  "/cds/exposure/granular/vessels/vessels_defaults/loh/loh_cover"
                ]}
                  syncColumnWidthsKey="key_1" />
              </HX.Pane>
              <HX.Pane flow="down"
                shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage">
                <HX.Collection fields={[
                  "/cds/exposure/granular/vessels/vessels_defaults/loh/freight_conditions",
                  "/cds/exposure/granular/vessels/vessels_defaults/loh/vessel_quality",
                  "/cds/exposure/granular/vessels/vessels_defaults/loh/area_of_operation"
                ]}
                  syncColumnWidthsKey="key_1" />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="LOH Vessels">
            <HX.With context={{
              "index": 0,
              "path": "/cds/layers",
              "type": "list"
            }}>
              <HX.Pane flow="down">
                <HX.Pane flow="right">
                  <HX.Button task="clear_loh_vessels_task"
                    title="Clear Vessels Table" />
                  <HX.Button task="lookup_loh_imos_task"
                    title="Lookup IMOs" />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    {
                      "field": "coverages/loh/loh_total_sum_insured",
                      "labelBy": "/cds/currency_loh_total_sum_insured_label"
                    },
                    "coverages/loh/loh_fleet_level",
                    {
                      "field": "coverages/loh/loh_total_premium",
                      "labelBy": "/non_cds/labels/loh/total_benchmark_premium_label"
                    }
                  ]}
                    horizontal={true}
                    syncColumnWidthsKey="key_1" />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    {
                      "field": "/non_cds/labels/loh/loh_vessels_number_greater_than_one_warning",
                      "shownBy": "/non_cds/show_hide_toggles/loh/show_number_of_vessels_warning"
                    },
                    {
                      "field": "/non_cds/labels/loh/data_mart_warning_message.read_only_option",
                      "shownBy": "/non_cds/show_hide_toggles/loh/show_data_mart_warning"
                    }
                  ]}
                    horizontal={true} />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
                <HX.Table data={[
                  "/cds/exposure/granular/vessels/loh_rating/loh_vessels_list"
                ]}
                  fields={[
                  {
                    "field": "loh_number_of_vessels",
                    "infoBy": "/non_cds/tooltips/loh/number_of_vessels"
                  },
                  "loh_vessel_details/loh_name",
                  "loh_vessel_details/loh_imo",
                  "loh_vessel_details/loh_vessel_type",
                  "loh_vessel_details/loh_year_built",
                  "loh_vessel_details/loh_gross_tonnage",
                  "loh_vessel_details/loh_dwt",
                  {
                    "field": "loh_daily_rate",
                    "labelBy": "/non_cds/labels/currency_loh_daily_rate_label"
                  },
                  "loh_xs_days",
                  "loh_cover",
                  "loh_conditions",
                  "loh_uw_adjustment",
                  {
                    "field": "loh_sum_insured",
                    "labelBy": "/cds/currency_loh_total_sum_insured_label"
                  },
                  "loh_vessel_base_rate",
                  "loh_vessel_daily_rate",
                  {
                    "field": "loh_benchmark_premium",
                    "labelBy": "/non_cds/labels/currency_loh_benchmark_premium_label"
                  },
                  "loh_vessel_achieved_rate"
                ]}
                  title=""
                  kb-interactive={true}
                  dynamic={true} />
                <HX.Pane>
                  <HX.Collection fields={[
                    {
                      "field": "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                      "shownBy": "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                    }
                  ]} />
                </HX.Pane>
                <HX.Pane flow="right"
                  shownBy="/non_cds/show_hide_toggles/show_powersearch">
                  <HX.Button task="push_vessels_to_datamart_task"
                    title="Push to Powersearch" />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
              </HX.Pane>
            </HX.With>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Shipbuilders - Exposure Rating"
        shownBy="/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
        fullWidth={true}>
        <HX.With context={{
          "index": 0,
          "path": "/cds/layers",
          "type": "list"
        }}>
          <HX.With context={{
            "index": 0,
            "path": "/cds/layers",
            "type": "list"
          }}>
            <HX.Section title="Inputs">
              <HX.Pane flow="down">
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    "coverages/ship_building/section_reference",
                    "coverages/ship_building/brokerage",
                    {
                      "field": "coverages/ship_building/other_deductions",
                      "infoBy": "/non_cds/tooltips/shipbuilders/other_deductions",
                      "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                    },
                    "coverages/ship_building/written_line",
                    {
                      "field": "coverages/ship_building/ship_building_is_war_cover",
                      "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                    },
                    {
                      "field": "/non_cds/show_hide_toggles/ship_building/show_ship_builders_actuarial_pricing",
                      "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                    },
                    {
                      "field": "coverages/loh/loh_achieved_premium",
                      "labelBy": "/non_cds/labels/loh/achieved_premium_label",
                      "shownBy": "/non_cds/show_hide_toggles/loh/show_loh_coverage"
                    }
                  ]}
                    horizontal={true} />
                  <HX.Pane />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    {
                      "field": "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                      "shownBy": "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                    }
                  ]} />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Button task="upsert_hx_meta_policy_references_task"
                    title="Pass Policy Reference to PAS" />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.Section title="Shipbuilders Vessels">
            <HX.Pane flow="down">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "coverages/ship_building/ship_building_policy_details"
                ]}
                  horizontal={true}
                  syncColumnWidthsKey="key_1" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  {
                    "field": "/non_cds/labels/shipbuilders/shipbuilders_vessels_number_greater_than_one_warning",
                    "shownBy": "/non_cds/show_hide_toggles/ship_building/show_number_of_vessels_warning"
                  }
                ]}
                  horizontal={true} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table data={[
                "/cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list"
              ]}
                fields={[
                "ship_building_vessel_type",
                {
                  "field": "ship_building_number_of_vessels",
                  "infoBy": "/non_cds/tooltips/shipbuilders/number_of_vessels"
                },
                "ship_building_vessel_name",
                "ship_building_attachment_date",
                "ship_building_delivery_date",
                {
                  "field": "ship_building_total_months_steel_cutting_keel_laying",
                  "shownBy": "coverages/ship_building/ship_building_show_production_stages_time"
                },
                {
                  "field": "ship_building_total_months_keel_laying_launch",
                  "shownBy": "coverages/ship_building/ship_building_show_production_stages_time"
                },
                {
                  "field": "ship_building_total_months_launch_delivery",
                  "shownBy": "coverages/ship_building/ship_building_show_production_stages_time"
                },
                {
                  "field": "ship_building_total_months_all_stages",
                  "shownBy": "coverages/ship_building/ship_building_show_overall_time"
                },
                "ship_building_country",
                "ship_building_survey_grade",
                "ship_building_deductible",
                "ship_building_sum_insured",
                "ship_building_benchmark_rate"
              ]}
                title=""
                kb-interactive={true}
                dynamic={true}
                maxListVisibleRows={20} />
              <HX.Table title="Actuarial Pricing"
                kb-interactive={true}
                dynamic={true}
                maxListVisibleRows={20}
                data={[
                "/cds/exposure/granular/vessels/ship_building_rating/ship_building_pricing_vessels_list"
              ]}
                shownBy="/non_cds/show_hide_toggles/ship_building/show_ship_builders_actuarial_pricing"
                fields={[
                "ship_building_pricing_overall_process_base_rate",
                "ship_building_pricing_base_rate_steel_cutting_keel_laying",
                "ship_building_pricing_base_rate_keel_laying_launch",
                "ship_building_pricing_base_rate_launch_delivery",
                "ship_building_pricing_base_rate_non_war",
                "ship_building_pricing_vessel_type",
                "ship_building_pricing_country",
                "ship_building_pricing_survey_grade",
                "ship_building_pricing_deductible",
                "ship_building_pricing_non_war_premium_net_rate",
                "ship_building_pricing_war_premium_net_rate",
                "ship_building_pricing_total_exposure_net_rate_pre_fleet",
                "ship_building_pricing_fleet_discount",
                "ship_building_pricing_total_exposure_net_rate",
                "ship_building_pricing_exposure_net_premium"
              ]} />
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  {
                    "field": "coverages/ship_building/ship_building_achieved_premium",
                    "labelBy": "/non_cds/labels/ship_building/achieved_premium"
                  },
                  {
                    "field": "coverages/ship_building/ship_building_net_benchmark_premium_pre_uw_adj",
                    "labelBy": "/non_cds/labels/ship_building/exposure_benchmark_premium"
                  },
                  {
                    "field": "coverages/ship_building/ship_building_experience_premium",
                    "infoBy": "/non_cds/tooltips/shipbuilders/experience_premium",
                    "labelBy": "/non_cds/labels/ship_building/experience_benchmark_premium"
                  },
                  {
                    "field": "coverages/ship_building/ship_building_experience_weighting",
                    "infoBy": "/non_cds/tooltips/shipbuilders/credibility",
                    "labelBy": "/non_cds/labels/ship_building/weight_to_experience"
                  },
                  {
                    "field": "coverages/ship_building/ship_building_blended_benchmark_premium_pre_uw_adj",
                    "labelBy": "/non_cds/labels/ship_building/blended_premium_pre_adj"
                  },
                  "coverages/ship_building/ship_building_uw_adjustment",
                  {
                    "field": "coverages/ship_building/ship_building_blended_benchmark_premium_post_uw_adj",
                    "labelBy": "/non_cds/labels/ship_building/blended_premium_post_adj"
                  }
                ]}
                  syncColumnWidthsKey="key_1" />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Shipbuilders - Experience Rating"
        fullWidth={true}
        with="cds/exposure/granular/vessels"
        shownBy="/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage">
        <HX.With context={{
          "path": "cds/experience_rating/ship_building",
          "type": "struct"
        }}>
          <HX.Section title="Data Input">
            <HX.Pane flow="down">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "claims_date"
                ]} />
                <HX.Button title="Populate BI Data"
                  task="populate_bi_data" />
                <HX.Collection fields={[
                  "claims_currency",
                  {
                    "field": "claims_fx_rate",
                    "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_exchange_rate_label"
                  }
                ]} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection shownBy="/non_cds/show_hide_toggles/ship_building/show_experience_rating_warning"
                  fields={[
                  {
                    "field": "/non_cds/labels/shipbuilders/experience_signed_line_warning.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/ship_building/show_experience_signed_line_warning"
                  },
                  {
                    "field": "/non_cds/labels/shipbuilders/number_of_vessels_warning.read_only_option",
                    "shownBy": "/non_cds/show_hide_toggles/ship_building/show_experience_number_of_vessels_warning"
                  }
                ]} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table freezeLeft={1}
                data={[
                "data_input_experience_table"
              ]}
                fields={[
                "yoa",
                "previous_insurer",
                "number_of_vessels",
                {
                  "field": "premium",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_gross_premium_label"
                },
                "acquisition_cost",
                {
                  "field": "net_premium_shared_line",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_net_premium_shared_line_label"
                },
                {
                  "field": "total_incurred_shared_line",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_total_incurred_label"
                },
                {
                  "field": "att_incurred_shared_line",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_att_incurred_label"
                },
                {
                  "field": "large_incurred_shared_line",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_data_input_large_incurred_label"
                },
                "signed_line",
                "rate_change",
                "is_include_year"
              ]}
                kb-interactive={true}
                freezeRight={1}
                dynamic={true} />
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  {
                    "field": "current_year_rate_change",
                    "labelBy": "/non_cds/labels/ship_building/experience_rating/current_year_experience_rating_rate_change_label"
                  }
                ]} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="ULR Projection"
            defaultCollapsed={true}>
            <HX.Pane flow="down">
              <HX.Table freezeLeft={1}
                data={[
                "ulr_projection_experience_table"
              ]}
                fields={[
                "yoa",
                {
                  "field": "premium",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_net_premium_label"
                },
                {
                  "field": "att_incurred_shared_line",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_att_incurred_label"
                },
                {
                  "field": "large_incurred_shared_line",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_large_incurred_label"
                },
                "rate_change",
                "rate_change_cumulative",
                {
                  "field": "on_levelled_premium",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_on_levelled_net_premium_label"
                },
                "claims_inflation_yoy",
                "claims_inflation_cumulative",
                {
                  "field": "on_levelled_att_incurred_shared_line",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_on_levelled_att_incurred_label"
                },
                "on_levelled_att_incurred_lr",
                {
                  "field": "on_levelled_large_incurred_shared_line",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_rating_projection_on_levelled_large_claims_label"
                },
                "on_levelled_large_incurred_lr",
                "development_month",
                "development_percent",
                "attritional_ulr",
                "is_include_year"
              ]}
                kb-interactive={true}
                dynamic={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Large Load Selection">
            <HX.With context={{
              "path": "large_load_selection",
              "type": "struct"
            }}>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "average_on_levelled_net_large_lr"
                ]}
                  title="From Experience" />
                <HX.Collection fields={[
                  "user_selected/user_number_of_years_expected_large_loss",
                  "user_selected/user_average_net_lr_of_large_loss",
                  "user_selected/selected_large_load"
                ]}
                  title="User Selected" />
                <HX.Collection fields={[
                  "portfolio_load_guidance/guidance_number_of_years_expected_large_loss",
                  "portfolio_load_guidance/guidance_average_net_lr_of_large_loss",
                  "portfolio_load_guidance/portfolio_large_load"
                ]}
                  title="Portfolio Load - Guidance" />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.With>
          </HX.Section>
          <HX.Section title="Experience Pricing Results 100% Share">
            <HX.Pane flow="right">
              <HX.Collection with="experience_pricing_results"
                fields={[
                "average_attritional_ulr",
                "large_load",
                "total_ulr",
                {
                  "field": "experience_claims_cost",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_claims_cost_label"
                },
                {
                  "field": "net_benchmark_premium_pure_experience",
                  "labelBy": "/non_cds/labels/ship_building/experience_rating/currency_experience_claims_net_benchmark_premium_pure_experience"
                }
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Experience Pricing Weighting Calculation">
            <HX.Pane flow="right">
              <HX.Collection with="experience_weighting_calculation"
                fields={[
                "total_number_of_vessels",
                "experience_weighting"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rating Summary"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="UW Comment">
          <HX.Notes field="cds/uw_comment" />
        </HX.Section>
        <HX.Section title="Coverage Options">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane shownBy="/non_cds/show_rating_summary_table/show_hull_table">
              <HX.Table title="Priced Quotes"
                data={[
                {
                  "datum": "coverages/hull"
                }
              ]}
                fields={[
                "status",
                "section_reference",
                "rating_summary_brokerage",
                {
                  "field": "other_deductions.read_only_option",
                  "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                },
                "rating_summary_written_line",
                null,
                {
                  "field": "quoted_premium_pro_rated_100pct",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "quoted_premium_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                "technical_premium_pro_rated_100pct",
                {
                  "field": "technical_premium_pre_uw_adj_pro_rated_100pct"
                },
                {
                  "field": "benchmark_premium_pro_rated_100pct"
                },
                null,
                "tpi",
                {
                  "field": "tpi_pre_uw_adj"
                },
                {
                  "field": "bpi",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "bpi_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                "pflr",
                "roc",
                {
                  "field": "uw_adj_impact",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                }
              ]}
                freezeLeft={0}
                transpose={true}
                key={0} />
            </HX.Pane>
            <HX.Pane shownBy="/non_cds/show_rating_summary_table/show_hull_iv_war_table">
              <HX.Table title="Priced Quotes"
                data={[
                {
                  "datum": "coverages/hull"
                },
                {
                  "datum": "coverages/iv"
                },
                {
                  "datum": "coverages/war"
                }
              ]}
                fields={[
                "status",
                "section_reference",
                "rating_summary_brokerage",
                {
                  "field": "other_deductions.read_only_option",
                  "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                },
                "rating_summary_written_line",
                null,
                {
                  "field": "quoted_premium_pro_rated_100pct",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "quoted_premium_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                "technical_premium_pro_rated_100pct",
                {
                  "field": "technical_premium_pre_uw_adj_pro_rated_100pct"
                },
                {
                  "field": "benchmark_premium_pro_rated_100pct"
                },
                null,
                "tpi",
                {
                  "field": "tpi_pre_uw_adj"
                },
                {
                  "field": "bpi",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "bpi_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                "pflr",
                "roc",
                {
                  "field": "uw_adj_impact",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                }
              ]}
                freezeLeft={0}
                transpose={true}
                key={1} />
            </HX.Pane>
            <HX.Pane shownBy="/non_cds/show_rating_summary_table/show_hull_iv_table">
              <HX.Table title="Priced Quotes"
                data={[
                {
                  "datum": "coverages/hull"
                },
                {
                  "datum": "coverages/iv"
                }
              ]}
                fields={[
                "status",
                "section_reference",
                "rating_summary_brokerage",
                {
                  "field": "other_deductions.read_only_option",
                  "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                },
                "rating_summary_written_line",
                null,
                {
                  "field": "quoted_premium_pro_rated_100pct",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "quoted_premium_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                "technical_premium_pro_rated_100pct",
                {
                  "field": "technical_premium_pre_uw_adj_pro_rated_100pct"
                },
                {
                  "field": "benchmark_premium_pro_rated_100pct"
                },
                null,
                "tpi",
                {
                  "field": "tpi_pre_uw_adj"
                },
                {
                  "field": "bpi",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "bpi_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                "pflr",
                "roc",
                {
                  "field": "uw_adj_impact",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                }
              ]}
                freezeLeft={0}
                transpose={true}
                key={2} />
            </HX.Pane>
            <HX.Pane shownBy="/non_cds/show_rating_summary_table/show_hull_war_table">
              <HX.Table title="Priced Quotes"
                data={[
                {
                  "datum": "coverages/hull"
                },
                {
                  "datum": "coverages/war"
                }
              ]}
                fields={[
                "status",
                "section_reference",
                "rating_summary_brokerage",
                {
                  "field": "other_deductions.read_only_option",
                  "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                },
                "rating_summary_written_line",
                null,
                {
                  "field": "quoted_premium_pro_rated_100pct",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "quoted_premium_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                "technical_premium_pro_rated_100pct",
                {
                  "field": "technical_premium_pre_uw_adj_pro_rated_100pct"
                },
                {
                  "field": "benchmark_premium_pro_rated_100pct"
                },
                null,
                "tpi",
                {
                  "field": "tpi_pre_uw_adj"
                },
                {
                  "field": "bpi",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "bpi_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                "pflr",
                "roc",
                {
                  "field": "uw_adj_impact",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                }
              ]}
                freezeLeft={0}
                transpose={true}
                key={3} />
            </HX.Pane>
            <HX.Pane shownBy="/non_cds/show_rating_summary_table/show_loh_table">
              <HX.Table title="Priced Quotes"
                data={[
                {
                  "datum": "coverages/loh"
                }
              ]}
                fields={[
                "status",
                "section_reference",
                "rating_summary_brokerage",
                {
                  "field": "other_deductions.read_only_option",
                  "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                },
                "rating_summary_written_line",
                null,
                {
                  "field": "quoted_premium_pro_rated_100pct",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "quoted_premium_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                "technical_premium_pro_rated_100pct",
                {
                  "field": "technical_premium_pre_uw_adj_pro_rated_100pct"
                },
                {
                  "field": "benchmark_premium_pro_rated_100pct"
                },
                null,
                "tpi",
                {
                  "field": "tpi_pre_uw_adj"
                },
                {
                  "field": "bpi",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "bpi_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                "pflr",
                "roc",
                {
                  "field": "uw_adj_impact",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                }
              ]}
                freezeLeft={0}
                transpose={true}
                key={4} />
            </HX.Pane>
            <HX.Pane shownBy="/non_cds/show_rating_summary_table/show_ship_building_table">
              <HX.Table title="Priced Quotes"
                data={[
                {
                  "datum": "coverages/ship_building"
                }
              ]}
                fields={[
                "status",
                "section_reference",
                "rating_summary_brokerage",
                {
                  "field": "other_deductions.read_only_option",
                  "shownBy": "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                },
                "rating_summary_written_line",
                null,
                {
                  "field": "quoted_premium_pro_rated_100pct",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "quoted_premium_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                "technical_premium_pro_rated_100pct",
                {
                  "field": "technical_premium_pre_uw_adj_pro_rated_100pct"
                },
                {
                  "field": "benchmark_premium_pro_rated_100pct"
                },
                null,
                "tpi",
                {
                  "field": "tpi_pre_uw_adj"
                },
                {
                  "field": "bpi",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "bpi_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                "pflr",
                "roc",
                {
                  "field": "uw_adj_impact",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                }
              ]}
                freezeLeft={0}
                transpose={true}
                key={5} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Export to Excel">
          <HX.Pane flow="right">
            <HX.Button title="Generate Output Summary"
              task="generate_rating_summary_xlsx_task" />
            <HX.File field="cds/exposure/granular/vessels/hull_rating/output_summary_xlsx"
              shownBy="/non_cds/show_hide_toggles/hull/show_generated_output_summary_xlsx" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={true}
        shownBy="cds/standard_fields/is_renewal"
        viewScale={0.9}>
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id"
            ]} />
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane />
        </HX.Section>
        <HX.Section title="Renewal"
          shownBy="cds/rate_change/show_layer_1">
          <HX.Pane flow="right">
            <HX.Button task="rarc_task"
              title="Calculate Rate Change"
              shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Notes with="cds/rate_change"
              field="rarc_note_for_uw"
              shownBy="/non_cds/show_hide_toggles/rate_change/show_rarc_note_for_uw" />
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table title="Hull"
                data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                "benchmark_premium",
                "bpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                }
              ]}
                with="rate_change/hull"
                shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage"
                kb-interactive={true} />
              <HX.Table title="Iv"
                data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                "benchmark_premium",
                "bpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                }
              ]}
                with="rate_change/iv"
                shownBy="/non_cds/show_hide_toggles/iv/show_iv_coverage"
                kb-interactive={true} />
              <HX.Table title="War"
                data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                "benchmark_premium",
                "bpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                }
              ]}
                with="rate_change/war"
                shownBy="/non_cds/show_hide_toggles/war/show_war_coverage"
                kb-interactive={true} />
              <HX.Table title="Loss of Hire (LOH)"
                data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                "benchmark_premium",
                "bpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                }
              ]}
                with="rate_change/loh"
                shownBy="/non_cds/show_hide_toggles/loh/show_loh_coverage"
                kb-interactive={true} />
              <HX.Table title="Shipbuilders"
                data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                "benchmark_premium",
                "bpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                }
              ]}
                with="rate_change/ship_building"
                shownBy="/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane shownBy="rate_change/hull/rarc_calcs_show">
                <HX.Table title="Hull Rate Change"
                  shownBy="/cds/standard_fields/is_rater_priced"
                  data={[
                  "exposure_change",
                  "risk_characteristics_change",
                  "deductible_change",
                  "limit_change",
                  "terms_conditions_change",
                  "brokerage_change",
                  "other_change",
                  null,
                  "rate_change"
                ]}
                  fields={[
                  {
                    "field": "model_calculated",
                    "width": 125
                  },
                  {
                    "field": "uw_selected",
                    "width": 125
                  },
                  {
                    "field": "comments",
                    "width": 250
                  }
                ]}
                  with="rate_change/hull"
                  kb-interactive={true} />
                <HX.Collection title="Hull Final Rate Change (Gross Brokerage)"
                  with="rate_change"
                  fields={[
                  "hull/risk_adjusted_rate_change_uw_selected/uw_selected",
                  null
                ]}
                  horizontal={true}
                  shownBy="/cds/standard_fields/is_rater_priced" />
              </HX.Pane>
              <HX.Pane shownBy="rate_change/iv/rarc_calcs_show">
                <HX.Table title="IV Rate Change"
                  shownBy="/cds/standard_fields/is_rater_priced"
                  data={[
                  "exposure_change",
                  "risk_characteristics_change",
                  "deductible_change",
                  "limit_change",
                  "terms_conditions_change",
                  "brokerage_change",
                  "other_change",
                  null,
                  "rate_change"
                ]}
                  fields={[
                  {
                    "field": "model_calculated",
                    "width": 125
                  },
                  {
                    "field": "uw_selected",
                    "width": 125
                  },
                  {
                    "field": "comments",
                    "width": 250
                  }
                ]}
                  with="rate_change/iv"
                  kb-interactive={true} />
                <HX.Collection title="IV Final Rate Change (Gross Brokerage)"
                  with="rate_change"
                  fields={[
                  "iv/risk_adjusted_rate_change_uw_selected/uw_selected",
                  null
                ]}
                  horizontal={true}
                  shownBy="/cds/standard_fields/is_rater_priced" />
              </HX.Pane>
              <HX.Pane shownBy="rate_change/war/rarc_calcs_show">
                <HX.Table title="War Rate Change"
                  shownBy="/cds/standard_fields/is_rater_priced"
                  data={[
                  "exposure_change",
                  "risk_characteristics_change",
                  "deductible_change",
                  "limit_change",
                  "terms_conditions_change",
                  "brokerage_change",
                  "other_change",
                  null,
                  "rate_change"
                ]}
                  fields={[
                  {
                    "field": "model_calculated",
                    "width": 125
                  },
                  {
                    "field": "uw_selected",
                    "width": 125
                  },
                  {
                    "field": "comments",
                    "width": 250
                  }
                ]}
                  with="rate_change/war"
                  kb-interactive={true} />
                <HX.Collection title="War Final Rate Change (Gross Brokerage)"
                  with="rate_change"
                  fields={[
                  "war/risk_adjusted_rate_change_uw_selected/uw_selected",
                  null
                ]}
                  horizontal={true}
                  shownBy="/cds/standard_fields/is_rater_priced" />
              </HX.Pane>
              <HX.Pane shownBy="rate_change/loh/rarc_calcs_show">
                <HX.Table title="Loss of Hire (LOH) Rate Change"
                  shownBy="/cds/standard_fields/is_rater_priced"
                  data={[
                  "exposure_change",
                  "risk_characteristics_change",
                  "deductible_change",
                  "limit_change",
                  "terms_conditions_change",
                  "brokerage_change",
                  "other_change",
                  null,
                  "rate_change"
                ]}
                  fields={[
                  {
                    "field": "model_calculated",
                    "width": 125
                  },
                  {
                    "field": "uw_selected",
                    "width": 125
                  },
                  {
                    "field": "comments",
                    "width": 250
                  }
                ]}
                  with="rate_change/loh"
                  kb-interactive={true} />
                <HX.Collection title="LOH Final Rate Change (Gross Brokerage)"
                  with="rate_change"
                  fields={[
                  "loh/risk_adjusted_rate_change_uw_selected/uw_selected",
                  null
                ]}
                  horizontal={true}
                  shownBy="/cds/standard_fields/is_rater_priced" />
              </HX.Pane>
              <HX.Pane shownBy="rate_change/ship_building/rarc_calcs_show">
                <HX.Table title="Shipbuilders Rate Change"
                  shownBy="/cds/standard_fields/is_rater_priced"
                  data={[
                  "exposure_change",
                  "risk_characteristics_change",
                  "deductible_change",
                  "limit_change",
                  "terms_conditions_change",
                  "brokerage_change",
                  "other_change",
                  null,
                  "rate_change"
                ]}
                  fields={[
                  {
                    "field": "model_calculated",
                    "width": 125
                  },
                  {
                    "field": "uw_selected",
                    "width": 125
                  },
                  {
                    "field": "comments",
                    "width": 250
                  }
                ]}
                  with="rate_change/ship_building"
                  kb-interactive={true} />
                <HX.Collection title="Shipbuilders Final Rate Change (Gross Brokerage)"
                  with="rate_change"
                  fields={[
                  "ship_building/risk_adjusted_rate_change_uw_selected/uw_selected",
                  null
                ]}
                  horizontal={true}
                  shownBy="/cds/standard_fields/is_rater_priced" />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Rate Change"
          shownBy="/cds/standard_fields/is_case_priced">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection title="Hull Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={[
                "hull/risk_adjusted_rate_change_case_priced/uw_selected",
                null
              ]}
                shownBy="hull/rarc_calcs_show"
                horizontal={true} />
              <HX.Collection title="IV Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={[
                "iv/risk_adjusted_rate_change_case_priced/uw_selected",
                null
              ]}
                shownBy="iv/rarc_calcs_show"
                horizontal={true} />
              <HX.Collection title="War Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={[
                "war/risk_adjusted_rate_change_case_priced/uw_selected",
                null
              ]}
                shownBy="war/rarc_calcs_show"
                horizontal={true} />
              <HX.Collection title="LOH Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={[
                "loh/risk_adjusted_rate_change_case_priced/uw_selected",
                null
              ]}
                shownBy="loh/rarc_calcs_show"
                horizontal={true} />
              <HX.Collection title="Shipbuilders Final Rate Change (Gross Brokerage)"
                with="rate_change"
                fields={[
                "ship_building/risk_adjusted_rate_change_case_priced/uw_selected",
                null
              ]}
                shownBy="ship_building/rarc_calcs_show"
                horizontal={true} />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Export to Excel"
          shownBy="/non_cds/show_hide_toggles/rate_change/show_generate_output_summary_button">
          <HX.Pane flow="right">
            <HX.Button title="Generate Output Summary"
              task="generate_rating_summary_xlsx_task" />
            <HX.File field="cds/exposure/granular/vessels/hull_rating/output_summary_xlsx"
              shownBy="/non_cds/show_hide_toggles/hull/show_generated_output_summary_xlsx" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Modelling"
        shownBy="/non_cds/show_hide_toggles/hull/show_modelling_page">
        <HX.With context={{
          "path": "cds/exposure/granular/vessels/hull_rating",
          "type": "struct"
        }}>
          <HX.Section title="">
            <HX.Pane flow="down">
              <HX.Section title="Fleet Average Static Relativity">
                <HX.Table data={[
                  {
                    "datum": "fleet_average_relativity/static",
                    "labelBy": "/non_cds/labels/modelling/average_static_fleet_relativity"
                  }
                ]}
                  fields={[
                  "base",
                  "fleet_size",
                  "year_built",
                  "frequency_vessel_type",
                  "flag",
                  "frequency_dwt",
                  "base_x_year_x_value",
                  "severity_vessel_type",
                  "severity_dwt"
                ]}
                  kb-interactive={true} />
              </HX.Section>
            </HX.Pane>
            <HX.Pane flow="down">
              <HX.Section title="Fleet Average Behavioural Relativity">
                <HX.Table title=""
                  data={[
                  {
                    "datum": "fleet_average_relativity/behavioural",
                    "labelBy": "/non_cds/labels/modelling/average_behavioural_fleet_relativity"
                  }
                ]}
                  fields={[
                  "base",
                  "fleet_size",
                  "year_built",
                  "frequency_vessel_type",
                  "flag",
                  "frequency_dwt",
                  "ratio_moored",
                  "base_x_year_x_value",
                  "severity_vessel_type",
                  "severity_dwt"
                ]}
                  kb-interactive={true} />
              </HX.Section>
            </HX.Pane>
            <HX.Section title="Behaviour and Static Modelling">
              <HX.Pane flow="down">
                <HX.Collection fields={[
                  "/non_cds/show_hide_toggles/modelling/show_adjustment_factors",
                  "/non_cds/show_hide_toggles/modelling/show_static_calculations",
                  "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations",
                  "/non_cds/show_hide_toggles/modelling/show_behavoural_rating_levels"
                ]}
                  horizontal={true} />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table data={[
                "modelling_list"
              ]}
                fields={[
                "modelling_imo",
                "modelling_name",
                "modelling_vessel_type",
                {
                  "field": "modelling_agreed_value",
                  "labelBy": "/cds/currency_agreed_value_label"
                },
                "modelling_gross_tonnage",
                "modelling_dwt",
                "modelling_year_built",
                "modelling_flag",
                "modelling_vessel_class",
                {
                  "field": "modelling_freight_conditions",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_adjustment_factors"
                },
                {
                  "field": "modelling_vessel_quality",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_adjustment_factors"
                },
                {
                  "field": "modelling_area_of_operation",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_adjustment_factors"
                },
                {
                  "field": "modelling_fleet_casualty_history",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_adjustment_factors"
                },
                {
                  "field": "modelling_owner_quality",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_adjustment_factors"
                },
                {
                  "field": "modelling_uw_adjustment",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_adjustment_factors"
                },
                {
                  "field": "modelling_agg_uw_adjustment"
                },
                null,
                "static_base",
                "static_fleet_size",
                "static_year_built",
                "static_frequency_vessel_type",
                "static_flag",
                "static_frequency_dwt",
                null,
                "static_severity_base_x_build_year_x_agreed_value",
                "static_severity_vessel_type",
                "static_severity_dwt",
                null,
                {
                  "field": "static_model_frequency",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_model_severity",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_large_loss_overlay",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_coverage",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_coverage_factor",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_expected_loss",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_deductible",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_mbbefdg",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_order_percent",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_el_pre_uw_adj",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_all_uw_adj",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                {
                  "field": "static_el_post_uw_adj",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_static_calculations"
                },
                null,
                {
                  "field": "modelling_behavioural_ratio_moored",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavoural_rating_levels"
                },
                null,
                "behavioural_base",
                "behavioural_fleet_size",
                "behavioural_year_built",
                "behavioural_frequency_vessel_type",
                "behavioural_flag",
                "behavioural_frequency_dwt",
                {
                  "field": "behavioural_ratio_moored"
                },
                null,
                "behavioural_severity_base_x_build_year_x_agreed_value",
                "behavioural_severity_vessel_type",
                "behavioural_severity_dwt",
                null,
                {
                  "field": "behavioural_model_frequency",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_model_severity",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_large_loss_overlay",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_coverage",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_coverage_factor",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_expected_loss",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_deductible",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_mbbefdg",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_order_percent",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_el_pre_uw_adj",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_all_uw_adj",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                {
                  "field": "behavioural_el_post_uw_adj",
                  "shownBy": "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations"
                },
                null,
                {
                  "field": "pro_rata_adjustment"
                }
              ]}
                kb-interactive={true}
                dynamic={true}
                freezeLeft={3} />
            </HX.Section>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Vessel Analysis"
        shownBy="/non_cds/show_hide_toggles/hull/show_modelling_page">
        <HX.With context={{
          "path": "cds/vessel_analysis/hull_rating",
          "type": "struct"
        }}>
          <HX.Section title="Options">
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "imo_and_name/vessel_analysis_imo",
                "imo_and_name/vessel_analysis_name",
                "vessel_analysis_achieved_rate"
              ]}
                horizontal={true} />
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Similar Vessel Rate Comparison - Achieved vs. Achieved Rate Distribution">
            <HX.Pane flow="down">
              <HX.Pane flow="right">
                <HX.Table title="Vessel Type Age DWT"
                  data={[
                  "vessel_analysis_vessel_type_age_dwt_table"
                ]}
                  fields={[
                  "vessel_analysis_vessel_type",
                  "vessel_analysis_age_range",
                  "vessel_analysis_dwt_range"
                ]} />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <CustomComponent title="Achieved Rate Distribution - Type, Age & DWT"
                  data={[
                  {
                    "labelBy": "constant_pre_y",
                    "list": "vessel_analysis_vessel_pre_type_age_dwt_list"
                  },
                  {
                    "labelBy": "constant_post_y",
                    "list": "vessel_analysis_vessel_post_type_age_dwt_list"
                  }
                ]}
                  traces={[
                  {
                    "field": "vessel_analysis_pre_type_age_dwt",
                    "label": "Vessels with lower rate"
                  },
                  {
                    "field": "vessel_analysis_post_type_age_dwt",
                    "label": "Vessels with higher rate"
                  }
                ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Achieved Rate"
                  yAxisLabel=""
                  barMode="stack" />
                <HX.Collection fields={[
                  "vessel_analysis_vessels_type_age_dwt_lower_rate",
                  "vessel_analysis_vessels_type_age_dwt_higher_rate",
                  "vessel_analysis_vessels_type_age_dwt_count"
                ]} />
              </HX.Pane>
              <HX.Pane />
              <HX.Pane />
              <HX.Pane flow="right">
                <CustomComponent title="Achieved Rate Distribution - Type & Age"
                  data={[
                  {
                    "labelBy": "constant_pre_y",
                    "list": "vessel_analysis_vessel_pre_type_age_list"
                  },
                  {
                    "labelBy": "constant_post_y",
                    "list": "vessel_analysis_vessel_post_type_age_list"
                  }
                ]}
                  traces={[
                  {
                    "field": "vessel_analysis_pre_type_age",
                    "label": "Vessels with lower rate"
                  },
                  {
                    "field": "vessel_analysis_post_type_age",
                    "label": "Vessels with higher rate"
                  }
                ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Achieved Rate"
                  yAxisLabel=""
                  barMode="stack" />
                <HX.Collection fields={[
                  "vessel_analysis_vessels_type_age_lower_rate",
                  "vessel_analysis_vessels_type_age_higher_rate",
                  "vessel_analysis_vessels_type_age_count"
                ]} />
              </HX.Pane>
              <HX.Pane />
              <HX.Pane />
              <HX.Pane flow="right">
                <CustomComponent title="Achieved Rate Distribution - Type"
                  data={[
                  {
                    "labelBy": "constant_pre_y",
                    "list": "vessel_analysis_vessel_pre_type_list"
                  },
                  {
                    "labelBy": "constant_post_y",
                    "list": "vessel_analysis_vessel_post_type_list"
                  }
                ]}
                  traces={[
                  {
                    "field": "vessel_analysis_pre_type",
                    "label": "Vessels with lower rate"
                  },
                  {
                    "field": "vessel_analysis_post_type",
                    "label": "Vessels with higher rate"
                  }
                ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Achieved Rate"
                  yAxisLabel=""
                  barMode="stack" />
                <HX.Collection fields={[
                  "vessel_analysis_vessels_type_lower_rate",
                  "vessel_analysis_vessels_type_higher_rate",
                  "vessel_analysis_vessels_type_count"
                ]} />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Output Summary"
        fullWidth={true}
        shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage">
        <HX.Section title="">
          <HX.Pane flow="down">
            <HX.With context={{
              "index": 0,
              "path": "cds/exposure/granular/vessels/hull_rating/vessels_list",
              "type": "list"
            }}>
              <HX.Table maxListVisibleRows={15}
                data={[
                "/cds/exposure/granular/vessels/hull_rating/vessels_list"
              ]}
                fields={[
                "vessel_details/imo.read_only_option",
                "vessel_details/name.read_only_option",
                "coverage.output_summary",
                {
                  "field": "agreed_value.output_summary",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/agreed_value"
                },
                "achieved_rate.output_summary",
                {
                  "field": "iv/iv_output_summary_coverage",
                  "shownBy": "/non_cds/show_hide_toggles/iv/show_iv_coverage"
                },
                {
                  "field": "iv/iv_output_summary_agreed_value",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/agreed_value",
                  "shownBy": "/non_cds/show_hide_toggles/iv/show_iv_coverage"
                },
                {
                  "field": "iv/iv_output_summary_achieved_rate",
                  "shownBy": "/non_cds/show_hide_toggles/iv/show_iv_coverage"
                },
                {
                  "field": "war/war_output_summary_coverage",
                  "shownBy": "/non_cds/show_hide_toggles/war/show_war_coverage"
                },
                {
                  "field": "war/war_output_summary_agreed_value",
                  "labelBy": "/non_cds/labels/required_vessels_columns_labels/agreed_value",
                  "shownBy": "/non_cds/show_hide_toggles/war/show_war_coverage"
                },
                {
                  "field": "war/war_output_summary_achieved_rate",
                  "shownBy": "/non_cds/show_hide_toggles/war/show_war_coverage"
                }
              ]}
                kb-interactive={true} />
            </HX.With>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Portfolio Analysis"
        fullWidth={true}
        shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage">
        <HX.With context={{
          "path": "cds/portfolio_analysis/hull_rating",
          "type": "struct"
        }}>
          <HX.Section title="Filter Options">
            <HX.With context={{
              "path": "filter_options",
              "type": "struct"
            }}>
              <HX.Pane flow="right"
                reflow={false}>
                <HX.Pane flow="down">
                  <HX.Collection with="effective_date"
                    fields={[
                    "effective_date_from",
                    "effective_date_to"
                  ]}
                    horizontal={true} />
                  <HX.Collection fields={[
                    "insured"
                  ]} />
                  <HX.Collection fields={[
                    "vessel_type"
                  ]} />
                  <HX.Collection fields={[
                    "operator_domicile"
                  ]} />
                </HX.Pane>
                <HX.Pane flow="down"
                  stretch={true}>
                  <HX.Button task="portfolio_analysis_search_task"
                    title="Search" />
                  <HX.Button task="clear_portfolio_analysis_search_task"
                    title="Clear Search" />
                  <HX.Button task="generate_portfolio_analysis_excel"
                    title="Export Excel" />
                  <HX.File field="/cds/portfolio_analysis/hull_rating/exported_data"
                    shownBy="/non_cds/show_hide_toggles/hull/show_generated_portfolio_analysis_excel" />
                  <HX.Pane />
                </HX.Pane>
                <HX.Pane flow="down">
                  <HX.Collection fields={[
                    "status"
                  ]} />
                  <HX.Collection fields={[
                    "imo"
                  ]} />
                  <HX.Collection fields={[
                    "coverage"
                  ]} />
                  <HX.Collection fields={[
                    "currency"
                  ]} />
                </HX.Pane>
                <HX.Pane flow="down">
                  <HX.Collection with="agreed_value"
                    fields={[
                    "agreed_value_from",
                    "agreed_value_to"
                  ]}
                    horizontal={true} />
                  <HX.Collection with="gross_tonnage"
                    fields={[
                    "gross_tonnage_from",
                    "gross_tonnage_to"
                  ]}
                    horizontal={true} />
                  <HX.Collection with="dwt"
                    fields={[
                    "dwt_from",
                    "dwt_to"
                  ]}
                    horizontal={true} />
                  <HX.Collection with="year_built"
                    fields={[
                    "year_built_from",
                    "year_built_to"
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane flow="down">
                  <HX.Collection fields={[
                    "has_policy_reference"
                  ]} />
                  <HX.Collection fields={[
                    "policy_reference"
                  ]} />
                  <HX.Collection fields={[
                    "flag"
                  ]} />
                  <HX.Collection fields={[
                    "vessel_class"
                  ]} />
                </HX.Pane>
                <HX.Pane flow="down">
                  <HX.Collection fields={[
                    "live_risk_entry"
                  ]} />
                  <HX.Collection fields={[
                    "follow_lead"
                  ]} />
                  <HX.Collection fields={[
                    "broker"
                  ]} />
                </HX.Pane>
              </HX.Pane>
            </HX.With>
          </HX.Section>
          <HX.Section title="Portfolio Metrics">
            <HX.With context={{
              "path": "portfolio_metrics",
              "type": "struct"
            }}>
              <HX.Pane flow="down">
                <HX.Collection fields={[
                  "vessels_count",
                  {
                    "field": "average_agreed_value",
                    "labelBy": "/non_cds/labels/portfolio_analysis_labels/currency_avg_agreed_value"
                  },
                  "average_achieved_rate"
                ]}
                  horizontal={true} />
                <HX.Table maxListVisibleRows={10}
                  data={[
                  "vessels"
                ]}
                  fields={[
                  "id",
                  "imo",
                  "insured",
                  "policy_reference",
                  "effective_date",
                  "expiry_date",
                  "coverage",
                  "original_agreed_value",
                  "original_currency",
                  {
                    "field": "agreed_value_converted",
                    "labelBy": "/non_cds/labels/portfolio_analysis_labels/currency_agreed_value_converted"
                  },
                  "vessel_type",
                  "gross_tonnage",
                  "dwt",
                  "year_built",
                  "flag",
                  "classification",
                  "achieved_rate",
                  "order_percent",
                  "written_line_percent",
                  "operator_domicile",
                  "broker",
                  "follow_lead",
                  "vessel_name",
                  "type_abrv"
                ]} />
              </HX.Pane>
            </HX.With>
          </HX.Section>
        </HX.With>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};