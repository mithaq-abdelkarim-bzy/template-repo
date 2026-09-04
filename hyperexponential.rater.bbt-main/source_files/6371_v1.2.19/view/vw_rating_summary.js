//########### OUTSTANDING ########################
// Needs a shownby criteria 


import * as HX from "hx-model-components";
import TwoAxisLineChart from "components/line";
import ScatterBestFit from "components/scatter_with_best_fit";
import CompoundBar from "components/compound_bar_graph";
import LineBar from "components/combined_bar_line";
import Bar from "components/bar";
import Waterfall from "components/waterfall";
import Line from "components/working_line";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} viewScale={0.7} shownBy="cds/model_state/show_after_landing_page">


      <HX.Section title="Inputs" shownBy="/cds/show_hide/node/not_new_to_market">

        <HX.Pane flow="right">

          <HX.Table
            title="Data"
            data={[{ datum: "detail_by_year", elementLabelBy: "display_yoa" }]}
            fields={[{ field: "policy_length_calc", maxWidth: 140 }
              , { field: "policy_length_override", maxWidth: 140 }
              , null
              , { field: "include_suggested", maxWidth: 140 }
              , { field: "include_override", maxWidth: 140 }
              , null
              , { field: "premium_suggested", maxWidth: 140 }
              , { field: "premium_override", maxWidth: 140 }
              , null
              , { field: "incurred_suggested", maxWidth: 140 }
              , { field: "incurred_override", maxWidth: 140 }
              , null
              , { field: "incurred_large_suggested", maxWidth: 140 }
              , { field: "incurred_large_override", maxWidth: 140 }
              , null
              , { field: "incurred_cat_suggested", maxWidth: 140 }
              , { field: "incurred_cat_override", maxWidth: 140 }
              , null
              , { field: "incurred_att_suggested", maxWidth: 140 }
              , { field: "incurred_att_override", maxWidth: 140 }
            ]}
            with="cds/rating_summary"
            filter="display_show_row_inputs"
            kb-interactive
          />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Table
            title="Assumptions"
            data={[{ datum: "detail_by_year", elementLabelBy: "display_yoa" }]}
            fields={[{ field: "port_chg_suggested", maxWidth: 140 }
              , { field: "port_chg_override", maxWidth: 140 }
              , null
              , { field: "rate_chg_suggested", maxWidth: 140 }
              , { field: "rate_chg_override", maxWidth: 140 }
              , null
              , { field: "infl_chg_suggested", maxWidth: 140 }
              , { field: "infl_chg_override", maxWidth: 140 }
              , null
              , { field: "interp_blended_selected_perc_ult", maxWidth: 140 }
              , { field: "large_threshold_sett_fx", maxWidth: 140 }

            ]}
            with="cds/rating_summary"
            //filter="display_show_row_inputs" // need to see current year as well
            kb-interactive
          />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Collection fields={["cds/triangle_projection/benchmark_use_occurrence"]} shownBy="/cds/show_hide/node/not_new_to_market" />
          <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
          <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
          <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
        </HX.Pane>

      </HX.Section>


      <HX.Section title="Loss Ratio Summary">

        <HX.Pane flow="right">

          <HX.Pane flow="down">
            <HX.Collection
              title="Attritional Adjustments"
              fields={["cds/rating_summary/summary_ratios/attritional/uw_adjustment"
                , "cds/rating_summary/summary_ratios/attritional/gg_pst_uw_adj/ulr_uw_override"
              ]}
              syncColumnWidthsKey="att"

            />
            <HX.Collection
              fields={["cds/rating_summary/summary_ratios/attritional/uw_rationale"]}
              shownBy="cds/show_hide/node/rs_att_rationale"
            />
          </HX.Pane>

          <HX.Pane flow="down">
            <HX.Collection
              title="Large Adjustments"
              fields={["cds/rating_summary/summary_ratios/large/uw_adjustment"
                , "cds/rating_summary/summary_ratios/large/uw_override"
              ]}
              syncColumnWidthsKey="large"

            />
            <HX.Collection
              fields={["cds/rating_summary/summary_ratios/large/uw_rationale"]}
              shownBy="cds/show_hide/node/rs_lrg_rationale"
            />
          </HX.Pane>

          <HX.Pane flow="down">
            <HX.Collection
              title="Catastrophe Adjustments"
              fields={["cds/rating_summary/summary_ratios/catastrophe/uw_adjustment"
                , "cds/rating_summary/summary_ratios/catastrophe/uw_override"
              ]}
              syncColumnWidthsKey="cat"

            />
            <HX.Collection
              fields={["cds/rating_summary/summary_ratios/catastrophe/uw_rationale"]}
              shownBy="cds/show_hide/node/rs_cat_rationale"
            />
          </HX.Pane>


        </HX.Pane>


        <HX.Pane flow="right">

          <HX.Table
            title="Attritional Loss Ratio Analysis"
            data={[
              null
              , { datum: "gg_pre_uw_adj", maxWidth: 140 }
              , { datum: "gn_pre_uw_adj", maxWidth: 140 }
              , { datum: "gg_pst_uw_adj", maxWidth: 140 }
              , { datum: "gn_pst_uw_adj", maxWidth: 140 }
            ]}
            fields={[
              "ulr_initial_benchmark"
              , "ulr_initial_experience"
              , "ulr_initial_experience_weighting"
              , "ulr_initial_selected"
              , "ulr_selected_ol"
              , "ulr_uw_override"
              , "ulr_final_uw"
              , "ulr_actuarial_override_output"
              , "ulr_final"
            ]}
            with="cds/rating_summary/summary_ratios/attritional"
            transpose
            syncColumnWidthsKey="att"

          />

          <HX.Table
            title="Large Loss Ratio Analysis"
            data={[
              null
              , { datum: "gg_pre_uw_adj", maxWidth: 140 }
              , { datum: "gn_pre_uw_adj", maxWidth: 140 }
              , { datum: "gg_pst_uw_adj", maxWidth: 140 }
              , { datum: "gn_pst_uw_adj", maxWidth: 140 }
            ]}
            fields={[
              "ulr_benchmark"
              , "ulr_experience"
              , "ulr_experience_weighting"
              , "ulr_selected_ol"
              , "ulr_uw_override"
              , "ulr_final_uw"
              , "ulr_actuarial_override_output"
              , "ulr_final"
            ]}
            with="cds/rating_summary/summary_ratios/large"
            transpose
            syncColumnWidthsKey="large"

          />

          <HX.Table
            title="Catastrophe Loss Ratio Analysis"
            data={[
              null
              , { datum: "gg_pre_uw_adj", maxWidth: 140 }
              , { datum: "gn_pre_uw_adj", maxWidth: 140 }
              , { datum: "gg_pst_uw_adj", maxWidth: 140 }
              , { datum: "gn_pst_uw_adj", maxWidth: 140 }
            ]}
            fields={[
              { field: "ulr_rms", shownBy: "/cds/show_hide/node/loss_ratio_rms" }
              , { field: "ulr_benchmark", shownBy: "/cds/show_hide/node/loss_ratio_benchmark" }
              , "ulr_experience"
              , "ulr_experience_weighting"
              , "ulr_selected_ol_exc_nml"
              , "ulr_selected_ol"
              , "ulr_uw_override"
              , "ulr_final_uw"
              , "ulr_actuarial_override_output"
              , "ulr_final"
            ]}
            with="cds/rating_summary/summary_ratios/catastrophe"
            transpose
            syncColumnWidthsKey="cat"
          />

        </HX.Pane>

      </HX.Section>


      <HX.Section title="Loss Ratio Charts" shownBy="/cds/show_hide/node/not_new_to_market">
        <HX.Pane flow="right">
          <HX.Collection fields={["chart_basis"]} with="cds/rating_summary" horizontal />
          <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
          <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
          <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
        </HX.Pane>



        <HX.Pane flow="right" shownBy="cds/rating_summary/chart_show_basis_gg" >
          <LineBar
            title="GG Att. ILR"
            data={[
              { list: "cds/rating_summary/detail_by_year", labelBy: "yoa" }
            ]}
            traces={[
              { field: "chart_att_ilr_gg", label: "Att. ILR", color: "#2A3178" },
              { field: "chart_att_ilr_ol_gg", label: "Att. ILR on-level", color: "#CA3397" }, //Isn't the correct data but can just be easily replaced by correct 'on-level' series
            ]}
            series={[
              {
                seriesLabel: "Att. Proposed",
                seriesColor: "#4FADC7",
                seriesLineType: 'dash',
                seriesMode: 'lines',
                points: [
                  {
                    list: "cds/rating_summary/detail_by_year",
                    x: "yoa",
                    y: "chart_att_ilr_proposed_gg", //Also wrong data, just replace with path to correct 'proposed'
                  },
                ],
              },
            ]}
            xAxisTickAngle={-45}
            xAxisLabel="Year"
            yAxisLabel="GG ILR"
            barMode="group"
            gapBetweenBarsSize={0.4}
            width={600}
            height={500}
            y2SeparateAxis={false}
          />
          <LineBar
            title="GG Large ILR"
            data={[
              { list: "cds/rating_summary/detail_by_year", labelBy: "yoa" }
            ]}
            traces={[
              { field: "chart_large_ilr_gg", label: "Large ILR", color: "#2A3178" },
              { field: "chart_large_ilr_ol_gg", label: "Large ILR on-level", color: "#CA3397" }, //Isn't the correct data but can just be easily replaced by correct 'on-level' series
            ]}
            series={[
              {
                seriesLabel: "Large Proposed",
                seriesColor: "#4FADC7",
                seriesLineType: 'dash',
                seriesMode: 'lines',
                points: [
                  {
                    list: "cds/rating_summary/detail_by_year",
                    x: "yoa",
                    y: "chart_large_ilr_proposed_gg", //Also wrong data, just replace with path to correct 'proposed'
                  },
                ],
              },
            ]}
            xAxisTickAngle={-45}
            xAxisLabel="Year"
            yAxisLabel="GG ILR"
            barMode="group"
            gapBetweenBarsSize={0.4}
            width={600}
            height={500}
            y2SeparateAxis={false}
          />
          <LineBar
            title="GG CAT ILR"
            data={[
              { list: "cds/rating_summary/detail_by_year", labelBy: "yoa" }
            ]}
            traces={[
              { field: "chart_cat_ilr_gg", label: "Cat ILR", color: "#2A3178" },
              { field: "chart_cat_ilr_ol_gg", label: "Cat ILR on-level", color: "#CA3397" }, //Isn't the correct data but can just be easily replaced by correct 'on-level' series
            ]}
            series={[
              {
                seriesLabel: "Cat Proposed",
                seriesColor: "#4FADC7",
                seriesLineType: 'dash',
                seriesMode: 'lines',
                points: [
                  {
                    list: "cds/rating_summary/detail_by_year",
                    x: "yoa",
                    y: "chart_cat_ilr_proposed_gg", //Also wrong data, just replace with path to correct 'proposed'
                  },
                ],
              },
            ]}
            xAxisTickAngle={-45}
            xAxisLabel="Year"
            yAxisLabel="GG ILR"
            barMode="group"
            gapBetweenBarsSize={0.4}
            width={600}
            height={500}
            y2SeparateAxis={false}
          />
        </HX.Pane>


        <HX.Pane flow="right" shownBy="cds/rating_summary/chart_show_basis_gn" >
          <LineBar
            title="GN Att. ILR"
            data={[
              { list: "cds/rating_summary/detail_by_year", labelBy: "yoa" }
            ]}
            traces={[
              { field: "chart_att_ilr_gn", label: "Att. ILR", color: "#2A3178" },
              { field: "chart_att_ilr_ol_gn", label: "Att. ILR on-level", color: "#CA3397" }, //Isn't the correct data but can just be easily replaced by correct 'on-level' series
            ]}
            series={[
              {
                seriesLabel: "Att. Proposed",
                seriesColor: "#4FADC7",
                seriesLineType: 'dash',
                seriesMode: 'lines',
                points: [
                  {
                    list: "cds/rating_summary/detail_by_year",
                    x: "yoa",
                    y: "chart_att_ilr_proposed_gn", //Also wrong data, just replace with path to correct 'proposed'
                  },
                ],
              },
            ]}
            xAxisTickAngle={-45}
            xAxisLabel="Year"
            yAxisLabel="GN ILR"
            barMode="group"
            gapBetweenBarsSize={0.4}
            width={800}
            height={500}
            y2SeparateAxis={false}
          />

          <LineBar
            title="GN Large ILR"
            data={[
              { list: "cds/rating_summary/detail_by_year", labelBy: "yoa" }
            ]}
            traces={[
              { field: "chart_large_ilr_gn", label: "Large ILR", color: "#2A3178" },
              { field: "chart_large_ilr_ol_gn", label: "Large ILR on-level", color: "#CA3397" }, //Isn't the correct data but can just be easily replaced by correct 'on-level' series
            ]}
            series={[
              {
                seriesLabel: "Large Proposed",
                seriesColor: "#4FADC7",
                seriesLineType: 'dash',
                seriesMode: 'lines',
                points: [
                  {
                    list: "cds/rating_summary/detail_by_year",
                    x: "yoa",
                    y: "chart_large_ilr_proposed_gn", //Also wrong data, just replace with path to correct 'proposed'
                  },
                ],
              },
            ]}
            xAxisTickAngle={-45}
            xAxisLabel="Year"
            yAxisLabel="GN ILR"
            barMode="group"
            gapBetweenBarsSize={0.4}
            width={800}
            height={500}
            y2SeparateAxis={false}
          />

          <LineBar
            title="GN CAT ILR"
            data={[
              { list: "cds/rating_summary/detail_by_year", labelBy: "yoa" }
            ]}
            traces={[
              { field: "chart_cat_ilr_gn", label: "Cat ILR", color: "#2A3178" },
              { field: "chart_cat_ilr_ol_gn", label: "Cat ILR on-level", color: "#CA3397" }, //Isn't the correct data but can just be easily replaced by correct 'on-level' series
            ]}
            series={[
              {
                seriesLabel: "Cat Proposed",
                seriesColor: "#4FADC7",
                seriesLineType: 'dash',
                seriesMode: 'lines',
                points: [
                  {
                    list: "cds/rating_summary/detail_by_year",
                    x: "yoa",
                    y: "chart_cat_ilr_proposed_gn", //Also wrong data, just replace with path to correct 'proposed'
                  },
                ],
              },
            ]}
            xAxisTickAngle={-45}
            xAxisLabel="Year"
            yAxisLabel="GN ILR"
            barMode="group"
            gapBetweenBarsSize={0.4}
            width={800}
            height={500}
            y2SeparateAxis={false}
          />
        </HX.Pane>
      </HX.Section>



      <HX.Section title="Loss Ratio Development" defaultCollapsed={true} shownBy="/cds/show_hide/node/not_new_to_market">

        <HX.Pane flow="right">

          <HX.Table
            title="Attritional On-level GG Loss Ratio Progression"
            data={[{ datum: "detail_by_year", elementLabelBy: "display_yoa" }]}
            fields={[
              null
              , { field: "display_attritional_incurred_lr", maxWidth: 140 }
              , { field: "display_attritional_chainladder_lr", maxWidth: 140 }
              , { field: "display_attritional_approach", maxWidth: 140 }
              , { field: "display_attritional_selected_lr", maxWidth: 140 }
            ]}
            with="cds/rating_summary"
            filter="display_show_row_rating"
            syncColumnWidthsKey="att"
          />

          <HX.Table
            title="Large On-level GG Loss Ratio Progression"
            data={[{ datum: "detail_by_year", elementLabelBy: "display_yoa" }]}
            fields={[
              null
              , { field: "display_large_incurred_lr", maxWidth: 140 }
              , { field: "display_large_chainladder_lr", maxWidth: 140 }
              , { field: "display_large_approach", maxWidth: 140 }
              , { field: "display_large_selected_lr", maxWidth: 140 }
            ]}
            with="cds/rating_summary"
            filter="display_show_row_rating"
            syncColumnWidthsKey="large"
          />

          <HX.Table
            title="Catastrophe On-level GG Loss Ratio Progression"
            data={[{ datum: "detail_by_year", elementLabelBy: "display_yoa" }]}
            fields={[
              null
              , { field: "display_cat_incurred_lr", maxWidth: 140 }
              , { field: "display_cat_chainladder_lr", maxWidth: 140 }
              , { field: "display_cat_approach", maxWidth: 140 }
              , { field: "display_cat_selected_lr", maxWidth: 140 }
            ]}
            with="cds/rating_summary"
            filter="display_show_row_rating"
            syncColumnWidthsKey="cat"
          />

        </HX.Pane>

      </HX.Section>



      <HX.Section title="Profit Commission">
        <HX.Pane flow="down">
          <HX.Table
            title="Profit Commission Summary"
            data={[
              null
              , { datum: "technical", maxWidth: 140 }
            ]}
            fields={[
              "percent_pc"
              , null
              , "amount_pc_100"
              , "amount_pc_afb"
              , null
              , "percent_pc_prior"

            ]}
            with="cds/rating_summary"
            transpose
            syncColumnWidthsKey="pc_summary"
          />


          <HX.Pane flow="right">
            <HX.Collection fields={["cds/profit_commission/consistent_pc_latest_param"]} />
            <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
            <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
            <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
          </HX.Pane>


          <HX.Pane flow="right">
            <HX.Button task="simulate_pc_task" title="Calculate Profit Commission" />
            <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
            <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
            <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
          </HX.Pane>


        </HX.Pane>
      </HX.Section>

      <HX.Section title="Loss Ratio Summary">
        <HX.Pane flow="down">
          <HX.Table
            title="Loss Ratio Summary"
            data={[
              null
              , { datum: "gg_pre_uw_adj", maxWidth: 140 }
              , { datum: "gg_pst_uw_adj", maxWidth: 140 }
            ]}
            fields={["ulr_priced_final"]}
            with="cds/rating_summary/summary_ratios/total"
            transpose
            syncColumnWidthsKey="lr_summary"
          />

          <HX.Table
            data={[
              null
              , { datum: "gn_pre_uw_adj", maxWidth: 140 }
              , { datum: "gn_pst_uw_adj", maxWidth: 140 }
            ]}
            fields={[
              "ulr_bench"
              , "ulr_plan"
              , null
              , "ulr_priced_final_exc_pc"
              , "ulr_priced_final_inc_pc"
              , null
              , "ulr_prior"

            ]}
            with="cds/rating_summary/summary_ratios/total"
            transpose
            syncColumnWidthsKey="lr_summary"
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="KPI Summary and Exhibits">

        <HX.Pane flow="right">
          <HX.Pane flow="down" stretch>
            <HX.Table
              title="KPI Summary"
              data={[
                null
                , { datum: "pre_uw_adj", maxWidth: 140 }
                , { datum: "pst_uw_adj", maxWidth: 140 }
              ]}
              fields={[
                "expected_profit"
                , "allocated_capital"
                , "roc"
                , null
                , "bpi"
                , "tpi"
                , null
                , "bpi_prior"
                , "tpi_prior"
              ]}
              with="cds/rating_summary/kpi"
              transpose
              syncColumnWidthsKey="lr_summary"
            />


            <HX.With context={{
              "index": 0,
              "path": "cds/layers",
              "type": "list"
            }}>
              <HX.Pane flow="right" >
                <HX.Collection fields={["rate_change/rate_change/uw_selected"]} title="Rate Change" />
                <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
              </HX.Pane>
            </HX.With>

            <HX.Pane flow="right" >
              <HX.Collection fields={["cds/rating_summary/chart_premium_breakdown/uw_adj_basis"]} title="Chart Settings" />
              <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
            </HX.Pane>


            <HX.Pane flow="right">
              <HX.Collection fields={["cds/rating_summary/chart_premium_breakdown/premium_basis"]} />
              <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
            </HX.Pane>

          </HX.Pane>


          <CompoundBar
            title="Premium Breakdown"
            data={[

              { structure: "cds/rating_summary/chart_premium_breakdown/technical", label: "Technical" },
              { structure: "cds/rating_summary/chart_premium_breakdown/benchmark", label: "Benchmark" },
              { structure: "cds/rating_summary/chart_premium_breakdown/client", label: "Client" },
            ]}
            traces={[
              { field: "client_premium", label: "Client Premium", color: "#F7CFEC" },
              { field: "losses", label: "Losses", color: "#6C0D7A" },
              { field: "reinsurance", label: "Reinsurance", color: "#0C6122" },
              { field: "cost_of_capital", label: "Cost of Capital", color: "#4FADC7" },
              { field: "expense", label: "Expense", color: "#0DB0E0" },
              { field: "bp_loading", label: "BP Loading", color: "#1E4671" },
              { field: "brokerage", label: "Brokerage", color: "#F47211" },

            ]}
            xAxisTickAngle={-0}
            gapBetweenBarsSize={0.05}
            xAxisLabel="Section"
            yAxisLabel="Amount"
            barMode="relative"
            tpiLabelString="cds/rating_summary/chart_premium_breakdown/technical/metric_string"
            bpiLabelString="cds/rating_summary/chart_premium_breakdown/benchmark/metric_string"
            dynamicTitle="cds/rating_summary/chart_premium_breakdown/title_string"
          />





          <Bar
            title="ILR BY CLAIM TYPE & YOA"
            data={[
              { list: "cds/rating_summary/detail_by_year", labelBy: "yoa" }
            ]}
            traces={[
              { field: "chart_att_ilr", label: "Attrition", color: "#4FADC7" },
              { field: "chart_large_ilr", label: "Large", color: "#E8A4D5" },
              { field: "chart_cat_ilr", label: "Cat", color: "#CA3397" },
            ]}

            xAxisTickAngle={-45}
            xAxisLabel="Year"
            yAxisLabel="GG ILR"
            barMode="stack" //or set to "overlay" if you want all bars to start from 0
            gapBetweenBarsSize={0.4}
          />

          <LineBar
            title="TOTAL LR SUMMARY BY YOA"
            data={[
              { list: "cds/rating_summary/detail_by_year", labelBy: "yoa" }
            ]}
            traces={[
              { field: "chart_premium", label: "GGWP", color: "#E8A4D5" },]}
            series={[
              {
                seriesLabel: "GG Pricing LR %",
                seriesColor: "#CA3397",
                seriesLineType: 'dash',
                points: [
                  {
                    list: "cds/rating_summary/detail_by_year",
                    x: "yoa",
                    y: "chart_pricing_lr", //Also wrong data, just replace with path to correct 'GG pricing LR %'
                  },
                ],
              },
              {
                seriesLabel: "GG Exp LR %",
                seriesColor: "#4FADC7",
                seriesMode: 'lines',
                points: [
                  {
                    list: "cds/rating_summary/detail_by_year",
                    x: "yoa",
                    y: "chart_experience_lr", //Also wrong data, just replace with path to correct 'GG exp LR %'
                  },
                ],
              },
            ]}
            xAxisTickAngle={-45}
            yAxis2Label="GG ILR"
            yAxisLabel="GGWP"
            xAxisLabel='Year'
            barMode="group"
            gapBetweenBarsSize={0.4}
            width={800}
            height={500}
            y2SeparateAxis={true}
          />



        </HX.Pane>
      </HX.Section>




      <HX.Section title="Premium Summary" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Pane flow="down" stretch>
            <HX.Table
              title="Premium Summary"
              data={[
                null
                , { datum: "technical", maxWidth: 140 }
              ]}
              fields={[
                "gn_premium_quoted_inc_pc_afb"
                , "gn_premium_quoted_exc_pc_afb"
                , "gg_premium_quoted_afb"
              ]}
              with="cds/rating_summary"
              transpose
              syncColumnWidthsKey="pc_summary"
            />



            <HX.Table

              data={[
                null
                , { datum: "amts_pre_uw_adj", maxWidth: 140 }
                , { datum: "amts_pst_uw_adj", maxWidth: 140 }
              ]}
              fields={[
                "gn_premium_tech_inc_pc_afb"
                , "gg_premium_tech_afb"
                , null
                , "gn_premium_bench_inc_pc_afb"
                , "gg_premium_bench_afb"
              ]}
              with="cds/rating_summary/technical"
              transpose
              syncColumnWidthsKey="pc_summary"
            />
          </HX.Pane>

          <HX.Pane flow="down" stretch >

            <HX.Table
              title="Technical Premium Derivation"
              data={[
                null
                , { datum: "amts_pre_uw_adj", maxWidth: 140 }
                , { datum: "amts_pst_uw_adj", maxWidth: 140 }
              ]}
              fields={[
                "losses_tot_afb"
                , null
                , "expense_afb"
                , "investment_afb"
                , "profit_req_afb"
                , null
                , "gn_premium_tech_inc_pc_afb"
                , null
                , "aqn_comm_afb"
                , "aqn_brok_afb"
                , "aqn_iptax_afb"
                , "aqn_pc_afb"
                , null
                , "gg_premium_tech_afb"
              ]}
              with="cds/rating_summary/technical"
              transpose
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>






    </HX.Page >
  )
}

export { vw_rating_summary };
