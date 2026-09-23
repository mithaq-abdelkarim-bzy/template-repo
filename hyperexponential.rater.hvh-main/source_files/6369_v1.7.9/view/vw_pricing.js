import * as HX from "hx-model-components";
import {
  perils_covered_tables_configs, pricing_table_config,
  kpi_splits_tables_configs, hvh_kpi_premiums_tables_configs,
  paf_kpi_premiums_tables_configs, total_kpi_premiums_tables_configs,
  paf_deductibles_configs
} from "view/vw_option_tables_configs";
import { generate_tables } from "view/vw_build_option_tables";


function vw_pricing(scale) {
  return (
    <HX.Page title="Pricing" fullWidth={true} viewScale={scale}>
      <HX.Section title="Set Number of Options">
        <HX.Pane flow="right">
          <HX.Collection fields={["number_of_options"]} with="cds" horizontal syncColumnWidthsKey="number_of_options" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Perils Covered">
        <HX.Button task="generate_recommended_peril_inclusions" title="Generate Recommended Perils & Limits" />
        {generate_tables(perils_covered_tables_configs)}
      </HX.Section>
      <HX.Section title="Pricing">
        {generate_tables(pricing_table_config)}
        <HX.Section title="PAF" shownBy="cds/show_paf_options">
          <HX.Collection fields={[
            "/cds/exposure/granular/paf/based_in_nyc_metro_area",
            "insured_occupation",
            // { field: "insured_occupation", shownBy: "/cds/validation/insured_occupation/valid" },
            // { field: "insured_occupation.notSupported", shownBy: "/cds/validation/insured_occupation/invalid", infoBy: "/cds/validation/insured_occupation/info_text" },
            "safe",
            "credit_score"
          ]} with='cds/rating_factors' horizontal />
          <HX.Table
            data={[
              "cameras_scheduled_professional_use",
              "cameras_scheduled_personal_use",
              "cameras_blanket",
              "fine_art_scheduled_non_fragile",
              "fine_art_scheduled_fragile",
              "fine_art_blanket",
              "gold_silver_bullion_bank_vault",
              "gold_silver_bullion_home_safe",
              "golf_clubs_scheduled",
              "golf_clubs_scheduled_golf_carts_excluding_collision",
              "jewellery_watches_scheduled_jewellery",
              "jewellery_watches_scheduled_watches",
              "jewellery_watches_scheduled_jewellery_watches_bank_vault_only",
              "jewellery_watches_blanket",
              "musical_instruments_scheduled_professional_use",
              "musical_instruments_scheduled_personal_use",
              "musical_instruments_blanket",
              null,
              "/cds/exposure/granular/paf/specific_schedules_totals_structure",
            ]}
            fields={[
              "tiv",
              "coverage_type",
              "rate"
            ]}
            with="cds/exposure/granular/paf/specific_schedules_structure"
            kb-interactive
            syncColumnWidthsKey="paf_section"
          />
          <HX.Table
            data={[
              "antique_furniture",
              "baseball_sports_cards_and_comic_books",
              "books",
              "coins",
              "furs",
              "guns",
              "handbags",
              "memorabilia",
              "rugs",
              "silverware",
              "stamps",
              "wine_and_cigars",
              "audio_visual_equipment",
              "bicycles",
              "computers",
              "misc",
              null,
              "/cds/exposure/granular/paf/scheduled_and_blanket_coverages_totals_structure",
            ]}
            fields={[
              "scheduled_tiv",
              "blanket_tiv",
              "scheduled_rate",
              "blanket_rate"
            ]}
            with="cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure"
            kb-interactive
            syncColumnWidthsKey="paf_section"
          />
          <HX.Notes field="cds/notes/paf_pricing_collectible_classification_note.read_only" />
          <HX.Collection fields={["tiv"]} with="cds/exposure/aggregate/paf" syncColumnWidthsKey="paf_section" />
          <HX.Collection fields={["base_premium", "base_rate"]} horizontal with="cds/exposure/aggregate/paf" syncColumnWidthsKey="paf_section" />
          <HX.Collection fields={["total_modifier_impact/option_to_bind_factor"]} with="cds/rating_factors/paf" syncColumnWidthsKey="paf_section" />
          <HX.Section title="Mysterious Disappearance Coverage">
            <HX.Collection fields={[
              "include",
              { field: "engagement_ring", shownBy: "include" },
              { field: "tiv", shownBy: "include" },
              { field: "base_premium", shownBy: "include" },
            ]} with="cds/exposure/granular/paf/my_dis_coverage" syncColumnWidthsKey="paf_section" />
          </HX.Section>
          <HX.Collection fields={["wearing_limit"]} with="cds/exposure/granular/paf" syncColumnWidthsKey="paf_section" />
          <HX.Collection fields={["paid_claims_amount_last_five_years", "paid_claims_impact"]} with="cds/exposure/granular/paf" horizontal syncColumnWidthsKey="paf_section" />
          <HX.Collection fields={["single_item_limit", "single_item_limit_impact"]} with="cds/exposure/granular/paf" horizontal syncColumnWidthsKey="paf_section" />
          {generate_tables(paf_deductibles_configs)}
        </HX.Section>
      </HX.Section>
      <HX.Section title="Final KPIs">
        {generate_tables(kpi_splits_tables_configs)}
        <HX.Section title="Premiums / Rates">
          <HX.Collection fields={["kpis_rate_premium_toggle"]}
            syncColumnWidthsKey="number_of_options"
            with="cds" />
          {generate_tables(hvh_kpi_premiums_tables_configs)}
          <HX.Pane flow="right">
            <HX.Notes field="cds/notes/hvh_cp_deviate_warning" shownBy="cds/notes/hvh_cp_deviate_warning_flag" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          {generate_tables(paf_kpi_premiums_tables_configs)}
          <HX.Pane flow="right">
            <HX.Notes field="cds/notes/paf_cp_deviate_warning" shownBy="cds/notes/paf_cp_deviate_warning_flag" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          {generate_tables(total_kpi_premiums_tables_configs)}
        </HX.Section >
      </HX.Section >
    </HX.Page >
  )
}

export { vw_pricing };