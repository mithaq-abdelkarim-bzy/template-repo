import * as HX from "hx-model-components";

function vw_education(scale) {
  return (
    <HX.Page title="Education" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Education">
        <HX.Pane>
          <HX.Table data={["cds/exposure/granular/education"]}
            fields={[
              "institution_name",
              "num_schools",
              "country",
              "state_code",
              "state_name",
              "city_risk",
              "location",
              "school_grade",
              "school_type",
              "boarding_day",
              "num_students",
              "num_employees",
              "sex_of_school",
              "num_req_counselling",
              "factor_city_risk",
            ]}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_education };