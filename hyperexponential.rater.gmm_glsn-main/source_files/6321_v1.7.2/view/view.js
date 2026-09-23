
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_venue_factors } from "view/vw_venue_factors";
import { vw_exposure_details } from "view/vw_exposure_details";
import { vw_triage } from "view/vw_triage";
import { vw_aggregation } from "view/vw_aggregation";
// import { vw_experience_rating } from "view/vw_experience_rating";
import { vw_pricing } from "view/vw_pricing";
import { vw_tech_eo } from "view/vw_tech_eo";
import { vw_cyber } from "view/vw_cyber";
import { vw_umbrella } from "view/vw_umbrella";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";


function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_venue_factors(scale)}
      {vw_exposure_details(scale)}
      {vw_triage(scale)}
      {vw_aggregation(scale)}
      {vw_pricing(scale)}
      {vw_tech_eo(scale)}
      {vw_cyber(scale)}
      {vw_umbrella(scale)}
      {vw_rating_summary(scale)}
      {vw_rate_change(scale)}
      {vw_rationale(scale)}
      {vw_bug_report()}
    </HX.Root >
  );
}

export default HXModel;



