import * as HX from "hx-model-components";
import EditableText from "components/text_box_editable";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Underwriter Rationale Comments">
        <EditableText textNode="cds/standard_fields/uw_rationale" />
        {/* <HX.Notes field="cds/standard_fields/uw_rationale" /> */}
      </HX.Section>
      <HX.Section title="General Comments">
        <EditableText textNode="cds/comment" />
        {/* <HX.Notes field="cds/comment" /> */}
      </HX.Section>
      <HX.Section title="Claims History Comments">
        <EditableText textNode="cds/claims_history" />                  {/* #"Claims History" */}
        {/* <HX.Notes field="cds/claims_history" title="Claims History" />
        <HX.Notes field="cds/t_and_c_comment" title="T&C's" /> */}
      </HX.Section>
      <HX.Section title="T&C's Comments">
        <EditableText textNode="cds/t_and_c_comment" />                 {/* #"T&C's" */}
      </HX.Section>
      <HX.Section title="File Uploads">
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
          <HX.Pane>
            <HX.File field="cds/file_upload_6" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/file_upload_7" />
          </HX.Pane>
          <HX.Pane>
            <HX.File field="cds/file_upload_8" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      {/* <HX.Section title="Convert Comment to Document">
        <HX.Pane flow="right">
          <HX.Collection horizontal fields={["cds/comment_tool/input_comment", null]} />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Button task="process_comment_task" title="Convert Selected Comment" />
          <HX.File field="cds/comment_tool/document" />
        </HX.Pane>
      </HX.Section> */}
    </HX.Page>
  )
}

export { vw_rationale };