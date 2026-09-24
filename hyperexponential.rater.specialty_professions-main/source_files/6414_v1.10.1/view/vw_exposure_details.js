import * as HX from "hx-model-components";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Rateable Exposure">
        <HX.Pane flow="right">
          <HX.Notes field="cds/currency_label" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Table kb-interactive
            fields={["other_specify", "rateable_exposure_discipline",
              "current_yr_construction_value", "current_yr_professional_fees", "current_yr_rateable_exposure",
              "last_yr_construction_value", "last_yr_professional_fees", "last_yr_rateable_exposure",
              "two_yr_ago_construction_value", "two_yr_ago_professional_fees", "two_yr_ago_rateable_exposure"]}
            data={[
              { datum: "cds/exposure/granular/construction_with_in_house_design" },
              { datum: "cds/exposure/granular/construction_with_sub_contracted_design" },
              { datum: "cds/exposure/granular/design_only_no_construction" },
              { datum: "cds/exposure/granular/construction_only_no_design" },
              { datum: "cds/exposure/granular/at_risk_construction_management" },
              { datum: "cds/exposure/granular/agency_construction_management" },
              { datum: "cds/exposure/granular/other" },
              { datum: "cds/exposure/granular/total" }
            ]}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Underwriter Comments">
        <HX.Notes field="cds/exposure/aggregate/uw_comment" />
      </HX.Section>

      <HX.Section title="Average Rateable Exposure">
        <HX.Pane flow="right">
          <HX.Notes field="cds/currency_label" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Table kb-interactive
            fields={["three_yr_avg_rateable_exposure", "two_yr_avg_rateable_exposure", "current_yr_avg_rateable_exposure",
              "selected_avg_rateable_exposure", "override_avg_rateable_exposure"]}
            data={[
              { datum: "cds/exposure/granular/construction_with_in_house_design" },
              { datum: "cds/exposure/granular/construction_with_sub_contracted_design" },
              { datum: "cds/exposure/granular/design_only_no_construction" },
              { datum: "cds/exposure/granular/construction_only_no_design" },
              { datum: "cds/exposure/granular/at_risk_construction_management" },
              { datum: "cds/exposure/granular/agency_construction_management" },
              { datum: "cds/exposure/granular/other" },
              { datum: "cds/exposure/granular/total" }
            ]}
          />
        </HX.Pane>
      </HX.Section>


    </HX.Page>
  )
}

export { vw_exposure_details };

