import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="model_state/show_rationale">
      <HX.With context={{ type: "struct", path: "cds/rationale" }}>

        <HX.Section title="Underwriter Rationale">
          <HX.Section title="Exporting Analysis">
            {/* <HX.Pane flow="right">
            <HX.Button task="generate_word_document_task" title="Generate Word Document" />
            <HX.File field="word_rationale_template" />
          </HX.Pane> */}
            <HX.Pane flow="down">
              <HX.Pane flow="right">
                <HX.Collection fields={["/non_cds/excel_analysis/projection_complete"]} />
              </HX.Pane>
              <HX.Pane flow="right" shownBy="/non_cds/excel_analysis/projection_complete">
                <HX.Button task="generate_excel_document_task" title="Generate Excel Document" />
                <HX.File field="/non_cds/excel_analysis/output_file" shownBy="/non_cds/excel_analysis/show_download" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>

          <HX.Section title="Key information about account">
            <HX.Notes field="key_information" />
          </HX.Section>
          <HX.Section title="Rationale behind assumption selection">
            <HX.Notes field="rationale_assumptions" />
          </HX.Section>
          <HX.Section title="Rationale behind methodology selection and overrides">
            <HX.Notes field="rationale_methodology" />
          </HX.Section>
          <HX.Section title="Key uncertainties">
            <HX.Notes field="key_uncertainties" />
          </HX.Section>
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_rationale };