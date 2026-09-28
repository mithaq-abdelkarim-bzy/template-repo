import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

// function to dynamically create looped layer fields in claims table based on max layers defined in model
function loop_claim_fields(num_layers) {
  const objects = [];

  // This is the actual loop, going through and creating the objects and saving them to the objects list
  for (let n = 1; n <= num_layers; n++) {
    objects.push(
      { field: null, shownBy: `/cds/experience_rating/claims_show_layer_${n}` },
      { field: `deductible_to_use_layer_${n}`, shownBy: `/cds/experience_rating/claims_show_layer_${n}` },
      { field: `limit_layer_${n}`, shownBy: `/cds/experience_rating/claims_show_layer_${n}` },
      { field: `excess_layer_${n}`, shownBy: `/cds/experience_rating/claims_show_layer_${n}` },
      { field: `cl_developed_total_incurred_layer_${n}`, shownBy: `/cds/experience_rating/claims_show_layer_${n}` }
    )
  }

  // Return the list of objects so it can be unpacked, just like using multiple view files
  return objects
}

// function to dynamically calculated layer experience rating columns based on max layers defined in model
function loop_layer_exp_rating_fields(num_layers) {
  const objects = [];
  const fields = ["cl_developed_layer", "ult_layer", "ult_rate_layer"]

  // This is the actual loop, going through and creating the objects and saving them to the objects list
  for (let i = 0; i < fields.length; i++) {
    objects.push(
      { field: null, shownBy: "/cds/experience_rating/use_experience_rating_full" }
    )
    for (let n = 1; n <= num_layers; n++) {
      objects.push(
        { field: `${fields[i]}_${n}`, shownBy: `calculation_show_layer_${n}` }
      )
    }
  }

  // Return the list of objects so it can be unpacked, just like using multiple view files
  return objects
}


// function to create list of layer experience rating final output
function loop_results_summary(num_layers) {
  const objects = [];

  // This is the actual loop, going through and creating the objects and saving them to the objects list
  for (let n = 1; n <= num_layers; n++) {
    objects.push(
      { datum: `summary_layer_${n}` }
    )
  }

  // Return the list of objects so it can be unpacked, just like using multiple view files
  return objects
}


function vw_experience_rating() {
  return (
    <HX.Page title="Experience Rating" fullWidth={true} >
      <HX.With context={{ type: "struct", path: "cds/experience_rating" }}>

        <HX.Section title="Initial Selections">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "claims_available",
              { field: "claims_fgu", shownBy: "claims_available" }
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Basic Experience Rating" shownBy="use_experience_rating_basic">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "experience_rating_basic/clean_years",
              "experience_rating_basic/experience_adjustment",
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Claims Data" shownBy="show_claims_input_table">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                { field: "claims_net_of_deductible", shownBy: "show_claims_input_table" },
                { field: "show_to_layer_fields", shownBy: "use_experience_rating_full" },
                { field: "use_triangle", shownBy: "use_experience_rating_full" },
                { field: "use_output_triangle", shownBy: "use_experience_rating_full" },
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table
              data={["claims"]}
              fields={[
                // claim inputs
                "claim_id",
                "loss_date",
                "claim_made_date",
                "claim_status",
                "claim_close_date",
                "deductible",
                "paid_claims",
                "incurred_claims",
                "transaction_date",
                "currency",

                // claim outputs
                "use_claim",
                null,
                "estimated_yoa",
                "total_incurred_clm_curr",
                "clm_to_slip_fx_rate" /*hide*/,
                "total_incurred",
                "inflated_total_incurred",
                null,
                "claims_development" /*hide*/,
                "development_method" /*hide*/,
                "developed_inflated_total_incurred" /*hide*/,
                ...loop_claim_fields(max_layers())
              ]}
              title="Claims"
              maxListVisibleRows={10}
              kb-interactive
            /*transpose*/
            />
          </HX.Pane>
        </HX.Section>

        {/* sample input triangle */}
        <HX.Section title="Triangle Parameters" shownBy="use_triangle">
          <HX.Pane>
            <HX.TriangleParameters title="Triangle Parameters" triangle="triangle" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Triangle Data" shownBy="use_triangle">
          <HX.Pane>
            <HX.TriangleData title="Triangle Data" triangle="triangle" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Triangle Development Factors" shownBy="use_triangle">
          <HX.Pane>
            <HX.TriangleDevFactors title="Loss Development Factors" triangle="triangle" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Triangle Averages" shownBy="use_triangle">
          <HX.Pane>
            <HX.TriangleAverages title="Triangle Averages" triangle="triangle" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Experience Rating" shownBy="show_claims_input_table">
          <HX.Pane>
            <HX.Table
              data={[{ datum: "experience_table", width: 150 }]}
              fields={[
                // policy history inputs
                "yoa", "exposure", "exposure_onlevelled", "premium", "premium_rate_adjusted",
                // claims summarised
                null, "agg_num_claims", "agg_sum_claims", "include_year", //"include_year_2", placeholder for alternative weightied inclusion
                // calculated experience metrics based on type of claims
                null,

                //for non FGU claims information
                { field: "loss_ratio", shownBy: "use_experience_rating_agg" },
                // benhcmark ULR for FGU
                { field: "ulr", shownBy: "use_experience_rating_full" },
                "claims_development",
                //FGU fields
                { field: "alternate_claims_development", shownBy: "use_experience_rating_full" },
                { field: "development_method", shownBy: "use_experience_rating_full" },

                // by layer fields for FGU claims
                ...loop_layer_exp_rating_fields(max_layers()),

                // fields to weight by year
                null,
                { field: "exposure_weight", shownBy: "show_weights" },
                { field: "decay_weight", shownBy: "show_weights" },
                { field: "development_weight", shownBy: "show_weights" },
                // rescale weights to sum to 100%
                { field: "overall_score", shownBy: "show_weights" },
                "weight_to_year"]}
              title="Claims"
              transpose
              kb-interactive
              dynamic
            />

            {/* toggle to show additional weight details*/}
            <HX.Pane flow="right">
              <HX.Collection fields={["show_weights"]}>
              </HX.Collection>
              <HX.Pane></HX.Pane>
              <HX.Pane></HX.Pane>
            </HX.Pane>

            {/* non FGU claims results*/}
            {/* <HX.Pane flow="right" shownBy="use_experience_rating_agg">
              <HX.Collection fields={[
                "expected_loss_ratio"
              ]} />
              <HX.Collection fields={[
                "expected_losses"
              ]} />
              <HX.Pane></HX.Pane>
            </HX.Pane> */}

            {/* FGU claims results*/}
            <HX.Pane>
              <HX.Table
                data={[
                  ...loop_results_summary(max_layers())
                ]}
                fields={[
                  { field: "expected_loss_ratio", shownBy: "use_experience_rating_agg" },
                  { field: "loss_rate", shownBy: "use_experience_rating_full" },
                  "expected_losses"
                ]}
                title="Summary"
                filter={"filter"}
              />
              <HX.Pane />
            </HX.Pane>

          </HX.Pane>
        </HX.Section>

        {/* sample output triangle */}
        <HX.Section title="Triangle Parameters" shownBy="use_output_triangle">
          <HX.Pane>
            <HX.TriangleParameters title="Triangle Parameters" triangle="output_triangle" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Triangle Data" shownBy="use_output_triangle">
          <HX.Pane>
            <HX.TriangleData title="Triangle Data" triangle="output_triangle" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Triangle Development Factors" shownBy="use_output_triangle">
          <HX.Pane>
            <HX.TriangleDevFactors title="Loss Development Factors" triangle="output_triangle" />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Triangle Averages" shownBy="use_output_triangle">
          <HX.Pane>
            <HX.TriangleAverages title="Triangle Averages" triangle="output_triangle" />
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}


export { vw_experience_rating };