import * as HX from "hx-model-components";

function vw_triage(scale) {
  return (
    <HX.Page title="Triage" fullWidth={true} viewScale={scale} shownBy="cds/triage_masking">

      <HX.Section title="Running Total OBE">
        <HX.Pane flow="right">
          <HX.Collection
            fields={["cds/show_prior_triage_years"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Table
            // syncColumnWidthsKey="mySyncedTables1"
            data={["cds/exposure/aggregate/triage_running_total_obe"]}
            fields={[
              { field: "four_years_ago", shownBy: "cds/show_prior_triage_years" },
              { field: "three_years_ago", shownBy: "cds/show_prior_triage_years" },
              { field: "two_years_ago", shownBy: "cds/show_prior_triage_years" },
              "one_years_ago",
              "current_year",
            ]}
            title="Runnng Total OBE"
          />
        </HX.Pane>


      </HX.Section>

      <HX.Section title="Doctors and Residents" defaultCollapsed={true}>
        <HX.Pane>
          <HX.Table
            data={["cds/exposure/granular/triage_doctors_residents"]}
            fields={["specialty",
              "iso_code",
              "iso_class",
              null,
              "obe_per_doctor",
              { field: "doc_four_years_ago", shownBy: "cds/show_prior_triage_years" },
              { field: "doc_three_years_ago", shownBy: "cds/show_prior_triage_years" },
              { field: "doc_two_years_ago", shownBy: "cds/show_prior_triage_years" },
              "doc_one_years_ago",
              "doc_current_year",
              null,
              "obe_per_resident",
              { field: "resident_four_years_ago", shownBy: "cds/show_prior_triage_years" },
              { field: "resident_three_years_ago", shownBy: "cds/show_prior_triage_years" },
              { field: "resident_two_years_ago", shownBy: "cds/show_prior_triage_years" },
              "resident_one_years_ago",
              "resident_current_year",

            ]}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Procedures - Outpatient Surgery" defaultCollapsed={true} >
        <HX.Pane>
          <HX.Table
            data={["cds/exposure/granular/triage_procedures"]}
            fields={["category",
              "exposure_measure",
              "formatted_obe_or_fte",
              { field: "four_years_ago", shownBy: "cds/show_prior_triage_years", labelBy: "cds/rating_factors/four_years_ago_label" },
              { field: "three_years_ago", shownBy: "cds/show_prior_triage_years", labelBy: "cds/rating_factors/three_years_ago_label" },
              { field: "two_years_ago", shownBy: "cds/show_prior_triage_years", labelBy: "cds/rating_factors/two_years_ago_label" },
              { field: "one_years_ago", labelBy: "cds/rating_factors/one_years_ago_label" },
              { field: "current_year", labelBy: "cds/rating_factors/current_year_label" },
            ]}
            kb-interactive
          />

        </HX.Pane>
      </HX.Section>

      <HX.Section title="Historical Bed, Procedure, Doctor and Resident Calculation" defaultCollapsed={true} >
        <HX.Pane>
          <HX.Table
            data={["cds/exposure/granular/triage_historical_obe"]}
            fields={["category",
              "exposure_measure",
              "obe_or_fte",
              "obe_equivalent",
              "overall_obe",
              { field: "four_years_ago", shownBy: "cds/show_prior_triage_years", labelBy: "cds/rating_factors/four_years_ago_label" },
              { field: "three_years_ago", shownBy: "cds/show_prior_triage_years", labelBy: "cds/rating_factors/three_years_ago_label" },
              { field: "two_years_ago", shownBy: "cds/show_prior_triage_years", labelBy: "cds/rating_factors/two_years_ago_label" },
              { field: "one_years_ago", labelBy: "cds/rating_factors/one_years_ago_label" },
              { field: "current_year", labelBy: "cds/rating_factors/current_year_label" },
            ]}
          />

        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_triage };