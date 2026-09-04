
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_exposure_details } from "view/vw_exposure_details";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_eso } from "view/vw_eso";
import { vw_rationale } from "view/vw_rationale";
import { vw_generate_doc } from "view/vw_generate_doc";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";

function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_landing_page()}
      {vw_risk_information()}
      {vw_exposure_details()}
      {vw_rating_summary()}
      {vw_eso()}
      {vw_rationale()}
      {vw_generate_doc()}
      {vw_bug_report()}
      {/* <HX.Page title="To Report a Bug Report" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
        <HX.Section title="Bug Report">
          <HX.Notes field="bug_report_email" />
        </HX.Section>
      </HX.Page> */}
      {/* {vw_standard_kpi(scale)} */}
    </HX.Root >
  );
}

export default HXModel;



