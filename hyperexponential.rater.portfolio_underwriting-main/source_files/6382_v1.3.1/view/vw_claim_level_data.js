import * as HX from "hx-model-components";

function vw_claim_level_data(scale) {
  return (
    <HX.Page
      title="Claim Level Data"
      fullWidth={true}
      viewScale={scale}
      shownBy="model_state/show_claim_data">
      <HX.Section title="Data Mapping" shownBy="cds/claim_level_data_table/show_importer">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.File field="cds/claim_level_data_table/unformatted_sov_file" />
            <HX.Pane flow="right">
              <HX.Button title="Map Submission Data Columns to Hx (Step 1)" task="get_column_headers_from_claim_data_csv_task" />
              <HX.Button title="Load Submission Data into Hx Model (Step 2)" task="import_claim_data_from_csv_task" />
            </HX.Pane>
          </HX.Pane>
          <HX.Table data={["cds/claim_level_data_table/unformatted_file_column_mapping"]}
            fields={["unformatted_column", "renew_column", "similarity_score"]} kb-interactive dynamic />
        </HX.Pane>
      </HX.Section >

      <HX.Section title="Data Mapping" shownBy="cds/risk_information/is_large_model_mode">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.File field="cds/claim_level_data_table/unformatted_sov_file" />
            <HX.Pane flow="right">
              <HX.Button title="Map Submission Data Columns to Hx (Step 1)" task="get_column_headers_from_claim_data_csv_task" />
              <HX.Button title="Load Submission Data into Hx Model (Step 2)" task="import_claim_data_from_csv_task" />
              <HX.Button title={"Clear Cache"} task={"un_group_claim_data_task"} />
            </HX.Pane>
          </HX.Pane>
          <HX.Table data={["cds/claim_level_data_table/unformatted_file_column_mapping"]}
            fields={["unformatted_column", "renew_column", "similarity_score"]} kb-interactive dynamic />
        </HX.Pane>
      </HX.Section >

      <HX.Section title="Claim Level Data Import" shownBy="non_cds/risk_information/not_large_model_mode">
        <HX.Pane>
          <HX.Notes field="cds/claim_level_data_table/req_fields" />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/claim_level_data_table/show_importer"]} />
          <HX.Button task="clear_claim_level_table_task" title="Clear Table" />
          <HX.Pane />
          <HX.Button task={"pre_group_claim_data_task"} title={"Cache Claim Data"} shownBy="cds/claim_level_data_table/use_claim_level_data_ungrouped" />
          <HX.Button task={"un_group_claim_data_task"} title={"Edit Claim Data"} shownBy="cds/claim_level_data_table/use_claim_level_data_grouped" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Table title="Claim Data"
            shownBy="cds/claim_level_data_table/use_claim_level_data_ungrouped"
            data={["cds/claim_level_data_table/claim_level_data"]}
            fields={[
              "umr",
              "policy_reference",
              "claim_reference",
              "account_name",
              "facility_lob",
              "loss_date",
              "claim_made_date",
              "closed_date",
              "month_processed",
              "yoa",
              "claim_status",
              "risk_code", "currency", "claim_type",
              "cat_code", "paid", "outstanding",
              "incurred", "paid_cnv",
              "outstanding_cnv",
              "incurred_cnv",
              "modelled",
              "selected_lob"]}
            kb-interactive
            dynamic
            maxListVisibleRows={28}
            syncColumnWidthsKey="mySyncedTablesInput" />
          <HX.Table title="Claim Data"
            shownBy="cds/claim_level_data_table/use_claim_level_data_grouped"
            data={["cds/claim_level_data_table/claim_level_data"]}
            fields={[
              "umr.read_only_option",
              "policy_reference.read_only_option",
              "claim_reference.read_only_option",
              "account_name.read_only_option",
              "facility_lob.read_only_option",
              "loss_date.read_only_option",
              "claim_made_date.read_only_option",
              "closed_date.read_only_option",
              "month_processed.read_only_option",
              "yoa.read_only_option",
              "claim_status.read_only_option",
              "risk_code.read_only_option",
              "currency.read_only_option",
              "claim_type.read_only_option",
              "cat_code.read_only_option",
              "paid.read_only_option", "outstanding.read_only_option", "incurred.read_only_option",
              "paid_cnv",
              "outstanding_cnv",
              "incurred_cnv",
              "modelled",
              "selected_lob"]}
            kb-interactive
            dynamic
            maxListVisibleRows={28}
            syncColumnWidthsKey="mySyncedTablesInput" />

        </HX.Pane>
      </HX.Section>
      <HX.Section title="Claim Level Data" shownBy="cds/risk_information/is_large_model_mode">
        <HX.Pane flow="right">
          <HX.Table title="Summary Data" data={["cds/claim_level_data_table/claim_level_data_grouped"]} fields={[
            "facility_lob.read_only_option",
            "yoa.read_only_option",
            "claim_status.read_only_option",
            "risk_code.read_only_option",
            "currency.read_only_option",
            "claim_type.read_only_option",
            "paid.read_only_option",
            "outstanding.read_only_option",
            "incurred.read_only_option"
          ]} />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Import Notes">
        <HX.Notes field="cds/claim_level_data_table/replacement_log" />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_claim_level_data };