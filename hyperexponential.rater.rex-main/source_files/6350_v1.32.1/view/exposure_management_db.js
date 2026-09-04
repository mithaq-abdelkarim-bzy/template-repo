import * as HX from "hx-model-components";

function exposure_management_db() {
  return (
    <HX.Page title="Exposure Management DB" fullWidth={true}>
      <HX.Section title="Search Filters">
        <HX.Pane>
          <HX.Collection fields={[
            "exposure_management_api/inputs/accgrpid",
            "exposure_management_api/inputs/portinfoid",
          ]} horizontal />
          <HX.Collection fields={[
            "exposure_management_api/inputs/reference",
            "exposure_management_api/inputs/team",
            "exposure_management_api/inputs/perspcode",
          ]} horizontal />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Button task="search_exposure_management_data_task" title="Search Exposure Management Database" />
          <HX.Notes field="exposure_management_api/search_fetch_status" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Search Results">
        <HX.Table
          data={["exposure_management_api/search_results"]}
          fields={[
            "portinfoid",
            "accgrpid",
            "policyid_eq",
            "policyid_ws",
            "reference",
            "account_number",
            "account_name",
            "selected"
          ]}
        />
        <HX.Pane flow="right">
          <HX.Button task="pull_in_exposure_management_data_task" title="Pull in Selected" />
          <HX.Notes field="exposure_management_api/location_fetch_status" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Schedule">
        <HX.Table
          data={["exposure_management_api/location_results"]}
          fields={[
            "portinfoid",
            "accgrpid",
            "policyid_eq",
            "policyid_ws",
            "reference",
            "account_number",
            "account_name",
            "locid",
            "locname",
            "Latitude",
            "Longitude",
            "Street",
            "City",
            "construction_code"
          ]}
        />
      </HX.Section>
    </HX.Page>
  )
}

export { exposure_management_db };