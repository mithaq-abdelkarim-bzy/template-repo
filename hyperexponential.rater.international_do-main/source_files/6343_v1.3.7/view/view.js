
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_risk_assessment } from "view/vw_risk_assessment";
import { vw_exposure_details } from "view/vw_exposure_details";
// import { vw_experience_rating } from "view/vw_experience_rating";
import { vw_pricing } from "view/vw_pricing";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rating_summary_mmp } from "view/vw_rating_summary_mmp";
// import { vw_rating_summary2 } from "view/vw_rating_summary2";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_dashboard } from "view/vw_dashboard";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";

import { vw_landing_page } from "view/vw_landing_page";

function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_exposure_details(scale)}
      {vw_risk_assessment(scale)}
      {/* {vw_pricing(scale)} */}
      {/* {vw_experience_rating(scale)} */}
      {vw_rating_summary(scale)}
      {vw_rating_summary_mmp(scale)}
      {/* {vw_rating_summary2(scale)} */}
      {vw_rate_change(scale)}
      {vw_rationale(scale)}
      {vw_standard_kpi(scale)}
      {vw_dashboard(scale)}
      {vw_bug_report()}
    </HX.Root >
  );
}

export default HXModel;



