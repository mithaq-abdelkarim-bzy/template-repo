// v0.3.0
import * as HX from "hx-model-components";

function vw_exposure_rating_national_mourning(scale) {
  return (
    <HX.Page title="National Mourning" fullWidth={true} viewScale={scale} shownBy="model_state/show_page_national_mourning">
      <HX.With context={{ type: "struct", path: "cds/exposure/granular/event_cancel" }} >
        <HX.Section title="Event Cancellation - National Mourning" defaultCollapsed={false}>
          <HX.Collection
            fields={["national_mourning/cover_level", "national_mourning/mourning_period"]}
            horizontal
          />
          <HX.Table
            title="National Mourning - Under 75s"
            data={[
              { datum: "national_mourning/under_75", elementLabelBy: "label" },
            ]}
            fields={["include", "country", "age"
              , "prob_die", "prob_live", "mod_affluence", "mod_health", "prob_die_mod", "prob_live_mod", "check"]}
            dynamic
            kb-interactive
          />
          <HX.Table
            title="National Mourning - 75 and over - note can only add rows from row 3 onward"
            data={[
              { datum: "national_mourning/bespoke_1", elementLabelBy: "label" },
              { datum: "national_mourning/bespoke_2", elementLabelBy: "label" },
              { datum: "national_mourning/over_75", elementLabelBy: "label" },
            ]}
            fields={["include", "name.uw_view", "country.uw_view", "gender.uw_view", "date_of_birth.uw_view", "age"
              , "prob_die", "prob_live", "mod_affluence", "mod_health", "prob_die_mod", "prob_live_mod", "check"]}
            dynamic
            kb-interactive
          />
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_exposure_rating_national_mourning };