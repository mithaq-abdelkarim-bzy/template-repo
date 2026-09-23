import * as HX from "hx-model-components";
import { glsn_danger_ingred_1, glsn_danger_ingred_2 } from "view/vw_constants";


function vw_aggregation(scale) {
  return (
    <HX.Page title="Aggregation" fullWidth={true} viewScale={scale} shownBy="/cds/glsn_masking">

      <HX.Section title="Potential Aggregation From Overlapping Entities">
        <HX.Pane>
          <HX.Table
            // syncColumnWidthsKey="mySyncedTables2"
            data={["cds/exposure/granular/glsn_aggregation_details"]}
            fields={["type",
              "name",
              "beazley_insured",
              "aggregated_capacity",
              "notes"
            ]}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Dangerous Ingredients Exception">
        <HX.Pane>
          <HX.Table
            syncColumnWidthsKey="mySyncedTables1"
            data={glsn_danger_ingred_1()}
            fields={["exposed", "revenue", "notes"]}
            with="cds/exposure/granular"
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            syncColumnWidthsKey="mySyncedTables1"
            data={glsn_danger_ingred_2()}
            fields={["exposed", "revenue", "notes"]}
            with="cds/exposure/granular"
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Other Dangerous Ingredient">
        <HX.Pane>
          <HX.Collection
            fields={["cds/exposure/granular/glsn_dangerous_ingredient_other_selection"]} horizontal />
        </HX.Pane>
        <HX.Pane shownBy="cds/exposure/granular/glsn_dangerous_ingredient_other_selection">
          <HX.Table
            // syncColumnWidthsKey="mySyncedTables1"
            data={["cds/exposure/granular/glsn_dangerous_ingredient_other"]}
            fields={["name",
              "exposed",
              "revenue",
              "notes"
            ]}
          />
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_aggregation };