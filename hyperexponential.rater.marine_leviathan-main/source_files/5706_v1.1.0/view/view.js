
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_exposure_details } from "view/vw_exposure_details";
import { vw_rating_summary2 } from "view/vw_rating_summary2";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_standard_kpi } from "view/vw_standard_kpi";

function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_exposure_details(scale)}
      {vw_rating_summary2(scale)}
      {vw_rate_change(scale)}
      {vw_rationale(scale)}
      {vw_standard_kpi(scale)}
      {/* <HX.Page title="Something Is Broken" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
        <HX.Section title="Bug Report">
          <HX.Notes field="bug_report_email" />
        </HX.Section>
      </HX.Page> */}
    </HX.Root >
  );
}

export default HXModel;



