import * as HX from "hx-model-components";

function vw_excel_export(scale) {
  return (
    <HX.Page title="Excel Export" shownBy="model_state/show_after_landing_page" viewScale={scale}>
      <HX.Section title="Excel Export">
        <HX.Notes field="excel_export_notes" />
        <HX.Button task="export_to_excel" title="Export to Excel" />
        <HX.File field="output_file" title="Output File" stretch />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_excel_export };