// v0.3.0
import * as HX from "hx-model-components";


function vw_standard_kpi_case_priced(scale) {
  return (
    <HX.Page title="Standard KPIs" shownBy="model_state/show_page_kpi_case">
      <HX.Section title={"Summary Layer"} defaultCollapsed >
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "coverages/ec_total/status",
              "coverages/ec_total/section_reference.read_only",
              "coverages/ec_total/brokerage",
              "coverages/ec_total/written_line",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              { field: "quoted_premium_100", labelBy: "premium_label" },
              null,
              "technical_premium_100",
              "benchmark_premium_100",
              "tpi",
              "bpi",
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_rater_priced"
            numCols={3}
            fields={["pflr", "pflr_pre_uw_adj", "uw_adj_impact"]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_case_priced"
            numCols={3}
            fields={["pflr", null, null]}
          />
          <HX.Collection
            title="Rate Change"
            shownBy="/cds/standard_fields/is_renewal"
            numCols={3}
            fields={[
              { field: "rate_change/risk_adjusted_rate_change", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "rate_change/risk_adjusted_rate_change_case_priced.read_only", shownBy: "/cds/standard_fields/is_case_priced" },
              null, null
            ]}
          />
        </HX.With>
      </HX.Section>

    </HX.Page >
  )
}
export { vw_standard_kpi_case_priced };









function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs" shownBy="model_state/show_page_kpi">
      <HX.Section title={"Summary Layer - Event Cancellation"} defaultCollapsed >
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "coverages/ec_total/status",
              "coverages/ec_total/section_reference.read_only",
              "coverages/ec_total/brokerage",
              "coverages/ec_total/written_line",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              { field: "coverages/ec_total/quoted_premium_100.read_only", labelBy: "premium_label" },
              null,
              "coverages/ec_total/technical_premium_100",
              "coverages/ec_total/benchmark_premium_100",
              "coverages/ec_total/tpi",
              "coverages/ec_total/bpi",
              { field: "coverages/ec_total/tpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "coverages/ec_total/bpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" }
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_rater_priced"
            numCols={3}
            fields={[
              "coverages/ec_total/pflr",
              "coverages/ec_total/pflr_pre_uw_adj",
              "coverages/ec_total/uw_adj_impact"
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_case_priced"
            numCols={3}
            fields={[
              "pflr",
              null,
              null
            ]}
          />
          <HX.Collection
            title="Rate Change"
            shownBy="/cds/standard_fields/is_renewal"
            numCols={3}
            fields={[
              { field: "rate_change/risk_adjusted_rate_change", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "rate_change/risk_adjusted_rate_change_case_priced.read_only", shownBy: "/cds/standard_fields/is_case_priced" },
              null, null
            ]}
          />
        </HX.With>
      </HX.Section>

      <HX.Section title={"Summary Layer - Non Appearance"} defaultCollapsed shownBy="/model_state/show_non_appearance" >
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "coverages/na_total/status",
              "coverages/na_total/section_reference.read_only",
              "coverages/na_total/brokerage",
              "coverages/na_total/written_line",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              { field: "coverages/na_total/quoted_premium_100.read_only", labelBy: "premium_label" },
              null,
              "coverages/na_total/technical_premium_100",
              "coverages/na_total/benchmark_premium_100",
              "coverages/na_total/tpi",
              "coverages/na_total/bpi",
              { field: "coverages/na_total/tpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "coverages/na_total/bpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" }
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_rater_priced"
            numCols={3}
            fields={[
              "coverages/na_total/pflr",
              "coverages/na_total/pflr_pre_uw_adj",
              "coverages/na_total/uw_adj_impact"
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_case_priced"
            numCols={3}
            fields={[
              "pflr",
              null,
              null
            ]}
          />
          <HX.Collection
            title="Rate Change"
            shownBy="/cds/standard_fields/is_renewal"
            numCols={3}
            fields={[
              { field: "rate_change/risk_adjusted_rate_change", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "rate_change/risk_adjusted_rate_change_case_priced.read_only", shownBy: "/cds/standard_fields/is_case_priced" },
              null, null
            ]}
          />
        </HX.With>
      </HX.Section>

    </HX.Page >

  )
}


export { vw_standard_kpi };