import * as HX from "hx-model-components";
import Line from "components/line";

// Define function for build-up table
function BuildUpTable(transpose, shownBy) {
  return (
    <HX.Table
      title="Selected Build Up and Premium Summary"
      data={["years", null, "years_total", "years_annual"]}
      fields={[
        // "year",
        "end_date",
        null,
        "build_up_calculated",
        "build_up_override",
        "build_up_selected",
        "sum_insured",
        null,
        "total_cvg_nl_roe",
        "total_subcvg_nl_roe",
        null,
        "cvg_expo_curve",
        "subcvg_expo_curve",
        null,
        "cvg_premium",
        "subcvg_premium",
        "total_premium",
        null,
        "model_premium_pre_uw_adj",
        "model_premium",
        "benchmark_premium",
        "model_premium_post_agg_adj"
      ]}
      kb-interactive
      transpose={transpose}
      shownBy={shownBy}
      {...(transpose === false ? { freezeLeft: 2 } : {})}
    />
  );
}

function vw_construction() {
  return (
    <HX.Page title="Construction" shownBy="cds/exposure/aggregate/has_construction" viewScale={0.9} fullWidth>

      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.With context={{ type: "struct", path: "coverages/construction" }}>
          <HX.Section title="Construction">
            <HX.Pane>
              <HX.Pane flow="right" reflow={false}>
                <HX.Pane>
                  <HX.Collection title="Policy Details" fields={["/hx_core/inception_date", "/hx_core/expiry_date"]} horizontal syncColumnWidthsKey="details" />
                  <HX.Collection fields={["/cds/exposure/aggregate/total_sum_insured", "days_difference"]} horizontal syncColumnWidthsKey="details" />
                  <HX.Collection with="/cds/exposure/aggregate" fields={["policy_limit", "policy_sublimit"]} horizontal syncColumnWidthsKey="details" />
                  <HX.Collection with="/cds/exposure/aggregate" fields={["policy_excess", "policy_deductible"]} horizontal syncColumnWidthsKey="details" />
                  <HX.Table
                    title="Default"
                    data={["thirds"]}
                    fields={["third", "build_up", "end_date"]}
                    kb-interactive
                  />
                </HX.Pane>
                <Line
                  title="Construction Build Up"
                  xAxisLabel="Year"
                  yAxisLabel="Build Up %"
                  series={[
                    { seriesLabel: "Proposed", points: [{ list: "years", x: "year", y: "build_up_calculated", },], },
                    { seriesLabel: "Selected", points: [{ list: "years", x: "year", y: "build_up_selected", },], },
                  ]}
                />
              </HX.Pane>
              <HX.Collection fields={[null, null, null, "are_years_horizontal"]} horizontal />
              {BuildUpTable(transpose = false, shownBy = "are_years_vertical")}
              {BuildUpTable(transpose = true, shownBy = "are_years_horizontal")}
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.With>

    </HX.Page >
  )
}

export { vw_construction };
