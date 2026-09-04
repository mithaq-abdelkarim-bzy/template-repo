import * as HX from "hx-model-components";

function pre_uw_summary() {
  return (
    <HX.Page title="Pre UW Adj Summary" fullWidth={true}>
      <HX.Section title="Peril Summary">
        <HX.Table
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "layer_label", "pre_uw_adjustment/achieved_premium", "pre_uw_adjustment/achieved_rate",
            null,
            "pre_uw_adjustment/gross_tech_prem/gross_tech_prem_total",
            null,
            "pre_uw_adjustment/gross_tech_prem/fire",
            null,
            "pre_uw_adjustment/gross_tech_prem/us_cat/us_cat_total", "pre_uw_adjustment/gross_tech_prem/us_cat/windstorm_us",
            "pre_uw_adjustment/gross_tech_prem/us_cat/tornado_us", "pre_uw_adjustment/gross_tech_prem/us_cat/hail_us",
            "pre_uw_adjustment/gross_tech_prem/us_cat/flood_us", "pre_uw_adjustment/gross_tech_prem/us_cat/earthquake_us",
            "pre_uw_adjustment/gross_tech_prem/us_cat/wildfire_us",
            null,
            "pre_uw_adjustment/gross_tech_prem/intl_cat/intl_cat_total", "pre_uw_adjustment/gross_tech_prem/intl_cat/windstorm_intl",
            "pre_uw_adjustment/gross_tech_prem/intl_cat/tornado_intl", "pre_uw_adjustment/gross_tech_prem/intl_cat/hail_intl",
            "pre_uw_adjustment/gross_tech_prem/intl_cat/flood_intl", "pre_uw_adjustment/gross_tech_prem/intl_cat/earthquake_intl",
            "pre_uw_adjustment/gross_tech_prem/intl_cat/wildfire_intl",
            null,
            "pre_uw_adjustment/gross_tech_prem_rate/gross_tech_prem_rate_total",
            null,
            "pre_uw_adjustment/gross_tech_prem_rate/fire",
            null,
            "pre_uw_adjustment/gross_tech_prem_rate/us_cat/us_cat_total", "pre_uw_adjustment/gross_tech_prem_rate/us_cat/windstorm_us",
            "pre_uw_adjustment/gross_tech_prem_rate/us_cat/tornado_us", "pre_uw_adjustment/gross_tech_prem_rate/us_cat/hail_us",
            "pre_uw_adjustment/gross_tech_prem_rate/us_cat/flood_us", "pre_uw_adjustment/gross_tech_prem_rate/us_cat/earthquake_us",
            "pre_uw_adjustment/gross_tech_prem_rate/us_cat/wildfire_us",
            null,
            "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/intl_cat_total", "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/windstorm_intl",
            "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/tornado_intl", "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/hail_intl",
            "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/flood_intl", "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/earthquake_intl",
            "pre_uw_adjustment/gross_tech_prem_rate/intl_cat/wildfire_intl",
          ]}
          kb-interactive
          transpose
        />
      </HX.Section>

    </HX.Page>
  )
}

function post_uw_summary() {
  return (
    <HX.Page title="Post UW Adj Summary" fullWidth={true}>
      <HX.Section title="Underwriter Adjustments">
        <HX.Pane flow="right">
          <HX.Table
            data={[
              { datum: "non_layer_perils/fire/uw_adjustments", width: 200 },
            ]}
            fields={[
              { field: "risk_man", shownBy: "policy_information/doesnt_require_validation/fire/risk_man" },
              { field: "risk_man.validation", shownBy: "policy_information/requires_validation/fire/risk_man" },
              { field: "experience", shownBy: "policy_information/doesnt_require_validation/fire/experience" },
              { field: "experience.validation", shownBy: "policy_information/requires_validation/fire/experience" },
              { field: "valuation", shownBy: "policy_information/doesnt_require_validation/fire/valuation" },
              { field: "valuation.validation", shownBy: "policy_information/requires_validation/fire/valuation" },
              { field: "other", shownBy: "policy_information/doesnt_require_validation/fire/other" },
              { field: "other.validation", shownBy: "policy_information/requires_validation/fire/other" }
            ]}
            kb-interactive
            transpose
          />
          <HX.Table
            data={[
              { datum: "non_layer_perils/named_windstorm/uw_adjustments", width: 200 },
            ]}
            fields={[
              { field: "risk_man", shownBy: "policy_information/doesnt_require_validation/named_windstorm/risk_man" },
              { field: "risk_man.validation", shownBy: "policy_information/requires_validation/named_windstorm/risk_man" },
              { field: "experience", shownBy: "policy_information/doesnt_require_validation/named_windstorm/experience" },
              { field: "experience.validation", shownBy: "policy_information/requires_validation/named_windstorm/experience" },
              { field: "valuation", shownBy: "policy_information/doesnt_require_validation/named_windstorm/valuation" },
              { field: "valuation.validation", shownBy: "policy_information/requires_validation/named_windstorm/valuation" },
              { field: "other", shownBy: "policy_information/doesnt_require_validation/named_windstorm/other" },
              { field: "other.validation", shownBy: "policy_information/requires_validation/named_windstorm/other" }
            ]}
            kb-interactive
            transpose
          />
          <HX.Table
            data={[
              { datum: "non_layer_perils/scs/uw_adjustments", width: 200 },
            ]}
            fields={[
              { field: "risk_man", shownBy: "policy_information/doesnt_require_validation/scs/risk_man" },
              { field: "risk_man.validation", shownBy: "policy_information/requires_validation/scs/risk_man" },
              { field: "experience", shownBy: "policy_information/doesnt_require_validation/scs/experience" },
              { field: "experience.validation", shownBy: "policy_information/requires_validation/scs/experience" },
              { field: "valuation", shownBy: "policy_information/doesnt_require_validation/scs/valuation" },
              { field: "valuation.validation", shownBy: "policy_information/requires_validation/scs/valuation" },
              { field: "other", shownBy: "policy_information/doesnt_require_validation/scs/other" },
              { field: "other.validation", shownBy: "policy_information/requires_validation/scs/other" }
            ]}
            kb-interactive
            transpose
          />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table
            data={[
              { datum: "non_layer_perils/flood/uw_adjustments", width: 200 },
            ]}
            fields={[
              { field: "risk_man", shownBy: "policy_information/doesnt_require_validation/flood/risk_man" },
              { field: "risk_man.validation", shownBy: "policy_information/requires_validation/flood/risk_man" },
              { field: "experience", shownBy: "policy_information/doesnt_require_validation/flood/experience" },
              { field: "experience.validation", shownBy: "policy_information/requires_validation/flood/experience" },
              { field: "valuation", shownBy: "policy_information/doesnt_require_validation/flood/valuation" },
              { field: "valuation.validation", shownBy: "policy_information/requires_validation/flood/valuation" },
              { field: "other", shownBy: "policy_information/doesnt_require_validation/flood/other" },
              { field: "other.validation", shownBy: "policy_information/requires_validation/flood/other" }
            ]}
            kb-interactive
            transpose
          />
          <HX.Table
            data={[
              { datum: "non_layer_perils/quake/uw_adjustments", width: 200 },
            ]}
            fields={[
              { field: "risk_man", shownBy: "policy_information/doesnt_require_validation/quake/risk_man" },
              { field: "risk_man.validation", shownBy: "policy_information/requires_validation/quake/risk_man" },
              { field: "experience", shownBy: "policy_information/doesnt_require_validation/quake/experience" },
              { field: "experience.validation", shownBy: "policy_information/requires_validation/quake/experience" },
              { field: "valuation", shownBy: "policy_information/doesnt_require_validation/quake/valuation" },
              { field: "valuation.validation", shownBy: "policy_information/requires_validation/quake/valuation" },
              { field: "other", shownBy: "policy_information/doesnt_require_validation/quake/other" },
              { field: "other.validation", shownBy: "policy_information/requires_validation/quake/other" }
            ]}
            kb-interactive
            transpose
          />
          <HX.Table
            data={[
              { datum: "non_layer_perils/wildfire/uw_adjustments", width: 200 },
            ]}
            fields={[
              { field: "risk_man", shownBy: "policy_information/doesnt_require_validation/wildfire/risk_man" },
              { field: "risk_man.validation", shownBy: "policy_information/requires_validation/wildfire/risk_man" },
              { field: "experience", shownBy: "policy_information/doesnt_require_validation/wildfire/experience" },
              { field: "experience.validation", shownBy: "policy_information/requires_validation/wildfire/experience" },
              { field: "valuation", shownBy: "policy_information/doesnt_require_validation/wildfire/valuation" },
              { field: "valuation.validation", shownBy: "policy_information/requires_validation/wildfire/valuation" },
              { field: "other", shownBy: "policy_information/doesnt_require_validation/wildfire/other" },
              { field: "other.validation", shownBy: "policy_information/requires_validation/wildfire/other" }
            ]}
            kb-interactive
            transpose
          />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Button task="run_schedule_rater_task" title="Rerun rater" />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Adjusted Peril Summary">
        <HX.Table
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "layer_label", "post_uw_adjustment/achieved_premium", "post_uw_adjustment/achieved_rate",
            null,
            "post_uw_adjustment/gross_tech_prem/gross_tech_prem_total",
            null,
            "post_uw_adjustment/gross_tech_prem/fire",
            null,
            "post_uw_adjustment/gross_tech_prem/us_cat/us_cat_total", "post_uw_adjustment/gross_tech_prem/us_cat/windstorm_us",
            "post_uw_adjustment/gross_tech_prem/us_cat/tornado_us", "post_uw_adjustment/gross_tech_prem/us_cat/hail_us",
            "post_uw_adjustment/gross_tech_prem/us_cat/flood_us", "post_uw_adjustment/gross_tech_prem/us_cat/earthquake_us",
            "post_uw_adjustment/gross_tech_prem/us_cat/wildfire_us",
            null,
            "post_uw_adjustment/gross_tech_prem/intl_cat/intl_cat_total", "post_uw_adjustment/gross_tech_prem/intl_cat/windstorm_intl",
            "post_uw_adjustment/gross_tech_prem/intl_cat/tornado_intl", "post_uw_adjustment/gross_tech_prem/intl_cat/hail_intl",
            "post_uw_adjustment/gross_tech_prem/intl_cat/flood_intl", "post_uw_adjustment/gross_tech_prem/intl_cat/earthquake_intl",
            "post_uw_adjustment/gross_tech_prem/intl_cat/wildfire_intl",
            null,
            "post_uw_adjustment/gross_tech_prem_rate/gross_tech_prem_rate_total",
            null,
            "post_uw_adjustment/gross_tech_prem_rate/fire",
            null,
            "post_uw_adjustment/gross_tech_prem_rate/us_cat/us_cat_total", "post_uw_adjustment/gross_tech_prem_rate/us_cat/windstorm_us",
            "post_uw_adjustment/gross_tech_prem_rate/us_cat/tornado_us", "post_uw_adjustment/gross_tech_prem_rate/us_cat/hail_us",
            "post_uw_adjustment/gross_tech_prem_rate/us_cat/flood_us", "post_uw_adjustment/gross_tech_prem_rate/us_cat/earthquake_us",
            "post_uw_adjustment/gross_tech_prem_rate/us_cat/wildfire_us",
            null,
            "post_uw_adjustment/gross_tech_prem_rate/intl_cat/intl_cat_total", "post_uw_adjustment/gross_tech_prem_rate/intl_cat/windstorm_intl",
            "post_uw_adjustment/gross_tech_prem_rate/intl_cat/tornado_intl", "post_uw_adjustment/gross_tech_prem_rate/intl_cat/hail_intl",
            "post_uw_adjustment/gross_tech_prem_rate/intl_cat/flood_intl", "post_uw_adjustment/gross_tech_prem_rate/intl_cat/earthquake_intl",
            "post_uw_adjustment/gross_tech_prem_rate/intl_cat/wildfire_intl",
          ]}
          kb-interactive
          transpose
        />
      </HX.Section>
    </HX.Page>
  )
}

function full_results() {
  return (
    <HX.Page title="Full Results" fullWidth={true}>
      <HX.Section title="Risk Appetite Summary">
        <HX.Table
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "layer_label", "risk_appetite_summary/us_wind_aal", "risk_appetite_summary/us_quake_aal", "risk_appetite_summary/us_all_perils_aal",
            null,
            "risk_appetite_summary/us_wind_sd", "risk_appetite_summary/us_quake_sd", "risk_appetite_summary/us_all_perils_sd",
            null,
            "risk_appetite_summary/aep_impact_1_in_10", "risk_appetite_summary/oep_impact_1_in_250"
          ]}
          kb-interactive
          transpose
        />
      </HX.Section>
      <HX.Section title="Climate Metrics">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Collection fields={["non_layer_summary/climate_metrics/weighted_climate_score"]} />
            <HX.Notes title="Description" field="non_layer_summary/climate_metrics/climate_score_description" />
          </HX.Pane>
          <HX.Table title="Score"
            data={["score_0", "score_1", "score_2", "score_3", "score_4", "score_5"]}
            fields={["score", "loc_count"]}
            kb-interactive
            with="non_layer_summary/climate_metrics/score_locations"
          />
          <HX.Pane />
        </HX.Pane>

        <HX.Section title="Client Questions">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Pane flow="right">
                <HX.Pane ratio={5}>
                  <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/awareness/question"]} />
                </HX.Pane>
                <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/awareness/answer"]} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Notes title="Rationale" field="non_layer_summary/climate_metrics/client_questions/awareness/rationale" />
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Pane flow="right">
                <HX.Pane ratio={5}>
                  <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/protection_measures/question"]} />
                </HX.Pane>
                <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/protection_measures/answer"]} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Notes title="Rationale" field="non_layer_summary/climate_metrics/client_questions/protection_measures/rationale" />
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Section>

      <HX.Section title="Simulation Output">
        <HX.Section title="RDS Events" defaultCollapsed={true}>
          <HX.Table
            data={[{ datum: "layers", width: 200 }]}
            fields={[
              "layer_label",
              "simulation_output/rds_events/ca_quake_la", "simulation_output/rds_events/ca_quake_sf",
              "simulation_output/rds_events/nm_quake", "simulation_output/rds_events/nm_extreme_stress",
              "simulation_output/rds_events/nw_quake", "simulation_output/rds_events/fl_wind_miami",
              "simulation_output/rds_events/fl_wind_pinellas", "simulation_output/rds_events/us_wind_gulf_of_mexico",
              "simulation_output/rds_events/carolinas_wind", "simulation_output/rds_events/north_east_wind"
            ]}
            kb-interactive
            transpose
          />
        </HX.Section>
        <HX.Section title="Account OEP - 100% Ground Up Loss" defaultCollapsed={true}>
          <HX.Table
            data={[{ datum: "layers", width: 200 }]}
            fields={[
              "layer_label",
              "simulation_output/acc_oep_gu_loss/one_in_10000", "simulation_output/acc_oep_gu_loss/one_in_5000",
              "simulation_output/acc_oep_gu_loss/one_in_1000", "simulation_output/acc_oep_gu_loss/one_in_500",
              "simulation_output/acc_oep_gu_loss/one_in_250", "simulation_output/acc_oep_gu_loss/one_in_200",
              "simulation_output/acc_oep_gu_loss/one_in_150", "simulation_output/acc_oep_gu_loss/one_in_100",
              "simulation_output/acc_oep_gu_loss/one_in_50", "simulation_output/acc_oep_gu_loss/one_in_30",
              "simulation_output/acc_oep_gu_loss/one_in_10", "simulation_output/acc_oep_gu_loss/one_in_2"
            ]}
            kb-interactive
            transpose
          />
        </HX.Section>
        <HX.Section title="Smooth Property + Treaty + Risk OEP - AFB Share Gross Loss" defaultCollapsed={true}>
          <HX.Table
            data={[{ datum: "layers", width: 200 }]}
            fields={[
              "layer_label",
              "simulation_output/pt_oep_loss/one_in_10000", "simulation_output/pt_oep_loss/one_in_5000",
              "simulation_output/pt_oep_loss/one_in_1000", "simulation_output/pt_oep_loss/one_in_500",
              "simulation_output/pt_oep_loss/one_in_250", "simulation_output/pt_oep_loss/one_in_200",
              "simulation_output/pt_oep_loss/one_in_150", "simulation_output/pt_oep_loss/one_in_100",
              "simulation_output/pt_oep_loss/one_in_50", "simulation_output/pt_oep_loss/one_in_30",
              "simulation_output/pt_oep_loss/one_in_10", "simulation_output/pt_oep_loss/one_in_2"
            ]}
            kb-interactive
            transpose
          />
        </HX.Section>
        <HX.Section title="Smooth Property + Treaty + Risk AEP - AFB Share Gross Loss" defaultCollapsed={true}>
          <HX.Table
            data={[{ datum: "layers", width: 200 }]}
            fields={[
              "layer_label",
              "simulation_output/pt_aep_loss/one_in_10000", "simulation_output/pt_aep_loss/one_in_5000",
              "simulation_output/pt_aep_loss/one_in_1000", "simulation_output/pt_aep_loss/one_in_500",
              "simulation_output/pt_aep_loss/one_in_250", "simulation_output/pt_aep_loss/one_in_200",
              "simulation_output/pt_aep_loss/one_in_150", "simulation_output/pt_aep_loss/one_in_100",
              "simulation_output/pt_aep_loss/one_in_50", "simulation_output/pt_aep_loss/one_in_30",
              "simulation_output/pt_aep_loss/one_in_10", "simulation_output/pt_aep_loss/one_in_2"
            ]}
            kb-interactive
            transpose
          />
        </HX.Section>
      </HX.Section>

      <HX.Section title="Output File" shownBy="policy_information/large_schedule_model" defaultCollapsed={true}>
        <HX.File field="schedule/large_schedule_workflow/schedule_output_file" title="Output Calculation File" />
      </HX.Section>
    </HX.Page>
  )
}

export { pre_uw_summary, post_uw_summary, full_results };