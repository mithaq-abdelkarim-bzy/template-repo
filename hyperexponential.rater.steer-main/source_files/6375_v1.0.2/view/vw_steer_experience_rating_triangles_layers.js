// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";
import { createLayersListSelector } from "view/vw_utilities";

// Define the layers to loop through
const layers = [...createLayersListSelector(max_layers())];

function vw_steer_experience_rating_triangles_layers(scale) {
  return (

    <HX.Page title="Triangle Projection Per Layer" fullWidth={true} viewScale={scale * 0.9} shownBy="model_state/show_steer_experience_rating" >
      <HX.Selector
        with="cds/steer/experience_rating/layers"
        data={[...createLayersListSelector(max_layers())]}
        dropdown={"layer_name"} >
        <HX.Section title="Triangle Instructions" defaultCollapsed>
          <HX.Pane flow="right">
            <HX.Notes field="/model_state/triangle_per_layer_instructions" />
          </HX.Pane>
        </HX.Section >

        <HX.Section title="Triangle - Raw Data" defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Collection fields={["triangle_projection/tri_1_basis"]} />
            </HX.Pane>
            <HX.Pane ratio={3}>
              <HX.Collection fields={[null]} />
            </HX.Pane>
          </HX.Pane>
          <HX.TriangleData title="Triangle Data" triangle="tri_1_raw_data" with="triangle_projection" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />

        </HX.Section>

        {/* <HX.Section title="Triangle - Manual Input" defaultCollapsed={true}>

          <HX.Pane flow="right">
            <HX.Collection fields={["override_triangle_date", "override_triangle_years"]} with="triangle_projection" horizontal />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="tri_override_setup_task" title="Setup Override Triangle" />
            <HX.Collection fields={["async_override_triangle_status"]} with="triangle_projection" horizontal />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={["override_triangle"]} with="triangle_projection" horizontal />
            <HX.Collection fields={["assign_override_triangle_status"]} with="triangle_projection" horizontal />
          </HX.Pane>

          <HX.TriangleData title="Triangle Data" triangle="tri_2_manual_input" with="triangle_projection" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />


        </HX.Section> */}

        <HX.Section title="Triangle - Selected" defaultCollapsed={false}>
          {/*<HX.TriangleParameters title="Triangle Parameters" triangle="tri_3_selected" with="triangle_projection" syncColumnWidthsKey="align_tri_2" />*/}
          <HX.TriangleData title="Triangle Data" triangle="tri_3_selected" with="triangle_projection" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />
          <HX.TriangleDevFactors title="Triangle Incurred Development Factors" triangle="tri_3_selected" with="triangle_projection" syncColumnWidthsKey="align_tri_2" />
        </HX.Section>

        <HX.Section title="Triangle - Exclusions" defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Button task="steer_tri_exclusions_setup_task" title="Setup Exclusions Triangle For Use" />
            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Pane flow="down">
                <HX.Notes field="triangle_projection/tri_exclusions_setup_task_status" />
                <HX.Notes field="triangle_projection/tri_exclusions_dimensions_status" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Collection fields={[null]} />
            </HX.Pane>
          </HX.Pane>
          <HX.TriangleData title="Triangle - Exclusions" triangle="tri_3a_exclusions" with="triangle_projection" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />
        </HX.Section>

        <HX.Section title="Triangle - Averages" defaultCollapsed={true}>
          <HX.TriangleAverages title="Triangle Averages" triangle="tri_3_selected" with="triangle_projection" syncColumnWidthsKey="align_tri_2" />
        </HX.Section>

        <HX.Section title="Algorithmic Development and Overrides" defaultCollapsed={false}>
          <HX.Table
            title="Experience Analysis - Incremental Development Factors"
            data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
            fields={["experience_default", "experience_override", "experience_selected"]}
            with="triangle_projection"
            kb-interactive
            transpose
            syncColumnWidthsKey="align_tri_2"
            filter="show_idf_row"
          />

          <HX.Pane flow="right">
            <HX.Pane ratio={1}>

              <HX.Button task="steer_populate_bc_patterns_task" title="Populate Burning Cost Pattern" />

            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Collection fields={["triangle_projection/update_pattern_message"]} shownBy="triangle_projection/is_not_experience_selected_updated" horizontal />

            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Collection fields={[null]} />
            </HX.Pane>
          </HX.Pane>

          {/* <HX.Table
          title="Benchmarking Assumptions"
          data={["triangle_projection/experience_weight", "triangle_projection/benchmark_name"]}
          fields={["default", "override", "selected"]}
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
        />

        <HX.Collection
          fields={["triangle_projection/benchmark_use_occurrence"]}
          syncColumnWidthsKey="align_tri_2"
        />

        <HX.Table
          title="Blending - Default - Incremental Development Factors"
          data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
          fields={["experience_default", "benchmark_default", "blended_default"]}
          with="triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_idf_row"
        />

        <HX.Table
          title="Blending - Selected - Incremental Development Factors"
          data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
          fields={["experience_selected", "benchmark_selected", "blended_selected"]}
          with="triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_idf_row"
        />



        <HX.Table
          title="Blending - Default - Percentage of Ultimate"
          data={[{ datum: "percents_ultimate", elementLabelBy: "percents_label" }]}
          fields={["experience_default_perc_ult", "benchmark_default_perc_ult", "blended_default_perc_ult"]}
          with="cds"layers/
  /triangle_projection        kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_ult_row"
        />

        <HX.Table
          title="Blending - Selected - Percentage of Ultimate"
          data={[{ datum: "percents_ultimate", elementLabelBy: "percents_label" }]}
          fields={["experience_selected_perc_ult", "benchmark_selected_perc_ult", "blended_selected_perc_ult"]}
          with="cds"layers/
  /triangle_projection        kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_ult_row"
        /> */}


        </HX.Section>


        <HX.Section title="Projection" defaultCollapsed={false}>
          <HX.TriangleProjections title="Triangle Projections" triangle="tri_4_result" with="triangle_projection" syncColumnWidthsKey="align_tri_2" />
          <HX.TriangleChart title="Triangle Graphing" triangle="tri_4_result" with="triangle_projection" />
        </HX.Section >
      </HX.Selector>

    </HX.Page >

  )
}


export { vw_steer_experience_rating_triangles_layers };