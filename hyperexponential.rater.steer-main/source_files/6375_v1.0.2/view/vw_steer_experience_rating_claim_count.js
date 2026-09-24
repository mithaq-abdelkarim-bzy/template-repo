// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";
import { createLayersList } from "view/vw_utilities";

// Define the layers to loop through
const layers = [...createLayersList(max_layers())];

function vw_steer_experience_rating_claim_count(scale) {
  return (

    <HX.Page title="Claim Count" fullWidth={true} viewScale={scale * 0.9} shownBy="model_state/show_steer_experience_rating">
      <HX.Section title="Triangle Instructions" defaultCollapsed>
        <HX.Pane flow="right">
          <HX.Notes field="model_state/triangle_claim_count_instructions" />
        </HX.Pane>
      </HX.Section >
      <HX.Section title="Claim Count - Raw Data (Incurred only) " defaultCollapsed={true}>
        <HX.TriangleData title="Triangle Data" triangle="tri_1_raw_data" with="cds/steer/experience_rating/layers/fgu/claim_count" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />
      </HX.Section>

      {/* <HX.Section title="Triangle - Manual Input" defaultCollapsed={true}>

        <HX.Pane flow="right">
          <HX.Collection fields={["override_triangle_date", "override_triangle_years"]} with="cds/steer/experience_rating/layers/fgu/claim_count" horizontal />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Button task="steer_tri_count_override_setup_task" title="Setup Override Triangle" />
          <HX.Collection fields={["async_override_triangle_status"]} with="cds/steer/experience_rating/layers/fgu/claim_count" horizontal />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={["override_triangle"]} with="cds/steer/experience_rating/layers/fgu/claim_count" horizontal />
          <HX.Collection fields={["assign_override_triangle_status"]} with="cds/steer/experience_rating/layers/fgu/claim_count" horizontal />
        </HX.Pane>
        <HX.TriangleData title="Triangle Data" triangle="tri_2_manual_input" with="cds/steer/experience_rating/layers/fgu/claim_count" syncColumnWidthsKey="align_tri_2" />
      
      </HX.Section> */}

      <HX.Section title="Claim Count - Selected" defaultCollapsed={false}>
        <HX.TriangleData title="Triangle Data" triangle="tri_3_selected" with="cds/steer/experience_rating/layers/fgu/claim_count" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />
        <HX.TriangleDevFactors title="Triangle Incurred Development Factors" triangle="tri_3_selected" with="cds/steer/experience_rating/layers/fgu/claim_count" syncColumnWidthsKey="align_tri_2" />
      </HX.Section>

      <HX.Section title="Claim Count - Exclusions" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Pane ratio={1}>
            <HX.Button task="steer_tri_count_exclusions_setup_task" title="Setup Exclusions Triangle For Use" />
          </HX.Pane>
          <HX.Pane ratio={1}>
            <HX.Pane flow="down">
              <HX.Notes field="cds/steer/experience_rating/layers/fgu/claim_count/tri_exclusions_setup_task_status" />
              <HX.Notes field="cds/steer/experience_rating/layers/fgu/claim_count/tri_exclusions_dimensions_status" />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane ratio={2}>
            <HX.Collection fields={[null]} />
          </HX.Pane>
        </HX.Pane>
        <HX.TriangleData title="Claim Count - Exclusions" triangle="tri_3a_exclusions" with="cds/steer/experience_rating/layers/fgu/claim_count" syncColumnWidthsKey="align_tri_2" defaultMode="cumulative" />
      </HX.Section>

      <HX.Section title="Claim Count - Averages" defaultCollapsed={true}>
        <HX.TriangleAverages title="Claim Count Averages" triangle="tri_3_selected" with="cds/steer/experience_rating/layers/fgu/claim_count" syncColumnWidthsKey="align_tri_2" />
      </HX.Section>

      <HX.Section title="Algorithmic Development and Overrides" defaultCollapsed={false}>
        <HX.Collection fields={["selected_average_option_input", null, null, null]} with="cds/steer/experience_rating/layers/fgu/claim_count" horizontal syncColumnWidthsKey="align_tri_2" />

        <HX.Table
          title="Experience Analysis - Incremental Development Factors"
          data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
          fields={["experience_default", "experience_override", "experience_selected"]}
          with="cds/steer/experience_rating/layers/fgu/claim_count"
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
            <HX.Collection fields={["claim_count/update_pattern_message"]} shownBy="claim_count/is_not_experience_selected_updated" with="cds/steer/experience_rating/layers/fgu" horizontal />
          </HX.Pane>
          <HX.Pane ratio={2}>
            <HX.Collection fields={[null]} />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Projection" defaultCollapsed={false}>
        <HX.TriangleProjections title="Claim Count Projections" triangle="tri_4_result" with="cds/steer/experience_rating/layers/fgu/claim_count" syncColumnWidthsKey="align_tri_2" />
        <HX.TriangleChart title="Claim Count Graphing" triangle="tri_4_result" with="cds/steer/experience_rating/layers/fgu/claim_count" />
      </HX.Section >

    </HX.Page >

  )
}

export { vw_steer_experience_rating_claim_count };