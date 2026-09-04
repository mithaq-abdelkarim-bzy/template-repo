
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_policy_level_information } from "view/vw_policy_level_information";
import { vw_experience_rating } from "view/vw_experience_rating";
import { vw_education } from "view/vw_education";
import { vw_non_education } from "view/vw_non_education";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_subsector_rates_display } from "view/vw_subsector_rates_display";
import { vw_city_rates_display } from "view/vw_city_rates_display";
import { vw_claims } from "view/vw_claims";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";


function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_policy_level_information(scale)}
      {vw_education(scale)}
      {vw_non_education(scale)}
      {vw_experience_rating(scale)}
      {vw_rating_summary(scale)}
      {vw_rationale(scale)}
      {vw_rate_change(scale)}
      {/* {vw_rationale(scale)} */}
      {/* {vw_subsector_rates_display(scale)} */}
      {/* {vw_city_rates_display(scale)} */}
      {vw_claims(scale)}
      {/* <HX.Page title="Something Is Broken" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
        <HX.Section title="Bug Report">
          <HX.Notes field="bug_report_email" />
        </HX.Section>
      </HX.Page> */}
      {vw_standard_kpi(scale)}
      {vw_bug_report(scale)}


    </HX.Root >
  );
}

export default HXModel;



