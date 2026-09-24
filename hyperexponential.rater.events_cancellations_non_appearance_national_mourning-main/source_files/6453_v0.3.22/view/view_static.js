
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
              <HX.Button task="task_start_renewal"
                title="Start Policy" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_page_risk_info">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "inception_date",
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/underwriter",
              "cds/risk_info/product_bool"
            ]}
              horizontal={true} />
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "/cds/currencies/source_currency",
                "/cds/standard_fields/is_renewal"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "coverages/ec_total/section_reference",
                {
                  "field": "coverages/na_total/section_reference",
                  "shownBy": "/model_state/show_non_appearance"
                },
                {
                  "field": null,
                  "shownBy": "/model_state/show_event_cancellation"
                }
              ]}
                horizontal={true} />
            </HX.With>
            <HX.Collection fields={[
              "cds/standard_fields/insured_name"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Policy Information">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/risk_info/event_name"
            ]}
              horizontal={true} />
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "written_line",
                "brokerage",
                "status"
              ]}
                horizontal={true} />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Actuarial">
          <HX.Collection fields={[
            "model_state/show_actuarial"
          ]}
            horizontal={true} />
          <HX.Collection fields={[
            "cds/standard_fields/rating_methodology"
          ]}
            horizontal={true}
            shownBy="model_state/show_actuarial" />
          <HX.Collection fields={[
            "schema_view/force_show_view"
          ]}
            horizontal={true}
            shownBy="model_state/show_actuarial" />
          <HX.Collection fields={[
            "model_state/use_nm_app_old_model"
          ]}
            horizontal={true}
            shownBy="model_state/show_actuarial" />
          <HX.Collection fields={[
            "model_state/use_determ_agg_calc"
          ]}
            horizontal={true}
            shownBy="model_state/show_actuarial" />
          <HX.Collection fields={[
            "model_state/is_migrated"
          ]}
            horizontal={true}
            shownBy="model_state/show_actuarial" />
          <HX.Collection fields={[
            "model_state/disable_validation"
          ]}
            horizontal={true}
            shownBy="model_state/show_actuarial" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_page_exposure">
        <HX.Section title="Event Cancellation - Coverages">
          <HX.With context={{
            "path": "cds/exposure/granular/event_cancel",
            "type": "struct"
          }}>
            <HX.Collection title="Policy Details"
              fields={[
              "event_type",
              null,
              null
            ]}
              horizontal={true} />
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "/cds/layers",
            "type": "list"
          }}>
            <HX.Collection with="coverages/ec_total"
              horizontal={true}
              fields={[
              "limit",
              "aggregate_limit",
              null
            ]} />
            <HX.Collection with="coverages/ec_total"
              horizontal={true}
              fields={[
              "excess_use",
              {
                "field": "excess",
                "shownBy": "/model_state/show_ec_excess"
              },
              {
                "field": null,
                "shownBy": "/model_state/show_ec_deductible"
              },
              null
            ]} />
            <HX.Collection with="coverages/ec_total"
              horizontal={true}
              fields={[
              "deductible",
              "aggregate_deductible",
              null
            ]}
              shownBy="/model_state/show_ec_deductible" />
          </HX.With>
          <HX.With context={{
            "path": "cds/exposure/granular/event_cancel",
            "type": "struct"
          }}>
            <HX.Table title="Events"
              with="base_coverages"
              data={[
              {
                "datum": "all_risks"
              },
              {
                "datum": "adverse_weather"
              },
              {
                "datum": "earthquake"
              },
              {
                "datum": "windstorm"
              },
              {
                "datum": "wildfire"
              },
              {
                "datum": "terrorism"
              },
              {
                "datum": "cyber"
              },
              {
                "datum": "national_mourning"
              },
              {
                "datum": "riots_and_civil_commotion"
              },
              {
                "datum": "strike"
              },
              {
                "datum": "war"
              },
              {
                "datum": "catastrophic_non_app"
              }
            ]}
              fields={[
              "covered",
              "sublimit",
              "trigger",
              "delegates",
              "uw_adj_min",
              "uw_adj_sel",
              "uw_adj_max",
              "uw_adj_fin",
              "uw_comment",
              {
                "field": "net_el_usd",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "net_el",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "net_el_mod",
                "shownBy": "/model_state/show_actuarial"
              }
            ]}
              dynamic={true}
              kb-interactive={true} />
          </HX.With>
        </HX.Section>
        <HX.With context={{
          "path": "cds/exposure/granular/event_cancel",
          "type": "struct"
        }}>
          <HX.Section title="Event Cancellation - Modifiers"
            defaultCollapsed={true}>
            <HX.Collection title="Terrorism Terms"
              fields={[
              "terrorism_terms/time_distance",
              "terrorism_terms/event_profile",
              "terrorism_terms/city_load"
            ]}
              shownBy="/model_state/show_ec_terrorism"
              horizontal={true} />
            <HX.Collection title="Exposure Curve"
              fields={[
              "exposure_curve",
              {
                "field": "exposure_curve_warning",
                "shownBy": "/model_state/show_exposure_curve_warning"
              },
              "exposure_curve_comments",
              null
            ]}
              horizontal={true} />
            <HX.Collection title="Experience Factor"
              fields={[
              "experience",
              "experience_ratio",
              "experience_factor"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "ncb",
              "ncb_offered",
              "ncb_factor"
            ]}
              horizontal={true} />
          </HX.Section>
          <HX.Section title="Event Cancellation - Events">
            <HX.Collection fields={[
              "agg_tiv_calc",
              "agg_tiv_uw",
              {
                "field": "agg_tiv_warning",
                "shownBy": "/model_state/show_tiv_warning"
              }
            ]}
              horizontal={true} />
            <HX.Table title="Events"
              data={[
              "events"
            ]}
              fields={[
              "event_name",
              "country",
              "state",
              "date_start",
              "date_end",
              "tiv",
              "venue",
              "check",
              {
                "field": "ihs_terrorism",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "ihs_riots_and_civil_commotion",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "ihs_strike",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "ihs_war",
                "shownBy": "/model_state/show_actuarial"
              }
            ]}
              dynamic={true}
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="Settings"
            shownBy="/model_state/show_ihs_sim_settings">
            <HX.Pane flow="right">
              <HX.Pane flow="down"
                stretch={true}
                shownBy="/model_state/show_ihs">
                <HX.Collection fields={[
                  "last_run_status",
                  "check_run_consistent",
                  "calc_run_value"
                ]}
                  with="/cds/ihs"
                  title="Enter country details in prior sections then press button to load IHS info." />
                <HX.Button title="Load IHS Data"
                  task="task_fetch_ihs_data" />
              </HX.Pane>
              <HX.Pane flow="down"
                stretch={true}
                shownBy="/model_state/show_simulation">
                <HX.Collection fields={[
                  "last_run_status",
                  "check_run_consistent",
                  "calc_run_value"
                ]}
                  with="/cds/exposure/granular/event_cancel/simulation"
                  title="Enter all details in prior sections then press button here to run simulation." />
                <HX.Button title="Simulate Losses"
                  task="task_simulation" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="National Mourning"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_page_national_mourning">
        <HX.With context={{
          "path": "cds/exposure/granular/event_cancel",
          "type": "struct"
        }}>
          <HX.Section title="Event Cancellation - National Mourning"
            defaultCollapsed={false}>
            <HX.Collection fields={[
              "national_mourning/cover_level",
              "national_mourning/mourning_period"
            ]}
              horizontal={true} />
            <HX.Table title="National Mourning - Under 75s"
              data={[
              {
                "datum": "national_mourning/under_75",
                "elementLabelBy": "label"
              }
            ]}
              fields={[
              "include",
              "country",
              "age",
              "prob_die",
              "prob_live",
              "mod_affluence",
              "mod_health",
              "prob_die_mod",
              "prob_live_mod",
              "check"
            ]}
              dynamic={true}
              kb-interactive={true} />
            <HX.Table title="National Mourning - 75 and over - note can only add rows from row 3 onward"
              data={[
              {
                "datum": "national_mourning/bespoke_1",
                "elementLabelBy": "label"
              },
              {
                "datum": "national_mourning/bespoke_2",
                "elementLabelBy": "label"
              },
              {
                "datum": "national_mourning/over_75",
                "elementLabelBy": "label"
              }
            ]}
              fields={[
              "include",
              "name.uw_view",
              "country.uw_view",
              "gender.uw_view",
              "date_of_birth.uw_view",
              "age",
              "prob_die",
              "prob_live",
              "mod_affluence",
              "mod_health",
              "prob_die_mod",
              "prob_live_mod",
              "check"
            ]}
              dynamic={true}
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Non Appearance"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_page_non_appearance">
        <HX.With context={{
          "path": "cds/exposure/granular/non_appearance",
          "type": "struct"
        }}>
          <HX.Section title="Non Appearance">
            <HX.Collection horizontal={true}
              fields={[
              "genre",
              "base_rate"
            ]}
              title="Exposure Measure" />
            <HX.Collection horizontal={true}
              fields={[
              "num_shows",
              null
            ]} />
            <HX.Collection horizontal={true}
              fields={[
              "avg_show_value",
              null
            ]} />
            <HX.Collection horizontal={true}
              fields={[
              "agg_show_value",
              null
            ]} />
            <HX.Collection horizontal={true}
              fields={[
              "el_fgu",
              null
            ]} />
            <HX.Collection horizontal={true}
              fields={[
              "num_band_members",
              "num_band_members_mod"
            ]}
              title="Objective Modifiers" />
            <HX.Collection horizontal={true}
              fields={[
              "claim_experience",
              "claim_experience_mod"
            ]} />
            <HX.Collection horizontal={true}
              fields={[
              null,
              "nmp_mod"
            ]} />
            <HX.Collection horizontal={true}
              fields={[
              "el_fgu_mod",
              "total_mod"
            ]} />
            <HX.Collection horizontal={true}
              fields={[
              "fl_curve",
              null
            ]} />
            <HX.Collection horizontal={true}
              fields={[
              "uw_adj_min",
              "uw_adj_sel",
              "uw_adj_max",
              "uw_adj_fin"
            ]}
              title="UW Adjustments" />
            <HX.Notes field="uw_comment"
              title="UW Comment" />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Experience Rating"
        fullWidth={true}
        shownBy="model_state/show_page_experience">
        <HX.With context={{
          "path": "cds/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="Initial Selections">
            <HX.Pane flow="right">
              <HX.Table title="Key Values"
                data={[
                {
                  "datum": "/cds/experience_rating"
                }
              ]}
                fields={[
                "evaluation_date_calc",
                "evaluation_date_ovd",
                null,
                {
                  "field": "el_final_calc",
                  "shownBy": "/model_state/show_actuarial"
                },
                {
                  "field": "el_final_ovd",
                  "shownBy": "/model_state/show_actuarial"
                },
                "el_final",
                null,
                {
                  "field": "el_weight_calc",
                  "shownBy": "/model_state/show_actuarial"
                },
                {
                  "field": "el_weight_ovd",
                  "shownBy": "/model_state/show_actuarial"
                },
                "el_weight"
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table title="BI Data Load"
                  data={[
                  {
                    "datum": "/cds/bi"
                  }
                ]}
                  fields={[
                  "last_run_status",
                  "last_run_date",
                  {
                    "field": "last_run_value",
                    "shownBy": "/model_state/show_actuarial"
                  },
                  {
                    "field": "calc_run_value",
                    "shownBy": "/model_state/show_actuarial"
                  },
                  "check_run_consistent"
                ]}
                  transpose={true}
                  kb-interactive={true} />
                <HX.Button task="task_sql_bi_data"
                  title="Load BI Data" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Overall">
            <HX.Collection fields={[
              "exposure_trend_backfill",
              null,
              null,
              null,
              null
            ]}
              horizontal={true} />
            <HX.Table data={[
              {
                "datum": "analysis_table",
                "elementLabelBy": "yoa_label"
              },
              {
                "datum": "analysis_table_cy",
                "elementLabelBy": "yoa_label"
              },
              null,
              {
                "datum": "analysis_table_total_included",
                "elementLabelBy": "yoa_label"
              }
            ]}
              fields={[
              "include",
              "tiv_calc",
              "tiv_ovd",
              "gnwp_ol_dup",
              "total_ol_selected_ultimate_dup",
              "total_ol_selected_ulr_dup",
              "total_ol_selected_ult_to_tiv"
            ]}
              maxListVisibleRows={10}
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="Experience Rating - Input and Assumption"
            defaultCollapsed={true}>
            <HX.Table data={[
              {
                "datum": "analysis_table",
                "elementLabelBy": "yoa_label"
              },
              {
                "datum": "analysis_table_cy",
                "elementLabelBy": "yoa_label"
              }
            ]}
              fields={[
              "gnwp_nominal_calc",
              "gnwp_nominal_ovd",
              null,
              "attr_incurred_calc",
              "attr_incurred_ovd",
              null,
              "large_incurred_calc",
              "large_incurred_ovd",
              null,
              "cat_incurred_calc",
              "cat_incurred_ovd",
              null,
              "rate_inc_calc",
              "rate_inc_ovd",
              {
                "field": "rate_inc",
                "shownBy": "/model_state/show_actuarial"
              },
              "rate_cum",
              null,
              "inf_inc_calc",
              "inf_inc_ovd",
              {
                "field": "inf_inc",
                "shownBy": "/model_state/show_actuarial"
              },
              "inf_cum",
              {
                "field": null,
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "attr_pct_ultimate_calc",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "attr_pct_ultimate_ovd",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "attr_ielr_calc",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "attr_ielr_ovd",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": null,
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "large_pct_ultimate_calc",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "large_pct_ultimate_ovd",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "large_ielr_calc",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "large_ielr_ovd",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": null,
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "cat_pct_ultimate_calc",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "cat_pct_ultimate_ovd",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "cat_ielr_calc",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "cat_ielr_ovd",
                "shownBy": "/model_state/show_actuarial"
              }
            ]}
              title="Analysis Table"
              maxListVisibleRows={10}
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="Experience Rating - LR Projection"
            defaultCollapsed={true}>
            <HX.Table data={[
              {
                "datum": "analysis_table",
                "elementLabelBy": "yoa_label"
              },
              null,
              {
                "datum": "analysis_table_total",
                "elementLabelBy": "yoa_label"
              }
            ]}
              fields={[
              "gnwp_ol",
              "attr_ol_incurred",
              "large_ol_incurred",
              "cat_ol_incurred",
              {
                "field": "total_ol_incurred",
                "shownBy": "/model_state/show_actuarial"
              },
              null,
              "attr_pct_ultimate",
              {
                "field": "attr_ol_cl_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "attr_ol_bf_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "attr_ol_ielr_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              "attr_ol_cl_lr",
              "attr_ol_bf_lr",
              "attr_ol_ielr",
              "attr_method",
              "attr_ol_selected_ultimate",
              "attr_ol_selected_ulr",
              null,
              {
                "field": "large_pct_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "large_ol_cl_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "large_ol_bf_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "large_ol_ielr_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              "large_ol_cl_lr",
              {
                "field": "large_ol_bf_lr",
                "shownBy": "/model_state/show_actuarial"
              },
              "large_ol_ielr",
              "large_method",
              {
                "field": "large_credibility",
                "shownBy": "/model_state/show_actuarial"
              },
              "large_ol_selected_ultimate",
              "large_ol_selected_ulr",
              null,
              {
                "field": "cat_pct_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "cat_ol_cl_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "cat_ol_bf_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "cat_ol_ielr_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              "cat_ol_cl_lr",
              {
                "field": "cat_ol_bf_lr",
                "shownBy": "/model_state/show_actuarial"
              },
              "cat_ol_ielr",
              "cat_method",
              "cat_ol_selected_ultimate",
              "cat_ol_selected_ulr",
              null,
              {
                "field": "total_pct_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "total_ol_cl_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "total_ol_bf_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "total_ol_ielr_ultimate",
                "shownBy": "/model_state/show_actuarial"
              },
              "total_ol_selected_ultimate",
              {
                "field": "total_ol_cl_lr",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "total_ol_bf_lr",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "total_ol_ielr",
                "shownBy": "/model_state/show_actuarial"
              },
              "total_ol_selected_ulr",
              {
                "field": null,
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "wgt_include",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "wgt_decay",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "wgt_exposure",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "wgt_pct_ult",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "wgt_overall_initial",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "wgt_overall_final",
                "shownBy": "/model_state/show_actuarial"
              }
            ]}
              title="Analysis Table"
              maxListVisibleRows={10}
              kb-interactive={true} />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rating Summary"
        viewScale={0.9}
        fullWidth={true}
        shownBy="/model_state/show_page_rat_sum">
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
        <HX.Section title="Overall Summary">
          <HX.Pane flow="down"
            shownBy="model_state/show_actuarial">
            <HX.Collection fields={[
              "total_sim_claim_number_calc",
              "total_sim_claim_number_override",
              "total_sim_claim_number",
              null,
              "last_run_status",
              "calc_run_value",
              "last_run_value",
              "check_run_consistent",
              "total_sim_loss_before_agg",
              "total_sim_loss_after_agg",
              "total_sim_loss_after_agg_adj",
              "total_sim_loss_after_agg_adj_scaled",
              "total_det_loss_before_agg",
              "total_det_loss_after_agg",
              null,
              "total_det_loss_after_agg_adj",
              "sim_error",
              null,
              "num_sims",
              "sim_agg_adj"
            ]}
              with="cds/exposure/granular/event_cancel/simulation"
              numCols={4}
              title="Enter Risk details in section below then press button here to run simulation." />
            <HX.Button task="task_simulation"
              title="Simulate Losses" />
          </HX.Pane>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={5}
              fields={[
              "status",
              "/cds/currencies/source_currency",
              "brokerage",
              "written_line",
              null
            ]} />
            <HX.Collection with="coverages/ec_total"
              numCols={5}
              fields={[
              "limit",
              "aggregate_limit",
              "excess_use",
              {
                "field": "excess",
                "shownBy": "/model_state/show_ec_excess"
              },
              {
                "field": null,
                "shownBy": "/model_state/show_ec_excess"
              },
              {
                "field": "deductible",
                "shownBy": "/model_state/show_ec_deductible"
              },
              {
                "field": "aggregate_deductible",
                "shownBy": "/model_state/show_ec_deductible"
              }
            ]} />
            <HX.Collection shownBy="/model_state/show_actuarial"
              title="Priced Quotes"
              numCols={3}
              fields={[
              "quoted_premium_100",
              "quoted_premium",
              "quoted_rol",
              "benchmark_premium_100",
              "benchmark_premium",
              "quoted_roe",
              "technical_premium_100",
              "technical_premium",
              null
            ]} />
            <HX.Collection shownBy="/model_state/show_underwriter"
              title="Priced Quotes"
              numCols={2}
              fields={[
              "quoted_premium_100",
              "quoted_rol",
              "benchmark_premium_100",
              "quoted_roe",
              "technical_premium_100",
              null
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "bpi",
              "pflr",
              "uw_adj_impact",
              "tpi",
              "tpi_pre_uw_adj",
              "roc"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Metrics - Event Cancellation"
          defaultCollapsed={false}
          shownBy="model_state/show_event_cancellation">
          <HX.Collection fields={[
            "/model_state/show_rs_plan",
            null,
            null
          ]}
            horizontal={true} />
          <HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Table title="Summary - after UW Adj"
                with="coverages"
                data={[
                null,
                {
                  "datum": "ec_total",
                  "maxWidth": 240
                },
                null,
                "all_risks",
                "adverse_weather",
                "earthquake",
                "windstorm",
                "wildfire",
                "terrorism",
                "cyber",
                "national_mourning",
                "riots_and_civil_commotion",
                "strike",
                "war",
                "catastrophic_non_app"
              ]}
                fields={[
                null,
                "section_reference",
                null,
                "quoted_premium_100",
                "quoted_rol",
                "quoted_roe",
                null,
                "technical_premium_100",
                "technical_rol",
                "tpi",
                null,
                "benchmark_premium_100",
                "benchmark_rol",
                "bpi",
                null,
                "pflr",
                {
                  "field": null,
                  "shownBy": "/model_state/show_rs_plan"
                },
                {
                  "field": "plan_premium_100",
                  "shownBy": "/model_state/show_rs_plan"
                },
                {
                  "field": "plan_rol",
                  "shownBy": "/model_state/show_rs_plan"
                }
              ]}
                transpose={true}
                kb-interactive={true}
                freezeLeft={0}
                syncColumnWidthsKey="wibble" />
              <HX.Table title="Summary - before UW Adj"
                shownBy="/model_state/show_actuarial"
                with="coverages"
                data={[
                null,
                {
                  "datum": "ec_total",
                  "maxWidth": 240
                },
                null,
                "all_risks",
                "adverse_weather",
                "earthquake",
                "windstorm",
                "wildfire",
                "terrorism",
                "cyber",
                "national_mourning",
                "riots_and_civil_commotion",
                "strike",
                "war",
                "catastrophic_non_app"
              ]}
                fields={[
                null,
                "technical_premium_pre_uw_adj_100",
                "technical_rol_pre_uw_adj",
                "tpi_pre_uw_adj",
                null,
                "benchmark_premium_pre_uw_adj_100",
                "benchmark_rol_pre_uw_adj",
                "bpi_pre_uw_adj",
                null,
                "pflr_pre_uw_adj",
                {
                  "field": null,
                  "shownBy": "/model_state/show_rs_plan"
                },
                {
                  "field": "plan_premium_pre_uw_adj_100",
                  "shownBy": "/model_state/show_rs_plan"
                },
                {
                  "field": "plan_rol_pre_uw_adj",
                  "shownBy": "/model_state/show_rs_plan"
                }
              ]}
                transpose={true}
                kb-interactive={true}
                freezeLeft={0}
                syncColumnWidthsKey="wibble" />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Loss Cost - Event Cancellation"
          defaultCollapsed={true}
          shownBy="model_state/show_event_cancellation">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Table title="Loss Costs"
              data={[
              null,
              {
                "datum": "ec_total",
                "maxWidth": 240
              },
              null,
              "all_risks",
              "adverse_weather",
              "earthquake",
              "windstorm",
              "wildfire",
              "terrorism",
              "cyber",
              "national_mourning",
              "riots_and_civil_commotion",
              "strike",
              "war",
              "catastrophic_non_app"
            ]}
              fields={[
              null,
              {
                "field": "loss_cost_layer_adj",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": null,
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "agg_adjustment",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "loss_cost_layer_agg_adj",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": null,
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "uw_adjustment",
                "shownBy": "/model_state/show_actuarial"
              },
              "loss_cost_layer_agg_uw_adj",
              null,
              "experience_weight",
              "experience_loss_cost",
              null,
              "blended_loss_cost_no_uw_adj",
              "blended_loss_cost"
            ]}
              kb-interactive={true}
              with="coverages"
              freezeLeft={0}
              transpose={true}
              syncColumnWidthsKey="wibble" />
          </HX.With>
        </HX.Section>
        <HX.Section title="Metrics - Event Cancellation including Non Appearance"
          defaultCollapsed={false}
          shownBy="model_state/show_non_appearance">
          <HX.Collection fields={[
            "/model_state/show_rs_plan",
            null,
            null
          ]}
            horizontal={true} />
          <HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Table title="Summary - after UW Adj"
                with="coverages"
                data={[
                null,
                {
                  "datum": "/cds/layers",
                  "elementLabelBy": "rat_sum_label",
                  "maxWidth": 240
                },
                null,
                {
                  "datum": "na_total",
                  "maxWidth": 240
                },
                null,
                {
                  "datum": "ec_total",
                  "maxWidth": 240
                },
                null,
                "all_risks",
                "adverse_weather",
                "earthquake",
                "windstorm",
                "wildfire",
                "terrorism",
                "cyber",
                "national_mourning",
                "riots_and_civil_commotion",
                "strike",
                "war",
                "catastrophic_non_app"
              ]}
                fields={[
                null,
                "section_reference",
                null,
                "quoted_premium_100",
                "quoted_rol",
                "quoted_roe",
                null,
                "technical_premium_100",
                "technical_rol",
                "tpi",
                null,
                "benchmark_premium_100",
                "benchmark_rol",
                "bpi",
                null,
                "pflr",
                {
                  "field": null,
                  "shownBy": "/model_state/show_rs_plan"
                },
                {
                  "field": "plan_premium_100",
                  "shownBy": "/model_state/show_rs_plan"
                },
                {
                  "field": "plan_rol",
                  "shownBy": "/model_state/show_rs_plan"
                }
              ]}
                transpose={true}
                kb-interactive={true}
                freezeLeft={0}
                syncColumnWidthsKey="wibble" />
              <HX.Table title="Summary - before UW Adj"
                shownBy="/model_state/show_actuarial"
                with="coverages"
                data={[
                null,
                {
                  "datum": "/cds/layers",
                  "elementLabelBy": "rat_sum_label",
                  "maxWidth": 240
                },
                null,
                {
                  "datum": "na_total",
                  "maxWidth": 240
                },
                null,
                {
                  "datum": "ec_total",
                  "maxWidth": 240
                },
                null,
                "all_risks",
                "adverse_weather",
                "earthquake",
                "windstorm",
                "wildfire",
                "terrorism",
                "cyber",
                "national_mourning",
                "riots_and_civil_commotion",
                "strike",
                "war",
                "catastrophic_non_app"
              ]}
                fields={[
                null,
                "technical_premium_pre_uw_adj_100",
                "technical_rol_pre_uw_adj",
                "tpi_pre_uw_adj",
                null,
                "benchmark_premium_pre_uw_adj_100",
                "benchmark_rol_pre_uw_adj",
                "bpi_pre_uw_adj",
                null,
                "pflr_pre_uw_adj",
                {
                  "field": null,
                  "shownBy": "/model_state/show_rs_plan"
                },
                {
                  "field": "plan_premium_pre_uw_adj_100",
                  "shownBy": "/model_state/show_rs_plan"
                },
                {
                  "field": "plan_rol_pre_uw_adj",
                  "shownBy": "/model_state/show_rs_plan"
                }
              ]}
                transpose={true}
                kb-interactive={true}
                freezeLeft={0}
                syncColumnWidthsKey="wibble" />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Loss Cost - Event Cancellation including Non Appearance"
          defaultCollapsed={true}
          shownBy="model_state/show_non_appearance">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Table title="Loss Costs"
              data={[
              null,
              {
                "datum": "/cds/layers",
                "elementLabelBy": "rat_sum_label",
                "maxWidth": 240
              },
              null,
              {
                "datum": "na_total",
                "maxWidth": 240
              },
              null,
              {
                "datum": "ec_total",
                "maxWidth": 240
              },
              null,
              "all_risks",
              "adverse_weather",
              "earthquake",
              "windstorm",
              "wildfire",
              "terrorism",
              "cyber",
              "national_mourning",
              "riots_and_civil_commotion",
              "strike",
              "war",
              "catastrophic_non_app"
            ]}
              fields={[
              null,
              {
                "field": "loss_cost_layer_adj",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": null,
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "agg_adjustment",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "loss_cost_layer_agg_adj",
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": null,
                "shownBy": "/model_state/show_actuarial"
              },
              {
                "field": "uw_adjustment",
                "shownBy": "/model_state/show_actuarial"
              },
              "loss_cost_layer_agg_uw_adj",
              null,
              "experience_weight",
              "experience_loss_cost",
              null,
              "blended_loss_cost_no_uw_adj",
              "blended_loss_cost"
            ]}
              kb-interactive={true}
              with="coverages"
              freezeLeft={0}
              transpose={true}
              syncColumnWidthsKey="wibble" />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        viewScale={0.9}
        fullWidth={true}
        shownBy="/model_state/show_page_rat_sum_case">
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
        <HX.Section title="Overall Summary"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={5}
              fields={[
              "status",
              "/cds/currencies/source_currency",
              "brokerage",
              "written_line",
              "coverages/ec_total/section_reference"
            ]} />
            <HX.Collection with="coverages/ec_total"
              numCols={5}
              fields={[
              "limit",
              "aggregate_limit",
              "excess_use",
              {
                "field": "excess",
                "shownBy": "/model_state/show_ec_excess"
              },
              {
                "field": null,
                "shownBy": "/model_state/show_ec_excess"
              },
              {
                "field": "deductible",
                "shownBy": "/model_state/show_ec_deductible"
              },
              {
                "field": "aggregate_deductible",
                "shownBy": "/model_state/show_ec_deductible"
              }
            ]} />
            <HX.Collection title="Priced Quotes @ Term & Beazley Share"
              numCols={2}
              fields={[
              "quoted_premium_100_case_priced",
              "bpi_case_priced",
              "technical_premium_100",
              "benchmark_premium_100",
              "technical_premium",
              "benchmark_premium"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "tpi",
              "pflr",
              "roc"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Case Pricing Analysis Filepath"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.Notes field="cds/case_pricing_analysis_location" />
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
          defaultCollapsed={false}
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
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
          defaultCollapsed={false}
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
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
          defaultCollapsed={false}
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
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
          defaultCollapsed={false}
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
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
          defaultCollapsed={false}
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
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
          defaultCollapsed={false}
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
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
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
        <HX.Section title="Actuarial Commentary"
          defaultCollapsed={true}>
          <HX.Collection fields={[
            "cds/rationale/actuarial_review"
          ]} />
          <HX.Notes field="cds/rationale/actuarial_notes" />
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
        <HX.Section title="Useful Information">
          <HX.Pane flow="right">
            <HX.Notes field="cds/rationale/help_file" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs"
        shownBy="model_state/show_page_kpi">
        <HX.Section title="Summary Layer - Event Cancellation"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/ec_total/status",
              "coverages/ec_total/section_reference.read_only",
              "coverages/ec_total/brokerage",
              "coverages/ec_total/written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/ec_total/quoted_premium_100.read_only",
                "labelBy": "premium_label"
              },
              null,
              "coverages/ec_total/technical_premium_100",
              "coverages/ec_total/benchmark_premium_100",
              "coverages/ec_total/tpi",
              "coverages/ec_total/bpi",
              {
                "field": "coverages/ec_total/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/ec_total/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "coverages/ec_total/pflr",
              "coverages/ec_total/pflr_pre_uw_adj",
              "coverages/ec_total/uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
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
        <HX.Section title="Summary Layer - Non Appearance"
          defaultCollapsed={true}
          shownBy="/model_state/show_non_appearance">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/na_total/status",
              "coverages/na_total/section_reference.read_only",
              "coverages/na_total/brokerage",
              "coverages/na_total/written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/na_total/quoted_premium_100.read_only",
                "labelBy": "premium_label"
              },
              null,
              "coverages/na_total/technical_premium_100",
              "coverages/na_total/benchmark_premium_100",
              "coverages/na_total/tpi",
              "coverages/na_total/bpi",
              {
                "field": "coverages/na_total/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/na_total/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "coverages/na_total/pflr",
              "coverages/na_total/pflr_pre_uw_adj",
              "coverages/na_total/uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
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
      <HX.Page title="Standard KPIs"
        shownBy="model_state/show_page_kpi_case">
        <HX.Section title="Summary Layer"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/ec_total/status",
              "coverages/ec_total/section_reference.read_only",
              "coverages/ec_total/brokerage",
              "coverages/ec_total/written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium_100",
              "benchmark_premium_100",
              "tpi",
              "bpi"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
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
      <HX.Page title="Actuarial Info (typically hidden)"
        fullWidth={true}
        shownBy="model_state/show_page_actuarial">
        <HX.Section title="IHS Dataframe"
          defaultCollapsed={true}>
          <HX.Collection fields={[
            "last_run_status",
            "last_run_date",
            "last_run_value",
            "calc_run_value",
            "check_run_consistent"
          ]}
            with="cds/ihs"
            horizontal={true} />
          <HX.Button title="Load IHS Data"
            task="task_fetch_ihs_data" />
          <HX.Pane flow="right">
            <HX.Table title="IHS Outlook"
              data={[
              "cds/ihs/ihs_detail"
            ]}
              fields={[
              {
                "field": "country_code",
                "maxWidth": 100
              },
              {
                "field": "risk_name",
                "maxWidth": 250
              },
              {
                "field": "latest_outlook",
                "maxWidth": 120
              },
              {
                "field": "latest_description",
                "maxWidth": 500
              },
              {
                "field": "updated_on",
                "maxWidth": 200
              },
              {
                "field": "value",
                "maxWidth": 200
              }
            ]}
              maxListVisibleRows={15}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Load from Beazley Intelligence"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Collection fields={[
              "last_run_status",
              "last_run_date",
              "last_run_value",
              "calc_run_value",
              "check_run_consistent"
            ]}
              with="cds/bi"
              title="Enter Policy Section Reference then press button here to load latest Beazley Intelligence information." />
            <HX.Button title="Load from BI"
              task="task_sql_bi_data"
              stretch={true} />
          </HX.Pane>
          <HX.Table title="Policy Table"
            data={[
            "cds/experience_rating/policy_table"
          ]}
            fields={[
            "policy_ref",
            "section_ref",
            "yoa",
            "coverage_name",
            "trifocus_name",
            "division",
            "settlement_fx",
            "index_bzly",
            "class_code",
            "bool_ec",
            "bool_na",
            "gnwp_bzly_usd",
            "incurred_bzly_usd",
            "gnwp_100_usd",
            "incurred_100_usd",
            "share_bzly",
            "rate_chg_init",
            "rate_chg",
            "fx_rate_usd_sett",
            "gnwp_bzly",
            "incurred_bzly",
            "gnwp_100",
            "incurred_100",
            "gnwp_bzly_scc",
            "incurred_bzly_scc",
            "gnwp_100_scc",
            "incurred_100_scc"
          ]}
            maxListVisibleRows={15}
            kb-interactive={true}
            dynamic={true} />
          <HX.Table title="Claim Table"
            data={[
            "cds/experience_rating/claim_table"
          ]}
            fields={[
            "policy_ref",
            "section_ref",
            "claim_ref",
            "trifocus_name",
            "division",
            "yoa",
            "settlement_fx",
            "cat_code_bzly",
            "cat_desc_bzly",
            "cat_code_mkt",
            "cat_desc_mkt",
            "cat_bzly_bool",
            "cause_of_loss",
            "bool_covid",
            "index_bzly",
            "class_code",
            "bool_ec",
            "bool_na",
            "bool_large",
            "incurred_bzly",
            "os_bzly",
            "incurred_100",
            "share_bzly",
            "incurred_bzly_scc",
            "os_bzly_scc",
            "incurred_100_scc",
            "incurred_100_scc_attr",
            "incurred_100_scc_large",
            "incurred_100_scc_cat"
          ]}
            maxListVisibleRows={15}
            kb-interactive={true}
            dynamic={true} />
        </HX.Section>
        <HX.Section title="Exposure Rating Dataframe - Event Cancellation"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Complete List"
              data={[
              "cds/exposure/granular/event_cancel/events"
            ]}
              fields={[
              "event_name",
              "country",
              "state",
              "date_start",
              "date_end",
              "tiv",
              "venue",
              "ihs_terrorism",
              "ihs_riots_and_civil_commotion",
              "ihs_strike",
              "ihs_war",
              "check",
              "country_code",
              "date_cover_start",
              "mths_diff",
              "venue_multiplier",
              "tiv_usd",
              "cap_tiv_usd",
              "m_terrorism",
              "c_terrorism",
              "m_riots_and_civil_commotion",
              "c_riots_and_civil_commotion",
              "m_strike",
              "c_strike",
              "m_war",
              "c_war",
              "base_rate_adverse_weather",
              "pat_adverse_weather",
              "base_rate_windstorm",
              "pat_windstorm",
              "base_rate_wildfire",
              "pat_wildfire",
              "base_rate_earthquake",
              "pat_earthquake",
              "season_adverse_weather",
              "season_windstorm",
              "season_wildfire",
              "nm_o75_sx",
              "nm_o75_sx_mod",
              "nm_u75_sx",
              "nm_sx",
              "nm_qx",
              "nm_qx_daily",
              "nm_u75_sx_mod",
              "nm_sx_mod",
              "nm_qx_mod",
              "nm_qx_daily_mod",
              "nm_death_rate",
              "nm_funeral_rate",
              "nm_mourning_rate",
              "nm_rate",
              "nm_death_rate_mod",
              "nm_funeral_rate_mod",
              "nm_mourning_rate_mod",
              "nm_rate_mod",
              "rate_all_risks",
              "rate_adverse_weather",
              "rate_windstorm",
              "rate_wildfire",
              "rate_earthquake",
              "rate_cyber",
              "rate_national_mourning",
              "rate_national_mourning_mod",
              "rate_terrorism",
              "rate_riots_and_civil_commotion",
              "rate_strike",
              "rate_war",
              "rate_catastrophic_non_app",
              "el_usd_total",
              "net_el_usd_total",
              "struct_pct_all_risks",
              "el_usd_all_risks",
              "net_el_usd_all_risks",
              "struct_pct_terrorism",
              "el_usd_terrorism",
              "net_el_usd_terrorism",
              "struct_pct_cyber",
              "el_usd_cyber",
              "net_el_usd_cyber",
              "struct_pct_national_mourning",
              "el_usd_national_mourning",
              "net_el_usd_national_mourning",
              "struct_pct_riots_and_civil_commotion",
              "el_usd_riots_and_civil_commotion",
              "net_el_usd_riots_and_civil_commotion",
              "struct_pct_strike",
              "el_usd_strike",
              "net_el_usd_strike",
              "struct_pct_war",
              "el_usd_war",
              "net_el_usd_war",
              "struct_pct_catastrophic_non_app",
              "el_usd_catastrophic_non_app",
              "net_el_usd_catastrophic_non_app",
              "struct_pct_adverse_weather",
              "el_usd_adverse_weather",
              "net_el_usd_adverse_weather",
              "struct_pct_windstorm",
              "el_usd_windstorm",
              "net_el_usd_windstorm",
              "struct_pct_wildfire",
              "el_usd_wildfire",
              "net_el_usd_wildfire",
              "struct_pct_earthquake",
              "el_usd_earthquake",
              "net_el_usd_earthquake",
              "el_usd_national_mourning_mod",
              "net_el_usd_national_mourning_mod"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Rating Dataframe - National Mourning"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Over 75s"
              data={[
              "cds/exposure/granular/event_cancel/national_mourning/over_75"
            ]}
              fields={[
              "label",
              "include",
              "name",
              "country",
              "gender",
              "date_of_birth",
              "age",
              "prob_die",
              "prob_live",
              "mod_affluence",
              "mod_health",
              "prob_die_mod",
              "prob_live_mod"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Experience Analysis"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Experience Analysis"
              data={[
              {
                "datum": "cds/experience_rating/analysis_table"
              },
              {
                "datum": "cds/experience_rating/analysis_table_cy"
              },
              {
                "datum": null
              },
              {
                "datum": "cds/experience_rating/analysis_table_total"
              },
              {
                "datum": null
              },
              {
                "datum": "cds/experience_rating/analysis_table_total_included"
              }
            ]}
              fields={[
              "yoa",
              "yoa_label",
              "include",
              "tiv_calc",
              "tiv_ovd",
              "tiv",
              "gnwp_ol_dup",
              "total_ol_selected_ultimate_dup",
              "total_ol_selected_ulr_dup",
              "total_ol_selected_ult_to_tiv",
              "gnwp_nominal_calc",
              "gnwp_nominal_ovd",
              "gnwp_nominal",
              "attr_incurred_calc",
              "attr_incurred_ovd",
              "attr_incurred",
              "large_incurred_calc",
              "large_incurred_ovd",
              "large_incurred",
              "cat_incurred_calc",
              "cat_incurred_ovd",
              "cat_incurred",
              "rate_inc_calc",
              "rate_inc_ovd",
              "rate_inc",
              "rate_cum",
              "inf_inc_calc",
              "inf_inc_ovd",
              "inf_inc",
              "inf_cum",
              "attr_pct_ultimate_calc",
              "attr_pct_ultimate_ovd",
              "large_pct_ultimate_calc",
              "large_pct_ultimate_ovd",
              "cat_pct_ultimate_calc",
              "cat_pct_ultimate_ovd",
              "attr_ielr_calc",
              "attr_ielr_ovd",
              "large_ielr_calc",
              "large_ielr_ovd",
              "cat_ielr_calc",
              "cat_ielr_ovd",
              "gnwp_ol",
              "attr_ol_incurred",
              "large_ol_incurred",
              "cat_ol_incurred",
              "total_ol_incurred",
              "attr_pct_ultimate",
              "attr_method",
              "attr_ol_cl_ultimate",
              "attr_ol_bf_ultimate",
              "attr_ol_ielr_ultimate",
              "attr_ol_selected_ultimate",
              "attr_ol_cl_lr",
              "attr_ol_bf_lr",
              "attr_ol_ielr",
              "attr_ol_selected_ulr",
              "large_pct_ultimate",
              "large_method",
              "large_credibility",
              "large_ol_cl_ultimate",
              "large_ol_bf_ultimate",
              "large_ol_ielr_ultimate",
              "large_ol_selected_ultimate",
              "large_ol_cl_lr",
              "large_ol_bf_lr",
              "large_ol_ielr",
              "large_ol_selected_ulr",
              "cat_pct_ultimate",
              "cat_method",
              "cat_ol_cl_ultimate",
              "cat_ol_bf_ultimate",
              "cat_ol_ielr_ultimate",
              "cat_ol_selected_ultimate",
              "cat_ol_cl_lr",
              "cat_ol_bf_lr",
              "cat_ol_ielr",
              "cat_ol_selected_ulr",
              "total_pct_ultimate",
              "total_ol_cl_ultimate",
              "total_ol_bf_ultimate",
              "total_ol_ielr_ultimate",
              "total_ol_selected_ultimate",
              "total_ol_cl_lr",
              "total_ol_bf_lr",
              "total_ol_ielr",
              "total_ol_selected_ulr",
              "wgt_include",
              "wgt_decay",
              "wgt_exposure",
              "wgt_pct_ult",
              "wgt_overall_initial",
              "wgt_overall_final"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Layer Metric by coverage"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                null,
                {
                  "datum": "/cds/layers",
                  "elementLabelBy": "rat_sum_label",
                  "maxWidth": 240
                },
                null,
                {
                  "datum": "na_total",
                  "maxWidth": 240
                },
                null,
                {
                  "datum": "ec_total",
                  "maxWidth": 240
                },
                null,
                "all_risks",
                "adverse_weather",
                "earthquake",
                "windstorm",
                "wildfire",
                "terrorism",
                "cyber",
                "national_mourning",
                "riots_and_civil_commotion",
                "strike",
                "war",
                "catastrophic_non_app"
              ]}
                fields={[
                "limit",
                "excess",
                "deductible",
                "aggregate_limit",
                "aggregate_excess",
                "aggregate_deductible",
                "currency",
                "section_reference",
                "brokerage",
                "written_line",
                "premium",
                "status",
                "benchmark_premium",
                "bpi",
                "bpi_pre_uw_adj",
                "model_premium",
                "unity_premium",
                "quoted_premium",
                "technical_premium",
                "technical_premium_pre_uw_adj",
                "technical_premium_net",
                "tpi",
                "tpi_pre_uw_adj",
                "pflr_att",
                "pflr_cat",
                "pflr",
                "roc",
                "uw_adj_impact",
                "trifocus",
                "expected_loss_cost",
                "expected_loss_cost_pre_uw_adj",
                "expected_loss_cost_100",
                "quoted_premium_net",
                "quoted_premium_net_100",
                "quoted_premium_100",
                "quoted_premium_annual",
                "quoted_premium_annual_100",
                "benchmark_premium_net",
                "benchmark_premium_net_100",
                "benchmark_premium_100",
                "benchmark_premium_annual",
                "benchmark_premium_annual_100",
                "benchmark_premium_pre_uw_adj",
                "technical_premium_100",
                "technical_premium_net_100",
                "pflr_pre_uw_adj",
                "bpi_case_priced",
                "premium_label",
                "technical_premium_pre_uw_adj_100",
                "technical_premium_annual_100",
                "technical_premium_annual",
                "expected_loss_cost_pre_uw_adj_100",
                "plan_premium_100",
                "plan_rol",
                "quoted_rol",
                "quoted_roe",
                "benchmark_rol",
                "technical_rol",
                "benchmark_rol_pre_uw_adj",
                "technical_rol_pre_uw_adj",
                "plan_premium_pre_uw_adj_100",
                "benchmark_premium_pre_uw_adj_100",
                "plan_rol_pre_uw_adj",
                "quoted_rol_pre_uw_adj",
                "loss_cost_layer_adj",
                "agg_adjustment",
                "loss_cost_layer_agg_adj",
                "uw_adjustment",
                "loss_cost_layer_agg_uw_adj",
                "experience_weight",
                "experience_loss_cost",
                "blended_loss_cost_no_uw_adj",
                "blended_loss_cost"
              ]}
                with="coverages"
                transpose={true}
                syncColumnWidthsKey="xxxxxxxxxxxxxxxxxxxxx" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Mapping to standard fields"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Table title="hx - standard fields"
                data={[
                "hx_core"
              ]}
                fields={[
                "inception_date",
                "expiry_date",
                "model_premium",
                "charged_premium",
                "premium_currency",
                "ulr",
                "class_code"
              ]}
                transpose={true} />
              <HX.Table title="cds - currencies"
                data={[
                "cds/currencies"
              ]}
                fields={[
                "target_currency",
                "source_currency",
                "multi_currency_support"
              ]}
                transpose={true} />
              <HX.Table title="cds - experience rating"
                data={[
                "cds/experience_rating"
              ]}
                fields={[
                "claims_available",
                "claims_fgu",
                "claims_net_of_deductible"
              ]}
                transpose={true} />
              <HX.Table title="cds"
                data={[
                "cds"
              ]}
                fields={[
                "database_id",
                "broker_contact",
                "product"
              ]}
                transpose={true} />
            </HX.Pane>
            <HX.Table title="cds - standard fields"
              data={[
              "cds/standard_fields"
            ]}
              fields={[
              "insured_name",
              "broker",
              "expiry_date",
              "inception_date",
              "insured_country",
              "insured_postal_code",
              "insured_state_or_province",
              "is_admitted_or_surplus",
              "is_free_trade_zone",
              "is_renewal",
              "underwriter",
              "policy_reference",
              "facility_reference",
              "benchmark_class",
              "uw_rationale",
              "trifocus",
              "rating_methodology",
              "is_case_priced",
              "is_rater_priced"
            ]}
              transpose={true} />
            <HX.Table title="cds - standard layer fields"
              data={[
              "cds/layers"
            ]}
              fields={[
              "limit",
              "excess",
              "deductible",
              "aggregate_limit",
              "aggregate_excess",
              "aggregate_deductible",
              "currency",
              "section_reference",
              "brokerage",
              "written_line",
              "premium",
              "status",
              "is_primary_excess",
              "benchmark_premium",
              "bpi",
              "bpi_pre_uw_adj",
              "model_premium",
              "unity_premium",
              "quoted_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj",
              "technical_premium_net",
              "tpi",
              "tpi_pre_uw_adj",
              "pflr_att",
              "pflr_cat",
              "pflr",
              "roc",
              "uw_adj_impact",
              "trifocus",
              "expected_loss_cost",
              "expected_loss_cost_pre_uw_adj",
              "bpi_case_priced",
              "pflr_pre_uw_adj",
              "premium_label"
            ]}
              transpose={true} />
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
      <HX.Page title="JSON View"
        shownBy="schema_view/show_view">
        <HX.Section>
          <CustomComponent title="Schema Viewer"
            stringifiedJsonPath="schema_view/stringified_json" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Timer"
        shownBy="model_profiling/show">
        <HX.Section title="Function Tree">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "selected_segment",
              "timer_threshold"
            ]}
              horizontal={true}
              with="model_profiling" />
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Notes field="function_tree"
            title="Function Call Tree"
            with="model_profiling" />
        </HX.Section>
        <HX.Section title="Timed Segments">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "selected_segment",
              "timer_threshold"
            ]}
              horizontal={true}
              with="model_profiling" />
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Table data={[
            "timed_segments"
          ]}
            fields={[
            "name",
            "time_taken",
            "start_time",
            "end_time"
          ]}
            filter="show"
            with="model_profiling"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Gantt View">
          <CustomComponent title="Profiling"
            listSegments="model_profiling/timed_segments"
            myListFields={[
            "name",
            "start_time",
            "time_taken",
            "end_time",
            "show"
          ]} />
        </HX.Section>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};