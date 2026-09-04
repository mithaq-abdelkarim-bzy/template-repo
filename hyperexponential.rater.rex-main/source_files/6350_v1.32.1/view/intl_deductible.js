import * as HX from "hx-model-components";

function intl_deductible() {
  const sections = [
    "Named Windstorm",
    "Severe Convective Storms",
    "Flood",
    "Quake",
  ];
  const deductibles = [
    "named_windstorm",
    "scs",
    "flood",
    "quake",
  ];

  return (
    <HX.Section title="International Deductibles">
      <HX.Notes field="model_state/intl_ded_message.read_only" />
      <HX.Pane flow="right">
        <HX.Button task="fill_intl_ded_countries_task" title="Populate Countries from Schedule" />
        <HX.Pane ratio={2} />
      </HX.Pane>
      <HX.Section title="Fire" shownBy="non_layer_perils/fire/show_section">
        <HX.Pane>
          <HX.Table
            title="Intl Location Deductibles"
            data={[{ datum: "intl_ded", elementLabelBy: "country" }]}
            fields={[
              { field: "tiv", width: 200 },
              { field: "perc_of_tiv", width: 200 },
              { field: "fixed_min", width: 200, labelBy: "/model_state/min_ded_label" },
              { field: "fixed_max", width: 200, labelBy: "/model_state/max_ded_label" }
            ]}
            with={`non_layer_perils/fire`}
            syncColumnWidthsKey="intl_ded"
            kb-interactive
          />
          <HX.Pane flow="right">
            <HX.Button task="copy_intl_ded_perils_task" title="Copy Down Fire Ded" />
            <HX.Pane ratio={2} />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      {sections.map((section, index) => (
        <HX.Section title={section} shownBy={`non_layer_perils/${deductibles[index]}/show_section`} >
          <HX.Pane>
            <HX.Table
              title="Intl Location Deductibles"
              data={[{ datum: "intl_ded", elementLabelBy: "country" }]}
              fields={[
                { field: "tiv", width: 200 },
                { field: "perc_of_tiv", width: 200 },
                { field: "fixed_min", width: 200, labelBy: "/model_state/min_ded_label" },
                { field: "fixed_max", width: 200, labelBy: "/model_state/max_ded_label" },
                { field: "country_sublimit", width: 200, labelBy: "/model_state/sublimit_label" }
              ]}
              with={`non_layer_perils/${deductibles[index]}`}
              syncColumnWidthsKey="intl_ded"
              kb-interactive
            />
          </HX.Pane>
        </HX.Section>
      ))}
      <HX.Section title="Wildfire" shownBy="non_layer_perils/wildfire/show_section">
        <HX.Pane>
          <HX.Table
            title="Intl Location Deductibles"
            data={[{ datum: "intl_ded", elementLabelBy: "country" }]}
            fields={[
              { field: "tiv", width: 200 },
              { field: "perc_of_tiv", width: 200 },
              { field: "fixed_min", width: 200, labelBy: "/model_state/min_ded_label" },
              { field: "fixed_max", width: 200, labelBy: "/model_state/max_ded_label" }
            ]}
            with={`non_layer_perils/wildfire`}
            syncColumnWidthsKey="intl_ded"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
    </HX.Section>
  );
}

export { intl_deductible };
