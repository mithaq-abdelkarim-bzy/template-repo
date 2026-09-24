// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";
import { createLayersList } from "view/vw_utilities";

// Define the layers to loop through
const layers = [...createLayersList(max_layers())];

function vw_steer_experience_rating_triangles(scale) {
  return (

    <HX.Page title="Triangle Projection" fullWidth={true} viewScale={scale * 0.9} shownBy="model_state/show_steer_experience_rating">
      <HX.Section title="Triangle Instructions" defaultCollapsed>
        <HX.Pane flow="right">
          <HX.Notes field="model_state/triangle_fgu_instructions" />
        </HX.Pane>
      </HX.Section >
      <HX.Section title="Triangle - Raw Data" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Pane ratio={1}>
            <HX.Collection fields={["cds/steer/experience_rating/layers/fgu/triangle_projection/tri_1_basis"]} />
          </HX.Pane>
          <HX.Pane ratio={3}>
            <HX.Collection fields={[null]} />
          </HX.Pane>
        </HX.Pane>
        <HX.TriangleData title="Triangle Data" triangle="tri_1_raw_data" with="cds/steer/experience_rating/layers/fgu/triangle_projection" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />
      </HX.Section>

      <HX.Section title="Triangle - Manual Input" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Collection fields={["override_triangle_date", "override_triangle_years", null, null]} with="cds/steer/experience_rating/layers/fgu/triangle_projection" horizontal />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Pane ratio={1}>
            <HX.Button task="steer_tri_override_setup_task" title="Setup Override Triangle" />
          </HX.Pane>
          <HX.Pane ratio={3}>
            <HX.Collection fields={["async_override_triangle_status", null, null]} with="cds/steer/experience_rating/layers/fgu/triangle_projection" horizontal />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={["override_triangle", "assign_override_triangle_status", null, null]} with="cds/steer/experience_rating/layers/fgu/triangle_projection" horizontal />
        </HX.Pane>
        <HX.TriangleData title="Triangle Data" triangle="tri_2_manual_input" with="cds/steer/experience_rating/layers/fgu/triangle_projection" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />
      </HX.Section>

      <HX.Section title="Triangle - Selected" defaultCollapsed={false}>
        <HX.TriangleData title="Triangle Data" triangle="tri_3_selected" with="cds/steer/experience_rating/layers/fgu/triangle_projection" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />
        <HX.TriangleDevFactors title="Triangle Incurred Development Factors" triangle="tri_3_selected" with="cds/steer/experience_rating/layers/fgu/triangle_projection" syncColumnWidthsKey="align_tri_2" />
      </HX.Section>

      <HX.Section title="Triangle - Exclusions" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Pane ratio={1}>
            <HX.Button task="steer_tri_exclusions_setup_task" title="Setup Exclusions Triangle For Use" />
          </HX.Pane>
          <HX.Pane ratio={1}>
            <HX.Pane flow="down">
              <HX.Notes field="cds/steer/experience_rating/layers/fgu/triangle_projection/tri_exclusions_setup_task_status" />
              <HX.Notes field="cds/steer/experience_rating/layers/fgu/triangle_projection/tri_exclusions_dimensions_status" />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane ratio={2}>
            <HX.Collection fields={[null]} />
          </HX.Pane>
        </HX.Pane>
        <HX.TriangleData title="Triangle - Exclusions" triangle="tri_3a_exclusions" with="cds/steer/experience_rating/layers/fgu/triangle_projection" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />
      </HX.Section>

      <HX.Section title="Triangle - Averages" defaultCollapsed={true}>
        <HX.TriangleAverages title="Triangle Averages" triangle="tri_3_selected" with="cds/steer/experience_rating/layers/fgu/triangle_projection" syncColumnWidthsKey="align_tri_2" />
      </HX.Section>

      <HX.Section title="Algorithmic Development and Overrides" defaultCollapsed={false}>
        <HX.Collection fields={["selected_average_option_input", null, null, null]} with="cds/steer/experience_rating/layers/fgu/triangle_projection" horizontal syncColumnWidthsKey="align_tri_2" />
        <HX.Table
          title="Experience Analysis - Incremental Development Factors"
          data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
          fields={["experience_default", "experience_override", "experience_selected"]}
          with="cds/steer/experience_rating/layers/fgu/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_idf_row"
        />
        <HX.Pane flow="right">
          <HX.Pane ratio={1}>
            <HX.Button task="steer_populate_bc_patterns_task" title="Update Burning Cost Pattern" />
          </HX.Pane>
          <HX.Pane ratio={1}>
            <HX.Collection fields={["triangle_projection/update_pattern_message"]} shownBy="triangle_projection/is_not_experience_selected_updated" with="cds/steer/experience_rating/layers/fgu" horizontal />
          </HX.Pane>
          <HX.Pane ratio={2}>
            <HX.Collection fields={[null]} />
          </HX.Pane>
        </HX.Pane>

        {/* <HX.Table
          title="Benchmarking Assumptions"
          data={["cds/steer/experience_rating/layers/fgu/triangle_projection/experience_weight", "cds/steer/experience_rating/layers/fgu/triangle_projection/benchmark_name"]}
          fields={["default", "override", "selected"]}
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
        />

        <HX.Collection
          fields={["cds/steer/experience_rating/layers/fgu/triangle_projection/benchmark_use_occurrence"]}
          syncColumnWidthsKey="align_tri_2"
        />

        <HX.Table
          title="Blending - Default - Incremental Development Factors"
          data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
          fields={["experience_default", "benchmark_default", "blended_default"]}
          with="cds/steer/experience_rating/layers/fgu/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_idf_row"
        />

        <HX.Table
          title="Blending - Selected - Incremental Development Factors"
          data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
          fields={["experience_selected", "benchmark_selected", "blended_selected"]}
          with="cds/steer/experience_rating/layers/fgu/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_idf_row"
        />


        <HX.Table
          title="Blending - Default - Percentage of Ultimate"
          data={[{ datum: "percents_ultimate", elementLabelBy: "percents_label" }]}
          fields={["experience_default_perc_ult", "benchmark_default_perc_ult", "blended_default_perc_ult"]}
          with="cds/steer/experience_rating/layers/fgu/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_ult_row"
        />

        <HX.Table
          title="Blending - Selected - Percentage of Ultimate"
          data={[{ datum: "percents_ultimate", elementLabelBy: "percents_label" }]}
          fields={["experience_selected_perc_ult", "benchmark_selected_perc_ult", "blended_selected_perc_ult"]}
          with="cds/steer/experience_rating/layers/fgu/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_ult_row"
        /> */}
      </HX.Section>

      <HX.Section title="Projection" defaultCollapsed={false}>
        <HX.TriangleProjections title="Triangle Projections" triangle="tri_4_result" with="cds/steer/experience_rating/layers/fgu/triangle_projection" syncColumnWidthsKey="align_tri_2" />
        <HX.TriangleChart title="Triangle Graphing" triangle="tri_4_result" with="cds/steer/experience_rating/layers/fgu/triangle_projection" />
      </HX.Section >

    </HX.Page >
  )
}


export { vw_steer_experience_rating_triangles };