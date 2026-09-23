import * as HX from "hx-model-components";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed>
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status.read_only",
              "/cds/standard_fields/policy_reference.read_only",
              "/cds/final_premium_summary_table/acq_cost.read_only",
              "/cds/final_premium_summary_table/signed_line.read_only",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              { field: "quoted_premium", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "quoted_prem_kpi_summary.read_only", shownBy: "/cds/standard_fields/is_case_priced" },
              null,
              { field: "/cds/final_premium_summary_table/tech_prem_adj.kpi_summary_option", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "/cds/final_premium_summary_table/bench_prem_adj.kpi_summary_option", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "technical_prem_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
              { field: "bench_prem_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
              { field: "tpi", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "tpi_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
              { field: "bpi", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "bpi_case_priced.read_only", shownBy: "/cds/standard_fields/is_case_priced" },
              { field: "tpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "bpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" }
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            numCols={3}
            fields={[
              "pflr",
              { field: null, shownBy: "/cds/standard_fields/is_case_priced" },
              { field: null, shownBy: "/cds/standard_fields/is_case_priced" },
              { field: "pflr_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "uw_adj_impact", shownBy: "/cds/standard_fields/is_rater_priced" }
            ]}
          />
        </HX.With>
      </HX.Section>
    );

  }
  return objects
}


function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs" shownBy="cds/show_page/show_other">
      {vw_loop_rate_change_layer(1)}
    </HX.Page >

  )
}


export { vw_standard_kpi };