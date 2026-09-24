// v0.3.0
import * as HX from "hx-model-components";

function vw_exposure_rating_non_appearance(scale) {
  return (
    <HX.Page title="Non Appearance" fullWidth={true} viewScale={scale} shownBy="model_state/show_page_non_appearance">
      <HX.With context={{ type: "struct", path: "cds/exposure/granular/non_appearance" }} >
        <HX.Section title="Non Appearance">
          <HX.Collection horizontal fields={["genre", "base_rate"]} title="Exposure Measure" />
          <HX.Collection horizontal fields={["num_shows", null]} />
          <HX.Collection horizontal fields={["avg_show_value", null]} />
          <HX.Collection horizontal fields={["agg_show_value", null]} />
          <HX.Collection horizontal fields={["el_fgu", null]} />


          <HX.Collection horizontal fields={["num_band_members", "num_band_members_mod"]} title="Objective Modifiers" />
          <HX.Collection horizontal fields={["claim_experience", "claim_experience_mod"]} />
          <HX.Collection horizontal fields={[null, "nmp_mod"]} />
          <HX.Collection horizontal fields={["el_fgu_mod", "total_mod"]} />
          <HX.Collection horizontal fields={["fl_curve", null]} />


          <HX.Collection horizontal fields={["uw_adj_min", "uw_adj_sel", "uw_adj_max", "uw_adj_fin"]} title="UW Adjustments" />
          <HX.Notes field={"uw_comment"} title="UW Comment" />
        </HX.Section>

      </HX.With>
    </HX.Page>
  )
}

export { vw_exposure_rating_non_appearance };