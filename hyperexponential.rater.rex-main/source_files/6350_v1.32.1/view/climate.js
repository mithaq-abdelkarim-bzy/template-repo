import * as HX from "hx-model-components";
import { render_notifications } from "view/results_tables";

function climate() {
  return (
    <HX.Page title="Climate" fullWidth={true} shownBy="model_state/show_after_landing_page">
      {render_notifications()}

      <HX.Section title="Generate Metrics">
        <HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="generate_flood_climate_metrics_task" title="Generate Climate Metrics" />
            <HX.Collection fields={["/non_layer_summary/climate_metrics/perils/peril_selection"]} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="generate_climate_doc_task" title="Generate Climate Change Spotlight Document" />
            <HX.File field="/non_layer_summary/climate_metrics/document" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Climate Summary">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Collection fields={["non_layer_summary/climate_metrics/weighted_climate_score"]} />
            <HX.CategoryChart
              data={["score_0", "score_1", "score_2", "score_3", "score_4", "score_5"]}
              fields={["total_tiv"]} // "gn_tech_pre_uw"
              columnType="cluster"
              dataLabelField="score"
              title="TIV by Hurricane Climate Score"
              primaryAxis={{ label: "Total TIV ($m USD)" }}
              // secondaryAxis={{ label: "US Windstorm Tech Premium ($000 USD)" }}
              with="non_layer_summary/climate_metrics/score_locations"
            />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection fields={["non_layer_summary/climate_metrics/flood/flood_climate_risk_score"]} />
            <HX.CategoryChart
              data={["score_summary"]}
              fields={["tiv_total_usd_chart"]}
              columnType="cluster"
              dataLabelField="bzly_loc_score"
              title="TIV by Flood Climate Score"
              primaryAxis={{ label: "Total TIV ($m USD)" }}
              //secondaryAxis={{ label: "US Windstorm Tech Premium ($000 USD)" }}
              with="non_layer_summary/climate_metrics/flood"
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Hurricane Climate Metrics" shownBy="/non_layer_summary/climate_metrics/perils/ws_selected">
        <HX.Pane flow="right">
          <HX.Pane>
            {/* <HX.Pane flow="right"> */}
            <HX.Collection fields={["non_layer_summary/climate_metrics/weighted_climate_score"]} />
            <HX.Notes field="non_layer_summary/climate_metrics/climate_score_description" />
            {/* <HX.Collection fields="non_layer_summary/climate_metrics/climate_score_description" /> */}
            {/* </HX.Pane> */}
            <HX.Table title="Score"
              data={["score_0", "score_1", "score_2", "score_3", "score_4", "score_5"]}
              // fields={["score", "loc_count", "total_tiv", "gn_tech_pre_uw", "aal_cgear_masked", "aal_weighted_cgear"]}
              fields={["score", "loc_count", "loc_prop", "aal_weighted_cgear"]}
              kb-interactive
              with="non_layer_summary/climate_metrics/score_locations"
            />
          </HX.Pane>

          <HX.CategoryChart
            data={["score_0", "score_1", "score_2", "score_3", "score_4", "score_5"]}
            fields={["loc_count", "loc_prop"]}
            columnType="cluster"
            dataLabelField="score"
            // title="Count and Proportion of Locations by Scores"
            title="Count and Proportion of Locations by Score"
            primaryAxis={{ label: "Number of Locations" }}
            secondaryAxis={{ label: "Proportion" }}
            with="non_layer_summary/climate_metrics/score_locations"
          />
          <HX.CategoryChart
            data={["score_0", "score_1", "score_2", "score_3", "score_4", "score_5"]}
            fields={["total_tiv", "gn_tech_pre_uw"]}
            columnType="cluster"
            dataLabelField="score"
            title="TIV and US Windstorm Technical Prem Pre UW Adj. by Score"
            primaryAxis={{ label: "Total TIV ($m USD)" }}
            secondaryAxis={{ label: "US Windstorm Tech Premium ($000 USD)" }}
            with="non_layer_summary/climate_metrics/score_locations"
          />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Hurricane Group Summaries" shownBy="/non_layer_summary/climate_metrics/perils/ws_selected">
        <HX.Pane flow="right">
          <HX.Table title="WS CC Score by Occupancy"
            data={["ws_cc_score_occupancy"]}
            fields={["occupancy", "cgear_score", "tiv_total_usd", "gn_tech_pre_uw_layer"]}
            kb-interactive
            with="non_layer_summary/climate_metrics"
          />
          <HX.Table title="WS CC Score by Gate"
            data={["ws_cc_score_gate"]}
            fields={["ws_gate", "cgear_0", "cgear_1", "cgear_2", "cgear_3", "cgear_4", "cgear_5"]}
            kb-interactive
            with="non_layer_summary/climate_metrics"
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Hurricane Location Detail" shownBy="/non_layer_summary/climate_metrics/perils/ws_selected">
        <HX.Pane>
          <HX.Table title="WS CC Score Top 10 Locations by AAL"
            data={["ws_cc_score_location"]}
            fields={["tiv_total_usd", "aal_weighted_cgear", "cgear_score", "ws_gate", "distance_from_coast", "zip", "occupancy", "constr_desc"]}
            kb-interactive
            with="non_layer_summary/climate_metrics"
          />
          <HX.Button task="produce_climate_map_task" title="Generate Climate Score Map" />
          <HX.Section title="Climate Map" shownBy="/non_layer_summary/climate_metrics/show_file_component">
            <HX.File field="/non_layer_summary/climate_metrics/climate_heatmap_file" />
          </HX.Section>
          {/* map */}
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Hurricane Mitigation Measures" shownBy="/non_layer_summary/climate_metrics/perils/ws_selected">
        <HX.Pane flow="right">
          <HX.Pane ratio={2}>
            <HX.Pane flow="right">
              <HX.Pane ratio={5}>
                <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/risk_mitigation_measures/question"]} />
              </HX.Pane>
              <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/risk_mitigation_measures/answer"]} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Pane shownBy="non_layer_summary/climate_metrics/client_questions/risk_mitigation_measures/show_risk_mitigation_measures" ratio={2}>
            <HX.Pane flow="right" >
              <HX.Pane>
                <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/emergency_response_plans/selection"]} />
              </HX.Pane>
              <HX.Pane ratio={5}>
                <HX.Notes field="non_layer_summary/climate_metrics/client_questions/emergency_response_plans/climate_question.read_only" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/hurricane_focused_renovations/selection"]} />
              </HX.Pane>
              <HX.Pane ratio={5}>
                <HX.Notes field="non_layer_summary/climate_metrics/client_questions/hurricane_focused_renovations/climate_question.read_only" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/emergency_generators/selection"]} />
              </HX.Pane>
              <HX.Pane ratio={5}>
                <HX.Notes field="non_layer_summary/climate_metrics/client_questions/emergency_generators/climate_question.read_only" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/flooding_mitigation_plans/selection"]} />
              </HX.Pane>
              <HX.Pane ratio={5}>
                <HX.Notes field="non_layer_summary/climate_metrics/client_questions/flooding_mitigation_plans/climate_question.read_only" />
              </HX.Pane>
            </HX.Pane>
          </HX.Pane>
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Pane ratio={2}>
            <HX.Pane flow="right">
              <HX.Pane ratio={5}>
                <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/additional_risk_mitigation_practices/question"]} />
              </HX.Pane>
              <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/additional_risk_mitigation_practices/answer"]} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right" shownBy="/non_layer_summary/climate_metrics/client_questions/additional_risk_mitigation_practices/show_additional_risk_mitigation_practices">
          <HX.Pane ratio={2}>
            <HX.Notes title="Rationale" field="non_layer_summary/climate_metrics/client_questions/additional_risk_mitigation_practices/rationale" />
          </HX.Pane>
          <HX.Pane />
        </HX.Pane>
        <HX.Pane />
      </HX.Section>

      <HX.Section title="Flood Climate Metrics" shownBy="/non_layer_summary/climate_metrics/perils/fl_selected">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Collection fields={["non_layer_summary/climate_metrics/flood/flood_climate_risk_score"]} />
            <HX.Collection fields={["non_layer_summary/climate_metrics/flood/pol_change_five_years"]} />

            <HX.Table title="FL Score"
              data={["score_summary"]}
              fields={["bzly_loc_score", "loc_count", "loc_prop", "tiv_total_usd", "current_fl_el"]}
              kb-interactive
              with="non_layer_summary/climate_metrics/flood"
            />
          </HX.Pane>

          <HX.CategoryChart
            data={["score_summary"]}
            fields={["loc_count", "loc_prop"]}
            columnType="cluster"
            dataLabelField="bzly_loc_score"
            title="Count and Proportion of Locations by Score"
            primaryAxis={{ label: "Number of Locations" }}
            secondaryAxis={{ label: "Proportion" }}
            with="non_layer_summary/climate_metrics/flood"
          />

          <HX.CategoryChart
            data={["score_summary"]}
            fields={["tiv_total_usd_chart"]}
            columnType="cluster"
            dataLabelField="bzly_loc_score"
            title="TIV by Score"
            primaryAxis={{ label: "Total TIV ($m USD)" }}
            //secondaryAxis={{ label: "US Windstorm Tech Premium ($000 USD)" }}
            with="non_layer_summary/climate_metrics/flood"
          />

        </HX.Pane>
      </HX.Section>

      <HX.Section title="Flood Group Summaries" shownBy="/non_layer_summary/climate_metrics/perils/fl_selected">
        <HX.Pane flow="right">
          <HX.Table title="FL CC by Construction"
            data={["constr_summary"]}
            fields={["constr_code", "locations", "tiv_total_usd", "current_fl_el", "bzly_loc_score", "change_five_years"]}
            kb-interactive
            with="non_layer_summary/climate_metrics/flood"
          />
          <HX.Table title="FL CC by Num Stories"
            data={["num_stories_summary"]}
            fields={["num_stories", "locations", "tiv_total_usd", "current_fl_el", "bzly_loc_score", "change_five_years"]}
            kb-interactive
            with="non_layer_summary/climate_metrics/flood"
          />
          <HX.Table title="FL CC by Flood Risk Category"
            data={["flood_risk_summary"]}
            fields={["risk_level_fl", "locations", "tiv_total_usd", "current_fl_el", "bzly_loc_score", "change_five_years"]}
            kb-interactive
            with="non_layer_summary/climate_metrics/flood"
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Flood Location Detail" shownBy="/non_layer_summary/climate_metrics/perils/fl_selected">
        <HX.Pane>
          <HX.Table title="FL CC Top 10 Locations"
            data={["top_10_locations_summary"]}
            fields={["industry", "occupancy", "tiv_total_usd", "current_fl_el", "bzly_loc_score", "change_five_years", "constr_code", "num_stories"]}
            kb-interactive
            with="non_layer_summary/climate_metrics/flood"
          />
        </HX.Pane>
      </HX.Section>







      {/* <HX.Section title="Client Questions">
        <HX.Pane ratio={20}>
          <HX.Pane flow="right">
            <HX.Pane ratio={7}>
              <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/awareness/question"]} />
            </HX.Pane>
            <HX.Collection fields={["non_layer_summary/climate_metrics/client_questions/awareness/answer"]} />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane />
        <HX.Pane>
          <HX.Table title="Climate protection measures question"
            data={["awareness_list"]}
            fields={["question", "response"]}
            kb-interactive
            with="non_layer_summary/climate_metrics/client_questions"
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes title="Rationale" field="non_layer_summary/climate_metrics/client_questions/awareness/rationale" />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane />
        <HX.Pane>
          <HX.Table title="Climate protection measures question"
            data={["protection_measures_list"]}
            fields={["question"]}
            kb-interactive
            with="non_layer_summary/climate_metrics/client_questions"
          />
        </HX.Pane>
        <HX.Pane ratio={2}>
          <HX.Notes title="Rationale" field="non_layer_summary/climate_metrics/client_questions/protection_measures/rationale" />
        </HX.Pane>
      </HX.Section> */}
    </HX.Page >
  )
}

export { climate };