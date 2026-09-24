
/* eslint-disable */
import * as HX from "hx-model-components";
import { vw_risk_information } from "view/vw_risk_information";
import { vw_rate_change } from "view/vw_rate_change";
import { vw_rationale } from "view/vw_rationale";
import { vw_landing_page } from "view/vw_landing_page";
import { vw_standard_kpi } from "view/vw_standard_kpi";
import { vw_modelling } from "view/vw_modelling";
import { vw_non_modelled_perils } from "view/vw_non_modelled_perils";
import { vw_pml_curves } from "view/vw_pml_curves";
import { vw_burn_input } from "view/vw_burn_input";
import { vw_burn_output } from "view/vw_burn_output";
import { vw_curve_aggregator } from "view/vw_curve_aggregator";
import { vw_peril_allocation } from "view/vw_peril_allocation";
import { vw_quote } from "view/vw_quote";
import { vw_summary } from "view/vw_summary";
import { vw_simulation } from "view/vw_simulation";
import { vw_simulation_file_formatter } from "view/vw_simulation_file_formatter";
import { vw_aggregates } from "view/vw_aggregates";
import { vw_calculator } from "view/vw_calculator";
import { vw_front_sheet } from "view/vw_front_sheet";
import { vw_send_rate_change } from "view/vw_send_rate_change";
import { vw_pre_bind } from "view/vw_pre_bind";
import { vw_post_bind } from "view/vw_post_bind";
import { vw_rate_change_synergy } from "view/vw_rate_change_synergy";
import { vw_area_codes } from "view/vw_area_codes";
import { vw_tp_notes } from "view/vw_tp_notes";
import { vw_eso } from "view/vw_eso";
import { vw_populate_model } from "view/vw_populate_model";
import { vw_risk_xl_exposure_rating } from "view/vw_risk_xl_exposure_rating";

function HXModel() {
  const scale = 0.7
  return (
    <HX.Root>
      {vw_landing_page(scale)}
      {vw_risk_information(scale)}
      {vw_pml_curves(0.6)}
      {vw_non_modelled_perils(scale)}
      {vw_modelling(scale)}
      {vw_aggregates(scale)}
      {vw_risk_xl_exposure_rating(scale)}
      {vw_burn_input(scale)}
      {vw_burn_output(scale)}
      {vw_curve_aggregator(scale)}
      {vw_quote(scale)}
      {vw_tp_notes(scale)}
      {vw_peril_allocation(scale)}
      {vw_rate_change(scale)}
      {vw_summary(scale)}
      {vw_eso(scale)}
      {vw_simulation(scale)}
      {vw_simulation_file_formatter(scale)}
      {vw_calculator(scale)}
      {vw_rate_change_synergy(scale)}
      {vw_rationale(scale)}
      {vw_area_codes(scale)}
      {vw_pre_bind(scale)}
      {vw_post_bind(scale)}
      {vw_front_sheet(scale)}
      {vw_send_rate_change(scale)}
      {vw_populate_model(scale)}

      <HX.Page title="Something Is Broken" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
        <HX.Section title="Bug Report">
          <HX.Notes field="bug_report_email" />
        </HX.Section>
      </HX.Page>
      {vw_standard_kpi(scale)}
    </HX.Root >
  );
}

export default HXModel;



