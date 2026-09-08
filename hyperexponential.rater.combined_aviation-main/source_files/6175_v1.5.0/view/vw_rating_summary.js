import * as HX from "hx-model-components";

function vw_rating_summary() {
  return (
    <HX.Page title="Rating Summary" shownBy="cds/exposure/granular/all_fields_valid">

      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_rater_priced">

        <HX.Section title="Cover">
          <HX.Table
            with="coverages"
            data={["hull", "liability/pax", "liability/tpl"]}
            fields={["benchmark_premium_pre_exp", "benchmark_rate_pre_exp"]}
            kb-interactive
            transpose
          />
        </HX.Section>
        <HX.Section title="Experience Rating">
          <HX.Table
            with="coverages"
            data={["hull", "liability"]}
            fields={["benchmark_premium_exp", "exp_credibility", { field: "benchmark_premium_pre_uw_adj", infoBy: "liability/min_rate_info" }]}
            kb-interactive
            transpose
            syncColumnWidthsKey="pre-adj"
          />
        </HX.Section>
        <HX.Section title="Underwriter Adjustments">
          <HX.Pane flow="right">
            <HX.Collection fields={["pilot_uw_adj", "coverages/hull/uw_adj", "coverages/liability/uw_adj"]} />
            <HX.Notes title="UW Rationale" field="/cds/standard_fields/uw_rationale" stretch />
          </HX.Pane>
          <HX.Table
            with="coverages"
            data={["hull", "liability"]}
            fields={["benchmark_premium_post_uw_adj", "uw_adj_impact"]}
            kb-interactive
            transpose
            syncColumnWidthsKey="pre-adj"
          />
        </HX.Section>
        <HX.Section title="BPI - Premium for Policy Term">
          <HX.Table
            data={["coverages/hull", "coverages/liability", "totals"]}
            fields={[
              "benchmark_premium",
              "quoted_premium",
              null,
              "pflr",
              "pflr_net",
              "bpi",
              null,
              "business_plan_bpi",
              "roc_bpi"
            ]}
            kb-interactive
            transpose
            syncColumnWidthsKey="summary"
          />
        </HX.Section>
        <HX.Section title="TPI - Premium for Policy Term">
          <HX.Table
            data={["coverages/hull", "coverages/liability", "totals"]}
            fields={[
              "technical_premium",
              "technical_premium_pre_uw_adj",
              null,
              "tpi",
              "tpi_pre_uw_adj"
            ]}
            kb-interactive
            transpose
            syncColumnWidthsKey="summary"
          />
        </HX.Section>

      </HX.With>

      <HX.Section title="Overall Summary">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "section_reference",
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
              "quoted_premium",
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
              "roc",
              "uw_adj_impact",
            ]}
          />
          {/*NOTE: below for case pricing only */}
        </HX.With>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_case_priced">
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              "quoted_premium_case_priced",
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

      <HX.Section title="Summary Document">
        <HX.Pane>
          <HX.Collection with="policy_doc" fields={["premium_check"]} shownBy="show_premium_check" />
          <HX.Button title="Generate Quote Summary" task="quote_to_excel_task" shownBy="policy_doc/show_generate_button" />
          {/* <HX.Collection with="policy_doc" fields={["premium_check"]} />
          <HX.Button title="Generate Summary of Results" task="quote_to_excel_task" /> */}
          <HX.File with="policy_doc" field="output_file" title="Click on the icon below to download the summary document" shownBy="show_download" />
        </HX.Pane>
      </HX.Section>

      {/* 
      <HX.Section>
        <HX.Collection fields={["debug_str"]} />
        <HX.Pane flow="right">
          <HX.Button title="Assign name" task="name_task" />
          <HX.Button title="Generate doc" task="doc_task" />
        </HX.Pane>
        <HX.File field="file" title="Download" />
      </HX.Section> */}

    </HX.Page >

  )
}


export { vw_rating_summary };