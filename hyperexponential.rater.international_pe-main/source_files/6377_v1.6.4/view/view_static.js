
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
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Notes field="model_state/landing_page_info" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "inception_date",
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "underwriter",
              "insured_name"
            ]}
              with="cds/standard_fields"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/source_currency_name",
              "cds/currencies/source_currency",
              "cds/standard_fields/is_renewal"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Coverage Selection">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/coverage_selection"
            ]} />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure E&O"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/eo_coverage_selection">
        <HX.Section title="Exposure Information">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/eo_territory/input_value"
            ]} />
            <HX.Collection fields={[
              "cds/exposure/granular/eo_profession"
            ]} />
            <HX.Collection fields={[
              {
                "field": "cds/exposure/aggregate/eo_total_fees",
                "labelBy": "/cds/eo_fees_currency_label"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Fees Split by Discipline"
          shownBy="cds/exposure/granular/eo_exposure_shownby">
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "eo_total_fees_pct"
                }
              ]} />
              <HX.Button task="clear_eo_input_task"
                title="Clear All the Input of Fees %" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table title=" "
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "eo_ae_architecture_commercial",
              "eo_ae_architecture_residential",
              "eo_ae_chemical_engineering",
              "eo_ae_civil_engineering",
              "eo_ae_commercial_surveys",
              "eo_ae_eia_studies",
              "eo_ae_electrical_engineering",
              "eo_ae_environmental",
              "eo_ae_feasibility_studies",
              "eo_ae_geology_land_surveying",
              "eo_ae_interior_design",
              "eo_ae_landscape_architecture",
              "eo_ae_mechanical_engineering",
              "eo_ae_project_coordination",
              "eo_ae_project_management",
              "eo_ae_quantity_surveying",
              "eo_ae_residential_surveys",
              "eo_ae_soils_engineering",
              "eo_ae_structural_engineering",
              "eo_ae_structural_surveys",
              "eo_ae_town_planning",
              "eo_ae_valuations",
              "eo_ae_other",
              "eo_lawyer_civil_litigation",
              "eo_lawyer_consultancy",
              "eo_lawyer_conveyance",
              "eo_lawyer_corporate_finance",
              "eo_lawyer_criminal_litigation",
              "eo_lawyer_employment",
              "eo_lawyer_estate_planning_probate",
              "eo_lawyer_family_law",
              "eo_lawyer_financial_institutions",
              "eo_lawyer_formation_administration_of_companies",
              "eo_lawyer_formation_administration_of_trusts",
              "eo_lawyer_general_commercial",
              "eo_lawyer_insolvency",
              "eo_lawyer_insurance_claims_handling_monitoring",
              "eo_lawyer_insurance_other",
              "eo_lawyer_marine_litigation",
              "eo_lawyer_patentintellectual_property",
              "eo_lawyer_property_development",
              "eo_lawyer_provision_of_directors_officers",
              "eo_lawyer_trustee_appointments",
              "eo_lawyer_other",
              "eo_misc_accident_investigation_consultants",
              "eo_misc_advertising_site_consultants",
              "eo_misc_arboricultural_consultants",
              "eo_misc_archaeological_consultants",
              "eo_misc_auctioneers",
              "eo_misc_boat_agents",
              "eo_misc_business_training_development_consultants",
              "eo_misc_clerical_administration",
              "eo_misc_debt_collectors",
              "eo_misc_disability_and_access_audit_consultants",
              "eo_misc_disaster_recovery_consultants",
              "eo_misc_educational_guardians",
              "eo_misc_energy_consultants",
              "eo_misc_event_organisers",
              "eo_misc_exhibition_organisers",
              "eo_misc_expert_witness_work",
              "eo_misc_facilities_management_consultants",
              "eo_misc_fashion_designers",
              "eo_misc_fire_trainers",
              "eo_misc_forestry_woodland_management_consultants",
              "eo_misc_graphic_designers",
              "eo_misc_health_safety_consultants",
              "eo_misc_horticultural_consultants",
              "eo_misc_human_resource_consultants",
              "eo_misc_insurance_fraud_investigators",
              "eo_misc_inventory_consultants",
              "eo_misc_landscape_gardeners",
              "eo_misc_law_costs_draughtsman",
              "eo_misc_licensed_court_enforcement_officers",
              "eo_misc_licensing_consultants",
              "eo_misc_local_search_companies",
              "eo_misc_loss_adjusters",
              "eo_misc_loss_assessors",
              "eo_misc_management_consultants",
              "eo_misc_market_research_consultants",
              "eo_misc_noise_abatement_consultants",
              "eo_misc_nvq_assessors",
              "eo_misc_ofsted_inspectors_education_consultants",
              "eo_misc_private_investigators",
              "eo_misc_property_insurance_surveyors",
              "eo_misc_property_maintenance_consultants",
              "eo_misc_purchase_supply_consultants",
              "eo_misc_quality_assessors",
              "eo_misc_recruitment_consultants_employment_agencies",
              "eo_misc_regeneration_consultants",
              "eo_misc_relocation_consultants",
              "eo_misc_secretarial_administration_consultants",
              "eo_misc_sign_language_interpreters",
              "eo_misc_stock_takers_valuers",
              "eo_misc_telecommunications_consultants",
              "eo_misc_tracing_consultant",
              "eo_misc_trade_associations",
              "eo_misc_trading_standards_consultants",
              "eo_misc_translators",
              "eo_misc_tree_surgeons",
              "eo_misc_utility_consultants",
              "eo_misc_vat_consultants",
              "eo_misc_other",
              "eo_insbroker_bloodstock",
              "eo_insbroker_cargo_goods_in_transit",
              "eo_insbroker_claims_adjusting",
              "eo_insbroker_commercial_property",
              "eo_insbroker_crime",
              "eo_insbroker_fac_reinsurance",
              "eo_insbroker_group_accident_life",
              "eo_insbroker_householders",
              "eo_insbroker_individual_term_life_health",
              "eo_insbroker_industrial_property",
              "eo_insbroker_liability",
              "eo_insbroker_marine_aviation_hull",
              "eo_insbroker_marine_private_yacht",
              "eo_insbroker_med_mal",
              "eo_insbroker_mortgage_broking",
              "eo_insbroker_motor",
              "eo_insbroker_non_marine",
              "eo_insbroker_pensions_life_investment_products",
              "eo_insbroker_personal_accident",
              "eo_insbroker_reinsurance_treaty",
              "eo_insbroker_risk_management_consultancy",
              "eo_insbroker_other"
            ]}
              fields={[
              {
                "field": "input_pct",
                "width": 250
              },
              {
                "field": "relativity",
                "width": 250
              }
            ]}
              filter="show_row"
              kb-interactive={true} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Architects and Engineers Operations"
          shownBy="cds/exposure/granular/eo_ae_operaion_shownby">
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "eo_ae_operation_pct"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table title=" "
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "eo_ae_operation_aerospace",
              "eo_ae_operation_airports",
              "eo_ae_operation_bridgestunnels",
              "eo_ae_operation_chemicalpetrochemicalpipelines",
              "eo_ae_operation_commercial_clients",
              "eo_ae_operation_consultingengineeringmanufacturing",
              "eo_ae_operation_damsharboursjetties",
              "eo_ae_operation_financial_clients",
              "eo_ae_operation_foundationsunderpinning",
              "eo_ae_operation_healthcaremedical",
              "eo_ae_operation_highways",
              "eo_ae_operation_hospitalsschoolspublic_buildings",
              "eo_ae_operation_hotelsresorts",
              "eo_ae_operation_industrialfactories",
              "eo_ae_operation_internetecommerce",
              "eo_ae_operation_machinerymechanical_design",
              "eo_ae_operation_nuclear",
              "eo_ae_operation_offshore",
              "eo_ae_operation_other",
              "eo_ae_operation_publicgovernment_clients",
              "eo_ae_operation_residential_individual_dwelling",
              "eo_ae_operation_residential_multiple_dwelling",
              "eo_ae_operation_retailofficecommercial",
              "eo_ae_operation_theatresstadiumsleisure",
              "eo_ae_operation_trade_wholesaleretail",
              "eo_ae_operation_water_systemssewerage"
            ]}
              fields={[
              {
                "field": "input_pct",
                "width": 250
              },
              {
                "field": "relativity",
                "width": 250
              }
            ]}
              filter="show_row"
              kb-interactive={true} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Insurance Information">
          <HX.Table title=" "
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            "eo_prior_knowledge"
          ]}
            fields={[
            {
              "field": "input_value",
              "width": 250
            },
            {
              "field": "relativity",
              "width": 250
            }
          ]}
            with="cds/rating_factors" />
          <HX.Table title=" "
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            "eo_insurance_history"
          ]}
            fields={[
            {
              "field": "input_value",
              "width": 400
            },
            {
              "field": "input_rel",
              "width": 200
            },
            {
              "field": "min_rel",
              "width": 200
            },
            {
              "field": "max_rel",
              "width": 200
            },
            {
              "field": "applied_rel",
              "width": 200
            }
          ]}
            with="cds/modifiers" />
        </HX.Section>
        <HX.Section title="Claims Experience">
          <HX.Table title=" "
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            "eo_cost_included"
          ]}
            fields={[
            {
              "field": "input_value",
              "width": 250
            },
            {
              "field": "relativity",
              "width": 250
            }
          ]}
            with="cds/rating_factors" />
          <HX.Table title=" "
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            "eo_claim_history"
          ]}
            fields={[
            {
              "field": "input_value",
              "width": 250
            },
            {
              "field": "input_rel",
              "width": 250
            },
            {
              "field": "min_rel",
              "width": 250
            },
            {
              "field": "max_rel",
              "width": 250
            },
            {
              "field": "applied_rel",
              "width": 250
            }
          ]}
            with="cds/modifiers" />
        </HX.Section>
        <HX.Section title="Schedule Rating">
          <HX.Table title=" "
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            "eo_schedule_modifier"
          ]}
            fields={[
            {
              "field": "input_value",
              "width": 250
            },
            {
              "field": "min_rel",
              "width": 250
            },
            {
              "field": "max_rel",
              "width": 250
            },
            {
              "field": "applied_rel",
              "width": 250
            }
          ]}
            with="cds/modifiers" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Media Tech"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/mediatech_coverage_selection">
        <HX.Section title="Exposure Information">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/mediatech_territory/input_value"
            ]} />
            <HX.Collection fields={[
              {
                "field": "cds/exposure/aggregate/mediatech_revenue",
                "labelBy": "/cds/mediatech_revenue_currency_label"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Revenue Split by Industry">
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "mediatech_total_revenue_pct"
              ]} />
              <HX.Button task="clear_mediatech_input_task"
                title="Clear All the Input of Revenue %" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table title=" "
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "mediatech_reseller_distributor",
              "mediatech_archiving_records_management",
              "mediatech_training_education",
              "mediatech_automation_word_processing",
              "mediatech_consulting_administrative_services_low_exposure",
              "mediatech_prepackaged_software_products_services_low_exposure",
              "mediatech_technology_hardware_low_exposure",
              "mediatech_internet_access_provider_low_exposure",
              "mediatech_other_class_1",
              null,
              "mediatech_network_design_administration",
              "mediatech_systems_engineering",
              "mediatech_consulting_administrative_services_standard_exposure",
              "mediatech_installation_maintenance_support_services",
              "mediatech_prepackaged_software_products_services_standard_exposure",
              "mediatech_graphic_design_imaging_communications_consulting",
              "mediatech_technology_hardware_standard_exposure",
              "mediatech_internet_access_provider_standard_exposure",
              "mediatech_software_hardware_management_systems",
              "mediatech_telecommunication_consulting_services_low_exposure",
              "mediatech_custom_software_development_low_exposure",
              "mediatech_data_processing_low_exposure",
              "mediatech_advertising_media_consulting_low_exposure",
              "mediatech_internet_based_services_products_low_exposure",
              "mediatech_other_class_2",
              null,
              "mediatech_internet_based_services_products_standard_exposure",
              "mediatech_telecommunication_consulting_services_standard_exposure",
              "mediatech_site_operations",
              "mediatech_custom_software_development_standard_exposure",
              "mediatech_data_processing_standard_exposure",
              "mediatech_advertising_media_consulting_standard_exposure",
              "mediatech_software_hardware_accounting_financial_non_funds_transfer",
              "mediatech_consulting_administrative_services_high_exposure",
              "mediatech_prepackaged_software_products_services_high_exposure",
              "mediatech_technology_hardware_high_exposure",
              "mediatech_internet_access_provider_high_exposure",
              "mediatech_other_class_3",
              null,
              "mediatech_software_hardware_payroll_systems",
              "mediatech_edp_audits_feasibility_studies_needs_evaluation_implementation",
              "mediatech_software_hardware_computer_aided_design_non_structural",
              "mediatech_computer_security_consulting",
              "mediatech_telecommunication_consulting_services_high_exposure",
              "mediatech_custom_software_development_high_exposure",
              "mediatech_data_processing_high_exposure",
              "mediatech_advertising_media_consulting_high_exposure",
              "mediatech_internet_based_services_products_high_exposure",
              "mediatech_other_class_4",
              null,
              "mediatech_computer_security_products_services",
              "mediatech_software_hardware_medical_management_non_diagnostic",
              "mediatech_other_class_5",
              null,
              "mediatech_software_hardware_computer_aided_manufacturing_structural_design",
              "mediatech_software_hardware_medical_management_diagnostic",
              "mediatech_software_hardware_financial_fund_transfer",
              "mediatech_software_hardware_scientific_and_technical",
              "mediatech_system_integration_control_automation_systems",
              "mediatech_hosting",
              "mediatech_other_class_6"
            ]}
              fields={[
              {
                "field": "input_pct",
                "width": 250
              },
              {
                "field": "revenue_amount",
                "width": 250
              },
              {
                "field": "class_name",
                "width": 250
              }
            ]}
              kb-interactive={true} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Optional Coverage">
          <HX.Table title=" "
            data={[
            "mediatech_bipd"
          ]}
            fields={[
            {
              "field": "input_value",
              "width": 250
            },
            {
              "field": "input_relativity",
              "width": 250
            },
            {
              "field": "min_rel",
              "width": 250
            },
            {
              "field": "max_rel",
              "width": 250
            },
            {
              "field": "applied_rel",
              "width": 250
            }
          ]}
            with="cds/modifiers" />
        </HX.Section>
        <HX.Section title="Retroactivity">
          <HX.With context={{
            "path": "cds/rating_factors",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "mediatech_prior_acts/coverage"
              ]} />
              <HX.Collection fields={[
                "mediatech_prior_acts/retroactive_date"
              ]}
                shownBy="mediatech_prior_acts/shown_by" />
              <HX.Collection fields={[
                "mediatech_prior_acts/relativity"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Longevity">
          <HX.With context={{
            "path": "cds/rating_factors",
            "type": "struct"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "mediatech_longevity/business_years"
              ]} />
              <HX.Collection fields={[
                "mediatech_longevity/relativity"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Claims Experience">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/mediatech_cost_included/cost_included"
            ]} />
            <HX.Collection fields={[
              "cds/rating_factors/mediatech_cost_included/relativity"
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table title=" "
            data={[
            "mediatech_claim_experience"
          ]}
            fields={[
            {
              "field": "input_value",
              "width": 250
            },
            {
              "field": "input_relativity",
              "width": 250
            },
            {
              "field": "min_rel",
              "width": 250
            },
            {
              "field": "max_rel",
              "width": 250
            },
            {
              "field": "applied_rel",
              "width": 250
            }
          ]}
            with="cds/modifiers" />
        </HX.Section>
        <HX.Section title="Schedule Rating">
          <HX.Table title=" "
            data={[
            "mediatech_accredited_certified",
            "mediatech_standardized_written_contract",
            "mediatech_risk_management",
            "mediatech_financial_condition",
            "mediatech_atypical_proportion",
            "mediatech_media_content_review",
            "mediatech_privacy_controls",
            "mediatech_overall_quality",
            null,
            "mediatech_total_schedule"
          ]}
            fields={[
            {
              "field": "input_value",
              "width": 250
            },
            {
              "field": "min_val",
              "width": 250
            },
            {
              "field": "max_val",
              "width": 250
            },
            {
              "field": "applied_val",
              "width": 250
            }
          ]}
            with="cds/modifiers" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure GL"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/gl_coverage_selection">
        <HX.Section title="Exposure Information">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/gl_territory/input_value"
            ]} />
            <HX.Collection fields={[
              "cds/exposure/granular/gl_product"
            ]} />
            <HX.Collection fields={[
              {
                "field": "cds/exposure/granular/gl_exposure_info/occupation"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Revenue Tiers">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/local_currency_output"
            ]} />
            <HX.Collection fields={[
              {
                "field": "cds/gl_tier_notes/show_box"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Table title=" "
              data={[
              "gl_revenue"
            ]}
              fields={[
              {
                "field": "tier_input",
                "width": 250
              },
              {
                "field": "revenue_input",
                "labelBy": "/cds/gl_revenue_currency_label",
                "width": 250
              },
              {
                "field": "revenue_input_usd",
                "width": 250
              },
              {
                "field": "exposure_type",
                "width": 250
              }
            ]}
              kb-interactive={true} />
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "/cds/exposure/aggregate/gl_revenue",
                  "labelBy": "/cds/gl_revenue_total_currency_label"
                }
              ]} />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Additional Coverages">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              {
                "field": "/cds/rating_factors/gl_excess_primary/input_value"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Loss Experience">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              {
                "field": "cds/rating_factors/gl_loss/input_value"
              }
            ]} />
            <HX.Collection fields={[
              {
                "field": "cds/rating_factors/gl_loss/relativity"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="UW Judgement (risk based)">
          <HX.Table title=" "
            data={[
            "gl_uw_adjustment"
          ]}
            fields={[
            {
              "field": "input_value",
              "width": 250
            },
            {
              "field": "min_value",
              "width": 250
            },
            {
              "field": "max_value",
              "width": 250
            },
            {
              "field": "applied_value",
              "width": 250
            }
          ]}
            with="cds/modifiers"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Product Tiers Information"
          shownBy="cds/gl_tier_notes/show_box">
          <HX.Notes field="cds/gl_tier_notes/text_box" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Pricing and Rating Summary"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage: E&O"
          shownBy="cds/eo_coverage_selection">
          <HX.Table data={[
            {
              "datum": "layers",
              "width": 250
            }
          ]}
            fields={[
            "coverages/eo/limit",
            "coverages/eo/aggregate_limit",
            "coverages/eo/deductible",
            "coverages/eo/guideline_deductible"
          ]}
            title="Policy Limits and Retentions"
            syncColumnWidthsKey="mySyncedTables1"
            with="cds"
            freezeLeft={0}
            kb-interactive={true}
            transpose={true} />
          <HX.Table title="Priced Quotes"
            data={[
            {
              "datum": "cds/layers",
              "width": 250
            }
          ]}
            syncColumnWidthsKey="mySyncedTables1"
            fields={[
            "coverages/eo/status",
            {
              "field": "coverages/eo/section_reference.case_priced_label",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/eo/section_reference.rater_priced_label",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            "coverages/eo/brokerage",
            {
              "field": "written_line_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/eo/option_selected",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            "coverages/eo/quoted_premium",
            {
              "field": null,
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "technical_premium",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "benchmark_premium",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/eo/technical_premium_before_minimum_prem",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "coverages/eo/technical_premium",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "coverages/eo/benchmark_premium",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            {
              "field": "coverages/eo/tpi",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "tpi",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/eo/bpi_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/eo/bpi",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            {
              "field": "coverages/eo/pflr",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "pflr",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/eo/roc",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "roc",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/eo/uw_adj_impact",
              "shownBy": "cds/standard_fields/is_rater_priced"
            }
          ]}
            freezeLeft={0}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Coverage: Media Tech"
          shownBy="cds/mediatech_coverage_selection">
          <HX.Table data={[
            {
              "datum": "layers",
              "width": 250
            }
          ]}
            fields={[
            "coverages/mediatech/limit",
            "coverages/mediatech/aggregate_limit",
            "coverages/mediatech/additional_defense_limit",
            "coverages/mediatech/deductible",
            "coverages/mediatech/guideline_deductible"
          ]}
            title="Policy Limits and Retentions"
            syncColumnWidthsKey="mySyncedTables1"
            with="cds"
            freezeLeft={0}
            kb-interactive={true}
            transpose={true} />
          <HX.Table title="Priced Quotes"
            data={[
            {
              "datum": "cds/layers",
              "width": 250
            }
          ]}
            syncColumnWidthsKey="mySyncedTables1"
            fields={[
            "coverages/mediatech/status",
            {
              "field": "coverages/mediatech/section_reference.case_priced_label",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/mediatech/section_reference.rater_priced_label",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            "coverages/mediatech/brokerage",
            {
              "field": "written_line_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/mediatech/option_selected",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            "coverages/mediatech/quoted_premium",
            {
              "field": null,
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "technical_premium",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "benchmark_premium",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/mediatech/technical_premium_before_minimum_prem",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "coverages/mediatech/technical_premium",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "coverages/mediatech/benchmark_premium",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            {
              "field": "coverages/mediatech/tpi",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "tpi",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/mediatech/bpi_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/mediatech/bpi",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            {
              "field": "coverages/mediatech/pflr",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "pflr",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/mediatech/roc",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "roc",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/mediatech/uw_adj_impact",
              "shownBy": "cds/standard_fields/is_rater_priced"
            }
          ]}
            freezeLeft={0}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Coverage: GL"
          shownBy="cds/gl_coverage_selection">
          <HX.Table data={[
            {
              "datum": "layers",
              "width": 250
            }
          ]}
            fields={[
            "coverages/gl/limit",
            "coverages/gl/aggregate_limit",
            "coverages/gl/gl_limit_agg",
            "coverages/gl/personal_advertise_limit_agg",
            "coverages/gl/defence_outside_limit",
            "coverages/gl/deductible",
            {
              "field": "coverages/gl/excess_of",
              "shownBy": "/cds/rating_factors/gl_excess_show"
            }
          ]}
            title="Policy Limits in $ USD and Retentions in $ USD "
            syncColumnWidthsKey="mySyncedTables1"
            with="cds"
            kb-interactive={true}
            freezeLeft={0}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection fields={[
              {
                "field": "cds/local_currency_output",
                "shownBy": "cds/gl_coverage_selection"
              }
            ]} />
            <HX.Collection fields={[
              {
                "field": "cds/gl_local_currency",
                "labelBy": "cds/gl_local_currency_label"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane shownBy="cds/gl_local_currency">
            <HX.Table data={[
              {
                "datum": "layers",
                "width": 250
              }
            ]}
              fields={[
              "coverages/gl/limit_local_currency",
              "coverages/gl/aggregate_limit_local_currency",
              "coverages/gl/gl_limit_agg_local_currency",
              "coverages/gl/personal_advertise_limit_agg_local_currency",
              "coverages/gl/defence_outside_limit_local_currency",
              "coverages/gl/deductible_local_currency",
              {
                "field": "coverages/gl/excess_of_local_currency",
                "shownBy": "/cds/rating_factors/gl_excess_show"
              }
            ]}
              title="Policy Limits and Retentions Converted to Source Currency "
              syncColumnWidthsKey="mySyncedTables1"
              with="cds"
              kb-interactive={true}
              freezeLeft={0}
              transpose={true} />
          </HX.Pane>
          <HX.Table title="Priced Quotes in Source Currency"
            data={[
            {
              "datum": "cds/layers",
              "width": 250
            }
          ]}
            fields={[
            "coverages/gl/status",
            {
              "field": "coverages/gl/section_reference.case_priced_label",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/gl/section_reference.rater_priced_label",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            "coverages/gl/brokerage",
            {
              "field": "written_line_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/gl/option_selected",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            "coverages/gl/quoted_premium",
            {
              "field": null,
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "technical_premium",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "benchmark_premium",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/gl/technical_premium_before_minimum_prem",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "coverages/gl/technical_premium",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "coverages/gl/benchmark_premium",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            {
              "field": "coverages/gl/tpi",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "tpi",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/gl/bpi_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/gl/bpi",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            {
              "field": "coverages/gl/pflr",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "pflr",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/gl/roc",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "roc",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            {
              "field": "coverages/gl/uw_adj_impact",
              "shownBy": "cds/standard_fields/is_rater_priced"
            }
          ]}
            syncColumnWidthsKey="mySyncedTables1"
            freezeLeft={0}
            transpose={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        shownBy="cds/standard_fields/is_renewal">
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id"
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title=""
              data={[
              {
                "datum": "cds/layers",
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "deal_status_record"
              },
              {
                "field": "option_selected"
              }
            ]}
              transpose={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data"
              shownBy="cds/rate_change/fetch_rarc_show_hide" />
            <HX.Button task="rarc_task"
              title="Calculate Rate Change"
              shownBy="cds/rate_change/fetch_rarc_show_hide" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Renewal Option 1"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 250
                },
                {
                  "field": "expiring",
                  "width": 250
                }
              ]}
                syncColumnWidthsKey="mySyncedTables1"
                with="rate_change" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change",
                null,
                "total_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 250
                },
                {
                  "field": "uw_selected",
                  "width": 250
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                syncColumnWidthsKey="mySyncedTables1"
                with="rate_change" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/expiry_onlevel_premium_uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Option 2"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 250
                },
                {
                  "field": "expiring",
                  "width": 250
                }
              ]}
                syncColumnWidthsKey="mySyncedTables1"
                with="rate_change" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change",
                null,
                "total_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 250
                },
                {
                  "field": "uw_selected",
                  "width": 250
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                syncColumnWidthsKey="mySyncedTables1"
                with="rate_change" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/expiry_onlevel_premium_uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Option 3"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 250
                },
                {
                  "field": "expiring",
                  "width": 250
                }
              ]}
                syncColumnWidthsKey="mySyncedTables1"
                with="rate_change" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change",
                null,
                "total_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 250
                },
                {
                  "field": "uw_selected",
                  "width": 250
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                syncColumnWidthsKey="mySyncedTables1"
                with="rate_change" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/expiry_onlevel_premium_uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Option 4"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 250
                },
                {
                  "field": "expiring",
                  "width": 250
                }
              ]}
                syncColumnWidthsKey="mySyncedTables1"
                with="rate_change" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change",
                null,
                "total_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 250
                },
                {
                  "field": "uw_selected",
                  "width": 250
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                syncColumnWidthsKey="mySyncedTables1"
                with="rate_change" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/expiry_onlevel_premium_uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}>
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs">
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}
          shownBy="cds/eo_coverage_selection">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/eo/status.read_only",
              "coverages/eo/section_reference.read_only",
              "coverages/eo/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/eo/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}
          shownBy="cds/mediatech_coverage_selection">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/mediatech/status.read_only",
              "coverages/mediatech/section_reference.read_only",
              "coverages/mediatech/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/mediatech/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}
          shownBy="cds/gl_coverage_selection">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/gl/status.read_only",
              "coverages/gl/section_reference.read_only",
              "coverages/gl/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/gl/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 2"
          defaultCollapsed={true}
          shownBy="cds/eo_coverage_selection">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/eo/status.read_only",
              "coverages/eo/section_reference.read_only",
              "coverages/eo/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/eo/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 2"
          defaultCollapsed={true}
          shownBy="cds/mediatech_coverage_selection">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/mediatech/status.read_only",
              "coverages/mediatech/section_reference.read_only",
              "coverages/mediatech/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/mediatech/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 2"
          defaultCollapsed={true}
          shownBy="cds/gl_coverage_selection">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/gl/status.read_only",
              "coverages/gl/section_reference.read_only",
              "coverages/gl/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/gl/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 3"
          defaultCollapsed={true}
          shownBy="cds/eo_coverage_selection">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/eo/status.read_only",
              "coverages/eo/section_reference.read_only",
              "coverages/eo/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/eo/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 3"
          defaultCollapsed={true}
          shownBy="cds/mediatech_coverage_selection">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/mediatech/status.read_only",
              "coverages/mediatech/section_reference.read_only",
              "coverages/mediatech/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/mediatech/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 3"
          defaultCollapsed={true}
          shownBy="cds/gl_coverage_selection">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/gl/status.read_only",
              "coverages/gl/section_reference.read_only",
              "coverages/gl/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/gl/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 4"
          defaultCollapsed={true}
          shownBy="cds/eo_coverage_selection">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/eo/status.read_only",
              "coverages/eo/section_reference.read_only",
              "coverages/eo/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/eo/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/eo/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/eo/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 4"
          defaultCollapsed={true}
          shownBy="cds/mediatech_coverage_selection">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/mediatech/status.read_only",
              "coverages/mediatech/section_reference.read_only",
              "coverages/mediatech/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/mediatech/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/mediatech/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/mediatech/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 4"
          defaultCollapsed={true}
          shownBy="cds/gl_coverage_selection">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "coverages/gl/status.read_only",
              "coverages/gl/section_reference.read_only",
              "coverages/gl/brokerage.read_only",
              {
                "field": "written_line_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/written_line.read_only",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "coverages/gl/quoted_premium.read_only"
              },
              null,
              {
                "field": "technical_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/technical_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "benchmark_premium",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/benchmark_premium.short_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "tpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/tpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/bpi",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              {
                "field": "pflr",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "coverages/gl/pflr",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "coverages/gl/uw_adj_impact",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
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