import * as HX from "hx-model-components";

function vw_cash_in_transit(scale) {
  return (
    <HX.Page title="Cash in Transit" fullWidth={true} viewScale={scale} shownBy="cds/show_page/show_cit">
      <HX.With context={{ "index": 0, "path": "cds/layers", "type": "list" }}>
        <HX.Section title="Exposure Rate Summary">
          <HX.Pane>
            <HX.Table
              data={["cit_premises", "cit_additional"]}
              fields={["premium", "tsi", "deductible", "ded_perc", "credit", "uw_adj_impact", "prem_post_ded", "implied_rate_post_ded", "prem_ly", "tsi_ly", "ded_credit_ly", "uw_adj_impact_ly", "prem_post_ded_ly"]}
              kb-interactive
              with="coverages"
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Premises Rating">
          <HX.Pane>
            <HX.Table
              title="General"
              data={["cit_general_summary", "cit_general_summary_subtotal"]}
              fields={["country", "tsi", "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "rate_band_1", "rate_band_2", "rate_band_3", "rate_band_4", "rate_band_5", "rate_band_6"]}
              kb-interactive
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Cash in Transit Specific">
          <HX.Table
            title="Primary Carrying Method"
            data={["specific_0", "specific_1", "specific_2", "specific_3", "specific_4"]}
            fields={["coverage", "usa", "na_ex_usa", "sa", "uk", "europe", "asia", "oceania", "africa", "total", "rate_usa", "rate_na_ex_usa", "rate_sa", "rate_uk", "rate_europe", "rate_asia", "rate_oceania", "rate_africa", "rate_total"]}
            kb-interactive
            with="coverages/cit_additional"
          />
          <HX.Table
            title="Other Carrying Methods"
            data={["specific_5", "specific_6", "specific_7", "specific_8", "specific_custom"]}
            fields={["coverage", "usa", "na_ex_usa", "sa", "uk", "europe", "asia", "oceania", "africa", "total", "rate_usa", "rate_na_ex_usa", "rate_sa", "rate_uk", "rate_europe", "rate_asia", "rate_oceania", "rate_africa", "rate_total"]}
            kb-interactive
            with="coverages/cit_additional"
          />
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_cash_in_transit };