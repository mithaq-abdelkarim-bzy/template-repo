/* eslint-disable */
import * as HX from "hx-model-components";

function vw_exposure_details() {
  return (
    <HX.Page title="Exposure Details" shownBy="model_state/show_after_landing_page" >
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Inputs">
          <HX.Pane flow="right">
            <HX.Collection fields={["/cds/type_of_insured", "/cds/standard_fields/insured_state_or_province", "/cds/policy_form_used"]} />
            <HX.Collection fields={["/cds/exposure/aggregate/assets_june", "/cds/exposure/aggregate/assets_december", "/cds/exposure/aggregate/number_of_employees"]} />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes field={"rating_note"} title="Rating Notes" />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive
              data={["/cds/exposure/aggregate/branch_offices", "/cds/exposure/aggregate/facilities", "/cds/exposure/aggregate/mobile_branch_units"]}
              fields={[
                { field: "us", width: 100 },
                { field: "other", width: 100 }
              ]}
              title="Additional Locations"
            />
          </HX.Pane>
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
              ]}
              fields={[{ field: "include", width: 100 }]}
              filter="available"
              syncColumnWidthsKey="coverage_table"
            />
            <HX.Table kb-interactive
              title="Safe Deposit Policy"
              data={[
                { datum: 'coverages/cover_24_liability_depository', infoBy: 'coverages/cover_24_liability_depository/info' },
                { datum: 'coverages/cover_25_loss_property_damage', infoBy: 'coverages/cover_25_loss_property_damage/info' },
              ]}
              fields={[{ field: "include", width: 100 }]}
              filter="available"
              syncColumnWidthsKey="coverage_table"
            />
            <HX.Table kb-interactive
              title="Computer Crime Policy"
              data={[
                { datum: 'coverages/cover_26_computer_fraud', infoBy: 'coverages/cover_26_computer_fraud/info' },
                { datum: 'coverages/cover_27_data_processing', infoBy: 'coverages/cover_27_data_processing/info' },
                { datum: 'coverages/cover_28_voice_transfer_fraud', infoBy: 'coverages/cover_28_voice_transfer_fraud/info' },
                { datum: 'coverages/cover_29_telefacsimile_transfer_fraud', infoBy: 'coverages/cover_29_telefacsimile_transfer_fraud/info' },
                { datum: 'coverages/cover_30_hacker', infoBy: 'coverages/cover_30_hacker/info' },
                { datum: 'coverages/cover_31_virus', infoBy: 'coverages/cover_31_virus/info' },
                { datum: 'coverages/cover_32_voice_computer_fraud', infoBy: 'coverages/cover_32_voice_computer_fraud/info' },
                { datum: 'coverages/cover_33_account_takeover', infoBy: 'coverages/cover_33_account_takeover/info' },
              ]}
              fields={[{ field: "include", width: 100 }]}
              filter="available"
              syncColumnWidthsKey="coverage_table"
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection
                shownBy="coverages/cover_2_insuring_agreement_d/final_include"
                title="Insuring Agreement D"
                fields={[{ field: "include_checking_accounts_coverage", infoBy: "/checking_accounts_info" }]} />
              <HX.Collection
                shownBy="coverages/cover_3_agents/final_include"
                title="Agents Coverage"
                fields={["/cds/exposure/aggregate/number_of_agents"]} />
              <HX.Collection
                shownBy="coverages/cover_19_insuring_agreement_e/final_include"
                title="Insuring Agreement E (Securities)"
                fields={[
                  { field: "/cds/exposure/aggregate/loan_to_deposit_ratio", infoBy: "/loan_to_deposit_ratio_info" },
                  { field: "include_loan_participation_coverage" }
                ]} />
              <HX.Collection
                shownBy="coverages/cover_5_electronic_data_processors/final_include"
                title="Electronic Data Processing"
                fields={["num_data_processing_orgs"]} />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right" shownBy="coverages/cover_6_extortion_persons/final_include">
            <HX.Table kb-interactive
              data={[
                "/cds/exposure/aggregate/branch_offices_ex_per",
                "/cds/exposure/aggregate/facilities_ex_per",
                "/cds/exposure/aggregate/mobile_branch_units_ex_per"
              ]}
              fields={[{ field: "us", width: 100 },
              { field: "other", width: 100 }]}
              title="Extortion - Threats to Persons (Excluded Territories)"
            />
            <HX.Collection fields={["/cds/exposure/aggregate/excluded_employees_persons"]} title=" " />
          </HX.Pane>
          <HX.Pane flow="right" shownBy="coverages/cover_7_extortion_property/final_include">
            <HX.Table kb-interactive
              data={[
                "/cds/exposure/aggregate/branch_offices_ex_prop",
                "/cds/exposure/aggregate/facilities_ex_prop",
                "/cds/exposure/aggregate/mobile_branch_units_ex_prop"
              ]}
              fields={[{ field: "us", width: 100 },
              { field: "other", width: 100 }]}
              title="Extortion - Threats to Property (Excluded Territories)"
            />
            <HX.Collection fields={["/cds/exposure/aggregate/excluded_employees_property"]} title=" " />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection
              shownBy="coverages/cover_11_issuers_orders/final_include"
              title="Issuers of Register Checks or Personal Money Orders"
              fields={["/cds/exposure/aggregate/number_of_issuers_of_register_checks"]}
            />
            <HX.Collection
              shownBy="coverages/cover_13_partners_members/final_include"
              title="Partners/Members"
              fields={["/cds/exposure/aggregate/number_of_partners_or_members"]}
            />
            <HX.Collection
              shownBy="coverages/cover_14_registered_reps/final_include"
              title="Registered Reps. (NASD)"
              fields={["/cds/exposure/aggregate/number_of_registered_reps"]}
            />
            <HX.Collection
              shownBy="coverages/cover_15_servicing_contractors/final_include"
              title="Servicing Contractors"
              fields={["/cds/exposure/aggregate/number_of_servicing_contractors"]}
            />
            <HX.Collection
              shownBy="coverages/cover_18_unattended_atms/final_include"
              title="Unattended ATMs"
              fields={["/cds/exposure/aggregate/number_of_atms"]}
            />
            <HX.Table kb-interactive
              title="Safe Deposit Box Coverage"
              shownBy="/show_safe_deposit_policy_table"
              data={[{ datum: "/cds/exposure/aggregate/safe_deposit_box_coverage", width: 100 }]}
              fields={[
                "num_of_rented_boxes",
                "num_of_locations",
                "combined_limit",
                "include_money_coverage"]}
              transpose={true}
            />
            <HX.Table kb-interactive
              title="Computer Systems Fraud (Loss Cost Determination)"
              shownBy="/show_computer_crime_policy_table"
              data={[
                { datum: "/cds/exposure/aggregate/independent_software_contractors", infoBy: "/cds/exposure/aggregate/independent_software_contractors/info" },
                { datum: "/cds/exposure/aggregate/access_to_computer", infoBy: "/cds/exposure/aggregate/access_to_computer/info" },
                { datum: "/cds/exposure/aggregate/atms_accessed_to_system", infoBy: "/cds/exposure/aggregate/atms_accessed_to_system/info" },
                { datum: "/cds/exposure/aggregate/does_include_clearing_houses", infoBy: "/cds/exposure/aggregate/does_include_clearing_houses/info" },
                { datum: "/cds/exposure/aggregate/does_use_fed_wire" },
                { datum: "/cds/exposure/aggregate/additional_computer_system", infoBy: "/cds/exposure/aggregate/additional_computer_system/info" },
                { datum: "/cds/exposure/aggregate/other_atm_systems", infoBy: "/cds/exposure/aggregate/other_atm_systems/info" },
                { datum: "/cds/exposure/aggregate/use_telex", infoBy: "/cds/exposure/aggregate/use_telex/info" },
                null,
                "computer_crime_total"
              ]}
              fields={[
                { field: "include", width: 100 },
                { field: "how_many", width: 100 },
                { field: "loss_cost", width: 200 }
              ]}
            />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_exposure_details };
