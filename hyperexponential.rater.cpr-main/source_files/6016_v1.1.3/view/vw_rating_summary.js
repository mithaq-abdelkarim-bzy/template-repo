import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} shownBy="cds/show_hide/page/show_rating_summary">


      <HX.Section title="Summary @ Share & Policy Period">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line",
            ]}
          />
        </HX.With>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_rater_priced">
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              "quoted_premium",
              "model_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj",
              "benchmark_premium",
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "tpi",
              "pflr",
              "bpi",
              // { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
              "tpi_pre_uw_adj",
              "pflr_pre_uw_adj",
              "bpi_pre_uw_adj",

            ]}
          />
          <HX.Collection
            title="Other Metrics"
            numCols={2}
            fields={[
              "roc",
              "uw_adj_impact",
            ]}
          />
          {/*NOTE: below for case pricing only */}
        </HX.With>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_case_priced">
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              "quoted_premium",
              "bpi_case_priced",
              "technical_premium",
              "benchmark_premium",
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "tpi",
              "pflr",
              "roc",
            ]}
          />
        </HX.With>
      </HX.Section>



      <HX.Section title="Summary Metrics @100% & Annual - Political Risks" shownBy="/cds/show_hide/node/show_political">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right" reflow={false}>
            <HX.Table
              title="Rate-on-Line & Kpis"
              data={[
                null
                , { datum: "metrics_summary_pre_uwadj", maxWidth: 140 }
                , { datum: "metrics_summary_pst_uwadj", maxWidth: 140 }
              ]}
              fields={[
                "rol_offered"
                , "rol_model"
                , "rol_technical"
                , "rol_benchmark"
                , null
                , "bpi"
                , "tpi"
                , "priced_to_plan"
                , "priced_gglr"
                , "priced_gnlr"
              ]}
              with="political"
              transpose
              removeHorizontalScroll
            />

            <HX.Table
              title="Premium Analysis by Peril - AFTER Underwriter Adjustment"
              data={[
                null
                , { datum: "total", maxWidth: 140 }
                , null
                , { datum: "gov_action", maxWidth: 140 }
                , { datum: "pol_violence", maxWidth: 140 }
                , { datum: "cur_inconvertibility", maxWidth: 140 }
                , { datum: "cont_relation_govt", maxWidth: 140 }
              ]}
              fields={[
                "premium_bound"
                , "premium_benchmark"
                , "premium_model"
                , null
                , "premium_technical"
                , "expected_loss"
                , "che"
                , "fixed_expenses"
                , "variable_expenses"
                , "investment_income"
                , "cost_of_reinsurance"
                , "capital"
                , "brokerage"
              ]}
              with="political/premium_composition_pst_uwadj"
              transpose
              removeHorizontalScroll
            />


            <HX.Table
              title="Premium Analysis by Peril - BEFORE Underwriter Adjustment"
              data={[
                null
                , { datum: "total", maxWidth: 140 }
                , null
                , { datum: "gov_action", maxWidth: 140 }
                , { datum: "pol_violence", maxWidth: 140 }
                , { datum: "cur_inconvertibility", maxWidth: 140 }
                , { datum: "cont_relation_govt", maxWidth: 140 }

              ]}
              fields={[
                "premium_bound"
                , "premium_benchmark"
                , "premium_model"
                , null
                , "premium_technical"
                , "expected_loss"
                , "che"
                , "fixed_expenses"
                , "variable_expenses"
                , "investment_income"
                , "cost_of_reinsurance"
                , "capital"
                , "brokerage"
              ]}
              with="political/premium_composition_pre_uwadj"
              transpose
              removeHorizontalScroll
            />


          </HX.Pane>
        </HX.With>
      </HX.Section>






      <HX.Section title="Summary Metrics @100% - CRCF" shownBy="/cds/show_hide/node/show_crcf">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right" reflow={false}>
            <HX.Table
              title="Rate-on-Exposure & KPI's"
              data={[
                null
                , { datum: "metrics_summary_pre_uwadj_annual", maxWidth: 140 }
                , { datum: "metrics_summary_pre_uwadj_term", maxWidth: 140 }
                , null
                , { datum: "metrics_summary_pst_uwadj_annual", maxWidth: 140 }
                , { datum: "metrics_summary_pst_uwadj_term", maxWidth: 140 }]}
              fields={[
                "roe_offered"
                , "roe_plan"
                , "roe_technical"
                , "roe_benchmark"
                , null
                , "bpi"
                , "tpi"
                , "priced_to_plan"
                , "priced_gglr"
                , "priced_gnlr"
                , "lgd_bound"
                , "credit_rating_bound"
              ]}
              with="crcf"
              transpose
              removeHorizontalScroll
            />


            <HX.Table
              title="Loss Composition"
              data={[
                null
                , { datum: "loss_composition_pre_uwadj_term", maxWidth: 140 }
                , { datum: "loss_composition_pst_uwadj_term", maxWidth: 140 }]}
              fields={[
                "exposure"
                , "credit_rating"
                , "pod"
                , "tenor_load"
                , "lgd"
                , "recovery_discounted"
                , "limit_discount"
                , "term"
                , "other"
                , "expected_loss"
              ]}
              with="crcf"
              transpose
              removeHorizontalScroll
            />


            <HX.Table
              title="Premium Analysis"
              data={[
                null
                , { datum: "premium_composition_pre_uwadj_annual", maxWidth: 140 }
                , { datum: "premium_composition_pre_uwadj_term", maxWidth: 140 }
                , null
                , { datum: "premium_composition_pst_uwadj_annual", maxWidth: 140 }
                , { datum: "premium_composition_pst_uwadj_term", maxWidth: 140 }
              ]}
              fields={[
                "premium_bound"
                , "premium_benchmark"
                , "premium_plan"
                , null
                , "premium_technical"
                , "expected_loss"
                , "che"
                , "fixed_expenses"
                , "variable_expenses"
                , "investment_income"
                , "cost_of_reinsurance"
                , "capital"
                , "brokerage"
              ]}
              with="crcf"
              transpose
              removeHorizontalScroll
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>




    </HX.Page >

  )
}


export { vw_rating_summary };