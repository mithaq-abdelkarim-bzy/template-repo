import * as HX from "hx-model-components";

function vw_rate_change_synergy(scale) {
  return (
    <HX.Page title="Rate Change Synergy" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Rate Change Synergy">
        <HX.Pane>
          <HX.Table
            data={["cds/layers"]}
            fields={[
              { field: "section_reference.read_only_option" },
              { field: "layer_structure" },
              { field: "layer_description.read_only_option" },
              null,
              { field: "rate_change/rol_ly_to_use" },
              { field: "rate_change/exposure_change_fixed/final" },
              { field: "rate_change/risk_characteristics_change_fixed/final" },
              { field: "rate_change/deductible_change_fixed/final" },
              { field: "rate_change/limit_change_fixed/final" },
              { field: "rate_change/terms_conditions_change_fixed/final" },
              { field: "rate_change/other_change_fixed/final" },
              { field: "rate_change/rol_rebased" },
              { field: "quote/rol_ty/rol_fot.read_only_option" },
              { field: "rate_change/risk_adjusted_rate_change" },
              null,
              { field: "quote/rol_ty/est_sign_written_ratio" },
              { field: "quote/rol_ty/ulr" },
              { field: "quote/rol_ty/bpi" },
              null,
              { field: "rate_change/rationale_outside_plan" }
            ]}
            kb-interactive
            transpose
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rate_change_synergy };