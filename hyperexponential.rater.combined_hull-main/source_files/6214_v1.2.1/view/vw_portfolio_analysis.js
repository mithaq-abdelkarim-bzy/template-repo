import * as HX from "hx-model-components";

function vw_portfolio_analysis(scale) {
  return (
    <HX.Page
      title="Portfolio Analysis"
      fullWidth
      shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage"
    >
      <HX.With
        context={{
          type: "struct",
          path: "cds/portfolio_analysis/hull_rating",
        }}
      >
        <HX.Section title="Filter Options">
          <HX.With context={{ type: "struct", path: "filter_options" }}>
            <HX.Pane flow="right" reflow={false}>
              <HX.Pane flow="down">
                <HX.Collection
                  with="effective_date"
                  fields={["effective_date_from", "effective_date_to"]}
                  horizontal
                />
                <HX.Collection fields={["insured"]} />
                <HX.Collection fields={["vessel_type"]} />
                <HX.Collection fields={["operator_domicile"]} />
              </HX.Pane>
              <HX.Pane flow="down" stretch>
                <HX.Button
                  task={"portfolio_analysis_search_task"}
                  title="Search"
                />
                <HX.Button
                  task={"clear_portfolio_analysis_search_task"}
                  title="Clear Search"
                />
                <HX.Button
                  task={"generate_portfolio_analysis_excel"}
                  title="Export Excel"
                />
                <HX.File
                  field="/cds/portfolio_analysis/hull_rating/exported_data"
                  shownBy="/non_cds/show_hide_toggles/hull/show_generated_portfolio_analysis_excel"
                />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="down">
                <HX.Collection fields={["status"]} />
                <HX.Collection fields={["imo"]} />
                <HX.Collection fields={["coverage"]} />
                <HX.Collection fields={["currency"]} />
              </HX.Pane>
              <HX.Pane flow="down">
                <HX.Collection
                  with="agreed_value"
                  fields={["agreed_value_from", "agreed_value_to"]}
                  horizontal
                />
                <HX.Collection
                  with="gross_tonnage"
                  fields={["gross_tonnage_from", "gross_tonnage_to"]}
                  horizontal
                />
                <HX.Collection
                  with="dwt"
                  fields={["dwt_from", "dwt_to"]}
                  horizontal
                />
                <HX.Collection
                  with="year_built"
                  fields={["year_built_from", "year_built_to"]}
                  horizontal
                />
              </HX.Pane>
              <HX.Pane flow="down">
                <HX.Collection fields={["has_policy_reference"]} />
                <HX.Collection fields={["policy_reference"]} />
                <HX.Collection fields={["flag"]} />
                <HX.Collection fields={["vessel_class"]} />
              </HX.Pane>
              <HX.Pane flow="down">
                <HX.Collection fields={["live_risk_entry"]} />
                <HX.Collection fields={["follow_lead"]} />
                <HX.Collection fields={["broker"]} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Portfolio Metrics">
          <HX.With context={{ type: "struct", path: "portfolio_metrics" }}>
            <HX.Pane flow="down">
              <HX.Collection
                fields={[
                  "vessels_count",
                  {
                    field: "average_agreed_value",
                    labelBy:
                      "/non_cds/labels/portfolio_analysis_labels/currency_avg_agreed_value",
                  },
                  "average_achieved_rate",
                ]}
                horizontal
              />
              <HX.Table
                maxListVisibleRows={10}
                data={["vessels"]}
                fields={[
                  "id",
                  "imo",
                  "insured",
                  "policy_reference",
                  "effective_date",
                  "expiry_date",
                  "coverage",
                  "original_agreed_value",
                  "original_currency",
                  {
                    field: "agreed_value_converted",
                    labelBy:
                      "/non_cds/labels/portfolio_analysis_labels/currency_agreed_value_converted",
                  },
                  "vessel_type",
                  "gross_tonnage",
                  "dwt",
                  "year_built",
                  "flag",
                  "classification",
                  "achieved_rate",
                  "order_percent",
                  "written_line_percent",
                  "operator_domicile",
                  "broker",
                  "follow_lead",
                  "vessel_name",
                  "type_abrv",
                ]}
              />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_portfolio_analysis };
