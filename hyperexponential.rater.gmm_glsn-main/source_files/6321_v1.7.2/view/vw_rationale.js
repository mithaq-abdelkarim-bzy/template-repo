import * as HX from "hx-model-components";
import ExpandableEditableText from "components/ExpandableEditableText";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale}>
      <HX.Section title="Underwriter Notes">
        {/* <HX.Notes
          field="cds/uw_notes"
        // title="Current Year"
        /> */}
        <ExpandableEditableText
          textNode="cds/uw_notes"
          label="Current Year Notes"
        />
        {/* <HX.Button task="clear_uw_rationale_task" title="Clear UW Notes" /> */}
      </HX.Section>

      <HX.Section title="Mid Term Adjustments">
        {/* <HX.Notes field="cds/mid_term_adjustments" /> */}
        <ExpandableEditableText
          textNode="cds/mid_term_adjustments"
          label="Mid Term Adjustments"
        />
      </HX.Section>

      <HX.Section title="Historical Comments">
        {/* <HX.Notes field="cds/historical_comments" /> */}
        <ExpandableEditableText
          textNode="cds/historical_comments"
          label="Historical Comments"
        />
      </HX.Section>

      <HX.Section title="Additional Information - File Uploads">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.File field="cds/file_upload_1" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/file_upload_2" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/file_upload_3" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/file_upload_4" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/file_upload_5" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Generate Email Rationale">
        {/* <HX.Collection with="cds/email" fields={["sender", "recipient"]} horizontal /> */}
        <HX.Pane flow="right">
          <HX.Button task="generate_email_task" title="Generate Rationale Email" />
          <HX.File field="cds/email/rationale_file" />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Button task="generate_referral_email_task" title="Generate Referral Email" />
          <HX.File field="cds/email/referral_file" />
        </HX.Pane>

      </HX.Section>
      <HX.Section title="Generate Email Proposal">
        <HX.Pane flow="right">
          <HX.Button task="generate_primary_proposal_template_task" title="Generate Primary Proposal Template" />
          <HX.File field="cds/primary_proposal_template_file" />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Button task="generate_excess_proposal_template_task" title="Generate Excess Proposal Template" />
          <HX.File field="cds/excess_proposal_template_file" />
        </HX.Pane>

      </HX.Section>

    </HX.Page>
  )
}

export { vw_rationale };