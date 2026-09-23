import * as HX from "hx-model-components";
import Bar from "components/bar";
import CombinationChart from "components/combination";

function vw_experience_rating(scale) {
  return (
    <HX.Page title="Experience Rating" fullWidth={true} viewScale={0.90} shownBy="cds/show_page/show_other">
      <HX.Section title="Data Source and Experience Rate Summary">
        <HX.Pane flow="right">
          <HX.Pane >
            <HX.Pane flow="right">
              <HX.Table
                data={["cds/experience_rating"]}
                fields={["data_source", null, "policy_ref", "expiring_policy_ref"]}
                transpose
                kb-interactive
              />
              <HX.Pane >
                <HX.Button task="bi_intelligence_fetch_task" title="Populate Experience from BI" shownBy="cds/bi_masking" />
                <HX.Collection shownBy="cds/bi_masking"
                  fields={["cds/fetch_bi_task_status_policy", "cds/fetch_bi_task_status_claims"]}
                />
                <HX.Collection shownBy="cds/manual_masking"
                  fields={[null]}
                />
              </HX.Pane >
            </HX.Pane >
            <HX.Table
              data={["cds/experience_final_selections_model", "cds/experience_final_selections_uw"]}
              fields={["gn_ulr", "gn_ulr_expiry", "exp_weight"]}
              transpose
              kb-interactive
            />
          </HX.Pane >
          <HX.Table
            data={["cds/experience_lr_summary_list", null, "cds/experience_lr_summary_subtotal_1", "cds/experience_lr_summary_subtotal_2"]}
            fields={["yoa", "gnwp", "ilr", "ulr", "ulr_inf"]}
            kb-interactive
            title="Experience Summary"
          />
        </HX.Pane >
      </HX.Section >
      <HX.Section title="Experience Rate Calculations - BI" shownBy="cds/bi_masking">
        <HX.Pane flow="right">
          <HX.Table
            data={["cds/experience_attr_projection"]}
            fields={["yoa", "incurred", "dev_factor", "ielr", "ultimate"]}
            title="Attritional Claims Projection"
            kb-interactive
          />
          <HX.Table
            data={["cds/experience_large_projection"]}
            fields={["ll_avg_lr", "ll_assumption", "ll_weighted", "ultimate"]}
            title="Large Claims Projection"
            kb-interactive
          />
          <HX.Table
            data={["cds/experience_cat_projection"]}
            fields={["cat_incurred", "cat_average", "cat_rms", "ultimate"]}
            title="Cat Claims Projection"
            kb-interactive
          />
          <HX.Table
            data={["cds/experience_ult_claims"]}
            fields={["ult_incurred", "inf_index", "ult_incurred_inf", "ulr", "include"]}
            title="Ultimate Claims"
            kb-interactive
          />
        </HX.Pane >
        <HX.Pane flow="right">
          <HX.Collection
            fields={[null]}
          />
          {/* # SA: You can just use an empty pane <HX.Pane /> to space things out! 
                    (note the above is equivalent to <HX.Pane></HX.Pane>, it's just 
                    using "self-closing" to combine it into one block for readability )*/}
          <HX.Collection
            fields={[null]}
          />
          <HX.Table
            data={["cds/experience_rms_defaults"]}
            fields={["rms_cat_el", "rms_cat_prem", "rms_cat_lr"]}
          />
          <HX.Collection
            fields={[null]}
          />
        </HX.Pane>
        <HX.Pane flow="right">
          {/* <HX.Table
            data={["experience_gnwp_summary"]}
            fields={["yoa", "gnwp", "rate_change", "rate_change_index", "gnwp_onlvl"]}
            title="Premium Summary"
          /> */}
          {/* <HX.Table
            data={["experience_ult_claims"]}
            fields={["yoa", "ult_incurred", "inf_index", "ult_incurred_inf", "include"]}
            title="Ultimate Claims"
          /> */}
          {/* <HX.Table
            data={["experience_lr_summaries"]}
            fields={["yoa", "ilr", "ulr"]}
            title="Loss Ratio Summaries (GN)"
          /> */}
        </HX.Pane >
      </HX.Section >
      <HX.Section title="Experience Rate Calculations - Manual" shownBy="cds/manual_masking">
        <HX.Pane flow="right">
          <HX.Table
            data={["cds/experience_gnwp_summary_manual"]}
            fields={["yoa", "gnwp", "rate_change", "gnwp_onlvl"]}
            title="Premium Summary"
            kb-interactive
          />
          <HX.Table
            data={["cds/experience_attr_projection_manual"]}
            fields={["total_incurred", "large_cat", "incurred", "ultimate"]}
            title="Attritional Claims Projection"
            kb-interactive
          />
          <HX.Table
            data={["cds/experience_large_projection_manual"]}
            fields={["ll_assumption", "ll_uw_view", "ll_selected", "ultimate"]}
            title="Large Claims Projection"
            kb-interactive
          />
          <HX.Table
            data={["cds/experience_cat_projection_manual"]}
            fields={["cat_uw_view", "cat_bp", "cat_rms", "ultimate"]}
            title="Cat Claims Projection"
            kb-interactive
          />
          <HX.Table
            data={["cds/experience_ult_claims_manual"]}
            fields={["ult_incurred", "inf_index", "ult_incurred_inf", "ulr", "include"]}
            title="Ultimate Claims"
            kb-interactive
          />
        </HX.Pane >
        <HX.Pane flow="right">
          <HX.Collection
            fields={[null]}
          />
          <HX.Collection
            fields={[null]}
          />
          <HX.Collection
            fields={[null]}
          />
          <HX.Table
            data={["cds/experience_rms_defaults"]}
            fields={["rms_cat_el", "rms_cat_prem", "rms_cat_lr"]}
            kb-interactive
          />
          <HX.Collection
            fields={[null]}
          />
        </HX.Pane>
        <HX.Pane flow="right">
          {/* <HX.Table
            data={["experience_gnwp_summary_manual"]}
            fields={["yoa", "gnwp", "rate_change", "rate_change_index", "gnwp_onlvl"]}
            title="Premium Summary"
            kb-interactive
          /> */}
          {/* <HX.Table
            data={["experience_ult_claims_manual"]}
            fields={["yoa", "ult_incurred", "inf_index", "ult_incurred_inf", "include"]}
            title="Ultimate Claims"
          /> */}
          {/* <HX.Table
            data={["experience_lr_summaries_manual"]}
            fields={["yoa", "ilr", "ulr"]}
            title="Loss Ratio Summaries (GN)"
          /> */}
        </HX.Pane >
      </HX.Section >
      <HX.Section title="Detailed Claim Listing" shownBy="cds/bi_masking" defaultCollapsed>
        <HX.Pane flow="right">
          <HX.Table
            data={["cds/bi_claims_data"]}
            fields={["PolicyReference", "SectionReference", "ClaimReference", "TriFocusName", "PolicyYOA",
              "MarketCatCode", "MarketCat", "BeazleyShareTotalIncurredInUSD",
              "BeazleyShareTotalOutstandingInUSD", "SignedLineMultiplier", "TotalIncurredInUSD"]}
            kb-interactive
            dynamic
            maxListVisibleRows={15}
          />
        </HX.Pane >
      </HX.Section >
      <HX.Section title="GNWP and Loss Ratio Charts" defaultCollapsed>
        <HX.Pane flow="right">
          {/* <HX.Collection
            fields={[null]}
          /> */}
          {/* <HX.CategoryChart
            data={["experience_loss_ratio_summary_chart"]}
            fields={["gnwp", "ulr", "ilr", "sel_ulr", "uw_ulr"]}
            dataLabelField="yoa"
            columnType="cluster"
            title="GNWP and ULR"
            primaryAxis={{ label: "Premium" }}
            secondaryAxis={{ label: "ULR" }}
          />
          <HX.CategoryChart
            data={["experience_loss_ratio_type_chart"]}
            fields={["attr_lr", "large_lr", "cat_lr"]}
            dataLabelField="yoa"
            columnType="stack"
            title="Loss Ratio by Type"
            primaryAxis={{ label: "Loss Ratio" }}
          /> */}
          <CombinationChart
            title="GNWP and ULR"
            data={[{ list: "cds/experience_loss_ratio_summary_chart", labelBy: "yoa" }]}
            traces={[{ field: "gnwp", label: "Premium", color: "#DC199B" }]}
            series={[
              {
                seriesLabel: "ULR",
                color: "#4B0050",
                points: [
                  {
                    list: "cds/experience_loss_ratio_summary_chart",
                    x: "yoa",
                    y: "ulr",
                  },
                ],
              },
              {
                seriesLabel: "ILR",
                color: "#F56B00",
                points: [
                  {
                    list: "cds/experience_loss_ratio_summary_chart",
                    x: "yoa",
                    y: "ilr",
                  },
                ],
              },
              {
                seriesLabel: "Sel. ULR",
                color: "#3741A5",
                points: [
                  {
                    list: "cds/experience_loss_ratio_summary_chart",
                    x: "yoa",
                    y: "sel_ulr",
                  },
                ],
              },
              {
                seriesLabel: "UW ULR",
                color: "#00A7E2",
                points: [
                  {
                    list: "cds/experience_loss_ratio_summary_chart",
                    x: "yoa",
                    y: "uw_ulr",
                  },
                ],
              },
            ]}
            xAxisTickAngle={-45}
            gapBetweenBarsSize={0.05}
            // xAxisLabel=""
            yAxisLabel="Premium"
            yAxis2Label="ULR"
          />
          <Bar
            title="Loss Ratio by Type"
            data={[
              { list: "cds/experience_loss_ratio_type_chart", labelBy: "yoa" },
              { list: "cds/experience_loss_ratio_type_chart", labelBy: "yoa" },
              { list: "cds/experience_loss_ratio_type_chart", labelBy: "yoa" },
            ]}
            traces={[
              { field: "attr_ulr", label: "Attritional ULR", color: "#DC199B" },
              { field: "large_ulr", label: "Large ULR", color: "#4B0050" },
              { field: "cat_ulr", label: "Cat ULR", color: "#F56B00" },
            ]}
            xAxisTickAngle={-45}
            gapBetweenBarsSize={0.05}
            // xAxisLabel=""
            yAxisLabel="Loss Ratio"
            barMode="stack"
          />
          <HX.Collection
            fields={[null]}
          />
        </HX.Pane>
      </HX.Section >
      {/* <HX.Section title="Detailed" defaultCollapsed >
        <HX.Pane>
          <HX.Table
            data={["experience_detailed"]}
            fields={["trifocus", "bp_rc", "infl", "ll_threshold", "ll_load", "cat_load"]}
            kb-interactive
          />
        </HX.Pane>

      </HX.Section> */}
    </HX.Page >
  )
}

export { vw_experience_rating };