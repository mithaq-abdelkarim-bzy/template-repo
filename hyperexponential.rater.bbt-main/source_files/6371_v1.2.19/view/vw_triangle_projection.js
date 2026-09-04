//########### OUTSTANDING ########################



import * as HX from "hx-model-components";

function vw_triangle_projection(scale) {
  return (

    <HX.Page title="Triangle Projection" fullWidth shownBy="cds/show_hide/page/show_triangle">
      <HX.Section title="Triangle - Beazley Intelligence" defaultCollapsed={true}>
        {/*<HX.TriangleParameters title="Triangle Parameters" triangle="tri_1_loaded_from_bi" with="cds/triangle_projection" syncColumnWidthsKey="align_tri_1" />*/}
        <HX.TriangleData title="Triangle Data" triangle="tri_1_loaded_from_bi" with="cds/triangle_projection" syncColumnWidthsKey="align_tri_1" />
        <HX.Collection fields={[null, null]} />
      </HX.Section>

      <HX.Section title="Triangle - Override" defaultCollapsed={true}>

        <HX.Pane flow="right">
          <HX.Collection fields={["override_triangle_date", "override_triangle_years"]} with="cds/triangle_projection" horizontal />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Button task="tri_override_setup_task" title="Setup Override Triangle" />
          <HX.Collection fields={["async_override_triangle_status"]} with="cds/triangle_projection" horizontal />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={["override_triangle"]} with="cds/triangle_projection" horizontal />
          <HX.Collection fields={["assign_override_triangle_status"]} with="cds/triangle_projection" horizontal />
        </HX.Pane>

        <HX.TriangleData title="Triangle Data" triangle="tri_2_manual_input" with="cds/triangle_projection" syncColumnWidthsKey="align_tri_1" />


      </HX.Section>

      <HX.Section title="Triangle - Selected" defaultCollapsed={false}>
        {/*<HX.TriangleParameters title="Triangle Parameters" triangle="tri_3_selected" with="cds/triangle_projection" syncColumnWidthsKey="align_tri_2" />*/}
        <HX.TriangleData title="Triangle Data" triangle="tri_3_selected" with="cds/triangle_projection" syncColumnWidthsKey="align_tri_2" />
        <HX.TriangleDevFactors title="Triangle Incurred Development Factors" triangle="tri_3_selected" with="cds/triangle_projection" syncColumnWidthsKey="align_tri_2" />
      </HX.Section>


      <HX.Section title="Triangle - Exclusions" defaultCollapsed={true}>

        <HX.Pane flow="right">
          <HX.Button task="tri_exclusions_setup_task" title="Setup Exclusions Triangle For Use" />
          <HX.Pane flow="down">
            <HX.Notes field="cds/triangle_projection/tri_exclusions_setup_task_status" />
            <HX.Notes field="cds/triangle_projection/tri_exclusions_dimensions_status" />
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Collection fields={[null]} />
            <HX.Collection fields={[null]} />
          </HX.Pane>
        </HX.Pane>

        <HX.TriangleData title="Triangle - Exclusions" triangle="tri_3a_exclusions" with="cds/triangle_projection" syncColumnWidthsKey="align_tri_2" />
      </HX.Section>





      <HX.Section title="Triangle - Averages" defaultCollapsed={true}>
        <HX.TriangleAverages title="Triangle Averages" triangle="tri_3_selected" with="cds/triangle_projection" syncColumnWidthsKey="align_tri_2" />
      </HX.Section>

      <HX.Section title="Algorithmic Development and Overrides" defaultCollapsed={false}>
        <HX.Table
          title="Experience Analysis - Incremental Development Factors"
          data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
          fields={["experience_default", "experience_override", "experience_selected"]}
          with="cds/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_idf_row"
        />

        <HX.Table
          title="Benchmarking Assumptions"
          data={["cds/triangle_projection/experience_weight", "cds/triangle_projection/benchmark_name"]}
          fields={["default", "override", "selected"]}
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
        />

        <HX.Collection
          fields={["cds/triangle_projection/benchmark_use_occurrence"]}
          syncColumnWidthsKey="align_tri_2"
        />

        <HX.Table
          title="Blending - Default - Incremental Development Factors"
          data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
          fields={["experience_default", "benchmark_default", "blended_default"]}
          with="cds/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_idf_row"
        />

        <HX.Table
          title="Blending - Selected - Incremental Development Factors"
          data={[{ datum: "incremental_dev_factor", elementLabelBy: "development_label" }, null, "tail_factor"]}
          fields={["experience_selected", "benchmark_selected", "blended_selected"]}
          with="cds/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_idf_row"
        />



        <HX.Table
          title="Blending - Default - Percentage of Ultimate"
          data={[{ datum: "percents_ultimate", elementLabelBy: "percents_label" }]}
          fields={["experience_default_perc_ult", "benchmark_default_perc_ult", "blended_default_perc_ult"]}
          with="cds/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_ult_row"
        />

        <HX.Table
          title="Blending - Selected - Percentage of Ultimate"
          data={[{ datum: "percents_ultimate", elementLabelBy: "percents_label" }]}
          fields={["experience_selected_perc_ult", "benchmark_selected_perc_ult", "blended_selected_perc_ult"]}
          with="cds/triangle_projection"
          kb-interactive
          transpose
          syncColumnWidthsKey="align_tri_2"
          filter="show_ult_row"
        />


      </HX.Section>


      <HX.Section title="Projection" defaultCollapsed={false}>
        <HX.TriangleProjections title="Triangle Projections" triangle="tri_4_result" with="cds/triangle_projection" />
        <HX.TriangleChart title="Triangle Graphing" triangle="tri_4_result" with="cds/triangle_projection" />
      </HX.Section >

    </HX.Page >

  )
}

export { vw_triangle_projection };
