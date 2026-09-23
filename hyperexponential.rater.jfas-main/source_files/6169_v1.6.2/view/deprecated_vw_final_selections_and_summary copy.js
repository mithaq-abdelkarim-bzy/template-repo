import * as HX from "hx-model-components";
import Waterfall from "components/waterfall";

function vw_final_selections_and_summary() {
  return (
    <HX.Page title="Final Selections and Summary" fullWidth>

      <HX.Section title="Policy Information">
        <HX.Pane>
          <HX.Collection fields={[
            "final_policy_ref",
            "final_start_date",
            "final_end_date",
            "final_class",
            "final_currency",

          ]}
            numCols={2}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Risk Quality Scoring">
        <HX.Pane shownBy="jb_masking" flow="right">
          <HX.Table
            title="High Level Questions"
            data={["jb_final_selection"]}
            fields={["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]}
            transpose
          />
          <HX.Table
            title="Jewellers Block Specific"
            data={["final_jb_rqs_specific"]}
            fields={["q1", "q2", "q3", "q4", "q5", "q6"]}
            transpose
          />
          <HX.Collection fields={["final_risk_quality_score"]}
          />
        </HX.Pane>
        <HX.Pane shownBy="cit_masking" flow="right">
          <HX.Table
            title="High Level Questions"
            data={["final_cit_rqs_high_level"]}
            fields={["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]}
            transpose
          />
          <HX.Table
            title="Cash In Transit Block Specific"
            data={["final_cit_rqs_specific"]}
            fields={["q1", "q2", "q3", "q4", "q5", "q6"]}
            transpose
          />
          <HX.Collection fields={["final_risk_quality_score"]}
          />
        </HX.Pane>
        <HX.Pane shownBy="fa_masking" flow="right">
          Risk Quality Score not used for Fine Art
        </HX.Pane>

        <HX.Pane shownBy="gs_masking" flow="right">
          Risk Quality Score not used for General Specie
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Claims Summary" >
        <HX.Pane shownBy="jb_masking">
          <HX.Table
            data={["final_jb_premises_summary", "final_jb_travel_summary", "final_jb_additional_summary"]}
            fields={["tsi", "prem_post_ded", "loss_cost_ly", "final_loss_cost"]}
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane shownBy="fa_masking">
          <HX.Table
            data={["final_fa_premises_summary", "final_fa_travel_summary", "final_fa_additional_summary"]}
            fields={["tsi", "prem_post_ded", "loss_cost_ly", "final_loss_cost"]}
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane shownBy="gs_masking">
          <HX.Table
            data={["final_gs_metals_summary", "final_gs_cash_summary", "final_gs_securities_summary"]}
            fields={["tsi", "prem_post_ded", "loss_cost_ly", "final_loss_cost"]}
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane shownBy="cit_masking">
          <HX.Table
            data={["final_cit_premises_summary", "final_cit_additional_summary"]}
            fields={["tsi", "prem_post_ded", "loss_cost_ly", "final_loss_cost"]}
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            data={["final_claims_summary_table"]}
            fields={["tsi", "exp_prem_post_ded", "assumed_comms", "assumed_lr_gn", "exposure_loss_cost_length_adj", "experience_loss_cost_length_adj",
              "rec_exp_weight", "sel_exp_weight", "loss_cost_ly", "final_loss_cost", "perc_cat_bp", "perc_cat_data", "perc_cat_sel"]}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Premium Summary">
        <HX.Pane>
          <HX.Table
            data={["final_prem_summary_limit_table"]}
            fields={["limit", "excess", "uw_auth_limit", "uw_auth_flag"]}
            kb-interactive
          />
          <HX.Table
            data={["final_premium_summary_table", "final_prem_prioryear_table"]}
            fields={["loss_cost", "tech_prem", "bench_prem", "uw_credit", "client_credit", "risk_score_credit", "total_credit", "tech_prem_adj", "bench_prem_adj",
              "quote_prem", "acq_cost", "signed_line", "tpi", "bpi", "implied_roc", "expected_profit"]}
            kb-interactive
          />
          <HX.Table shownBy="jb_masking"
            data={["jb_premises_final_premium_summary", "jb_travel_final_premium_summary", "jb_additional_final_premium_summary"]}
            fields={["tsi", "tech_rate", "ach_rate", "tsi_ly", "tech_rate_ly", "ach_rate_ly"]}
            kb-interactive
          />
          <HX.Table shownBy="fa_masking"
            data={["fa_premises_final_premium_summary", "fa_travel_final_premium_summary", "fa_additional_final_premium_summary"]}
            fields={["tsi", "tech_rate", "ach_rate", "tsi_ly", "tech_rate_ly", "ach_rate_ly"]}
            kb-interactive
          />
          <HX.Table shownBy="gs_masking"
            data={["gs_metals_final_premium_summary", "gs_cash_final_premium_summary", "gs_securities_final_premium_summary"]}
            fields={["tsi", "tech_rate", "ach_rate", "tsi_ly", "tech_rate_ly", "ach_rate_ly"]}
            kb-interactive
          />
          <HX.Table shownBy="cit_masking"
            data={["final_prem_summary_cit_premises", "final_prem_summary_cit_additional"]}
            fields={["tsi", "tech_rate", "ach_rate", "tsi_ly", "tech_rate_ly", "ach_rate_ly"]}
            kb-interactive
          />
          <HX.Table
            data={["final_prem_summary_tp_table", "final_prem_summary_tp_postuwadj_table"]}
            fields={["loss_cost", "var_exp", "fixed_exp", "inv_income", "reins", "acq_cost", "cap_load", "tech_prem", "alloc_cap"]}
            title="Technical Premium Breakdown"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Rate Change Summary" >
        <HX.Pane>
          <HX.Table
            data={["final_rc_total_summary", "final_rc_uwadj_summary"]}
            fields={["exp_prem", "exposure", "deduct", "limit", "risk", "t_and_cs", "risk_adj_prem", "quoted_prem"]}
            title="Rate Change Summary Metrics"
            kb-interactive
          />
          <HX.Table
            data={["final_rc_total_summary2", "final_rc_uwadj_summary2"]}
            fields={["pure_rc", "rarc", "business", "rarc_ly"]}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Waterfall Chart">
        <HX.Pane>
          <Waterfall
            title="Rate Change Waterfall"
            xAxisLabel="Risk component"
            yAxisLabel="GNWP (USD)"
            textPosition="inside"
            data={[
              { value: "exp_prem", label: "Expiring Premium" },
              { value: "exposure", label: "Exposure" },
              { value: "deduct", label: "Deductibles" },
              { value: "limit", label: "Limits" },
              { value: "risk", label: "Risk" },
              { value: "t_and_cs", label: "T&Cs" },
              { value: "risk_adj_prem", label: "Risk Adj Prem" },
            ]}
            with="final_rc_waterfall"
          />
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_final_selections_and_summary };