import * as HX from "hx-model-components";
import { render_notifications } from "view/results_tables";

function quote_docs() {
  return (
    <HX.Page title="Policy Document" fullWidth={true} shownBy="quote_documents/show_page">
      {render_notifications()}
      <HX.Section title="BPro RPA">
        <HX.Pane>
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "layer",
              ]} with="quote_documents" />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Collection fields={[
                "insured_name",
                "underwriter",
                "tria",
                "equipment_breakdown",
                "insured_from",
                "insured_until",
              ]} with="quote_documents/bpro_outputs" />
              <HX.Collection fields={[
                "commission",
                "office",
                "bpro_ref",
                "global_rater_id",
                "limit",
                "location_per_schedule",
              ]} with="quote_documents/bpro_outputs" />
              <HX.Collection fields={[
                "num_locs",
                "tiv",
                "itv_per_sqft",
                "prem_rates",
                "peril",
                "min_earned_pct",
              ]} with="quote_documents/bpro_outputs" />
              <HX.Collection fields={[
                "bpro_outputs/min_earned",
                "bpro_outputs/george_occupancy",
                "bpro_outputs/bpro_occupancy",
                "bpro_outputs/risk_class",
                "schedule_received_date",
                { field: "mailing_address", shownBy: "manuscript_flag" },
              ]} with="quote_documents" />
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Table data={["covered_property", "additional_covered_property"]}
                fields={["option_1", "option_2", "option_3"]}
                title="Covered Property"
                with="quote_documents/covered_property" />
              <HX.Pane />
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Collection fields={[
                "property_only",
                "equipment_breakdown",
                "tria",
                "total_exc_fees",
                "inspection_fees",
              ]} with="quote_documents/premium"
                title="Gross Premium - USD, Beazley Share" />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Collection fields={[
                "loss_run",
                "favourable_inspection",
              ]} with="quote_documents/subjectivities"
                title="Subjectives" />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Table
                data={[
                  "fixed_sublimits/ordinance_and_law",
                  "fixed_sublimits/wind",
                  "fixed_sublimits/wind_2",
                  "fixed_sublimits/quake",
                  "fixed_sublimits/quake_2",
                  "fixed_sublimits/flood",
                  "other_sublimits"
                ]}
                fields={["val", "comments"]}
                title="Sublimits"
                with="quote_documents" />
              <HX.Pane />
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Table
                data={["deductibles"]}
                fields={["peril", "ded_pct", "ded_min", "comments"]}
                title="Deductibles"
                with="quote_documents" />
              <HX.Pane />
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Notes field="deductibles_override_comment" with="quote_documents"
                title="Deductibles override comment" />
              <HX.Pane />
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Table data={["pd", "bi"]}
                fields={["settlement", "pct"]}
                title="Coinsurance/Val"
                with="quote_documents/coinsurance" />
              <HX.Pane />
            </HX.Pane>

            {endorsement_table()}

            <HX.Notes
              field="quote_documents/quote_comments"
              title="Quote Comments"
            />
          </HX.Pane>

          <HX.Pane>
            <HX.Button task="generate_quote_doc_task" title="Generate Quote Document" />
            <HX.File field="quote_documents/document" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page >

  )
}

function endorsement_table() {
  return (
    <HX.Pane flow="right">
      <HX.Table
        with="quote_documents/endorsements"
        data={[
          "additional_covered_property",
          "additional_property_not_covered",
          "burglary_or_robbery_safeguards",
          "civil_or_military_authority_ext",
          "condition_of_coverage",
          "condo_maintenance_fees",
          "condo_association_coverage",
          "endorcements_condo_maintenance_fees",
          "damage_to_roof_structure_limitation",
          "fire_and_explosion",
          "first_tier_wind_counties_and_parishes",
          "hurricane_minimum_earned_premium",
          "ingress_egress_extension",
          "limitations_on_coverage_for_roof_surfacing",
          "ordinance_or_law_increased_period_of_restoration",
          "outdoor_property_extension",
          "prior_loss_clause",
          "property_enhancement",
          "protective_safeguards",
          "second_tier_wind_counties_and_parishes",
          "theft_and_resulting_damage_limitation",
          "vacancy_permit",
          "vacant_or_unoccupied_limitatin",
          "values_limitation_clause",
          "wind_limitation",
          "windstorm_or_hail_exclusion"
        ]}
        fields={[
          "yesno",
          "comments"
        ]}
        title={"Endorsements"}
      />
    </HX.Pane>
  )
}

export { quote_docs };
