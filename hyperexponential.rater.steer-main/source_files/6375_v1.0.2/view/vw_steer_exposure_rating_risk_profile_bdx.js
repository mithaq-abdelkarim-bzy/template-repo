// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";
import { createLayersList, createLayersListNoFgu, convertToFieldObjects, node_names_with_prefix } from "view/vw_utilities";

const layer_fields = [
  "expo_pct",
  "expo_premium",
  "excess",
  "sum_insured",
  "ilf_xs_and_xm",
  "ilf_xs_and_xl",
  "ilf_xs_and_lmt",
  "ilf_xs",
  "pr_pct",
  "pr_net_premium"
]

const layersAssumptionsFields = [
  "limit",
  "excess",
  "pricing_selection/risk_profile_bdx/pure_rate"
]

const riskProfileFields = [

  "insured",

  "limit",
  "excess",
  "net_premium",
  "share",
  "linkage",
  "exposure",

  "currency",
  "fx_rate_to_usd",

  null,
  "parametric",
  "curve_type",
  "first_loss",
  "first_loss_factor",
  "param_1",
  "param_2",
  "param_3",
  "param_4",

  null,
  ...node_names_with_prefix("layer", "_", max_layers(), "/", layer_fields)
]

function vw_steer_exposure_rating_risk_profile_bdx(scale) {
  return (
    <HX.Page title="Risk Profile Bdx" fullWidth={true} viewScale={scale} shownBy="model_state/show_steer_risk_bdx">
      <HX.With context={{ type: "struct", path: "cds/steer/exposure_rating/risk_profile_bdx" }} >
        <HX.Section title="Risk Profile Bdx">
          <HX.Pane flow="down">

            <HX.Pane flow="right">
              <HX.Pane flow="right" ratio={2}>

                <HX.Pane ratio={1}>
                  <HX.Collection fields={["exposure_lr", "exposure_profile_gross_premium", "no_of_risk", "curve"]} />
                  <HX.Notes field="message" shownBy="/model_state/is_bdx_input_issue" />

                </HX.Pane>

                <HX.Pane ratio={1}>

                  <HX.Table
                    title="Layers Assumptions"
                    with="/cds"

                    data={[
                      "layers"
                      // ...createLayersListNoFgu(max_layers())
                    ]}

                    fields={[
                      ...convertToFieldObjects(layersAssumptionsFields, 170)

                    ]}
                    kb-interactive={true}
                  />
                </HX.Pane>

              </HX.Pane>

              <HX.Pane ratio={2}>
                <HX.Pane>

                  <HX.Table
                    title="Layers"
                    with="/cds"
                    data={[{ datum: "layers", width: 220 }]}
                    fields={[
                      "risk_profile_bdx/pro_rata_premium",
                      // "risk_profile_bdx/exposure_premium",
                      { field: "risk_profile_bdx/exposure_premium", infoBy: "/model_state/info_by_risk_bdx_exposure_prem" },
                      "risk_profile_bdx/glr_pick",
                      "risk_profile_bdx/exposure_lr",
                      "risk_profile_bdx/el_at_loss_ratio",
                      "risk_profile_bdx/rate_on_npi",
                      "risk_profile_bdx/loss_premium",
                    ]}
                    transpose
                  />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
            <HX.Pane>
              <HX.Table
                title="Risk profiles"
                data={[
                  "risk_profiles"
                ]}
                fields={[

                  { field: "cob", maxWidth: 350 },
                  { field: "curve", maxWidth: 350 },
                  ...convertToFieldObjects(riskProfileFields, 150)
                ]}
                // freezeLeft={10}
                dynamic
                kb-interactive
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_steer_exposure_rating_risk_profile_bdx };