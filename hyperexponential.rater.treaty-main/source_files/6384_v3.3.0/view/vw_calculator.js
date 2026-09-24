import * as HX from "hx-model-components";

function vw_calculator(scale) {
  return (
    <HX.Page title="Calculator" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Calculator">
        <HX.Table
          data={[
            { datum: "cds/calculator/input_list" },
            null,
            { datum: "cds/calculator/results" }
          ]}
          fields={[
            { field: "el", maxWidth: 400 },
            { field: "sd", maxWidth: 400 }
          ]}
          freezeLeft={0}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Transposer">
        <HX.Table
          title="Modelling Sheet Output"
          data={[
            { datum: "cds/calculator/transposer" },
          ]}
          fields={[
            { field: "el" },
            { field: "sd" }
          ]}
          freezeLeft={0}
          kb-interactive
          transpose
        />
        <HX.Table
          title="Transposed"
          data={[
            { datum: "cds/calculator/transposer" },
          ]}
          fields={[
            { field: "el.read_only_option", maxWidth: 400 },
            { field: "sd.read_only_option", maxWidth: 400 }
          ]}
          freezeLeft={0}
          kb-interactive
        />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_calculator };