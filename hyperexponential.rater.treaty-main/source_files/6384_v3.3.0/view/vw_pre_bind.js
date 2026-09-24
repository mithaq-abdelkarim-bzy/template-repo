import * as HX from "hx-model-components";

function vw_pre_bind(scale) {
  return (
    <HX.Page title="Pre Bind" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Pre Bind">
        <HX.Collection
          numCols={3}
          fields={[
            "cds/standard_fields/insured_name.read_only_option",
            "cds/standard_fields/underwriter.read_only_option"
          ]}
        />
        <HX.Pane>
          <HX.Table
            title=' By signing below I confirm that the answer to all of the following questions is "Yes": '
            data={["cds/pre_bind/question", { datum: "cds/pre_bind/answer", width: 100 }]}
            fields={[
              { field: "q_1", labelAlign: "left" },
              { field: "q_2", labelAlign: "left" },
              { field: "q_3", labelAlign: "left" },
              { field: "q_4", labelAlign: "left" },
              { field: "q_5", labelAlign: "left" },
              { field: "q_6", labelAlign: "left" },
              { field: "q_7", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
        </HX.Pane>
        <HX.Collection
          numCols={1}
          fields={[
            "cds/pre_bind/uw_signature",
            "cds/pre_bind/date"
          ]}
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_pre_bind };