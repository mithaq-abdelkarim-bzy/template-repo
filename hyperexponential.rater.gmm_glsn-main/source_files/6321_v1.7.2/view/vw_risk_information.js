import * as HX from "hx-model-components";
import { account_scoring } from "view/vw_constants";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information">
      <HX.Section title="Account Details">
        <HX.Pane >
          {/* NOTE  uncomment if rater requires databse_id to be displayed */}
          {/* <HX.Collection fields={["database_id"]} with="cds" horizontal /> */}
          <HX.Collection fields={["hx_core/inception_date", "hx_core/expiry_date", { field: "cds/standard_fields/is_renewal", shownBy: "/model_state/show_rate_change" }]} horizontal />
          <HX.Collection fields={["underwriter", "insured_name"]} with="cds/standard_fields" horizontal />
          <HX.Button task="save_uw_to_pas_reference" title="Save UW Name to PAS Reference" />
          {/* <HX.Collection fields={["underwriter", "benchmark_class"]} with="cds/standard_fields" horizontal /> */}


        </HX.Pane>
      </HX.Section>
      {/* NOTE use the below code if the model does not price multiple layers and it is required to store line size
        brokerage & status on teh risk Information sheet */}
      {/* <HX.Section title="Policy Information" >
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["written_line", "brokerage", "status"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section> */}
      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section>

      <HX.Section title="Rater Selection">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/rater_selection"]} />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Risk Details">
        <HX.Pane flow="right">
          <HX.Table
            title="Operating Region"
            data={["cds/rating_factors/us_international_choice_of_law"]}
            fields={["us_international", "choice_of_law"]}
          />

          < HX.Collection fields={["cds/rating_factors/currency"]} horizontal />

        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={[
            { field: "cds/exposure/aggregate/revenue", shownBy: "cds/exposure/aggregate/revenue_filled" },
            { field: "cds/exposure/aggregate/revenue.mandatory", shownBy: "cds/exposure/aggregate/revenue_empty", infoBy: "cds/exposure/aggregate/revenue_info" }
          ]} />
          <HX.Collection fields={["cds/rating_factors/profit_status"]} />
          <HX.Collection shownBy="cds/glsn_masking"
            fields={["cds/rating_factors/glsn/brag_status"]} />
          <HX.Collection shownBy="cds/gmm_masking"
            fields={["cds/rating_factors/gmm/product_override"]} />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/rating_factors/business_segment"]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table shownBy="cds/gmm_masking"
            title="COB Selection"
            data={["cds/exposure/granular/gmm_product"]}
            fields={["product", "cob_code_description", "cob_class"]}
          />
          <HX.Table shownBy="cds/glsn_masking"
            title="COB Selection"
            data={["cds/exposure/granular/glsn_product"]}
            fields={["product", "cob_code_description"]}
          />
          <HX.Collection shownBy="cds/glsn_masking"
            fields={["cds/rating_factors/glsn/form"]} />
        </HX.Pane>
        <HX.Button task="clear_exposures_task" title="Clear Exposure Inputs (current and prior years): Run if changing COB selection" />
        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/glsn_masking"
            fields={["cds/rating_factors/glsn/supply_chain"]} />
          <HX.Collection shownBy="cds/glsn_masking"
            fields={["cds/rating_factors/glsn/supply_chain_factor"]} />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/glsn_masking"
            fields={["cds/rating_factors/glsn/clinical_trial"]} />
          <HX.Collection shownBy="cds/glsn_masking"
            fields={["cds/rating_factors/glsn/clinical_trial_factor"]} />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Account Scorings">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "cds/rating_factors/total_net_score/value"]} />
          <HX.Collection fields={[
            "cds/rating_factors/account_score"]} />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table
            data={account_scoring()}
            fields={["value", "comment"]}
            title="Account Scorings"
            with="cds/rating_factors/account_scoring"
            kb-interactive
          />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Collection fields={["cds/rating_factors/total_net_score/comment"]} />
          <HX.Collection fields={["cds/rating_factors/account_scoring_details/show_account_scoring"]} />
        </HX.Pane>

        <HX.Pane >
          <HX.Table shownBy="/cds/rating_factors/account_scoring_details/show_account_scoring"
            data={account_scoring()}
            fields={[{ field: "pro_example", maxWidth: 700 }, { field: "neutral_example", maxWidth: 700 }, { field: "con_example", maxWidth: 700 }]}
            title="Account Scoring Key"
            with="cds/rating_factors/account_scoring_details"
            kb-interactive
          />
          <HX.Table shownBy="/cds/rating_factors/account_scoring_details/show_account_scoring"
            data={[{ datum: "cds/rating_factors/account_scoring_details/parameters" }]}
            fields={["five_or_more", "three_or_more", "two_or_fewer", "three_or_more_cons", "five_or_more_cons"]}
            title="Parameters"
            kb-interactive
            filter={"show_row"}
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };


