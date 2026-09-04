import * as HX from "hx-model-components";
import Bar from "components/bar";

function vw_experience_rating(scale) {
  return (
    <HX.Page title="Experience Rating" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Control">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/experience_rating/data_source"]} />
          <HX.Button task="sql_bi_fetch_task" title="Fetch BI Data" shownBy="flags/er_source_bi" />
          <HX.Button task="sql_bi_clear" title="Clear BI Data" shownBy="flags/er_source_bi" />
          <HX.Collection fields={["flags/show_bi_claims"]} shownBy="flags/er_source_bi" />
          <HX.Collection fields={["cds/experience_rating/experience_data"]} shownBy="flags/er_source_user" />
          <HX.Pane shownBy="flags/er_source_user" />
          <HX.Pane shownBy="flags/er_source_user" />
          <HX.Pane shownBy="flags/er_source_user" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={["messages/fetch_bi_task_status"]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Experience Rating Summary">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/experience_rating/exposure_trend"]} />
          <HX.Button task="backfill_exposure" title="Backfill with Current Exposure" />
          <HX.Collection fields={[
            { field: "final_burning_cost", infoBy: "/messages/experience_rating_note" },
            "cat_rms_or_bp"
          ]} with="cds/experience_rating" numCols={2} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table
            data={[
              { datum: "er_calcs", elementLabelBy: "yoa_label" },
              { datum: "curr_yr", elementLabelBy: "yoa_label" },
              null,
              { datum: "er_totals", labelBy: "er_totals/yoa" }
            ]}
            fields={[
              { field: "exp_non_ed", width: 150 },
              { field: "exp_ed", width: 120 },
              { field: "sel_exp_base", width: 120 },
              { field: "ultimate_claims", width: 100 },
              { field: "sel_infl_index", width: 120 },
              { field: "inf_ultimate", width: 120 },
              { field: "include", width: 100 },
            ]}
            with="cds/experience_rating"
            kb-interactive
          />
          <Bar
            title="Projected on-levelled ULR by YOA"
            data={[
              { list: "cds/experience_rating/er_calcs", labelBy: "yoa" },
            ]}
            traces={[
              { field: "attrition_on_level_ulr", label: "Attritional ULR" },
              { field: "large_ulr", label: "Large ULR" },
              { field: "cat_ulr", label: "Cat ULR" },
            ]}
            xAxisTickAngle={-45}
            gapBetweenBarsSize={0.10}
            xAxisLabel="YOA"
            yAxisLabel="ULR"
            barMode="stack"
          />
          <Bar
            title="Percentage Change in Exposure Relative to Prior Year"
            data={[
              { list: "cds/experience_rating/er_chart_data", labelBy: "yoa" },
              // { list: "cds/experience_rating/er_chart_data", labelBy: "yoa" },
              // { list: "cds/experience_rating/er_chart_data", labelBy: "yoa" },
            ]}
            traces={[
              { field: "exp_non_ed_perc", label: "Non-Education" },
              { field: "exp_ed_perc", label: "Education" },
              { field: "gnwp_perc", label: "Original GNWP" },
            ]}
            xAxisTickAngle={-45}
            gapBetweenBarsSize={0.20}
            xAxisLabel="YOA"
            yAxisLabel="% Change"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Experience Rating Calculations" shownBy="flags/er_experience_data" >
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/experience_rating/cat_event"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Table
          data={[
            { datum: "er_calcs", elementLabelBy: "yoa_label" },
            { datum: "curr_yr", elementLabelBy: "yoa_label" },
            null,
            { datum: "er_totals", labelBy: "er_totals/yoa" }
          ]}
          fields={[
            { field: "gnwp", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "rate_change", width: 120, shownBy: "/flags/er_source_bi" },
            { field: "user_input_gnwp", width: 100, shownBy: "/flags/er_source_user" },
            { field: "user_input_rate_change", width: 120, shownBy: "/flags/er_source_user" },
            { field: "rate_change_index", width: 120 },
            { field: "on_level_premium", width: 120 },
            //{ field: "user_input_att", width: 100, shownBy: "/flags/er_source_user" },
            //{ field: "user_input_large", width: 100, shownBy: "/flags/er_source_user" },
            //{ field: "user_input_cat", width: 100, shownBy: "/flags/er_source_user" },
            { field: "user_input_att_ll_total", width: 230, shownBy: "/flags/er_source_user" },
            null,
            { field: "attrition_incurred", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "attrition_dev_factor", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "attrition_ielr", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "attrition_ult_claims", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "attrition_on_level_ulr", width: 120, shownBy: "/flags/er_source_bi" },
            null,
            { field: "large_incurred", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "large_avg_lr", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "large_ll_assumption", width: 120, shownBy: "/flags/er_source_bi" },
            { field: "large_weighted_ll", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "large_ult_claims", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "large_ulr", width: 100, shownBy: "/flags/er_source_bi" },
            null,
            { field: "cat_incurred", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "cat_avg", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "cat_rms_or_bp", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "cat_ult_claims", width: 100, shownBy: "/flags/er_source_bi" },
            { field: "cat_ulr", width: 100, shownBy: "/flags/er_source_bi" },
            null,
            { field: "total_att_ll_dev_factor", width: 100 },
            { field: "total_att_ll_ielr", width: 100 },
            { field: "attrition_ll_ult_claims", width: 100 },
            { field: "cat_bp", width: 100 },
            { field: "total_ult_claims", width: 100 },
            { field: "total_on_level_ulr", width: 120 },

          ]}
          with="cds/experience_rating"
          freezeLeft={0}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Experience Rating Frequency" shownBy="flags/er_experience_data_no">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/experience_rating/actual_incurred"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Table
          data={[
            { datum: "er_calcs", elementLabelBy: "yoa_label" },
            { datum: "curr_yr", elementLabelBy: "yoa_label" },
            null,
            { datum: "er_totals", labelBy: "er_totals/yoa" }
          ]}
          fields={[
            { field: "user_input_num_incidents", width: 100 },
            { field: "user_input_num_deaths", width: 100 },
            { field: "user_input_num_injuries", width: 100 },
            { field: "user_input_incurred_total", width: 230, shownBy: "/flags/er_actual_incurred" },
            { field: "frequency_ult_claims", width: 100 },
            { field: "frequency_infl_index", width: 100 },
            { field: "frequency_inf_ultimate", width: 120 },
          ]}
          with="cds/experience_rating"
          freezeLeft={0}
          kb-interactive
        />
      </HX.Section>
    </HX.Page>


  )
}
export { vw_experience_rating };