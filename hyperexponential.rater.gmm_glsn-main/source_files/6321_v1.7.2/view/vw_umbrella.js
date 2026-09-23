import * as HX from "hx-model-components";
import { gmm_umbrella_class, glsn_umbrella_class, max_options } from "view/vw_constants";

function vw_umbrella_calcs(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Umbrella Calculations Option " + (n + 1)} shownBy={"cds/show_option_" + (n + 1)} >
        <HX.With context={{ type: "list", path: "cds/options", index: n }}>
          <HX.Pane flow="right">
            <HX.Table kb-interactive shownBy="/cds/gmm_masking"
              data={[{ datum: "gmm_auto_liability", labelAlign: "left" },
              { datum: "gmm_employers_liability", labelAlign: "left" },
              { datum: "gmm_general_liability", labelAlign: "left" },
              { datum: "gmm_foreign_liability", labelAlign: "left" },
              { datum: "gmm_aircraft_nonowned", labelAlign: "left" },
              { datum: "gmm_aircraft_owned", labelAlign: "left" },
              { datum: "gmm_auto_ambulance", labelAlign: "left" },
              { datum: "gmm_educators_liability", labelAlign: "left" },
              { datum: "gmm_garage_keepers_liability", labelAlign: "left" },
              { datum: "gmm_helipad", labelAlign: "left" },
              { datum: "gmm_liquor_law_liability", labelAlign: "left" },
              { datum: "gmm_managed_care_eo_health_plan", labelAlign: "left" },
              { datum: "gmm_managed_care_eo_nonhealth_plan", labelAlign: "left" },
              { datum: "gmm_watercraft_nonowned", labelAlign: "left" },
              { datum: "gmm_watercraft_owned", labelAlign: "left" },
                null,
              { datum: "umbrella_eel", labelAlign: "left" },
                null,
              { datum: "umbrella_unsupported_net_premium", labelAlign: "left" },
              { datum: "umbrella_total_excess_net_premium", labelAlign: "left" },
                null,
              { datum: "umbrella_munich_cession_net", labelAlign: "left" },
              { datum: "umbrella_munich_cession_gross", labelAlign: "left" }]}
              fields={["premium_primary",
                { field: "premium_1_excess", shownBy: "/cds/add_excess_1" },
                { field: "premium_2_excess", shownBy: "/cds/add_excess_2" },
                { field: "premium_3_excess", shownBy: "/cds/add_excess_3" },
                { field: "premium_4_excess", shownBy: "/cds/add_excess_4" },
                { field: "premium_5_excess", shownBy: "/cds/add_excess_5" },
                { field: "premium_6_excess", shownBy: "/cds/add_excess_6" },
                { field: "premium_7_excess", shownBy: "/cds/add_excess_7" },
                { field: "premium_8_excess", shownBy: "/cds/add_excess_8" },
                { field: "premium_9_excess", shownBy: "/cds/add_excess_9" },
                { field: "premium_10_excess", shownBy: "/cds/add_excess_10" },]}
              title={"Option " + (n + 1)}
            />
            {/* The table below is for the output table for the cession premium splits */}
            <HX.Table kb-interactive shownBy="/cds/gmm_masking"
              data={[{ datum: "gmm_auto_liability", labelAlign: "left" },
              { datum: "gmm_employers_liability", labelAlign: "left" },
              { datum: "gmm_general_liability", labelAlign: "left" },
              { datum: "gmm_foreign_liability", labelAlign: "left" },
              { datum: "gmm_aircraft_nonowned", labelAlign: "left" },
              { datum: "gmm_aircraft_owned", labelAlign: "left" },
              { datum: "gmm_auto_ambulance", labelAlign: "left" },
              { datum: "gmm_educators_liability", labelAlign: "left" },
              { datum: "gmm_garage_keepers_liability", labelAlign: "left" },
              { datum: "gmm_helipad", labelAlign: "left" },
              { datum: "gmm_liquor_law_liability", labelAlign: "left" },
              { datum: "gmm_managed_care_eo_health_plan", labelAlign: "left" },
              { datum: "gmm_managed_care_eo_nonhealth_plan", labelAlign: "left" },
              { datum: "gmm_watercraft_nonowned", labelAlign: "left" },
              { datum: "gmm_watercraft_owned", labelAlign: "left" },
              ]}
              fields={[{ field: "cession_premium_split_1_excess", shownBy: "/cds/add_excess_1" },
              { field: "cession_premium_split_2_excess", shownBy: "/cds/add_excess_2" },
              { field: "cession_premium_split_3_excess", shownBy: "/cds/add_excess_3" },
              { field: "cession_premium_split_4_excess", shownBy: "/cds/add_excess_4" },
              { field: "cession_premium_split_5_excess", shownBy: "/cds/add_excess_5" },
              { field: "cession_premium_split_6_excess", shownBy: "/cds/add_excess_6" },
              { field: "cession_premium_split_7_excess", shownBy: "/cds/add_excess_7" },
              { field: "cession_premium_split_8_excess", shownBy: "/cds/add_excess_8" },
              { field: "cession_premium_split_9_excess", shownBy: "/cds/add_excess_9" },
              { field: "cession_premium_split_10_excess", shownBy: "/cds/add_excess_10" },]}
              title={"Cession Premium Splits Option " + (n + 1)}
            />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Table kb-interactive shownBy="/cds/glsn_masking"
              data={[{ datum: "glsn_auto_liability", labelAlign: "left" },
              { datum: "glsn_employers_liability", labelAlign: "left" },
              { datum: "glsn_general_liability", labelAlign: "left" },
              { datum: "glsn_foreign_liability", labelAlign: "left" },
              { datum: "glsn_aircraft_nonowned", labelAlign: "left" },
              { datum: "glsn_aircraft_owned", labelAlign: "left" },
              { datum: "glsn_garage_keepers_liability", labelAlign: "left" },
              { datum: "glsn_liquor_law_liability", labelAlign: "left" },
              { datum: "glsn_watercraft_non_owned", labelAlign: "left" },
              { datum: "glsn_watercraft_owned", labelAlign: "left" },
              { datum: "glsn_foreign_employers_liability", labelAlign: "left" },
              { datum: "glsn_foreign_general_liability", labelAlign: "left" },
              { datum: "glsn_foreign_auto_liability", labelAlign: "left" },
                null,
              { datum: "umbrella_eel", labelAlign: "left" },
                null,
              { datum: "umbrella_unsupported_net_premium", labelAlign: "left" },
              { datum: "umbrella_total_excess_net_premium", labelAlign: "left" },
                null,
              { datum: "umbrella_munich_cession_net", labelAlign: "left" },
              { datum: "umbrella_munich_cession_gross", labelAlign: "left" }]}
              fields={["premium_primary",
                { field: "premium_1_excess", shownBy: "/cds/add_excess_1" },
                { field: "premium_2_excess", shownBy: "/cds/add_excess_2" },
                { field: "premium_3_excess", shownBy: "/cds/add_excess_3" },
                { field: "premium_4_excess", shownBy: "/cds/add_excess_4" },
                { field: "premium_5_excess", shownBy: "/cds/add_excess_5" },
                { field: "premium_6_excess", shownBy: "/cds/add_excess_6" },
                { field: "premium_7_excess", shownBy: "/cds/add_excess_7" },
                { field: "premium_8_excess", shownBy: "/cds/add_excess_8" },
                { field: "premium_9_excess", shownBy: "/cds/add_excess_9" },
                { field: "premium_10_excess", shownBy: "/cds/add_excess_10" },]}
              title={"Option " + (n + 1)}
            />
            <HX.Table kb-interactive shownBy="/cds/glsn_masking"
              data={[{ datum: "glsn_auto_liability", labelAlign: "left" },
              { datum: "glsn_employers_liability", labelAlign: "left" },
              { datum: "glsn_general_liability", labelAlign: "left" },
              { datum: "glsn_foreign_liability", labelAlign: "left" },
              { datum: "glsn_aircraft_nonowned", labelAlign: "left" },
              { datum: "glsn_aircraft_owned", labelAlign: "left" },
              { datum: "glsn_garage_keepers_liability", labelAlign: "left" },
              { datum: "glsn_liquor_law_liability", labelAlign: "left" },
              { datum: "glsn_watercraft_non_owned", labelAlign: "left" },
              { datum: "glsn_watercraft_owned", labelAlign: "left" },
              { datum: "glsn_foreign_employers_liability", labelAlign: "left" },
              { datum: "glsn_foreign_general_liability", labelAlign: "left" },
              { datum: "glsn_foreign_auto_liability", labelAlign: "left" },
              ]}
              fields={[{ field: "cession_premium_split_1_excess", shownBy: "/cds/add_excess_1" },
              { field: "cession_premium_split_2_excess", shownBy: "/cds/add_excess_2" },
              { field: "cession_premium_split_3_excess", shownBy: "/cds/add_excess_3" },
              { field: "cession_premium_split_4_excess", shownBy: "/cds/add_excess_4" },
              { field: "cession_premium_split_5_excess", shownBy: "/cds/add_excess_5" },
              { field: "cession_premium_split_6_excess", shownBy: "/cds/add_excess_6" },
              { field: "cession_premium_split_7_excess", shownBy: "/cds/add_excess_7" },
              { field: "cession_premium_split_8_excess", shownBy: "/cds/add_excess_8" },
              { field: "cession_premium_split_9_excess", shownBy: "/cds/add_excess_9" },
              { field: "cession_premium_split_10_excess", shownBy: "/cds/add_excess_10" },]}
              title={"Cession Premium Splits Option " + (n + 1)}
            />
          </HX.Pane>


        </HX.With>

      </HX.Section >
    );
  }

  return objects
}




function vw_umbrella(scale) {
  return (
    <HX.Page title="Umbrella" fullWidth={true} viewScale={scale}>
      <HX.Section title="Umbrella Coverages">
        <HX.Pane>
          <HX.Table shownBy="/cds/gmm_masking"
            data={gmm_umbrella_class()}
            fields={["underlying_ee", "underlying_agg", "underlying_premium", "occurrence_cover"]}
            with="cds/rating_factors/gmm/umbrella"
            kb-interactive
          />
          <HX.Table shownBy="/cds/glsn_masking"
            data={glsn_umbrella_class()}
            fields={["underlying_ee", "underlying_agg", "underlying_premium", "occurrence_cover"]}
            with="cds/rating_factors/glsn/umbrella"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      {vw_umbrella_calcs(max_options())}

    </HX.Page>
  )
}

export { vw_umbrella };
