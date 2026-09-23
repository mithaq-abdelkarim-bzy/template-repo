import * as HX from "hx-model-components";

function capitalise(string) {
  return (
    string.charAt(0).replace("_", " ").toUpperCase()
    + string.slice(1)
  )
}

function fa_summarise_premise(premise, title_in) {
  return (
    <HX.Table
      title={title_in}
      data={["fa_premises/" + premise + "_summary", "fa_premises/" + premise + "_summary_subtotal"]}
      fields={[
        "country",
        "tsi",
        "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "exp_band_7", "exp_band_8"]}
      with="coverages"
    />
  )
}

function fa_summarise_premise_2(premise, title_in) {
  return (
    <HX.Table
      title={title_in}
      data={["fa_premises/" + premise + "_summary_rates"]}
      fields={[
        "country",
        "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "exp_band_7", "exp_band_8"]}
      with="coverages"
    />
  )
}

function vw_fine_art(scale) {
  return (
    <HX.Page fullWidth={true} viewScale={0.8} title="Fine Art" shownBy="cds/show_page/show_fa">
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
        <HX.Section title="Exposure Rate Summary">
          <HX.Pane flow="right">
            <HX.Table
              data={["fa_premises", "fa_travel", "fa_additional"]}
              fields={["premium",
                "tsi",
                "deductible",
                "ded_perc",
                "credit",
                "uw_adj_impact",
                "prem_post_ded",
                "implied_rate_post_ded",
                "prem_ly", "tsi_ly",
                "ded_credit_ly",
                "uw_adj_impact_ly",
                "prem_post_ded_ly"]}
              title="Summary"
              with="coverages"
            />
          </HX.Pane >
        </HX.Section >
        <HX.Section title="Premises Rating">
          <HX.Pane flow="right">
            {fa_summarise_premise("static_art", "Static Art")}
            {fa_summarise_premise_2("static_art", "Static Art")}
          </HX.Pane>
          <HX.Pane flow="right">
            {fa_summarise_premise("exhibitions", "Exhibitions")}
            {fa_summarise_premise_2("exhibitions", "Exhibitions")}
          </HX.Pane>
          <HX.Pane flow="right">
            {fa_summarise_premise("fa_misc", "FA Misc")}
            {fa_summarise_premise_2("fa_misc", "FA Misc")}
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Travel Rating">
          <HX.Pane>
            <HX.Table
              data={[
                "rating_0",
                "rating_1",
                "rating_2",
                "rating_3",
                "rating_4"]}
              fields={["travel_type", "tsi", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
              with="coverages/fa_travel"
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Fine Art Specific">
          <HX.Pane flow="down">
            <HX.Table
              title="Additional Peril Premium"
              data={[
                "additional_0",
                "additional_1",
                "additional_2",
                "additional_3",
                "additional_4",
                "additional_5",
                "additional_6",
                "additional_7",
                "additional_custom"
              ]}
              fields={["coverage", "tsi", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
              with="coverages/fa_specific"
            />
            <HX.Collection
              fields={[null]}
            />
            <HX.Table
              title="Ancilliary Premium"
              data={[
                "ancilliary_0",
                "ancilliary_1",
                "ancilliary_2",
                "ancilliary_custom"
              ]}
              fields={["coverage", "tsi", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
              with="coverages/fa_specific"
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Table
                title="Exhibitions"
                data={[
                  "exhibitions_0",
                  "exhibitions_1",
                  "exhibitions_2"
                ]}
                fields={["coverage", "tsi", "no_of_transits_per_month", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
                with="coverages/fa_specific"
              />
              <HX.Collection
                fields={[null]}
              />
              <HX.Table
                title="Exhibitions Transit"
                data={[
                  "exhibitions_transit_0",
                  "exhibitions_transit_1",
                  "exhibitions_transit_2",
                  "exhibitions_transit_3",
                  "exhibitions_transit_4",
                  "exhibitions_transit_custom"]}
                fields={["coverage", "tsi", "no_of_transits_each_way", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
                with="coverages/fa_specific"
              />
            </HX.Pane>
            <HX.Pane flow="down">
              <HX.Table
                title="Employers Liability"
                data={[
                  "liability_employers_0",
                  "liability_employers_1",
                  "liability_employers_2",
                  "liability_employers_3"
                ]}
                fields={["employers_liability", "no_of_employees", "per_employee", "premium"]}
                with="coverages/fa_specific"
              />
              <HX.Table
                title="Manual Work Surcharge"
                data={[
                  "liability_manual_0",
                  "liability_manual_1",
                  "liability_manual_2",
                  "liability_manual_3"
                ]}
                fields={["manual_work_surcharge", "salary", "prem_rate", "premium"]}
                with="coverages/fa_specific"
              />
              <HX.Table
                title="Public Liability"
                data={["liability_public"]}
                fields={["public_liability", "include_flag", "premium"]}
                with="coverages/fa_specific"
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page >
  )
}

export { vw_fine_art };