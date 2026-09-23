import * as HX from "hx-model-components";

function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page" viewScale={scale}>
      <HX.Section title="Account Details">
        <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
        <HX.Collection fields={["standard_fields/underwriter", null]} with="cds" horizontal />
        <HX.Collection fields={["standard_fields/insured_name"]} with="cds" />
        <HX.Collection fields={["risk_info/currency", "standard_fields/is_renewal"]} with="cds" horizontal />
        <HX.Pane flow="right">
          <HX.Collection fields={["risk_info/quote_details_search"]} with="cds" />
          <HX.Button task="save_quote_details_to_pas_reference" title="Save Quote Details to PAS Reference" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Broker Details">
        <HX.Collection fields={["standard_fields/broker", "risk_info/broker_contact"]} with="cds" horizontal />
      </HX.Section>
      <HX.Section title="Industry Details">
        <HX.Collection fields={["rating_factors/risk_info/region", "standard_fields/insured_country"]} with="cds" horizontal />
        <HX.Collection fields={["key_industry/code_name", "rating_factors/risk_info/sub_industry"]} with="cds" horizontal />
        <HX.Pane flow="right">
          <HX.Collection fields={["ownership_type"]} with="cds/rating_factors/risk_info" />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Cover Required">
        <HX.Collection fields={["crime_coverage_required", "pi_coverage_required", "do_coverage_required"]} with="cds/rating_factors/risk_info" horizontal />
      </HX.Section>
      <HX.Section title="Other Information">
        <HX.Pane>
          <HX.Collection fields={["platform", "eea_non_eea_indicator"]} with="cds/risk_info" horizontal />
          <HX.Collection fields={["direct_ri", "cedant_name"]} with="cds/risk_info" horizontal />
        </HX.Pane>
        <HX.Pane flow='right'>
          <HX.Button task="generate_tags" title="Create Policy Tags" />
          <HX.Collection fields={["policy_tag_msg"]} with="cds" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Comments">
        <HX.Notes field="comments" with="cds/risk_info" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_risk_information };