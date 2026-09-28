import * as HX from "hx-model-components";

function vw_claims(scale) {
  return (
    <HX.Page title="Claims" fullWidth={false} viewScale={scale}>
      <HX.With context={{ type: "struct", path: "cds/claims" }}>
        <HX.Section title="">
          <HX.Pane flow="right">
            <HX.Collection fields={["as_at_date", "threshold", "claims_net_of_retentions"]} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table
              data={["list"]}
              fields={[
                "claimant_name",
                "claim_description",
                "date_claim_made",
                "date_claim_closed",
                "current_status",
                "paid_defense",
                "outstanding_defense",
                "paid_indemnity",
                "outstanding_indemnity",
                "attachment",
                "limit",
                "currency",
                "claim_type",
                "claim_location",
                "proc_code",
                "loss_date",
                "credit",
                "reviewed_indemnity_os",
                "comments",
                "claimant_type",
                "claimant_status",
                "cause_of_loss",
                "area_of_practice",
            ]}           
            />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page >
  );
}

export { vw_claims };
