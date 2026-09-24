import * as HX from "hx-model-components";
import CombinationChart from "components/combination";

function vw_burn_output(scale) {
  return (
    <HX.Page title="Burn Output" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Summary">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Collection
              fields={["cds/experience_rating/exposure/burn_start_year"]}
            />
          </HX.Pane>
          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Table
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "limit_cnv", maxWidth: 400 },
                { field: "excess_cnv", maxWidth: 400 }
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane ratio={2}>
            <HX.Table
              data={[{ datum: "cds/experience_rating/claims_other/ten_largest" }]}
              fields={[
                { field: "year", width: 100 },
                { field: "description", maxWidth: 400 },
                { field: "previous_year_total", maxWidth: 400 },
                { field: "this_year_total", maxWidth: 400 },
                { field: "on_levelled_loss", maxWidth: 400 }
              ]}
              kb-interactive
            />
          </HX.Pane>
        </HX.Pane>

      </HX.Section >
      <HX.Section title="Layer Loss Summary">
        <HX.Pane flow="right" reflow={false}>
          <HX.Table
            title=" "
            data={[{ datum: "cds/experience_rating/claims_other/burn_year_result" }]}
            fields={[
              { field: "year", width: 100 },
              { field: "non_zero_claim_count", maxWidth: 400 },
              { field: "severity", maxWidth: 400 },
              { field: "on_levelled_loss", maxWidth: 400 },
              null,
              { field: "loss_layer_1", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_1", maxWidth: 400 },
              { field: "loss_layer_2", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_2", maxWidth: 400 },
              { field: "loss_layer_3", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_3", maxWidth: 400 },
              { field: "loss_layer_4", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_4", maxWidth: 400 },
              { field: "loss_layer_5", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_5", maxWidth: 400 },
              { field: "loss_layer_6", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_6", maxWidth: 400 },
              { field: "loss_layer_7", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_7", maxWidth: 400 },
              { field: "loss_layer_8", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_8", maxWidth: 400 },
              { field: "loss_layer_9", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_9", maxWidth: 400 },
              { field: "loss_layer_10", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_10", maxWidth: 400 },
              { field: "loss_layer_11", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_11", maxWidth: 400 },
              { field: "loss_layer_12", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_12", maxWidth: 400 },
              { field: "loss_layer_13", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_13", maxWidth: 400 },
              { field: "loss_layer_14", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_14", maxWidth: 400 },
              { field: "loss_layer_15", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_15", maxWidth: 400 },
              { field: "loss_layer_16", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_16", maxWidth: 400 },
              { field: "loss_layer_17", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_17", maxWidth: 400 },
              { field: "loss_layer_18", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_18", maxWidth: 400 },
              { field: "loss_layer_19", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_19", maxWidth: 400 },
              { field: "loss_layer_20", shownBy: "/cds/experience_rating/claims_other/show_loss_layer_20", maxWidth: 400 }
            ]}
            filter={"show_row"}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Selection">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane shownBy="cds/show_non_risk_xl" ratio={1}>
            <HX.Collection
              fields={["cds/experience_rating/claims_other/net_or_gross_reins_calc"]}
            />
          </HX.Pane>
          <HX.Pane shownBy="cds/show_risk_xl" ratio={1}>
            <HX.Collection
              fields={["cds/experience_rating/claims_other/risk_xl_use_rms_cat"]}
            />
          </HX.Pane>
          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>
        <HX.Notes stretch={true}
          field="cds/experience_rating/claims_other/burn_output_comments"
          title="Comments" />
        <HX.Table
          data={[{ datum: "cds/layers", maxWidth: 400 }]}
          fields={[
            { field: "burn/burn_result/avg_3_year" },
            { field: "burn/burn_result/avg_5_year" },
            { field: "burn/burn_result/avg_7_year" },
            { field: "burn/burn_result/avg_all_year" },
            { field: "burn/burn_result/selection" },
            null,
            { field: "burn/burn_result/gross_burn_el", shownBy: "/cds/experience_rating/claims_other/show_gross_fields" },
            { field: "burn/burn_result/gross_burn_sd", shownBy: "/cds/experience_rating/claims_other/show_gross_fields" },
            { field: "burn/burn_result/gross_burn_lol", shownBy: "/cds/experience_rating/claims_other/show_gross_fields" },
            { field: "burn/burn_result/gross_burn_sd_rol", shownBy: "/cds/experience_rating/claims_other/show_gross_fields" },

            { field: "burn/burn_result/risk_xl_non_cat_burn_gross_el", shownBy: "/cds/show_risk_xl" },
            { field: "burn/burn_result/risk_xl_cat_burn_gross_el", shownBy: "/cds/show_risk_xl" },
            { field: "burn/burn_result/risk_xl_rms_gross_el", shownBy: "/cds/show_risk_xl" },
            { field: null, shownBy: "/cds/show_risk_xl" },

            { field: "burn/burn_result/net_burn_el", shownBy: "/cds/experience_rating/claims_other/show_net_fields" },
            { field: "burn/burn_result/net_burn_sd", shownBy: "/cds/experience_rating/claims_other/show_net_fields" },
            { field: "burn/burn_result/net_burn_lol", shownBy: "/cds/experience_rating/claims_other/show_net_fields" },
            { field: "burn/burn_result/net_burn_sd_rol", shownBy: "/cds/experience_rating/claims_other/show_net_fields" }
          ]}
          rowHeaderSettings={{ width: 150 }}
          transpose
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Historic Losses">
        <HX.Pane >
          <CombinationChart
            title="Loss Chart"
            data={[
              { list: "cds/experience_rating/claims_other/burn_year_result", labelBy: "year" },
              { list: "cds/experience_rating/claims_other/burn_year_result", labelBy: "year" }
            ]}
            traces={[
              { field: "nominal_loss", label: "Nominal Losses" },
              { field: "on_levelled_loss", label: "OL Losses (excl. SuperCat)" },
            ]}
            series={[
              {
                seriesLabel: "Frequency Per CCYm Premium (OL)",
                points: [
                  {
                    list: "cds/experience_rating/claims_other/burn_year_result",
                    x: "year",
                    y: "freq_per_m_prem",
                  },
                ],
              }
            ]}
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_burn_output };