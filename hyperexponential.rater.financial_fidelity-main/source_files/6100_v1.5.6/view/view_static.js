
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page title="Landing Page"
        shownBy="model_state/show_landing_page">
        <HX.Section title="Start Policy">
          <HX.Pane flow="right">
            <HX.Button task="start_renewal_task"
              title="Press on 'Import Expiring Policy Data' at the top right corner then click here" />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_after_landing_page">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Account Details">
            <HX.Pane>
              <HX.Pane ratio={1}>
                <HX.Collection fields={[
                  "/hx_core/inception_date",
                  "/hx_core/expiry_date"
                ]}
                  horizontal={true} />
              </HX.Pane>
              <HX.Pane>
                <HX.Collection fields={[
                  "/cds/standard_fields/underwriter",
                  "status"
                ]}
                  horizontal={true} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection fields={[
                  "/cds/standard_fields/insured_name",
                  "/cds/standard_fields/policy_reference"
                ]}
                  horizontal={true} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={[
                "/cds/standard_fields/is_admitted_or_surplus",
                "is_primary_excess",
                "brokerage"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "quota_share_flag",
                "/hx_core/premium_currency",
                "/cds/standard_fields/is_renewal"
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Quota Share Information"
            shownBy="quota_share_flag">
            <HX.Pane>
              <HX.Collection fields={[
                "is_follow",
                "beazley_share"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "lead_insurer",
                "participating_insurer"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "lead_limit",
                "lead_premium"
              ]}
                horizontal={true}
                shownBy="is_follow" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Broker Details">
            <HX.Collection fields={[
              "/cds/standard_fields/broker",
              "/cds/broker_contact"
            ]}
              horizontal={true} />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Exposure Details"
        shownBy="model_state/show_after_landing_page">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Inputs">
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/cds/type_of_insured",
                "/cds/standard_fields/insured_state_or_province",
                "/cds/policy_form_used"
              ]} />
              <HX.Collection fields={[
                "/cds/exposure/aggregate/assets_june",
                "/cds/exposure/aggregate/assets_december",
                "/cds/exposure/aggregate/number_of_employees"
              ]} />
            </HX.Pane>
            <HX.Pane>
              <HX.Notes field="rating_note"
                title="Rating Notes" />
            </HX.Pane>
            <HX.Pane>
              <HX.Table kb-interactive={true}
                data={[
                "/cds/exposure/aggregate/branch_offices",
                "/cds/exposure/aggregate/facilities",
                "/cds/exposure/aggregate/mobile_branch_units"
              ]}
                fields={[
                {
                  "field": "us",
                  "width": 100
                },
                {
                  "field": "other",
                  "width": 100
                }
              ]}
                title="Additional Locations" />
            </HX.Pane>
            <HX.Pane>
              <HX.Table kb-interactive={true}
                title="Form"
                data={[
                {
                  "datum": "coverages/cover_1_basic_bond",
                  "infoBy": "coverages/cover_1_basic_bond/info"
                },
                {
                  "datum": "coverages/cover_2_insuring_agreement_d",
                  "infoBy": "coverages/cover_2_insuring_agreement_d/info"
                },
                {
                  "datum": "coverages/cover_3_agents",
                  "infoBy": "coverages/cover_3_agents/info"
                },
                {
                  "datum": "coverages/cover_4_audit_expense",
                  "infoBy": "coverages/cover_4_audit_expense/info"
                },
                {
                  "datum": "coverages/cover_5_electronic_data_processors",
                  "infoBy": "coverages/cover_5_electronic_data_processors/info"
                },
                {
                  "datum": "coverages/cover_6_extortion_persons",
                  "infoBy": "coverages/cover_6_extortion_persons/info"
                },
                {
                  "datum": "coverages/cover_7_extortion_property",
                  "infoBy": "coverages/cover_7_extortion_property/info"
                },
                {
                  "datum": "coverages/cover_8_faithful_duty",
                  "infoBy": "coverages/cover_8_faithful_duty/info"
                },
                {
                  "datum": "coverages/cover_9_fraudulent_mortgages",
                  "infoBy": "coverages/cover_9_fraudulent_mortgages/info"
                },
                {
                  "datum": "coverages/cover_10_fraudulent_instructions",
                  "infoBy": "coverages/cover_10_fraudulent_instructions/info"
                },
                {
                  "datum": "coverages/cover_11_issuers_orders",
                  "infoBy": "coverages/cover_11_issuers_orders/info"
                },
                {
                  "datum": "coverages/cover_12_misplacement",
                  "infoBy": "coverages/cover_12_misplacement/info"
                },
                {
                  "datum": "coverages/cover_13_partners_members",
                  "infoBy": "coverages/cover_13_partners_members/info"
                },
                {
                  "datum": "coverages/cover_14_registered_reps",
                  "infoBy": "coverages/cover_14_registered_reps/info"
                },
                {
                  "datum": "coverages/cover_15_servicing_contractors",
                  "infoBy": "coverages/cover_15_servicing_contractors/info"
                },
                {
                  "datum": "coverages/cover_16_trading_loss",
                  "infoBy": "coverages/cover_16_trading_loss/info"
                },
                {
                  "datum": "coverages/cover_17_transit_cash_letter",
                  "infoBy": "coverages/cover_17_transit_cash_letter/info"
                },
                {
                  "datum": "coverages/cover_18_unattended_atms",
                  "infoBy": "coverages/cover_18_unattended_atms/info"
                },
                {
                  "datum": "coverages/cover_19_insuring_agreement_e",
                  "infoBy": "coverages/cover_19_insuring_agreement_e/info"
                },
                {
                  "datum": "coverages/cover_20_computer_fraud_fi",
                  "infoBy": "coverages/cover_20_computer_fraud_fi/info"
                },
                {
                  "datum": "coverages/cover_21_data_processing_fi",
                  "infoBy": "coverages/cover_21_data_processing_fi/info"
                },
                {
                  "datum": "coverages/cover_22_voice_transfer_fraud_fi",
                  "infoBy": "coverages/cover_22_voice_transfer_fraud_fi/info"
                },
                {
                  "datum": "coverages/cover_23_telefacsimile_transfer_fraud_fi",
                  "infoBy": "coverages/cover_23_telefacsimile_transfer_fraud_fi/info"
                }
              ]}
                fields={[
                {
                  "field": "include",
                  "width": 100
                }
              ]}
                filter="available"
                syncColumnWidthsKey="coverage_table" />
              <HX.Table kb-interactive={true}
                title="Safe Deposit Policy"
                data={[
                {
                  "datum": "coverages/cover_24_liability_depository",
                  "infoBy": "coverages/cover_24_liability_depository/info"
                },
                {
                  "datum": "coverages/cover_25_loss_property_damage",
                  "infoBy": "coverages/cover_25_loss_property_damage/info"
                }
              ]}
                fields={[
                {
                  "field": "include",
                  "width": 100
                }
              ]}
                filter="available"
                syncColumnWidthsKey="coverage_table" />
              <HX.Table kb-interactive={true}
                title="Computer Crime Policy"
                data={[
                {
                  "datum": "coverages/cover_26_computer_fraud",
                  "infoBy": "coverages/cover_26_computer_fraud/info"
                },
                {
                  "datum": "coverages/cover_27_data_processing",
                  "infoBy": "coverages/cover_27_data_processing/info"
                },
                {
                  "datum": "coverages/cover_28_voice_transfer_fraud",
                  "infoBy": "coverages/cover_28_voice_transfer_fraud/info"
                },
                {
                  "datum": "coverages/cover_29_telefacsimile_transfer_fraud",
                  "infoBy": "coverages/cover_29_telefacsimile_transfer_fraud/info"
                },
                {
                  "datum": "coverages/cover_30_hacker",
                  "infoBy": "coverages/cover_30_hacker/info"
                },
                {
                  "datum": "coverages/cover_31_virus",
                  "infoBy": "coverages/cover_31_virus/info"
                },
                {
                  "datum": "coverages/cover_32_voice_computer_fraud",
                  "infoBy": "coverages/cover_32_voice_computer_fraud/info"
                },
                {
                  "datum": "coverages/cover_33_account_takeover",
                  "infoBy": "coverages/cover_33_account_takeover/info"
                }
              ]}
                fields={[
                {
                  "field": "include",
                  "width": 100
                }
              ]}
                filter="available"
                syncColumnWidthsKey="coverage_table" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection shownBy="coverages/cover_2_insuring_agreement_d/final_include"
                  title="Insuring Agreement D"
                  fields={[
                  {
                    "field": "include_checking_accounts_coverage",
                    "infoBy": "/checking_accounts_info"
                  }
                ]} />
                <HX.Collection shownBy="coverages/cover_3_agents/final_include"
                  title="Agents Coverage"
                  fields={[
                  "/cds/exposure/aggregate/number_of_agents"
                ]} />
                <HX.Collection shownBy="coverages/cover_19_insuring_agreement_e/final_include"
                  title="Insuring Agreement E (Securities)"
                  fields={[
                  {
                    "field": "/cds/exposure/aggregate/loan_to_deposit_ratio",
                    "infoBy": "/loan_to_deposit_ratio_info"
                  },
                  {
                    "field": "include_loan_participation_coverage"
                  }
                ]} />
                <HX.Collection shownBy="coverages/cover_5_electronic_data_processors/final_include"
                  title="Electronic Data Processing"
                  fields={[
                  "num_data_processing_orgs"
                ]} />
              </HX.Pane>
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right"
              shownBy="coverages/cover_6_extortion_persons/final_include">
              <HX.Table kb-interactive={true}
                data={[
                "/cds/exposure/aggregate/branch_offices_ex_per",
                "/cds/exposure/aggregate/facilities_ex_per",
                "/cds/exposure/aggregate/mobile_branch_units_ex_per"
              ]}
                fields={[
                {
                  "field": "us",
                  "width": 100
                },
                {
                  "field": "other",
                  "width": 100
                }
              ]}
                title="Extortion - Threats to Persons (Excluded Territories)" />
              <HX.Collection fields={[
                "/cds/exposure/aggregate/excluded_employees_persons"
              ]}
                title=" " />
            </HX.Pane>
            <HX.Pane flow="right"
              shownBy="coverages/cover_7_extortion_property/final_include">
              <HX.Table kb-interactive={true}
                data={[
                "/cds/exposure/aggregate/branch_offices_ex_prop",
                "/cds/exposure/aggregate/facilities_ex_prop",
                "/cds/exposure/aggregate/mobile_branch_units_ex_prop"
              ]}
                fields={[
                {
                  "field": "us",
                  "width": 100
                },
                {
                  "field": "other",
                  "width": 100
                }
              ]}
                title="Extortion - Threats to Property (Excluded Territories)" />
              <HX.Collection fields={[
                "/cds/exposure/aggregate/excluded_employees_property"
              ]}
                title=" " />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection shownBy="coverages/cover_11_issuers_orders/final_include"
                title="Issuers of Register Checks or Personal Money Orders"
                fields={[
                "/cds/exposure/aggregate/number_of_issuers_of_register_checks"
              ]} />
              <HX.Collection shownBy="coverages/cover_13_partners_members/final_include"
                title="Partners/Members"
                fields={[
                "/cds/exposure/aggregate/number_of_partners_or_members"
              ]} />
              <HX.Collection shownBy="coverages/cover_14_registered_reps/final_include"
                title="Registered Reps. (NASD)"
                fields={[
                "/cds/exposure/aggregate/number_of_registered_reps"
              ]} />
              <HX.Collection shownBy="coverages/cover_15_servicing_contractors/final_include"
                title="Servicing Contractors"
                fields={[
                "/cds/exposure/aggregate/number_of_servicing_contractors"
              ]} />
              <HX.Collection shownBy="coverages/cover_18_unattended_atms/final_include"
                title="Unattended ATMs"
                fields={[
                "/cds/exposure/aggregate/number_of_atms"
              ]} />
              <HX.Table kb-interactive={true}
                title="Safe Deposit Box Coverage"
                shownBy="/show_safe_deposit_policy_table"
                data={[
                {
                  "datum": "/cds/exposure/aggregate/safe_deposit_box_coverage",
                  "width": 100
                }
              ]}
                fields={[
                "num_of_rented_boxes",
                "num_of_locations",
                "combined_limit",
                "include_money_coverage"
              ]}
                transpose={true} />
              <HX.Table kb-interactive={true}
                title="Computer Systems Fraud (Loss Cost Determination)"
                shownBy="/show_computer_crime_policy_table"
                data={[
                {
                  "datum": "/cds/exposure/aggregate/independent_software_contractors",
                  "infoBy": "/cds/exposure/aggregate/independent_software_contractors/info"
                },
                {
                  "datum": "/cds/exposure/aggregate/access_to_computer",
                  "infoBy": "/cds/exposure/aggregate/access_to_computer/info"
                },
                {
                  "datum": "/cds/exposure/aggregate/atms_accessed_to_system",
                  "infoBy": "/cds/exposure/aggregate/atms_accessed_to_system/info"
                },
                {
                  "datum": "/cds/exposure/aggregate/does_include_clearing_houses",
                  "infoBy": "/cds/exposure/aggregate/does_include_clearing_houses/info"
                },
                {
                  "datum": "/cds/exposure/aggregate/does_use_fed_wire"
                },
                {
                  "datum": "/cds/exposure/aggregate/additional_computer_system",
                  "infoBy": "/cds/exposure/aggregate/additional_computer_system/info"
                },
                {
                  "datum": "/cds/exposure/aggregate/other_atm_systems",
                  "infoBy": "/cds/exposure/aggregate/other_atm_systems/info"
                },
                {
                  "datum": "/cds/exposure/aggregate/use_telex",
                  "infoBy": "/cds/exposure/aggregate/use_telex/info"
                },
                null,
                "computer_crime_total"
              ]}
                fields={[
                {
                  "field": "include",
                  "width": 100
                },
                {
                  "field": "how_many",
                  "width": 100
                },
                {
                  "field": "loss_cost",
                  "width": 200
                }
              ]} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Pricing"
        fullWidth={false}
        shownBy="model_state/show_after_landing_page">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Pricing">
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "/cols_flag"
              ]} />
              <HX.Button task="copy_basic_bond_terms"
                title="Copy Basic Bond Terms" />
            </HX.Pane>
            <HX.Notes field="/pricing_info" />
            <HX.Pane>
              <HX.Table kb-interactive={true}
                title="Form"
                data={[
                {
                  "datum": "coverages/cover_1_basic_bond",
                  "infoBy": "coverages/cover_1_basic_bond/info"
                },
                {
                  "datum": "coverages/cover_2_insuring_agreement_d",
                  "infoBy": "coverages/cover_2_insuring_agreement_d/info"
                },
                {
                  "datum": "coverages/cover_3_agents",
                  "infoBy": "coverages/cover_3_agents/info"
                },
                {
                  "datum": "coverages/cover_4_audit_expense",
                  "infoBy": "coverages/cover_4_audit_expense/info"
                },
                {
                  "datum": "coverages/cover_5_electronic_data_processors",
                  "infoBy": "coverages/cover_5_electronic_data_processors/info"
                },
                {
                  "datum": "coverages/cover_6_extortion_persons",
                  "infoBy": "coverages/cover_6_extortion_persons/info"
                },
                {
                  "datum": "coverages/cover_7_extortion_property",
                  "infoBy": "coverages/cover_7_extortion_property/info"
                },
                {
                  "datum": "coverages/cover_8_faithful_duty",
                  "infoBy": "coverages/cover_8_faithful_duty/info"
                },
                {
                  "datum": "coverages/cover_9_fraudulent_mortgages",
                  "infoBy": "coverages/cover_9_fraudulent_mortgages/info"
                },
                {
                  "datum": "coverages/cover_10_fraudulent_instructions",
                  "infoBy": "coverages/cover_10_fraudulent_instructions/info"
                },
                {
                  "datum": "coverages/cover_11_issuers_orders",
                  "infoBy": "coverages/cover_11_issuers_orders/info"
                },
                {
                  "datum": "coverages/cover_12_misplacement",
                  "infoBy": "coverages/cover_12_misplacement/info"
                },
                {
                  "datum": "coverages/cover_13_partners_members",
                  "infoBy": "coverages/cover_13_partners_members/info"
                },
                {
                  "datum": "coverages/cover_14_registered_reps",
                  "infoBy": "coverages/cover_14_registered_reps/info"
                },
                {
                  "datum": "coverages/cover_15_servicing_contractors",
                  "infoBy": "coverages/cover_15_servicing_contractors/info"
                },
                {
                  "datum": "coverages/cover_16_trading_loss",
                  "infoBy": "coverages/cover_16_trading_loss/info"
                },
                {
                  "datum": "coverages/cover_17_transit_cash_letter",
                  "infoBy": "coverages/cover_17_transit_cash_letter/info"
                },
                {
                  "datum": "coverages/cover_18_unattended_atms",
                  "infoBy": "coverages/cover_18_unattended_atms/info"
                },
                {
                  "datum": "coverages/cover_19_insuring_agreement_e",
                  "infoBy": "coverages/cover_19_insuring_agreement_e/info"
                },
                {
                  "datum": "coverages/cover_20_computer_fraud_fi",
                  "infoBy": "coverages/cover_20_computer_fraud_fi/info"
                },
                {
                  "datum": "coverages/cover_21_data_processing_fi",
                  "infoBy": "coverages/cover_21_data_processing_fi/info"
                },
                {
                  "datum": "coverages/cover_22_voice_transfer_fraud_fi",
                  "infoBy": "coverages/cover_22_voice_transfer_fraud_fi/info"
                },
                {
                  "datum": "coverages/cover_23_telefacsimile_transfer_fraud_fi",
                  "infoBy": "coverages/cover_23_telefacsimile_transfer_fraud_fi/info"
                },
                null,
                "subtotal_forms"
              ]}
                fields={[
                {
                  "field": "available",
                  "shownBy": "/cols_flag",
                  "width": 100
                },
                {
                  "field": "min_coverage",
                  "shownBy": "/cols_flag"
                },
                {
                  "field": "max_coverage",
                  "shownBy": "/cols_flag"
                },
                {
                  "field": "min_deductible",
                  "shownBy": "/cols_flag"
                },
                {
                  "field": "max_deductible",
                  "shownBy": "/cols_flag"
                },
                "coverage",
                "deductible",
                "coverage_premium_post_a_rating_annual",
                "coverage_premium_post_a_rating"
              ]}
                filter="final_include" />
              <HX.Table kb-interactive={true}
                title="Safe Deposit Policy"
                shownBy="include_safe_deposit_box"
                data={[
                {
                  "datum": "coverages/cover_24_liability_depository",
                  "infoBy": "coverages/cover_24_liability_depository/info"
                },
                {
                  "datum": "coverages/cover_25_loss_property_damage",
                  "infoBy": "coverages/cover_25_loss_property_damage/info"
                },
                null,
                "subtotal_safe_deposit_policy"
              ]}
                fields={[
                {
                  "field": "available",
                  "shownBy": "/cols_flag",
                  "width": 100
                },
                {
                  "field": "min_coverage",
                  "shownBy": "/cols_flag"
                },
                {
                  "field": "max_coverage",
                  "shownBy": "/cols_flag"
                },
                {
                  "field": "min_deductible",
                  "shownBy": "/cols_flag"
                },
                {
                  "field": "max_deductible",
                  "shownBy": "/cols_flag"
                },
                "coverage",
                "deductible",
                "coverage_premium_post_a_rating_annual",
                "coverage_premium_post_a_rating"
              ]}
                filter="final_include" />
              <HX.Table kb-interactive={true}
                title="Computer Crime Policy"
                shownBy="include_computer_crime"
                data={[
                {
                  "datum": "coverages/cover_26_computer_fraud",
                  "infoBy": "coverages/cover_26_computer_fraud/info"
                },
                {
                  "datum": "coverages/cover_27_data_processing",
                  "infoBy": "coverages/cover_27_data_processing/info"
                },
                {
                  "datum": "coverages/cover_28_voice_transfer_fraud",
                  "infoBy": "coverages/cover_28_voice_transfer_fraud/info"
                },
                {
                  "datum": "coverages/cover_29_telefacsimile_transfer_fraud",
                  "infoBy": "coverages/cover_29_telefacsimile_transfer_fraud/info"
                },
                {
                  "datum": "coverages/cover_30_hacker",
                  "infoBy": "coverages/cover_30_hacker/info"
                },
                {
                  "datum": "coverages/cover_31_virus",
                  "infoBy": "coverages/cover_31_virus/info"
                },
                {
                  "datum": "coverages/cover_32_voice_computer_fraud",
                  "infoBy": "coverages/cover_32_voice_computer_fraud/info"
                },
                {
                  "datum": "coverages/cover_33_account_takeover",
                  "infoBy": "coverages/cover_33_account_takeover/info"
                },
                null,
                "subtotal_computer_crime_policy"
              ]}
                fields={[
                {
                  "field": "available",
                  "shownBy": "/cols_flag",
                  "width": 100
                },
                {
                  "field": "min_coverage",
                  "shownBy": "/cols_flag"
                },
                {
                  "field": "max_coverage",
                  "shownBy": "/cols_flag"
                },
                {
                  "field": "min_deductible",
                  "shownBy": "/cols_flag"
                },
                {
                  "field": "max_deductible",
                  "shownBy": "/cols_flag"
                },
                "coverage",
                "deductible",
                "coverage_premium_post_a_rating_annual",
                "coverage_premium_post_a_rating"
              ]}
                filter="final_include" />
              <HX.Table kb-interactive={true}
                title="Premium Bearing Endorsements"
                data={[
                "premium_bearing_endorsements",
                null,
                "premium_bearing_endorsements_total"
              ]}
                fields={[
                "endorsement",
                "is_impersonation_fraud",
                "coverage",
                "deductible",
                "premium_annual",
                "premium"
              ]} />
              <HX.Collection horizontal={true}
                fields={[
                null,
                null,
                "final_premium_annual",
                "final_premium"
              ]} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Experience Rating"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Experience Rating">
            <HX.Table kb-interactive={true}
              data={[
              "/cds/experience_rating/claims",
              null,
              "/cds/experience_rating/total"
            ]}
              fields={[
              "date",
              "loss",
              "coverage",
              "limited_coverage",
              "limited_deductible",
              "net_direct_loss_incurred",
              "exceeds_500k",
              "adjusted_loss"
            ]} />
          </HX.Section>
          <HX.Section title="Excess Rating">
            <HX.Collection fields={[
              "/cds/experience_rating/eligible_for_excess_experience_mod",
              {
                "field": "/cds/experience_rating/use_excess_experience_mod",
                "shownBy": "/cds/experience_rating/eligible_for_excess_experience_mod"
              }
            ]}
              horizontal={true} />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        shownBy="/show_rate_change">
        <HX.Section title="Rate Change">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_policy_option_id"
              ]}
                horizontal={true} />
              <HX.Button task="expiring_policy_fetch_task"
                title="Fetch Expiring Data" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_insured_name"
              ]} />
              <HX.Button task="copy_expiring_basic_bond_terms"
                title="Copy Basic Bond Terms" />
            </HX.Pane>
            <HX.Table kb-interactive={true}
              data={[
              "rate_change/exposure_change",
              "rate_change/risk_characteristics_change",
              "rate_change/deductible_change",
              "rate_change/limit_change",
              "rate_change/terms_conditions_change",
              "rate_change/brokerage_change",
              "rate_change/other_change"
            ]}
              fields={[
              "uw_selected",
              "comments"
            ]}
              title="Impact Split" />
            <HX.Pane>
              <HX.Collection horizontal={true}
                title="Expiring Policy"
                fields={[
                "rate_change/expiring_premium",
                "rate_change/expiring_beazley_share",
                "rate_change/bound_final"
              ]} />
              <HX.Collection horizontal={true}
                fields={[
                "rate_change/expiring_policy_term",
                "rate_change/expiring_policy_reference",
                "/rate_change/expiring_brokerage"
              ]} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Select Prior Coverages">
          <HX.Pane flow="right">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "show_all_covers_for_rate_change"
              ]} />
            </HX.With>
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              data={[
              "rate_change/cover_1_basic_bond",
              "rate_change/cover_2_insuring_agreement_d",
              "rate_change/cover_3_agents",
              "rate_change/cover_4_audit_expense",
              "rate_change/cover_5_electronic_data_processors",
              "rate_change/cover_6_extortion_persons",
              "rate_change/cover_7_extortion_property",
              "rate_change/cover_8_faithful_duty",
              "rate_change/cover_9_fraudulent_mortgages",
              "rate_change/cover_10_fraudulent_instructions",
              "rate_change/cover_11_issuers_orders",
              "rate_change/cover_12_misplacement",
              "rate_change/cover_13_partners_members",
              "rate_change/cover_14_registered_reps",
              "rate_change/cover_15_servicing_contractors",
              "rate_change/cover_16_trading_loss",
              "rate_change/cover_17_transit_cash_letter",
              "rate_change/cover_18_unattended_atms",
              "rate_change/cover_19_insuring_agreement_e",
              "rate_change/cover_20_computer_fraud_fi",
              "rate_change/cover_21_data_processing_fi",
              "rate_change/cover_22_voice_transfer_fraud_fi",
              "rate_change/cover_23_telefacsimile_transfer_fraud_fi",
              null,
              "rate_change/cover_24_liability_depository",
              "rate_change/cover_25_loss_property_damage",
              null,
              "rate_change/cover_26_computer_fraud",
              "rate_change/cover_27_data_processing",
              "rate_change/cover_28_voice_transfer_fraud",
              "rate_change/cover_29_telefacsimile_transfer_fraud",
              "rate_change/cover_30_hacker",
              "rate_change/cover_31_virus",
              "rate_change/cover_32_voice_computer_fraud",
              "rate_change/cover_33_account_takeover"
            ]}
              fields={[
              {
                "field": "available",
                "width": 100
              },
              {
                "field": "include",
                "width": 100
              },
              "coverage",
              "deductible"
            ]}
              filter="available" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Expiring Exposure Details">
          <HX.Pane>
            <HX.Collection fields={[
              "financial_assets_june_rc",
              "financial_assets_dec_rc",
              "number_of_employees_rc"
            ]}
              horizontal={true}
              with="rate_change" />
            <HX.Collection fields={[
              "financial_assets_june_yoy",
              "financial_assets_dec_yoy",
              "number_of_employees_yoy"
            ]}
              horizontal={true}
              with="rate_change" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table kb-interactive={true}
              data={[
              "branch_offices_rc",
              "facilities",
              "mobile_branch_units"
            ]}
              fields={[
              {
                "field": "us",
                "width": 100
              },
              {
                "field": "other",
                "width": 100
              }
            ]}
              title="Additional Locations"
              with="rate_change" />
            <HX.Table kb-interactive={true}
              data={[
              "branch_offices_yoy",
              "facilities_yoy",
              "mobile_branch_units_yoy"
            ]}
              fields={[
              {
                "field": "us",
                "width": 100
              },
              {
                "field": "other",
                "width": 100
              }
            ]}
              title="YoY Change in Locations"
              with="rate_change" />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection shownBy="cover_2_insuring_agreement_d/final_include"
              title="Insuring Agreement D"
              fields={[
              "include_checking_accounts_coverage"
            ]}
              with="rate_change" />
            <HX.Collection shownBy="cover_3_agents/final_include"
              title="Agents Coverage"
              fields={[
              "number_of_agents"
            ]}
              with="rate_change" />
            <HX.Collection shownBy="cover_19_insuring_agreement_e/final_include"
              title="Insuring Agreement E (Securities)"
              fields={[
              "loan_to_deposit_ratio",
              "include_loan_participation_coverage"
            ]}
              with="rate_change" />
            <HX.Collection shownBy="cover_5_electronic_data_processors/final_include"
              title="Electronic Data Processing"
              fields={[
              "num_data_processing_orgs"
            ]}
              with="rate_change" />
          </HX.Pane>
          <HX.Pane flow="right"
            shownBy="rate_change/cover_6_extortion_persons/final_include">
            <HX.Table kb-interactive={true}
              data={[
              "branch_offices_ex_per",
              "facilities_ex_per",
              "mobile_branch_units_ex_per"
            ]}
              fields={[
              {
                "field": "us",
                "width": 100
              },
              {
                "field": "other",
                "width": 100
              }
            ]}
              title="Extortion - Threats to Persons (Excluded Territories)"
              with="rate_change" />
            <HX.Collection fields={[
              "rate_change/excluded_employees_persons"
            ]}
              title=" " />
          </HX.Pane>
          <HX.Pane flow="right"
            shownBy="rate_change/cover_7_extortion_property/final_include">
            <HX.Table kb-interactive={true}
              data={[
              "branch_offices_ex_prop",
              "facilities_ex_prop",
              "mobile_branch_units_ex_prop"
            ]}
              fields={[
              {
                "field": "us",
                "width": 100
              },
              {
                "field": "other",
                "width": 100
              }
            ]}
              title="Extortion - Threats to Property (Excluded Territories)"
              with="rate_change" />
            <HX.Collection fields={[
              "rate_change/excluded_employees_property"
            ]}
              title=" " />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection shownBy="cover_11_issuers_orders/final_include"
              title="Issuers of Register Checks or Personal Money Orders"
              fields={[
              "number_of_issuers_of_register_checks"
            ]}
              with="rate_change" />
            <HX.Collection shownBy="cover_13_partners_members/final_include"
              title="Partners/Members"
              fields={[
              "number_of_partners_or_members"
            ]}
              with="rate_change" />
            <HX.Collection shownBy="cover_14_registered_reps/final_include"
              title="Registered Reps. (NASD)"
              fields={[
              "number_of_registered_reps"
            ]}
              with="rate_change" />
            <HX.Collection shownBy="cover_15_servicing_contractors/final_include"
              title="Servicing Contractors"
              fields={[
              "number_of_servicing_contractors"
            ]}
              with="rate_change" />
            <HX.Collection shownBy="cover_18_unattended_atms/final_include"
              title="Unattended ATMs"
              fields={[
              "number_of_atms"
            ]}
              with="rate_change" />
            <HX.Table kb-interactive={true}
              shownBy="show_safe_deposit_policy_table"
              data={[
              {
                "datum": "safe_deposit_box_coverage",
                "width": 100
              }
            ]}
              fields={[
              "num_of_rented_boxes",
              "num_of_locations",
              "combined_limit",
              "include_money_coverage"
            ]}
              title="Safe Deposit Box Coverage"
              transpose={true}
              with="rate_change" />
          </HX.Pane>
          <HX.Table kb-interactive={true}
            title="Computer Systems Fraud (Loss Cost Determination)"
            shownBy="show_computer_crime_policy_table"
            data={[
            {
              "datum": "independent_software_contractors",
              "infoBy": "independent_software_contractors/info"
            },
            {
              "datum": "access_to_computer",
              "infoBy": "access_to_computer/info"
            },
            {
              "datum": "atms_accessed_to_system",
              "infoBy": "atms_accessed_to_system/info"
            },
            {
              "datum": "does_include_clearing_houses",
              "infoBy": "does_include_clearing_houses/info"
            },
            {
              "datum": "does_use_fed_wire"
            },
            {
              "datum": "additional_computer_system",
              "infoBy": "additional_computer_system/info"
            },
            {
              "datum": "other_atm_systems",
              "infoBy": "other_atm_systems/info"
            },
            {
              "datum": "use_telex",
              "infoBy": "use_telex/info"
            },
            null,
            "computer_crime_total"
          ]}
            fields={[
            {
              "field": "include",
              "width": 100
            },
            {
              "field": "how_many",
              "width": 100
            },
            {
              "field": "loss_cost",
              "width": 200
            }
          ]}
            with="rate_change" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        shownBy="model_state/show_after_landing_page">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Rating Summary">
            <HX.Section title="Rating Methodology">
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "/cds/standard_fields/rating_methodology"
                ]} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Section>
            <HX.Section title="Coverage Options"
              shownBy="/cds/standard_fields/is_case_priced">
              <HX.Table title="Priced Quotes"
                data={[
                {
                  "datum": "/cds/layers",
                  "width": 250
                }
              ]}
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
                "roc"
              ]}
                freezeLeft={0}
                transpose={true}
                shownBy="/cds/standard_fields/is_case_priced" />
            </HX.Section>
            <HX.Pane shownBy="/cds/standard_fields/is_rater_priced">
              <HX.Collection fields={[
                "/cds/standard_fields/is_admitted_or_surplus",
                "brokerage"
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  {
                    "field": "a_rating_dev_factor",
                    "shownBy": "/cds/is_surplus"
                  }
                ]} />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane shownBy="modifier_flag">
                <HX.Table kb-interactive={true}
                  title="Schedule Rating Modifiers"
                  data={[
                  "audit_procedures",
                  "internal_controls",
                  "management_and_personnel",
                  "classification_peculiarities",
                  null,
                  {
                    "datum": "total_modifiers",
                    "infoBy": "modifier_label"
                  }
                ]}
                  fields={[
                  "minimum",
                  "maximum",
                  "uw_selected",
                  "comment"
                ]} />
              </HX.Pane>
              <HX.Pane>
                <HX.Collection title="Premium"
                  fields={[
                  "final_premium",
                  "final_premium_annual",
                  "status"
                ]}
                  numCols={3} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane flow="right"
              shownBy="/cds/standard_fields/is_rater_priced">
              <HX.Collection title="Benchmark Pricing"
                fields={[
                "benchmark_premium",
                "bpi"
              ]} />
              <HX.Collection title="Technical Pricing"
                fields={[
                "technical_premium",
                "tpi"
              ]} />
              <HX.Collection title="Other Metrics"
                fields={[
                "/hx_core/ulr",
                "term_adjustment",
                {
                  "field": "rate_change/bound_final",
                  "shownBy": "/cds/standard_fields/is_renewal"
                }
              ]} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/standard_fields/is_rater_priced">
              <HX.Table kb-interactive={true}
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
                "coverages/cover_33_account_takeover"
              ]}
                fields={[
                {
                  "field": "coverage_premium_post_a_rating_annual"
                }
              ]}
                filter="final_include" />
              <HX.Table kb-interactive={true}
                title=" "
                data={[
                "premium_bearing_endorsements"
              ]}
                fields={[
                "endorsement",
                "premium_annual"
              ]} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rationale"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="General Comments">
          <HX.Notes field="cds/general_comments" />
        </HX.Section>
        <HX.Section title="Underwriting Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs">
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "/cds/standard_fields/policy_reference.read_only",
              "brokerage.read_only",
              "written_line_view"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "quoted_premium_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "technical_premium_case_priced",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium_case_priced",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi_case_priced",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]}
              shownBy="/cds/standard_fields/is_case_priced" />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]}
              shownBy="/cds/standard_fields/is_rater_priced" />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Something is Broken">
        <HX.With context={{
          "path": "bug_report",
          "type": "struct"
        }}>
          <HX.Section title="Log a New Incident">
            <HX.Notes field="helper_text" />
            <HX.Pane>
              <HX.Button task="new_bug_report_task"
                title="Log a New Incident" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Incident Details"
            shownBy="commenced_flag">
            <HX.Pane>
              <HX.Collection fields={[
                "summary"
              ]}
                title="Summary" />
              <HX.Notes field="email_body"
                title="Details" />
              <HX.Pane flow="right"
                ratio={2}>
                <HX.Pane shownBy="inputs_outputs_file_show">
                  <HX.File field="inputs_outputs_file"
                    title="Inputs/Outputs Attachment" />
                  <HX.Button task="generate_bug_report_task"
                    title="Generate Inputs/Outputs" />
                </HX.Pane>
                <HX.With context={{
                  "path": "screenshot_files",
                  "type": "struct"
                }}>
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f1/show_text" />
                  <HX.File field="f1/file"
                    title="Screenshot Attachment"
                    shownBy="f1/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f2/show_text" />
                  <HX.File field="f2/file"
                    title="Screenshot Attachment 2"
                    shownBy="f2/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f3/show_text" />
                  <HX.File field="f3/file"
                    title="Screenshot Attachment 3"
                    shownBy="f3/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f4/show_text" />
                  <HX.File field="f4/file"
                    title="Screenshot Attachment 4"
                    shownBy="f4/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f5/show_text" />
                  <HX.File field="f5/file"
                    title="Screenshot Attachment 5"
                    shownBy="f5/show_file" />
                </HX.With>
              </HX.Pane>
              <HX.Button task="add_additional_file_task"
                title="Upload Additional Screenshots" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="send_bug_report_task"
                title="Send Incident" />
              <HX.Button task="cancel_bug_report_task"
                title="Cancel Incident" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};