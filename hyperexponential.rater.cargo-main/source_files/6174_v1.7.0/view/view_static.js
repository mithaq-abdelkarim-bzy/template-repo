
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page title="Risk Information">
        <HX.Section title="Fetch Expiring Policy"
          shownBy="cds/standard_fields/is_renewal">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id"
            ]} />
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "inception_date",
              "expiry_date"
            ]}
              with="hx_core"
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/underwriter",
              "cds/term"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/insured_name"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "cds/standard_fields/policy_reference",
              "cds/currencies/source_currency",
              "cds/standard_fields/is_renewal"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage Selection">
          <HX.Collection with="cds/cover_selection"
            fields={[
            "select_message",
            "cover",
            {
              "field": "is_cargo_cyber",
              "shownBy": "show_cargo_cyber"
            }
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Policy Information">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "has_double_section_ref"
              ]}
                horizontal={true} />
              <HX.Pane />
            </HX.Pane>
            <HX.Table data={[
              "eea_section_reference",
              "non_eea_section_reference",
              "coverages/cargo_cyber_addon/eea_section_reference",
              "coverages/cargo_cyber_addon/non_eea_section_reference"
            ]}
              fields={[
              "ref",
              "type"
            ]}
              shownBy="has_double_section_ref"
              filter={[
              "/cds/main_polref_is_shown",
              "/cds/main_polref_is_shown",
              "/cds/cargo_cyber_is_shown",
              "/cds/cargo_cyber_is_shown"
            ]} />
            <HX.Table data={[
              "single_section_reference",
              "coverages/cargo_cyber_addon/single_section_reference"
            ]}
              fields={[
              "ref",
              "type"
            ]}
              shownBy="has_single_section_ref"
              filter={[
              "/cds/main_polref_is_shown",
              "/cds/cargo_cyber_is_shown"
            ]} />
            <HX.Collection fields={[
              "status",
              "brokerage",
              "written_line"
            ]}
              horizontal={true} />
            <HX.Pane flow="right"
              ratio={3}>
              <HX.Button task="pass_pas_reference"
                title="Pass Policy Reference to PAS" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Cargo"
        viewScale={1}
        shownBy="cds/cover_selection/is_cargo">
        <HX.Section title="Cargo - Transit"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "transit_flag",
                "base_rate"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "wh_to_port_flag",
                "loading_flag",
                "voyage_flag",
                "unloading_flag",
                "port_to_wh_flag"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "commodity",
                "commodity_factor"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "trans_vals",
                "trans_vals_factor"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "deductible_level",
                "deductible_level_factor"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "excess",
                "excess_factor"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "packaging",
                "packaging_factor"
              ]} />
              <HX.Section title="Cargo - Conveyance"
                collapsible={false}>
                <HX.Pane flow="right">
                  <HX.Collection with="coverages/cargo_transit"
                    fields={[
                    "conv_air",
                    "conv_land",
                    "conv_sea"
                  ]} />
                  <HX.Collection with="coverages/cargo_transit"
                    fields={[
                    "conv_air_factor",
                    "conv_land_factor",
                    "conv_sea_factor",
                    "conv_factor"
                  ]} />
                </HX.Pane>
                <HX.Collection with="coverages/cargo_transit"
                  horizontal={true}
                  fields={[
                  null,
                  "conv_check"
                ]}
                  shownBy="conv_check_show" />
              </HX.Section>
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "voyage",
                "voyage_factor"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "surveyor",
                "surveyor_factor"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "vessel",
                "vessel_factor"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "type_of_cover",
                "type_of_cover_factor"
              ]} />
              <HX.Collection with="coverages/cargo_transit"
                horizontal={true}
                fields={[
                "uw_discretion",
                "uw_discretion_factor"
              ]} />
              <HX.Section title="Premium Summary"
                defaultCollapsed={true}>
                <HX.Collection with="coverages/cargo_transit"
                  horizontal={true}
                  title="Model"
                  fields={[
                  "technical_deductions",
                  "technical_rate",
                  "technical_premium"
                ]} />
                <HX.Collection with="coverages/cargo_transit"
                  horizontal={true}
                  title="Actual"
                  fields={[
                  "pct_of_technical",
                  "actual_rate",
                  "quoted_premium"
                ]} />
              </HX.Section>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Cargo - Storage"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                "storage_flag",
                "base_rate"
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                "stock_vals",
                null
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                "deductible_level",
                "deductible_level_factor"
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                "excess",
                "excess_factor"
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                "survey",
                "survey_factor"
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                "risk_mgmt",
                "risk_mgmt_factor"
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                "type_of_cover",
                "type_of_cover_factor"
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                "uw_discretion",
                "uw_discretion_factor"
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                null,
                "rate"
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                "avg_val_pcm",
                null
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                title="Cargo - CAT"
                fields={[
                "cat_expo",
                "cat_pct_of_total",
                "combined_cat_load",
                "cat_expo_tp"
              ]} />
              <HX.Section title="CAT Exposure by Country"
                defaultCollapsed={true}>
                <HX.Table data={[
                  "coverages/cargo_storage/countries"
                ]}
                  fields={[
                  "country",
                  "cat_expo",
                  "cat_load",
                  "pct_of_cat"
                ]}
                  dynamic={true}
                  kb-interactive={true} />
              </HX.Section>
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                fields={[
                null,
                "cat_expo_check"
              ]}
                shownBy="cat_expo_check_show" />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                title="Retail"
                fields={[
                "retail_expo",
                "retail_pct_of_total",
                "retail_load",
                "retail_expo_tp"
              ]} />
              <HX.Collection with="coverages/cargo_storage"
                horizontal={true}
                title="Everything Else"
                fields={[
                "all_else_expo",
                "all_else_pct_of_total",
                "all_else_load",
                "all_else_expo_tp"
              ]} />
              <HX.Section title="Premium Summary"
                defaultCollapsed={true}>
                <HX.Collection with="coverages/cargo_storage"
                  horizontal={true}
                  title="Model"
                  fields={[
                  "technical_deductions",
                  "technical_rate",
                  "technical_premium"
                ]} />
                <HX.Collection with="coverages/cargo_storage"
                  horizontal={true}
                  title="Actual"
                  fields={[
                  "pct_of_technical",
                  "actual_rate",
                  "quoted_premium"
                ]} />
              </HX.Section>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Cargo Cyber"
        viewScale={1}
        shownBy="cds/cover_selection/is_cargo_cyber_combined">
        <HX.Section title="">
          <HX.Button title="Load Cargo Input"
            task="load_cargo_input"
            shownBy="cds/cover_selection/is_cargo_cyber" />
        </HX.Section>
        <HX.Section title="Cargo Cyber - Transit"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "transit_flag",
                "base_rate"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "wh_to_port_flag",
                "loading_flag",
                "voyage_flag",
                "unloading_flag",
                "port_to_wh_flag"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "commodity",
                "commodity_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "trans_vals",
                "trans_vals_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "deductible_level",
                "deductible_level_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "excess",
                "excess_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "packaging",
                "packaging_factor"
              ]} />
              <HX.Section title="Cargo Cyber - Conveyance"
                collapsible={false}>
                <HX.Pane flow="right">
                  <HX.Collection with="coverages/cargo_cyber_transit"
                    fields={[
                    "conv_air",
                    "conv_land",
                    "conv_sea"
                  ]} />
                  <HX.Collection with="coverages/cargo_cyber_transit"
                    fields={[
                    "conv_air_factor",
                    "conv_land_factor",
                    "conv_sea_factor",
                    "conv_factor"
                  ]} />
                </HX.Pane>
                <HX.Collection with="coverages/cargo_cyber_transit"
                  horizontal={true}
                  fields={[
                  null,
                  "conv_check"
                ]}
                  shownBy="conv_check_show" />
              </HX.Section>
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "voyage",
                "voyage_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "surveyor",
                "surveyor_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "vessel",
                "vessel_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "type_of_cover",
                "type_of_cover_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_transit"
                horizontal={true}
                fields={[
                "uw_discretion",
                "uw_discretion_factor"
              ]} />
              <HX.Section title="Premium Summary"
                defaultCollapsed={true}>
                <HX.Collection with="coverages/cargo_cyber_transit"
                  horizontal={true}
                  title="Model"
                  fields={[
                  "technical_deductions",
                  "technical_rate",
                  "technical_premium"
                ]} />
                <HX.Collection with="coverages/cargo_cyber_transit"
                  horizontal={true}
                  title="Actual"
                  fields={[
                  "pct_of_technical",
                  "actual_rate",
                  "quoted_premium"
                ]} />
              </HX.Section>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Cargo Cyber - Storage"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                "storage_flag",
                "base_rate"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                "stock_vals",
                null
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                "deductible_level",
                "deductible_level_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                "excess",
                "excess_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                "survey",
                "survey_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                "risk_mgmt",
                "risk_mgmt_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                "type_of_cover",
                "type_of_cover_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                "uw_discretion",
                "uw_discretion_factor"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                null,
                "rate"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                "avg_val_pcm",
                null
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                title="Cargo Cyber - CAT"
                fields={[
                "cat_expo",
                "cat_pct_of_total",
                "combined_cat_load",
                "cat_expo_tp"
              ]} />
              <HX.Section title="CAT Exposure by Country"
                defaultCollapsed={true}>
                <HX.Table data={[
                  "coverages/cargo_cyber_storage/countries"
                ]}
                  fields={[
                  "country",
                  "cat_expo",
                  "cat_load",
                  "pct_of_cat"
                ]}
                  dynamic={true}
                  kb-interactive={true} />
              </HX.Section>
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                fields={[
                null,
                "cat_expo_check"
              ]}
                shownBy="cat_expo_check_show" />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                title="Retail"
                fields={[
                "retail_expo",
                "retail_pct_of_total",
                "retail_load",
                "retail_expo_tp"
              ]} />
              <HX.Collection with="coverages/cargo_cyber_storage"
                horizontal={true}
                title="Everything Else"
                fields={[
                "all_else_expo",
                "all_else_pct_of_total",
                "all_else_load",
                "all_else_expo_tp"
              ]} />
              <HX.Section title="Premium Summary"
                defaultCollapsed={true}>
                <HX.Collection with="coverages/cargo_cyber_storage"
                  horizontal={true}
                  title="Model"
                  fields={[
                  "technical_deductions",
                  "technical_rate",
                  "technical_premium"
                ]} />
                <HX.Collection with="coverages/cargo_cyber_storage"
                  horizontal={true}
                  title="Actual"
                  fields={[
                  "pct_of_technical",
                  "actual_rate",
                  "quoted_premium"
                ]} />
              </HX.Section>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Specie"
        viewScale={1}
        shownBy="cds/cover_selection/is_specie">
        <HX.Section title="Transit"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection with="coverages/specie_transit"
                horizontal={true}
                fields={[
                "transit_flag",
                "base_rate"
              ]} />
              <HX.Collection with="coverages/specie_transit"
                horizontal={true}
                fields={[
                "commodity",
                "commodity_factor"
              ]} />
              <HX.Collection with="coverages/specie_transit"
                horizontal={true}
                fields={[
                "trans_vals",
                "trans_vals_factor"
              ]} />
              <HX.Collection with="coverages/specie_transit"
                horizontal={true}
                fields={[
                "deductible_level",
                "deductible_level_factor"
              ]} />
              <HX.Collection with="coverages/specie_transit"
                horizontal={true}
                fields={[
                "excess",
                "excess_factor"
              ]} />
              <HX.Collection with="coverages/specie_transit"
                horizontal={true}
                fields={[
                "type_of_cover",
                "type_of_cover_factor"
              ]} />
              <HX.Collection with="coverages/specie_transit"
                horizontal={true}
                fields={[
                "uw_discretion",
                "uw_discretion_factor"
              ]} />
              <HX.Section title="Premium Summary"
                defaultCollapsed={true}>
                <HX.Collection with="coverages/specie_transit"
                  horizontal={true}
                  title="Model"
                  fields={[
                  "technical_deductions",
                  "technical_rate",
                  "technical_premium"
                ]} />
                <HX.Collection with="coverages/specie_transit"
                  horizontal={true}
                  title="Actual"
                  fields={[
                  "pct_of_technical",
                  "actual_rate",
                  "quoted_premium"
                ]} />
              </HX.Section>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Storage"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "storage_flag",
                "base_rate"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "commodity",
                "commodity_factor"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "stock_vals",
                "stock_vals_factor"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "deductible_level",
                "deductible_level_factor"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "excess",
                "excess_factor"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "survey",
                "survey_factor"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "risk_mgmt",
                "risk_mgmt_factor"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "type_of_cover",
                "type_of_cover_factor"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "uw_discretion",
                "uw_discretion_factor"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                null,
                "rate"
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                "avg_val_pcm",
                null
              ]} />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                title="CAT"
                fields={[
                "cat_expo",
                "cat_pct_of_total",
                "combined_cat_load",
                "cat_expo_tp"
              ]} />
              <HX.Section title="CAT Exposure by Country"
                defaultCollapsed={true}>
                <HX.Table data={[
                  "coverages/specie_storage/countries"
                ]}
                  fields={[
                  "country",
                  "cat_expo",
                  "cat_load",
                  "pct_of_cat"
                ]}
                  dynamic={true}
                  kb-interactive={true} />
              </HX.Section>
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                fields={[
                null,
                "cat_expo_check"
              ]}
                shownBy="cat_expo_check_show" />
              <HX.Collection with="coverages/specie_storage"
                horizontal={true}
                title="Non-CAT"
                fields={[
                "non_cat_expo",
                "non_cat_pct_of_total",
                "non_cat_load",
                "non_cat_expo_tp"
              ]} />
              <HX.Section title="Premium Summary"
                defaultCollapsed={true}>
                <HX.Collection with="coverages/specie_storage"
                  horizontal={true}
                  title="Model"
                  fields={[
                  "technical_deductions",
                  "technical_rate",
                  "technical_premium"
                ]} />
                <HX.Collection with="coverages/specie_storage"
                  horizontal={true}
                  title="Actual"
                  fields={[
                  "pct_of_technical",
                  "actual_rate",
                  "quoted_premium"
                ]} />
              </HX.Section>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Con Loss"
        viewScale={1}
        shownBy="cds/cover_selection/is_conloss">
        <HX.Section title="Transit"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection with="coverages/conloss_transit"
                horizontal={true}
                fields={[
                "transit_flag",
                "base_rate"
              ]} />
              <HX.Collection with="coverages/conloss_transit"
                horizontal={true}
                fields={[
                "trans_vals",
                "trans_vals_factor"
              ]} />
              <HX.Collection with="coverages/conloss_transit"
                horizontal={true}
                fields={[
                "deductible_level",
                "deductible_level_factor"
              ]} />
              <HX.Section title="Packaging"
                collapsible={false}>
                <HX.Pane flow="right">
                  <HX.Collection with="coverages/conloss_transit"
                    fields={[
                    "packaging_1",
                    "packaging_2"
                  ]} />
                  <HX.Collection with="coverages/conloss_transit"
                    fields={[
                    "packaging_1_factor",
                    "packaging_2_factor",
                    "packaging_factor"
                  ]} />
                </HX.Pane>
                <HX.Collection with="coverages/conloss_transit"
                  horizontal={true}
                  fields={[
                  null,
                  "packaging_check"
                ]}
                  shownBy="packaging_check_show" />
              </HX.Section>
              <HX.Section title="Conveyance"
                collapsible={false}>
                <HX.Pane flow="right">
                  <HX.Collection with="coverages/conloss_transit"
                    fields={[
                    "conv_air",
                    "conv_land",
                    "conv_sea"
                  ]} />
                  <HX.Collection with="coverages/conloss_transit"
                    fields={[
                    "conv_air_factor",
                    "conv_land_factor",
                    "conv_sea_factor",
                    "conv_factor"
                  ]} />
                </HX.Pane>
                <HX.Collection with="coverages/conloss_transit"
                  horizontal={true}
                  fields={[
                  null,
                  "conv_check"
                ]}
                  shownBy="conv_check_show" />
              </HX.Section>
              <HX.Collection with="coverages/conloss_transit"
                horizontal={true}
                fields={[
                "voyage",
                "voyage_factor"
              ]} />
              <HX.Collection with="coverages/conloss_transit"
                horizontal={true}
                fields={[
                "surveyor",
                "surveyor_factor"
              ]} />
              <HX.Collection with="coverages/conloss_transit"
                horizontal={true}
                fields={[
                "vessel",
                "vessel_factor"
              ]} />
              <HX.Collection with="coverages/conloss_transit"
                horizontal={true}
                fields={[
                "type_of_cover",
                "type_of_cover_factor"
              ]} />
              <HX.Collection with="coverages/conloss_transit"
                horizontal={true}
                fields={[
                "uw_discretion",
                "uw_discretion_factor"
              ]} />
              <HX.Section title="Premium Summary"
                defaultCollapsed={true}>
                <HX.Collection with="coverages/conloss_transit"
                  horizontal={true}
                  title="Model"
                  fields={[
                  "technical_deductions",
                  "technical_rate",
                  "technical_premium"
                ]} />
                <HX.Collection with="coverages/conloss_transit"
                  horizontal={true}
                  title="Actual"
                  fields={[
                  "pct_of_technical",
                  "actual_rate",
                  "quoted_premium"
                ]} />
              </HX.Section>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Con Loss"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection with="coverages/conloss"
                horizontal={true}
                fields={[
                "conloss_flag",
                "base_rate"
              ]} />
              <HX.Collection with="coverages/conloss"
                horizontal={true}
                fields={[
                "limit",
                "limit_factor"
              ]} />
              <HX.Collection with="coverages/conloss"
                horizontal={true}
                fields={[
                "exposure",
                "exposure_factor"
              ]} />
              <HX.Collection with="coverages/conloss"
                horizontal={true}
                fields={[
                "indemnity_period",
                null
              ]} />
              <HX.Collection with="coverages/conloss"
                horizontal={true}
                fields={[
                "deductible_level",
                "deductible_level_factor"
              ]} />
              <HX.Collection with="coverages/conloss"
                horizontal={true}
                fields={[
                null,
                "indemnity_message"
              ]}
                shownBy="indemnity_message_show" />
              <HX.Collection with="coverages/conloss"
                horizontal={true}
                fields={[
                "uw_discretion",
                "uw_discretion_factor"
              ]} />
              <HX.Section title="Premium Summary"
                defaultCollapsed={true}>
                <HX.Collection with="coverages/conloss"
                  horizontal={true}
                  title="Model"
                  fields={[
                  "technical_deductions",
                  "technical_rate",
                  "technical_premium"
                ]} />
                <HX.Collection with="coverages/conloss"
                  horizontal={true}
                  title="Actual"
                  fields={[
                  "pct_of_technical",
                  "actual_rate",
                  "quoted_premium"
                ]} />
              </HX.Section>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        shownBy="cds/cover_selection/is_selected">
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Summary - Main Coverage">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/cover_selection/cover"
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Table data={[
              "eea_section_reference",
              "non_eea_section_reference"
            ]}
              fields={[
              "ref",
              "type"
            ]}
              shownBy="has_double_section_ref" />
            <HX.Table data={[
              "single_section_reference"
            ]}
              fields={[
              "ref",
              "type"
            ]}
              shownBy="has_single_section_ref" />
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "brokerage",
              "written_line"
            ]} />
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}
            shownBy="cds/standard_fields/is_rater_priced">
            <HX.Collection title="Priced Quotes"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "gross_premium_label"
              },
              "benchmark_premium",
              "technical_premium",
              "technical_premium_pre_uw_adj"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "tpi",
              "tpi_pre_uw_adj",
              "bpi",
              "pflr",
              "pflr_att",
              "pflr_cat"
            ]} />
            <HX.Collection title="Other Metrics"
              numCols={2}
              fields={[
              "roc",
              "uw_adj_impact"
            ]} />
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}
            shownBy="cds/standard_fields/is_case_priced">
            <HX.Collection title="Priced Quotes"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "gross_premium_label"
              },
              "bpi_case_priced",
              "technical_premium",
              "benchmark_premium"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "tpi",
              "pflr",
              "roc"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary - Cargo Cyber Add On"
          shownBy="cds/cover_selection/is_cargo_cyber">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Table data={[
              "coverages/cargo_cyber_addon/eea_section_reference",
              "coverages/cargo_cyber_addon/non_eea_section_reference"
            ]}
              fields={[
              "ref",
              "type"
            ]}
              shownBy="has_double_section_ref" />
            <HX.Table data={[
              "coverages/cargo_cyber_addon/single_section_reference"
            ]}
              fields={[
              "ref",
              "type"
            ]}
              shownBy="has_single_section_ref" />
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "coverages/cargo_cyber_addon/brokerage",
              "coverages/cargo_cyber_addon/written_line"
            ]} />
          </HX.With>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}
            shownBy="cds/standard_fields/is_rater_priced">
            <HX.Collection title="Priced Quotes"
              numCols={2}
              fields={[
              {
                "field": "coverages/cargo_cyber_addon/quoted_premium",
                "labelBy": "gross_premium_label"
              },
              "coverages/cargo_cyber_addon/benchmark_premium",
              "coverages/cargo_cyber_addon/technical_premium",
              "coverages/cargo_cyber_addon/technical_premium_pre_uw_adj"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              with="coverages/cargo_cyber_addon"
              fields={[
              "tpi",
              "tpi_pre_uw_adj",
              "bpi",
              "pflr",
              "pflr_att",
              "pflr_cat"
            ]} />
            <HX.Collection title="Other Metrics"
              numCols={2}
              with="coverages/cargo_cyber_addon"
              fields={[
              "roc",
              "uw_adj_impact"
            ]} />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        shownBy="cds/standard_fields/is_renewal">
        <HX.With context={{
          "index": 0,
          "path": "cds/layers",
          "type": "list"
        }}>
          <HX.Section title="Renewal vs. Expiring"
            shownBy="/cds/rate_change/show_layer_1">
            <HX.Pane>
              <HX.Table data={[
                "premium_policy_term_100pct",
                "premium_policy_term_beazley_share",
                "written_line",
                null,
                "benchmark_premium",
                "bpi",
                null,
                "technical_premium",
                "tpi"
              ]}
                fields={[
                {
                  "field": "renewal",
                  "width": 200
                },
                {
                  "field": "expiring",
                  "width": 200
                }
              ]}
                with="rate_change" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Rate Change"
            shownBy="/cds/rate_change/has_expiring_data"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Button task="rarc_task"
                title="Calculate Rate Change" />
              <HX.Pane />
            </HX.Pane>
            <HX.Notes with="/cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
            <HX.Pane shownBy="/cds/rate_change/rarc_calcs_show">
              <HX.Pane>
                <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                  data={[
                  "exposure_change",
                  "risk_characteristics_change",
                  "deductible_change",
                  "limit_change",
                  "terms_conditions_change",
                  "brokerage_change",
                  "other_change",
                  null,
                  "rate_change"
                ]}
                  fields={[
                  {
                    "field": "model_calculated",
                    "width": 125
                  },
                  {
                    "field": "uw_selected",
                    "width": 125
                  },
                  {
                    "field": "comments",
                    "width": 250
                  }
                ]}
                  with="rate_change" />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection title="Final Rate Change (Gross Brokerage)"
                  fields={[
                  "rate_change/risk_adjusted_rate_change/uw_selected"
                ]}
                  shownBy="/cds/standard_fields/is_rater_priced" />
                <HX.Collection title="Final Rate Change (Gross Brokerage)"
                  fields={[
                  "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
                ]}
                  shownBy="/cds/standard_fields/is_case_priced" />
                <HX.Collection title=" "
                  fields={[
                  "rate_change/risk_adjusted_rate_change_case_priced/comments"
                ]}
                  shownBy="/cds/standard_fields/is_case_priced" />
                <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}
        shownBy="cds/cover_selection/is_selected">
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
        <HX.Section title="Policy Document">
          <HX.Button task="policy_to_excel_task"
            title="Generate Policy Document"
            shownBy="policy_doc/show_generate_button" />
          <HX.Notes field="policy_doc/premium_check"
            shownBy="policy_doc/show_premium_check" />
          <HX.File with="policy_doc"
            field="output_file"
            title="Click on the icon below to download the policy document"
            shownBy="show_download" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs">
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}
          shownBy="cds/cover_selection/is_selected">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status_view",
              "section_reference_view",
              "brokerage_view",
              "written_line_view"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_view",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]}
              shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]}
              shownBy="/cds/standard_fields/is_rater_priced" />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_view",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi"
            ]}
              shownBy="/cds/standard_fields/is_case_priced" />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]}
              shownBy="/cds/standard_fields/is_case_priced" />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Something is Broken">
        <HX.With context={{
          "path": "bug_report",
          "type": "struct"
        }}>
          <HX.Section title="Log a New Incident">
            <HX.Notes field="helper_text" />
            <HX.Pane>
              <HX.Button task="new_bug_report_task"
                title="Log a New Incident" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Incident Details"
            shownBy="commenced_flag">
            <HX.Pane>
              <HX.Collection fields={[
                "summary"
              ]}
                title="Summary" />
              <HX.Notes field="email_body"
                title="Details" />
              <HX.Pane flow="right"
                ratio={2}>
                <HX.Pane shownBy="inputs_outputs_file_show">
                  <HX.File field="inputs_outputs_file"
                    title="Inputs/Outputs Attachment" />
                  <HX.Button task="generate_bug_report_task"
                    title="Generate Inputs/Outputs" />
                </HX.Pane>
                <HX.With context={{
                  "path": "screenshot_files",
                  "type": "struct"
                }}>
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f1/show_text" />
                  <HX.File field="f1/file"
                    title="Screenshot Attachment"
                    shownBy="f1/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f2/show_text" />
                  <HX.File field="f2/file"
                    title="Screenshot Attachment 2"
                    shownBy="f2/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f3/show_text" />
                  <HX.File field="f3/file"
                    title="Screenshot Attachment 3"
                    shownBy="f3/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f4/show_text" />
                  <HX.File field="f4/file"
                    title="Screenshot Attachment 4"
                    shownBy="f4/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f5/show_text" />
                  <HX.File field="f5/file"
                    title="Screenshot Attachment 5"
                    shownBy="f5/show_file" />
                </HX.With>
              </HX.Pane>
              <HX.Button task="add_additional_file_task"
                title="Upload Additional Screenshots" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="send_bug_report_task"
                title="Send Incident" />
              <HX.Button task="cancel_bug_report_task"
                title="Cancel Incident" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};