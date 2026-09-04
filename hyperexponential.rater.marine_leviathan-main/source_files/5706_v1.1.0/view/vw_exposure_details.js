import * as HX from "hx-model-components";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Risk Details" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page" >
      <HX.Section title="Vessel Details">
        <HX.Pane>
          <HX.Table
            data={["number_of_units",
              { datum: "total_sum_insured", labelBy: "total_sum_insured_label" },
              { datum: "average_sum_insured_per_unit", labelBy: "average_sum_insured_label" },
              "excess_per_loss",
              { datum: "benchmark_premium", labelBy: "benchmark_premium_label" }
              ,]}
            fields={[
              { field: "rov", infoBy: "rov_hovertext" },
              "auv", "seismic_towed", "seismic_ocean_bottom", "diving_oceanographic", "submersibles", "other", "total",

            ]}

            with="cds/exposure/granular"
            dynamic
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Excess per loss (AUV)">
        <HX.Collection fields={["normal_ops", null, null, null]}
          with="cds/exposure/granular/excess_per_loss_auv"
          horizontal />
        <HX.Collection fields={["launch_recovery", null, null, null]}
          with="cds/exposure/granular/excess_per_loss_auv"
          horizontal />
      </HX.Section>
      <HX.Section title="Other (Policy-Level) Risk Factors">
        <HX.Pane >
          <HX.Collection fields={["type_of_work", null, null, null]}
            with="cds/exposure/granular"
            horizontal />
          <HX.Collection fields={["ice_debris_other_traffic", null, null, null]}
            with="cds/exposure/granular"
            horizontal />
          <HX.Collection fields={["experience_level", null, null, null]}
            with="cds/exposure/granular"
            horizontal />
          <HX.Collection fields={["usage_factor", null, null, null]}
            with="cds/exposure/granular"
            horizontal />
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_exposure_details };