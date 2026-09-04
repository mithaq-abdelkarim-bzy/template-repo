import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="cds/model_state/show_after_landing_page">

      <HX.Section title="Underwriter Rationale">
        <HX.Notes field="cds/standard_fields/uw_rationale" />
      </HX.Section>


      <HX.Section title="UW Summary Document">
        <HX.Pane flow="right">
          <HX.Button task="generate_uw_doc_task" title="Generate Document" />
          <HX.File field="uw_doc_template" />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Actuarial Commentary" defaultCollapsed={true}>
        <HX.Collection fields={["cds/rationale/actuarial_review"]} />
        <HX.Notes field="cds/rationale/actuarial_notes" />
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