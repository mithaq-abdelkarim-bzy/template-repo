import * as HX from "hx-model-components";

function vw_risk_xl_exposure_rating(scale) {
  return (
    <HX.Page title="Risk XL Exposure Rating" fullWidth={true} viewScale={scale} shownBy="cds/show_risk_xl">
      <HX.Section title="Layer Information">
        <HX.Pane>
          <HX.Table
            title="This Year"
            data={[{ datum: "cds/layers" }]}
            fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "aggregate_deductible.read_only_option",
              { field: "summary/ty/reinstatement_description" },
              null,
              { field: "model/rms/gross_el" },
              { field: "model/rms/gross_sd" },
              null,

              { field: "model/rms/eq_el", shownBy: "/cds/show_us_fields" },
              { field: "model/rms/ws_el", shownBy: "/cds/show_us_fields" },
              { field: "model/rms/scs_el", shownBy: "/cds/show_us_fields" },

              { field: "model/rms/eu_ws_el", shownBy: "/cds/show_intl_fields" },
              { field: "model/rms/jp_eq_el", shownBy: "/cds/show_intl_fields" },
              { field: "model/rms/jp_ws_el", shownBy: "/cds/show_intl_fields" },
              { field: "model/rms/can_eq_el", shownBy: "/cds/show_intl_fields" },
              { field: "model/rms/caribbean_ws_el", shownBy: "/cds/show_intl_fields" },
              null,
              { field: "model/rms/perc_us_el", shownBy: "/cds/show_perc_us_el" }
            ]}
            freezeLeft={0}
            kb-interactive
          />
          <HX.Table
            title="Previous Year"
            data={[{ datum: "cds/layers" }]}
            fields={[
              "limit_ly",
              "excess_ly",
              "aggregate_deductible_ly",
              { field: "summary/ly/reinstatement_description" },
              null,
              { field: "model_prev/rms/gross_el" },
              { field: "model_prev/rms/gross_sd" },
              null,
              { field: "model_prev/rms/eq_el", shownBy: "/cds/show_us_fields" },
              { field: "model_prev/rms/ws_el", shownBy: "/cds/show_us_fields" },
              { field: "model_prev/rms/scs_el", shownBy: "/cds/show_us_fields" },

              { field: "model_prev/rms/eu_ws_el", shownBy: "/cds/show_intl_fields" },
              { field: "model_prev/rms/jp_eq_el", shownBy: "/cds/show_intl_fields" },
              { field: "model_prev/rms/jp_ws_el", shownBy: "/cds/show_intl_fields" },
              { field: "model_prev/rms/can_eq_el", shownBy: "/cds/show_intl_fields" },
              { field: "model_prev/rms/caribbean_ws_el", shownBy: "/cds/show_intl_fields" },
              null,
              { field: "model_prev/rms/perc_us_el", shownBy: "/cds/show_perc_us_el" }
            ]}
            freezeLeft={0}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Coverage">
        <HX.Pane>
          <HX.Table
            data={[
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_total" },
              null,
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_1" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_2" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_3" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_4" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_5" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_6" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_7" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_8" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_9" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_10" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_11" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_12" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_13" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_14" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_15" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_16" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_17" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_18" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_19" },
              { datum: "cds/risk_xl_exposure_rating/exposure_segment_20" },
            ]}
            fields={[
              "segment_name",
              "ex_cat_ulr",
              "curve_selection",
              "commentary",
              "exposed_limit_ty",
              "exposed_limit_ly",
              "exposed_limit_change"
            ]}
            freezeLeft={0}
            kb-interactive
            transpose
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Exposure Entry">
        <HX.Pane>
          <HX.Collection
            numCols={5}

            fields={[
              "cds/risk_xl_exposure_rating/gnepi_exposure_adjustment",
              "cds/risk_xl_exposure_rating/gnepi_adj_factor",
              null,
              null,
              null,
              "cds/risk_xl_exposure_rating/gnepi_by_band"
            ]}
          />
          <HX.Table
            data={[{ datum: "cds/risk_xl_exposure_rating/exposure_listing" }]}
            fields={[
              "lel_from",
              "lel_to",
              // "attachment_band",
              "segment",
              null,
              "location_count",
              "gnepi",
              "tiv",
              // "net_exposed_limit",
              // "avg_cedant_participation",
              // "avg_attachment",
              null,
              "location_count_adj",
              "gnepi_adj",
              "tiv_adj",
              // "net_exposed_limit_adj",
              null,
              "avg_tiv",
              // "avg_lel",
              // "avg_100_pol_limit",
              null,
              // "gross_el",
              // "avg_policy_worth",
              "ex_cat_ulr_readonly",
              "ex_cat_ulr_override",
              null,
              "gu_el",
              null,
              "swiss_re_c",
              "swiss_re_c_override",
              null,
              "expected_severity_perc",
              "expected_severity",
              "expected_frequency",
              null,
              { field: "loss_layer_1", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_1" },
              { field: "loss_layer_2", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_2" },
              { field: "loss_layer_3", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_3" },
              { field: "loss_layer_4", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_4" },
              { field: "loss_layer_5", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_5" },
              { field: "loss_layer_6", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_6" },
              { field: "loss_layer_7", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_7" },
              { field: "loss_layer_8", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_8" },
              { field: "loss_layer_9", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_9" },
              { field: "loss_layer_10", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_10" },
              { field: "loss_layer_11", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_11" },
              { field: "loss_layer_12", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_12" },
              { field: "loss_layer_13", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_13" },
              { field: "loss_layer_14", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_14" },
              { field: "loss_layer_15", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_15" },
              { field: "loss_layer_16", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_16" },
              { field: "loss_layer_17", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_17" },
              { field: "loss_layer_18", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_18" },
              { field: "loss_layer_19", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_19" },
              { field: "loss_layer_20", shownBy: "/cds/risk_xl_exposure_rating/show_loss_layer_20" }
            ]}
            freezeLeft={0}
            kb-interactive
            maxListVisibleRows={25}
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="">
        <HX.Pane flow="right" reflow={false}>
          <HX.Button task="run_exposure_simulation_task" title="Run Exposure Simulation" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Simulation Output">
        <HX.Table
          data={[{ datum: "cds/layers" }]}
          fields={[
            { field: "risk_xl_exposure_rating/gross_non_cat_el_deterministic" },
            { field: "risk_xl_exposure_rating/gross_total_el_deterministic" },
            null,
            { field: "risk_xl_exposure_rating/gross_total_el_sim" },
            null,
            { field: "risk_xl_exposure_rating/model_limit_factor", infoBy: "/cds/number_reins_factor_info" },
            { field: "risk_xl_exposure_rating/net_el_excl_reins_prem" },
            null,
            { field: "risk_xl_exposure_rating/no_expected_reins", infoBy: "/cds/paid_reins_factor_info" },
            null,
            { field: "risk_xl_exposure_rating/net_el" }
          ]}
          freezeLeft={0}
          kb-interactive
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_risk_xl_exposure_rating };