
// v0.5.0
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_exposure_details } from "view/vw_exposure_details";
import { vw_territory } from "view/vw_territory";
import { vw_client_details_lawyers } from "view/vw_client_details_lawyers";
import { vw_client_details_AEC } from "view/vw_client_details_AEC";
import { vw_claims } from "view/vw_claims";
import { vw_experience_rating } from "view/vw_experience_rating";
import { vw_experience_rating_2 } from "view/vw_experience_rating_2";
import { vw_experience_rating_3 } from "view/vw_experience_rating_3";
import { vw_pricing } from "view/vw_pricing";
import { vw_pricing_coverages } from "view/vw_pricing_coverages";
import { vw_pricing_coverages_insured_asset } from "view/vw_pricing_coverages_insured_asset";
import { vw_pricing_layers_insured_asset } from "view/vw_pricing_layers_insured_asset";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rating_summary2 } from "view/vw_rating_summary2";
import { vw_rating_summary_coverages } from "view/vw_rating_summary_coverages";
import { vw_rating_summary_coverages_insured_asset } from "view/vw_rating_summary_coverages_insured_asset";
import { vw_rating_summary_layers_insured_asset } from "view/vw_rating_summary_layers_insured_asset";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rate_change_coverages } from "view/vw_rate_change_coverages";
import { vw_rate_change_coverages_insured_asset } from "view/vw_rate_change_coverages_insured_asset";
import { vw_rate_change_layers_insured_asset } from "view/vw_rate_change_layers_insured_asset";
import { vw_rationale } from "view/vw_rationale";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";


function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_exposure_details(scale)}
      {vw_territory(scale)}
      {vw_client_details_lawyers(scale)}
      {vw_client_details_AEC(scale)}
      {vw_claims(scale)}
      {/* {vw_experience_rating_2(scale)} */}
      {vw_experience_rating_3(scale)}
      {vw_pricing(scale)}
      {vw_pricing_coverages(scale)}
      {vw_pricing_coverages_insured_asset(scale)}
      {vw_pricing_layers_insured_asset(scale)}
      {/* {vw_rating_summary(scale)} */}
      {/* {vw_rating_summary2(scale)} */}
      {/* {vw_rating_summary_coverages(scale)}
      {vw_rating_summary_coverages_insured_asset(scale)}
      {vw_rating_summary_layers_insured_asset(scale)} */}
      {vw_rate_change(scale)}
      {vw_rate_change_coverages(scale)}
      {vw_rate_change_coverages_insured_asset(scale)}
      {vw_rate_change_layers_insured_asset(scale)}
      {vw_rationale(scale)}
      {vw_standard_kpi(scale)}
      {/* Add bug repot view */}
      {vw_bug_report(scale)}
      {/* <HX.Page title="Something Is Broken" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
        <HX.Section title="Bug Report">
          <HX.Notes field="bug_report_email" />
        </HX.Section>
      </HX.Page> */}
    </HX.Root >
  );
}

export default HXModel;


