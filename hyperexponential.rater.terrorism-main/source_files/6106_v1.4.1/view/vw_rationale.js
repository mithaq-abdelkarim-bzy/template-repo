import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale}
    // shownBy="cds/show_hide/page/show_rationale"
    >
      <HX.Section title="Underwriter Rationale">
        <HX.Notes field="cds/standard_fields/uw_rationale" />
      </HX.Section>

      <HX.Section title="Actuarial Commentary" defaultCollapsed={true}>
        <HX.Collection fields={["cds/rationale/actuarial_review"]} />
        <HX.Notes field="cds/rationale/actuarial_notes" />
      </HX.Section>

      <HX.Section title="Policy Document" >
        <HX.Button task="task_policy_to_excel" title="Generate Policy Document" shownBy="policy_doc/show_generate_button" />
        <HX.Notes field="policy_doc/premium_check" shownBy="policy_doc/show_premium_check" />
        <HX.File
          with="policy_doc"
          field="output_file"
          title="Click on the icon below to download the policy document"
          shownBy="show_download" />
      </HX.Section>

      <HX.Section title="Useful Information">
        <HX.Pane flow="right">
          <HX.Notes field="cds/rationale/help_file" />
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_rationale };