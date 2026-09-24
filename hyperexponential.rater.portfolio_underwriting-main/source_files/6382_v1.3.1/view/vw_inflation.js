import * as HX from "hx-model-components";
import { YEARS_TO_CONSIDER_IN_Inflation } from "view/vw_constants";
function vw_inflation(scale) {

  const getYearsHeaders = () =>
    Array.from({ length: YEARS_TO_CONSIDER_IN_Inflation }, (_, i) => ({ field: `year_${i}`, labelBy: `non_cds/inflation/year_${i}` }));

  common_fields = [
    "selected_lob",
    "risk_code",
    "composition",
    "bp_class",
    ...getYearsHeaders()
  ]

  return (
    <HX.Page title="Inflation" fullWidth={true} viewScale={scale} shownBy="model_state/show_inflation">
      <HX.Section title="Inflation">
        <HX.Table
          title="Summary by Line of Business"
          data={["cds/inflation/summary_by_lob"]}
          fields={common_fields}
          syncColumnWidthsKey="table_1"
          kb-interactive
        />
        <HX.Table
          title="Inflation Details"
          data={["cds/inflation/details"]}
          fields={common_fields}
          syncColumnWidthsKey="table_1"
          filter={"is_row_visible"}
          maxListVisibleRows={8}
          kb-interactive
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_inflation };