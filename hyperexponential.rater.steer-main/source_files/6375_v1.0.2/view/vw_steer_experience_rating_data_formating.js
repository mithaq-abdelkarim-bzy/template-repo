// # v0.5.1
import * as HX from "hx-model-components";
import { convertToFieldObjects, node_name_list_with_suffix, convertToDataObjects } from "view/vw_utilities";

const rawDataFields = [
  "field",
  "field_name",
  "description",
  "mandatory_column",
  "specify_column",
  "accept_missing",
  "field_type",
  "value_within_range",
  "replace_missing_with_default"
]

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

const dataMappingTableData = [
  ...node_name_list_with_suffix("field", "_", 18)
]

const rawDataColumnNames = [
  ...node_name_list_with_suffix("column", "_", 109)
]

function vw_steer_experience_rating_data_formating(scale) {
  return (
    <HX.Page title="Data Format" fullWidth={true} viewScale={0.8} shownBy="model_state/show_steer_experience_rating">
      <HX.With context={{ type: "struct", path: "cds/steer/experience_rating" }}>
        <HX.Section title="Misc Parameters">

          <HX.Pane flow="right" reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Pane flow="down">
                <HX.Collection fields={
                  [
                    { "field": "target_year", "infoBy": "target_year_info" },
                    { "field": "closed_indicator", "infoBy": "closed_indicator_info" },
                    // { "field": "data_layout", "infoBy": "data_layout_info" },

                  ]}
                  syncColumnWidthsKey="target_year"
                  with="misc_parameters"
                />
              </HX.Pane>
            </HX.Pane>

            <HX.Pane ratio={1}>
              <HX.Table
                // title="Other Fields"
                with="other_fields"
                data={[
                  { datum: "fvy", elementInfoBy: "description" },
                  { datum: "lvy", elementInfoBy: "description" },
                  { datum: "data_as_at_date", elementInfoBy: "description" },
                  { datum: "coverage_basis", elementInfoBy: "description" },
                  { datum: "bcost_measure", elementInfoBy: "description" },
                ]}
                fields={[
                  // "description",
                  "value",
                ]}
                kb-interactive
                syncColumnWidthsKey="field"
              // transpose
              />
            </HX.Pane>

            <HX.Pane ratio={1}>
              <HX.Button task="steer_clear_raw_data_task" title="Clear Raw Data" />
              {/* <HX.Button task="steer_validate_raw_data_task" title="Validate Raw Data" /> */}
              <HX.Button task="steer_format_raw_data_task" title="Format Raw Data" />
              {/* <HX.Button task="steer_tri_triangles_setup_task" title="Create Triangles" /> */}
            </HX.Pane>

            <HX.Pane ratio={2}>
              <HX.Notes field="raw_data_error/pre_val_err_messages.warning" shownBy="raw_data_error/show_pre_val_err_messages" />
            </HX.Pane>

          </HX.Pane>
        </HX.Section>
      </HX.With>
      <HX.With context={{ type: "struct", path: "cds/steer/experience_rating" }}>
        <HX.Section title="Data Mapping & Other Fields">
          <HX.Pane>
            {/* <HX.Pane ratio={1} > */}
            <HX.Pane flow="right" ratio={4} reflow={false}>
              <HX.Pane ratio={3}>
                <HX.Pane>
                  <HX.Table
                    title="Raw Data Mapping"
                    with="data_mapping"
                    data={[
                      ...convertToDataObjects(dataMappingTableData, { elementLabelBy: "field" })

                    ]}
                    fields={[
                      ...convertToFieldObjects(rawDataFields, 250)
                    ]}
                    kb-interactive
                  // syncColumnWidthsKey="field"
                  />
                </HX.Pane>
                <HX.Pane flow="right">
                  <HX.Pane></HX.Pane>
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="right" ratio={2} reflow={false}>
                <HX.Pane>

                  <HX.Table
                    title="Raw Data Column Name"
                    data={[
                      {
                        "datum": "/steer/experience_rating/raw_data_column_names",
                        "width": 350
                      }
                    ]}
                    fields={[
                      ...rawDataColumnNames
                    ]}
                    kb-interactive
                    transpose
                  />
                </HX.Pane>

                <HX.Pane>
                  <HX.Table
                    title="Display"
                    with="/steer/experience_rating/column_display"
                    data={[
                      "reference",
                      "claimant",
                      "insured",
                      "status",
                      "incident_date",
                      "report_date",
                      "closed_date",
                      "incident_year",
                      "policy_year",
                      "closed_year",
                      "policy_limit",
                      "policy_excess",

                      // "paid",
                      // "incurred",

                      // "paid_expenses",
                      // "incurred_expenses",

                      // "paid_claim_ind",
                      // "inc_claim_ind",

                      "incurred_claims",
                      "inflated_claims",
                      "incurred_capped",
                      "trended_claim",
                      "trended_expenses",


                      // "ri_claim_ind",
                      // "ri_claim_ind_closed",
                      "claim_ranking",
                      "row_number",

                      "ri_claim",
                      "ri_claim_on_levelled",
                      "ri_claim_count",
                      "ri_claim_count_on_levelled",

                    ]}
                    fields={[
                      { field: "show", maxWidth: 250 }
                    ]}
                    kb-interactive
                  />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>

          </HX.Pane>
        </HX.Section>
      </HX.With>


    </HX.Page >
  )
}


export { vw_steer_experience_rating_data_formating };