// v0.3.0
import * as HX from "hx-model-components";
import { exposure_detail_years } from "view/vw_constants";
import EditableText from "components/text_box_editable";

function vw_territory(scale) {
  return (
    <HX.Page title="Territory" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Instructions" defaultCollapsed={false}>
        <HX.Notes field="cds/exposure/granular/territory/instructions" title="How to use:" />
      </HX.Section>
      <HX.Section title="Options" defaultCollapsed={false}>
        <HX.Collection fields={["territory/bool_individual_country_level", "territory/bool_individual_state_level", "territory/is_percentage_bool", "bool_show_inception_year_client_details_input"]}
          horizontal
          with="cds/exposure/granular" />
      </HX.Section>
      <HX.Section title="Summary" defaultCollapsed={false}>
        {/* <EditableText textNode="cds/exposure/granular/territory/summary_label" pdfbutton={false} width="200" minHeight="30" maxHeight="30" /> */}
        <HX.Pane flow="right">
          <HX.Notes field="cds/exposure/granular/territory/summary_label" stretch={false} />
          <HX.Collection fields={[null]} />
          <HX.Collection fields={[null]} />
          <HX.Collection fields={[null]} />
        </HX.Pane>
        <HX.Table
          data={[
            { datum: "summary/total" }
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "summary_year_total_labels/year_0", shownBy: "bool_incept_year_pcnt", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "summary_year_total_labels/year_1", shownBy: "is_percentage_bool" },
            { field: "year_2_pcnt", width: 130, labelBy: "summary_year_total_labels/year_2", shownBy: "is_percentage_bool" },
            { field: "year_3_pcnt", width: 130, labelBy: "summary_year_total_labels/year_3", shownBy: "is_percentage_bool" },
            { field: "year_4_pcnt", width: 130, labelBy: "summary_year_total_labels/year_4", shownBy: "is_percentage_bool" },
            { field: "year_5_pcnt", width: 130, labelBy: "summary_year_total_labels/year_5", shownBy: "is_percentage_bool" },
            { field: "year_0_value", width: 130, labelBy: "summary_year_total_labels/year_0", shownBy: "bool_incept_year_value" },
            { field: "year_1_value", width: 130, labelBy: "summary_year_total_labels/year_1", shownBy: "is_percentage_bool_not" },
            { field: "year_2_value", width: 130, labelBy: "summary_year_total_labels/year_2", shownBy: "is_percentage_bool_not" },
            { field: "year_3_value", width: 130, labelBy: "summary_year_total_labels/year_3", shownBy: "is_percentage_bool_not" },
            { field: "year_4_value", width: 130, labelBy: "summary_year_total_labels/year_4", shownBy: "is_percentage_bool_not" },
            { field: "year_5_value", width: 130, labelBy: "summary_year_total_labels/year_5", shownBy: "is_percentage_bool_not" },
            null,
            { field: "weighted", width: 200 },
            null,
            { field: "elc", width: 200 },
          ]}
          rowHeaderSettings={{ width: 350 }}
          with="cds/exposure/granular/territory"
          dynamic
          kb-interactive
        />

        <HX.Table
          shownBy="bool_table_1"
          data={[
            { datum: "summary/united_kingdom", labelBy: "summary_modifier_labels/united_kingdom" },
            { datum: "summary/australia", labelBy: "summary_modifier_labels/australia" },
            { datum: "summary/canada", labelBy: "summary_modifier_labels/canada" },
            { datum: "summary/quebec", labelBy: "summary_modifier_labels/quebec" },
            { datum: "summary/ireland", labelBy: "summary_modifier_labels/ireland" },
            { datum: "summary/united_states", labelBy: "summary_modifier_labels/united_states" },
            { datum: "summary/asia_pac_south_africa", labelBy: "summary_modifier_labels/asia_pac_south_africa" },
            { datum: "summary/europe", labelBy: "summary_modifier_labels/europe" },
            { datum: "summary/middle_east", labelBy: "summary_modifier_labels/middle_east" },
            { datum: "summary/tax_haven", labelBy: "summary_modifier_labels/tax_haven" },
            { datum: "summary/rest_of_world", labelBy: "summary_modifier_labels/rest_of_world" },
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "bool_incept_year_pcnt", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool" },
            { field: "year_2_pcnt", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool" },
            { field: "year_3_pcnt", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool" },
            { field: "year_4_pcnt", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool" },
            { field: "year_5_pcnt", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool" },
            { field: "year_0_value", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "bool_incept_year_value" },
            { field: "year_1_value", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool_not" },
            { field: "year_2_value", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool_not" },
            { field: "year_3_value", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool_not" },
            { field: "year_4_value", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool_not" },
            { field: "year_5_value", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool_not" },
            null,
            { field: "weighted", width: 200 },
            null,
            { field: "frequency", width: 200 },
            { field: "severity", width: 200 }
          ]}
          rowHeaderSettings={{ width: 350 }}
          with="cds/exposure/granular/territory"
          dynamic
          kb-interactive
        />
        <HX.Table
          shownBy="bool_table_2"
          data={[
            { datum: "summary/united_kingdom", labelBy: "summary_modifier_labels/united_kingdom" },
            { datum: "summary/australia", labelBy: "summary_modifier_labels/australia" },
            { datum: "summary/canada", labelBy: "summary_modifier_labels/canada" },
            { datum: "summary/quebec", labelBy: "summary_modifier_labels/quebec" },
            { datum: "summary/ireland", labelBy: "summary_modifier_labels/ireland" },
            { datum: "summary/united_states", labelBy: "summary_modifier_labels/united_states" },
            { datum: "summary/asia_pac_south_africa_country_sum", labelBy: "summary_modifier_labels/asia_pac_south_africa" },
            { datum: "summary/europe_country_sum", labelBy: "summary_modifier_labels/europe" },
            { datum: "summary/middle_east_country_sum", labelBy: "summary_modifier_labels/middle_east" },
            { datum: "summary/tax_haven_country_sum", labelBy: "summary_modifier_labels/tax_haven" },
            { datum: "summary/rest_of_world_country_sum", labelBy: "summary_modifier_labels/rest_of_world" },
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool" },
            { field: "year_2_pcnt", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool" },
            { field: "year_3_pcnt", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool" },
            { field: "year_4_pcnt", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool" },
            { field: "year_5_pcnt", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool" },
            { field: "year_0_value", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool_not" },
            { field: "year_1_value", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool_not" },
            { field: "year_2_value", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool_not" },
            { field: "year_3_value", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool_not" },
            { field: "year_4_value", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool_not" },
            { field: "year_5_value", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool_not" },
            null,
            { field: "weighted", width: 200 },
            null,
            { field: "frequency", width: 200 },
            { field: "severity", width: 200 },
          ]}
          rowHeaderSettings={{ width: 350 }}
          with="cds/exposure/granular/territory"
          dynamic
          kb-interactive
        />
        <HX.Table
          shownBy="bool_table_3"
          data={[
            { datum: "summary/united_kingdom", labelBy: "summary_modifier_labels/united_kingdom" },
            { datum: "summary/australia", labelBy: "summary_modifier_labels/australia" },
            { datum: "summary/canada", labelBy: "summary_modifier_labels/canada" },
            { datum: "summary/quebec", labelBy: "summary_modifier_labels/quebec" },
            { datum: "summary/ireland", labelBy: "summary_modifier_labels/ireland" },
            { datum: "summary/united_states_state_sum", labelBy: "summary_modifier_labels/united_states" },
            { datum: "summary/asia_pac_south_africa", labelBy: "summary_modifier_labels/asia_pac_south_africa" },
            { datum: "summary/europe", labelBy: "summary_modifier_labels/europe" },
            { datum: "summary/middle_east", labelBy: "summary_modifier_labels/middle_east" },
            { datum: "summary/tax_haven", labelBy: "summary_modifier_labels/tax_haven" },
            { datum: "summary/rest_of_world", labelBy: "summary_modifier_labels/rest_of_world" },
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool" },
            { field: "year_2_pcnt", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool" },
            { field: "year_3_pcnt", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool" },
            { field: "year_4_pcnt", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool" },
            { field: "year_5_pcnt", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool" },
            { field: "year_0_value", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool_not" },
            { field: "year_1_value", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool_not" },
            { field: "year_2_value", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool_not" },
            { field: "year_3_value", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool_not" },
            { field: "year_4_value", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool_not" },
            { field: "year_5_value", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool_not" },
            null,
            { field: "weighted", width: 200 },
            null,
            { field: "frequency", width: 200 },
            { field: "severity", width: 200 }
          ]}
          rowHeaderSettings={{ width: 350 }}
          with="cds/exposure/granular/territory"
          dynamic
          kb-interactive
        />
        <HX.Table
          shownBy="bool_table_4"
          // title="Please enter by project location:"
          data={[
            { datum: "summary/united_kingdom", labelBy: "summary_modifier_labels/united_kingdom" },
            { datum: "summary/australia", labelBy: "summary_modifier_labels/australia" },
            { datum: "summary/canada", labelBy: "summary_modifier_labels/canada" },
            { datum: "summary/quebec", labelBy: "summary_modifier_labels/quebec" },
            { datum: "summary/ireland", labelBy: "summary_modifier_labels/ireland" },
            { datum: "summary/united_states_state_sum", labelBy: "summary_modifier_labels/united_states" },
            { datum: "summary/asia_pac_south_africa_country_sum", labelBy: "summary_modifier_labels/asia_pac_south_africa" },
            { datum: "summary/europe_country_sum", labelBy: "summary_modifier_labels/europe" },
            { datum: "summary/middle_east_country_sum", labelBy: "summary_modifier_labels/middle_east" },
            { datum: "summary/tax_haven_country_sum", labelBy: "summary_modifier_labels/tax_haven" },
            { datum: "summary/rest_of_world_country_sum", labelBy: "summary_modifier_labels/rest_of_world" },

          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool" },
            { field: "year_2_pcnt", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool" },
            { field: "year_3_pcnt", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool" },
            { field: "year_4_pcnt", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool" },
            { field: "year_5_pcnt", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool" },
            { field: "year_0_value", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool_not" },
            { field: "year_1_value", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool_not" },
            { field: "year_2_value", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool_not" },
            { field: "year_3_value", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool_not" },
            { field: "year_4_value", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool_not" },
            { field: "year_5_value", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool_not" },
            null,
            { field: "weighted", width: 200 },
            null,
            { field: "frequency", width: 200 },
            { field: "severity", width: 200 },
          ]}
          rowHeaderSettings={{ width: 350 }}
          with="cds/exposure/granular/territory"
          dynamic
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Individual Countries" shownBy="cds/exposure/granular/territory/bool_individual_country_level" defaultCollapsed={false}>
        <HX.Table
          data={[
            {
              datum: "individual_countries",
              elementLabelBy: "region",
            }

          ]}
          fields={[
            // { field: "territory_group", width: 150 },
            { field: "country", width: 175 },
            { field: "year_0_pcnt", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool" },
            { field: "year_2_pcnt", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool" },
            { field: "year_3_pcnt", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool" },
            { field: "year_4_pcnt", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool" },
            { field: "year_5_pcnt", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool" },
            { field: "year_0_value", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool_not" },
            { field: "year_1_value", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool_not" },
            { field: "year_2_value", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool_not" },
            { field: "year_3_value", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool_not" },
            { field: "year_4_value", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool_not" },
            { field: "year_5_value", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool_not" },
          ]}
          title="Individual Countries"
          rowHeaderSettings={{ width: 350 }}
          with="cds/exposure/granular/territory"
          dynamic
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Individual States" shownBy="cds/exposure/granular/territory/bool_individual_state_level" defaultCollapsed={false}>
        <HX.Table
          data={[
            {
              datum: "state",
              elementLabelBy: "state",
            }
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool" },
            { field: "year_2_pcnt", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool" },
            { field: "year_3_pcnt", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool" },
            { field: "year_4_pcnt", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool" },
            { field: "year_5_pcnt", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool" },
            { field: "year_0_value", width: 130, labelBy: "summary_year_labels/year_0", shownBy: "is_percentage_bool_not" },
            { field: "year_1_value", width: 130, labelBy: "summary_year_labels/year_1", shownBy: "is_percentage_bool_not" },
            { field: "year_2_value", width: 130, labelBy: "summary_year_labels/year_2", shownBy: "is_percentage_bool_not" },
            { field: "year_3_value", width: 130, labelBy: "summary_year_labels/year_3", shownBy: "is_percentage_bool_not" },
            { field: "year_4_value", width: 130, labelBy: "summary_year_labels/year_4", shownBy: "is_percentage_bool_not" },
            { field: "year_5_value", width: 130, labelBy: "summary_year_labels/year_5", shownBy: "is_percentage_bool_not" },
          ]}
          title="Individual States"
          rowHeaderSettings={{ width: 350 }}
          with="cds/exposure/granular/territory"
          dynamic
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Chart - FGU Loss by Territory" defaultCollapsed={false}>
        <HX.CategoryChart
          data={["united_kingdom",
            "australia",
            "canada",
            "quebec",
            "ireland",
            "united_states",
            "asia_pac_south_africa",
            "europe",
            "middle_east",
            "tax_haven",
            "rest_of_world"]}
          fields={["expected_loss_cost"]}
          columnType="cluster"
          with="cds/exposure/granular/territory/summary"
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_territory };