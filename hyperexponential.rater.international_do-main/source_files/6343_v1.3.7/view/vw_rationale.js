import * as HX from "hx-model-components";
import EditableText from "components/text_box_editable";
import ExpandableEditableText from "components/text_box_expandable";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale}>
      <HX.Section title="1. Summary  of Programme Discussion with Broker" shownBy="cds/risk_information/not_mmp_flag">
        <ExpandableEditableText textNode="cds/uw_rationale/broker_discussion" />
      </HX.Section>

      <HX.Section title="2. Wording and any Unusual Coverage" shownBy="cds/risk_information/not_mmp_flag">
        <ExpandableEditableText textNode="cds/uw_rationale/unusual_coverage" />
      </HX.Section>

      <HX.Section title="3. Any Other Factors not Captured Elsewhere" shownBy="cds/risk_information/not_mmp_flag">
        <ExpandableEditableText textNode="cds/uw_rationale/other_factors" />
      </HX.Section>

      <HX.Section title="4. ESG">
        <HX.Notes field="cds/uw_rationale/esg_info" />
        <ExpandableEditableText textNode="cds/uw_rationale/esg" />
      </HX.Section>

      <HX.Section title="5. I am Writing this Because (including comments on BPI)" >
        < HX.Notes field="cds/uw_rationale/bpi_comment_info" />
        <ExpandableEditableText textNode="cds/uw_rationale/bpi_comment" />
      </HX.Section>

      <HX.Section title="File Uploads">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.File field="cds/uw_rationale/file_upload_1" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/uw_rationale/file_upload_2" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/uw_rationale/file_upload_3" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/uw_rationale/file_upload_4" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/uw_rationale/file_upload_5" />
          </HX.Pane>
          {/* <HX.Pane>
            <HX.File field="cds/uw_rationale/file_upload_6" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/uw_rationale/file_upload_7" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/uw_rationale/file_upload_8" />
          </HX.Pane> */}
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Download Rationale">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Button task="generate_uw_rationale_doc_task" title="Generate UW Rationale Document" />
            <HX.File field="cds/uw_rationale/file_download_1" />
          </HX.Pane>
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rationale };