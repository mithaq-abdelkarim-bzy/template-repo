/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_airlines } from "view/vw_airlines";
import { vw_al_rating } from "view/vw_al_rating";
import { vw_ga } from "view/vw_ga";
import { vw_ga_rating } from "view/vw_ga_rating";
import { vw_aircraft_summary } from "view/vw_aircraft_summary";
import { vw_experience_rating } from "view/vw_experience_rating";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";


function HXModel() {
  const showAfterLandingPage = "model_state/show_after_landing_page"
  // const showAirlines = "model_state/pressed_airlines_task"
  // const showGA = "model_state/pressed_ga_task"
  const showAirlines = "model_state/show_airlines"
  const showGA = "model_state/show_ga"
  return (
    <HX.Root keyFields={[{ field: "model_state/inconsistent_product_msg", shownBy: "model_state/is_product_inconsistent" }]}>
      {vw_landing_page()}
      {vw_risk_information(showAfterLandingPage)}
      {vw_experience_rating()}
      {vw_airlines(showAirlines)}
      {vw_ga(showGA)}
      {vw_al_rating()}
      {vw_ga_rating("total_loss_freq")}
      {vw_ga_rating("hull_rating")}
      {vw_ga_rating("pax_rating")}
      {vw_ga_rating("tpl_rating")}
      {vw_aircraft_summary()}
      {vw_rating_summary(showAfterLandingPage)}
      {vw_rate_change()}
      {vw_bug_report(1)}
    </HX.Root >
  );
}

export default HXModel;

