import * as HX from "hx-model-components";

function vw_cashflow() {
  return (
    <HX.Page title="PC & NCB" fullWidth>
      {/* <HX.Section><HX.Notes field="debug_str" /></HX.Section> */}
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Inputs and Model Results">
          <HX.Pane>
            <HX.Collection
              title="Profit Commission"
              fields={[
                "/cds/policy_info/has_profit_commission",
                "/cds/policy_info/profit_commission",
                "/cds/policy_info/pc_expenses",
                "/cds/policy_info/pc_deficit"
              ]}
              horizontal
            />
            <HX.Pane flow="right">
              <HX.Collection
                title="No Claims Bonus"
                fields={[
                  "/cds/policy_info/has_no_claims_bonus",
                  "/cds/policy_info/ncb_pct"
                ]}
                horizontal
              />
              <HX.Collection
                title="Model Results"
                fields={[
                  "expected_loss_cost",
                  "no_claim_prob"
                ]}
                horizontal
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>

        <HX.Section title="PC and NCB Cashflows - Model Premium">
          <HX.Pane flow="right">
            <HX.Table
              title="Profit commission calculations to hit 70% loss ratio"
              data={["pc/model/gross", "pc/model/net"]}
              fields={[
                "premium",
                "net_profits",
                "pc_cost",
                "pc_load",
              ]}
              kb-interactive
              transpose
            />
            <HX.Table
              title="NCB calculations to hit 70% loss ratio"
              data={["ncb/model/gross", "ncb/model/net"]}
              fields={[
                "premium",
                "ncb_load",
                "ncb_premium"
              ]}
              kb-interactive
              transpose
            />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="PC and NCB Cashflows - Achieved Premium">
          <HX.Pane flow="right">
            <HX.Table
              title="Profit Commission - Expected Payments"
              data={["pc/quoted/gross", "pc/quoted/net"]}
              fields={[
                "premium",
                "net_profits",
                "payment",
              ]}
              kb-interactive
              transpose
            />
            <HX.Table
              title="NCB - Expected Payments"
              data={["ncb/quoted/gross", "ncb/quoted/net"]}
              fields={[
                "premium",
                "ncb_load",
              ]}
              kb-interactive
              transpose
            />
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}


export { vw_cashflow };