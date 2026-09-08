import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" shownBy="cds/cover_selection/is_selected">
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Summary - Main Coverage">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/cover_selection/cover"]} />
          <HX.Pane></HX.Pane>
          <HX.Pane></HX.Pane>
        </HX.Pane>

        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Table
            data={["eea_section_reference", "non_eea_section_reference"]}
            fields={["ref", "type"]}
            shownBy="has_double_section_ref"
          />
          <HX.Table
            data={["single_section_reference"]}
            fields={["ref", "type"]}
            shownBy="has_single_section_ref"
          />
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              // "section_reference_view",
              "status",
              "brokerage",
              "written_line",
            ]}
          />
        </HX.With>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_rater_priced">
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              { field: "quoted_premium", labelBy: "gross_premium_label" },
              "benchmark_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj",
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "tpi",
              "tpi_pre_uw_adj",
              "bpi",
              // { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
              "pflr",
              "pflr_att",
              "pflr_cat",

            ]}
          />
          <HX.Collection
            title="Other Metrics"
            numCols={2}
            fields={[
              "roc",
              "uw_adj_impact",
            ]}
          />
        </HX.With>
        {/*NOTE: below for case pricing only */}
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_case_priced">
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              { field: "quoted_premium", labelBy: "gross_premium_label" },
              "bpi_case_priced",
              "technical_premium",
              "benchmark_premium",
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "tpi",
              "pflr",
              "roc",
            ]}
          />
        </HX.With>
      </HX.Section>

      {/*NOTE: below for add on Cargo Cyber */}
      <HX.Section title="Summary - Cargo Cyber Add On" shownBy="cds/cover_selection/is_cargo_cyber">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Table
            data={["coverages/cargo_cyber_addon/eea_section_reference", "coverages/cargo_cyber_addon/non_eea_section_reference"]}
            fields={["ref", "type"]}
            shownBy="has_double_section_ref"
          />
          <HX.Table
            data={["coverages/cargo_cyber_addon/single_section_reference"]}
            fields={["ref", "type"]}
            shownBy="has_single_section_ref"
          />
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              // "coverages/cargo_cyber_addon/section_reference_view",
              "status",
              "coverages/cargo_cyber_addon/brokerage",
              "coverages/cargo_cyber_addon/written_line",
            ]}
          />
        </HX.With>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_rater_priced">
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              { field: "coverages/cargo_cyber_addon/quoted_premium", labelBy: "gross_premium_label" },
              "coverages/cargo_cyber_addon/benchmark_premium",
              "coverages/cargo_cyber_addon/technical_premium",
              "coverages/cargo_cyber_addon/technical_premium_pre_uw_adj",
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            with="coverages/cargo_cyber_addon"
            fields={[
              "tpi",
              "tpi_pre_uw_adj",
              "bpi",
              // { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
              "pflr",
              "pflr_att",
              "pflr_cat",

            ]}
          />
          <HX.Collection
            title="Other Metrics"
            numCols={2}
            with="coverages/cargo_cyber_addon"
            fields={[
              "roc",
              "uw_adj_impact",
            ]}
          />
        </HX.With>

      </HX.Section>

    </HX.Page >

  )
}


export { vw_rating_summary };