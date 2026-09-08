/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_exposure_details } from "view/vw_exposure_details";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_standard_kpi, vw_standard_kpi_rater } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";
import { vw_admitted_excess } from "libraries/admitted_excess_premium/view/vw_admitted_excess";
import { vw_exposure_change_calculation } from "view/vw_exposure_change_calc";


function HXModel() {
  return (
    // Your model code goes here
    <HX.Root>
      {vw_landing_page()}
      {vw_risk_information()}
      {vw_exposure_details()}
      {vw_rate_change()}
      {vw_rating_summary()}
      <HX.Page title="Rationale" shownBy="model_state/show_after_landing_page">
        <HX.Section title="General Comments">
          <HX.Notes field="cds/general_comments" />
        </HX.Section>
        <HX.Section title="Underwriting Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
      </HX.Page>
      {vw_standard_kpi_rater()}
      {vw_standard_kpi()}
      {/* vw_admitted_excess() */}
      {vw_bug_report()}
    </HX.Root >
  );
}

export default HXModel;
