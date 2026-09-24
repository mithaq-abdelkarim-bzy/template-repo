
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
          <HX.Pane>
            <HX.Collection fields={[
              {
                "field": "model_state/landing_page_info"
              }
            ]} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "database_id"
            ]}
              with="cds"
              horizontal={true} />
            <HX.Collection fields={[
              "inception_date",
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "underwriter",
              "benchmark_class"
            ]}
              with="cds/standard_fields"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/insured_name",
              "cds/ccy",
              "cds/standard_fields/is_renewal"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Location">
          <HX.Table title="Location Input"
            data={[
            "cds/rating_factors/location/states",
            null,
            "cds/rating_factors/location"
          ]}
            fields={[
            "state",
            {
              "field": "percentage",
              "shownBy": "/noncds/validation/location_percentage/valid"
            },
            {
              "field": "percentage.notSupported",
              "infoBy": "/noncds/validation/location_percentage/info_text",
              "shownBy": "/noncds/validation/location_percentage/invalid"
            },
            "risk_group",
            "state_factor_selected"
          ]}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/broker_contact",
            "cds/brokerage"
          ]}
            horizontal={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rateable Exposure">
          <HX.Pane flow="right">
            <HX.Notes field="cds/currency_label" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              fields={[
              "other_specify",
              "rateable_exposure_discipline",
              "current_yr_construction_value",
              "current_yr_professional_fees",
              "current_yr_rateable_exposure",
              "last_yr_construction_value",
              "last_yr_professional_fees",
              "last_yr_rateable_exposure",
              "two_yr_ago_construction_value",
              "two_yr_ago_professional_fees",
              "two_yr_ago_rateable_exposure"
            ]}
              data={[
              {
                "datum": "cds/exposure/granular/construction_with_in_house_design"
              },
              {
                "datum": "cds/exposure/granular/construction_with_sub_contracted_design"
              },
              {
                "datum": "cds/exposure/granular/design_only_no_construction"
              },
              {
                "datum": "cds/exposure/granular/construction_only_no_design"
              },
              {
                "datum": "cds/exposure/granular/at_risk_construction_management"
              },
              {
                "datum": "cds/exposure/granular/agency_construction_management"
              },
              {
                "datum": "cds/exposure/granular/other"
              },
              {
                "datum": "cds/exposure/granular/total"
              }
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Underwriter Comments">
          <HX.Notes field="cds/exposure/aggregate/uw_comment" />
        </HX.Section>
        <HX.Section title="Average Rateable Exposure">
          <HX.Pane flow="right">
            <HX.Notes field="cds/currency_label" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              fields={[
              "three_yr_avg_rateable_exposure",
              "two_yr_avg_rateable_exposure",
              "current_yr_avg_rateable_exposure",
              "selected_avg_rateable_exposure",
              "override_avg_rateable_exposure"
            ]}
              data={[
              {
                "datum": "cds/exposure/granular/construction_with_in_house_design"
              },
              {
                "datum": "cds/exposure/granular/construction_with_sub_contracted_design"
              },
              {
                "datum": "cds/exposure/granular/design_only_no_construction"
              },
              {
                "datum": "cds/exposure/granular/construction_only_no_design"
              },
              {
                "datum": "cds/exposure/granular/at_risk_construction_management"
              },
              {
                "datum": "cds/exposure/granular/agency_construction_management"
              },
              {
                "datum": "cds/exposure/granular/other"
              },
              {
                "datum": "cds/exposure/granular/total"
              }
            ]} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Discipline Details"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Engineering Disciplines">
          <HX.Pane flow="right">
            <HX.Notes field="cds/currency_label" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Notes field="cds/exposure/granular/engineering/considerations" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              fields={[
              {
                "field": "other_specify",
                "width": 200
              },
              {
                "field": "percentage",
                "shownBy": "/noncds/validation/engineering_disp_percentage/valid",
                "width": 125
              },
              {
                "field": "percentage.notSupported",
                "infoBy": "/noncds/validation/engineering_disp_percentage/info_text",
                "shownBy": "/noncds/validation/engineering_disp_percentage/invalid",
                "width": 125
              },
              {
                "field": "rateable_exposure",
                "width": 175
              },
              {
                "field": "default_base_rate",
                "width": 200
              },
              {
                "field": "base_rate_override",
                "width": 175
              },
              {
                "field": "base_premium",
                "width": 200
              },
              {
                "field": "guidelines",
                "width": 400
              }
            ]}
              data={[
              "aerospace",
              "architect_comm",
              "architect_resi",
              "aviation",
              "chemical",
              "civil",
              "civil_bridges_roads",
              "cm_atrisk",
              "cm_agency",
              "drafting",
              "electrical",
              "enviro_cons",
              "enviro_labs",
              "fp",
              "forensic",
              "geotechnical",
              "hvac",
              "int_design",
              "landscape",
              "leed_cons",
              "mech",
              "mech_electrical",
              "mining",
              "non_destructive_testing",
              "nuclear",
              "oil_gas",
              "process",
              "struct_resi_inst",
              "struct_steel_stairs",
              "struct_non_resi_inst",
              "surveyor",
              "surveyor_resi",
              "other_one",
              "other_two",
              "other_three",
              "other_four",
              "other_five",
              "total"
            ]}
              with="cds/exposure/granular/engineering" />
            <HX.Collection fields={[
              "size_discount",
              null,
              null,
              null,
              null,
              null
            ]}
              with="cds/exposure/aggregate"
              syncColumnWidthsKey="Collections_width1"
              numCols={6} />
            <HX.Collection fields={[
              "base_premium_size_discount"
            ]}
              with="cds/exposure/granular/engineering/total"
              syncColumnWidthsKey="Collections_width1" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Contractor Disciplines">
          <HX.Pane flow="right">
            <HX.Notes field="cds/currency_label" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Notes field="cds/exposure/granular/contractor/considerations" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              fields={[
              {
                "field": "other_specify",
                "width": 200
              },
              {
                "field": "percentage",
                "shownBy": "/noncds/validation/contractor_disp_percentage/valid",
                "width": 125
              },
              {
                "field": "percentage.notSupported",
                "infoBy": "/noncds/validation/contractor_disp_percentage/info_text",
                "shownBy": "/noncds/validation/contractor_disp_percentage/invalid",
                "width": 125
              },
              {
                "field": "rateable_exposure",
                "width": 175
              },
              {
                "field": "default_base_rate",
                "width": 200
              },
              {
                "field": "base_rate_override",
                "width": 175
              },
              {
                "field": "base_premium",
                "width": 200
              },
              {
                "field": "guidelines",
                "width": 400
              }
            ]}
              data={[
              "asbestos_lead",
              "build_envelop",
              "carpenter",
              "concrete",
              "demolition",
              "drywall",
              "electrical",
              "enviro",
              "fp_dry",
              "fp_wet",
              "foundation_excav",
              "general_comm",
              "general_resi",
              "glazing",
              "hvac_industrial",
              "hvac_non_industrial",
              "landscape",
              "masonry",
              "mech",
              "reno_non_resi",
              "oil_gas",
              "painting",
              "plumbing",
              "resi_reno",
              "roofing",
              "steel",
              "telecom_heavy",
              "telecom_light",
              "utilities",
              "other_one",
              "other_two",
              "other_three",
              "other_four",
              "other_five",
              "total"
            ]}
              with="cds/exposure/granular/contractor" />
            <HX.Collection fields={[
              "size_discount",
              null,
              null,
              null,
              null,
              null
            ]}
              with="cds/exposure/aggregate"
              syncColumnWidthsKey="Collections_width1"
              numCols={6} />
            <HX.Collection fields={[
              "base_premium_size_discount"
            ]}
              with="cds/exposure/granular/contractor/total"
              syncColumnWidthsKey="Collections_width1" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Modifier Details"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rate Modification Factors">
          <HX.Pane>
            <HX.Table kb-interactive={true}
              title="1. Experience Modification"
              data={[
              {
                "datum": "exp_mod",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "incurred_loss"
              },
              {
                "field": "number_of_claims"
              },
              {
                "field": "number_of_incidents"
              },
              {
                "field": "written_premium"
              },
              {
                "field": "incurred_lr",
                "infoBy": "exp_mod/incurred_lr_info_label"
              },
              {
                "field": "exp_mod_factor",
                "infoBy": "exp_mod/exp_mod_factor_info_label"
              }
            ]}
              with="cds/modifiers"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Notes title="Underwriter Comments"
              field="cds/modifiers/exp_mod/uw_comment" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              title="2. Use of Written Contracts"
              data={[
              {
                "datum": "written_contracts",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "percentage"
              },
              {
                "field": "written_contracts_factor"
              }
            ]}
              with="cds/rating_factors"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              title="3. Longevity with Carrier (Applies for RENEWALS ONLY)"
              data={[
              {
                "datum": "longevity_with_carrier",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "yrs_insured"
              },
              {
                "field": "lr"
              },
              {
                "field": "longevity_with_carrier_factor"
              }
            ]}
              with="cds/rating_factors"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              title="4. Longevity"
              data={[
              {
                "datum": "longevity",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "yr_start"
              },
              {
                "field": "yrs_in_business"
              },
              {
                "field": "longevity_factor"
              }
            ]}
              with="cds/rating_factors"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              title="5. Extended Reporting Period"
              data={[
              {
                "datum": "erp",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "erp"
              },
              {
                "field": "erp_factor"
              }
            ]}
              with="cds/rating_factors"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Residential">
          <HX.Pane>
            <HX.Table kb-interactive={true}
              title="6. Residential"
              data={[
              {
                "datum": "resi",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "resi_proj"
              },
              {
                "field": "multiple_units"
              },
              {
                "field": "high_value"
              },
              {
                "field": "condos"
              },
              {
                "field": "resi_proj_factor"
              }
            ]}
              with="cds/rating_factors"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Optional Coverages">
          <HX.Pane>
            <HX.Table kb-interactive={true}
              title="7. Full Prior Act"
              data={[
              {
                "datum": "opt_coverages",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "full_prior_act"
              },
              {
                "field": "full_prior_act_date"
              },
              {
                "field": "retro_factor"
              }
            ]}
              with="cds/rating_factors"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
            <HX.Table kb-interactive={true}
              title="8. CPL Coverage"
              data={[
              {
                "datum": "opt_coverages",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "cpl"
              },
              {
                "field": "cpl_factor"
              }
            ]}
              with="cds/rating_factors"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
            <HX.Table kb-interactive={true}
              title="9. Tech Coverage"
              data={[
              {
                "datum": "opt_coverages",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "tech"
              },
              {
                "field": "tech_cpl_factor"
              }
            ]}
              with="cds/rating_factors"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
            <HX.Table kb-interactive={true}
              title="10. Non-Contributary"
              data={[
              {
                "datum": "opt_coverages",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "non_contributary"
              },
              {
                "field": "non_contributary_factor"
              }
            ]}
              with="cds/rating_factors"
              transpose={true}
              rowHeaderSettings={{
              "minWidth": 750
            }} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Project Types">
          <HX.Pane>
            <HX.Table data={[
              "/cds/exposure/granular/project_type"
            ]}
              fields={[
              {
                "field": "project_type_name",
                "width": 400
              },
              {
                "field": "code_e_o",
                "width": 125
              },
              {
                "field": "fee_percentage",
                "shownBy": "/noncds/validation/fee_percentage/valid",
                "width": 125
              },
              {
                "field": "fee_percentage.notSupported",
                "infoBy": "/noncds/validation/fee_percentage/info_text",
                "shownBy": "/noncds/validation/fee_percentage/invalid",
                "width": 125
              }
            ]}
              dynamic={true}
              freezeLeft={0}
              kb-interactive={true}
              maxListVisibleRows={10} />
            <HX.Table kb-interactive={true}
              title="Category Loadings"
              fields={[
              {
                "field": "code",
                "width": 125
              },
              {
                "field": "category_factor",
                "width": 125
              },
              {
                "field": "fee_percentage",
                "width": 125
              },
              {
                "field": "proportional_loading",
                "width": 200
              }
            ]}
              data={[
              "cat_type_target",
              "cat_type_average",
              "cat_type_expensive",
              "cat_type_refer",
              "cat_type_decline",
              "cat_type_total"
            ]}
              with="cds/exposure/aggregate/project_type_category" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Schedule Rating Factor">
          <HX.Pane>
            <HX.Table kb-interactive={true}
              data={[
              {
                "datum": "qual_of_staff"
              },
              {
                "datum": "rm_attendance"
              },
              {
                "datum": "foreign_work"
              },
              {
                "datum": "loss_prev"
              },
              {
                "datum": "client_type"
              },
              {
                "datum": "contractual_practices"
              },
              {
                "datum": "engi_procure_construct"
              },
              {
                "datum": "peer_review"
              },
              {
                "datum": "total"
              }
            ]}
              fields={[
              {
                "field": "min",
                "width": 300
              },
              {
                "field": "max",
                "width": 300
              },
              {
                "field": "factor",
                "width": 300
              },
              {
                "field": "comment",
                "width": 300
              }
            ]}
              with="cds/modifiers/schedule_rating_factor"
              rowHeaderSettings={{
              "minWidth": 750
            }} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Beazley Rater Pricing"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Section title="Primary Layer">
            <HX.Pane flow="right">
              <HX.Notes field="cds/currency_label" />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table kb-interactive={true}
              rowHeaderSettings={{
              "width": 500
            }}
              title="Primary Layer Priced Quotes (Beazley Share)"
              fields={[
              "ilf_type",
              "limit",
              "aggregate_limit",
              "number_of_reinstatements",
              "deductible",
              "guideline_deductible",
              "minimum_deductible_flag",
              null,
              "ilf_factor",
              "reinstatements_factor",
              "deductible_factor",
              null,
              "beazley_primary",
              {
                "field": "carrier",
                "shownBy": "cds/carrier_primary"
              },
              {
                "field": "carrier_premium",
                "shownBy": "cds/carrier_primary"
              },
              null,
              "quoted_premium",
              "brokerage_primary",
              "technical_premium",
              "benchmark_premium",
              "minimum_premium_flag",
              null,
              "tpi",
              "bpi",
              "pflr",
              "roc"
            ]}
              data={[
              {
                "datum": "cds/options",
                "width": 250
              }
            ]}
              transpose={true} />
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "cds/add_excess_1"
              ]}
                horizontal={true} />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Excess Layers"
            shownBy="cds/add_excess_1">
            <HX.Pane key={1}>
              <HX.Table title="Excess Layer 1"
                shownBy="cds/add_excess_1"
                kb-interactive={true}
                rowHeaderSettings={{
                "width": 500
              }}
                fields={[
                "excess_1_beazley_participation",
                "excess_1_cum_attachment",
                "excess_1_limit",
                null,
                {
                  "field": "excess_1_quoted_premium",
                  "shownBy": "cds/excess_1_beazley_participation"
                },
                {
                  "field": "excess_1_brokerage",
                  "shownBy": "cds/excess_1_beazley_participation"
                },
                {
                  "field": "excess_1_technical_premium",
                  "shownBy": "cds/excess_1_beazley_participation"
                },
                {
                  "field": "excess_1_benchmark_premium",
                  "shownBy": "cds/excess_1_beazley_participation"
                },
                {
                  "field": "excess_1_ilf_curve",
                  "shownBy": "cds/excess_1_beazley_participation"
                },
                {
                  "field": "excess_1_tpi",
                  "shownBy": "cds/excess_1_beazley_participation"
                },
                {
                  "field": "excess_1_bpi",
                  "shownBy": "cds/excess_1_beazley_participation"
                },
                {
                  "field": "excess_1_pflr",
                  "shownBy": "cds/excess_1_beazley_participation"
                },
                {
                  "field": "excess_1_roc",
                  "shownBy": "cds/excess_1_beazley_participation"
                },
                null,
                {
                  "field": "excess_1_carrier_premium"
                },
                {
                  "field": "excess_1_carrier_tpi"
                },
                {
                  "field": "excess_1_carrier_bpi"
                }
              ]}
                data={[
                {
                  "datum": "cds/options",
                  "width": 250
                }
              ]}
                transpose={true} />
              <HX.Pane flow="right"
                shownBy="cds/add_excess_1">
                <HX.Collection fields={[
                  "cds/add_excess_2"
                ]}
                  horizontal={true} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane key={2}>
              <HX.Table title="Excess Layer 2"
                shownBy="cds/add_excess_2"
                kb-interactive={true}
                rowHeaderSettings={{
                "width": 500
              }}
                fields={[
                "excess_2_beazley_participation",
                "excess_2_cum_attachment",
                "excess_2_limit",
                null,
                {
                  "field": "excess_2_quoted_premium",
                  "shownBy": "cds/excess_2_beazley_participation"
                },
                {
                  "field": "excess_2_brokerage",
                  "shownBy": "cds/excess_2_beazley_participation"
                },
                {
                  "field": "excess_2_technical_premium",
                  "shownBy": "cds/excess_2_beazley_participation"
                },
                {
                  "field": "excess_2_benchmark_premium",
                  "shownBy": "cds/excess_2_beazley_participation"
                },
                {
                  "field": "excess_2_ilf_curve",
                  "shownBy": "cds/excess_2_beazley_participation"
                },
                {
                  "field": "excess_2_tpi",
                  "shownBy": "cds/excess_2_beazley_participation"
                },
                {
                  "field": "excess_2_bpi",
                  "shownBy": "cds/excess_2_beazley_participation"
                },
                {
                  "field": "excess_2_pflr",
                  "shownBy": "cds/excess_2_beazley_participation"
                },
                {
                  "field": "excess_2_roc",
                  "shownBy": "cds/excess_2_beazley_participation"
                },
                null,
                {
                  "field": "excess_2_carrier_premium"
                },
                {
                  "field": "excess_2_carrier_tpi"
                },
                {
                  "field": "excess_2_carrier_bpi"
                }
              ]}
                data={[
                {
                  "datum": "cds/options",
                  "width": 250
                }
              ]}
                transpose={true} />
              <HX.Pane flow="right"
                shownBy="cds/add_excess_2">
                <HX.Collection fields={[
                  "cds/add_excess_3"
                ]}
                  horizontal={true} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane key={3}>
              <HX.Table title="Excess Layer 3"
                shownBy="cds/add_excess_3"
                kb-interactive={true}
                rowHeaderSettings={{
                "width": 500
              }}
                fields={[
                "excess_3_beazley_participation",
                "excess_3_cum_attachment",
                "excess_3_limit",
                null,
                {
                  "field": "excess_3_quoted_premium",
                  "shownBy": "cds/excess_3_beazley_participation"
                },
                {
                  "field": "excess_3_brokerage",
                  "shownBy": "cds/excess_3_beazley_participation"
                },
                {
                  "field": "excess_3_technical_premium",
                  "shownBy": "cds/excess_3_beazley_participation"
                },
                {
                  "field": "excess_3_benchmark_premium",
                  "shownBy": "cds/excess_3_beazley_participation"
                },
                {
                  "field": "excess_3_ilf_curve",
                  "shownBy": "cds/excess_3_beazley_participation"
                },
                {
                  "field": "excess_3_tpi",
                  "shownBy": "cds/excess_3_beazley_participation"
                },
                {
                  "field": "excess_3_bpi",
                  "shownBy": "cds/excess_3_beazley_participation"
                },
                {
                  "field": "excess_3_pflr",
                  "shownBy": "cds/excess_3_beazley_participation"
                },
                {
                  "field": "excess_3_roc",
                  "shownBy": "cds/excess_3_beazley_participation"
                },
                null,
                {
                  "field": "excess_3_carrier_premium"
                },
                {
                  "field": "excess_3_carrier_tpi"
                },
                {
                  "field": "excess_3_carrier_bpi"
                }
              ]}
                data={[
                {
                  "datum": "cds/options",
                  "width": 250
                }
              ]}
                transpose={true} />
              <HX.Pane flow="right"
                shownBy="cds/add_excess_3">
                <HX.Collection fields={[
                  "cds/add_excess_4"
                ]}
                  horizontal={true} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane key={4}>
              <HX.Table title="Excess Layer 4"
                shownBy="cds/add_excess_4"
                kb-interactive={true}
                rowHeaderSettings={{
                "width": 500
              }}
                fields={[
                "excess_4_beazley_participation",
                "excess_4_cum_attachment",
                "excess_4_limit",
                null,
                {
                  "field": "excess_4_quoted_premium",
                  "shownBy": "cds/excess_4_beazley_participation"
                },
                {
                  "field": "excess_4_brokerage",
                  "shownBy": "cds/excess_4_beazley_participation"
                },
                {
                  "field": "excess_4_technical_premium",
                  "shownBy": "cds/excess_4_beazley_participation"
                },
                {
                  "field": "excess_4_benchmark_premium",
                  "shownBy": "cds/excess_4_beazley_participation"
                },
                {
                  "field": "excess_4_ilf_curve",
                  "shownBy": "cds/excess_4_beazley_participation"
                },
                {
                  "field": "excess_4_tpi",
                  "shownBy": "cds/excess_4_beazley_participation"
                },
                {
                  "field": "excess_4_bpi",
                  "shownBy": "cds/excess_4_beazley_participation"
                },
                {
                  "field": "excess_4_pflr",
                  "shownBy": "cds/excess_4_beazley_participation"
                },
                {
                  "field": "excess_4_roc",
                  "shownBy": "cds/excess_4_beazley_participation"
                },
                null,
                {
                  "field": "excess_4_carrier_premium"
                },
                {
                  "field": "excess_4_carrier_tpi"
                },
                {
                  "field": "excess_4_carrier_bpi"
                }
              ]}
                data={[
                {
                  "datum": "cds/options",
                  "width": 250
                }
              ]}
                transpose={true} />
              <HX.Pane flow="right"
                shownBy="cds/add_excess_4">
                <HX.Collection fields={[
                  "cds/add_excess_5"
                ]}
                  horizontal={true} />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane key={5}>
              <HX.Table title="Excess Layer 5"
                shownBy="cds/add_excess_5"
                kb-interactive={true}
                rowHeaderSettings={{
                "width": 500
              }}
                fields={[
                "excess_5_beazley_participation",
                "excess_5_cum_attachment",
                "excess_5_limit",
                null,
                {
                  "field": "excess_5_quoted_premium",
                  "shownBy": "cds/excess_5_beazley_participation"
                },
                {
                  "field": "excess_5_brokerage",
                  "shownBy": "cds/excess_5_beazley_participation"
                },
                {
                  "field": "excess_5_technical_premium",
                  "shownBy": "cds/excess_5_beazley_participation"
                },
                {
                  "field": "excess_5_benchmark_premium",
                  "shownBy": "cds/excess_5_beazley_participation"
                },
                {
                  "field": "excess_5_ilf_curve",
                  "shownBy": "cds/excess_5_beazley_participation"
                },
                {
                  "field": "excess_5_tpi",
                  "shownBy": "cds/excess_5_beazley_participation"
                },
                {
                  "field": "excess_5_bpi",
                  "shownBy": "cds/excess_5_beazley_participation"
                },
                {
                  "field": "excess_5_pflr",
                  "shownBy": "cds/excess_5_beazley_participation"
                },
                {
                  "field": "excess_5_roc",
                  "shownBy": "cds/excess_5_beazley_participation"
                },
                null,
                {
                  "field": "excess_5_carrier_premium"
                },
                {
                  "field": "excess_5_carrier_tpi"
                },
                {
                  "field": "excess_5_carrier_bpi"
                }
              ]}
                data={[
                {
                  "datum": "cds/options",
                  "width": 250
                }
              ]}
                transpose={true} />
              <HX.Pane flow="right"
                shownBy="cds/add_excess_5">
                {false}
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Selected Option"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/option_selected"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table kb-interactive={true}
            fields={[
            "cum_attachment",
            "limit",
            "status_view",
            "section_reference_view",
            "quoted_premium",
            "brokerage",
            "technical_premium",
            "benchmark_premium",
            "tpi",
            "bpi",
            "pflr",
            "roc"
          ]}
            data={[
            {
              "datum": "cds/primary"
            },
            {
              "datum": "cds/layers",
              "elementLabelBy": "layer_label"
            }
          ]}
            filter="excess_flag" />
        </HX.Section>
        <HX.Section title="Priced Quotes (Beazley Share)"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.Pane flow="right">
            <HX.Notes field="cds/currency_label" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table kb-interactive={true}
              data={[
              {
                "datum": "cds/options",
                "width": 250
              }
            ]}
              fields={[
              "status_view",
              "section_reference_view",
              "brokerage",
              "written_line_view",
              null,
              "quoted_premium",
              "technical_premium_case_priced",
              "benchmark_premium_case_priced",
              null,
              "tpi_case_priced",
              "bpi_case_priced",
              null,
              "pflr_case_priced",
              "roc_case_priced"
            ]}
              transpose={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        shownBy="model_state/show_rate_change_layer_no_ia_use">
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id",
              null
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title="Deal Status by Renewal Layers"
              data={[
              {
                "datum": "cds/layers",
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status"
              }
            ]}
              transpose={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data"
              shownBy="cds/rate_change/has_rarc_not_run" />
            <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
            <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
            <HX.Button title="Calculate Rate Change"
              task="rarc_task"
              shownBy="cds/standard_fields/is_rater_priced" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
          </HX.Pane>
          <HX.Section title="Rate Change Instructions and Key"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Notes field="cds/rate_change/instructions" />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Renewal: Primary Layer"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                {
                  "field": "rate_change/expiring_layer",
                  "labelBy": "rate_change/expiring_layer_info"
                },
                null,
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced/uw_selected",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal: Excess Layer 1"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                {
                  "field": "rate_change/expiring_layer",
                  "labelBy": "rate_change/expiring_layer_info"
                },
                null,
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced/uw_selected",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal: Excess Layer 2"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                {
                  "field": "rate_change/expiring_layer",
                  "labelBy": "rate_change/expiring_layer_info"
                },
                null,
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced/uw_selected",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal: Excess Layer 3"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                {
                  "field": "rate_change/expiring_layer",
                  "labelBy": "rate_change/expiring_layer_info"
                },
                null,
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced/uw_selected",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal: Excess Layer 4"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                {
                  "field": "rate_change/expiring_layer",
                  "labelBy": "rate_change/expiring_layer_info"
                },
                null,
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced/uw_selected",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal: Excess Layer 5"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                {
                  "field": "rate_change/expiring_layer",
                  "labelBy": "rate_change/expiring_layer_info"
                },
                null,
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "currency",
                "premium/line_100pct/annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced/uw_selected",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs">
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 2"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 3"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 4"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 5"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 6"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Option 1"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_case_priced">
          <HX.With context={{
            "index": 0,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage_view",
              "written_line_case_priced"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_view",
              null,
              "technical_premium_case_priced",
              "benchmark_premium_case_priced",
              "tpi_case_priced",
              "bpi_case_priced_view"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr_case_priced",
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Option 2"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_case_priced">
          <HX.With context={{
            "index": 1,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage_view",
              "written_line_case_priced"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_view",
              null,
              "technical_premium_case_priced",
              "benchmark_premium_case_priced",
              "tpi_case_priced",
              "bpi_case_priced_view"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr_case_priced",
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Option 3"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_case_priced">
          <HX.With context={{
            "index": 2,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage_view",
              "written_line_case_priced"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_view",
              null,
              "technical_premium_case_priced",
              "benchmark_premium_case_priced",
              "tpi_case_priced",
              "bpi_case_priced_view"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr_case_priced",
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Option 4"
          defaultCollapsed={true}
          shownBy="cds/standard_fields/is_case_priced">
          <HX.With context={{
            "index": 3,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage_view",
              "written_line_case_priced"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_view",
              null,
              "technical_premium_case_priced",
              "benchmark_premium_case_priced",
              "tpi_case_priced",
              "bpi_case_priced_view"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr_case_priced",
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};