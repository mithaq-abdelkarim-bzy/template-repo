// v0.3.0
import * as HX from "hx-model-components";
import EditableText from "components/text_box_editable";

function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">
      <HX.Section title="Account Details">
        <HX.Pane >
          <HX.Collection
            fields={[
              { field: "inception_date", infoBy: "/cds/hover_info/inception_date" },
              "expiry_date",
            ]}
            with="hx_core"
            horizontal
          />
          <HX.Collection fields={["underwriter", "benchmark_class"]} with="cds/standard_fields" horizontal />
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          <HX.Collection fields={["cds/standard_fields/policy_reference", "cds/currencies/source_currency", "cds/standard_fields/is_renewal"]} horizontal />
        </HX.Pane>
      </HX.Section>
      {/* NOTE use the below code if the model does not price multiple layers and it is required to store line size
        brokerage & status on teh risk Information sheet */}
      {/* <HX.Section title="Policy Information" >
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["written_line", "brokerage", "status"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section> */}
      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section>
      <HX.Section title="Coverage">
        <HX.Collection fields={["cds/profession", "cds/retro_date"]} horizontal />
        <HX.Collection fields={["cds/lawyers_num_attorneys_full", "cds/lawyers_num_attorneys_fte"]} horizontal shownBy="cds/profession_lawyers_bool" />
      </HX.Section>
      <HX.Section title="Comments">
        <EditableText textNode="cds/risk_comments" />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };
