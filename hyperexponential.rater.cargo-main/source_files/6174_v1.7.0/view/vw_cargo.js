import * as HX from "hx-model-components";

function TransitCollection(props) {
  return <HX.Collection with="coverages/cargo_transit" horizontal {...props} />;
}

function StorageCollection(props) {
  return <HX.Collection with="coverages/cargo_storage" horizontal {...props} />;
}

function vw_cargo(scale) {
  return (
    <HX.Page title="Cargo" viewScale={scale} shownBy="cds/cover_selection/is_cargo">

      <HX.Section title="Cargo - Transit" defaultCollapsed>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane>
            {TransitCollection({ fields: ["transit_flag", "base_rate"] })}
            {TransitCollection({ fields: ["wh_to_port_flag", "loading_flag", "voyage_flag", "unloading_flag", "port_to_wh_flag"] })}
            {TransitCollection({ fields: ["commodity", "commodity_factor"] })}
            {TransitCollection({ fields: ["trans_vals", "trans_vals_factor"] })}
            {TransitCollection({ fields: ["deductible_level", "deductible_level_factor"] })}
            {TransitCollection({ fields: ["excess", "excess_factor"] })}
            {TransitCollection({ fields: ["packaging", "packaging_factor"] })}
            <HX.Section title="Cargo - Conveyance" collapsible={false}>
              <HX.Pane flow="right">
                <HX.Collection with="coverages/cargo_transit" fields={["conv_air", "conv_land", "conv_sea"]} />
                <HX.Collection with="coverages/cargo_transit" fields={["conv_air_factor", "conv_land_factor", "conv_sea_factor", "conv_factor"]} />
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

      <HX.Section title="Cargo - Storage" defaultCollapsed>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane>
            {StorageCollection({ fields: ["storage_flag", "base_rate"] })}
            {StorageCollection({ fields: ["stock_vals", null] })}
            {StorageCollection({ fields: ["deductible_level", "deductible_level_factor"] })}
            {StorageCollection({ fields: ["excess", "excess_factor"] })}
            {StorageCollection({ fields: ["survey", "survey_factor"] })}
            {StorageCollection({ fields: ["risk_mgmt", "risk_mgmt_factor"] })}
            {StorageCollection({ fields: ["type_of_cover", "type_of_cover_factor"] })}
            {StorageCollection({ fields: ["uw_discretion", "uw_discretion_factor"] })}
            {StorageCollection({ fields: [null, "rate"] })}
            {StorageCollection({ fields: ["avg_val_pcm", null] })}
            {StorageCollection({
              title: "Cargo - CAT",
              fields: ["cat_expo", "cat_pct_of_total", "combined_cat_load", "cat_expo_tp"]
            })}
            <HX.Section title="CAT Exposure by Country" defaultCollapsed>
              <HX.Table
                data={["coverages/cargo_storage/countries"]}
                fields={["country", "cat_expo", "cat_load", "pct_of_cat"]}
                dynamic
                kb-interactive
              />
            </HX.Section>
            {StorageCollection({ fields: [null, "cat_expo_check"], shownBy: "cat_expo_check_show" })}
            {StorageCollection({
              title: "Retail",
              fields: ["retail_expo", "retail_pct_of_total", "retail_load", "retail_expo_tp"]
            })}
            {StorageCollection({
              title: "Everything Else",
              fields: ["all_else_expo", "all_else_pct_of_total", "all_else_load", "all_else_expo_tp"]
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

// function vw_cargo_2(scale) {

//   return (
//     <HX.Page title="Cargo" viewScale={scale} fullWidth>
//       <HX.Section title="Cargo">
//         <HX.Selector data={["cds/layers"]} dropdown="name">

//           <HX.Pane flow="right">
//             {CargoCollection({ fields: ["transit_flag"] })}
//             {CargoCollection({ fields: ["storage_flag"] })}
//           </HX.Pane>

//           <HX.Pane flow="right">
//             {/* Transit */}
//             <HX.Pane shownBy="coverages/cargo/transit_flag">
//               {CargoCollection({ fields: ["to_port", "load", "voyage", "unload", "to_warehouse"] })}
//               {CargoCollection({ fields: ["commodity", "commodity_factor"] })}
//               {CargoCollection({ fields: ["trans_val", "trans_val_factor"] })}
//               {CargoCollection({ fields: ["deductible_level", "deductible_level_factor"] })}
//             </HX.Pane>
//             <HX.Pane shownBy="coverages/cargo/transit_flag_opposite" />
//             {/* Storage */}
//             <HX.Pane shownBy="coverages/cargo/storage_flag">
//               {CargoCollection({ fields: ["commodity", "commodity_factor"] })}
//               {CargoCollection({ fields: ["trans_val", "trans_val_factor"] })}
//               {CargoCollection({ fields: ["deductible_level", "deductible_level_factor"] })}
//             </HX.Pane>
//             <HX.Pane shownBy="coverages/cargo/storage_flag_opposite" />
//           </HX.Pane>

//         </HX.Selector>
//       </HX.Section>

//     </HX.Page>
//   );
// }

export { vw_cargo };
