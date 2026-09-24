
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_risk_information_v2 } from "view/vw_risk_information_v2";
import { vw_tpi_calculations } from "view/vw_tpi_calculations";
import { vw_pricing } from "view/vw_pricing";
import { vw_pricing_runoff } from "view/vw_pricing_runoff";
import { vw_historical_freq } from "view/vw_historical_freq";
import { vw_admitted } from "view/vw_admitted";
import { vw_admitted_excess } from "view/vw_admitted_excess";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_bug_report } from "../libraries/email_notification/view/vw_bug_report";

function HXModel() {
  const scale = 1
  return (
    //JD?: Don't know how to do the below with a loop through max limit
    <HX.Root keyFields={[
      { field: "cds/technical_premium_1", shownBy: "cds/show_tech_prem_1" },
      { field: "cds/technical_premium_2", shownBy: "cds/show_tech_prem_2" },
      { field: "cds/technical_premium_3", shownBy: "cds/show_tech_prem_3" },
      { field: "cds/technical_premium_4", shownBy: "cds/show_tech_prem_4" },
      { field: "cds/technical_premium_5", shownBy: "cds/show_tech_prem_5" },
      { field: "cds/technical_premium_6", shownBy: "cds/show_tech_prem_6" },
      { field: "cds/admitted/bici/final_premium", shownBy: "cds/admitted/is_bici" },
      { field: "cds/admitted/baic/final_premium", shownBy: "cds/admitted/is_baic" },
      { field: "cds/admitted_excess/adm_exc_model_prem/value", shownBy: "cds/admitted_excess/conditions_met" },
      { field: "cds/admitted/quoted_premium", shownBy: "cds/admitted/is_admitted" }
    ]}>
      {vw_landing_page(scale)}
      {/* {vw_risk_information(scale)} */}
      {vw_risk_information_v2(scale)}
      {vw_pricing_runoff(scale)}
      {vw_pricing(scale)}
      {/*{vw_rating_summary(scale)}*/}
      {vw_admitted(scale)}
      {vw_admitted_excess(scale)}
      {vw_tpi_calculations(scale)}
      {vw_historical_freq(scale)}
      {vw_rate_change(scale)}
      {vw_rationale(scale)}
      {vw_bug_report(scale)}
    </HX.Root >
    //</HX.With>
  );
}

export default HXModel;


