
// # v0.5.1
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_pricing } from "view/vw_pricing";

import { vw_steer_experience_rating_on_levelling } from "view/vw_steer_experience_rating_on_levelling";
import { vw_steer_experience_rating_raw_data } from "view/vw_steer_experience_rating_raw_data";
import { vw_steer_experience_rating_data_formating } from "view/vw_steer_experience_rating_data_formating";
import { vw_steer_experience_rating_raw_data_error } from "view/vw_steer_experience_rating_raw_data_error";
import { vw_steer_experience_rating_processed_claims } from "view/vw_steer_experience_rating_processed_claims";
import { vw_steer_experience_rating_claim_movements } from "view/vw_steer_experience_rating_claim_movements";
import { vw_steer_experience_rating_triangles } from "view/vw_steer_experience_rating_triangles";
import { vw_steer_experience_rating_claim_count } from "view/vw_steer_experience_rating_claim_count";
import { vw_steer_experience_rating_triangles_layers } from "view/vw_steer_experience_rating_triangles_layers";
import { vw_steer_experience_rating_burning_cost_selector } from "view/vw_steer_experience_rating_burning_cost_selector";

import { vw_steer_exposure_rating_curve_descriptions } from "view/vw_steer_exposure_rating_curve_descriptions";
import { vw_steer_exposure_rating_risk_profile_bdx } from "view/vw_steer_exposure_rating_risk_profile_bdx";
import { vw_steer_exposure_rating_limit_average_severity } from "view/vw_steer_exposure_rating_limit_average_severity";

import { vw_healthcare_cat_trial_history } from "view/vw_healthcare_cat_trial_history";
import { vw_healthcare_cat_exposure_territory } from "view/vw_healthcare_cat_exposure_territory";
import { vw_healthcare_cat_pricing } from "view/vw_healthcare_cat_pricing";
import { vw_healthcare_cat_pricing_calculation } from "view/vw_healthcare_cat_pricing_calculation";



import { vw_pricing_selection } from "view/vw_pricing_selection";
import { vw_advanced_features } from "view/vw_advanced_features";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";

import { vw_rationale } from "view/vw_rationale";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";

import timerProfiling from "libraries/model_profiler/view/timerProfilingPage";
import SchemaViewPage from "view/schema_view";

function HXModel() {
  const scale = 0.8
  return (
    <HX.Root>
      {vw_landing_page(scale)}

      {vw_risk_information(scale)}
      {vw_pricing(scale)}

      {vw_steer_experience_rating_on_levelling(scale)}
      {vw_steer_experience_rating_raw_data(scale)}
      {vw_steer_experience_rating_data_formating(scale)}
      {vw_steer_experience_rating_raw_data_error(scale)}
      {vw_steer_experience_rating_processed_claims(scale)}
      {vw_steer_experience_rating_claim_movements(scale)}
      {vw_steer_experience_rating_triangles(scale)}
      {vw_steer_experience_rating_claim_count(scale)}
      {vw_steer_experience_rating_triangles_layers(scale)}
      {vw_steer_experience_rating_burning_cost_selector(scale)}

      {vw_steer_exposure_rating_curve_descriptions(scale)}
      {vw_steer_exposure_rating_risk_profile_bdx(scale)}
      {vw_steer_exposure_rating_limit_average_severity(scale)}

      {vw_healthcare_cat_trial_history(scale)}
      {vw_healthcare_cat_exposure_territory(scale)}
      {vw_healthcare_cat_pricing(scale)}
      {vw_healthcare_cat_pricing_calculation(scale)}



      {vw_pricing_selection(scale)}
      {vw_advanced_features(scale)}


      {vw_rating_summary(scale)}

      {vw_rate_change(scale)}


      {vw_rationale(scale)}
      {vw_standard_kpi(scale)}
      {/* Add bug repot view */}
      {vw_bug_report(scale)}
      {/* <HX.Page title="Something Is Broken" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
        <HX.Section title="Bug Report">
          <HX.Notes field="bug_report_email" />
        </HX.Section>
      </HX.Page> */}
      {SchemaViewPage()}
      {timerProfiling()}

    </HX.Root >
  );
}

export default HXModel;



