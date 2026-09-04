import * as HX from "hx-model-components";
import { render_quick_run_bar, render_notifications } from "view/results_tables";
import InfoBox from "components/infobox";


function additional_coverages() {
  return (
    <HX.Page title="Additional Coverages" fullWidth={true} shownBy="control/show_additional_coverages_page">
      {/* <HX.Page title="Additional Coverages" fullWidth={true} shownBy="model_state/show_after_landing_page"> */}
      {render_notifications()}
      {render_quick_run_bar()}

      {/* Equipment Breakdown Section */}
      <HX.Section title="Equipment Breakdown" shownBy="non_layer_perils/equipment_breakdown/show_section">
        <InfoBox textNode="info/equipment_breakdown_msg" />
        <HX.Pane flow="right">
          <HX.Pane ratio={3}>
            <HX.Collection fields={["industry", "occupancy", "deductible"]} with="non_layer_perils/equipment_breakdown" horizontal />
          </HX.Pane>
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Pane ratio={2}>
            <HX.Collection fields={["non_layer_perils/equipment_breakdown/referral"]} />
          </HX.Pane>
          <HX.Collection fields={["non_layer_perils/equipment_breakdown/travelers"]} />
          <HX.Pane />
        </HX.Pane>
        <HX.Table
          title="Coverage Extensions"
          data={["perishable_goods", "expediting_expense", "pollution", "data_media", "demolition", "water_damage"]}
          fields={[
            { field: "covered", width: 250 },
            { field: "pd_sublimit", width: 250 }
          ]}
          with="non_layer_perils/equipment_breakdown"
          kb-interactive
        />
        <HX.Section title="Premium">
          <HX.Table
            data={[{ datum: "layers", width: 250 }]}
            fields={["layer_label", "perils/equipment_breakdown/eb_premium", "perils/equipment_breakdown/actual_eb_premium",]}
            transpose
            kb-interactive
          />
        </HX.Section>
      </HX.Section>

      {/* TRIA Section */}
      <HX.Section title="TRIA" shownBy="non_layer_perils/tria/show_section">
        <HX.Table
          data={[{ datum: "layers", width: 250 }]}
          fields={["layer_label", "perils/tria/tria_premium", "perils/tria/actual_tria_premium",]}
          transpose
          kb-interactive
        />
      </HX.Section>

      {/* Cyber & Data Restoration Section */}
      <HX.Section title="Cyber" shownBy="non_layer_perils/cyber/show_section">
        <InfoBox textNode="non_layer_perils/cyber/info_note" />
        <HX.Table
          data={[{ datum: "layers", width: 250 }]}
          fields={["layer_label", "perils/cyber/include_affirmative", "perils/cyber/include_malicious"]}
          transpose
          kb-interactive
        />
        <HX.Table
          data={[{ datum: "layers", width: 250 }]}
          fields={["layer_label", { field: "perils/cyber/sublimit", shownBy: "control/show_affirmative_cyber" }, { field: "perils/cyber/deductible", shownBy: "control/show_affirmative_cyber" },
            { field: "perils/cyber/ensuing_sublimit", shownBy: "control/show_ensuing_loss_cyber" }, { field: "perils/cyber/ensuing_deductible", shownBy: "control/show_ensuing_loss_cyber" },
            { field: "perils/cyber/calculated_premium", shownBy: "control/show_affirmative_cyber" }]}
          transpose
          kb-interactive
        />
        <HX.Pane flow="right">
          <HX.Notes field="non_layer_perils/cyber/cyber_coverage_note" title="Cyber Coverage Note" />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

    </HX.Page >
  )
}

export { additional_coverages };