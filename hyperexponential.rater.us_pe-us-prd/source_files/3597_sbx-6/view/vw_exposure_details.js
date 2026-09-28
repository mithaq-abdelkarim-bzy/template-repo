// Importing HX module from "hx-model-components"
import * as HX from "hx-model-components";

// Function to render the exposure details view
function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} viewScale={scale}>
      <HX.Section
        title="Optional Exposure"
        shownBy="cds/rating_factors/med_mal/hide"
      >
        <HX.With context={{ type: "struct", path: "cds/rating_factors" }}>
          <HX.Pane flow="right">
            <HX.Collection
              fields={[
                { field: "/cds/key_industry/code_name", infoBy: "/cds/tooltips/occupation" },
                {
                  field: "/cds/key_industry/sub_occupation/name",
                  infoBy: "/cds/tooltips/sub_occupation",
                },
                { field: "/cds/standard_fields/insured_state_or_province", infoBy: "/cds/tooltips/state" },
              ]}
              horizontal
            />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Collection
              fields={[
                {
                  field: "/cds/rating_factors/loss_experience",
                  infoBy: "/cds/tooltips/loss_experience",
                },
                {
                  field: "longevity/years",
                  infoBy: "/cds/tooltips/longevity",
                  shownBy: "longevity/show",
                },
                {
                  field: "professional_experience/years",
                  infoBy: "/cds/tooltips/professional_experience",
                  shownBy: "professional_experience/show",
                },
              ]}
              horizontal
            />
            <HX.Pane shownBy="show_loss_experience_empty_panel" />
            <HX.Pane shownBy="show_loss_experience_empty_panel" />
          </HX.Pane>

          <HX.Pane flow="right" shownBy="business_with_written_contract/show">
            <HX.Collection
              fields={[
                {
                  field: "business_with_written_contract/percentage",
                  infoBy: "/cds/tooltips/business_with_written_contract_percentage",
                },
                {
                  field: "business_with_written_contract/revenue",
                  infoBy: "/cds/tooltips/business_with_written_contract_revenue",
                },
              ]}
              horizontal
            />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Collection with="/cds/modifiers"
              fields={[
                {
                  field: "underwriter_judgement",
                  infoBy: "/cds/tooltips/underwriter_judgement",
                },
                {
                  field: "underwriter_judgement_justification",
                  infoBy: "/cds/tooltips/underwriter_judgement_justification",
                },
              ]}
              horizontal
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>
      <HX.Section
        title="Revenue Tiers"
        shownBy="cds/rating_factors/med_mal/hide"
      >
        <HX.With context={{ type: "struct", path: "cds" }}>
          <HX.Pane flow="right">
            <HX.Table
              data={[{ datum: "rating_factors/revenues" }]}
              fields={[
                "hazard_tier/tier",
                "hazard_tier/business_description",
                "value",
                { field: "type", shownBy: "rating_factors/show_revenue_type" },
              ]}
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={["exposure/aggregate/total_revenue"]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.With>
      </HX.Section>

      <HX.Section
        title="Optional Exposure"
        shownBy="cds/rating_factors/med_mal/show"
      >
        <HX.With context={{ type: "struct", path: "cds/rating_factors" }}>
          <HX.Pane flow="down">
            <HX.Collection
              fields={[
                {
                  field: "/cds/standard_fields/insured_state_or_province",
                  infoBy: "/cds/tooltips/state",
                },
                {
                  field: "loss_experience",
                  infoBy: "/cds/tooltips/loss_experience",
                },
              ]}
              horizontal
            />
            <HX.Collection with="/cds/modifiers"
              fields={[
                {
                  field: "underwriter_judgement",
                  infoBy: "/cds/tooltips/underwriter_judgement",
                },
                {
                  field: "underwriter_judgement_justification",
                  infoBy: "/cds/tooltips/underwriter_judgement_justification",
                },
              ]}
              horizontal
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>

      <HX.Section title="Med Mal" shownBy="cds/rating_factors/med_mal/show">
        <HX.With context={{ type: "struct", path: "cds/rating_factors" }}>
          <HX.Pane flow="right">
            <HX.Collection with="med_mal" fields={["allied_medical/allied_medical_type", "social_services/social_services_type"]} />
            <HX.Collection with="med_mal"
              fields={["allied_medical/exposure_measure", "social_services/exposure_measure"]}
            />
            <HX.Collection with="med_mal"
              fields={["allied_medical/exposure_type", "social_services/exposure_type"]}
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection
              fields={[
                {
                  field: "professional_experience/years",
                  labelBy:
                    "professional_experience/med_mal_professional_experience_label"
                },
              ]}
            />
            <HX.Collection fields={["professional_experience/factor"]} />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Collection
              fields={[
                {
                  field: "longevity/years",
                  labelBy: "longevity/med_mal_longevity_label"
                },
              ]}
            />
            <HX.Collection fields={["longevity/factor"]} />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Collection fields={["med_mal/total_credit_or_debit"]} />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Table
              data={[{ datum: "med_mal/endorsements" }]}
              fields={["endorsement", "factor"]}
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={["med_mal/total_endorsement"]} />
          </HX.Pane>
        </HX.With>
      </HX.Section>
      <HX.Section
        title="Staffing Risk Type"
        shownBy="cds/rating_factors/staffing/show"
      >
        <HX.With
          context={{ type: "struct", path: "cds/rating_factors/staffing" }}
        >
          <HX.Pane flow="down">
            <HX.Pane flow="right">
              <HX.Collection fields={["permanent"]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={["peo"]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={["temporary"]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={["total"]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Pane>
        </HX.With>
      </HX.Section>
    </HX.Page>
  );
}

// Exporting the vw_exposure_details function
export { vw_exposure_details };
