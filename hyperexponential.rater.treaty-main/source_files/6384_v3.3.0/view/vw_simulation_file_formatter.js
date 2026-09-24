import * as HX from "hx-model-components";

function vw_simulation_file_formatter(scale) {
  return (
    <HX.Page title="ELT / YLT File Formatter" fullWidth={true} viewScale={scale} shownBy="cds/show_non_risk_xl">

      <HX.Section title="File Formatting">
        <HX.Pane flow="right" reflow={false}>
          <HX.Notes
            field="cds/simulation/format"
            title="ELT/YLT Required Format"
          />
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.File field="cds/simulation/file_formatter/input_file" title="Input File" />
          </HX.Pane>
          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>
        <HX.Pane>
          <HX.Button task="file_formatter_read_task" title="Read Input File" />
          <HX.Table
            title="Table Run Selection"
            data={[{ datum: "cds/simulation/file_formatter/file_column_names" }, null, { datum: "cds/simulation/file_formatter/override_column_names" }]}
            fields={[
              { field: "column_1" },
              { field: "column_2" },
              { field: "column_3" },
              { field: "column_4" },
              { field: "column_5" },
              { field: "column_6" },
              { field: "column_7" },
              { field: "column_8" },
              { field: "column_9" },
              { field: "column_10" }
            ]}
            freezeLeft={0}
            kb-interactive
          />

          <HX.Button task="file_formatter_write_task" title="Clean Columns" />
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.File field="cds/simulation/file_formatter/output_file" title="Output File" />
          </HX.Pane>
          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>

      </HX.Section>

    </HX.Page >
  )
}

export { vw_simulation_file_formatter };