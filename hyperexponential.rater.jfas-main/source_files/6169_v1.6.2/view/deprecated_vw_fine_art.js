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
      data={["fa_" + premise + "_summary", "fa_" + premise + "_summary_subtotal"]}
      fields={[
        "country",
        "tsi",
        "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "exp_band_7", "exp_band_8"]}
    />
  )
}

function fa_summarise_premise_2(premise, title_in) {
  return (
    <HX.Table
      title={title_in}
      data={["fa_" + premise + "_summary_rates"]}
      fields={[
        "country",
        "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "exp_band_7", "exp_band_8"]}
    />
  )
}

function deprecated_vw_fine_art() {
  return (
    <HX.Page fullWidth={true} viewScale={0.8} title="Deprecated Fine Art">
      <HX.Section title="Exposure Rate Summary">
        <HX.Pane flow="right">
          <HX.Table
            data={["fa_premises_summary", "fa_travel_summary", "fa_additional_summary"]}
            fields={["premium",
              "tsi",
              "ded",
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
              "fa_travel_rating_transitswithincity",
              "fa_travel_rating_transitswithincountry",
              "fa_travel_rating_transitswithineu",
              "fa_travel_rating_transitseuusa",
              "fa_travel_rating_transitsrow"]}
            fields={["travel_type", "tsi", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Fine Art Specific">
        <HX.Pane flow="down">
          <HX.Table
            title="Additional Peril Premium"
            data={[
              "fa_specific_additional_defectivetitle",
              "fa_specific_additional_computerslaptops",
              "fa_specific_additional_glass",
              "fa_specific_additional_jewelleryinsafe",
              "fa_specific_additional_jewelleryworn",
              "fa_specific_additional_libraryreference",
              "fa_specific_additional_money",
              "fa_specific_additional_officecontents",
              "fa_specific_additional_custom"
            ]}
            fields={["coverage", "tsi", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
          />
          <HX.Table
            title="Ancilliary Premium"
            data={[
              "fa_specific_ancilliary_bi",
              "fa_specific_ancilliary_buildings",
              "fa_specific_ancilliary_terrorism",
              "fa_specific_ancilliary_custom"
            ]}
            fields={["coverage", "tsi", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
          />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table
            title="Exhibitions"
            data={["fa_specific_exhibitions_natcat", "fa_specific_exhibitions_stay", "fa_specific_exhibitions_terrorism", "fa_specific_exhibitions_custom"]}
            fields={["coverage", "tsi", "no_of_transits_per_month", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
          />
          <HX.Table
            title="Exhibitions Transit"
            data={[
              "fa_specific_exhibitions_transit_transitswithincity",
              "fa_specific_exhibitions_transit_transitswithincountry",
              "fa_specific_exhibitions_transit_transitswithineu",
              "fa_specific_exhibitions_transit_transitseuusa",
              "fa_specific_exhibitions_transit_transitsrow",
              "fa_specific_exhibitions_transit_custom"]}
            fields={["coverage", "tsi", "no_of_transits_each_way", "uw_rate_per_100_tsi", "prem_rate_per_100_tsi", "premium"]}
          />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table
            title="Employers Liability"
            data={["fa_specific_liability_employers_base_premium", "fa_specific_liability_employers_5_10_employees", "fa_specific_liability_employers_10_20_employees", "fa_specific_liability_employers_20_or_more_employees"]}
            fields={["employers_liability", "no_of_employees", "per_employee", "premium"]}
          />
          <HX.Table
            title="Manual Work Surcharge"
            data={["fa_specific_liability_manual_woodworkers", "fa_specific_liability_manual_warehouseman", "fa_specific_liability_manual_drivers", "fa_specific_liability_manual_metalworkerspolishers"]}
            fields={["manual_work_surcharge", "salary", "prem_rate", "premium"]}
          />
          <HX.Table
            title="Public Liability"
            data={["fa_specific_liability_public"]}
            fields={["public_liability", "include_flag", "premium"]}
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { deprecated_vw_fine_art };