/* eslint-disable */
import * as HX from "hx-model-components";

function vw_pricing() {
  return (
    <HX.Page title="Pricing" fullWidth={false} shownBy="model_state/show_after_landing_page" >
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Pricing">
          <HX.Pane flow="right">
            <HX.Collection fields={["/cols_flag"]} />
            <HX.Button task="copy_basic_bond_terms" title="Copy Basic Bond Terms" />
          </HX.Pane>
          <HX.Notes field="/pricing_info"></HX.Notes>
          <HX.Pane>
            <HX.Table kb-interactive
              title="Form"
              data={[
                { datum: 'coverages/cover_1_basic_bond', infoBy: 'coverages/cover_1_basic_bond/info' },
                { datum: 'coverages/cover_2_insuring_agreement_d', infoBy: 'coverages/cover_2_insuring_agreement_d/info' },
                { datum: 'coverages/cover_3_agents', infoBy: 'coverages/cover_3_agents/info' },
                { datum: 'coverages/cover_4_audit_expense', infoBy: 'coverages/cover_4_audit_expense/info' },
                { datum: 'coverages/cover_5_electronic_data_processors', infoBy: 'coverages/cover_5_electronic_data_processors/info' },
                { datum: 'coverages/cover_6_extortion_persons', infoBy: 'coverages/cover_6_extortion_persons/info' },
                { datum: 'coverages/cover_7_extortion_property', infoBy: 'coverages/cover_7_extortion_property/info' },
                { datum: 'coverages/cover_8_faithful_duty', infoBy: 'coverages/cover_8_faithful_duty/info' },
                { datum: 'coverages/cover_9_fraudulent_mortgages', infoBy: 'coverages/cover_9_fraudulent_mortgages/info' },
                { datum: 'coverages/cover_10_fraudulent_instructions', infoBy: 'coverages/cover_10_fraudulent_instructions/info' },
                { datum: 'coverages/cover_11_issuers_orders', infoBy: 'coverages/cover_11_issuers_orders/info' },
                { datum: 'coverages/cover_12_misplacement', infoBy: 'coverages/cover_12_misplacement/info' },
                { datum: 'coverages/cover_13_partners_members', infoBy: 'coverages/cover_13_partners_members/info' },
                { datum: 'coverages/cover_14_registered_reps', infoBy: 'coverages/cover_14_registered_reps/info' },
                { datum: 'coverages/cover_15_servicing_contractors', infoBy: 'coverages/cover_15_servicing_contractors/info' },
                { datum: 'coverages/cover_16_trading_loss', infoBy: 'coverages/cover_16_trading_loss/info' },
                { datum: 'coverages/cover_17_transit_cash_letter', infoBy: 'coverages/cover_17_transit_cash_letter/info' },
                { datum: 'coverages/cover_18_unattended_atms', infoBy: 'coverages/cover_18_unattended_atms/info' },
                { datum: 'coverages/cover_19_insuring_agreement_e', infoBy: 'coverages/cover_19_insuring_agreement_e/info' },
                { datum: 'coverages/cover_20_computer_fraud_fi', infoBy: 'coverages/cover_20_computer_fraud_fi/info' },
                { datum: 'coverages/cover_21_data_processing_fi', infoBy: 'coverages/cover_21_data_processing_fi/info' },
                { datum: 'coverages/cover_22_voice_transfer_fraud_fi', infoBy: 'coverages/cover_22_voice_transfer_fraud_fi/info' },
                { datum: 'coverages/cover_23_telefacsimile_transfer_fraud_fi', infoBy: 'coverages/cover_23_telefacsimile_transfer_fraud_fi/info' },
                null,
                "subtotal_forms"
              ]}
              fields={[
                { field: "available", width: 100, shownBy: "/cols_flag" },
                { field: "min_coverage", shownBy: "/cols_flag" },
                { field: "max_coverage", shownBy: "/cols_flag" },
                { field: "min_deductible", shownBy: "/cols_flag" },
                { field: "max_deductible", shownBy: "/cols_flag" },
                "coverage",
                "deductible",
                "coverage_premium_post_a_rating_annual",
                "coverage_premium_post_a_rating"
                // "include"
              ]}
              filter="final_include"
            />
            <HX.Table kb-interactive
              title="Safe Deposit Policy" shownBy="include_safe_deposit_box"
              data={[
                { datum: 'coverages/cover_24_liability_depository', infoBy: 'coverages/cover_24_liability_depository/info' },
                { datum: 'coverages/cover_25_loss_property_damage', infoBy: 'coverages/cover_25_loss_property_damage/info' },
                null,
                "subtotal_safe_deposit_policy"
              ]}
              fields={[
                { field: "available", width: 100, shownBy: "/cols_flag" },
                { field: "min_coverage", shownBy: "/cols_flag" },
                { field: "max_coverage", shownBy: "/cols_flag" },
                { field: "min_deductible", shownBy: "/cols_flag" },
                { field: "max_deductible", shownBy: "/cols_flag" },
                "coverage",
                "deductible",
                "coverage_premium_post_a_rating_annual",
                "coverage_premium_post_a_rating"
              ]}
              filter="final_include"
            />
            <HX.Table kb-interactive
              title="Computer Crime Policy" shownBy="include_computer_crime"
              data={[
                { datum: 'coverages/cover_26_computer_fraud', infoBy: 'coverages/cover_26_computer_fraud/info' },
                { datum: 'coverages/cover_27_data_processing', infoBy: 'coverages/cover_27_data_processing/info' },
                { datum: 'coverages/cover_28_voice_transfer_fraud', infoBy: 'coverages/cover_28_voice_transfer_fraud/info' },
                { datum: 'coverages/cover_29_telefacsimile_transfer_fraud', infoBy: 'coverages/cover_29_telefacsimile_transfer_fraud/info' },
                { datum: 'coverages/cover_30_hacker', infoBy: 'coverages/cover_30_hacker/info' },
                { datum: 'coverages/cover_31_virus', infoBy: 'coverages/cover_31_virus/info' },
                { datum: 'coverages/cover_32_voice_computer_fraud', infoBy: 'coverages/cover_32_voice_computer_fraud/info' },
                { datum: 'coverages/cover_33_account_takeover', infoBy: 'coverages/cover_33_account_takeover/info' },
                null,
                "subtotal_computer_crime_policy"
              ]}
              fields={[
                { field: "available", width: 100, shownBy: "/cols_flag" },
                { field: "min_coverage", shownBy: "/cols_flag" },
                { field: "max_coverage", shownBy: "/cols_flag" },
                { field: "min_deductible", shownBy: "/cols_flag" },
                { field: "max_deductible", shownBy: "/cols_flag" },
                "coverage",
                "deductible",
                "coverage_premium_post_a_rating_annual",
                "coverage_premium_post_a_rating"
              ]}
              filter="final_include"
            />
            <HX.Table kb-interactive
              title="Premium Bearing Endorsements"
              data={["premium_bearing_endorsements", null, "premium_bearing_endorsements_total"]}
              fields={["endorsement", "is_impersonation_fraud", "coverage", "deductible", "premium_annual", "premium"]}
            />
            <HX.Collection horizontal
              fields={[null, null, "final_premium_annual", "final_premium"]}
            />

          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_pricing };
