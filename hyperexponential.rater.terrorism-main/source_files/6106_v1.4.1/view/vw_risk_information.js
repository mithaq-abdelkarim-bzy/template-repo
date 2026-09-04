import * as HX from "hx-model-components";


function vw_risk_information(shownBy) {
  return (
    <HX.Page title="Risk Information" shownBy={shownBy}>

      <HX.Section title="Rating Model">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology", null]} horizontal />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Account Details">
        <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
        <HX.Collection with="cds/standard_fields" fields={["underwriter", "insured_name"]} horizontal />
        <HX.Collection fields={["cds/currencies/source_currency", "cds/policy_info/source_system"]} horizontal />
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection fields={["section_reference", "status", "/cds/standard_fields/is_renewal"]} horizontal />
        </HX.With>
      </HX.Section>

      <HX.Section title="Policy Information">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection fields={["written_line", "written_line_basis", "order"]} horizontal />
          <HX.Collection fields={["quoted_premium_100_pct", "brokerage", "line"]} horizontal />
        </HX.With>
        <HX.With context={{ type: "list", path: "cds/exposure/granular/countries", index: 0 }}>
          <HX.Collection fields={["limit", "excess", "deductible"]} horizontal />
        </HX.With>
        <HX.Collection fields={["cds/policy_info/single_country_only", null, null]} horizontal />
      </HX.Section>

      <HX.Section title="Single Country Details" shownBy="cds/policy_info/single_country_only">
        <HX.With context={{ type: "list", path: "cds/exposure/granular/countries", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Collection
              numCols={3}
              fields={[
                "country",
                "coverage",
                "total_sum_insured",
                "no_of_locations",
                "subcoverage",
                "bi_sum_insured",
                "pml",
                "sublimit",
                "pd_sum_insured"
              ]}
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>

      <HX.Section title="Broker Details - Optional">
        <HX.Collection with="cds" fields={["standard_fields/broker", "policy_info/broker_contact"]} horizontal />
      </HX.Section>

    </HX.Page >
  )
}

export { vw_risk_information };
