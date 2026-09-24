import * as HX from "hx-model-components";
import CombinationChart from "components/combination";
import Bar from "components/bar";
import CompoundBar from "components/compound_bar_graph";

function vw_quote(scale) {
  return (
    <HX.Page title="Quote" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="ROL Calc" shownBy="cds/show_non_risk_xl">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Notes
              field="cds/tp_comments"
              title="Quote Comments"
            />
            <HX.Notes
              field="cds/quote/quote_reins_information"
              title="KPI Basis Information"
            />
          </HX.Pane>
          <HX.Pane ratio={1}>
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={8}>
            <HX.Table
              title="This Year"
              data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
              fields={[
                { field: "layer_structure" },
                null,
                { field: "quote/rol_ty/rol_rms" },
                { field: "quote/rol_ty/weighting_rms" },
                { field: "quote/rol_ty/rol_ivor" },
                { field: "quote/rol_ty/weighting_ivor" },
                { field: "quote/rol_ty/rol_air" },
                { field: "quote/rol_ty/weighting_air" },
                { field: "quote/rol_ty/rol_burn" },
                { field: "quote/rol_ty/rol_burn_override" },
                { field: "quote/rol_ty/weighting_burn" },
                null,
                { field: "quote/rol_ty/rol_afb_tech" },
                null,
                { field: "quote/rol_ty/ulr" },
                { field: "quote/rol_ty/bpi" },
                null,
                { field: "quote/rol_ty/lol_rms" },
                { field: "quote/rol_ty/lol_ivor" },
                { field: "quote/rol_ty/lol_air" },
                { field: "quote/rol_ty/lol_burn" },
                { field: "quote/rol_ty/lol_weighted" }
              ]}
              kb-interactive
              syncColumnWidthsKey="rol_calc_table"
            />
          </HX.Pane>
          <HX.Pane ratio={3} flow="right" reflow={false}>
            <HX.Table
              title="All Perils"
              data={["cds/layers"]}
              fields={[
                { field: "quote/rol_ty/rp_attach" },
                { field: "quote/rol_ty/rp_exit" },
                { field: "quote/rol_ty/rp_pml_selection" }
              ]}
              kb-interactive
              syncColumnWidthsKey="all_perils_table"
            />
            <HX.Table
              title="Peak Peril"
              data={["cds/layers"]}
              fields={[
                { field: "quote/rol_ty/rp_attach_peak" },
                { field: "quote/rol_ty/rp_exit_peak" },
                { field: "quote/rol_ty/rp_pml_selection_peak" }
              ]}
              kb-interactive
              syncColumnWidthsKey="peak_perils_table"
            />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={8}>
            <HX.Table
              title="Previous Year"
              data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
              fields={[
                { field: "layer_structure_ly" },
                null,
                { field: "quote/rol_ly/rol_rms" },
                { field: "quote/rol_ly/weighting_rms" },
                { field: "quote/rol_ly/rol_ivor" },
                { field: "quote/rol_ly/weighting_ivor" },
                { field: "quote/rol_ly/rol_air" },
                { field: "quote/rol_ly/weighting_air" },
                { field: "quote/rol_ly/rol_burn" },
                { field: "quote/rol_ly/rol_burn_override" },
                { field: "quote/rol_ly/weighting_burn" },
                null,
                { field: "quote/rol_ly/rol_afb_tech" },
                null,
                { field: "quote/rol_ly/ulr" },
                { field: "quote/rol_ly/bpi" },
                null,
                { field: "quote/rol_ly/lol_rms" },
                { field: "quote/rol_ly/lol_ivor" },
                { field: "quote/rol_ly/lol_air" },
                { field: "quote/rol_ly/lol_burn" },
                { field: "quote/rol_ly/lol_weighted" }
              ]}
              kb-interactive
              syncColumnWidthsKey="rol_calc_table"
            />
          </HX.Pane>
          <HX.Pane ratio={3} flow="right" reflow={false}>
            <HX.Table
              title="All Perils"
              data={["cds/layers"]}
              fields={[
                { field: "quote/rol_ly/rp_attach" },
                { field: "quote/rol_ly/rp_exit" },
                { field: "quote/rol_ly/rp_pml_selection" }
              ]}
              kb-interactive
              syncColumnWidthsKey="all_perils_table"
            />
            <HX.Table
              title="Peak Peril"
              data={["cds/layers"]}
              fields={[
                { field: "quote/rol_ly/rp_attach_peak" },
                { field: "quote/rol_ly/rp_exit_peak" },
                { field: "quote/rol_ly/rp_pml_selection_peak" }
              ]}
              kb-interactive
              syncColumnWidthsKey="peak_perils_table"
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="ROL Calc" shownBy="cds/show_risk_xl">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Notes
              field="cds/tp_comments"
              title="Quote Comments"
            />
            <HX.Notes
              field="cds/quote/quote_reins_information"
              title="KPI Basis Information"
            />
          </HX.Pane>
          <HX.Pane ratio={1}>
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={8}>
            <HX.Table
              title="This Year"
              data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
              fields={[
                { field: "layer_structure" },
                null,
                { field: "quote/rol_ty/risk_xl_rol_exposure" },
                { field: "quote/rol_ty/risk_xl_weighting_exposure" },
                { field: "quote/rol_ty/rol_burn" },
                { field: "quote/rol_ty/rol_burn_override" },
                { field: "quote/rol_ty/weighting_burn" },
                null,
                { field: "quote/rol_ty/rol_afb_tech" },
                null,
                { field: "quote/rol_ty/layer_exposure" },
                { field: "quote/rol_ty/roev" },
                null,
                { field: "quote/rol_ty/ulr" },
                { field: "quote/rol_ty/bpi" },
                null,
                { field: "quote/rol_ty/risk_xl_lol_exposure" },
                { field: "quote/rol_ty/lol_burn" },
                { field: "quote/rol_ty/lol_weighted" }
              ]}
              kb-interactive
              syncColumnWidthsKey="rol_calc_table"
            />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={8}>
            <HX.Table
              title="Previous Year"
              data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
              fields={[
                { field: "layer_structure_ly" },
                null,
                { field: "quote/rol_ly/risk_xl_rol_exposure" },
                { field: "quote/rol_ly/risk_xl_weighting_exposure" },
                { field: "quote/rol_ly/rol_burn" },
                { field: "quote/rol_ly/rol_burn_override" },
                { field: "quote/rol_ly/weighting_burn" },
                null,
                { field: "quote/rol_ly/rol_afb_tech" },
                null,
                { field: "quote/rol_ly/layer_exposure" },
                { field: "quote/rol_ly/roev" },
                null,
                { field: "quote/rol_ly/ulr" },
                { field: "quote/rol_ly/bpi" },
                null,
                { field: "quote/rol_ly/risk_xl_lol_exposure" },
                { field: "quote/rol_ly/lol_burn" },
                { field: "quote/rol_ly/lol_weighted" }
              ]}
              kb-interactive
              syncColumnWidthsKey="rol_calc_table"
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>


      <HX.Section title="BI Data" defaultCollapsed>
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Button task="bi_data_fetch_task" title="Fetch BI Data" />
            <HX.Collection
              numCols={1}
              fields={[
                "cds/bi_data/profit",
                "cds/bi_data/ilr",
                "cds/bi_data/break_even"
              ]}
            />
          </HX.Pane>
          <HX.Pane ratio={3}>
            <CombinationChart
              title="BI Data"
              data={[
                { list: "cds/bi_data/graph_list", labelBy: "yoa" },
                { list: "cds/bi_data/graph_list", labelBy: "yoa" },
                { list: "cds/bi_data/graph_list", labelBy: "yoa" }
              ]}
              traces={[
                { field: "wep", label: "WEP" },
                { field: "incurred", label: "Incurred" },
                { field: "exposure", label: "Exposure" }
              ]}
              series={[
                {
                  seriesLabel: "ELR",
                  points: [
                    {
                      list: "cds/bi_data/graph_list",
                      x: "yoa",
                      y: "elr",
                    },
                  ],
                },
                {
                  seriesLabel: "Rate Change",
                  points: [
                    {
                      list: "cds/bi_data/graph_list",
                      x: "yoa",
                      y: "cumulative_rate_change",
                    },
                  ],
                }
              ]}
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Line Size">
        <HX.Table
          title="This Year"
          data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }, null, { datum: "cds/quote_total_usd" }]}
          fields={[
            { field: "limit_cnv" },
            { field: "excess_cnv" },
            { field: "layer_description.read_only_option" },
            null,
            { field: "quote/rol_ty/rol_quote" },
            { field: "quote/rol_ty/rol_fot" },
            { field: "summary/ty/risk_adjusted_rate_change" },
            { field: "quote/rol_ty/rol_afb_tech" },
            { field: "quote/rol_ty/quote_fot_ratio" },
            { field: "quote/rol_ty/quote_adequacy" },
            { field: "quote/rol_ty/fot_adequacy" },
            null,
            { field: "quote/rol_ty/prem_full_line" },
            { field: "quote/rol_ty/written_line" },
            { field: "quote/rol_ty/written_line_dollar" },
            { field: "quote/rol_ty/estimated_signing" },
            { field: "quote/rol_ty/estimated_signing_dollar" },
            { field: "quote/rol_ty/signed_line" },
            { field: "quote/rol_ty/signed_line_dollar" },
            null,
            { field: "quote/rol_ty/epi_written" },
            { field: "quote/rol_ty/epi_estimated" },
            { field: "quote/rol_ty/epi_signed" }
          ]}
          kb-interactive
          removeHorizontalScroll={true}
          syncColumnWidthsKey="line_size_table"
        />
        <HX.Table
          title="Previous Year"
          data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }, null, { datum: "cds/quote_total_usd" }]}
          fields={[
            { field: "limit_cnv_ly" },
            { field: "excess_cnv_ly" },
            { field: "layer_description_ly" },
            null,
            { field: "quote/rol_ly/rol_quote" },
            { field: "quote/rol_ly/rol_fot" },
            { field: "summary/ly/risk_adjusted_rate_change" },
            { field: "quote/rol_ly/rol_afb_tech" },
            { field: "quote/rol_ly/quote_fot_ratio" },
            { field: "quote/rol_ly/quote_adequacy" },
            { field: "quote/rol_ly/fot_adequacy" },
            null,
            { field: "quote/rol_ly/prem_full_line" },
            { field: "quote/rol_ly/written_line" },
            { field: "quote/rol_ly/written_line_dollar" },
            { field: "quote/rol_ly/estimated_signing" },
            { field: "quote/rol_ly/estimated_signing_dollar" },
            { field: "quote/rol_ly/signed_line" },
            { field: "quote/rol_ly/signed_line_dollar" },
            null,
            { field: "quote/rol_ly/epi_written" },
            { field: "quote/rol_ly/epi_estimated" },
            { field: "quote/rol_ly/epi_signed" }
          ]}
          kb-interactive
          removeHorizontalScroll={true}
          syncColumnWidthsKey="line_size_table"
        />
      </HX.Section>
      <HX.Section title="RMS TP Calc" shownBy="cds/show_non_risk_xl">
        <HX.Pane>
          <HX.Notes
            field="cds/quote/rms_tp_calc_reins_information"
            title="Net Expected Loss Calculation Information"
          />
        </HX.Pane>
        <HX.Table
          title="Net Expected Loss"
          data={["cds/layers"]}
          fields={[
            { field: "quote/rms_tp_calc/gross_lol" },
            null,
            { field: "quote/rms_tp_calc/gross_el" },
            { field: "quote/rms_tp_calc/gross_sd" },
            { field: "quote/rms_tp_calc/model_limit_factor", infoBy: "/cds/number_reins_factor_info" },
            { field: "quote/rms_tp_calc/override_limit_factor" },
            { field: "quote/rms_tp_calc/net_el_excl_reins_prem" },
            { field: "quote/rms_tp_calc/no_expected_reins", infoBy: "/cds/paid_reins_factor_info" },
            null,
            { field: "quote/rms_tp_calc/net_el" },
            { field: "quote/rms_tp_calc/net_sd" },
            null,
            { field: "quote/rms_tp_calc/net_el_incl_bs" },
            { field: "quote/rms_tp_calc/net_sd_incl_bs" }
          ]}
          kb-interactive
        />
        <HX.Table
          title="Technical Premium Components"
          data={["cds/layers"]}
          fields={[
            { field: "quote/rms_tp_calc/afb_net_el" },
            { field: "quote/rms_tp_calc/afb_net_sd" },
            null,
            { field: "quote/rms_tp_calc/indirect_expenses" },
            { field: "quote/rms_tp_calc/direct_expenses" },
            { field: "quote/rms_tp_calc/lae" },
            { field: "quote/rms_tp_calc/total_expenses" },
            null,
            { field: "quote/rms_tp_calc/mi_250" },
            { field: "quote/rms_tp_calc/marginal_impact" },
            { field: "quote/rms_tp_calc/capital_us" },
            { field: "quote/rms_tp_calc/capital_intl" },
            { field: "quote/rms_tp_calc/attritional_capital" },
            { field: "quote/rms_tp_calc/total_capital" },
            { field: "quote/rms_tp_calc/total_coc" },
            null,
            { field: "quote/rms_tp_calc/ri_cost" }
          ]}
          kb-interactive
        />
        <HX.Table
          title="Technical Premium Calculations"
          data={["cds/layers"]}
          fields={[
            { field: "quote/rms_tp_calc/tp_calc_1", infoBy: "/cds/tp_calc_1_info" },
            { field: "quote/rms_tp_calc/tp_calc_2", infoBy: "/cds/tp_calc_2_info" },
            { field: "quote/rms_tp_calc/tp_calc_3", infoBy: "/cds/tp_calc_3_info" },
            null,
            { field: "quote/rms_tp_calc/tp_max_calculation" },
            { field: "quote/rms_tp_calc/tp_final" },
            null,
            { field: "quote/rms_tp_calc/tp_non_loss_cost" },
            null,
            { field: "quote/rol_ty/rol_rms" }
          ]}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Other TP Calculations" shownBy="cds/show_non_risk_xl">

        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={2}>
            <HX.Table
              title="IVOR"
              data={["cds/layers"]}
              fields={[
                { field: "quote/ivor_tp_calc/afb_net_el" },
                { field: "quote/ivor_tp_calc/afb_net_sd" },
                null,
                { field: "quote/ivor_tp_calc/tp_final" },
                null,
                { field: "quote/rol_ty/rol_ivor" }
              ]}
              kb-interactive
              syncColumnWidthsKey="other_tp_tables"
            />
          </HX.Pane>
          <HX.Pane ratio={1}>
          </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={2}>
            <HX.Table
              title="AIR"
              data={["cds/layers"]}
              fields={[
                { field: "quote/air_tp_calc/afb_net_el" },
                { field: "quote/air_tp_calc/afb_net_sd" },
                null,
                { field: "quote/air_tp_calc/tp_final" },
                null,
                { field: "quote/rol_ty/rol_air" }
              ]}
              kb-interactive
              syncColumnWidthsKey="other_tp_tables"
            />
          </HX.Pane>
          <HX.Pane ratio={1}>
          </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={2}>
            <HX.Table
              title="Burn"
              data={["cds/layers"]}
              fields={[
                { field: "quote/burn_tp_calc/afb_net_el" },
                { field: "quote/burn_tp_calc/afb_net_sd" },
                null,
                { field: "quote/burn_tp_calc/tp_final" },
                null,
                { field: "quote/rol_ty/rol_burn" }
              ]}
              kb-interactive
              syncColumnWidthsKey="other_tp_tables"
            />
          </HX.Pane>
          <HX.Pane ratio={1}>
          </HX.Pane>
        </HX.Pane>

      </HX.Section>
      <HX.Section title="Technical Premium Breakdown" shownBy="cds/show_non_risk_xl">
        <HX.Pane flow="right">
          <Bar
            title="Technical Premium (GN) - Calculation 1"
            data={[{ list: "cds/layers", labelBy: "layer_index" }]}
            traces={[
              { field: "quote/rol_ty/weighted_el", label: "EL", color: "#F7CFEC" },
              { field: "quote/rms_tp_calc/total_coc", label: "Cost of Capital", color: "#6C0D7A" },
              { field: "quote/rms_tp_calc/ri_cost", label: "RI Cost", color: "#0C6122" },
              { field: "quote/rms_tp_calc/expenses_less_inv_income", label: "Expenses less Inv. Inc.", color: "#4FADC7" }
            ]}
            xAxisTickAngle={-45}
            gapBetweenBarsSize={0.05}
            barMode="stack"
            xAxisLabel="Layer"
            yAxisLabel="TP Component"
          />
          <Bar
            title="Technical Premium (GN) - Calculation 2"
            data={[{ list: "cds/layers", labelBy: "layer_index" }]}
            traces={[
              { field: "quote/rol_ty/weighted_el", label: "EL", color: "#F7CFEC" },
              { field: "quote/rms_tp_calc/sd_load", label: "SD Load", color: "#6C0D7A" },
              { field: "quote/rms_tp_calc/expenses_less_inv_income", label: "Expenses", color: "#4FADC7" }
            ]}
            xAxisTickAngle={-45}
            gapBetweenBarsSize={0.05}
            barMode="stack"
            xAxisLabel="Layer"
            yAxisLabel="TP Component"
          />
          <Bar
            title="Technical Premium (GN) - Calculation 3"
            data={[{ list: "cds/layers", labelBy: "layer_index" }]}
            traces={[
              { field: "quote/rol_ty/weighted_el", label: "EL", color: "#F7CFEC" },
              { field: "quote/rms_tp_calc/calc_3_lr_load", label: "LR Load", color: "#6C0D7A" }
            ]}
            xAxisTickAngle={-45}
            gapBetweenBarsSize={0.05}
            barMode="stack"
            xAxisLabel="Layer"
            yAxisLabel="TP Component"
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_quote };