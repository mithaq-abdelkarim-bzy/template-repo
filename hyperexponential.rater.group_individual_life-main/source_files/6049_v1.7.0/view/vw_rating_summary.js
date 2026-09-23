import * as HX from "hx-model-components";

function vw_rating_summary(scale, shownBy = null) {
  return (
    <HX.Page title="Rating Summary" fullWidth shownBy={shownBy}>

      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>

        <HX.Section title="Aggregate Limit and Deductible - Expected Loss" shownBy="/cds/cover_selection/are_agg_limits_full">
          <HX.Pane flow="right">
            <HX.Button title="Price for PC/NCB or (and) Agg" task="simulate_years_task" />
            <HX.Collection fields={["temp/task_update_msg"]} stretch />
          </HX.Pane>
          <HX.Collection with="coverages/death" fields={["el_cost_post_sim_pre_agg", "el_cost_post_sim", "agg_impact_on_el"]} horizontal />
        </HX.Section>

      </HX.With>

      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Premium Summary" shownBy="/cds/standard_fields/is_rater_priced">
          <HX.Notes with="/cds/cover_selection" field="agg_limits_check_message" shownBy="agg_limits_check_show" />
          <HX.Table
            data={[
              { datum: "coverages/death", labelBy: "coverages/death/label" },
              "coverages/additional_death",
              "coverages/repat_exp",
              { datum: "coverages/critical_illness", infoBy: "coverages/critical_illness/age_info" },
              { datum: "coverages/terminal_illness", infoBy: "coverages/terminal_illness/age_info" },
              null,
              "totals/total_ex_pc_ncb",
              null,
              "totals/pc",
              "totals/ncb",
              null,
              "totals/total"
            ]}
            fields={[
              "el_cost_pre_uw_pre_exp",
              "el_rate_pre_uw_pre_exp",
              "uw_adj",
              "el_cost_post_uw_pre_exp",
              "el_rate_post_uw_pre_exp",
              "expected_loss_cost",
              null,
              "technical_premium",
              "technical_rate",
              "benchmark_premium",
              "benchmark_rate",
              null,
              "quoted_rate",
              "uw_adj_impact",
              "quoted_premium"
            ]}
            filter={"is_covered"}
            kb-interactive
            transpose
            freezeLeft={0}
          />
        </HX.Section>

        <HX.Section title="Technical Summary" shownBy="/cds/standard_fields/is_rater_priced">
          <HX.Pane flow="right" shownBy="/cds/cover_selection/are_agg_limits_full">
            <HX.Button title="Price for PC/NCB or (and) Agg" task="simulate_years_task" />
            <HX.Notes with="/cds/cover_selection" field="agg_limits_check_message" shownBy="agg_limits_check_show" stretch  />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={["/cds/quote/total_sum_insured", "total_no_lives"]} />
            <HX.Collection fields={["expected_pc", "expected_ncb"]} />
            <HX.Collection fields={[{ field: "bpi_pre_uw_adj", infoBy: "expe_adj_label" }, { field: "bpi", infoBy: "expe_adj_label" }]} />
            <HX.Collection fields={[{ field: "tpi_pre_uw_adj", infoBy: "expe_adj_label" }, { field: "tpi", infoBy: "expe_adj_label" }]} />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Summary Statistics" shownBy="/cds/standard_fields/is_rater_priced">
          <HX.Pane flow="right">
            <HX.Collection title="Age" fields={["lives_wtd_avg_age", "si_wtd_avg_age", "max_age", "min_age"]} />
            <HX.Collection title="Salary" fields={["lives_wtd_avg_salary", "max_salary", "min_salary"]} />
            <HX.Collection title="Sum Insured" fields={["lives_wtd_avg_si", "max_si", "min_si"]} />
            <HX.Collection title="Expected Values" fields={["no_claim_prob", "exp_no_deaths_per_thousand", "exp_no_deaths", "avg_cost", "sd_cost"]} />
          </HX.Pane>
        </HX.Section>

      </HX.With>

      <HX.Section title="Technical Summary" shownBy="cds/standard_fields/is_case_priced">
        <HX.Table
          title="Priced Quote"
          data={[{ datum: "cds/layers", width: 250 }]}
          fields={[
            "status",
            "/cds/standard_fields/policy_reference",
            "brokerage",
            "written_line_input",
            null,
            "quoted_premium_case_priced",
            "technical_premium",
            "benchmark_premium",
            null,
            "tpi",
            "bpi_case_priced",
            null,
            "pflr",
            "roc"
          ]}
          freezeLeft={0}
          kb-interactive
          transpose
        />
      </HX.Section>

      <HX.Section title="Notes">
        <HX.Pane flow="right">
          <HX.Notes title="Underwriter Rationale" field="cds/standard_fields/uw_rationale" />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

    </HX.Page >

  )
}


export { vw_rating_summary };