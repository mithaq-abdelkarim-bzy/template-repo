import * as HX from "hx-model-components";
import { YEARS_TO_CONSIDER_IN_PORTFOLIO_PROFILE } from "./vw_constants"

function generateYearColumns(prefix, years = YEARS_TO_CONSIDER_IN_PORTFOLIO_PROFILE) {
  return Array.from({ length: years }, (_, i) => ({
    field: `${prefix}/year_${i}`,
    labelBy: `non_cds/portfolio_profile/${prefix}/year_${i}`
  }));
}

const generateCommonFields = [
  'selected_lob',
  'bp_class',
  'risk_code',
  'selected_premium',
  'weighting',
  null,
  ...generateYearColumns('rate_change_with_selection_override'),
  null,
  ...generateYearColumns('rate_change_no_override'),
  null,
  ...generateYearColumns('lloyds_incurred_development'),
  null,
  ...generateYearColumns('lloyds_paid_development'),
  null,
  ...generateYearColumns('lloyds_premium_development'),
  null,
  'lloyds_risk_code_results/final_gn_ulr',
  'lloyds_risk_code_results/selected_ielr',
  'lloyds_risk_code_results/model_ielr',
  null,
  'beazley_risk_code_results/final_gn_ulr',
]


function vw_portfolio_profile(scale) {
  return (
    <HX.Page title="Portfolio Profile" fullWidth={true} viewScale={scale} shownBy="model_state/show_portfolio_profile">
      <HX.Section title="Summary By Lob" collapsible={false}>
        <HX.Table
          kb-interactive
          data={["cds/portfolio_profile/summary_by_lob"]}
          fields={generateCommonFields}
          freezeLeft={1}
        />
      </HX.Section>
      <HX.Section title="All combinations of Selected Lob x Risk Code" collapsible={false}>
        <HX.Table
          kb-interactive
          data={["cds/portfolio_profile/selected_lob_and_risk_code_combination"]}
          fields={generateCommonFields}
          freezeLeft={1}
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_portfolio_profile };