import * as HX from "hx-model-components";

function vw_exposure_details() {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} shownBy="model_state/show_after_landing_page">

      <HX.Section title="Insured State, Information and Coverage Elections">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/state", "cds/reactive_zipcode/zipcode", "cds/county"]} title="Insured State" />
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["brokerage"]} title="Brokerage Information" />
          </HX.With>
          <HX.Collection fields={["cds/coverage_elections/epl", "cds/coverage_elections/fid", "cds/coverage_elections/pcl"]} title="Coverage Elections" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Industry Information">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/industry/naics_search"]} />
          <HX.Collection fields={["cds/industry/mapped_sic_code"]} />
          <HX.Pane />
        </HX.Pane >

        <HX.Pane flow="right">
          <HX.Collection fields={["cds/industry/class_of_business"]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane >

        <HX.Pane flow="right" >
          <HX.Notes field={"cds/industry/alert"} />
          <HX.Notes field={"cds/industry/wh_status"} />
          <HX.Notes field={"cds/industry/wh_information"} />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Company Ownership, State Requirements and Package Information">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/company_ownership"]} title="Company Ownership" />
          <HX.Collection fields={["cds/state_requirements/retroactive_date", "cds/state_requirements/prior_knowledge_date"]} title="State Requirements" />
          <HX.Collection fields={["cds/package_information/combined_single_aggregate_limit", "cds/package_information/package_discount"]} title="Package Information" />

        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_exposure_details };