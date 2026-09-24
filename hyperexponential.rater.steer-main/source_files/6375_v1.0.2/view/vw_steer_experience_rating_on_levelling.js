// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers, max_raw_data_columns } from "view/vw_constants";

import { convertToFieldObjects, node_name_list_with_suffix } from "view/vw_utilities";

const exposureAssumptionsFields = [
  null,
  "exposure",
  "annual_rate_change",
  "rate_change_index",
  "exposure_on_level",
  "claims_inflation",
  "inflation_index"
  , null
  // , ...node_name_list_with_suffix("exposure_adjusted_layer", "_", max_layers())
]

const exposureAdjustedFields = [
  ...node_name_list_with_suffix("exposure_adjusted_layer", "_", max_layers())
]
const exposureAdjustedShownBy = [
  ...node_name_list_with_suffix("/model_state/show_layer", "_", max_layers())
]

// const rawDataInputFields = [...node_name_list_with_suffix("column", "_", max_raw_data_columns())]

function vw_steer_experience_rating_on_levelling(scale) {
  return (
    <HX.Page title="On-Levelling" viewScale={0.8} shownBy="model_state/show_steer_experience_rating">
      <HX.With context={{ type: "struct", path: "cds/steer/experience_rating" }}>
        <HX.Section title="On Level Assumptions">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection fields={[
                "measure",
                "/cds/risk_information/inception_year",
                // "raw_data_comment",

              ]}
                syncColumnWidthsKey="measure"
                with="on_levelling"

              />
            </HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
          <HX.Pane>

            <HX.Table
              title="Exposure Assumptions"
              with="on_levelling"
              data={[{ datum: "exposure_assumptions", elementLabelBy: "display_yoa" }
              ]}
              fields={[
                ...convertToFieldObjects(exposureAssumptionsFields, 150),
                ...convertToFieldObjects(exposureAdjustedFields, 150, exposureAdjustedShownBy),
              ]}
              kb-interactive

            />
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_steer_experience_rating_on_levelling };