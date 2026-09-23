import * as HX from "hx-model-components";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} viewScale={scale} shownBy="cds/exposure_masking">

      <HX.Section title="Total Base Premium">
        <HX.Pane flow="right">
          <HX.Pane />
          <HX.Pane />
          <HX.Collection shownBy="cds/gmm_masking"
            fields={[
              {
                field: "cds/rating_factors/mix_of_exposure_measures_message",
                shownBy: "cds/rating_factors/exposure_measures_message_show"
              },
              "cds/show_prior_exposure_years",
              {
                field: "cds/exposure/aggregate/gmm_total_base_premium_one_years_ago",
                infoBy: "cds/exposure/aggregate/gmm_total_base_premium_one_years_ago_info_by",
              },
              "cds/exposure/aggregate/gmm_total_base_premium_current_year"]} horizontal />

        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Pane />
          <HX.Pane />
          <HX.Collection shownBy="cds/glsn_masking"
            fields={[{ field: "cds/rating_factors/mix_of_exposure_measures_message", shownBy: "cds/rating_factors/exposure_measures_message_show" },
              "cds/show_prior_exposure_years",
              "cds/rating_factors/glsn/size_discount_selection",
            {
              field: "cds/exposure/aggregate/glsn_total_base_premium_one_years_ago",
              infoBy: "cds/exposure/aggregate/glsn_total_base_premium_one_years_ago_info_by",
            },
              "cds/exposure/aggregate/glsn_total_base_premium_current_year"]} horizontal />
        </HX.Pane>


      </HX.Section>

      <HX.Section title="Primary Exposure Class">
        <HX.Pane>
          <HX.Table shownBy="cds/gmm_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={["cds/exposure/granular/gmm_primary_exposure_details"]}
            fields={["exposure_class",
              "exposure_measure",
              "formatted_base_rate",
              { field: "five_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/five_years_ago_label" },
              { field: "four_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/four_years_ago_label" },
              { field: "three_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/three_years_ago_label" },
              { field: "two_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/two_years_ago_label" },
              { field: "one_years_ago", labelBy: "cds/rating_factors/one_years_ago_label" },
              { field: "current_year", labelBy: "cds/rating_factors/current_year_label" },
              "selection",
              "base_premium"
            ]}
            filter={"show_row"}
            title="Exposure Calculation - Primary Class"
            kb-interactive
          />

          <HX.Table shownBy="cds/glsn_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={["cds/exposure/granular/glsn_primary_exposure_details"]}
            fields={["cob",
              "exposure_base",
              "exposure_measure",
              "formatted_base_rate",
              { field: "five_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/five_years_ago_label" },
              { field: "four_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/four_years_ago_label" },
              { field: "three_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/three_years_ago_label" },
              { field: "two_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/two_years_ago_label" },
              { field: "one_years_ago", labelBy: "cds/rating_factors/one_years_ago_label" },
              { field: "current_year", labelBy: "cds/rating_factors/current_year_label" },
              "selection",
              "base_premium"
            ]}
            filter={"show_row"}
            title="Exposure Calculation - Primary Class"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Secondary Exposure Class">
        <HX.Pane>
          <HX.Table shownBy="cds/gmm_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={["cds/exposure/granular/gmm_secondary_exposure_details"]}
            fields={["gmm_secondary_exposure/exposure_class",
              "gmm_secondary_exposure/exposure_measure",
              "formatted_base_rate",
              { field: "five_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/five_years_ago_label" },
              { field: "four_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/four_years_ago_label" },
              { field: "three_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/three_years_ago_label" },
              { field: "two_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/two_years_ago_label" },
              { field: "one_years_ago", labelBy: "cds/rating_factors/one_years_ago_label" },
              { field: "current_year", labelBy: "cds/rating_factors/current_year_label" },
              "selection",
              "base_premium"
            ]}
            title="Exposure Calculation - Secondary Class"
            kb-interactive
          />
          <HX.Table shownBy="cds/glsn_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={["cds/exposure/granular/glsn_secondary_exposure_details"]}
            fields={["glsn_secondary_exposure/cob",
              "glsn_secondary_exposure/exposure_base",
              "glsn_secondary_exposure/exposure_measure",
              "formatted_base_rate",
              { field: "five_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/five_years_ago_label" },
              { field: "four_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/four_years_ago_label" },
              { field: "three_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/three_years_ago_label" },
              { field: "two_years_ago", shownBy: "cds/show_prior_exposure_years", labelBy: "cds/rating_factors/two_years_ago_label" },
              { field: "one_years_ago", labelBy: "cds/rating_factors/one_years_ago_label" },
              { field: "current_year", labelBy: "cds/rating_factors/current_year_label" },
              "selection",
              "base_premium"
            ]}
            title="Exposure Calculation - Secondary Class"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_exposure_details };