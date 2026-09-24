import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title=" ">
        <HX.Collection
          numCols={3}
          fields={[
            "cds/standard_fields/insured_name.read_only_option"
          ]}
        />
      </HX.Section>
      <HX.Section title="Underwriter Rationale">
        <HX.Notes field="cds/rationale/knowledge_comments" title="Knowledge of the reinsured" />
        <HX.Notes field="cds/rationale/portfolio_comments" title="Portfolio fit" />
        <HX.Notes field="cds/rationale/basis_comments" title="Basis of risk selection" />
        <HX.Notes field="cds/rationale/unusual_comments" title="Any unusual or complex considerations" />
        <HX.Notes field="cds/rationale/facts_comments" title="Facts which affect the underwriter's decision" />
      </HX.Section>
      {/*<HX.Section title="Policy Document" >
        <HX.Button task="policy_to_excel_task" title="Generate Policy Document" shownBy="policy_doc/show_generate_button" />
        <HX.Notes field="policy_doc/premium_check" shownBy="policy_doc/show_premium_check" />
        <HX.File
          with="policy_doc"
          field="output_file"
          title="Click on the icon below to download the policy document"
          shownBy="show_download" />
      </HX.Section>
      */}
    </HX.Page>
  )
}

export { vw_rationale };