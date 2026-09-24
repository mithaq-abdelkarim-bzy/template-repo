import * as HX from "hx-model-components";

function vw_tp_notes(scale) {
  return (
    <HX.Page title="TP Notes" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="TP Notes">
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/quote/tp_calc_info/description" }, { datum: "cds/quote/tp_calc_info/value" }, { datum: "cds/quote/tp_calc_info/value_ly" }]}
            fields={[
              { field: "general_notes" },
              { field: "default_line" },
              null,
              { field: "tp_calc_1" },
              { field: "tp_calc_2" },
              { field: "tp_calc_3" },
              null,
              { field: "lae" },
              { field: "indirect_expenses" },
              { field: "direct_expenses" },
              { field: "inv_income" },
              { field: "ri_cost" },
              { field: "capital_alloc" },
              { field: "roc" },
              { field: "sd_load" }
            ]}
            kb-interactive
            transpose
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="RI Loads">
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/quote/tp_calc_info/ri_cost_ty", width: 250 }, { datum: "cds/quote/tp_calc_info/ri_cost_ly", width: 250 }, { datum: "cds/quote/tp_calc_info/mvt", width: 250 }]}
            fields={[
              { field: "north_east" },
              { field: "mid_atlantic" },
              { field: "carolinas" },
              { field: "fl_se" },
              { field: "fl_non_se" },
              { field: "al_miss" },
              { field: "louisiana" },
              { field: "tx_east" },
              { field: "tx_west" },
              { field: "cal_south" },
              { field: "cal_north" },
              { field: "pnw" },
              { field: "new_madrid" },
              { field: "hawaii" },
              { field: "us_wf" },
              null,
              { field: "eu_ws" },
              { field: "jp_eq" },
              { field: "jp_ws" },
              { field: "can_eq" },
              { field: "caribbean_ws" },
            ]}
            kb-interactive
            transpose
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_tp_notes };