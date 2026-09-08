import * as HX from "hx-model-components";

function render_quick_run_bar() {
  return (
    <HX.Section title="" collapsible={false}>
      <HX.Pane flow="right">
        <HX.Button title="Run Simulation" task="run_placeholder_task" />
        <HX.Button title="Run Rater" task="run_bordereau_rater_task" />
      </HX.Pane>
    </HX.Section>
  )
}

// function render_notifications() {
//   return (
//     <HX.Section title="Notifications" collapsible={true} shownBy="policy_information/notifications/show_notifications">
//       <HX.Pane >
//         <HX.Notes field="policy_information/notifications/notification_box" />
//       </HX.Pane>
//     </HX.Section>
//   )
// }


function render_kpi_summary_table_pre_uw_adj() {
  return (
    <HX.Table title="Pre UW Adj KPIs"
      data={[
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "premium.read_only", "achieved_rate",
        null,
        "pre_uw_adjustment/exposure_rating/gross_tech_prem_total",
        "pre_uw_adjustment/exposure_rating/benchmark_premium",
        "pre_uw_adjustment/exposure_rating/expected_loss",
        null,
        "pre_uw_adjustment/exposure_rating/tpi",
        "pre_uw_adjustment/exposure_rating/bpi",
        "pre_uw_adjustment/exposure_rating/elr",
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
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "premium.read_only", "achieved_rate",
        null,
        "post_uw_adjustment/exposure_rating/gross_tech_prem_total",
        "post_uw_adjustment/exposure_rating/benchmark_premium",
        "post_uw_adjustment/exposure_rating/expected_loss",
        null,
        "post_uw_adjustment/exposure_rating/tpi",
        "post_uw_adjustment/exposure_rating/bpi",
        "post_uw_adjustment/exposure_rating/elr",
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
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "coverages/fire/technical_premium_pre_uw_adj",
        null,
        "pre_uw_adjustment/us_gross_tech_prem", "coverages/ws/pre_uw_adjustment/us_gross_tech_prem",
        "coverages/scs/pre_uw_adjustment/us_gross_tech_prem", "coverages/fl/pre_uw_adjustment/us_gross_tech_prem",
        "coverages/eq/pre_uw_adjustment/us_gross_tech_prem", "coverages/wf/pre_uw_adjustment/us_gross_tech_prem",
        null,
        "pre_uw_adjustment/intl_gross_tech_prem", "coverages/ws/pre_uw_adjustment/intl_gross_tech_prem",
        "coverages/scs/pre_uw_adjustment/intl_gross_tech_prem", "coverages/fl/pre_uw_adjustment/intl_gross_tech_prem",
        "coverages/eq/pre_uw_adjustment/intl_gross_tech_prem", "coverages/wf/pre_uw_adjustment/intl_gross_tech_prem",
        null,
        "pre_uw_adjustment/gross_prem_rate",
        null,
        "coverages/fire/pre_uw_adjustment/gross_prem_rate",
        null,
        "pre_uw_adjustment/us_gross_prem_rate", "coverages/ws/pre_uw_adjustment/us_gross_prem_rate",
        "coverages/scs/pre_uw_adjustment/us_gross_prem_rate", "coverages/fl/pre_uw_adjustment/us_gross_prem_rate",
        "coverages/eq/pre_uw_adjustment/us_gross_prem_rate", "coverages/wf/pre_uw_adjustment/us_gross_prem_rate",
        null,
        "pre_uw_adjustment/intl_gross_prem_rate", "coverages/ws/pre_uw_adjustment/intl_gross_prem_rate",
        "coverages/scs/pre_uw_adjustment/intl_gross_prem_rate", "coverages/fl/pre_uw_adjustment/intl_gross_prem_rate",
        "coverages/eq/pre_uw_adjustment/intl_gross_prem_rate", "coverages/wf/pre_uw_adjustment/intl_gross_prem_rate",
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
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "coverages/fire/pre_uw_adjustment/exp_loss",
        null,
        "pre_uw_adjustment/us_exp_loss", "coverages/ws/pre_uw_adjustment/us_exp_loss",
        "coverages/scs/pre_uw_adjustment/us_exp_loss", "coverages/fl/pre_uw_adjustment/us_exp_loss",
        "coverages/eq/pre_uw_adjustment/us_exp_loss", "coverages/wf/pre_uw_adjustment/us_exp_loss",
        null,
        "pre_uw_adjustment/intl_exp_loss", "coverages/ws/pre_uw_adjustment/intl_exp_loss",
        "coverages/scs/pre_uw_adjustment/intl_exp_loss", "coverages/fl/pre_uw_adjustment/intl_exp_loss",
        "coverages/eq/pre_uw_adjustment/intl_exp_loss", "coverages/wf/pre_uw_adjustment/intl_exp_loss",
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
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "risk_appetite_summary/us_wind_aal", "risk_appetite_summary/us_eq_aal", "risk_appetite_summary/us_all_perils_aal",
        null,
        "risk_appetite_summary/us_wind_sd", "risk_appetite_summary/us_eq_sd", "risk_appetite_summary/us_all_perils_sd",
        null,
        "risk_appetite_summary/aep_impact_1_in_10", "risk_appetite_summary/oep_impact_1_in_250"
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}

function render_uw_adj_table() { // to do
  return (
    <HX.Table
      data={[
        "cds/uw_adjustments/risk_man",
        "cds/uw_adjustments/experience",
        "cds/uw_adjustments/valuation",
        "cds/uw_adjustments/other",
        "cds/uw_adjustments/total",
      ]}
      fields={[
        { field: "fire", width: 200 },
        // { field: "fire.validation", shownBy: "policy_information/requires_validation/fire", width: 200 },
        { field: "ws", width: 200 },
        // { field: "ws.validation", width: 200 },
        { field: "scs", width: 200 },
        // { field: "scs.validation", width: 200 },
        { field: "fl", width: 200 },
        // { field: "fl.validation", width: 200 },
        { field: "eq", width: 200 },
        // { field: "eq.validation", width: 200 },
        { field: "wf", width: 200 },
        // { field: "wf.validation", width: 200 },
      ]}
      kb-interactive
    />
  )
}

function render_peril_summary_table_post_uw_adj() {
  return (
    <HX.Table title="Post UW Adj Peril Details"
      data={[
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "coverages/fire/technical_premium",
        null,
        "post_uw_adjustment/us_gross_tech_prem", "coverages/ws/post_uw_adjustment/us_gross_tech_prem",
        "coverages/scs/post_uw_adjustment/us_gross_tech_prem", "coverages/fl/post_uw_adjustment/us_gross_tech_prem",
        "coverages/eq/post_uw_adjustment/us_gross_tech_prem", "coverages/wf/post_uw_adjustment/us_gross_tech_prem",
        null,
        "post_uw_adjustment/intl_gross_tech_prem", "coverages/ws/post_uw_adjustment/intl_gross_tech_prem",
        "coverages/scs/post_uw_adjustment/intl_gross_tech_prem", "coverages/fl/post_uw_adjustment/intl_gross_tech_prem",
        "coverages/eq/post_uw_adjustment/intl_gross_tech_prem", "coverages/wf/post_uw_adjustment/intl_gross_tech_prem",
        null,
        "post_uw_adjustment/gross_prem_rate",
        null,
        "coverages/fire/post_uw_adjustment/gross_prem_rate",
        null,
        "post_uw_adjustment/us_gross_prem_rate", "coverages/ws/post_uw_adjustment/us_gross_prem_rate",
        "coverages/scs/post_uw_adjustment/us_gross_prem_rate", "coverages/fl/post_uw_adjustment/us_gross_prem_rate",
        "coverages/eq/post_uw_adjustment/us_gross_prem_rate", "coverages/wf/post_uw_adjustment/us_gross_prem_rate",
        null,
        "post_uw_adjustment/intl_gross_prem_rate", "coverages/ws/post_uw_adjustment/intl_gross_prem_rate",
        "coverages/scs/post_uw_adjustment/intl_gross_prem_rate", "coverages/fl/post_uw_adjustment/intl_gross_prem_rate",
        "coverages/eq/post_uw_adjustment/intl_gross_prem_rate", "coverages/wf/post_uw_adjustment/intl_gross_prem_rate",
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
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "coverages/fire/post_uw_adjustment/exp_loss",
        null,
        "post_uw_adjustment/us_exp_loss", "coverages/ws/post_uw_adjustment/us_exp_loss",
        "coverages/scs/post_uw_adjustment/us_exp_loss", "coverages/fl/post_uw_adjustment/us_exp_loss",
        "coverages/eq/post_uw_adjustment/us_exp_loss", "coverages/wf/post_uw_adjustment/us_exp_loss",
        null,
        "post_uw_adjustment/intl_exp_loss", "coverages/ws/post_uw_adjustment/intl_exp_loss",
        "coverages/scs/post_uw_adjustment/intl_exp_loss", "coverages/fl/post_uw_adjustment/intl_exp_loss",
        "coverages/eq/post_uw_adjustment/intl_exp_loss", "coverages/wf/post_uw_adjustment/intl_exp_loss",
      ]}
      kb-interactive
      transpose
      freezeLeft={0}
    />
  )
}
// ############## JK comment 
// very confusing naming here "pre_uw_adjustment/us_exp_loss" is US Weather perils and "pre_uw_adjustment/exp_loss" is total us exepcted loss. I think need to change the naming convention here 
// I also think we need to add a gross or net indicator to the name

function render_tp_components_pre_uw_adj() {
  return (
    <HX.Table title="Pre UW Adj Technical Premium Breakdown"
      data={[
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "pre_uw_adjustment/exp_loss",
        "pre_uw_adjustment/tech_prem_components/coc",
        "pre_uw_adjustment/tech_prem_components/direct_expenses",
        "pre_uw_adjustment/tech_prem_components/indirect_expenses",
        "pre_uw_adjustment/tech_prem_components/lae",
        "pre_uw_adjustment/tech_prem_components/ri",
        "pre_uw_adjustment/tech_prem_components/sd",
        "pre_uw_adjustment/exposure_rating/gross_tech_prem_total",
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
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "post_uw_adjustment/exp_loss",
        "post_uw_adjustment/tech_prem_components/coc",
        "post_uw_adjustment/tech_prem_components/direct_expenses",
        "post_uw_adjustment/tech_prem_components/indirect_expenses",
        "post_uw_adjustment/tech_prem_components/lae",
        "post_uw_adjustment/tech_prem_components/ri",
        "post_uw_adjustment/tech_prem_components/sd",
        "post_uw_adjustment/exposure_rating/gross_tech_prem_total",
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
        { datum: "cds/layers", width: 150 }
      ]}
      fields={[
        "cat_aop_split/perc_us_wind",
        "cat_aop_split/perc_us_eq",
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

function render_simulation_results() {
  return (
    <HX.Section title="Simulation Output" defaultCollapsed={true}>
      <HX.Section title="RDS Events" defaultCollapsed={true}>
        <HX.Table
          data={[{ datum: "cds/layers", width: 200 }]}
          fields={[
            "simulation_output/rds_events/ca_eq_la", "simulation_output/rds_events/ca_eq_sf",
            "simulation_output/rds_events/nm_eq", "simulation_output/rds_events/nm_extreme_stress",
            "simulation_output/rds_events/nw_eq", "simulation_output/rds_events/fl_wind_miami",
            "simulation_output/rds_events/fl_wind_pinellas", "simulation_output/rds_events/us_wind_gulf_of_mexico",
            "simulation_output/rds_events/carolinas_wind", "simulation_output/rds_events/north_east_wind"
          ]}
          kb-interactive
          transpose
        />
      </HX.Section>
      <HX.Section title="Account OEP - 100% Ground Up Loss" defaultCollapsed={true}>
        <HX.Table
          data={[{ datum: "cds/layers", width: 200 }]}
          fields={[
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
          data={[{ datum: "cds/layers", width: 200 }]}
          fields={[
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
          data={[{ datum: "cds/layers", width: 200 }]}
          fields={[
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

// function render_output_schedule_calculation() {
//   return (
//     <HX.Section title="Output File" shownBy="policy_information/large_schedule_model" defaultCollapsed={true}>
//       <HX.File field="schedule/large_schedule_workflow/schedule_output_file" title="Output Calculation File" />
//     </HX.Section>
//   )
// }

export { render_quick_run_bar, /*render_notifications,*/ render_kpi_summary_table_pre_uw_adj, render_kpi_summary_table_post_uw_adj, render_peril_summary_table_pre_uw_adj, render_peril_summary_el_table_pre_uw_adj, render_risk_appetite_summary_table, render_uw_adj_table, render_peril_summary_table_post_uw_adj, render_peril_summary_el_table_post_uw_adj, render_tp_components_pre_uw_adj, render_tp_components_post_uw_adj, render_cat_aop_split, render_simulation_results, /*render_output_schedule_calculation*/ };