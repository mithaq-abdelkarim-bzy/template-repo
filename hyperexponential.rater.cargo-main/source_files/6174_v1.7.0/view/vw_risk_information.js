import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information">
      <HX.Section title="Fetch Expiring Policy" shownBy="cds/standard_fields/is_renewal">
        <HX.Pane flow="right" >
          <HX.Collection fields={["cds/rate_change/expiring_policy_option_id"]} />
          <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Account Details">
        <HX.Pane >
          {/* <HX.Collection fields={["database_id", "application_date"]} with="cds" horizontal /> */}
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["cds/standard_fields/underwriter", "cds/term"]} horizontal />
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          <HX.Collection fields={["cds/standard_fields/policy_reference", "cds/currencies/source_currency", "cds/standard_fields/is_renewal"]} horizontal />
        </HX.Pane>
      </HX.Section>
      {/* <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section> */}
      <HX.Section title="Coverage Selection">
        <HX.Collection with="cds/cover_selection" fields={["select_message", "cover", { "field": "is_cargo_cyber", shownBy: "show_cargo_cyber" }]} horizontal />
      </HX.Section>
      <HX.Section title="Policy Information">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Collection fields={["has_double_section_ref"]} horizontal />
            <HX.Pane />
          </HX.Pane>
          <HX.Table
            data={["eea_section_reference", "non_eea_section_reference", "coverages/cargo_cyber_addon/eea_section_reference", "coverages/cargo_cyber_addon/non_eea_section_reference"]}
            fields={["ref", "type"]}
            shownBy="has_double_section_ref"
            // filter={["/cds/layer[0]/eea_section_reference/is_shown", "/cds/layer[0]/non_eea_section_reference/is_shown", "/cds/layer[0]/eea_section_reference_cargo_cyber/is_shown", "/cds/layer[0]/non_eea_section_reference_cargo_cyber/is_shown"]}
            filter={["/cds/main_polref_is_shown", "/cds/main_polref_is_shown", "/cds/cargo_cyber_is_shown", "/cds/cargo_cyber_is_shown"]}
          />
          <HX.Table
            data={["single_section_reference", "coverages/cargo_cyber_addon/single_section_reference"]}
            fields={["ref", "type"]}
            shownBy="has_single_section_ref"
            filter={["/cds/main_polref_is_shown", "/cds/cargo_cyber_is_shown"]}
          // filter={["/single_section_reference/is_shown", "/single_section_reference_cargo_cyber/is_shown"]}
          />
          <HX.Collection fields={["status", "brokerage", "written_line"]} horizontal />
          <HX.Pane flow="right" ratio={3}>
            <HX.Button task="pass_pas_reference" title="Pass Policy Reference to PAS" />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
        </HX.With>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };
