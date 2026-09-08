import * as HX from "hx-model-components";

function TransitCollection(props) {
  return <HX.Collection with="coverages/conloss_transit" horizontal {...props} />;
}

function ConLossCollection(props) {
  return <HX.Collection with="coverages/conloss" horizontal {...props} />;
}

function vw_conloss(scale) {
  return (
    <HX.Page title="Con Loss" viewScale={scale} shownBy="cds/cover_selection/is_conloss">

      <HX.Section title="Transit" defaultCollapsed>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane>
            {TransitCollection({ fields: ["transit_flag", "base_rate"] })}
            {TransitCollection({ fields: ["trans_vals", "trans_vals_factor"] })}
            {TransitCollection({ fields: ["deductible_level", "deductible_level_factor"] })}
            <HX.Section title="Packaging" collapsible={false}>
              <HX.Pane flow="right">
                <HX.Collection with="coverages/conloss_transit" fields={["packaging_1", "packaging_2"]} />
                <HX.Collection with="coverages/conloss_transit" fields={["packaging_1_factor", "packaging_2_factor", "packaging_factor"]} />
              </HX.Pane>
              {TransitCollection({ fields: [null, "packaging_check"], shownBy: "packaging_check_show" })}
            </HX.Section>
            <HX.Section title="Conveyance" collapsible={false}>
              <HX.Pane flow="right">
                <HX.Collection with="coverages/conloss_transit" fields={["conv_air", "conv_land", "conv_sea"]} />
                <HX.Collection with="coverages/conloss_transit" fields={["conv_air_factor", "conv_land_factor", "conv_sea_factor", "conv_factor"]} />
              </HX.Pane>
              {TransitCollection({ fields: [null, "conv_check"], shownBy: "conv_check_show" })}
            </HX.Section>
            {TransitCollection({ fields: ["voyage", "voyage_factor"] })}
            {TransitCollection({ fields: ["surveyor", "surveyor_factor"] })}
            {TransitCollection({ fields: ["vessel", "vessel_factor"] })}
            {TransitCollection({ fields: ["type_of_cover", "type_of_cover_factor"] })}
            {TransitCollection({ fields: ["uw_discretion", "uw_discretion_factor"] })}
            <HX.Section title="Premium Summary" defaultCollapsed>
              {TransitCollection({
                title: "Model",
                fields: ["technical_deductions", "technical_rate", "technical_premium"]
              })}
              {TransitCollection({
                title: "Actual",
                fields: ["pct_of_technical", "actual_rate", "quoted_premium"]
              })}
            </HX.Section>
          </HX.Pane>
        </HX.With>
      </HX.Section>

      <HX.Section title="Con Loss" defaultCollapsed>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane>
            {ConLossCollection({ fields: ["conloss_flag", "base_rate"] })}
            {ConLossCollection({ fields: ["limit", "limit_factor"] })}
            {ConLossCollection({ fields: ["exposure", "exposure_factor"] })}
            {ConLossCollection({ fields: ["indemnity_period", null] })}
            {ConLossCollection({ fields: ["deductible_level", "deductible_level_factor"] })}
            {ConLossCollection({ fields: [null, "indemnity_message"], shownBy: "indemnity_message_show" })}
            {ConLossCollection({ fields: ["uw_discretion", "uw_discretion_factor"] })}
            <HX.Section title="Premium Summary" defaultCollapsed>
              {ConLossCollection({
                title: "Model",
                fields: ["technical_deductions", "technical_rate", "technical_premium"]
              })}
              {ConLossCollection({
                title: "Actual",
                fields: ["pct_of_technical", "actual_rate", "quoted_premium"]
              })}
            </HX.Section>
          </HX.Pane>
        </HX.With>
      </HX.Section>

    </HX.Page >
  );
}

export { vw_conloss };
