import * as HX from "hx-model-components";
import { mediatech_industry_list, mediatech_schedule_list } from "view/vw_constants";

function vw_mediatech_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Media Tech" fullWidth={true} viewScale={scale} shownBy="cds/mediatech_coverage_selection">
      <HX.Section title="Exposure Information">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "cds/rating_factors/mediatech_territory/input_value"]} />
          <HX.Collection fields={[
            { field: "cds/exposure/aggregate/mediatech_revenue", labelBy: "/cds/mediatech_revenue_currency_label" }]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Revenue Split by Industry">
        <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
          <HX.Pane flow="right">
            <HX.Collection fields={["mediatech_total_revenue_pct"]} />
            <HX.Button task="clear_mediatech_input_task" title="Clear All the Input of Revenue %"></HX.Button>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
          <HX.Table
            title=" "
            syncColumnWidthsKey="mySyncedTables1"
            data={mediatech_industry_list()}
            fields={[{ field: "input_pct", width: 250 }, { field: "revenue_amount", width: 250 }, { field: "class_name", width: 250 }]}
            kb-interactive
          />
        </HX.With>
      </HX.Section>
      <HX.Section title="Optional Coverage">
        <HX.Table
          title=" "
          data={["mediatech_bipd"]}
          fields={[{ field: "input_value", width: 250 }, { field: "input_relativity", width: 250 },
          { field: "min_rel", width: 250 }, { field: "max_rel", width: 250 }, { field: "applied_rel", width: 250 }]}
          with="cds/modifiers"
        />
      </HX.Section>

      <HX.Section title="Retroactivity" >
        <HX.With context={{ type: "struct", path: "cds/rating_factors" }}>
          <HX.Pane flow="right">
            <HX.Collection fields={["mediatech_prior_acts/coverage"]} />
            <HX.Collection fields={["mediatech_prior_acts/retroactive_date"]} shownBy="mediatech_prior_acts/shown_by" />
            <HX.Collection fields={["mediatech_prior_acts/relativity"]} />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
        </HX.With>
      </HX.Section>
      <HX.Section title="Longevity" >
        <HX.With context={{ type: "struct", path: "cds/rating_factors" }}>
          <HX.Pane flow="right">
            <HX.Collection fields={["mediatech_longevity/business_years"]} />
            <HX.Collection fields={["mediatech_longevity/relativity"]} />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
        </HX.With>
      </HX.Section>
      <HX.Section title="Claims Experience" >
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/rating_factors/mediatech_cost_included/cost_included"]} />
          <HX.Collection fields={["cds/rating_factors/mediatech_cost_included/relativity"]} />
          <HX.Pane></HX.Pane>
          <HX.Pane></HX.Pane>
        </HX.Pane>
        <HX.Table
          title=" "
          data={["mediatech_claim_experience"]}
          fields={[{ field: "input_value", width: 250 }, { field: "input_relativity", width: 250 },
          { field: "min_rel", width: 250 }, { field: "max_rel", width: 250 }, { field: "applied_rel", width: 250 }]}
          with="cds/modifiers"
        />

      </HX.Section>
      <HX.Section title="Schedule Rating" >
        <HX.Table
          title=" "
          data={mediatech_schedule_list()}
          fields={[{ field: "input_value", width: 250 }, { field: "min_val", width: 250 }, { field: "max_val", width: 250 }, { field: "applied_val", width: 250 }]}
          with="cds/modifiers"
        />
      </HX.Section>

    </HX.Page >
  )
}

export { vw_mediatech_exposure_details };