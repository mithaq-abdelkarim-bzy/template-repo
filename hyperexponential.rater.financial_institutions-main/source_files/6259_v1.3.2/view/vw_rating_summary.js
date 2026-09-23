import * as HX from "hx-model-components";
import { max_towers } from "./vw_constants";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" shownBy="model_state/show_after_landing_page" fullWidth={true} viewScale={scale}>
      <HX.Section title="Program Structure">
        <HX.Collection fields={["table1_label", null, null, null, null]} with="non_cds/rating_summary" syncColumnWidthsKey="field" horizontal />
        <HX.Table data={[
          { datum: "cds/layers", elementLabelBy: "label" },
        ]} fields={[
          ...getTowerFields("coverage", "coverage_show"),
          null,
          ...getTowerFields("limit"),
          null,
          ...getTowerFields("excess_str"),
          null,
          ...getTowerFields("direct_reinstatements", "direct_reinstatements_show"),
          null,
          ...getTowerFields("rtc_reinstatements", "rtc_reinstatements_show"),
          null,
          { field: "coverages/crime/all_manager/sublimit", shownBy: "non_cds/rating_summary/crime/sublimit_show" },
          { field: "coverages/pi/all_manager/sublimit", shownBy: "non_cds/rating_summary/pi/sublimit_show" },
          { field: "coverages/do/all_manager/sublimit", shownBy: "non_cds/rating_summary/do/sublimit_show" },
          { field: "coverages/crime/all_manager/sublimit.manager", shownBy: "non_cds/rating_summary/crime/all_manager_sublimit_show" },
          { field: "coverages/pi/all_manager/sublimit.manager", shownBy: "non_cds/rating_summary/pi/all_manager_sublimit_show" },
          { field: "coverages/do/all_manager/sublimit.manager", shownBy: "non_cds/rating_summary/do/all_manager_sublimit_show" },
          { field: "coverages/crime/fund/sublimit", shownBy: "non_cds/rating_summary/crime/fund_sublimit_show" },
          { field: "coverages/pi/fund/sublimit", shownBy: "non_cds/rating_summary/pi/fund_sublimit_show" },
          { field: "coverages/do/fund/sublimit", shownBy: "non_cds/rating_summary/do/fund_sublimit_show" },
          null,
          "quoted_premium_pro_rata_100.input",
          { field: "brokerage.input", shownBy: "non_cds/rating_summary/is_brokerage_per_layer" },
          { field: "ncb", shownBy: "non_cds/rating_summary/is_brokerage_per_layer" },
          { field: "lta", shownBy: "non_cds/rating_summary/is_brokerage_per_layer" },
          "net_premium",
          { field: "coverages/crime/premium_split", shownBy: "non_cds/rating_summary/crime/premium_split_show" },
          { field: "coverages/pi/premium_split", shownBy: "non_cds/rating_summary/pi/premium_split_show" },
          { field: "coverages/do/premium_split", shownBy: "non_cds/rating_summary/do/premium_split_show" },
          null,
          ...getTowerFields("beazley_line"),
          null,
          "esg",
          null,
          "exposure",
          "afb_net_premium",
          "net_rol",
          "actual_ilf",
          null,
          "bpi",
          "benchmark_premium_annualised_100",
          "benchmark_premium_pro_rata_100",
          { field: "coverages/crime/losses_split", shownBy: "cds/rating_factors/risk_info/crime_coverage_required" },
          { field: "coverages/pi/losses_split", shownBy: "cds/rating_factors/risk_info/pi_coverage_required" },
          { field: "coverages/do/losses_split", shownBy: "cds/rating_factors/risk_info/do_coverage_required" },
          "model_ilf",
          null,
          "expected_loss_cost_att",
          "expected_loss_cost_cat",
          "tpi",
          "technical_premium_net",
          "technical_premium",
          null,
          "status.input",
          { field: "coverages/crime/pol_ref", shownBy: "cds/rating_factors/risk_info/crime_coverage_required", minWidth: 200 },
          { field: "coverages/pi/pol_ref", shownBy: "cds/rating_factors/risk_info/pi_coverage_required", minWidth: 200 },
          { field: "coverages/do/pol_ref", shownBy: "cds/rating_factors/risk_info/do_coverage_required", minWidth: 200 },
          { field: "coverages/crime/pol_ref_non_eea", shownBy: "non_cds/rating_summary/crime/pol_ref_non_eea_show", minWidth: 200 },
          { field: "coverages/pi/pol_ref_non_eea", shownBy: "non_cds/rating_summary/pi/pol_ref_non_eea_show", minWidth: 200 },
          { field: "coverages/do/pol_ref_non_eea", shownBy: "non_cds/rating_summary/do/pol_ref_non_eea_show", minWidth: 200 },
          "slip_lead"
        ]} freezeLeft={0} kb-interactive />
      </HX.Section>
      <HX.Section title="Program Structure - USD" shownBy="non_cds/rating_summary/secondry_summary_show">
        <HX.Collection fields={["authorities_fx"]} with="cds/rating_summary" syncColumnWidthsKey="field" horizontal />
        <HX.Table data={[
          { datum: "cds/layers", elementLabelBy: "label" },
        ]} fields={[
          ...getTowerFields("coverage"),
          null,
          ...getTowerFields("limit_fx"),
          null,
          ...getTowerFields("excess_str_fx"),
          null,
          ...getTowerFields("direct_reinstatements", "direct_reinstatements_show"),
          null,
          ...getTowerFields("rtc_reinstatements_fx", "rtc_reinstatements_show"),
          null,
          { field: "coverages/crime/all_manager/sublimit_fx", shownBy: "non_cds/rating_summary/crime/sublimit_show" },
          { field: "coverages/pi/all_manager/sublimit_fx", shownBy: "non_cds/rating_summary/pi/sublimit_show" },
          { field: "coverages/do/all_manager/sublimit_fx", shownBy: "non_cds/rating_summary/do/sublimit_show" },
          { field: "coverages/crime/all_manager/sublimit_fx.manager", shownBy: "non_cds/rating_summary/crime/all_manager_sublimit_show" },
          { field: "coverages/pi/all_manager/sublimit_fx.manager", shownBy: "non_cds/rating_summary/pi/all_manager_sublimit_show" },
          { field: "coverages/do/all_manager/sublimit_fx.manager", shownBy: "non_cds/rating_summary/do/all_manager_sublimit_show" },
          { field: "coverages/crime/fund/sublimit_fx", shownBy: "non_cds/rating_summary/crime/fund_sublimit_show" },
          { field: "coverages/pi/fund/sublimit_fx", shownBy: "non_cds/rating_summary/pi/fund_sublimit_show" },
          { field: "coverages/do/fund/sublimit_fx", shownBy: "non_cds/rating_summary/do/fund_sublimit_show" },
          null,
          "quoted_premium_pro_rata_100_fx",
          { field: "brokerage", shownBy: "non_cds/rating_summary/is_brokerage_per_layer" },
          { field: "ncb", shownBy: "non_cds/rating_summary/is_brokerage_per_layer" },
          { field: "lta", shownBy: "non_cds/rating_summary/is_brokerage_per_layer" },
          "net_premium_fx",
          { field: "coverages/crime/premium_split", shownBy: "non_cds/rating_summary/crime/premium_split_show" },
          { field: "coverages/pi/premium_split", shownBy: "non_cds/rating_summary/pi/premium_split_show" },
          { field: "coverages/do/premium_split", shownBy: "non_cds/rating_summary/do/premium_split_show" },
          null,
          ...getTowerFields("beazley_line"),
          null,
          "esg",
          null,
          "exposure_fx",
          "afb_net_premium_fx",
          "net_rol",
          "actual_ilf",
          null,
          "bpi",
          "benchmark_premium_annualised_100_fx",
          "benchmark_premium_pro_rata_100_fx",
          { field: "coverages/crime/losses_split", shownBy: "cds/rating_factors/risk_info/crime_coverage_required" },
          { field: "coverages/pi/losses_split", shownBy: "cds/rating_factors/risk_info/pi_coverage_required" },
          { field: "coverages/do/losses_split", shownBy: "cds/rating_factors/risk_info/do_coverage_required" },
          "model_ilf",
          null,
          "expected_loss_cost_att",
          "expected_loss_cost_cat",
          "tpi",
          "technical_premium_net_fx",
          "technical_premium_fx",
          null,
          "status.input",
          { field: "coverages/crime/pol_ref", shownBy: "cds/rating_factors/risk_info/crime_coverage_required", minWidth: 200 },
          { field: "coverages/pi/pol_ref", shownBy: "cds/rating_factors/risk_info/pi_coverage_required", minWidth: 200 },
          { field: "coverages/do/pol_ref", shownBy: "cds/rating_factors/risk_info/do_coverage_required", minWidth: 200 },
          { field: "coverages/crime/pol_ref_non_eea", shownBy: "non_cds/rating_summary/crime/pol_ref_non_eea_show", minWidth: 200 },
          { field: "coverages/pi/pol_ref_non_eea", shownBy: "non_cds/rating_summary/pi/pol_ref_non_eea_show", minWidth: 200 },
          { field: "coverages/do/pol_ref_non_eea", shownBy: "non_cds/rating_summary/do/pol_ref_non_eea_show", minWidth: 200 },
          "slip_lead"
        ]} freezeLeft={0} />
      </HX.Section>
    </HX.Page>
  )
}

function getTowerFields(fid, shownBy = null) {
  let tower_fields = [];

  for (let i = 1; i <= max_towers(); i++) {
    let shownByPath = `non_cds/cover_details/tower_${i}_show`;
    if (shownBy) shownByPath = `non_cds/rating_summary/tower_${i}/${shownBy}`;
    tower_fields.push({ field: `tower_${i}/${fid}`, shownBy: shownByPath });
  }

  return tower_fields;
}

export { vw_rating_summary };