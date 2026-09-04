import * as HX from "hx-model-components";
import Line from "components/line";

function vw_countries(shownBy) {

  // Create Series data for chart
  const ihsRiskNames = {
    political: "Political",
    terrorism_raw: "Terrorism",
    labour_strikes: "LabourStrikes",
    protests_riots: "ProtestsAndRiots",
    interstate_war: "InterstateWar",
    civil_war: "CivilWar",
  };

  const seriesData = Object.entries(ihsRiskNames).map(([key, label]) => ({
    seriesLabel: label,
    points: [{ list: `/ihs_${key}`, x: "updated_on", y: "value" }],
  }));

  return (
    <HX.Page title="Countries" shownBy={shownBy} fullWidth viewScale={0.8}>
      <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
        <HX.Section title="Country Details">
          <HX.Pane flow="right">
            <HX.Collection fields={["show_ihs_scores", "show_country_clean"]} horizontal />
            <HX.Button task="clean_country_task" title="Paste the Cleaned Country Names to 'Country' " shownBy="show_country_clean" />
            <HX.Collection fields={[null, null, null]} horizontal />
          </HX.Pane>
          <HX.Pane>
            <HX.Button
              task="copy_country_covers_task"
              title="Copy [Coverage, Limit, Excess, Sub-coverage, Sub-limit, Deductible] to all countries"
            />
          </HX.Pane>
          <HX.Table
            data={["countries"]}
            fields={[
              "rated_country",
              "country",
              "proxy_rating_country",
              // { field: "country_raw", shownBy: "show_country_clean" },
              { field: "country_clean", shownBy: "show_country_clean" },
              // "country_code_original",
              // "country_code",
              // "country_cvg_subcvg",
              "no_of_locations",
              "pml",
              "coverage",
              "limit",
              "excess",
              "subcoverage",
              "sublimit",
              "deductible",
              "total_sum_insured",
              "bi_sum_insured",
              "pd_sum_insured",
              "liability_risk",
              "attritional_risk",
              "geog_risk",
              "location_cat_risk",
              { field: "political", shownBy: "show_ihs_scores" },
              { field: "terrorism_raw", shownBy: "show_ihs_scores" },
              { field: "labour_strikes", shownBy: "show_ihs_scores" },
              { field: "protests_riots", shownBy: "show_ihs_scores" },
              { field: "interstate_war", shownBy: "show_ihs_scores" },
              { field: "civil_war", shownBy: "show_ihs_scores" },
              "civil_unrest",
              "war",
              "terrorism",
              "selected_sum_insured",
              { field: "warning", shownBy: "show_warning" }
            ]}
            dynamic
            kb-interactive
            freezeLeft={1}
            freezeRight={1}
          />
        </HX.Section>
      </HX.With>

      <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
        <HX.Section title="IHS Data" shownBy="has_at_least_one_country">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Button title="Refresh IHS Scores" task="task_fetch_ihs_data" />
              <HX.Notes field="refresh_message" />
            </HX.Pane>
            <HX.Pane shownBy="show_chart">
              <HX.Collection fields={["selected_country", null]} horizontal />
              <HX.Collection fields={["country_message", null]} horizontal shownBy="show_country_message" />
              <HX.Pane flow="right">
                <Line
                  title="Historical Values"
                  xAxisLabel="Time"
                  yAxisLabel="Risk"
                  series={seriesData}
                />
                <HX.Table
                  data={["/ihs_descriptions"]}
                  fields={[
                    "risk_name",
                    "description"
                  ]}
                  dynamic
                  kb-interactive
                  freezeLeft={1}
                />
              </HX.Pane>
            </HX.Pane>
            {/* <HX.Table
              data={["/ihs"]}
              fields={[
                "country_code",
                "risk_name",
                "value",
                "updated_on",
                // "description"
              ]}
              dynamic
              kb-interactive
            /> */}
          </HX.Pane>
        </HX.Section>
      </HX.With>

    </HX.Page >
  )
}

export { vw_countries };
