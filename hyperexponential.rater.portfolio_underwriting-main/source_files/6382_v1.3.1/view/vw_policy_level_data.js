import * as HX from "hx-model-components";

function vw_policy_level_data(scale) {
  return (
    <HX.Page
      title="Policy Level Data"
      fullWidth={true}
      viewScale={scale}
      shownBy="model_state/show_policy_data">
      <HX.Section title="Data Mapping" shownBy="cds/policy_level_data_table/show_importer">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.File field="cds/policy_level_data_table/unformatted_sov_file" />
            <HX.Pane flow="right">
              <HX.Button title="Map Submission Data Columns to Hx (Step 1)" task="get_column_headers_from_policy_data_csv_task" />
              <HX.Button title="Load Submission Data into Hx Model (Step 2)" task="import_policy_data_from_csv_task" />
            </HX.Pane>
          </HX.Pane>
          <HX.Table data={["cds/policy_level_data_table/unformatted_file_column_mapping"]}
            fields={["unformatted_column", "renew_column", "similarity_score"]} kb-interactive dynamic />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Data Mapping" shownBy="cds/risk_information/is_large_model_mode">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.File field="cds/policy_level_data_table/unformatted_sov_file" />
            <HX.Pane flow="right">
              <HX.Button title="Map Submission Data Columns to Hx (Step 1)" task="get_column_headers_from_policy_data_csv_task" />
              <HX.Button title="Load Submission Data into Hx Model (Step 2)" task="import_policy_data_from_csv_task" />
              <HX.Button title={"Clear Cache"} task={"un_group_policy_data_task"} />
            </HX.Pane>
          </HX.Pane>
          <HX.Table data={["cds/policy_level_data_table/unformatted_file_column_mapping"]}
            fields={["unformatted_column", "renew_column", "similarity_score"]} kb-interactive dynamic />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Policy Level Data Import" shownBy="non_cds/risk_information/not_large_model_mode">
        <HX.Pane>
          <HX.Notes field="cds/policy_level_data_table/req_fields" />
        </HX.Pane >
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/policy_level_data_table/show_importer"]} />
          <HX.Button task="clear_policy_level_table_task" title="Clear Table" shownBy="non_cds/risk_information/not_large_model_mode" />
          <HX.Pane />
          <HX.Button task={"pre_group_policy_data_task"} title={"Cache Policy Data"} shownBy="cds/policy_level_data_table/use_policy_level_data_ungrouped" />
          <HX.Button task={"un_group_policy_data_task"} title={"Edit Policy Data"} shownBy="cds/policy_level_data_table/use_policy_level_data_grouped" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Table title="Policy Level Data"
            shownBy="cds/policy_level_data_table/use_policy_level_data_ungrouped"
            data={["cds/policy_level_data_table/policy_level_data"]}
            fields={[
              "umr",
              "policy_reference",
              "account_name",
              "facility_lob",
              "inception_date",
              "expiry_date",
              "yoa",
              "month_processed",
              "risk_code", "currency", "gross_premium",
              "net_premium",
              "paid_attritional",
              "paid_large", "paid_cat", "paid_total",
              "incurred_attritional", "incurred_large",
              "incurred_cat", "incurred_total",
              "sum_insured_tiv", "limit_attachment_currency", "limit",
              "attachment", "primary", "order_per",
              "risk_location", "industry_type",
              "region", "occupancy_property",
              "habitational", "slip_leader", "naic_sic",
              "gross_premium_cnv", "net_premium_cnv",
              "paid_attritional_cnv", "paid_large_cnv",
              "paid_cat_cnv", "paid_total_cnv",
              "incurred_attritional_cnv", "incurred_large_cnv",
              "incurred_cat_cnv", "incurred_total_cnv",
              "modelled", "selected_lob"]}
            kb-interactive
            dynamic
            maxListVisibleRows={28}
            syncColumnWidthsKey="mySyncedTablesInput" />
          <HX.Table title="Policy Level Data"
            shownBy="cds/policy_level_data_table/use_policy_level_data_grouped"
            data={["cds/policy_level_data_table/policy_level_data"]}
            fields={[
              "umr.read_only_option",
              "policy_reference.read_only_option",
              "account_name.read_only_option",
              "facility_lob.read_only_option",
              "inception_date.read_only_option",
              "expiry_date.read_only_option",
              "yoa.read_only_option",
              "month_processed.read_only_option",
              "risk_code.read_only_option",
              "currency.read_only_option",
              "gross_premium.read_only_option",
              "net_premium.read_only_option",
              "paid_attritional.read_only_option",
              "paid_large.read_only_option",
              "paid_cat.read_only_option",
              "paid_total.read_only_option",
              "incurred_attritional.read_only_option",
              "incurred_large.read_only_option",
              "incurred_cat.read_only_option",
              "incurred_total.read_only_option",
              "sum_insured_tiv.read_only_option",
              "limit_attachment_currency.read_only_option",
              "limit.read_only_option",
              "attachment.read_only_option",
              "primary.read_only_option",
              "order_per.read_only_option",
              "risk_location.read_only_option",
              "industry_type.read_only_option",
              "region.read_only_option",
              "occupancy_property.read_only_option",
              "habitational.read_only_option",
              "slip_leader.read_only_option",
              "naic_sic.read_only_option",
              "gross_premium_cnv",
              "net_premium_cnv",
              "paid_attritional_cnv",
              "paid_large_cnv",
              "paid_cat_cnv",
              "paid_total_cnv",
              "incurred_attritional_cnv",
              "incurred_large_cnv",
              "incurred_cat_cnv",
              "incurred_total_cnv",
              "modelled",
              "selected_lob"]}
            kb-interactive
            dynamic
            maxListVisibleRows={28}
            syncColumnWidthsKey="mySyncedTablesInput" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Policy Level Data" shownBy="cds/risk_information/is_large_model_mode">
        <HX.Pane flow="right">
          <HX.Table title="Summary Data" data={["cds/policy_level_data_table/policy_level_data_grouped"]} fields={[
            "account_name.read_only_option",
            "facility_lob.read_only_option",
            "yoa.read_only_option",
            "risk_code.read_only_option",
            "currency.read_only_option",
            "gross_premium.read_only_option",
            "net_premium.read_only_option",
            "paid_attritional.read_only_option",
            "paid_large.read_only_option",
            "paid_cat.read_only_option",
            "paid_total.read_only_option",
            "incurred_attritional.read_only_option",
            "incurred_large.read_only_option",
            "incurred_cat.read_only_option",
            "incurred_total.read_only_option"
          ]} />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Import Notes" shownBy="non_cds/risk_information/not_large_model_mode">
        <HX.Notes field="cds/policy_level_data_table/replacement_log" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_policy_level_data };