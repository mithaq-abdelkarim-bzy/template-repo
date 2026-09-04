/* eslint-disable */
import * as HX from "hx-model-components";
import { render_notifications, render_quick_run_bar } from "view/results_tables";

function policy_info() {

  return (
    <HX.Page title="Policy Info" fullWidth={true} shownBy="model_state/show_after_landing_page">
      {render_notifications()}
      <HX.Section title="" collapsible={false} shownBy="policy_information/notifications/notifications_populated">
        <HX.Button title="Show/Hide Notifications" task="show_hide_notifications_task" />
      </HX.Section>
      {render_quick_run_bar()}
      <HX.Section title="Insured Search">
        <HX.Collection fields={["firmname_input"]} with="policy_information/insured_search" horizontal />
        <HX.Pane flow="right">
          <HX.Pane />
          <HX.Button task="search_firm_task" title="Search Insured" />
        </HX.Pane>
        <HX.Table
          data={["policy_information/insured_search/search_result"]}
          fields={[
            { field: "firm_name" },
            { field: "selected", maxWidth: 300 }
          ]}
          kb-interactive
        />
        <HX.Pane flow="right">
          <HX.Collection fields={["policy_information/insured_search/custom_firmname"]} />
          <HX.Button task="import_firm_task" title="Load Insured Name" />
        </HX.Pane>
      </HX.Section>

      {/* Policy Information Section */}
      <HX.Section title="Policy Information">
        <HX.Collection fields={["insured.read_only", "version_comment"]} with="policy_information" horizontal />
        <HX.Collection fields={["underwriter", "team", "uw_office", "bi_waiting_period"]} with="policy_information" horizontal />
        <HX.Collection fields={["hx_core/inception_date", "hx_core/expiry_date", "policy_information/policy_length", "policy_information/bi_indemnity_period"]} horizontal />
        <HX.Collection fields={["broker_branch", "broker_contact", "lead_follow", "cbi"]} with="policy_information" horizontal />
        <HX.Collection fields={["slip_currency", "exchange_rate_date", "exchange_rate", "accgrpid", "account_group_name"]} with="policy_information" horizontal />
        <HX.Collection fields={["large_schedule_model", "is_case_priced", null, null, null]} with="policy_information" horizontal />
      </HX.Section>

      {/* Layer Details Section */}
      <HX.Section title="Layer Details">
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "layer_label", "reference", "limit", "excess", "achieved_premium_100_gg",
            "brokerage",
            { field: "written_line_perc", shownBy: "control/show_wrt_line" },
            { field: "written_line_perc.validation", shownBy: "control/show_wrt_line_validation" },
            "quoted_line_perc",
            "new_renewal", "status",
            "sim_used", "elt_for_sim"
          ]}
          transpose
          kb-interactive
        />
      </HX.Section>

      {/* Case Pricing Section */}
      <HX.Section title="Case Pricing Results" shownBy="policy_information/is_case_priced">
        <HX.Pane flow="right">
          <HX.Button task="save_case_pricing_results_task" title="Save Case Pricing Results To Model" />
          <HX.Button task="case_pricing_calc_tech_premium_task" title="Calculate Technical Premium From Expected Loss" />
          <HX.Pane ratio={4} />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Notes field="case_pricing_info" with="policy_information" />
          <HX.Pane />
        </HX.Pane>
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "layer_label",
            "case_pricing/technical_premium",
            "case_pricing/benchmark_premium",
            "case_pricing/total_exp_loss",
            "case_pricing/tpi",
            "case_pricing/bpi",
            "case_pricing/elr",
            null,
            "case_pricing/risk_adj_rate_change"
          ]}
          transpose
          kb-interactive
        />

        <HX.Table
          title="Technical Premium Breakdown"
          syncColumnWidthsKey="mySyncedTables1"
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "layer_label",
            "case_pricing/tech_premium/fire",
            null,
            "case_pricing/us_tech_prem",
            "case_pricing/tech_premium/us_ws",
            "case_pricing/tech_premium/us_tn",
            "case_pricing/tech_premium/us_ha",
            "case_pricing/tech_premium/us_fl",
            "case_pricing/tech_premium/us_eq",
            "case_pricing/tech_premium/us_wf",
            null,
            "case_pricing/intl_tech_prem",
            "case_pricing/tech_premium/intl_ws",
            "case_pricing/tech_premium/intl_tn",
            "case_pricing/tech_premium/intl_ha",
            "case_pricing/tech_premium/intl_fl",
            "case_pricing/tech_premium/intl_eq",
            "case_pricing/tech_premium/intl_wf",
            null,
            "case_pricing/nmp_premium",
            null,
            "case_pricing/aep_impact_1_in_10",
            "case_pricing/oep_impact_1_in_250",
            "case_pricing/tp_breakdown/ri_cost",
            null,
            "case_pricing/tp_breakdown/coc",
            "case_pricing/tp_breakdown/dir_exp",
            "case_pricing/tp_breakdown/ind_exp",
            "case_pricing/tp_breakdown/lae",
            "case_pricing/tp_breakdown/sd_loading",
            "case_pricing/tp_breakdown/inv_ret"
          ]}
          transpose
          kb-interactive
        />

        <HX.Table
          title="Expected Loss Breakdown"
          syncColumnWidthsKey="mySyncedTables1"
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "layer_label",
            "case_pricing/expected_loss/fire",
            null,
            "case_pricing/us_exp_loss",
            "case_pricing/expected_loss/us_ws",
            "case_pricing/expected_loss/us_tn",
            "case_pricing/expected_loss/us_ha",
            "case_pricing/expected_loss/us_fl",
            "case_pricing/expected_loss/us_eq",
            "case_pricing/expected_loss/us_wf",
            null,
            "case_pricing/intl_exp_loss",
            "case_pricing/expected_loss/intl_ws",
            "case_pricing/expected_loss/intl_tn",
            "case_pricing/expected_loss/intl_ha",
            "case_pricing/expected_loss/intl_fl",
            "case_pricing/expected_loss/intl_eq",
            "case_pricing/expected_loss/intl_wf",
          ]}
          transpose
          kb-interactive
        />
        <HX.Notes field="case_pricing_note" with="policy_information" title="Case Pricing Note (include analysis link)" />
      </HX.Section>

      {/* Additional References Section */}
      <HX.Section title="Additional References" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Button task="upsert_hx_meta_pas_references_task" title="Pass References to PAS" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "reference.read_only", "additional_reference_1", "additional_reference_2", "additional_reference_3", "additional_reference_4", "additional_reference_5", "additional_reference_6"
          ]}
          transpose
          kb-interactive
        />
      </HX.Section>

      {/* Manual RMS Input Section */}
      <HX.Section title="Manual RMS Inputs" defaultCollapsed={true}>
        <HX.Table
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "quake_aal", "wind_aal", "quake_sd", "wind_sd", "all_perils_sd",
            "mi_1_in_10_aep_pt", "mi_1_in_250_oep_pt",
            null,
            "intl_quake_aal", "intl_wind_aal", "intl_quake_sd", "intl_wind_sd", "intl_all_perils_sd"
          ]}
          transpose
          kb-interactive
        />
      </HX.Section>

      {/* Useful Links Section */}
      <HX.Section title="Useful Links" defaultCollapsed={false}>
        <HX.Pane flow="right">
          <HX.Notes field="user_guide_note" with="policy_information" />
          <HX.Notes field="fac_powerapp_note" with="policy_information" />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      {/* Comments Section */}
      <HX.Section title="Comments">
        <HX.Notes field="comments/comment_input_box" title="Comment" shownBy="comments/show_comment_input_box" />
        <HX.Pane flow="right">
          <HX.Button task="add_new_comment_task" title="Add Comment" shownBy="comments/show_comment_input_box" />
          <HX.Button task="start_add_comments_task" title="Show Comment Box" shownBy="comments/hide_comment_input_box" />
          <HX.Pane />
        </HX.Pane>
        <HX.Table
          data={["comments/comments_table"]}
          fields={[
            "comment",
            { field: "created_date", maxWidth: 200 },
            { field: "created_by", maxWidth: 200 }
          ]}
          kb-interactive
        />
      </HX.Section>
    </HX.Page >
  );
}

export { policy_info };
