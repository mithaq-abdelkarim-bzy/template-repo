import * as HX from "hx-model-components";
import { tech_eo_class } from "view/vw_constants";

function vw_tech_eo(scale) {
  return (
    <HX.Page title="Tech E&O" fullWidth={true} viewScale={scale}  >
      {/* shownBy="cds/tech_eo_selection" */}
      <HX.Section title="Tech E&O">

        <HX.Pane flow="right">
          <HX.Collection fields={["cds/exposure/aggregate/tech_eo_rateble_revenue"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Collection fields={["cds/exposure/aggregate/tech_eo_total_revenue"]} />
        </HX.Pane>

        <HX.Pane>
          <HX.Table
            data={tech_eo_class()}
            fields={["tech_eo_percent_rateble_revenue", "tech_eo_class", "tech_eo_revenue"]}
            title="Revenue by Class"
            with="cds/exposure/granular"
            kb-interactive
          />
        </HX.Pane>

      </HX.Section>

      <HX.Section title="Contingent BI/PD" shownBy="cds/glsn_masking">
        <HX.Pane flow="right">
          <HX.Collection
            fields={["cds/rating_factors/tech_eo/contingent_bi_pd", "cds/rating_factors/tech_eo/contingent_bi_pd_factor"]} horizontal >
          </HX.Collection>
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_tech_eo };
