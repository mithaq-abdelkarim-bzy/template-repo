
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
        viewScale={0.9}
        shownBy="cds/model_state/show_after_landing_page">
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
        <HX.Section title="Settings">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "new_to_market",
              "rms_modelling_available",
              "pc_modelling_required",
              "tri_modelling_required"
            ]}
              with="cds/risk_info"
              horizontal={true} />
          </HX.Pane>
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
            <HX.Button task="bi_clm_and_mvmt_inc_triangles_fetch_task"
              title="Load remaining data including triangles" />
            <HX.Button task="bi_clm_and_mvmt_exc_triangles_fetch_task"
              title="Load remaining data excluding triangles" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes field="cds/bi_data/fetch_clm_and_mvmt_detail_task_status" />
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
        <HX.Section title="Basic Financial Details">
          <HX.Pane flow="right">
            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "quoted_premium_100pct",
                "written_line",
                "quoted_premium",
                "status"
              ]}
                title="Premium & Status" />
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
                title="Deductions - Fixed" />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Profit Commission Details">
          <HX.Pane flow="right">
            <HX.With context={{
              "index": 0,
              "path": "cds/profit_commission/scenarios",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "additionalfeaturesindicator"
              ]}
                title="Profit Commission (PC)" />
              <HX.Collection fields={[
                "share",
                "expenses",
                "basis",
                "deficit"
              ]}
                shownBy="/cds/show_hide/node/pc_standard" />
            </HX.With>
            <HX.With context={{
              "index": 0,
              "path": "cds/profit_commission/scenarios",
              "type": "list"
            }}>
              <HX.Collection fields={[
                "threshold_bonus_share",
                "threshold_lr_cutoff"
              ]}
                title="Additional Features"
                shownBy="/cds/show_hide/node/pc_threshold" />
              <HX.Collection fields={[
                "slidingscale_bonus_lr",
                "slidingscale_bonus_scale",
                "slidingscale_bonus_maxtotalpc",
                "slidingscale_clawback_lr",
                "slidingscale_clawback_scale",
                "slidingscale_clawback_mintotalpc"
              ]}
                title="Additional Features"
                shownBy="/cds/show_hide/node/pc_sliding_scale" />
            </HX.With>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Strikes, riots and civil commotions">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "srcc_coverage_given_indicator",
              "srcc_fully_excluded_indicator",
              "srcc_sublimit_indicator",
              "srcc_sublimit"
            ]}
              with="cds/risk_info"
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        viewScale={0.7}
        shownBy="cds/model_state/show_after_landing_page">
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
        <HX.Section title="Loss Ratio Summary">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection title="Attritional Adjustments"
                fields={[
                "cds/rating_summary/summary_ratios/attritional/uw_adjustment",
                "cds/rating_summary/summary_ratios/attritional/gg_pst_uw_adj/ulr_uw_override"
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
              null,
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              },
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
              "ulr_initial_benchmark",
              "ulr_initial_experience",
              "ulr_initial_experience_weighting",
              "ulr_initial_selected",
              "ulr_selected_ol",
              "ulr_uw_override",
              "ulr_final_uw",
              "ulr_actuarial_override_output",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/attritional"
              transpose={true}
              syncColumnWidthsKey="att" />
            <HX.Table title="Large Loss Ratio Analysis"
              data={[
              null,
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              },
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
              "ulr_benchmark",
              "ulr_experience",
              "ulr_experience_weighting",
              "ulr_selected_ol",
              "ulr_uw_override",
              "ulr_final_uw",
              "ulr_actuarial_override_output",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/large"
              transpose={true}
              syncColumnWidthsKey="large" />
            <HX.Table title="Catastrophe Loss Ratio Analysis"
              data={[
              null,
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              },
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
              {
                "field": "ulr_rms",
                "shownBy": "/cds/show_hide/node/loss_ratio_rms"
              },
              {
                "field": "ulr_benchmark",
                "shownBy": "/cds/show_hide/node/loss_ratio_benchmark"
              },
              "ulr_experience",
              "ulr_experience_weighting",
              "ulr_selected_ol_exc_nml",
              "ulr_selected_ol",
              "ulr_uw_override",
              "ulr_final_uw",
              "ulr_actuarial_override_output",
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
              yAxisLabel="GG ILR"
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
              yAxisLabel="GG ILR"
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
              yAxisLabel="GG ILR"
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
              yAxisLabel="GN ILR"
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
              yAxisLabel="GN ILR"
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
              yAxisLabel="GN ILR"
              barMode="group"
              gapBetweenBarsSize={0.4}
              width={800}
              height={500}
              y2SeparateAxis={false} />
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
              "ulr_bench",
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
              <HX.With context={{
                "index": 0,
                "path": "cds/layers",
                "type": "list"
              }}>
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    "rate_change/rate_change/uw_selected"
                  ]}
                    title="Rate Change" />
                  <HX.Pane>
            
                    <HX.Collection fields={[
                      null
                    ]} />
          
                  </HX.Pane>
                </HX.Pane>
              </HX.With>
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
              yAxisLabel="GG ILR"
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
              yAxis2Label="GG ILR"
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
                "expense_afb",
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
        viewScale={1}
        shownBy="cds/model_state/show_after_landing_page">
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
        <HX.Section title="UW Summary Document">
          <HX.Pane flow="right">
            <HX.Button task="generate_uw_doc_task"
              title="Generate Document" />
            <HX.File field="uw_doc_template" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Actuarial Commentary"
          defaultCollapsed={true}>
          <HX.Collection fields={[
            "cds/rationale/actuarial_review"
          ]} />
          <HX.Notes field="cds/rationale/actuarial_notes" />
        </HX.Section>
        <HX.Section title="Useful Information">
          <HX.Pane flow="right">
            <HX.Notes field="cds/rationale/help_file" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Claim Summary"
        fullWidth={true}
        shownBy="cds/model_state/show_after_landing_page">
        <HX.Section title="Large Loss Exhibits">
          <HX.Pane flow="right">
            <HX.Table title="Large Loss Freq/Sev Trends @100% in Settlement Fx"
              data={[
              {
                "datum": "chart_freq_sev",
                "elementLabelBy": "yoa_label"
              }
            ]}
              fields={[
              "premium",
              "freq_per_million",
              "severity"
            ]}
              with="cds/claim_summary"
              filter="show_row"
              kb-interactive={true}
              dynamic={true} />
            <HX.Table title="Top 15 Cat Events - @100% in Settlement Fx"
              data={[
              "cds/claim_summary/top15_cat_events"
            ]}
              fields={[
              "beazley_catcode",
              "bi_paid",
              "bi_os",
              "bi_incurred",
              "pre_peer_blend_incurred",
              "pre_peer_most_likely_incurred"
            ]}
              filter="show_row"
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Claims Details">
          <HX.Pane flow="right">
            <HX.Table title="Claims Listing - Top 100 large losses"
              data={[
              "cds/bi_data/claims_listing"
            ]}
              fields={[
              "class_rank",
              "claim_reference",
              "yoa",
              "claim_made_date",
              "bi_paid",
              "bi_os",
              "bi_incurred",
              "pre_peer_blend_incurred",
              "pre_peer_most_likely_incurred"
            ]}
              filter="show_large"
              kb-interactive={true}
              dynamic={true} />
            <HX.Table title="Claims Listing - Top 100 cat losses"
              data={[
              "cds/bi_data/claims_listing"
            ]}
              fields={[
              "class_rank",
              "claim_reference",
              "yoa",
              "claim_made_date",
              "beazley_catcode",
              "bi_paid",
              "bi_os",
              "bi_incurred",
              "pre_peer_blend_incurred",
              "pre_peer_most_likely_incurred"
            ]}
              filter="show_cat"
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
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
            "aal",
            "std_dev",
            "prem",
            "coeff_var",
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
                "field": "threshold_bonus_share"
              },
              {
                "field": "threshold_lr_cutoff"
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
          <HX.Table title="Experience Analysis - Incremental Development Factors"
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
      <HX.Page title="Actuarial Info (typically hidden)"
        fullWidth={true}
        shownBy="cds/show_hide/page/show_actuarial">
        <HX.Section title="Keep actuarial view open:">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rationale/actuarial_view"
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
        </HX.Section>
        <HX.Section title="Nodes not shown to UW:">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "final_data_asat",
              "bic_data_asat"
            ]}
              with="cds/risk_info"
              title="Submission Details" />
            <HX.Collection fields={[
              "migrated_record"
            ]}
              with="cds/model_state" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Loss Ratio Summary - detailed, with Actuarial Overrides Active">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection title="Attritional Adjustments"
                fields={[
                "cds/rating_summary/summary_ratios/attritional/uw_adjustment",
                "cds/rating_summary/summary_ratios/attritional/gg_pst_uw_adj/ulr_uw_override"
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
              null,
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              },
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
              "ulr_initial_benchmark",
              "ulr_initial_experience",
              "ulr_initial_experience_weighting",
              "ulr_initial_selected",
              "ulr_previous_selected_inferred",
              "ulr_previous_override",
              "ulr_previous",
              "ulr_previous_suggested",
              "ulr_selected_ol_py_factors_data",
              "ulr_selected_ol_py_factors",
              "ulr_selected_ol_py_ol_assump",
              "ulr_selected_ol_exc_scalant",
              "ulr_selected_ol",
              "ulr_uw_override",
              "ulr_final_uw",
              "ulr_actuarial_override",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/attritional"
              transpose={true}
              syncColumnWidthsKey="att" />
            <HX.Table title="Large Loss Ratio Analysis"
              data={[
              null,
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              },
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
              "ulr_previous",
              "ulr_benchmark",
              "ulr_experience",
              "ulr_experience_weighting",
              "ulr_selected_ol",
              "ulr_uw_override",
              "ulr_final_uw",
              "ulr_actuarial_override",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/large"
              transpose={true}
              syncColumnWidthsKey="large" />
            <HX.Table title="Catastrophe Loss Ratio Analysis"
              data={[
              null,
              {
                "datum": "gg_pre_uw_adj",
                "maxWidth": 140
              },
              {
                "datum": "gn_pre_uw_adj",
                "maxWidth": 140
              },
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
              "ulr_previous_exc_nml",
              "ulr_previous",
              "ulr_rms",
              "ulr_benchmark",
              "ulr_experience",
              "ulr_experience_weighting",
              "ulr_selected_ol_exc_nml",
              "ulr_selected_ol_nml",
              "ulr_selected_ol",
              "ulr_uw_override",
              "ulr_final_uw",
              "ulr_actuarial_override",
              "ulr_final"
            ]}
              with="cds/rating_summary/summary_ratios/catastrophe"
              transpose={true}
              syncColumnWidthsKey="cat" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="KPI - detailed - Summary and Exhibits"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane flow="down"
              stretch={true}>
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
                "percent_pc_prior",
                "amount_pc_100",
                "amount_pc_afb"
              ]}
                with="cds/rating_summary"
                transpose={true}
                syncColumnWidthsKey="pc_summary" />
              <HX.Collection fields={[
                "cds/profit_commission/consistent_pc_latest_param"
              ]} />
              <HX.Button task="simulate_pc_task"
                title="Calculate Profit Commission" />
              <HX.Table data={[
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
              <HX.Table title="Premium Summary"
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
              <HX.Table data={[
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
                transpose={true}
                syncColumnWidthsKey="lr_summary" />
              <HX.Table title="Loss Ratio Summary"
                data={[
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
                "ulr_bench",
                "ulr_plan",
                null,
                "ulr_prior",
                null,
                "ulr_priced_final_exc_pc",
                "ulr_priced_final_inc_pc"
              ]}
                with="cds/rating_summary/summary_ratios/total"
                transpose={true}
                syncColumnWidthsKey="lr_summary" />
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
                "losses_att_afb",
                "losses_lrg_afb",
                "losses_cat_afb",
                "losses_tot_afb",
                null,
                "lae_afb",
                "reinsurance_afb",
                "expense_afb",
                "investment_afb",
                "profit_req_afb",
                null,
                "gn_premium_tech_inc_pc_afb",
                null,
                "aqn_comm_afb",
                "aqn_brok_afb",
                "aqn_iptax_afb",
                "aqn_total_exc_pc_afb",
                null,
                "aqn_pc_afb",
                null,
                "gg_premium_tech_afb"
              ]}
                with="cds/rating_summary/technical"
                transpose={true} />
            </HX.Pane>
          </HX.Pane>
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
            <HX.Table title="Please select policies you wish to include:"
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
            <HX.Button task="bi_clm_and_mvmt_inc_triangles_fetch_task"
              title="Load remaining data including triangles" />
            <HX.Button task="bi_clm_and_mvmt_exc_triangles_fetch_task"
              title="Load remaining data excluding triangles" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes field="cds/bi_data/fetch_clm_and_mvmt_detail_task_status" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Facility/Policy Listing Dataframe"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Table title="Returned Beazley Intelligence Data"
              data={[
              "cds/bi_data/facility_detail"
            ]}
              fields={[
              "include",
              "date_extracted",
              "section_reference",
              "insured_party",
              "inception_date",
              "expiry_date",
              "underwriter_name",
              "settlement_currency",
              "section_is_renewal",
              "division",
              "written_or_estimated_signed_line",
              "trifocus_name",
              "external_acquisition_cost_multiplier",
              "profit_commission_multiplier",
              "placing_brokername",
              "risk_class_code",
              "yoa",
              "written_or_estimated_premium",
              "rate_change_divisor",
              "spot_rate_usd_to_sett",
              "net_beazley_premium_sett_fx",
              "net_100pct_premium_sett_fx",
              "gross_100pct_premium_sett_fx",
              "net_100pct_premium_adjexp_sett_fx"
            ]}
              kb-interactive={true}
              dynamic={true} />
            <HX.Collection fields={[
              null,
              null
            ]}
              horizontal={false} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Claims Details Listing Dataframe"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Table title="Returned Beazley Intelligence Data"
              data={[
              "cds/bi_data/claims_listing"
            ]}
              fields={[
              "date_extracted",
              "section_reference",
              "claim_reference",
              "exposure_reference",
              "yoa",
              "beazley_catcode",
              "market_catcode",
              "trifocus_name",
              "settlement_currency",
              "block_indicator",
              "date_of_loss",
              "claim_made_date",
              "claim_or_circumstance",
              "beazley_share_total_incurred",
              "slip_order_total_incurred",
              "slip_order_total_paid",
              "beazley_share_pre_peer_blend",
              "beazley_share_pre_peer_most_likely",
              "loss_category",
              "bi_paid",
              "bi_os",
              "bi_incurred",
              "pre_peer_blend_incurred",
              "pre_peer_most_likely_incurred",
              "show_cat",
              "show_large",
              "class_rank"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
          <HX.Collection fields={[
            null,
            null
          ]}
            horizontal={false} />
        </HX.Section>
        <HX.Section title="Claims Incurred Movements Dataframe"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Table title="Returned Beazley Intelligence Data"
              data={[
              "cds/bi_data/claims_movements"
            ]}
              fields={[
              "date_extracted",
              "loss_category",
              "yoa",
              "mvmt_yr",
              "incurredmvmt_100_sett_fx"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
          <HX.Collection fields={[
            null,
            null
          ]}
            horizontal={false} />
        </HX.Section>
        <HX.Section title="EDM Dataframe"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Table data={[
              "cds/rms/edm"
            ]}
              fields={[
              "return_period",
              "probability",
              "portnum",
              "ws_loss_amount",
              "ws_premium",
              "ws_currency",
              "ws_fxrate",
              "eq_loss_amount",
              "eq_premium",
              "eq_currency",
              "eq_fxrate"
            ]}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rating Dataframe"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Table title="Complete List"
              data={[
              "cds/rating_summary/detail_by_year"
            ]}
              fields={[
              "yoa",
              "incept_date",
              "expiry_date",
              "expiry_date_annual_est",
              "include_suggested",
              "include_override",
              "include_selected",
              "include_selected_weight",
              "policy_length_calc",
              "policy_length_override",
              "policy_length_selected",
              "policy_length_scalant",
              "maturity",
              "port_chg_prior",
              "port_chg_suggested",
              "port_chg_override",
              "port_chg_selected",
              "port_chg_cumul_prior",
              "port_chg_cumul_suggested",
              "port_chg_cumul_selected",
              "rate_chg_prior",
              "rate_chg_account",
              "rate_chg_portfolio",
              "rate_chg_suggested",
              "rate_chg_override",
              "rate_chg_selected",
              "rate_chg_cumul_prior",
              "rate_chg_cumul_suggested",
              "rate_chg_cumul_selected",
              "infl_chg_prior",
              "infl_chg_suggested",
              "infl_chg_override",
              "infl_chg_selected",
              "infl_chg_cumul_prior",
              "infl_chg_cumul_suggested",
              "infl_chg_cumul_selected",
              "experience_default_perc_ult",
              "experience_selected_perc_ult",
              "benchmark_default_perc_ult",
              "benchmark_selected_perc_ult",
              "blended_default_perc_ult",
              "blended_selected_perc_ult",
              "interp_blended_selected_perc_ult",
              "premium_prior",
              "premium_suggested",
              "premium_override",
              "premium_selected",
              "premium_selected_ol",
              "premium_selected_ol_scaled",
              "incurred_prior",
              "paid_listing",
              "incurred_listing",
              "incurred_pp_blend",
              "incurred_pp_most_likely",
              "incurred_triangle",
              "incurred_suggested",
              "incurred_override",
              "incurred_selected",
              "large_threshold_usd",
              "large_threshold_sett_fx",
              "incurred_large_prior",
              "paid_large_listing",
              "incurred_large_listing",
              "incurred_large_pp_blend",
              "incurred_large_pp_most_likely",
              "incurred_large_triangle",
              "incurred_large_suggested",
              "incurred_large_override",
              "incurred_large_selected",
              "incurred_large_selected_lr",
              "incurred_large_selected_inflated",
              "incurred_cat_prior",
              "paid_cat_listing",
              "incurred_cat_listing",
              "incurred_cat_pp_blend",
              "incurred_cat_pp_most_likely",
              "incurred_cat_triangle",
              "incurred_cat_suggested",
              "incurred_cat_override",
              "incurred_cat_selected",
              "incurred_cat_selected_lr",
              "incurred_cat_selected_inflated",
              "incurred_att_prior",
              "paid_att_listing",
              "incurred_att_listing",
              "incurred_att_pp_blend",
              "incurred_att_pp_most_likely",
              "incurred_att_triangle",
              "incurred_att_suggested",
              "incurred_att_override",
              "incurred_att_selected",
              "incurred_att_selected_lr",
              "incurred_att_selected_inflated",
              "ultimate_att_cl_selected",
              "ultimate_att_cl_selected_py_factors",
              "ultimate_att_cl_selected_py_factors_data",
              "ultimate_att_cl_selected_ol",
              "ultimate_att_cl_selected_ol_exc_scalant",
              "ultimate_att_cl_selected_ol_py_ol_assump",
              "ultimate_att_cl_selected_ol_py_factors",
              "ultimate_att_cl_selected_ol_py_factors_data",
              "reserving_method_attritional",
              "ultimate_att_meth_selected_ol",
              "ultimate_att_meth_selected_ol_exc_scalant",
              "ultimate_att_meth_selected_ol_py_ol_assump",
              "ultimate_att_meth_selected_ol_py_factors",
              "ultimate_att_meth_selected_ol_py_factors_data",
              "weighting_exposure",
              "weighting_decay",
              "weighting_development",
              "weighting_combined",
              "weighting_final",
              "display_yoa",
              "display_premium_ol",
              "display_attritional_weight",
              "display_attritional_incurred_lr",
              "display_attritional_chainladder_lr",
              "display_attritional_approach",
              "display_attritional_selected_lr",
              "display_large_incurred_lr",
              "display_large_chainladder_lr",
              "display_large_approach",
              "display_large_selected_lr",
              "display_cat_incurred_lr",
              "display_cat_chainladder_lr",
              "display_cat_approach",
              "display_cat_selected_lr",
              "display_show_row_inputs",
              "display_show_row_rating"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
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