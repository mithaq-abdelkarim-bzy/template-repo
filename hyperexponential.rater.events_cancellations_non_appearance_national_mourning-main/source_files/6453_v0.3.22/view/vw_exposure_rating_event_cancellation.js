// v0.3.0
import * as HX from "hx-model-components";

function vw_exposure_rating_event_cancellation(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} viewScale={scale} shownBy="model_state/show_page_exposure">

      <HX.Section title="Event Cancellation - Coverages">
        <HX.With context={{ type: "struct", path: "cds/exposure/granular/event_cancel" }} >
          <HX.Collection
            title="Policy Details"
            fields={["event_type", null, null]}
            horizontal
          />
        </HX.With>



        <HX.With context={{ type: "list", path: "/cds/layers", index: 0 }}>
          <HX.Collection with="coverages/ec_total" horizontal fields={["limit", "aggregate_limit", null]} />
          <HX.Collection with="coverages/ec_total" horizontal fields={["excess_use", { field: "excess", shownBy: "/model_state/show_ec_excess" }, { field: null, shownBy: "/model_state/show_ec_deductible" }, null]} />
          <HX.Collection with="coverages/ec_total" horizontal fields={["deductible", "aggregate_deductible", null]} shownBy="/model_state/show_ec_deductible" />
          {/* <HX.Collection with="structure" horizontal fields={["excess_aoc", null, null]} shownBy="/model_state/show_ec_excess" /> */}
        </HX.With>

        <HX.With context={{ type: "struct", path: "cds/exposure/granular/event_cancel" }} >
          <HX.Table
            title="Events"
            with="base_coverages"
            data={[
              { "datum": "all_risks" },
              { "datum": "adverse_weather" },
              { "datum": "earthquake" },
              { "datum": "windstorm" },
              { "datum": "wildfire" },
              { "datum": "terrorism" },
              { "datum": "cyber" },
              { "datum": "national_mourning" },
              { "datum": "riots_and_civil_commotion" },
              { "datum": "strike" },
              { "datum": "war" },
              { "datum": "catastrophic_non_app" }
            ]}
            fields={["covered", "sublimit", "trigger", "delegates", "uw_adj_min", "uw_adj_sel", "uw_adj_max", "uw_adj_fin", "uw_comment"
              , { field: "net_el_usd", shownBy: "/model_state/show_actuarial" }
              , { field: "net_el", shownBy: "/model_state/show_actuarial" }
              , { field: "net_el_mod", shownBy: "/model_state/show_actuarial" }
            ]}
            dynamic
            kb-interactive
          />
        </HX.With>
      </HX.Section>



      <HX.With context={{ type: "struct", path: "cds/exposure/granular/event_cancel" }} >
        <HX.Section title="Event Cancellation - Modifiers" defaultCollapsed={true} >

          <HX.Collection
            title="Terrorism Terms"
            fields={["terrorism_terms/time_distance", "terrorism_terms/event_profile", "terrorism_terms/city_load"]}
            shownBy="/model_state/show_ec_terrorism"
            horizontal
          />

          <HX.Collection
            title="Exposure Curve"
            fields={["exposure_curve"
              , { field: "exposure_curve_warning", shownBy: "/model_state/show_exposure_curve_warning" }, "exposure_curve_comments", null]}
            horizontal
          />

          <HX.Collection
            title="Experience Factor"
            fields={["experience", "experience_ratio", "experience_factor"]}
            horizontal
          />
          <HX.Collection
            fields={["ncb", "ncb_offered", "ncb_factor"]}
            horizontal
          />
        </HX.Section>




        <HX.Section title="Event Cancellation - Events">
          <HX.Collection
            fields={["agg_tiv_calc", "agg_tiv_uw", { field: "agg_tiv_warning", shownBy: "/model_state/show_tiv_warning" }]}
            horizontal
          />
          <HX.Table
            title="Events"
            data={["events"]}
            fields={["event_name", "country", "state", "date_start", "date_end", "tiv", "venue", "check"
              , { field: "ihs_terrorism", shownBy: "/model_state/show_actuarial" }
              , { field: "ihs_riots_and_civil_commotion", shownBy: "/model_state/show_actuarial" }
              , { field: "ihs_strike", shownBy: "/model_state/show_actuarial" }
              , { field: "ihs_war", shownBy: "/model_state/show_actuarial" }
            ]}
            dynamic
            kb-interactive
          />
        </HX.Section>

        <HX.Section title="Settings" shownBy="/model_state/show_ihs_sim_settings">
          <HX.Pane flow="right" >
            <HX.Pane flow="down" stretch shownBy="/model_state/show_ihs">
              <HX.Collection
                fields={["last_run_status", "check_run_consistent", "calc_run_value"]}
                with="/cds/ihs"
                title="Enter country details in prior sections then press button to load IHS info."
              />
              <HX.Button title="Load IHS Data" task="task_fetch_ihs_data" />
            </HX.Pane>

            <HX.Pane flow="down" stretch shownBy="/model_state/show_simulation">
              <HX.Collection
                fields={["last_run_status", "check_run_consistent", "calc_run_value"]}
                with="/cds/exposure/granular/event_cancel/simulation"
                title="Enter all details in prior sections then press button here to run simulation."
              />
              <HX.Button title="Simulate Losses" task="task_simulation" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section >

      </HX.With>
    </HX.Page>
  )
}

export { vw_exposure_rating_event_cancellation };