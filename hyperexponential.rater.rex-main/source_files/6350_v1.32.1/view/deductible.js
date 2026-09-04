import * as HX from "hx-model-components";
import { render_quick_run_bar, render_notifications } from "view/results_tables";
import { intl_deductible } from "view/intl_deductible";


function render_options_table(data, fields, path_to_field, path_to_show) {
  const MaxOptions = 3
  const tables = []

  for (let i = 1; i < (MaxOptions + 1); i++) {
    var tableField = fields.map(f => {
      if (typeof f == "string") {
        return path_to_field + "/option_" + i + "/" + f;
      } else {
        return { field: (path_to_field + "/option_" + i + "/" + f.field), shownBy: path_to_show + "/" + f.shownBy + "_" + i }
      }
    })
    tableField = ["layer_label"].concat(tableField)
    tables.push(
      <HX.Table
        title={"Option " + i}
        data={data}
        fields={tableField}
        shownBy={path_to_show + "/show_option_" + i}
        transpose
        kb-interactive
      />
    )
  }

  return tables
}


function deductible() {
  return (
    <HX.Page title="Deductible" fullWidth={true} shownBy="model_state/show_after_landing_page">
      {render_notifications()}
      {render_quick_run_bar()}
      {/* Perils Section */}
      <HX.Section title="Perils">
        <HX.Table
          data={[
            { datum: "layers", width: 200 }
          ]}
          fields={[
            "layer_label", "perils/fire/include", "perils/named_windstorm/include",
            "perils/scs/include", "perils/flood/include", "perils/quake/include",
            "perils/wildfire/include",
            { field: "perils/equipment_breakdown/include", shownBy: "policy_information/is_nacp" },
            { field: "perils/tria/include", shownBy: "policy_information/is_nacp" },
            "perils/cyber/include"
          ]}
          transpose
          kb-interactive
        />
      </HX.Section>

      {/* Deductibles Section */}
      <HX.Section title="Deductibles">

        <HX.Section title="Defaults">
          <HX.Pane flow="right">
            <HX.Button task="named_storm_ws_task" title="Named Storm only - WS" />
            <HX.Button task="all_tier_fl_ws_task" title="All, Tier and FL - WS" />
            <HX.Button task="fl_ws_task" title="FL - WS" />
            <HX.Button task="tx_ws_task" title="TX - WS" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="tier_fl_ws_task" title="Tier, FL - WS" />
            <HX.Button task="all_wind_ws_scs_task" title="All Wind - WS/SCS" />
            <HX.Button task="ca_eq_task" title="CA - EQ" />
            <HX.Button task="all_ca_eq_task" title="All, CA - EQ" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane flow="right" ratio={2}>
              <HX.Button task="copy_primary_deductibles_task" title="Add new layer copying primary deductibles" />
              <HX.Button task="clear_deductibles_task" title="Clear" />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
        </HX.Section>

        <HX.Notes field="info/deductible_info" />

        <HX.Section title="Fire" shownBy="non_layer_perils/fire/show_section">
          <HX.Table
            data={[
              { datum: "layers", width: 200 }
            ]}
            fields={["layer_label", "perils/fire/deductible"]}
            transpose
            kb-interactive
          />
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Button task="copy_fire_ded_task" title="Copy Down Fire Ded" />
            </HX.Pane>
            <HX.Pane ratio={3} />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Named Windstorm" shownBy="non_layer_perils/named_windstorm/show_section">
          <HX.Table
            data={[
              { datum: "layers", width: 200 }
            ]}
            fields={["layer_label", "perils/named_windstorm/per_occurrence_ded"]}
            transpose
            kb-interactive
          />
          <HX.Section title="US Location deductibles">
            <HX.Pane flow="right">
              <HX.Collection fields={["non_layer_perils/named_windstorm/num_options"]} />
              <HX.Pane ratio={3} />
            </HX.Pane>
            {render_options_table(
              [{ datum: "layers", width: 200 }],
              ["named_storm_ded", "region_dropdown/region",
                { field: "region_dropdown/state", shownBy: "show_state" },
                { field: "region_dropdown/tier", shownBy: "show_tier" },
                "type", "cell_to_fill",
                { field: "percent", shownBy: "show_percent" },
                { field: "location_min_max", shownBy: "show_location_min_max" },
                "sublimit"],
              "perils/named_windstorm/location_ded",
              "non_layer_perils/named_windstorm"
            )}
          </HX.Section>
        </HX.Section>

        <HX.Section title="Severe Convective Storm" shownBy="non_layer_perils/scs/show_section">
          <HX.Table
            data={[
              { datum: "layers", width: 200 }
            ]}
            fields={["layer_label", "perils/scs/per_occurrence_ded"]}
            transpose
            kb-interactive
          />
          <HX.Section title="US Location deductibles">
            <HX.Pane flow="right">
              <HX.Collection fields={["non_layer_perils/scs/num_options"]} />
              <HX.Pane ratio={3} />
            </HX.Pane>
            {render_options_table(
              [{ datum: "layers", width: 200 }],
              ["region_dropdown/region",
                { field: "region_dropdown/state", shownBy: "show_state" },
                { field: "region_dropdown/tier", shownBy: "show_tier" },
                "type", "cell_to_fill",
                { field: "percent", shownBy: "show_percent" },
                { field: "location_min_max", shownBy: "show_location_min_max" },
                "sublimit"],
              "perils/scs/location_ded",
              "non_layer_perils/scs"
            )}
          </HX.Section>
        </HX.Section>

        <HX.Section title="Flood" shownBy="non_layer_perils/flood/show_section">
          <HX.Table
            data={[
              { datum: "layers", width: 200 }
            ]}
            fields={["layer_label", "perils/flood/per_occurrence_ded"]}
            transpose
            kb-interactive
          />
          <HX.Section title="US Location deductibles">
            <HX.Pane flow="right">
              <HX.Collection fields={["non_layer_perils/flood/num_options"]} />
              <HX.Pane ratio={3} />
            </HX.Pane>
            {render_options_table(
              [{ datum: "layers", width: 200 }],
              ["region_dropdown/region",
                { field: "region_dropdown/state", shownBy: "show_state" },
                { field: "region_dropdown/fema_zone", shownBy: "show_tier" },
                "type", "cell_to_fill",
                { field: "percent", shownBy: "show_percent" },
                { field: "location_min_max", shownBy: "show_location_min_max" },
                "sublimit"],
              "perils/flood/location_ded",
              "non_layer_perils/flood"
            )}
          </HX.Section>
        </HX.Section>

        <HX.Section title="Quake" shownBy="non_layer_perils/quake/show_section">
          <HX.Table
            data={[
              { datum: "layers", width: 200 }
            ]}
            fields={["layer_label", "perils/quake/per_occurrence_ded", "perils/quake/ca_quake_include"]}
            transpose
            kb-interactive
          />
          <HX.Section title="US Location deductibles">
            <HX.Pane flow="right">
              <HX.Collection fields={["non_layer_perils/quake/num_options"]} />
              <HX.Pane ratio={3} />
            </HX.Pane>
            {render_options_table(
              [{ datum: "layers", width: 200 }],
              ["region_dropdown/region",
                { field: "region_dropdown/state", shownBy: "show_state" },
                { field: "region_dropdown/tier", shownBy: "show_tier" },
                "type", "cell_to_fill",
                { field: "percent", shownBy: "show_percent" },
                { field: "location_min_max", shownBy: "show_location_min_max" },
                "sublimit"],
              "perils/quake/location_ded",
              "non_layer_perils/quake"
            )}
          </HX.Section>
        </HX.Section>

        <HX.Section title="Wildfire" shownBy="non_layer_perils/wildfire/show_section">
          <HX.Table
            data={[
              { datum: "layers", width: 200 }
            ]}
            fields={["layer_label", "perils/wildfire/deductible"]}
            transpose
            kb-interactive
          />
        </HX.Section>
      </HX.Section>

      {/* Intl' Country Level Deductibles Section */}
      {intl_deductible()}

      {/* Sublimits Section */}
      <HX.Section title="Sublimits">
        <HX.Pane flow="right">
          <HX.Collection fields={["scs_sublimit", "ws_sublimit", "eq_sublimit", "fl_sublimit"]} with="sublimit" />
          <HX.Pane />
          <HX.Pane ratio={2}>
            <HX.Notes field="sublimit/sublimit_warning" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { deductible };