import * as HX from "hx-model-components";

//shownBy="is_employee_count"
function vw_employee_count() {
  return (
    <HX.Page title="Employee Count" fullWidth={true} shownBy={"/non_cds/coverage_elections/epl_pcl"}>

      <HX.Section title="Employee Types">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Table
              data={[
                "cds/us_states/Alabama",
                "cds/us_states/Alaska",
                "cds/us_states/Arizona",
                "cds/us_states/Arkansas",
                "cds/us_states/California",
                "cds/us_states/Colorado",
                "cds/us_states/Connecticut",
                "cds/us_states/Delaware",
                "cds/us_states/District_of_Columbia",
                "cds/us_states/Florida",
                "cds/us_states/Georgia",
                "cds/us_states/Hawaii",
                "cds/us_states/Idaho",
                "cds/us_states/Illinois",
                "cds/us_states/Indiana",
                "cds/us_states/Iowa",
                "cds/us_states/Kansas",
                "cds/us_states/Kentucky",
                "cds/us_states/Louisiana",
                "cds/us_states/Maine",
                "cds/us_states/Maryland",
                "cds/us_states/Massachusetts",
                "cds/us_states/Michigan",
                "cds/us_states/Minnesota",
                "cds/us_states/Mississippi",
                "cds/us_states/Missouri",
                "cds/us_states/Montana",
                "cds/us_states/Nebraska",
                "cds/us_states/Nevada",
                "cds/us_states/New_Hampshire",
                "cds/us_states/New_Jersey",
                "cds/us_states/New_Mexico",
                "cds/us_states/New_York_metro",
                "cds/us_states/New_York_non_metro",
                "cds/us_states/North_Carolina",
                "cds/us_states/North_Dakota",
                "cds/us_states/Ohio",
                "cds/us_states/Oklahoma",
                "cds/us_states/Oregon",
                "cds/us_states/Pennsylvania",
                "cds/us_states/Rhode_Island",
                "cds/us_states/South_Carolina",
                "cds/us_states/South_Dakota",
                "cds/us_states/Tennessee",
                "cds/us_states/Texas",
                "cds/us_states/Utah",
                "cds/us_states/Vermont",
                "cds/us_states/Virginia",
                "cds/us_states/Washington",
                "cds/us_states/West_Virginia",
                "cds/us_states/Wisconsin",
                "cds/us_states/Wyoming",
                "cds/us_states/Total",

              ]}
              fields={["fte", "pte"

              ]}
              title="States"
              syncColumnWidthsKey="mySyncedTables1"
            />
          </HX.Pane>
          <HX.Pane>
            <HX.Table
              data={[
                "cds/split/seasonal",
                "cds/split/independent_contractors",
                "cds/split/temporary",
                "cds/split/foreign",


              ]}
              fields={["head_count"

              ]}
              title="Split"
              syncColumnWidthsKey="mySyncedTables1"
            />

            <HX.Table
              data={[
                "cds/weights/high",
                "cds/weights/above_average",
                "cds/weights/moderate",
                "cds/weights/average",
                "cds/weights/below_average",


              ]}
              fields={["ftes", "weighted_risk"

              ]}
              title="Weights"
              syncColumnWidthsKey="mySyncedTables1"
            />
            <HX.Collection fields={["cds/total_ftes"]} />
            <HX.Collection fields={["cds/total_state_factor"]} />
            <HX.Notes field="cds/comments" title="Comments" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_employee_count };