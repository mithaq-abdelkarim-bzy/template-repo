import * as HX from "hx-model-components";

function vw_rate_change(scale) {
  return (
    <HX.Page title="Rate Change" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Rate Change Summary">
        <HX.Table
          title="This Year"
          data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
          fields={[
            { field: "rate_change/expiring_layer_to_use", width: 200 },
            { field: "renewal_layer.read_only_option" },
            { field: "layer_structure" },
            { field: "summary/ty/reinstatement_description" },
            { field: "summary/ty/rol_quote" },
            { field: "summary/ty/rol_fot" },
            null,
            { field: "rate_change/rol_ly_to_use" },
            { field: "rate_change/rol_rebased" },
            null,
            { field: "rate_change/risk_adjusted_rate_change" },
          ]}
          kb-interactive
          syncColumnWidthsKey="rc_table"
        />
        <HX.Table
          title="Previous Year"
          data={["cds/layers"]}
          fields={[
            { field: "rate_change/expiring_layer_to_use_ly", width: 200 },
            { field: "renewal_layer_ly" },
            { field: "layer_structure_ly" },
            { field: "summary/ly/reinstatement_description" },
            { field: "quote/rol_ly/rol_quote" },
            { field: "quote/rol_ly/rol_fot" },
          ]}
          kb-interactive
          syncColumnWidthsKey="rc_table"
        />
      </HX.Section>

      <HX.Section title="Rate Change Workings">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane>
            <HX.Notes stretch={true}
              field="cds/rate_change/comments"
              title="Rate Change Comments"
            />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection
              numCols={2}
              fields={[
                "cds/send_rate_change/confirm_rate_change",
                null,
                { field: "cds/rate_change/risk_xl_exposure_selection", shownBy: "cds/show_risk_xl" }
              ]} />
          </HX.Pane>
        </HX.Pane>
        <HX.Button task="rate_change_task" title="Run Rate Change" />
        <HX.Table
          data={["cds/layers"]}
          fields={[
            { field: "rate_change/exposure_selection", shownBy: "cds/show_non_risk_xl" },
            { field: "rate_change/exposure_increase", shownBy: "cds/show_non_risk_xl" },
            null,
            { field: "rate_change/exposure_change_fixed/model_calculated" },
            { field: "rate_change/exposure_change_fixed/uw_selected" },
            null,
            { field: "rate_change/limit_change_fixed/model_calculated" },
            { field: "rate_change/limit_change_fixed/uw_selected" },
            null,
            { field: "rate_change/other_change_fixed/uw_selected" },
            null,
            { field: "rate_change/terms_conditions_change_fixed/uw_selected" },
            null,
            { field: "rate_change/rebase_factor" },
            null,
            { field: "rate_change/comments" },
          ]}
          kb-interactive
        />
      </HX.Section>

    </HX.Page >
  )
}

export { vw_rate_change };