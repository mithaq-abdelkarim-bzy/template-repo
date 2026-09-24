// v0.3.0
import * as HX from "hx-model-components";
import EditableText from "components/text_box_editable";
import { exposure_detail_years } from "view/vw_constants";

function vw_client_details_lawyers(scale) {
  return (
    <HX.Page title="Client Details - Lawyers" shownBy="cds/profession_lawyers_bool" fullWidth={true} viewScale={scale}>
      <HX.Section title="Instructions" defaultCollapsed={false}>
        <HX.Notes field="cds/exposure/granular/client_details_lawyers/notes" />
      </HX.Section>
      <HX.Section title="Areas of Practice" defaultCollapsed={false}>
        <HX.Collection fields={["cds/exposure/granular/client_details_lawyers/bool_is_pcnt",
          "cds/exposure/granular/bool_show_inception_year_client_details_input",
          null,
          null]}
          horizontal />
        <HX.Table
          data={[
            { datum: "client_details_lawyers/areas_of_practice_total" }
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_pcnt", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_1", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_2_pcnt", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_2", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_3_pcnt", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_3", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_4_pcnt", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_4", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_5_pcnt", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_5", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_0_value", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_value", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_value", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_1", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            { field: "year_2_value", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_2", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            { field: "year_3_value", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_3", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            { field: "year_4_value", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_4", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            { field: "year_5_value", width: 130, labelBy: "client_details_lawyers/summary_year_total_aop_labels/year_5", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            null,
            { field: "weighted", width: 130 },
            null,
            { field: "elc", width: 200 }
            // { field: "frequency", width: 200 },
            // { field: "severity", width: 200 },
          ]}
          rowHeaderSettings={{ width: 460 }}
          with="cds/exposure/granular"
          dynamic
          kb-interactive
        />
        <HX.Table
          data={[
            {
              datum: "client_details_lawyers/areas_of_practice",
              elementLabelBy: "areas_of_practice",
            }
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_pcnt", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_1", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_2_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_2", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_3_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_3", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_4_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_4", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_5_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_5", shownBy: "client_details_lawyers/bool_is_pcnt" },
            { field: "year_0_value", width: 130, labelBy: "territory/summary_year_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_value", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_value", width: 130, labelBy: "territory/summary_year_labels/year_1", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            { field: "year_2_value", width: 130, labelBy: "territory/summary_year_labels/year_2", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            { field: "year_3_value", width: 130, labelBy: "territory/summary_year_labels/year_3", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            { field: "year_4_value", width: 130, labelBy: "territory/summary_year_labels/year_4", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            { field: "year_5_value", width: 130, labelBy: "territory/summary_year_labels/year_5", shownBy: "client_details_lawyers/bool_is_pcnt_not" },
            null,
            { field: "weighted", width: 130 },
            null,
            { field: "frequency", width: 200 },
            { field: "severity", width: 200 },
          ]}
          rowHeaderSettings={{ width: 460 }}
          with="cds/exposure/granular"
          dynamic
          kb-interactive
        />
      </HX.Section>
      {/* <HX.Section title="Chart - Loss Cost by Area of Practice" defaultCollapsed={false}>
        <HX.CategoryChart
          data={["banking_financial_institutions",
            "bankruptcy_insolvency_restructuring",
            "class_actions",
            "construction",
            "corporate_commercial",
            "criminal",
            "debt_collection",
            "dispute_resolution",
            "employment_labour",
            "entertainment",
            "environmental",
            "family_matrimonial_children",
            "government",
            "immigration",
            "insurance",
            "intellectual_property_copyright_patent_litigation",
            "intellectual_property_copyright_patent_prosecution",
            "ma",
            "management_risk_consultancy",
            "natural_resources_energy",
            "pensions",
            "personal_injury_workers_comp_product_liability",
            "real_estate_conveyancing_commercial",
            "real_estate_conveyancing_residential",
            "regulatory_competition_antitrust_law_lobbying",
            "securities",
            "taxation",
            "trust_probate_wills"
          ]}
          fields={["expected_loss_cost"]}
          columnType="cluster"
          with="cds/exposure/granular/client_details_lawyers/areas_of_practice_chart"
        />
      </HX.Section> */}
      <HX.Section title="Client Specifics" defaultCollapsed={false}>
        <HX.Collection fields={["cds/exposure/granular/client_details_lawyers/size_of_matters", null]} horizontal />
        <EditableText textNode="cds/exposure/granular/client_details_lawyers/uw_comments" placeholderText="Underwriter Comments" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_client_details_lawyers };