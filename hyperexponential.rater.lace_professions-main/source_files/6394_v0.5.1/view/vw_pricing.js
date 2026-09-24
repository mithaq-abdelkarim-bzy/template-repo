// v0.3.0
import * as HX from "hx-model-components";
import EditableText from "components/text_box_editable";
import ModalNotesEditor from "components/modal_notes_editor";

function vw_pricing(scale) {
  return (
    // <HX.Page title="Pricing" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
    <HX.Page title="Structure & Pricing" fullWidth={true} viewScale={scale} shownBy="model_state/layer_no_ia_use">
      <HX.Section title="Simulation" defaultCollapsed={false}>
        <HX.Pane flow="right">
          <HX.Button
            title="Run Simulation"
            task="run_simulation_task"
          />
          <HX.Notes field="cds/run_simulation_notes" shownBy="cds/run_simulation_notes_bool" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Retention" defaultCollapsed={false}>
        <HX.Notes field="cds/retention_split_notes" />
        <HX.Table
          data={[
            {
              datum: "retention_split"
            }
          ]}
          fields={[
            { field: "region", width: 230 },
            { field: "ccy", width: 110 },
            { field: "eec", width: 170 },
            { field: "aggregate", width: 170 },
            { field: "retention_underlying", width: 170, infoBy: "hover_info/retention_underlying" },
            { field: "retention_residual", width: 170, infoBy: "hover_info/retention_residual" },
            { field: "defence_cost_bool", width: 240 }
          ]}
          rowHeaderSettings={{ width: 50 }}
          with="cds"
          dynamic
          kb-interactive
        />
        <ModalNotesEditor
          notesPath="cds/retention_split_uw_comments"
          plainTextPath="cds/retention_split_uw_comments_plaintext"
          label="Underwriter Comments"
          width="400px"
          marginTop="4px"
          marginBottom="4px"
          autosave={true}
        />
      </HX.Section>
      <HX.Section title="Policy Structure (Exposure CCY)" defaultCollapsed={false}>
        <HX.Notes field="cds/policy_notes" />
        <HX.Collection fields={[
          { field: "cds/rating_factors/elevated_risk_year_load", infoBy: "cds/hover_info/elevated_risk_year_load" },
          { field: "cds/rating_factors/cat_load", infoBy: "cds/hover_info/cat_load" },
          null, null, null]} horizontal />
        <HX.Table
          data={[
            {
              datum: "layers", elementLabelBy: "name"
            }
          ]}
          fields={[
            { field: "include", width: 100 },
            { field: "limit_eec", width: 170 },
            { field: "limit_agg", width: 170 },
            { field: "excess_eec", width: 170 },
            { field: "excess_agg", width: 170 },
            { field: "rtc", width: 170, infoBy: "hover_info/rtc" },
            { field: "rtc_agg", width: 170 },
            null,
            { field: "defense_cost", width: 170 },
            { field: "brokerage", width: 170 },
            { field: "wordings_adj", width: 170, infoBy: "hover_info/wordings_adj" },
            { field: "uw_adj", width: 170, infoBy: "hover_info/uw_adj" },
            null,
            { field: "exposure_rate", width: 170 },
            { field: "exposure_rate_incl_adj", width: 170 },
            { field: "experience_rate", width: 170 },
            { field: "experience_rate_incl_adj", width: 170 },
            null,
            { field: "experience_weighting_2", width: 170 },
            { field: "blended_model_net_rate_pre", width: 170, infoBy: "hover_info/blended_model_net_rate" },
            { field: "expected_loss_cost_net_pre", width: 170, infoBy: "hover_info/expected_loss_cost_net" },
            { field: "blended_model_net_rate", width: 170, infoBy: "hover_info/blended_model_net_rate" },
            { field: "expected_loss_cost_net", width: 170, infoBy: "hover_info/expected_loss_cost_net" },
            // null,
            // { field: "uw_experience_weighting", width: 170, infoBy: "hover_info/uw_experience_weighting" },
            // { field: "blended_uw_net_rate", width: 170, infoBy: "hover_info/blended_uw_net_rate" },
            // { field: "benchmark_premium_uw_view", width: 170, infoBy: "hover_info/benchmark_premium_uw_view" },
            null,
            { field: "technical_premium_100", width: 170 },
            { field: "benchmark_premium_100", width: 170 },
            { field: "technical_premium_100_incl_adj", width: 170 },
            { field: "benchmark_premium_100_incl_adj", width: 170 },
            { field: "benchmark_premium_experience_100", width: 190 },
            { field: "benchmark_premium_exposure_100", width: 190 },
            { field: "quoted_premium_100", width: 170 },
            { field: "bound_premium_100", width: 170 },
            { field: "gross_rate_per_mill", width: 170, infoBy: "hover_info/gross_rate_per_mill" },
            { field: "bpi_quoted_100", width: 170 },
            { field: "bpi_bound_100", width: 170 },
            { field: "tpi_quoted_100", width: 170 },
            { field: "tpi_bound_100", width: 170 },
            { field: "bpi_quoted_100_incl_adj", width: 170 },
            { field: "bpi_bound_100_incl_adj", width: 170 },
            { field: "tpi_quoted_100_incl_adj", width: 170 },
            { field: "tpi_bound_100_incl_adj", width: 170 },
            null,
            { field: "status", width: 170 },
            { field: "section_reference", width: 170 },
            null,
            { field: "written_line", width: 170 },
            { field: "bound_premium_share", width: 170 },
            null,
            { field: "gross_premium_uw_view", width: 170 },
            { field: "technical_premium_ryv", width: 170 },
            { field: "benchmark_premium_ryv", width: 170 },
            { field: "bpi_quoted_ryv", width: 170 },
            { field: "bpi_bound_ryv", width: 170 },
            { field: "tpi_quoted_ryv", width: 170 },
            { field: "tpi_bound_ryv", width: 170 },
          ]}
          with="cds"
          rowHeaderSettings={{ width: 100 }}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Additional Policy Structure (Exposure CCY)" defaultCollapsed={false}>
        <HX.Table
          data={[
            {
              datum: "layers_addl", elementLabelBy: "name"
            }
          ]}
          fields={[
            { field: "include", width: 100 },
            { field: "limit_eec", width: 170 },
            { field: "limit_agg", width: 170 },
            { field: "excess_eec", width: 170 },
            { field: "excess_agg", width: 170 },
            { field: "rtc", width: 170, infoBy: "hover_info/rtc" },
            { field: "rtc_agg", width: 170 },
            null,
            { field: "defense_cost", width: 170 },
            { field: "brokerage", width: 170 },
            { field: "wordings_adj", width: 170, infoBy: "hover_info/wordings_adj" },
            { field: "uw_adj", width: 170, infoBy: "hover_info/uw_adj" },
            null,
            { field: "exposure_rate", width: 170 },
            { field: "exposure_rate_incl_adj", width: 170 },
            { field: "experience_rate", width: 170 },
            { field: "experience_rate_incl_adj", width: 170 },
            null,
            { field: "experience_weighting_2", width: 170 },
            { field: "blended_model_net_rate_pre", width: 170, infoBy: "hover_info/blended_model_net_rate" },
            { field: "expected_loss_cost_net_pre", width: 170, infoBy: "hover_info/expected_loss_cost_net" },
            { field: "blended_model_net_rate", width: 170, infoBy: "hover_info/blended_model_net_rate" },
            { field: "expected_loss_cost_net", width: 170, infoBy: "hover_info/expected_loss_cost_net" },
            null,
            // { field: "uw_experience_weighting", width: 170, infoBy: "hover_info/uw_experience_weighting" },
            // { field: "blended_uw_net_rate", width: 170, infoBy: "hover_info/blended_uw_net_rate" },
            // { field: "benchmark_premium_uw_view", width: 170, infoBy: "hover_info/benchmark_premium_uw_view" },
            // null,
            { field: "technical_premium_100", width: 170 },
            { field: "benchmark_premium_100", width: 170 },
            { field: "technical_premium_100_incl_adj", width: 170 },
            { field: "benchmark_premium_100_incl_adj", width: 170 },
            { field: "benchmark_premium_experience_100", width: 190 },
            { field: "benchmark_premium_exposure_100", width: 190 },
            { field: "quoted_premium_100", width: 170 },
            { field: "bound_premium_100", width: 170 },
            { field: "gross_rate_per_mill", width: 170, infoBy: "hover_info/gross_rate_per_mill" },
            { field: "bpi_quoted_100", width: 170 },
            { field: "bpi_bound_100", width: 170 },
            { field: "tpi_quoted_100", width: 170 },
            { field: "tpi_bound_100", width: 170 },
            { field: "bpi_quoted_100_incl_adj", width: 170 },
            { field: "bpi_bound_100_incl_adj", width: 170 },
            { field: "tpi_quoted_100_incl_adj", width: 170 },
            { field: "tpi_bound_100_incl_adj", width: 170 },
            null,
            { field: "status", width: 170 },
            { field: "section_reference", width: 170 },
            null,
            { field: "written_line", width: 170 },
            { field: "bound_premium_share", width: 170 },
            null,
            { field: "gross_premium_uw_view", width: 170 },
            { field: "technical_premium_ryv", width: 170 },
            { field: "benchmark_premium_ryv", width: 170 },
            { field: "bpi_quoted_ryv", width: 170 },
            { field: "bpi_bound_ryv", width: 170 },
            { field: "tpi_quoted_ryv", width: 170 },
            { field: "tpi_bound_ryv", width: 170 },
          ]}
          with="cds"
          rowHeaderSettings={{ width: 100 }}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Exposure Simulation Results - With UW Adj" defaultCollapsed={false}>
        <HX.Table
          data={[
            {
              datum: "layers", elementLabelBy: "name"
            }
          ]}
          fields={[
            { field: "include", width: 100 },
            { field: "sim_output_uw_adj/exposure_premium", width: 300 },
            { field: "sim_output_uw_adj/average_freq", width: 300 },
            { field: "sim_output_uw_adj/average_defense_cost_freq", width: 300 },
            { field: "sim_output_uw_adj/layer_exhaust_prob", width: 300 },
          ]}
          with="cds"
          rowHeaderSettings={{ width: 100 }}
          kb-interactive
        />
        <HX.Table
          data={[
            {
              datum: "layers_addl", elementLabelBy: "name"
            }
          ]}
          fields={[
            { field: "include", width: 100 },
            { field: "sim_output_uw_adj/exposure_premium", width: 300 },
            { field: "sim_output_uw_adj/average_freq", width: 300 },
            { field: "sim_output_uw_adj/average_defense_cost_freq", width: 300 },
            { field: "sim_output_uw_adj/layer_exhaust_prob", width: 300 },
          ]}
          with="cds"
          rowHeaderSettings={{ width: 100 }}
          kb-interactive
        />
      </HX.Section>
      {/* <HX.Section title="Exposure Simulation Results - No UW Adj" defaultCollapsed={false}>
        <HX.Table
          data={[
            {
              datum: "layers", elementLabelBy: "name"
            }
          ]}
          fields={[
            { field: "include", width: 100 },
            { field: "sim_output_no_uw_adj/exposure_premium", width: 300 },
            { field: "sim_output_no_uw_adj/average_freq", width: 300 },
            { field: "sim_output_no_uw_adj/average_defense_cost_freq", width: 300 },
            { field: "sim_output_no_uw_adj/layer_exhaust_prob", width: 300 },
          ]}
          with="cds"
          rowHeaderSettings={{ width: 100 }}
          kb-interactive
        />
        <HX.Table
          data={[
            {
              datum: "layers_addl", elementLabelBy: "name"
            }
          ]}
          fields={[
            { field: "include", width: 100 },
            { field: "sim_output_no_uw_adj/exposure_premium", width: 300 },
            { field: "sim_output_no_uw_adj/average_freq", width: 300 },
            { field: "sim_output_no_uw_adj/average_defense_cost_freq", width: 300 },
            { field: "sim_output_no_uw_adj/layer_exhaust_prob", width: 300 },
          ]}
          with="cds"
          rowHeaderSettings={{ width: 100 }}
          kb-interactive
        />
      </HX.Section> */}
      <HX.Section title="Technical Premium Build Up" defaultCollapsed={false}>
        <HX.Collection fields={[
          {
            field: "cds/technical_premium_buildup_layer",
          },
          null, null, null]} horizontal />
        <HX.CategoryChart
          data={["technical_premium", "benchmark_premium", "bound_premium"]}
          fields={["brokerage", "profit_load", "expenses", "ri_cost", "elc"]}
          // dataLabelField="year_label"
          columnType="stack"
          title="Premium Build Up"
          primaryAxis={{ label: "Premium" }}
          with="cds/pbu_chart/data"
        />
      </HX.Section>
      <HX.Section title="AvE Chart (FGU)" defaultCollapsed={true}>
        <HX.XYChart
          data={["data", "data"]}
          points={["points_exposure", "points_experience"]}
          xField="loss"
          yField="percentile"
          formatFrom="y"
          labelField={["label_exposure", "label_experience"]}
          xAxis={{
            label: "Loss",
          }}
          yAxis={{
            label: "Percentile",
          }}
          with="cds/ave_chart"
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_pricing };