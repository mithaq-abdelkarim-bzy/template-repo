import * as HX from "hx-model-components";

function vw_cover_details(scale) {
  return (
    <HX.Page title="Cover Details" shownBy="model_state/show_after_landing_page" viewScale={scale}>
      <HX.Section title="Primary Layer">
        <HX.Collection fields={[
          { field: "different_towers_manager_fund_warning.read_only_option", shownBy: "show_different_towers_manager_fund_warning" }
        ]} with="/non_cds/cover_details" />
        <HX.Pane flow="right">
          <HX.Table data={["towers_all_manager"]} fields={[
            { field: "crime", shownBy: "/cds/rating_factors/risk_info/crime_coverage_required" },
            { field: "pi", shownBy: "/cds/rating_factors/risk_info/pi_coverage_required" },
            { field: "do", shownBy: "/cds/rating_factors/risk_info/do_coverage_required" },
          ]} shownBy="/non_cds/cover_details/all_manager_show" with="cds/rating_factors/cover_details/primary_layer" transpose kb-interactive />
          <HX.Table data={["towers_all_manager.manager", "towers_fund"]} fields={[
            { field: "crime", shownBy: "/cds/rating_factors/risk_info/crime_coverage_required" },
            { field: "pi", shownBy: "/cds/rating_factors/risk_info/pi_coverage_required" },
            { field: "do", shownBy: "/cds/rating_factors/risk_info/do_coverage_required" },
          ]} shownBy="/non_cds/cover_details/fund_show" with="cds/rating_factors/cover_details/primary_layer" transpose kb-interactive />
          <HX.Pane shownBy="/non_cds/cover_details/all_manager_show" />
          <HX.Table data={["sir_all_manager"]} fields={[
            { field: "crime", shownBy: "/cds/rating_factors/risk_info/crime_coverage_required" },
            { field: "pi", shownBy: "/cds/rating_factors/risk_info/pi_coverage_required" },
            { field: "do", shownBy: "/non_cds/cover_details/do_side_a_show" },
            { field: "do.side_b", shownBy: "/non_cds/cover_details/do_side_b_show" },
            { field: "do_side_c", shownBy: "/non_cds/cover_details/do_side_c_show" }
          ]} shownBy="/non_cds/cover_details/all_manager_show" with="cds/rating_factors/cover_details/primary_layer" transpose kb-interactive />
          <HX.Table data={["sir_all_manager.manager", "sir_fund"]} fields={[
            { field: "crime", shownBy: "/cds/rating_factors/risk_info/crime_coverage_required" },
            { field: "pi", shownBy: "/cds/rating_factors/risk_info/pi_coverage_required" },
            { field: "do", shownBy: "/non_cds/cover_details/do_side_a_show" },
            { field: "do.side_b", shownBy: "/non_cds/cover_details/do_side_b_show" },
            { field: "do_side_c", shownBy: "/non_cds/cover_details/do_side_c_show" }
          ]} shownBy="/non_cds/cover_details/fund_show" with="cds/rating_factors/cover_details/primary_layer" transpose kb-interactive />
        </HX.Pane>
        <HX.Collection fields={["do_type"]} shownBy="/cds/rating_factors/risk_info/do_coverage_required" with="cds/rating_factors/cover_details/primary_layer" syncColumnWidthsKey="coverage_details" />
      </HX.Section>
      <HX.Section title="Coverage specifics">
        <HX.Collection fields={[
          "sublimits_req",
          "details_reinstatements",
          { field: "reinst_rtc_program_limit", shownBy: "/non_cds/cover_details/rtc_limit_show" },
          { field: "no_direct_reinstatements", shownBy: "/non_cds/cover_details/direct_reinstatements_show" },
        ]} with="cds/rating_factors/cover_details" numCols={3} syncColumnWidthsKey="coverage_details" />
        <HX.Collection fields={[
          { field: "cover_details/crime_retroactive_date", shownBy: "risk_info/crime_coverage_required" },
          { field: "cover_details/pi_retroactive_date", shownBy: "risk_info/pi_coverage_required" },
          { field: "cover_details/do_retroactive_date", shownBy: "risk_info/do_coverage_required" },
        ]} shownBy="/non_cds/risk_info/is_coverage_required" with="cds/rating_factors" horizontal syncColumnWidthsKey="coverage_details" />
        <HX.Pane flow="right">
          <HX.Collection fields={["num_layers"]} with="non_cds/cover_details" syncColumnWidthsKey="coverage_details" />
          <HX.Button task="num_layers_task" title="Apply Number of Layers" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Split of premium" shownBy="non_cds/cover_details/premium_split_show">
        <HX.Collection fields={["eea", "non_eea"]} shownBy="/cds/risk_info/eea_non_eea_indicator" with="cds/rating_factors/cover_details/premium_split_all_layers" horizontal syncColumnWidthsKey="coverage_details" />
        <HX.Collection fields={["is_premium_split_all_layers", null, null]} shownBy="/non_cds/risk_info/is_coverage_required" with="non_cds/cover_details" horizontal />
        <HX.Collection fields={[
          { field: "cover_details/premium_split_all_layers/crime", shownBy: "risk_info/crime_coverage_required" },
          { field: "cover_details/premium_split_all_layers/pi", shownBy: "risk_info/pi_coverage_required" },
          { field: "cover_details/premium_split_all_layers/do", shownBy: "risk_info/do_coverage_required" },
          { field: "/non_cds/cover_details/premium_split_missing_amount", shownBy: "/non_cds/cover_details/show_premium_split_missing_amount" },
          { field: "/non_cds/cover_details/premium_split_missing_amount.bad", shownBy: "/non_cds/cover_details/show_bad_premium_split_missing_amount" }
        ]} shownBy="/non_cds/cover_details/premium_split_coverages_show" with="cds/rating_factors" numCols={3} syncColumnWidthsKey="coverage_details" />
      </HX.Section>
      <HX.Section title="Brokerage & Discounts">
        <HX.Collection fields={["is_brokerage_all_layers", null, null]} with="non_cds/cover_details" horizontal />
        <HX.Collection fields={["brk.input", "ncb", "lta"]} shownBy="/non_cds/cover_details/is_brokerage_all_layers" with="cds/rating_factors/cover_details/brokerage_all_layers" horizontal />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_cover_details };
