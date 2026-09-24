
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_risk_code_library } from "view/vw_risk_code_library";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_rate_change } from "view/vw_rate_change"
import { vw_assumed_deductions } from "view/vw_assumed_deductions"
import { vw_policy_level_data } from "view/vw_policy_level_data"
import { vw_claim_level_data } from "view/vw_claim_level_data"
import { vw_bp_projections } from "view/vw_bp_projections"

import { vw_risk_code_composition } from "view/vw_risk_code_composition";
import { vw_portfolio_profile } from "view/vw_portfolio_profile";
import { vw_inflation } from "view/vw_inflation";
import { vw_cat } from "view/vw_cat";
import { vw_premium_and_limit_profile } from "view/vw_premium_and_limit_profile";

import { vw_anti_selection } from "view/vw_anti_selection";
import { vw_uncertainty } from "view/vw_uncertainty";
import { vw_pc } from "view/vw_pc";
import { vw_pc_bbt } from "view/vw_pc_bbt";
import { vw_rating_summary } from "view/vw_rating_summary";
import { vw_rating_summary_bbt } from "view/vw_rating_summary_bbt";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_rationale } from "view/vw_rationale";
import timerProfiling from "libraries/model_profiler/view/timerProfilingPage";

import { vw_own_experience } from "view/vw_own_experience";
import { vw_lloyds_projections } from "view/vw_lloyds_projections";
import { vw_beazley_projections } from "view/vw_beazley_projections";
import { vw_rating_summary_case_priced } from "view/vw_rating_summary_case_priced";
import { vw_section_ref_allocation } from "view/vw_section_ref_allocation";
import { vw_bug_report } from "../libraries/email_notification/view/vw_bug_report";
import SchemaViewPage from "view/schema_view";


function HXModel() {
  const scale = 1
  return (
    <HX.Root
      keyFields={[
        { field: "non_cds/global_fields/lobs_error_msg.warning", shownBy: "non_cds/global_fields/is_lobs_msg_shown" },
        { field: "non_cds/global_fields/pc_error_msg.warning", shownBy: "non_cds/global_fields/is_pc_msg_shown" },
        { field: "non_cds/global_fields/oe_error_msg.warning", shownBy: "non_cds/global_fields/is_oe_msg_shown" },
        { field: "non_cds/global_fields/mismatched_lob_error_msg_global.warning", shownBy: "non_cds/global_fields/mismatched_lob_table_length" },
        { field: "non_cds/global_fields/projections_error_msg.warning", shownBy: "non_cds/global_fields/is_projections_msg_shown" },
        { field: null, shownBy: "non_cds/global_fields/is_lobs_msg_shown" },
        { field: null, shownBy: "non_cds/global_fields/is_pc_msg_shown" },
        { field: null, shownBy: "non_cds/global_fields/mismatched_lob_table_length" },
        { field: null, shownBy: "non_cds/global_fields/is_projections_msg_shown" },
        { field: null, shownBy: "non_cds/global_fields/is_there_global_message" }
      ]}
      keyFieldsViewScale={1}>

      {/* {vw_mtx(scale)} */}
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_section_ref_allocation(scale)}
      {vw_risk_code_library(scale)}
      {vw_policy_level_data(scale)}
      {vw_claim_level_data(scale)}
      {vw_risk_code_composition(scale)}
      {vw_assumed_deductions(scale)}
      {vw_rate_change(scale)}
      {vw_inflation(scale)}
      {vw_premium_and_limit_profile(scale)}
      {vw_cat(scale)}
      {vw_portfolio_profile(scale)}

      {vw_own_experience(scale)}
      {vw_lloyds_projections(scale)}
      {vw_beazley_projections(scale)}

      {vw_bp_projections(scale)}
      {vw_anti_selection(scale)}
      {vw_uncertainty(scale)}
      {vw_pc(scale)}

      {/* pb requested disabled 12-2-2026 */}
      {/* {vw_pc_bbt(scale)} */}

      {vw_rating_summary(scale)}
      {vw_rating_summary_bbt(scale)}
      {vw_rating_summary_case_priced(scale)}
      {vw_standard_kpi(scale)}
      {vw_rationale(scale)}

      {SchemaViewPage()}
      {timerProfiling()}
      {vw_bug_report()}
    </HX.Root >
  );
}

export default HXModel;









