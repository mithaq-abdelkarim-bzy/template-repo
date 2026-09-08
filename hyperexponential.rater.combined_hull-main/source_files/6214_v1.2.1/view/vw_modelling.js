import * as HX from "hx-model-components";

function get_modelling_vessel_details() {
  modelling_prefix = "modelling_";
  let vessel_details = [
    modelling_prefix + "imo",
    modelling_prefix + "name",
    modelling_prefix + "vessel_type",
    {
      field: modelling_prefix + "agreed_value",
      labelBy: "/cds/currency_agreed_value_label",
    },
    modelling_prefix + "gross_tonnage",
    modelling_prefix + "dwt",
    modelling_prefix + "year_built",
    modelling_prefix + "flag",
    modelling_prefix + "vessel_class",
    {
      field: modelling_prefix + "freight_conditions",
      shownBy: "/non_cds/show_hide_toggles/modelling/show_adjustment_factors",
    },
    {
      field: modelling_prefix + "vessel_quality",
      shownBy: "/non_cds/show_hide_toggles/modelling/show_adjustment_factors",
    },
    {
      field: modelling_prefix + "area_of_operation",
      shownBy: "/non_cds/show_hide_toggles/modelling/show_adjustment_factors",
    },
    {
      field: modelling_prefix + "fleet_casualty_history",
      shownBy: "/non_cds/show_hide_toggles/modelling/show_adjustment_factors",
    },
    {
      field: modelling_prefix + "owner_quality",
      shownBy: "/non_cds/show_hide_toggles/modelling/show_adjustment_factors",
    },
    {
      field: modelling_prefix + "uw_adjustment",
      shownBy: "/non_cds/show_hide_toggles/modelling/show_adjustment_factors",
    },
    { field: modelling_prefix + "agg_uw_adjustment" },
  ];

  return vessel_details;
}

function get_modelling_rating_factors(model_type) {
  prefix = model_type + "_";
  let rating_factors = [
    prefix + "base",
    prefix + "fleet_size",
    prefix + "year_built",
    prefix + "frequency_vessel_type",
    prefix + "flag",
    prefix + "frequency_dwt",
  ];

  if (model_type === "behavioural") {
    behavioural_fields = [
      // { field: prefix + "max_distance_ratio" },
      // { field: prefix + "number_of_unique_port_visits" },
      // { field: prefix + "perc_time_eez" },
      // { field: prefix + "ratio_moving" },
      { field: prefix + "ratio_moored" },
    ];
    rating_factors = rating_factors.concat(behavioural_fields);
  }

  return rating_factors;
}

function get_modelling_calculations(model_type) {
  prefix = model_type;
  let calculations = [
    "model_frequency",
    "model_severity",
    "large_loss_overlay",
    "coverage",
    "coverage_factor",
    "expected_loss",
    "deductible",
    "mbbefdg",
    "order_percent",
    "el_pre_uw_adj",
    "all_uw_adj",
    "el_post_uw_adj",
  ];

  calculations = calculations.map((element) => {
    return {
      field: prefix + "_" + element,
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" +
        model_type +
        "_calculations",
    };
  });

  return calculations;
}

function get_modelling_severity(model_type) {
  prefix = model_type + "_severity_";
  return [
    prefix + "base_x_build_year_x_agreed_value",
    prefix + "vessel_type",
    prefix + "dwt",
  ];
}

function get_modelling_build_up_calculations(model_type) {
  prefix = model_type + "_build_up_";
  let fields = [
    {
      field: prefix + "base",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "year_built",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "flag",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "frequency_vessel_type",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "frequency_dwt_lower_bound",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "frequency_dwt_upper_bound",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "frequency_dwt_lower_bound_factor",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "frequency_dwt_upper_bound_factor",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "frequency_dwt",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "frequency_predicted",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
    {
      field: prefix + "expected_loss",
      shownBy:
        "/non_cds/show_hide_toggles/modelling/show_" + model_type + "_build_up",
    },
  ];
  if (model_type == "behavioural") {
    fields = fields.concat([
      {
        field: prefix + "max_distance_ratio",
        shownBy:
          "/non_cds/show_hide_toggles/modelling/show_" +
          model_type +
          "_build_up",
      },
      {
        field: prefix + "number_of_unique_port_visits",
        shownBy:
          "/non_cds/show_hide_toggles/modelling/show_" +
          model_type +
          "_build_up",
      },
      {
        field: prefix + "perc_time_eez",
        shownBy:
          "/non_cds/show_hide_toggles/modelling/show_" +
          model_type +
          "_build_up",
      },
      {
        field: prefix + "ratio_moving",
        shownBy:
          "/non_cds/show_hide_toggles/modelling/show_" +
          model_type +
          "_build_up",
      },
      {
        field: prefix + "ratio_moored",
        shownBy:
          "/non_cds/show_hide_toggles/modelling/show_" +
          model_type +
          "_build_up",
      },
    ]);
  }

  order = [
    "base",
    // "max_distance_ratio",
    // "number_of_unique_port_visits",
    // "perc_time_eez",
    // "ratio_moving",
    "ratio_moored",
    "year_built",
    "flag",
    "frequency_vessel_type",
    "frequency_dwt_lower_bound",
    "frequency_dwt_upper_bound",
    "frequency_dwt_lower_bound_factor",
    "frequency_dwt_upper_bound_factor",
    "frequency_dwt",
    "frequency_predicted",
    "expected_loss",
  ];

  let orderMapping = {};
  order.forEach((field, index) => {
    orderMapping[prefix + field] = index;
  });

  fields.sort((a, b) => orderMapping[a.field] - orderMapping[b.field]);

  return fields;
}

function get_severity_build_up(model_type) {
  prefix = model_type + "_build_up_severity_";
  fields = [
    { field: prefix + "base_x_build_year_x_agreed_value" },
    { field: prefix + "vessel_type" },
    { field: prefix + "dwt_lower_bound" },
    { field: prefix + "dwt_upper_bound" },
    { field: prefix + "dwt_lower_bound_factor" },
    { field: prefix + "dwt_upper_bound_factor" },
    { field: prefix + "dwt" },
    { field: prefix + "predicted" },
    { field: prefix + "model" },
  ];
  return fields;
}

function vw_modelling(scale) {
  let modelling_table_fields_array = get_modelling_vessel_details();
  modelling_table_fields_array.push(null);
  modelling_table_fields_array = modelling_table_fields_array.concat(
    get_modelling_rating_factors((model_type = "static"))
  );
  modelling_table_fields_array.push(null);
  modelling_table_fields_array = modelling_table_fields_array.concat(
    get_modelling_severity((model_type = "static"))
  );
  modelling_table_fields_array.push(null);
  modelling_table_fields_array = modelling_table_fields_array.concat(
    get_modelling_calculations((model_type = "static"))
  );
  modelling_table_fields_array.push(null);
  modelling_table_fields_array = modelling_table_fields_array.concat([
    // { field: "modelling_behavioural_ratio_moving", shownBy: "/non_cds/show_hide_toggles/modelling/show_behavoural_rating_levels" },
    // { field: "modelling_behavioural_max_distance_ratio", shownBy: "/non_cds/show_hide_toggles/modelling/show_behavoural_rating_levels" },
    // { field: "modelling_behavioural_number_of_unique_port_visits", shownBy: "/non_cds/show_hide_toggles/modelling/show_behavoural_rating_levels" },
    // { field: "modelling_behavioural_perc_time_eez", shownBy: "/non_cds/show_hide_toggles/modelling/show_behavoural_rating_levels" },
    { field: "modelling_behavioural_ratio_moored", shownBy: "/non_cds/show_hide_toggles/modelling/show_behavoural_rating_levels" },
  ]);
  modelling_table_fields_array.push(null);
  modelling_table_fields_array = modelling_table_fields_array.concat(
    get_modelling_rating_factors((model_type = "behavioural"))
  );
  modelling_table_fields_array.push(null);
  modelling_table_fields_array = modelling_table_fields_array.concat(
    get_modelling_severity((model_type = "behavioural"))
  );
  modelling_table_fields_array.push(null);
  modelling_table_fields_array = modelling_table_fields_array.concat(
    get_modelling_calculations((model_type = "behavioural"))
  );
  modelling_table_fields_array.push(null);
  modelling_table_fields_array.push({ field: "pro_rata_adjustment" });
  // Commented and can be shown to follow the calculations logic for testing
  // modelling_table_fields_array.push(null);
  // modelling_table_fields_array = modelling_table_fields_array.concat(
  //   get_modelling_build_up_calculations((model_type = "static"))
  // );
  // modelling_table_fields_array.push(null);
  // modelling_table_fields_array = modelling_table_fields_array.concat(
  //   get_severity_build_up((model_type = "static"))
  // );
  // modelling_table_fields_array.push(null);
  // modelling_table_fields_array = modelling_table_fields_array.concat(
  //   get_severity_build_up((model_type = "behavioural"))
  // );
  // modelling_table_fields_array.push(null);
  // modelling_table_fields_array = modelling_table_fields_array.concat(
  //   get_modelling_build_up_calculations((model_type = "behavioural"))
  // );
  // modelling_table_fields_array.push(null);
  // modelling_table_fields_array.push({
  //   field: "modelling_converted_agreed_value",
  // });

  return (
    <HX.Page
      title="Modelling"
      shownBy="/non_cds/show_hide_toggles/hull/show_modelling_page"
    >
      <HX.With
        context={{
          type: "struct",
          path: "cds/exposure/granular/vessels/hull_rating",
        }}
      >
        <HX.Section title="">
          <HX.Pane flow="down">
            <HX.Section title="Fleet Average Static Relativity">
              <HX.Table
                data={[
                  {
                    datum:
                      "fleet_average_relativity/static",
                    labelBy:
                      "/non_cds/labels/modelling/average_static_fleet_relativity",
                  }
                ]}
                fields={[
                  "base",
                  "fleet_size",
                  "year_built",
                  "frequency_vessel_type",
                  "flag",
                  "frequency_dwt",
                  "base_x_year_x_value",
                  "severity_vessel_type",
                  "severity_dwt",
                ]}
                kb-interactive
              />
            </HX.Section>
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Section title="Fleet Average Behavioural Relativity">
              <HX.Table
                title=""
                data={[
                  {
                    datum:
                      "fleet_average_relativity/behavioural",
                    labelBy:
                      "/non_cds/labels/modelling/average_behavioural_fleet_relativity",
                  },
                ]}
                fields={[
                  "base",
                  "fleet_size",
                  "year_built",
                  "frequency_vessel_type",
                  "flag",
                  "frequency_dwt",
                  // "max_distance_ratio",
                  // "perc_time_eez",
                  // "ratio_moving",
                  // "number_of_unique_port_visits",
                  "ratio_moored",
                  "base_x_year_x_value",
                  "severity_vessel_type",
                  "severity_dwt",
                ]}
                kb-interactive
              />
            </HX.Section>
          </HX.Pane>
          <HX.Section title="Behaviour and Static Modelling">
            <HX.Pane flow="down">
              <HX.Collection
                fields={[
                  "/non_cds/show_hide_toggles/modelling/show_adjustment_factors",
                  "/non_cds/show_hide_toggles/modelling/show_static_calculations",
                  "/non_cds/show_hide_toggles/modelling/show_behavioural_calculations",
                  "/non_cds/show_hide_toggles/modelling/show_behavoural_rating_levels",
                ]}
                horizontal
              />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table
              data={["modelling_list"]}
              fields={modelling_table_fields_array}
              kb-interactive
              dynamic
              freezeLeft={3}
            />
          </HX.Section>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_modelling };
