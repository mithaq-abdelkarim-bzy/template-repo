
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
      <HX.Page title="Risk Information"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              {
                "field": "inception_date",
                "infoBy": "/cds/hover_info/inception_date"
              },
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "underwriter",
              null
            ]}
              with="cds/standard_fields"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/insured_name"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/policy_reference",
              "cds/currencies/source_currency",
              "cds/standard_fields/is_renewal"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            null
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Coverage">
          <HX.Collection fields={[
            "cds/profession",
            "cds/retro_date"
          ]}
            horizontal={true} />
          <HX.Collection fields={[
            {
              "field": "cds/lawyers_num_attorneys_full",
              "infoBy": "cds/hover_info/num_att_full"
            },
            {
              "field": "cds/lawyers_num_attorneys_fte",
              "infoBy": "cds/hover_info/num_att_fte"
            }
          ]}
            horizontal={true}
            shownBy="cds/profession_lawyers_bool" />
        </HX.Section>
        <HX.Section title="Comments">
          <CustomComponent textNode="cds/risk_comments" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Instructions"
          defaultCollapsed={false}>
          <HX.Notes field="cds/exposure/granular/exposure_details_notes" />
        </HX.Section>
        <HX.Section title="Exposure Details">
          <HX.Pane shownBy="cds/profession_lawyers_bool">
            <HX.Collection fields={[
              {
                "field": "cds/exposure/granular/exposure_expected_current_year",
                "labelBy": "cds/exposure/granular/exposure_expected_current_year_label"
              },
              {
                "field": "cds/experience_rating/experience_ccy"
              },
              null,
              null
            ]}
              horizontal={true} />
            <HX.Table title="Exposure Details"
              data={[
              {
                "datum": "exposure_details/year_20",
                "infoBy": "/cds/hover_info/calculated_policy_year",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_20"
              },
              {
                "datum": "exposure_details/year_19",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_19"
              },
              {
                "datum": "exposure_details/year_18",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_18"
              },
              {
                "datum": "exposure_details/year_17",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_17"
              },
              {
                "datum": "exposure_details/year_16",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_16"
              },
              {
                "datum": "exposure_details/year_15",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_15"
              },
              {
                "datum": "exposure_details/year_14",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_14"
              },
              {
                "datum": "exposure_details/year_13",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_13"
              },
              {
                "datum": "exposure_details/year_12",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_12"
              },
              {
                "datum": "exposure_details/year_11",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_11"
              },
              {
                "datum": "exposure_details/year_10",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_10"
              },
              {
                "datum": "exposure_details/year_9",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_9"
              },
              {
                "datum": "exposure_details/year_8",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_8"
              },
              {
                "datum": "exposure_details/year_7",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_7"
              },
              {
                "datum": "exposure_details/year_6",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_6"
              },
              {
                "datum": "exposure_details/year_5",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_5"
              },
              {
                "datum": "exposure_details/year_4",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_4"
              },
              {
                "datum": "exposure_details/year_3",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_3"
              },
              {
                "datum": "exposure_details/year_2",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_2"
              },
              {
                "datum": "exposure_details/year_1",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_1"
              },
              {
                "datum": "exposure_details/year_0",
                "infoBy": "/cds/hover_info/latest_policy_year",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_0"
              }
            ]}
              fields={[
              {
                "field": "gross_fee",
                "width": 180
              },
              {
                "field": "revalued_fee",
                "width": 180
              },
              {
                "field": "weighting",
                "width": 180
              }
            ]}
              rowHeaderSettings={{
              "width": 80
            }}
              with="cds/exposure/granular"
              dynamic={true}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane shownBy="cds/profession_lawyers_bool_not">
            <HX.Collection fields={[
              {
                "field": "cds/exposure/granular/exposure_expected_current_year",
                "labelBy": "cds/exposure/granular/exposure_expected_current_year_label"
              },
              {
                "field": "cds/experience_rating/experience_ccy"
              },
              null,
              null
            ]}
              horizontal={true} />
            <HX.Table title="Exposure Details"
              data={[
              {
                "datum": "exposure_details/year_20",
                "infoBy": "/cds/hover_info/calculated_policy_year",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_20"
              },
              {
                "datum": "exposure_details/year_19",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_19"
              },
              {
                "datum": "exposure_details/year_18",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_18"
              },
              {
                "datum": "exposure_details/year_17",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_17"
              },
              {
                "datum": "exposure_details/year_16",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_16"
              },
              {
                "datum": "exposure_details/year_15",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_15"
              },
              {
                "datum": "exposure_details/year_14",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_14"
              },
              {
                "datum": "exposure_details/year_13",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_13"
              },
              {
                "datum": "exposure_details/year_12",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_12"
              },
              {
                "datum": "exposure_details/year_11",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_11"
              },
              {
                "datum": "exposure_details/year_10",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_10"
              },
              {
                "datum": "exposure_details/year_9",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_9"
              },
              {
                "datum": "exposure_details/year_8",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_8"
              },
              {
                "datum": "exposure_details/year_7",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_7"
              },
              {
                "datum": "exposure_details/year_6",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_6"
              },
              {
                "datum": "exposure_details/year_5",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_5"
              },
              {
                "datum": "exposure_details/year_4",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_4"
              },
              {
                "datum": "exposure_details/year_3",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_3"
              },
              {
                "datum": "exposure_details/year_2",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_2"
              },
              {
                "datum": "exposure_details/year_1",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_1"
              },
              {
                "datum": "exposure_details/year_0",
                "infoBy": "/cds/hover_info/latest_policy_year",
                "labelAlign": "center",
                "labelBy": "exposure_details_year_labels/year_0"
              }
            ]}
              fields={[
              {
                "field": "professional_services_fee",
                "width": 180
              },
              {
                "field": "epc_design_construct_values",
                "width": 180
              },
              {
                "field": "hard_fm_revenue",
                "width": 180
              },
              {
                "field": "construct_pass_soft_fm_revenue",
                "width": 180
              },
              {
                "field": "revenue_100_pcnt",
                "width": 180
              },
              {
                "field": "notional_revenue",
                "width": 180
              },
              {
                "field": "revalued_notional_revenue",
                "width": 180
              },
              {
                "field": "weighting",
                "width": 180
              }
            ]}
              rowHeaderSettings={{
              "width": 80
            }}
              with="cds/exposure/granular"
              dynamic={true}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Territory"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Instructions"
          defaultCollapsed={false}>
          <HX.Notes field="cds/exposure/granular/territory/instructions"
            title="How to use:" />
        </HX.Section>
        <HX.Section title="Options"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            "territory/bool_individual_country_level",
            "territory/bool_individual_state_level",
            "territory/is_percentage_bool",
            "bool_show_inception_year_client_details_input"
          ]}
            horizontal={true}
            with="cds/exposure/granular" />
        </HX.Section>
        <HX.Section title="Summary"
          defaultCollapsed={false}>
          <HX.Pane flow="right">
            <HX.Notes field="cds/exposure/granular/territory/summary_label"
              stretch={false} />
            <HX.Collection fields={[
              null
            ]} />
            <HX.Collection fields={[
              null
            ]} />
            <HX.Collection fields={[
              null
            ]} />
          </HX.Pane>
          <HX.Table data={[
            {
              "datum": "summary/total"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "summary_year_total_labels/year_0",
              "shownBy": "bool_incept_year_pcnt",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "summary_year_total_labels/year_1",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "summary_year_total_labels/year_2",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "summary_year_total_labels/year_3",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "summary_year_total_labels/year_4",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "summary_year_total_labels/year_5",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_0_value",
              "labelBy": "summary_year_total_labels/year_0",
              "shownBy": "bool_incept_year_value",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "summary_year_total_labels/year_1",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "summary_year_total_labels/year_2",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "summary_year_total_labels/year_3",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "summary_year_total_labels/year_4",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "summary_year_total_labels/year_5",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 200
            },
            null,
            {
              "field": "elc",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 350
          }}
            with="cds/exposure/granular/territory"
            dynamic={true}
            kb-interactive={true} />
          <HX.Table shownBy="bool_table_1"
            data={[
            {
              "datum": "summary/united_kingdom",
              "labelBy": "summary_modifier_labels/united_kingdom"
            },
            {
              "datum": "summary/australia",
              "labelBy": "summary_modifier_labels/australia"
            },
            {
              "datum": "summary/canada",
              "labelBy": "summary_modifier_labels/canada"
            },
            {
              "datum": "summary/quebec",
              "labelBy": "summary_modifier_labels/quebec"
            },
            {
              "datum": "summary/ireland",
              "labelBy": "summary_modifier_labels/ireland"
            },
            {
              "datum": "summary/united_states",
              "labelBy": "summary_modifier_labels/united_states"
            },
            {
              "datum": "summary/asia_pac_south_africa",
              "labelBy": "summary_modifier_labels/asia_pac_south_africa"
            },
            {
              "datum": "summary/europe",
              "labelBy": "summary_modifier_labels/europe"
            },
            {
              "datum": "summary/middle_east",
              "labelBy": "summary_modifier_labels/middle_east"
            },
            {
              "datum": "summary/tax_haven",
              "labelBy": "summary_modifier_labels/tax_haven"
            },
            {
              "datum": "summary/rest_of_world",
              "labelBy": "summary_modifier_labels/rest_of_world"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "bool_incept_year_pcnt",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_0_value",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "bool_incept_year_value",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 200
            },
            null,
            {
              "field": "frequency",
              "width": 200
            },
            {
              "field": "severity",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 350
          }}
            with="cds/exposure/granular/territory"
            dynamic={true}
            kb-interactive={true} />
          <HX.Table shownBy="bool_table_2"
            data={[
            {
              "datum": "summary/united_kingdom",
              "labelBy": "summary_modifier_labels/united_kingdom"
            },
            {
              "datum": "summary/australia",
              "labelBy": "summary_modifier_labels/australia"
            },
            {
              "datum": "summary/canada",
              "labelBy": "summary_modifier_labels/canada"
            },
            {
              "datum": "summary/quebec",
              "labelBy": "summary_modifier_labels/quebec"
            },
            {
              "datum": "summary/ireland",
              "labelBy": "summary_modifier_labels/ireland"
            },
            {
              "datum": "summary/united_states",
              "labelBy": "summary_modifier_labels/united_states"
            },
            {
              "datum": "summary/asia_pac_south_africa_country_sum",
              "labelBy": "summary_modifier_labels/asia_pac_south_africa"
            },
            {
              "datum": "summary/europe_country_sum",
              "labelBy": "summary_modifier_labels/europe"
            },
            {
              "datum": "summary/middle_east_country_sum",
              "labelBy": "summary_modifier_labels/middle_east"
            },
            {
              "datum": "summary/tax_haven_country_sum",
              "labelBy": "summary_modifier_labels/tax_haven"
            },
            {
              "datum": "summary/rest_of_world_country_sum",
              "labelBy": "summary_modifier_labels/rest_of_world"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_0_value",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 200
            },
            null,
            {
              "field": "frequency",
              "width": 200
            },
            {
              "field": "severity",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 350
          }}
            with="cds/exposure/granular/territory"
            dynamic={true}
            kb-interactive={true} />
          <HX.Table shownBy="bool_table_3"
            data={[
            {
              "datum": "summary/united_kingdom",
              "labelBy": "summary_modifier_labels/united_kingdom"
            },
            {
              "datum": "summary/australia",
              "labelBy": "summary_modifier_labels/australia"
            },
            {
              "datum": "summary/canada",
              "labelBy": "summary_modifier_labels/canada"
            },
            {
              "datum": "summary/quebec",
              "labelBy": "summary_modifier_labels/quebec"
            },
            {
              "datum": "summary/ireland",
              "labelBy": "summary_modifier_labels/ireland"
            },
            {
              "datum": "summary/united_states_state_sum",
              "labelBy": "summary_modifier_labels/united_states"
            },
            {
              "datum": "summary/asia_pac_south_africa",
              "labelBy": "summary_modifier_labels/asia_pac_south_africa"
            },
            {
              "datum": "summary/europe",
              "labelBy": "summary_modifier_labels/europe"
            },
            {
              "datum": "summary/middle_east",
              "labelBy": "summary_modifier_labels/middle_east"
            },
            {
              "datum": "summary/tax_haven",
              "labelBy": "summary_modifier_labels/tax_haven"
            },
            {
              "datum": "summary/rest_of_world",
              "labelBy": "summary_modifier_labels/rest_of_world"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_0_value",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 200
            },
            null,
            {
              "field": "frequency",
              "width": 200
            },
            {
              "field": "severity",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 350
          }}
            with="cds/exposure/granular/territory"
            dynamic={true}
            kb-interactive={true} />
          <HX.Table shownBy="bool_table_4"
            data={[
            {
              "datum": "summary/united_kingdom",
              "labelBy": "summary_modifier_labels/united_kingdom"
            },
            {
              "datum": "summary/australia",
              "labelBy": "summary_modifier_labels/australia"
            },
            {
              "datum": "summary/canada",
              "labelBy": "summary_modifier_labels/canada"
            },
            {
              "datum": "summary/quebec",
              "labelBy": "summary_modifier_labels/quebec"
            },
            {
              "datum": "summary/ireland",
              "labelBy": "summary_modifier_labels/ireland"
            },
            {
              "datum": "summary/united_states_state_sum",
              "labelBy": "summary_modifier_labels/united_states"
            },
            {
              "datum": "summary/asia_pac_south_africa_country_sum",
              "labelBy": "summary_modifier_labels/asia_pac_south_africa"
            },
            {
              "datum": "summary/europe_country_sum",
              "labelBy": "summary_modifier_labels/europe"
            },
            {
              "datum": "summary/middle_east_country_sum",
              "labelBy": "summary_modifier_labels/middle_east"
            },
            {
              "datum": "summary/tax_haven_country_sum",
              "labelBy": "summary_modifier_labels/tax_haven"
            },
            {
              "datum": "summary/rest_of_world_country_sum",
              "labelBy": "summary_modifier_labels/rest_of_world"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_0_value",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 200
            },
            null,
            {
              "field": "frequency",
              "width": 200
            },
            {
              "field": "severity",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 350
          }}
            with="cds/exposure/granular/territory"
            dynamic={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Individual Countries"
          shownBy="cds/exposure/granular/territory/bool_individual_country_level"
          defaultCollapsed={false}>
          <HX.Table data={[
            {
              "datum": "individual_countries",
              "elementLabelBy": "region"
            }
          ]}
            fields={[
            {
              "field": "country",
              "width": 175
            },
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_0_value",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            }
          ]}
            title="Individual Countries"
            rowHeaderSettings={{
            "width": 350
          }}
            with="cds/exposure/granular/territory"
            dynamic={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Individual States"
          shownBy="cds/exposure/granular/territory/bool_individual_state_level"
          defaultCollapsed={false}>
          <HX.Table data={[
            {
              "datum": "state",
              "elementLabelBy": "state"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool",
              "width": 130
            },
            {
              "field": "year_0_value",
              "labelBy": "summary_year_labels/year_0",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "summary_year_labels/year_1",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "summary_year_labels/year_2",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "summary_year_labels/year_3",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "summary_year_labels/year_4",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "summary_year_labels/year_5",
              "shownBy": "is_percentage_bool_not",
              "width": 130
            }
          ]}
            title="Individual States"
            rowHeaderSettings={{
            "width": 350
          }}
            with="cds/exposure/granular/territory"
            dynamic={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Chart - FGU Loss by Territory"
          defaultCollapsed={false}>
          <HX.CategoryChart data={[
            "united_kingdom",
            "australia",
            "canada",
            "quebec",
            "ireland",
            "united_states",
            "asia_pac_south_africa",
            "europe",
            "middle_east",
            "tax_haven",
            "rest_of_world"
          ]}
            fields={[
            "expected_loss_cost"
          ]}
            columnType="cluster"
            with="cds/exposure/granular/territory/summary" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Client Details - Lawyers"
        shownBy="cds/profession_lawyers_bool"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Instructions"
          defaultCollapsed={false}>
          <HX.Notes field="cds/exposure/granular/client_details_lawyers/notes" />
        </HX.Section>
        <HX.Section title="Areas of Practice"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            "cds/exposure/granular/client_details_lawyers/bool_is_pcnt",
            "cds/exposure/granular/bool_show_inception_year_client_details_input",
            null,
            null
          ]}
            horizontal={true} />
          <HX.Table data={[
            {
              "datum": "client_details_lawyers/areas_of_practice_total"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_pcnt",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_1",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_2",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_3",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_4",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_5",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_0_value",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_value",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_1",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_2",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_3",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_4",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "client_details_lawyers/summary_year_total_aop_labels/year_5",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 130
            },
            null,
            {
              "field": "elc",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 460
          }}
            with="cds/exposure/granular"
            dynamic={true}
            kb-interactive={true} />
          <HX.Table data={[
            {
              "datum": "client_details_lawyers/areas_of_practice",
              "elementLabelBy": "areas_of_practice"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "territory/summary_year_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_pcnt",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "territory/summary_year_labels/year_1",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "territory/summary_year_labels/year_2",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "territory/summary_year_labels/year_3",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "territory/summary_year_labels/year_4",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "territory/summary_year_labels/year_5",
              "shownBy": "client_details_lawyers/bool_is_pcnt",
              "width": 130
            },
            {
              "field": "year_0_value",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "territory/summary_year_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_value",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "territory/summary_year_labels/year_1",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "territory/summary_year_labels/year_2",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "territory/summary_year_labels/year_3",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "territory/summary_year_labels/year_4",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "territory/summary_year_labels/year_5",
              "shownBy": "client_details_lawyers/bool_is_pcnt_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 130
            },
            null,
            {
              "field": "frequency",
              "width": 200
            },
            {
              "field": "severity",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 460
          }}
            with="cds/exposure/granular"
            dynamic={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Client Specifics"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            "cds/exposure/granular/client_details_lawyers/size_of_matters",
            null
          ]}
            horizontal={true} />
          <CustomComponent textNode="cds/exposure/granular/client_details_lawyers/uw_comments"
            placeholderText="Underwriter Comments" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Client Details - AEC "
        shownBy="cds/profession_lawyers_bool_not"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Instructions"
          defaultCollapsed={false}>
          <HX.Notes field="cds/exposure/granular/client_details_AEC/notes" />
        </HX.Section>
        <HX.Section title="Individual Project Type"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            "client_details_AEC/bool_ipt_is_pcnt",
            "client_details_AEC/bool_ipt_enter_at_level",
            "client_details_AEC/weighted_pcnt_filter_value",
            "bool_show_inception_year_client_details_input"
          ]}
            horizontal={true}
            with="cds/exposure/granular" />
          <HX.Table data={[
            {
              "datum": "client_details_AEC/individual_project_types/total"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_pcnt",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_1",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_2",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_3",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_4",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_5",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_0_value",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_value",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_1",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_2",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_3",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_4",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "client_details_AEC/summary_year_total_ipt_labels/year_5",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 200
            },
            null,
            {
              "field": "expected_loss_cost",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 380
          }}
            with="cds/exposure/granular"
            dynamic={true}
            kb-interactive={true} />
          <HX.Table shownBy="client_details_AEC/bool_ipt_enter_at_level"
            title="Please enter by project location:"
            data={[
            {
              "datum": "client_details_AEC/individual_project_types/airport_runways"
            },
            {
              "datum": "client_details_AEC/individual_project_types/arenas_stadiums_convention_centers"
            },
            {
              "datum": "client_details_AEC/individual_project_types/bridges_tunnels"
            },
            {
              "datum": "client_details_AEC/individual_project_types/chemical_pharmaceutical_plants"
            },
            {
              "datum": "client_details_AEC/individual_project_types/dams_harbours_jetties_wetland_mitigation"
            },
            {
              "datum": "client_details_AEC/individual_project_types/hospitals"
            },
            {
              "datum": "client_details_AEC/individual_project_types/mining"
            },
            {
              "datum": "client_details_AEC/individual_project_types/modular_buildings"
            },
            {
              "datum": "client_details_AEC/individual_project_types/oil_refineries_pipelines_powerplants"
            },
            {
              "datum": "client_details_AEC/individual_project_types/parking_garages"
            },
            {
              "datum": "client_details_AEC/individual_project_types/processing_treatment"
            },
            {
              "datum": "client_details_AEC/individual_project_types/residential_buildings_high_rise"
            },
            {
              "datum": "client_details_AEC/individual_project_types/warehouses_data_centres"
            },
            {
              "datum": "client_details_AEC/individual_project_types/residential_buildings_low_rise"
            },
            {
              "datum": "client_details_AEC/individual_project_types/institutional_lower_risk_output"
            },
            {
              "datum": "client_details_AEC/individual_project_types/churches"
            },
            {
              "datum": "client_details_AEC/individual_project_types/colleges_universities_schools"
            },
            {
              "datum": "client_details_AEC/individual_project_types/convalescent_retirement_facilities"
            },
            {
              "datum": "client_details_AEC/individual_project_types/correctional_facilities_jails"
            },
            {
              "datum": "client_details_AEC/individual_project_types/courthouses"
            },
            {
              "datum": "client_details_AEC/individual_project_types/institutional_other"
            },
            {
              "datum": "client_details_AEC/individual_project_types/military"
            },
            {
              "datum": "client_details_AEC/individual_project_types/recreational_lower_risk_output"
            },
            {
              "datum": "client_details_AEC/individual_project_types/amusement_park"
            },
            {
              "datum": "client_details_AEC/individual_project_types/casinos"
            },
            {
              "datum": "client_details_AEC/individual_project_types/parks_playgrounds_pools"
            },
            {
              "datum": "client_details_AEC/individual_project_types/recreational_other"
            },
            {
              "datum": "client_details_AEC/individual_project_types/sports_facilities"
            },
            {
              "datum": "client_details_AEC/individual_project_types/general_building_lower_risk_output"
            },
            {
              "datum": "client_details_AEC/individual_project_types/airport_terminals"
            },
            {
              "datum": "client_details_AEC/individual_project_types/general_building_other"
            },
            {
              "datum": "client_details_AEC/individual_project_types/hotels_motels"
            },
            {
              "datum": "client_details_AEC/individual_project_types/libraries_museums"
            },
            {
              "datum": "client_details_AEC/individual_project_types/offices"
            },
            {
              "datum": "client_details_AEC/individual_project_types/retail_malls_shopping_centers_restaurants"
            },
            {
              "datum": "client_details_AEC/individual_project_types/infrastructure_lower_risk_output"
            },
            {
              "datum": "client_details_AEC/individual_project_types/infrastructure_other"
            },
            {
              "datum": "client_details_AEC/individual_project_types/rail"
            },
            {
              "datum": "client_details_AEC/individual_project_types/roads"
            },
            {
              "datum": "client_details_AEC/individual_project_types/utilities"
            },
            {
              "datum": "client_details_AEC/individual_project_types/industrial_lower_risk_output"
            },
            {
              "datum": "client_details_AEC/individual_project_types/industrial_other"
            },
            {
              "datum": "client_details_AEC/individual_project_types/manufacturing_facilities"
            },
            {
              "datum": "client_details_AEC/individual_project_types/nuclear_facilities"
            },
            {
              "datum": "client_details_AEC/individual_project_types/environmental_lower_risk_output"
            },
            {
              "datum": "client_details_AEC/individual_project_types/asbestos_abatement"
            },
            {
              "datum": "client_details_AEC/individual_project_types/environmental_other"
            },
            {
              "datum": "client_details_AEC/individual_project_types/waste_brokering"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "territory/summary_year_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_pcnt",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "territory/summary_year_labels/year_1",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "territory/summary_year_labels/year_2",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "territory/summary_year_labels/year_3",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "territory/summary_year_labels/year_4",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "territory/summary_year_labels/year_5",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_0_value",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "territory/summary_year_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_value",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "territory/summary_year_labels/year_1",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "territory/summary_year_labels/year_2",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "territory/summary_year_labels/year_3",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "territory/summary_year_labels/year_4",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "territory/summary_year_labels/year_5",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 200
            },
            null,
            {
              "field": "frequency",
              "width": 200
            },
            {
              "field": "severity",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 380
          }}
            with="cds/exposure/granular"
            dynamic={true}
            filter="filter"
            kb-interactive={true} />
          <HX.Table shownBy="client_details_AEC/bool_ipt_enter_at_level_not"
            title="Please enter by project location:"
            data={[
            {
              "datum": "client_details_AEC/individual_project_types/airport_runways"
            },
            {
              "datum": "client_details_AEC/individual_project_types/arenas_stadiums_convention_centers"
            },
            {
              "datum": "client_details_AEC/individual_project_types/bridges_tunnels"
            },
            {
              "datum": "client_details_AEC/individual_project_types/chemical_pharmaceutical_plants"
            },
            {
              "datum": "client_details_AEC/individual_project_types/dams_harbours_jetties_wetland_mitigation"
            },
            {
              "datum": "client_details_AEC/individual_project_types/hospitals"
            },
            {
              "datum": "client_details_AEC/individual_project_types/mining"
            },
            {
              "datum": "client_details_AEC/individual_project_types/modular_buildings"
            },
            {
              "datum": "client_details_AEC/individual_project_types/oil_refineries_pipelines_powerplants"
            },
            {
              "datum": "client_details_AEC/individual_project_types/parking_garages"
            },
            {
              "datum": "client_details_AEC/individual_project_types/processing_treatment"
            },
            {
              "datum": "client_details_AEC/individual_project_types/residential_buildings_high_rise"
            },
            {
              "datum": "client_details_AEC/individual_project_types/warehouses_data_centres"
            },
            {
              "datum": "client_details_AEC/individual_project_types/residential_buildings_low_rise"
            },
            {
              "datum": "client_details_AEC/individual_project_types/institutional_lower_risk_input"
            },
            {
              "datum": "client_details_AEC/individual_project_types/recreational_lower_risk_input"
            },
            {
              "datum": "client_details_AEC/individual_project_types/general_building_lower_risk_input"
            },
            {
              "datum": "client_details_AEC/individual_project_types/infrastructure_lower_risk_input"
            },
            {
              "datum": "client_details_AEC/individual_project_types/industrial_lower_risk_input"
            },
            {
              "datum": "client_details_AEC/individual_project_types/environmental_lower_risk_input"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "territory/summary_year_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_pcnt",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "territory/summary_year_labels/year_1",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "territory/summary_year_labels/year_2",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "territory/summary_year_labels/year_3",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "territory/summary_year_labels/year_4",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "territory/summary_year_labels/year_5",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt",
              "width": 130
            },
            {
              "field": "year_0_value",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "territory/summary_year_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_value",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "territory/summary_year_labels/year_1",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "territory/summary_year_labels/year_2",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "territory/summary_year_labels/year_3",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "territory/summary_year_labels/year_4",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "territory/summary_year_labels/year_5",
              "shownBy": "client_details_AEC/bool_ipt_is_pcnt_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 200
            },
            null,
            {
              "field": "frequency",
              "width": 200
            },
            {
              "field": "severity",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 380
          }}
            with="cds/exposure/granular"
            dynamic={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Areas of Practice"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            "cds/exposure/granular/client_details_AEC/bool_aop_is_pcnt",
            "cds/exposure/granular/bool_show_inception_year_client_details_input",
            null,
            null
          ]}
            horizontal={true} />
          <HX.Table data={[
            {
              "datum": "client_details_AEC/areas_of_practice_total"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_pcnt",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_1",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_2",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_3",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_4",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_5",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_0_value",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_value",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_1",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_2",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_3",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_4",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "client_details_AEC/summary_year_total_aop_labels/year_5",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 130
            },
            null,
            {
              "field": "elc",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 380
          }}
            with="cds/exposure/granular"
            dynamic={true}
            kb-interactive={true} />
          <HX.Table data={[
            {
              "datum": "client_details_AEC/areas_of_practice",
              "elementLabelBy": "areas_of_practice"
            }
          ]}
            fields={[
            {
              "field": "year_0_pcnt",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "territory/summary_year_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_pcnt",
              "width": 130
            },
            {
              "field": "year_1_pcnt",
              "labelBy": "territory/summary_year_labels/year_1",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_2_pcnt",
              "labelBy": "territory/summary_year_labels/year_2",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_3_pcnt",
              "labelBy": "territory/summary_year_labels/year_3",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_4_pcnt",
              "labelBy": "territory/summary_year_labels/year_4",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_5_pcnt",
              "labelBy": "territory/summary_year_labels/year_5",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt",
              "width": 130
            },
            {
              "field": "year_0_value",
              "infoBy": "/cds/hover_info/territory_policy_year",
              "labelBy": "territory/summary_year_labels/year_0",
              "shownBy": "bool_show_inception_year_client_details_output_value",
              "width": 130
            },
            {
              "field": "year_1_value",
              "labelBy": "territory/summary_year_labels/year_1",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_2_value",
              "labelBy": "territory/summary_year_labels/year_2",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_3_value",
              "labelBy": "territory/summary_year_labels/year_3",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_4_value",
              "labelBy": "territory/summary_year_labels/year_4",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            {
              "field": "year_5_value",
              "labelBy": "territory/summary_year_labels/year_5",
              "shownBy": "client_details_AEC/bool_aop_is_pcnt_not",
              "width": 130
            },
            null,
            {
              "field": "weighted",
              "width": 130
            },
            null,
            {
              "field": "frequency",
              "width": 200
            },
            {
              "field": "severity",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 380
          }}
            with="cds/exposure/granular"
            dynamic={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Client Specifics"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            "cds/exposure/granular/client_details_AEC/size_of_matters",
            null
          ]}
            horizontal={true} />
          <CustomComponent textNode="cds/exposure/granular/client_details_AEC/uw_comments"
            placeholderText="Underwriter Comments" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Claims"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Instructions"
          defaultCollapsed={false}>
          <HX.Notes field="cds/experience_rating/claims_instructions" />
        </HX.Section>
        <HX.Section title="Settings"
          defaultCollapsed={false}>
          <HX.Collection horizontal={true}
            fields={[
            "cds/experience_rating/claims_asatdate",
            "cds/experience_rating/claims_policy_year",
            null,
            null,
            null
          ]} />
        </HX.Section>
        <HX.Section title="Claims Table"
          defaultCollapsed={false}>
          <HX.Table data={[
            {
              "datum": "experience_rating/claims"
            }
          ]}
            fields={[
            {
              "field": "claim_name",
              "width": 220
            },
            {
              "field": "claim_made_date",
              "width": 170
            },
            {
              "field": "claim_close_date",
              "width": 170
            },
            {
              "field": "claim_status",
              "width": 170
            },
            {
              "field": "defense_fgu_paid",
              "width": 200
            },
            {
              "field": "defense_fgu_os",
              "width": 200
            },
            {
              "field": "indemnity_fgu_paid",
              "width": 200
            },
            {
              "field": "indemnity_fgu_os",
              "width": 200
            },
            {
              "field": "currency",
              "width": 150
            },
            null,
            {
              "field": "claim_made_year",
              "width": 170
            },
            {
              "field": "defense_incurred",
              "width": 170
            },
            {
              "field": "indemnity_incurred",
              "width": 170
            },
            {
              "field": "claims_fx_rate",
              "width": 120
            },
            {
              "field": "policy_year_estimated",
              "width": 170
            },
            {
              "field": "defense_incurred_usd",
              "width": 170
            },
            {
              "field": "indemnity_incurred_usd",
              "width": 170
            },
            {
              "field": "incurred_total_usd",
              "width": 170
            },
            {
              "field": "incurred_total_usd_inflated",
              "width": 170
            },
            {
              "field": "paid_total_usd_inflated",
              "width": 170
            },
            {
              "field": "total_usd_inflated",
              "infoBy": "hover_info/total_usd_inflated",
              "width": 170
            }
          ]}
            rowHeaderSettings={{
            "width": 50
          }}
            with="cds"
            dynamic={true}
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Experience Rating"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Instructions"
          defaultCollapsed={false}>
          <HX.Notes field="cds/experience_rating/experience_instructions" />
        </HX.Section>
        <HX.Section title="Historical Account Performance"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            "units_to_view",
            "layer_to_view",
            "experience_ccy",
            null,
            null,
            null
          ]}
            with="cds/experience_rating"
            horizontal={true} />
          <HX.Table data={[
            {
              "datum": "layer_to_view_summary"
            }
          ]}
            fields={[
            {
              "field": "aoc_limit_oc",
              "width": 170
            },
            {
              "field": "agg_limit_oc",
              "width": 170
            },
            {
              "field": "aoc_attachment_oc",
              "width": 170
            },
            {
              "field": "agg_attachment_oc",
              "width": 170
            }
          ]}
            rowHeaderSettings={{
            "width": 70
          }}
            with="cds/experience_rating"
            dynamic={true}
            kb-interactive={true} />
          <HX.Table data={[
            {
              "datum": "claims_summary/year_20",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_20/policy_year"
            },
            {
              "datum": "claims_summary/year_19",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_19/policy_year"
            },
            {
              "datum": "claims_summary/year_18",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_18/policy_year"
            },
            {
              "datum": "claims_summary/year_17",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_17/policy_year"
            },
            {
              "datum": "claims_summary/year_16",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_16/policy_year"
            },
            {
              "datum": "claims_summary/year_15",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_15/policy_year"
            },
            {
              "datum": "claims_summary/year_14",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_14/policy_year"
            },
            {
              "datum": "claims_summary/year_13",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_13/policy_year"
            },
            {
              "datum": "claims_summary/year_12",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_12/policy_year"
            },
            {
              "datum": "claims_summary/year_11",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_11/policy_year"
            },
            {
              "datum": "claims_summary/year_10",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_10/policy_year"
            },
            {
              "datum": "claims_summary/year_9",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_9/policy_year"
            },
            {
              "datum": "claims_summary/year_8",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_8/policy_year"
            },
            {
              "datum": "claims_summary/year_7",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_7/policy_year"
            },
            {
              "datum": "claims_summary/year_6",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_6/policy_year"
            },
            {
              "datum": "claims_summary/year_5",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_5/policy_year"
            },
            {
              "datum": "claims_summary/year_4",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_4/policy_year"
            },
            {
              "datum": "claims_summary/year_3",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_3/policy_year"
            },
            {
              "datum": "claims_summary/year_2",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_2/policy_year"
            },
            {
              "datum": "claims_summary/year_1",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_1/policy_year"
            },
            {
              "datum": "claims_summary/year_0",
              "labelAlign": "center",
              "labelBy": "claims_summary/year_0/policy_year"
            }
          ]}
            fields={[
            {
              "field": "revalued_notional_revenue_oc",
              "width": 170
            },
            {
              "field": "revalued_notional_revenue_weighted_oc",
              "maxWidth": 170
            },
            {
              "field": "pcnt_developed",
              "width": 170
            },
            {
              "field": "gu_incurred_oc",
              "width": 170
            },
            {
              "field": "gu_inflated_oc",
              "width": 170
            },
            null,
            {
              "field": "ql_inflated_incurred_oc",
              "width": 200
            },
            null,
            {
              "field": "weighting_applied_year",
              "width": 200
            }
          ]}
            rowHeaderSettings={{
            "width": 70
          }}
            with="cds/experience_rating"
            dynamic={true}
            kb-interactive={true} />
          <HX.Pane flow="right">
            <HX.Table data={[
              {
                "datum": "experience_rating/weighted_revalued_notional_revenue"
              },
              {
                "datum": "experience_rating/developed_weighted_revalued_notional_revenue"
              },
              {
                "datum": "experience_rating/value_of_claims_data",
                "infoBy": "hover_info/value_of_claims_data"
              }
            ]}
              fields={[
              {
                "field": "last_10_years_oc",
                "labelBy": "experience_rating/last_x_year_labels/last_10_years",
                "width": 168
              },
              {
                "field": "last_15_years_oc",
                "labelBy": "experience_rating/last_x_year_labels/last_15_years",
                "width": 168
              },
              {
                "field": "last_20_years_oc",
                "labelBy": "experience_rating/last_x_year_labels/last_20_years",
                "width": 168
              }
            ]}
              with="cds"
              rowHeaderSettings={{
              "width": 380
            }}
              kb-interactive={true} />
            <HX.Table data={[
              {
                "datum": "experience_rating/inflated_incurred_to_quoted_layer"
              },
              {
                "datum": "experience_rating/per_yr_of_claims_data_value",
                "infoBy": "hover_info/per_year_claims_data"
              },
              {
                "datum": "experience_rating/gross_benchmark_experience_rated_premium"
              }
            ]}
              fields={[
              {
                "field": "last_10_years_oc",
                "labelBy": "experience_rating/last_x_year_labels/last_10_years",
                "width": 168
              },
              {
                "field": "last_15_years_oc",
                "labelBy": "experience_rating/last_x_year_labels/last_15_years",
                "width": 168
              },
              {
                "field": "last_20_years_oc",
                "labelBy": "experience_rating/last_x_year_labels/last_20_years",
                "width": 168
              }
            ]}
              with="cds"
              rowHeaderSettings={{
              "width": 380
            }}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Pricing Summary By Layer"
          defaultCollapsed={false}>
          <HX.Table data={[
            {
              "datum": "layers",
              "elementLabelBy": "name"
            }
          ]}
            fields={[
            {
              "field": "include",
              "width": 100
            },
            {
              "field": "experience_rating_summary/aoc_limit_oc",
              "width": 220
            },
            {
              "field": "experience_rating_summary/agg_limit_oc",
              "width": 220
            },
            {
              "field": "experience_rating_summary/aoc_attachment_oc",
              "width": 220
            },
            {
              "field": "experience_rating_summary/agg_attachment_oc",
              "width": 220
            },
            {
              "field": "experience_rating_summary/gross_benchmark_premium_oc",
              "infoBy": "hover_info/gross_benchmark_premium",
              "width": 240
            },
            {
              "field": "experience_rating_summary/ilf_gross_benchmark_premium_oc",
              "infoBy": "hover_info/ilf_gross_benchmark_premium",
              "width": 240
            }
          ]}
            with="cds"
            rowHeaderSettings={{
            "width": 100
          }}
            kb-interactive={true} />
          <HX.Table data={[
            {
              "datum": "layers_addl",
              "elementLabelBy": "name"
            }
          ]}
            fields={[
            {
              "field": "include",
              "width": 100
            },
            {
              "field": "experience_rating_summary/aoc_limit_oc",
              "width": 220
            },
            {
              "field": "experience_rating_summary/agg_limit_oc",
              "width": 220
            },
            {
              "field": "experience_rating_summary/aoc_attachment_oc",
              "width": 220
            },
            {
              "field": "experience_rating_summary/agg_attachment_oc",
              "width": 220
            },
            {
              "field": "experience_rating_summary/gross_benchmark_premium_oc",
              "infoBy": "hover_info/gross_benchmark_premium",
              "width": 240
            },
            {
              "field": "experience_rating_summary/ilf_gross_benchmark_premium_oc",
              "infoBy": "hover_info/ilf_gross_benchmark_premium",
              "width": 240
            }
          ]}
            with="cds"
            rowHeaderSettings={{
            "width": 100
          }}
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Structure & Pricing"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/layer_no_ia_use">
        <HX.Section title="Simulation"
          defaultCollapsed={false}>
          <HX.Pane flow="right">
            <HX.Button title="Run Simulation"
              task="run_simulation_task" />
            <HX.Notes field="cds/run_simulation_notes"
              shownBy="cds/run_simulation_notes_bool" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Retention"
          defaultCollapsed={false}>
          <HX.Notes field="cds/retention_split_notes" />
          <HX.Table data={[
            {
              "datum": "retention_split"
            }
          ]}
            fields={[
            {
              "field": "region",
              "width": 230
            },
            {
              "field": "ccy",
              "width": 110
            },
            {
              "field": "eec",
              "width": 170
            },
            {
              "field": "aggregate",
              "width": 170
            },
            {
              "field": "retention_underlying",
              "infoBy": "hover_info/retention_underlying",
              "width": 170
            },
            {
              "field": "retention_residual",
              "infoBy": "hover_info/retention_residual",
              "width": 170
            },
            {
              "field": "defence_cost_bool",
              "width": 240
            }
          ]}
            rowHeaderSettings={{
            "width": 50
          }}
            with="cds"
            dynamic={true}
            kb-interactive={true} />
          <CustomComponent notesPath="cds/retention_split_uw_comments"
            plainTextPath="cds/retention_split_uw_comments_plaintext"
            label="Underwriter Comments"
            width="400px"
            marginTop="4px"
            marginBottom="4px"
            autosave={true} />
        </HX.Section>
        <HX.Section title="Policy Structure (Exposure CCY)"
          defaultCollapsed={false}>
          <HX.Notes field="cds/policy_notes" />
          <HX.Collection fields={[
            {
              "field": "cds/rating_factors/elevated_risk_year_load",
              "infoBy": "cds/hover_info/elevated_risk_year_load"
            },
            {
              "field": "cds/rating_factors/cat_load",
              "infoBy": "cds/hover_info/cat_load"
            },
            null,
            null,
            null
          ]}
            horizontal={true} />
          <HX.Table data={[
            {
              "datum": "layers",
              "elementLabelBy": "name"
            }
          ]}
            fields={[
            {
              "field": "include",
              "width": 100
            },
            {
              "field": "limit_eec",
              "width": 170
            },
            {
              "field": "limit_agg",
              "width": 170
            },
            {
              "field": "excess_eec",
              "width": 170
            },
            {
              "field": "excess_agg",
              "width": 170
            },
            {
              "field": "rtc",
              "infoBy": "hover_info/rtc",
              "width": 170
            },
            {
              "field": "rtc_agg",
              "width": 170
            },
            null,
            {
              "field": "defense_cost",
              "width": 170
            },
            {
              "field": "brokerage",
              "width": 170
            },
            {
              "field": "wordings_adj",
              "infoBy": "hover_info/wordings_adj",
              "width": 170
            },
            {
              "field": "uw_adj",
              "infoBy": "hover_info/uw_adj",
              "width": 170
            },
            null,
            {
              "field": "exposure_rate",
              "width": 170
            },
            {
              "field": "exposure_rate_incl_adj",
              "width": 170
            },
            {
              "field": "experience_rate",
              "width": 170
            },
            {
              "field": "experience_rate_incl_adj",
              "width": 170
            },
            null,
            {
              "field": "experience_weighting_2",
              "width": 170
            },
            {
              "field": "blended_model_net_rate_pre",
              "infoBy": "hover_info/blended_model_net_rate",
              "width": 170
            },
            {
              "field": "expected_loss_cost_net_pre",
              "infoBy": "hover_info/expected_loss_cost_net",
              "width": 170
            },
            {
              "field": "blended_model_net_rate",
              "infoBy": "hover_info/blended_model_net_rate",
              "width": 170
            },
            {
              "field": "expected_loss_cost_net",
              "infoBy": "hover_info/expected_loss_cost_net",
              "width": 170
            },
            null,
            {
              "field": "technical_premium_100",
              "width": 170
            },
            {
              "field": "benchmark_premium_100",
              "width": 170
            },
            {
              "field": "technical_premium_100_incl_adj",
              "width": 170
            },
            {
              "field": "benchmark_premium_100_incl_adj",
              "width": 170
            },
            {
              "field": "benchmark_premium_experience_100",
              "width": 190
            },
            {
              "field": "benchmark_premium_exposure_100",
              "width": 190
            },
            {
              "field": "quoted_premium_100",
              "width": 170
            },
            {
              "field": "bound_premium_100",
              "width": 170
            },
            {
              "field": "gross_rate_per_mill",
              "infoBy": "hover_info/gross_rate_per_mill",
              "width": 170
            },
            {
              "field": "bpi_quoted_100",
              "width": 170
            },
            {
              "field": "bpi_bound_100",
              "width": 170
            },
            {
              "field": "tpi_quoted_100",
              "width": 170
            },
            {
              "field": "tpi_bound_100",
              "width": 170
            },
            {
              "field": "bpi_quoted_100_incl_adj",
              "width": 170
            },
            {
              "field": "bpi_bound_100_incl_adj",
              "width": 170
            },
            {
              "field": "tpi_quoted_100_incl_adj",
              "width": 170
            },
            {
              "field": "tpi_bound_100_incl_adj",
              "width": 170
            },
            null,
            {
              "field": "status",
              "width": 170
            },
            {
              "field": "section_reference",
              "width": 170
            },
            null,
            {
              "field": "written_line",
              "width": 170
            },
            {
              "field": "bound_premium_share",
              "width": 170
            },
            null,
            {
              "field": "gross_premium_uw_view",
              "width": 170
            },
            {
              "field": "technical_premium_ryv",
              "width": 170
            },
            {
              "field": "benchmark_premium_ryv",
              "width": 170
            },
            {
              "field": "bpi_quoted_ryv",
              "width": 170
            },
            {
              "field": "bpi_bound_ryv",
              "width": 170
            },
            {
              "field": "tpi_quoted_ryv",
              "width": 170
            },
            {
              "field": "tpi_bound_ryv",
              "width": 170
            }
          ]}
            with="cds"
            rowHeaderSettings={{
            "width": 100
          }}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Additional Policy Structure (Exposure CCY)"
          defaultCollapsed={false}>
          <HX.Table data={[
            {
              "datum": "layers_addl",
              "elementLabelBy": "name"
            }
          ]}
            fields={[
            {
              "field": "include",
              "width": 100
            },
            {
              "field": "limit_eec",
              "width": 170
            },
            {
              "field": "limit_agg",
              "width": 170
            },
            {
              "field": "excess_eec",
              "width": 170
            },
            {
              "field": "excess_agg",
              "width": 170
            },
            {
              "field": "rtc",
              "infoBy": "hover_info/rtc",
              "width": 170
            },
            {
              "field": "rtc_agg",
              "width": 170
            },
            null,
            {
              "field": "defense_cost",
              "width": 170
            },
            {
              "field": "brokerage",
              "width": 170
            },
            {
              "field": "wordings_adj",
              "infoBy": "hover_info/wordings_adj",
              "width": 170
            },
            {
              "field": "uw_adj",
              "infoBy": "hover_info/uw_adj",
              "width": 170
            },
            null,
            {
              "field": "exposure_rate",
              "width": 170
            },
            {
              "field": "exposure_rate_incl_adj",
              "width": 170
            },
            {
              "field": "experience_rate",
              "width": 170
            },
            {
              "field": "experience_rate_incl_adj",
              "width": 170
            },
            null,
            {
              "field": "experience_weighting_2",
              "width": 170
            },
            {
              "field": "blended_model_net_rate_pre",
              "infoBy": "hover_info/blended_model_net_rate",
              "width": 170
            },
            {
              "field": "expected_loss_cost_net_pre",
              "infoBy": "hover_info/expected_loss_cost_net",
              "width": 170
            },
            {
              "field": "blended_model_net_rate",
              "infoBy": "hover_info/blended_model_net_rate",
              "width": 170
            },
            {
              "field": "expected_loss_cost_net",
              "infoBy": "hover_info/expected_loss_cost_net",
              "width": 170
            },
            null,
            {
              "field": "technical_premium_100",
              "width": 170
            },
            {
              "field": "benchmark_premium_100",
              "width": 170
            },
            {
              "field": "technical_premium_100_incl_adj",
              "width": 170
            },
            {
              "field": "benchmark_premium_100_incl_adj",
              "width": 170
            },
            {
              "field": "benchmark_premium_experience_100",
              "width": 190
            },
            {
              "field": "benchmark_premium_exposure_100",
              "width": 190
            },
            {
              "field": "quoted_premium_100",
              "width": 170
            },
            {
              "field": "bound_premium_100",
              "width": 170
            },
            {
              "field": "gross_rate_per_mill",
              "infoBy": "hover_info/gross_rate_per_mill",
              "width": 170
            },
            {
              "field": "bpi_quoted_100",
              "width": 170
            },
            {
              "field": "bpi_bound_100",
              "width": 170
            },
            {
              "field": "tpi_quoted_100",
              "width": 170
            },
            {
              "field": "tpi_bound_100",
              "width": 170
            },
            {
              "field": "bpi_quoted_100_incl_adj",
              "width": 170
            },
            {
              "field": "bpi_bound_100_incl_adj",
              "width": 170
            },
            {
              "field": "tpi_quoted_100_incl_adj",
              "width": 170
            },
            {
              "field": "tpi_bound_100_incl_adj",
              "width": 170
            },
            null,
            {
              "field": "status",
              "width": 170
            },
            {
              "field": "section_reference",
              "width": 170
            },
            null,
            {
              "field": "written_line",
              "width": 170
            },
            {
              "field": "bound_premium_share",
              "width": 170
            },
            null,
            {
              "field": "gross_premium_uw_view",
              "width": 170
            },
            {
              "field": "technical_premium_ryv",
              "width": 170
            },
            {
              "field": "benchmark_premium_ryv",
              "width": 170
            },
            {
              "field": "bpi_quoted_ryv",
              "width": 170
            },
            {
              "field": "bpi_bound_ryv",
              "width": 170
            },
            {
              "field": "tpi_quoted_ryv",
              "width": 170
            },
            {
              "field": "tpi_bound_ryv",
              "width": 170
            }
          ]}
            with="cds"
            rowHeaderSettings={{
            "width": 100
          }}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Exposure Simulation Results - With UW Adj"
          defaultCollapsed={false}>
          <HX.Table data={[
            {
              "datum": "layers",
              "elementLabelBy": "name"
            }
          ]}
            fields={[
            {
              "field": "include",
              "width": 100
            },
            {
              "field": "sim_output_uw_adj/exposure_premium",
              "width": 300
            },
            {
              "field": "sim_output_uw_adj/average_freq",
              "width": 300
            },
            {
              "field": "sim_output_uw_adj/average_defense_cost_freq",
              "width": 300
            },
            {
              "field": "sim_output_uw_adj/layer_exhaust_prob",
              "width": 300
            }
          ]}
            with="cds"
            rowHeaderSettings={{
            "width": 100
          }}
            kb-interactive={true} />
          <HX.Table data={[
            {
              "datum": "layers_addl",
              "elementLabelBy": "name"
            }
          ]}
            fields={[
            {
              "field": "include",
              "width": 100
            },
            {
              "field": "sim_output_uw_adj/exposure_premium",
              "width": 300
            },
            {
              "field": "sim_output_uw_adj/average_freq",
              "width": 300
            },
            {
              "field": "sim_output_uw_adj/average_defense_cost_freq",
              "width": 300
            },
            {
              "field": "sim_output_uw_adj/layer_exhaust_prob",
              "width": 300
            }
          ]}
            with="cds"
            rowHeaderSettings={{
            "width": 100
          }}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Technical Premium Build Up"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            {
              "field": "cds/technical_premium_buildup_layer"
            },
            null,
            null,
            null
          ]}
            horizontal={true} />
          <HX.CategoryChart data={[
            "technical_premium",
            "benchmark_premium",
            "bound_premium"
          ]}
            fields={[
            "brokerage",
            "profit_load",
            "expenses",
            "ri_cost",
            "elc"
          ]}
            columnType="stack"
            title="Premium Build Up"
            primaryAxis={{
            "label": "Premium"
          }}
            with="cds/pbu_chart/data" />
        </HX.Section>
        <HX.Section title="AvE Chart (FGU)"
          defaultCollapsed={true}>
          <HX.XYChart data={[
            "data",
            "data"
          ]}
            points={[
            "points_exposure",
            "points_experience"
          ]}
            xField="loss"
            yField="percentile"
            formatFrom="y"
            labelField={[
            "label_exposure",
            "label_experience"
          ]}
            xAxis={{
            "label": "Loss"
          }}
            yAxis={{
            "label": "Percentile"
          }}
            with="cds/ave_chart" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Pricing Coverages"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/coverage_no_ia_use">
        <HX.Section title="Coverage Options Layer 1"
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Coverage 1"
                fields={[
                "coverages/example_coverage_1/currency",
                "coverages/example_coverage_1/limit",
                "coverages/example_coverage_1/excess",
                "coverages/example_coverage_1/deductible",
                "coverages/example_coverage_1/expected_loss_cost_100"
              ]} />
              <HX.Collection title="Coverage 2"
                fields={[
                "coverages/example_coverage_2/currency",
                "coverages/example_coverage_2/limit",
                "coverages/example_coverage_2/excess",
                "coverages/example_coverage_2/deductible",
                "coverages/example_coverage_2/expected_loss_cost_100"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Coverage Options Layer 2"
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Coverage 1"
                fields={[
                "coverages/example_coverage_1/currency",
                "coverages/example_coverage_1/limit",
                "coverages/example_coverage_1/excess",
                "coverages/example_coverage_1/deductible",
                "coverages/example_coverage_1/expected_loss_cost_100"
              ]} />
              <HX.Collection title="Coverage 2"
                fields={[
                "coverages/example_coverage_2/currency",
                "coverages/example_coverage_2/limit",
                "coverages/example_coverage_2/excess",
                "coverages/example_coverage_2/deductible",
                "coverages/example_coverage_2/expected_loss_cost_100"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Coverage Options Layer 3"
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Coverage 1"
                fields={[
                "coverages/example_coverage_1/currency",
                "coverages/example_coverage_1/limit",
                "coverages/example_coverage_1/excess",
                "coverages/example_coverage_1/deductible",
                "coverages/example_coverage_1/expected_loss_cost_100"
              ]} />
              <HX.Collection title="Coverage 2"
                fields={[
                "coverages/example_coverage_2/currency",
                "coverages/example_coverage_2/limit",
                "coverages/example_coverage_2/excess",
                "coverages/example_coverage_2/deductible",
                "coverages/example_coverage_2/expected_loss_cost_100"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Coverage Options Layer 4"
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Coverage 1"
                fields={[
                "coverages/example_coverage_1/currency",
                "coverages/example_coverage_1/limit",
                "coverages/example_coverage_1/excess",
                "coverages/example_coverage_1/deductible",
                "coverages/example_coverage_1/expected_loss_cost_100"
              ]} />
              <HX.Collection title="Coverage 2"
                fields={[
                "coverages/example_coverage_2/currency",
                "coverages/example_coverage_2/limit",
                "coverages/example_coverage_2/excess",
                "coverages/example_coverage_2/deductible",
                "coverages/example_coverage_2/expected_loss_cost_100"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Coverage Options Layer 5"
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Coverage 1"
                fields={[
                "coverages/example_coverage_1/currency",
                "coverages/example_coverage_1/limit",
                "coverages/example_coverage_1/excess",
                "coverages/example_coverage_1/deductible",
                "coverages/example_coverage_1/expected_loss_cost_100"
              ]} />
              <HX.Collection title="Coverage 2"
                fields={[
                "coverages/example_coverage_2/currency",
                "coverages/example_coverage_2/limit",
                "coverages/example_coverage_2/excess",
                "coverages/example_coverage_2/deductible",
                "coverages/example_coverage_2/expected_loss_cost_100"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Coverage Options Layer 6"
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Coverage 1"
                fields={[
                "coverages/example_coverage_1/currency",
                "coverages/example_coverage_1/limit",
                "coverages/example_coverage_1/excess",
                "coverages/example_coverage_1/deductible",
                "coverages/example_coverage_1/expected_loss_cost_100"
              ]} />
              <HX.Collection title="Coverage 2"
                fields={[
                "coverages/example_coverage_2/currency",
                "coverages/example_coverage_2/limit",
                "coverages/example_coverage_2/excess",
                "coverages/example_coverage_2/deductible",
                "coverages/example_coverage_2/expected_loss_cost_100"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Pricing Coverages Insured Asset"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/coverage_ia_use">
        <HX.Section title="Coverage Options Layer 1"
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table title="Priced Quotes Layer 1 Coverage 1"
                data={[
                {
                  "datum": "coverages/example_coverage_1",
                  "width": 250
                }
              ]}
                fields={[
                "brokerage"
              ]}
                freezeLeft={0}
                transpose={true}
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                "example_coverage_1"
              ]}
                fields={[
                "unique_id",
                "currency",
                "limit",
                "excess",
                "deductible",
                "quoted_premium_100",
                "brokerage",
                "status",
                "written_line",
                "section_reference",
                "expected_loss_cost_100",
                "quoted_premium",
                "quoted_premium_annual"
              ]}
                title="Coverage 1 Insured Assets"
                kb-interactive={true}
                freezeRight={1}
                dynamic={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table title="Priced Quotes Layer 1 Coverage 2"
                data={[
                {
                  "datum": "coverages/example_coverage_2",
                  "width": 250
                }
              ]}
                fields={[
                "brokerage"
              ]}
                freezeLeft={0}
                transpose={true}
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                "example_coverage_2"
              ]}
                fields={[
                "unique_id",
                "currency",
                "limit",
                "excess",
                "deductible",
                "quoted_premium_100",
                "brokerage",
                "status",
                "written_line",
                "section_reference",
                "expected_loss_cost_100",
                "quoted_premium",
                "quoted_premium_annual"
              ]}
                title="Coverage 2 Insured Assets"
                kb-interactive={true}
                freezeRight={1}
                dynamic={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Pricing Layer Insured Asset"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/layer_ia_use">
        <HX.Section title="Coverage Options Layer 1"
          shownBy="cds/rate_change/show_layer_1">
          <HX.Pane>
            <HX.Table title="Layer info"
              data={[
              {
                "datum": "cds/layers",
                "width": 250
              }
            ]}
              fields={[
              "brokerage"
            ]}
              freezeLeft={0}
              transpose={true}
              kb-interactive={true} />
          </HX.Pane>
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                "layers"
              ]}
                fields={[
                "unique_id",
                "currency",
                "limit",
                "excess",
                "deductible",
                "quoted_premium_100",
                "brokerage",
                "status",
                "written_line",
                "section_reference",
                "expected_loss_cost_100",
                "quoted_premium",
                "quoted_premium_annual"
              ]}
                title="Insured Assets"
                kb-interactive={true}
                freezeRight={1}
                dynamic={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        shownBy="model_state/show_rate_change_layer_no_ia_use">
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
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status.read_only"
              }
            ]}
              transpose={true} />
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
          <HX.Section title="Rate Change Instructions and Key"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Notes field="cds/rate_change/instructions" />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Renewal Layer 1"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
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
        <HX.Section title="Renewal Layer 2"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
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
        <HX.Section title="Renewal Layer 3"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
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
        <HX.Section title="Renewal Layer 4"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
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
        <HX.Section title="Renewal Layer 5"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
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
        <HX.Section title="Renewal Layer 6"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
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
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
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
      <HX.Page title="Rate Change Coverages"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_rate_change_coverage_no_ia_use">
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
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status.read_only"
              }
            ]}
              transpose={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="expiring_policy_fetch_coverages_task"
              title="Fetch Expiring Data"
              shownBy="cds/rate_change/has_rarc_not_run" />
            <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
            <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
            <HX.Button title="Calculate Rate Change"
              task="rarc_task_coverages"
              shownBy="cds/standard_fields/is_rater_priced" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
          </HX.Pane>
          <HX.Section title="Rate Change Instructions and Key"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Notes field="cds/rate_change/instructions" />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Renewal Layer 1"
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised",
                    "example_coverage_1/limit",
                    "example_coverage_1/deductible",
                    "example_coverage_1/excess",
                    "example_coverage_1/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised",
                    "example_coverage_2/limit",
                    "example_coverage_2/deductible",
                    "example_coverage_2/excess",
                    "example_coverage_2/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 2"
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised",
                    "example_coverage_1/limit",
                    "example_coverage_1/deductible",
                    "example_coverage_1/excess",
                    "example_coverage_1/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised",
                    "example_coverage_2/limit",
                    "example_coverage_2/deductible",
                    "example_coverage_2/excess",
                    "example_coverage_2/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 3"
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised",
                    "example_coverage_1/limit",
                    "example_coverage_1/deductible",
                    "example_coverage_1/excess",
                    "example_coverage_1/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised",
                    "example_coverage_2/limit",
                    "example_coverage_2/deductible",
                    "example_coverage_2/excess",
                    "example_coverage_2/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 4"
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised",
                    "example_coverage_1/limit",
                    "example_coverage_1/deductible",
                    "example_coverage_1/excess",
                    "example_coverage_1/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised",
                    "example_coverage_2/limit",
                    "example_coverage_2/deductible",
                    "example_coverage_2/excess",
                    "example_coverage_2/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 5"
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised",
                    "example_coverage_1/limit",
                    "example_coverage_1/deductible",
                    "example_coverage_1/excess",
                    "example_coverage_1/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised",
                    "example_coverage_2/limit",
                    "example_coverage_2/deductible",
                    "example_coverage_2/excess",
                    "example_coverage_2/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 6"
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised",
                    "example_coverage_1/limit",
                    "example_coverage_1/deductible",
                    "example_coverage_1/excess",
                    "example_coverage_1/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised",
                    "example_coverage_2/limit",
                    "example_coverage_2/deductible",
                    "example_coverage_2/excess",
                    "example_coverage_2/brokerage"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change Coverages Insured Assets"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_rate_change_coverage_ia_use">
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
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status.read_only"
              }
            ]}
              transpose={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="expiring_policy_fetch_coverages_task"
              title="Fetch Expiring Data"
              shownBy="cds/rate_change/has_rarc_not_run" />
            <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
            <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
            <HX.Button title="Calculate Rate Change"
              task="rarc_task_coverages_insured_asset"
              shownBy="cds/standard_fields/is_rater_priced" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
          </HX.Pane>
          <HX.Section title="Rate Change Instructions and Key"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Notes field="cds/rate_change/instructions" />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Renewal Layer 1"
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 2"
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 3"
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 4"
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 5"
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 6"
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_1/currency",
                    "example_coverage_1/premium/line_100pct/annualised",
                    "example_coverage_1/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_1/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_1/exposure_change",
                    "example_coverage_1/risk_characteristics_change",
                    "example_coverage_1/deductible_change",
                    "example_coverage_1/limit_change",
                    "example_coverage_1/terms_conditions_change",
                    "example_coverage_1/other_change",
                    null,
                    "example_coverage_1/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_1/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "example_coverage_2/currency",
                    "example_coverage_2/premium/line_100pct/annualised",
                    "example_coverage_2/premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "example_coverage_2/show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
                  <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                    data={[
                    "example_coverage_2/exposure_change",
                    "example_coverage_2/risk_characteristics_change",
                    "example_coverage_2/deductible_change",
                    "example_coverage_2/limit_change",
                    "example_coverage_2/terms_conditions_change",
                    "example_coverage_2/other_change",
                    null,
                    "example_coverage_2/rate_change"
                  ]}
                    fields={[
                    {
                      "field": "model_calculated",
                      "width": 140
                    },
                    {
                      "field": "uw_override",
                      "width": 140
                    },
                    {
                      "field": "final",
                      "width": 140
                    },
                    {
                      "field": "comments",
                      "width": 250
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
                    fields={[
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change",
                      "shownBy": "/cds/standard_fields/is_rater_priced"
                    },
                    {
                      "field": "rate_change/example_coverage_2/risk_adjusted_rate_change_case_priced",
                      "shownBy": "/cds/standard_fields/is_case_priced"
                    },
                    null,
                    null
                  ]}
                    horizontal={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change Layers Insured Assets"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_rate_change_layer_ia_use">
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
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status.read_only"
              }
            ]}
              transpose={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data"
              shownBy="cds/rate_change/has_rarc_not_run" />
            <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
            <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
            <HX.Button title="Calculate Rate Change"
              task="rarc_task_insured_asset"
              shownBy="cds/standard_fields/is_rater_priced" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
          </HX.Pane>
          <HX.Section title="Rate Change Instructions and Key"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Notes field="cds/rate_change/instructions" />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Renewal Layer 1"
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "currency",
                    "premium/line_100pct/annualised",
                    "premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
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
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
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
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 2"
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "currency",
                    "premium/line_100pct/annualised",
                    "premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
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
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
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
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 3"
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "currency",
                    "premium/line_100pct/annualised",
                    "premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
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
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
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
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 4"
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "currency",
                    "premium/line_100pct/annualised",
                    "premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
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
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
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
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 5"
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "currency",
                    "premium/line_100pct/annualised",
                    "premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
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
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
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
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 6"
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "currency",
                    "premium/line_100pct/annualised",
                    "premium/beazley_line/annualised"
                  ]}
                    fields={[
                    {
                      "field": "expiring",
                      "width": 130
                    },
                    {
                      "field": "expiring_revalued",
                      "shownBy": "show_expiring_revalued",
                      "width": 130
                    },
                    {
                      "field": "renewal",
                      "width": 130
                    }
                  ]}
                    with="rate_change" />
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
                      "width": 100
                    },
                    {
                      "field": "uw_override",
                      "width": 100
                    },
                    {
                      "field": "final",
                      "width": 100
                    },
                    {
                      "field": "comments",
                      "width": 150
                    }
                  ]}
                    with="rate_change"
                    syncColumnWidthsKey="syncRateChange"
                    kb-interactive={true} />
                  <HX.Collection title="Final Rate Change"
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
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
        <HX.Section title="Policy Document">
          <HX.Button task="policy_to_excel_task"
            title="Generate Policy Document"
            shownBy="policy_doc/show_generate_button" />
          <HX.Notes field="policy_doc/premium_check"
            shownBy="policy_doc/show_premium_check" />
          <HX.File with="policy_doc"
            field="output_file"
            title="Click on the icon below to download the policy document"
            shownBy="show_download" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs">
        <HX.Section title="Standard KPIs">
          <CustomComponent layersPath="cds/layers"
            additionalLayersPath="cds/layers_addl" />
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