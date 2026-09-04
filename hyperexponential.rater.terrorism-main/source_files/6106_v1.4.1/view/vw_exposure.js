import * as HX from "hx-model-components";



function risk_adj_Table(showIHS_read_only = false, selectedTitle = "") {

  //Default State
  let selectedData = ["security", "industry", "policy", "ihs_score"]

  let selectedFields = [
    null
    , { field: "level", maxWidth: 140 }
    , null
    , { field: "calculated", maxWidth: 140 }
    , null
    , { field: "min", maxWidth: 100 }
    , { field: "override", maxWidth: 100 }
    , { field: "max", maxWidth: 100 }
    , null
    , { field: "selected", maxWidth: 100 }
    , null
    , { field: "description" }
  ]

  // Updating selectedData based on showIHS_read_only
  if (showIHS_read_only === true) { selectedData = ["security", "industry", "policy", "ihs_score_read_only", "ihs_score_expiring"] }

  return (
    <HX.Table
      title={selectedTitle}
      data={selectedData}
      fields={selectedFields}
      with="risk_adjustments"
      kb-interactive
      freezeLeft={0}
    />
  )
}




function vw_exposure(shownBy) {
  return (
    <HX.Page title="Exposure Details" shownBy={shownBy} viewScale={0.9}>
      <HX.Section title="Cover Details">
        <HX.Pane flow="right" reflow={true}>

          <HX.Table
            title="Summary Details"
            data={["cds/exposure/aggregate"]}
            fields={[
              { field: "total_sum_insured", labelAlign: "right" }
              , { field: "bi_sum_insured", labelAlign: "right" }
              , { field: "pd_sum_insured", labelAlign: "right" }
              , { field: "policy_limit", labelAlign: "right" }
              , { field: "policy_sublimit", labelAlign: "right" }
              , { field: "policy_excess", labelAlign: "right" }
              , { field: "policy_deductible", labelAlign: "right" }
              , { field: "no_of_locations", labelAlign: "right" }
              , { field: "agg_discount", labelAlign: "right" }
            ]}
            transpose
            kb-interactive
          />

          <HX.Pane flow="down" >
            <HX.Table
              title="Additional Details"
              data={["cds/exposure/aggregate/details"]}
              fields={[
                { field: "limit_type", labelAlign: "right" }
                , { field: "bi_wait_period", labelAlign: "right" }
                , { field: "bi_indemnity_period", labelAlign: "right" }
                , { field: "contingent_bi", labelAlign: "right" }
                , { field: "aggregate_usage", labelAlign: "right" }
              ]}
              transpose
              kb-interactive
            />
            <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>         <HX.Collection fields={["coverages/construction/is_covered"]} horizontal />         </HX.With>
          </HX.Pane>
        </HX.Pane>
      </HX.Section>


      <HX.Section title="IHS Score Adjustment - tabular (click to reveal)" shownBy="/model_state/not_migrated" defaultCollapsed>
        <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
          <HX.Table
            data={[null, { datum: "countries", maxWidth: 280 }]}
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

              // { field: "civil_unrest_uw_adj", shownBy: "civil_unrest_uw_adj_valid" },
              // { field: "civil_unrest_uw_adj.red", infoBy: "civil_unrest_uw_adj_info", shownBy: "civil_unrest_uw_adj_invalid" },

              { field: "civil_unrest_roe_selected", infoBy: "civil_unrest_info" },
              null,
              "interstate_war",
              "civil_war",
              "war",
              "override_war",
              "selected_war",

              // { field: "war_uw_adj", shownBy: "war_uw_adj_valid" },
              // { field: "war_uw_adj.red", infoBy: "war_uw_adj_info", shownBy: "war_uw_adj_invalid" },

              { field: "war_roe_selected", infoBy: "war_info" },
              null,
              "terrorism_raw",
              "political",
              "civil_unrest",
              "war",
              "terrorism",
              "override_terrorism",
              "selected_terrorism",

              // { field: "terrorism_uw_adj", shownBy: "terrorism_uw_adj_valid" },
              // { field: "terrorism_uw_adj.red", infoBy: "terrorism_uw_adj_info", shownBy: "terrorism_uw_adj_invalid" },

              { field: "terrorism_roe_selected", infoBy: "terrorism_info" }
            ]}
            kb-interactive
            transpose
            freezeLeft={0}
          />
        </HX.With>
      </HX.Section>


      <HX.Section title="IHS Score Adjustment - detailed (click to reveal)" shownBy="/model_state/not_migrated" defaultCollapsed>
        <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
          <HX.Selector
            title="Select the country to adjust - only showing covered perils based on selected coverage and subcoverage"
            data={["countries"]}
            dropdown="rated_country"
          >
            <HX.Pane shownBy="has_civil_unrest">
              <HX.Collection title="Civil Unrest" fields={["labour_strikes", "protests_riots"]} horizontal />
              <HX.Collection fields={["civil_unrest", "override_civil_unrest", "selected_civil_unrest"]} horizontal />
              <HX.Collection fields={["civil_unrest_roe_calculated", null, "civil_unrest_roe_selected"]} horizontal />
            </HX.Pane>
            <HX.Pane shownBy="has_war">
              <HX.Collection title="War" fields={["interstate_war", "civil_war"]} horizontal />
              <HX.Collection fields={["war", "override_war", "selected_war"]} horizontal />
              <HX.Collection fields={["war_roe_calculated", null, "war_roe_selected"]} horizontal />
            </HX.Pane>
            <HX.Pane shownBy="has_terrorism">
              <HX.Collection title="Terrorism" fields={["political", "terrorism_raw"]} horizontal />
              <HX.Collection fields={["civil_unrest", "war"]} horizontal />
              <HX.Collection fields={["terrorism", "override_terrorism", "selected_terrorism"]} horizontal />
              <HX.Collection fields={["terrorism_roe_calculated", null, "terrorism_roe_selected"]} horizontal />
            </HX.Pane>
          </HX.Selector>

        </HX.With>
      </HX.Section>


      <HX.Section title="Risk Adjustments">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="down">

            <HX.Pane shownBy="/model_state/is_migrated">   {risk_adj_Table(false, "Underwriter Adjustments - including legacy IHS override approach")}   </HX.Pane>
            <HX.Pane shownBy="/model_state/not_migrated">  {risk_adj_Table(true, "Underwriter Adjustments")}                                             </HX.Pane>

            <HX.Collection title="Summary" fields={["uw_ihs_adjustment", "total_adj_score", "uw_multiplier"]} horizontal with="risk_adjustments" />
            {/* <HX.Collection title="Summary" fields={[{ field: "uw_ihs_adjustment", shownBy: "/model_state/is_migrated" }, "total_adj_score", "uw_multiplier"]} horizontal with="risk_adjustments" /> */}

            <HX.Notes field="risk_adjustments/uw_rationale" title="Please provide detail on the Risk Level associated with the selected scores:" />
          </HX.Pane>
        </HX.With>
      </HX.Section>

      <HX.Section title="Individual Risk Score Comments (click to reveal)" defaultCollapsed={true}>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Notes field="risk_adjustments/security/uw_rationale" title="Please provide detail on the Risk Level associated with the selected Security Score:" />
          <HX.Notes field="risk_adjustments/industry/uw_rationale" title="Please provide detail on the Risk Level associated with the selected Industry Score:" />
          <HX.Notes field="risk_adjustments/policy/uw_rationale" title="Please provide detail on the Risk Level associated with the selected Policy Score:" />
          <HX.Notes field="risk_adjustments/ihs_score/uw_rationale" title="Please provide detail on the Risk Level associated with the selected IHS Score:" />
        </HX.With>
      </HX.Section>

      <HX.Section title="General Comments">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="down">
            <HX.Notes field="risk_adjustments/uw_general_comments" />
          </HX.Pane>
        </HX.With>
      </HX.Section>


    </HX.Page >
  )
}

export { vw_exposure };
