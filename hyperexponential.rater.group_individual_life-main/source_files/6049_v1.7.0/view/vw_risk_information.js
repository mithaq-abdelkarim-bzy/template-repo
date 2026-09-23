import * as HX from "hx-model-components";


function vw_risk_information(scale, shownBy = null) {
  return (
    <HX.Page title="Risk Information" shownBy={shownBy}>
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology", "cds/rater"]} horizontal />
          {/* <HX.Collection fields={["model_state/show_after_landing_page"]} horizontal /> */}
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Account Details">
        <HX.Pane >
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["insured_name"]} with="cds/standard_fields" horizontal />
          <HX.Collection with="cds" fields={["policy_info/application_date", "standard_fields/underwriter"]} horizontal />
          <HX.Collection with="cds" fields={["currencies/source_currency", "standard_fields/is_renewal"]} horizontal />
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["/cds/standard_fields/policy_reference", "status"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Policy Information" >
        <HX.Pane shownBy="cds/is_group">
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection title="Details" fields={["written_line_input", { field: "brokerage", labelBy: "brokerage_label" }, "/cds/policy_info/direct_ri"]} horizontal />
            <HX.Collection title="Aggregate Limits" fields={["aggregate_limit", "aggregate_deductible"]} horizontal />
          </HX.With>
          <HX.Collection with="cds/policy_info" title="Profit Commission" fields={["has_profit_commission", "pc_to_gross"]} horizontal />
          <HX.Collection with="cds/policy_info" fields={["profit_commission", "pc_expenses", "pc_deficit"]} horizontal />
          <HX.Collection with="cds/policy_info" title="No Claims Bonus" fields={["has_no_claims_bonus", "ncb_pct", "ncb_to_gross"]} horizontal />
        </HX.Pane>
        <HX.Pane shownBy="cds/is_individual">
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={[{ field: "brokerage", labelBy: "brokerage_label" }, "brokerage_ri"]} horizontal />
            {/* <HX.Collection fields={["rga_load_mult", "rga_load_add"]} horizontal /> */}
          </HX.With>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Broker Details - Optional">
        <HX.Collection with="cds" fields={["standard_fields/broker", "policy_info/broker_contact"]} horizontal />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };
