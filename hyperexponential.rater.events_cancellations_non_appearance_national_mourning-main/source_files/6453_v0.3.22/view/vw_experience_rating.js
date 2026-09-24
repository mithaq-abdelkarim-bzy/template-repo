// v0.3.0
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";


function vw_experience_rating() {
  return (
    <HX.Page title="Experience Rating" fullWidth={true} shownBy="model_state/show_page_experience">
      <HX.With context={{ type: "struct", path: "cds/experience_rating" }}>
        <HX.Section title="Initial Selections">

          <HX.Pane flow="right">
            <HX.Table
              title="Key Values"
              data={[{ datum: "/cds/experience_rating" }]}
              fields={[
                "evaluation_date_calc",
                "evaluation_date_ovd",
                null,
                { "field": "el_final_calc", "shownBy": "/model_state/show_actuarial" },
                { "field": "el_final_ovd", "shownBy": "/model_state/show_actuarial" },
                "el_final",
                null,
                { "field": "el_weight_calc", "shownBy": "/model_state/show_actuarial" },
                { "field": "el_weight_ovd", "shownBy": "/model_state/show_actuarial" },
                "el_weight",
              ]}
              transpose
              kb-interactive
            />

            <HX.Pane>
              <HX.Table
                title="BI Data Load"
                data={[{ datum: "/cds/bi" }]}
                fields={[
                  "last_run_status",
                  "last_run_date",
                  { "field": "last_run_value", "shownBy": "/model_state/show_actuarial" },
                  { "field": "calc_run_value", "shownBy": "/model_state/show_actuarial" },
                  "check_run_consistent",
                ]}
                transpose
                kb-interactive
              />
              <HX.Button task="task_sql_bi_data"
                title="Load BI Data" />

            </HX.Pane>
          </HX.Pane>



        </HX.Section>




        <HX.Section title="Overall">
          <HX.Collection fields={["exposure_trend_backfill", null, null, null, null]} horizontal />
          <HX.Table
            data={[
              { datum: "analysis_table", elementLabelBy: "yoa_label" }
              , { datum: "analysis_table_cy", elementLabelBy: "yoa_label" }
              , null
              , { datum: "analysis_table_total_included", elementLabelBy: "yoa_label" }]}
            fields={[
              "include",
              "tiv_calc",
              "tiv_ovd",
              "gnwp_ol_dup",
              "total_ol_selected_ultimate_dup",
              "total_ol_selected_ulr_dup",
              "total_ol_selected_ult_to_tiv",
            ]}
            maxListVisibleRows={10}
            kb-interactive
          /*transpose*/
          />
        </HX.Section>

        <HX.Section title="Experience Rating - Input and Assumption" defaultCollapsed={true} >
          <HX.Table
            data={[
              { datum: "analysis_table", elementLabelBy: "yoa_label" }
              , { datum: "analysis_table_cy", elementLabelBy: "yoa_label" }]}
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
              { "field": "rate_inc", "shownBy": "/model_state/show_actuarial" },
              "rate_cum",
              null,
              "inf_inc_calc",
              "inf_inc_ovd",
              { "field": "inf_inc", "shownBy": "/model_state/show_actuarial" },
              "inf_cum",

              { "field": null, "shownBy": "/model_state/show_actuarial" },
              { "field": "attr_pct_ultimate_calc", "shownBy": "/model_state/show_actuarial" },
              { "field": "attr_pct_ultimate_ovd", "shownBy": "/model_state/show_actuarial" },
              { "field": "attr_ielr_calc", "shownBy": "/model_state/show_actuarial" },
              { "field": "attr_ielr_ovd", "shownBy": "/model_state/show_actuarial" },
              { "field": null, "shownBy": "/model_state/show_actuarial" },
              { "field": "large_pct_ultimate_calc", "shownBy": "/model_state/show_actuarial" },
              { "field": "large_pct_ultimate_ovd", "shownBy": "/model_state/show_actuarial" },
              { "field": "large_ielr_calc", "shownBy": "/model_state/show_actuarial" },
              { "field": "large_ielr_ovd", "shownBy": "/model_state/show_actuarial" },
              { "field": null, "shownBy": "/model_state/show_actuarial" },
              { "field": "cat_pct_ultimate_calc", "shownBy": "/model_state/show_actuarial" },
              { "field": "cat_pct_ultimate_ovd", "shownBy": "/model_state/show_actuarial" },
              { "field": "cat_ielr_calc", "shownBy": "/model_state/show_actuarial" },
              { "field": "cat_ielr_ovd", "shownBy": "/model_state/show_actuarial" },



            ]}
            title="Analysis Table"
            maxListVisibleRows={10}
            kb-interactive
          /*transpose*/
          />
        </HX.Section>



        <HX.Section title="Experience Rating - LR Projection" defaultCollapsed={true} >
          <HX.Table
            data={[
              { datum: "analysis_table", elementLabelBy: "yoa_label" }
              , null
              , { datum: "analysis_table_total", elementLabelBy: "yoa_label" }]}
            fields={[

              "gnwp_ol",
              "attr_ol_incurred",
              "large_ol_incurred",
              "cat_ol_incurred",
              { "field": "total_ol_incurred", "shownBy": "/model_state/show_actuarial" },
              null,

              "attr_pct_ultimate",
              { "field": "attr_ol_cl_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "attr_ol_bf_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "attr_ol_ielr_ultimate", "shownBy": "/model_state/show_actuarial" },
              "attr_ol_cl_lr",
              "attr_ol_bf_lr",
              "attr_ol_ielr",
              "attr_method",
              "attr_ol_selected_ultimate",
              "attr_ol_selected_ulr",
              null,

              { "field": "large_pct_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "large_ol_cl_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "large_ol_bf_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "large_ol_ielr_ultimate", "shownBy": "/model_state/show_actuarial" },
              "large_ol_cl_lr",
              { "field": "large_ol_bf_lr", "shownBy": "/model_state/show_actuarial" },
              "large_ol_ielr",
              "large_method",
              { "field": "large_credibility", "shownBy": "/model_state/show_actuarial" },
              "large_ol_selected_ultimate",
              "large_ol_selected_ulr",
              null,

              { "field": "cat_pct_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "cat_ol_cl_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "cat_ol_bf_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "cat_ol_ielr_ultimate", "shownBy": "/model_state/show_actuarial" },
              "cat_ol_cl_lr",
              { "field": "cat_ol_bf_lr", "shownBy": "/model_state/show_actuarial" },
              "cat_ol_ielr",
              "cat_method",
              "cat_ol_selected_ultimate",
              "cat_ol_selected_ulr",
              null,

              { "field": "total_pct_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "total_ol_cl_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "total_ol_bf_ultimate", "shownBy": "/model_state/show_actuarial" },
              { "field": "total_ol_ielr_ultimate", "shownBy": "/model_state/show_actuarial" },
              "total_ol_selected_ultimate",
              { "field": "total_ol_cl_lr", "shownBy": "/model_state/show_actuarial" },
              { "field": "total_ol_bf_lr", "shownBy": "/model_state/show_actuarial" },
              { "field": "total_ol_ielr", "shownBy": "/model_state/show_actuarial" },
              "total_ol_selected_ulr",

              { "field": null, "shownBy": "/model_state/show_actuarial" },
              { "field": "wgt_include", "shownBy": "/model_state/show_actuarial" },
              { "field": "wgt_decay", "shownBy": "/model_state/show_actuarial" },
              { "field": "wgt_exposure", "shownBy": "/model_state/show_actuarial" },
              { "field": "wgt_pct_ult", "shownBy": "/model_state/show_actuarial" },
              { "field": "wgt_overall_initial", "shownBy": "/model_state/show_actuarial" },
              { "field": "wgt_overall_final", "shownBy": "/model_state/show_actuarial" },

            ]}
            title="Analysis Table"
            maxListVisibleRows={10}
            kb-interactive
          /*transpose*/
          />
        </HX.Section>
      </HX.With>
    </HX.Page >
  )
}
export { vw_experience_rating };