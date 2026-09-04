import * as HX from "hx-model-components";

function resultsTable(term = false, coverages = false, beforeUwAdj = false, plan = false, selectedTitle = "") {

  //Default State
  let selectedData = [null, "total"]

  let selectedFields = ["quoted_premium", "quoted_rol", "quoted_roe"
    , null, "technical_premium", "tpi"
    , null, "benchmark_premium", "bpi", "expected_loss_ratio"]

  // Updating selectedData based on term & coverages
  if (term === true) {
    if (coverages === true) {
      selectedData = [null, "total/policy_period"
        , null, "property/policy_period", "property/policy_period/bi", "property/policy_period/pd"
        , null, "liability/policy_period", "construction/policy_period"]
    }
    else {
      selectedData = [null, "total/policy_period"]
    }
  }
  else {
    if (coverages === true) {
      selectedData = [null, "total"
        , null, "property", "property/bi", "property/pd"
        , null, "liability", "construction"]
    }
  }

  // Updating selectedFields based on beforeUwAdj and plan
  if (beforeUwAdj === true & plan === true) {
    selectedFields = ["model_premium_pre_uw_adj", "model_rol_pre_uw_adj"
      , null, "technical_premium_pre_uw_adj", "tpi_pre_uw_adj"
      , null, "benchmark_premium_pre_uw_adj", "bpi_pre_uw_adj", "expected_loss_ratio_pre_uw_adj"]
  }
  if (beforeUwAdj === true & plan === false) {
    selectedFields = ["technical_premium_pre_uw_adj", "tpi_pre_uw_adj"
      , null, "benchmark_premium_pre_uw_adj", "bpi_pre_uw_adj", "expected_loss_ratio_pre_uw_adj"]
  }
  if (beforeUwAdj === false & plan === true) {
    selectedFields = ["model_premium", "model_rol", "minimum_premium", "minimum_rol"
      , null, "quoted_premium", "quoted_rol", "quoted_roe"
      , null, "technical_premium", "tpi"
      , null, "benchmark_premium", "bpi", "expected_loss_ratio"]
  }

  return (
    <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
      <HX.Table
        title={selectedTitle}
        with="coverages"
        data={selectedData}
        fields={selectedFields}
        transpose
        kb-interactive
        freezeLeft={0}
      />
    </HX.With>
  )
}


function vw_rating_summary(shownBy) {
  return (
    <HX.Page title="Rating Summary" shownBy={shownBy} viewScale={0.9} fullWidth>

      <HX.Section title="Overall Summary">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Collection
            title="Risk Details"
            numCols={3}
            fields={[
              "section_reference",
              "status",
              "/cds/currencies/source_currency",
              "brokerage",
              "written_line"
            ]}
          />
          <HX.Collection
            title="Priced Quotes"
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
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "bpi",
              "pflr",
              "uw_adj_impact",
              "tpi",
              "tpi_pre_uw_adj",
              "roc"
            ]}
          />
        </HX.With>



        {/*NOTE: below for case pricing only */}
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_case_priced">
          <HX.Collection
            title="Priced Quotes @ Term & Beazley Share"
            numCols={2}
            fields={[
              "quoted_premium_case_priced",
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

      {/*NOTE: section removed from view Feb 2026*/}
      {/* <HX.Section title="Underwriter Authorities">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Pane ratio={3}>
              <HX.Table
                with="uw_authorities_current_currency"
                data={[
                  { datum: "authority", labelBy: "/cds/authority_ccy_label" },
                  { datum: "policy", labelBy: "/cds/policy_ccy_label" },
                  "warning"
                ]}
                fields={[
                  "nb_gross_line",
                  "nb_net_premium",
                  "ren_gross_line",
                  "ren_net_premium",
                  "term"
                ]}
                title="Selected currency"
                dynamic={true}
                freezeLeft={0}
                kb-interactive
                transpose
              />
            </HX.Pane>
            <HX.Pane ratio={1} />
          </HX.Pane>
        </HX.With>

        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Pane ratio={3}>
              <HX.Table
                with="uw_authorities"
                data={["authority", "policy", "warning"]}
                fields={[
                  "nb_gross_line",
                  "nb_net_premium",
                  "ren_gross_line",
                  "ren_net_premium",
                  "term"
                ]}
                kb-interactive
                transpose
                removeHorizontalScroll
                title="USD always"
              />
            </HX.Pane>
            <HX.Pane ratio={1} />
          </HX.Pane>
        </HX.With>
      </HX.Section> */}

      <HX.Section defaultCollapsed title="Policy Period vs. Annual Summary" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Collection fields={["/model_state/show_rs_cvg", "/model_state/show_rs_before_uw_adj", "/model_state/show_rs_plan", null]} horizontal />
        <HX.Pane flow="right">
          <HX.Pane shownBy="model_state/show_rs_not_cvg_not_before_uw_adj">  {resultsTable(true, false, false, true, "Term Summary - after UW Adj- No Coverage Detail")}   </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_not_cvg_not_before_uw_adj">  {resultsTable(false, false, false, true, "Annual Summary - after UW Adj - No Coverage Detail")} </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_yes_cvg_not_before_uw_adj">  {resultsTable(true, true, false, true, "Term Summary - after UW Adj - Coverage Detail")}      </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_yes_cvg_not_before_uw_adj">  {resultsTable(false, true, false, true, "Annual Summary - after UW Adj - Coverage Detail")}    </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Pane shownBy="model_state/show_rs_not_cvg_yes_before_uw_adj">  {resultsTable(true, false, true, true, "Term Summary - before UW Adj - No Coverage Detail")}    </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_not_cvg_yes_before_uw_adj">  {resultsTable(false, false, true, true, "Annual Summary - before UW Adj - No Coverage Detail")}  </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_yes_cvg_yes_before_uw_adj">  {resultsTable(true, true, true, true, "Term Summary - before UW Adj - Coverage Detail")}       </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_yes_cvg_yes_before_uw_adj">  {resultsTable(false, true, true, true, "Annual Summary - before UW Adj - Coverage Detail")}     </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Pane shownBy="model_state/show_rs_not_cvg_not_before_uw_adj_not_plan">  {resultsTable(true, false, false, false, "Term Summary - after UW Adj- No Coverage Detail")}   </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_not_cvg_not_before_uw_adj_not_plan">  {resultsTable(false, false, false, false, "Annual Summary - after UW Adj - No Coverage Detail")} </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_yes_cvg_not_before_uw_adj_not_plan">  {resultsTable(true, true, false, false, "Term Summary - after UW Adj - Coverage Detail")}      </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_yes_cvg_not_before_uw_adj_not_plan">  {resultsTable(false, true, false, false, "Annual Summary - after UW Adj - Coverage Detail")}    </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Pane shownBy="model_state/show_rs_not_cvg_yes_before_uw_adj_not_plan">  {resultsTable(true, false, true, false, "Term Summary - before UW Adj - No Coverage Detail")}    </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_not_cvg_yes_before_uw_adj_not_plan">  {resultsTable(false, false, true, false, "Annual Summary - before UW Adj - No Coverage Detail")}  </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_yes_cvg_yes_before_uw_adj_not_plan">  {resultsTable(true, true, true, false, "Term Summary - before UW Adj - Coverage Detail")}       </HX.Pane>
          <HX.Pane shownBy="model_state/show_rs_yes_cvg_yes_before_uw_adj_not_plan">  {resultsTable(false, true, true, false, "Annual Summary - before UW Adj - Coverage Detail")}     </HX.Pane>
        </HX.Pane>
      </HX.Section>



    </HX.Page >

  )
}


export { vw_rating_summary };