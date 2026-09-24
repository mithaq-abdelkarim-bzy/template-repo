import * as HX from "hx-model-components";

function vw_modelling(scale) {
  return (
    <HX.Page title="Modelling" fullWidth={true} viewScale={scale} shownBy="cds/show_non_risk_xl">
      <HX.Section title="Modelling Results">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={8}>
            <HX.Notes
              field="cds/modelling_account_level/comments"
              title="Comments" />
          </HX.Pane>
          <HX.Pane ratio={5} flow="right" reflow={false}>
            <HX.Pane ratio={1}>
            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Button task="rms_el_allocation_task" title="Run RMS EL Allocation Task" />
              <HX.Collection
                numCols={1}
                fields={[
                  "cds/send_rate_change/confirm_rms_el_allocation"
                ]} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane ratio={2}>
            <HX.Collection fields={[null, "cds/modelling_account_level/ivor_nmp_selection"]}
              stretch={true} />
          </HX.Pane>
          <HX.Pane ratio={2}>
          </HX.Pane>
          <HX.Pane ratio={4}>
          </HX.Pane>

        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane flow="right" reflow={false} ratio={3}>
            <HX.Table
              title="This Year                                                              RMS + NMP (In Application CCY)"
              syncColumnWidthsKey="rms_nmp_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "layer_structure", width: 200 },
                null,
                { field: "model/total_rms_nmp/gross_el" },
                { field: "model/total_rms_nmp/gross_sd" },
                { field: "model/total_rms_nmp/change_el" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane flow="right" reflow={false} ratio={5}>
            <HX.Table
              title="IVOR + NMP (In Application CCY)"
              syncColumnWidthsKey="ivor_nmp_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model/total_ivor_nmp/gross_el" },
                { field: "model/total_ivor_nmp/gross_sd" },
                { field: "model/total_ivor_nmp/change_el" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
            <HX.Table
              title="AIR + NMP (In Application CCY)"
              syncColumnWidthsKey="air_nmp_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model/total_air_nmp/gross_el" },
                { field: "model/total_air_nmp/gross_sd" },
                { field: "model/total_air_nmp/change_el" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane flow="right" reflow={false} ratio={5}>
            <HX.Table
              title="RMS"
              syncColumnWidthsKey="rms_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model/rms/gross_el" },
                { field: "model/rms/gross_sd" },
                { field: "model/rms/change_el" },

                { field: "model/rms/eq_el", shownBy: "/cds/show_us_fields" },
                { field: "model/rms/ws_el", shownBy: "/cds/show_us_fields" },
                { field: "model/rms/scs_el", shownBy: "/cds/show_us_fields" },

                { field: "model/rms/eu_ws_el", shownBy: "/cds/show_intl_fields" },
                { field: "model/rms/jp_eq_el", shownBy: "/cds/show_intl_fields" },
                { field: "model/rms/jp_ws_el", shownBy: "/cds/show_intl_fields" },
                { field: "model/rms/can_eq_el", shownBy: "/cds/show_intl_fields" },
                { field: "model/rms/caribbean_ws_el", shownBy: "/cds/show_intl_fields" },
                null,
                { field: "model/rms/perc_us_el", shownBy: "/cds/show_perc_us_el" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane flow="right" reflow={false} ratio={2}>
            <HX.Table
              title="IVOR"
              syncColumnWidthsKey="ivor_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model/ivor/gross_el" },
                { field: "model/ivor/gross_sd" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane reflow={false} ratio={2}>
            <HX.Table
              title="AIR"
              syncColumnWidthsKey="air_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model/air/gross_el" },
                { field: "model/air/gross_sd" },
                { field: "model/total_air_nmp/change_el" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane flow="right" reflow={false} ratio={4}>
            <HX.Table
              title="NMP"
              syncColumnWidthsKey="nmp_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model/nmp/gross_el_incl_rol" },
                { field: "model/nmp/gross_sd_incl_rol" },
                { field: "model/nmp/gross_el" },
                { field: "model/nmp/gross_sd" },
                { field: "model/nmp/additional_rol" },
                { field: "model/nmp/description" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right" reflow={false}>
          <HX.Pane flow="right" reflow={false} ratio={3}>
            <HX.Table
              title="Previous Year                                                   RMS + NMP (In Application CCY)"
              syncColumnWidthsKey="rms_nmp_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "layer_structure_ly" },
                null,
                { field: "model_prev/total_rms_nmp/gross_el" },
                { field: "model_prev/total_rms_nmp/gross_sd" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane flow="right" reflow={false} ratio={5}>
            <HX.Table
              title="IVOR + NMP (In Application CCY)"
              syncColumnWidthsKey="ivor_nmp_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model_prev/total_ivor_nmp/gross_el" },
                { field: "model_prev/total_ivor_nmp/gross_sd" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
            <HX.Table
              title="AIR + NMP (In Application CCY)"
              syncColumnWidthsKey="air_nmp_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model_prev/total_air_nmp/gross_el" },
                { field: "model_prev/total_air_nmp/gross_sd" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane flow="right" reflow={false} ratio={5}>
            <HX.Table
              title="RMS"
              syncColumnWidthsKey="rms_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model_prev/rms/gross_el" },
                { field: "model_prev/rms/gross_sd" },
                null,
                { field: "model_prev/rms/eq_el", shownBy: "/cds/show_us_fields" },
                { field: "model_prev/rms/ws_el", shownBy: "/cds/show_us_fields" },
                { field: "model_prev/rms/scs_el", shownBy: "/cds/show_us_fields" },

                { field: "model_prev/rms/eu_ws_el", shownBy: "/cds/show_intl_fields" },
                { field: "model_prev/rms/jp_eq_el", shownBy: "/cds/show_intl_fields" },
                { field: "model_prev/rms/jp_ws_el", shownBy: "/cds/show_intl_fields" },
                { field: "model_prev/rms/can_eq_el", shownBy: "/cds/show_intl_fields" },
                { field: "model_prev/rms/caribbean_ws_el", shownBy: "/cds/show_intl_fields" },
                null,
                { field: "model_prev/rms/perc_us_el", shownBy: "/cds/show_perc_us_el" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane flow="right" reflow={false} ratio={2}>
            <HX.Table
              title="IVOR"
              syncColumnWidthsKey="ivor_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model_prev/ivor/gross_el" },
                { field: "model_prev/ivor/gross_sd" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane reflow={false} ratio={2}>
            <HX.Table
              title="AIR"
              syncColumnWidthsKey="air_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model_prev/air/gross_el" },
                { field: "model_prev/air/gross_sd" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane flow="right" reflow={false} ratio={4}>
            <HX.Table
              title="NMP"
              syncColumnWidthsKey="nmp_table"
              data={[{ datum: "cds/layers" }]}
              fields={[
                { field: "model_prev/nmp/gross_el_incl_rol" },
                { field: "model_prev/nmp/gross_sd_incl_rol" },
                { field: "model_prev/nmp/gross_el" },
                { field: "model_prev/nmp/gross_sd" },
                { field: "model_prev/nmp/additional_rol" },
                { field: "model_prev/nmp/description" },
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Cedant RDS Gross Losses" shownBy={"cds/show_us_exposure_fields"} >
        <HX.Table
          with="cds/modelling_account_level/rds_gross_loss"
          data={["this_year", "previous_year", "yoy_growth"]}
          fields={[
            { field: "carolinas_ws", width: 200 },
            { field: "miami_dade_ws", width: 200 },
            { field: "gulf_ws", width: 200 },
            { field: "ne_ws", width: 200 },
            { field: "fl_pinnelas_ws", width: 200 },
            { field: "la_eq", width: 200 },
            { field: "nm_eq", width: 200 },
            { field: "nm_stress_eq", width: 200 },
            { field: "sf_eq", width: 200 },
          ]}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="RMS Regional Entries" shownBy={"cds/show_us_exposure_fields"} >
        <HX.Table
          title="This Year"
          data={[{ datum: "cds/layers" }]}
          fields={[
            { field: "rms_regional/north_east", width: 150 },
            { field: "rms_regional/mid_atlantic", width: 150 },
            { field: "rms_regional/carolinas", width: 150 },
            { field: "rms_regional/fl_se", width: 150 },
            { field: "rms_regional/fl_non_se", width: 150 },
            { field: "rms_regional/al_miss", width: 150 },
            { field: "rms_regional/louisiana", width: 150 },
            { field: "rms_regional/tx_east", width: 150 },
            { field: "rms_regional/tx_west", width: 150 },
            { field: "rms_regional/cal_south", width: 150 },
            { field: "rms_regional/cal_north", width: 150 },
            { field: "rms_regional/pnw", width: 150 },
            { field: "rms_regional/new_madrid", width: 150 },
            { field: "rms_regional/hawaii", width: 150 },
            null,
            { field: "rms_regional/mid_west_1", width: 150 },
            { field: "rms_regional/mid_west_2", width: 150 },
            { field: "rms_regional/second_event", width: 150 },
            { field: "rms_regional/ca_wildfire", width: 150 },
          ]}
          removeHorizontalScroll={true}
          kb-interactive
        />
        <HX.Table
          title="Previous Year"
          data={[{ datum: "cds/layers" }]}
          fields={[
            { field: "rms_regional_prev/north_east", width: 150 },
            { field: "rms_regional_prev/mid_atlantic", width: 150 },
            { field: "rms_regional_prev/carolinas", width: 150 },
            { field: "rms_regional_prev/fl_se", width: 150 },
            { field: "rms_regional_prev/fl_non_se", width: 150 },
            { field: "rms_regional_prev/al_miss", width: 150 },
            { field: "rms_regional_prev/louisiana", width: 150 },
            { field: "rms_regional_prev/tx_east", width: 150 },
            { field: "rms_regional_prev/tx_west", width: 150 },
            { field: "rms_regional_prev/cal_south", width: 150 },
            { field: "rms_regional_prev/cal_north", width: 150 },
            { field: "rms_regional_prev/pnw", width: 150 },
            { field: "rms_regional_prev/new_madrid", width: 150 },
            { field: "rms_regional_prev/hawaii", width: 150 },
            null,
            { field: "rms_regional_prev/mid_west_1", width: 150 },
            { field: "rms_regional_prev/mid_west_2", width: 150 },
            { field: "rms_regional_prev/second_event", width: 150 },
            { field: "rms_regional_prev/ca_wildfire", width: 150 },
          ]}
          removeHorizontalScroll={true}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Marginal Impacts">
        <HX.Pane flow="right" reflow={false} >
          <HX.Pane ratio={3} >
            <HX.Pane flow="right" reflow={false} >
              <HX.Table
                title="Treaty US marginal portfolio impact"
                data={[{ datum: "cds/layers" }]}
                fields={[
                  { field: "marginal_impacts/treaty_us/mi_250" },
                  { field: "marginal_impacts/treaty_us/mi_10" },
                ]}
                freezeLeft={0}
                kb-interactive
              />
              <HX.Table
                title="Treaty Group marginal portfolio impact"
                data={[{ datum: "cds/layers" }]}
                fields={[
                  { field: "marginal_impacts/treaty_group/mi_250" },
                  { field: "marginal_impacts/treaty_group/mi_10" },
                ]}
                freezeLeft={0}
                kb-interactive
              />
              <HX.Table
                title="Treaty US Quake marginal portfolio impact"
                data={[{ datum: "cds/layers" }]}
                fields={[
                  { field: "marginal_impacts/treaty_us_quake/mi_250" },
                  { field: "marginal_impacts/treaty_us_quake/mi_10" },
                ]}
                freezeLeft={0}
                kb-interactive
              />
              <HX.Table
                title="Treaty Intl marginal portfolio impact"
                data={[{ datum: "cds/layers" }]}
                fields={[
                  { field: "marginal_impacts/treaty_intl/mi_250" },
                  { field: "marginal_impacts/treaty_intl/mi_10" },
                ]}
                freezeLeft={0}
                kb-interactive
              />
            </HX.Pane>
            <HX.Pane flow="right" reflow={false} >
              <HX.Table
                title="Treaty US marginal portfolio impact"
                data={[{ datum: "cds/layers" }]}
                fields={[
                  { field: "marginal_impacts_prev/treaty_us/mi_250" },
                  { field: "marginal_impacts_prev/treaty_us/mi_10" },
                ]}
                freezeLeft={0}
                kb-interactive
              />
              <HX.Table
                title="Treaty Group marginal portfolio impact"
                data={[{ datum: "cds/layers" }]}
                fields={[
                  { field: "marginal_impacts_prev/treaty_group/mi_250" },
                  { field: "marginal_impacts_prev/treaty_group/mi_10" },
                ]}
                freezeLeft={0}
                kb-interactive
              />
              <HX.Table
                title="Treaty US Quake marginal portfolio impact"
                data={[{ datum: "cds/layers" }]}
                fields={[
                  { field: "marginal_impacts_prev/treaty_us_quake/mi_250" },
                  { field: "marginal_impacts_prev/treaty_us_quake/mi_10" },
                ]}
                freezeLeft={0}
                kb-interactive
              />
              <HX.Table
                title="Treaty Intl marginal portfolio impact"
                data={[{ datum: "cds/layers" }]}
                fields={[
                  { field: "marginal_impacts_prev/treaty_intl/mi_250" },
                  { field: "marginal_impacts_prev/treaty_intl/mi_10" },
                ]}
                freezeLeft={0}
                kb-interactive
              />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane ratio={1} >

          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_modelling };