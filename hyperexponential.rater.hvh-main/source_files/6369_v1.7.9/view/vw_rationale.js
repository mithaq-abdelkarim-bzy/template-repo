import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale}>
      <HX.Section title="Risk Information">
        <HX.With context={{ type: "list", path: "cds/layers", indexBy: "cds/option_to_bind_zero_indexed" }}>
          <HX.Collection
            fields={[
              "/cds/standard_fields/insured_name.read_only",
              "/hx_core/inception_date.read_only",
              "/hx_core/expiry_date.read_only",
              "/cds/standard_fields/policy_reference.read_only",
              "/cds/standard_fields/underwriter.read_only",
              "/cds/standard_fields/broker.read_only",
              "/cds/rating_factors/product_line.read_only",
              "coverages/aop/tiv/value",
              "/cds/standard_fields/is_renewal.read_only"
            ]}
            numCols={3}
          />
        </HX.With>
      </HX.Section>
      <HX.Section title="HVH">
        <HX.Section title="Rating & Terms">
          <HX.With context={{ type: "list", path: "cds/layers", indexBy: "cds/option_to_bind_zero_indexed" }}>
            <HX.Collection
              fields={[
                "kpis/hvh/commercial_premium_pre_uw_adj/premium",
                "kpis/hvh/modifiers/uw_adjustment",
                "kpis/hvh/commercial_premium/premium.read_only"
              ]}
              horizontal
            />
            <HX.Notes field="/cds/notes/underwriter_adjustments_hvh" title="Underwriter Adjustment Comment" />
          </HX.With>
        </HX.Section>
        <HX.Section title="Natural Perils">
          <HX.With context={{ type: "list", path: "cds/layers", indexBy: "cds/option_to_bind_zero_indexed" }}>
            <HX.Table
              data={[
                "coverages/aop",
                "coverages/wildfire",
                "coverages/ws",
                "coverages/eb",
                "coverages/fl",
                "coverages/eq"
              ]}
              fields={[
                "include_peril/value.read_only",
                "tiv/value.rationale_page",
                "deductible.read_only"
              ]}
            />
          </HX.With>
        </HX.Section>
      </HX.Section>
      <HX.Section title="PAF">
        <HX.With context={{ type: "list", path: "cds/layers", indexBy: "cds/option_to_bind_zero_indexed" }}>
          <HX.Collection
            fields={[
              "/cds/exposure/aggregate/paf/largest_collection_type",
              "/cds/exposure/aggregate/paf/tiv",
              "coverages/paf/deductible.read_only",
              "kpis/paf/commercial_premium_pre_uw_adj/premium",
              "kpis/paf/modifiers/uw_adjustment",
              "kpis/paf/commercial_premium/premium.read_only",
            ]}
            numCols={3}
          />
          <HX.Notes field="/cds/notes/underwriter_adjustments_paf" title="Underwriter Adjustment Comment" />
        </HX.With>
      </HX.Section>
      <HX.Section title="Total">
        <HX.With context={{ type: "list", path: "cds/layers", indexBy: "cds/option_to_bind_zero_indexed" }}>
          <HX.Collection
            fields={[
              "kpis/total/technical_premium/premium",
              "kpis/total/commercial_premium_pre_uw_adj/premium",
              "kpis/total/commercial_premium/premium",
              "/cds/brokerage.read_only",
              { field: "rate_change/risk_adjusted_rate_change", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "rate_change/risk_adjusted_rate_change_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
              "tpi"
            ]}
            numCols={3}
          />
        </HX.With>
      </HX.Section>
      <HX.Section title="Notes">
        <HX.Notes field="/cds/notes/rationale_description" title="Description" />
        <HX.Notes field="/cds/notes/rationale_special_processing" title="Special Processing" />
        <HX.Notes field="/cds/notes/rationale_underwriter_thoughts" title="Underwriter Thoughts" />
      </HX.Section>
      {/*<HX.Section title="Underwriter Rationale">
        <HX.Notes field="cds/standard_fields/uw_rationale" />
      </HX.Section>
      <HX.Section title="Policy Document" >
        <HX.Button task="policy_to_excel_task" title="Generate Policy Document" shownBy="policy_doc/show_generate_button" />
        <HX.Notes field="policy_doc/premium_check" shownBy="policy_doc/show_premium_check" />
        <HX.File
          with="policy_doc"
          field="output_file"
          title="Click on the icon below to download the policy document"
          shownBy="show_download" />
      </HX.Section>
      */}
    </HX.Page>
  )
}

export { vw_rationale };