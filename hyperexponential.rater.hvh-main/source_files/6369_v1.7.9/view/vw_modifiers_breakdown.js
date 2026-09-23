import * as HX from "hx-model-components";

function vw_modifiers_breakdown_page() {
  return (
    <HX.Page title="Modifiers Breakdown">
      <HX.Section title="Options">
        <HX.Pane flow="right">
          <HX.Collection fields={["option_to_show", "option_to_bind"]} with="cds" horizontal />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="AOP" shownBy="cds/show_modifiers_breakdown">
        <HX.Notes field="cds/notes/aop_modifiers_breakdown_note.read_only" />
        <HX.Table
          data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "crime_score",
            "fire_alarm",
            "burglar_alarm",
            "sprinkler",
            "ppc",
            "loss",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/aop/tp_uplift_factor"
          ]}
          fields={[
            "value",
            "factor",
            { field: "option_to_bind_factor", shownBy: "/cds/show_option_to_bind_factor" },
            { field: "variance", shownBy: "/cds/show_option_to_bind_factor" },
          ]}
          with="cds/rating_factors/aop"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Wildfire" shownBy="cds/show_modifiers_breakdown">
        <HX.Table
          data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "wildfire_score",
            "fire_alarm",
            "sprinkler",
            "ppc",
            "loss",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/wildfire/tp_uplift_factor"
          ]}
          fields={[
            "value",
            "factor",
            { field: "option_to_bind_factor", shownBy: "/cds/show_option_to_bind_factor" },
            { field: "variance", shownBy: "/cds/show_option_to_bind_factor" },
          ]}
          with="cds/rating_factors/wildfire"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="WS" shownBy="cds/show_modifiers_breakdown">
        <HX.Table
          data={[
            "policy_term",
            "product_line",
            "square_foot",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "distance_to_coast_options",
            "loss",
            "peril",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/ws/tp_uplift_factor"
          ]}
          fields={[
            "value",
            "factor",
            { field: "option_to_bind_factor", shownBy: "/cds/show_option_to_bind_factor" },
            { field: "variance", shownBy: "/cds/show_option_to_bind_factor" },
          ]}
          with="cds/rating_factors/ws"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Liability" shownBy="cds/show_modifiers_breakdown">
        <HX.Table
          data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            'construction_type',
            'year_built',
            'building_occupancy',
            "ppc",
            "loss",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/liability/tp_uplift_factor"
          ]}
          fields={[
            "value",
            "factor",
            { field: "option_to_bind_factor", shownBy: "/cds/show_option_to_bind_factor" },
            { field: "variance", shownBy: "/cds/show_option_to_bind_factor" },
          ]}
          with="cds/rating_factors/liability"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Equipment Breakdown" shownBy="cds/show_modifiers_breakdown">
        <HX.Table
          data={[
            "policy_term",
            "loss",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/eb/tp_uplift_factor"
          ]}
          fields={[
            "value",
            "factor",
            { field: "option_to_bind_factor", shownBy: "/cds/show_option_to_bind_factor" },
            { field: "variance", shownBy: "/cds/show_option_to_bind_factor" },
          ]}
          with="cds/rating_factors/eb"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Excess FL" shownBy="cds/show_modifiers_breakdown">
        <HX.Table
          data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "number_of_storeys",
            "loss",
            "basement",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/fl/tp_uplift_factor"
          ]}
          fields={[
            "value",
            "factor",
            { field: "option_to_bind_factor", shownBy: "/cds/show_option_to_bind_factor" },
            { field: "variance", shownBy: "/cds/show_option_to_bind_factor" },
          ]}
          with="cds/rating_factors/fl"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="EQ" shownBy="cds/show_modifiers_breakdown">
        <HX.Table
          data={[
            "policy_term",
            "product_line",
            "state_county_zone",
            "construction_type",
            "roof_type",
            "year_built",
            "roof_year",
            "building_occupancy",
            "number_of_storeys",
            "basement",
            "retrofit",
            "soft_storey",
            "loss",
            "tiv_scale",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/eq/tp_uplift_factor"
          ]}
          fields={[
            "value",
            "factor",
            { field: "option_to_bind_factor", shownBy: "/cds/show_option_to_bind_factor" },
            { field: "variance", shownBy: "/cds/show_option_to_bind_factor" },
          ]}
          with="cds/rating_factors/eq"
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="PAF" shownBy="cds/show_modifiers_breakdown">
        <HX.Notes field="cds/notes/paf_modifiers_breakdown_note.read_only" />
        <HX.Table
          data={[
            "policy_term",
            "fire_alarm",
            "burglar_alarm",
            "safe",
            'credit_score',
            "crime_score",
            "wildfire_score",
            "include_ws",
            "include_eq",
            "include_fl",
            "include_wildfire",
            "total_modifier_impact",
            null,
            "/cds/tp_uplift/paf/tp_uplift_factor"
          ]}
          fields={[
            "value",
            "factor",
            { field: "option_to_bind_factor", shownBy: "/cds/show_option_to_bind_factor" },
            { field: "variance", shownBy: "/cds/show_option_to_bind_factor" },
          ]}
          with="cds/rating_factors/paf"
          kb-interactive
        />
      </HX.Section>
    </HX.Page>
  );
}

export { vw_modifiers_breakdown_page };
