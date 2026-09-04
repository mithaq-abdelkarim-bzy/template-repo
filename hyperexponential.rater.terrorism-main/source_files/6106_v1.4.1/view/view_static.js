
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
            <HX.Pane ratio={2}>
              <HX.Notes field="model_state/landing_page_info" />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rating Model">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology",
              null
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Account Details">
          <HX.Collection fields={[
            "inception_date",
            "expiry_date"
          ]}
            with="hx_core"
            horizontal={true} />
          <HX.Collection with="cds/standard_fields"
            fields={[
            "underwriter",
            "insured_name"
          ]}
            horizontal={true} />
          <HX.Collection fields={[
            "cds/currencies/source_currency",
            "cds/policy_info/source_system"
          ]}
            horizontal={true} />
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection fields={[
              "section_reference",
              "status",
              "/cds/standard_fields/is_renewal"
            ]}
              horizontal={true} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Policy Information">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection fields={[
              "written_line",
              "written_line_basis",
              "order"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "quoted_premium_100_pct",
              "brokerage",
              "line"
            ]}
              horizontal={true} />
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/exposure/granular/countries",
            "type": "list"
          }}>
            <HX.Collection fields={[
              "limit",
              "excess",
              "deductible"
            ]}
              horizontal={true} />
          </HX.With>
          <HX.Collection fields={[
            "cds/policy_info/single_country_only",
            null,
            null
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Single Country Details"
          shownBy="cds/policy_info/single_country_only">
          <HX.With context={{
            "index": 0,
            "path": "cds/exposure/granular/countries",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection numCols={3}
                fields={[
                "country",
                "coverage",
                "total_sum_insured",
                "no_of_locations",
                "subcoverage",
                "bi_sum_insured",
                "pml",
                "sublimit",
                "pd_sum_insured"
              ]} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Broker Details - Optional">
          <HX.Collection with="cds"
            fields={[
            "standard_fields/broker",
            "policy_info/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Countries"
        shownBy="model_state/show_after_landing_page"
        fullWidth={true}
        viewScale={0.8}>
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="Country Details">
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "show_ihs_scores",
                "show_country_clean"
              ]}
                horizontal={true} />
              <HX.Button task="clean_country_task"
                title="Paste the Cleaned Country Names to 'Country' "
                shownBy="show_country_clean" />
              <HX.Collection fields={[
                null,
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="copy_country_covers_task"
                title="Copy [Coverage, Limit, Excess, Sub-coverage, Sub-limit, Deductible] to all countries" />
            </HX.Pane>
            <HX.Table data={[
              "countries"
            ]}
              fields={[
              "rated_country",
              "country",
              "proxy_rating_country",
              {
                "field": "country_clean",
                "shownBy": "show_country_clean"
              },
              "no_of_locations",
              "pml",
              "coverage",
              "limit",
              "excess",
              "subcoverage",
              "sublimit",
              "deductible",
              "total_sum_insured",
              "bi_sum_insured",
              "pd_sum_insured",
              "liability_risk",
              "attritional_risk",
              "geog_risk",
              "location_cat_risk",
              {
                "field": "political",
                "shownBy": "show_ihs_scores"
              },
              {
                "field": "terrorism_raw",
                "shownBy": "show_ihs_scores"
              },
              {
                "field": "labour_strikes",
                "shownBy": "show_ihs_scores"
              },
              {
                "field": "protests_riots",
                "shownBy": "show_ihs_scores"
              },
              {
                "field": "interstate_war",
                "shownBy": "show_ihs_scores"
              },
              {
                "field": "civil_war",
                "shownBy": "show_ihs_scores"
              },
              "civil_unrest",
              "war",
              "terrorism",
              "selected_sum_insured",
              {
                "field": "warning",
                "shownBy": "show_warning"
              }
            ]}
              dynamic={true}
              kb-interactive={true}
              freezeLeft={1}
              freezeRight={1} />
          </HX.Section>
        </HX.With>
        <HX.With context={{
          "path": "cds/exposure/granular",
          "type": "struct"
        }}>
          <HX.Section title="IHS Data"
            shownBy="has_at_least_one_country">
            <HX.Pane>
              <HX.Pane flow="right">
                <HX.Button title="Refresh IHS Scores"
                  task="task_fetch_ihs_data" />
                <HX.Notes field="refresh_message" />
              </HX.Pane>
              <HX.Pane shownBy="show_chart">
                <HX.Collection fields={[
                  "selected_country",
                  null
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "country_message",
                  null
                ]}
                  horizontal={true}
                  shownBy="show_country_message" />
                <HX.Pane flow="right">
                  <CustomComponent title="Historical Values"
                    xAxisLabel="Time"
                    yAxisLabel="Risk"
                    series={[
                    {
                      "points": [
                        {
                          "list": "/ihs_political",
                          "x": "updated_on",
                          "y": "value"
                        }
                      ],
                      "seriesLabel": "Political"
                    },
                    {
                      "points": [
                        {
                          "list": "/ihs_terrorism_raw",
                          "x": "updated_on",
                          "y": "value"
                        }
                      ],
                      "seriesLabel": "Terrorism"
                    },
                    {
                      "points": [
                        {
                          "list": "/ihs_labour_strikes",
                          "x": "updated_on",
                          "y": "value"
                        }
                      ],
                      "seriesLabel": "LabourStrikes"
                    },
                    {
                      "points": [
                        {
                          "list": "/ihs_protests_riots",
                          "x": "updated_on",
                          "y": "value"
                        }
                      ],
                      "seriesLabel": "ProtestsAndRiots"
                    },
                    {
                      "points": [
                        {
                          "list": "/ihs_interstate_war",
                          "x": "updated_on",
                          "y": "value"
                        }
                      ],
                      "seriesLabel": "InterstateWar"
                    },
                    {
                      "points": [
                        {
                          "list": "/ihs_civil_war",
                          "x": "updated_on",
                          "y": "value"
                        }
                      ],
                      "seriesLabel": "CivilWar"
                    }
                  ]} />
                  <HX.Table data={[
                    "/ihs_descriptions"
                  ]}
                    fields={[
                    "risk_name",
                    "description"
                  ]}
                    dynamic={true}
                    kb-interactive={true}
                    freezeLeft={1} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Exposure Details"
        shownBy="model_state/show_after_landing_page"
        viewScale={0.9}>
        <HX.Section title="Cover Details">
          <HX.Pane flow="right"
            reflow={true}>
            <HX.Table title="Summary Details"
              data={[
              "cds/exposure/aggregate"
            ]}
              fields={[
              {
                "field": "total_sum_insured",
                "labelAlign": "right"
              },
              {
                "field": "bi_sum_insured",
                "labelAlign": "right"
              },
              {
                "field": "pd_sum_insured",
                "labelAlign": "right"
              },
              {
                "field": "policy_limit",
                "labelAlign": "right"
              },
              {
                "field": "policy_sublimit",
                "labelAlign": "right"
              },
              {
                "field": "policy_excess",
                "labelAlign": "right"
              },
              {
                "field": "policy_deductible",
                "labelAlign": "right"
              },
              {
                "field": "no_of_locations",
                "labelAlign": "right"
              },
              {
                "field": "agg_discount",
                "labelAlign": "right"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Pane flow="down">
              <HX.Table title="Additional Details"
                data={[
                "cds/exposure/aggregate/details"
              ]}
                fields={[
                {
                  "field": "limit_type",
                  "labelAlign": "right"
                },
                {
                  "field": "bi_wait_period",
                  "labelAlign": "right"
                },
                {
                  "field": "bi_indemnity_period",
                  "labelAlign": "right"
                },
                {
                  "field": "contingent_bi",
                  "labelAlign": "right"
                },
                {
                  "field": "aggregate_usage",
                  "labelAlign": "right"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
         
                <HX.Collection fields={[
                  "coverages/construction/is_covered"
                ]}
                  horizontal={true} />
         
              </HX.With>
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="IHS Score Adjustment - tabular (click to reveal)"
          shownBy="/model_state/not_migrated"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Table data={[
              null,
              {
                "datum": "countries",
                "maxWidth": 280
              }
            ]}
              fields={[
              "rated_country",
              "leading_peril",
              "selected_sum_insured_contribution",
              null,
              "labour_strikes",
              "protests_riots",
              "civil_unrest",
              "override_civil_unrest",
              "selected_civil_unrest",
              {
                "field": "civil_unrest_roe_selected",
                "infoBy": "civil_unrest_info"
              },
              null,
              "interstate_war",
              "civil_war",
              "war",
              "override_war",
              "selected_war",
              {
                "field": "war_roe_selected",
                "infoBy": "war_info"
              },
              null,
              "terrorism_raw",
              "political",
              "civil_unrest",
              "war",
              "terrorism",
              "override_terrorism",
              "selected_terrorism",
              {
                "field": "terrorism_roe_selected",
                "infoBy": "terrorism_info"
              }
            ]}
              kb-interactive={true}
              transpose={true}
              freezeLeft={0} />
          </HX.With>
        </HX.Section>
        <HX.Section title="IHS Score Adjustment - detailed (click to reveal)"
          shownBy="/model_state/not_migrated"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/exposure/granular",
            "type": "struct"
          }}>
            <HX.Selector title="Select the country to adjust - only showing covered perils based on selected coverage and subcoverage"
              data={[
              "countries"
            ]}
              dropdown="rated_country">
              <HX.Pane shownBy="has_civil_unrest">
                <HX.Collection title="Civil Unrest"
                  fields={[
                  "labour_strikes",
                  "protests_riots"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "civil_unrest",
                  "override_civil_unrest",
                  "selected_civil_unrest"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "civil_unrest_roe_calculated",
                  null,
                  "civil_unrest_roe_selected"
                ]}
                  horizontal={true} />
              </HX.Pane>
              <HX.Pane shownBy="has_war">
                <HX.Collection title="War"
                  fields={[
                  "interstate_war",
                  "civil_war"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "war",
                  "override_war",
                  "selected_war"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "war_roe_calculated",
                  null,
                  "war_roe_selected"
                ]}
                  horizontal={true} />
              </HX.Pane>
              <HX.Pane shownBy="has_terrorism">
                <HX.Collection title="Terrorism"
                  fields={[
                  "political",
                  "terrorism_raw"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "civil_unrest",
                  "war"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "terrorism",
                  "override_terrorism",
                  "selected_terrorism"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "terrorism_roe_calculated",
                  null,
                  "terrorism_roe_selected"
                ]}
                  horizontal={true} />
              </HX.Pane>
            </HX.Selector>
          </HX.With>
        </HX.Section>
        <HX.Section title="Risk Adjustments">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="down">
              <HX.Pane shownBy="/model_state/is_migrated">
   
                <HX.Table title="Underwriter Adjustments - including legacy IHS override approach"
                  data={[
                  "security",
                  "industry",
                  "policy",
                  "ihs_score"
                ]}
                  fields={[
                  null,
                  {
                    "field": "level",
                    "maxWidth": 140
                  },
                  null,
                  {
                    "field": "calculated",
                    "maxWidth": 140
                  },
                  null,
                  {
                    "field": "min",
                    "maxWidth": 100
                  },
                  {
                    "field": "override",
                    "maxWidth": 100
                  },
                  {
                    "field": "max",
                    "maxWidth": 100
                  },
                  null,
                  {
                    "field": "selected",
                    "maxWidth": 100
                  },
                  null,
                  {
                    "field": "description"
                  }
                ]}
                  with="risk_adjustments"
                  kb-interactive={true}
                  freezeLeft={0} />
   
              </HX.Pane>
              <HX.Pane shownBy="/model_state/not_migrated">
  
                <HX.Table title="Underwriter Adjustments"
                  data={[
                  "security",
                  "industry",
                  "policy",
                  "ihs_score_read_only",
                  "ihs_score_expiring"
                ]}
                  fields={[
                  null,
                  {
                    "field": "level",
                    "maxWidth": 140
                  },
                  null,
                  {
                    "field": "calculated",
                    "maxWidth": 140
                  },
                  null,
                  {
                    "field": "min",
                    "maxWidth": 100
                  },
                  {
                    "field": "override",
                    "maxWidth": 100
                  },
                  {
                    "field": "max",
                    "maxWidth": 100
                  },
                  null,
                  {
                    "field": "selected",
                    "maxWidth": 100
                  },
                  null,
                  {
                    "field": "description"
                  }
                ]}
                  with="risk_adjustments"
                  kb-interactive={true}
                  freezeLeft={0} />
                                             
              </HX.Pane>
              <HX.Collection title="Summary"
                fields={[
                "uw_ihs_adjustment",
                "total_adj_score",
                "uw_multiplier"
              ]}
                horizontal={true}
                with="risk_adjustments" />
              <HX.Notes field="risk_adjustments/uw_rationale"
                title="Please provide detail on the Risk Level associated with the selected scores:" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Individual Risk Score Comments (click to reveal)"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Notes field="risk_adjustments/security/uw_rationale"
              title="Please provide detail on the Risk Level associated with the selected Security Score:" />
            <HX.Notes field="risk_adjustments/industry/uw_rationale"
              title="Please provide detail on the Risk Level associated with the selected Industry Score:" />
            <HX.Notes field="risk_adjustments/policy/uw_rationale"
              title="Please provide detail on the Risk Level associated with the selected Policy Score:" />
            <HX.Notes field="risk_adjustments/ihs_score/uw_rationale"
              title="Please provide detail on the Risk Level associated with the selected IHS Score:" />
          </HX.With>
        </HX.Section>
        <HX.Section title="General Comments">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="down">
              <HX.Notes field="risk_adjustments/uw_general_comments" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="ROE Calcs"
        fullWidth={true}
        viewScale={0.8}
        shownBy="cds/exposure/granular/show_pricing">
        <HX.Section title="ROE Calculations">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection title="BI and Countries"
                with="cds/exposure/granular"
                fields={[
                "bi_multiplier",
                "no_of_countries"
              ]} />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Collection title="Weighted Avg Min ROL"
                with="cds/exposure/granular"
                fields={[
                "wa_nl_min_rol",
                "wa_liab_min_rol"
              ]} />
            </HX.Pane>
            <HX.Table with="cds/exposure/granular"
              data={[
              "roe"
            ]}
              fields={[
              "country",
              "attritional_risk",
              "geog_risk",
              "location_cat_risk",
              "total_sum_insured",
              "bi_sum_insured",
              "pd_sum_insured",
              "civil_unrest",
              "war",
              "terrorism",
              "coverage",
              "coverage_code",
              "subcoverage",
              "subcoverage_code",
              "selected_sum_insured",
              "risk_multiplier",
              "bi_terrorism_c",
              "bi_terrorism_b",
              "bi_civil_unrest_c",
              "bi_civil_unrest_b",
              "bi_war_c",
              "bi_war_b",
              "bi_terrorism_roe",
              "bi_civil_unrest_roe",
              "bi_war_roe",
              "pd_terrorism_c",
              "pd_terrorism_b",
              "pd_civil_unrest_c",
              "pd_civil_unrest_b",
              "pd_war_c",
              "pd_war_b",
              "pd_terrorism_roe",
              "pd_civil_unrest_roe",
              "pd_war_roe",
              "selected_terrorism_roe",
              "selected_civil_unrest_roe",
              "selected_war_roe",
              "cvg_terrorism",
              "cvg_civil_unrest",
              "cvg_war",
              "cvg_loading",
              "subcvg_terrorism",
              "subcvg_civil_unrest",
              "subcvg_war",
              "subcvg_loading",
              "ihs_average_default",
              "bi_cvg_nl_roe",
              "pd_cvg_nl_roe",
              "total_cvg_nl_roe",
              "bi_subcvg_nl_roe",
              "pd_subcvg_nl_roe",
              "total_subcvg_nl_roe",
              "cvg_multiplier",
              "subcvg_multiplier",
              "nl_min_rol",
              "liab_min_rol"
            ]}
              dynamic={true}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Expanded Calcs"
        fullWidth={true}
        viewScale={0.8}
        shownBy="cds/exposure/granular/show_pricing">
        <HX.Section title="Expanded Calculations">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection title="Countries and FX"
                with="cds/exposure/granular"
                fields={[
                "no_of_countries",
                "fx_to_usd"
              ]} />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Collection title="Summary"
                with="cds/exposure/granular"
                fields={[
                "trapped_exposure",
                "limit_ded_difference",
                "expo_limit_ratio"
              ]} />
            </HX.Pane>
            <HX.Table with="cds/exposure/granular"
              data={[
              "curves"
            ]}
              fields={[
              "location_number",
              "country",
              "country_number",
              "no_of_locations",
              "pml",
              "coverage",
              "limit",
              "excess",
              "subcoverage",
              "sublimit",
              "deductible",
              "total_sum_insured",
              "bi_sum_insured",
              "pd_sum_insured",
              "selected_sum_insured",
              "band",
              "kth_smallest",
              "decile",
              "category",
              "no_in_category",
              "si_unscaled",
              "si_scaled",
              "si_scaled_2",
              "liability_risk",
              "attritional_risk",
              "geog_risk",
              "location_cat_risk",
              "bi_cvg_nl_roe",
              "bi_subcvg_nl_roe",
              "pd_cvg_nl_roe",
              "pd_subcvg_nl_roe",
              "cvg_bi_rate_si",
              "cvg_pd_rate_si",
              "cvg_bi_mbbefd",
              "cvg_pd_mbbefd",
              "cvg_bi_base_premium",
              "cvg_pd_base_premium",
              "cvg_limit_usd",
              "cvg_excess_usd",
              "cvg_ilf_upper",
              "cvg_ilf_lower",
              "cvg_liab_base_premium",
              "subcvg_bi_rate_si",
              "subcvg_pd_rate_si",
              "subcvg_bi_mbbefd",
              "subcvg_pd_mbbefd",
              "subcvg_bi_base_premium",
              "subcvg_pd_base_premium",
              "subcvg_sublimit_usd",
              "subcvg_ilf_upper",
              "subcvg_liab_base_premium",
              "trapped_exposure"
            ]}
              maxListVisibleRows={25}
              dynamic={true}
              kb-interactive={true}
              freezeLeft={2} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Construction"
        shownBy="cds/exposure/aggregate/has_construction"
        viewScale={0.9}
        fullWidth={true}>
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.With context={{
            "path": "coverages/construction",
            "type": "struct"
          }}>
            <HX.Section title="Construction">
              <HX.Pane>
                <HX.Pane flow="right"
                  reflow={false}>
                  <HX.Pane>
                    <HX.Collection title="Policy Details"
                      fields={[
                      "/hx_core/inception_date",
                      "/hx_core/expiry_date"
                    ]}
                      horizontal={true}
                      syncColumnWidthsKey="details" />
                    <HX.Collection fields={[
                      "/cds/exposure/aggregate/total_sum_insured",
                      "days_difference"
                    ]}
                      horizontal={true}
                      syncColumnWidthsKey="details" />
                    <HX.Collection with="/cds/exposure/aggregate"
                      fields={[
                      "policy_limit",
                      "policy_sublimit"
                    ]}
                      horizontal={true}
                      syncColumnWidthsKey="details" />
                    <HX.Collection with="/cds/exposure/aggregate"
                      fields={[
                      "policy_excess",
                      "policy_deductible"
                    ]}
                      horizontal={true}
                      syncColumnWidthsKey="details" />
                    <HX.Table title="Default"
                      data={[
                      "thirds"
                    ]}
                      fields={[
                      "third",
                      "build_up",
                      "end_date"
                    ]}
                      kb-interactive={true} />
                  </HX.Pane>
                  <CustomComponent title="Construction Build Up"
                    xAxisLabel="Year"
                    yAxisLabel="Build Up %"
                    series={[
                    {
                      "points": [
                        {
                          "list": "years",
                          "x": "year",
                          "y": "build_up_calculated"
                        }
                      ],
                      "seriesLabel": "Proposed"
                    },
                    {
                      "points": [
                        {
                          "list": "years",
                          "x": "year",
                          "y": "build_up_selected"
                        }
                      ],
                      "seriesLabel": "Selected"
                    }
                  ]} />
                </HX.Pane>
                <HX.Collection fields={[
                  null,
                  null,
                  null,
                  "are_years_horizontal"
                ]}
                  horizontal={true} />
                <HX.Table title="Selected Build Up and Premium Summary"
                  data={[
                  "years",
                  null,
                  "years_total",
                  "years_annual"
                ]}
                  fields={[
                  "end_date",
                  null,
                  "build_up_calculated",
                  "build_up_override",
                  "build_up_selected",
                  "sum_insured",
                  null,
                  "total_cvg_nl_roe",
                  "total_subcvg_nl_roe",
                  null,
                  "cvg_expo_curve",
                  "subcvg_expo_curve",
                  null,
                  "cvg_premium",
                  "subcvg_premium",
                  "total_premium",
                  null,
                  "model_premium_pre_uw_adj",
                  "model_premium",
                  "benchmark_premium",
                  "model_premium_post_agg_adj"
                ]}
                  kb-interactive={true}
                  transpose={false}
                  shownBy="are_years_vertical"
                  freezeLeft={2} />
                <HX.Table title="Selected Build Up and Premium Summary"
                  data={[
                  "years",
                  null,
                  "years_total",
                  "years_annual"
                ]}
                  fields={[
                  "end_date",
                  null,
                  "build_up_calculated",
                  "build_up_override",
                  "build_up_selected",
                  "sum_insured",
                  null,
                  "total_cvg_nl_roe",
                  "total_subcvg_nl_roe",
                  null,
                  "cvg_expo_curve",
                  "subcvg_expo_curve",
                  null,
                  "cvg_premium",
                  "subcvg_premium",
                  "total_premium",
                  null,
                  "model_premium_pre_uw_adj",
                  "model_premium",
                  "benchmark_premium",
                  "model_premium_post_agg_adj"
                ]}
                  kb-interactive={true}
                  transpose={true}
                  shownBy="are_years_horizontal" />
              </HX.Pane>
            </HX.Section>
          </HX.With>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rating Summary"
        shownBy="model_state/show_after_landing_page"
        viewScale={0.9}
        fullWidth={true}>
        <HX.Section title="Overall Summary">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={3}
              fields={[
              "section_reference",
              "status",
              "/cds/currencies/source_currency",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Priced Quotes"
              numCols={3}
              fields={[
              "quoted_premium_100_pct",
              "quoted_premium",
              "coverages/total/policy_period/quoted_rol",
              "coverages/total/policy_period/benchmark_premium",
              "benchmark_premium",
              "coverages/total/policy_period/quoted_roe",
              "coverages/total/policy_period/technical_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "bpi",
              "pflr",
              "uw_adj_impact",
              "tpi",
              "tpi_pre_uw_adj",
              "roc"
            ]} />
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}
            shownBy="cds/standard_fields/is_case_priced">
            <HX.Collection title="Priced Quotes @ Term & Beazley Share"
              numCols={2}
              fields={[
              "quoted_premium_case_priced",
              "bpi_case_priced",
              "technical_premium",
              "benchmark_premium"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "tpi",
              "pflr",
              "roc"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section defaultCollapsed={true}
          title="Policy Period vs. Annual Summary"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Collection fields={[
            "/model_state/show_rs_cvg",
            "/model_state/show_rs_before_uw_adj",
            "/model_state/show_rs_plan",
            null
          ]}
            horizontal={true} />
          <HX.Pane flow="right">
            <HX.Pane shownBy="model_state/show_rs_not_cvg_not_before_uw_adj">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Term Summary - after UW Adj- No Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total/policy_period"
                ]}
                  fields={[
                  "model_premium",
                  "model_rol",
                  "minimum_premium",
                  "minimum_rol",
                  null,
                  "quoted_premium",
                  "quoted_rol",
                  "quoted_roe",
                  null,
                  "technical_premium",
                  "tpi",
                  null,
                  "benchmark_premium",
                  "bpi",
                  "expected_loss_ratio"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
   
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_not_cvg_not_before_uw_adj">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Annual Summary - after UW Adj - No Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total"
                ]}
                  fields={[
                  "model_premium",
                  "model_rol",
                  "minimum_premium",
                  "minimum_rol",
                  null,
                  "quoted_premium",
                  "quoted_rol",
                  "quoted_roe",
                  null,
                  "technical_premium",
                  "tpi",
                  null,
                  "benchmark_premium",
                  "bpi",
                  "expected_loss_ratio"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
 
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_yes_cvg_not_before_uw_adj">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Term Summary - after UW Adj - Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total/policy_period",
                  null,
                  "property/policy_period",
                  "property/policy_period/bi",
                  "property/policy_period/pd",
                  null,
                  "liability/policy_period",
                  "construction/policy_period"
                ]}
                  fields={[
                  "model_premium",
                  "model_rol",
                  "minimum_premium",
                  "minimum_rol",
                  null,
                  "quoted_premium",
                  "quoted_rol",
                  "quoted_roe",
                  null,
                  "technical_premium",
                  "tpi",
                  null,
                  "benchmark_premium",
                  "bpi",
                  "expected_loss_ratio"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
      
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_yes_cvg_not_before_uw_adj">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Annual Summary - after UW Adj - Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total",
                  null,
                  "property",
                  "property/bi",
                  "property/pd",
                  null,
                  "liability",
                  "construction"
                ]}
                  fields={[
                  "model_premium",
                  "model_rol",
                  "minimum_premium",
                  "minimum_rol",
                  null,
                  "quoted_premium",
                  "quoted_rol",
                  "quoted_roe",
                  null,
                  "technical_premium",
                  "tpi",
                  null,
                  "benchmark_premium",
                  "bpi",
                  "expected_loss_ratio"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
    
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane shownBy="model_state/show_rs_not_cvg_yes_before_uw_adj">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Term Summary - before UW Adj - No Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total/policy_period"
                ]}
                  fields={[
                  "model_premium_pre_uw_adj",
                  "model_rol_pre_uw_adj",
                  null,
                  "technical_premium_pre_uw_adj",
                  "tpi_pre_uw_adj",
                  null,
                  "benchmark_premium_pre_uw_adj",
                  "bpi_pre_uw_adj",
                  "expected_loss_ratio_pre_uw_adj"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
    
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_not_cvg_yes_before_uw_adj">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Annual Summary - before UW Adj - No Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total"
                ]}
                  fields={[
                  "model_premium_pre_uw_adj",
                  "model_rol_pre_uw_adj",
                  null,
                  "technical_premium_pre_uw_adj",
                  "tpi_pre_uw_adj",
                  null,
                  "benchmark_premium_pre_uw_adj",
                  "bpi_pre_uw_adj",
                  "expected_loss_ratio_pre_uw_adj"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
  
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_yes_cvg_yes_before_uw_adj">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Term Summary - before UW Adj - Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total/policy_period",
                  null,
                  "property/policy_period",
                  "property/policy_period/bi",
                  "property/policy_period/pd",
                  null,
                  "liability/policy_period",
                  "construction/policy_period"
                ]}
                  fields={[
                  "model_premium_pre_uw_adj",
                  "model_rol_pre_uw_adj",
                  null,
                  "technical_premium_pre_uw_adj",
                  "tpi_pre_uw_adj",
                  null,
                  "benchmark_premium_pre_uw_adj",
                  "bpi_pre_uw_adj",
                  "expected_loss_ratio_pre_uw_adj"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
       
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_yes_cvg_yes_before_uw_adj">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Annual Summary - before UW Adj - Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total",
                  null,
                  "property",
                  "property/bi",
                  "property/pd",
                  null,
                  "liability",
                  "construction"
                ]}
                  fields={[
                  "model_premium_pre_uw_adj",
                  "model_rol_pre_uw_adj",
                  null,
                  "technical_premium_pre_uw_adj",
                  "tpi_pre_uw_adj",
                  null,
                  "benchmark_premium_pre_uw_adj",
                  "bpi_pre_uw_adj",
                  "expected_loss_ratio_pre_uw_adj"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
     
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane shownBy="model_state/show_rs_not_cvg_not_before_uw_adj_not_plan">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Term Summary - after UW Adj- No Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total/policy_period"
                ]}
                  fields={[
                  "quoted_premium",
                  "quoted_rol",
                  "quoted_roe",
                  null,
                  "technical_premium",
                  "tpi",
                  null,
                  "benchmark_premium",
                  "bpi",
                  "expected_loss_ratio"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
   
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_not_cvg_not_before_uw_adj_not_plan">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Annual Summary - after UW Adj - No Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total"
                ]}
                  fields={[
                  "quoted_premium",
                  "quoted_rol",
                  "quoted_roe",
                  null,
                  "technical_premium",
                  "tpi",
                  null,
                  "benchmark_premium",
                  "bpi",
                  "expected_loss_ratio"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
 
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_yes_cvg_not_before_uw_adj_not_plan">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Term Summary - after UW Adj - Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total/policy_period",
                  null,
                  "property/policy_period",
                  "property/policy_period/bi",
                  "property/policy_period/pd",
                  null,
                  "liability/policy_period",
                  "construction/policy_period"
                ]}
                  fields={[
                  "quoted_premium",
                  "quoted_rol",
                  "quoted_roe",
                  null,
                  "technical_premium",
                  "tpi",
                  null,
                  "benchmark_premium",
                  "bpi",
                  "expected_loss_ratio"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
      
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_yes_cvg_not_before_uw_adj_not_plan">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Annual Summary - after UW Adj - Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total",
                  null,
                  "property",
                  "property/bi",
                  "property/pd",
                  null,
                  "liability",
                  "construction"
                ]}
                  fields={[
                  "quoted_premium",
                  "quoted_rol",
                  "quoted_roe",
                  null,
                  "technical_premium",
                  "tpi",
                  null,
                  "benchmark_premium",
                  "bpi",
                  "expected_loss_ratio"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
    
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane shownBy="model_state/show_rs_not_cvg_yes_before_uw_adj_not_plan">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Term Summary - before UW Adj - No Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total/policy_period"
                ]}
                  fields={[
                  "technical_premium_pre_uw_adj",
                  "tpi_pre_uw_adj",
                  null,
                  "benchmark_premium_pre_uw_adj",
                  "bpi_pre_uw_adj",
                  "expected_loss_ratio_pre_uw_adj"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
    
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_not_cvg_yes_before_uw_adj_not_plan">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Annual Summary - before UW Adj - No Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total"
                ]}
                  fields={[
                  "technical_premium_pre_uw_adj",
                  "tpi_pre_uw_adj",
                  null,
                  "benchmark_premium_pre_uw_adj",
                  "bpi_pre_uw_adj",
                  "expected_loss_ratio_pre_uw_adj"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
  
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_yes_cvg_yes_before_uw_adj_not_plan">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Term Summary - before UW Adj - Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total/policy_period",
                  null,
                  "property/policy_period",
                  "property/policy_period/bi",
                  "property/policy_period/pd",
                  null,
                  "liability/policy_period",
                  "construction/policy_period"
                ]}
                  fields={[
                  "technical_premium_pre_uw_adj",
                  "tpi_pre_uw_adj",
                  null,
                  "benchmark_premium_pre_uw_adj",
                  "bpi_pre_uw_adj",
                  "expected_loss_ratio_pre_uw_adj"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
       
            </HX.Pane>
            <HX.Pane shownBy="model_state/show_rs_yes_cvg_yes_before_uw_adj_not_plan">
  
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Table title="Annual Summary - before UW Adj - Coverage Detail"
                  with="coverages"
                  data={[
                  null,
                  "total",
                  null,
                  "property",
                  "property/bi",
                  "property/pd",
                  null,
                  "liability",
                  "construction"
                ]}
                  fields={[
                  "technical_premium_pre_uw_adj",
                  "tpi_pre_uw_adj",
                  null,
                  "benchmark_premium_pre_uw_adj",
                  "bpi_pre_uw_adj",
                  "expected_loss_ratio_pre_uw_adj"
                ]}
                  transpose={true}
                  kb-interactive={true}
                  freezeLeft={0} />
              </HX.With>
     
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Peril Sheet"
        shownBy="model_state/show_after_landing_page"
        fullWidth={true}
        viewScale={0.9}>
        <HX.Section title="Policy Summary">
          <HX.Pane flow="right">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "/cds/standard_fields/insured_name",
                "section_reference"
              ]} />
            </HX.With>
            <HX.Collection with="cds/exposure/aggregate"
              fields={[
              "no_of_locations",
              "total_sum_insured",
              "details/limit_type"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.With context={{
          "path": "cds/exposure/aggregate",
          "type": "struct"
        }}>
          <HX.Section title="Summary of Perils">
            <HX.Pane flow="right">
              <HX.Button task="task_confirm_limits"
                title="Confirm limits" />
              <HX.Notes field="confirm_message" />
            </HX.Pane>
            <HX.Notes field="peril_comments"
              title="Comments" />
            <HX.Pane>
              <HX.Table title="Perils"
                with="perils"
                data={[
                "terrorism",
                "sabotage",
                "rscc",
                "damage",
                "insurrection",
                "coup",
                "war",
                "insurgency",
                "liability",
                "cyber",
                "nrcb",
                "looting"
              ]}
                fields={[
                null,
                {
                  "field": "is_covered_calculated",
                  "maxWidth": 140
                },
                {
                  "field": "is_covered_override",
                  "maxWidth": 140
                },
                {
                  "field": "is_covered_selected",
                  "maxWidth": 140
                },
                null,
                {
                  "field": "limit_calculated",
                  "maxWidth": 140
                },
                {
                  "field": "limit_override",
                  "maxWidth": 140
                },
                {
                  "field": "limit_selected",
                  "maxWidth": 140
                },
                null,
                {
                  "field": "excess_calculated",
                  "maxWidth": 140
                },
                {
                  "field": "excess_override",
                  "maxWidth": 140
                },
                {
                  "field": "excess_selected",
                  "maxWidth": 140
                },
                null,
                {
                  "field": "deductible_calculated",
                  "maxWidth": 140
                },
                {
                  "field": "deductible_override",
                  "maxWidth": 140
                },
                {
                  "field": "deductible_selected",
                  "maxWidth": 140
                }
              ]}
                kb-interactive={true}
                freezeLeft={1} />
              <HX.Table title="CBI Perils"
                with="cbi_perils"
                data={[
                "unnamed",
                "named",
                "interruption",
                "denial",
                "ingress",
                "authority"
              ]}
                fields={[
                null,
                {
                  "field": "is_covered_selected",
                  "maxWidth": 140
                },
                {
                  "field": "limit_selected",
                  "maxWidth": 140
                },
                {
                  "field": "excess_selected",
                  "maxWidth": 140
                },
                {
                  "field": "deductible_selected",
                  "maxWidth": 140
                },
                null,
                {
                  "field": "territory_covered",
                  "maxWidth": 140,
                  "shownBy": "/cds/exposure/aggregate/cbi_peril_territory_covered_show"
                },
                {
                  "field": "distance_selected",
                  "maxWidth": 140
                },
                {
                  "field": "metric_selected",
                  "maxWidth": 140
                }
              ]}
                kb-interactive={true}
                freezeLeft={1}
                syncColumnWidthsKey="perils" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rate Change"
        viewScale={0.9}
        shownBy="cds/standard_fields/is_renewal">
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id"
            ]} />
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Renewal"
          shownBy="cds/rate_change/show_layer_1">
          <HX.Pane flow="right">
            <HX.Button task="rarc_task"
              title="Calculate Rate Change" />
            <HX.Pane />
          </HX.Pane>
          <HX.Notes with="cds/rate_change"
            field="rarc_run_again_message"
            shownBy="rarc_message_show" />
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "written_line"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 150
                },
                {
                  "field": "expiring",
                  "width": 150
                },
                {
                  "field": "expiring_override",
                  "width": 200
                }
              ]}
                with="rate_change" />
            </HX.Pane>
            <HX.Pane shownBy="/cds/rate_change/rarc_calcs_show">
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
                  "field": "uw_selected",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
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
        fullWidth={false}>
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
        <HX.Section title="Actuarial Commentary"
          defaultCollapsed={true}>
          <HX.Collection fields={[
            "cds/rationale/actuarial_review"
          ]} />
          <HX.Notes field="cds/rationale/actuarial_notes" />
        </HX.Section>
        <HX.Section title="Policy Document">
          <HX.Button task="task_policy_to_excel"
            title="Generate Policy Document"
            shownBy="policy_doc/show_generate_button" />
          <HX.Notes field="policy_doc/premium_check"
            shownBy="policy_doc/show_premium_check" />
          <HX.File with="policy_doc"
            field="output_file"
            title="Click on the icon below to download the policy document"
            shownBy="show_download" />
        </HX.Section>
        <HX.Section title="Useful Information">
          <HX.Pane flow="right">
            <HX.Notes field="cds/rationale/help_file" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Actuarial Info (typically hidden)"
        fullWidth={true}
        shownBy="cds/show_hide/page/show_actuarial">
        <HX.Section title="Model State"
          defaultCollapsed={true}>
          <HX.Collection fields={[
            "pressed_start_renewal_task",
            "show_landing_page",
            "show_after_landing_page",
            "show_rate_change"
          ]}
            with="model_state"
            horizontal={true} />
          <HX.Collection fields={[
            "has_import_failed",
            "landing_page_info",
            null,
            null
          ]}
            with="model_state"
            horizontal={true} />
          <HX.Collection fields={[
            "is_migrated",
            "not_migrated",
            "is_new",
            null
          ]}
            with="model_state"
            horizontal={true} />
          <HX.Collection fields={[
            "show_rs_cvg",
            "show_rs_before_uw_adj",
            null,
            null
          ]}
            with="model_state"
            horizontal={true} />
          <HX.Collection fields={[
            "show_rs_not_cvg_not_before_uw_adj",
            "show_rs_yes_cvg_not_before_uw_adj",
            "show_rs_not_cvg_yes_before_uw_adj",
            "show_rs_yes_cvg_yes_before_uw_adj"
          ]}
            with="model_state"
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Countries Dataframe"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Complete List"
              maxListVisibleRows={15}
              data={[
              "cds/exposure/granular/countries"
            ]}
              fields={[
              "country",
              "proxy_rating_country",
              "rated_country",
              "country_code_original",
              "country_code",
              "no_of_locations",
              "pml",
              "coverage",
              "limit",
              "excess",
              "subcoverage",
              "sublimit",
              "deductible",
              "total_sum_insured",
              "bi_sum_insured",
              "pd_sum_insured",
              "liability_risk",
              "attritional_risk",
              "geog_risk",
              "location_cat_risk",
              "political",
              "terrorism_raw",
              "labour_strikes",
              "protests_riots",
              "interstate_war",
              "civil_war",
              "civil_unrest",
              "war",
              "terrorism",
              "selected_sum_insured",
              "warning",
              "civil_unrest_roe_calculated",
              "civil_unrest_roe_selected",
              "war_roe_calculated",
              "war_roe_selected",
              "terrorism_roe_calculated",
              "terrorism_roe_selected",
              "civil_unrest_uw_adj",
              "war_uw_adj",
              "terrorism_uw_adj",
              "override_civil_unrest",
              "override_war",
              "override_terrorism",
              "selected_civil_unrest",
              "selected_war",
              "selected_terrorism",
              "has_civil_unrest",
              "has_war",
              "has_terrorism",
              "leading_peril",
              "selected_sum_insured_contribution",
              "country_cvg_subcvg",
              "country_cvg_subcvg_live"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="ROE Dataframe"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Complete List"
              maxListVisibleRows={15}
              data={[
              "cds/exposure/granular/roe"
            ]}
              fields={[
              "country",
              "no_of_locations",
              "attritional_risk",
              "geog_risk",
              "location_cat_risk",
              "total_sum_insured",
              "bi_sum_insured",
              "pd_sum_insured",
              "civil_unrest",
              "war",
              "terrorism",
              "coverage",
              "coverage_code",
              "subcoverage",
              "subcoverage_code",
              "selected_sum_insured",
              "risk_multiplier",
              "bi_terrorism_c",
              "bi_terrorism_b",
              "bi_civil_unrest_c",
              "bi_civil_unrest_b",
              "bi_war_c",
              "bi_war_b",
              "bi_terrorism_roe",
              "bi_civil_unrest_roe",
              "bi_war_roe",
              "pd_terrorism_c",
              "pd_terrorism_b",
              "pd_civil_unrest_c",
              "pd_civil_unrest_b",
              "pd_war_c",
              "pd_war_b",
              "pd_terrorism_roe",
              "pd_civil_unrest_roe",
              "pd_war_roe",
              "selected_terrorism_roe",
              "selected_civil_unrest_roe",
              "selected_war_roe",
              "cvg_terrorism",
              "cvg_civil_unrest",
              "cvg_war",
              "cvg_loading",
              "subcvg_terrorism",
              "subcvg_civil_unrest",
              "subcvg_war",
              "subcvg_loading",
              "ihs_average_default",
              "ihs_average_selected",
              "bi_cvg_nl_roe",
              "pd_cvg_nl_roe",
              "total_cvg_nl_roe",
              "bi_subcvg_nl_roe",
              "pd_subcvg_nl_roe",
              "total_subcvg_nl_roe",
              "cvg_multiplier",
              "subcvg_multiplier",
              "nl_min_rol",
              "liab_min_rol"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curves Dataframe"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Complete List"
              maxListVisibleRows={15}
              data={[
              "cds/exposure/granular/curves"
            ]}
              fields={[
              "index",
              "country_number",
              "no_of_locations",
              "location_number",
              "country",
              "pml",
              "coverage",
              "limit",
              "excess",
              "subcoverage",
              "sublimit",
              "deductible",
              "total_sum_insured",
              "bi_sum_insured",
              "pd_sum_insured",
              "selected_sum_insured",
              "band",
              "kth_smallest",
              "decile",
              "category",
              "no_in_category",
              "si_unscaled",
              "si_scaled",
              "si_scaled_2",
              "liability_risk",
              "attritional_risk",
              "geog_risk",
              "location_cat_risk",
              "bi_cvg_nl_roe",
              "bi_subcvg_nl_roe",
              "pd_cvg_nl_roe",
              "pd_subcvg_nl_roe",
              "cvg_bi_rate_si",
              "cvg_pd_rate_si",
              "cvg_bi_mbbefd",
              "cvg_pd_mbbefd",
              "cvg_bi_base_premium",
              "cvg_pd_base_premium",
              "cvg_limit_usd",
              "cvg_excess_usd",
              "cvg_ilf_upper",
              "cvg_ilf_lower",
              "cvg_liab_base_premium",
              "subcvg_bi_rate_si",
              "subcvg_pd_rate_si",
              "subcvg_bi_mbbefd",
              "subcvg_pd_mbbefd",
              "subcvg_bi_base_premium",
              "subcvg_pd_base_premium",
              "subcvg_sublimit_usd",
              "subcvg_ilf_upper",
              "subcvg_liab_base_premium",
              "trapped_exposure"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Construction Dataframe"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Table title="Complete List"
                data={[
                "years"
              ]}
                fields={[
                "year",
                "end_date",
                "build_up_calculated",
                "build_up_override",
                "build_up_selected",
                "sum_insured",
                "total_cvg_nl_roe",
                "total_subcvg_nl_roe",
                "cvg_expo_curve",
                "subcvg_expo_curve",
                "cvg_premium",
                "subcvg_premium",
                "total_premium",
                "model_premium_pre_uw_adj",
                "model_premium",
                "benchmark_premium",
                "model_premium_post_agg_adj"
              ]}
                kb-interactive={true}
                dynamic={true}
                with="coverages/construction" />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Mapping to standard fields"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Table title="hx - standard fields"
                data={[
                "hx_core"
              ]}
                fields={[
                "inception_date",
                "expiry_date",
                "model_premium",
                "charged_premium",
                "premium_currency",
                "ulr",
                "class_code"
              ]}
                transpose={true} />
              <HX.Table title="cds - currencies"
                data={[
                "cds/currencies"
              ]}
                fields={[
                "target_currency",
                "source_currency",
                "multi_currency_support"
              ]}
                transpose={true} />
              <HX.Table title="cds - experience rating"
                data={[
                "cds/experience_rating"
              ]}
                fields={[
                "claims_available",
                "claims_fgu",
                "claims_net_of_deductible"
              ]}
                transpose={true} />
              <HX.Table title="cds"
                data={[
                "cds"
              ]}
                fields={[
                "database_id"
              ]}
                transpose={true} />
            </HX.Pane>
            <HX.Table title="cds - standard fields"
              data={[
              "cds/standard_fields"
            ]}
              fields={[
              "insured_name",
              "broker",
              "expiry_date",
              "inception_date",
              "insured_country",
              "insured_postal_code",
              "insured_state_or_province",
              "is_admitted_or_surplus",
              "is_free_trade_zone",
              "is_renewal",
              "underwriter",
              "policy_reference",
              "facility_reference",
              "benchmark_class",
              "uw_rationale",
              "trifocus",
              "rating_methodology",
              "is_case_priced",
              "is_rater_priced"
            ]}
              transpose={true} />
            <HX.Table title="cds - standard layer fields"
              data={[
              "cds/layers"
            ]}
              fields={[
              "limit",
              "excess",
              "deductible",
              "aggregate_limit",
              "aggregate_excess",
              "aggregate_deductible",
              "currency",
              "section_reference",
              "brokerage",
              "written_line",
              "premium",
              "status",
              "is_primary_excess",
              "benchmark_premium",
              "bpi",
              "bpi_pre_uw_adj",
              "model_premium",
              "unity_premium",
              "quoted_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj",
              "technical_premium_net",
              "tpi",
              "tpi_pre_uw_adj",
              "pflr_att",
              "pflr_cat",
              "pflr",
              "roc",
              "uw_adj_impact",
              "trifocus",
              "expected_loss_cost",
              "expected_loss_cost_pre_uw_adj",
              "bpi_case_priced",
              "pflr_pre_uw_adj",
              "premium_label"
            ]}
              transpose={true} />
          </HX.Pane>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Table title="cds - coverage fields"
              data={[
              "coverages/property",
              "coverages/property/bi",
              "coverages/property/pd",
              "coverages/property/policy_period",
              "coverages/property/policy_period/bi",
              "coverages/property/policy_period/pd",
              "coverages/liability",
              "coverages/liability/policy_period",
              "coverages/construction",
              "coverages/construction/policy_period",
              "coverages/total",
              "coverages/total/policy_period"
            ]}
              fields={[
              "limit",
              "excess",
              "deductible",
              "aggregate_limit",
              "aggregate_excess",
              "aggregate_deductible",
              "currency",
              "section_reference",
              "brokerage",
              "written_line",
              "premium",
              "status",
              "is_primary_excess",
              "benchmark_premium",
              "bpi",
              "bpi_pre_uw_adj",
              "model_premium",
              "unity_premium",
              "quoted_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj",
              "technical_premium_net",
              "tpi",
              "tpi_pre_uw_adj",
              "pflr_att",
              "pflr_cat",
              "pflr",
              "roc",
              "uw_adj_impact",
              "trifocus",
              "expected_loss_cost",
              "expected_loss_cost_pre_uw_adj",
              "bpi_case_priced",
              "pflr_pre_uw_adj",
              "premium_label"
            ]}
              transpose={true} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Totals by Coverage Dataframe"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Table title="Repeating Column Names - first Annual then Term"
                data={[
                "coverages/property",
                "coverages/property/bi",
                "coverages/property/pd",
                "coverages/property/policy_period",
                "coverages/property/policy_period/bi",
                "coverages/property/policy_period/pd",
                "coverages/liability",
                "coverages/liability/policy_period",
                "coverages/construction",
                "coverages/construction/policy_period",
                "coverages/total",
                "coverages/total/policy_period"
              ]}
                fields={[
                "limit",
                "excess",
                "deductible",
                "aggregate_limit",
                "aggregate_excess",
                "aggregate_deductible",
                "currency",
                "section_reference",
                "brokerage",
                "written_line",
                "premium",
                "status",
                "benchmark_premium",
                "bpi",
                "bpi_pre_uw_adj",
                "model_premium",
                "unity_premium",
                "quoted_premium",
                "technical_premium",
                "technical_premium_pre_uw_adj",
                "technical_premium_net",
                "tpi",
                "tpi_pre_uw_adj",
                "pflr_att",
                "pflr_cat",
                "pflr",
                "roc",
                "uw_adj_impact",
                "model_premium_pre_uw_adj",
                "model_rol_pre_uw_adj",
                "model_rol",
                "minimum_premium",
                "minimum_rol",
                "quoted_rol",
                "quoted_roe",
                "expected_loss_ratio",
                "benchmark_premium_pre_uw_adj",
                "expected_loss_ratio_pre_uw_adj",
                "quoted_premium_annualised",
                "benchmark_premium_annualised"
              ]}
                kb-interactive={true}
                dynamic={true}
                transpose={true} />
            </HX.With>
          </HX.Pane>
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
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "quoted_premium_case_priced",
                "labelBy": "premium_label",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
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
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
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