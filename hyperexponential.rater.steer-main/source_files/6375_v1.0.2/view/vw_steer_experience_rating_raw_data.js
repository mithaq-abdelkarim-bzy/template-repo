// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers, max_raw_data_columns } from "view/vw_constants";

import { convertToFieldObjects, node_name_list_with_suffix } from "view/vw_utilities";

const rawDataInputFields = [...node_name_list_with_suffix("column", "_", max_raw_data_columns())]

function vw_steer_experience_rating_raw_data(scale) {
  return (
    <HX.Page title="Raw Data" fullWidth={true} viewScale={0.8} shownBy="model_state/show_steer_experience_rating">
      <HX.With context={{ type: "struct", path: "cds/steer/experience_rating" }}>

        <HX.Section title="Raw Data Input">

          <HX.Pane>
            <HX.Collection fields={["on_levelling/raw_data_comment", null, null]} horizontal />
            <HX.Pane flow="right">
              <HX.Pane ratio={1}>
                <HX.Button task="steer_clear_raw_data_task" title="Clear Raw Data" />
              </HX.Pane>
              <HX.Pane ratio={3}>
              </HX.Pane>
            </HX.Pane>



            <HX.Table
              title="Raw Data"
              data={[{ datum: "raw_data" }
              ]}
              fields={[
                ...convertToFieldObjects(rawDataInputFields, 250)
              ]}
              kb-interactive
            />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page >
  )
}

export { vw_steer_experience_rating_raw_data };