// # v0.5.1
import * as HX from "hx-model-components";
import { convertToFieldObjects } from "view/vw_utilities";

const loss_cost_fields = [
  "limit",
  "excess",
  "expected_loss",
  "expected_aad.read_only",
  "loss_corridor_loss_cost.read_only",
  "expected_losses_after_loss_sensitive_features",
]

const renumeration_fields = [
  "limit",
  "excess",
  // "no_reinstatement",
  "number_of_rips",
  "brokerage_inc_swing",
  "ceding_commission",
  "bkg_gross_or_net",
  "upfront_premium_gross_100",
  "upfront_premium_net_100",
  null,
  "expected_reinstatement_factor.read_only",
  "expected_ncb_pct.read_only",
  "profit_commission.read_only",
  "swing_premium.read_only",
  null,
  "expected_premium_paid_gross_100",
  "expected_premium_paid_net_100",
  null,
  "quoted_premium_100",
  "quoted_premium_net_100",
]

const params_fields = [
  "default",
  "overwrite",
  "selected"
]

function vw_advanced_features(scale) {
  return (
    <HX.Page title="Advanced Features" fullWidth={true} viewScale={scale} shownBy="model_state/show_rater_priced">

      <HX.Section title="Advanced Features">
        <HX.Pane>
          <HX.Pane flow="right" reflow={false}>
            <HX.Pane ratio={5}>
              <HX.Table
                title="Loss Cost Features - Loss Impact"
                with="cds"
                data={[
                  // { datum: "layers", width: 250 }
                  "layers"
                ]}
                fields={[
                  ...convertToFieldObjects(loss_cost_fields)
                ]}

                kb-interactive
              //dynamic // filter and sort
              // transpose
              />
            </HX.Pane>

            <HX.Pane ratio={2}>
              <HX.Pane>
                <HX.Table
                  title="COB Assumptions"
                  with="cds/pricing_selection"
                  data={[
                    "pareto_parameters",
                    "odf_parameters",
                  ]}
                  fields={[
                    ...convertToFieldObjects(params_fields)
                  ]}
                  kb-interactive
                  rowHeaderSettings={{ width: 170 }}
                />
              </HX.Pane>
              <HX.Pane>
                <HX.Notes field="/model_state/pure_premium_error_message" shownBy="/model_state/is_pure_premium_not_calculated" />

                <HX.Button task="advanced_features_task" title="Calculate Advanced Features" />
              </HX.Pane>


            </HX.Pane>
          </HX.Pane>
          <HX.Pane>
            <HX.Table
              title="Remuneration Features - Premium Impact"
              with="cds"
              data={[
                // { datum: "layers", width: 250 }
                "layers"
              ]}
              fields={[
                ...convertToFieldObjects(renumeration_fields)
              ]}

              kb-interactive
            //dynamic // filter and sort
            // transpose
            />
          </HX.Pane>

        </HX.Pane>


      </HX.Section>
    </HX.Page>
  )
}

export { vw_advanced_features };