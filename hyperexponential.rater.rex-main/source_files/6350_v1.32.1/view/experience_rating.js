import * as HX from "hx-model-components";
import { MAX_LAYERS } from "view/constants";
import { render_notifications } from "view/results_tables";

// function to dynamically create looped layer fields in claims table based on max layers defined in model
function loop_claim_fields(num_layers) {
  const objects = [];

  // This is the actual loop, going through and creating the objects and saving them to the objects list
  for (let n = 1; n <= num_layers; n++) {
    objects.push(
      { field: null, shownBy: `/experience_rating/claims_show_layer_${n}` },
      { field: `deductible_to_use_layer_${n}`, shownBy: `/experience_rating/claims_show_layer_${n}` },
      { field: `limit_layer_${n}`, shownBy: `/experience_rating/claims_show_layer_${n}` },
      { field: `excess_layer_${n}`, shownBy: `/experience_rating/claims_show_layer_${n}` },
      { field: `cl_developed_total_incurred_layer_${n}`, shownBy: `/experience_rating/claims_show_layer_${n}` }
    )
  }

  // Return the list of objects so it can be unpacked, just like using multiple view files
  return objects
}

// function to dynamically calculated layer experience rating columns based on max layers defined in model
function loop_peril_summ_fields() {
  const objects = [];
  const perils = ["fire", "named_windstorm", "scs", "flood", "quake", "wildfire"]
  const fields = ["num_claims", "unadj_sum_claims", "sum_claims"]

  // This is the actual loop, going through and creating the objects and saving them to the objects list
  for (let i = 0; i < fields.length; i++) {
    objects.push(
      { field: null }
    )
    for (let j = 0; j < perils.length; j++) {
      objects.push(
        { field: `${fields[i]}_${perils[j]}` }
      )
    }
  }

  // Return the list of objects so it can be unpacked, just like using multiple view files
  return objects
}

// function to dynamically calculated layer experience rating columns based on max layers defined in model
function loop_layer_exp_rating_fields(num_layers) {
  const objects = [];
  // commented out as removing Cat component from experience rating for now
  // const cat_status = ['non_cat', 'cat']
  const cat_status = ['non_cat']
  const fields = [/*"cl_developed_layer",*/ "ult_layer", "ult_rate_layer"]

  // This is the actual loop, going through and creating the objects and saving them to the objects list
  for (let i = 0; i < fields.length; i++) {
    for (let j = 0; j < cat_status.length; j++) {
      objects.push(
        { field: null, shownBy: "/experience_rating/use_experience_rating_full" }
      )
      for (let n = 1; n <= num_layers; n++) {
        objects.push(
          { field: `${cat_status[j]}_${fields[i]}_${n}`, shownBy: `/experience_rating/calculation_show_layer_${n}` }
        )
      }
    }
  }

  // Return the list of objects so it can be unpacked, just like using multiple view files
  return objects
}

// function to dynamically calculated layer experience rating columns based on max layers defined in model
function loop_layer_exp_rating_rate_fields(num_layers) {
  const objects = [];
  // commented out as removing Cat component from experience rating for now
  // const cat_status = ['non_cat', 'cat']
  const cat_status = ['non_cat']
  const fields = ["ult_rate_layer"]

  // This is the actual loop, going through and creating the objects and saving them to the objects list
  for (let i = 0; i < fields.length; i++) {
    for (let j = 0; j < cat_status.length; j++) {
      objects.push(
        { field: null, shownBy: "/experience_rating/use_experience_rating_full" }
      )
      for (let n = 1; n <= num_layers; n++) {
        objects.push(
          { field: `${cat_status[j]}_${fields[i]}_${n}`, shownBy: `/experience_rating/calculation_show_layer_${n}` }
        )
      }
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

function experience_rating() {
  return (
    <HX.Page title="Experience Rating" fullWidth={true} shownBy="model_state/show_after_landing_page">
      {render_notifications()}
      <HX.Section title="" collapsible={false}>
        <HX.Pane flow="right">
          <HX.Pane />
          <HX.Button title="Run Rater" task="run_schedule_rater_task" />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Initial Selections">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "experience_rating/claims_available",
            { field: "experience_rating/claims_fgu", shownBy: "experience_rating/claims_available" }
          ]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Basic Experience Rating" shownBy="experience_rating/use_experience_rating_basic">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "experience_rating/experience_rating_basic/clean_years",
            "experience_rating/experience_rating_basic/experience_adjustment",
          ]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Button task="apply_experience_adjustment_task" title="Populate Non-Cat Experience Adjustment" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Claims Data" shownBy="experience_rating/show_claims_input_table">
        <HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              { field: "experience_rating/claims_net_of_deductible", shownBy: "experience_rating/show_claims_input_table" },
              { field: "experience_rating/show_to_layer_fields", shownBy: "experience_rating/use_experience_rating_full" },
            ]} />
            {/*Button actually just pulls exchange rates for claims but has a misleading title to ensure underwriters press it*/}
            <HX.Button task="pull_exchange_rate_claim_data_task" title="Push Claims to Experience Rating calculation" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table
            data={["claims"]}
            fields={[
              // claim inputs
              "claim_id",
              "claim_made_date",
              "claim_status",
              "cause_of_loss",
              "deductible",
              "incurred_claims",
              "currency",

              // claim outputs
              "use_claim",
              "is_cat",
              null,
              "estimated_yoa",
              "total_incurred_clm_curr",
              // "clm_to_slip_fx_rate",
              // "total_incurred",
              "inflated_total_incurred",
              null,
              "claims_development",
              // "development_method",
              // "developed_inflated_total_incurred",
              // "sublimit",
              ...loop_claim_fields(MAX_LAYERS())
            ]}
            with="experience_rating"
            title="Claims"
            maxListVisibleRows={10}
            kb-interactive
          /*transpose*/
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Experience Rating" shownBy="experience_rating/show_claims_input_table">
        <HX.Pane>
          <HX.Section title="Inputs" shownBy="experience_rating/show_claims_input_table" defaultCollapsed={false}>
            <HX.Notes field="experience_rating/input_instructions" />
            <HX.Table
              data={[{ datum: "experience_rating/experience_table", width: 150, elementLabelBy: "str_yoa" }]}
              fields={[
                // policy history inputs
                // "yoa", // stripping out yoa as it's now in the column headers 
                "exposure",
                "exposure_inflation",
                "exposure_onlevelled",
                { field: "premium", shownBy: "experience_rating/use_experience_rating_agg" },
                { field: "premium_rate_change", shownBy: "experience_rating/use_experience_rating_agg" },
                { field: "premium_rate_adjusted", shownBy: "experience_rating/use_experience_rating_agg" },
                null,
                "include_year"
              ]}
              transpose
              kb-interactive
              dynamic
              syncColumnWidthsKey="experience_rating_calc"
            />
          </HX.Section>
          <HX.Section title="Claims Summary" shownBy="experience_rating/show_claims_input_table" defaultCollapsed={true}>
            <HX.Table
              data={[{ datum: "experience_rating/experience_table", width: 150, elementLabelBy: "str_yoa" }]}
              fields={[
                // claims summarised
                ...loop_peril_summ_fields()
              ]}
              // title="Claims"
              transpose
              kb-interactive
              dynamic
              syncColumnWidthsKey="experience_rating_calc"
            />
          </HX.Section>
          <HX.Section title="Experience Rating Calculation" shownBy="experience_rating/show_claims_input_table" defaultCollapsed={true}>
            <HX.Table
              data={[{ datum: "experience_rating/experience_table", width: 150, elementLabelBy: "str_yoa" }]}
              fields={[
                // calculated experience metrics based on type of claims
                //for non FGU claims information
                { field: "loss_ratio", shownBy: "experience_rating/use_experience_rating_agg" },
                // benhcmark ULR for FGU
                { field: "non_cat_ulr", shownBy: "experience_rating/use_experience_rating_full" },
                // commented out as removing Cat component from experience rating for now
                // { field: "cat_ulr", shownBy: "experience_rating/use_experience_rating_full" },
                //FGU fields
                { field: "claims_development", shownBy: "experience_rating/use_experience_rating_full" },
                { field: "development_method", shownBy: "experience_rating/use_experience_rating_full" },

                // by layer fields for FGU claims
                ...loop_layer_exp_rating_fields(MAX_LAYERS())
              ]}
              transpose
              kb-interactive
              dynamic
              syncColumnWidthsKey="experience_rating_calc"
            />
          </HX.Section>
          <HX.Section title="Results" shownBy="experience_rating/show_claims_input_table" defaultCollapsed={false}>
            <HX.Table
              data={[{ datum: "experience_rating/experience_table", width: 150, elementLabelBy: "str_yoa" }]}
              fields={[
                //for non FGU claims information
                { field: "loss_ratio", shownBy: "experience_rating/use_experience_rating_agg" },
                // by layer fields for FGU claims
                ...loop_layer_exp_rating_rate_fields(MAX_LAYERS()),
                null,
                // fields to weight by year
                { field: "exposure_weight", shownBy: "experience_rating/show_weights" },
                { field: "decay_weight", shownBy: "experience_rating/show_weights" },
                { field: "development_weight", shownBy: "experience_rating/show_weights" },
                // rescale weights to sum to 100%
                { field: "overall_score", shownBy: "experience_rating/show_weights" },
                "weight_to_year"
              ]}
              transpose
              kb-interactive
              dynamic
              syncColumnWidthsKey="experience_rating_calc"
            />
            {/* toggle to show additional weight details*/}
            <HX.Pane flow="right">
              <HX.Collection fields={["experience_rating/show_weights"]}>
              </HX.Collection>
              <HX.Pane></HX.Pane>
              <HX.Pane></HX.Pane>
            </HX.Pane>
          </HX.Section>

          {/*results*/}
          <HX.Pane>
            <HX.Table
              data={[
                ...loop_results_summary(MAX_LAYERS())
              ]}
              fields={[
                { field: "non_cat_elr_non_cat_prem" },
                { field: "non_cat_expected_loss_ratio", shownBy: "use_experience_rating_agg" },
                { field: "model_non_cat_loss_ratio", shownBy: "use_experience_rating_agg" },
                { field: "non_cat_loss_rate", shownBy: "use_experience_rating_full" },
                // commented out as removing Cat component from experience rating for now
                // { field: "cat_loss_rate", shownBy: "use_experience_rating_full" },
                // { field: "rms_loss_rate", shownBy: "use_experience_rating_full" },
                // { field: "combined_loss_rate", shownBy: "use_experience_rating_full" },
                "non_cat_expected_losses",
                "model_non_cat_expected_losses",
                "cred_weight",
                "experience_adjustment"
              ]}
              with="experience_rating"
              title="Summary"
              filter={"filter"}
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane />
            <HX.Button task="apply_experience_adjustment_task" title="Populate Non-Cat Experience Adjustment" />
            <HX.Pane />
          </HX.Pane>

        </HX.Pane>
      </HX.Section >


    </HX.Page >
  )
}

export { experience_rating };