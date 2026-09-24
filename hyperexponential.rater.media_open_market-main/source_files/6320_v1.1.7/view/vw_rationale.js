import * as HX from "hx-model-components";
import ExpandableEditableText from "components/ExpandableEditableText";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Underwriter Rationale">
        {/* <HX.Notes field="cds/standard_fields/uw_rationale" /> */}
        <ExpandableEditableText
          textNode="cds/standard_fields/uw_rationale"
          label="Click to view/edit Rationale"
        />
      </HX.Section>
      <HX.Section title="Policy Document" >
        <HX.Button task="policy_to_excel_task" title="Generate Policy Document" shownBy="policy_doc/show_generate_button" />
        <HX.Notes field="policy_doc/premium_check" shownBy="policy_doc/show_premium_check" />
        <HX.File
          with="policy_doc"
          field="output_file"
          title="Click on the icon below to download the policy document"
          shownBy="show_download" />

        <HX.Button task="generate_email_task" title="Generate Rationale Email" shownBy="policy_doc/show_generate_button" />
        <HX.File field="cds/email/rationale_file"
          title="Click on the icon below to download the policy email document"
          shownBy="cds/email/show_download"
        />

      </HX.Section>
    </HX.Page>
  )
}

export { vw_rationale };