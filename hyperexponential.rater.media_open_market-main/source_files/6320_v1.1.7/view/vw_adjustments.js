import * as HX from "hx-model-components";
import { media_schedule_mods, music_schedule_mods, tvfilm_schedule_mods, optional_coverages } from "view/vw_constants";

function vw_adjustments(scale) {
  return (
    <HX.Page title="Adjustments" fullWidth={true} viewScale={scale} shownBy="cds/standard_rater_masking">

      <HX.Section title="Longevity and Experience Factors">
        <HX.Pane>
          <HX.Collection fields={["longevity_factor", null, null]} horizontal with="cds/modifiers" />
          <HX.Collection title="Experience Factor" fields={["response", "selected", "min", "max"]} horizontal with="cds/modifiers/experience_factor" />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Schedule Rating">
        <HX.Pane>
          <HX.Table shownBy="/cds/media_masking"
            data={media_schedule_mods()}
            fields={[{ field: "selected", width: 180 }, { field: "min", width: 180 }, { field: "max", width: 180 }]}
            with="cds/modifiers/media"
            kb-interactive
          />
          <HX.Table shownBy="/cds/music_masking"
            data={music_schedule_mods()}
            fields={[{ field: "selected", width: 180 }, { field: "min", width: 180 }, { field: "max", width: 180 }]}
            with="cds/modifiers/music"
            kb-interactive
          />
          <HX.Table shownBy="/cds/tvfilm_masking"
            data={tvfilm_schedule_mods()}
            fields={[{ field: "selected", width: 180 }, { field: "min", width: 180 }, { field: "max", width: 180 }]}
            with="cds/modifiers/tvfilm"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Optional Coverages">
        <HX.Pane>
          <HX.Table //title="Optional Coverages"
            data={optional_coverages()}
            fields={["included", "selected", "min", "max", "comment"]}
            with="cds/modifiers/optional_coverages"
            kb-interactive
          />
          <HX.Collection title="Extended Reporting Period"
            fields={["length", "factor"]}
            horizontal
            with="cds/modifiers/extended_reporting_period"
          />
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_adjustments };