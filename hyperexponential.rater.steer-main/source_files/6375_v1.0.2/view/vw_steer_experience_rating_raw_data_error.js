// # v0.5.1
import * as HX from "hx-model-components";
import { convertToFieldObjects, node_name_list_with_suffix, convertToDataObjects } from "view/vw_utilities";


const fieldTypeFields = [
  "requirement",
  "column_name",
  "cell_address",
  "value_found",
]

const valueWithinRange = [
  "requirement",
  "column_name",
  "cell_address",
  "value_found",
]

const rawDataErrorFields = [
  "requirement",
  "column_name",
  "cell_address",
  "value_found",
]


function vw_steer_experience_rating_raw_data_error(scale) {
  return (
    // <HX.Page title="Raw Data Error" fullWidth={true} viewScale={0.8} shownBy="model_state/show_after_landing_page"></HX.Page>
    <HX.Page title="Raw Data Error" fullWidth={true} viewScale={0.8} shownBy="model_state/is_steer_raw_data_not_validated">
      <HX.With context={{ type: "struct", path: "cds/steer/experience_rating" }}>
        <HX.Section title="Raw Data Error">

          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Table
                title="Accepted Missing Value"
                with="raw_data_error"
                data={[
                  "accepted_missing_value",
                ]}
                fields={[
                  ...convertToFieldObjects(rawDataErrorFields, 250)
                ]}

                kb-interactive
              />
            </HX.Pane>
            <HX.Pane>
              <HX.Table
                title="Field Type"
                with="raw_data_error"
                data={[
                  "field_type",
                ]}
                fields={[
                  ...convertToFieldObjects(fieldTypeFields, 250)
                ]}

                kb-interactive
              />
            </HX.Pane>
            <HX.Pane>
              <HX.Table
                title="Value Within Range"
                with="raw_data_error"
                data={[
                  "value_within_range"
                ]}
                fields={[
                  ...convertToFieldObjects(valueWithinRange, 250)
                ]}
                kb-interactive
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.With>
      {/* {vw_experience_rating_detail()} */}
    </HX.Page >
  )
}


export { vw_steer_experience_rating_raw_data_error };