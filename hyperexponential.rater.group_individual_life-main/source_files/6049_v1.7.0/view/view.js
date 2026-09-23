
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_coverage } from "view/vw_coverage";
import { vw_premium_group } from "view/vw_premium_group";
import { vw_premium_individual } from "view/vw_premium_individual";
import ChoroplethPage from "view/components/choropleth";
import { vw_experience_rating } from "view/vw_experience_rating";
import { vw_cashflow } from "view/vw_cashflow";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_quote_summary } from "view/vw_quote_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";



function HXModel() {
  const scale = 1
  const showAfterLandingPage = "model_state/show_after_landing_page"
  const showGroup = "model_state/show_group"
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale, showAfterLandingPage)}
      {vw_coverage(scale, showGroup)}
      {vw_premium_group(scale)}
      {vw_premium_individual(scale)}
      {ChoroplethPage("lives_by_nation", "nationality")}
      {ChoroplethPage("lives_by_location", "location")}
      {vw_experience_rating()}
      {/* {vw_cashflow()} */}
      {vw_rating_summary(scale, showGroup)}
      {vw_quote_summary(scale, showGroup)}
      {vw_rate_change(scale)}
      {vw_standard_kpi(scale)}
      {vw_bug_report(scale)}
    </HX.Root >
  );
}

export default HXModel;

