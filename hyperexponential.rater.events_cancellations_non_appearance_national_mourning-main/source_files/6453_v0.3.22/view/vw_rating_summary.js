import * as HX from "hx-model-components";
import { EC_COVERAGES } from "view/vw_constants";

const FIELDS_LOSS_COSTS = [
  null,
  { field: "loss_cost_layer_adj", shownBy: "/model_state/show_actuarial" },
  { field: null, shownBy: "/model_state/show_actuarial" },
  { field: "agg_adjustment", shownBy: "/model_state/show_actuarial" },
  { field: "loss_cost_layer_agg_adj", shownBy: "/model_state/show_actuarial" },
  { field: null, shownBy: "/model_state/show_actuarial" },
  { field: "uw_adjustment", shownBy: "/model_state/show_actuarial" },
  "loss_cost_layer_agg_uw_adj",
  null,
  "experience_weight",
  "experience_loss_cost",
  null,
  "blended_loss_cost_no_uw_adj",
  "blended_loss_cost",

];

const FIELDS_POST_UW_ADJ = [
  null,
  "section_reference",
  null,
  "quoted_premium_100",
  "quoted_rol",
  "quoted_roe",
  null,
  "technical_premium_100",
  "technical_rol",
  "tpi",
  null,
  "benchmark_premium_100",
  "benchmark_rol",
  "bpi",
  null,
  "pflr",
  { field: null, shownBy: "/model_state/show_rs_plan" },
  { field: "plan_premium_100", shownBy: "/model_state/show_rs_plan" },
  { field: "plan_rol", shownBy: "/model_state/show_rs_plan" },

];


const FIELDS_PRE_UW_ADJ = [
  null,
  "technical_premium_pre_uw_adj_100",
  "technical_rol_pre_uw_adj",
  "tpi_pre_uw_adj",
  null,
  "benchmark_premium_pre_uw_adj_100",
  "benchmark_rol_pre_uw_adj",
  "bpi_pre_uw_adj",
  null,
  "pflr_pre_uw_adj",
  { field: null, shownBy: "/model_state/show_rs_plan" },
  { field: "plan_premium_pre_uw_adj_100", shownBy: "/model_state/show_rs_plan" },
  { field: "plan_rol_pre_uw_adj", shownBy: "/model_state/show_rs_plan" }
];



{/*NOTE: below for case pricing only */ }
function vw_rating_summary_case_priced(scale) {
  return (
    <HX.Page title="Rating Summary" viewScale={0.9} fullWidth shownBy="/model_state/show_page_rat_sum_case">

      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />          <HX.Pane />
          <HX.Pane />          <HX.Pane />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Overall Summary" shownBy="cds/standard_fields/is_case_priced"      >
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>

          <HX.Collection title="Risk Details" numCols={5} fields={["status", "/cds/currencies/source_currency", "brokerage", "written_line", "coverages/ec_total/section_reference"]} />

          <HX.Collection with="coverages/ec_total" numCols={5}
            fields={["limit", "aggregate_limit", "excess_use",
              { field: "excess", shownBy: "/model_state/show_ec_excess" },
              { field: null, shownBy: "/model_state/show_ec_excess" },
              { field: "deductible", shownBy: "/model_state/show_ec_deductible" },
              { field: "aggregate_deductible", shownBy: "/model_state/show_ec_deductible" }
            ]}
          />

          <HX.Collection
            title="Priced Quotes @ Term & Beazley Share"
            numCols={2}
            fields={[
              "quoted_premium_100_case_priced",
              "bpi_case_priced",
              "technical_premium_100",
              "benchmark_premium_100",
              "technical_premium",
              "benchmark_premium",
            ]}
          />

          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "tpi",
              "pflr",
              "roc",
            ]}
          />

        </HX.With>
      </HX.Section>

      <HX.Section title="Case Pricing Analysis Filepath" shownBy="cds/standard_fields/is_case_priced">
        <HX.Notes field="cds/case_pricing_analysis_location" />
      </HX.Section>

    </HX.Page >
  )
}
export { vw_rating_summary_case_priced };




function vw_rating_summary(scale) {
  return (

    <HX.Page title="Rating Summary" viewScale={0.9} fullWidth shownBy="/model_state/show_page_rat_sum">

      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />          <HX.Pane />
          <HX.Pane />          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Overall Summary" >


        <HX.Pane flow="down" shownBy="model_state/show_actuarial">
          <HX.Collection
            fields={[
              "total_sim_claim_number_calc", "total_sim_claim_number_override", "total_sim_claim_number", null
              , "last_run_status", "calc_run_value", "last_run_value", "check_run_consistent"
              , "total_sim_loss_before_agg", "total_sim_loss_after_agg", "total_sim_loss_after_agg_adj", "total_sim_loss_after_agg_adj_scaled"
              , "total_det_loss_before_agg", "total_det_loss_after_agg", null, "total_det_loss_after_agg_adj"
              , "sim_error", null, "num_sims", "sim_agg_adj"
            ]}
            with="cds/exposure/granular/event_cancel/simulation"
            numCols={4}
            title="Enter Risk details in section below then press button here to run simulation."
          />
          <HX.Button task="task_simulation" title="Simulate Losses" />
        </HX.Pane>



        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}        >

          <HX.Collection title="Risk Details" numCols={5} fields={["status", "/cds/currencies/source_currency", "brokerage", "written_line", null]} />
          <HX.Collection with="coverages/ec_total" numCols={5}
            fields={["limit", "aggregate_limit", "excess_use",
              { field: "excess", shownBy: "/model_state/show_ec_excess" },
              { field: null, shownBy: "/model_state/show_ec_excess" },
              { field: "deductible", shownBy: "/model_state/show_ec_deductible" },
              { field: "aggregate_deductible", shownBy: "/model_state/show_ec_deductible" }]} />

          <HX.Collection
            shownBy="/model_state/show_actuarial"
            title="Priced Quotes"
            numCols={3}
            fields={[
              "quoted_premium_100", "quoted_premium", "quoted_rol",
              "benchmark_premium_100", "benchmark_premium", "quoted_roe",
              "technical_premium_100", "technical_premium", null]}
          />

          <HX.Collection
            shownBy="/model_state/show_underwriter"
            title="Priced Quotes"
            numCols={2}
            fields={[
              "quoted_premium_100", "quoted_rol",
              "benchmark_premium_100", "quoted_roe",
              "technical_premium_100", null]}
          />

          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "bpi", "pflr", "uw_adj_impact",
              "tpi", "tpi_pre_uw_adj", "roc"
            ]}
          />
        </HX.With>


      </HX.Section>


      {/*NOTE: below for EVENT CANCELLATION only */}
      <HX.Section title="Metrics - Event Cancellation" defaultCollapsed={false} shownBy="model_state/show_event_cancellation">
        <HX.Collection fields={["/model_state/show_rs_plan", null, null]} horizontal />
        <HX.Pane >
          <HX.With context={{ "index": 0, "path": "cds/layers", "type": "list" }}>
            <HX.Table title="Summary - after UW Adj"
              with="coverages"
              data={[
                null, { datum: "ec_total", maxWidth: 240 },
                null, ...EC_COVERAGES
              ]}
              fields={[...FIELDS_POST_UW_ADJ]}
              transpose={true}
              kb-interactive={true}
              freezeLeft={0}
              syncColumnWidthsKey="wibble" />


            <HX.Table title="Summary - before UW Adj"
              shownBy="/model_state/show_actuarial"
              with="coverages"
              data={[
                null, { datum: "ec_total", maxWidth: 240 },
                null, ...EC_COVERAGES
              ]}
              fields={[...FIELDS_PRE_UW_ADJ]}
              transpose={true}
              kb-interactive={true}
              freezeLeft={0}
              syncColumnWidthsKey="wibble" />
          </HX.With>


        </HX.Pane>
      </HX.Section>


      <HX.Section title="Loss Cost - Event Cancellation" defaultCollapsed={true} shownBy="model_state/show_event_cancellation">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Table
            title="Loss Costs"
            data={[
              null, { datum: "ec_total", maxWidth: 240 },
              null, ...EC_COVERAGES
            ]}
            fields={[...FIELDS_LOSS_COSTS]}
            kb-interactive
            with="coverages"
            freezeLeft={0}
            transpose
            syncColumnWidthsKey="wibble"
          />
        </HX.With>
      </HX.Section>





      {/*NOTE: below for EVENT CANCELLATION INCLUDING NON APPEARANCE only */}
      <HX.Section title="Metrics - Event Cancellation including Non Appearance" defaultCollapsed={false} shownBy="model_state/show_non_appearance">
        <HX.Collection fields={["/model_state/show_rs_plan", null, null]} horizontal />
        <HX.Pane >
          <HX.With context={{ "index": 0, "path": "cds/layers", "type": "list" }}>
            <HX.Table title="Summary - after UW Adj"
              with="coverages"
              data={[
                null, { datum: "/cds/layers", maxWidth: 240, elementLabelBy: "rat_sum_label" },
                null, { datum: "na_total", maxWidth: 240 },
                null, { datum: "ec_total", maxWidth: 240 },
                null, ...EC_COVERAGES
              ]}
              fields={[...FIELDS_POST_UW_ADJ]}
              transpose={true}
              kb-interactive={true}
              freezeLeft={0}
              syncColumnWidthsKey="wibble" />



            <HX.Table title="Summary - before UW Adj"
              shownBy="/model_state/show_actuarial"
              with="coverages"
              data={[
                null, { datum: "/cds/layers", maxWidth: 240, elementLabelBy: "rat_sum_label" },
                null, { datum: "na_total", maxWidth: 240 },
                null, { datum: "ec_total", maxWidth: 240 },
                null, ...EC_COVERAGES
              ]}
              fields={[...FIELDS_PRE_UW_ADJ]}
              transpose={true}
              kb-interactive={true}
              freezeLeft={0}
              syncColumnWidthsKey="wibble" />
          </HX.With>


        </HX.Pane>
      </HX.Section>


      <HX.Section title="Loss Cost - Event Cancellation including Non Appearance" defaultCollapsed={true} shownBy="model_state/show_non_appearance">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Table
            title="Loss Costs"
            data={[
              null, { datum: "/cds/layers", maxWidth: 240, elementLabelBy: "rat_sum_label" },
              null, { datum: "na_total", maxWidth: 240 },
              null, { datum: "ec_total", maxWidth: 240 },
              null, ...EC_COVERAGES
            ]}
            fields={[...FIELDS_LOSS_COSTS]}
            kb-interactive
            with="coverages"
            freezeLeft={0}
            transpose
            syncColumnWidthsKey="wibble"
          />
        </HX.With>

      </HX.Section>



    </HX.Page >

  )
}


export { vw_rating_summary };
