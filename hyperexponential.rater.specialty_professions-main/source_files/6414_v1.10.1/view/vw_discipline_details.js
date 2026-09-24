import * as HX from "hx-model-components";

function vw_discipline_details(scale) {
  return (
    <HX.Page title="Discipline Details" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Engineering Disciplines">
        <HX.Pane flow="right">
          <HX.Notes field="cds/currency_label" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Notes field="cds/exposure/granular/engineering/considerations" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Table kb-interactive
            fields={[
              { field: "other_specify", width: 200 },
              { field: "percentage", shownBy: "/noncds/validation/engineering_disp_percentage/valid", width: 125 },
              { field: "percentage.notSupported", shownBy: "/noncds/validation/engineering_disp_percentage/invalid", infoBy: "/noncds/validation/engineering_disp_percentage/info_text", width: 125 },
              { field: "rateable_exposure", width: 175 },
              { field: "default_base_rate", width: 200 },
              { field: "base_rate_override", width: 175 },
              { field: "base_premium", width: 200 },
              { field: "guidelines", width: 400 }
            ]}
            data={[
              "aerospace",
              "architect_comm",
              "architect_resi",
              "aviation",
              "chemical",
              "civil",
              "civil_bridges_roads",
              "cm_atrisk",
              "cm_agency",
              "drafting",
              "electrical",
              "enviro_cons",
              "enviro_labs",
              "fp",
              "forensic",
              "geotechnical",
              "hvac",
              "int_design",
              "landscape",
              "leed_cons",
              "mech",
              "mech_electrical",
              "mining",
              "non_destructive_testing",
              "nuclear",
              "oil_gas",
              "process",
              "struct_resi_inst",
              "struct_steel_stairs",
              "struct_non_resi_inst",
              "surveyor",
              "surveyor_resi",
              "other_one",
              "other_two",
              "other_three",
              "other_four",
              "other_five",
              "total"
            ]}
            with="cds/exposure/granular/engineering"
          />
          <HX.Collection
            fields={["size_discount", null, null, null, null, null]}
            with="cds/exposure/aggregate"
            syncColumnWidthsKey="Collections_width1"
            numCols={6} />
          <HX.Collection
            fields={["base_premium_size_discount"]}
            with="cds/exposure/granular/engineering/total"
            syncColumnWidthsKey="Collections_width1" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Contractor Disciplines">
        <HX.Pane flow="right">
          <HX.Notes field="cds/currency_label" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Notes field="cds/exposure/granular/contractor/considerations" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Table kb-interactive
            fields={[
              { field: "other_specify", width: 200 },
              { field: "percentage", shownBy: "/noncds/validation/contractor_disp_percentage/valid", width: 125 },
              { field: "percentage.notSupported", shownBy: "/noncds/validation/contractor_disp_percentage/invalid", infoBy: "/noncds/validation/contractor_disp_percentage/info_text", width: 125 },
              { field: "rateable_exposure", width: 175 },
              { field: "default_base_rate", width: 200 },
              { field: "base_rate_override", width: 175 },
              { field: "base_premium", width: 200 },
              { field: "guidelines", width: 400 }
            ]}
            data={[
              "asbestos_lead",
              "build_envelop",
              "carpenter",
              "concrete",
              "demolition",
              "drywall",
              "electrical",
              "enviro",
              "fp_dry",
              "fp_wet",
              "foundation_excav",
              "general_comm",
              "general_resi",
              "glazing",
              "hvac_industrial",
              "hvac_non_industrial",
              "landscape",
              "masonry",
              "mech",
              "reno_non_resi",
              "oil_gas",
              "painting",
              "plumbing",
              "resi_reno",
              "roofing",
              "steel",
              "telecom_heavy",
              "telecom_light",
              "utilities",
              "other_one",
              "other_two",
              "other_three",
              "other_four",
              "other_five",
              "total"
            ]}
            with="cds/exposure/granular/contractor"
          />
          <HX.Collection
            fields={["size_discount", null, null, null, null, null]}
            with="cds/exposure/aggregate"
            syncColumnWidthsKey="Collections_width1"
            numCols={6} />
          <HX.Collection
            fields={["base_premium_size_discount"]}
            with="cds/exposure/granular/contractor/total"
            syncColumnWidthsKey="Collections_width1" />
        </HX.Pane>
      </HX.Section>

    </HX.Page >
  )
}

export { vw_discipline_details };

