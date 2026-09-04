import * as HX from "hx-model-components";

function vw_claims(scale) {
  return (
    <HX.Page title="BI Data" fullWidth={true} viewScale={scale} shownBy="flags/show_bi_claims">
      <HX.Section title="Policy Data">
        <HX.Pane>
          <HX.Table data={["cds/experience_rating/bi_policy_data"]}
            fields={[
              "PolicyReference",
              "SectionReference",
              "TriFocusName",
              "ClassOfBusinessCode",
              "StatsCode",
              "YOA",
              "SettlementCurrency",
              "ExternalAcquisitionCostMultiplier",
              "WrittenOrEstimatedPremium",
              "RateChangeDivisor",
              "BenchmarkPremium",
              "TotalWrittenIfNotSignedMultiplier",
            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Claim Data">
        <HX.Pane>
          <HX.Table data={["cds/experience_rating/bi_claim_data"]}
            fields={[
              "PolicyReference",
              "SectionReference",
              "TriFocusName",
              "YOA",
              "ClaimReference",
              "MarketCatCode",
              "BeazleyShareTotalPaidInUSD",
              "BeazleyShareTotalOutstandingInUSD",
              "BeazleyShareTotalIncurredInUSD",
              "SettlementCurrency",
              "SlipOrderTotalIncurred",
              "SignedLineMultiplier"
            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_claims };

