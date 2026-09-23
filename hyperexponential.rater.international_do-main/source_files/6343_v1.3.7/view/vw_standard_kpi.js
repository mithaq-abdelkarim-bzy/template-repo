import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_standard_layer_kpi(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy={"cds/rate_change/show_layer_" + (n + 1)}>
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              { field: "quoted_premium_100" },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              { field: "tpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "bpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" }
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_rater_priced"
            numCols={3}
            fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
    );
  }
  return objects
}



function vw_standard_kpi_mmp() {
  const objects = [];

  objects.push(
    <HX.Section title={"Summary MMP Total"} shownBy={"cds/risk_information/mmp_flag"}>
      <HX.Collection
        title="Risk Details"
        numCols={4}
        fields={[
          "cds/mmp/total/status.read_only",
          "cds/mmp/total/section_reference.read_only",
          "cds/mmp/total/brokerage",
          "cds/mmp/total/written_line",
        ]}
      />
      <HX.Collection
        title="Pricing"
        numCols={2}
        fields={[
          { field: "cds/mmp/total/quoted_premium_100" },
          null,
          "cds/mmp/total/technical_premium",
          "cds/mmp/total/benchmark_premium",
          "cds/mmp/total/tpi",
          "cds/mmp/total/bpi",
          // { field: "cds/mmp/total/tpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" },
          // { field: "cds/mmp/total/bpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" }
        ]}
      />
      <HX.Collection
        title="Expected Loss Ratio"
        shownBy="/cds/standard_fields/is_rater_priced"
        numCols={3}
        fields={[
          "cds/mmp/total/pflr",
          null,
          null
          // "cds/mmp/total/pflr_pre_uw_adj",
          // "cds/mmp/total/uw_adj_impact"
        ]}
      />
      <HX.Collection
        title="Expected Loss Ratio"
        shownBy="/cds/standard_fields/is_case_priced"
        numCols={3}
        fields={[
          "cds/mmp/total/pflr",
          null,
          null
        ]}
      />
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
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
  );
  return objects
}


function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs" >
      {vw_standard_layer_kpi(max_layers())}
      {vw_standard_kpi_mmp()}
    </HX.Page >

  )
}


export { vw_standard_kpi };