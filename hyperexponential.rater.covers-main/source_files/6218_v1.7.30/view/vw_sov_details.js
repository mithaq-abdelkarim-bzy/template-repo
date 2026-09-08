import * as HX from "hx-model-components";

function vw_sov_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} viewScale={scale} shownBy="cds/show_hide/page/show_sov">
      <HX.Section title="Exposure Management Database Import">
        {/* {/* <HX.Button task="import_accgrpid_only_task" title="Run" /> */}

        <HX.Section title="Search Filters">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/exposure_management_api/inputs/binder_name", "cds/exposure_management_api/inputs/binder_reference"
            ]} horizontal />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Collection fields={["cds/exposure_management_api/limit_results"]} />
            <HX.Button task="search_exposure_management_data_task" title="Search Exposure Management Database" />
            <HX.Notes field="cds/exposure_management_api/search_fetch_status" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Search Results">
          <HX.Table
            data={["cds/exposure_management_api/search_results"]}
            fields={[
              "binder_name",
              "binder_reference",
              "binder_date",
              "num_locs",
              "selected"
            ]}
          />

          <HX.Pane flow="right">
            <HX.Button task="pull_in_exposure_management_data_task" title="Pull in Selected" />
            <HX.Notes field="cds/exposure_management_api/location_fetch_status" />
          </HX.Pane>
          <HX.Pane>
            <HX.Button title="Run Rater" task="run_bordereau_rater_task" />
          </HX.Pane>
        </HX.Section>

      </HX.Section >

      <HX.Section title="Schedule" defaultCollapsed={true} >
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/exposure/granular/sov_total/num_locs"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Table
          data={["sov_total", null, "schedule_table"]}
          fields={[
            "last_updated", "loc_id", "acc_name", "acc_number", "inception_date", "expiry_date", "new_renewal", "acc_beazley_received_gg_prem", "ceded_share", "loc_1_in_250_oep", "loc_1_in_10_aep",
            "address_dropdown/country", "address_dropdown/state", "address_dropdown/county", "address_dropdown/city", "street_address", "zip", "latitude", "longitude",
            "loc_tiv_buildings", "loc_tiv_contents", "loc_tiv_bi", "loc_tiv_total",
            "industry_occupancy_dropdown/industry", "industry_occupancy_dropdown/occupancy", "occupancy_description", "num_stories", "year_built", "floor_area", "iso_constr",
            "ppc_code", "sprinkler", "distance_to_coast", "beazley_gate",
            "loc_aop_covered.fire_exposure_details", "loc_aop_limit.fire_exposure_details", "loc_aop_excess.fire_exposure_details", "loc_aop_ded.fire_exposure_details",
            "loc_ws_beazley_share_gg_aal", "loc_ws_covered.exposure_details", "loc_ws_limit.exposure_details", "loc_ws_excess.exposure_details", "loc_ws_ded.exposure_details",
            "loc_eq_beazley_share_gg_aal", "loc_eq_covered.exposure_details", "loc_eq_limit.exposure_details", "loc_eq_excess.exposure_details", "loc_eq_ded.exposure_details",
            "loc_scs_covered.exposure_details", "loc_scs_limit.exposure_details", "loc_scs_excess.exposure_details", "loc_scs_ded.exposure_details",
            "loc_aop_covered.fl_exposure_details", "loc_aop_limit.fl_exposure_details", "loc_aop_excess.fl_exposure_details", "loc_aop_ded.fl_exposure_details",
            "loc_aop_covered.wf_exposure_details", "loc_aop_limit.wf_exposure_details", "loc_aop_excess.wf_exposure_details", "loc_aop_ded.wf_exposure_details",


          ]}
          with="cds/exposure/granular"
          dynamic={true}
          freezeLeft={0}
          kb-interactive
          maxListVisibleRows={10}
        />
      </HX.Section>

    </HX.Page >
  )
}

export { vw_sov_details };