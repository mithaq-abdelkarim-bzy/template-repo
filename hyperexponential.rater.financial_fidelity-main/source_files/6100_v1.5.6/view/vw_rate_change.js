import * as HX from "hx-model-components";

function vw_rate_change(scale) {
  return (
    <HX.Page title="Rate Change" fullWidth={false} viewScale={scale} shownBy="/show_rate_change">
      <HX.Section title="Rate Change">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Collection fields={["rate_change/expiring_policy_option_id"]} horizontal />
            <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={["rate_change/expiring_insured_name"]} />
            <HX.Button task="copy_expiring_basic_bond_terms" title="Copy Basic Bond Terms" />
          </HX.Pane>
          <HX.Table kb-interactive
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
            title="Impact Split"
          />
          <HX.Pane>
            <HX.Collection
              horizontal
              title="Expiring Policy"
              fields={[
                "rate_change/expiring_premium",
                "rate_change/expiring_beazley_share",
                "rate_change/bound_final"
              ]}
            />
            <HX.Collection
              horizontal
              fields={[
                "rate_change/expiring_policy_term",
                "rate_change/expiring_policy_reference",
                "/rate_change/expiring_brokerage"
              ]}
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>
      <HX.Section title="Select Prior Coverages">
        <HX.Pane flow="right">
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["show_all_covers_for_rate_change"]} />
          </HX.With>
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Table kb-interactive
            data={[
              'rate_change/cover_1_basic_bond',
              'rate_change/cover_2_insuring_agreement_d',
              'rate_change/cover_3_agents',
              'rate_change/cover_4_audit_expense',
              'rate_change/cover_5_electronic_data_processors',
              'rate_change/cover_6_extortion_persons',
              'rate_change/cover_7_extortion_property',
              'rate_change/cover_8_faithful_duty',
              'rate_change/cover_9_fraudulent_mortgages',
              'rate_change/cover_10_fraudulent_instructions',
              'rate_change/cover_11_issuers_orders',
              'rate_change/cover_12_misplacement',
              'rate_change/cover_13_partners_members',
              'rate_change/cover_14_registered_reps',
              'rate_change/cover_15_servicing_contractors',
              'rate_change/cover_16_trading_loss',
              'rate_change/cover_17_transit_cash_letter',
              'rate_change/cover_18_unattended_atms',
              'rate_change/cover_19_insuring_agreement_e',
              'rate_change/cover_20_computer_fraud_fi',
              'rate_change/cover_21_data_processing_fi',
              'rate_change/cover_22_voice_transfer_fraud_fi',
              'rate_change/cover_23_telefacsimile_transfer_fraud_fi',
              null,
              'rate_change/cover_24_liability_depository',
              'rate_change/cover_25_loss_property_damage',
              null,
              'rate_change/cover_26_computer_fraud',
              'rate_change/cover_27_data_processing',
              'rate_change/cover_28_voice_transfer_fraud',
              'rate_change/cover_29_telefacsimile_transfer_fraud',
              'rate_change/cover_30_hacker',
              'rate_change/cover_31_virus',
              'rate_change/cover_32_voice_computer_fraud',
              'rate_change/cover_33_account_takeover'
            ]}
            fields={[
              { field: "available", width: 100 },
              { field: "include", width: 100 },
              "coverage",
              "deductible"
            ]}
            // fields={[{ field: "available",  width: 100 },
            // {field: "include", 
            //   width: 100 },
            // "coverage",
            // "deductible",
            // "expiring_premium",
            // "expiring_premium_update_deductible",
            // "expiring_premium_update_deductible_limit", 
            //   "coverage_premium_current"]}
            filter="available"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Expiring Exposure Details">
        <HX.Pane>
          <HX.Collection fields={[
            "financial_assets_june_rc", "financial_assets_dec_rc", "number_of_employees_rc"]} horizontal
            with="rate_change"
          />
          <HX.Collection fields={[
            "financial_assets_june_yoy", "financial_assets_dec_yoy", "number_of_employees_yoy"]} horizontal
            with="rate_change"
          />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table kb-interactive
            data={[
              "branch_offices_rc",
              "facilities",
              "mobile_branch_units"
            ]}
            fields={[
              { field: "us", width: 100 },
              { field: "other", width: 100 }
            ]}
            title="Additional Locations"
            with="rate_change"
          />
          <HX.Table kb-interactive
            data={[
              "branch_offices_yoy",
              "facilities_yoy",
              "mobile_branch_units_yoy"
            ]}
            fields={[
              { field: "us", width: 100 },
              { field: "other", width: 100 }
            ]}
            title="YoY Change in Locations"
            with="rate_change"
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Collection
            shownBy="cover_2_insuring_agreement_d/final_include"
            title="Insuring Agreement D"
            fields={["include_checking_accounts_coverage"]}
            with="rate_change"
          />
          <HX.Collection
            shownBy="cover_3_agents/final_include"
            title="Agents Coverage"
            fields={["number_of_agents"]}
            with="rate_change"
          />
          <HX.Collection
            shownBy="cover_19_insuring_agreement_e/final_include"
            title="Insuring Agreement E (Securities)"
            fields={[
              "loan_to_deposit_ratio",
              "include_loan_participation_coverage"
            ]}
            with="rate_change"
          />
          <HX.Collection
            shownBy="cover_5_electronic_data_processors/final_include"
            title="Electronic Data Processing"
            fields={["num_data_processing_orgs"]}
            with="rate_change"
          />
        </HX.Pane>
        <HX.Pane flow="right" shownBy="rate_change/cover_6_extortion_persons/final_include">
          <HX.Table kb-interactive
            data={[
              "branch_offices_ex_per",
              "facilities_ex_per",
              "mobile_branch_units_ex_per"
            ]}
            fields={[
              { field: "us", width: 100 },
              { field: "other", width: 100 }
            ]}
            title="Extortion - Threats to Persons (Excluded Territories)"
            with="rate_change"
          />
          <HX.Collection fields={["rate_change/excluded_employees_persons"]} title=" " />
        </HX.Pane>
        <HX.Pane flow="right" shownBy="rate_change/cover_7_extortion_property/final_include">
          <HX.Table kb-interactive
            data={[
              "branch_offices_ex_prop",
              "facilities_ex_prop",
              "mobile_branch_units_ex_prop"
            ]}
            fields={[{
              field: "us",
              width: 100
            },
            {
              field: "other",
              width: 100
            }]}
            title="Extortion - Threats to Property (Excluded Territories)"
            with="rate_change"
          />
          <HX.Collection fields={["rate_change/excluded_employees_property"]} title=" " />
        </HX.Pane>
        <HX.Pane>
          <HX.Collection
            shownBy="cover_11_issuers_orders/final_include"
            title="Issuers of Register Checks or Personal Money Orders"
            fields={["number_of_issuers_of_register_checks"]}
            with="rate_change"
          />
          <HX.Collection
            shownBy="cover_13_partners_members/final_include"
            title="Partners/Members"
            fields={["number_of_partners_or_members"]}
            with="rate_change"
          />
          <HX.Collection
            shownBy="cover_14_registered_reps/final_include"
            title="Registered Reps. (NASD)"
            fields={["number_of_registered_reps"]}
            with="rate_change"
          />
          <HX.Collection
            shownBy="cover_15_servicing_contractors/final_include"
            title="Servicing Contractors"
            fields={["number_of_servicing_contractors"]}
            with="rate_change"
          />
          <HX.Collection
            shownBy="cover_18_unattended_atms/final_include"
            title="Unattended ATMs"
            fields={["number_of_atms"]}
            with="rate_change"
          />
          <HX.Table kb-interactive
            shownBy="show_safe_deposit_policy_table"
            data={[{
              datum: "safe_deposit_box_coverage",
              width: 100
            }]}
            fields={[
              "num_of_rented_boxes",
              "num_of_locations",
              "combined_limit",
              "include_money_coverage"
            ]}
            title="Safe Deposit Box Coverage"
            transpose={true}
            with="rate_change"
          />
        </HX.Pane>
        <HX.Table kb-interactive
          title="Computer Systems Fraud (Loss Cost Determination)"
          shownBy="show_computer_crime_policy_table"
          data={[
            {
              datum: "independent_software_contractors",
              infoBy: "independent_software_contractors/info"
            },
            {
              datum: "access_to_computer",
              infoBy: "access_to_computer/info"
            },
            {
              datum: "atms_accessed_to_system",
              infoBy: "atms_accessed_to_system/info"
            },
            {
              datum: "does_include_clearing_houses",
              infoBy: "does_include_clearing_houses/info"
            },
            { datum: "does_use_fed_wire" },
            {
              datum: "additional_computer_system",
              infoBy: "additional_computer_system/info"
            },
            {
              datum: "other_atm_systems",
              infoBy: "other_atm_systems/info"
            },
            {
              datum: "use_telex",
              infoBy: "use_telex/info"
            },
            null,
            "computer_crime_total"
          ]}
          fields={[
            { field: "include", width: 100 },
            { field: "how_many", width: 100 },
            { field: "loss_cost", width: 200 }
          ]}
          with="rate_change"
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rate_change };