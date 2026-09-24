import * as HX from "hx-model-components";

function vw_risk_code_library(scale) {
  return (
    <HX.Page title="Risk Code Library" fullWidth={true} viewScale={scale} shownBy="model_state/show_risk_code_library">
      <HX.Section title="Active Risk Codes: Mappings and Full Descriptions">

        <HX.Pane flow="right">
          <HX.Collection fields={["cds/year_start", "cds/year_end", "cds/risk_code_description_expanded", null, null, null]} horizontal={true} />
        </HX.Pane>

        <HX.Table
          kb-interactive
          dynamic
          maxListVisibleRows={28}
          data={["cds/risk_code_library"]}
          fields={[
            "risk_code",
            "high_level_cob",
            "generic_cob",
            //"type_of_placement", 
            "risk_code_description",
            { field: "risk_code_explained", shownBy: "cds/risk_code_description_expanded" },
            "oecd_class_mapping",
            "assigned_tracker",
            "assigned_bp_class",
            "do_we_model",
            "gnpi_lloyds",
            "incured_lloyds",
            "gn_ilr_lloyds",
            "gnpi_beazley",
            "incurred_beazley",
            "gn_ilr_beazley"]}
        />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_code_library };