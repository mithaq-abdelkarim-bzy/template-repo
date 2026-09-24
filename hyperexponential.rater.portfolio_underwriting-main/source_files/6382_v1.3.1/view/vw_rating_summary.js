import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} viewScale={scale} shownBy="model_state/show_rat_sum_std">
      <HX.Section title="Rating Summary" collapsible={false}>
        <HX.Pane flow='right'>
          <HX.Pane >
            <HX.Button title="Calculate Profit commission" task="calculate_profit_commission_task" shownBy="cds/risk_information/is_profit_comission" />
          </HX.Pane>
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Section title="Model GN ULR">
          <HX.Table
            title="Projected GN ULRs"
            data={[{ datum: "table", elementLabelBy: "selected_lob", maxWidth: 200 }, null, { datum: "summary", maxWidth: 300 }]}
            fields={[
              "tracker_class",
              // "policy_ref_by_lob", removed per PB Teams message 5-Mar-26
              "gn_premium",
              "portfolio_percent",
              "total_deductions",
              "own_exp_gn_ulr",
              "lloyds_gn_ulr",
              "beazley_gn_ulr",
              "bp_gn_ulr",
              "case_pricing",
              { field: "own_exp_gn_ulr_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "lloyds_gn_ulr_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "beazley_gn_ulr_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "bp_gn_ulr_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "case_pricing_ly", shownBy: "/cds/standard_fields/is_renewal" }
            ]}
            with="cds/rating_summary/model_gn_ulr/projected_gn_ulr"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
            filter={"is_row_visible"}
          />
          <HX.Table
            title="Model Weights"
            data={[{ datum: "table", elementLabelBy: "selected_lob", maxWidth: 200 }, null, { datum: "summary", maxWidth: 300 }]}
            fields={[
              "own_experience",
              "lloyds_proj",
              "beazley_proj",
              "bp_proj",
              "case_pricing",
              "weighting_check",
              { field: "own_experience_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "lloyds_proj_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "beazley_proj_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "bp_proj_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "case_pricing_ly", shownBy: "/cds/standard_fields/is_renewal" },
              "model_estimate",
              { field: "model_estimate_ly", shownBy: "/cds/standard_fields/is_renewal" }
            ]}
            with="cds/rating_summary/model_gn_ulr/model_weights"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
            filter={"is_row_visible"}
          />
        </HX.Section>
        <HX.Section title="CAT Loadings">
          <HX.Collection fields={["cds/rating_summary/cat_loadings/show_details", null, null, null, null, null]} horizontal />
          <HX.Table
            title="CAT Allocation"
            data={[{ datum: "cat_allocation", elementLabelBy: "selected_lob", maxWidth: 200 }, null, { datum: "summary", maxWidth: 300 }]}
            fields={[
              { field: "attr_and_lrg_exp", shownBy: "show_details" },
              { field: "cat_exp", shownBy: "show_details" },
              { field: "attr_and_lrg_bp", shownBy: "show_details" },
              { field: "cat_bp", shownBy: "show_details" },
              "attr_and_lrg",
              "cat",
              "climate_change_load",
              "nmp_load_general",
              "nmp_load_weather"]}
            with="cds/rating_summary/cat_loadings"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
            filter={"is_row_visible"}
          />
        </HX.Section>
        <HX.Section title="Additional Loadings">
          <HX.Table
            title="Additional Pricing Loads"
            data={[{ datum: "additional_pricing_loads", elementLabelBy: "selected_lob", maxWidth: 200 }, null, { datum: "summary", maxWidth: 300 }]}
            fields={["anti_selection_charge", "uncertainty_charge", "additional_charge"]}
            with="cds/rating_summary/additional_loadings"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
            filter={"is_row_visible"}
          />
        </HX.Section>
        <HX.Section title="Pricing Adequacy Metrics">
          <HX.Table
            title="Pricing Adequacy - (Pre Anti-Selection & Uncertainty)"
            data={[{ datum: "table", elementLabelBy: "selected_lob", maxWidth: 200 }, null, { datum: "summary", maxWidth: 300 }]}
            fields={["best_estimate_pre_pc_adj", "pc_impact", "best_estimate", "bpi", "tpi", "roc"]}
            with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_pre_adj"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
            filter={"is_row_visible"}
          />
          <HX.Table
            title="Pricing Adequacy - (Actuarial Basis)"
            data={[{ datum: "table", elementLabelBy: "selected_lob", maxWidth: 200 }, null, { datum: "summary", maxWidth: 300 }]}
            fields={["best_estimate_pre_pc_adj", "pc_impact", "best_estimate", "bpi", "tpi", "roc"]}
            with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_actuarial_basis"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
            filter={"is_row_visible"}
          />
          <HX.Table
            title="Pricing Adequacy - (Final Pricing Basis)"
            data={[{ datum: "table", elementLabelBy: "selected_lob", maxWidth: 200 }, null, { datum: "summary", maxWidth: 300 }]}
            fields={[
              "uw_adj",
              "best_estimate_gn",
              "best_estimate_gg",
              "bpi",
              "tpi",
              "roc",
              { field: "best_estimate_gn_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "best_estimate_gg_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "bpi_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "tpi_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "roc_ly", shownBy: "/cds/standard_fields/is_renewal" }]}
            with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_final_pricing"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
            filter={"is_row_visible"}
          />
        </HX.Section>
        <HX.Section title="Catastrophe ULR Summary">
          <HX.Table
            data={[{ datum: "details", elementLabelBy: "selected_lob", maxWidth: 200 }, null, { datum: "summary", maxWidth: 300 }]}
            fields={["gn_cat_ulr_excl_loads", "gn_cat_ulr_inc_loads"]}
            with="cds/rating_summary/cat_ulr_summary"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
            filter={"is_row_visible"}
          />
        </HX.Section>
        <HX.Section title="Technical Premium Build Up">
          <HX.Collection fields={[
            { field: 'cds/rating_summary/technical_premium_build_up/tpi_year.read_only_option', shownBy: "/non_cds/risk_information/is_underwriter" },
            { field: "cds/rating_summary/technical_premium_build_up/tpi_year", shownBy: "/non_cds/risk_information/is_actuarial" },
            null, null, null, null, null]}
            horizontal />
          <HX.Table
            title="Technical Premium"
            data={[{ datum: "technical_premium", elementLabelBy: "selected_lob", maxWidth: 200 }, null, { datum: "summary", maxWidth: 300 }]}
            fields={[
              "el_pre_adj",
              "el_actuarial",
              "el_final",
              "net_expense",
              "inv_income",
              "ri_premium",
              "ri_recoveries",
              "capital_required",
              "target_roc",
              "tp_pre_adj",
              "tp_actuarial",
              "tp_final",
              "gg_tp_final",
              "gg_bm_final"]}
            with="cds/rating_summary/technical_premium_build_up"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
            filter={"is_row_visible"}
          />
        </HX.Section>
        <HX.Section title="Trifocus Summary">
          <HX.Table
            data={[
              "model_estimate",
              "be_before_loads",
              "anti_selection",
              "uncertainty",
              "additional_charge",
              "pc_impact",
              "be_after_pc",
              "uw_adj",
              "be_post_uw",
              "bpi",
              "tpi",
              "roc"]}
            fields={[
              { field: "tracker_property", shownBy: "show_tracker_property", width: 200 },
              { field: "tracker_sr", shownBy: "show_tracker_sr", width: 200 },
              { field: "tracker_marine", shownBy: "show_tracker_marine", width: 200 },
              { field: "tracker_pac", shownBy: "show_tracker_pac", width: 200 },
              { field: "tracker_cyber", shownBy: "show_tracker_cyber", width: 200 },
              null,
              { field: "summary", width: 200 }
            ]}
            with="cds/rating_summary/trifocus_summary"
            kb-interactive
          />
        </HX.Section>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rating_summary };