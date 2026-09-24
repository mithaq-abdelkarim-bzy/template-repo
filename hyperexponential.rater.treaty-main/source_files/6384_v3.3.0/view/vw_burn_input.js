import * as HX from "hx-model-components";

function vw_burn_input(scale) {
  return (
    <HX.Page title="Burn Input" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Coverage">
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/experience_rating/coverage" }]}
            fields={[
              "coverage_1",
              "coverage_2",
              "coverage_3",
              "coverage_4",
              "coverage_5",
              "coverage_6",
              "coverage_7",
              "coverage_8"]}
            freezeLeft={0}
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/layers" }]}
            fields={["limit_cnv"
              , "excess_cnv"
              , null
              , { field: "burn/burn_coverage/coverage_1", labelBy: "/cds/experience_rating/coverage/coverage_1" }
              , { field: "burn/burn_coverage/coverage_2", labelBy: "/cds/experience_rating/coverage/coverage_2" }
              , { field: "burn/burn_coverage/coverage_3", labelBy: "/cds/experience_rating/coverage/coverage_3" }
              , { field: "burn/burn_coverage/coverage_4", labelBy: "/cds/experience_rating/coverage/coverage_4" }
              , { field: "burn/burn_coverage/coverage_5", labelBy: "/cds/experience_rating/coverage/coverage_5" }
              , { field: "burn/burn_coverage/coverage_6", labelBy: "/cds/experience_rating/coverage/coverage_6" }
              , { field: "burn/burn_coverage/coverage_7", labelBy: "/cds/experience_rating/coverage/coverage_7" }
              , { field: "burn/burn_coverage/coverage_8", labelBy: "/cds/experience_rating/coverage/coverage_8" }
            ]}
            freezeLeft={0}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section >
      <HX.Section title="Exposure Input">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Notes
              field="cds/experience_rating/exposure/exposure_input_information"
              title="Exposure Input Information"
            />
            <HX.Collection
              fields={["cds/experience_rating/exposure/exposure_start_year"]}
            />
          </HX.Pane>
          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>
        <HX.With context={{ type: "struct", path: "cds/experience_rating/exposure" }} >
          <HX.Pane flow="right" reflow={false} shownBy="/cds/show_non_risk_xl" >
            <HX.Table
              title=" "
              data={[
                "gnepi_exposure_segment",
                null,
                { datum: "exposure_segment_1" },
                { datum: "exposure_segment_2" },
                { datum: "exposure_segment_3" }
              ]}
              fields={["segment_type", "segment_name", "allow_for_rc", "allow_for_other_changes", "inflation_option"]}
              transpose
              kb-interactive
            />
            <HX.Notes stretch={true}
              field="comments"
              title="Comments" />
          </HX.Pane>
          <HX.Pane>
            <HX.Pane flow="right" reflow={false}>
              <HX.Table
                data={["rate_change_gross_net", null, "exposure_listing"]}
                fields={[
                  "year",
                  { field: "pif", shownBy: "/cds/show_risk_xl" },
                  "gnepi_actual",
                  "gnepi_projected",
                  null,
                  { field: "exposure_value_1", labelBy: "/cds/experience_rating/exposure/exposure_segment_1/exposure_label", shownBy: "/cds/show_non_risk_xl" },
                  { field: "exposure_value_2", labelBy: "/cds/experience_rating/exposure/exposure_segment_2/exposure_label", shownBy: "/cds/show_non_risk_xl" },
                  { field: "exposure_value_3", labelBy: "/cds/experience_rating/exposure/exposure_segment_3/exposure_label", shownBy: "/cds/show_non_risk_xl" },
                  null,
                  "rate_change",
                  "inflation_option_1",
                  { field: "inflation_option_2", shownBy: "/cds/show_non_risk_xl" },
                  { field: "other_changes", shownBy: "/cds/show_non_risk_xl" },
                  null,
                  "gnepi_exposure_change",
                  { field: "exposure_change_1", labelBy: "/cds/experience_rating/exposure/exposure_segment_1/exposure_change_label", shownBy: "/cds/show_non_risk_xl" },
                  { field: "exposure_change_2", labelBy: "/cds/experience_rating/exposure/exposure_segment_2/exposure_change_label", shownBy: "/cds/show_non_risk_xl" },
                  { field: "exposure_change_3", labelBy: "/cds/experience_rating/exposure/exposure_segment_3/exposure_change_label", shownBy: "/cds/show_non_risk_xl" },
                  null,
                  "gnepi_exposure_index",
                  { field: "exposure_index_1", labelBy: "/cds/experience_rating/exposure/exposure_segment_1/exposure_index_label", shownBy: "/cds/show_non_risk_xl" },
                  { field: "exposure_index_2", labelBy: "/cds/experience_rating/exposure/exposure_segment_2/exposure_index_label", shownBy: "/cds/show_non_risk_xl" },
                  { field: "exposure_index_3", labelBy: "/cds/experience_rating/exposure/exposure_segment_3/exposure_index_label", shownBy: "/cds/show_non_risk_xl" },
                  null,
                  { field: "gnepi_total_index", shownBy: "/cds/show_non_risk_xl" },
                  { field: "total_index_1", labelBy: "/cds/experience_rating/exposure/exposure_segment_1/total_index_label", shownBy: "/cds/show_non_risk_xl" },
                  { field: "total_index_2", labelBy: "/cds/experience_rating/exposure/exposure_segment_2/total_index_label", shownBy: "/cds/show_non_risk_xl" },
                  { field: "total_index_3", labelBy: "/cds/experience_rating/exposure/exposure_segment_3/total_index_label", shownBy: "/cds/show_non_risk_xl" },
                  null,
                  { field: "risk_frequency_index", shownBy: "/cds/show_risk_xl" },
                  null,
                  { field: "risk_avg_exposure_index", shownBy: "/cds/show_risk_xl" },
                  { field: "risk_inflation_index", shownBy: "/cds/show_risk_xl" },
                  { field: "risk_severity_index", shownBy: "/cds/show_risk_xl" }
                ]}
                freezeLeft={1}
                filter={"show_row_exposure"}
                kb-interactive
              />
            </HX.Pane>
          </HX.Pane>
        </HX.With>
      </HX.Section>

      <HX.Section title="Claims Input">
        <HX.With context={{ type: "struct", path: "cds/experience_rating" }} >
          <HX.Notes stretch={true}
            field="claims_other/comments"
            title="Comments" />
          <HX.Table
            data={["claims"]}
            fields={[
              "year",
              "currency",
              "description",
              { field: "cat_non_cat", shownBy: "/cds/show_risk_xl" },
              { field: "cat_name", shownBy: "/cds/show_risk_xl" },
              "large_loss",
              "coverage",
              null,
              "gnepi_loss",
              { field: "loss_segment_1", labelBy: "/cds/experience_rating/claims_other/loss_segment_label_1", shownBy: "/cds/show_non_risk_xl" },
              { field: "loss_segment_2", labelBy: "/cds/experience_rating/claims_other/loss_segment_label_2", shownBy: "/cds/show_non_risk_xl" },
              { field: "loss_segment_3", labelBy: "/cds/experience_rating/claims_other/loss_segment_label_3", shownBy: "/cds/show_non_risk_xl" },
              null,
              "previous_year_total",
              "this_year_total",
              "movement",
              "loss_type",
              "as_if_loss",
              { field: "on_levelled_loss", labelBy: "/cds/burn_ol_ccy_label" },
              { field: "return_period", shownBy: "/cds/show_non_risk_xl" },
              "comment",
              null,
              { field: "loss_layer_1", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_1" },
              { field: "loss_layer_2", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_2" },
              { field: "loss_layer_3", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_3" },
              { field: "loss_layer_4", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_4" },
              { field: "loss_layer_5", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_5" },
              { field: "loss_layer_6", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_6" },
              { field: "loss_layer_7", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_7" },
              { field: "loss_layer_8", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_8" },
              { field: "loss_layer_9", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_9" },
              { field: "loss_layer_10", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_10" },
              { field: "loss_layer_11", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_11" },
              { field: "loss_layer_12", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_12" },
              { field: "loss_layer_13", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_13" },
              { field: "loss_layer_14", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_14" },
              { field: "loss_layer_15", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_15" },
              { field: "loss_layer_16", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_16" },
              { field: "loss_layer_17", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_17" },
              { field: "loss_layer_18", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_18" },
              { field: "loss_layer_19", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_19" },
              { field: "loss_layer_20", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_20" }
            ]}
            kb-interactive
          />
        </HX.With>
      </HX.Section>

    </HX.Page >
  )
}

export { vw_burn_input };