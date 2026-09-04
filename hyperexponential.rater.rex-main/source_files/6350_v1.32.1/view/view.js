/* eslint-disable */
import * as HX from "hx-model-components";
import { policy_info } from "view/policy_info";
import { deductible } from "view/deductible";
import { additional_coverages } from "view/additional_coverages";
import { schedule } from "view/schedule";
import { experience_rating } from "view/experience_rating";
import { rating_summary, by_peril_summary } from "view/rating_summary";
import { underwriter_appetite } from "./underwriter_appetite";
import { climate } from "view/climate";
import { rate_change } from "view/rate_change";
import { quote_docs } from "view/quote_docs";
import { account_segmentation } from "view/account_segmentation";
import { rationale } from "view/rationale";
import { landing_page } from "view/landing_page";
import { vw_bug_report } from "libraries/email_notification/view/vw_bug_report";

function HXModel() {
  return (
    // Your model code goes here
    <HX.Root>
      {landing_page()}
      {policy_info()}
      {deductible()}
      {additional_coverages()}
      {schedule()}
      {experience_rating()}
      {rating_summary()}
      {account_segmentation()}
      {by_peril_summary()}
      {underwriter_appetite()}
      {climate()}
      {rationale()}
      {rate_change()}
      {quote_docs()}
      {vw_bug_report()}
    </HX.Root>
  );
}

export default HXModel;
