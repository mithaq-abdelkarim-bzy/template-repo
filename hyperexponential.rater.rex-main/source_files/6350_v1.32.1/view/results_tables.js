import * as HX from "hx-model-components";

function render_quick_run_bar() {
  return (
    <HX.Section title="" collapsible={false}>
      <HX.Pane flow="right">
        <HX.Button title="Run Simulation" task="run_simulation_task" />
        <HX.Button title="Run Rater" task="run_schedule_rater_task" />
      </HX.Pane>
    </HX.Section>
  )
}

function render_notifications() {
  return (
    <HX.Section title="Notifications" collapsible={true} shownBy="policy_information/notifications/show_notifications">
      <HX.Pane >
        <HX.Notes field="policy_information/notifications/notification_box" />
      </HX.Pane>
    </HX.Section>
  )
}


function render_adjustment_summary_table(path, table_title) {
  return (
    <HX.Table
      data={[path]}
      fields={[
        { field: "name", width: 200 },
        { field: "num_locations", width: 100 },
        { field: "tiv", width: 150 },
        { field: "gu_tech_rate", width: 150 },
        { field: "worth", width: 100 },
        { field: "tech_rate", width: 120 },
        { field: "uw_adj_tech_rate", width: 150 },
        { field: "uw_adj_tech_prem", width: 150 }
      ]}
      title={table_title}
      kb-interactive
      dynamic={true}
      freezeLeft={1}
    />
  )
}

function render_kpi_summary_table_pre_uw_adj() {
  return (
    <HX.Table title="Pre UW Adj KPIs"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label", "pre_uw_adjustment/achieved_premium", "pre_uw_adjustment/achieved_rate",
        null,
        "pre_uw_adjustment/gross_tech_prem/gross_tech_prem_total",
        "pre_uw_adjustment/gross_tech_prem_rate/gross_tech_prem_rate_total",
        "pre_uw_adjustment/benchmark_premium/benchmark_premium",
        "pre_uw_adjustment/expected_loss/expected_loss",
        null,
        "pre_uw_adjustment/gross_tech_prem/tpi",
        "pre_uw_adjustment/benchmark_premium/bpi",
        "pre_uw_adjustment/expected_loss/elr",
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_kpi_summary_table_post_uw_adj() {
  return (
    <HX.Table title="Post UW Adj KPIs"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label", "post_uw_adjustment/achieved_premium", "post_uw_adjustment/achieved_rate",
        null,
        "post_uw_adjustment/gross_tech_prem/gross_tech_prem_total",
        "post_uw_adjustment/gross_tech_prem_rate/gross_tech_prem_rate_total",
        "post_uw_adjustment/benchmark_premium/benchmark_premium",
        "post_uw_adjustment/expected_loss/expected_loss",
        null,
        "post_uw_adjustment/gross_tech_prem/tpi",
        "post_uw_adjustment/benchmark_premium/bpi",
        "post_uw_adjustment/expected_loss/elr",
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_peril_summary_table_pre_uw_adj() {
  return (
    <HX.Table title="Pre UW Adj Peril Details"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label",
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
        { field: null, shownBy: "control/show_cyber_premium" },
        { field: "pre_uw_adjustment/gross_tech_prem/cyber", shownBy: "control/show_cyber_premium" },
        //"pre_uw_adjustment/gross_tech_prem/nmp"
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_peril_summary_rates_table_pre_uw_adj() {
  return (
    <HX.Table title="Pre UW Adj Peril Details"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label",
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
        { field: null, shownBy: "control/show_cyber_premium" },
        { field: "pre_uw_adjustment/gross_tech_prem_rate/cyber", shownBy: "control/show_cyber_premium" },
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_peril_summary_el_table_pre_uw_adj() {
  return (
    <HX.Table title="Pre UW Adj Peril Details"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label",
        null,
        "pre_uw_adjustment/expected_loss/fire",
        null,
        "pre_uw_adjustment/expected_loss/us_cat/us_cat_total", "pre_uw_adjustment/expected_loss/us_cat/windstorm_us",
        "pre_uw_adjustment/expected_loss/us_cat/tornado_us", "pre_uw_adjustment/expected_loss/us_cat/hail_us",
        "pre_uw_adjustment/expected_loss/us_cat/flood_us", "pre_uw_adjustment/expected_loss/us_cat/earthquake_us",
        "pre_uw_adjustment/expected_loss/us_cat/wildfire_us",
        null,
        "pre_uw_adjustment/expected_loss/intl_cat/intl_cat_total", "pre_uw_adjustment/expected_loss/intl_cat/windstorm_intl",
        "pre_uw_adjustment/expected_loss/intl_cat/tornado_intl", "pre_uw_adjustment/expected_loss/intl_cat/hail_intl",
        "pre_uw_adjustment/expected_loss/intl_cat/flood_intl", "pre_uw_adjustment/expected_loss/intl_cat/earthquake_intl",
        "pre_uw_adjustment/expected_loss/intl_cat/wildfire_intl",
        { field: null, shownBy: "control/show_cyber_premium" },
        { field: "pre_uw_adjustment/expected_loss/cyber", shownBy: "control/show_cyber_premium" },
        //"pre_uw_adjustment/expected_loss/nmp"
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_risk_appetite_summary_table() {
  return (
    <HX.Table
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label", "risk_appetite_summary/us_wind_aal", "risk_appetite_summary/us_quake_aal", "risk_appetite_summary/us_all_perils_aal",
        null,
        "risk_appetite_summary/us_wind_sd", "risk_appetite_summary/us_quake_sd", "risk_appetite_summary/us_all_perils_sd",
        null,
        "risk_appetite_summary/aep_impact_1_in_10", "risk_appetite_summary/oep_impact_1_in_250",
        "risk_appetite_summary/aep_impact_1_in_10_wrt_line", "risk_appetite_summary/oep_impact_1_in_250_wrt_line",
        null,
        "risk_appetite_summary/oep_impact_1_in_250_cat_premium_ratio",
        null,
        "risk_appetite_summary/intl_wind_aal", "risk_appetite_summary/intl_quake_aal", "risk_appetite_summary/intl_all_perils_aal",
        null,
        "risk_appetite_summary/intl_wind_sd", "risk_appetite_summary/intl_quake_sd", "risk_appetite_summary/intl_all_perils_sd"
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_uw_adj_table() {
  return (
    <HX.Table
      data={[
        "non_layer_perils/uw_adjustments/risk_man",
        "non_layer_perils/uw_adjustments/experience",
        "non_layer_perils/uw_adjustments/valuation",
        "non_layer_perils/uw_adjustments/other",
        "non_layer_perils/uw_adjustments/total",
      ]}
      fields={[
        { field: "fire", shownBy: "policy_information/doesnt_require_validation/fire", width: 200 },
        { field: "fire.validation", shownBy: "policy_information/requires_validation/fire", width: 200 },
        { field: "scs", shownBy: "policy_information/doesnt_require_validation/scs", width: 200 },
        { field: "scs.validation", shownBy: "policy_information/requires_validation/scs", width: 200 },
        { field: "flood", shownBy: "policy_information/doesnt_require_validation/flood", width: 200 },
        { field: "flood.validation", shownBy: "policy_information/requires_validation/flood", width: 200 },
        { field: "wildfire", shownBy: "policy_information/doesnt_require_validation/wildfire", width: 200 },
        { field: "wildfire.validation", shownBy: "policy_information/requires_validation/wildfire", width: 200 },
        { field: "named_windstorm", shownBy: "policy_information/doesnt_require_validation/named_windstorm", width: 200 },
        { field: "named_windstorm.validation", shownBy: "policy_information/requires_validation/named_windstorm", width: 200 },
        { field: "quake", shownBy: "policy_information/doesnt_require_validation/quake", width: 200 },
        { field: "quake.validation", shownBy: "policy_information/requires_validation/quake", width: 200 },
      ]}
      kb-interactive
    />
  )
}

function render_experience_rating_adj_table() {
  return (
    <HX.Table
      data={[
        { datum: "layers" }
      ]}
      fields={[
        { field: "perils/fire/experience_rating_adj", width: 200 },
        { field: "perils/scs/experience_rating_adj", width: 200 },
        { field: "perils/flood/experience_rating_adj", width: 200 },
        { field: "perils/wildfire/experience_rating_adj", width: 200 },
      ]}
      title="Non-Cat Experience Rating Adjustments"
      kb-interactive
    />
  )
}

function render_peril_summary_table_post_uw_adj() {
  return (
    <HX.Table title="Post UW Adj Peril Details"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label",
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
        { field: null, shownBy: "control/show_cyber_premium" },
        { field: "post_uw_adjustment/gross_tech_prem/cyber", shownBy: "control/show_cyber_premium" },
        //"post_uw_adjustment/gross_tech_prem/nmp"
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_peril_summary_rates_table_post_uw_adj() {
  return (
    <HX.Table title="Post UW Adj Peril Details"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label",
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
        { field: null, shownBy: "control/show_cyber_premium" },
        { field: "post_uw_adjustment/gross_tech_prem_rate/cyber", shownBy: "control/show_cyber_premium" },
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_peril_summary_el_table_post_uw_adj() {
  return (
    <HX.Table title="Post UW Adj Peril Details"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label",
        null,
        "post_uw_adjustment/expected_loss/fire",
        null,
        "post_uw_adjustment/expected_loss/us_cat/us_cat_total", "post_uw_adjustment/expected_loss/us_cat/windstorm_us",
        "post_uw_adjustment/expected_loss/us_cat/tornado_us", "post_uw_adjustment/expected_loss/us_cat/hail_us",
        "post_uw_adjustment/expected_loss/us_cat/flood_us", "post_uw_adjustment/expected_loss/us_cat/earthquake_us",
        "post_uw_adjustment/expected_loss/us_cat/wildfire_us",
        null,
        "post_uw_adjustment/expected_loss/intl_cat/intl_cat_total", "post_uw_adjustment/expected_loss/intl_cat/windstorm_intl",
        "post_uw_adjustment/expected_loss/intl_cat/tornado_intl", "post_uw_adjustment/expected_loss/intl_cat/hail_intl",
        "post_uw_adjustment/expected_loss/intl_cat/flood_intl", "post_uw_adjustment/expected_loss/intl_cat/earthquake_intl",
        "post_uw_adjustment/expected_loss/intl_cat/wildfire_intl",
        { field: null, shownBy: "control/show_cyber_premium" },
        { field: "post_uw_adjustment/expected_loss/cyber", shownBy: "control/show_cyber_premium" },
        //"post_uw_adjustment/expected_loss/nmp",
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_tp_components_pre_uw_adj() {
  return (
    <HX.Table title="Pre UW Adj Technical Premium Breakdown"
      data={[
        { datum: "layers", width: 150 }
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
        "pre_uw_adjustment/gross_tech_prem/gross_tech_prem_total",
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_tp_components_post_uw_adj() {
  return (
    <HX.Table title="Post UW Adj Technical Premium Breakdown"
      data={[
        { datum: "layers", width: 150 }
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
        "post_uw_adjustment/gross_tech_prem/gross_tech_prem_total",
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_cat_aop_split() {
  return (
    <HX.Table title="CAT/AOP Splits"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label",
        "cat_aop_split/perc_us_wind",
        "cat_aop_split/perc_us_quake",
        "cat_aop_split/perc_us_aop",
        "cat_aop_split/perc_intl_cat",
        "cat_aop_split/perc_intl_aop",
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_trapped_exposure() {
  return (
    <HX.Table title="Trapped Exposure"
      data={[
        { datum: "layers", width: 150 }
      ]}
      fields={[
        "layer_label",
        "trapped_exposure",
        "trapped_exposure_rate",
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_simulation_results() {
  return (
    <HX.Section title="Simulation Output" defaultCollapsed={true}>
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
  )
}

function render_output_schedule_calculation() {
  return (
    <HX.Section title="Output File" shownBy="policy_information/large_schedule_model" defaultCollapsed={true}>
      <HX.File field="schedule/large_schedule_workflow/schedule_output_file" title="Output Calculation File" />
    </HX.Section>
  )
}

export { render_quick_run_bar, render_notifications, render_adjustment_summary_table, render_kpi_summary_table_pre_uw_adj, render_kpi_summary_table_post_uw_adj, render_peril_summary_table_pre_uw_adj, render_peril_summary_el_table_pre_uw_adj, render_risk_appetite_summary_table, render_uw_adj_table, render_experience_rating_adj_table, render_peril_summary_table_post_uw_adj, render_peril_summary_el_table_post_uw_adj, render_tp_components_pre_uw_adj, render_tp_components_post_uw_adj, render_cat_aop_split, render_trapped_exposure, render_simulation_results, render_output_schedule_calculation, render_peril_summary_rates_table_post_uw_adj, render_peril_summary_rates_table_pre_uw_adj };