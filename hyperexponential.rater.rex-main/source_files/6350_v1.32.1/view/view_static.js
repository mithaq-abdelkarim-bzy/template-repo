
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
            <HX.Button task="start_renewal_task"
              title="Start Policy" />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Policy Info"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title=""
          collapsible={false}
          shownBy="policy_information/notifications/notifications_populated">
          <HX.Button title="Show/Hide Notifications"
            task="show_hide_notifications_task" />
        </HX.Section>
        <HX.Section title=""
          collapsible={false}>
          <HX.Pane flow="right">
            <HX.Button title="Run Simulation"
              task="run_simulation_task" />
            <HX.Button title="Run Rater"
              task="run_schedule_rater_task" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Insured Search">
          <HX.Collection fields={[
            "firmname_input"
          ]}
            with="policy_information/insured_search"
            horizontal={true} />
          <HX.Pane flow="right">
            <HX.Pane />
            <HX.Button task="search_firm_task"
              title="Search Insured" />
          </HX.Pane>
          <HX.Table data={[
            "policy_information/insured_search/search_result"
          ]}
            fields={[
            {
              "field": "firm_name"
            },
            {
              "field": "selected",
              "maxWidth": 300
            }
          ]}
            kb-interactive={true} />
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "policy_information/insured_search/custom_firmname"
            ]} />
            <HX.Button task="import_firm_task"
              title="Load Insured Name" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Policy Information">
          <HX.Collection fields={[
            "insured.read_only",
            "version_comment"
          ]}
            with="policy_information"
            horizontal={true} />
          <HX.Collection fields={[
            "underwriter",
            "team",
            "uw_office",
            "bi_waiting_period"
          ]}
            with="policy_information"
            horizontal={true} />
          <HX.Collection fields={[
            "hx_core/inception_date",
            "hx_core/expiry_date",
            "policy_information/policy_length",
            "policy_information/bi_indemnity_period"
          ]}
            horizontal={true} />
          <HX.Collection fields={[
            "broker_branch",
            "broker_contact",
            "lead_follow",
            "cbi"
          ]}
            with="policy_information"
            horizontal={true} />
          <HX.Collection fields={[
            "slip_currency",
            "exchange_rate_date",
            "exchange_rate",
            "accgrpid",
            "account_group_name"
          ]}
            with="policy_information"
            horizontal={true} />
          <HX.Collection fields={[
            "large_schedule_model",
            "is_case_priced",
            null,
            null,
            null
          ]}
            with="policy_information"
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Layer Details">
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "layers",
              "width": 200
            }
          ]}
            fields={[
            "layer_label",
            "reference",
            "limit",
            "excess",
            "achieved_premium_100_gg",
            "brokerage",
            {
              "field": "written_line_perc",
              "shownBy": "control/show_wrt_line"
            },
            {
              "field": "written_line_perc.validation",
              "shownBy": "control/show_wrt_line_validation"
            },
            "quoted_line_perc",
            "new_renewal",
            "status",
            "sim_used",
            "elt_for_sim"
          ]}
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Case Pricing Results"
          shownBy="policy_information/is_case_priced">
          <HX.Pane flow="right">
            <HX.Button task="save_case_pricing_results_task"
              title="Save Case Pricing Results To Model" />
            <HX.Button task="case_pricing_calc_tech_premium_task"
              title="Calculate Technical Premium From Expected Loss" />
            <HX.Pane ratio={4} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Notes field="case_pricing_info"
              with="policy_information" />
            <HX.Pane />
          </HX.Pane>
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "layers",
              "width": 200
            }
          ]}
            fields={[
            "layer_label",
            "case_pricing/technical_premium",
            "case_pricing/benchmark_premium",
            "case_pricing/total_exp_loss",
            "case_pricing/tpi",
            "case_pricing/bpi",
            "case_pricing/elr",
            null,
            "case_pricing/risk_adj_rate_change"
          ]}
            transpose={true}
            kb-interactive={true} />
          <HX.Table title="Technical Premium Breakdown"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "layers",
              "width": 200
            }
          ]}
            fields={[
            "layer_label",
            "case_pricing/tech_premium/fire",
            null,
            "case_pricing/us_tech_prem",
            "case_pricing/tech_premium/us_ws",
            "case_pricing/tech_premium/us_tn",
            "case_pricing/tech_premium/us_ha",
            "case_pricing/tech_premium/us_fl",
            "case_pricing/tech_premium/us_eq",
            "case_pricing/tech_premium/us_wf",
            null,
            "case_pricing/intl_tech_prem",
            "case_pricing/tech_premium/intl_ws",
            "case_pricing/tech_premium/intl_tn",
            "case_pricing/tech_premium/intl_ha",
            "case_pricing/tech_premium/intl_fl",
            "case_pricing/tech_premium/intl_eq",
            "case_pricing/tech_premium/intl_wf",
            null,
            "case_pricing/nmp_premium",
            null,
            "case_pricing/aep_impact_1_in_10",
            "case_pricing/oep_impact_1_in_250",
            "case_pricing/tp_breakdown/ri_cost",
            null,
            "case_pricing/tp_breakdown/coc",
            "case_pricing/tp_breakdown/dir_exp",
            "case_pricing/tp_breakdown/ind_exp",
            "case_pricing/tp_breakdown/lae",
            "case_pricing/tp_breakdown/sd_loading",
            "case_pricing/tp_breakdown/inv_ret"
          ]}
            transpose={true}
            kb-interactive={true} />
          <HX.Table title="Expected Loss Breakdown"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "layers",
              "width": 200
            }
          ]}
            fields={[
            "layer_label",
            "case_pricing/expected_loss/fire",
            null,
            "case_pricing/us_exp_loss",
            "case_pricing/expected_loss/us_ws",
            "case_pricing/expected_loss/us_tn",
            "case_pricing/expected_loss/us_ha",
            "case_pricing/expected_loss/us_fl",
            "case_pricing/expected_loss/us_eq",
            "case_pricing/expected_loss/us_wf",
            null,
            "case_pricing/intl_exp_loss",
            "case_pricing/expected_loss/intl_ws",
            "case_pricing/expected_loss/intl_tn",
            "case_pricing/expected_loss/intl_ha",
            "case_pricing/expected_loss/intl_fl",
            "case_pricing/expected_loss/intl_eq",
            "case_pricing/expected_loss/intl_wf"
          ]}
            transpose={true}
            kb-interactive={true} />
          <HX.Notes field="case_pricing_note"
            with="policy_information"
            title="Case Pricing Note (include analysis link)" />
        </HX.Section>
        <HX.Section title="Additional References"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Button task="upsert_hx_meta_pas_references_task"
              title="Pass References to PAS" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "layers",
              "width": 200
            }
          ]}
            fields={[
            "reference.read_only",
            "additional_reference_1",
            "additional_reference_2",
            "additional_reference_3",
            "additional_reference_4",
            "additional_reference_5",
            "additional_reference_6"
          ]}
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Manual RMS Inputs"
          defaultCollapsed={true}>
          <HX.Table data={[
            {
              "datum": "layers",
              "width": 200
            }
          ]}
            fields={[
            "quake_aal",
            "wind_aal",
            "quake_sd",
            "wind_sd",
            "all_perils_sd",
            "mi_1_in_10_aep_pt",
            "mi_1_in_250_oep_pt",
            null,
            "intl_quake_aal",
            "intl_wind_aal",
            "intl_quake_sd",
            "intl_wind_sd",
            "intl_all_perils_sd"
          ]}
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Useful Links"
          defaultCollapsed={false}>
          <HX.Pane flow="right">
            <HX.Notes field="user_guide_note"
              with="policy_information" />
            <HX.Notes field="fac_powerapp_note"
              with="policy_information" />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Comments">
          <HX.Notes field="comments/comment_input_box"
            title="Comment"
            shownBy="comments/show_comment_input_box" />
          <HX.Pane flow="right">
            <HX.Button task="add_new_comment_task"
              title="Add Comment"
              shownBy="comments/show_comment_input_box" />
            <HX.Button task="start_add_comments_task"
              title="Show Comment Box"
              shownBy="comments/hide_comment_input_box" />
            <HX.Pane />
          </HX.Pane>
          <HX.Table data={[
            "comments/comments_table"
          ]}
            fields={[
            "comment",
            {
              "field": "created_date",
              "maxWidth": 200
            },
            {
              "field": "created_by",
              "maxWidth": 200
            }
          ]}
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Deductible"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title=""
          collapsible={false}>
          <HX.Pane flow="right">
            <HX.Button title="Run Simulation"
              task="run_simulation_task" />
            <HX.Button title="Run Rater"
              task="run_schedule_rater_task" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Perils">
          <HX.Table data={[
            {
              "datum": "layers",
              "width": 200
            }
          ]}
            fields={[
            "layer_label",
            "perils/fire/include",
            "perils/named_windstorm/include",
            "perils/scs/include",
            "perils/flood/include",
            "perils/quake/include",
            "perils/wildfire/include",
            {
              "field": "perils/equipment_breakdown/include",
              "shownBy": "policy_information/is_nacp"
            },
            {
              "field": "perils/tria/include",
              "shownBy": "policy_information/is_nacp"
            },
            "perils/cyber/include"
          ]}
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Deductibles">
          <HX.Section title="Defaults">
            <HX.Pane flow="right">
              <HX.Button task="named_storm_ws_task"
                title="Named Storm only - WS" />
              <HX.Button task="all_tier_fl_ws_task"
                title="All, Tier and FL - WS" />
              <HX.Button task="fl_ws_task"
                title="FL - WS" />
              <HX.Button task="tx_ws_task"
                title="TX - WS" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="tier_fl_ws_task"
                title="Tier, FL - WS" />
              <HX.Button task="all_wind_ws_scs_task"
                title="All Wind - WS/SCS" />
              <HX.Button task="ca_eq_task"
                title="CA - EQ" />
              <HX.Button task="all_ca_eq_task"
                title="All, CA - EQ" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane flow="right"
                ratio={2}>
                <HX.Button task="copy_primary_deductibles_task"
                  title="Add new layer copying primary deductibles" />
                <HX.Button task="clear_deductibles_task"
                  title="Clear" />
              </HX.Pane>
              <HX.Pane ratio={2} />
            </HX.Pane>
          </HX.Section>
          <HX.Notes field="info/deductible_info" />
          <HX.Section title="Fire"
            shownBy="non_layer_perils/fire/show_section">
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "perils/fire/deductible"
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Button task="copy_fire_ded_task"
                  title="Copy Down Fire Ded" />
              </HX.Pane>
              <HX.Pane ratio={3} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Named Windstorm"
            shownBy="non_layer_perils/named_windstorm/show_section">
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "perils/named_windstorm/per_occurrence_ded"
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Section title="US Location deductibles">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "non_layer_perils/named_windstorm/num_options"
                ]} />
                <HX.Pane ratio={3} />
              </HX.Pane>
              <HX.Table title="Option 1"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/named_windstorm/location_ded/option_1/named_storm_ded",
                "perils/named_windstorm/location_ded/option_1/region_dropdown/region",
                {
                  "field": "perils/named_windstorm/location_ded/option_1/region_dropdown/state",
                  "shownBy": "non_layer_perils/named_windstorm/show_state_1"
                },
                {
                  "field": "perils/named_windstorm/location_ded/option_1/region_dropdown/tier",
                  "shownBy": "non_layer_perils/named_windstorm/show_tier_1"
                },
                "perils/named_windstorm/location_ded/option_1/type",
                "perils/named_windstorm/location_ded/option_1/cell_to_fill",
                {
                  "field": "perils/named_windstorm/location_ded/option_1/percent",
                  "shownBy": "non_layer_perils/named_windstorm/show_percent_1"
                },
                {
                  "field": "perils/named_windstorm/location_ded/option_1/location_min_max",
                  "shownBy": "non_layer_perils/named_windstorm/show_location_min_max_1"
                },
                "perils/named_windstorm/location_ded/option_1/sublimit"
              ]}
                shownBy="non_layer_perils/named_windstorm/show_option_1"
                transpose={true}
                kb-interactive={true} />
              <HX.Table title="Option 2"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/named_windstorm/location_ded/option_2/named_storm_ded",
                "perils/named_windstorm/location_ded/option_2/region_dropdown/region",
                {
                  "field": "perils/named_windstorm/location_ded/option_2/region_dropdown/state",
                  "shownBy": "non_layer_perils/named_windstorm/show_state_2"
                },
                {
                  "field": "perils/named_windstorm/location_ded/option_2/region_dropdown/tier",
                  "shownBy": "non_layer_perils/named_windstorm/show_tier_2"
                },
                "perils/named_windstorm/location_ded/option_2/type",
                "perils/named_windstorm/location_ded/option_2/cell_to_fill",
                {
                  "field": "perils/named_windstorm/location_ded/option_2/percent",
                  "shownBy": "non_layer_perils/named_windstorm/show_percent_2"
                },
                {
                  "field": "perils/named_windstorm/location_ded/option_2/location_min_max",
                  "shownBy": "non_layer_perils/named_windstorm/show_location_min_max_2"
                },
                "perils/named_windstorm/location_ded/option_2/sublimit"
              ]}
                shownBy="non_layer_perils/named_windstorm/show_option_2"
                transpose={true}
                kb-interactive={true} />
              <HX.Table title="Option 3"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/named_windstorm/location_ded/option_3/named_storm_ded",
                "perils/named_windstorm/location_ded/option_3/region_dropdown/region",
                {
                  "field": "perils/named_windstorm/location_ded/option_3/region_dropdown/state",
                  "shownBy": "non_layer_perils/named_windstorm/show_state_3"
                },
                {
                  "field": "perils/named_windstorm/location_ded/option_3/region_dropdown/tier",
                  "shownBy": "non_layer_perils/named_windstorm/show_tier_3"
                },
                "perils/named_windstorm/location_ded/option_3/type",
                "perils/named_windstorm/location_ded/option_3/cell_to_fill",
                {
                  "field": "perils/named_windstorm/location_ded/option_3/percent",
                  "shownBy": "non_layer_perils/named_windstorm/show_percent_3"
                },
                {
                  "field": "perils/named_windstorm/location_ded/option_3/location_min_max",
                  "shownBy": "non_layer_perils/named_windstorm/show_location_min_max_3"
                },
                "perils/named_windstorm/location_ded/option_3/sublimit"
              ]}
                shownBy="non_layer_perils/named_windstorm/show_option_3"
                transpose={true}
                kb-interactive={true} />
            </HX.Section>
          </HX.Section>
          <HX.Section title="Severe Convective Storm"
            shownBy="non_layer_perils/scs/show_section">
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "perils/scs/per_occurrence_ded"
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Section title="US Location deductibles">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "non_layer_perils/scs/num_options"
                ]} />
                <HX.Pane ratio={3} />
              </HX.Pane>
              <HX.Table title="Option 1"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/scs/location_ded/option_1/region_dropdown/region",
                {
                  "field": "perils/scs/location_ded/option_1/region_dropdown/state",
                  "shownBy": "non_layer_perils/scs/show_state_1"
                },
                {
                  "field": "perils/scs/location_ded/option_1/region_dropdown/tier",
                  "shownBy": "non_layer_perils/scs/show_tier_1"
                },
                "perils/scs/location_ded/option_1/type",
                "perils/scs/location_ded/option_1/cell_to_fill",
                {
                  "field": "perils/scs/location_ded/option_1/percent",
                  "shownBy": "non_layer_perils/scs/show_percent_1"
                },
                {
                  "field": "perils/scs/location_ded/option_1/location_min_max",
                  "shownBy": "non_layer_perils/scs/show_location_min_max_1"
                },
                "perils/scs/location_ded/option_1/sublimit"
              ]}
                shownBy="non_layer_perils/scs/show_option_1"
                transpose={true}
                kb-interactive={true} />
              <HX.Table title="Option 2"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/scs/location_ded/option_2/region_dropdown/region",
                {
                  "field": "perils/scs/location_ded/option_2/region_dropdown/state",
                  "shownBy": "non_layer_perils/scs/show_state_2"
                },
                {
                  "field": "perils/scs/location_ded/option_2/region_dropdown/tier",
                  "shownBy": "non_layer_perils/scs/show_tier_2"
                },
                "perils/scs/location_ded/option_2/type",
                "perils/scs/location_ded/option_2/cell_to_fill",
                {
                  "field": "perils/scs/location_ded/option_2/percent",
                  "shownBy": "non_layer_perils/scs/show_percent_2"
                },
                {
                  "field": "perils/scs/location_ded/option_2/location_min_max",
                  "shownBy": "non_layer_perils/scs/show_location_min_max_2"
                },
                "perils/scs/location_ded/option_2/sublimit"
              ]}
                shownBy="non_layer_perils/scs/show_option_2"
                transpose={true}
                kb-interactive={true} />
              <HX.Table title="Option 3"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/scs/location_ded/option_3/region_dropdown/region",
                {
                  "field": "perils/scs/location_ded/option_3/region_dropdown/state",
                  "shownBy": "non_layer_perils/scs/show_state_3"
                },
                {
                  "field": "perils/scs/location_ded/option_3/region_dropdown/tier",
                  "shownBy": "non_layer_perils/scs/show_tier_3"
                },
                "perils/scs/location_ded/option_3/type",
                "perils/scs/location_ded/option_3/cell_to_fill",
                {
                  "field": "perils/scs/location_ded/option_3/percent",
                  "shownBy": "non_layer_perils/scs/show_percent_3"
                },
                {
                  "field": "perils/scs/location_ded/option_3/location_min_max",
                  "shownBy": "non_layer_perils/scs/show_location_min_max_3"
                },
                "perils/scs/location_ded/option_3/sublimit"
              ]}
                shownBy="non_layer_perils/scs/show_option_3"
                transpose={true}
                kb-interactive={true} />
            </HX.Section>
          </HX.Section>
          <HX.Section title="Flood"
            shownBy="non_layer_perils/flood/show_section">
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "perils/flood/per_occurrence_ded"
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Section title="US Location deductibles">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "non_layer_perils/flood/num_options"
                ]} />
                <HX.Pane ratio={3} />
              </HX.Pane>
              <HX.Table title="Option 1"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/flood/location_ded/option_1/region_dropdown/region",
                {
                  "field": "perils/flood/location_ded/option_1/region_dropdown/state",
                  "shownBy": "non_layer_perils/flood/show_state_1"
                },
                {
                  "field": "perils/flood/location_ded/option_1/region_dropdown/fema_zone",
                  "shownBy": "non_layer_perils/flood/show_tier_1"
                },
                "perils/flood/location_ded/option_1/type",
                "perils/flood/location_ded/option_1/cell_to_fill",
                {
                  "field": "perils/flood/location_ded/option_1/percent",
                  "shownBy": "non_layer_perils/flood/show_percent_1"
                },
                {
                  "field": "perils/flood/location_ded/option_1/location_min_max",
                  "shownBy": "non_layer_perils/flood/show_location_min_max_1"
                },
                "perils/flood/location_ded/option_1/sublimit"
              ]}
                shownBy="non_layer_perils/flood/show_option_1"
                transpose={true}
                kb-interactive={true} />
              <HX.Table title="Option 2"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/flood/location_ded/option_2/region_dropdown/region",
                {
                  "field": "perils/flood/location_ded/option_2/region_dropdown/state",
                  "shownBy": "non_layer_perils/flood/show_state_2"
                },
                {
                  "field": "perils/flood/location_ded/option_2/region_dropdown/fema_zone",
                  "shownBy": "non_layer_perils/flood/show_tier_2"
                },
                "perils/flood/location_ded/option_2/type",
                "perils/flood/location_ded/option_2/cell_to_fill",
                {
                  "field": "perils/flood/location_ded/option_2/percent",
                  "shownBy": "non_layer_perils/flood/show_percent_2"
                },
                {
                  "field": "perils/flood/location_ded/option_2/location_min_max",
                  "shownBy": "non_layer_perils/flood/show_location_min_max_2"
                },
                "perils/flood/location_ded/option_2/sublimit"
              ]}
                shownBy="non_layer_perils/flood/show_option_2"
                transpose={true}
                kb-interactive={true} />
              <HX.Table title="Option 3"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/flood/location_ded/option_3/region_dropdown/region",
                {
                  "field": "perils/flood/location_ded/option_3/region_dropdown/state",
                  "shownBy": "non_layer_perils/flood/show_state_3"
                },
                {
                  "field": "perils/flood/location_ded/option_3/region_dropdown/fema_zone",
                  "shownBy": "non_layer_perils/flood/show_tier_3"
                },
                "perils/flood/location_ded/option_3/type",
                "perils/flood/location_ded/option_3/cell_to_fill",
                {
                  "field": "perils/flood/location_ded/option_3/percent",
                  "shownBy": "non_layer_perils/flood/show_percent_3"
                },
                {
                  "field": "perils/flood/location_ded/option_3/location_min_max",
                  "shownBy": "non_layer_perils/flood/show_location_min_max_3"
                },
                "perils/flood/location_ded/option_3/sublimit"
              ]}
                shownBy="non_layer_perils/flood/show_option_3"
                transpose={true}
                kb-interactive={true} />
            </HX.Section>
          </HX.Section>
          <HX.Section title="Quake"
            shownBy="non_layer_perils/quake/show_section">
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "perils/quake/per_occurrence_ded",
              "perils/quake/ca_quake_include"
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Section title="US Location deductibles">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "non_layer_perils/quake/num_options"
                ]} />
                <HX.Pane ratio={3} />
              </HX.Pane>
              <HX.Table title="Option 1"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/quake/location_ded/option_1/region_dropdown/region",
                {
                  "field": "perils/quake/location_ded/option_1/region_dropdown/state",
                  "shownBy": "non_layer_perils/quake/show_state_1"
                },
                {
                  "field": "perils/quake/location_ded/option_1/region_dropdown/tier",
                  "shownBy": "non_layer_perils/quake/show_tier_1"
                },
                "perils/quake/location_ded/option_1/type",
                "perils/quake/location_ded/option_1/cell_to_fill",
                {
                  "field": "perils/quake/location_ded/option_1/percent",
                  "shownBy": "non_layer_perils/quake/show_percent_1"
                },
                {
                  "field": "perils/quake/location_ded/option_1/location_min_max",
                  "shownBy": "non_layer_perils/quake/show_location_min_max_1"
                },
                "perils/quake/location_ded/option_1/sublimit"
              ]}
                shownBy="non_layer_perils/quake/show_option_1"
                transpose={true}
                kb-interactive={true} />
              <HX.Table title="Option 2"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/quake/location_ded/option_2/region_dropdown/region",
                {
                  "field": "perils/quake/location_ded/option_2/region_dropdown/state",
                  "shownBy": "non_layer_perils/quake/show_state_2"
                },
                {
                  "field": "perils/quake/location_ded/option_2/region_dropdown/tier",
                  "shownBy": "non_layer_perils/quake/show_tier_2"
                },
                "perils/quake/location_ded/option_2/type",
                "perils/quake/location_ded/option_2/cell_to_fill",
                {
                  "field": "perils/quake/location_ded/option_2/percent",
                  "shownBy": "non_layer_perils/quake/show_percent_2"
                },
                {
                  "field": "perils/quake/location_ded/option_2/location_min_max",
                  "shownBy": "non_layer_perils/quake/show_location_min_max_2"
                },
                "perils/quake/location_ded/option_2/sublimit"
              ]}
                shownBy="non_layer_perils/quake/show_option_2"
                transpose={true}
                kb-interactive={true} />
              <HX.Table title="Option 3"
                data={[
                {
                  "datum": "layers",
                  "width": 200
                }
              ]}
                fields={[
                "layer_label",
                "perils/quake/location_ded/option_3/region_dropdown/region",
                {
                  "field": "perils/quake/location_ded/option_3/region_dropdown/state",
                  "shownBy": "non_layer_perils/quake/show_state_3"
                },
                {
                  "field": "perils/quake/location_ded/option_3/region_dropdown/tier",
                  "shownBy": "non_layer_perils/quake/show_tier_3"
                },
                "perils/quake/location_ded/option_3/type",
                "perils/quake/location_ded/option_3/cell_to_fill",
                {
                  "field": "perils/quake/location_ded/option_3/percent",
                  "shownBy": "non_layer_perils/quake/show_percent_3"
                },
                {
                  "field": "perils/quake/location_ded/option_3/location_min_max",
                  "shownBy": "non_layer_perils/quake/show_location_min_max_3"
                },
                "perils/quake/location_ded/option_3/sublimit"
              ]}
                shownBy="non_layer_perils/quake/show_option_3"
                transpose={true}
                kb-interactive={true} />
            </HX.Section>
          </HX.Section>
          <HX.Section title="Wildfire"
            shownBy="non_layer_perils/wildfire/show_section">
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "perils/wildfire/deductible"
            ]}
              transpose={true}
              kb-interactive={true} />
          </HX.Section>
        </HX.Section>
        <HX.Section title="International Deductibles">
          <HX.Notes field="model_state/intl_ded_message.read_only" />
          <HX.Pane flow="right">
            <HX.Button task="fill_intl_ded_countries_task"
              title="Populate Countries from Schedule" />
            <HX.Pane ratio={2} />
          </HX.Pane>
          <HX.Section title="Fire"
            shownBy="non_layer_perils/fire/show_section">
            <HX.Pane>
              <HX.Table title="Intl Location Deductibles"
                data={[
                {
                  "datum": "intl_ded",
                  "elementLabelBy": "country"
                }
              ]}
                fields={[
                {
                  "field": "tiv",
                  "width": 200
                },
                {
                  "field": "perc_of_tiv",
                  "width": 200
                },
                {
                  "field": "fixed_min",
                  "labelBy": "/model_state/min_ded_label",
                  "width": 200
                },
                {
                  "field": "fixed_max",
                  "labelBy": "/model_state/max_ded_label",
                  "width": 200
                }
              ]}
                with="non_layer_perils/fire"
                syncColumnWidthsKey="intl_ded"
                kb-interactive={true} />
              <HX.Pane flow="right">
                <HX.Button task="copy_intl_ded_perils_task"
                  title="Copy Down Fire Ded" />
                <HX.Pane ratio={2} />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Named Windstorm"
            shownBy="non_layer_perils/named_windstorm/show_section">
            <HX.Pane>
              <HX.Table title="Intl Location Deductibles"
                data={[
                {
                  "datum": "intl_ded",
                  "elementLabelBy": "country"
                }
              ]}
                fields={[
                {
                  "field": "tiv",
                  "width": 200
                },
                {
                  "field": "perc_of_tiv",
                  "width": 200
                },
                {
                  "field": "fixed_min",
                  "labelBy": "/model_state/min_ded_label",
                  "width": 200
                },
                {
                  "field": "fixed_max",
                  "labelBy": "/model_state/max_ded_label",
                  "width": 200
                },
                {
                  "field": "country_sublimit",
                  "labelBy": "/model_state/sublimit_label",
                  "width": 200
                }
              ]}
                with="non_layer_perils/named_windstorm"
                syncColumnWidthsKey="intl_ded"
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Severe Convective Storms"
            shownBy="non_layer_perils/scs/show_section">
            <HX.Pane>
              <HX.Table title="Intl Location Deductibles"
                data={[
                {
                  "datum": "intl_ded",
                  "elementLabelBy": "country"
                }
              ]}
                fields={[
                {
                  "field": "tiv",
                  "width": 200
                },
                {
                  "field": "perc_of_tiv",
                  "width": 200
                },
                {
                  "field": "fixed_min",
                  "labelBy": "/model_state/min_ded_label",
                  "width": 200
                },
                {
                  "field": "fixed_max",
                  "labelBy": "/model_state/max_ded_label",
                  "width": 200
                },
                {
                  "field": "country_sublimit",
                  "labelBy": "/model_state/sublimit_label",
                  "width": 200
                }
              ]}
                with="non_layer_perils/scs"
                syncColumnWidthsKey="intl_ded"
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Flood"
            shownBy="non_layer_perils/flood/show_section">
            <HX.Pane>
              <HX.Table title="Intl Location Deductibles"
                data={[
                {
                  "datum": "intl_ded",
                  "elementLabelBy": "country"
                }
              ]}
                fields={[
                {
                  "field": "tiv",
                  "width": 200
                },
                {
                  "field": "perc_of_tiv",
                  "width": 200
                },
                {
                  "field": "fixed_min",
                  "labelBy": "/model_state/min_ded_label",
                  "width": 200
                },
                {
                  "field": "fixed_max",
                  "labelBy": "/model_state/max_ded_label",
                  "width": 200
                },
                {
                  "field": "country_sublimit",
                  "labelBy": "/model_state/sublimit_label",
                  "width": 200
                }
              ]}
                with="non_layer_perils/flood"
                syncColumnWidthsKey="intl_ded"
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Quake"
            shownBy="non_layer_perils/quake/show_section">
            <HX.Pane>
              <HX.Table title="Intl Location Deductibles"
                data={[
                {
                  "datum": "intl_ded",
                  "elementLabelBy": "country"
                }
              ]}
                fields={[
                {
                  "field": "tiv",
                  "width": 200
                },
                {
                  "field": "perc_of_tiv",
                  "width": 200
                },
                {
                  "field": "fixed_min",
                  "labelBy": "/model_state/min_ded_label",
                  "width": 200
                },
                {
                  "field": "fixed_max",
                  "labelBy": "/model_state/max_ded_label",
                  "width": 200
                },
                {
                  "field": "country_sublimit",
                  "labelBy": "/model_state/sublimit_label",
                  "width": 200
                }
              ]}
                with="non_layer_perils/quake"
                syncColumnWidthsKey="intl_ded"
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Wildfire"
            shownBy="non_layer_perils/wildfire/show_section">
            <HX.Pane>
              <HX.Table title="Intl Location Deductibles"
                data={[
                {
                  "datum": "intl_ded",
                  "elementLabelBy": "country"
                }
              ]}
                fields={[
                {
                  "field": "tiv",
                  "width": 200
                },
                {
                  "field": "perc_of_tiv",
                  "width": 200
                },
                {
                  "field": "fixed_min",
                  "labelBy": "/model_state/min_ded_label",
                  "width": 200
                },
                {
                  "field": "fixed_max",
                  "labelBy": "/model_state/max_ded_label",
                  "width": 200
                }
              ]}
                with="non_layer_perils/wildfire"
                syncColumnWidthsKey="intl_ded"
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Sublimits">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "scs_sublimit",
              "ws_sublimit",
              "eq_sublimit",
              "fl_sublimit"
            ]}
              with="sublimit" />
            <HX.Pane />
            <HX.Pane ratio={2}>
              <HX.Notes field="sublimit/sublimit_warning" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Additional Coverages"
        fullWidth={true}
        shownBy="control/show_additional_coverages_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title=""
          collapsible={false}>
          <HX.Pane flow="right">
            <HX.Button title="Run Simulation"
              task="run_simulation_task" />
            <HX.Button title="Run Rater"
              task="run_schedule_rater_task" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Equipment Breakdown"
          shownBy="non_layer_perils/equipment_breakdown/show_section">
          <CustomComponent textNode="info/equipment_breakdown_msg" />
          <HX.Pane flow="right">
            <HX.Pane ratio={3}>
              <HX.Collection fields={[
                "industry",
                "occupancy",
                "deductible"
              ]}
                with="non_layer_perils/equipment_breakdown"
                horizontal={true} />
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Collection fields={[
                "non_layer_perils/equipment_breakdown/referral"
              ]} />
            </HX.Pane>
            <HX.Collection fields={[
              "non_layer_perils/equipment_breakdown/travelers"
            ]} />
            <HX.Pane />
          </HX.Pane>
          <HX.Table title="Coverage Extensions"
            data={[
            "perishable_goods",
            "expediting_expense",
            "pollution",
            "data_media",
            "demolition",
            "water_damage"
          ]}
            fields={[
            {
              "field": "covered",
              "width": 250
            },
            {
              "field": "pd_sublimit",
              "width": 250
            }
          ]}
            with="non_layer_perils/equipment_breakdown"
            kb-interactive={true} />
          <HX.Section title="Premium">
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 250
              }
            ]}
              fields={[
              "layer_label",
              "perils/equipment_breakdown/eb_premium",
              "perils/equipment_breakdown/actual_eb_premium"
            ]}
              transpose={true}
              kb-interactive={true} />
          </HX.Section>
        </HX.Section>
        <HX.Section title="TRIA"
          shownBy="non_layer_perils/tria/show_section">
          <HX.Table data={[
            {
              "datum": "layers",
              "width": 250
            }
          ]}
            fields={[
            "layer_label",
            "perils/tria/tria_premium",
            "perils/tria/actual_tria_premium"
          ]}
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Cyber"
          shownBy="non_layer_perils/cyber/show_section">
          <CustomComponent textNode="non_layer_perils/cyber/info_note" />
          <HX.Table data={[
            {
              "datum": "layers",
              "width": 250
            }
          ]}
            fields={[
            "layer_label",
            "perils/cyber/include_affirmative",
            "perils/cyber/include_malicious"
          ]}
            transpose={true}
            kb-interactive={true} />
          <HX.Table data={[
            {
              "datum": "layers",
              "width": 250
            }
          ]}
            fields={[
            "layer_label",
            {
              "field": "perils/cyber/sublimit",
              "shownBy": "control/show_affirmative_cyber"
            },
            {
              "field": "perils/cyber/deductible",
              "shownBy": "control/show_affirmative_cyber"
            },
            {
              "field": "perils/cyber/ensuing_sublimit",
              "shownBy": "control/show_ensuing_loss_cyber"
            },
            {
              "field": "perils/cyber/ensuing_deductible",
              "shownBy": "control/show_ensuing_loss_cyber"
            },
            {
              "field": "perils/cyber/calculated_premium",
              "shownBy": "control/show_affirmative_cyber"
            }
          ]}
            transpose={true}
            kb-interactive={true} />
          <HX.Pane flow="right">
            <HX.Notes field="non_layer_perils/cyber/cyber_coverage_note"
              title="Cyber Coverage Note" />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Schedule"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Management Database Import">
          <HX.Section title="Search Filters">
            <HX.Pane>
              <HX.Collection fields={[
                "exposure_management_api/inputs/accgrpid",
                "exposure_management_api/inputs/account_name"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "exposure_management_api/inputs/reference",
                "exposure_management_api/inputs/team"
              ]}
                horizontal={true} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "exposure_management_api/limit_results"
              ]} />
              <HX.Button task="search_exposure_management_data_task"
                title="Search Exposure Management Database" />
              <HX.Notes field="exposure_management_api/search_fetch_status" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Search Results">
            <HX.Table data={[
              "exposure_management_api/search_results"
            ]}
              fields={[
              "accgrpid",
              "reference",
              "account_number",
              "account_name",
              "last_edit",
              "num_locs",
              "selected"
            ]} />
            <HX.Pane flow="right">
              <HX.Button task="pull_in_exposure_management_data_task"
                title="Pull in Selected" />
              <HX.Notes field="exposure_management_api/location_fetch_status" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Schedule Upload"
          shownBy="policy_information/large_schedule_model"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.File field="schedule/large_schedule_workflow/schedule_file"
                title="Schedule Upload" />
              <HX.Button task="confirm_override_task"
                title="Confirm Upload" />
            </HX.Pane>
            <HX.File field="schedule/large_schedule_workflow/large_schedule_em_file"
              title="Schedule Download" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="SpatialKey Integration">
          <HX.Pane flow="right">
            <HX.Button title="Upload"
              task="run_spatialkey_task" />
            <HX.Notes field="spatialkey/fetch_status" />
            <HX.Button title="Refresh Dashboard Link"
              task="open_spatialkey_dashboard_task" />
            <HX.Notes field="dashboard_note"
              with="spatialkey" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Schedule"
          shownBy="policy_information/small_schedule_model">
          <HX.Pane flow="right">
            <HX.Collection horizontal={true}
              fields={[
              "schedule/schedule_total/num_locs",
              {
                "field": "schedule/schedule_total/tiv_total",
                "labelBy": "schedule/tiv_total_outside_table_label"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane flow="right"
              shownBy="info/remodelling_not_needed">
              <HX.Button task="check_remodel_task"
                title="Remodelling Check" />
              <HX.Notes field="info/remodel_msg" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right"
              shownBy="info/remodelling_needed">
              <HX.Button task="check_remodel_task"
                title="Remodelling Check" />
              <HX.Notes field="info/remodel_msg" />
              <HX.File field="email/remodelling_check_file" />
              <CustomComponent textNode="info/remodelling_info_msg" />
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>
          <HX.Table data={[
            "schedule_total",
            null,
            "schedule_table"
          ]}
            fields={[
            "address_dropdown/country",
            "address_dropdown/state",
            "address_dropdown/county",
            "address_dropdown/city",
            "street_name",
            "zip",
            "property_description",
            "latitude",
            "longitude",
            "currency",
            {
              "field": "tiv_buildings",
              "labelBy": "tiv_buildings_label"
            },
            {
              "field": "tiv_contents",
              "labelBy": "tiv_contents_label"
            },
            {
              "field": "tiv_other",
              "labelBy": "tiv_other_label"
            },
            {
              "field": "tiv_bi",
              "labelBy": "tiv_bi_label"
            },
            {
              "field": "tiv_total",
              "labelBy": "tiv_total_label"
            },
            "fire_deductible",
            "fire_covered",
            "eq_covered",
            "ws_covered",
            "fl_covered",
            "scs_covered",
            "wf_covered",
            "industry_occupancy_dropdown/industry",
            "industry_occupancy_dropdown/occupancy",
            "broker_occu_desc",
            "rms_occupancy",
            "constr_code",
            "raw_constr_code",
            "constr_description",
            "num_buildings",
            "num_stories",
            "year_built",
            "year_updated",
            "sprinkler",
            "catnet_score_tn",
            "catnet_score_ha",
            "katrisk_score_fl",
            "catnet_score_fl",
            "catnet_score_wf",
            "catnet_score_eq",
            "catnet_score_ws",
            "riskmeter_score_wf",
            "pc_code",
            "year_cov_last_replaced",
            "roof_age",
            "floor_area",
            "distance_from_coast",
            "roof_covering",
            "roof_geometry",
            "floodzone",
            "basement",
            "eq_construction_quality",
            "plan_irregularity",
            "soft_story",
            "vertical_irregularity",
            "ornamentation",
            "equipment_eq_bracing",
            "liquefaction",
            "equipment_support_maintenance",
            "pounding",
            "ws_construction_quality",
            "roof_anchor",
            "roof_equipment_hurricane_bracing",
            "cladding_type",
            "frame_foundation_connection",
            "ws_tier",
            "wf_tier",
            "ws_gate",
            "eq_gate",
            "eq_crit_cat_zone",
            "ws_crit_cat_zone",
            "cresta_zone",
            "risk_level_eq",
            "risk_level_ws",
            "risk_level_fl",
            "risk_level_scs",
            "risk_level_wf",
            "loc_id",
            "broker_loc_id",
            "broker_subloc_id"
          ]}
            with="schedule"
            dynamic={true}
            freezeLeft={0}
            kb-interactive={true}
            maxListVisibleRows={10} />
        </HX.Section>
        <HX.Section title="Occupancy Detail"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "non_layer_perils/fire/occupancy_guide/industry_occupancy_dropdown/industry"
            ]} />
            <HX.Collection fields={[
              "non_layer_perils/fire/occupancy_guide/industry_occupancy_dropdown/occupancy"
            ]} />
            <HX.Pane ratio={6} />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes field="non_layer_perils/fire/occupancy_guide/occupancy_description" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Machinery Breakdown">
          <CustomComponent textNode="info/machinery_breakdown_msg" />
          <HX.Pane flow="right">
            <HX.Button task="machinery_breakdown_industry_task"
              title="Load Industries" />
            <HX.Pane ratio={3} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Notes field="non_layer_perils/fire/machinery_breakdown_message" />
            <HX.Pane ratio={3} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table data={[
              "machinery_breakdown"
            ]}
              fields={[
              {
                "field": "industry",
                "width": 300
              },
              {
                "field": "tiv_contents",
                "width": 150
              },
              {
                "field": "fire_mb_proportion",
                "width": 150
              }
            ]}
              kb-interactive={true}
              with="non_layer_perils/fire" />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "non_layer_perils/fire/machinery_breakdown_sublimit"
            ]} />
            <HX.Pane ratio={3} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Run Simulation">
          <HX.Pane flow="right">
            <HX.Notes field="exposure_management_api/simulation_fetch_status" />
            <HX.Button title="Run Simulation"
              task="run_simulation_task" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Run Rater">
          <HX.Pane flow="right">
            <HX.Notes field="schedule/large_schedule_workflow/run_rater_information"
              shownBy="policy_information/large_schedule_model" />
            <HX.Notes field="schedule/small_schedule_workflow/run_rater_information"
              shownBy="policy_information/small_schedule_model" />
            <HX.Pane>
              <HX.Button title="Run Rater"
                task="run_schedule_rater_task" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Warnings/Messages">
          <HX.Notes field="schedule/schedule_warnings" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Experience Rating"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title=""
          collapsible={false}>
          <HX.Pane flow="right">
            <HX.Pane />
            <HX.Button title="Run Rater"
              task="run_schedule_rater_task" />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Initial Selections">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "experience_rating/claims_available",
              {
                "field": "experience_rating/claims_fgu",
                "shownBy": "experience_rating/claims_available"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Basic Experience Rating"
          shownBy="experience_rating/use_experience_rating_basic">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "experience_rating/experience_rating_basic/clean_years",
              "experience_rating/experience_rating_basic/experience_adjustment"
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="apply_experience_adjustment_task"
              title="Populate Non-Cat Experience Adjustment" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Claims Data"
          shownBy="experience_rating/show_claims_input_table">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "experience_rating/claims_net_of_deductible",
                  "shownBy": "experience_rating/show_claims_input_table"
                },
                {
                  "field": "experience_rating/show_to_layer_fields",
                  "shownBy": "experience_rating/use_experience_rating_full"
                }
              ]} />
              <HX.Button task="pull_exchange_rate_claim_data_task"
                title="Push Claims to Experience Rating calculation" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table data={[
              "claims"
            ]}
              fields={[
              "claim_id",
              "claim_made_date",
              "claim_status",
              "cause_of_loss",
              "deductible",
              "incurred_claims",
              "currency",
              "use_claim",
              "is_cat",
              null,
              "estimated_yoa",
              "total_incurred_clm_curr",
              "inflated_total_incurred",
              null,
              "claims_development",
              {
                "field": null,
                "shownBy": "/experience_rating/claims_show_layer_1"
              },
              {
                "field": "deductible_to_use_layer_1",
                "shownBy": "/experience_rating/claims_show_layer_1"
              },
              {
                "field": "limit_layer_1",
                "shownBy": "/experience_rating/claims_show_layer_1"
              },
              {
                "field": "excess_layer_1",
                "shownBy": "/experience_rating/claims_show_layer_1"
              },
              {
                "field": "cl_developed_total_incurred_layer_1",
                "shownBy": "/experience_rating/claims_show_layer_1"
              },
              {
                "field": null,
                "shownBy": "/experience_rating/claims_show_layer_2"
              },
              {
                "field": "deductible_to_use_layer_2",
                "shownBy": "/experience_rating/claims_show_layer_2"
              },
              {
                "field": "limit_layer_2",
                "shownBy": "/experience_rating/claims_show_layer_2"
              },
              {
                "field": "excess_layer_2",
                "shownBy": "/experience_rating/claims_show_layer_2"
              },
              {
                "field": "cl_developed_total_incurred_layer_2",
                "shownBy": "/experience_rating/claims_show_layer_2"
              },
              {
                "field": null,
                "shownBy": "/experience_rating/claims_show_layer_3"
              },
              {
                "field": "deductible_to_use_layer_3",
                "shownBy": "/experience_rating/claims_show_layer_3"
              },
              {
                "field": "limit_layer_3",
                "shownBy": "/experience_rating/claims_show_layer_3"
              },
              {
                "field": "excess_layer_3",
                "shownBy": "/experience_rating/claims_show_layer_3"
              },
              {
                "field": "cl_developed_total_incurred_layer_3",
                "shownBy": "/experience_rating/claims_show_layer_3"
              },
              {
                "field": null,
                "shownBy": "/experience_rating/claims_show_layer_4"
              },
              {
                "field": "deductible_to_use_layer_4",
                "shownBy": "/experience_rating/claims_show_layer_4"
              },
              {
                "field": "limit_layer_4",
                "shownBy": "/experience_rating/claims_show_layer_4"
              },
              {
                "field": "excess_layer_4",
                "shownBy": "/experience_rating/claims_show_layer_4"
              },
              {
                "field": "cl_developed_total_incurred_layer_4",
                "shownBy": "/experience_rating/claims_show_layer_4"
              },
              {
                "field": null,
                "shownBy": "/experience_rating/claims_show_layer_5"
              },
              {
                "field": "deductible_to_use_layer_5",
                "shownBy": "/experience_rating/claims_show_layer_5"
              },
              {
                "field": "limit_layer_5",
                "shownBy": "/experience_rating/claims_show_layer_5"
              },
              {
                "field": "excess_layer_5",
                "shownBy": "/experience_rating/claims_show_layer_5"
              },
              {
                "field": "cl_developed_total_incurred_layer_5",
                "shownBy": "/experience_rating/claims_show_layer_5"
              },
              {
                "field": null,
                "shownBy": "/experience_rating/claims_show_layer_6"
              },
              {
                "field": "deductible_to_use_layer_6",
                "shownBy": "/experience_rating/claims_show_layer_6"
              },
              {
                "field": "limit_layer_6",
                "shownBy": "/experience_rating/claims_show_layer_6"
              },
              {
                "field": "excess_layer_6",
                "shownBy": "/experience_rating/claims_show_layer_6"
              },
              {
                "field": "cl_developed_total_incurred_layer_6",
                "shownBy": "/experience_rating/claims_show_layer_6"
              }
            ]}
              with="experience_rating"
              title="Claims"
              maxListVisibleRows={10}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Experience Rating"
          shownBy="experience_rating/show_claims_input_table">
          <HX.Pane>
            <HX.Section title="Inputs"
              shownBy="experience_rating/show_claims_input_table"
              defaultCollapsed={false}>
              <HX.Notes field="experience_rating/input_instructions" />
              <HX.Table data={[
                {
                  "datum": "experience_rating/experience_table",
                  "elementLabelBy": "str_yoa",
                  "width": 150
                }
              ]}
                fields={[
                "exposure",
                "exposure_inflation",
                "exposure_onlevelled",
                {
                  "field": "premium",
                  "shownBy": "experience_rating/use_experience_rating_agg"
                },
                {
                  "field": "premium_rate_change",
                  "shownBy": "experience_rating/use_experience_rating_agg"
                },
                {
                  "field": "premium_rate_adjusted",
                  "shownBy": "experience_rating/use_experience_rating_agg"
                },
                null,
                "include_year"
              ]}
                transpose={true}
                kb-interactive={true}
                dynamic={true}
                syncColumnWidthsKey="experience_rating_calc" />
            </HX.Section>
            <HX.Section title="Claims Summary"
              shownBy="experience_rating/show_claims_input_table"
              defaultCollapsed={true}>
              <HX.Table data={[
                {
                  "datum": "experience_rating/experience_table",
                  "elementLabelBy": "str_yoa",
                  "width": 150
                }
              ]}
                fields={[
                {
                  "field": null
                },
                {
                  "field": "num_claims_fire"
                },
                {
                  "field": "num_claims_named_windstorm"
                },
                {
                  "field": "num_claims_scs"
                },
                {
                  "field": "num_claims_flood"
                },
                {
                  "field": "num_claims_quake"
                },
                {
                  "field": "num_claims_wildfire"
                },
                {
                  "field": null
                },
                {
                  "field": "unadj_sum_claims_fire"
                },
                {
                  "field": "unadj_sum_claims_named_windstorm"
                },
                {
                  "field": "unadj_sum_claims_scs"
                },
                {
                  "field": "unadj_sum_claims_flood"
                },
                {
                  "field": "unadj_sum_claims_quake"
                },
                {
                  "field": "unadj_sum_claims_wildfire"
                },
                {
                  "field": null
                },
                {
                  "field": "sum_claims_fire"
                },
                {
                  "field": "sum_claims_named_windstorm"
                },
                {
                  "field": "sum_claims_scs"
                },
                {
                  "field": "sum_claims_flood"
                },
                {
                  "field": "sum_claims_quake"
                },
                {
                  "field": "sum_claims_wildfire"
                }
              ]}
                transpose={true}
                kb-interactive={true}
                dynamic={true}
                syncColumnWidthsKey="experience_rating_calc" />
            </HX.Section>
            <HX.Section title="Experience Rating Calculation"
              shownBy="experience_rating/show_claims_input_table"
              defaultCollapsed={true}>
              <HX.Table data={[
                {
                  "datum": "experience_rating/experience_table",
                  "elementLabelBy": "str_yoa",
                  "width": 150
                }
              ]}
                fields={[
                {
                  "field": "loss_ratio",
                  "shownBy": "experience_rating/use_experience_rating_agg"
                },
                {
                  "field": "non_cat_ulr",
                  "shownBy": "experience_rating/use_experience_rating_full"
                },
                {
                  "field": "claims_development",
                  "shownBy": "experience_rating/use_experience_rating_full"
                },
                {
                  "field": "development_method",
                  "shownBy": "experience_rating/use_experience_rating_full"
                },
                {
                  "field": null,
                  "shownBy": "/experience_rating/use_experience_rating_full"
                },
                {
                  "field": "non_cat_ult_layer_1",
                  "shownBy": "/experience_rating/calculation_show_layer_1"
                },
                {
                  "field": "non_cat_ult_layer_2",
                  "shownBy": "/experience_rating/calculation_show_layer_2"
                },
                {
                  "field": "non_cat_ult_layer_3",
                  "shownBy": "/experience_rating/calculation_show_layer_3"
                },
                {
                  "field": "non_cat_ult_layer_4",
                  "shownBy": "/experience_rating/calculation_show_layer_4"
                },
                {
                  "field": "non_cat_ult_layer_5",
                  "shownBy": "/experience_rating/calculation_show_layer_5"
                },
                {
                  "field": "non_cat_ult_layer_6",
                  "shownBy": "/experience_rating/calculation_show_layer_6"
                },
                {
                  "field": null,
                  "shownBy": "/experience_rating/use_experience_rating_full"
                },
                {
                  "field": "non_cat_ult_rate_layer_1",
                  "shownBy": "/experience_rating/calculation_show_layer_1"
                },
                {
                  "field": "non_cat_ult_rate_layer_2",
                  "shownBy": "/experience_rating/calculation_show_layer_2"
                },
                {
                  "field": "non_cat_ult_rate_layer_3",
                  "shownBy": "/experience_rating/calculation_show_layer_3"
                },
                {
                  "field": "non_cat_ult_rate_layer_4",
                  "shownBy": "/experience_rating/calculation_show_layer_4"
                },
                {
                  "field": "non_cat_ult_rate_layer_5",
                  "shownBy": "/experience_rating/calculation_show_layer_5"
                },
                {
                  "field": "non_cat_ult_rate_layer_6",
                  "shownBy": "/experience_rating/calculation_show_layer_6"
                }
              ]}
                transpose={true}
                kb-interactive={true}
                dynamic={true}
                syncColumnWidthsKey="experience_rating_calc" />
            </HX.Section>
            <HX.Section title="Results"
              shownBy="experience_rating/show_claims_input_table"
              defaultCollapsed={false}>
              <HX.Table data={[
                {
                  "datum": "experience_rating/experience_table",
                  "elementLabelBy": "str_yoa",
                  "width": 150
                }
              ]}
                fields={[
                {
                  "field": "loss_ratio",
                  "shownBy": "experience_rating/use_experience_rating_agg"
                },
                {
                  "field": null,
                  "shownBy": "/experience_rating/use_experience_rating_full"
                },
                {
                  "field": "non_cat_ult_rate_layer_1",
                  "shownBy": "/experience_rating/calculation_show_layer_1"
                },
                {
                  "field": "non_cat_ult_rate_layer_2",
                  "shownBy": "/experience_rating/calculation_show_layer_2"
                },
                {
                  "field": "non_cat_ult_rate_layer_3",
                  "shownBy": "/experience_rating/calculation_show_layer_3"
                },
                {
                  "field": "non_cat_ult_rate_layer_4",
                  "shownBy": "/experience_rating/calculation_show_layer_4"
                },
                {
                  "field": "non_cat_ult_rate_layer_5",
                  "shownBy": "/experience_rating/calculation_show_layer_5"
                },
                {
                  "field": "non_cat_ult_rate_layer_6",
                  "shownBy": "/experience_rating/calculation_show_layer_6"
                },
                null,
                {
                  "field": "exposure_weight",
                  "shownBy": "experience_rating/show_weights"
                },
                {
                  "field": "decay_weight",
                  "shownBy": "experience_rating/show_weights"
                },
                {
                  "field": "development_weight",
                  "shownBy": "experience_rating/show_weights"
                },
                {
                  "field": "overall_score",
                  "shownBy": "experience_rating/show_weights"
                },
                "weight_to_year"
              ]}
                transpose={true}
                kb-interactive={true}
                dynamic={true}
                syncColumnWidthsKey="experience_rating_calc" />
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "experience_rating/show_weights"
                ]} />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Section>
            <HX.Pane>
              <HX.Table data={[
                {
                  "datum": "summary_layer_1"
                },
                {
                  "datum": "summary_layer_2"
                },
                {
                  "datum": "summary_layer_3"
                },
                {
                  "datum": "summary_layer_4"
                },
                {
                  "datum": "summary_layer_5"
                },
                {
                  "datum": "summary_layer_6"
                }
              ]}
                fields={[
                {
                  "field": "non_cat_elr_non_cat_prem"
                },
                {
                  "field": "non_cat_expected_loss_ratio",
                  "shownBy": "use_experience_rating_agg"
                },
                {
                  "field": "model_non_cat_loss_ratio",
                  "shownBy": "use_experience_rating_agg"
                },
                {
                  "field": "non_cat_loss_rate",
                  "shownBy": "use_experience_rating_full"
                },
                "non_cat_expected_losses",
                "model_non_cat_expected_losses",
                "cred_weight",
                "experience_adjustment"
              ]}
                with="experience_rating"
                title="Summary"
                filter="filter" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane />
              <HX.Button task="apply_experience_adjustment_task"
                title="Populate Non-Cat Experience Adjustment" />
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        viewScale={0.9}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title=""
          collapsible={false}>
          <HX.Pane flow="right">
            <HX.Button title="Run Simulation"
              task="run_simulation_task" />
            <HX.Button title="Run Rater"
              task="run_schedule_rater_task" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Warnings/Messages"
          shownBy="control/show_run_rater_warning">
          <HX.Notes field="info/run_rater_warning" />
        </HX.Section>
        <HX.Section title="Underwriter Adjustments">
          <HX.Table data={[
            "non_layer_perils/uw_adjustments/risk_man",
            "non_layer_perils/uw_adjustments/experience",
            "non_layer_perils/uw_adjustments/valuation",
            "non_layer_perils/uw_adjustments/other",
            "non_layer_perils/uw_adjustments/total"
          ]}
            fields={[
            {
              "field": "fire",
              "shownBy": "policy_information/doesnt_require_validation/fire",
              "width": 200
            },
            {
              "field": "fire.validation",
              "shownBy": "policy_information/requires_validation/fire",
              "width": 200
            },
            {
              "field": "scs",
              "shownBy": "policy_information/doesnt_require_validation/scs",
              "width": 200
            },
            {
              "field": "scs.validation",
              "shownBy": "policy_information/requires_validation/scs",
              "width": 200
            },
            {
              "field": "flood",
              "shownBy": "policy_information/doesnt_require_validation/flood",
              "width": 200
            },
            {
              "field": "flood.validation",
              "shownBy": "policy_information/requires_validation/flood",
              "width": 200
            },
            {
              "field": "wildfire",
              "shownBy": "policy_information/doesnt_require_validation/wildfire",
              "width": 200
            },
            {
              "field": "wildfire.validation",
              "shownBy": "policy_information/requires_validation/wildfire",
              "width": 200
            },
            {
              "field": "named_windstorm",
              "shownBy": "policy_information/doesnt_require_validation/named_windstorm",
              "width": 200
            },
            {
              "field": "named_windstorm.validation",
              "shownBy": "policy_information/requires_validation/named_windstorm",
              "width": 200
            },
            {
              "field": "quake",
              "shownBy": "policy_information/doesnt_require_validation/quake",
              "width": 200
            },
            {
              "field": "quake.validation",
              "shownBy": "policy_information/requires_validation/quake",
              "width": 200
            }
          ]}
            kb-interactive={true} />
          <HX.Table data={[
            {
              "datum": "layers"
            }
          ]}
            fields={[
            {
              "field": "perils/fire/experience_rating_adj",
              "width": 200
            },
            {
              "field": "perils/scs/experience_rating_adj",
              "width": 200
            },
            {
              "field": "perils/flood/experience_rating_adj",
              "width": 200
            },
            {
              "field": "perils/wildfire/experience_rating_adj",
              "width": 200
            }
          ]}
            title="Non-Cat Experience Rating Adjustments"
            kb-interactive={true} />
          <HX.Pane flow="right">
            <HX.Button task="remove_experience_adjustment_task"
              title="Clear Non-Cat Experience Adjustment" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="KPIs">
          <HX.Pane flow="right">
            <HX.Table title="Pre UW Adj KPIs"
              data={[
              {
                "datum": "layers",
                "width": 150
              }
            ]}
              fields={[
              "layer_label",
              "pre_uw_adjustment/achieved_premium",
              "pre_uw_adjustment/achieved_rate",
              null,
              "pre_uw_adjustment/gross_tech_prem/gross_tech_prem_total",
              "pre_uw_adjustment/gross_tech_prem_rate/gross_tech_prem_rate_total",
              "pre_uw_adjustment/benchmark_premium/benchmark_premium",
              "pre_uw_adjustment/expected_loss/expected_loss",
              null,
              "pre_uw_adjustment/gross_tech_prem/tpi",
              "pre_uw_adjustment/benchmark_premium/bpi",
              "pre_uw_adjustment/expected_loss/elr"
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
            <HX.Table title="Post UW Adj KPIs"
              data={[
              {
                "datum": "layers",
                "width": 150
              }
            ]}
              fields={[
              "layer_label",
              "post_uw_adjustment/achieved_premium",
              "post_uw_adjustment/achieved_rate",
              null,
              "post_uw_adjustment/gross_tech_prem/gross_tech_prem_total",
              "post_uw_adjustment/gross_tech_prem_rate/gross_tech_prem_rate_total",
              "post_uw_adjustment/benchmark_premium/benchmark_premium",
              "post_uw_adjustment/expected_loss/expected_loss",
              null,
              "post_uw_adjustment/gross_tech_prem/tpi",
              "post_uw_adjustment/benchmark_premium/bpi",
              "post_uw_adjustment/expected_loss/elr"
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Peril Details">
          <HX.Pane flow="right">
            <HX.Table title="Pre UW Adj Peril Details"
              data={[
              {
                "datum": "layers",
                "width": 150
              }
            ]}
              fields={[
              "layer_label",
              null,
              "pre_uw_adjustment/gross_tech_prem/fire",
              null,
              "pre_uw_adjustment/gross_tech_prem/us_cat/us_cat_total",
              "pre_uw_adjustment/gross_tech_prem/us_cat/windstorm_us",
              "pre_uw_adjustment/gross_tech_prem/us_cat/tornado_us",
              "pre_uw_adjustment/gross_tech_prem/us_cat/hail_us",
              "pre_uw_adjustment/gross_tech_prem/us_cat/flood_us",
              "pre_uw_adjustment/gross_tech_prem/us_cat/earthquake_us",
              "pre_uw_adjustment/gross_tech_prem/us_cat/wildfire_us",
              null,
              "pre_uw_adjustment/gross_tech_prem/intl_cat/intl_cat_total",
              "pre_uw_adjustment/gross_tech_prem/intl_cat/windstorm_intl",
              "pre_uw_adjustment/gross_tech_prem/intl_cat/tornado_intl",
              "pre_uw_adjustment/gross_tech_prem/intl_cat/hail_intl",
              "pre_uw_adjustment/gross_tech_prem/intl_cat/flood_intl",
              "pre_uw_adjustment/gross_tech_prem/intl_cat/earthquake_intl",
              "pre_uw_adjustment/gross_tech_prem/intl_cat/wildfire_intl",
              {
                "field": null,
                "shownBy": "control/show_cyber_premium"
              },
              {
                "field": "pre_uw_adjustment/gross_tech_prem/cyber",
                "shownBy": "control/show_cyber_premium"
              }
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
            <HX.Table title="Post UW Adj Peril Details"
              data={[
              {
                "datum": "layers",
                "width": 150
              }
            ]}
              fields={[
              "layer_label",
              null,
              "post_uw_adjustment/gross_tech_prem/fire",
              null,
              "post_uw_adjustment/gross_tech_prem/us_cat/us_cat_total",
              "post_uw_adjustment/gross_tech_prem/us_cat/windstorm_us",
              "post_uw_adjustment/gross_tech_prem/us_cat/tornado_us",
              "post_uw_adjustment/gross_tech_prem/us_cat/hail_us",
              "post_uw_adjustment/gross_tech_prem/us_cat/flood_us",
              "post_uw_adjustment/gross_tech_prem/us_cat/earthquake_us",
              "post_uw_adjustment/gross_tech_prem/us_cat/wildfire_us",
              null,
              "post_uw_adjustment/gross_tech_prem/intl_cat/intl_cat_total",
              "post_uw_adjustment/gross_tech_prem/intl_cat/windstorm_intl",
              "post_uw_adjustment/gross_tech_prem/intl_cat/tornado_intl",
              "post_uw_adjustment/gross_tech_prem/intl_cat/hail_intl",
              "post_uw_adjustment/gross_tech_prem/intl_cat/flood_intl",
              "post_uw_adjustment/gross_tech_prem/intl_cat/earthquake_intl",
              "post_uw_adjustment/gross_tech_prem/intl_cat/wildfire_intl",
              {
                "field": null,
                "shownBy": "control/show_cyber_premium"
              },
              {
                "field": "post_uw_adjustment/gross_tech_prem/cyber",
                "shownBy": "control/show_cyber_premium"
              }
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
          </HX.Pane>
          <HX.Section title="Technical Rates"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Table title="Pre UW Adj Peril Details"
                data={[
                {
                  "datum": "layers",
                  "width": 150
                }
              ]}
                fields={[
                "layer_label",
                null,
                "pre_uw_adjustment/gross_tech_prem_rate/gross_tech_prem_rate_total",
                null,
                "pre_uw_adjustment/gross_tech_prem_rate/fire",
                null,
                "pre_uw_adjustment/gross_tech_prem_rate/us_cat/us_cat_total",
                "pre_uw_adjustment/gross_tech_prem_rate/us_cat/windstorm_us",
                "pre_uw_adjustment/gross_tech_prem_rate/us_cat/tornado_us",
                "pre_uw_adjustment/gross_tech_prem_rate/us_cat/hail_us",
                "pre_uw_adjustment/gross_tech_prem_rate/us_cat/flood_us",
                "pre_uw_adjustment/gross_tech_prem_rate/us_cat/earthquake_us",
                "pre_uw_adjustment/gross_tech_prem_rate/us_cat/wildfire_us",
                null,
                "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/intl_cat_total",
                "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/windstorm_intl",
                "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/tornado_intl",
                "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/hail_intl",
                "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/flood_intl",
                "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/earthquake_intl",
                "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/wildfire_intl",
                {
                  "field": null,
                  "shownBy": "control/show_cyber_premium"
                },
                {
                  "field": "pre_uw_adjustment/gross_tech_prem_rate/cyber",
                  "shownBy": "control/show_cyber_premium"
                }
              ]}
                kb-interactive={true}
                transpose={true}
                freezeLeft={0} />
              <HX.Table title="Post UW Adj Peril Details"
                data={[
                {
                  "datum": "layers",
                  "width": 150
                }
              ]}
                fields={[
                "layer_label",
                null,
                "post_uw_adjustment/gross_tech_prem_rate/gross_tech_prem_rate_total",
                null,
                "post_uw_adjustment/gross_tech_prem_rate/fire",
                null,
                "post_uw_adjustment/gross_tech_prem_rate/us_cat/us_cat_total",
                "post_uw_adjustment/gross_tech_prem_rate/us_cat/windstorm_us",
                "post_uw_adjustment/gross_tech_prem_rate/us_cat/tornado_us",
                "post_uw_adjustment/gross_tech_prem_rate/us_cat/hail_us",
                "post_uw_adjustment/gross_tech_prem_rate/us_cat/flood_us",
                "post_uw_adjustment/gross_tech_prem_rate/us_cat/earthquake_us",
                "post_uw_adjustment/gross_tech_prem_rate/us_cat/wildfire_us",
                null,
                "post_uw_adjustment/gross_tech_prem_rate/intl_cat/intl_cat_total",
                "post_uw_adjustment/gross_tech_prem_rate/intl_cat/windstorm_intl",
                "post_uw_adjustment/gross_tech_prem_rate/intl_cat/tornado_intl",
                "post_uw_adjustment/gross_tech_prem_rate/intl_cat/hail_intl",
                "post_uw_adjustment/gross_tech_prem_rate/intl_cat/flood_intl",
                "post_uw_adjustment/gross_tech_prem_rate/intl_cat/earthquake_intl",
                "post_uw_adjustment/gross_tech_prem_rate/intl_cat/wildfire_intl",
                {
                  "field": null,
                  "shownBy": "control/show_cyber_premium"
                },
                {
                  "field": "post_uw_adjustment/gross_tech_prem_rate/cyber",
                  "shownBy": "control/show_cyber_premium"
                }
              ]}
                kb-interactive={true}
                transpose={true}
                freezeLeft={0} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Expected Loss"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Table title="Pre UW Adj Peril Details"
                data={[
                {
                  "datum": "layers",
                  "width": 150
                }
              ]}
                fields={[
                "layer_label",
                null,
                "pre_uw_adjustment/expected_loss/fire",
                null,
                "pre_uw_adjustment/expected_loss/us_cat/us_cat_total",
                "pre_uw_adjustment/expected_loss/us_cat/windstorm_us",
                "pre_uw_adjustment/expected_loss/us_cat/tornado_us",
                "pre_uw_adjustment/expected_loss/us_cat/hail_us",
                "pre_uw_adjustment/expected_loss/us_cat/flood_us",
                "pre_uw_adjustment/expected_loss/us_cat/earthquake_us",
                "pre_uw_adjustment/expected_loss/us_cat/wildfire_us",
                null,
                "pre_uw_adjustment/expected_loss/intl_cat/intl_cat_total",
                "pre_uw_adjustment/expected_loss/intl_cat/windstorm_intl",
                "pre_uw_adjustment/expected_loss/intl_cat/tornado_intl",
                "pre_uw_adjustment/expected_loss/intl_cat/hail_intl",
                "pre_uw_adjustment/expected_loss/intl_cat/flood_intl",
                "pre_uw_adjustment/expected_loss/intl_cat/earthquake_intl",
                "pre_uw_adjustment/expected_loss/intl_cat/wildfire_intl",
                {
                  "field": null,
                  "shownBy": "control/show_cyber_premium"
                },
                {
                  "field": "pre_uw_adjustment/expected_loss/cyber",
                  "shownBy": "control/show_cyber_premium"
                }
              ]}
                kb-interactive={true}
                transpose={true}
                freezeLeft={0} />
              <HX.Table title="Post UW Adj Peril Details"
                data={[
                {
                  "datum": "layers",
                  "width": 150
                }
              ]}
                fields={[
                "layer_label",
                null,
                "post_uw_adjustment/expected_loss/fire",
                null,
                "post_uw_adjustment/expected_loss/us_cat/us_cat_total",
                "post_uw_adjustment/expected_loss/us_cat/windstorm_us",
                "post_uw_adjustment/expected_loss/us_cat/tornado_us",
                "post_uw_adjustment/expected_loss/us_cat/hail_us",
                "post_uw_adjustment/expected_loss/us_cat/flood_us",
                "post_uw_adjustment/expected_loss/us_cat/earthquake_us",
                "post_uw_adjustment/expected_loss/us_cat/wildfire_us",
                null,
                "post_uw_adjustment/expected_loss/intl_cat/intl_cat_total",
                "post_uw_adjustment/expected_loss/intl_cat/windstorm_intl",
                "post_uw_adjustment/expected_loss/intl_cat/tornado_intl",
                "post_uw_adjustment/expected_loss/intl_cat/hail_intl",
                "post_uw_adjustment/expected_loss/intl_cat/flood_intl",
                "post_uw_adjustment/expected_loss/intl_cat/earthquake_intl",
                "post_uw_adjustment/expected_loss/intl_cat/wildfire_intl",
                {
                  "field": null,
                  "shownBy": "control/show_cyber_premium"
                },
                {
                  "field": "post_uw_adjustment/expected_loss/cyber",
                  "shownBy": "control/show_cyber_premium"
                }
              ]}
                kb-interactive={true}
                transpose={true}
                freezeLeft={0} />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Technical Premium Breakdown">
          <HX.Pane flow="right">
            <HX.Table title="Pre UW Adj Technical Premium Breakdown"
              data={[
              {
                "datum": "layers",
                "width": 150
              }
            ]}
              fields={[
              "layer_label",
              "pre_uw_adjustment/expected_loss/expected_loss",
              "pre_uw_adjustment/tech_prem_components/coc",
              "pre_uw_adjustment/tech_prem_components/direct_expenses",
              "pre_uw_adjustment/tech_prem_components/indirect_expenses",
              "pre_uw_adjustment/tech_prem_components/lae",
              "pre_uw_adjustment/tech_prem_components/ri",
              "pre_uw_adjustment/tech_prem_components/sd",
              "pre_uw_adjustment/tech_prem_components/investment_income",
              "pre_uw_adjustment/net_tech_prem/net_tech_prem_total",
              "pre_uw_adjustment/gross_tech_prem/gross_tech_prem_total"
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
            <HX.Table title="Post UW Adj Technical Premium Breakdown"
              data={[
              {
                "datum": "layers",
                "width": 150
              }
            ]}
              fields={[
              "layer_label",
              "post_uw_adjustment/expected_loss/expected_loss",
              "post_uw_adjustment/tech_prem_components/coc",
              "post_uw_adjustment/tech_prem_components/direct_expenses",
              "post_uw_adjustment/tech_prem_components/indirect_expenses",
              "post_uw_adjustment/tech_prem_components/lae",
              "post_uw_adjustment/tech_prem_components/ri",
              "post_uw_adjustment/tech_prem_components/sd",
              "post_uw_adjustment/tech_prem_components/investment_income",
              "post_uw_adjustment/net_tech_prem/net_tech_prem_total",
              "post_uw_adjustment/gross_tech_prem/gross_tech_prem_total"
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Risk Appetite Summary">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 150
              }
            ]}
              fields={[
              "layer_label",
              "risk_appetite_summary/us_wind_aal",
              "risk_appetite_summary/us_quake_aal",
              "risk_appetite_summary/us_all_perils_aal",
              null,
              "risk_appetite_summary/us_wind_sd",
              "risk_appetite_summary/us_quake_sd",
              "risk_appetite_summary/us_all_perils_sd",
              null,
              "risk_appetite_summary/aep_impact_1_in_10",
              "risk_appetite_summary/oep_impact_1_in_250",
              "risk_appetite_summary/aep_impact_1_in_10_wrt_line",
              "risk_appetite_summary/oep_impact_1_in_250_wrt_line",
              null,
              "risk_appetite_summary/oep_impact_1_in_250_cat_premium_ratio",
              null,
              "risk_appetite_summary/intl_wind_aal",
              "risk_appetite_summary/intl_quake_aal",
              "risk_appetite_summary/intl_all_perils_aal",
              null,
              "risk_appetite_summary/intl_wind_sd",
              "risk_appetite_summary/intl_quake_sd",
              "risk_appetite_summary/intl_all_perils_sd"
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Additional Diagnostics">
          <HX.Pane flow="down">
            <HX.Table title="CAT/AOP Splits"
              data={[
              {
                "datum": "layers",
                "width": 150
              }
            ]}
              fields={[
              "layer_label",
              "cat_aop_split/perc_us_wind",
              "cat_aop_split/perc_us_quake",
              "cat_aop_split/perc_us_aop",
              "cat_aop_split/perc_intl_cat",
              "cat_aop_split/perc_intl_aop"
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
            <HX.Table title="Trapped Exposure"
              data={[
              {
                "datum": "layers",
                "width": 150
              }
            ]}
              fields={[
              "layer_label",
              "trapped_exposure",
              "trapped_exposure_rate"
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Simulation Output"
          defaultCollapsed={true}>
          <HX.Section title="RDS Events"
            defaultCollapsed={true}>
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "simulation_output/rds_events/ca_quake_la",
              "simulation_output/rds_events/ca_quake_sf",
              "simulation_output/rds_events/nm_quake",
              "simulation_output/rds_events/nm_extreme_stress",
              "simulation_output/rds_events/nw_quake",
              "simulation_output/rds_events/fl_wind_miami",
              "simulation_output/rds_events/fl_wind_pinellas",
              "simulation_output/rds_events/us_wind_gulf_of_mexico",
              "simulation_output/rds_events/carolinas_wind",
              "simulation_output/rds_events/north_east_wind"
            ]}
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
          <HX.Section title="Account OEP - 100% Ground Up Loss"
            defaultCollapsed={true}>
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "simulation_output/acc_oep_gu_loss/one_in_10000",
              "simulation_output/acc_oep_gu_loss/one_in_5000",
              "simulation_output/acc_oep_gu_loss/one_in_1000",
              "simulation_output/acc_oep_gu_loss/one_in_500",
              "simulation_output/acc_oep_gu_loss/one_in_250",
              "simulation_output/acc_oep_gu_loss/one_in_200",
              "simulation_output/acc_oep_gu_loss/one_in_150",
              "simulation_output/acc_oep_gu_loss/one_in_100",
              "simulation_output/acc_oep_gu_loss/one_in_50",
              "simulation_output/acc_oep_gu_loss/one_in_30",
              "simulation_output/acc_oep_gu_loss/one_in_10",
              "simulation_output/acc_oep_gu_loss/one_in_2"
            ]}
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
          <HX.Section title="Smooth Property + Treaty + Risk OEP - AFB Share Gross Loss"
            defaultCollapsed={true}>
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "simulation_output/pt_oep_loss/one_in_10000",
              "simulation_output/pt_oep_loss/one_in_5000",
              "simulation_output/pt_oep_loss/one_in_1000",
              "simulation_output/pt_oep_loss/one_in_500",
              "simulation_output/pt_oep_loss/one_in_250",
              "simulation_output/pt_oep_loss/one_in_200",
              "simulation_output/pt_oep_loss/one_in_150",
              "simulation_output/pt_oep_loss/one_in_100",
              "simulation_output/pt_oep_loss/one_in_50",
              "simulation_output/pt_oep_loss/one_in_30",
              "simulation_output/pt_oep_loss/one_in_10",
              "simulation_output/pt_oep_loss/one_in_2"
            ]}
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
          <HX.Section title="Smooth Property + Treaty + Risk AEP - AFB Share Gross Loss"
            defaultCollapsed={true}>
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 200
              }
            ]}
              fields={[
              "layer_label",
              "simulation_output/pt_aep_loss/one_in_10000",
              "simulation_output/pt_aep_loss/one_in_5000",
              "simulation_output/pt_aep_loss/one_in_1000",
              "simulation_output/pt_aep_loss/one_in_500",
              "simulation_output/pt_aep_loss/one_in_250",
              "simulation_output/pt_aep_loss/one_in_200",
              "simulation_output/pt_aep_loss/one_in_150",
              "simulation_output/pt_aep_loss/one_in_100",
              "simulation_output/pt_aep_loss/one_in_50",
              "simulation_output/pt_aep_loss/one_in_30",
              "simulation_output/pt_aep_loss/one_in_10",
              "simulation_output/pt_aep_loss/one_in_2"
            ]}
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
        </HX.Section>
        <HX.Section title="Output File"
          shownBy="policy_information/large_schedule_model"
          defaultCollapsed={true}>
          <HX.File field="schedule/large_schedule_workflow/schedule_output_file"
            title="Output Calculation File" />
        </HX.Section>
        <HX.Section title="DF Output"
          shownBy="policy_information/is_case_priced"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.File field="df_output" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Account Segmentation"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Visualisation ">
          <HX.Pane flow="right">
            <HX.Pane>
              <CustomComponent title="Countries"
                node_path="pricing_layer_segmentation/state_country_choropleth_data"
                zs={[
                "tiv",
                "num_locations",
                "gu_loss",
                "gu_tech_rate"
              ]}
                options={[
                "TIV",
                "Num of locations",
                "GU Loss",
                "GU Tech Rate"
              ]}
                percentFormat={[
                false,
                false,
                false,
                true
              ]}
                withMarkers={false} />
            </HX.Pane>
            <HX.Pane>
              <CustomComponent title="States"
                node_path="pricing_layer_segmentation/state_country_choropleth_data"
                zs={[
                "tiv",
                "num_locations",
                "gu_loss",
                "gu_tech_rate"
              ]}
                options={[
                "TIV",
                "Num of locations",
                "GU Loss",
                "GU Tech Rate"
              ]}
                percentFormat={[
                false,
                false,
                false,
                true
              ]}
                withMarkers={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Account Segmentation by Layer">
          <HX.Selector data={[
            "layers"
          ]}
            dropdown="layer_label">
            <HX.Section title="Exposure Segmentation">
              <HX.Pane flow="right">
                <HX.Pane ratio={1}>
                  <HX.Collection fields={[
                    "segmentation_tables/table_selector"
                  ]} />
                </HX.Pane>
                <HX.Pane ratio={4}>
                  <CustomComponent title="TIV and Location Segmentation"
                    data={[
                    {
                      "labelBy": "name",
                      "list": "other_segmentations/state_summary"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#dc1998",
                      "field": "tiv",
                      "label": "TIV"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "other_segmentations/state_summary",
                          "x": "name",
                          "y": "num_locations"
                        }
                      ],
                      "seriesColor": "#4b0050",
                      "seriesLabel": "No of Locs"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    gapBetweenBarsSize={0.05}
                    xAxisLabel="State"
                    yAxisLabel="TIV"
                    yAxis2Label="No of Locs"
                    shownBy="segmentation_tables/show_segmentation_tables/state" />
                  <CustomComponent title="TIV and Location Segmentation"
                    data={[
                    {
                      "labelBy": "name",
                      "list": "perils/fire/occupancy_summary"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#dc1998",
                      "field": "tiv",
                      "label": "TIV"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "perils/fire/occupancy_summary",
                          "x": "name",
                          "y": "num_locations"
                        }
                      ],
                      "seriesColor": "#4b0050",
                      "seriesLabel": "No of Locs"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    gapBetweenBarsSize={0.05}
                    xAxisLabel="Occupancy"
                    yAxisLabel="TIV"
                    yAxis2Label="No of Locs"
                    shownBy="segmentation_tables/show_segmentation_tables/fire_occupancy" />
                  <CustomComponent title="TIV and Location Segmentation"
                    data={[
                    {
                      "labelBy": "name",
                      "list": "perils/fire/construction_summary"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#dc1998",
                      "field": "tiv",
                      "label": "TIV"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "perils/fire/construction_summary",
                          "x": "name",
                          "y": "num_locations"
                        }
                      ],
                      "seriesColor": "#4b0050",
                      "seriesLabel": "No of Locs"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    gapBetweenBarsSize={0.05}
                    xAxisLabel="Construction"
                    yAxisLabel="TIV"
                    yAxis2Label="No of Locs"
                    shownBy="segmentation_tables/show_segmentation_tables/fire_construction" />
                  <CustomComponent title="TIV and Location Segmentation"
                    data={[
                    {
                      "labelBy": "name",
                      "list": "perils/named_windstorm/ws_zone_summary"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#dc1998",
                      "field": "tiv",
                      "label": "TIV"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "perils/named_windstorm/ws_zone_summary",
                          "x": "name",
                          "y": "num_locations"
                        }
                      ],
                      "seriesColor": "#4b0050",
                      "seriesLabel": "No of Locs"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    gapBetweenBarsSize={0.05}
                    xAxisLabel="WS Zone"
                    yAxisLabel="TIV"
                    yAxis2Label="No of Locs"
                    shownBy="segmentation_tables/show_segmentation_tables/ws_zone" />
                  <CustomComponent title="TIV and Location Segmentation"
                    data={[
                    {
                      "labelBy": "name",
                      "list": "perils/named_windstorm/distance_from_coast_summary"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#dc1998",
                      "field": "tiv",
                      "label": "TIV"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "perils/named_windstorm/distance_from_coast_summary",
                          "x": "name",
                          "y": "num_locations"
                        }
                      ],
                      "seriesColor": "#4b0050",
                      "seriesLabel": "No of Locs"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    gapBetweenBarsSize={0.05}
                    xAxisLabel="DTC"
                    yAxisLabel="TIV"
                    yAxis2Label="No of Locs"
                    shownBy="segmentation_tables/show_segmentation_tables/dtc" />
                  <CustomComponent title="TIV and Location Segmentation"
                    data={[
                    {
                      "labelBy": "name",
                      "list": "perils/quake/eq_zone_summary"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#dc1998",
                      "field": "tiv",
                      "label": "TIV"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "perils/quake/eq_zone_summary",
                          "x": "name",
                          "y": "num_locations"
                        }
                      ],
                      "seriesColor": "#4b0050",
                      "seriesLabel": "No of Locs"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    gapBetweenBarsSize={0.05}
                    xAxisLabel="Quake Zone"
                    yAxisLabel="TIV"
                    yAxis2Label="No of Locs"
                    shownBy="segmentation_tables/show_segmentation_tables/eq_zone" />
                </HX.Pane>
              </HX.Pane>
              <HX.Button task="produce_heatmap_task"
                title="Generate Exposure Map" />
              <HX.Section title="Exposure Map"
                shownBy="/pricing_layer_segmentation/show_file_component">
                <HX.File field="/pricing_layer_segmentation/heatmap_file" />
              </HX.Section>
            </HX.Section>
            <HX.Section title="Exposure Segmentation (detailed)">
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Table data={[
                    "perils/fire/occupancy_summary"
                  ]}
                    fields={[
                    {
                      "field": "name",
                      "width": 400
                    },
                    "tiv",
                    "itv",
                    "num_locations",
                    "gu_tech_rate",
                    "total_gu_tech_rate"
                  ]}
                    title="Occupancy Summary"
                    kb-interactive={true}
                    dynamic={true} />
                  <HX.Table data={[
                    "perils/fire/sprinkler_summary"
                  ]}
                    fields={[
                    {
                      "field": "name",
                      "width": 400
                    },
                    "tiv",
                    "itv",
                    "num_locations",
                    "gu_tech_rate",
                    "total_gu_tech_rate"
                  ]}
                    title="Sprinkler Summary"
                    kb-interactive={true}
                    dynamic={true} />
                  <HX.Table data={[
                    "perils/fire/construction_summary"
                  ]}
                    fields={[
                    {
                      "field": "name",
                      "width": 400
                    },
                    "tiv",
                    "itv",
                    "num_locations",
                    "gu_tech_rate",
                    "total_gu_tech_rate"
                  ]}
                    title="Construction Summary"
                    kb-interactive={true}
                    dynamic={true} />
                  <HX.Table data={[
                    "perils/quake/eq_zone_summary"
                  ]}
                    fields={[
                    {
                      "field": "name",
                      "width": 400
                    },
                    "tiv",
                    "itv",
                    "num_locations",
                    "gu_tech_rate",
                    "total_gu_tech_rate"
                  ]}
                    title="EQ Zone"
                    kb-interactive={true}
                    dynamic={true} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Table data={[
                    "perils/named_windstorm/ws_zone_summary"
                  ]}
                    fields={[
                    {
                      "field": "name",
                      "width": 400
                    },
                    "tiv",
                    "itv",
                    "num_locations",
                    "gu_tech_rate",
                    "total_gu_tech_rate"
                  ]}
                    title="WS Zone"
                    kb-interactive={true}
                    dynamic={true} />
                  <HX.Table data={[
                    "perils/named_windstorm/distance_from_coast_summary"
                  ]}
                    fields={[
                    {
                      "field": "name",
                      "width": 400
                    },
                    "tiv",
                    "itv",
                    "num_locations",
                    "gu_tech_rate",
                    "total_gu_tech_rate"
                  ]}
                    title="DTC"
                    kb-interactive={true}
                    dynamic={true} />
                  <HX.Table data={[
                    "perils/named_windstorm/year_built_summary"
                  ]}
                    fields={[
                    {
                      "field": "name",
                      "width": 400
                    },
                    "tiv",
                    "itv",
                    "num_locations",
                    "gu_tech_rate",
                    "total_gu_tech_rate"
                  ]}
                    title="Construction Summary"
                    kb-interactive={true}
                    dynamic={true} />
                  <HX.Table data={[
                    "other_segmentations/state_summary"
                  ]}
                    fields={[
                    {
                      "field": "name",
                      "width": 400
                    },
                    "tiv",
                    "itv",
                    "num_locations",
                    "total_gu_tech_rate"
                  ]}
                    title="State Summary"
                    kb-interactive={true}
                    dynamic={true} />
                </HX.Pane>
              </HX.Pane>
            </HX.Section>
          </HX.Selector>
        </HX.Section>
        <HX.Section title="Pricing Layer Segmentation">
          <HX.Section title="Marginal Impact Summary">
            <HX.Table with="pricing_layer_segmentation/marginal_impact_summary"
              data={[
              "mi_1_in_10_aep_pt",
              "mi_1_in_250_oep_pt"
            ]}
              fields={[
              "layer1",
              "layer2",
              "layer3",
              "layer4",
              "layer5",
              "layer6"
            ]} />
          </HX.Section>
          <HX.Section title="Global Summary">
            <HX.Table title=""
              data={[
              "pricing_layer_segmentation/country"
            ]}
              fields={[
              {
                "field": "name",
                "width": 400
              },
              "tiv",
              "num_locations",
              "gu_loss",
              "gu_tech_rate",
              "gu_prem",
              "tech_prem_layer1",
              "tech_prem_layer2",
              "tech_prem_layer3",
              "tech_prem_layer4",
              "tech_prem_layer5",
              "tech_prem_layer6",
              "uw_adj_tech_prem_layer1",
              "uw_adj_tech_prem_layer2",
              "uw_adj_tech_prem_layer3",
              "uw_adj_tech_prem_layer4",
              "uw_adj_tech_prem_layer5",
              "uw_adj_tech_prem_layer6"
            ]}
              freezeLeft={1}
              kb-interactive={true} />
            <HX.Selector data={[
              "pricing_layer_segmentation/state_country_outer"
            ]}
              dropdown="country">
              <HX.Table title="Country Drilldown"
                data={[
                "country_list"
              ]}
                fields={[
                {
                  "field": "name",
                  "width": 400
                },
                "tiv",
                "num_locations",
                "gu_loss",
                "gu_tech_rate",
                "gu_prem",
                "tech_prem_layer1",
                "tech_prem_layer2",
                "tech_prem_layer3",
                "tech_prem_layer4",
                "tech_prem_layer5",
                "tech_prem_layer6",
                "uw_adj_tech_prem_layer1",
                "uw_adj_tech_prem_layer2",
                "uw_adj_tech_prem_layer3",
                "uw_adj_tech_prem_layer4",
                "uw_adj_tech_prem_layer5",
                "uw_adj_tech_prem_layer6"
              ]}
                freezeLeft={1}
                kb-interactive={true} />
            </HX.Selector>
          </HX.Section>
          <HX.Section title="Peril Summaries">
            <HX.Table title=""
              data={[
              "pricing_layer_segmentation/fire_occupancy"
            ]}
              fields={[
              {
                "field": "name",
                "width": 400
              },
              "tiv",
              "num_locations",
              "gu_loss",
              "gu_tech_rate",
              "gu_prem",
              "tech_prem_layer1",
              "tech_prem_layer2",
              "tech_prem_layer3",
              "tech_prem_layer4",
              "tech_prem_layer5",
              "tech_prem_layer6",
              "uw_adj_tech_prem_layer1",
              "uw_adj_tech_prem_layer2",
              "uw_adj_tech_prem_layer3",
              "uw_adj_tech_prem_layer4",
              "uw_adj_tech_prem_layer5",
              "uw_adj_tech_prem_layer6"
            ]}
              freezeLeft={1}
              kb-interactive={true} />
            <HX.Table title=""
              data={[
              "pricing_layer_segmentation/ws_zone"
            ]}
              fields={[
              {
                "field": "name",
                "width": 400
              },
              "tiv",
              "num_locations",
              "gu_loss",
              "gu_tech_rate",
              "gu_prem",
              "tech_prem_layer1",
              "tech_prem_layer2",
              "tech_prem_layer3",
              "tech_prem_layer4",
              "tech_prem_layer5",
              "tech_prem_layer6",
              "uw_adj_tech_prem_layer1",
              "uw_adj_tech_prem_layer2",
              "uw_adj_tech_prem_layer3",
              "uw_adj_tech_prem_layer4",
              "uw_adj_tech_prem_layer5",
              "uw_adj_tech_prem_layer6"
            ]}
              freezeLeft={1}
              kb-interactive={true} />
            <HX.Table title=""
              data={[
              "pricing_layer_segmentation/eq_zone"
            ]}
              fields={[
              {
                "field": "name",
                "width": 400
              },
              "tiv",
              "num_locations",
              "gu_loss",
              "gu_tech_rate",
              "gu_prem",
              "tech_prem_layer1",
              "tech_prem_layer2",
              "tech_prem_layer3",
              "tech_prem_layer4",
              "tech_prem_layer5",
              "tech_prem_layer6",
              "uw_adj_tech_prem_layer1",
              "uw_adj_tech_prem_layer2",
              "uw_adj_tech_prem_layer3",
              "uw_adj_tech_prem_layer4",
              "uw_adj_tech_prem_layer5",
              "uw_adj_tech_prem_layer6"
            ]}
              freezeLeft={1}
              kb-interactive={true} />
            <HX.Table title=""
              data={[
              "pricing_layer_segmentation/fl_risk_category"
            ]}
              fields={[
              {
                "field": "name",
                "width": 400
              },
              "tiv",
              "num_locations",
              "gu_loss",
              "gu_tech_rate",
              "gu_prem",
              "tech_prem_layer1",
              "tech_prem_layer2",
              "tech_prem_layer3",
              "tech_prem_layer4",
              "tech_prem_layer5",
              "tech_prem_layer6",
              "uw_adj_tech_prem_layer1",
              "uw_adj_tech_prem_layer2",
              "uw_adj_tech_prem_layer3",
              "uw_adj_tech_prem_layer4",
              "uw_adj_tech_prem_layer5",
              "uw_adj_tech_prem_layer6"
            ]}
              freezeLeft={1}
              kb-interactive={true} />
            <HX.Table title=""
              data={[
              "pricing_layer_segmentation/wf_risk_category"
            ]}
              fields={[
              {
                "field": "name",
                "width": 400
              },
              "tiv",
              "num_locations",
              "gu_loss",
              "gu_tech_rate",
              "gu_prem",
              "tech_prem_layer1",
              "tech_prem_layer2",
              "tech_prem_layer3",
              "tech_prem_layer4",
              "tech_prem_layer5",
              "tech_prem_layer6",
              "uw_adj_tech_prem_layer1",
              "uw_adj_tech_prem_layer2",
              "uw_adj_tech_prem_layer3",
              "uw_adj_tech_prem_layer4",
              "uw_adj_tech_prem_layer5",
              "uw_adj_tech_prem_layer6"
            ]}
              freezeLeft={1}
              kb-interactive={true} />
            <HX.Table title=""
              data={[
              "pricing_layer_segmentation/scs_risk_category"
            ]}
              fields={[
              {
                "field": "name",
                "width": 400
              },
              "tiv",
              "num_locations",
              "gu_loss",
              "gu_tech_rate",
              "gu_prem",
              "tech_prem_layer1",
              "tech_prem_layer2",
              "tech_prem_layer3",
              "tech_prem_layer4",
              "tech_prem_layer5",
              "tech_prem_layer6",
              "uw_adj_tech_prem_layer1",
              "uw_adj_tech_prem_layer2",
              "uw_adj_tech_prem_layer3",
              "uw_adj_tech_prem_layer4",
              "uw_adj_tech_prem_layer5",
              "uw_adj_tech_prem_layer6"
            ]}
              freezeLeft={1}
              kb-interactive={true} />
          </HX.Section>
        </HX.Section>
      </HX.Page>
      <HX.Page title="By Peril Summary"
        fullWidth={true}
        viewScale={0.9}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Fire Rating"
          defaultCollapsed={true}
          shownBy="non_layer_perils/fire/show_section">
          <HX.Selector data={[
            "layers"
          ]}
            dropdown="layer_label">
            <HX.Section title="Modifier Summary">
              <HX.Table data={[
                "perils/fire/modifier_summary"
              ]}
                fields={[
                "peril_name",
                "no_of_locs",
                "sum_tiv_total_usd",
                "occupancy",
                "construction",
                "pc_code",
                "sprinkler",
                "bi_waiting_period",
                "bi_indemnity_period",
                "cbi",
                "fire_size_discount",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true} />
            </HX.Section>
            <HX.Section title="Risk Factors Summary">
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/fire/occupancy_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Occupancy Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Table data={[
                  "perils/fire/construction_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Construction Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
              </HX.Pane>
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/fire/sprinkler_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Sprinkler Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Table title="Machinery Breakdown Summary"
                  data={[
                  "perils/fire/machinery_breakdown_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "fire_mb_proportion",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Section>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/policy_information/top_20_sort_by"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Section title="Top 20 Largest Locations">
              <HX.Table data={[
                "perils/fire/top_20_locations_summary"
              ]}
                fields={[
                "country",
                "state",
                "county",
                "zip",
                "tiv_buildings",
                "tiv_contents_total",
                "tiv_bi",
                "tiv_total",
                "itv",
                "base_rate",
                "occupancy",
                "construction",
                "pc_code",
                "sprinkler",
                "bi_waiting_period",
                "bi_indemnity_period",
                "cbi",
                "fire_size_discount",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true}
                minListVisibleRows={30} />
            </HX.Section>
          </HX.Selector>
        </HX.Section>
        <HX.Section title="SCS Rating"
          defaultCollapsed={true}
          shownBy="non_layer_perils/scs/show_section">
          <HX.Selector data={[
            "layers"
          ]}
            dropdown="layer_label">
            <HX.Section title="Modifier Summary">
              <HX.Table data={[
                "perils/scs/modifier_summary"
              ]}
                fields={[
                "peril_name",
                "num_locs",
                "sum_tiv_total_usd",
                "occupancy",
                "construction",
                "year_built",
                "floor_area",
                "roof_age",
                "roof_covering",
                "roof_geometry",
                "catnet_score",
                "size_discount",
                "total_modifier_impact",
                "worth",
                "gu_tech_rate",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true} />
            </HX.Section>
            <HX.Section title="Risk Factors Summary">
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/scs/risk_category_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Risk Category"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Table data={[
                  "perils/scs/construction_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Construction Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
              </HX.Pane>
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/scs/occupancy_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Occupancy Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Pane />
              </HX.Pane>
            </HX.Section>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/policy_information/top_20_sort_by"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Section title="Top 20 Largest Locations">
              <HX.Table data={[
                "perils/scs/top_20_locations_summary"
              ]}
                fields={[
                "country",
                "state",
                "county",
                "zip",
                "tiv_buildings",
                "tiv_contents_total",
                "tiv_bi",
                "tiv_total",
                "itv",
                "base_rate",
                "occupancy",
                "construction",
                "year_built",
                "floor_area",
                "roof_age",
                "roof_covering",
                "roof_geometry",
                "catnet_score",
                "size_discount",
                "total_modifier_impact",
                "worth",
                "gu_tech_rate",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true}
                minListVisibleRows={30} />
            </HX.Section>
          </HX.Selector>
        </HX.Section>
        <HX.Section title="Flood Rating"
          defaultCollapsed={true}
          shownBy="non_layer_perils/flood/show_section">
          <HX.Selector data={[
            "layers"
          ]}
            dropdown="layer_label">
            <HX.Section title="Modifier Summary">
              <HX.Table data={[
                "perils/flood/modifier_summary"
              ]}
                fields={[
                "peril_name",
                "no_of_locs",
                "sum_tiv_total_usd",
                "construction",
                "num_of_floors",
                "basement",
                "elevation",
                "katrisk_catnet_score",
                "size_discount",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true} />
            </HX.Section>
            <HX.Section title="Risk Factors Summary">
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/flood/risk_category_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Flood Risk Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Table data={[
                  "perils/flood/construction_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Construction Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
              </HX.Pane>
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/flood/num_of_floors_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Number of Floors"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Pane />
              </HX.Pane>
            </HX.Section>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/policy_information/top_20_sort_by"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Section title="Top 20 Largest Locations">
              <HX.Table data={[
                "perils/flood/top_20_locations_summary"
              ]}
                fields={[
                "country",
                "state",
                "county",
                "zip",
                "tiv_buildings",
                "tiv_contents_total",
                "tiv_bi",
                "tiv_total",
                "itv",
                "base_rate",
                "construction",
                "num_of_floors",
                "basement",
                "elevation",
                "katrisk_catnet_score",
                "size_discount",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true}
                minListVisibleRows={30} />
            </HX.Section>
          </HX.Selector>
        </HX.Section>
        <HX.Section title="Wildfire Rating"
          defaultCollapsed={true}
          shownBy="non_layer_perils/wildfire/show_section">
          <HX.Selector data={[
            "layers"
          ]}
            dropdown="layer_label">
            <HX.Section title="Modifier Summary">
              <HX.Table data={[
                "perils/wildfire/modifier_summary"
              ]}
                fields={[
                "peril_name",
                "num_locs",
                "sum_tiv_total_usd",
                "occupancy",
                "construction",
                "pc_code",
                "catnet_score",
                "size_discount",
                "bi_waiting_period",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true} />
            </HX.Section>
            <HX.Section title="Risk Factors Summary">
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/wildfire/risk_category_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Risk Category"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Table data={[
                  "perils/wildfire/construction_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Construction Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
              </HX.Pane>
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/wildfire/occupancy_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Occupancy Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Pane />
              </HX.Pane>
            </HX.Section>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/policy_information/top_20_sort_by"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Section title="Top 20 Largest Locations">
              <HX.Table data={[
                "perils/wildfire/top_20_locations_summary"
              ]}
                fields={[
                "country",
                "state",
                "county",
                "zip",
                "tiv_buildings",
                "tiv_contents_total",
                "tiv_bi",
                "tiv_total",
                "itv",
                "base_rate",
                "occupancy",
                "construction",
                "pc_code",
                "catnet_score",
                "size_discount",
                "bi_waiting_period",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true}
                minListVisibleRows={30} />
            </HX.Section>
          </HX.Selector>
        </HX.Section>
        <HX.Section title="Windstorm Rating"
          defaultCollapsed={true}
          shownBy="non_layer_perils/named_windstorm/show_section">
          <HX.Selector data={[
            "layers"
          ]}
            dropdown="layer_label">
            <HX.Section title="Windstorm Simulation Summary">
              <HX.Table data={[
                "risk_appetite_summary"
              ]}
                fields={[
                "us_wind_aal",
                "us_wind_sd",
                "aep_impact_1_in_10",
                "oep_impact_1_in_250",
                "intl_wind_aal",
                "intl_wind_sd"
              ]}
                kb-interactive={true} />
              <HX.Table title="Intl. AAL Summary"
                data={[
                {
                  "datum": "risk_appetite_summary_intl_country",
                  "elementLabelBy": "country"
                }
              ]}
                fields={[
                {
                  "field": "aal_ws",
                  "width": 200
                }
              ]}
                filter={[
                "show_ws"
              ]}
                kb-interactive={true} />
            </HX.Section>
            <HX.Section title="Modifier Summary">
              <HX.Table data={[
                "perils/named_windstorm/modifier_summary"
              ]}
                fields={[
                "peril_name",
                "no_of_locs",
                "sum_tiv_total_usd",
                "occupancy",
                "construction",
                "year_built",
                "floor_area",
                "num_of_floors",
                "roof_age",
                "roof_covering",
                "roof_geometry",
                "construction_quality",
                "roof_anchor",
                "roof_bracing",
                "roof_cladding",
                "frame_connection",
                "storm_surge",
                "catnet_score",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true} />
            </HX.Section>
            <HX.Section title="Risk Factors Summary">
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/named_windstorm/gate_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Windstorm Gate"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Table data={[
                  "perils/named_windstorm/risk_category_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Windstorm Risk Category"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
              </HX.Pane>
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/named_windstorm/occupancy_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Occupancy Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Table data={[
                  "perils/named_windstorm/construction_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Construction Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
              </HX.Pane>
            </HX.Section>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/policy_information/top_20_sort_by"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Section title="Top 20 Largest Locations">
              <HX.Table data={[
                "perils/named_windstorm/top_20_locations_summary"
              ]}
                fields={[
                "country",
                "state",
                "county",
                "zip",
                "tiv_buildings",
                "tiv_contents_total",
                "tiv_bi",
                "tiv_total",
                "itv",
                "base_rate",
                "catnet_score",
                "occupancy",
                "construction",
                "year_built",
                "floor_area",
                "num_of_floors",
                "roof_age",
                "roof_covering",
                "roof_geometry",
                "construction_quality",
                "roof_anchor",
                "roof_bracing",
                "roof_cladding",
                "frame_connection",
                "storm_surge",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true}
                minListVisibleRows={30} />
            </HX.Section>
          </HX.Selector>
        </HX.Section>
        <HX.Section title="Earthquake Rating"
          defaultCollapsed={true}
          shownBy="non_layer_perils/quake/show_section">
          <HX.Selector data={[
            "layers"
          ]}
            dropdown="layer_label">
            <HX.Section title="Earthquake Simulation Summary">
              <HX.Table data={[
                "risk_appetite_summary"
              ]}
                fields={[
                "us_quake_aal",
                "us_quake_sd",
                "aep_impact_1_in_10",
                "oep_impact_1_in_250",
                "intl_quake_aal",
                "intl_quake_sd"
              ]}
                kb-interactive={true} />
              <HX.Table title="Intl. AAL Summary"
                data={[
                {
                  "datum": "risk_appetite_summary_intl_country",
                  "elementLabelBy": "country"
                }
              ]}
                fields={[
                {
                  "field": "aal_eq",
                  "width": 200
                }
              ]}
                filter={[
                "show_eq"
              ]}
                kb-interactive={true} />
            </HX.Section>
            <HX.Section title="Modifier Summary">
              <HX.Table data={[
                "perils/quake/modifier_summary"
              ]}
                fields={[
                "peril_name",
                "no_of_locs",
                "sum_tiv_total_usd",
                "occupancy",
                "construction",
                "year_built",
                "num_of_floors",
                "construction_quality",
                "plan_irregularity",
                "soft_story",
                "vertical_irregularity",
                "ornamentation",
                "equipment_bracing",
                "equipment_maintenance",
                "pounding",
                "catnet_score",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true} />
            </HX.Section>
            <HX.Section title="Risk Factors Summary">
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/quake/cresta_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="CRESTA Zone"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Table data={[
                  "perils/quake/risk_category_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Earthquake Risk Category"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
              </HX.Pane>
              <HX.Pane flow="right"
                reflow={true}>
                <HX.Table data={[
                  "perils/quake/occupancy_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Occupancy Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
                <HX.Table data={[
                  "perils/quake/construction_summary"
                ]}
                  fields={[
                  {
                    "field": "name",
                    "width": 200
                  },
                  {
                    "field": "num_locations",
                    "width": 100
                  },
                  {
                    "field": "tiv",
                    "width": 150
                  },
                  {
                    "field": "gu_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "worth",
                    "width": 100
                  },
                  {
                    "field": "tech_rate",
                    "width": 120
                  },
                  {
                    "field": "uw_adj_tech_rate",
                    "width": 150
                  },
                  {
                    "field": "uw_adj_tech_prem",
                    "width": 150
                  }
                ]}
                  title="Construction Summary"
                  kb-interactive={true}
                  dynamic={true}
                  freezeLeft={1} />
              </HX.Pane>
            </HX.Section>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/policy_information/top_20_sort_by"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Section title="Top 20 Largest Locations">
              <HX.Table data={[
                "perils/quake/top_20_locations_summary"
              ]}
                fields={[
                "country",
                "state",
                "county",
                "zip",
                "tiv_buildings",
                "tiv_contents_total",
                "tiv_bi",
                "tiv_total",
                "itv",
                "base_rate",
                "catnet_score",
                "occupancy",
                "construction",
                "year_built",
                "num_of_floors",
                "construction_quality",
                "plan_irregularity",
                "soft_story",
                "vertical_irregularity",
                "ornamentation",
                "equipment_bracing",
                "equipment_maintenance",
                "pounding",
                "total_modifier_impact",
                "gu_tech_rate",
                "worth",
                "tech_rate",
                "uw_adj_tech_rate",
                "uw_adj_tech_prem"
              ]}
                kb-interactive={true}
                minListVisibleRows={30} />
            </HX.Section>
          </HX.Selector>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Underwriter Appetite"
        fullWidth={true}>
        <HX.Section title="CAT Limit Framework Information">
          <HX.Notes field="info/cat_limit_framwork_msg" />
        </HX.Section>
        <HX.Selector data={[
          "layers"
        ]}
          dropdown="layer_label">
          <HX.Section title="Critical CAT Zone Summary">
            <HX.Pane flow="right">
              <HX.Table title="WS CAT Zone Summary"
                data={[
                "perils/named_windstorm/crit_cat_zone_total_summary"
              ]}
                fields={[
                "cat_zone",
                "exposed_limit_threshold",
                "within_threshold"
              ]} />
              <HX.Table title="EQ CAT Zone Summary"
                data={[
                "perils/quake/crit_cat_zone_total_summary"
              ]}
                fields={[
                "cat_zone",
                "exposed_limit_threshold",
                "within_threshold"
              ]} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Critical CAT Zone Detail">
            <HX.Pane flow="right">
              <HX.Table title="WS CAT Zone Detail"
                data={[
                "perils/named_windstorm/crit_cat_zone_summary"
              ]}
                fields={[
                "cat_zone",
                "tiv",
                "exposed_limit",
                "exposed_limit_threshold",
                "within_threshold",
                "flood_zone_av_exposed_limit"
              ]} />
              <HX.Table title="EQ CAT Zone Detail"
                data={[
                "perils/quake/crit_cat_zone_summary"
              ]}
                fields={[
                "cat_zone",
                "tiv",
                "exposed_limit",
                "exposed_limit_threshold",
                "within_threshold"
              ]} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Gate Detail"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Table title="WS Gate Detail"
                data={[
                "perils/named_windstorm/gate_appetite_summary"
              ]}
                fields={[
                "gate",
                "tiv",
                "exposed_limit",
                "flood_zone_av_exposed_limit"
              ]} />
              <HX.Table title="EQ Gate Detail"
                data={[
                "perils/quake/gate_appetite_summary"
              ]}
                fields={[
                "gate",
                "tiv",
                "exposed_limit"
              ]} />
            </HX.Pane>
          </HX.Section>
        </HX.Selector>
      </HX.Page>
      <HX.Page title="Climate"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Generate Metrics">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="generate_flood_climate_metrics_task"
                title="Generate Climate Metrics" />
              <HX.Collection fields={[
                "/non_layer_summary/climate_metrics/perils/peril_selection"
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="generate_climate_doc_task"
                title="Generate Climate Change Spotlight Document" />
              <HX.File field="/non_layer_summary/climate_metrics/document" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Climate Summary">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={[
                "non_layer_summary/climate_metrics/weighted_climate_score"
              ]} />
              <HX.CategoryChart data={[
                "score_0",
                "score_1",
                "score_2",
                "score_3",
                "score_4",
                "score_5"
              ]}
                fields={[
                "total_tiv"
              ]}
                columnType="cluster"
                dataLabelField="score"
                title="TIV by Hurricane Climate Score"
                primaryAxis={{
                "label": "Total TIV ($m USD)"
              }}
                with="non_layer_summary/climate_metrics/score_locations" />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={[
                "non_layer_summary/climate_metrics/flood/flood_climate_risk_score"
              ]} />
              <HX.CategoryChart data={[
                "score_summary"
              ]}
                fields={[
                "tiv_total_usd_chart"
              ]}
                columnType="cluster"
                dataLabelField="bzly_loc_score"
                title="TIV by Flood Climate Score"
                primaryAxis={{
                "label": "Total TIV ($m USD)"
              }}
                with="non_layer_summary/climate_metrics/flood" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Hurricane Climate Metrics"
          shownBy="/non_layer_summary/climate_metrics/perils/ws_selected">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={[
                "non_layer_summary/climate_metrics/weighted_climate_score"
              ]} />
              <HX.Notes field="non_layer_summary/climate_metrics/climate_score_description" />
              <HX.Table title="Score"
                data={[
                "score_0",
                "score_1",
                "score_2",
                "score_3",
                "score_4",
                "score_5"
              ]}
                fields={[
                "score",
                "loc_count",
                "loc_prop",
                "aal_weighted_cgear"
              ]}
                kb-interactive={true}
                with="non_layer_summary/climate_metrics/score_locations" />
            </HX.Pane>
            <HX.CategoryChart data={[
              "score_0",
              "score_1",
              "score_2",
              "score_3",
              "score_4",
              "score_5"
            ]}
              fields={[
              "loc_count",
              "loc_prop"
            ]}
              columnType="cluster"
              dataLabelField="score"
              title="Count and Proportion of Locations by Score"
              primaryAxis={{
              "label": "Number of Locations"
            }}
              secondaryAxis={{
              "label": "Proportion"
            }}
              with="non_layer_summary/climate_metrics/score_locations" />
            <HX.CategoryChart data={[
              "score_0",
              "score_1",
              "score_2",
              "score_3",
              "score_4",
              "score_5"
            ]}
              fields={[
              "total_tiv",
              "gn_tech_pre_uw"
            ]}
              columnType="cluster"
              dataLabelField="score"
              title="TIV and US Windstorm Technical Prem Pre UW Adj. by Score"
              primaryAxis={{
              "label": "Total TIV ($m USD)"
            }}
              secondaryAxis={{
              "label": "US Windstorm Tech Premium ($000 USD)"
            }}
              with="non_layer_summary/climate_metrics/score_locations" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Hurricane Group Summaries"
          shownBy="/non_layer_summary/climate_metrics/perils/ws_selected">
          <HX.Pane flow="right">
            <HX.Table title="WS CC Score by Occupancy"
              data={[
              "ws_cc_score_occupancy"
            ]}
              fields={[
              "occupancy",
              "cgear_score",
              "tiv_total_usd",
              "gn_tech_pre_uw_layer"
            ]}
              kb-interactive={true}
              with="non_layer_summary/climate_metrics" />
            <HX.Table title="WS CC Score by Gate"
              data={[
              "ws_cc_score_gate"
            ]}
              fields={[
              "ws_gate",
              "cgear_0",
              "cgear_1",
              "cgear_2",
              "cgear_3",
              "cgear_4",
              "cgear_5"
            ]}
              kb-interactive={true}
              with="non_layer_summary/climate_metrics" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Hurricane Location Detail"
          shownBy="/non_layer_summary/climate_metrics/perils/ws_selected">
          <HX.Pane>
            <HX.Table title="WS CC Score Top 10 Locations by AAL"
              data={[
              "ws_cc_score_location"
            ]}
              fields={[
              "tiv_total_usd",
              "aal_weighted_cgear",
              "cgear_score",
              "ws_gate",
              "distance_from_coast",
              "zip",
              "occupancy",
              "constr_desc"
            ]}
              kb-interactive={true}
              with="non_layer_summary/climate_metrics" />
            <HX.Button task="produce_climate_map_task"
              title="Generate Climate Score Map" />
            <HX.Section title="Climate Map"
              shownBy="/non_layer_summary/climate_metrics/show_file_component">
              <HX.File field="/non_layer_summary/climate_metrics/climate_heatmap_file" />
            </HX.Section>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Hurricane Mitigation Measures"
          shownBy="/non_layer_summary/climate_metrics/perils/ws_selected">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Pane flow="right">
                <HX.Pane ratio={5}>
                  <HX.Collection fields={[
                    "non_layer_summary/climate_metrics/client_questions/risk_mitigation_measures/question"
                  ]} />
                </HX.Pane>
                <HX.Collection fields={[
                  "non_layer_summary/climate_metrics/client_questions/risk_mitigation_measures/answer"
                ]} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane shownBy="non_layer_summary/climate_metrics/client_questions/risk_mitigation_measures/show_risk_mitigation_measures"
              ratio={2}>
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Collection fields={[
                    "non_layer_summary/climate_metrics/client_questions/emergency_response_plans/selection"
                  ]} />
                </HX.Pane>
                <HX.Pane ratio={5}>
                  <HX.Notes field="non_layer_summary/climate_metrics/client_questions/emergency_response_plans/climate_question.read_only" />
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Collection fields={[
                    "non_layer_summary/climate_metrics/client_questions/hurricane_focused_renovations/selection"
                  ]} />
                </HX.Pane>
                <HX.Pane ratio={5}>
                  <HX.Notes field="non_layer_summary/climate_metrics/client_questions/hurricane_focused_renovations/climate_question.read_only" />
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Collection fields={[
                    "non_layer_summary/climate_metrics/client_questions/emergency_generators/selection"
                  ]} />
                </HX.Pane>
                <HX.Pane ratio={5}>
                  <HX.Notes field="non_layer_summary/climate_metrics/client_questions/emergency_generators/climate_question.read_only" />
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Pane>
                  <HX.Collection fields={[
                    "non_layer_summary/climate_metrics/client_questions/flooding_mitigation_plans/selection"
                  ]} />
                </HX.Pane>
                <HX.Pane ratio={5}>
                  <HX.Notes field="non_layer_summary/climate_metrics/client_questions/flooding_mitigation_plans/climate_question.read_only" />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Pane flow="right">
                <HX.Pane ratio={5}>
                  <HX.Collection fields={[
                    "non_layer_summary/climate_metrics/client_questions/additional_risk_mitigation_practices/question"
                  ]} />
                </HX.Pane>
                <HX.Collection fields={[
                  "non_layer_summary/climate_metrics/client_questions/additional_risk_mitigation_practices/answer"
                ]} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right"
            shownBy="/non_layer_summary/climate_metrics/client_questions/additional_risk_mitigation_practices/show_additional_risk_mitigation_practices">
            <HX.Pane ratio={2}>
              <HX.Notes title="Rationale"
                field="non_layer_summary/climate_metrics/client_questions/additional_risk_mitigation_practices/rationale" />
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane />
        </HX.Section>
        <HX.Section title="Flood Climate Metrics"
          shownBy="/non_layer_summary/climate_metrics/perils/fl_selected">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={[
                "non_layer_summary/climate_metrics/flood/flood_climate_risk_score"
              ]} />
              <HX.Collection fields={[
                "non_layer_summary/climate_metrics/flood/pol_change_five_years"
              ]} />
              <HX.Table title="FL Score"
                data={[
                "score_summary"
              ]}
                fields={[
                "bzly_loc_score",
                "loc_count",
                "loc_prop",
                "tiv_total_usd",
                "current_fl_el"
              ]}
                kb-interactive={true}
                with="non_layer_summary/climate_metrics/flood" />
            </HX.Pane>
            <HX.CategoryChart data={[
              "score_summary"
            ]}
              fields={[
              "loc_count",
              "loc_prop"
            ]}
              columnType="cluster"
              dataLabelField="bzly_loc_score"
              title="Count and Proportion of Locations by Score"
              primaryAxis={{
              "label": "Number of Locations"
            }}
              secondaryAxis={{
              "label": "Proportion"
            }}
              with="non_layer_summary/climate_metrics/flood" />
            <HX.CategoryChart data={[
              "score_summary"
            ]}
              fields={[
              "tiv_total_usd_chart"
            ]}
              columnType="cluster"
              dataLabelField="bzly_loc_score"
              title="TIV by Score"
              primaryAxis={{
              "label": "Total TIV ($m USD)"
            }}
              with="non_layer_summary/climate_metrics/flood" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Flood Group Summaries"
          shownBy="/non_layer_summary/climate_metrics/perils/fl_selected">
          <HX.Pane flow="right">
            <HX.Table title="FL CC by Construction"
              data={[
              "constr_summary"
            ]}
              fields={[
              "constr_code",
              "locations",
              "tiv_total_usd",
              "current_fl_el",
              "bzly_loc_score",
              "change_five_years"
            ]}
              kb-interactive={true}
              with="non_layer_summary/climate_metrics/flood" />
            <HX.Table title="FL CC by Num Stories"
              data={[
              "num_stories_summary"
            ]}
              fields={[
              "num_stories",
              "locations",
              "tiv_total_usd",
              "current_fl_el",
              "bzly_loc_score",
              "change_five_years"
            ]}
              kb-interactive={true}
              with="non_layer_summary/climate_metrics/flood" />
            <HX.Table title="FL CC by Flood Risk Category"
              data={[
              "flood_risk_summary"
            ]}
              fields={[
              "risk_level_fl",
              "locations",
              "tiv_total_usd",
              "current_fl_el",
              "bzly_loc_score",
              "change_five_years"
            ]}
              kb-interactive={true}
              with="non_layer_summary/climate_metrics/flood" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Flood Location Detail"
          shownBy="/non_layer_summary/climate_metrics/perils/fl_selected">
          <HX.Pane>
            <HX.Table title="FL CC Top 10 Locations"
              data={[
              "top_10_locations_summary"
            ]}
              fields={[
              "industry",
              "occupancy",
              "tiv_total_usd",
              "current_fl_el",
              "bzly_loc_score",
              "change_five_years",
              "constr_code",
              "num_stories"
            ]}
              kb-interactive={true}
              with="non_layer_summary/climate_metrics/flood" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Risk Information">
          <HX.Collection fields={[
            "rationale/fill_rationale"
          ]} />
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "rationale/layers"
            ]}
              shownBy="rationale/show_dropdown" />
            <HX.Collection fields={[
              "rationale/bound_layer"
            ]}
              shownBy="rationale/show_bound" />
            <HX.Collection fields={[
              "rationale/layer_label"
            ]} />
            <HX.Collection fields={[
              "rationale/first_saved.read_only"
            ]} />
            <HX.Button task="update_first_saved_task"
              title="Save"
              shownBy="rationale/show_save_button" />
            <HX.Collection fields={[
              "rationale/button_text.read_only"
            ]}
              shownBy="rationale/show_button_text" />
          </HX.Pane>
          <HX.Collection fields={[
            "risk_name",
            "policy_period_start",
            "policy_period_end"
          ]}
            with="rationale/risk_information"
            horizontal={true} />
          <HX.Collection fields={[
            "policy_ref",
            "underwriter",
            "broker"
          ]}
            with="rationale/risk_information"
            horizontal={true} />
          <HX.Collection fields={[
            "occupancy",
            "tiv",
            "new_renewal"
          ]}
            with="rationale/risk_information"
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Rating & Terms">
          <HX.Pane>
            <HX.Table data={[
              "rationale/rating_terms"
            ]}
              fields={[
              "insurance_type",
              "limit",
              "excess",
              "written_line",
              "afb_exposure"
            ]} />
            <HX.Collection fields={[
              "achieved_premium_100_gg",
              "commission",
              "rate_change"
            ]}
              with="rationale/rating_terms_2"
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Natural Perils">
          <HX.Pane flow="right"
            reflow={true}>
            <HX.Table data={[
              "fire",
              "windstorm",
              "eq",
              "wildfire",
              "scs",
              "flood"
            ]}
              fields={[
              "limit",
              "deductible",
              "complex_ded_structure",
              "premium"
            ]}
              with="rationale/natural_perils"
              kb-interactive={true} />
            <HX.Pane>
              <HX.Collection fields={[
                "rationale/natural_perils/tpi_post_uw_adj"
              ]}
                horizontal={true} />
              <HX.Notes title="Adj factor (reason)"
                field="rationale/natural_perils/adj_factor_reason"
                stretch={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Reinsurance">
          <HX.Pane>
            <HX.Collection fields={[
              "consortium",
              "fac_purchased"
            ]}
              with="rationale/reinsurance"
              horizontal={true} />
            <HX.Notes title="FAC Structure"
              field="rationale/reinsurance/fac_structure"
              shownBy="rationale/reinsurance/fac_purchased" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Notes">
          <HX.Notes title="Description"
            field="rationale/note_section/description" />
          <HX.Notes title="Special Processing"
            field="rationale/note_section/special_processing" />
          <HX.Notes title="Underwriter Thoughts"
            field="rationale/note_section/underwriter_thoughts" />
          <HX.Button task="generate_uw_rationale_doc_task"
            title="Generate UW Rationale Document" />
          <HX.File field="rationale/document" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "rate_change/expiring_policy_option_id"
            ]} />
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data" />
          </HX.Pane>
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/layer/renewal",
                "rate_change/layer/expiring"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection title="Premium - Policy Term (100% Share)"
                fields={[
                "renewal",
                "expiring"
              ]}
                with="rate_change/premium_policy_term_100pct" />
              <HX.Collection title="Premium - Policy Term (Beazley Share)"
                fields={[
                "renewal",
                "expiring"
              ]}
                with="rate_change/premium_policy_term" />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection title="Premium - Annualized (100% Share)"
                fields={[
                "renewal",
                "expiring"
              ]}
                with="rate_change/premium_annualized_100pct" />
              <HX.Collection title="Premium - Annualized (Beazley Share)"
                fields={[
                "renewal",
                "expiring"
              ]}
                with="rate_change/premium_annualized" />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection title="BPro Premium"
                fields={[
                "rate_change/expiring_bpro_premium"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="UW Rate Change">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection title="Model %"
                fields={[
                "exposure_change/ratio",
                "risk_characteristics_change/ratio",
                "deductible_change/ratio",
                "limit_change/ratio",
                "terms_and_conditions_change/ratio",
                "other_change/ratio"
              ]}
                with="rate_change" />
              <HX.Collection title="UW Selected %"
                fields={[
                "exposure_change/ratio_uw",
                "risk_characteristics_change/ratio_uw",
                "deductible_change/ratio_uw",
                "limit_change/ratio_uw",
                "terms_and_conditions_change/ratio_uw",
                "other_change/ratio_uw"
              ]}
                with="rate_change" />
              <HX.Collection title="Comments"
                fields={[
                "exposure_change/comments",
                "risk_characteristics_change/comments",
                "deductible_change/comments",
                "limit_change/comments",
                "terms_and_conditions_change/comments",
                "other_change/comments"
              ]}
                with="rate_change" />
              <HX.Collection title="Renewal"
                fields={[
                "exposure_change/renewal",
                "risk_characteristics_change/renewal",
                "deductible_change/renewal",
                "limit_change/renewal",
                "terms_and_conditions_change/renewal",
                "other_change/renewal_brokerage",
                "other_change/renewal_signed_line"
              ]}
                with="rate_change" />
              <HX.Collection title="Expiring"
                fields={[
                "exposure_change/expiring",
                "risk_characteristics_change/expiring",
                "deductible_change/expiring",
                "limit_change/expiring",
                "terms_and_conditions_change/expiring",
                "other_change/expiring_brokerage",
                "other_change/expiring_signed_line"
              ]}
                with="rate_change" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection title="Rate Changes"
                fields={[
                "total_factor/technical",
                "risk_adjusted_rate_change/technical",
                "simple_rate_change"
              ]}
                with="rate_change" />
              <HX.Collection title="Underwriter Selected"
                fields={[
                "total_factor/underwriter",
                "risk_adjusted_rate_change/underwriter"
              ]}
                with="rate_change" />
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Policy Document"
        fullWidth={true}
        shownBy="quote_documents/show_page">
        <HX.Section title="Notifications"
          collapsible={true}
          shownBy="policy_information/notifications/show_notifications">
          <HX.Pane>
            <HX.Notes field="policy_information/notifications/notification_box" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="BPro RPA">
          <HX.Pane>
            <HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "layer"
                ]}
                  with="quote_documents" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "insured_name",
                  "underwriter",
                  "tria",
                  "equipment_breakdown",
                  "insured_from",
                  "insured_until"
                ]}
                  with="quote_documents/bpro_outputs" />
                <HX.Collection fields={[
                  "commission",
                  "office",
                  "bpro_ref",
                  "global_rater_id",
                  "limit",
                  "location_per_schedule"
                ]}
                  with="quote_documents/bpro_outputs" />
                <HX.Collection fields={[
                  "num_locs",
                  "tiv",
                  "itv_per_sqft",
                  "prem_rates",
                  "peril",
                  "min_earned_pct"
                ]}
                  with="quote_documents/bpro_outputs" />
                <HX.Collection fields={[
                  "bpro_outputs/min_earned",
                  "bpro_outputs/george_occupancy",
                  "bpro_outputs/bpro_occupancy",
                  "bpro_outputs/risk_class",
                  "schedule_received_date",
                  {
                    "field": "mailing_address",
                    "shownBy": "manuscript_flag"
                  }
                ]}
                  with="quote_documents" />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table data={[
                  "covered_property",
                  "additional_covered_property"
                ]}
                  fields={[
                  "option_1",
                  "option_2",
                  "option_3"
                ]}
                  title="Covered Property"
                  with="quote_documents/covered_property" />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "property_only",
                  "equipment_breakdown",
                  "tria",
                  "total_exc_fees",
                  "inspection_fees"
                ]}
                  with="quote_documents/premium"
                  title="Gross Premium - USD, Beazley Share" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "loss_run",
                  "favourable_inspection"
                ]}
                  with="quote_documents/subjectivities"
                  title="Subjectives" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table data={[
                  "fixed_sublimits/ordinance_and_law",
                  "fixed_sublimits/wind",
                  "fixed_sublimits/wind_2",
                  "fixed_sublimits/quake",
                  "fixed_sublimits/quake_2",
                  "fixed_sublimits/flood",
                  "other_sublimits"
                ]}
                  fields={[
                  "val",
                  "comments"
                ]}
                  title="Sublimits"
                  with="quote_documents" />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table data={[
                  "deductibles"
                ]}
                  fields={[
                  "peril",
                  "ded_pct",
                  "ded_min",
                  "comments"
                ]}
                  title="Deductibles"
                  with="quote_documents" />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Notes field="deductibles_override_comment"
                  with="quote_documents"
                  title="Deductibles override comment" />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table data={[
                  "pd",
                  "bi"
                ]}
                  fields={[
                  "settlement",
                  "pct"
                ]}
                  title="Coinsurance/Val"
                  with="quote_documents/coinsurance" />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table with="quote_documents/endorsements"
                  data={[
                  "additional_covered_property",
                  "additional_property_not_covered",
                  "burglary_or_robbery_safeguards",
                  "civil_or_military_authority_ext",
                  "condition_of_coverage",
                  "condo_maintenance_fees",
                  "condo_association_coverage",
                  "endorcements_condo_maintenance_fees",
                  "damage_to_roof_structure_limitation",
                  "fire_and_explosion",
                  "first_tier_wind_counties_and_parishes",
                  "hurricane_minimum_earned_premium",
                  "ingress_egress_extension",
                  "limitations_on_coverage_for_roof_surfacing",
                  "ordinance_or_law_increased_period_of_restoration",
                  "outdoor_property_extension",
                  "prior_loss_clause",
                  "property_enhancement",
                  "protective_safeguards",
                  "second_tier_wind_counties_and_parishes",
                  "theft_and_resulting_damage_limitation",
                  "vacancy_permit",
                  "vacant_or_unoccupied_limitatin",
                  "values_limitation_clause",
                  "wind_limitation",
                  "windstorm_or_hail_exclusion"
                ]}
                  fields={[
                  "yesno",
                  "comments"
                ]}
                  title="Endorsements" />
              </HX.Pane>
              <HX.Notes field="quote_documents/quote_comments"
                title="Quote Comments" />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="generate_quote_doc_task"
                title="Generate Quote Document" />
              <HX.File field="quote_documents/document" />
            </HX.Pane>
          </HX.Pane>
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