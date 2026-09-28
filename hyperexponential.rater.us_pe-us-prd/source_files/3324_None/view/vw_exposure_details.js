// Importing HX module from "hx-model-components"
import * as HX from "hx-model-components";

const key_names = [
  "occupation",
  "sub_occupation",
  "state",
  "loss_experience",
  "underwriter_judgement",
  "underwriter_judgement_justification",
  "longevity",
  "professional_experience",
  "business_with_written_contract_percentage",
  "business_with_written_contract_revenue",
];
// Function to render the exposure details view
function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={false} viewScale={scale}>      
      <HX.Section
        title="Optional Exposure"
        shownBy="cds/exposure/aggregate/med_mal/hide"
      >
        <HX.With context={{ type: "struct", path: "cds/exposure/aggregate" }}>
          <HX.Pane flow="right">
            <HX.Collection
              fields={[
                { field: "/cds/key_industry/code_name", infoBy: "tooltips/occupation" },
                {
                  field: "/cds/key_industry/sub_occupation/name",
                  infoBy: "tooltips/sub_occupation",
                },
                { field: "state", infoBy: "tooltips/state" },
              ]}
              horizontal
            />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Collection
              fields={[
                {
                  field: "loss_experience",
                  infoBy: "tooltips/loss_experience",
                },
                {
                  field: "longevity/years",
                  infoBy: "tooltips/longevity",
                  shownBy: "longevity/show",
                },
                {
                  field: "professional_experience/years",
                  infoBy: "tooltips/professional_experience",
                  shownBy: "professional_experience/show",
                },
              ]}
              horizontal
            />
            <HX.Pane shownBy="show_loss_experience_empty_panel" />
            <HX.Pane shownBy="show_loss_experience_empty_panel" />
          </HX.Pane>

          <HX.Pane flow="right" shownBy="business_with_written_contract/show">
            <HX.Collection with="business_with_written_contract"
              fields={[
                {
                  field: "percentage",
                  infoBy: "/cds/exposure/aggregate/tooltips/business_with_written_contract_percentage",
                },
                {
                  field: "revenue",
                  infoBy: "/cds/exposure/aggregate/tooltips/business_with_written_contract_revenue",
                },
              ]}
              horizontal
            />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Collection
              fields={[
                {
                  field: "underwriter_judgement",
                  infoBy: "tooltips/underwriter_judgement",
                },
                {
                  field: "underwriter_judgement_justification",
                  infoBy: "tooltips/underwriter_judgement_justification",
                },
              ]}
              horizontal
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>
      <HX.Section
        title="Revenue Tiers"
        shownBy="cds/exposure/aggregate/med_mal/hide"
      >
        <HX.With context={{ type: "struct", path: "cds/exposure" }}>
          <HX.Pane flow="right">
            <HX.Table
              data={[{ datum: "aggregate/revenues" }]}
              fields={[
                "hazard_tier/tier",
                "hazard_tier/business_description",
                "value",
                { field: "type", shownBy: "aggregate/staffing/hide" },
              ]}
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={["aggregate/total_revenue"]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.With>
      </HX.Section>

      <HX.Section
        title="Optional Exposure"
        shownBy="cds/exposure/aggregate/med_mal/show"
      >
        <HX.With context={{ type: "struct", path: "cds/exposure/aggregate" }}>
          <HX.Pane flow="down">
            <HX.Collection
              fields={[
                {
                  field: "state",
                  infoBy: "tooltips/state",
                },
                {
                  field: "loss_experience",
                  infoBy: "tooltips/loss_experience",
                },
              ]}
              horizontal
            />
            <HX.Collection
              fields={[
                {
                  field: "underwriter_judgement",
                  infoBy: "tooltips/underwriter_judgement",
                },
                {
                  field: "underwriter_judgement_justification",
                  infoBy: "tooltips/underwriter_judgement_justification",
                },
              ]}
              horizontal
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>

      <HX.Section title="Med Mal" shownBy="cds/exposure/aggregate/med_mal/show">
        <HX.With context={{ type: "struct", path: "cds/exposure/aggregate" }}>
          <HX.Pane flow="right">
            <HX.Collection with="med_mal" fields={["allied_medical/allied_medical", "social_services/social_services"]} />
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
        shownBy="cds/exposure/aggregate/staffing/show"
      >
        <HX.With
          context={{ type: "struct", path: "cds/exposure/aggregate/staffing" }}
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
