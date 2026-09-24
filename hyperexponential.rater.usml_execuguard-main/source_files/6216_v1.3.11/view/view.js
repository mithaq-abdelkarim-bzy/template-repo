/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_exposure_details } from "view/vw_exposure_details";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_epl_inputs } from "view/vw_epl_inputs";
import { vw_employee_count } from "view/vw_employee_count";
import { vw_fiduciary_inputs } from "view/vw_fiduciary_inputs";
import { vw_pcl_inputs } from "view/vw_pcl_inputs";
import { vw_admitted_excess } from "libraries/admitted_excess_premium/view/vw_admitted_excess";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_excess_rate_change } from "view/vw_excess_rate_change";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";

// const quoted_premium = () => {
//   return (
//     <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
//       <HX.Collection fields={["quoted_premium"]} />
//     </HX.With>
//   )
// };
function HXModel() {
  const scale = 1
  return (
    <HX.Root keyFields={[null, "cds/final_premium_summary/tpi", "cds/final_premium_summary/bpi", { field: "cds/final_premium_summary/final_admitted_term_premium", labelBy: "/non_cds/premium_label" }, null]}>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_exposure_details()}
      {vw_employee_count()}
      {vw_epl_inputs()}
      {vw_fiduciary_inputs()}
      {vw_pcl_inputs()}
      {vw_admitted_excess(scale)}
      {vw_rating_summary(scale)}
      {vw_rate_change()}
      {vw_excess_rate_change()}
      {vw_rationale(scale)}
      {vw_standard_kpi(scale)}
      {vw_bug_report(scale)}

    </HX.Root >
  );
}

export default HXModel;



