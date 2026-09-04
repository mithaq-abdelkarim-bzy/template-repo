import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Coverage Options">
        <HX.Table
          title="Priced Quotes (Beazley Share)"
          data={[{ datum: "cds/layers", width: 250 }]}
          fields={[
            "section_reference",
            { field: "is_fun_top_up_coverage", shownBy: "cds/policy_info/fundamental_top_up_flag" },
            "is_primary_excess",
            "option_name",
            "status.input",
            "written_line",
            null,
            "limit",
            "limit_pct",
            "excess",
            "excess_pct",
            "indicated",
            null,
            "quoted_premium",
            { field: "model_premium", shownBy: "cds/standard_fields/is_rater_priced" },
            "technical_premium",
            { field: "benchmark_premium" },
            "model_rol",
            // "midpt",
            "warnings",
            "expected_loss_cost",
            null,
            "tpi",
            { field: "bpi", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
            null,
            "pflr",
            "roc",
            { field: "uw_adj_impact", shownBy: "cds/standard_fields/is_rater_priced" },
          ]}
          freezeLeft={0}
          transpose
          kb-interactive
        />

      </HX.Section>


      <HX.Section title="Blend Quotes">

        <HX.Pane flow="right">

          <HX.Pane flow="down">

            <HX.Collection fields={[
              "cds/blend_option/instruction"
            ]} />

            <HX.Table
              title="Blend Options"
              data={["cds/blend_option/option_1", "cds/blend_option/option_2", "cds/blend_option/option_3"]}
              fields={[
                "option_name",
                "weight",
                "weight_excess",
                "model_rol"
              ]}
              freezeLeft={0}
              transpose
              kb-interactive
            />

          </HX.Pane>

          <HX.Pane>
            <HX.Table
              title="Blended Quote"
              data={[{ datum: "cds/blend_option" }]}
              fields={[
                "option_name",
                "limit",
                "limit_pct",
                "excess",
                "excess_pct",
                "indicated",
                "date",
              ]}
              freezeLeft={0}
              transpose
              kb-interactive
            />
          </HX.Pane>

        </HX.Pane>

      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary };