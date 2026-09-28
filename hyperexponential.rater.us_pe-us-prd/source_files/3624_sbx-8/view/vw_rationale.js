import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale}>
      <HX.With context={{ type: "struct", path: "cds/rationale" }}>
        <HX.Section title="KNOWLEDGE OF INSURED">
          <HX.Notes field="knowledge_of_insured" />
        </HX.Section>
        <HX.Section title="PORTFOLIO FIT">
          <HX.Notes field="portfolio_fit" />
        </HX.Section>
        <HX.Section title="BASIS OF RISK SELECTION">
          <HX.Notes field="basis_of_risk_selection" />
        </HX.Section>
        <HX.Section title="UNUSUAL OR COMPLEX OPERATIONS">
          <HX.Notes field="unusual_or_complex_operations" />
        </HX.Section>
        <HX.Section title="FACTS AFFECTING DECISION">
          <HX.Notes field="facts_affecting_decision" />
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_rationale };