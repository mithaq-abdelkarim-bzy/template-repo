import * as HX from "hx-model-components";

const COVERAGES_TABLE_FIELDS = [
  "status",
  "section_reference",
  "rating_summary_brokerage",
  {
    field: "other_deductions.read_only_option", shownBy:
      "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage"
  },
  "rating_summary_written_line",
  null,
  { field: "quoted_premium_pro_rated_100pct", shownBy: "/cds/standard_fields/is_rater_priced" },
  {
    field: "quoted_premium_case_priced",
    shownBy: "/cds/standard_fields/is_case_priced",
  },
  "technical_premium_pro_rated_100pct",
  {
    field: "technical_premium_pre_uw_adj_pro_rated_100pct",
  },
  { field: "benchmark_premium_pro_rated_100pct" },
  null,
  "tpi",
  {
    field: "tpi_pre_uw_adj",
  },
  { field: "bpi", shownBy: "/cds/standard_fields/is_rater_priced" },
  // { field: "bpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" },
  { field: "bpi_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
  null,
  "pflr",
  // "pflr_pre_uw_adj",
  "roc",
  {
    field: "uw_adj_impact",
    shownBy: "/cds/standard_fields/is_rater_priced",
  },
];

function populate_coverage_options() {
  const tableData = [
    {
      datum: "coverages/hull",
    },
    { datum: "coverages/iv" },
    { datum: "coverages/war" },
    { datum: "coverages/loh" },
    { datum: "coverages/ship_building" },
  ];
  const table_path = "/non_cds/show_rating_summary_table/";
  const coverageOptions = [
    { coverages: ["coverages/hull"], shownBy: table_path + "show_hull_table" },
    {
      coverages: ["coverages/hull", "coverages/iv", "coverages/war"],
      shownBy: table_path + "show_hull_iv_war_table",
    },
    {
      coverages: ["coverages/hull", "coverages/iv"],
      shownBy: table_path + "show_hull_iv_table",
    },
    {
      coverages: ["coverages/hull", "coverages/war"],
      shownBy: table_path + "show_hull_war_table",
    },
    {
      coverages: ["coverages/loh"],
      shownBy: table_path + "show_loh_table",
    },
    {
      coverages: ["coverages/ship_building"],
      shownBy: table_path + "show_ship_building_table",
    },
  ];

  return coverageOptions.map((option, index) => {
    const filteredData = tableData.filter((item) =>
      option.coverages.includes(item.datum)
    );
    return (
      <HX.Pane shownBy={option.shownBy}>
        <HX.Table
          key={index}
          title={"Priced Quotes"}
          data={filteredData}
          fields={COVERAGES_TABLE_FIELDS}
          freezeLeft={0}
          transpose
        />
      </HX.Pane>
    );
  });
}

function vw_rating_summary(scale) {
  return (
    <HX.Page
      title="Rating Summary"
      shownBy="model_state/show_after_landing_page"
    >
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="UW Comment">
        <HX.Notes field="cds/uw_comment" />
      </HX.Section>
      <HX.Section title="Coverage Options">
        <HX.With context={{ type: "list", index: 0, path: "cds/layers" }}>
          {populate_coverage_options()}
        </HX.With>
      </HX.Section>
      <HX.Section title="Export to Excel">
        <HX.Pane flow="right">
          <HX.Button
            title="Generate Output Summary"
            task="generate_rating_summary_xlsx_task"
          />
          <HX.File
            field="cds/exposure/granular/vessels/hull_rating/output_summary_xlsx"
            shownBy="/non_cds/show_hide_toggles/hull/show_generated_output_summary_xlsx"
          />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  );
}

export { vw_rating_summary };
