import * as HX from "hx-model-components";

function vw_risk_assessment(scale) {
  return (
    < HX.Page title="Risk Assessment" viewScale={scale} fullWidth={true} shownBy="cds/risk_information/not_mmp_flag" >
      <HX.Section title="Sector Commentary">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Notes field="cds/modifiers/message" title="Message" />
            <HX.Pane>
              <HX.Collection
                fields={[
                  { field: "sca_freq_adj_factor", infoBy: "sca_freq_adj_factor_info" },
                  null, null, null, null, null
                ]}
                with="cds/modifiers"
                horizontal
              />
              <HX.Collection
                fields={[
                  "sca_freq_adj_factor_comment"]}
                with="cds/modifiers"
              />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane>
          </HX.Pane>
        </HX.Pane>

      </HX.Section >

      <HX.Section title="Underwriting Modifiers - AB/ABC">
        <HX.Pane flow="right">
          <HX.Table
            data={["cds/modifiers/management_corp_gov_factors", "cds/modifiers/business_financial_model_factors",
              "cds/modifiers/significant_event_factors", "cds/modifiers/stock_market_factors", "cds/modifiers/sca_adj_factors"]}
            fields={[
              { field: "value", width: 100 },
              { field: "min", width: 100 },
              { field: "max", width: 100 },
              { field: "comment", maxWidth: 600 }
            ]}
            rowHeaderSettings={{ width: 400 }}
            shownBy="cds/risk_information/public_flag"
            kb-interactive />
          <HX.Table
            data={["cds/modifiers/management_corp_gov_factors", "cds/modifiers/business_financial_model_factors",
              "cds/modifiers/significant_event_factors", "cds/modifiers/sca_adj_factors"]}
            fields={[
              { field: "value", width: 100 },
              { field: "min", width: 100 },
              { field: "max", width: 100 },
              { field: "comment", maxWidth: 600 }
            ]}
            rowHeaderSettings={{ width: 400 }}
            shownBy="cds/risk_information/private_flag"
            kb-interactive />
        </HX.Pane>

        <HX.Pane>

        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Table
            data={["regulatory_factors", "mergers_and_acquisitions_factors", "territory_of_operation_factors", "total_factors"]}
            fields={[
              { field: "value", width: 100 },
              { field: "min", width: 100 },
              { field: "max", width: 100 },
              { field: "comment", maxWidth: 600 }
            ]}
            rowHeaderSettings={{ width: 400 }}
            with="cds/modifiers"
            kb-interactive />
        </HX.Pane>


      </HX.Section>

      <HX.Section title="Underwriting Modifiers - Side A">
        <HX.Pane flow="right">
          <HX.Table
            data={["cds/modifiers/management_corp_gov_factors_side_a", "cds/modifiers/business_financial_model_factors_side_a", "cds/modifiers/significant_event_factors_side_a", "cds/modifiers/stock_market_factors_side_a", "cds/modifiers/sca_adj_factors_side_a"]}
            fields={[
              { field: "value", width: 100 },
              { field: "min", width: 100 },
              { field: "max", width: 100 },
              { field: "comment", maxWidth: 600 }
            ]}
            rowHeaderSettings={{ width: 400 }}
            shownBy="cds/risk_information/public_flag"
            kb-interactive />
          <HX.Table
            data={["cds/modifiers/management_corp_gov_factors_side_a", "cds/modifiers/business_financial_model_factors_side_a", "cds/modifiers/significant_event_factors_side_a", "cds/modifiers/sca_adj_factors_side_a"]}
            fields={[
              { field: "value", width: 100 },
              { field: "min", width: 100 },
              { field: "max", width: 100 },
              { field: "comment", maxWidth: 600 }
            ]}
            rowHeaderSettings={{ width: 400 }}
            shownBy="cds/risk_information/private_flag"
            kb-interactive />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Table
            data={["financial_stability_side_a_factors", "indemnification_side_a_factors", "total_factors_side_a"]}
            fields={[
              { field: "value", width: 100 },
              { field: "min", width: 100 },
              { field: "max", width: 100 },
              { field: "comment", maxWidth: 600 }
            ]}
            rowHeaderSettings={{ width: 400 }}
            with="cds/modifiers"
            kb-interactive />
        </HX.Pane>

      </HX.Section>

      <HX.Section title="Side A Modification Commentary">
        <HX.Pane >
          <HX.Pane>
            <HX.Collection
              fields={["suggested_factor", null, null, null, null, null]}
              with="cds/modifiers"
              horizontal
            />
          </HX.Pane>

          <HX.Pane>
            <HX.Notes field="cds/modifiers/suggested_factor_message" title="Message" />
            <HX.Notes field="cds/modifiers/suggested_factor_message_for_adj" title="Message for Adjustments" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}


export { vw_risk_assessment };