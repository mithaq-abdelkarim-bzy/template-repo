import * as HX from "hx-model-components";

function capitalise(string) {
  return (
    string.charAt(0).toUpperCase()
    + string.slice(1)
  )
}

function jb_summarise_premise(premise) {
  return (
    <HX.Table
      title={capitalise(premise)}
      data={["jb_premises/" + premise + "_summary", "jb_premises/" + premise + "_summary_subtotal"]}
      fields={["country", "tsi", "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "rate_band_1", "rate_band_2", "rate_band_3", "rate_band_4", "rate_band_5"]}
      kb-interactive
      with="coverages"
    />
  )
}

function jb_specific(specific, title, default_coverages) {
  const default_options = Array.from({ length: default_coverages }, (_, index) => "jb_specific/" + specific + "_" + index)
  default_options.push("jb_specific/" + specific + "_custom")
  return (
    <HX.Table
      title={title}
      data={default_options}
      fields={["coverage", "tsi", "prem_rate_per_100_tsi", "premium"]}
      kb-interactive
      with="coverages"
    />
  )
}

function vw_jewellers_block(scale) {
  return (
    <HX.Page title="Jewellers Block" fullWidth={true} viewScale={scale} shownBy="cds/show_page/show_jb">
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
        <HX.Section title="Exposure Rate Summary">
          <HX.Pane>
            <HX.Table
              data={["jb_premises", "jb_travel", "jb_additional"]}
              fields={["premium", "tsi", "deductible", "ded_perc", "credit", "uw_adj_impact", "prem_post_ded", "implied_rate_post_ded", "prem_ly", "tsi_ly", "ded_credit_ly", "uw_adj_impact_ly", "prem_post_ded_ly"]}
              kb-interactive
              with="coverages"
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Premises Rating">
          <HX.Pane>
            {jb_summarise_premise("retail")}
            {jb_summarise_premise("wholesale")}
            {jb_summarise_premise("manufacturing")}
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Travel Rating">
          <HX.Pane>
            <HX.Table
              data={["jb_travel/rating"]}
              fields={[
                "origin_region",
                "type_elsewhere_region/type",
                "type_elsewhere_region/elsewhere_region",
                "max_carryings",
                "average_carryings",
                "no_of_days",
                "prem_rate_per_100_tsi",
                "premium"]}
              kb-interactive
              with="coverages"
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Jewellers Block Specific">
          <HX.Pane flow="right">
            {jb_specific("additional", "Additional Peril Premiums", 10)}
            {jb_specific("ancillary", "Ancillary Premiums", 4)}
            {jb_specific("shipping", "Shipping Premiums", 8)}
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_jewellers_block };