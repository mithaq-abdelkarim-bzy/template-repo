/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_experience_rating } from "view/vw_experience_rating";
import { vw_exposure_details } from "view/vw_exposure_details";
import { vw_modifiers } from "view/vw_modifiers";
import { vw_pricing } from "view/vw_pricing";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";

function HXModel() {
  return (
    // Your model code goes here
    <HX.Root
    // keyFields={["hx_core/model_premium", "hx_core/charged_premium", "hx_core/ulr"]}
    >
      {vw_landing_page()}
      {vw_risk_information()}
      {vw_exposure_details()}
      {vw_pricing()}
      {/* {vw_modifiers()} */}
      {vw_experience_rating()}
      {vw_rate_change()}
      {vw_rating_summary()}
      <HX.Page title="Rationale" shownBy="model_state/show_after_landing_page" >
        <HX.Section title="General Comments">
          <HX.Notes field="cds/general_comments" />
        </HX.Section>
        <HX.Section title="Underwriting Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
      </HX.Page>
      {vw_standard_kpi()}
      {/* <HX.Page title="Debug">
        <HX.Section>
          <HX.Collection fields={["debug_num", "debug_num2", "debug_num3", 'debug_str', "manual_premium"]} />
        </HX.Section>
      </HX.Page> */}
      {vw_bug_report()}
    </HX.Root >
  );
}

export default HXModel;
