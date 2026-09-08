
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_sov_details } from "view/vw_sov_details";
import { vw_report_summary } from "view/vw_report_summary";
import { vw_region_summary } from "view/vw_region_summary";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rationale } from "view/vw_rationale";
import { vw_profit_commission } from "view/vw_profit_commission";
import { vw_triangle_projection } from "view/vw_triangle_projection";
import { vw_rms } from "view/vw_rms";

function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_sov_details(scale)}
      {vw_report_summary(scale)}
      {vw_region_summary(scale)}
      {vw_rating_summary(scale)}
      {vw_rationale(scale)}
      {vw_profit_commission(scale)}
      {vw_triangle_projection(scale)}
      {vw_rms(scale)}
    </HX.Root >
  );
}

export default HXModel;



