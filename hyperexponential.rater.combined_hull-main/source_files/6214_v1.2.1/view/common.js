import * as HX from "hx-model-components";

function get_vessel_details(coverage_type, show_details) {
  if (!["iv", "war"].includes(coverage_type)) {
    return [];
  }

  const read_only_suffix = ".read_only_option";
  const vessel_details_prefix = "vessel_details/";
  const coverage_prefix = coverage_type + "/" + coverage_type + "_";

  let common_vessel_details_fields = [
    "imo",
    "name",
    "inception_date",
    "expiry_date",
    "gross_tonnage",
  ];

  const final_field_order = [
    "imo",
    "name",
    "inception_date",
    "expiry_date",
    "coverage",
    "vessel_type",
    "agreed_value",
    "gross_tonnage",
    "dwt",
    "year_built",
    "flag",
    "vessel_class",
    "deductible",
    "order_percent",
    "freight_conditions",
    "vessel_quality",
    "area_of_operation",
    "behavioural_model_rate",
    "behavioural_benchmark_premium",
    "static_model_rate",
    "static_benchmark_premium",
    "achieved_rate",
    "achieved_premium",
    "average_achieved_rate",
    "uw_adjustment",
    "benchmark_premium",
    "is_include_vessel",
  ];

  const vessel_read_only_fields = [
    "deductible",
    "vessel_type",
    "dwt",
    "year_built",
    "flag",
  ];

  const extra_vessel_details_fields = [
    "vessel_class",
    "order_percent",
    "freight_conditions",
    "vessel_quality",
    "area_of_operation",
  ];

  const extra_vessel_coverage_fields = [
    "behavioural_model_rate",
    "behavioural_benchmark_premium",
    "static_model_rate",
    "static_benchmark_premium",
  ];

  const common_iv_and_war_fields = [
    "agreed_value",
    "coverage",
    "achieved_rate",
    "achieved_premium",
    "uw_adjustment",
    "benchmark_premium",
    "is_include_vessel",
  ];

  const vessel_coverage_specific_fields = {
    iv: [...common_iv_and_war_fields, "average_achieved_rate", "deductible"],
    war: [...common_iv_and_war_fields],
  };

  const all_fields = [
    ...common_vessel_details_fields,
    ...extra_vessel_details_fields,
    ...vessel_read_only_fields,
    ...extra_vessel_coverage_fields,
    ...vessel_coverage_specific_fields[coverage_type],
  ];

  const sorted_fields = final_field_order.filter((field) =>
    all_fields.includes(field)
  );

  const coverage_vessel_details = sorted_fields.map((element) => {
    return common_vessel_details_fields.includes(element)
      ? vessel_details_prefix + element + read_only_suffix
      : extra_vessel_details_fields.includes(element)
        ? {
          field: vessel_details_prefix + element + read_only_suffix,
          shownBy: show_details,
        }
        : extra_vessel_coverage_fields.includes(element)
          ? { field: coverage_prefix + element, shownBy: show_details }
          : element === "agreed_value"
            ? {
              field: coverage_prefix + element,
              labelBy: "/cds/currency_agreed_value_label",
            }
            : vessel_coverage_specific_fields[coverage_type].includes(element)
              ? coverage_prefix + element
              : vessel_read_only_fields.includes(element)
                ? element + read_only_suffix
                : null;
  });

  return coverage_vessel_details;
}

function get_inputs_section(coverage_type) {
  const prefix = coverage_type
    ? "coverages/" + coverage_type + "/" + coverage_type + "_"
    : "";

  const coverage_path = coverage_type ? "coverages/" + coverage_type + "/" : "";
  const standard_coverages_fields_prefix = "coverages/" + coverage_type + "/";
  return (
    <HX.With
      context={{
        type: "list",
        index: 0,
        path: "/cds/layers",
      }}
    >
      <HX.Section title="Inputs">
        <HX.Pane flow="down">
          <HX.Pane flow="right">
            <HX.Collection
              fields={
                coverage_type === "ship_building" || coverage_type === "loh"
                  ? [
                    coverage_path + "section_reference",
                    standard_coverages_fields_prefix + "brokerage",
                    {
                      field:
                        standard_coverages_fields_prefix +
                        "other_deductions",
                      shownBy:
                        "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage",
                      infoBy:
                        "/non_cds/tooltips/shipbuilders/other_deductions",
                    },
                    standard_coverages_fields_prefix + "written_line",
                    {
                      field: prefix + "is_war_cover",
                      shownBy:
                        "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage",
                    },
                    {
                      field:
                        "/non_cds/show_hide_toggles/ship_building/show_ship_builders_actuarial_pricing",
                      shownBy:
                        "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage",
                    },
                    {
                      field: "coverages/loh/loh_achieved_premium",
                      labelBy: "/non_cds/labels/loh/achieved_premium_label",
                      shownBy:
                        "/non_cds/show_hide_toggles/loh/show_loh_coverage",
                    },
                  ]
                  : coverage_type == "hull"
                    ? [
                      coverage_path + "section_reference",
                      standard_coverages_fields_prefix + "brokerage",
                      standard_coverages_fields_prefix + "written_line",
                      prefix + "lead_follow",
                      "/cds/exposure/granular/vessels/hull_rating/operator_domicile",
                      "/cds/exposure/granular/vessels/hull_rating/is_modelling",
                    ]
                    : [
                      coverage_path + "section_reference",
                      standard_coverages_fields_prefix + "brokerage",
                      standard_coverages_fields_prefix + "written_line",
                      prefix + "lead_follow",
                    ]
              }
              horizontal
            />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection
              fields={[{ field: "/non_cds/labels/mismatched_inception_year_warning.warning_option", shownBy: "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning" }]}
            />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button
              task={"upsert_hx_meta_policy_references_task"}
              title="Pass Policy Reference to PAS"
            />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.With>
  );
}

function get_default_section(coverage_type) {
  const LOH_PREFIX = "loh_";
  const EXPOSURE_PREFIX =
    "/cds/exposure/granular/vessels/vessels_defaults/" + coverage_type + "/";
  const TASK_PREFIX = coverage_type == "hull" ? "" : "_loh";
  hull_dates = [
    "/cds/standard_fields/inception_date",
    "/cds/standard_fields/expiry_date",
  ];

  const HULL_DEFAULT_FIELDS = [
    [EXPOSURE_PREFIX + "inception_date", EXPOSURE_PREFIX + "expiry_date"],
    [
      EXPOSURE_PREFIX + "coverage",
      EXPOSURE_PREFIX + "deductible",
      EXPOSURE_PREFIX + "order_percent",
    ],
    [
      EXPOSURE_PREFIX + "freight_conditions",
      EXPOSURE_PREFIX + "vessel_quality",
      EXPOSURE_PREFIX + "area_of_operation",
    ]
  ]
  const LOH_DEFAULT_FIELDS = [
    [
      {
        field: EXPOSURE_PREFIX + LOH_PREFIX + "daily_rate",
        labelBy: "/non_cds/labels/currency_loh_daily_rate_label",
      },
      EXPOSURE_PREFIX + LOH_PREFIX + "uw_adjustment",
    ],
    [
      EXPOSURE_PREFIX + LOH_PREFIX + "xs_days",
      EXPOSURE_PREFIX + LOH_PREFIX + "cover",
    ]
  ]

  const shownBy =
    coverage_type == "loh"
      ? "/non_cds/show_hide_toggles/loh/show_defaults"
      : null;
  return (
    <HX.Section title="Vessels Defaults">
      <HX.Pane shownBy="/non_cds/show_hide_toggles/loh/show_loh_coverage">
        <HX.Collection
          fields={["/non_cds/show_hide_toggles/loh/show_defaults"]}
          syncColumnWidthsKey="key_1"
        />
      </HX.Pane>
      <HX.Pane shownBy={shownBy} flow="right" reflow={false}>
        <HX.Pane flow="down">
          <HX.Collection
            fields={(coverage_type == "hull") ? HULL_DEFAULT_FIELDS[0] : LOH_DEFAULT_FIELDS[0]}
            syncColumnWidthsKey="key_1"
          />
          <HX.Pane flow="right">
            <HX.Button
              task={"set" + TASK_PREFIX + "_vessels_defaults_task"}
              title="Set Vessels Defaults"
            />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="down">
          <HX.Collection
            fields={(coverage_type == "hull") ? HULL_DEFAULT_FIELDS[1] : LOH_DEFAULT_FIELDS[1]}
            syncColumnWidthsKey="key_1"
          />
        </HX.Pane>
        <HX.Pane flow="down" shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage">
          <HX.Collection
            fields={HULL_DEFAULT_FIELDS[2]}
            syncColumnWidthsKey="key_1"
          />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane />
        <HX.Pane />
        <HX.Pane />
        <HX.Pane />
      </HX.Pane>
    </HX.Section>
  );
}

export { get_vessel_details, get_inputs_section, get_default_section };
