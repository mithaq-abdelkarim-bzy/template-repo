import * as HX from "hx-model-components";
import ChoroplethMap from "components/choropleth";

function vw_simulation(scale) {
  return (
    <HX.Page title="Simulation" fullWidth={true} viewScale={scale} shownBy="cds/show_non_risk_xl">

      <HX.Section title="Simulation Summary">
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/layers", maxWidth: 250 }]}
            fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              null,
              "simulation/sim_result/aal",
              "simulation/sim_result/subject_loss",
              null,
              "simulation/sim_result/gross_el_pre_inur",
              "simulation/sim_result/gross_sd_pre_inur",
              null,
              "simulation/sim_result/gross_el",
              "simulation/sim_result/gross_sd",
              null,
              "simulation/sim_result/net_el",
              "simulation/sim_result/net_sd"
            ]}
            freezeLeft={0}
            kb-interactive
            transpose
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Simulation Parameters">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={2}>
            <HX.Collection numCols={2}
              fields={[
                "cds/simulation/max_sims",
                "cds/simulation/sims_commentary",
                "cds/simulation/exposure_increase",
                null,
                "cds/simulation/subject_lae",
                null,
                "cds/simulation/cut_off"
              ]}
              stretch={true}
            />
            <HX.Table
              title="Attritional Sim"
              data={["cds/simulation/attritional_sim"]}
              fields={[
                "mean",
                "sd"
              ]}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right" reflow={false}>
          <HX.Table
            title="FHCF"
            data={["cds/simulation/fhcf_1", "cds/simulation/fhcf_2"]}
            fields={[
              { field: "limit", width: 250 },
              { field: "excess", width: 250 },
              { field: "participation", width: 250 },
              { field: "lae_cap", width: 250 },
              null,
              { field: "el", width: 250 },
              { field: "sd", width: 250 },
            ]}
            kb-interactive
          />
        </HX.Pane>

        <HX.Pane flow="right" reflow={false}>
          <HX.Table
            title="Inuring Layers"
            with="cds/simulation/inuring_ri"
            data={["inur_1", "inur_2", "inur_3", "inur_4"]}
            fields={[
              { field: "limit", width: 250 },
              { field: "excess", width: 250 },
              { field: "placed", width: 250 },
              { field: "deductible_type", width: 250 },
              { field: "reinstatements", width: 250 },
              { field: "inur_lae", width: 250 }
            ]}
            kb-interactive
          />
        </HX.Pane>

      </HX.Section>

      <HX.Section title="File Input">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane>
            <HX.Notes
              field="cds/simulation/format"
              title="ELT/YLT Required Format"
            />
          </HX.Pane>
          <HX.Pane>
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.File field="cds/simulation/files/input_file_1" title="Input File" />
          <HX.File field="cds/simulation/files/input_file_2" title="Input File" />
          <HX.File field="cds/simulation/files/input_file_3" title="Input File" />
          <HX.File field="cds/simulation/files/input_file_4" title="Input File" />
          <HX.File field="cds/simulation/files/input_file_5" title="Input File" />
          <HX.File field="cds/simulation/files/input_file_6" title="Input File" />
          <HX.File field="cds/simulation/files/input_file_7" title="Input File" />
          <HX.File field="cds/simulation/files/input_file_8" title="Input File" />
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Button task="file_processing_task" title="Load Tables" />
          <HX.Button task="run_simulation_task" title="Run Simulation" />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            title="Table List"
            data={["cds/simulation/file_list"]}
            fields={[
              "file_name",
              "table_type",
              "max_sims",
              "table_el",
              "description",
              null,
              "qualifying_excess",
              "qualifying_limit",
              null,
              "fhcf_1",
              "fhcf_2",
              null,
              "inur_1",
              "inur_2",
              "inur_3",
              "inur_4"
            ]}
            kb-interactive
          />
        </HX.Pane>
        <HX.Table
          title="Table Run Selection"
          data={[{ datum: "cds/layers", width: 250 }]}
          fields={[
            "limit.read_only_option",
            "excess.read_only_option",
            null,
            "simulation/run_layer",
            //"simulation/include_combined_layer_1",
            //"simulation/include_combined_layer_2",
            null,
            { field: "simulation/sim_coverage/coverage_1" },
            { field: "simulation/sim_coverage/coverage_2" },
            { field: "simulation/sim_coverage/coverage_3" },
            { field: "simulation/sim_coverage/coverage_4" },
            { field: "simulation/sim_coverage/coverage_5" },
            { field: "simulation/sim_coverage/coverage_6" },
            { field: "simulation/sim_coverage/coverage_7" },
            { field: "simulation/sim_coverage/coverage_8" }
          ]}
          freezeLeft={0}
          kb-interactive
          transpose
        />

      </HX.Section>
      <HX.Section title="Total PML Comparison">
        <HX.Pane>
          <HX.Table
            title="OEP Curve Comparison"
            with="cds/simulation/pml_comparison"
            data={["rp_labels", null, "simulation_gross", "simulation_net_inur", null, "model_gross", "model_net_inur", null, "difference_gross", "difference_net_inur"]}
            fields={[
              "rp_10000",
              "rp_5000",
              "rp_1000",
              "rp_500",
              "rp_250",
              "rp_200",
              "rp_100",
              "rp_50",
              "rp_25",
              "rp_10",
              "rp_5",
              "rp_2"
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="AEP Curve Comparison"
            with="cds/simulation/pml_comparison"
            data={["rp_labels", null, "simulation_gross_aep", "simulation_net_inur_aep", null, "model_gross_aep", "model_net_inur_aep", null, "difference_gross_aep", "difference_net_inur_aep"]}
            fields={[
              "rp_10000",
              "rp_5000",
              "rp_1000",
              "rp_500",
              "rp_250",
              "rp_200",
              "rp_100",
              "rp_50",
              "rp_25",
              "rp_10",
              "rp_5",
              "rp_2",
              null,
              "aal"
            ]}
            transpose
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Table PML Curves">
        <HX.Pane>
          <HX.Table
            title="OEP Curves"
            data={["cds/simulation/file_list"]}
            fields={[
              "description.read_only_option",
              null,
              "curve/rp_10000",
              "curve/rp_5000",
              "curve/rp_1000",
              "curve/rp_500",
              "curve/rp_250",
              "curve/rp_200",
              "curve/rp_100",
              "curve/rp_50",
              "curve/rp_25",
              "curve/rp_10",
              "curve/rp_5",
              "curve/rp_2",
              null,
              "aal"
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="AEP Curves"
            data={["cds/simulation/file_list"]}
            fields={[
              "description.read_only_option",
              null,
              "curve_aep/rp_10000",
              "curve_aep/rp_5000",
              "curve_aep/rp_1000",
              "curve_aep/rp_500",
              "curve_aep/rp_250",
              "curve_aep/rp_200",
              "curve_aep/rp_100",
              "curve_aep/rp_50",
              "curve_aep/rp_25",
              "curve_aep/rp_10",
              "curve_aep/rp_5",
              "curve_aep/rp_2",
              null,
              "aal"
            ]}
            transpose
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="RMS Map">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Table
              data={["cds/simulation/choropleth_map", null, "cds/simulation/choropleth_caribbean", null, "cds/simulation/choropleth_other", null, "cds/simulation/total"]}
              fields={[
                "state",
                "value"
              ]}
              freezeLeft={0}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane>
            <ChoroplethMap
              title="AAL by State"
              list="cds/simulation/choropleth_map"
              text="hi"
              locations="state"
              z="value"
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Peril-Layer">
        <HX.Pane>
          <HX.Table
            title="EL Percentage"
            data={[{ datum: "cds/layers" }]}
            fields={[
              "layer_structure",
              null,
              { field: "peril_allocation/simulation_perc/gross_table_0", labelBy: "/cds/simulation/table_labels/gross_table_0" },
              { field: "peril_allocation/simulation_perc/gross_table_1", labelBy: "/cds/simulation/table_labels/gross_table_1" },
              { field: "peril_allocation/simulation_perc/gross_table_2", labelBy: "/cds/simulation/table_labels/gross_table_2" },
              { field: "peril_allocation/simulation_perc/gross_table_3", labelBy: "/cds/simulation/table_labels/gross_table_3" },
              { field: "peril_allocation/simulation_perc/gross_table_4", labelBy: "/cds/simulation/table_labels/gross_table_4" },
              { field: "peril_allocation/simulation_perc/gross_table_5", labelBy: "/cds/simulation/table_labels/gross_table_5" },
              { field: "peril_allocation/simulation_perc/gross_table_6", labelBy: "/cds/simulation/table_labels/gross_table_6" },
              { field: "peril_allocation/simulation_perc/gross_table_7", labelBy: "/cds/simulation/table_labels/gross_table_7" }
            ]}
            freezeLeft={0}
            kb-interactive
            syncColumnWidthsKey="peril_layer_tables"
          />
          <HX.Table
            title="EL $"
            data={[{ datum: "cds/layers" }]}
            fields={[
              "layer_structure",
              null,
              { field: "peril_allocation/simulation_dollar/gross_table_0", labelBy: "/cds/simulation/table_labels/gross_table_0" },
              { field: "peril_allocation/simulation_dollar/gross_table_1", labelBy: "/cds/simulation/table_labels/gross_table_1" },
              { field: "peril_allocation/simulation_dollar/gross_table_2", labelBy: "/cds/simulation/table_labels/gross_table_2" },
              { field: "peril_allocation/simulation_dollar/gross_table_3", labelBy: "/cds/simulation/table_labels/gross_table_3" },
              { field: "peril_allocation/simulation_dollar/gross_table_4", labelBy: "/cds/simulation/table_labels/gross_table_4" },
              { field: "peril_allocation/simulation_dollar/gross_table_5", labelBy: "/cds/simulation/table_labels/gross_table_5" },
              { field: "peril_allocation/simulation_dollar/gross_table_6", labelBy: "/cds/simulation/table_labels/gross_table_6" },
              { field: "peril_allocation/simulation_dollar/gross_table_7", labelBy: "/cds/simulation/table_labels/gross_table_7" }
            ]}
            freezeLeft={0}
            kb-interactive
            syncColumnWidthsKey="peril_layer_tables"
          />
          <HX.Table
            title="STD $ (NB: Where tables are not independent (event overlap), sum of variances will not equal total variance.)"
            data={[{ datum: "cds/layers" }]}
            fields={[
              "layer_structure",
              null,
              { field: "peril_allocation/simulation_std_dollar/gross_table_0", labelBy: "/cds/simulation/table_labels/gross_table_0" },
              { field: "peril_allocation/simulation_std_dollar/gross_table_1", labelBy: "/cds/simulation/table_labels/gross_table_1" },
              { field: "peril_allocation/simulation_std_dollar/gross_table_2", labelBy: "/cds/simulation/table_labels/gross_table_2" },
              { field: "peril_allocation/simulation_std_dollar/gross_table_3", labelBy: "/cds/simulation/table_labels/gross_table_3" },
              { field: "peril_allocation/simulation_std_dollar/gross_table_4", labelBy: "/cds/simulation/table_labels/gross_table_4" },
              { field: "peril_allocation/simulation_std_dollar/gross_table_5", labelBy: "/cds/simulation/table_labels/gross_table_5" },
              { field: "peril_allocation/simulation_std_dollar/gross_table_6", labelBy: "/cds/simulation/table_labels/gross_table_6" },
              { field: "peril_allocation/simulation_std_dollar/gross_table_7", labelBy: "/cds/simulation/table_labels/gross_table_7" }
            ]}
            freezeLeft={0}
            kb-interactive
            syncColumnWidthsKey="peril_layer_tables"
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Results For Copy">
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/layers" }]}
            fields={[
              { field: "simulation/sim_result/gross_el", width: 250 },
              { field: "simulation/sim_result/gross_sd", width: 250 }
            ]}
            freezeLeft={0}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

    </HX.Page >
  )
}

export { vw_simulation };