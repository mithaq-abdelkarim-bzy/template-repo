import * as HX from "hx-model-components";
import Waterfall from "components/waterfall";
import Waterfall_TP from "components/waterfall_tp";

function vw_final_selections_and_summary() {
  return (
    <HX.Page title="Final Selections and Summary" fullWidth shownBy="cds/show_page/show_other">
      <HX.Section title="Rating Methodology" >
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>



      <HX.Section title="Policy Information">
        <HX.Pane>
          <HX.Collection fields={[
            "policy_ref", // # SA: Should a null be put here or the list reordered so start and end date are on the same line?
            "start_date",
            "end_date",
            "policy_class",
            "currency"
          ]}
            with="cds/final_selection"
            numCols={2}
          />
        </HX.Pane>
      </HX.Section>

      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
        <HX.Section title="Risk Quality Scoring">
          <HX.Pane shownBy="/cds/jb_masking" flow="right">
            <HX.Table
              title="High Level Questions"
              data={["jb_final_selection"]}
              fields={[
                "high_level_q1",
                "high_level_q2",
                "high_level_q3",
                "high_level_q4",
                "high_level_q5",
                "high_level_q6",
                "high_level_q7",
                "high_level_q8",
                "high_level_q9",
                "high_level_q10"
              ]}
              transpose
            />
            <HX.Table
              title="Jewellers Block Specific"
              data={["jb_final_selection"]}
              fields={[
                "specific_q1",
                "specific_q2",
                "specific_q3",
                "specific_q4",
                "specific_q5",
                "specific_q6"
              ]}
              transpose
            />

          </HX.Pane>
          <HX.Pane shownBy="/cds/jb_masking" flow="right">
            <HX.Collection fields={["/cds/final_selection/quality_score"]}
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/cit_masking" flow="right">
            <HX.Table
              title="High Level Questions"
              data={["cit_final_selection"]}
              fields={[
                "high_level_q1",
                "high_level_q2",
                "high_level_q3",
                "high_level_q4",
                "high_level_q5",
                "high_level_q6",
                "high_level_q7",
                "high_level_q8",
                "high_level_q9",
                "high_level_q10"
              ]}
              transpose
            />
            <HX.Table
              title="Cash In Transit Block Specific"
              data={["cit_final_selection"]}
              fields={[
                "specific_q1",
                "specific_q2",
                "specific_q3",
                "specific_q4",
                "specific_q5",
                "specific_q6"
              ]}
              transpose
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/cit_masking" flow="right">
            <HX.Collection fields={["/cds/final_selection/quality_score"]}
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/fa_masking" flow="right">
            Risk Quality Score not used for Fine Art
          </HX.Pane>

          <HX.Pane shownBy="/cds/gs_masking" flow="right">
            Risk Quality Score not used for General Specie
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Claims Summary" >
          <HX.Pane flow="right">
            <HX.Table
              data={["/cds/final_claims_summary_table"]}
              fields={["tsi", "exp_prem_post_ded", "assumed_comms", "assumed_lr_gn", "perc_cat_bp", "perc_cat_data", "perc_cat_sel"]}
              kb-interactive
              title="Exposure Loss Cost"
              transpose
            />
            <HX.Table
              data={["/cds/final_claims_summary_table"]}
              fields={[
                "exposure_loss_cost_length_adj",
                "experience_loss_cost_length_adj",
                null,
                "rec_exp_weight",
                { field: "sel_exp_weight", shownBy: "/cds/validation/sel_exp_weight/valid" },
                { field: "sel_exp_weight.invalid", shownBy: "/cds/validation/sel_exp_weight/invalid" },
                null,
                "final_loss_cost",
                "loss_cost_ly"]}
              kb-interactive
              title="Selected Loss Cost"
              transpose
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Claims Summary - Allocated Loss Cost" defaultCollapsed>
          <HX.Pane shownBy="/cds/jb_masking" flow="right">
            <HX.Table
              data={["jb_premises", "jb_travel", "jb_additional"]}
              fields={["final_summary_tsi", "final_summary_prem_post_ded", "final_summary_loss_cost_ly", "final_summary_final_loss_cost"]}
              title="Jewellers Block Allocated Loss Cost by Sub-type"
              kb-interactive
              with="coverages"
            />
            <HX.Collection
              fields={[null]}
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/fa_masking" flow="right">
            <HX.Table
              data={["fa_premises", "fa_travel", "fa_additional"]}
              fields={["final_summary_tsi", "final_summary_prem_post_ded", "final_summary_loss_cost_ly", "final_summary_final_loss_cost"]}
              title="Fine Art Allocated Loss Cost by Sub-type"
              kb-interactive
              with="coverages"
            />
            <HX.Collection
              fields={[null]}
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/gs_masking" flow="right">
            <HX.Table
              data={["gs_metals", "gs_cash", "gs_securities", "gs_additional"]}
              fields={["final_summary_tsi", "final_summary_prem_post_ded", "final_summary_loss_cost_ly", "final_summary_final_loss_cost"]}
              title="General Specie Allocated Loss Cost by Sub-type"
              kb-interactive
              with="coverages"
            />
            <HX.Collection
              fields={[null]}
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/cit_masking" flow="right">
            <HX.Table
              data={["cit_premises", "cit_additional"]}
              fields={["final_summary_tsi", "final_summary_prem_post_ded", "final_summary_loss_cost_ly", "final_summary_final_loss_cost"]}
              title="Cash in Transit Allocated Loss Cost by Sub-type"
              kb-interactive
              with="coverages"
            />
            <HX.Collection
              fields={[null]}
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Limits">
          <HX.Pane flow="right">
            <HX.Table
              data={["/cds/final_prem_summary_limit_table"]}
              fields={[
                { field: "limit", shownBy: "/cds/validation/limit/valid" },
                { field: "limit.invalid", shownBy: "/cds/validation/limit/invalid" },
                { field: "excess", shownBy: "/cds/validation/excess/valid" },
                { field: "excess.invalid", shownBy: "/cds/validation/excess/invalid" },
                "uw_auth_limit",
                "uw_auth_flag"]}
              kb-interactive
            />
          </HX.Pane>
        </HX.Section>
      </HX.With>
      <HX.Section title="KPI Summary" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Pane flow="right">
          {/* Section 3 */}
          <HX.Table
            data={["cds/final_premium_summary_table", "cds/final_prem_prioryear_table"]}
            fields={[
              { field: "quoted_premium_slip_curr", shownBy: "/cds/validation/quoted_premium/valid" },
              { field: "quoted_premium_slip_curr.invalid", shownBy: "/cds/validation/quoted_premium/invalid" },
              "quoted_premium",
              { field: "acq_cost", shownBy: "/cds/validation/brokerage/valid" },
              { field: "acq_cost.invalid", shownBy: "/cds/validation/brokerage/invalid" },
              { field: "signed_line", shownBy: "/cds/validation/signed_line/valid" },
              { field: "signed_line.invalid", shownBy: "/cds/validation/signed_line/invalid" },
              null,
              "gg_achieved_rate",
              "gn_achieved_rate"]}
            kb-interactive
            title="Quote Premium Information"
            transpose
          />

          {/* Section 2 */}
          <HX.Table
            data={["cds/final_premium_summary_table", "cds/final_prem_prioryear_table"]}
            fields={["uw_credit", "client_credit", "risk_score_credit", null, "total_credit"]}
            kb-interactive
            title="Selected UW Adjustments"
            transpose
          />
          {/* Section 1 */}
          <HX.Table
            data={["cds/final_premium_summary_table", "cds/final_prem_prioryear_table"]}
            fields={["tech_prem", "bench_prem", null, "tpi_pre_uw_adj", "bpi_pre_uw_adj", null, "implied_roc_pre_uw_adj", "expected_profit_pre_uw_adj"]}
            kb-interactive
            title="KPI Pre UW Adjustments"
            transpose
          />
          {/* Section 4 */}
          <HX.Table
            data={["cds/final_premium_summary_table", "cds/final_prem_prioryear_table"]}
            fields={["tech_prem_adj", "bench_prem_adj", null, "tpi", "bpi", null, "implied_roc", "expected_profit"]}
            kb-interactive
            title="KPI Post UW Adjustments"
            transpose
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="KPI Summary" shownBy="cds/standard_fields/is_case_priced">
        <HX.Table
          title={"Priced Quotes"}
          data={[{ datum: "cds/layers", width: 250 }]}
          syncColumnWidthsKey="mySyncedTables1"
          fields={[
            "status.kpi_summary_option",
            "/cds/standard_fields/policy_reference.kpi_summary_option",
            "/cds/final_premium_summary_table/acq_cost.short_label_option",
            "/cds/final_premium_summary_table/signed_line.kpi_summary_option",
            null,
            "quoted_prem_kpi_summary",
            "technical_prem_case_priced",
            "bench_prem_case_priced",
            null,
            "tpi_case_priced",
            "bpi_case_priced",
            null,
            "pflr",
            "implied_roc_pre_uw_adj",
          ]}
          freezeLeft={0}
          // kb-interactive // can interact with tables like excel e.g. c&p
          transpose // note un-transpose if require layers to be listed vertically
        />
      </HX.Section>
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
        <HX.Section title="Achieved Rate Allocation" defaultCollapsed>
          <HX.Pane flow="right">
            <HX.Table shownBy="/cds/jb_masking"
              data={["jb_premises", "jb_travel", "jb_additional"]}
              fields={["final_premium_summary_tsi", "final_premium_summary_tech_rate", "final_premium_summary_ach_rate", "final_premium_summary_tsi_ly", "final_premium_summary_tech_rate_ly", "final_premium_summary_ach_rate_ly"]}
              kb-interactive
              with="coverages"
            />
            <HX.Table shownBy="/cds/fa_masking"
              data={["fa_premises", "fa_travel", "fa_additional"]}
              fields={["final_premium_summary_tsi", "final_premium_summary_tech_rate", "final_premium_summary_ach_rate", "final_premium_summary_tsi_ly", "final_premium_summary_tech_rate_ly", "final_premium_summary_ach_rate_ly"]}
              kb-interactive
              with="coverages"
            />
            <HX.Table shownBy="/cds/gs_masking"
              data={["gs_metals", "gs_cash", "gs_securities", "gs_additional"]}
              fields={["final_premium_summary_tsi", "final_premium_summary_tech_rate", "final_premium_summary_ach_rate", "final_premium_summary_tsi_ly", "final_premium_summary_tech_rate_ly", "final_premium_summary_ach_rate_ly"]}
              kb-interactive
              with="coverages"
            />
            <HX.Table shownBy="/cds/cit_masking"
              data={["cit_premises", "cit_additional"]}
              fields={["final_premium_summary_tsi", "final_premium_summary_tech_rate", "final_premium_summary_ach_rate", "final_premium_summary_tsi_ly", "final_premium_summary_tech_rate_ly", "final_premium_summary_ach_rate_ly"]}
              kb-interactive
              with="coverages"
            />
          </HX.Pane>
        </HX.Section>
      </HX.With>
      <HX.Section title="Technical Premium Breakdown" defaultCollapsed>
        <HX.Pane flow="right">
          <HX.Table
            data={["cds/final_prem_summary_tp_table", "cds/final_prem_summary_tp_postuwadj_table"]}
            fields={["loss_cost", "var_exp", "fixed_exp", "inv_income", "reins", "acq_cost", "cap_load", "tech_prem", "allocated_capital"]}
            kb-interactive
            transpose
          />
          <Waterfall_TP
            title="Technical Premium Build-Up (Pre UW Adj.)"
            // xAxisLabel="Risk component"
            yAxisLabel="Premium"
            textPosition="inside"
            data={[
              { value: "loss_cost", label: "Model Loss Cost" },
              // { value: "var_expense", label: "Variable Expenses" },
              // { value: "fixed_expense", label: "Fixed Expenses" },
              { value: "tot_expense", label: "Total Expenses" },
              { value: "inv_income", label: "Investment Income" },
              { value: "ri", label: "Reinsurance" },
              { value: "capital", label: "Capital Load" },
              { value: "brokerage", label: "Brokerage" },
              { value: "tech_prem", label: "GG Technical Premium" },
              { value: "quoted_premium", label: "Quote Premium" },
            ]}
            with="cds/final_tp_waterfall"
          />
          <Waterfall_TP
            title="Technical Premium Build-Up (Post UW Adj.)"
            // xAxisLabel="Risk component"
            yAxisLabel="Premium"
            textPosition="inside"
            data={[
              { value: "loss_cost", label: "Model Loss Cost" },
              // { value: "var_expense", label: "Variable Expenses" },
              // { value: "fixed_expense", label: "Fixed Expenses" },
              { value: "tot_expense", label: "Total Expenses" },
              { value: "inv_income", label: "Investment Income" },
              { value: "ri", label: "Reinsurance" },
              { value: "capital", label: "Capital Load" },
              { value: "brokerage", label: "Brokerage" },
              { value: "tech_prem", label: "GG Technical Premium" },
              { value: "quoted_premium", label: "Quote Premium" },
            ]}
            with="cds/final_tp_uwadj_waterfall"
          />

        </HX.Pane>
      </HX.Section>


      <HX.Section title="Rate Change Summary" shownBy="/cds/standard_fields/is_renewal">
        {/* # SA: I've tried to follow the mapping spreadsheet as closely as possible but to enable this view I've had to duplicate several 
        items so that they're in the correct structures to display on the front end. This has caused quite a messy implementation about 
        which direction to pass these data schema items in. In order to display the uw_selected and model_calculated fields side by side 
        I've had to copy them over to final_rc_total_summary_view_only. This is saved outside the hxd as it contains nothing useful for 
        reporting */}
        <HX.Pane flow="right">
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
            <HX.Table
              data={["/final_rc_total_summary_view_only", "rate_change"]}
              fields={[
                "expiry_premium/uw_selected",
                "exposure_change/uw_selected",
                "deductible_change/uw_selected",
                "limit_change/uw_selected",
                "risk_characteristics_change/uw_selected",
                "terms_conditions_change/uw_selected",
                "risk_adj_premium/uw_selected",
                "quoted_premium"
              ]}
              title="Rate Change Components"
              kb-interactive
              transpose
            />
            <HX.Table
              data={["/final_rc_total_summary_view_only", "rate_change"]}
              fields={[
                "pure_rc",
                "rate_change/uw_selected",
                "business",
                "rate_change_calculated_pryr"
              ]}
              title="Rate Change Summary"
              kb-interactive
              transpose
            />
          </HX.With>
          <Waterfall
            title="Rate Change Waterfall"
            // xAxisLabel="Risk component"
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
              { value: "quoted_premium", label: "Quote Premium" },
            ]}
            with="cds/final_rc_waterfall"
          />
        </HX.Pane>
      </HX.Section>

    </HX.Page >
  )
}

export { vw_final_selections_and_summary };