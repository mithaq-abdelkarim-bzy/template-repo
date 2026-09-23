
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
            <HX.Pane ratio={2}>
              <HX.Notes field="model_state/landing_page_info" />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "inception_date",
                "expiry_date"
              ]}
                with="hx_core"
                horizontal={true} />
              <HX.Button title="Auto-Set Expiry Date (1 Year)"
                task="set_expiry_date_to_one_year" />
            </HX.Pane>
            <HX.Collection fields={[
              "underwriter",
              "benchmark_class"
            ]}
              with="cds/standard_fields"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/insured_name"
            ]}
              horizontal={true} />
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "cds/standard_fields/policy_reference"
              ]} />
              <HX.Collection fields={[
                "cds/standard_fields/is_renewal"
              ]} />
            </HX.Pane>
            <HX.Collection fields={[
              "cds/rating_factors/product_line"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            {
              "field": "cds/standard_fields/broker",
              "shownBy": "cds/validation/broker/valid"
            },
            {
              "field": "cds/standard_fields/broker.notSupported",
              "infoBy": "cds/validation/broker/info_text",
              "shownBy": "cds/validation/broker/invalid"
            },
            "cds/broker_contact",
            "cds/brokerage"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Geography">
          <HX.Collection fields={[
            "street_number",
            "street_name",
            "zip",
            "city"
          ]}
            with="cds/rating_factors"
            horizontal={true} />
          <HX.Collection fields={[
            "state",
            "county",
            "distance_to_coast_options"
          ]}
            with="cds/rating_factors"
            horizontal={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Characteristics">
        <HX.With context={{
          "path": "cds/rating_factors",
          "type": "struct"
        }}>
          <HX.Section title="Mandatory">
            <HX.Collection fields={[
              "building_occupancy",
              {
                "field": "construction_type",
                "shownBy": "/cds/validation/construction_type/valid"
              },
              {
                "field": "construction_type.notSupported",
                "infoBy": "/cds/validation/construction_type/info_text",
                "shownBy": "/cds/validation/construction_type/invalid"
              },
              "year_built",
              "ppc",
              "roof_type"
            ]}
              numCols={4} />
          </HX.Section>
          <HX.Section title="Non-Mandatory">
            <HX.Collection fields={[
              "square_foot",
              {
                "field": "number_of_units",
                "shownBy": "/cds/validation/number_of_units/valid"
              },
              {
                "field": "number_of_units.notSupported",
                "infoBy": "/cds/validation/number_of_units/info_text",
                "shownBy": "/cds/validation/number_of_units/invalid"
              },
              "basement",
              {
                "field": "roof_shape",
                "shownBy": "/cds/validation/roof_shape/valid"
              },
              {
                "field": "roof_shape.notSupported",
                "infoBy": "/cds/validation/roof_shape/info_text",
                "shownBy": "/cds/validation/roof_shape/invalid"
              },
              "number_of_storeys",
              "fire_alarm",
              "burglar_alarm",
              "sprinkler",
              "updated_roof_year",
              "updated_wiring_year",
              "updated_plumbing_year",
              "updated_heating_year"
            ]}
              numCols={4} />
          </HX.Section>
        </HX.With>
        <HX.Section title="Loss History">
          <HX.Table title="Loss History"
            data={[
            "aop",
            "wildfire",
            "ws",
            "liability",
            "eb",
            "fl",
            "eq",
            null,
            "/cds/experience_rating/coverages/total"
          ]}
            fields={[
            {
              "field": "number_of_losses",
              "width": 300
            },
            {
              "field": "amount_of_losses",
              "width": 300
            }
          ]}
            with="cds/experience_rating/coverages"
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Pricing"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Set Number of Options">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "number_of_options"
            ]}
              with="cds"
              horizontal={true}
              syncColumnWidthsKey="number_of_options" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Perils Covered">
          <HX.Button task="generate_recommended_peril_inclusions"
            title="Generate Recommended Perils & Limits" />
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="Include Peril">
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/aop/include_peril/value",
                    "shownBy": "show_aop_option"
                  },
                  {
                    "field": "coverages/wildfire/include_peril/value",
                    "shownBy": "wildfire_enabled"
                  },
                  {
                    "field": "coverages/wildfire/include_peril/value.read_only_same_label",
                    "shownBy": "wildfire_disabled"
                  },
                  {
                    "field": "coverages/ws/include_peril/value",
                    "shownBy": "show_ws_option"
                  },
                  {
                    "field": "coverages/eb/include_peril/value",
                    "shownBy": "show_eb_option"
                  },
                  {
                    "field": "coverages/fl/include_peril/value",
                    "shownBy": "show_fl_option"
                  },
                  {
                    "field": "coverages/eq/include_peril/value",
                    "shownBy": "show_eq_option"
                  },
                  {
                    "field": "coverages/paf/include_peril/value",
                    "shownBy": "show_paf_option"
                  }
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="show_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
                {false}
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="Limits">
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverage_a_building_limit",
                    "shownBy": "pricing_limits_table/show_coverage_a_building_limit"
                  },
                  {
                    "field": "coverage_b_other_structures_limit",
                    "shownBy": "pricing_limits_table/show_coverage_b_other_structures_limit"
                  },
                  {
                    "field": "coverage_c_personal_property_limit",
                    "shownBy": "pricing_limits_table/show_coverage_c_personal_property_limit"
                  },
                  {
                    "field": "coverage_d_loss_of_use_limit",
                    "shownBy": "pricing_limits_table/show_coverage_d_loss_of_use_limit"
                  },
                  {
                    "field": "coverage_e_additional_living_expense_limit",
                    "shownBy": "pricing_limits_table/show_coverage_e_additional_living_expense_limit"
                  },
                  {
                    "field": "coverage_l_liability_limit",
                    "shownBy": "pricing_limits_table/show_coverage_l_liability_limit"
                  },
                  {
                    "field": "coverage_m_med_pay_limit",
                    "shownBy": "/cds/validation/coverage_m_med_pay_limit/valid"
                  },
                  {
                    "field": "coverage_m_med_pay_limit.notSupported",
                    "infoBy": "/cds/validation/coverage_m_med_pay_limit/info_text",
                    "shownBy": "/cds/validation/coverage_m_med_pay_limit/invalid"
                  }
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="unlock_layers"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverage_a_building_limit.read_only",
                    "shownBy": "pricing_limits_table/show_coverage_a_building_limit"
                  },
                  {
                    "field": "coverage_b_other_structures_limit.read_only",
                    "shownBy": "pricing_limits_table/show_coverage_b_other_structures_limit"
                  },
                  {
                    "field": "coverage_c_personal_property_limit.read_only",
                    "shownBy": "pricing_limits_table/show_coverage_c_personal_property_limit"
                  },
                  {
                    "field": "coverage_d_loss_of_use_limit.read_only",
                    "shownBy": "pricing_limits_table/show_coverage_d_loss_of_use_limit"
                  },
                  {
                    "field": "coverage_e_additional_living_expense_limit.read_only",
                    "shownBy": "pricing_limits_table/show_coverage_e_additional_living_expense_limit"
                  },
                  {
                    "field": "coverage_l_liability_limit.read_only",
                    "shownBy": "pricing_limits_table/show_coverage_l_liability_limit"
                  },
                  {
                    "field": "coverage_m_med_pay_limit.read_only",
                    "shownBy": "/cds/validation/coverage_m_med_pay_limit/valid"
                  },
                  {
                    "field": "coverage_m_med_pay_limit.read_only",
                    "infoBy": "/cds/validation/coverage_m_med_pay_limit/info_text",
                    "shownBy": "/cds/validation/coverage_m_med_pay_limit/invalid"
                  }
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="lock_layers"
                  shownBy="/cds/lock_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="Sub-Limits">
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  "sublimits/animal_included",
                  {
                    "field": "sublimits/animal",
                    "shownBy": "/cds/validation/animal/valid"
                  },
                  {
                    "field": "sublimits/animal.notSupported",
                    "infoBy": "/cds/validation/animal/info_text",
                    "shownBy": "/cds/validation/animal/invalid"
                  },
                  "sublimits/diving_board_and_pool_included",
                  {
                    "field": "sublimits/diving_board_and_pool",
                    "shownBy": "/cds/validation/diving_board_and_pool/valid"
                  },
                  {
                    "field": "sublimits/diving_board_and_pool.notSupported",
                    "infoBy": "/cds/validation/diving_board_and_pool/info_text",
                    "shownBy": "/cds/validation/diving_board_and_pool/invalid"
                  },
                  "sublimits/trampoline_included",
                  {
                    "field": "sublimits/trampoline",
                    "shownBy": "/cds/validation/trampoline/valid"
                  },
                  {
                    "field": "sublimits/trampoline.notSupported",
                    "infoBy": "/cds/validation/trampoline/info_text",
                    "shownBy": "/cds/validation/trampoline/invalid"
                  },
                  "sublimits/swimming_pool_included",
                  {
                    "field": "sublimits/swimming_pool",
                    "shownBy": "/cds/validation/swimming_pool/valid"
                  },
                  {
                    "field": "sublimits/swimming_pool.notSupported",
                    "infoBy": "/cds/validation/swimming_pool/info_text",
                    "shownBy": "/cds/validation/swimming_pool/invalid"
                  },
                  "sublimits/premises_only"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="show_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
                {false}
              </HX.Pane>
            </HX.Section>
          </HX.With>
        </HX.Section>
        <HX.Section title="Pricing">
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="AOP"
              shownBy="show_aop_options">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "show_full_pricing_tables_aop"
                ]}
                  shownBy="show_aop_options" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/aop/tiv/value",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/base_rate",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/adjusted_base_rate",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/minimum_rate",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/final_modified_rate",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/deductible",
                    "shownBy": "/cds/validation/aop_deductible/valid"
                  },
                  {
                    "field": "coverages/aop/deductible.notSupported",
                    "infoBy": "/cds/validation/aop_deductible/info_text",
                    "shownBy": "/cds/validation/aop_deductible/invalid"
                  },
                  "coverages/aop/minimum_deductible",
                  "coverages/aop/final_deductible",
                  "coverages/aop/water_damage_deductible",
                  "coverages/aop/deductible_impact",
                  "coverages/aop/water_damage_sublimit",
                  "coverages/aop/model_premium",
                  {
                    "field": "coverages/aop/model_premium_water_damage",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_premium_hail",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_premium_fire",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_premium_other",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  "coverages/aop/model_rate",
                  {
                    "field": "coverages/aop/model_rate_water_damage",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_rate_hail",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_rate_fire",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_rate_other",
                    "shownBy": "show_full_pricing_tables_aop"
                  }
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="unlock_layers"
                  shownBy="show_aop_options"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/aop/tiv/value",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/base_rate",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/adjusted_base_rate",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/minimum_rate",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/final_modified_rate",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/deductible.read_only",
                    "shownBy": "/cds/validation/aop_deductible/valid"
                  },
                  {
                    "field": "coverages/aop/deductible.read_only",
                    "infoBy": "/cds/validation/aop_deductible/info_text",
                    "shownBy": "/cds/validation/aop_deductible/invalid"
                  },
                  "coverages/aop/minimum_deductible",
                  "coverages/aop/final_deductible",
                  "coverages/aop/water_damage_deductible.read_only",
                  "coverages/aop/deductible_impact",
                  "coverages/aop/water_damage_sublimit.read_only",
                  "coverages/aop/model_premium",
                  {
                    "field": "coverages/aop/model_premium_water_damage",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_premium_hail",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_premium_fire",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_premium_other",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  "coverages/aop/model_rate",
                  {
                    "field": "coverages/aop/model_rate_water_damage",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_rate_hail",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_rate_fire",
                    "shownBy": "show_full_pricing_tables_aop"
                  },
                  {
                    "field": "coverages/aop/model_rate_other",
                    "shownBy": "show_full_pricing_tables_aop"
                  }
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="lock_layers"
                  shownBy="/cds/lock_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="Wildfire"
              shownBy="show_wildfire_options">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "show_full_pricing_tables_wildfire"
                ]}
                  shownBy="show_wildfire_options" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/wildfire/tiv/value",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/base_rate",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/adjusted_base_rate",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/minimum_rate",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/final_modified_rate",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/deductible_type",
                    "shownBy": "/cds/validation/wildfire_deductible_type/valid"
                  },
                  {
                    "field": "coverages/wildfire/deductible_type.notSupported",
                    "infoBy": "/cds/validation/wildfire_deductible_type/info_text",
                    "shownBy": "/cds/validation/wildfire_deductible_type/invalid"
                  },
                  {
                    "field": "coverages/wildfire/deductible",
                    "shownBy": "/cds/validation/wildfire_deductible/valid"
                  },
                  {
                    "field": "coverages/wildfire/deductible.notSupported",
                    "infoBy": "/cds/validation/wildfire_deductible/info_text",
                    "shownBy": "/cds/validation/wildfire_deductible/invalid"
                  },
                  "coverages/wildfire/minimum_deductible",
                  "coverages/wildfire/final_deductible",
                  "coverages/wildfire/deductible_impact",
                  "coverages/wildfire/model_premium",
                  "coverages/wildfire/model_rate",
                  "coverages/wildfire/wildfire_score"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="unlock_layers"
                  shownBy="show_wildfire_options"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/wildfire/tiv/value",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/base_rate",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/adjusted_base_rate",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/minimum_rate",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/final_modified_rate",
                    "shownBy": "show_full_pricing_tables_wildfire"
                  },
                  {
                    "field": "coverages/wildfire/deductible_type.read_only",
                    "shownBy": "/cds/validation/wildfire_deductible_type/valid"
                  },
                  {
                    "field": "coverages/wildfire/deductible_type.read_only",
                    "infoBy": "/cds/validation/wildfire_deductible_type/info_text",
                    "shownBy": "/cds/validation/wildfire_deductible_type/invalid"
                  },
                  {
                    "field": "coverages/wildfire/deductible.read_only",
                    "shownBy": "/cds/validation/wildfire_deductible/valid"
                  },
                  {
                    "field": "coverages/wildfire/deductible.read_only",
                    "infoBy": "/cds/validation/wildfire_deductible/info_text",
                    "shownBy": "/cds/validation/wildfire_deductible/invalid"
                  },
                  "coverages/wildfire/minimum_deductible",
                  "coverages/wildfire/final_deductible",
                  "coverages/wildfire/deductible_impact",
                  "coverages/wildfire/model_premium",
                  "coverages/wildfire/model_rate",
                  "coverages/wildfire/wildfire_score.read_only"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="lock_layers"
                  shownBy="/cds/lock_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="WS"
              shownBy="show_ws_options">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "show_full_pricing_tables_ws"
                ]}
                  shownBy="show_ws_options" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/ws/tiv/value",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/base_rate",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/adjusted_base_rate",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/minimum_rate",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/final_modified_rate",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/deductible_type/value",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/deductible",
                    "infoBy": "/cds/validation/ws_deductible/info_text",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/deductible_all_perils",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/xs_building_coverage",
                    "shownBy": "/cds/excess_wind_hail_selected"
                  },
                  {
                    "field": "coverages/ws/xs_contents_coverage",
                    "shownBy": "/cds/excess_wind_hail_selected"
                  },
                  {
                    "field": "coverages/ws/minimum_deductible",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/final_deductible",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/deductible_impact",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  "coverages/ws/model_premium",
                  "coverages/ws/model_rate"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="unlock_layers"
                  shownBy="show_ws_options"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/ws/tiv/value",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/base_rate",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/adjusted_base_rate",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/minimum_rate",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/final_modified_rate",
                    "shownBy": "show_full_pricing_tables_ws"
                  },
                  {
                    "field": "coverages/ws/deductible_type/value.read_only",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/deductible.read_only",
                    "infoBy": "/cds/validation/ws_deductible/info_text",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/deductible_all_perils.read_only",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/xs_building_coverage.read_only",
                    "shownBy": "/cds/excess_wind_hail_selected"
                  },
                  {
                    "field": "coverages/ws/xs_contents_coverage.read_only",
                    "shownBy": "/cds/excess_wind_hail_selected"
                  },
                  {
                    "field": "coverages/ws/minimum_deductible",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/final_deductible",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  {
                    "field": "coverages/ws/deductible_impact",
                    "shownBy": "/cds/excess_wind_hail_not_selected"
                  },
                  "coverages/ws/model_premium",
                  "coverages/ws/model_rate"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="lock_layers"
                  shownBy="/cds/lock_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="Liability">
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/liability/tiv/value"
                  },
                  {
                    "field": "coverages/liability/base_rate"
                  },
                  {
                    "field": "coverages/liability/modifiers_impact/factor"
                  },
                  "coverages/liability/model_premium",
                  "coverages/liability/model_rate"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="show_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="Equipment Breakdown"
              shownBy="show_eb_options">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "show_full_pricing_tables_eb"
                ]}
                  shownBy="show_eb_options" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  "coverages/eb/tiv/value",
                  {
                    "field": "coverages/eb/base_rate",
                    "shownBy": "show_full_pricing_tables_eb"
                  },
                  {
                    "field": "coverages/eb/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_eb"
                  },
                  "coverages/eb/deductible",
                  "coverages/eb/deductible_impact",
                  "coverages/eb/model_premium",
                  "coverages/eb/model_rate"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="unlock_layers"
                  shownBy="show_eb_options"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  "coverages/eb/tiv/value.read_only",
                  {
                    "field": "coverages/eb/base_rate",
                    "shownBy": "show_full_pricing_tables_eb"
                  },
                  {
                    "field": "coverages/eb/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_eb"
                  },
                  "coverages/eb/deductible.read_only",
                  "coverages/eb/deductible_impact",
                  "coverages/eb/model_premium",
                  "coverages/eb/model_rate"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="lock_layers"
                  shownBy="/cds/lock_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Notes field="notes/equipment_breakdown_note" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="Excess FL"
              shownBy="show_fl_options">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "show_full_pricing_tables_fl"
                ]}
                  shownBy="show_fl_options" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/fl/tiv/value",
                    "shownBy": "show_full_pricing_tables_fl"
                  },
                  {
                    "field": "coverages/fl/base_rate",
                    "shownBy": "show_full_pricing_tables_fl"
                  },
                  {
                    "field": "coverages/fl/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_fl"
                  },
                  {
                    "field": "coverages/fl/adjusted_base_rate",
                    "shownBy": "show_full_pricing_tables_fl"
                  },
                  {
                    "field": "coverages/fl/minimum_rate",
                    "shownBy": "show_full_pricing_tables_fl"
                  },
                  {
                    "field": "coverages/fl/final_modified_rate",
                    "shownBy": "show_full_pricing_tables_fl"
                  },
                  "coverages/fl/xs_building_coverage",
                  "coverages/fl/xs_contents_coverage",
                  "coverages/fl/model_premium",
                  "coverages/fl/model_rate"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="show_layer"
                  shownBy="show_fl_options"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="EQ"
              shownBy="show_eq_options">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "show_full_pricing_tables_eq"
                ]}
                  shownBy="show_eq_options" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/eq/tiv/value",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/base_rate",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/adjusted_base_rate",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/minimum_rate",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/final_modified_rate",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  "coverages/eq/deductible",
                  "coverages/eq/deductible_impact",
                  "coverages/eq/model_premium",
                  "coverages/eq/model_rate"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="unlock_layers"
                  shownBy="show_eq_options"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "coverages/eq/tiv/value",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/base_rate",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/modifiers_impact/factor",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/adjusted_base_rate",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/minimum_rate",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  {
                    "field": "coverages/eq/final_modified_rate",
                    "shownBy": "show_full_pricing_tables_eq"
                  },
                  "coverages/eq/deductible.read_only",
                  "coverages/eq/deductible_impact",
                  "coverages/eq/model_premium",
                  "coverages/eq/model_rate"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="lock_layers"
                  shownBy="/cds/lock_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.Section title="PAF"
            shownBy="cds/show_paf_options">
            <HX.Collection fields={[
              "/cds/exposure/granular/paf/based_in_nyc_metro_area",
              "insured_occupation",
              "safe",
              "credit_score"
            ]}
              with="cds/rating_factors"
              horizontal={true} />
            <HX.Table data={[
              "cameras_scheduled_professional_use",
              "cameras_scheduled_personal_use",
              "cameras_blanket",
              "fine_art_scheduled_non_fragile",
              "fine_art_scheduled_fragile",
              "fine_art_blanket",
              "gold_silver_bullion_bank_vault",
              "gold_silver_bullion_home_safe",
              "golf_clubs_scheduled",
              "golf_clubs_scheduled_golf_carts_excluding_collision",
              "jewellery_watches_scheduled_jewellery",
              "jewellery_watches_scheduled_watches",
              "jewellery_watches_scheduled_jewellery_watches_bank_vault_only",
              "jewellery_watches_blanket",
              "musical_instruments_scheduled_professional_use",
              "musical_instruments_scheduled_personal_use",
              "musical_instruments_blanket",
              null,
              "/cds/exposure/granular/paf/specific_schedules_totals_structure"
            ]}
              fields={[
              "tiv",
              "coverage_type",
              "rate"
            ]}
              with="cds/exposure/granular/paf/specific_schedules_structure"
              kb-interactive={true}
              syncColumnWidthsKey="paf_section" />
            <HX.Table data={[
              "antique_furniture",
              "baseball_sports_cards_and_comic_books",
              "books",
              "coins",
              "furs",
              "guns",
              "handbags",
              "memorabilia",
              "rugs",
              "silverware",
              "stamps",
              "wine_and_cigars",
              "audio_visual_equipment",
              "bicycles",
              "computers",
              "misc",
              null,
              "/cds/exposure/granular/paf/scheduled_and_blanket_coverages_totals_structure"
            ]}
              fields={[
              "scheduled_tiv",
              "blanket_tiv",
              "scheduled_rate",
              "blanket_rate"
            ]}
              with="cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure"
              kb-interactive={true}
              syncColumnWidthsKey="paf_section" />
            <HX.Notes field="cds/notes/paf_pricing_collectible_classification_note.read_only" />
            <HX.Collection fields={[
              "tiv"
            ]}
              with="cds/exposure/aggregate/paf"
              syncColumnWidthsKey="paf_section" />
            <HX.Collection fields={[
              "base_premium",
              "base_rate"
            ]}
              horizontal={true}
              with="cds/exposure/aggregate/paf"
              syncColumnWidthsKey="paf_section" />
            <HX.Collection fields={[
              "total_modifier_impact/option_to_bind_factor"
            ]}
              with="cds/rating_factors/paf"
              syncColumnWidthsKey="paf_section" />
            <HX.Section title="Mysterious Disappearance Coverage">
              <HX.Collection fields={[
                "include",
                {
                  "field": "engagement_ring",
                  "shownBy": "include"
                },
                {
                  "field": "tiv",
                  "shownBy": "include"
                },
                {
                  "field": "base_premium",
                  "shownBy": "include"
                }
              ]}
                with="cds/exposure/granular/paf/my_dis_coverage"
                syncColumnWidthsKey="paf_section" />
            </HX.Section>
            <HX.Collection fields={[
              "wearing_limit"
            ]}
              with="cds/exposure/granular/paf"
              syncColumnWidthsKey="paf_section" />
            <HX.Collection fields={[
              "paid_claims_amount_last_five_years",
              "paid_claims_impact"
            ]}
              with="cds/exposure/granular/paf"
              horizontal={true}
              syncColumnWidthsKey="paf_section" />
            <HX.Collection fields={[
              "single_item_limit",
              "single_item_limit_impact"
            ]}
              with="cds/exposure/granular/paf"
              horizontal={true}
              syncColumnWidthsKey="paf_section" />
            <HX.With context={{
              "path": "cds",
              "type": "struct"
            }}>
              <HX.Section title="PAF Options"
                shownBy="show_paf_options">
                {false}
                <HX.Pane flow="right">
                  <HX.Table data={[
                    {
                      "datum": "layers",
                      "elementLabelBy": "layer_label",
                      "width": 250
                    }
                  ]}
                    fields={[
                    "coverages/paf/deductible",
                    "coverages/paf/deductible_impact",
                    "coverages/paf/model_premium",
                    "coverages/paf/model_rate"
                  ]}
                    syncColumnWidthsKey="options_table_column_widths"
                    filter="unlock_layers"
                    shownBy="show_paf_options"
                    freezeLeft={0}
                    transpose={true}
                    kb-interactive={true} />
                  <HX.Table data={[
                    {
                      "datum": "layers",
                      "elementLabelBy": "layer_label",
                      "width": 250
                    }
                  ]}
                    fields={[
                    "coverages/paf/deductible.read_only",
                    "coverages/paf/deductible_impact",
                    "coverages/paf/model_premium",
                    "coverages/paf/model_rate"
                  ]}
                    syncColumnWidthsKey="options_table_column_widths"
                    filter="lock_layers"
                    shownBy="/cds/lock_layer"
                    freezeLeft={0}
                    transpose={true}
                    kb-interactive={true} />
                </HX.Pane>
              </HX.Section>
            </HX.With>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Final KPIs">
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="Coverage Split By % TIV">
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  "kpis/tiv_split/cov_a_perc",
                  "kpis/tiv_split/cov_b_perc",
                  "kpis/tiv_split/cov_c_perc",
                  "kpis/tiv_split/others_perc"
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="show_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.With context={{
            "path": "cds",
            "type": "struct"
          }}>
            <HX.Section title="Peril Split By % EL">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  {
                    "field": "kpis_show_aop_break_down",
                    "shownBy": "show_aop_options"
                  }
                ]} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              {false}
              <HX.Pane flow="right">
                <HX.Table data={[
                  {
                    "datum": "layers",
                    "elementLabelBy": "layer_label",
                    "width": 250
                  }
                ]}
                  fields={[
                  {
                    "field": "kpis/pflr_split/aop_perc",
                    "shownBy": "show_aop_options"
                  },
                  {
                    "field": "kpis/pflr_split/water_damage_perc",
                    "shownBy": "/cds/kpis_show_aop_break_down"
                  },
                  {
                    "field": "kpis/pflr_split/hail_perc",
                    "shownBy": "/cds/kpis_show_aop_break_down"
                  },
                  {
                    "field": "kpis/pflr_split/fire_perc",
                    "shownBy": "/cds/kpis_show_aop_break_down"
                  },
                  {
                    "field": "kpis/pflr_split/other_perc",
                    "shownBy": "/cds/kpis_show_aop_break_down"
                  },
                  "kpis/pflr_split/liability_perc",
                  {
                    "field": "kpis/pflr_split/ws_perc",
                    "shownBy": "show_ws_options"
                  },
                  {
                    "field": "kpis/pflr_split/eq_perc",
                    "shownBy": "show_eq_options"
                  },
                  {
                    "field": "kpis/pflr_split/fl_perc",
                    "shownBy": "show_fl_options"
                  },
                  {
                    "field": "kpis/pflr_split/eb_perc",
                    "shownBy": "show_eb_options"
                  },
                  {
                    "field": "kpis/pflr_split/paf_perc",
                    "shownBy": "show_paf_options"
                  }
                ]}
                  syncColumnWidthsKey="options_table_column_widths"
                  filter="show_layer"
                  freezeLeft={0}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
          </HX.With>
          <HX.Section title="Premiums / Rates">
            <HX.Collection fields={[
              "kpis_rate_premium_toggle"
            ]}
              syncColumnWidthsKey="number_of_options"
              with="cds" />
            <HX.With context={{
              "path": "cds",
              "type": "struct"
            }}>
              <HX.Section title="HVH">
                <HX.Pane flow="right">
                  <CustomComponent boolNode="show_commercial_premium_breakdown"
                    label="Commercial Premium Breakdown" />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                  <HX.Pane />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Table data={[
                    {
                      "datum": "layers",
                      "elementLabelBy": "layer_label",
                      "width": 250
                    }
                  ]}
                    fields={[
                    {
                      "field": "kpis/hvh/technical_premium/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/hvh/technical_premium/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/ho",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/eq",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/excess_flood",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/equipment_breakdown",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/ho",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/eq",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/excess_flood",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/equipment_breakdown",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium_splits/ho",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium_splits/eq",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium_splits/excess_flood",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium_splits/equipment_breakdown",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate_splits/ho",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate_splits/eq",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate_splits/excess_flood",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate_splits/equipment_breakdown",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    "kpis/hvh/modifiers/uw_adjustment"
                  ]}
                    syncColumnWidthsKey="options_table_column_widths"
                    filter="unlock_layers"
                    freezeLeft={0}
                    transpose={true}
                    kb-interactive={true} />
                  <HX.Table data={[
                    {
                      "datum": "layers",
                      "elementLabelBy": "layer_label",
                      "width": 250
                    }
                  ]}
                    fields={[
                    {
                      "field": "kpis/hvh/technical_premium/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/hvh/technical_premium/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/ho",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/eq",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/excess_flood",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/equipment_breakdown",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/ho",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/eq",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/excess_flood",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/equipment_breakdown",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate.read_only",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium.read_only",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium_splits/ho",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium_splits/eq",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium_splits/excess_flood",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/premium_splits/equipment_breakdown",
                      "shownBy": "/cds/show_premium_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate_splits/ho",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate_splits/eq",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate_splits/excess_flood",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    {
                      "field": "kpis/hvh/commercial_premium/rate_splits/equipment_breakdown",
                      "shownBy": "/cds/show_rate_splits"
                    },
                    "kpis/hvh/modifiers/uw_adjustment"
                  ]}
                    syncColumnWidthsKey="options_table_column_widths"
                    filter="lock_layers"
                    shownBy="/cds/lock_layer"
                    freezeLeft={0}
                    transpose={true}
                    kb-interactive={true} />
                </HX.Pane>
              </HX.Section>
            </HX.With>
            <HX.Pane flow="right">
              <HX.Notes field="cds/notes/hvh_cp_deviate_warning"
                shownBy="cds/notes/hvh_cp_deviate_warning_flag" />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.With context={{
              "path": "cds",
              "type": "struct"
            }}>
              <HX.Section title="PAF"
                shownBy="show_paf_options">
                {false}
                <HX.Pane flow="right">
                  <HX.Table data={[
                    {
                      "datum": "layers",
                      "elementLabelBy": "layer_label",
                      "width": 250
                    }
                  ]}
                    fields={[
                    {
                      "field": "kpis/paf/technical_premium/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/paf/technical_premium/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/paf/commercial_premium_pre_uw_adj/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/paf/commercial_premium_pre_uw_adj/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/paf/commercial_premium/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/paf/commercial_premium/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    "kpis/paf/modifiers/uw_adjustment"
                  ]}
                    syncColumnWidthsKey="options_table_column_widths"
                    filter="unlock_layers"
                    shownBy="show_paf_options"
                    freezeLeft={0}
                    transpose={true}
                    kb-interactive={true} />
                  <HX.Table data={[
                    {
                      "datum": "layers",
                      "elementLabelBy": "layer_label",
                      "width": 250
                    }
                  ]}
                    fields={[
                    {
                      "field": "kpis/paf/technical_premium/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/paf/technical_premium/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/paf/commercial_premium_pre_uw_adj/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/paf/commercial_premium_pre_uw_adj/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/paf/commercial_premium/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/paf/commercial_premium/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    "kpis/paf/modifiers/uw_adjustment"
                  ]}
                    syncColumnWidthsKey="options_table_column_widths"
                    filter="lock_layers"
                    shownBy="/cds/lock_layer"
                    freezeLeft={0}
                    transpose={true}
                    kb-interactive={true} />
                </HX.Pane>
              </HX.Section>
            </HX.With>
            <HX.Pane flow="right">
              <HX.Notes field="cds/notes/paf_cp_deviate_warning"
                shownBy="cds/notes/paf_cp_deviate_warning_flag" />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.With context={{
              "path": "cds",
              "type": "struct"
            }}>
              <HX.Section title="Total">
                {false}
                <HX.Pane flow="right">
                  <HX.Table data={[
                    {
                      "datum": "layers",
                      "elementLabelBy": "layer_label",
                      "width": 250
                    }
                  ]}
                    fields={[
                    {
                      "field": "status",
                      "shownBy": "/cds/validation/status/valid"
                    },
                    {
                      "field": "status.notSupported",
                      "infoBy": "/cds/validation/status/info_text",
                      "shownBy": "/cds/validation/status/invalid"
                    },
                    {
                      "field": "kpis/total/technical_premium/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/total/technical_premium/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/total/commercial_premium_pre_uw_adj/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/total/commercial_premium_pre_uw_adj/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    {
                      "field": "kpis/total/commercial_premium/rate",
                      "shownBy": "kpis_show_rates"
                    },
                    {
                      "field": "kpis/total/commercial_premium/premium",
                      "shownBy": "kpis_show_premiums"
                    },
                    "kpis/total/tpi_pre_uw_adj",
                    "kpis/total/tpi",
                    "kpis/total/pflr_pre_uw_adj",
                    "kpis/total/pflr"
                  ]}
                    syncColumnWidthsKey="options_table_column_widths"
                    filter="show_layer"
                    freezeLeft={0}
                    transpose={true}
                    kb-interactive={true} />
                </HX.Pane>
              </HX.Section>
            </HX.With>
          </HX.Section>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Modifiers Breakdown">
        <HX.Section title="Options">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "option_to_show",
              "option_to_bind"
            ]}
              with="cds"
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="AOP"
          shownBy="cds/show_modifiers_breakdown">
          <HX.Notes field="cds/notes/aop_modifiers_breakdown_note.read_only" />
          <HX.Table data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "crime_score",
            "fire_alarm",
            "burglar_alarm",
            "sprinkler",
            "ppc",
            "loss",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/aop/tp_uplift_factor"
          ]}
            fields={[
            "value",
            "factor",
            {
              "field": "option_to_bind_factor",
              "shownBy": "/cds/show_option_to_bind_factor"
            },
            {
              "field": "variance",
              "shownBy": "/cds/show_option_to_bind_factor"
            }
          ]}
            with="cds/rating_factors/aop"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Wildfire"
          shownBy="cds/show_modifiers_breakdown">
          <HX.Table data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "wildfire_score",
            "fire_alarm",
            "sprinkler",
            "ppc",
            "loss",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/wildfire/tp_uplift_factor"
          ]}
            fields={[
            "value",
            "factor",
            {
              "field": "option_to_bind_factor",
              "shownBy": "/cds/show_option_to_bind_factor"
            },
            {
              "field": "variance",
              "shownBy": "/cds/show_option_to_bind_factor"
            }
          ]}
            with="cds/rating_factors/wildfire"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="WS"
          shownBy="cds/show_modifiers_breakdown">
          <HX.Table data={[
            "policy_term",
            "product_line",
            "square_foot",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "distance_to_coast_options",
            "loss",
            "peril",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/ws/tp_uplift_factor"
          ]}
            fields={[
            "value",
            "factor",
            {
              "field": "option_to_bind_factor",
              "shownBy": "/cds/show_option_to_bind_factor"
            },
            {
              "field": "variance",
              "shownBy": "/cds/show_option_to_bind_factor"
            }
          ]}
            with="cds/rating_factors/ws"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Liability"
          shownBy="cds/show_modifiers_breakdown">
          <HX.Table data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            "construction_type",
            "year_built",
            "building_occupancy",
            "ppc",
            "loss",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/liability/tp_uplift_factor"
          ]}
            fields={[
            "value",
            "factor",
            {
              "field": "option_to_bind_factor",
              "shownBy": "/cds/show_option_to_bind_factor"
            },
            {
              "field": "variance",
              "shownBy": "/cds/show_option_to_bind_factor"
            }
          ]}
            with="cds/rating_factors/liability"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Equipment Breakdown"
          shownBy="cds/show_modifiers_breakdown">
          <HX.Table data={[
            "policy_term",
            "loss",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/eb/tp_uplift_factor"
          ]}
            fields={[
            "value",
            "factor",
            {
              "field": "option_to_bind_factor",
              "shownBy": "/cds/show_option_to_bind_factor"
            },
            {
              "field": "variance",
              "shownBy": "/cds/show_option_to_bind_factor"
            }
          ]}
            with="cds/rating_factors/eb"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Excess FL"
          shownBy="cds/show_modifiers_breakdown">
          <HX.Table data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "number_of_storeys",
            "loss",
            "basement",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/fl/tp_uplift_factor"
          ]}
            fields={[
            "value",
            "factor",
            {
              "field": "option_to_bind_factor",
              "shownBy": "/cds/show_option_to_bind_factor"
            },
            {
              "field": "variance",
              "shownBy": "/cds/show_option_to_bind_factor"
            }
          ]}
            with="cds/rating_factors/fl"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="EQ"
          shownBy="cds/show_modifiers_breakdown">
          <HX.Table data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "number_of_storeys",
            "basement",
            "retrofit",
            "soft_storey",
            "loss",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/eq/tp_uplift_factor"
          ]}
            fields={[
            "value",
            "factor",
            {
              "field": "option_to_bind_factor",
              "shownBy": "/cds/show_option_to_bind_factor"
            },
            {
              "field": "variance",
              "shownBy": "/cds/show_option_to_bind_factor"
            }
          ]}
            with="cds/rating_factors/eq"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="PAF"
          shownBy="cds/show_modifiers_breakdown">
          <HX.Notes field="cds/notes/paf_modifiers_breakdown_note.read_only" />
          <HX.Table data={[
            "policy_term",
            "fire_alarm",
            "burglar_alarm",
            "safe",
            "credit_score",
            "crime_score",
            "wildfire_score",
            "include_ws",
            "include_eq",
            "include_fl",
            "include_wildfire",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/paf/tp_uplift_factor"
          ]}
            fields={[
            "value",
            "factor",
            {
              "field": "option_to_bind_factor",
              "shownBy": "/cds/show_option_to_bind_factor"
            },
            {
              "field": "variance",
              "shownBy": "/cds/show_option_to_bind_factor"
            }
          ]}
            with="cds/rating_factors/paf"
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}>
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
        <HX.Section title="Coverage Options">
          <HX.Table title="Priced Quotes"
            data={[
            {
              "datum": "cds/layers",
              "elementLabelBy": "layer_label",
              "width": 250
            }
          ]}
            fields={[
            "status.read_only",
            "section_reference",
            "brokerage",
            "written_line",
            null,
            {
              "field": "quoted_premium",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "quoted_premium_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            "technical_premium",
            {
              "field": "benchmark_premium"
            },
            null,
            "tpi",
            {
              "field": "tpi_pre_uw_adj",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "bpi",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "bpi_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            null,
            {
              "field": "pflr_att",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "pflr_cat",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            "pflr",
            {
              "field": "uw_adj_impact",
              "shownBy": "cds/standard_fields/is_rater_priced"
            }
          ]}
            freezeLeft={0}
            transpose={true}
            filter="show_layer" />
        </HX.Section>
        <HX.Section title="Case Pricing Analysis Filepath"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.Notes field="cds/case_pricing_analysis_location" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}>
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id",
              null
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title="Deal Status by Renewal Layers"
              data={[
              {
                "datum": "cds/layers",
                "elementLabelBy": "layer_label",
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status"
              }
            ]}
              transpose={true}
              filter="option_to_bind" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data"
              shownBy="cds/rate_change/has_rarc_not_run" />
            <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
            <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
            <HX.Button title="Calculate Rate Change"
              task="rarc_task"
              shownBy="cds/standard_fields/is_rater_priced" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Renewal Layer">
          <HX.With context={{
            "indexBy": "cds/option_to_bind_zero_indexed",
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "beazley_line/annualised"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 150
                },
                {
                  "field": "renewal",
                  "width": 150
                }
              ]}
                with="rate_change/premium" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_selected",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}>
        <HX.Section title="Risk Information">
          <HX.With context={{
            "indexBy": "cds/option_to_bind_zero_indexed",
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection fields={[
              "/cds/standard_fields/insured_name.read_only",
              "/hx_core/inception_date.read_only",
              "/hx_core/expiry_date.read_only",
              "/cds/standard_fields/policy_reference.read_only",
              "/cds/standard_fields/underwriter.read_only",
              "/cds/standard_fields/broker.read_only",
              "/cds/rating_factors/product_line.read_only",
              "coverages/aop/tiv/value",
              "/cds/standard_fields/is_renewal.read_only"
            ]}
              numCols={3} />
          </HX.With>
        </HX.Section>
        <HX.Section title="HVH">
          <HX.Section title="Rating & Terms">
            <HX.With context={{
              "indexBy": "cds/option_to_bind_zero_indexed",
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "kpis/hvh/commercial_premium_pre_uw_adj/premium",
                "kpis/hvh/modifiers/uw_adjustment",
                "kpis/hvh/commercial_premium/premium.read_only"
              ]}
                horizontal={true} />
              <HX.Notes field="/cds/notes/underwriter_adjustments_hvh"
                title="Underwriter Adjustment Comment" />
            </HX.With>
          </HX.Section>
          <HX.Section title="Natural Perils">
            <HX.With context={{
              "indexBy": "cds/option_to_bind_zero_indexed",
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Table data={[
                "coverages/aop",
                "coverages/wildfire",
                "coverages/ws",
                "coverages/eb",
                "coverages/fl",
                "coverages/eq"
              ]}
                fields={[
                "include_peril/value.read_only",
                "tiv/value.rationale_page",
                "deductible.read_only"
              ]} />
            </HX.With>
          </HX.Section>
        </HX.Section>
        <HX.Section title="PAF">
          <HX.With context={{
            "indexBy": "cds/option_to_bind_zero_indexed",
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection fields={[
              "/cds/exposure/aggregate/paf/largest_collection_type",
              "/cds/exposure/aggregate/paf/tiv",
              "coverages/paf/deductible.read_only",
              "kpis/paf/commercial_premium_pre_uw_adj/premium",
              "kpis/paf/modifiers/uw_adjustment",
              "kpis/paf/commercial_premium/premium.read_only"
            ]}
              numCols={3} />
            <HX.Notes field="/cds/notes/underwriter_adjustments_paf"
              title="Underwriter Adjustment Comment" />
          </HX.With>
        </HX.Section>
        <HX.Section title="Total">
          <HX.With context={{
            "indexBy": "cds/option_to_bind_zero_indexed",
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection fields={[
              "kpis/total/technical_premium/premium",
              "kpis/total/commercial_premium_pre_uw_adj/premium",
              "kpis/total/commercial_premium/premium",
              "/cds/brokerage.read_only",
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              "tpi"
            ]}
              numCols={3} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Notes">
          <HX.Notes field="/cds/notes/rationale_description"
            title="Description" />
          <HX.Notes field="/cds/notes/rationale_special_processing"
            title="Special Processing" />
          <HX.Notes field="/cds/notes/rationale_underwriter_thoughts"
            title="Underwriter Thoughts" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Summary Layer">
          <HX.With context={{
            "indexBy": "cds/option_to_bind_zero_indexed",
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_att",
              "pflr_cat",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Something is Broken">
        <HX.With context={{
          "path": "bug_report",
          "type": "struct"
        }}>
          <HX.Section title="Log a New Incident">
            <HX.Notes field="helper_text" />
            <HX.Pane>
              <HX.Button task="new_bug_report_task"
                title="Log a New Incident" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Incident Details"
            shownBy="commenced_flag">
            <HX.Pane>
              <HX.Collection fields={[
                "summary"
              ]}
                title="Summary" />
              <HX.Notes field="email_body"
                title="Details" />
              <HX.Pane flow="right"
                ratio={2}>
                <HX.Pane shownBy="inputs_outputs_file_show">
                  <HX.File field="inputs_outputs_file"
                    title="Inputs/Outputs Attachment" />
                  <HX.Button task="generate_bug_report_task"
                    title="Generate Inputs/Outputs" />
                </HX.Pane>
                <HX.With context={{
                  "path": "screenshot_files",
                  "type": "struct"
                }}>
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f1/show_text" />
                  <HX.File field="f1/file"
                    title="Screenshot Attachment"
                    shownBy="f1/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f2/show_text" />
                  <HX.File field="f2/file"
                    title="Screenshot Attachment 2"
                    shownBy="f2/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f3/show_text" />
                  <HX.File field="f3/file"
                    title="Screenshot Attachment 3"
                    shownBy="f3/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f4/show_text" />
                  <HX.File field="f4/file"
                    title="Screenshot Attachment 4"
                    shownBy="f4/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f5/show_text" />
                  <HX.File field="f5/file"
                    title="Screenshot Attachment 5"
                    shownBy="f5/show_file" />
                </HX.With>
              </HX.Pane>
              <HX.Button task="add_additional_file_task"
                title="Upload Additional Screenshots" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="send_bug_report_task"
                title="Send Incident" />
              <HX.Button task="cancel_bug_report_task"
                title="Cancel Incident" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};