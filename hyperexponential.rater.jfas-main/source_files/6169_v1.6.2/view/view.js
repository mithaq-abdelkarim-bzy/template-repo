/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_exposure_input } from "view/vw_exposure_input";
import { vw_fine_art } from "view/vw_fine_art";
import { vw_jewellers_block } from "view/vw_jewellers_block";
import { vw_general_specie } from "view/vw_general_specie";
import { vw_cash_in_transit } from "view/vw_cash_in_transit";
import { vw_experience_rating } from "view/vw_experience_rating";
// import { vw_final_selections_and_summary } from "view/deprecated_vw_final_selections_and_summary";
import { vw_final_selections_and_summary } from "view/vw_final_selections_and_summary";
import { vw_rationale } from "view/vw_rationale";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";

function HXModel() {
  const scale = 1
  return (
    // Why doesn't scale work for risk_information and rationale 
    <HX.Root>
      {vw_landing_page()}
      {vw_risk_information()}
      {vw_exposure_input()}
      {vw_fine_art()}
      {vw_jewellers_block()}
      {vw_general_specie()}
      {vw_cash_in_transit()}
      {vw_experience_rating()}
      {vw_final_selections_and_summary()}
      {vw_rationale()}
      {vw_rate_change()}
      {vw_standard_kpi()}
      {vw_bug_report()}
    </HX.Root >
  );
}



export default HXModel;
