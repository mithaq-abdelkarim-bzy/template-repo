import * as HX from "hx-model-components";

function vw_claims(scale) {
  return (
    <HX.Page title="Claims" fullWidth={true} viewScale={scale}>
      <HX.Section title="Instructions" defaultCollapsed={false}>
        <HX.Notes field="cds/experience_rating/claims_instructions" />
      </HX.Section>
      <HX.Section title="Settings" defaultCollapsed={false}>
        <HX.Collection horizontal fields={[
          "cds/experience_rating/claims_asatdate", "cds/experience_rating/claims_policy_year", null, null, null
        ]}
        />
      </HX.Section>
      <HX.Section title="Claims Table" defaultCollapsed={false}>
        <HX.Table
          data={[
            {
              datum: "experience_rating/claims"
            }
          ]}
          fields={[
            { field: "claim_name", width: 220 },
            { field: "claim_made_date", width: 170 },
            { field: "claim_close_date", width: 170 },
            { field: "claim_status", width: 170 },
            { field: "defense_fgu_paid", width: 200 },
            { field: "defense_fgu_os", width: 200 },
            { field: "indemnity_fgu_paid", width: 200 },
            { field: "indemnity_fgu_os", width: 200 },
            { field: "currency", width: 150 },
            { field: "to_use", width: 100 },
            null,
            { field: "claim_made_year", width: 170 },
            { field: "defense_incurred", width: 170 },
            { field: "indemnity_incurred", width: 170 },
            { field: "claims_fx_rate", width: 120 },
            { field: "policy_year_estimated", width: 170 },
            { field: "defense_incurred_usd", width: 170 },
            { field: "indemnity_incurred_usd", width: 170 },
            { field: "incurred_total_usd", width: 170 },
            { field: "incurred_total_usd_inflated", width: 170 },
            { field: "paid_total_usd_inflated", width: 170 },
            { field: "total_usd_inflated", width: 170, infoBy: "hover_info/total_usd_inflated" },
          ]}
          rowHeaderSettings={{ width: 50 }}
          with="cds"
          dynamic
          kb-interactive
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_claims }