import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "cds/standard_fields/rating_methodology",
            { field: "cds/case_pricing_analysis_location", shownBy: "/cds/show_case_priced" }
          ]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Mandatory Details">
        <HX.Pane >
          <HX.Collection
            numCols={3}
            fields={[
              "cds/standard_fields/insured_name",
              "cds/standard_fields/underwriter",
              "cds/standard_fields/broker",
              "cds/deadline_date",
              "hx_core/inception_date",
              "hx_core/expiry_date",
              "cds/standard_fields/is_renewal",
              "cds/short_description",
              null,
              { field: "cds/underwriter_location", shownBy: "cds/show_bermuda" },
              { field: "cds/discussed_london", shownBy: "cds/show_bermuda" },
              { field: "cds/technical_underwriter", shownBy: "cds/show_bermuda" }
            ]}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Status">
        <HX.Pane >
          <HX.Collection
            numCols={3}
            fields={[
              "cds/deal_status",
              "cds/quotation",
              "cds/quoted"
            ]}
          />
          <HX.Collection
            numCols={3}
            fields={[
              { field: "cds/declinature_reason", shownBy: "/cds/show_declined_reasons" },
              { field: "cds/declinature_comments", shownBy: "/cds/show_declined_reasons" },
              null
            ]}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Rating Details">
        <HX.Pane>
          <HX.Collection
            numCols={3}
            fields={[
              "cds/programme",
              "cds/calc_type",
              "cds/currency",
              "cds/multi_year",
              "cds/brokerage",
              "cds/tax",
              "cds/treaty_basis",
              { field: "cds/second_loss_brokerage", shownBy: "cds/show_bermuda" },
              { field: "cds/ceding_commission", shownBy: "cds/show_ceding_commission" },
              { field: "cds/other_acq_costs", shownBy: "cds/show_ceding_commission" },
              { field: "cds/includes_us_exposure", shownBy: "cds/show_intl_fields" }
            ]}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Additional Risk Details">
        <HX.Pane>
          <HX.Collection
            numCols={3}
            fields={[
              "cds/territory",
              "cds/adj_base",
              "cds/territorial_focus_group",
              "cds/market_share",
              "cds/broker_contact",
              "cds/risk_carrier",
              "cds/personal_commercial",
              "cds/core_account",
              "cds/met_client_last_12_months",
              "cds/carrier_type",
              "cds/hours_clause",
              "cds/cyber_code",
              "cds/sanctions_clause",
              "cds/terrorism_code",
              "cds/named_perils",
              "cds/non_pd_bi",
              "cds/com_disease",
              "cds/am_best_rating",
              null,
              null,
              null,
              { field: "cds/risk_xl_risk_definition", shownBy: "/cds/show_risk_xl" },
              { field: "cds/risk_xl_profile", shownBy: "/cds/show_risk_xl" },
              { field: "cds/risk_xl_sublimit_wind", shownBy: "/cds/show_risk_xl" },
              { field: "cds/risk_xl_sublimit_quake", shownBy: "/cds/show_risk_xl" },
              { field: "cds/risk_xl_sublimit_flood", shownBy: "/cds/show_risk_xl" },
              { field: "cds/risk_xl_non_cat_lr", shownBy: "/cds/show_risk_xl" },
            ]}
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes stretch={true}
            field="cds/application_comments"
            title="Comments" />
        </HX.Pane>
        <HX.Pane>
          <HX.Button task="generate_tags_task" title="Generate Tags" />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Layer Details This Year">
        <HX.Table
          data={["cds/layers", null, "cds/layer_totals"]}
          fields={[
            { field: "renewal_layer" },
            { field: "is_facility" },
            { field: "section_reference" },
            { field: "loss_affected" },
            { field: "currency", shownBy: "/cds/show_intl_fields" },
            { field: "leader" },
            { field: "layer_description" },
            { field: "limit" },
            { field: "excess" },
            { field: "risk_xl_occurrence_limit", shownBy: "/cds/show_risk_xl" },
            { field: "limit_cnv", shownBy: "/cds/show_intl_fields", labelBy: "/cds/limit_application_ccy_label" },
            { field: "excess_cnv", shownBy: "/cds/show_intl_fields", labelBy: "/cds/excess_application_ccy_label" },
            { field: "inner_type", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "aggregate_deductible", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "aggregate_deductible_cnv", shownBy: "/cds/show_aad_cnv_field", labelBy: "/cds/aggregate_deductible_application_ccy_label" },
            { field: "number_reins", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "perc_reins_1", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "perc_reins_2", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "perc_reins_3", shownBy: "/cds/show_cat_work_comp_input" },
            null,
            { field: "effective_brokerage" },
            null,
            { field: "risk_xl_us_pml_code", shownBy: "/cds/show_risk_xl" },
            { field: "risk_xl_intl_pml_code", shownBy: "/cds/show_risk_xl" }
          ]}
          kb-interactive
          freezeLeft={0}
          syncColumnWidthsKey="layer_table"
        />
      </HX.Section>

      <HX.Section title="Layer Details Previous Year">
        <HX.Table
          data={["cds/layers", null, "cds/layer_totals"]}
          fields={[
            { field: "renewal_layer_ly" },
            { field: "is_facility_ly" },
            { field: "section_reference_ly" },
            { field: "loss_affected_ly" },
            { field: "currency_ly", shownBy: "/cds/show_intl_fields" },
            { field: "leader_ly" },
            { field: "layer_description_ly" },
            { field: "limit_ly" },
            { field: "excess_ly" },
            { field: "risk_xl_occurrence_limit_ly", shownBy: "/cds/show_risk_xl" },
            { field: "limit_cnv_ly", shownBy: "/cds/show_intl_fields", labelBy: "/cds/limit_application_ccy_label" },
            { field: "excess_cnv_ly", shownBy: "/cds/show_intl_fields", labelBy: "/cds/excess_application_ccy_label" },
            { field: "inner_type_ly", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "aggregate_deductible_ly", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "aggregate_deductible_cnv_ly", shownBy: "/cds/show_aad_cnv_field", labelBy: "/cds/aggregate_deductible_application_ccy_label" },
            { field: "number_reins_ly", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "perc_reins_1_ly", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "perc_reins_2_ly", shownBy: "/cds/show_cat_work_comp_input" },
            { field: "perc_reins_3_ly", shownBy: "/cds/show_cat_work_comp_input" },
            null,
            { field: "effective_brokerage_ly" },
            null,
            { field: "risk_xl_us_pml_code_ly", shownBy: "/cds/show_risk_xl" },
            { field: "risk_xl_intl_pml_code_ly", shownBy: "/cds/show_risk_xl" }
          ]}
          kb-interactive
          freezeLeft={0}
          syncColumnWidthsKey="layer_table"
        />
      </HX.Section>

    </HX.Page >
  )
}

export { vw_risk_information };


