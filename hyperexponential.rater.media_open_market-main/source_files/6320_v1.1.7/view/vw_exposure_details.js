import * as HX from "hx-model-components";
import { media_exposures, music_exposures, tvfilm_exposures, annualtv_genre } from "view/vw_constants";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Exposure Details">

        <HX.Pane shownBy="/cds/standard_rater_masking">
          <HX.Collection fields={["years_in_business", null, null, null]} with="cds/rating_factors" horizontal />
          <HX.Collection fields={["location", "territory_factor", null, null]} with="cds/rating_factors" horizontal />
          <HX.Collection fields={["total_revenue", null, null, null]} with="cds/exposure/aggregate" horizontal />
          <HX.Collection fields={["revenue", "base_rate", null, null]} with="cds/exposure/aggregate/rateable" horizontal />
          <HX.Collection fields={["nonrateable/revenue", "nonrateable/base_rate", "hazard_group", null]} with="cds/exposure/aggregate" horizontal />
        </HX.Pane>

        <HX.Table shownBy="/cds/media_masking"
          title=""
          data={media_exposures()}
          fields={[
            { field: "base_rate", maxWidth: 300 },
            { field: "comment", maxWidth: 900 }
          ]}
          with="cds/exposure/granular/media"
          // filter={"show_row"}
          kb-interactive
        />
        <HX.Table shownBy="/cds/music_masking"
          title=""
          data={music_exposures()}
          fields={[
            { field: "base_rate", maxWidth: 300 },
            { field: "comment", maxWidth: 900 }
          ]}
          with="cds/exposure/granular/music"
          // filter={"show_row"}
          kb-interactive
        />
        <HX.Table shownBy="/cds/tvfilm_masking"
          title=""
          data={tvfilm_exposures()}
          fields={[
            { field: "base_rate", maxWidth: 300 },
            { field: "comment", maxWidth: 900 }
          ]}
          with="cds/exposure/granular/tvfilm"
          // filter={"show_row"}
          kb-interactive
        />

        <HX.Pane shownBy="/cds/individualtv_masking">
          <HX.Collection fields={["location", "territory_factor", null, null]} with="cds/rating_factors" horizontal />
          <HX.Collection fields={["length", "number_of_episodes", null, null]} with="cds/exposure/aggregate/individual_tv" horizontal />
          <HX.Collection fields={["individual_tv/selections/genre", "exposure/aggregate/total_base_premium", null, null]} with="cds" horizontal />
          <HX.Table
            title="Individual TV Modifiers"
            data={[
              { datum: "selections", maxWidth: 400 },
              { datum: "modifiers", maxWidth: 400 }
            ]}
            with="cds/individual_tv"
            fields={[
              { field: "jurisdiction", labelAlign: "left" },
              { field: "policy_period", labelAlign: "left" },
              { field: "soundtrack", labelAlign: "left" },
              { field: "merchandising", labelAlign: "left" },
              { field: "australian", labelAlign: "left" },
              { field: "coverage_basis", labelAlign: "left" },
              { field: "established_format", labelAlign: "left" },
              { field: "primary_broadcast", labelAlign: "left" },
              { field: "lawyers", labelAlign: "left" },
              { field: "webisodes", labelAlign: "left" },
            ]}
            kb-interactive
            transpose
            syncColumnWidthsKey="mySyncedTables1"
          />
        </HX.Pane>

        <HX.Pane shownBy="/cds/annualtv_masking">
          <HX.Collection horizontal syncColumnWidthsKey="mySyncedTables1"
            fields={["location", "territory_factor", null, null]}
            with="cds/rating_factors" />
          <HX.Collection syncColumnWidthsKey="mySyncedTables1"
            fields={["turnover", "annual_budget"]}
            with="cds/annual_tv" />
          <HX.Collection horizontal syncColumnWidthsKey="mySyncedTables1"
            fields={["number_of_productions", "capped_productions"]}
            with="cds/exposure/aggregate/annual_tv" />
          <HX.Table
            title="Genre"
            data={annualtv_genre()}
            with="cds/exposure/granular/annual_tv/genre"
            fields={[
              { field: "perc_of_total_turnover", width: 250 },
              { field: "turnover_amount", width: 180 },
              { field: "alloc_production_number", width: 250 },
              { field: "average_premium", width: 180 },
              { field: "base_premium", width: 180 }]}
            kb-interactive
          // syncColumnWidthsKey="mySyncedTables1"
          />
          <HX.Collection horizontal syncColumnWidthsKey="mySyncedTables1"
            fields={["total_base_premium", null, null, null]}
            with="cds/exposure/aggregate"
          />
          <HX.Table
            title="Annual TV Modifiers"
            data={[
              { datum: "selections", maxWidth: 400 },
              { datum: "modifiers", maxWidth: 400 }
            ]}
            with="cds/annual_tv"
            fields={[
              // { field: "aggregate_limit", labelAlign: "left" },
              // { field: "annual_policy", labelAlign: "left" },
              { field: "jurisdiction", labelAlign: "left" },
              { field: "australian", labelAlign: "left" },
              { field: "lawyers", labelAlign: "left" },
            ]}
            kb-interactive
            transpose
          // syncColumnWidthsKey="mySyncedTables1"
          />
        </HX.Pane>

        <HX.Pane shownBy="/cds/individualfilm_masking">
          <HX.Collection fields={["location", "territory_factor", null, null]} with="cds/rating_factors" horizontal />
          <HX.Collection fields={["individual_film/exhibition", "total_base_premium", null, null]} with="cds/exposure/aggregate" horizontal />
          <HX.Table
            title="Individual Film Modifiers"
            data={[
              { datum: "selections", maxWidth: 400 },
              { datum: "modifiers", maxWidth: 400 }
            ]}
            with="cds/individual_film"
            fields={[
              { field: "budget", labelAlign: "left" },
              { field: "cast", labelAlign: "left" },
              { field: "appeal", labelAlign: "left" },
              { field: "subject_matter", labelAlign: "left" },
              { field: "jurisdiction", labelAlign: "left" },
              { field: "foreign_language", labelAlign: "left" },
              { field: "soundtrack", labelAlign: "left" },
              { field: "merchandising", labelAlign: "left" },
              { field: "policy_period", labelAlign: "left" },
              { field: "australian", labelAlign: "left" },
              { field: "coverage_basis", labelAlign: "left" },
              { field: "established_format", labelAlign: "left" },
              { field: "lawyers", labelAlign: "left" },
            ]}
            kb-interactive
            transpose
            syncColumnWidthsKey="mySyncedTables1"
          />
        </HX.Pane>

      </HX.Section>
    </HX.Page>
  )
}

export { vw_exposure_details };