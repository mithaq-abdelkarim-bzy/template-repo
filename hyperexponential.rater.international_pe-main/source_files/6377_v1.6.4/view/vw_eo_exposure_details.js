import * as HX from "hx-model-components";
import { discipline, ae_operation } from "view/vw_constants";

function vw_eo_exposure_details(scale) {
  return (
    <HX.Page title="Exposure E&O" fullWidth={true} viewScale={scale} shownBy="cds/eo_coverage_selection">
      <HX.Section title="Exposure Information">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "cds/rating_factors/eo_territory/input_value"]} />
          <HX.Collection fields={[
            "cds/exposure/granular/eo_profession"]} />
          <HX.Collection fields={[
            { field: "cds/exposure/aggregate/eo_total_fees", labelBy: "/cds/eo_fees_currency_label" }]} />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Fees Split by Discipline" shownBy="cds/exposure/granular/eo_exposure_shownby">
        <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
          <HX.Pane flow="right">
            <HX.Collection fields={[{ field: "eo_total_fees_pct" }]} />
            <HX.Button task="clear_eo_input_task" title="Clear All the Input of Fees %"></HX.Button>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
          <HX.Table
            title=" "
            syncColumnWidthsKey="mySyncedTables1"
            data={discipline()}
            fields={[{ field: "input_pct", width: 250 }, { field: "relativity", width: 250 }]}
            filter={"show_row"}
            kb-interactive
          />
        </HX.With>
      </HX.Section>
      <HX.Section title="Architects and Engineers Operations" shownBy="cds/exposure/granular/eo_ae_operaion_shownby" >
        <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
          <HX.Pane flow="right">
            <HX.Collection fields={["eo_ae_operation_pct"]} />
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>

          <HX.Table
            title=" "
            syncColumnWidthsKey="mySyncedTables1"
            data={ae_operation()}
            fields={[{ field: "input_pct", width: 250 }, { field: "relativity", width: 250 }]}
            filter={"show_row"}
            kb-interactive
          />
        </HX.With>
      </HX.Section>
      <HX.Section title="Insurance Information" >
        <HX.Table
          title=" "
          syncColumnWidthsKey="mySyncedTables1"
          data={["eo_prior_knowledge"]}
          fields={[{ field: "input_value", width: 250 }, { field: "relativity", width: 250 }]}
          with="cds/rating_factors"
        />
        <HX.Table
          title=" "
          syncColumnWidthsKey="mySyncedTables1"
          data={["eo_insurance_history"]}
          fields={[{ field: "input_value", width: 400 }, { field: "input_rel", width: 200 },
          { field: "min_rel", width: 200 }, { field: "max_rel", width: 200 }, { field: "applied_rel", width: 200 }]}
          with="cds/modifiers"
        />
      </HX.Section>
      <HX.Section title="Claims Experience" >
        <HX.Table
          title=" "
          syncColumnWidthsKey="mySyncedTables1"
          data={["eo_cost_included"]}
          fields={[{ field: "input_value", width: 250 }, { field: "relativity", width: 250 }]}
          with="cds/rating_factors"
        />
        <HX.Table
          title=" "
          syncColumnWidthsKey="mySyncedTables1"
          data={["eo_claim_history"]}
          fields={[{ field: "input_value", width: 250 }, { field: "input_rel", width: 250 },
          { field: "min_rel", width: 250 }, { field: "max_rel", width: 250 }, { field: "applied_rel", width: 250 }]}
          with="cds/modifiers"
        />

      </HX.Section>
      <HX.Section title="Schedule Rating" >
        <HX.Table
          title=" "
          syncColumnWidthsKey="mySyncedTables1"
          data={["eo_schedule_modifier"]}
          fields={[{ field: "input_value", width: 250 }, { field: "min_rel", width: 250 }, { field: "max_rel", width: 250 }, { field: "applied_rel", width: 250 }]}
          with="cds/modifiers"
        />
      </HX.Section>

    </HX.Page >
  )
}

export { vw_eo_exposure_details };