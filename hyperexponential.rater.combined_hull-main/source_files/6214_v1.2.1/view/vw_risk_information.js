import * as HX from "hx-model-components";

function vw_risk_information(scale) {
  const coverage_type_key = "coverage_type_key";
  return (
    <HX.Page
      title="Risk Information"
      shownBy="model_state/show_after_landing_page"
    >
      <HX.Section title="Account Details">
        <HX.Pane>
          {/* NOTE  uncomment if rater requires databse_id to be displayed */}
          {/* <HX.Collection fields={["database_id"]} with="cds" horizontal /> */}
          <HX.Collection
            fields={["inception_date", "expiry_date"]}
            with="hx_core"
            horizontal
          />
          <HX.Collection
            fields={["underwriter", "insured_name", { field: "/cds/name_on_yard", shownBy: "/non_cds/show_hide_toggles/ship_building/show_ship_building_coverage" }]}
            with="cds/standard_fields"
            horizontal
          />
          <HX.Collection
            fields={[
              "cds/currencies/source_currency",
              "cds/standard_fields/is_renewal",
            ]}
            horizontal
            syncColumnWidthsKey={coverage_type_key}
          />
        </HX.Pane>
      </HX.Section>
      {/* NOTE use the below code if the model does not price multiple layers and it is required to store line size
        brokerage & status on teh risk Information sheet */}
      {/* <HX.Section title="Policy Information" >
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["written_line", "brokerage", "status"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section> */}
      <HX.Section title="Broker Details">
        <HX.Collection
          fields={["cds/standard_fields/broker", "cds/broker_contact"]}
          horizontal
        />
      </HX.Section>
      <HX.Section title="Coverage">
        <HX.Pane flow="right">
          <HX.Collection
            fields={[
              "cds/coverage_type",
              { field: "/non_cds/show_hide_toggles/hull/show_hull_coverage", shownBy: "/non_cds/show_hide_toggles/hull/show_hull_coverage" },
              { field: "cds/is_iv_coverage", shownBy: "/non_cds/show_hide_toggles/hull/show_hull_coverage" },
              { field: "cds/is_war_coverage", shownBy: "/non_cds/show_hide_toggles/hull/show_hull_coverage" },
            ]}
            horizontal
            syncColumnWidthsKey={coverage_type_key}
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  );
}

export { vw_risk_information };
