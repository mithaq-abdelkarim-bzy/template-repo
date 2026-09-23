import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";


/*
function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy={"cds/rate_change/show_layer_" + (n + 1)}>
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status.read_only",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              { field: "quoted_premium.read_only", labelBy: "premium_label" },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            numCols={3}
            fields={[
              "pflr",
              "pflr_att",
              "pflr_cat",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
*/


function vw_rate_change_layer() {
  return (
    <HX.Section title="Summary Layer" >
      <HX.With context={{ type: "list", path: "cds/layers", indexBy: "cds/option_to_bind_zero_indexed" }}>
        <HX.Collection
          title="Risk Details"
          numCols={4}
          fields={[
            "status.read_only",
            "section_reference",
            "brokerage",
            "written_line",
          ]}
        />
        <HX.Collection
          title="Pricing"
          numCols={2}
          fields={[
            { field: "quoted_premium", labelBy: "premium_label" },
            null,
            "technical_premium",
            "benchmark_premium",
            "tpi",
            "bpi",
            "tpi_pre_uw_adj",
          ]}
        />
        <HX.Collection
          title="Expected Loss Ratio"
          numCols={3}
          fields={[
            "pflr",
            "pflr_att",
            "pflr_cat",
            "pflr_pre_uw_adj",
            "uw_adj_impact"
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
    </HX.Section >
  );
}


function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs" shownBy="model_state/show_after_landing_page">
      {/*vw_loop_rate_change_layer(max_layers())*/}
      {vw_rate_change_layer()}
    </HX.Page >

  )
}


export { vw_standard_kpi };