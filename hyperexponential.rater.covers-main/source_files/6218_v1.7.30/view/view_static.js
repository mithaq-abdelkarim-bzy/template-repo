
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
              title="Start Policy" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="NB:"
          collapsible={false}>
          <HX.Notes field="model_state/landing_page_info" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "database_id",
              "application_date"
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
              "cds/standard_fields/insured_name"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/facility_reference",
              "cds/currencies/source_currency",
              "cds/standard_fields/is_renewal"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Business Line">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "standard_fields/trifocus",
              {
                "field": "risk_info/proxy_trifocus",
                "shownBy": "show_hide/node/ri_proxy_trifocus"
              },
              "risk_info/division"
            ]}
              with="cds"
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
        <HX.Section title="Load Facility Data"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/facility_reference",
              "cds/risk_info/facility_reference2",
              "cds/risk_info/facility_reference3",
              "cds/risk_info/facility_reference4",
              "cds/risk_info/facility_reference5",
              "cds/risk_info/facility_reference6",
              "cds/risk_info/facility_reference7"
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/bi_data/include_all_facility_references"
            ]} />
            <HX.Button task="bi_facility_fetch_task"
              title="Search Database" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes field="cds/bi_data/fetch_facility_detail_task_status" />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title="Please select references you wish to include:"
              maxListVisibleRows={8}
              freezeLeft={1}
              data={[
              "cds/bi_data/facility_detail"
            ]}
              fields={[
              "include",
              "section_reference",
              "insured_party",
              "yoa",
              "underwriter_name",
              "written_or_estimated_premium"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="bi_facility_include_all_task"
              title="Select  All" />
            <HX.Button task="bi_facility_exclude_all_task"
              title=" Deselect All" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="bi_clm_and_mvmt_exc_triangles_fetch_task"
              title="Load premium and claims history" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes field="cds/bi_data/fetch_clm_and_mvmt_detail_task_status" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Binder Details">
          <HX.Pane flow="right">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "quoted_premium_100pct",
                "written_line"
              ]}
                title="Policy Details" />
              <HX.Collection fields={[
                "signed_line"
              ]}
                shownBy="/cds/show_hide/node/signed_line" />
              <HX.Collection fields={[
                "expiry_signed_line",
                "follow_lead",
                "country",
                "status"
              ]} />
            </HX.With>
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "commission",
                "brokerage",
                "ipt",
                "total_deductions"
              ]}
                title="Commissions" />
            </HX.With>
            <HX.With context={{
              "index": 0,
              "path": "cds/profit_commission/scenarios",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "basis"
              ]}
                title="Profit Commission (PC)" />
              <HX.Collection fields={[
                "expenses"
              ]} />
              <HX.Collection fields={[
                "deficit"
              ]} />
              <HX.Collection fields={[
                "share"
              ]}
                shownBy="/cds/show_hide/node/pc_standard" />
              <HX.Collection fields={[
                "share"
              ]}
                shownBy="/cds/show_hide/node/pc_sliding_scale" />
              <HX.Collection fields={[
                "additionalfeaturesindicator"
              ]} />
            </HX.With>
          </HX.Pane>
          <HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/profit_commission/scenarios",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "threshold_lr_cutoff1",
                "threshold_bonus_share1"
              ]}
                horizontal={true}
                title="Addtional Features"
                shownBy="/cds/show_hide/node/pc_threshold" />
              <HX.Collection fields={[
                "threshold_lr_cutoff2",
                "threshold_bonus_share2"
              ]}
                horizontal={true}
                shownBy="/cds/show_hide/node/pc_threshold" />
              <HX.Collection fields={[
                "threshold_lr_cutoff3",
                "threshold_bonus_share3"
              ]}
                horizontal={true}
                shownBy="/cds/show_hide/node/pc_threshold" />
              <HX.Pane flow="right">
                <HX.Pane ratio={2}>
                  <HX.Collection fields={[
                    null,
                    "threshold_bonus_share4"
                  ]}
                    horizontal={true}
                    shownBy="/cds/show_hide/node/pc_threshold" />
                </HX.Pane>
              </HX.Pane>
            </HX.With>
          </HX.Pane>
          <HX.Pane>
            <HX.With context={{
              "index": 0,
              "path": "cds/profit_commission/scenarios",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "slidingscale_bonus_lr",
                "slidingscale_bonus_scale",
                "slidingscale_bonus_maxtotalpc",
                "slidingscale_clawback_lr",
                "slidingscale_clawback_scale",
                "slidingscale_clawback_mintotalpc"
              ]}
                title="Addtional Features"
                shownBy="/cds/show_hide/node/pc_sliding_scale" />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverages"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table fields={[
              "coverage",
              null,
              "fire",
              "water_damage",
              "tn",
              "ha",
              "wf",
              "wts",
              "fl",
              "riot_or_civil_commotion"
            ]}
              data={[
              {
                "datum": "cds/risk_info",
                "width": 200
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
                "HO6_coverage",
                "extra_expense_coverage",
                "standard_non_standard"
              ]}
                title="Additional Coverage Details" />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Settings">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "sov_available",
              "new_to_market",
              "rms_modelling_available",
              "pc_modelling_required",
              "case_priced"
            ]}
              with="cds/risk_info"
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/show_hide/page/show_sov">
        <HX.Section title="Exposure Management Database Import">
          <HX.Section title="Search Filters">
            <HX.Pane>
              <HX.Collection fields={[
                "cds/exposure_management_api/inputs/binder_name",
                "cds/exposure_management_api/inputs/binder_reference"
              ]}
                horizontal={true} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "cds/exposure_management_api/limit_results"
              ]} />
              <HX.Button task="search_exposure_management_data_task"
                title="Search Exposure Management Database" />
              <HX.Notes field="cds/exposure_management_api/search_fetch_status" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Search Results">
            <HX.Table data={[
              "cds/exposure_management_api/search_results"
            ]}
              fields={[
              "binder_name",
              "binder_reference",
              "binder_date",
              "num_locs",
              "selected"
            ]} />
            <HX.Pane flow="right">
              <HX.Button task="pull_in_exposure_management_data_task"
                title="Pull in Selected" />
              <HX.Notes field="cds/exposure_management_api/location_fetch_status" />
            </HX.Pane>
            <HX.Pane>
              <HX.Button title="Run Rater"
                task="run_bordereau_rater_task" />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Schedule"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/exposure/granular/sov_total/num_locs"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table data={[
            "sov_total",
            null,
            "schedule_table"
          ]}
            fields={[
            "last_updated",
            "loc_id",
            "acc_name",
            "acc_number",
            "inception_date",
            "expiry_date",
            "new_renewal",
            "acc_beazley_received_gg_prem",
            "ceded_share",
            "loc_1_in_250_oep",
            "loc_1_in_10_aep",
            "address_dropdown/country",
            "address_dropdown/state",
            "address_dropdown/county",
            "address_dropdown/city",
            "street_address",
            "zip",
            "latitude",
            "longitude",
            "loc_tiv_buildings",
            "loc_tiv_contents",
            "loc_tiv_bi",
            "loc_tiv_total",
            "industry_occupancy_dropdown/industry",
            "industry_occupancy_dropdown/occupancy",
            "occupancy_description",
            "num_stories",
            "year_built",
            "floor_area",
            "iso_constr",
            "ppc_code",
            "sprinkler",
            "distance_to_coast",
            "beazley_gate",
            "loc_aop_covered.fire_exposure_details",
            "loc_aop_limit.fire_exposure_details",
            "loc_aop_excess.fire_exposure_details",
            "loc_aop_ded.fire_exposure_details",
            "loc_ws_beazley_share_gg_aal",
            "loc_ws_covered.exposure_details",
            "loc_ws_limit.exposure_details",
            "loc_ws_excess.exposure_details",
            "loc_ws_ded.exposure_details",
            "loc_eq_beazley_share_gg_aal",
            "loc_eq_covered.exposure_details",
            "loc_eq_limit.exposure_details",
            "loc_eq_excess.exposure_details",
            "loc_eq_ded.exposure_details",
            "loc_scs_covered.exposure_details",
            "loc_scs_limit.exposure_details",
            "loc_scs_excess.exposure_details",
            "loc_scs_ded.exposure_details",
            "loc_aop_covered.fl_exposure_details",
            "loc_aop_limit.fl_exposure_details",
            "loc_aop_excess.fl_exposure_details",
            "loc_aop_ded.fl_exposure_details",
            "loc_aop_covered.wf_exposure_details",
            "loc_aop_limit.wf_exposure_details",
            "loc_aop_excess.wf_exposure_details",
            "loc_aop_ded.wf_exposure_details"
          ]}
            with="cds/exposure/granular"
            dynamic={true}
            freezeLeft={0}
            kb-interactive={true}
            maxListVisibleRows={10} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Report Summary"
        fullWidth={true}
        viewScale={0.9}
        shownBy="cds/show_hide/page/show_sov">
        <HX.With context={{
          "path": "cds/exposure/aggregate",
          "type": "struct"
        }}>
          <HX.Section title="TIV Summary">
            <HX.Pane flow="right">
              <HX.Pane ratio={2}>
                <HX.Table fields={[
                  "coverage",
                  "value",
                  "percentage"
                ]}
                  data={[
                  "tiv_summary",
                  null,
                  "tiv_summary_total"
                ]}
                  filter="show_row"
                  kb-interactive={true} />
              </HX.Pane>
              <HX.Pane>
                <HX.Collection fields={[
                  "show_coverage_chart"
                ]} />
                <CustomComponent title="Coverage Breakdown"
                  textInfo="value"
                  data={[
                  {
                    "labelBy": "coverage",
                    "list": "tiv_summary",
                    "value": "value"
                  }
                ]}
                  ignoreLastRow={true}
                  shownBy="show_coverage_chart" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Construction Summary">
            <HX.Pane flow="right">
              <HX.Pane ratio={2}>
                <HX.Table fields={[
                  "iso_constr",
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  data={[
                  "construction_summary",
                  null,
                  "construction_summary_total"
                ]}
                  kb-interactive={true}
                  filter="show_row"
                  freezeLeft={1}
                  syncColumnWidthsKey="table_sync" />
              </HX.Pane>
              <HX.Pane>
                <HX.Collection fields={[
                  "show_construction_chart"
                ]} />
                <CustomComponent title="Construction Summary"
                  data={[
                  {
                    "labelBy": "iso_constr",
                    "list": "construction_summary"
                  }
                ]}
                  fields={[
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  labels={[
                  "TIV",
                  "Share Limit",
                  "Share Limit %",
                  "GN Premium",
                  "WS AAL",
                  "EQ AAL",
                  "AOP EL",
                  "GN Rate",
                  "WS AAL Rate",
                  "EQ AAL Rate",
                  "AOP EL Rate",
                  "Premium as a % of AAL"
                ]}
                  percentFormat={[
                  false,
                  false,
                  true,
                  false,
                  false,
                  false,
                  false,
                  true,
                  true,
                  true,
                  true,
                  true
                ]}
                  colors={[
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366"
                ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Construction"
                  yAxisLabel="Value"
                  ignoreLastRow={true}
                  shownBy="show_construction_chart" />
                <CustomComponent title="Construction Classification"
                  data={[
                  {
                    "labelBy": "iso_constr",
                    "list": "construction_summary"
                  }
                ]}
                  traces={[
                  {
                    "color": "#FCD8EF",
                    "field": "ws_aal",
                    "label": "WS AAL"
                  },
                  {
                    "color": "#993366",
                    "field": "aop_el",
                    "label": "AOP EL"
                  }
                ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Construction"
                  yAxisLabel="Value"
                  ignoreLastRow={true}
                  shownBy="show_construction_chart" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Year Built Summary">
            <HX.Pane flow="right">
              <HX.Pane ratio={2}>
                <HX.Table fields={[
                  "year_built",
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  data={[
                  "year_built_summary",
                  null,
                  "year_built_summary_total"
                ]}
                  kb-interactive={true}
                  filter="show_row"
                  freezeLeft={1}
                  syncColumnWidthsKey="table_sync" />
              </HX.Pane>
              <HX.Pane>
                <HX.Collection fields={[
                  "show_year_built_chart"
                ]} />
                <CustomComponent title="Year Built Summary"
                  data={[
                  {
                    "labelBy": "year_built",
                    "list": "year_built_summary"
                  }
                ]}
                  fields={[
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  labels={[
                  "TIV",
                  "Share Limit",
                  "Share Limit %",
                  "GN Premium",
                  "WS AAL",
                  "EQ AAL",
                  "AOP EL",
                  "GN Rate",
                  "WS AAL Rate",
                  "EQ AAL Rate",
                  "AOP EL Rate",
                  "Premium as a % of AAL"
                ]}
                  percentFormat={[
                  false,
                  false,
                  true,
                  false,
                  false,
                  false,
                  false,
                  true,
                  true,
                  true,
                  true,
                  true
                ]}
                  colors={[
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366"
                ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Year Built"
                  yAxisLabel="Value"
                  ignoreLastRow={true}
                  shownBy="show_year_built_chart" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Occupancy Summary">
            <HX.Pane flow="right">
              <HX.Pane ratio={2}>
                <HX.Table fields={[
                  "occupancy",
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  data={[
                  "occupancy_summary",
                  null,
                  "occupancy_summary_total"
                ]}
                  kb-interactive={true}
                  filter="show_row"
                  freezeLeft={1}
                  syncColumnWidthsKey="table_sync" />
              </HX.Pane>
              <HX.Pane>
                <HX.Collection fields={[
                  "show_occupancy_chart"
                ]} />
                <CustomComponent title="Occupancy Summary"
                  data={[
                  {
                    "labelBy": "occupancy",
                    "list": "occupancy_summary"
                  }
                ]}
                  fields={[
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  labels={[
                  "TIV",
                  "Share Limit",
                  "Share Limit %",
                  "GN Premium",
                  "WS AAL",
                  "EQ AAL",
                  "AOP EL",
                  "GN Rate",
                  "WS AAL Rate",
                  "EQ AAL Rate",
                  "AOP EL Rate",
                  "Premium as a % of AAL"
                ]}
                  percentFormat={[
                  false,
                  false,
                  true,
                  false,
                  false,
                  false,
                  false,
                  true,
                  true,
                  true,
                  true,
                  true
                ]}
                  colors={[
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366"
                ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Occupancy"
                  yAxisLabel="Value"
                  ignoreLastRow={true}
                  shownBy="show_occupancy_chart" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Number of Floors Summary">
            <HX.Pane flow="right">
              <HX.Pane ratio={2}>
                <HX.Table fields={[
                  "num_floors",
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  data={[
                  "num_floors_summary",
                  null,
                  "num_floors_summary_total"
                ]}
                  kb-interactive={true}
                  filter="show_row"
                  syncColumnWidthsKey="table_sync" />
              </HX.Pane>
              <HX.Pane>
                <HX.Collection fields={[
                  "show_num_floors_chart"
                ]} />
                <CustomComponent title="Number of Floors Summary"
                  data={[
                  {
                    "labelBy": "num_floors",
                    "list": "num_floors_summary"
                  }
                ]}
                  fields={[
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  labels={[
                  "TIV",
                  "Share Limit",
                  "Share Limit %",
                  "GN Premium",
                  "WS AAL",
                  "EQ AAL",
                  "AOP EL",
                  "GN Rate",
                  "WS AAL Rate",
                  "EQ AAL Rate",
                  "AOP EL Rate",
                  "Premium as a % of AAL"
                ]}
                  percentFormat={[
                  false,
                  false,
                  true,
                  false,
                  false,
                  false,
                  false,
                  true,
                  true,
                  true,
                  true,
                  true
                ]}
                  colors={[
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366"
                ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="Number of Floors"
                  yAxisLabel="Value"
                  ignoreLastRow={true}
                  shownBy="show_num_floors_chart" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="State Summary">
            <HX.Pane flow="right">
              <HX.Pane ratio={2}>
                <HX.Table fields={[
                  "state",
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  data={[
                  "state_summary",
                  null,
                  "state_summary_total"
                ]}
                  kb-interactive={true}
                  filter="show_row"
                  freezeLeft={1}
                  syncColumnWidthsKey="table_sync" />
              </HX.Pane>
              <HX.Pane>
                <HX.Collection fields={[
                  "show_state_chart"
                ]} />
                <CustomComponent title="State Summary"
                  data={[
                  {
                    "labelBy": "state",
                    "list": "state_summary"
                  }
                ]}
                  fields={[
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  labels={[
                  "TIV",
                  "Share Limit",
                  "Share Limit %",
                  "GN Premium",
                  "WS AAL",
                  "EQ AAL",
                  "AOP EL",
                  "GN Rate",
                  "WS AAL Rate",
                  "EQ AAL Rate",
                  "AOP EL Rate",
                  "Premium as a % of AAL"
                ]}
                  percentFormat={[
                  false,
                  false,
                  true,
                  false,
                  false,
                  false,
                  false,
                  true,
                  true,
                  true,
                  true,
                  true
                ]}
                  colors={[
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#FCD8EF",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366",
                  "#993366"
                ]}
                  xAxisTickAngle={-45}
                  gapBetweenBarsSize={0.05}
                  xAxisLabel="State"
                  yAxisLabel="Value"
                  ignoreLastRow={true}
                  shownBy="show_state_chart" />
                <CustomComponent title="USA States"
                  list="state_summary"
                  text="label"
                  locations="state"
                  locationmode="USA-states"
                  zs={[
                  "tiv",
                  "share_lim",
                  "perc_share_limit",
                  "gn_prem",
                  "ws_aal",
                  "eq_aal",
                  "aop_el",
                  "rate_received",
                  "ws_aal_rate",
                  "eq_aal_rate",
                  "aop_el_rate",
                  "prem_as_perc_of_aal"
                ]}
                  options={[
                  "TIV",
                  "Share Limit",
                  "Share Limit %",
                  "GN Premium",
                  "WS AAL",
                  "EQ AAL",
                  "AOP EL",
                  "GN Rate",
                  "WS AAL Rate",
                  "EQ AAL Rate",
                  "AOP EL Rate",
                  "Premium as a % of AAL"
                ]}
                  percentFormat={[
                  false,
                  false,
                  true,
                  false,
                  false,
                  false,
                  false,
                  true,
                  true,
                  true,
                  true,
                  true
                ]}
                  shownBy="show_state_chart" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Region Summary"
        fullWidth={true}
        shownBy="cds/show_hide/page/show_sov">
        <HX.With context={{
          "path": "cds/exposure/aggregate",
          "type": "struct"
        }}>
          <HX.Section title="Construction Summary">
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection fields={[
                  "show_chart"
                ]} />
              </HX.Pane>
              <HX.Pane ratio={5} />
            </HX.Pane>
            <CustomComponent boolNode="show_counties"
              falseLabel="States"
              trueLabel="States and Counties"
              shownBy="show_chart" />
            <HX.Pane flow="right"
              shownBy="show_chart">
              <HX.Pane>
                <CustomComponent title="USA States"
                  list="region_summary_state"
                  text="label"
                  locations="state"
                  locationmode="USA-states"
                  zs={[
                  "tiv",
                  "beazley_share_gn_prem",
                  "one_in_250_oep",
                  "one_in_10_aep",
                  "share_lim",
                  "perc_share_limit",
                  "beazley_share_lim"
                ]}
                  options={[
                  "TIV",
                  "Beazley Share GN Prem",
                  "1 in 250 OEP",
                  "1 in 10 AEP",
                  "Share Limit",
                  "Share Limit %",
                  "AFB Share Limit"
                ]}
                  percentFormat={[
                  false,
                  false,
                  false,
                  false,
                  false,
                  true,
                  false
                ]} />
              </HX.Pane>
              <HX.Pane shownBy="show_counties">
                <CustomComponent title="USA Counties"
                  list="region_summary"
                  text="county"
                  locations="fips"
                  locationmode="USA-counties"
                  zs={[
                  "tiv",
                  "beazley_share_gn_prem",
                  "one_in_250_oep",
                  "one_in_10_aep",
                  "share_lim",
                  "perc_share_limit",
                  "beazley_share_lim"
                ]}
                  options={[
                  "TIV",
                  "Beazley Share GN Prem",
                  "1 in 250 OEP",
                  "1 in 10 AEP",
                  "Share Limit",
                  "Share Limit %",
                  "AFB Share Limit"
                ]}
                  percentFormat={[
                  false,
                  false,
                  false,
                  false,
                  true,
                  false
                ]}
                  ignoreLastRow={true} />
              </HX.Pane>
            </HX.Pane>
            <HX.Table fields={[
              "state",
              "county",
              "tiv",
              "beazley_share_gn_prem",
              "one_in_250_oep",
              "one_in_10_aep",
              "share_lim",
              "perc_share_limit",
              "beazley_share_lim"
            ]}
              data={[
              "region_summary",
              null,
              "region_summary_total"
            ]}
              filter="show_row"
              dynamic={true}
              kb-interactive={true}
              freezeLeft={2}
              maxListVisibleRows={20} />
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        viewScale={0.67}
        shownBy="/model_state/show_after_landing_page">
        <HX.Section title="Case Pricing Inputs"
          shownBy="/cds/rating_summary/kpi/case_priced/show_case_pricing_input_section">
          <HX.Pane flow="down"
            stretch={true}>
            <HX.Table title="Case Priced Inputs"
              data={[
              null,
              {
                "datum": "case_priced",
                "maxWidth": 140
              }
            ]}
              fields={[
              "gg_att_ulr",
              "gg_lrg_ulr",
              "gg_cat_ulr",
              null,
              "bpi",
              "tpi"
            ]}
              with="cds/rating_summary/kpi"
              transpose={true}
              syncColumnWidthsKey="lr_summary" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Inputs"
          shownBy="/cds/show_hide/node/not_new_to_market">
          <HX.Pane flow="right">
            <HX.Table title="Data"
              data={[
              {
                "datum": "detail_by_year",
                "elementLabelBy": "display_yoa"
              }
            ]}
              fields={[
              {
                "field": "policy_length_calc",
                "maxWidth": 140
              },
              {
                "field": "policy_length_override",
                "maxWidth": 140
              },
              null,
              {
                "field": "include_suggested",
                "maxWidth": 140
              },
              {
                "field": "include_override",
                "maxWidth": 140
              },
              null,
              {
                "field": "premium_suggested",
                "maxWidth": 140
              },
              {
                "field": "premium_override",
                "maxWidth": 140
              },
              null,
              {
                "field": "incurred_suggested",
                "maxWidth": 140
              },
              {
                "field": "incurred_override",
                "maxWidth": 140
              },
              null,
              {
                "field": "incurred_large_suggested",
                "maxWidth": 140
              },
              {
                "field": "incurred_large_override",
                "maxWidth": 140
              },
              null,
              {
                "field": "incurred_cat_suggested",
                "maxWidth": 140
              },
              {
                "field": "incurred_cat_override",
                "maxWidth": 140
              },
              null,
              {
                "field": "incurred_att_suggested",
                "maxWidth": 140
              },
              {
                "field": "incurred_att_override",
                "maxWidth": 140
              }
            ]}
              with="cds/rating_summary"
              filter="display_show_row_inputs"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table title="Assumptions"
              data={[
              {
                "datum": "detail_by_year",
                "elementLabelBy": "display_yoa"
              }
            ]}
              fields={[
              {
                "field": "port_chg_suggested",
                "maxWidth": 140
              },
              {
                "field": "port_chg_override",
                "maxWidth": 140
              },
              null,
              {
                "field": "rate_chg_suggested",
                "maxWidth": 140
              },
              {
                "field": "rate_chg_override",
                "maxWidth": 140
              },
              null,
              {
                "field": "infl_chg_suggested",
                "maxWidth": 140
              },
              {
                "field": "infl_chg_override",
                "maxWidth": 140
              },
              null,
              {
                "field": "interp_blended_selected_perc_ult",
                "maxWidth": 140
              },
              {
                "field": "large_threshold_sett_fx",
                "maxWidth": 140
              }
            ]}
              with="cds/rating_summary"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/triangle_projection/benchmark_use_occurrence"
            ]}
              shownBy="/cds/show_hide/node/not_new_to_market" />
            <HX.Pane>
            
              <HX.Collection fields={[
                null
              ]} />
          
            </HX.Pane>
            <HX.Pane>
            
              <HX.Collection fields={[
                null
              ]} />
          
            </HX.Pane>
            <HX.Pane>
            
              <HX.Collection fields={[
                null
              ]} />
          
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Experience Loss Ratio Summary">
          <HX.Pane flow="right">
            <HX.Table title="Attritional Loss Ratio Analysis"
              data={[
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              }
            ]}
              fields={[
              "ulr_initial_benchmark",
              "ulr_initial_experience",
              "ulr_initial_experience_weighting",
              "ulr_initial_selected",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/attritional"
              transpose={true}
              syncColumnWidthsKey="att" />
            <HX.Table title="Large Loss Ratio Analysis"
              data={[
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              }
            ]}
              fields={[
              "ulr_benchmark",
              "ulr_experience",
              "ulr_experience_weighting",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/large"
              transpose={true}
              syncColumnWidthsKey="large" />
            <HX.Table title="Catastrophe Loss Ratio Analysis"
              data={[
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              }
            ]}
              fields={[
              "ulr_benchmark",
              "ulr_experience",
              "ulr_experience_weighting",
              {
                "field": "ulr_rms",
                "shownBy": "/cds/show_hide/node/loss_ratio_rms"
              },
              "ulr_selected_ol_exc_nml",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/catastrophe"
              transpose={true}
              syncColumnWidthsKey="cat" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Loss Ratio Development"
          defaultCollapsed={true}
          shownBy="/cds/show_hide/node/not_new_to_market">
          <HX.Pane flow="right">
            <HX.Table title="Attritional On-level GG Loss Ratio Progression"
              data={[
              {
                "datum": "detail_by_year",
                "elementLabelBy": "display_yoa"
              }
            ]}
              fields={[
              null,
              {
                "field": "display_attritional_incurred_lr",
                "maxWidth": 140
              },
              {
                "field": "display_attritional_chainladder_lr",
                "maxWidth": 140
              },
              {
                "field": "display_attritional_approach",
                "maxWidth": 140
              },
              {
                "field": "display_attritional_selected_lr",
                "maxWidth": 140
              }
            ]}
              with="cds/rating_summary"
              filter="display_show_row_rating"
              syncColumnWidthsKey="att" />
            <HX.Table title="Large On-level GG Loss Ratio Progression"
              data={[
              {
                "datum": "detail_by_year",
                "elementLabelBy": "display_yoa"
              }
            ]}
              fields={[
              null,
              {
                "field": "display_large_incurred_lr",
                "maxWidth": 140
              },
              {
                "field": "display_large_chainladder_lr",
                "maxWidth": 140
              },
              {
                "field": "display_large_approach",
                "maxWidth": 140
              },
              {
                "field": "display_large_selected_lr",
                "maxWidth": 140
              }
            ]}
              with="cds/rating_summary"
              filter="display_show_row_rating"
              syncColumnWidthsKey="large" />
            <HX.Table title="Catastrophe On-level GG Loss Ratio Progression"
              data={[
              {
                "datum": "detail_by_year",
                "elementLabelBy": "display_yoa"
              }
            ]}
              fields={[
              null,
              {
                "field": "display_cat_incurred_lr",
                "maxWidth": 140
              },
              {
                "field": "display_cat_chainladder_lr",
                "maxWidth": 140
              },
              {
                "field": "display_cat_approach",
                "maxWidth": 140
              },
              {
                "field": "display_cat_selected_lr",
                "maxWidth": 140
              }
            ]}
              with="cds/rating_summary"
              filter="display_show_row_rating"
              syncColumnWidthsKey="cat" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Rating Summary"
          shownBy="cds/show_hide/page/show_sov">
          <HX.Pane>
            <HX.Table title="Exposure Rating Summary"
              data={[
              null,
              {
                "datum": "att_and_large",
                "maxWidth": 140
              },
              {
                "datum": "cat",
                "maxWidth": 140
              }
            ]}
              fields={[
              "pre_uw_adj_gn_ulr"
            ]}
              with="cds/exposure_adj"
              kb-interactive={true}
              transpose={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Blended Summary"
          shownBy="cds/show_hide/page/show_sov">
          <HX.Pane>
            <HX.Table title="Exposure / Experience Rating Weights"
              data={[
              null,
              {
                "datum": "exposure_rating",
                "maxWidth": 140
              },
              {
                "datum": "experience_rating",
                "maxWidth": 140
              }
            ]}
              fields={[
              "pre_uw_adj_gn_ulr",
              null,
              "sugg_weight",
              "sel_weight"
            ]}
              with="cds/exposure_experience_weights"
              kb-interactive={true}
              transpose={true} />
            <HX.Collection fields={[
              "gn_final_ulr",
              null,
              null,
              null,
              null,
              null,
              null
            ]}
              with="cds/exposure_experience_weights"
              numCols={7} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Overall Summary">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection title="Attritional Adjustments"
                fields={[
                "cds/rating_summary/summary_ratios/attritional/uw_adjustment",
                "cds/rating_summary/summary_ratios/attritional/uw_override"
              ]}
                syncColumnWidthsKey="att" />
              <HX.Collection fields={[
                "cds/rating_summary/summary_ratios/attritional/uw_rationale"
              ]}
                shownBy="cds/show_hide/node/rs_att_rationale" />
            </HX.Pane>
            <HX.Pane flow="down">
              <HX.Collection title="Large Adjustments"
                fields={[
                "cds/rating_summary/summary_ratios/large/uw_adjustment",
                "cds/rating_summary/summary_ratios/large/uw_override"
              ]}
                syncColumnWidthsKey="large" />
              <HX.Collection fields={[
                "cds/rating_summary/summary_ratios/large/uw_rationale"
              ]}
                shownBy="cds/show_hide/node/rs_lrg_rationale" />
            </HX.Pane>
            <HX.Pane flow="down">
              <HX.Collection title="Catastrophe Adjustments"
                fields={[
                "cds/rating_summary/summary_ratios/catastrophe/uw_adjustment",
                "cds/rating_summary/summary_ratios/catastrophe/uw_override"
              ]}
                syncColumnWidthsKey="cat" />
              <HX.Collection fields={[
                "cds/rating_summary/summary_ratios/catastrophe/uw_rationale"
              ]}
                shownBy="cds/show_hide/node/rs_cat_rationale" />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table title="Attritional Loss Ratio Analysis"
              data={[
              {
                "datum": "gg_pst_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pst_uw_adj",
                "maxWidth": 140
              }
            ]}
              fields={[
              "blended_LR",
              "ulr_uw_override",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/attritional"
              transpose={true}
              syncColumnWidthsKey="att" />
            <HX.Table title="Large Loss Ratio Analysis"
              data={[
              {
                "datum": "gg_pst_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pst_uw_adj",
                "maxWidth": 140
              }
            ]}
              fields={[
              "blended_LR",
              "ulr_uw_override",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/large"
              transpose={true}
              syncColumnWidthsKey="large" />
            <HX.Table title="Catastrophe Loss Ratio Analysis"
              data={[
              {
                "datum": "gg_pst_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pst_uw_adj",
                "maxWidth": 140
              }
            ]}
              fields={[
              "blended_LR",
              "ulr_uw_override",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/catastrophe"
              transpose={true}
              syncColumnWidthsKey="cat" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Loss Ratio Charts"
          shownBy="/cds/show_hide/node/not_new_to_market">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "chart_basis"
            ]}
              with="cds/rating_summary"
              horizontal={true} />
            <HX.Pane>
            
              <HX.Collection fields={[
                null
              ]} />
          
            </HX.Pane>
            <HX.Pane>
            
              <HX.Collection fields={[
                null
              ]} />
          
            </HX.Pane>
            <HX.Pane>
            
              <HX.Collection fields={[
                null
              ]} />
          
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right"
            shownBy="cds/rating_summary/chart_show_basis_gg">
            <CustomComponent title="GG Att. ILR"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/rating_summary/detail_by_year"
              }
            ]}
              traces={[
              {
                "color": "#2A3178",
                "field": "chart_att_ilr_gg",
                "label": "Att. ILR"
              },
              {
                "color": "#CA3397",
                "field": "chart_att_ilr_ol_gg",
                "label": "Att. ILR on-level"
              }
            ]}
              series={[
              {
                "points": [
                  {
                    "list": "cds/rating_summary/detail_by_year",
                    "x": "yoa",
                    "y": "chart_att_ilr_proposed_gg"
                  }
                ],
                "seriesColor": "#4FADC7",
                "seriesLabel": "Att. Proposed",
                "seriesLineType": "dash",
                "seriesMode": "lines"
              }
            ]}
              xAxisTickAngle={-45}
              xAxisLabel="Year"
              yAxisLabel="GG ILR (%)"
              barMode="group"
              gapBetweenBarsSize={0.4}
              width={600}
              height={500}
              y2SeparateAxis={false} />
            <CustomComponent title="GG Large ILR"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/rating_summary/detail_by_year"
              }
            ]}
              traces={[
              {
                "color": "#2A3178",
                "field": "chart_large_ilr_gg",
                "label": "Large ILR"
              },
              {
                "color": "#CA3397",
                "field": "chart_large_ilr_ol_gg",
                "label": "Large ILR on-level"
              }
            ]}
              series={[
              {
                "points": [
                  {
                    "list": "cds/rating_summary/detail_by_year",
                    "x": "yoa",
                    "y": "chart_large_ilr_proposed_gg"
                  }
                ],
                "seriesColor": "#4FADC7",
                "seriesLabel": "Large Proposed",
                "seriesLineType": "dash",
                "seriesMode": "lines"
              }
            ]}
              xAxisTickAngle={-45}
              xAxisLabel="Year"
              yAxisLabel="GG ILR (%)"
              barMode="group"
              gapBetweenBarsSize={0.4}
              width={600}
              height={500}
              y2SeparateAxis={false} />
            <CustomComponent title="GG CAT ILR"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/rating_summary/detail_by_year"
              }
            ]}
              traces={[
              {
                "color": "#2A3178",
                "field": "chart_cat_ilr_gg",
                "label": "Cat ILR"
              },
              {
                "color": "#CA3397",
                "field": "chart_cat_ilr_ol_gg",
                "label": "Cat ILR on-level"
              }
            ]}
              series={[
              {
                "points": [
                  {
                    "list": "cds/rating_summary/detail_by_year",
                    "x": "yoa",
                    "y": "chart_cat_ilr_proposed_gg"
                  }
                ],
                "seriesColor": "#4FADC7",
                "seriesLabel": "Cat Proposed",
                "seriesLineType": "dash",
                "seriesMode": "lines"
              }
            ]}
              xAxisTickAngle={-45}
              xAxisLabel="Year"
              yAxisLabel="GG ILR (%)"
              barMode="group"
              gapBetweenBarsSize={0.4}
              width={600}
              height={500}
              y2SeparateAxis={false} />
          </HX.Pane>
          <HX.Pane flow="right"
            shownBy="cds/rating_summary/chart_show_basis_gn">
            <CustomComponent title="GN Att. ILR"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/rating_summary/detail_by_year"
              }
            ]}
              traces={[
              {
                "color": "#2A3178",
                "field": "chart_att_ilr_gn",
                "label": "Att. ILR"
              },
              {
                "color": "#CA3397",
                "field": "chart_att_ilr_ol_gn",
                "label": "Att. ILR on-level"
              }
            ]}
              series={[
              {
                "points": [
                  {
                    "list": "cds/rating_summary/detail_by_year",
                    "x": "yoa",
                    "y": "chart_att_ilr_proposed_gn"
                  }
                ],
                "seriesColor": "#4FADC7",
                "seriesLabel": "Att. Proposed",
                "seriesLineType": "dash",
                "seriesMode": "lines"
              }
            ]}
              xAxisTickAngle={-45}
              xAxisLabel="Year"
              yAxisLabel="GN ILR (%)"
              barMode="group"
              gapBetweenBarsSize={0.4}
              width={800}
              height={500}
              y2SeparateAxis={false} />
            <CustomComponent title="GN Large ILR"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/rating_summary/detail_by_year"
              }
            ]}
              traces={[
              {
                "color": "#2A3178",
                "field": "chart_large_ilr_gn",
                "label": "Large ILR"
              },
              {
                "color": "#CA3397",
                "field": "chart_large_ilr_ol_gn",
                "label": "Large ILR on-level"
              }
            ]}
              series={[
              {
                "points": [
                  {
                    "list": "cds/rating_summary/detail_by_year",
                    "x": "yoa",
                    "y": "chart_large_ilr_proposed_gn"
                  }
                ],
                "seriesColor": "#4FADC7",
                "seriesLabel": "Large Proposed",
                "seriesLineType": "dash",
                "seriesMode": "lines"
              }
            ]}
              xAxisTickAngle={-45}
              xAxisLabel="Year"
              yAxisLabel="GN ILR (%)"
              barMode="group"
              gapBetweenBarsSize={0.4}
              width={800}
              height={500}
              y2SeparateAxis={false} />
            <CustomComponent title="GN CAT ILR"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/rating_summary/detail_by_year"
              }
            ]}
              traces={[
              {
                "color": "#2A3178",
                "field": "chart_cat_ilr_gn",
                "label": "Cat ILR"
              },
              {
                "color": "#CA3397",
                "field": "chart_cat_ilr_ol_gn",
                "label": "Cat ILR on-level"
              }
            ]}
              series={[
              {
                "points": [
                  {
                    "list": "cds/rating_summary/detail_by_year",
                    "x": "yoa",
                    "y": "chart_cat_ilr_proposed_gn"
                  }
                ],
                "seriesColor": "#4FADC7",
                "seriesLabel": "Cat Proposed",
                "seriesLineType": "dash",
                "seriesMode": "lines"
              }
            ]}
              xAxisTickAngle={-45}
              xAxisLabel="Year"
              yAxisLabel="GN ILR (%)"
              barMode="group"
              gapBetweenBarsSize={0.4}
              width={800}
              height={500}
              y2SeparateAxis={false} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Profit Commission">
          <HX.Pane flow="down">
            <HX.Table title="Profit Commission Summary"
              data={[
              null,
              {
                "datum": "technical",
                "maxWidth": 140
              }
            ]}
              fields={[
              "percent_pc",
              null,
              "amount_pc_100",
              "amount_pc_afb",
              null,
              "percent_pc_prior"
            ]}
              with="cds/rating_summary"
              transpose={true}
              syncColumnWidthsKey="pc_summary" />
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "cds/profit_commission/consistent_pc_latest_param"
              ]} />
              <HX.Pane>
            
                <HX.Collection fields={[
                  null
                ]} />
          
              </HX.Pane>
              <HX.Pane>
            
                <HX.Collection fields={[
                  null
                ]} />
          
              </HX.Pane>
              <HX.Pane>
            
                <HX.Collection fields={[
                  null
                ]} />
          
              </HX.Pane>
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="simulate_pc_task"
                title="Calculate Profit Commission" />
              <HX.Pane>
            
                <HX.Collection fields={[
                  null
                ]} />
          
              </HX.Pane>
              <HX.Pane>
            
                <HX.Collection fields={[
                  null
                ]} />
          
              </HX.Pane>
              <HX.Pane>
            
                <HX.Collection fields={[
                  null
                ]} />
          
              </HX.Pane>
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Loss Ratio Summary">
          <HX.Pane flow="down">
            <HX.Table title="Loss Ratio Summary"
              data={[
              null,
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gg_pst_uw_adj",
                "maxWidth": 140
              }
            ]}
              fields={[
              "ulr_priced_final"
            ]}
              with="cds/rating_summary/summary_ratios/total"
              shownBy="/cds/show_hide/node/show_experience"
              transpose={true}
              syncColumnWidthsKey="lr_summary" />
            <HX.Table data={[
              null,
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pst_uw_adj",
                "maxWidth": 140
              }
            ]}
              fields={[
              "ulr_plan",
              null,
              "ulr_priced_final_exc_pc",
              "ulr_priced_final_inc_pc",
              null,
              "ulr_prior"
            ]}
              with="cds/rating_summary/summary_ratios/total"
              transpose={true}
              syncColumnWidthsKey="lr_summary" />
            <HX.Table data={[
              null,
              {
                "datum": "pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "pst_uw_adj",
                "maxWidth": 140
              }
            ]}
              fields={[
              "comb_ratio_exc_pc",
              "comb_ratio_inc_pc"
            ]}
              with="cds/rating_summary/summary_ratios/total"
              transpose={true}
              syncColumnWidthsKey="lr_summary" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="KPI Summary and Exhibits">
          <HX.Pane flow="right">
            <HX.Pane flow="down"
              stretch={true}>
              <HX.Table title="KPI Summary"
                data={[
                null,
                {
                  "datum": "pre_uw_adj",
                  "maxWidth": 140
                },
                {
                  "datum": "pst_uw_adj",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "expected_profit",
                "allocated_capital",
                "roc",
                null,
                "bpi",
                "tpi",
                null,
                "bpi_prior",
                "tpi_prior"
              ]}
                with="cds/rating_summary/kpi"
                transpose={true}
                syncColumnWidthsKey="lr_summary" />
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "cds/rating_summary/chart_premium_breakdown/uw_adj_basis"
                ]}
                  title="Chart Settings" />
                <HX.Pane>
            
                  <HX.Collection fields={[
                    null
                  ]} />
          
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection fields={[
                  "cds/rating_summary/chart_premium_breakdown/premium_basis"
                ]} />
                <HX.Pane>
            
                  <HX.Collection fields={[
                    null
                  ]} />
          
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
            <CustomComponent title="Premium Breakdown"
              data={[
              {
                "label": "Technical",
                "structure": "cds/rating_summary/chart_premium_breakdown/technical"
              },
              {
                "label": "Benchmark",
                "structure": "cds/rating_summary/chart_premium_breakdown/benchmark"
              },
              {
                "label": "Client",
                "structure": "cds/rating_summary/chart_premium_breakdown/client"
              }
            ]}
              traces={[
              {
                "color": "#F7CFEC",
                "field": "client_premium",
                "label": "Client Premium"
              },
              {
                "color": "#6C0D7A",
                "field": "losses",
                "label": "Losses"
              },
              {
                "color": "#0C6122",
                "field": "reinsurance",
                "label": "Reinsurance"
              },
              {
                "color": "#4FADC7",
                "field": "cost_of_capital",
                "label": "Cost of Capital"
              },
              {
                "color": "#0DB0E0",
                "field": "expense",
                "label": "Expense"
              },
              {
                "color": "#1E4671",
                "field": "bp_loading",
                "label": "BP Loading"
              },
              {
                "color": "#F47211",
                "field": "brokerage",
                "label": "Brokerage"
              }
            ]}
              xAxisTickAngle={0}
              gapBetweenBarsSize={0.05}
              xAxisLabel="Section"
              yAxisLabel="Amount"
              barMode="relative"
              tpiLabelString="cds/rating_summary/chart_premium_breakdown/technical/metric_string"
              bpiLabelString="cds/rating_summary/chart_premium_breakdown/benchmark/metric_string"
              dynamicTitle="cds/rating_summary/chart_premium_breakdown/title_string" />
            <CustomComponent title="ILR BY CLAIM TYPE & YOA"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/rating_summary/detail_by_year"
              }
            ]}
              traces={[
              {
                "color": "#4FADC7",
                "field": "chart_att_ilr",
                "label": "Attrition"
              },
              {
                "color": "#E8A4D5",
                "field": "chart_large_ilr",
                "label": "Large"
              },
              {
                "color": "#CA3397",
                "field": "chart_cat_ilr",
                "label": "Cat"
              }
            ]}
              xAxisTickAngle={-45}
              xAxisLabel="Year"
              yAxisLabel="GG ILR (%)"
              barMode="stack"
              gapBetweenBarsSize={0.4} />
            <CustomComponent title="TOTAL LR SUMMARY BY YOA"
              data={[
              {
                "labelBy": "yoa",
                "list": "cds/rating_summary/detail_by_year"
              }
            ]}
              traces={[
              {
                "color": "#E8A4D5",
                "field": "chart_premium",
                "label": "GGWP"
              }
            ]}
              series={[
              {
                "points": [
                  {
                    "list": "cds/rating_summary/detail_by_year",
                    "x": "yoa",
                    "y": "chart_pricing_lr"
                  }
                ],
                "seriesColor": "#CA3397",
                "seriesLabel": "GG Pricing LR %",
                "seriesLineType": "dash"
              },
              {
                "points": [
                  {
                    "list": "cds/rating_summary/detail_by_year",
                    "x": "yoa",
                    "y": "chart_experience_lr"
                  }
                ],
                "seriesColor": "#4FADC7",
                "seriesLabel": "GG Exp LR %",
                "seriesMode": "lines"
              }
            ]}
              xAxisTickAngle={-45}
              yAxis2Label="GG ILR (%)"
              yAxisLabel="GGWP"
              xAxisLabel="Year"
              barMode="group"
              gapBetweenBarsSize={0.4}
              width={800}
              height={500}
              y2SeparateAxis={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Premium Summary"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane flow="down"
              stretch={true}>
              <HX.Table title="Premium Summary"
                data={[
                null,
                {
                  "datum": "technical",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "gn_premium_quoted_inc_pc_afb",
                "gn_premium_quoted_exc_pc_afb",
                "gg_premium_quoted_afb"
              ]}
                with="cds/rating_summary"
                transpose={true}
                syncColumnWidthsKey="pc_summary" />
              <HX.Table data={[
                null,
                {
                  "datum": "amts_pre_uw_adj",
                  "maxWidth": 140
                },
                {
                  "datum": "amts_pst_uw_adj",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "gn_premium_tech_inc_pc_afb",
                "gg_premium_tech_afb",
                null,
                "gn_premium_bench_inc_pc_afb",
                "gg_premium_bench_afb"
              ]}
                with="cds/rating_summary/technical"
                transpose={true}
                syncColumnWidthsKey="pc_summary" />
            </HX.Pane>
            <HX.Pane flow="down"
              stretch={true}>
              <HX.Table title="Technical Premium Derivation"
                data={[
                null,
                {
                  "datum": "amts_pre_uw_adj",
                  "maxWidth": 140
                },
                {
                  "datum": "amts_pst_uw_adj",
                  "maxWidth": 140
                }
              ]}
                fields={[
                "losses_tot_afb",
                null,
                "lae_afb",
                "expense_afb",
                "reinsurance_afb",
                "investment_afb",
                "profit_req_afb",
                null,
                "gn_premium_tech_inc_pc_afb",
                null,
                "aqn_comm_afb",
                "aqn_brok_afb",
                "aqn_iptax_afb",
                "aqn_pc_afb",
                null,
                "gg_premium_tech_afb"
              ]}
                with="cds/rating_summary/technical"
                transpose={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}>
        <HX.Section title="Underwriter Rationale">
          <HX.Section title="Policy Details">
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "cds/standard_fields/insured_name.rationale",
                "hx_core/inception_date.rationale",
                "cds/standard_fields/facility_reference.rationale"
              ]} />
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Coverholder Background">
            <HX.Notes field="cds/rationale/coverholder_background_info" />
            <HX.Notes field="cds/rationale/coverholder_background" />
          </HX.Section>
          <HX.Section title="Binder History">
            <HX.Table title="Binder Historical Performance"
              data={[
              {
                "datum": "detail_by_year",
                "elementLabelBy": "display_yoa"
              },
              null,
              {
                "datum": "detail_by_year_total"
              }
            ]}
              fields={[
              {
                "field": "premium_selected",
                "maxWidth": 200
              },
              {
                "field": "premium_selected_gn",
                "maxWidth": 200
              },
              {
                "field": "incurred_selected",
                "maxWidth": 200
              },
              {
                "field": "incurred_selected_lr",
                "maxWidth": 150
              },
              {
                "field": "incurred_selected_lr_gn",
                "maxWidth": 150
              },
              {
                "field": "incurred_non_cat_selected_lr",
                "maxWidth": 150
              },
              {
                "field": "incurred_non_cat_selected_lr_gn",
                "maxWidth": 150
              }
            ]}
              with="cds/rating_summary"
              filter="display_show_row_inputs"
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="Binder Overview">
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Collection fields={[
                  "cds/rationale/contract_summary",
                  "cds/standard_fields/broker.rationale",
                  "cds/rationale/risk_type",
                  "cds/rationale/construction"
                ]} />
                <HX.With context={{
                  "index": 0,
                  "path": "cds/layers",
                  "type": "list"
                }}>
                  <HX.Collection fields={[
                    "written_line.rationale"
                  ]} />
                  <HX.Collection fields={[
                    "signed_line.rationale"
                  ]}
                    shownBy="/cds/show_hide/node/signed_line" />
                  <HX.Collection fields={[
                    "total_deductions"
                  ]} />
                </HX.With>
                <HX.Collection fields={[
                  "cds/currencies/source_currency.rationale",
                  "cds/rationale/risk_limit",
                  "cds/rationale/avg_limit",
                  "cds/rationale/top_counties",
                  "cds/rationale/avg_rate"
                ]} />
                <HX.Collection fields={[
                  "cds/rationale/curr_epi",
                  "cds/rationale/prev_epi",
                  "cds/rationale/curr_rc",
                  "cds/rationale/prev_rc"
                ]} />
                <HX.Collection fields={[
                  "cds/rationale/gg_att_lr_pre",
                  "cds/rationale/gn_att_lr_pre",
                  "cds/rationale/att_uw_adj",
                  "cds/rationale/gg_att_lr_pst",
                  "cds/rationale/gn_att_lr_pst"
                ]}
                  horizontal={true} />
                <HX.Collection title="Attritional Override UW Rationale"
                  fields={[
                  "cds/rating_summary/summary_ratios/attritional/uw_rationale"
                ]}
                  shownBy="cds/show_hide/node/rs_att_rationale"
                  horizontal={true} />
                <HX.Collection fields={[
                  "cds/rationale/gg_large_lr_pre",
                  "cds/rationale/gn_large_lr_pre",
                  "cds/rationale/large_uw_adj",
                  "cds/rationale/gg_large_lr_pst",
                  "cds/rationale/gn_large_lr_pst"
                ]}
                  horizontal={true} />
                <HX.Collection title="Large Override UW Rationale"
                  fields={[
                  "cds/rating_summary/summary_ratios/large/uw_rationale"
                ]}
                  shownBy="cds/show_hide/node/rs_lrg_rationale"
                  horizontal={true} />
                <HX.Collection fields={[
                  "cds/rationale/gg_cat_lr_pre",
                  "cds/rationale/gn_cat_lr_pre",
                  "cds/rationale/cat_uw_adj",
                  "cds/rationale/gg_cat_lr_pst",
                  "cds/rationale/gn_cat_lr_pst"
                ]}
                  horizontal={true} />
                <HX.Collection title="Catastrophe Override UW Rationale"
                  fields={[
                  "cds/rating_summary/summary_ratios/catastrophe/uw_rationale"
                ]}
                  shownBy="cds/show_hide/node/rs_cat_rationale"
                  horizontal={true} />
                <HX.Collection fields={[
                  "cds/rationale/gg_total_lr_pre",
                  "cds/rationale/gg_total_lr_pst"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "cds/rationale/comb_ratio_pre_adj_exc_pc",
                  "cds/rationale/comb_ratio_pst_adj_exc_pc"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "cds/rationale/comb_ratio_pre_adj_inc_pc",
                  "cds/rationale/comb_ratio_pst_adj_inc_pc"
                ]}
                  horizontal={true} />
                <HX.Collection fields={[
                  "cds/rating_summary/kpi/pst_uw_adj/bpi",
                  "cds/rating_summary/kpi/pst_uw_adj/tpi",
                  "cds/rating_summary/kpi/pst_uw_adj/roc",
                  "cds/rms/edm_summary/all_peril_selected_at_acc_fx/aal",
                  "cds/rationale/prm_aal_ratio",
                  "cds/rating_summary/technical/amount_pc_100",
                  "cds/rating_summary/technical/percent_pc"
                ]} />
              </HX.Pane>
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Underwriter Commentary">
            <HX.Notes field="cds/rationale/uw_commentary_info" />
            <HX.Notes field="cds/rationale/uw_commentary" />
            <HX.Pane flow="right">
              <HX.File field="cds/rationale/uw_commentary_file1" />
              <HX.File field="cds/rationale/uw_commentary_file2" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Actuarial Commentary">
            <HX.Collection fields={[
              "cds/rationale/actuarial_review"
            ]} />
            <HX.Notes field="cds/rationale/actuarial_notes" />
            <HX.Pane flow="right">
              <HX.File field="cds/rationale/actuarial_commentary_file1" />
              <HX.File field="cds/rationale/actuarial_commentary_file2" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Rate Change Rationale">
            <HX.Notes field="cds/rationale/rc_commentary" />
            <HX.Pane flow="right">
              <HX.File field="cds/rationale/rc_commentary_file1" />
              <HX.File field="cds/rationale/rc_commentary_file2" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Terms and Conditions Change">
            <HX.Notes field="cds/rationale/tc_commentary" />
            <HX.Pane flow="right">
              <HX.File field="cds/rationale/tc_commentary_file1" />
              <HX.File field="cds/rationale/tc_commentary_file2" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Aggregate Limits Vs. Utilisation">
            <HX.Notes field="cds/rationale/agglim_util_commentary" />
            <HX.Pane flow="right">
              <HX.File field="cds/rationale/agglim_util_commentary_file1" />
              <HX.File field="cds/rationale/agglim_util_commentary_file2" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Risk Profile">
            <HX.Notes field="cds/rationale/risk_profile_commentary_info" />
            <HX.Notes field="cds/rationale/risk_profile_commentary" />
            <HX.Pane flow="right">
              <HX.File field="cds/rationale/risk_profile_commentary_file1" />
              <HX.File field="cds/rationale/risk_profile_commentary_file2" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Territory Profile and Agg Distribution">
            <HX.Notes field="cds/rationale/territory_profile_commentary_info" />
            <HX.Notes field="cds/rationale/territory_profile_commentary" />
            <HX.Pane flow="right">
              <HX.File field="cds/rationale/territory_profile_commentary_file1" />
              <HX.File field="cds/rationale/territory_profile_commentary_file2" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Exposure Change">
            <HX.Notes field="cds/rationale/exposure_change_commentary_info" />
            <HX.Notes field="cds/rationale/exposure_change_commentary" />
            <HX.Pane flow="right">
              <HX.File field="cds/rationale/exposure_change_commentary_file1" />
              <HX.File field="cds/rationale/exposure_change_commentary_file2" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Large Losses">
            <HX.Notes field="cds/rationale/large_losses_commentary_info" />
            <HX.Notes field="cds/rationale/large_losses_commentary" />
            <HX.Pane flow="right">
              <HX.File field="cds/rationale/large_losses_commentary_file1" />
              <HX.File field="cds/rationale/large_losses_commentary_file2" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Download Rationale">
            <HX.Button task="generate_uw_rationale_doc_task"
              title="Generate UW Rationale Document" />
            <HX.File field="cds/rationale/document" />
          </HX.Section>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Profit Commission"
        fullWidth={true}
        viewScale={0.8}
        shownBy="cds/show_hide/page/show_profit_commission">
        <HX.Section title="Profit Commission Base Case Analysis">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Button task="simulate_pc_task"
                title="Calculate Profit Commission" />
              <HX.Notes field="cds/profit_commission/simulate_pc_task_status" />
              <HX.Notes field="cds/profit_commission/consistent_pc_latest_param" />
              <HX.With context={{
                "index": 0,
                "path": "cds/profit_commission/scenarios",
                "type": "list"
              }}>
                <HX.Collection fields={[
                  "result_exp_loss_att",
                  "result_exp_loss_large",
                  "result_exp_loss_cat_other",
                  "result_exp_loss_cat_natural",
                  "result_exp_loss_total",
                  null,
                  "result_exp_pc_payable",
                  "result_exp_pc_payable_override",
                  "result_exp_pc_payable_selected",
                  null,
                  "result_exp_frequency_loss"
                ]}
                  title="Base Case Analysis" />
              </HX.With>
            </HX.Pane>
            <HX.Pane flow="down">
            
              <HX.Collection fields={[
                null
              ]} />
          
            </HX.Pane>
            <HX.Pane flow="down">
            
              <HX.Collection fields={[
                null
              ]} />
          
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Simulation Parameters"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Simulation Parameters"
              data={[
              null,
              {
                "datum": "param_attritional"
              },
              {
                "datum": "param_large"
              },
              {
                "datum": "param_cat_natural"
              },
              {
                "datum": "param_cat_other"
              }
            ]}
              fields={[
              {
                "field": "expected_loss",
                "maxWidth": 140
              },
              {
                "field": "cov_benchmark",
                "maxWidth": 140
              },
              {
                "field": "cov_actual",
                "maxWidth": 140
              },
              {
                "field": "cov_selected",
                "maxWidth": 140
              },
              {
                "field": "stdev_benchmark",
                "maxWidth": 140
              },
              {
                "field": "stdev_actual",
                "maxWidth": 140
              },
              {
                "field": "stdev_selected",
                "maxWidth": 140
              },
              {
                "field": "distribution",
                "maxWidth": 300
              },
              {
                "field": "param_1",
                "maxWidth": 140
              },
              {
                "field": "param_2",
                "maxWidth": 140
              },
              {
                "field": "client_weight",
                "maxWidth": 140
              }
            ]}
              with="cds/profit_commission" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Profit Commission - Scenario Analysis"
          defaultCollapsed={true}>
          <HX.Pane flow="down">
            <HX.Table title="Simulation Scenario Inputs"
              data={[
              {
                "datum": "scenarios",
                "elementLabelBy": "label",
                "maxWidth": 140
              }
            ]}
              fields={[
              null,
              {
                "field": "include"
              },
              {
                "field": "additionalfeaturesindicator"
              },
              null,
              {
                "field": "share"
              },
              {
                "field": "expenses"
              },
              {
                "field": "basis"
              },
              {
                "field": "deficit"
              },
              null,
              {
                "field": "threshold_lr_cutoff1"
              },
              {
                "field": "threshold_bonus_share1"
              },
              {
                "field": "threshold_lr_cutoff2"
              },
              {
                "field": "threshold_bonus_share2"
              },
              {
                "field": "threshold_lr_cutoff3"
              },
              {
                "field": "threshold_bonus_share3"
              },
              {
                "field": "threshold_bonus_share4"
              },
              null,
              {
                "field": "slidingscale_bonus_lr"
              },
              {
                "field": "slidingscale_bonus_scale"
              },
              {
                "field": "slidingscale_bonus_maxtotalpc"
              },
              {
                "field": "slidingscale_clawback_lr"
              },
              {
                "field": "slidingscale_clawback_scale"
              },
              {
                "field": "slidingscale_clawback_mintotalpc"
              },
              null,
              {
                "field": "complete"
              }
            ]}
              with="cds/profit_commission"
              transpose={true}
              kb-interactive={true}
              syncColumnWidthsKey="pc_scenarios" />
            <HX.Table title="Simulation Scenario Outputs"
              data={[
              {
                "datum": "scenarios",
                "elementLabelBy": "label",
                "maxWidth": 140
              }
            ]}
              fields={[
              null,
              {
                "field": "result_exp_loss_att"
              },
              {
                "field": "result_exp_loss_large"
              },
              {
                "field": "result_exp_loss_cat_other"
              },
              {
                "field": "result_exp_loss_cat_natural"
              },
              {
                "field": "result_exp_loss_total"
              },
              null,
              {
                "field": "result_exp_pc_payable"
              },
              {
                "field": "result_exp_pc_payable_override"
              },
              {
                "field": "result_exp_pc_payable_selected"
              },
              null,
              {
                "field": "result_exp_frequency_loss"
              }
            ]}
              with="cds/profit_commission"
              transpose={true}
              kb-interactive={true}
              syncColumnWidthsKey="pc_scenarios" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Profit Commission - Loss Distributions"
          defaultCollapsed={true}>
          <HX.Pane flow="down">
            <HX.Table title="Simulation Scenario Inputs"
              data={[
              {
                "datum": "distributions",
                "elementLabelBy": "bucket"
              }
            ]}
              fields={[
              null,
              {
                "field": "ulr",
                "maxWidth": 140
              },
              null,
              {
                "field": "scenario",
                "maxWidth": 140
              },
              null,
              {
                "field": "uw_profit",
                "maxWidth": 140
              },
              {
                "field": "pc_payable",
                "maxWidth": 140
              },
              {
                "field": "pdf_att",
                "maxWidth": 140
              },
              {
                "field": "pdf_large",
                "maxWidth": 140
              },
              {
                "field": "pdf_cat_other",
                "maxWidth": 140
              },
              {
                "field": "pdf_cat_natural",
                "maxWidth": 140
              },
              {
                "field": "pdf_total",
                "maxWidth": 140
              }
            ]}
              with="cds/profit_commission"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Triangle Projection"
        fullWidth={true}
        shownBy="cds/show_hide/page/show_triangle">
        <HX.Section title="Triangle - Beazley Intelligence"
          defaultCollapsed={true}>
          <HX.TriangleData title="Triangle Data"
            triangle="tri_1_loaded_from_bi"
            with="cds/triangle_projection"
            syncColumnWidthsKey="align_tri_1" />
          <HX.Collection fields={[
            null,
            null
          ]} />
        </HX.Section>
        <HX.Section title="Triangle - Override"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "override_triangle_date",
              "override_triangle_years"
            ]}
              with="cds/triangle_projection"
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="tri_override_setup_task"
              title="Setup Override Triangle" />
            <HX.Collection fields={[
              "async_override_triangle_status"
            ]}
              with="cds/triangle_projection"
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "override_triangle"
            ]}
              with="cds/triangle_projection"
              horizontal={true} />
            <HX.Collection fields={[
              "assign_override_triangle_status"
            ]}
              with="cds/triangle_projection"
              horizontal={true} />
          </HX.Pane>
          <HX.TriangleData title="Triangle Data"
            triangle="tri_2_manual_input"
            with="cds/triangle_projection"
            syncColumnWidthsKey="align_tri_1" />
        </HX.Section>
        <HX.Section title="Triangle - Selected"
          defaultCollapsed={false}>
          <HX.TriangleData title="Triangle Data"
            triangle="tri_3_selected"
            with="cds/triangle_projection"
            syncColumnWidthsKey="align_tri_2" />
          <HX.TriangleDevFactors title="Triangle Incurred Development Factors"
            triangle="tri_3_selected"
            with="cds/triangle_projection"
            syncColumnWidthsKey="align_tri_2" />
        </HX.Section>
        <HX.Section title="Triangle - Exclusions"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Button task="tri_exclusions_setup_task"
              title="Setup Exclusions Triangle For Use" />
            <HX.Pane flow="down">
              <HX.Notes field="cds/triangle_projection/tri_exclusions_setup_task_status" />
              <HX.Notes field="cds/triangle_projection/tri_exclusions_dimensions_status" />
            </HX.Pane>
            <HX.Pane flow="down">
              <HX.Collection fields={[
                null
              ]} />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
          </HX.Pane>
          <HX.TriangleData title="Triangle - Exclusions"
            triangle="tri_3a_exclusions"
            with="cds/triangle_projection"
            syncColumnWidthsKey="align_tri_2" />
        </HX.Section>
        <HX.Section title="Triangle - Averages"
          defaultCollapsed={true}>
          <HX.TriangleAverages title="Triangle Averages"
            triangle="tri_3_selected"
            with="cds/triangle_projection"
            syncColumnWidthsKey="align_tri_2" />
        </HX.Section>
        <HX.Section title="Algorithmic Development and Overrides"
          defaultCollapsed={false}>
          <HX.Table title="Experience Analysis - incremental development factor"
            data={[
            {
              "datum": "incremental_dev_factor",
              "elementLabelBy": "development_label"
            },
            null,
            "tail_factor"
          ]}
            fields={[
            "experience_default",
            "experience_override",
            "experience_selected"
          ]}
            with="cds/triangle_projection"
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="align_tri_2"
            filter="show_idf_row" />
          <HX.Table title="Benchmarking Assumptions"
            data={[
            "cds/triangle_projection/experience_weight",
            "cds/triangle_projection/benchmark_name"
          ]}
            fields={[
            "default",
            "override",
            "selected"
          ]}
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="align_tri_2" />
          <HX.Collection fields={[
            "cds/triangle_projection/benchmark_use_occurrence"
          ]}
            syncColumnWidthsKey="align_tri_2" />
          <HX.Table title="Blending - Default - Incremental Development Factors"
            data={[
            {
              "datum": "incremental_dev_factor",
              "elementLabelBy": "development_label"
            },
            null,
            "tail_factor"
          ]}
            fields={[
            "experience_default",
            "benchmark_default",
            "blended_default"
          ]}
            with="cds/triangle_projection"
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="align_tri_2"
            filter="show_idf_row" />
          <HX.Table title="Blending - Selected - Incremental Development Factors"
            data={[
            {
              "datum": "incremental_dev_factor",
              "elementLabelBy": "development_label"
            },
            null,
            "tail_factor"
          ]}
            fields={[
            "experience_selected",
            "benchmark_selected",
            "blended_selected"
          ]}
            with="cds/triangle_projection"
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="align_tri_2"
            filter="show_idf_row" />
          <HX.Table title="Blending - Default - Percentage of Ultimate"
            data={[
            {
              "datum": "percents_ultimate",
              "elementLabelBy": "percents_label"
            }
          ]}
            fields={[
            "experience_default_perc_ult",
            "benchmark_default_perc_ult",
            "blended_default_perc_ult"
          ]}
            with="cds/triangle_projection"
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="align_tri_2"
            filter="show_ult_row" />
          <HX.Table title="Blending - Selected - Percentage of Ultimate"
            data={[
            {
              "datum": "percents_ultimate",
              "elementLabelBy": "percents_label"
            }
          ]}
            fields={[
            "experience_selected_perc_ult",
            "benchmark_selected_perc_ult",
            "blended_selected_perc_ult"
          ]}
            with="cds/triangle_projection"
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="align_tri_2"
            filter="show_ult_row" />
        </HX.Section>
        <HX.Section title="Projection"
          defaultCollapsed={false}>
          <HX.TriangleProjections title="Triangle Projections"
            triangle="tri_4_result"
            with="cds/triangle_projection" />
          <HX.TriangleChart title="Triangle Graphing"
            triangle="tri_4_result"
            with="cds/triangle_projection" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="RMS"
        shownBy="cds/show_hide/page/show_rms">
        <HX.Section title="RMS Results">
          <HX.Pane>
            <HX.Collection fields={[
              "rms/edm_reference_requested",
              null,
              null
            ]}
              with="cds"
              horizontal={true} />
            <HX.Pane flow="right">
              <HX.Button task="edm_fetch_task"
                title="Search Database" />
              <HX.Notes field="cds/rms/fetch_edm_data_reference_lookup_task_status" />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
            <HX.Collection fields={[
              "rms/edm_reference_selected",
              null,
              null
            ]}
              with="cds"
              horizontal={true} />
            <HX.Collection fields={[
              "rms/use_override",
              null,
              null
            ]}
              with="cds"
              horizontal={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection fields={[
              null
            ]} />
          </HX.Pane>
          <HX.Table title="Summary Information"
            data={[
            "cds/rms/edm_summary/all_peril_calc_at_acc_fx",
            "cds/rms/edm_summary/all_peril_override_at_acc_fx",
            "cds/rms/edm_summary/all_peril_selected_at_acc_fx"
          ]}
            fields={[
            "fx",
            "aal_raw",
            "aal",
            "std_dev",
            "prem",
            "coeff_var",
            "gross_lr_pre_adj",
            "gross_lr"
          ]}
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="rms" />
          <HX.Table title="EP Curve"
            data={[
            {
              "datum": "edm_epcurve",
              "elementLabelBy": "return_period_label"
            }
          ]}
            fields={[
            "all_peril_calc_at_acc_fx",
            "all_peril_override_at_acc_fx",
            "all_peril_selected_at_acc_fx"
          ]}
            with="cds/rms"
            kb-interactive={true}
            dynamic={true}
            syncColumnWidthsKey="rms" />
        </HX.Section>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};