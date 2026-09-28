
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "vw_risk_information";
import { vw_exposure_details } from "vw_exposure_details";
import { vw_rating_summary } from "./vw_rating_summary";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "vw_rationale";

function HXModel() {
  const scale = 1
  return (
    <HX.Root>
      {vw_risk_information(scale)}
      {vw_exposure_details(scale)}
      {vw_rating_summary(scale)}
      {vw_rate_change(scale)}
      {vw_rationale(scale)}
    </HX.Root >
  );
}

export default HXModel;



