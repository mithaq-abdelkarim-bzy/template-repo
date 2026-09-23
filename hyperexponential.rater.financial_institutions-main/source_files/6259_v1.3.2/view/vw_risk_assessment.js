import * as HX from "hx-model-components";

function vw_risk_assessment(scale) {
  return (
    <HX.Page title="Risk Assessment" shownBy="model_state/show_after_landing_page" viewScale={scale}>
      <HX.Section title="Underwriting considerations">
        <HX.Table data={["risk_category", "comment"]} fields={[
          { field: "policy_wording", shownBy: "/non_cds/risk_assesment/any_any" },
          { field: "claims_history_cpi", shownBy: "/non_cds/risk_assesment/any_crime_pi" },
          { field: "claims_history_do", shownBy: "/non_cds/risk_assesment/any_do" },
          { field: "risk_management", shownBy: "/non_cds/risk_assesment/any_any" },
          { field: "strength_of_financial", shownBy: "/non_cds/risk_assesment/any_any" },
          { field: "technological_infrastructure", shownBy: "/non_cds/risk_assesment/any_any" },
          { field: "quality_of_control", shownBy: "/non_cds/risk_assesment/any_crime" },
          { field: "agents_as_employees", shownBy: "/non_cds/risk_assesment/notins_crime_pi" },
          { field: "regulatory_risk", shownBy: "/non_cds/risk_assesment/any_pi_do" },
          { field: "quality_of_claims_handling", shownBy: "/non_cds/risk_assesment/ins_pi" },
          { field: "product_complexity", shownBy: "/non_cds/risk_assesment/any_pi" },
          { field: "quality_of_bcp", shownBy: "/non_cds/risk_assesment/fin_pi" },
          { field: "market_regulator", shownBy: "/non_cds/risk_assesment/ban_fin_pi" },
          { field: "extent_of_leveraged_gearing", shownBy: "/non_cds/risk_assesment/inv_pi" },
          { field: "quality_of_performance_non_pevc", shownBy: "/non_cds/risk_assesment/inv_pi" },
          { field: "redemption_gates", shownBy: "/non_cds/risk_assesment/inv_pi" },
          { field: "valuation_for_pevc", shownBy: "/non_cds/risk_assesment/inv_PE_VC_RE_pi" },
          { field: "loan_covenant", shownBy: "/non_cds/risk_assesment/inv_PE_VC_RE_pi" },
          { field: "dando_portfolio_companies", shownBy: "/non_cds/risk_assesment/inv_PE_VC_do" },
          { field: "data_centre", shownBy: "/non_cds/risk_assesment/fin_any" },
          { field: "tech_outsourcing", shownBy: "/non_cds/risk_assesment/fin_any" },
          "uw_adj.input"
        ]} with="cds/modifiers" transpose />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_risk_assessment };
