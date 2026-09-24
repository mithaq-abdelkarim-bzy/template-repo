// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers, max_raw_data_columns } from "view/vw_constants";
import Bar from "components/bar";
import { convertToFieldObjects, node_name_list_with_suffix } from "view/vw_utilities";

const overallExposurePerYearFields = [
  // "display_yoa",
  "physicians",
  "professional_associations",
  "ambulatory_surgery_centres",
  "hospitals",
  "ltc_facilities",
  "other_facilities",
  "dentists",
  "others",
  "total_physicians_in_force",

]

const exposureSplitPerStateFields = [
  "venue",
  "premium_written",
  "total_pif_current_year",
  "split",
]

function vw_healthcare_cat_exposure_territory(scale) {
  return (
    <HX.Page title="Exposure Territory" viewScale={scale} shownBy="model_state/show_healthcare_cat">
      <HX.With context={{ type: "struct", path: "cds/healthcare_cat/exposure_territory" }}>
        <HX.Section title="Exposure Type">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection
                // with="exposure_territory"
                fields={[
                  "type_of_business",
                  "specialty",

                ]}
                syncColumnWidthsKey="measure"

              />
            </HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Overall Exposure By Year">
          <HX.Pane>

            <HX.Table
              // title="Overall Exposure By Year"
              // with="trial_history"
              data={[{ datum: "overall_exposure_per_year", elementLabelBy: "display_yoa" }
              ]}
              fields={[
                ...convertToFieldObjects(overallExposurePerYearFields, 150),

              ]}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane>
            <Bar
              title="Exposure Mix per Year"
              data={[
                { list: "/cds/healthcare_cat/exposure_territory/overall_exposure_per_year", labelBy: "uw_year" },
              ]}
              traces={[
                { field: "physicians", label: "Physicians" },
                { field: "professional_associations", label: "Professional Associations" },
                { field: "ambulatory_surgery_centres", label: "Ambulatory Surgery Centres" },
                { field: "hospitals", label: "Hospitals" },
                { field: "ltc_facilities", label: "LTC Facilities" },
                { field: "other_facilities", label: "Other Facilities" },
                { field: "dentists", label: "Dentists" },
                { field: "others", label: "Others" },

              ]}
              xAxisTickAngle={-45}
              gapBetweenBarsSize={0.10}
              xAxisLabel="YOA"
              yAxisLabel="Number of Employees"
              barMode="stack"
              yAxisTickFormat="0"
              width={700}
              height={500}
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Split By State">
          <HX.Pane>
            <HX.Collection
              // with="exposure_territory"
              fields={[
                "choose_split_by",
              ]}
              syncColumnWidthsKey="measure"

            />
          </HX.Pane>
          <HX.Pane>
            <HX.Table
              title="Exposure Split By State"

              data={[{ datum: "exposure_spit_by_state" }
              ]}
              fields={[
                ...convertToFieldObjects(exposureSplitPerStateFields, 150),

              ]}
              kb-interactive
            />
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_healthcare_cat_exposure_territory };