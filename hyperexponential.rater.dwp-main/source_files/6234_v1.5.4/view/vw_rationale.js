import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="cds/uw_rationale/is_rationale_required">
      <HX.Section title="Underwriter Rationale">
        <HX.Notes field="cds/uw_rationale/knowledge_of_insured" title="Knowledge of the Insured" />
        <HX.Notes field="cds/uw_rationale/portfolio_fit" title="Portfolio Fit" />
        <HX.Notes field="cds/uw_rationale/basis_of_risk_selection" title="Basis of Risk Selection" />
        <HX.Notes field="cds/uw_rationale/complex_considerations" title="Any Unusual or Complex Considerations" />
        <HX.Notes field="cds/uw_rationale/facts_affecting_decision" title="Any facts which affect Underwriter's decision?" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rationale };

