import * as HX from "hx-model-components";


function vw_risk_information(shownBy = null) {
  return (
    <HX.Page title="Risk Information" shownBy={shownBy}>
      <HX.Section title="Rating Model">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology", "cds/rater"]} horizontal />
          {/* <HX.Collection fields={["model_state/show_after_landing_page"]} horizontal /> */}
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Account Details">
        <HX.Pane >
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          {/* <HX.Collection fields={["cds/standard_fields/insured_name", "cds/policy_info/term"]} horizontal /> */}
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          <HX.Collection with="cds" fields={["policy_info/application_date", "standard_fields/underwriter"]} horizontal />
          <HX.Collection with="cds" fields={["currencies/source_currency", "standard_fields/is_renewal"]} horizontal />
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["/cds/standard_fields/policy_reference", "status"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Cover Options" >
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Table
              data={["coverages/hull", null, "coverages/liability"]}
              fields={[
                "section_reference",
                "quoted_premium",
                "quoted_premium_net",
                null,
                "brokerage",
                "profit_commission",
                "ncb_pct",
                null,
                { field: "coverage", shownBy: "/cds/is_airlines" },
                "written_line",
                { field: "rate_change", labelBy: "coverages/hull/rate_change_label" },
                null,
                "limit",
                "excess",
                "currency"
              ]}
              transpose
              kb-interactive
              syncColumnWidthsKey="cover"
            />
          </HX.With>
          <HX.Pane flow="right">
            <HX.Collection fields={["cds/experience_rating/claims_available"]} />
            <HX.Pane shownBy="cds/is_neither" />
            <HX.Button title="Start Airlines" task="show_airlines_task" shownBy="cds/is_airlines" />
            <HX.Button title="Start General Aviation" task="show_ga_task" shownBy="cds/is_ga" />
          </HX.Pane>
          <HX.Collection fields={[null, "model_state/sql_failure_msg"]} horizontal shownBy="model_state/has_sql_conn_failed" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Broker Details - Optional">
        <HX.Collection with="cds" fields={["standard_fields/broker", "policy_info/broker_contact"]} horizontal />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };
