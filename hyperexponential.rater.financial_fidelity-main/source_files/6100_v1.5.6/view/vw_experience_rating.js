/* eslint-disable */
import * as HX from "hx-model-components";

function vw_experience_rating() {
  return (
    <HX.Page title="Experience Rating" fullWidth shownBy="model_state/show_after_landing_page" >
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Experience Rating">
          <HX.Table kb-interactive
            data={["/cds/experience_rating/claims", null, "/cds/experience_rating/total"]}
            fields={["date", "loss", "coverage", "limited_coverage", "limited_deductible", "net_direct_loss_incurred", "exceeds_500k", "adjusted_loss"]}
          />
        </HX.Section>
        <HX.Section title="Excess Rating">
          <HX.Collection fields={[
            "/cds/experience_rating/eligible_for_excess_experience_mod",
            { field: "/cds/experience_rating/use_excess_experience_mod", shownBy: "/cds/experience_rating/eligible_for_excess_experience_mod" }
          ]} horizontal />
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_experience_rating };
