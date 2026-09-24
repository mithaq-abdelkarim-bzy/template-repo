import * as HX from "hx-model-components";
import EditableText from "components/text_box_editable";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Underwriter Rationale">
        {/* <HX.Pane flow="right">
          <HX.Button task="rationale_word_documents_task" title="Generate Coverage Options" />
          <HX.File field="/cds/rationale_document" />
        </HX.Pane> */}

        <EditableText textNode="cds/standard_fields/uw_rationale" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rationale };