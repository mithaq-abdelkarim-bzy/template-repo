// # v0.5.1
import * as HX from "hx-model-components";

import { convertToFieldObjects } from "view/vw_utilities";

const claimsMovementsFields = [
  "claim_ranking",
  "claim_reference",
  "yoa",
  "status",
  null,
  "last_year",
  "this_year",
  "incurred_movement",
  null,
  "last_year_on_levelled",
  "this_year_on_levelled",
  "incurred_movement_on_levelled"
]

function vw_steer_experience_rating_claim_movements(scale) {
  return (
    // <HX.Page title="Claim Movements" fullWidth={true} viewScale={0.8} shownBy="model_state/show_after_landing_page">
    <HX.Page title="Claim Movements" viewScale={0.8} shownBy="model_state/show_steer_experience_rating">

      <HX.With context={{ type: "struct", path: "cds/steer/experience_rating" }}>
        <HX.Section title="Claim Movements">
          <HX.Pane flow="right">

            <HX.Table
              data={[
                "claim_movements"
              ]}
              fields={[
                ...convertToFieldObjects(claimsMovementsFields, 150)
              ]}
              title="Claim Movements"
              kb-interactive
              // with="processed_claims"
              syncColumnWidthsKey="field"
            />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page >
  )
}



export { vw_steer_experience_rating_claim_movements };