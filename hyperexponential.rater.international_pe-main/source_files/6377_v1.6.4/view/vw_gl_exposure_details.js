import * as HX from "hx-model-components";
import { mediatech_industry_list, mediatech_schedule_list } from "view/vw_constants";

function vw_gl_exposure_details(scale) {
  return (
    <HX.Page title="Exposure GL" fullWidth={true} viewScale={scale} shownBy="cds/gl_coverage_selection">
      <HX.Section title="Exposure Information">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "cds/rating_factors/gl_territory/input_value"]} />
          <HX.Collection fields={[
            "cds/exposure/granular/gl_product"]} />
          <HX.Collection fields={[
            { field: "cds/exposure/granular/gl_exposure_info/occupation" }]} />
          <HX.Pane></HX.Pane>
          <HX.Pane></HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Revenue Tiers">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/local_currency_output"]} />
          <HX.Collection fields={[
            { field: "cds/gl_tier_notes/show_box" }]} />
          <HX.Pane></HX.Pane>
          <HX.Pane></HX.Pane>
          <HX.Pane></HX.Pane>
        </HX.Pane>
        <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
          <HX.Table
            title=" "
            data={["gl_revenue"]}
            fields={[{ field: "tier_input", width: 250 }, { field: "revenue_input", width: 250, labelBy: "/cds/gl_revenue_currency_label" }, { field: "revenue_input_usd", width: 250 }, { field: "exposure_type", width: 250 }]}
            kb-interactive
          />
          <HX.Pane flow="right">
            <HX.Collection fields={[
              { field: "/cds/exposure/aggregate/gl_revenue", labelBy: "/cds/gl_revenue_total_currency_label" }]} />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
        </HX.With>
      </HX.Section>
      <HX.Section title="Additional Coverages">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            { field: "/cds/rating_factors/gl_excess_primary/input_value" }]} />
          <HX.Pane></HX.Pane>
          <HX.Pane></HX.Pane>
          <HX.Pane></HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Loss Experience">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            { field: "cds/rating_factors/gl_loss/input_value" }]} />
          <HX.Collection fields={[
            { field: "cds/rating_factors/gl_loss/relativity" }]} />
          <HX.Pane></HX.Pane>
          <HX.Pane></HX.Pane>
          <HX.Pane></HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="UW Judgement (risk based)">
        <HX.Table
          title=" "
          data={["gl_uw_adjustment"]}
          fields={[{ field: "input_value", width: 250 }, { field: "min_value", width: 250 }, { field: "max_value", width: 250 }, { field: "applied_value", width: 250 }]}
          with="cds/modifiers"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Product Tiers Information" shownBy="cds/gl_tier_notes/show_box">
        <HX.Notes field="cds/gl_tier_notes/text_box" />
      </HX.Section>

    </HX.Page >
  )
}

export { vw_gl_exposure_details };