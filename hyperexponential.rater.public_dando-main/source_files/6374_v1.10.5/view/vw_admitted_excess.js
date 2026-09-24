import * as HX from "hx-model-components";

function vw_admitted_excess(scale) {
  return (
    <HX.Page
      title="Admitted Excess"
      fullWidth={true}
      viewScale={scale}
      shownBy="cds/admitted_excess/conditions_met">
      <HX.Section title="Layer Information">
        <HX.Pane flow="right">
          <HX.Table
            data={["exc_prim_limit", "exc_prim_retention", "exc_prim_premium", "exc_excess_limit", "exc_excess_attach", "exc_no_policies"]}
            with="cds/admitted_excess"
            fields={[{ field: "value", width: 150 }]}
            title=""
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Admitted Rating">
        <HX.Pane flow="right">
          <HX.Table
            data={["exc_prim_rate_ade", "exc_large_loss", "exc_ind_risk_level", "exc_ind_sec_factor", "exc_comp_spe_risk_level", "exc_comp_spe_factor", "exc_liti_potential_risk_level", "exc_liti_potential_factor", "exc_fl_schedule_rating_factor", "adm_exc_model_prem", "adm_exc_max_round_down", "adm_exc_max_round_up", "adm_exc_round_prem"]} with="cds/admitted_excess"
            fields={[
              { field: "value", width: 150 },
              { field: "min", width: 150 },
              { field: "max", width: 150 }
            ]}
            title=""
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_admitted_excess };