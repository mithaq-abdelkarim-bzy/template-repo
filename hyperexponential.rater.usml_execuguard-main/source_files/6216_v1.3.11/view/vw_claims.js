import * as HX from "hx-model-components";

function vw_claims(scale) {
  return (
    <HX.Page title="Claims" fullWidth={true} viewScale={scale}>
      <HX.Section title="US ML Rater - Claims">
        <HX.Collection fields={[
          "as_at_date",
          "threshold",
          "claims_net_ret",
        ]} with="cds"
        />
      </HX.Section>
      <HX.Section>
        <HX.Pane>
          <HX.Table
            data={["claims"]}
            fields={["claimant_name", "claim_description", "date_claim_made", "date_claim_closed", "current_status", "paid_defense", "out_defense", "paid_indemnity", "out_indemnity", "attachment", "limit", "currency_claims", "claim_type", "claim_location", "area_of_practice"]}
            title=""
            with="cds"
          />
          <HX.Table
            data={["claims"]}
            fields={["year", "inc_claims_unr", "pd_claims_unr", "inc_claims_rev", "pd_claims_rev"]}
            title=""
            with="cds"
          />
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_claims };