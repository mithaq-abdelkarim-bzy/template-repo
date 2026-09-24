import * as HX from "hx-model-components";


function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs" fullWidth={false} shownBy="model_state/show_kpi">
      <HX.Section collapsible={false} >
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status",
              "/cds/standard_kpis/policy_reference",
              "brokerage",
              "written_line",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            numCols={3}
            fields={[
              "pflr",
              "/cds/standard_kpis/pflr_pre_uw_adj",
              "uw_adj_impact"
            ]}
          />
        </HX.With>
      </HX.Section>
    </HX.Page >

  )
}


export { vw_standard_kpi };