// v0.3.0
import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_page_risk_info">
      <HX.Section title="Account Details">
        <HX.Pane >
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["cds/standard_fields/underwriter", "cds/risk_info/product_bool"]} horizontal />
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["/cds/currencies/source_currency", "/cds/standard_fields/is_renewal"]} horizontal />
            <HX.Collection fields={[
              "coverages/ec_total/section_reference"
              , { shownBy: "/model_state/show_non_appearance", field: "coverages/na_total/section_reference" }
              , { shownBy: "/model_state/show_event_cancellation", field: null }
            ]} horizontal />
          </HX.With>
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
        </HX.Pane>
      </HX.Section>
      {/* NOTE use the below code if the model does not price multiple layers and it is required to store line size
        brokerage & status on teh risk Information sheet */}
      <HX.Section title="Policy Information" >
        <HX.Pane>
          <HX.Collection fields={["cds/risk_info/event_name"]} horizontal />
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["written_line", "brokerage", "status"]} horizontal />
          </HX.With>
        </HX.Pane>

      </HX.Section>
      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section>

      <HX.Section title="Actuarial">
        <HX.Collection fields={["model_state/show_actuarial"]} horizontal />
        <HX.Collection fields={["cds/standard_fields/rating_methodology"]} horizontal shownBy={"model_state/show_actuarial"} />
        <HX.Collection fields={["schema_view/force_show_view"]} horizontal shownBy={"model_state/show_actuarial"} />
        <HX.Collection fields={["model_state/use_nm_app_old_model"]} horizontal shownBy={"model_state/show_actuarial"} />
        <HX.Collection fields={["model_state/use_determ_agg_calc"]} horizontal shownBy={"model_state/show_actuarial"} />
        <HX.Collection fields={["model_state/is_migrated"]} horizontal shownBy={"model_state/show_actuarial"} />
        <HX.Collection fields={["model_state/disable_validation"]} horizontal shownBy={"model_state/show_actuarial"} />
        {/* <HX.Collection fields={["policy_doc/task_data_dict"]} horizontal shownBy={"model_state/show_actuarial"} />
        <HX.Collection fields={["policy_doc/data_dict"]} horizontal shownBy={"model_state/show_actuarial"} /> */}

      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };


