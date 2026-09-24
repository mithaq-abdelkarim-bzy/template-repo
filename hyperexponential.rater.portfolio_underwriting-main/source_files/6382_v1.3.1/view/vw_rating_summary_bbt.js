import * as HX from "hx-model-components";

function vw_rating_summary_bbt(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} viewScale={scale} shownBy="model_state/show_rat_sum_bbt">
      <HX.Section title="Rating Summary" collapsible={false}>
        <HX.Pane flow='right'>
          {/* pb requested disabled 12-2-2026 */}
          {/* <HX.Pane >
            <HX.Button title="Calculate Profit commission" task="calculate_profit_commission_task" shownBy="cds/risk_information/is_profit_comission" />
          </HX.Pane> */}
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Section title="623 / 2623 Pricing Outputs">
          <HX.Table
            title="623 / 2623 Benchmarking"
            data={[{ datum: "pricing_outputs", maxWidth: 300 }]}
            fields={["bbt_gn_ulr",
              "bbt_gn_cat_ulr",
              "attr_and_large",
              "cat",
              "deductions_623_2623",
              "deductions_5623",
              { field: "bbt_pc", shownBy: "/non_cds/risk_information/is_actuarial" },
              "bbt_class",
              "tracker_class",
              // "section_ref_5623", removed per PB Teams message 5-Mar-26
              "gn_ulr_5623",
              { field: "gn_ulr_5623_ly", shownBy: "/cds/standard_fields/is_renewal" },
              "afb_api",
              "line_size"]}
            with="cds/rating_summary"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
          />
        </HX.Section>
        <HX.Section title="Additional Loadings">
          <HX.Table
            title="Additional Pricing Loads"
            data={[{ datum: "summary", maxWidth: 300 }]}
            fields={["anti_selection_charge", "uncertainty_charge", "additional_charge_bbt"]}
            with="cds/rating_summary/additional_loadings"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
          />
        </HX.Section>
        <HX.Section title="Pricing Adequacy Metrics">
          <HX.Table
            title="Pricing Adequacy - (Pre Anti-Selection & Uncertainty)"
            data={[{ datum: "summary", maxWidth: 300 }]}
            fields={["best_estimate_pre_pc_adj", "pc_impact", "best_estimate", "bpi", "tpi", "roc"]}
            with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_pre_adj"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
          />
          <HX.Table
            title="Pricing Adequacy - (Actuarial Basis)"
            data={[{ datum: "summary", maxWidth: 300 }]}
            fields={["best_estimate_pre_pc_adj", "pc_impact", "best_estimate", "bpi", "tpi", "roc"]}
            with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_actuarial_basis"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
          />
          <HX.Table
            title="Pricing Adequacy - (Final Pricing Basis)"
            data={[{ datum: "summary", maxWidth: 300 }]}
            fields={[
              "uw_adj_bbt",
              "best_estimate_gn",
              "best_estimate_gg",
              "bpi",
              "tpi",
              "roc",
              { field: "best_estimate_gn_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "best_estimate_gg_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "bpi_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "tpi_ly", shownBy: "/cds/standard_fields/is_renewal" },
              { field: "roc_ly", shownBy: "/cds/standard_fields/is_renewal" }
            ]}
            with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_final_pricing"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
          />
        </HX.Section>
        <HX.Section title="Catastrophe ULR Summary">
          <HX.Table
            data={[{ datum: "summary", maxWidth: 300 }]}
            fields={["gn_cat_ulr_excl_loads", "gn_cat_ulr_inc_loads"]}
            with="cds/rating_summary/cat_ulr_summary"
            syncColumnWidthsKey="table_1"
            kb-interactive
            transpose
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
            data={[{ datum: "summary", maxWidth: 300 }]}
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
          />
        </HX.Section>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_rating_summary_bbt };