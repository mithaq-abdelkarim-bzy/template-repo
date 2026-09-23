import * as HX from "hx-model-components";


function vw_premium_group(scale) {
  return (
    <HX.Page title="Premium" fullWidth viewScale={0.9} shownBy="model_state/show_premium_group">
      <HX.Section title="Premium Calculations">
        {/* <HX.Collection fields={["debug_str", "debug_bool"]} /> */}
        <HX.Pane flow="right">
        </HX.Pane>
        <HX.Pane>
          <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
            <HX.Collection fields={["show_check_cols", "show_exposure_map", null, null]} horizontal syncColumnWidthsKey="aboveTable" />
            {/* Adding fields as a table to have kb-interactive */}
            <HX.Pane flow="right">
              <HX.Table data={["/cds/exposure/granular"]} fields={["data_check", "region_warning", "country_finder"]} kb-interactive rowHeaderSettings={{ width: 50 }} />
              <HX.Pane />
            </HX.Pane>
            {/* <HX.Collection fields={["data_check", "country_finder"]} horizontal syncColumnWidthsKey="aboveTable" /> */}
            <HX.Table
              data={["lives"]}
              fields={[
                { field: "no_lives", width: 100 },
                { field: "no_lives_check", width: 100, shownBy: "show_check_cols", labelBy: "check_col_labels/no_lives_check_label" },
                { field: "sex", width: 100 },
                { field: "sex_check", width: 100, shownBy: "show_check_cols", labelBy: "check_col_labels/sex_check_label" },
                { field: "age_attained", width: 110 },
                { field: "age_attained_check", width: 100, shownBy: "show_check_cols", labelBy: "check_col_labels/age_attained_check_label" },
                { field: "salary", width: 150 },
                { field: "salary_check", width: 100, shownBy: "show_check_cols", labelBy: "check_col_labels/salary_check_label" },
                { field: "salary_multiple", width: 100 },
                { field: "salary_multiple_check", width: 100, shownBy: "show_check_cols", labelBy: "check_col_labels/salary_multiple_check_label" },
                { field: "sum_insured", width: 150 },
                { field: "sum_insured_check", width: 100, shownBy: "show_check_cols", labelBy: "check_col_labels/sum_insured_check_label" },
                { field: "nationality", width: 200 },
                { field: "nationality_check", width: 100, shownBy: "show_check_cols", labelBy: "check_col_labels/nationality_check_label" },
                { field: "location", width: 200 },
                { field: "location_check", width: 100, shownBy: "show_check_cols", labelBy: "check_col_labels/location_check_label" },
                { field: "region", width: 200 },
                { field: "region_check", width: 150, shownBy: "show_check_cols", labelBy: "check_col_labels/region_check_label" },
                { field: "occupation_code", width: 130 },
                { field: "occupation_code_check", width: 100, shownBy: "show_check_cols", labelBy: "check_col_labels/occupation_code_check_label" },
                null,

                { field: "db_qx", width: 125 },
                { field: "db_expected_loss_cost_pre_uw_adj", width: 125 },
                { field: "db_technical_premium_pre_uw_adj", width: 125 },
                { field: "db_expected_loss_cost", width: 125 },
                { field: "db_technical_premium", width: 125 },

                { field: null, shownBy: "show_adb" },
                { field: "adb_qx", width: 125, shownBy: "show_adb" },
                { field: "adb_expected_loss_cost_pre_uw_adj", width: 125, shownBy: "show_adb" },
                { field: "adb_technical_premium_pre_uw_adj", width: 125, shownBy: "show_adb" },
                { field: "adb_expected_loss_cost", width: 125, shownBy: "show_adb" },
                { field: "adb_technical_premium", width: 125, shownBy: "show_adb" },

                { field: null, shownBy: "show_re" },
                { field: "re_rate", width: 125, shownBy: "show_re" },
                { field: "re_expected_loss_cost_pre_uw_adj", width: 125, shownBy: "show_re" },
                { field: "re_technical_premium_pre_uw_adj", width: 125, shownBy: "show_re" },
                { field: "re_expected_loss_cost", width: 125, shownBy: "show_re" },
                { field: "re_technical_premium", width: 125, shownBy: "show_re" },

                { field: null, shownBy: "show_ci" },
                { field: "ci_cover", width: 125, shownBy: "show_ci" },
                { field: "ci_rate", width: 125, shownBy: "show_ci" },
                { field: "ci_sum_insured", width: 125, shownBy: "show_ci" },
                { field: "ci_sum_insured_post_cap", width: 125, shownBy: "show_ci" },
                { field: "ci_expected_loss_cost_pre_uw_adj", width: 125, shownBy: "show_ci" },
                { field: "ci_technical_premium_pre_uw_adj", width: 125, shownBy: "show_ci" },
                { field: "ci_expected_loss_cost", width: 125, shownBy: "show_ci" },
                { field: "ci_technical_premium", width: 125, shownBy: "show_ci" },

                { field: null, shownBy: "show_ti" },
                { field: "ti_cover", width: 125, shownBy: "show_ti" },
                { field: "ti_proportion", width: 125, shownBy: "show_ti" },
                { field: "ti_rate", width: 125, shownBy: "show_ti" },
                { field: "ti_expected_loss_cost_pre_uw_adj", width: 125, shownBy: "show_ti" },
                { field: "ti_technical_premium_pre_uw_adj", width: 125, shownBy: "show_ti" },
                { field: "ti_expected_loss_cost", width: 125, shownBy: "show_ti" },
                { field: "ti_technical_premium", width: 125, shownBy: "show_ti" },

                null,
                { field: "no_claim_prob", width: 125 }
              ]}
              dynamic
              kb-interactive
              maxListVisibleRows={20}
            />
          </HX.With>
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_premium_group };
