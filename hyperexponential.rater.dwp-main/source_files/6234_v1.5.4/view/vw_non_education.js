import * as HX from "hx-model-components";

function vw_non_education(scale) {
  return (
    <HX.Page title="Non Education" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Non Education">
        <HX.Pane>
          <HX.Table data={["cds/exposure/granular/non_education"]}
            fields={[
              "establishment_name",
              "sector/sector",
              "sector/sub_sector",
              "num_of_est",
              "country",
              "state_code",
              "state_name",
              "city_risk",
              "location",
              "footfall_measure",
              "num_of_staff_per_est",
              "footfall_measure_per_est",
              "east_of_access",
              "enclosed_space",
              "num_of_days",
              "num_req_counselling",
              "footfall_band",
              "factor_city_risk",
            ]}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_non_education };