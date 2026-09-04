import * as HX from "hx-model-components";
import EditableText from "components/text_box_editable";
import ExpandableEditableText from "components/text_box_expandable";

// const layer_function()=>{
//   for abc in 
// }

function vw_eso(scale) {
  return (
    <HX.Page title="ESO" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.With context={{ type: "struct", path: "cds/eso" }}>
        <HX.Section title="">
          <HX.Collection horizontal
            fields={["/cds/standard_fields/underwriter.read_only", "/cds/currencies/source_currency.read_only"]} />
          <HX.Table
            data={[
              { datum: "coverage", labelBy: "coverage/label" },
              { datum: "include_option", labelBy: "include_option/label" }
            ]}
            fields={
              [
                { field: "option_0", shownBy: "show_hide/option_0" },
                { field: "option_1", shownBy: "show_hide/option_1" },
                { field: "option_2", shownBy: "show_hide/option_2" },
                { field: "option_3", shownBy: "show_hide/option_3" },
                { field: "option_4", shownBy: "show_hide/option_4" },
                { field: "option_5", shownBy: "show_hide/option_5" },
                { field: "option_6", shownBy: "show_hide/option_6" },
                { field: "option_7", shownBy: "show_hide/option_7" },
                { field: "option_8", shownBy: "show_hide/option_8" },
                { field: "option_9", shownBy: "show_hide/option_9" }
              ]}
            with="options"
            transpose
          />
        </HX.Section>
        <HX.Section title="">
          <HX.Pane flow="right">
            <HX.Notes field="section_references" title="Selected Policy References" />
            <HX.Collection horizontal
              fields={["bind_date"]} />
          </HX.Pane>
          <HX.Table
            data={[{ datum: "/cds/eso", labelBy: "/cds/eso/label" }]}
            fields={["premium_total", "limit_total", "term", "over_lining", "cob"]}
            transpose
            kb-interactive
          />
          <ExpandableEditableText
            textNode="additional_term_info"
            label="Additional Term details if needed"
          />

        </HX.Section>
        <HX.Section title="Amount Authorising/Further Comments" >
          <HX.Pane>
            <EditableText textNode="authorising_comments" />
            <HX.Notes field="authorising_comments_info" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Sign Off" >
          <HX.Pane>
            <HX.Collection title="Exception (Include all elements over authority)" horizontal
              fields={["approving_uw", "authorisation_date"]} />
            <HX.Notes field="info" />
          </HX.Pane>
        </HX.Section>

        {/* <HX.Section>
          <HX.Button task="generate_eso_doc_task" title="Generate ESO Document" />
          <HX.File field="document" />
        </HX.Section> */}

      </HX.With>


    </HX.Page>
  )
}


export { vw_eso };