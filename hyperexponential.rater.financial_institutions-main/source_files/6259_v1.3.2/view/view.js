/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_exposure_details } from "view/vw_exposure_details";
import { vw_risk_assessment } from "view/vw_risk_assessment";
import { vw_cover_details } from "view/vw_cover_details";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_excel_export } from "view/vw_excel_export";
import { vw_dashboard } from "view/vw_dashboard";
import { vw_standard_kpi } from "view/vw_standard_kpi";

function HXModel() {
  const scale = 1

  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_exposure_details(scale)}
      {vw_risk_assessment(scale)}
      {vw_cover_details(scale)}
      {vw_rating_summary(scale)}
      {vw_rationale(scale)}
      {vw_rate_change(scale)}
      {vw_excel_export(scale)}
      {vw_dashboard(scale)}
      {vw_standard_kpi(scale)}
    </HX.Root>
  );
}

export default HXModel;