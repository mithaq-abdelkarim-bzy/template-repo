/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_ihs } from "view/vw_ihs";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_countries } from "view/components/vw_countries";
import { vw_exposure } from "view/vw_exposure";
import { vw_construction } from "view/components/vw_construction";
import { vw_pricing } from "view/vw_pricing";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_perils } from "view/vw_perils";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_actuarial } from "view/vw_actuarial";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";


function HXModel() {
  const showAfterLandingPage = "model_state/show_after_landing_page"
  const scale = 1
  return (
    <HX.Root>
      {/* {vw_ihs()} */}
      {vw_landing_page()}
      {vw_risk_information(showAfterLandingPage)}
      {vw_countries(showAfterLandingPage)}
      {vw_exposure(showAfterLandingPage)}
      {vw_pricing("roeCalcs")}
      {vw_pricing("expandedCalcs")}
      {vw_construction()}
      {vw_rating_summary(showAfterLandingPage)}
      {vw_perils(showAfterLandingPage)}
      {vw_rate_change()}
      {vw_rationale()}
      {vw_actuarial()}
      {vw_standard_kpi(scale)}
      {vw_bug_report(scale)}
    </HX.Root >
  );
}

export default HXModel;

