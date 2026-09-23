import * as HX from "hx-model-components";


function vw_risk_characteristics(scale) {
  return (
    <HX.Page title="Risk Characteristics">
      <HX.With context={{ type: 'struct', path: 'cds/rating_factors' }}>
        <HX.Section title="Mandatory">
          <HX.Collection fields={[
            "building_occupancy",
            { field: 'construction_type', shownBy: "/cds/validation/construction_type/valid" },
            { field: 'construction_type.notSupported', shownBy: "/cds/validation/construction_type/invalid", infoBy: "/cds/validation/construction_type/info_text" },
            'year_built',
            'ppc',
            'roof_type',
            // 'roof_year',
          ]} numCols={4} />
        </HX.Section>
        <HX.Section title="Non-Mandatory">
          <HX.Collection fields={[
            "square_foot",
            { field: 'number_of_units', shownBy: "/cds/validation/number_of_units/valid" },
            { field: 'number_of_units.notSupported', shownBy: "/cds/validation/number_of_units/invalid", infoBy: "/cds/validation/number_of_units/info_text" },
            "basement",
            { field: 'roof_shape', shownBy: "/cds/validation/roof_shape/valid" },
            { field: 'roof_shape.notSupported', shownBy: "/cds/validation/roof_shape/invalid", infoBy: "/cds/validation/roof_shape/info_text" },
            "number_of_storeys",
            "fire_alarm",
            "burglar_alarm",
            "sprinkler",
            'updated_roof_year',
            "updated_wiring_year",
            "updated_plumbing_year",
            "updated_heating_year"
          ]} numCols={4} />
        </HX.Section>
      </HX.With>
      <HX.Section title="Loss History">
        <HX.Table
          title="Loss History"
          data={[
            "aop",
            "wildfire",
            "ws",
            "liability",
            "eb",
            "fl",
            "eq",
            null,
            "/cds/experience_rating/coverages/total"
          ]}
          fields={[
            //"any_losses_last_five_years",
            { field: "number_of_losses", width: 300 },
            { field: "amount_of_losses", width: 300 }]}
          with="cds/experience_rating/coverages"
          kb-interactive
        />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_characteristics };


