
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page title="Landing Page"
        shownBy="cds/model_state/show_landing_page">
        <HX.Section title="Start Policy">
          <HX.Pane flow="right">
            <HX.Button task="start_renewal_task"
              title="Start Policy" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="NB:"
          collapsible={false}>
          <HX.Notes field="cds/landing_page_note.read_only_option" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        fullWidth={false}
        shownBy="cds/show_page/show_risk_information">
        <HX.Section title="Policy Information">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/risk_info/database_id",
              "cds/risk_info/submission_date",
              {
                "field": "cds/standard_fields/policy_reference",
                "shownBy": "cds/policy_reference_filled"
              },
              {
                "field": "cds/standard_fields/policy_reference.invalid",
                "shownBy": "cds/policy_reference_not_filled"
              },
              "cds/risk_info/policy_reference_exp"
            ]}
              numCols={1} />
            <HX.Collection fields={[
              {
                "field": "cds/standard_fields/insured_name",
                "shownBy": "cds/insured_name_selected"
              },
              {
                "field": "cds/standard_fields/insured_name.invalid",
                "shownBy": "cds/insured_name_not_selected"
              },
              {
                "field": "cds/risk_info/new_replacement",
                "shownBy": "cds/insured_name_selected"
              },
              {
                "field": "cds/risk_info/new_replacement.invalid",
                "shownBy": "cds/insured_name_not_selected"
              },
              {
                "field": "cds/risk_info/insured_name_final"
              },
              "cds/standard_fields/is_renewal"
            ]}
              numCols={1} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Load Expiring Information"
          shownBy="cds/standard_fields/is_renewal">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/risk_info/expiring_policy_option_id"
            ]} />
            <HX.Button task="expiring_policy_fetch_task"
              title="Load Expiring Policy Information" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              {
                "field": "cds/standard_fields/benchmark_class",
                "shownBy": "cds/risk_class_selected"
              },
              {
                "field": "cds/standard_fields/benchmark_class.invalid",
                "shownBy": "cds/risk_class_not_selected"
              }
            ]} />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                {
                  "field": "/cds/standard_fields/underwriter",
                  "shownBy": "/cds/underwriter_selected"
                },
                {
                  "field": "/cds/standard_fields/underwriter.invalid",
                  "shownBy": "/cds/underwriter_not_selected"
                },
                {
                  "field": "status",
                  "shownBy": "/cds/validation/status/valid"
                },
                {
                  "field": "status.invalid",
                  "shownBy": "/cds/validation/status/invalid"
                },
                "/cds/currencies/source_currency"
              ]}
                numCols={2} />
            </HX.Pane>
          </HX.With>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "hx_core/inception_date",
              "hx_core/expiry_date",
              "cds/risk_info/policy_duration"
            ]}
              numCols={2} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Strikes, Riots and Civil Commotion">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/risk_info/srcc_coverage_given_indicator",
              "cds/risk_info/srcc_fully_excluded_indicator",
              "cds/risk_info/srcc_sublimit_indicator",
              "cds/risk_info/srcc_sublimit"
            ]}
              numCols={2} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/standard_fields/broker",
              "cds/risk_info/broker_contact"
            ]}
              numCols={2} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Underwriter Comments">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Input"
        fullWidth={true}
        shownBy="cds/show_page/show_other">
        <HX.Section title="Clear Exposure Information">
          <HX.Pane flow="right">
            <HX.Button task="clear_exposure_input_task"
              title="Clear Exposure Details Schedule" />
            <HX.Collection fields={[
              null
            ]} />
            <HX.Collection fields={[
              null
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Details">
          <HX.Pane>
            <HX.Table data={[
              "cds/schedule"
            ]}
              fields={[
              "risk_class",
              "region",
              "country",
              "currency",
              "type",
              "tsi",
              "tsi_cnv",
              "sanctioned_country",
              "tsi_band_1",
              "tsi_band_2",
              "tsi_band_3",
              "tsi_band_4",
              "tsi_band_5",
              "tsi_band_6",
              "tsi_band_7",
              "tsi_band_8",
              "tsi_band_9",
              "tsi_band_10"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Prior Year Exposure (Renewal Risks Only)"
          shownBy="cds/standard_fields/is_renewal"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Table data={[
              "cds/schedule_prior"
            ]}
              fields={[
              "risk_class",
              "region",
              "country",
              "currency",
              "type",
              "tsi",
              "tsi_cnv",
              "sanctioned_country",
              "tsi_band_1",
              "tsi_band_2",
              "tsi_band_3",
              "tsi_band_4",
              "tsi_band_5",
              "tsi_band_6",
              "tsi_band_7",
              "tsi_band_8",
              "tsi_band_9",
              "tsi_band_10"
            ]} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page fullWidth={true}
        viewScale={0.8}
        title="Fine Art"
        shownBy="cds/show_page/show_fa">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Exposure Rate Summary">
            <HX.Pane flow="right">
              <HX.Table data={[
                "fa_premises",
                "fa_travel",
                "fa_additional"
              ]}
                fields={[
                "premium",
                "tsi",
                "deductible",
                "ded_perc",
                "credit",
                "uw_adj_impact",
                "prem_post_ded",
                "implied_rate_post_ded",
                "prem_ly",
                "tsi_ly",
                "ded_credit_ly",
                "uw_adj_impact_ly",
                "prem_post_ded_ly"
              ]}
                title="Summary"
                with="coverages" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Premises Rating">
            <HX.Pane flow="right">
              <HX.Table title="Static Art"
                data={[
                "fa_premises/static_art_summary",
                "fa_premises/static_art_summary_subtotal"
              ]}
                fields={[
                "country",
                "tsi",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "exp_band_6",
                "exp_band_7",
                "exp_band_8"
              ]}
                with="coverages" />
              <HX.Table title="Static Art"
                data={[
                "fa_premises/static_art_summary_rates"
              ]}
                fields={[
                "country",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "exp_band_6",
                "exp_band_7",
                "exp_band_8"
              ]}
                with="coverages" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table title="Exhibitions"
                data={[
                "fa_premises/exhibitions_summary",
                "fa_premises/exhibitions_summary_subtotal"
              ]}
                fields={[
                "country",
                "tsi",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "exp_band_6",
                "exp_band_7",
                "exp_band_8"
              ]}
                with="coverages" />
              <HX.Table title="Exhibitions"
                data={[
                "fa_premises/exhibitions_summary_rates"
              ]}
                fields={[
                "country",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "exp_band_6",
                "exp_band_7",
                "exp_band_8"
              ]}
                with="coverages" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table title="FA Misc"
                data={[
                "fa_premises/fa_misc_summary",
                "fa_premises/fa_misc_summary_subtotal"
              ]}
                fields={[
                "country",
                "tsi",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "exp_band_6",
                "exp_band_7",
                "exp_band_8"
              ]}
                with="coverages" />
              <HX.Table title="FA Misc"
                data={[
                "fa_premises/fa_misc_summary_rates"
              ]}
                fields={[
                "country",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "exp_band_6",
                "exp_band_7",
                "exp_band_8"
              ]}
                with="coverages" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Travel Rating">
            <HX.Pane>
              <HX.Table data={[
                "rating_0",
                "rating_1",
                "rating_2",
                "rating_3",
                "rating_4"
              ]}
                fields={[
                "travel_type",
                "tsi",
                "uw_rate_per_100_tsi",
                "prem_rate_per_100_tsi",
                "premium"
              ]}
                with="coverages/fa_travel" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Fine Art Specific">
            <HX.Pane flow="down">
              <HX.Table title="Additional Peril Premium"
                data={[
                "additional_0",
                "additional_1",
                "additional_2",
                "additional_3",
                "additional_4",
                "additional_5",
                "additional_6",
                "additional_7",
                "additional_custom"
              ]}
                fields={[
                "coverage",
                "tsi",
                "uw_rate_per_100_tsi",
                "prem_rate_per_100_tsi",
                "premium"
              ]}
                with="coverages/fa_specific" />
              <HX.Collection fields={[
                null
              ]} />
              <HX.Table title="Ancilliary Premium"
                data={[
                "ancilliary_0",
                "ancilliary_1",
                "ancilliary_2",
                "ancilliary_custom"
              ]}
                fields={[
                "coverage",
                "tsi",
                "uw_rate_per_100_tsi",
                "prem_rate_per_100_tsi",
                "premium"
              ]}
                with="coverages/fa_specific" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="">
            <HX.Pane flow="right">
              <HX.Pane flow="down">
                <HX.Table title="Exhibitions"
                  data={[
                  "exhibitions_0",
                  "exhibitions_1",
                  "exhibitions_2"
                ]}
                  fields={[
                  "coverage",
                  "tsi",
                  "no_of_transits_per_month",
                  "uw_rate_per_100_tsi",
                  "prem_rate_per_100_tsi",
                  "premium"
                ]}
                  with="coverages/fa_specific" />
                <HX.Collection fields={[
                  null
                ]} />
                <HX.Table title="Exhibitions Transit"
                  data={[
                  "exhibitions_transit_0",
                  "exhibitions_transit_1",
                  "exhibitions_transit_2",
                  "exhibitions_transit_3",
                  "exhibitions_transit_4",
                  "exhibitions_transit_custom"
                ]}
                  fields={[
                  "coverage",
                  "tsi",
                  "no_of_transits_each_way",
                  "uw_rate_per_100_tsi",
                  "prem_rate_per_100_tsi",
                  "premium"
                ]}
                  with="coverages/fa_specific" />
              </HX.Pane>
              <HX.Pane flow="down">
                <HX.Table title="Employers Liability"
                  data={[
                  "liability_employers_0",
                  "liability_employers_1",
                  "liability_employers_2",
                  "liability_employers_3"
                ]}
                  fields={[
                  "employers_liability",
                  "no_of_employees",
                  "per_employee",
                  "premium"
                ]}
                  with="coverages/fa_specific" />
                <HX.Table title="Manual Work Surcharge"
                  data={[
                  "liability_manual_0",
                  "liability_manual_1",
                  "liability_manual_2",
                  "liability_manual_3"
                ]}
                  fields={[
                  "manual_work_surcharge",
                  "salary",
                  "prem_rate",
                  "premium"
                ]}
                  with="coverages/fa_specific" />
                <HX.Table title="Public Liability"
                  data={[
                  "liability_public"
                ]}
                  fields={[
                  "public_liability",
                  "include_flag",
                  "premium"
                ]}
                  with="coverages/fa_specific" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Jewellers Block"
        fullWidth={true}
        shownBy="cds/show_page/show_jb">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Exposure Rate Summary">
            <HX.Pane>
              <HX.Table data={[
                "jb_premises",
                "jb_travel",
                "jb_additional"
              ]}
                fields={[
                "premium",
                "tsi",
                "deductible",
                "ded_perc",
                "credit",
                "uw_adj_impact",
                "prem_post_ded",
                "implied_rate_post_ded",
                "prem_ly",
                "tsi_ly",
                "ded_credit_ly",
                "uw_adj_impact_ly",
                "prem_post_ded_ly"
              ]}
                kb-interactive={true}
                with="coverages" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Premises Rating">
            <HX.Pane>
              <HX.Table title="Retail"
                data={[
                "jb_premises/retail_summary",
                "jb_premises/retail_summary_subtotal"
              ]}
                fields={[
                "country",
                "tsi",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "rate_band_1",
                "rate_band_2",
                "rate_band_3",
                "rate_band_4",
                "rate_band_5"
              ]}
                kb-interactive={true}
                with="coverages" />
              <HX.Table title="Wholesale"
                data={[
                "jb_premises/wholesale_summary",
                "jb_premises/wholesale_summary_subtotal"
              ]}
                fields={[
                "country",
                "tsi",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "rate_band_1",
                "rate_band_2",
                "rate_band_3",
                "rate_band_4",
                "rate_band_5"
              ]}
                kb-interactive={true}
                with="coverages" />
              <HX.Table title="Manufacturing"
                data={[
                "jb_premises/manufacturing_summary",
                "jb_premises/manufacturing_summary_subtotal"
              ]}
                fields={[
                "country",
                "tsi",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "rate_band_1",
                "rate_band_2",
                "rate_band_3",
                "rate_band_4",
                "rate_band_5"
              ]}
                kb-interactive={true}
                with="coverages" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Travel Rating">
            <HX.Pane>
              <HX.Table data={[
                "jb_travel/rating"
              ]}
                fields={[
                "origin_region",
                "type_elsewhere_region/type",
                "type_elsewhere_region/elsewhere_region",
                "max_carryings",
                "average_carryings",
                "no_of_days",
                "prem_rate_per_100_tsi",
                "premium"
              ]}
                kb-interactive={true}
                with="coverages" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Jewellers Block Specific">
            <HX.Pane flow="right">
              <HX.Table title="Additional Peril Premiums"
                data={[
                "jb_specific/additional_0",
                "jb_specific/additional_1",
                "jb_specific/additional_2",
                "jb_specific/additional_3",
                "jb_specific/additional_4",
                "jb_specific/additional_5",
                "jb_specific/additional_6",
                "jb_specific/additional_7",
                "jb_specific/additional_8",
                "jb_specific/additional_9",
                "jb_specific/additional_custom"
              ]}
                fields={[
                "coverage",
                "tsi",
                "prem_rate_per_100_tsi",
                "premium"
              ]}
                kb-interactive={true}
                with="coverages" />
              <HX.Table title="Ancillary Premiums"
                data={[
                "jb_specific/ancillary_0",
                "jb_specific/ancillary_1",
                "jb_specific/ancillary_2",
                "jb_specific/ancillary_3",
                "jb_specific/ancillary_custom"
              ]}
                fields={[
                "coverage",
                "tsi",
                "prem_rate_per_100_tsi",
                "premium"
              ]}
                kb-interactive={true}
                with="coverages" />
              <HX.Table title="Shipping Premiums"
                data={[
                "jb_specific/shipping_0",
                "jb_specific/shipping_1",
                "jb_specific/shipping_2",
                "jb_specific/shipping_3",
                "jb_specific/shipping_4",
                "jb_specific/shipping_5",
                "jb_specific/shipping_6",
                "jb_specific/shipping_7",
                "jb_specific/shipping_custom"
              ]}
                fields={[
                "coverage",
                "tsi",
                "prem_rate_per_100_tsi",
                "premium"
              ]}
                kb-interactive={true}
                with="coverages" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page fullWidth={true}
        title="General Specie"
        shownBy="cds/show_page/show_gs">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Exposure Rate Summary">
            <HX.Pane flow="right">
              <HX.Table data={[
                "gs_metals",
                "gs_cash",
                "gs_securities",
                "gs_additional"
              ]}
                fields={[
                "premium",
                "tsi",
                "deductible",
                "ded_perc",
                "credit",
                "uw_adj_impact",
                "prem_post_ded",
                "implied_rate_post_ded",
                "prem_ly",
                "tsi_ly",
                "ded_credit_ly",
                "uw_adj_impact_ly",
                "prem_post_ded_ly"
              ]}
                title="Summary"
                with="coverages" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="General Specie Specific">
            <HX.Pane flow="right">
              <HX.Collection fields={[
                null
              ]} />
              <HX.Collection fields={[
                "/cds/gs_transit_relativity"
              ]} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table data={[
                "static_0",
                "static_1",
                "static_2",
                "static_3",
                "static_4",
                "static_5",
                "static_6",
                null,
                "static_subtotal"
              ]}
                fields={[
                "region",
                "tsi",
                "rate",
                "premium"
              ]}
                title="STATIC - Metal"
                with="coverages/gs_metals" />
              <HX.Table data={[
                "transit_0",
                "transit_1",
                "transit_2",
                "transit_3",
                "transit_4",
                "transit_5",
                "transit_6",
                null,
                "transit_subtotal"
              ]}
                fields={[
                "region",
                "tsi",
                "rate",
                "premium"
              ]}
                title="TRANSIT - Metal"
                with="coverages/gs_metals" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table data={[
                "static_0",
                "static_1",
                "static_2",
                "static_3",
                "static_4",
                "static_5",
                "static_6",
                null,
                "static_subtotal"
              ]}
                fields={[
                "region",
                "tsi",
                "rate",
                "premium"
              ]}
                title="STATIC - Cash"
                with="coverages/gs_cash" />
              <HX.Table data={[
                "transit_0",
                "transit_1",
                "transit_2",
                "transit_3",
                "transit_4",
                "transit_5",
                "transit_6",
                null,
                "transit_subtotal"
              ]}
                fields={[
                "region",
                "tsi",
                "rate",
                "premium"
              ]}
                title="TRANSIT - Cash"
                with="coverages/gs_cash" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table data={[
                "static_0",
                "static_1",
                "static_2",
                "static_3",
                "static_4",
                "static_5",
                "static_6",
                null,
                "static_subtotal"
              ]}
                fields={[
                "region",
                "tsi",
                "rate",
                "premium"
              ]}
                title="STATIC - Securities"
                with="coverages/gs_securities" />
              <HX.Table data={[
                "transit_0",
                "transit_1",
                "transit_2",
                "transit_3",
                "transit_4",
                "transit_5",
                "transit_6",
                null,
                "transit_subtotal"
              ]}
                fields={[
                "region",
                "tsi",
                "rate",
                "premium"
              ]}
                title="TRANSIT - Securities"
                with="coverages/gs_securities" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table data={[
                "custom"
              ]}
                fields={[
                "coverage",
                "tsi",
                "prem_rate_per_100_tsi",
                "premium"
              ]}
                title="Additional"
                with="coverages/gs_additional" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Cash in Transit"
        fullWidth={true}
        shownBy="cds/show_page/show_cit">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Exposure Rate Summary">
            <HX.Pane>
              <HX.Table data={[
                "cit_premises",
                "cit_additional"
              ]}
                fields={[
                "premium",
                "tsi",
                "deductible",
                "ded_perc",
                "credit",
                "uw_adj_impact",
                "prem_post_ded",
                "implied_rate_post_ded",
                "prem_ly",
                "tsi_ly",
                "ded_credit_ly",
                "uw_adj_impact_ly",
                "prem_post_ded_ly"
              ]}
                kb-interactive={true}
                with="coverages" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Premises Rating">
            <HX.Pane>
              <HX.Table title="General"
                data={[
                "cit_general_summary",
                "cit_general_summary_subtotal"
              ]}
                fields={[
                "country",
                "tsi",
                "exp_band_1",
                "exp_band_2",
                "exp_band_3",
                "exp_band_4",
                "exp_band_5",
                "exp_band_6",
                "rate_band_1",
                "rate_band_2",
                "rate_band_3",
                "rate_band_4",
                "rate_band_5",
                "rate_band_6"
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Cash in Transit Specific">
            <HX.Table title="Primary Carrying Method"
              data={[
              "specific_0",
              "specific_1",
              "specific_2",
              "specific_3",
              "specific_4"
            ]}
              fields={[
              "coverage",
              "usa",
              "na_ex_usa",
              "sa",
              "uk",
              "europe",
              "asia",
              "oceania",
              "africa",
              "total",
              "rate_usa",
              "rate_na_ex_usa",
              "rate_sa",
              "rate_uk",
              "rate_europe",
              "rate_asia",
              "rate_oceania",
              "rate_africa",
              "rate_total"
            ]}
              kb-interactive={true}
              with="coverages/cit_additional" />
            <HX.Table title="Other Carrying Methods"
              data={[
              "specific_5",
              "specific_6",
              "specific_7",
              "specific_8",
              "specific_custom"
            ]}
              fields={[
              "coverage",
              "usa",
              "na_ex_usa",
              "sa",
              "uk",
              "europe",
              "asia",
              "oceania",
              "africa",
              "total",
              "rate_usa",
              "rate_na_ex_usa",
              "rate_sa",
              "rate_uk",
              "rate_europe",
              "rate_asia",
              "rate_oceania",
              "rate_africa",
              "rate_total"
            ]}
              kb-interactive={true}
              with="coverages/cit_additional" />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Experience Rating"
        fullWidth={true}
        viewScale={0.9}
        shownBy="cds/show_page/show_other">
        <HX.Section title="Data Source and Experience Rate Summary">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Pane flow="right">
                <HX.Table data={[
                  "cds/experience_rating"
                ]}
                  fields={[
                  "data_source",
                  null,
                  "policy_ref",
                  "expiring_policy_ref"
                ]}
                  transpose={true}
                  kb-interactive={true} />
                <HX.Pane>
                  <HX.Button task="bi_intelligence_fetch_task"
                    title="Populate Experience from BI"
                    shownBy="cds/bi_masking" />
                  <HX.Collection shownBy="cds/bi_masking"
                    fields={[
                    "cds/fetch_bi_task_status_policy",
                    "cds/fetch_bi_task_status_claims"
                  ]} />
                  <HX.Collection shownBy="cds/manual_masking"
                    fields={[
                    null
                  ]} />
                </HX.Pane>
              </HX.Pane>
              <HX.Table data={[
                "cds/experience_final_selections_model",
                "cds/experience_final_selections_uw"
              ]}
                fields={[
                "gn_ulr",
                "gn_ulr_expiry",
                "exp_weight"
              ]}
                transpose={true}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Table data={[
              "cds/experience_lr_summary_list",
              null,
              "cds/experience_lr_summary_subtotal_1",
              "cds/experience_lr_summary_subtotal_2"
            ]}
              fields={[
              "yoa",
              "gnwp",
              "ilr",
              "ulr",
              "ulr_inf"
            ]}
              kb-interactive={true}
              title="Experience Summary" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Experience Rate Calculations - BI"
          shownBy="cds/bi_masking">
          <HX.Pane flow="right">
            <HX.Table data={[
              "cds/experience_attr_projection"
            ]}
              fields={[
              "yoa",
              "incurred",
              "dev_factor",
              "ielr",
              "ultimate"
            ]}
              title="Attritional Claims Projection"
              kb-interactive={true} />
            <HX.Table data={[
              "cds/experience_large_projection"
            ]}
              fields={[
              "ll_avg_lr",
              "ll_assumption",
              "ll_weighted",
              "ultimate"
            ]}
              title="Large Claims Projection"
              kb-interactive={true} />
            <HX.Table data={[
              "cds/experience_cat_projection"
            ]}
              fields={[
              "cat_incurred",
              "cat_average",
              "cat_rms",
              "ultimate"
            ]}
              title="Cat Claims Projection"
              kb-interactive={true} />
            <HX.Table data={[
              "cds/experience_ult_claims"
            ]}
              fields={[
              "ult_incurred",
              "inf_index",
              "ult_incurred_inf",
              "ulr",
              "include"
            ]}
              title="Ultimate Claims"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              null
            ]} />
            <HX.Collection fields={[
              null
            ]} />
            <HX.Table data={[
              "cds/experience_rms_defaults"
            ]}
              fields={[
              "rms_cat_el",
              "rms_cat_prem",
              "rms_cat_lr"
            ]} />
            <HX.Collection fields={[
              null
            ]} />
          </HX.Pane>
          <HX.Pane flow="right" />
        </HX.Section>
        <HX.Section title="Experience Rate Calculations - Manual"
          shownBy="cds/manual_masking">
          <HX.Pane flow="right">
            <HX.Table data={[
              "cds/experience_gnwp_summary_manual"
            ]}
              fields={[
              "yoa",
              "gnwp",
              "rate_change",
              "gnwp_onlvl"
            ]}
              title="Premium Summary"
              kb-interactive={true} />
            <HX.Table data={[
              "cds/experience_attr_projection_manual"
            ]}
              fields={[
              "total_incurred",
              "large_cat",
              "incurred",
              "ultimate"
            ]}
              title="Attritional Claims Projection"
              kb-interactive={true} />
            <HX.Table data={[
              "cds/experience_large_projection_manual"
            ]}
              fields={[
              "ll_assumption",
              "ll_uw_view",
              "ll_selected",
              "ultimate"
            ]}
              title="Large Claims Projection"
              kb-interactive={true} />
            <HX.Table data={[
              "cds/experience_cat_projection_manual"
            ]}
              fields={[
              "cat_uw_view",
              "cat_bp",
              "cat_rms",
              "ultimate"
            ]}
              title="Cat Claims Projection"
              kb-interactive={true} />
            <HX.Table data={[
              "cds/experience_ult_claims_manual"
            ]}
              fields={[
              "ult_incurred",
              "inf_index",
              "ult_incurred_inf",
              "ulr",
              "include"
            ]}
              title="Ultimate Claims"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              null
            ]} />
            <HX.Collection fields={[
              null
            ]} />
            <HX.Collection fields={[
              null
            ]} />
            <HX.Table data={[
              "cds/experience_rms_defaults"
            ]}
              fields={[
              "rms_cat_el",
              "rms_cat_prem",
              "rms_cat_lr"
            ]}
              kb-interactive={true} />
            <HX.Collection fields={[
              null
            ]} />
          </HX.Pane>
          <HX.Pane flow="right" />
        </HX.Section>
        <HX.Section title="Detailed Claim Listing"
          shownBy="cds/bi_masking"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table data={[
              "cds/bi_claims_data"
            ]}
              fields={[
              "PolicyReference",
              "SectionReference",
              "ClaimReference",
              "TriFocusName",
              "PolicyYOA",
              "MarketCatCode",
              "MarketCat",
              "BeazleyShareTotalIncurredInUSD",
              "BeazleyShareTotalOutstandingInUSD",
              "SignedLineMultiplier",
              "TotalIncurredInUSD"
            ]}
              kb-interactive={true}
              dynamic={true}
              maxListVisibleRows={15} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="GNWP and Loss Ratio Charts"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <CustomComponent title="GNWP and ULR"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/experience_loss_ratio_summary_chart"
              }
            ]}
              traces={[
              {
                "color": "#DC199B",
                "field": "gnwp",
                "label": "Premium"
              }
            ]}
              series={[
              {
                "color": "#4B0050",
                "points": [
                  {
                    "list": "cds/experience_loss_ratio_summary_chart",
                    "x": "yoa",
                    "y": "ulr"
                  }
                ],
                "seriesLabel": "ULR"
              },
              {
                "color": "#F56B00",
                "points": [
                  {
                    "list": "cds/experience_loss_ratio_summary_chart",
                    "x": "yoa",
                    "y": "ilr"
                  }
                ],
                "seriesLabel": "ILR"
              },
              {
                "color": "#3741A5",
                "points": [
                  {
                    "list": "cds/experience_loss_ratio_summary_chart",
                    "x": "yoa",
                    "y": "sel_ulr"
                  }
                ],
                "seriesLabel": "Sel. ULR"
              },
              {
                "color": "#00A7E2",
                "points": [
                  {
                    "list": "cds/experience_loss_ratio_summary_chart",
                    "x": "yoa",
                    "y": "uw_ulr"
                  }
                ],
                "seriesLabel": "UW ULR"
              }
            ]}
              xAxisTickAngle={-45}
              gapBetweenBarsSize={0.05}
              yAxisLabel="Premium"
              yAxis2Label="ULR" />
            <CustomComponent title="Loss Ratio by Type"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/experience_loss_ratio_type_chart"
              },
              {
                "labelBy": "yoa",
                "list": "cds/experience_loss_ratio_type_chart"
              },
              {
                "labelBy": "yoa",
                "list": "cds/experience_loss_ratio_type_chart"
              }
            ]}
              traces={[
              {
                "color": "#DC199B",
                "field": "attr_ulr",
                "label": "Attritional ULR"
              },
              {
                "color": "#4B0050",
                "field": "large_ulr",
                "label": "Large ULR"
              },
              {
                "color": "#F56B00",
                "field": "cat_ulr",
                "label": "Cat ULR"
              }
            ]}
              xAxisTickAngle={-45}
              gapBetweenBarsSize={0.05}
              yAxisLabel="Loss Ratio"
              barMode="stack" />
            <HX.Collection fields={[
              null
            ]} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Final Selections and Summary"
        fullWidth={true}
        shownBy="cds/show_page/show_other">
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
        <HX.Section title="Policy Information">
          <HX.Pane>
            <HX.Collection fields={[
              "policy_ref",
              "start_date",
              "end_date",
              "policy_class",
              "currency"
            ]}
              with="cds/final_selection"
              numCols={2} />
          </HX.Pane>
        </HX.Section>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Risk Quality Scoring">
            <HX.Pane shownBy="/cds/jb_masking"
              flow="right">
              <HX.Table title="High Level Questions"
                data={[
                "jb_final_selection"
              ]}
                fields={[
                "high_level_q1",
                "high_level_q2",
                "high_level_q3",
                "high_level_q4",
                "high_level_q5",
                "high_level_q6",
                "high_level_q7",
                "high_level_q8",
                "high_level_q9",
                "high_level_q10"
              ]}
                transpose={true} />
              <HX.Table title="Jewellers Block Specific"
                data={[
                "jb_final_selection"
              ]}
                fields={[
                "specific_q1",
                "specific_q2",
                "specific_q3",
                "specific_q4",
                "specific_q5",
                "specific_q6"
              ]}
                transpose={true} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/jb_masking"
              flow="right">
              <HX.Collection fields={[
                "/cds/final_selection/quality_score"
              ]} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/cit_masking"
              flow="right">
              <HX.Table title="High Level Questions"
                data={[
                "cit_final_selection"
              ]}
                fields={[
                "high_level_q1",
                "high_level_q2",
                "high_level_q3",
                "high_level_q4",
                "high_level_q5",
                "high_level_q6",
                "high_level_q7",
                "high_level_q8",
                "high_level_q9",
                "high_level_q10"
              ]}
                transpose={true} />
              <HX.Table title="Cash In Transit Block Specific"
                data={[
                "cit_final_selection"
              ]}
                fields={[
                "specific_q1",
                "specific_q2",
                "specific_q3",
                "specific_q4",
                "specific_q5",
                "specific_q6"
              ]}
                transpose={true} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/cit_masking"
              flow="right">
              <HX.Collection fields={[
                "/cds/final_selection/quality_score"
              ]} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/fa_masking"
              flow="right">
              Risk Quality Score not used for Fine Art
            </HX.Pane>
            <HX.Pane shownBy="/cds/gs_masking"
              flow="right">
              Risk Quality Score not used for General Specie
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Claims Summary">
            <HX.Pane flow="right">
              <HX.Table data={[
                "/cds/final_claims_summary_table"
              ]}
                fields={[
                "tsi",
                "exp_prem_post_ded",
                "assumed_comms",
                "assumed_lr_gn",
                "perc_cat_bp",
                "perc_cat_data",
                "perc_cat_sel"
              ]}
                kb-interactive={true}
                title="Exposure Loss Cost"
                transpose={true} />
              <HX.Table data={[
                "/cds/final_claims_summary_table"
              ]}
                fields={[
                "exposure_loss_cost_length_adj",
                "experience_loss_cost_length_adj",
                null,
                "rec_exp_weight",
                {
                  "field": "sel_exp_weight",
                  "shownBy": "/cds/validation/sel_exp_weight/valid"
                },
                {
                  "field": "sel_exp_weight.invalid",
                  "shownBy": "/cds/validation/sel_exp_weight/invalid"
                },
                null,
                "final_loss_cost",
                "loss_cost_ly"
              ]}
                kb-interactive={true}
                title="Selected Loss Cost"
                transpose={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Claims Summary - Allocated Loss Cost"
            defaultCollapsed={true}>
            <HX.Pane shownBy="/cds/jb_masking"
              flow="right">
              <HX.Table data={[
                "jb_premises",
                "jb_travel",
                "jb_additional"
              ]}
                fields={[
                "final_summary_tsi",
                "final_summary_prem_post_ded",
                "final_summary_loss_cost_ly",
                "final_summary_final_loss_cost"
              ]}
                title="Jewellers Block Allocated Loss Cost by Sub-type"
                kb-interactive={true}
                with="coverages" />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/fa_masking"
              flow="right">
              <HX.Table data={[
                "fa_premises",
                "fa_travel",
                "fa_additional"
              ]}
                fields={[
                "final_summary_tsi",
                "final_summary_prem_post_ded",
                "final_summary_loss_cost_ly",
                "final_summary_final_loss_cost"
              ]}
                title="Fine Art Allocated Loss Cost by Sub-type"
                kb-interactive={true}
                with="coverages" />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/gs_masking"
              flow="right">
              <HX.Table data={[
                "gs_metals",
                "gs_cash",
                "gs_securities",
                "gs_additional"
              ]}
                fields={[
                "final_summary_tsi",
                "final_summary_prem_post_ded",
                "final_summary_loss_cost_ly",
                "final_summary_final_loss_cost"
              ]}
                title="General Specie Allocated Loss Cost by Sub-type"
                kb-interactive={true}
                with="coverages" />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/cit_masking"
              flow="right">
              <HX.Table data={[
                "cit_premises",
                "cit_additional"
              ]}
                fields={[
                "final_summary_tsi",
                "final_summary_prem_post_ded",
                "final_summary_loss_cost_ly",
                "final_summary_final_loss_cost"
              ]}
                title="Cash in Transit Allocated Loss Cost by Sub-type"
                kb-interactive={true}
                with="coverages" />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Exposure Limits">
            <HX.Pane flow="right">
              <HX.Table data={[
                "/cds/final_prem_summary_limit_table"
              ]}
                fields={[
                {
                  "field": "limit",
                  "shownBy": "/cds/validation/limit/valid"
                },
                {
                  "field": "limit.invalid",
                  "shownBy": "/cds/validation/limit/invalid"
                },
                {
                  "field": "excess",
                  "shownBy": "/cds/validation/excess/valid"
                },
                {
                  "field": "excess.invalid",
                  "shownBy": "/cds/validation/excess/invalid"
                },
                "uw_auth_limit",
                "uw_auth_flag"
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
        <HX.Section title="KPI Summary"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Pane flow="right">
            <HX.Table data={[
              "cds/final_premium_summary_table",
              "cds/final_prem_prioryear_table"
            ]}
              fields={[
              {
                "field": "quoted_premium_slip_curr",
                "shownBy": "/cds/validation/quoted_premium/valid"
              },
              {
                "field": "quoted_premium_slip_curr.invalid",
                "shownBy": "/cds/validation/quoted_premium/invalid"
              },
              "quoted_premium",
              {
                "field": "acq_cost",
                "shownBy": "/cds/validation/brokerage/valid"
              },
              {
                "field": "acq_cost.invalid",
                "shownBy": "/cds/validation/brokerage/invalid"
              },
              {
                "field": "signed_line",
                "shownBy": "/cds/validation/signed_line/valid"
              },
              {
                "field": "signed_line.invalid",
                "shownBy": "/cds/validation/signed_line/invalid"
              },
              null,
              "gg_achieved_rate",
              "gn_achieved_rate"
            ]}
              kb-interactive={true}
              title="Quote Premium Information"
              transpose={true} />
            <HX.Table data={[
              "cds/final_premium_summary_table",
              "cds/final_prem_prioryear_table"
            ]}
              fields={[
              "uw_credit",
              "client_credit",
              "risk_score_credit",
              null,
              "total_credit"
            ]}
              kb-interactive={true}
              title="Selected UW Adjustments"
              transpose={true} />
            <HX.Table data={[
              "cds/final_premium_summary_table",
              "cds/final_prem_prioryear_table"
            ]}
              fields={[
              "tech_prem",
              "bench_prem",
              null,
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj",
              null,
              "implied_roc_pre_uw_adj",
              "expected_profit_pre_uw_adj"
            ]}
              kb-interactive={true}
              title="KPI Pre UW Adjustments"
              transpose={true} />
            <HX.Table data={[
              "cds/final_premium_summary_table",
              "cds/final_prem_prioryear_table"
            ]}
              fields={[
              "tech_prem_adj",
              "bench_prem_adj",
              null,
              "tpi",
              "bpi",
              null,
              "implied_roc",
              "expected_profit"
            ]}
              kb-interactive={true}
              title="KPI Post UW Adjustments"
              transpose={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="KPI Summary"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.Table title="Priced Quotes"
            data={[
            {
              "datum": "cds/layers",
              "width": 250
            }
          ]}
            syncColumnWidthsKey="mySyncedTables1"
            fields={[
            "status.kpi_summary_option",
            "/cds/standard_fields/policy_reference.kpi_summary_option",
            "/cds/final_premium_summary_table/acq_cost.short_label_option",
            "/cds/final_premium_summary_table/signed_line.kpi_summary_option",
            null,
            "quoted_prem_kpi_summary",
            "technical_prem_case_priced",
            "bench_prem_case_priced",
            null,
            "tpi_case_priced",
            "bpi_case_priced",
            null,
            "pflr",
            "implied_roc_pre_uw_adj"
          ]}
            freezeLeft={0}
            transpose={true} />
        </HX.Section>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Achieved Rate Allocation"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Table shownBy="/cds/jb_masking"
                data={[
                "jb_premises",
                "jb_travel",
                "jb_additional"
              ]}
                fields={[
                "final_premium_summary_tsi",
                "final_premium_summary_tech_rate",
                "final_premium_summary_ach_rate",
                "final_premium_summary_tsi_ly",
                "final_premium_summary_tech_rate_ly",
                "final_premium_summary_ach_rate_ly"
              ]}
                kb-interactive={true}
                with="coverages" />
              <HX.Table shownBy="/cds/fa_masking"
                data={[
                "fa_premises",
                "fa_travel",
                "fa_additional"
              ]}
                fields={[
                "final_premium_summary_tsi",
                "final_premium_summary_tech_rate",
                "final_premium_summary_ach_rate",
                "final_premium_summary_tsi_ly",
                "final_premium_summary_tech_rate_ly",
                "final_premium_summary_ach_rate_ly"
              ]}
                kb-interactive={true}
                with="coverages" />
              <HX.Table shownBy="/cds/gs_masking"
                data={[
                "gs_metals",
                "gs_cash",
                "gs_securities",
                "gs_additional"
              ]}
                fields={[
                "final_premium_summary_tsi",
                "final_premium_summary_tech_rate",
                "final_premium_summary_ach_rate",
                "final_premium_summary_tsi_ly",
                "final_premium_summary_tech_rate_ly",
                "final_premium_summary_ach_rate_ly"
              ]}
                kb-interactive={true}
                with="coverages" />
              <HX.Table shownBy="/cds/cit_masking"
                data={[
                "cit_premises",
                "cit_additional"
              ]}
                fields={[
                "final_premium_summary_tsi",
                "final_premium_summary_tech_rate",
                "final_premium_summary_ach_rate",
                "final_premium_summary_tsi_ly",
                "final_premium_summary_tech_rate_ly",
                "final_premium_summary_ach_rate_ly"
              ]}
                kb-interactive={true}
                with="coverages" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
        <HX.Section title="Technical Premium Breakdown"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table data={[
              "cds/final_prem_summary_tp_table",
              "cds/final_prem_summary_tp_postuwadj_table"
            ]}
              fields={[
              "loss_cost",
              "var_exp",
              "fixed_exp",
              "inv_income",
              "reins",
              "acq_cost",
              "cap_load",
              "tech_prem",
              "allocated_capital"
            ]}
              kb-interactive={true}
              transpose={true} />
            <CustomComponent title="Technical Premium Build-Up (Pre UW Adj.)"
              yAxisLabel="Premium"
              textPosition="inside"
              data={[
              {
                "label": "Model Loss Cost",
                "value": "loss_cost"
              },
              {
                "label": "Total Expenses",
                "value": "tot_expense"
              },
              {
                "label": "Investment Income",
                "value": "inv_income"
              },
              {
                "label": "Reinsurance",
                "value": "ri"
              },
              {
                "label": "Capital Load",
                "value": "capital"
              },
              {
                "label": "Brokerage",
                "value": "brokerage"
              },
              {
                "label": "GG Technical Premium",
                "value": "tech_prem"
              },
              {
                "label": "Quote Premium",
                "value": "quoted_premium"
              }
            ]}
              with="cds/final_tp_waterfall" />
            <CustomComponent title="Technical Premium Build-Up (Post UW Adj.)"
              yAxisLabel="Premium"
              textPosition="inside"
              data={[
              {
                "label": "Model Loss Cost",
                "value": "loss_cost"
              },
              {
                "label": "Total Expenses",
                "value": "tot_expense"
              },
              {
                "label": "Investment Income",
                "value": "inv_income"
              },
              {
                "label": "Reinsurance",
                "value": "ri"
              },
              {
                "label": "Capital Load",
                "value": "capital"
              },
              {
                "label": "Brokerage",
                "value": "brokerage"
              },
              {
                "label": "GG Technical Premium",
                "value": "tech_prem"
              },
              {
                "label": "Quote Premium",
                "value": "quoted_premium"
              }
            ]}
              with="cds/final_tp_uwadj_waterfall" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rate Change Summary"
          shownBy="/cds/standard_fields/is_renewal">
          <HX.Pane flow="right">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Table data={[
                "/final_rc_total_summary_view_only",
                "rate_change"
              ]}
                fields={[
                "expiry_premium/uw_selected",
                "exposure_change/uw_selected",
                "deductible_change/uw_selected",
                "limit_change/uw_selected",
                "risk_characteristics_change/uw_selected",
                "terms_conditions_change/uw_selected",
                "risk_adj_premium/uw_selected",
                "quoted_premium"
              ]}
                title="Rate Change Components"
                kb-interactive={true}
                transpose={true} />
              <HX.Table data={[
                "/final_rc_total_summary_view_only",
                "rate_change"
              ]}
                fields={[
                "pure_rc",
                "rate_change/uw_selected",
                "business",
                "rate_change_calculated_pryr"
              ]}
                title="Rate Change Summary"
                kb-interactive={true}
                transpose={true} />
            </HX.With>
            <CustomComponent title="Rate Change Waterfall"
              yAxisLabel="GNWP (USD)"
              textPosition="inside"
              data={[
              {
                "label": "Expiring Premium",
                "value": "exp_prem"
              },
              {
                "label": "Exposure",
                "value": "exposure"
              },
              {
                "label": "Deductibles",
                "value": "deduct"
              },
              {
                "label": "Limits",
                "value": "limit"
              },
              {
                "label": "Risk",
                "value": "risk"
              },
              {
                "label": "T&Cs",
                "value": "t_and_cs"
              },
              {
                "label": "Risk Adj Prem",
                "value": "risk_adj_prem"
              },
              {
                "label": "Quote Premium",
                "value": "quoted_premium"
              }
            ]}
              with="cds/final_rc_waterfall" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        shownBy="cds/show_page/show_other">
        <HX.Section title="Insured Details">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "insured_name",
              "inception_date",
              "policy_ref"
            ]}
              with="cds/rationale"
              title="Current Year" />
            <HX.Collection shownBy="cds/standard_fields/is_renewal"
              fields={[
              "cds/rationale/insured_name_expiry",
              "cds/rationale/inception_date_expiry",
              "cds/risk_info/policy_reference_exp"
            ]}
              title="Last Year" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverholder Background">
          <HX.Pane flow="right">
            <HX.Notes field="coverholder_background"
              title="Current Year"
              with="cds/rationale" />
            <HX.Notes shownBy="/cds/standard_fields/is_renewal"
              field="coverholder_background_expiry"
              title="Last Year"
              with="cds/rationale" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Risk Overview">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "risk_type",
              "construction",
              "signed_line",
              "limit",
              "deductions",
              "avg_limit",
              "top_country",
              null,
              "avg_model_rate",
              "avg_uw_rate",
              "epi",
              "rate_change",
              "attr_lr",
              "cat_load",
              null,
              "bpi",
              "tpi",
              "roc"
            ]}
              with="cds/rationale"
              title="Current Year" />
            <HX.Collection shownBy="/cds/standard_fields/is_renewal"
              fields={[
              "risk_type_expiry",
              "construction_expiry",
              "signed_line_expiry",
              "limit_expiry",
              "deductions_expiry",
              "avg_limit_expiry",
              "top_country_expiry",
              null,
              "avg_model_rate_expiry",
              "avg_uw_rate_expiry",
              "epi_expiry",
              "rate_change_expiry",
              "attr_lr_expiry",
              "cat_load_expiry",
              null,
              "bpi_expiry",
              "tpi_expiry",
              "roc_expiry"
            ]}
              with="cds/rationale"
              title="Last Year" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Underwriter Commentary">
          <HX.Pane flow="right">
            <HX.Notes field="uw_comments"
              title="Current Year"
              with="cds/rationale" />
            <HX.Notes shownBy="/cds/standard_fields/is_renewal"
              field="uw_comments_expiry"
              title="Last Year"
              with="cds/rationale" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rate Change Rationale">
          <HX.Pane flow="right">
            <HX.Notes field="rate_change_rationale"
              title="Current Year"
              with="cds/rationale" />
            <HX.Notes shownBy="/cds/standard_fields/is_renewal"
              field="rate_change_expiry_rationale"
              title="Last Year"
              with="cds/rationale" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Terms and Conditions Change">
          <HX.Pane flow="right">
            <HX.Notes field="tnc_change"
              title="Current Year"
              with="cds/rationale" />
            <HX.Notes shownBy="/cds/standard_fields/is_renewal"
              field="tnc_change_expiry"
              title="Last Year"
              with="cds/rationale" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Risk Profile">
          <HX.Pane flow="right">
            <HX.Notes field="risk_profile"
              title="Current Year"
              with="cds/rationale" />
            <HX.Notes shownBy="/cds/standard_fields/is_renewal"
              field="risk_profile_expiry"
              title="Last Year"
              with="cds/rationale" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Territory Profile and Agg Distribution">
          <HX.Pane flow="right">
            <HX.Notes field="territory_and_agg_dist"
              title="Current Year"
              with="cds/rationale" />
            <HX.Notes shownBy="/cds/standard_fields/is_renewal"
              field="territory_and_agg_dist_expiry"
              title="Last Year"
              with="cds/rationale" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Change / Management">
          <HX.Pane flow="right">
            <HX.Notes field="exposure_change"
              title="Current Year"
              with="cds/rationale" />
            <HX.Notes shownBy="/cds/standard_fields/is_renewal"
              field="exposure_change_expiry"
              title="Last Year"
              with="cds/rationale" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Large Losses">
          <HX.Pane flow="right">
            <HX.Notes field="large_losses"
              title="Current Year"
              with="cds/rationale" />
            <HX.Notes shownBy="/cds/standard_fields/is_renewal"
              field="large_losses_expiry"
              title="Last Year"
              with="cds/rationale" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Generate Rationale Document">
          <HX.Pane>
            <HX.Button task="generate_rationale_doc_task"
              title="Generate Rationale Document" />
            <HX.File field="rationale_file" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={true}
        shownBy="cds/show_page/show_rate_change">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Technical Rate Change">
            <HX.Pane>
              <HX.Table shownBy="/cds/jb_masking"
                data={[
                "jb_rc_tech"
              ]}
                fields={[
                "prem_ly",
                "prem_exp_ly",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/fa_masking"
                data={[
                "fa_rc_tech"
              ]}
                fields={[
                "prem_ly",
                "prem_exp_ly",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/gs_masking"
                data={[
                "gs_rc_tech"
              ]}
                fields={[
                "prem_ly",
                "prem_exp_ly",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/cit_masking"
                data={[
                "cit_rc_tech"
              ]}
                fields={[
                "prem_ly",
                "prem_exp_ly",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
            </HX.Pane>
            <HX.Pane shownBy="/cds/jb_masking"
              flow="right">
              <CustomComponent title="JB Premises Rate Change"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="jb_1_rc_waterfall" />
              <CustomComponent title="JB Travel Rate Change"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="jb_2_rc_waterfall" />
              <CustomComponent title="JB Additional Rate Change"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="jb_3_rc_waterfall" />
            </HX.Pane>
            <HX.Pane shownBy="/cds/fa_masking"
              flow="right">
              <CustomComponent title="FA Premises Rate Change"
                xAxisLabel="Risk component"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="fa_1_rc_waterfall" />
              <CustomComponent title="FA Travel Rate Change"
                xAxisLabel="Risk component"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="fa_2_rc_waterfall" />
              <CustomComponent title="FA Additional Rate Change"
                xAxisLabel="Risk component"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="fa_3_rc_waterfall" />
            </HX.Pane>
            <HX.Pane shownBy="/cds/gs_masking"
              flow="right">
              <CustomComponent title="GS Metals Rate Change"
                xAxisLabel="Risk component"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="gs_1_rc_waterfall" />
              <CustomComponent title="GS Cash Rate Change"
                xAxisLabel="Risk component"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="gs_2_rc_waterfall" />
              <CustomComponent title="GS Securities Rate Change"
                xAxisLabel="Risk component"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="gs_3_rc_waterfall" />
              <CustomComponent title="GS Additional Rate Change"
                xAxisLabel="Risk component"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="gs_4_rc_waterfall" />
            </HX.Pane>
            <HX.Pane shownBy="/cds/cit_masking"
              flow="right">
              <CustomComponent title="CIT Premises Rate Change"
                xAxisLabel="Risk component"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="cit_1_rc_waterfall" />
              <CustomComponent title="CIT Additional Rate Change"
                xAxisLabel="Risk component"
                yAxisLabel="GNWP (USD)"
                data={[
                {
                  "label": "Expiring Premium",
                  "value": "exp_prem"
                },
                {
                  "label": "Exposure",
                  "value": "exposure"
                },
                {
                  "label": "Deductibles",
                  "value": "deduct"
                },
                {
                  "label": "Limits",
                  "value": "limit"
                },
                {
                  "label": "Risk",
                  "value": "risk"
                },
                {
                  "label": "T&Cs",
                  "value": "t_and_cs"
                },
                {
                  "label": "Risk Adj Prem",
                  "value": "risk_adj_prem"
                },
                {
                  "label": "Quote Prem",
                  "value": "quote_prem"
                }
              ]}
                with="cit_2_rc_waterfall" />
            </HX.Pane>
            <HX.Pane>
              <HX.Table shownBy="/cds/jb_masking"
                title="Rate Change Calculations"
                data={[
                "jb_1_rc_tech",
                "jb_2_rc_tech",
                "jb_3_rc_tech"
              ]}
                fields={[
                "subcategory",
                "prem_ly",
                "prem_exp_ly",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/fa_masking"
                title="Rate Change Calculations"
                data={[
                "fa_1_rc_tech",
                "fa_2_rc_tech",
                "fa_3_rc_tech"
              ]}
                fields={[
                "subcategory",
                "prem_ly",
                "prem_exp_ly",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/gs_masking"
                title="Rate Change Calculations"
                data={[
                "gs_1_rc_tech",
                "gs_2_rc_tech",
                "gs_3_rc_tech",
                "gs_4_rc_tech"
              ]}
                fields={[
                "subcategory",
                "prem_ly",
                "prem_exp_ly",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/cit_masking"
                title="Rate Change Calculations"
                data={[
                "cit_1_rc_tech",
                "cit_2_rc_tech",
                "cit_3_rc_tech"
              ]}
                fields={[
                "subcategory",
                "prem_ly",
                "prem_exp_ly",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Underwriter Adjusted Rate Change">
            <HX.Pane>
              <HX.Table shownBy="/cds/jb_masking"
                data={[
                "jb_rc_uwadj"
              ]}
                fields={[
                "prem_ly",
                "prem_exp_ly",
                "uwinput_exp",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "uwinput_ded",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "uwinput_lim",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "uwinput_risk",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "uwinput_tc",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/fa_masking"
                data={[
                "fa_rc_uwadj"
              ]}
                fields={[
                "prem_ly",
                "prem_exp_ly",
                "uwinput_exp",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "uwinput_ded",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "uwinput_lim",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "uwinput_risk",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "uwinput_tc",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/gs_masking"
                data={[
                "gs_rc_uwadj"
              ]}
                fields={[
                "prem_ly",
                "prem_exp_ly",
                "uwinput_exp",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "uwinput_ded",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "uwinput_lim",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "uwinput_risk",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "uwinput_tc",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/cit_masking"
                data={[
                "cit_rc_uwadj"
              ]}
                fields={[
                "prem_ly",
                "prem_exp_ly",
                "uwinput_exp",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "uwinput_ded",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "uwinput_lim",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "uwinput_risk",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "uwinput_tc",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
            </HX.Pane>
            <HX.Pane>
              <HX.Table shownBy="/cds/jb_masking"
                title="Rate Change Calculations"
                data={[
                "jb_1_rc_uwadj",
                "jb_2_rc_uwadj",
                "jb_3_rc_uwadj"
              ]}
                fields={[
                "subcategory",
                "prem_ly",
                "prem_exp_ly",
                "uwinput_exp",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "uwinput_ded",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "uwinput_lim",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "uwinput_risk",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "uwinput_tc",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/fa_masking"
                title="Rate Change Calculations"
                data={[
                "fa_1_rc_uwadj",
                "fa_2_rc_uwadj",
                "fa_3_rc_uwadj"
              ]}
                fields={[
                "subcategory",
                "prem_ly",
                "prem_exp_ly",
                "uwinput_exp",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "uwinput_ded",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "uwinput_lim",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "uwinput_risk",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "uwinput_tc",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/gs_masking"
                title="Rate Change Calculations"
                data={[
                "gs_1_rc_uwadj",
                "gs_2_rc_uwadj",
                "gs_3_rc_uwadj",
                "gs_4_rc_uwadj"
              ]}
                fields={[
                "subcategory",
                "prem_ly",
                "prem_exp_ly",
                "uwinput_exp",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "uwinput_ded",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "uwinput_lim",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "uwinput_risk",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "uwinput_tc",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
              <HX.Table shownBy="/cds/cit_masking"
                title="Rate Change Calculations"
                data={[
                "cit_1_rc_uwadj",
                "cit_2_rc_uwadj",
                "cit_3_rc_uwadj"
              ]}
                fields={[
                "subcategory",
                "prem_ly",
                "prem_exp_ly",
                "uwinput_exp",
                "prem_exp_ty",
                "chg_exp",
                "prem_adj_exp",
                "prem_ded_ly",
                "uwinput_ded",
                "prem_ded_ty",
                "chg_ded",
                "prem_adj_ded",
                "prem_lim_ly",
                "uwinput_lim",
                "prem_lim_ty",
                "chg_lim",
                "prem_adj_lim",
                "prem_risk_ly",
                "uwinput_risk",
                "prem_risk_ty",
                "chg_risk",
                "prem_adj_risk",
                "prem_tc_ly",
                "uwinput_tc",
                "prem_tc_ty",
                "chg_tc",
                "prem_adj_tc",
                "prem_ty",
                "rarc"
              ]} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Standard KPIs"
        shownBy="cds/show_page/show_other">
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
              "/cds/final_premium_summary_table/acq_cost.read_only",
              "/cds/final_premium_summary_table/signed_line.read_only"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "quoted_prem_kpi_summary.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              {
                "field": "/cds/final_premium_summary_table/tech_prem_adj.kpi_summary_option",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "/cds/final_premium_summary_table/bench_prem_adj.kpi_summary_option",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "technical_prem_case_priced",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "bench_prem_case_priced",
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
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": null,
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              {
                "field": "pflr_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "uw_adj_impact",
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