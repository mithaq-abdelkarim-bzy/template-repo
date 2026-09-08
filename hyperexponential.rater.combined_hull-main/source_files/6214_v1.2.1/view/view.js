
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_vessels } from "view/vw_vessels";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_war } from "view/vw_war";
import { vw_iv } from "view/vw_iv";
import { vw_loh } from "view/vw_loh";
import { vw_ship_building } from "view/vw_ship_building";
import { vw_output_summary } from "./vw_output_summary";
import { vw_modelling } from "view/vw_modelling";
import { vw_vessel_analysis } from "view/vw_vessel_analysis";
import { vw_portfolio_analysis } from "view/vw_portfolio_analysis";
import { vw_experience_rating } from "./vw_experience_rating";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";

function HXModel() {
  const scale = 1.5
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_vessels(scale)}
      {vw_iv(scale)}
      {vw_war(scale)}
      {vw_loh(scale)}
      {vw_ship_building(scale)}
      {vw_experience_rating(scale)}
      {vw_rating_summary(scale)}
      {vw_rate_change(scale)}
      {vw_modelling(scale)}
      {vw_vessel_analysis(scale)}
      {vw_output_summary(scale)}
      {vw_portfolio_analysis(scale)}
    </HX.Root >
  );
}

export default HXModel;



