import * as HX from "hx-model-components";
import { render_notifications, render_quick_run_bar, render_kpi_summary_table_pre_uw_adj, render_kpi_summary_table_post_uw_adj, render_peril_summary_table_pre_uw_adj, render_peril_summary_el_table_pre_uw_adj, render_risk_appetite_summary_table, render_uw_adj_table, render_experience_rating_adj_table, render_peril_summary_table_post_uw_adj, render_peril_summary_el_table_post_uw_adj, render_tp_components_pre_uw_adj, render_tp_components_post_uw_adj, render_cat_aop_split, render_trapped_exposure, render_simulation_results, render_output_schedule_calculation, render_peril_summary_rates_table_pre_uw_adj, render_peril_summary_rates_table_post_uw_adj } from "view/results_tables";
import { render_fire_rating_table } from "view/fire_analysis"
import { render_scs_rating_table } from "view/scs_analysis"
import { render_flood_rating_table } from "view/flood_analysis"
import { render_wildfire_rating_table } from "view/wildfire_analysis"
import { render_hurricane_rating_table } from "view/windstorm_analysis"
import { render_earthquake_rating_table } from "view/earthquake_analysis"

function rating_summary() {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} viewScale={0.9} shownBy="model_state/show_after_landing_page">
      {render_notifications()}
      {render_quick_run_bar()}
      <HX.Section title="Warnings/Messages" shownBy="control/show_run_rater_warning">
        <HX.Notes field="info/run_rater_warning" />
      </HX.Section>
      <HX.Section title="Underwriter Adjustments">
        {render_uw_adj_table()}
        {render_experience_rating_adj_table()}
        <HX.Pane flow="right">
          <HX.Button task="remove_experience_adjustment_task" title="Clear Non-Cat Experience Adjustment" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="KPIs">
        <HX.Pane flow="right">
          {render_kpi_summary_table_pre_uw_adj()}
          {render_kpi_summary_table_post_uw_adj()}
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Peril Details">
        <HX.Pane flow="right">
          {render_peril_summary_table_pre_uw_adj()}
          {render_peril_summary_table_post_uw_adj()}
        </HX.Pane>
        <HX.Section title="Technical Rates" defaultCollapsed={true}>
          <HX.Pane flow="right">
            {render_peril_summary_rates_table_pre_uw_adj()}
            {render_peril_summary_rates_table_post_uw_adj()}
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Expected Loss" defaultCollapsed={true}>
          <HX.Pane flow="right">
            {render_peril_summary_el_table_pre_uw_adj()}
            {render_peril_summary_el_table_post_uw_adj()}
          </HX.Pane>
        </HX.Section>
      </HX.Section>
      <HX.Section title="Technical Premium Breakdown">
        <HX.Pane flow="right">
          {render_tp_components_pre_uw_adj()}
          {render_tp_components_post_uw_adj()}
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Risk Appetite Summary">
        <HX.Pane>
          {render_risk_appetite_summary_table()}
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Additional Diagnostics">
        <HX.Pane flow="down">
          {render_cat_aop_split()}
          {render_trapped_exposure()}
        </HX.Pane>
      </HX.Section>
      {render_simulation_results()}
      {render_output_schedule_calculation()}
      <HX.Section title="DF Output" shownBy="policy_information/is_case_priced" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.File field={"df_output"} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

function by_peril_summary() {
  return (
    <HX.Page title="By Peril Summary" fullWidth={true} viewScale={0.9} shownBy="model_state/show_after_landing_page">
      {render_notifications()}
      {render_fire_rating_table()}
      {render_scs_rating_table()}
      {render_flood_rating_table()}
      {render_wildfire_rating_table()}
      {render_hurricane_rating_table()}
      {render_earthquake_rating_table()}
    </HX.Page >
  )
}

export { rating_summary, by_peril_summary };