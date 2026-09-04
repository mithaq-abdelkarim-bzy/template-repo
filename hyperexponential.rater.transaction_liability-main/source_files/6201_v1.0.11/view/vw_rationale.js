import * as HX from "hx-model-components";
import EditableText from "components/text_box_editable";
import ExpandableEditableText from "components/text_box_expandable";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Transaction Description and Summary of Target">
        <ExpandableEditableText textNode="cds/rationale/transaction_description" />
      </HX.Section>
      <HX.Section title="Knowledge of the Insured - List of DD Reports">
        <ExpandableEditableText textNode="cds/rationale/knowledge_of_insured" />
      </HX.Section>
      <HX.Section title="Reasons for writing the Risk">
        <ExpandableEditableText textNode="cds/rationale/reasons_for_writing_risk" />
      </HX.Section>
      <HX.Section title="Unusual Or Complex Aspects of the Risk">
        <ExpandableEditableText textNode="cds/rationale/complex_considerations" />
      </HX.Section>
      <HX.Section title="Exclusions and Carve Outs">
        <ExpandableEditableText textNode="cds/rationale/exclusions_and_carve_outs" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rationale };