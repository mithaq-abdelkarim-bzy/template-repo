/* eslint-disable */
import * as HX from "hx-model-components";

function vw_rating_summary() {
  return (
    <HX.Page title="Rating Summary" shownBy="model_state/show_after_landing_page" >
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Rating Summary">
          <HX.Section title="Rating Methodology" >
            <HX.Pane flow="right">
              <HX.Collection fields={["/cds/standard_fields/rating_methodology"]} />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Coverage Options" shownBy="/cds/standard_fields/is_case_priced">
            <HX.Table
              title={"Priced Quotes"}
              data={[{ datum: "/cds/layers", width: 250 }]}
              syncColumnWidthsKey="mySyncedTables1"
              fields={[
                "status.rating_summary_option",
                "/cds/standard_fields/policy_reference.rating_summary_option",
                "brokerage.rating_summary_option",
                "written_line",
                null,
                "quoted_premium_case_priced",
                "technical_premium_case_priced",
                "benchmark_premium_case_priced",
                null,
                "tpi_case_priced",
                "bpi_case_priced",
                null,
                "pflr",
                "roc",
              ]}
              freezeLeft={0}
              // kb-interactive // can interact with tables like excel e.g. c&p
              transpose // note un-transpose if require layers to be listed vertically
              shownBy="/cds/standard_fields/is_case_priced"
            />
          </HX.Section>
          <HX.Pane shownBy="/cds/standard_fields/is_rater_priced">
            <HX.Collection fields={["/cds/standard_fields/is_admitted_or_surplus", "brokerage"]} horizontal />
            <HX.Pane flow="right">
              <HX.Collection fields={[{ field: "a_rating_dev_factor", shownBy: "/cds/is_surplus" }]} />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane shownBy="modifier_flag">
              <HX.Table kb-interactive
                title="Schedule Rating Modifiers"
                data={["audit_procedures", "internal_controls", "management_and_personnel", "classification_peculiarities", null, { datum: "total_modifiers", infoBy: "modifier_label" }]}
                fields={["minimum", "maximum", "uw_selected", "comment"]}
              />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection
                title="Premium"
                fields={["final_premium", "final_premium_annual", "status"]}
                numCols={3} />
            </HX.Pane>
          </HX.Pane >
          <HX.Pane flow="right" shownBy="/cds/standard_fields/is_rater_priced">
            <HX.Collection title="Benchmark Pricing" fields={["benchmark_premium", "bpi"]} />
            <HX.Collection title="Technical Pricing" fields={["technical_premium", "tpi"]} />
            <HX.Collection title="Other Metrics" fields={[
              "/hx_core/ulr",
              "term_adjustment",
              { field: "rate_change/bound_final", shownBy: "/cds/standard_fields/is_renewal" }
            ]} />
          </HX.Pane>
          <HX.Pane shownBy="/cds/standard_fields/is_rater_priced">
            <HX.Table kb-interactive
              title="Premium Split"
              data={[
                "coverages/cover_1_basic_bond",
                "coverages/cover_2_insuring_agreement_d",
                "coverages/cover_3_agents",
                "coverages/cover_4_audit_expense",
                "coverages/cover_5_electronic_data_processors",
                "coverages/cover_6_extortion_persons",
                "coverages/cover_7_extortion_property",
                "coverages/cover_8_faithful_duty",
                "coverages/cover_9_fraudulent_mortgages",
                "coverages/cover_10_fraudulent_instructions",
                "coverages/cover_11_issuers_orders",
                "coverages/cover_12_misplacement",
                "coverages/cover_13_partners_members",
                "coverages/cover_14_registered_reps",
                "coverages/cover_15_servicing_contractors",
                "coverages/cover_16_trading_loss",
                "coverages/cover_17_transit_cash_letter",
                "coverages/cover_18_unattended_atms",
                "coverages/cover_19_insuring_agreement_e",
                "coverages/cover_20_computer_fraud_fi",
                "coverages/cover_21_data_processing_fi",
                "coverages/cover_22_voice_transfer_fraud_fi",
                "coverages/cover_23_telefacsimile_transfer_fraud_fi",
                null,
                "coverages/cover_24_liability_depository",
                "coverages/cover_25_loss_property_damage",
                null,
                "coverages/cover_26_computer_fraud",
                "coverages/cover_27_data_processing",
                "coverages/cover_28_voice_transfer_fraud",
                "coverages/cover_29_telefacsimile_transfer_fraud",
                "coverages/cover_30_hacker",
                "coverages/cover_31_virus",
                "coverages/cover_32_voice_computer_fraud",
                "coverages/cover_33_account_takeover",
              ]}
              // fields={["manual_premium", "coverage_premium", "coverage_premium_post_experience", "coverage_premium_post_schedule", "coverage_premium_post_a_rating"]}
              fields={[{ field: "coverage_premium_post_a_rating_annual" }]}
              filter="final_include"
            />
            <HX.Table kb-interactive
              title=" "
              data={["premium_bearing_endorsements"]}
              fields={["endorsement", "premium_annual"]}
            />
          </HX.Pane>
        </HX.Section >
      </HX.With>
    </HX.Page >
  )
}

export { vw_rating_summary };
