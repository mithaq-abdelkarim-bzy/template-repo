import * as HX from "hx-model-components";

function TransitCollection(props) {
  return <HX.Collection with="coverages/specie_transit" horizontal {...props} />;
}

function StorageCollection(props) {
  return <HX.Collection with="coverages/specie_storage" horizontal {...props} />;
}

function vw_specie(scale) {
  return (
    <HX.Page title="Specie" viewScale={scale} shownBy="cds/cover_selection/is_specie">

      <HX.Section title="Transit" defaultCollapsed>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane>
            {TransitCollection({ fields: ["transit_flag", "base_rate"] })}
            {TransitCollection({ fields: ["commodity", "commodity_factor"] })}
            {TransitCollection({ fields: ["trans_vals", "trans_vals_factor"] })}
            {TransitCollection({ fields: ["deductible_level", "deductible_level_factor"] })}
            {TransitCollection({ fields: ["excess", "excess_factor"] })}
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

      <HX.Section title="Storage" defaultCollapsed>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane>
            {StorageCollection({ fields: ["storage_flag", "base_rate"] })}
            {StorageCollection({ fields: ["commodity", "commodity_factor"] })}
            {StorageCollection({ fields: ["stock_vals", "stock_vals_factor"] })}
            {StorageCollection({ fields: ["deductible_level", "deductible_level_factor"] })}
            {StorageCollection({ fields: ["excess", "excess_factor"] })}
            {StorageCollection({ fields: ["survey", "survey_factor"] })}
            {StorageCollection({ fields: ["risk_mgmt", "risk_mgmt_factor"] })}
            {StorageCollection({ fields: ["type_of_cover", "type_of_cover_factor"] })}
            {StorageCollection({ fields: ["uw_discretion", "uw_discretion_factor"] })}
            {StorageCollection({ fields: [null, "rate"] })}
            {StorageCollection({ fields: ["avg_val_pcm", null] })}
            {StorageCollection({
              title: "CAT",
              fields: ["cat_expo", "cat_pct_of_total", "combined_cat_load", "cat_expo_tp"]
            })}
            <HX.Section title="CAT Exposure by Country" defaultCollapsed>
              <HX.Table
                data={["coverages/specie_storage/countries"]}
                fields={["country", "cat_expo", "cat_load", "pct_of_cat"]}
                dynamic
                kb-interactive
              />
            </HX.Section>
            {StorageCollection({ fields: [null, "cat_expo_check"], shownBy: "cat_expo_check_show" })}
            {StorageCollection({
              title: "Non-CAT",
              fields: ["non_cat_expo", "non_cat_pct_of_total", "non_cat_load", "non_cat_expo_tp"]
            })}
            <HX.Section title="Premium Summary" defaultCollapsed>
              {StorageCollection({
                title: "Model",
                fields: ["technical_deductions", "technical_rate", "technical_premium"]
              })}
              {StorageCollection({
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

export { vw_specie };
