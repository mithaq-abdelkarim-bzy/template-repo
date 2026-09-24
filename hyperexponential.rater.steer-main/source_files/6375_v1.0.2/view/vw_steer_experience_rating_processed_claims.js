// # v0.5.1
import * as HX from "hx-model-components";
import { experience_rating_max_years, max_layers, } from "view/vw_constants";
import { convertToFieldObjects, node_name_list_with_suffix } from "view/vw_utilities";

function vw_steer_experience_rating_processed_claims(scale) {
  return (
    <HX.Page title="Experience" fullWidth={true} viewScale={0.8} shownBy="model_state/show_steer_experience_rating">
      <HX.With context={{ type: "struct", path: "cds/steer/experience_rating" }}>
        <HX.Section title="Processed Claims">
          <HX.Pane flow="right">

            <HX.Table
              data={[
                "processed_claims"
              ]}
              fields={[

                { field: "reference", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/reference/show" },
                { field: "claimant", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/claimant/show" },
                { field: "insured", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/insured/show" },
                { field: "status", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/status/show" },
                { field: "incident_date", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/incident_date/show" },
                { field: "report_date", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/report_date/show" },
                { field: "closed_date", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/closed_date/show" },
                { field: "incident_year", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/incident_year/show" },
                { field: "policy_year", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/policy_year/show" },
                { field: "closed_year", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/closed_year/show" },
                { field: "policy_limit", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/policy_limit/show" },
                { field: "policy_excess", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/policy_excess/show" },
                null,

                { field: "incurred_claims", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/incurred_claims/show" },
                { field: "inflated_claims", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/inflated_claims/show" },
                { field: "incurred_capped", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/incurred_capped/show" },
                { field: "trended_claim", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/trended_claim/show" },
                { field: "trended_expenses", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/trended_expenses/show" },
                { field: "claim_ranking", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/claim_ranking/show" },
                { field: "row_number", maxWidth: 150, shownBy: "/steer/experience_rating/column_display/row_number/show" },
                null,

                ...convertToFieldObjects(riClaimsLayerFields, 150, riClaimsLayerShownBy),
                ...convertToFieldObjects(riClaimsLayerOnLevelledFields, 150, riClaimsLayerShownBy),
                null,
                ...convertToFieldObjects(riClaimsCountLayerFields, 150, riClaimsLayerShownBy),
                ...convertToFieldObjects(riClaimsCountLayerOnLevelledFields, 150, riClaimsLayerShownBy),
                null,
                ...generateFieldNames(experience_rating_max_years()),
              ]}
              title="Processed Claims"
              kb-interactive
            // with="processed_claims"
            // syncColumnWidthsKey="field"
            />


          </HX.Pane>
        </HX.Section>
      </HX.With>

    </HX.Page >
  )
}
const riClaimsLayerFields = [
  ...node_name_list_with_suffix("ri_claim_layer", "_", max_layers())
]
const riClaimsLayerOnLevelledFields = [
  ...node_name_list_with_suffix("ri_claim_on_levelled_layer", "_", max_layers())
]
const riClaimsCountLayerFields = [
  ...node_name_list_with_suffix("ri_claim_count_layer", "_", max_layers())
]
const riClaimsCountLayerOnLevelledFields = [
  ...node_name_list_with_suffix("ri_claim_count_on_levelled_layer", "_", max_layers())
]
const riClaimsLayerShownBy = [
  ...node_name_list_with_suffix("/model_state/show_layer", "_", max_layers())
]
const trianglesDataYearShownBy = [
  ...node_name_list_with_suffix("/model_state/show_data_year", "_", experience_rating_max_years())
]
function repeatArray(baseArray, repetitions) {
  let repeatedArray = [];
  for (let i = 0; i < repetitions; i++) {
    repeatedArray = repeatedArray.concat(baseArray);
  }
  return repeatedArray;
}


function generateFieldNames(experienceRatingMaxYears, maxWidth = 150) {
  const LIST = [
    "Paid DY ",
    "Incurred DY ",
    "Paid Expenses DY ",
    "Incurred Expenses DY ",
    "Paid Claim Indemnity DY ",
    "Incurred Claim Indemnity DY ",
    "Paid Claim Count DY ",
    "Incurred Claim Count DY ",

  ];
  const result = [];

  for (const prefix of LIST) {

    for (let year = 1; year <= experienceRatingMaxYears + 1; year++) {
      // Convert prefix to snake_case
      const snakePrefix = prefix.toLowerCase()
        .replace(/ /g, "_")
        .replace(/-/g, "_");
      const formatted_year = year.toString().padStart(2, '0'); // Format as 01, 02, ..., 100, 101,
      const fieldName = `${snakePrefix}${formatted_year}`;
      // result.push(fieldName);
      result.push({
        field: fieldName,
        maxWidth,
        shownBy: `/model_state/show_data_year_${formatted_year}`,
      });
    }
    result.push(null); // Add null before each prefix's years are processed
  }
  // Remove the last null if it exists
  if (result.length > 0 && result[result.length - 1] === null) {
    result.pop();
  }
  return result;
}

export { vw_steer_experience_rating_processed_claims };