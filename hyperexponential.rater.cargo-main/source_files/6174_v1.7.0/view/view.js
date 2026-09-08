
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_cargo } from "view/vw_cargo";
import { vw_cargo_cyber } from "view/vw_cargo_cyber";
import { vw_specie } from "view/vw_specie";
import { vw_conloss } from "view/vw_conloss";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";


function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_risk_information(scale)}
      {vw_cargo(scale)}
      {vw_cargo_cyber(scale)}
      {vw_specie(scale)}
      {vw_conloss(scale)}
      {vw_rating_summary(scale)}
      {vw_rate_change(scale)}
      {vw_rationale(scale)}
      {vw_standard_kpi(scale)}
      {vw_bug_report(scale)}
    </HX.Root >
  );
}

export default HXModel;



