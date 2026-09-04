
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_rms } from "view/vw_rms";
import { vw_actuarial } from "view/vw_actuarial";
import { vw_triangle_projection } from "view/vw_triangle_projection";
import { vw_claim_summary } from "view/vw_claim_summary";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_profit_commission } from "view/vw_profit_commission";
import { vw_rationale } from "view/vw_rationale";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";
/* 
import ImageComponent from "components/image";
import { vw_exposure_details } from "view/vw_exposure_details";
import { vw_experience_rating } from "view/vw_experience_rating";
import { vw_pricing } from "view/vw_pricing";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
*/

function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_rating_summary(scale)}
      {vw_rationale(scale)}
      {vw_claim_summary(scale)}
      {vw_rms(scale)}
      {vw_profit_commission(scale)}
      {vw_triangle_projection(scale)}
      {vw_actuarial(scale)}
      {/*vw_exposure_details(scale)}
      {vw_pricing(scale)}
      {vw_experience_rating(scale)}
      {vw_rating_summary(scale)}
      {vw_rate_change(scale)}
      {vw_rationale(scale)*/}
      {vw_bug_report()}
    </HX.Root >
  );
}

export default HXModel;



