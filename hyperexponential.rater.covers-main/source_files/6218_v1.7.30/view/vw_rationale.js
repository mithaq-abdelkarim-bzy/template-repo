import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale}>
      <HX.Section title="Underwriter Rationale">
        <HX.Section title="Policy Details">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/insured_name.rationale",
              "hx_core/inception_date.rationale",
              "cds/standard_fields/facility_reference.rationale"
            ]} />
            <HX.Pane />
          </HX.Pane>

        </HX.Section>
        <HX.Section title="Coverholder Background">
          <HX.Notes field="cds/rationale/coverholder_background_info" />
          <HX.Notes field="cds/rationale/coverholder_background" />
        </HX.Section>

        <HX.Section title="Binder History">
          <HX.Table
            title="Binder Historical Performance"
            data={[
              { datum: "detail_by_year", elementLabelBy: "display_yoa" },
              null,
              { datum: "detail_by_year_total" }
            ]}
            fields={[
              { field: "premium_selected", maxWidth: 200 },
              { field: "premium_selected_gn", maxWidth: 200 },
              { field: "incurred_selected", maxWidth: 200 },
              { field: "incurred_selected_lr", maxWidth: 150 },
              { field: "incurred_selected_lr_gn", maxWidth: 150 },
              { field: "incurred_non_cat_selected_lr", maxWidth: 150 },
              { field: "incurred_non_cat_selected_lr_gn", maxWidth: 150 }
            ]}
            with="cds/rating_summary"
            filter="display_show_row_inputs"
            kb-interactive
          />
        </HX.Section>

        <HX.Section title="Binder Overview">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={[
                "cds/rationale/contract_summary",
                "cds/standard_fields/broker.rationale",
                "cds/rationale/risk_type",
                "cds/rationale/construction",
              ]} />
              <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
                <HX.Collection fields={["written_line.rationale"]} />
                <HX.Collection fields={["signed_line.rationale"]} shownBy="/cds/show_hide/node/signed_line" />
                <HX.Collection fields={["total_deductions"]}
                />
              </HX.With>
              <HX.Collection fields={[
                "cds/currencies/source_currency.rationale",
                "cds/rationale/risk_limit",
                "cds/rationale/avg_limit",
                "cds/rationale/top_counties",
                "cds/rationale/avg_rate",
              ]} />

              <HX.Collection fields={["cds/rationale/curr_epi", "cds/rationale/prev_epi", "cds/rationale/curr_rc", "cds/rationale/prev_rc"]} />

              <HX.Collection fields={["cds/rationale/gg_att_lr_pre", "cds/rationale/gn_att_lr_pre", "cds/rationale/att_uw_adj", "cds/rationale/gg_att_lr_pst", "cds/rationale/gn_att_lr_pst"]} horizontal />

              <HX.Collection title="Attritional Override UW Rationale" fields={["cds/rating_summary/summary_ratios/attritional/uw_rationale"]} shownBy="cds/show_hide/node/rs_att_rationale" horizontal />

              <HX.Collection fields={["cds/rationale/gg_large_lr_pre", "cds/rationale/gn_large_lr_pre", "cds/rationale/large_uw_adj", "cds/rationale/gg_large_lr_pst", "cds/rationale/gn_large_lr_pst"]} horizontal />

              <HX.Collection title="Large Override UW Rationale" fields={["cds/rating_summary/summary_ratios/large/uw_rationale"]} shownBy="cds/show_hide/node/rs_lrg_rationale" horizontal />

              <HX.Collection fields={["cds/rationale/gg_cat_lr_pre", "cds/rationale/gn_cat_lr_pre", "cds/rationale/cat_uw_adj", "cds/rationale/gg_cat_lr_pst", "cds/rationale/gn_cat_lr_pst"]} horizontal />

              <HX.Collection title="Catastrophe Override UW Rationale" fields={["cds/rating_summary/summary_ratios/catastrophe/uw_rationale"]} shownBy="cds/show_hide/node/rs_cat_rationale" horizontal />

              <HX.Collection fields={["cds/rationale/gg_total_lr_pre", "cds/rationale/gg_total_lr_pst",]} horizontal />

              <HX.Collection fields={["cds/rationale/comb_ratio_pre_adj_exc_pc", "cds/rationale/comb_ratio_pst_adj_exc_pc",]} horizontal />
              <HX.Collection fields={["cds/rationale/comb_ratio_pre_adj_inc_pc", "cds/rationale/comb_ratio_pst_adj_inc_pc",]} horizontal />

              <HX.Collection fields={[
                "cds/rating_summary/kpi/pst_uw_adj/bpi",
                "cds/rating_summary/kpi/pst_uw_adj/tpi",
                "cds/rating_summary/kpi/pst_uw_adj/roc",
                "cds/rms/edm_summary/all_peril_selected_at_acc_fx/aal",
                "cds/rationale/prm_aal_ratio",
                "cds/rating_summary/technical/amount_pc_100",
                "cds/rating_summary/technical/percent_pc",
              ]} />
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Underwriter Commentary">
          <HX.Notes field="cds/rationale/uw_commentary_info" />
          <HX.Notes field="cds/rationale/uw_commentary" />
          <HX.Pane flow="right">
            <HX.File field="cds/rationale/uw_commentary_file1" />
            <HX.File field="cds/rationale/uw_commentary_file2" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Actuarial Commentary">
          <HX.Collection fields={["cds/rationale/actuarial_review"]} />
          <HX.Notes field="cds/rationale/actuarial_notes" />
          <HX.Pane flow="right">
            <HX.File field="cds/rationale/actuarial_commentary_file1" />
            <HX.File field="cds/rationale/actuarial_commentary_file2" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Rate Change Rationale">
          <HX.Notes field="cds/rationale/rc_commentary" />
          <HX.Pane flow="right">
            <HX.File field="cds/rationale/rc_commentary_file1" />
            <HX.File field="cds/rationale/rc_commentary_file2" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Terms and Conditions Change">
          <HX.Notes field="cds/rationale/tc_commentary" />
          <HX.Pane flow="right">
            <HX.File field="cds/rationale/tc_commentary_file1" />
            <HX.File field="cds/rationale/tc_commentary_file2" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Aggregate Limits Vs. Utilisation">
          <HX.Notes field="cds/rationale/agglim_util_commentary" />
          <HX.Pane flow="right">
            <HX.File field="cds/rationale/agglim_util_commentary_file1" />
            <HX.File field="cds/rationale/agglim_util_commentary_file2" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Risk Profile">
          <HX.Notes field="cds/rationale/risk_profile_commentary_info" />
          <HX.Notes field="cds/rationale/risk_profile_commentary" />
          <HX.Pane flow="right">
            <HX.File field="cds/rationale/risk_profile_commentary_file1" />
            <HX.File field="cds/rationale/risk_profile_commentary_file2" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Territory Profile and Agg Distribution">
          <HX.Notes field="cds/rationale/territory_profile_commentary_info" />
          <HX.Notes field="cds/rationale/territory_profile_commentary" />
          <HX.Pane flow="right">
            <HX.File field="cds/rationale/territory_profile_commentary_file1" />
            <HX.File field="cds/rationale/territory_profile_commentary_file2" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Exposure Change">
          <HX.Notes field="cds/rationale/exposure_change_commentary_info" />
          <HX.Notes field="cds/rationale/exposure_change_commentary" />
          <HX.Pane flow="right">
            <HX.File field="cds/rationale/exposure_change_commentary_file1" />
            <HX.File field="cds/rationale/exposure_change_commentary_file2" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Large Losses">
          <HX.Notes field="cds/rationale/large_losses_commentary_info" />
          <HX.Notes field="cds/rationale/large_losses_commentary" />
          <HX.Pane flow="right">
            <HX.File field="cds/rationale/large_losses_commentary_file1" />
            <HX.File field="cds/rationale/large_losses_commentary_file2" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Download Rationale">
          <HX.Button task="generate_uw_rationale_doc_task" title="Generate UW Rationale Document" />
          <HX.File field="cds/rationale/document" />
        </HX.Section>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rationale };