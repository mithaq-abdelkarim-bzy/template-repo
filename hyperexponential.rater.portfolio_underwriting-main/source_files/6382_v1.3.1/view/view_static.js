
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root keyFields={[
      {
        "field": "non_cds/global_fields/lobs_error_msg.warning",
        "shownBy": "non_cds/global_fields/is_lobs_msg_shown"
      },
      {
        "field": "non_cds/global_fields/pc_error_msg.warning",
        "shownBy": "non_cds/global_fields/is_pc_msg_shown"
      },
      {
        "field": "non_cds/global_fields/oe_error_msg.warning",
        "shownBy": "non_cds/global_fields/is_oe_msg_shown"
      },
      {
        "field": "non_cds/global_fields/mismatched_lob_error_msg_global.warning",
        "shownBy": "non_cds/global_fields/mismatched_lob_table_length"
      },
      {
        "field": "non_cds/global_fields/projections_error_msg.warning",
        "shownBy": "non_cds/global_fields/is_projections_msg_shown"
      },
      {
        "field": null,
        "shownBy": "non_cds/global_fields/is_lobs_msg_shown"
      },
      {
        "field": null,
        "shownBy": "non_cds/global_fields/is_pc_msg_shown"
      },
      {
        "field": null,
        "shownBy": "non_cds/global_fields/mismatched_lob_table_length"
      },
      {
        "field": null,
        "shownBy": "non_cds/global_fields/is_projections_msg_shown"
      },
      {
        "field": null,
        "shownBy": "non_cds/global_fields/is_there_global_message"
      }
    ]}
      keyFieldsViewScale={1}>
      <HX.Page title="Landing Page"
        shownBy="model_state/show_landing_page">
        <HX.Section title="Start Policy">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Notes field="model_state/landing_page_info" />
              <HX.Collection fields={[
                "cds/risk_information/expiring_option_id"
              ]} />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_risk_information">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection with="cds/risk_information"
              numCols={2}
              fields={[
              "/hx_core/inception_date",
              "/hx_core/expiry_date",
              "/cds/standard_fields/underwriter",
              "deal_status",
              "facility_type",
              "/cds/standard_fields/insured_name",
              "/cds/currencies/source_currency",
              "/cds/standard_fields/policy_reference",
              "/cds/standard_fields/is_renewal"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Settings">
          <HX.Pane>
            <HX.Collection with="cds/risk_information"
              numCols={2}
              fields={[
              "follow_main_syndicate",
              {
                "field": "is_large_model_mode",
                "shownBy": "/non_cds/risk_information/not_follow_main_syndicate"
              },
              {
                "field": "prem_data_available",
                "shownBy": "/non_cds/risk_information/not_follow_main_syndicate"
              },
              "is_profit_comission",
              {
                "field": "insured_data_date",
                "shownBy": "/non_cds/risk_information/not_follow_main_syndicate"
              },
              {
                "field": "data_yoa_basis",
                "shownBy": "/non_cds/risk_information/not_follow_main_syndicate"
              },
              {
                "field": "det_claims_data_available",
                "shownBy": "/non_cds/risk_information/not_follow_main_syndicate"
              },
              {
                "field": "cat_modelling_available",
                "shownBy": "/non_cds/risk_information/not_follow_main_syndicate"
              }
            ]} />
            <HX.Pane flow="right">
              <HX.Collection with="cds/risk_information"
                fields={[
                "bbt_option_id"
              ]}
                horizontal={true}
                shownBy="follow_main_syndicate" />
              <HX.Button task="fetch_bbt_task"
                title="Fetch BBT Outputs"
                shownBy="cds/risk_information/follow_main_syndicate" />
            </HX.Pane>
            <HX.Collection numCols={2}
              fields={[
              null,
              "bbt_last_fetch_time"
            ]}
              with="cds/risk_information"
              shownBy="follow_main_syndicate" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection numCols={2}
            with="cds/risk_information"
            fields={[
            "broker_contact",
            "/cds/standard_fields/broker",
            "broker_email",
            "broker_location"
          ]} />
        </HX.Section>
        <HX.Section title="Show Actuarial Details and Reference Tables"
          shownBy="/non_cds/risk_information/not_follow_main_syndicate">
          <HX.Collection numCols={2}
            with="cds/risk_information"
            fields={[
            "priced_by",
            {
              "field": null,
              "shownBy": "/non_cds/risk_information/is_underwriter"
            },
            {
              "field": "actuary_reviewed",
              "shownBy": "/non_cds/risk_information/is_actuarial"
            },
            {
              "field": "show_refs",
              "shownBy": "/non_cds/risk_information/is_actuarial"
            }
          ]} />
        </HX.Section>
        <HX.Section title="Show Actuarial Details and Reference Tables"
          shownBy="cds/risk_information/follow_main_syndicate">
          <HX.Collection numCols={2}
            with="cds/risk_information"
            fields={[
            "priced_by",
            {
              "field": null,
              "shownBy": "/non_cds/risk_information/is_underwriter"
            },
            {
              "field": "actuary_reviewed",
              "shownBy": "/non_cds/risk_information/is_actuarial"
            }
          ]} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Section Reference Allocation"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_risk_information">
        <HX.Section title="Section Reference Allocation">
          <HX.Collection fields={[
            "/cds/rating_summary/section_ref_allocation/num_ref"
          ]}
            syncColumnWidthsKey="table_1" />
          <HX.Pane flow="down">
            <HX.Table syncColumnWidthsKey="table_1"
              with="/cds/rating_summary/section_ref_allocation"
              kb-interactive={true}
              data={[
              {
                "datum": "section_ref"
              },
              {
                "datum": "total_trifocus"
              },
              {
                "datum": "premium_by_lob",
                "elementLabelBy": "label"
              }
            ]}
              fields={[
              "total"
            ]}
              transpose={true}
              filter="is_row_visible" />
            <HX.Table syncColumnWidthsKey="table_1"
              with="/cds/rating_summary/section_ref_allocation"
              kb-interactive={true}
              data={[
              {
                "datum": "section_ref"
              },
              {
                "datum": "trifocus"
              },
              {
                "datum": "table_pcts",
                "elementLabelBy": "label"
              }
            ]}
              fields={[
              {
                "field": "ref_01",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_01"
              },
              {
                "field": "ref_02",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_02"
              },
              {
                "field": "ref_03",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_03"
              },
              {
                "field": "ref_04",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_04"
              },
              {
                "field": "ref_05",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_05"
              },
              {
                "field": "ref_06",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_06"
              },
              {
                "field": "ref_07",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_07"
              },
              {
                "field": "ref_08",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_08"
              },
              {
                "field": "ref_09",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_09"
              },
              {
                "field": "ref_10",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_10"
              },
              {
                "field": "ref_11",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_11"
              },
              {
                "field": "ref_12",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_12"
              },
              {
                "field": "ref_13",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_13"
              },
              {
                "field": "ref_14",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_14"
              },
              {
                "field": "ref_15",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_15"
              },
              {
                "field": "ref_16",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_16"
              },
              {
                "field": "ref_17",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_17"
              },
              {
                "field": "ref_18",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_18"
              },
              {
                "field": "ref_19",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_19"
              },
              {
                "field": "ref_20",
                "shownBy": "/non_cds/rating_summary/section_ref_allocation/show_refs/ref_20"
              }
            ]}
              transpose={true}
              filter="is_row_visible" />
            <HX.Table syncColumnWidthsKey="table_1"
              with="/cds/rating_summary/section_ref_allocation"
              kb-interactive={true}
              data={[
              {
                "datum": "total_section_ref"
              },
              {
                "datum": "total_trifocus"
              },
              {
                "datum": "total_pcts_by_lob",
                "elementLabelBy": "label"
              }
            ]}
              fields={[
              "total",
              "check"
            ]}
              transpose={true}
              filter="is_row_visible" />
          </HX.Pane>
          <HX.Table title="Amounts Allocated to Section Reference"
            with="/cds/rating_summary/section_ref_allocation"
            kb-interactive={true}
            data={[
            {
              "datum": "metrics_by_ref",
              "elementLabelBy": "section_ref"
            },
            null,
            "metrics_summary"
          ]}
            fields={[
            "trifocus",
            "status",
            null,
            "quoted_premium_gn_bst",
            "written_line",
            "quoted_premium_gg_bst",
            null,
            "market_deductions",
            "mga_fee",
            "facility_brokerage",
            "leaders_fee",
            "service_fee",
            "other",
            "selected_effective_deductions",
            null,
            "technical_premium_gn_bst",
            "benchmark_premium_gn_bst",
            "technical_premium_gg_bst",
            "benchmark_premium_gg_bst",
            "tpi",
            "bpi",
            "pflr",
            "roc",
            "rarc",
            null,
            "technical_premium_gn_bst_pre",
            "benchmark_premium_gn_bst_pre",
            "technical_premium_gg_bst_pre",
            "benchmark_premium_gg_bst_pre",
            "tpi_pre_uw_adj",
            "bpi_pre_uw_adj",
            "pflr_pre_uw_adj",
            "roc_pre_uw_adj",
            "uw_adj_impact"
          ]} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Code Library"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_risk_code_library">
        <HX.Section title="Active Risk Codes: Mappings and Full Descriptions">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/year_start",
              "cds/year_end",
              "cds/risk_code_description_expanded",
              null,
              null,
              null
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Table kb-interactive={true}
            dynamic={true}
            maxListVisibleRows={28}
            data={[
            "cds/risk_code_library"
          ]}
            fields={[
            "risk_code",
            "high_level_cob",
            "generic_cob",
            "risk_code_description",
            {
              "field": "risk_code_explained",
              "shownBy": "cds/risk_code_description_expanded"
            },
            "oecd_class_mapping",
            "assigned_tracker",
            "assigned_bp_class",
            "do_we_model",
            "gnpi_lloyds",
            "incured_lloyds",
            "gn_ilr_lloyds",
            "gnpi_beazley",
            "incurred_beazley",
            "gn_ilr_beazley"
          ]} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Policy Level Data"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_policy_data">
        <HX.Section title="Data Mapping"
          shownBy="cds/policy_level_data_table/show_importer">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.File field="cds/policy_level_data_table/unformatted_sov_file" />
              <HX.Pane flow="right">
                <HX.Button title="Map Submission Data Columns to Hx (Step 1)"
                  task="get_column_headers_from_policy_data_csv_task" />
                <HX.Button title="Load Submission Data into Hx Model (Step 2)"
                  task="import_policy_data_from_csv_task" />
              </HX.Pane>
            </HX.Pane>
            <HX.Table data={[
              "cds/policy_level_data_table/unformatted_file_column_mapping"
            ]}
              fields={[
              "unformatted_column",
              "renew_column",
              "similarity_score"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Data Mapping"
          shownBy="cds/risk_information/is_large_model_mode">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.File field="cds/policy_level_data_table/unformatted_sov_file" />
              <HX.Pane flow="right">
                <HX.Button title="Map Submission Data Columns to Hx (Step 1)"
                  task="get_column_headers_from_policy_data_csv_task" />
                <HX.Button title="Load Submission Data into Hx Model (Step 2)"
                  task="import_policy_data_from_csv_task" />
                <HX.Button title="Clear Cache"
                  task="un_group_policy_data_task" />
              </HX.Pane>
            </HX.Pane>
            <HX.Table data={[
              "cds/policy_level_data_table/unformatted_file_column_mapping"
            ]}
              fields={[
              "unformatted_column",
              "renew_column",
              "similarity_score"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Policy Level Data Import"
          shownBy="non_cds/risk_information/not_large_model_mode">
          <HX.Pane>
            <HX.Notes field="cds/policy_level_data_table/req_fields" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/policy_level_data_table/show_importer"
            ]} />
            <HX.Button task="clear_policy_level_table_task"
              title="Clear Table"
              shownBy="non_cds/risk_information/not_large_model_mode" />
            <HX.Pane />
            <HX.Button task="pre_group_policy_data_task"
              title="Cache Policy Data"
              shownBy="cds/policy_level_data_table/use_policy_level_data_ungrouped" />
            <HX.Button task="un_group_policy_data_task"
              title="Edit Policy Data"
              shownBy="cds/policy_level_data_table/use_policy_level_data_grouped" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title="Policy Level Data"
              shownBy="cds/policy_level_data_table/use_policy_level_data_ungrouped"
              data={[
              "cds/policy_level_data_table/policy_level_data"
            ]}
              fields={[
              "umr",
              "policy_reference",
              "account_name",
              "facility_lob",
              "inception_date",
              "expiry_date",
              "yoa",
              "month_processed",
              "risk_code",
              "currency",
              "gross_premium",
              "net_premium",
              "paid_attritional",
              "paid_large",
              "paid_cat",
              "paid_total",
              "incurred_attritional",
              "incurred_large",
              "incurred_cat",
              "incurred_total",
              "sum_insured_tiv",
              "limit_attachment_currency",
              "limit",
              "attachment",
              "primary",
              "order_per",
              "risk_location",
              "industry_type",
              "region",
              "occupancy_property",
              "habitational",
              "slip_leader",
              "naic_sic",
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
              "selected_lob"
            ]}
              kb-interactive={true}
              dynamic={true}
              maxListVisibleRows={28}
              syncColumnWidthsKey="mySyncedTablesInput" />
            <HX.Table title="Policy Level Data"
              shownBy="cds/policy_level_data_table/use_policy_level_data_grouped"
              data={[
              "cds/policy_level_data_table/policy_level_data"
            ]}
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
              "selected_lob"
            ]}
              kb-interactive={true}
              dynamic={true}
              maxListVisibleRows={28}
              syncColumnWidthsKey="mySyncedTablesInput" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Policy Level Data"
          shownBy="cds/risk_information/is_large_model_mode">
          <HX.Pane flow="right">
            <HX.Table title="Summary Data"
              data={[
              "cds/policy_level_data_table/policy_level_data_grouped"
            ]}
              fields={[
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
        <HX.Section title="Import Notes"
          shownBy="non_cds/risk_information/not_large_model_mode">
          <HX.Notes field="cds/policy_level_data_table/replacement_log" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Claim Level Data"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_claim_data">
        <HX.Section title="Data Mapping"
          shownBy="cds/claim_level_data_table/show_importer">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.File field="cds/claim_level_data_table/unformatted_sov_file" />
              <HX.Pane flow="right">
                <HX.Button title="Map Submission Data Columns to Hx (Step 1)"
                  task="get_column_headers_from_claim_data_csv_task" />
                <HX.Button title="Load Submission Data into Hx Model (Step 2)"
                  task="import_claim_data_from_csv_task" />
              </HX.Pane>
            </HX.Pane>
            <HX.Table data={[
              "cds/claim_level_data_table/unformatted_file_column_mapping"
            ]}
              fields={[
              "unformatted_column",
              "renew_column",
              "similarity_score"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Data Mapping"
          shownBy="cds/risk_information/is_large_model_mode">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.File field="cds/claim_level_data_table/unformatted_sov_file" />
              <HX.Pane flow="right">
                <HX.Button title="Map Submission Data Columns to Hx (Step 1)"
                  task="get_column_headers_from_claim_data_csv_task" />
                <HX.Button title="Load Submission Data into Hx Model (Step 2)"
                  task="import_claim_data_from_csv_task" />
                <HX.Button title="Clear Cache"
                  task="un_group_claim_data_task" />
              </HX.Pane>
            </HX.Pane>
            <HX.Table data={[
              "cds/claim_level_data_table/unformatted_file_column_mapping"
            ]}
              fields={[
              "unformatted_column",
              "renew_column",
              "similarity_score"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Claim Level Data Import"
          shownBy="non_cds/risk_information/not_large_model_mode">
          <HX.Pane>
            <HX.Notes field="cds/claim_level_data_table/req_fields" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/claim_level_data_table/show_importer"
            ]} />
            <HX.Button task="clear_claim_level_table_task"
              title="Clear Table" />
            <HX.Pane />
            <HX.Button task="pre_group_claim_data_task"
              title="Cache Claim Data"
              shownBy="cds/claim_level_data_table/use_claim_level_data_ungrouped" />
            <HX.Button task="un_group_claim_data_task"
              title="Edit Claim Data"
              shownBy="cds/claim_level_data_table/use_claim_level_data_grouped" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title="Claim Data"
              shownBy="cds/claim_level_data_table/use_claim_level_data_ungrouped"
              data={[
              "cds/claim_level_data_table/claim_level_data"
            ]}
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
              "risk_code",
              "currency",
              "claim_type",
              "cat_code",
              "paid",
              "outstanding",
              "incurred",
              "paid_cnv",
              "outstanding_cnv",
              "incurred_cnv",
              "modelled",
              "selected_lob"
            ]}
              kb-interactive={true}
              dynamic={true}
              maxListVisibleRows={28}
              syncColumnWidthsKey="mySyncedTablesInput" />
            <HX.Table title="Claim Data"
              shownBy="cds/claim_level_data_table/use_claim_level_data_grouped"
              data={[
              "cds/claim_level_data_table/claim_level_data"
            ]}
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
              "paid.read_only_option",
              "outstanding.read_only_option",
              "incurred.read_only_option",
              "paid_cnv",
              "outstanding_cnv",
              "incurred_cnv",
              "modelled",
              "selected_lob"
            ]}
              kb-interactive={true}
              dynamic={true}
              maxListVisibleRows={28}
              syncColumnWidthsKey="mySyncedTablesInput" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Claim Level Data"
          shownBy="cds/risk_information/is_large_model_mode">
          <HX.Pane flow="right">
            <HX.Table title="Summary Data"
              data={[
              "cds/claim_level_data_table/claim_level_data_grouped"
            ]}
              fields={[
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
      </HX.Page>
      <HX.Page title="Risk Code Composition"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_risk_code_comp">
        <HX.Section title="Risk Code Composition"
          collapsible={false}>
          <HX.Pane shownBy="non_cds/global_fields/mismatched_lob_table_length"
            flow="right">
            <HX.Collection fields={[
              "non_cds/global_fields/mismatched_lob_error_msg.warning"
            ]} />
            <HX.Button task="sync_lob_lists_task"
              title="Sync LOB Lists" />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection fields={[
              "cds/risk_code_composition/model_type",
              null,
              null,
              null,
              null,
              null,
              null,
              null,
              null,
              "cds/risk_code_composition/data_driven_composition/year_start",
              "cds/risk_code_composition/data_driven_composition/year_end",
              null,
              "cds/risk_code_composition/data_driven_composition/premium_basis",
              null,
              null
            ]}
              syncColumnWidthsKey="input_1"
              shownBy="cds/risk_information/prem_data_available"
              horizontal={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Pane>
              <HX.Table title="Premium summary by Risk Code and YOA from Policy Level Data"
                data={[
                "cds/risk_code_composition/data_driven_composition/premiums_table",
                null,
                "cds/risk_code_composition/data_driven_composition/summary"
              ]}
                fields={[
                "risk_code",
                {
                  "field": "year_8",
                  "labelBy": "non_cds/risk_code_composition/year_8"
                },
                {
                  "field": "year_7",
                  "labelBy": "non_cds/risk_code_composition/year_7"
                },
                {
                  "field": "year_6",
                  "labelBy": "non_cds/risk_code_composition/year_6"
                },
                {
                  "field": "year_5",
                  "labelBy": "non_cds/risk_code_composition/year_5"
                },
                {
                  "field": "year_4",
                  "labelBy": "non_cds/risk_code_composition/year_4"
                },
                {
                  "field": "year_3",
                  "labelBy": "non_cds/risk_code_composition/year_3"
                },
                {
                  "field": "year_2",
                  "labelBy": "non_cds/risk_code_composition/year_2"
                },
                {
                  "field": "year_1",
                  "labelBy": "non_cds/risk_code_composition/year_1"
                },
                {
                  "field": "year_0",
                  "labelBy": "non_cds/risk_code_composition/year_0"
                },
                null,
                "selected_premium",
                "exist_in_lloyds_data_bool",
                "composition"
              ]}
                syncColumnWidthsKey="input_1"
                shownBy="cds/risk_information/prem_data_available"
                maxListVisibleRows={20}
                kb-interactive={true}
                dynamic={true} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane>
            <HX.Pane>
              <HX.Collection fields={[
                "cds/risk_code_composition/data_driven_composition/composition_selection/modelled",
                null,
                null,
                null,
                null,
                null,
                null
              ]}
                shownBy="cds/risk_information/prem_data_available"
                horizontal={true} />
              <HX.Table title="Risk Code Composition Derived from Data"
                data={[
                "cds/risk_code_composition/data_driven_composition/composition_selection/table"
              ]}
                fields={[
                "cs_risk_code",
                "cs_composition",
                "exists_in_data_bool",
                "model",
                "composition_reweighted",
                "cs_facility_line_of_business",
                "selected_lob",
                "selected_bp_class",
                "tracker_class",
                "risk_code_description"
              ]}
                syncColumnWidthsKey="table_1"
                shownBy="cds/risk_information/prem_data_available"
                maxListVisibleRows={20}
                kb-interactive={true}
                dynamic={true}
                filter="is_row_visible" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Button task="copy_composition_selection_table"
                  title="Copy Risk Code Composition"
                  shownBy="non_cds/risk_code_composition/is_manual_and_prem_data_available_true" />
                <HX.Button task="clear_manual_risk_code_composition_table"
                  title="Clear Table"
                  shownBy="non_cds/risk_code_composition/is_manual" />
              </HX.Pane>
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={[
                "cds/risk_code_composition/composition_manual/modelled",
                null,
                null,
                null,
                null,
                null
              ]}
                horizontal={true}
                shownBy="non_cds/risk_code_composition/is_manual" />
              <HX.Table title="Risk Code Composition Manually Entered"
                data={[
                "cds/risk_code_composition/composition_manual/table"
              ]}
                fields={[
                "cs_risk_code",
                "cs_composition",
                "exists_in_data_bool",
                "model",
                "composition_reweighted",
                "cs_facility_line_of_business",
                "selected_lob",
                "selected_bp_class",
                "tracker_class",
                "risk_code_description"
              ]}
                syncColumnWidthsKey="table_1"
                maxListVisibleRows={20}
                kb-interactive={true}
                dynamic={true}
                shownBy="non_cds/risk_code_composition/is_manual" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Deductions"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_deductions">
        <HX.Section collapsible={false}
          shownBy="cds/risk_information/prem_data_available"
          title=" ">
          <HX.Collection fields={[
            "cds/assumed_deductions/model_type",
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            "cds/assumed_deductions/data_driven_deductions/year_start",
            "cds/assumed_deductions/data_driven_deductions/year_end"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Gross Premium"
          shownBy="cds/risk_information/prem_data_available"
          defaultCollapsed={true}>
          <HX.Table kb-interactive={true}
            title="Gross Premium Derived From Data"
            with="cds/assumed_deductions/data_driven_deductions/gross_premium"
            data={[
            "deductions_derived_from_data",
            null,
            "summary"
          ]}
            fields={[
            "selected_lob",
            {
              "field": "year_8",
              "labelBy": "/non_cds/assumed_deductions/year_8"
            },
            {
              "field": "year_7",
              "labelBy": "/non_cds/assumed_deductions/year_7"
            },
            {
              "field": "year_6",
              "labelBy": "/non_cds/assumed_deductions/year_6"
            },
            {
              "field": "year_5",
              "labelBy": "/non_cds/assumed_deductions/year_5"
            },
            {
              "field": "year_4",
              "labelBy": "/non_cds/assumed_deductions/year_4"
            },
            {
              "field": "year_3",
              "labelBy": "/non_cds/assumed_deductions/year_3"
            },
            {
              "field": "year_2",
              "labelBy": "/non_cds/assumed_deductions/year_2"
            },
            {
              "field": "year_1",
              "labelBy": "/non_cds/assumed_deductions/year_1"
            },
            {
              "field": "year_0",
              "labelBy": "/non_cds/assumed_deductions/year_0"
            }
          ]}
            syncColumnWidthsKey="table_1" />
        </HX.Section>
        <HX.Section title="Net Premium"
          shownBy="cds/risk_information/prem_data_available"
          defaultCollapsed={true}>
          <HX.Table kb-interactive={true}
            title="Net Premium Derived From Data"
            with="cds/assumed_deductions/data_driven_deductions/net_premium"
            data={[
            "deductions_derived_from_data",
            null,
            "summary"
          ]}
            fields={[
            "selected_lob",
            {
              "field": "year_8",
              "labelBy": "/non_cds/assumed_deductions/year_8"
            },
            {
              "field": "year_7",
              "labelBy": "/non_cds/assumed_deductions/year_7"
            },
            {
              "field": "year_6",
              "labelBy": "/non_cds/assumed_deductions/year_6"
            },
            {
              "field": "year_5",
              "labelBy": "/non_cds/assumed_deductions/year_5"
            },
            {
              "field": "year_4",
              "labelBy": "/non_cds/assumed_deductions/year_4"
            },
            {
              "field": "year_3",
              "labelBy": "/non_cds/assumed_deductions/year_3"
            },
            {
              "field": "year_2",
              "labelBy": "/non_cds/assumed_deductions/year_2"
            },
            {
              "field": "year_1",
              "labelBy": "/non_cds/assumed_deductions/year_1"
            },
            {
              "field": "year_0",
              "labelBy": "/non_cds/assumed_deductions/year_0"
            }
          ]}
            syncColumnWidthsKey="table_1" />
        </HX.Section>
        <HX.Section title="Market Deductions"
          shownBy="cds/risk_information/prem_data_available"
          defaultCollapsed={true}>
          <HX.Table kb-interactive={true}
            title="Implied Market Deductions Derived From Data"
            with="cds/assumed_deductions/data_driven_deductions/market_deductions"
            data={[
            "deductions_derived_from_data",
            null,
            "summary"
          ]}
            fields={[
            "selected_lob",
            {
              "field": "year_8",
              "labelBy": "/non_cds/assumed_deductions/year_8"
            },
            {
              "field": "year_7",
              "labelBy": "/non_cds/assumed_deductions/year_7"
            },
            {
              "field": "year_6",
              "labelBy": "/non_cds/assumed_deductions/year_6"
            },
            {
              "field": "year_5",
              "labelBy": "/non_cds/assumed_deductions/year_5"
            },
            {
              "field": "year_4",
              "labelBy": "/non_cds/assumed_deductions/year_4"
            },
            {
              "field": "year_3",
              "labelBy": "/non_cds/assumed_deductions/year_3"
            },
            {
              "field": "year_2",
              "labelBy": "/non_cds/assumed_deductions/year_2"
            },
            {
              "field": "year_1",
              "labelBy": "/non_cds/assumed_deductions/year_1"
            },
            {
              "field": "year_0",
              "labelBy": "/non_cds/assumed_deductions/year_0"
            }
          ]}
            syncColumnWidthsKey="table_1" />
        </HX.Section>
        <HX.Section title="Data Driven Deductions"
          shownBy="cds/risk_information/prem_data_available"
          collapsible={false}>
          <HX.Table title="Data Driven Deductions"
            data={[
            "cds/assumed_deductions/data_driven_deductions/deductions/amount",
            "cds/assumed_deductions/data_driven_deductions/deductions/basis",
            null,
            "cds/assumed_deductions/data_driven_deductions/deductions/table"
          ]}
            fields={[
            "selected_lob",
            "market_deductions",
            "mga_fee",
            "facility_brokerage",
            "leaders_fee",
            "service_fee",
            "other",
            "selected_effective_deductions"
          ]}
            syncColumnWidthsKey="bp_summary_by_lob"
            filter="is_row_visible"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Manually Entered Deductions"
          shownBy="non_cds/assumed_deductions/is_manual"
          collapsible={false}>
          <HX.Table title=" "
            data={[
            "cds/assumed_deductions/deductions_manually_entered/amount",
            "cds/assumed_deductions/deductions_manually_entered/basis"
          ]}
            fields={[
            "selected_lob",
            "market_deductions",
            "mga_fee",
            "facility_brokerage",
            "leaders_fee",
            "service_fee",
            "other"
          ]}
            syncColumnWidthsKey="bp_summary_by_lob"
            kb-interactive={true} />
          <HX.Table title="Manually entered Deductions"
            data={[
            "cds/assumed_deductions/deductions_manually_entered/table"
          ]}
            fields={[
            "selected_lob",
            "market_deductions",
            "mga_fee",
            "facility_brokerage",
            "leaders_fee",
            "service_fee",
            "other",
            "selected_effective_deductions"
          ]}
            syncColumnWidthsKey="bp_summary_by_lob"
            maxListVisibleRows={15}
            filter="is_row_visible"
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_rate_change">
        <HX.Section title="Rate Change - Tabular"
          collapsible={false}>
          <HX.Table kb-interactive={true}
            data={[
            "cds/rate_change",
            null,
            "cds/rate_change_summary"
          ]}
            fields={[
            "selected_lob",
            "dominant_risk_code",
            "bp_class",
            null,
            "year_0/yoa",
            {
              "field": "year_0/facility",
              "labelBy": "non_cds/rate_change/year_0/facility"
            },
            "year_0/bp_rate_change",
            {
              "field": "year_0/bp_rarc_margin",
              "infoBy": "cds/rate_change_summary/year_0/bp_rarc_margin_info"
            },
            "year_0/source",
            "year_0/selected",
            null,
            "year_1/yoa",
            {
              "field": "year_1/facility",
              "labelBy": "non_cds/rate_change/year_1/facility"
            },
            "year_1/beazley_group_achieved",
            "year_1/selected",
            null,
            "year_2/yoa",
            {
              "field": "year_2/facility",
              "labelBy": "non_cds/rate_change/year_2/facility"
            },
            "year_2/beazley_group_achieved",
            "year_2/selected",
            null,
            "year_3/yoa",
            {
              "field": "year_3/facility",
              "labelBy": "non_cds/rate_change/year_3/facility"
            },
            "year_3/beazley_group_achieved",
            "year_3/selected",
            null,
            "year_4/yoa",
            {
              "field": "year_4/facility",
              "labelBy": "non_cds/rate_change/year_4/facility"
            },
            "year_4/beazley_group_achieved",
            "year_4/selected",
            null,
            "year_5/yoa",
            {
              "field": "year_5/facility",
              "labelBy": "non_cds/rate_change/year_5/facility"
            },
            "year_5/beazley_group_achieved",
            "year_5/selected",
            null,
            "year_6/yoa",
            {
              "field": "year_6/facility",
              "labelBy": "non_cds/rate_change/year_6/facility"
            },
            "year_6/beazley_group_achieved",
            "year_6/selected",
            null,
            "year_7/yoa",
            {
              "field": "year_7/facility",
              "labelBy": "non_cds/rate_change/year_7/facility"
            },
            "year_7/beazley_group_achieved",
            "year_7/selected",
            null,
            "year_8/yoa",
            {
              "field": "year_8/facility",
              "labelBy": "non_cds/rate_change/year_8/facility"
            },
            "year_8/beazley_group_achieved",
            "year_8/selected",
            null,
            "year_9/yoa",
            {
              "field": "year_9/facility",
              "labelBy": "non_cds/rate_change/year_9/facility"
            },
            "year_9/beazley_group_achieved",
            "year_9/selected",
            null,
            "year_10/yoa",
            {
              "field": "year_10/facility",
              "labelBy": "non_cds/rate_change/year_10/facility"
            },
            "year_10/beazley_group_achieved",
            "year_10/selected",
            null,
            "year_11/yoa",
            {
              "field": "year_11/facility",
              "labelBy": "non_cds/rate_change/year_11/facility"
            },
            "year_11/beazley_group_achieved",
            "year_11/selected",
            null,
            "year_12/yoa",
            {
              "field": "year_12/facility",
              "labelBy": "non_cds/rate_change/year_12/facility"
            },
            "year_12/beazley_group_achieved",
            "year_12/selected",
            null,
            "year_13/yoa",
            {
              "field": "year_13/facility",
              "labelBy": "non_cds/rate_change/year_13/facility"
            },
            "year_13/beazley_group_achieved",
            "year_13/selected",
            null,
            "year_14/yoa",
            {
              "field": "year_14/facility",
              "labelBy": "non_cds/rate_change/year_14/facility"
            },
            "year_14/beazley_group_achieved",
            "year_14/selected",
            null,
            "year_15/yoa",
            {
              "field": "year_15/facility",
              "labelBy": "non_cds/rate_change/year_15/facility"
            },
            "year_15/beazley_group_achieved",
            "year_15/selected"
          ]}
            filter="is_row_visible" />
        </HX.Section>
        <HX.Section title="Rate Change - Expiring"
          defaultCollapsed={true}
          shownBy="/cds/standard_fields/is_renewal">
          <HX.Button task="map_expiring_rate_change_task"
            title="Map Expiring Rate Change to Renewing" />
          <HX.Table kb-interactive={true}
            data={[
            "cds/expiring/rate_change"
          ]}
            fields={[
            "selected_lob",
            null,
            "year_0/yoa",
            "year_0/facility",
            "year_0/source",
            null,
            "year_1/yoa",
            "year_1/facility",
            null,
            "year_2/yoa",
            "year_2/facility",
            null,
            "year_3/yoa",
            "year_3/facility",
            null,
            "year_4/yoa",
            "year_4/facility",
            null,
            "year_5/yoa",
            "year_5/facility",
            null,
            "year_6/yoa",
            "year_6/facility",
            null,
            "year_7/yoa",
            "year_7/facility",
            null,
            "year_8/yoa",
            "year_8/facility",
            null,
            "year_9/yoa",
            "year_9/facility",
            null,
            "year_10/yoa",
            "year_10/facility",
            null,
            "year_11/yoa",
            "year_11/facility",
            null,
            "year_12/yoa",
            "year_12/facility",
            null,
            "year_13/yoa",
            "year_13/facility",
            null,
            "year_14/yoa",
            "year_14/facility",
            null,
            "year_15/yoa",
            "year_15/facility"
          ]} />
        </HX.Section>
        <HX.Section title="Commentary"
          collapsible={false}>
          <HX.Notes field="cds/rationale/rate_change_notes"
            title="Please note any rationale for selection below, and any use of overrides:" />
        </HX.Section>
        <HX.Section title="Rate Change - Selector"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Selector with="cds"
              title="Renewing"
              data={[
              "rate_change"
            ]}
              dropdown="selected_lob">
              <HX.Table kb-interactive={true}
                data={[
                {
                  "datum": "year_0"
                },
                {
                  "datum": "year_1"
                },
                {
                  "datum": "year_2"
                },
                {
                  "datum": "year_3"
                },
                {
                  "datum": "year_4"
                },
                {
                  "datum": "year_5"
                },
                {
                  "datum": "year_6"
                },
                {
                  "datum": "year_7"
                },
                {
                  "datum": "year_8"
                },
                {
                  "datum": "year_9"
                },
                {
                  "datum": "year_10"
                },
                {
                  "datum": "year_11"
                },
                {
                  "datum": "year_12"
                },
                {
                  "datum": "year_13"
                },
                {
                  "datum": "year_14"
                },
                {
                  "datum": "year_15"
                }
              ]}
                fields={[
                {
                  "field": "yoa",
                  "maxWidth": 100
                },
                {
                  "field": "facility",
                  "maxWidth": 150
                },
                {
                  "field": "beazley_group_achieved",
                  "maxWidth": 150
                },
                {
                  "field": "bp_rate_change",
                  "maxWidth": 150
                },
                {
                  "field": "bp_rarc_margin",
                  "maxWidth": 150
                },
                {
                  "field": "source",
                  "maxWidth": 150
                },
                {
                  "field": "selected",
                  "maxWidth": 150
                }
              ]}
                transpose={false} />
            </HX.Selector>
            <HX.Selector with="cds/expiring"
              title="Expiring"
              data={[
              "rate_change"
            ]}
              dropdown="selected_lob"
              shownBy="/cds/standard_fields/is_renewal">
              <HX.Table kb-interactive={true}
                data={[
                {
                  "datum": "year_0"
                },
                {
                  "datum": "year_1"
                },
                {
                  "datum": "year_2"
                },
                {
                  "datum": "year_3"
                },
                {
                  "datum": "year_4"
                },
                {
                  "datum": "year_5"
                },
                {
                  "datum": "year_6"
                },
                {
                  "datum": "year_7"
                },
                {
                  "datum": "year_8"
                },
                {
                  "datum": "year_9"
                },
                {
                  "datum": "year_10"
                },
                {
                  "datum": "year_11"
                },
                {
                  "datum": "year_12"
                },
                {
                  "datum": "year_13"
                },
                {
                  "datum": "year_14"
                },
                {
                  "datum": "year_15"
                }
              ]}
                fields={[
                {
                  "field": "yoa",
                  "maxWidth": 100
                },
                {
                  "field": "facility",
                  "maxWidth": 150
                },
                {
                  "field": "source",
                  "maxWidth": 150
                }
              ]}
                transpose={false} />
            </HX.Selector>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Inflation"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_inflation">
        <HX.Section title="Inflation">
          <HX.Table title="Summary by Line of Business"
            data={[
            "cds/inflation/summary_by_lob"
          ]}
            fields={[
            "selected_lob",
            "risk_code",
            "composition",
            "bp_class",
            {
              "field": "year_0",
              "labelBy": "non_cds/inflation/year_0"
            },
            {
              "field": "year_1",
              "labelBy": "non_cds/inflation/year_1"
            },
            {
              "field": "year_2",
              "labelBy": "non_cds/inflation/year_2"
            },
            {
              "field": "year_3",
              "labelBy": "non_cds/inflation/year_3"
            },
            {
              "field": "year_4",
              "labelBy": "non_cds/inflation/year_4"
            },
            {
              "field": "year_5",
              "labelBy": "non_cds/inflation/year_5"
            },
            {
              "field": "year_6",
              "labelBy": "non_cds/inflation/year_6"
            },
            {
              "field": "year_7",
              "labelBy": "non_cds/inflation/year_7"
            },
            {
              "field": "year_8",
              "labelBy": "non_cds/inflation/year_8"
            },
            {
              "field": "year_9",
              "labelBy": "non_cds/inflation/year_9"
            },
            {
              "field": "year_10",
              "labelBy": "non_cds/inflation/year_10"
            },
            {
              "field": "year_11",
              "labelBy": "non_cds/inflation/year_11"
            },
            {
              "field": "year_12",
              "labelBy": "non_cds/inflation/year_12"
            },
            {
              "field": "year_13",
              "labelBy": "non_cds/inflation/year_13"
            },
            {
              "field": "year_14",
              "labelBy": "non_cds/inflation/year_14"
            },
            {
              "field": "year_15",
              "labelBy": "non_cds/inflation/year_15"
            },
            {
              "field": "year_16",
              "labelBy": "non_cds/inflation/year_16"
            },
            {
              "field": "year_17",
              "labelBy": "non_cds/inflation/year_17"
            },
            {
              "field": "year_18",
              "labelBy": "non_cds/inflation/year_18"
            },
            {
              "field": "year_19",
              "labelBy": "non_cds/inflation/year_19"
            },
            {
              "field": "year_20",
              "labelBy": "non_cds/inflation/year_20"
            },
            {
              "field": "year_21",
              "labelBy": "non_cds/inflation/year_21"
            },
            {
              "field": "year_22",
              "labelBy": "non_cds/inflation/year_22"
            },
            {
              "field": "year_23",
              "labelBy": "non_cds/inflation/year_23"
            },
            {
              "field": "year_24",
              "labelBy": "non_cds/inflation/year_24"
            },
            {
              "field": "year_25",
              "labelBy": "non_cds/inflation/year_25"
            }
          ]}
            syncColumnWidthsKey="table_1"
            kb-interactive={true} />
          <HX.Table title="Inflation Details"
            data={[
            "cds/inflation/details"
          ]}
            fields={[
            "selected_lob",
            "risk_code",
            "composition",
            "bp_class",
            {
              "field": "year_0",
              "labelBy": "non_cds/inflation/year_0"
            },
            {
              "field": "year_1",
              "labelBy": "non_cds/inflation/year_1"
            },
            {
              "field": "year_2",
              "labelBy": "non_cds/inflation/year_2"
            },
            {
              "field": "year_3",
              "labelBy": "non_cds/inflation/year_3"
            },
            {
              "field": "year_4",
              "labelBy": "non_cds/inflation/year_4"
            },
            {
              "field": "year_5",
              "labelBy": "non_cds/inflation/year_5"
            },
            {
              "field": "year_6",
              "labelBy": "non_cds/inflation/year_6"
            },
            {
              "field": "year_7",
              "labelBy": "non_cds/inflation/year_7"
            },
            {
              "field": "year_8",
              "labelBy": "non_cds/inflation/year_8"
            },
            {
              "field": "year_9",
              "labelBy": "non_cds/inflation/year_9"
            },
            {
              "field": "year_10",
              "labelBy": "non_cds/inflation/year_10"
            },
            {
              "field": "year_11",
              "labelBy": "non_cds/inflation/year_11"
            },
            {
              "field": "year_12",
              "labelBy": "non_cds/inflation/year_12"
            },
            {
              "field": "year_13",
              "labelBy": "non_cds/inflation/year_13"
            },
            {
              "field": "year_14",
              "labelBy": "non_cds/inflation/year_14"
            },
            {
              "field": "year_15",
              "labelBy": "non_cds/inflation/year_15"
            },
            {
              "field": "year_16",
              "labelBy": "non_cds/inflation/year_16"
            },
            {
              "field": "year_17",
              "labelBy": "non_cds/inflation/year_17"
            },
            {
              "field": "year_18",
              "labelBy": "non_cds/inflation/year_18"
            },
            {
              "field": "year_19",
              "labelBy": "non_cds/inflation/year_19"
            },
            {
              "field": "year_20",
              "labelBy": "non_cds/inflation/year_20"
            },
            {
              "field": "year_21",
              "labelBy": "non_cds/inflation/year_21"
            },
            {
              "field": "year_22",
              "labelBy": "non_cds/inflation/year_22"
            },
            {
              "field": "year_23",
              "labelBy": "non_cds/inflation/year_23"
            },
            {
              "field": "year_24",
              "labelBy": "non_cds/inflation/year_24"
            },
            {
              "field": "year_25",
              "labelBy": "non_cds/inflation/year_25"
            }
          ]}
            syncColumnWidthsKey="table_1"
            filter="is_row_visible"
            maxListVisibleRows={8}
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Premium and Limit Profile"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_premium_limit_prof">
        <HX.Section title="Premium and Limit Profile"
          collapsible={false}>
          <HX.Pane>
            <HX.Table title="Premium and Limit Profile Table"
              data={[
              "cds/prem_limit_profile/table",
              null,
              "cds/prem_limit_profile/summary"
            ]}
              fields={[
              "lob",
              "selected_lob",
              "assigned_trifocus",
              "max_limit_at_100_per",
              "avg_limit_at_100_per",
              "avg_attachment_point",
              "primary",
              "max_limit_at_bst_share",
              null,
              "future_ultimate_gross_prem",
              "bst_share_line_size",
              "bst_share_ultimate_gross_premium",
              "bst_deductions",
              "bst_net_premium",
              "portfolio_composition"
            ]}
              filter="is_row_visible"
              syncColumnWidthsKey="table_1"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Commentary"
          collapsible={false}>
          <HX.Notes field="cds/rationale/prem_limit_notes"
            title="Please note any rationale for selection below, and any use of overrides:" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Cat"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_cat">
        <HX.Section collapsible={false}
          title="CAT MODELLING">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/cat/currency",
              null,
              null,
              null,
              null,
              null,
              null
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "cds/cat/modelling_as_at_date",
              null,
              null,
              null,
              null,
              null,
              null
            ]}
              horizontal={true} />
            <HX.Table title="Cat"
              with="cds/cat"
              kb-interactive={true}
              data={[
              "curve_label",
              "model",
              "one_in_10000",
              "one_in_5000",
              "one_in_1000",
              "one_in_500",
              "one_in_250",
              "one_in_200",
              "one_in_100",
              "one_in_50",
              "one_in_30",
              "one_in_10",
              "one_in_5",
              "one_in_2",
              null,
              "aal",
              "standard_deviation",
              "cov",
              null,
              "selected_class",
              "gn_in_force_premium",
              "unadjusted_gn_cat_ulr",
              null,
              "roll_forward",
              "inflation_factor",
              "rate_change_factor",
              "selected_gn_cat_ulr"
            ]}
              fields={[
              "critical_prob",
              "return_period",
              "curve_1",
              "curve_2",
              "curve_3",
              "curve_4",
              "curve_5",
              "curve_6",
              "curve_7",
              "curve_8",
              "curve_9",
              "curve_10",
              null,
              "curve_1_cnv",
              "curve_2_cnv",
              "curve_3_cnv",
              "curve_4_cnv",
              "curve_5_cnv",
              "curve_6_cnv",
              "curve_7_cnv",
              "curve_8_cnv",
              "curve_9_cnv",
              "curve_10_cnv"
            ]} />
          </HX.Pane>
          <HX.Notes field="cds/cat/note_1.read_only" />
          <HX.Notes field="cds/cat/note_2.read_only" />
        </HX.Section>
        <HX.Section title="Commentary"
          collapsible={false}>
          <HX.Notes field="cds/rationale/cat_notes"
            title="Please note any rationale for selection below, and any use of overrides:" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Portfolio Profile"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_portfolio_profile">
        <HX.Section title="Summary By Lob"
          collapsible={false}>
          <HX.Table kb-interactive={true}
            data={[
            "cds/portfolio_profile/summary_by_lob"
          ]}
            fields={[
            "selected_lob",
            "bp_class",
            "risk_code",
            "selected_premium",
            "weighting",
            null,
            {
              "field": "rate_change_with_selection_override/year_0",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_0"
            },
            {
              "field": "rate_change_with_selection_override/year_1",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_1"
            },
            {
              "field": "rate_change_with_selection_override/year_2",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_2"
            },
            {
              "field": "rate_change_with_selection_override/year_3",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_3"
            },
            {
              "field": "rate_change_with_selection_override/year_4",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_4"
            },
            {
              "field": "rate_change_with_selection_override/year_5",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_5"
            },
            {
              "field": "rate_change_with_selection_override/year_6",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_6"
            },
            {
              "field": "rate_change_with_selection_override/year_7",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_7"
            },
            {
              "field": "rate_change_with_selection_override/year_8",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_8"
            },
            {
              "field": "rate_change_with_selection_override/year_9",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_9"
            },
            {
              "field": "rate_change_with_selection_override/year_10",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_10"
            },
            {
              "field": "rate_change_with_selection_override/year_11",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_11"
            },
            {
              "field": "rate_change_with_selection_override/year_12",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_12"
            },
            {
              "field": "rate_change_with_selection_override/year_13",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_13"
            },
            {
              "field": "rate_change_with_selection_override/year_14",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_14"
            },
            {
              "field": "rate_change_with_selection_override/year_15",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_15"
            },
            {
              "field": "rate_change_with_selection_override/year_16",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_16"
            },
            {
              "field": "rate_change_with_selection_override/year_17",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_17"
            },
            {
              "field": "rate_change_with_selection_override/year_18",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_18"
            },
            {
              "field": "rate_change_with_selection_override/year_19",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_19"
            },
            {
              "field": "rate_change_with_selection_override/year_20",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_20"
            },
            {
              "field": "rate_change_with_selection_override/year_21",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_21"
            },
            {
              "field": "rate_change_with_selection_override/year_22",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_22"
            },
            {
              "field": "rate_change_with_selection_override/year_23",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_23"
            },
            {
              "field": "rate_change_with_selection_override/year_24",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_24"
            },
            {
              "field": "rate_change_with_selection_override/year_25",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_25"
            },
            null,
            {
              "field": "rate_change_no_override/year_0",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_0"
            },
            {
              "field": "rate_change_no_override/year_1",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_1"
            },
            {
              "field": "rate_change_no_override/year_2",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_2"
            },
            {
              "field": "rate_change_no_override/year_3",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_3"
            },
            {
              "field": "rate_change_no_override/year_4",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_4"
            },
            {
              "field": "rate_change_no_override/year_5",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_5"
            },
            {
              "field": "rate_change_no_override/year_6",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_6"
            },
            {
              "field": "rate_change_no_override/year_7",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_7"
            },
            {
              "field": "rate_change_no_override/year_8",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_8"
            },
            {
              "field": "rate_change_no_override/year_9",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_9"
            },
            {
              "field": "rate_change_no_override/year_10",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_10"
            },
            {
              "field": "rate_change_no_override/year_11",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_11"
            },
            {
              "field": "rate_change_no_override/year_12",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_12"
            },
            {
              "field": "rate_change_no_override/year_13",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_13"
            },
            {
              "field": "rate_change_no_override/year_14",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_14"
            },
            {
              "field": "rate_change_no_override/year_15",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_15"
            },
            {
              "field": "rate_change_no_override/year_16",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_16"
            },
            {
              "field": "rate_change_no_override/year_17",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_17"
            },
            {
              "field": "rate_change_no_override/year_18",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_18"
            },
            {
              "field": "rate_change_no_override/year_19",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_19"
            },
            {
              "field": "rate_change_no_override/year_20",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_20"
            },
            {
              "field": "rate_change_no_override/year_21",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_21"
            },
            {
              "field": "rate_change_no_override/year_22",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_22"
            },
            {
              "field": "rate_change_no_override/year_23",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_23"
            },
            {
              "field": "rate_change_no_override/year_24",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_24"
            },
            {
              "field": "rate_change_no_override/year_25",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_25"
            },
            null,
            {
              "field": "lloyds_incurred_development/year_0",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_0"
            },
            {
              "field": "lloyds_incurred_development/year_1",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_1"
            },
            {
              "field": "lloyds_incurred_development/year_2",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_2"
            },
            {
              "field": "lloyds_incurred_development/year_3",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_3"
            },
            {
              "field": "lloyds_incurred_development/year_4",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_4"
            },
            {
              "field": "lloyds_incurred_development/year_5",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_5"
            },
            {
              "field": "lloyds_incurred_development/year_6",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_6"
            },
            {
              "field": "lloyds_incurred_development/year_7",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_7"
            },
            {
              "field": "lloyds_incurred_development/year_8",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_8"
            },
            {
              "field": "lloyds_incurred_development/year_9",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_9"
            },
            {
              "field": "lloyds_incurred_development/year_10",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_10"
            },
            {
              "field": "lloyds_incurred_development/year_11",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_11"
            },
            {
              "field": "lloyds_incurred_development/year_12",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_12"
            },
            {
              "field": "lloyds_incurred_development/year_13",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_13"
            },
            {
              "field": "lloyds_incurred_development/year_14",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_14"
            },
            {
              "field": "lloyds_incurred_development/year_15",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_15"
            },
            {
              "field": "lloyds_incurred_development/year_16",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_16"
            },
            {
              "field": "lloyds_incurred_development/year_17",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_17"
            },
            {
              "field": "lloyds_incurred_development/year_18",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_18"
            },
            {
              "field": "lloyds_incurred_development/year_19",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_19"
            },
            {
              "field": "lloyds_incurred_development/year_20",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_20"
            },
            {
              "field": "lloyds_incurred_development/year_21",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_21"
            },
            {
              "field": "lloyds_incurred_development/year_22",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_22"
            },
            {
              "field": "lloyds_incurred_development/year_23",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_23"
            },
            {
              "field": "lloyds_incurred_development/year_24",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_24"
            },
            {
              "field": "lloyds_incurred_development/year_25",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_25"
            },
            null,
            {
              "field": "lloyds_paid_development/year_0",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_0"
            },
            {
              "field": "lloyds_paid_development/year_1",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_1"
            },
            {
              "field": "lloyds_paid_development/year_2",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_2"
            },
            {
              "field": "lloyds_paid_development/year_3",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_3"
            },
            {
              "field": "lloyds_paid_development/year_4",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_4"
            },
            {
              "field": "lloyds_paid_development/year_5",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_5"
            },
            {
              "field": "lloyds_paid_development/year_6",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_6"
            },
            {
              "field": "lloyds_paid_development/year_7",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_7"
            },
            {
              "field": "lloyds_paid_development/year_8",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_8"
            },
            {
              "field": "lloyds_paid_development/year_9",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_9"
            },
            {
              "field": "lloyds_paid_development/year_10",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_10"
            },
            {
              "field": "lloyds_paid_development/year_11",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_11"
            },
            {
              "field": "lloyds_paid_development/year_12",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_12"
            },
            {
              "field": "lloyds_paid_development/year_13",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_13"
            },
            {
              "field": "lloyds_paid_development/year_14",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_14"
            },
            {
              "field": "lloyds_paid_development/year_15",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_15"
            },
            {
              "field": "lloyds_paid_development/year_16",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_16"
            },
            {
              "field": "lloyds_paid_development/year_17",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_17"
            },
            {
              "field": "lloyds_paid_development/year_18",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_18"
            },
            {
              "field": "lloyds_paid_development/year_19",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_19"
            },
            {
              "field": "lloyds_paid_development/year_20",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_20"
            },
            {
              "field": "lloyds_paid_development/year_21",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_21"
            },
            {
              "field": "lloyds_paid_development/year_22",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_22"
            },
            {
              "field": "lloyds_paid_development/year_23",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_23"
            },
            {
              "field": "lloyds_paid_development/year_24",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_24"
            },
            {
              "field": "lloyds_paid_development/year_25",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_25"
            },
            null,
            {
              "field": "lloyds_premium_development/year_0",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_0"
            },
            {
              "field": "lloyds_premium_development/year_1",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_1"
            },
            {
              "field": "lloyds_premium_development/year_2",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_2"
            },
            {
              "field": "lloyds_premium_development/year_3",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_3"
            },
            {
              "field": "lloyds_premium_development/year_4",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_4"
            },
            {
              "field": "lloyds_premium_development/year_5",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_5"
            },
            {
              "field": "lloyds_premium_development/year_6",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_6"
            },
            {
              "field": "lloyds_premium_development/year_7",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_7"
            },
            {
              "field": "lloyds_premium_development/year_8",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_8"
            },
            {
              "field": "lloyds_premium_development/year_9",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_9"
            },
            {
              "field": "lloyds_premium_development/year_10",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_10"
            },
            {
              "field": "lloyds_premium_development/year_11",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_11"
            },
            {
              "field": "lloyds_premium_development/year_12",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_12"
            },
            {
              "field": "lloyds_premium_development/year_13",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_13"
            },
            {
              "field": "lloyds_premium_development/year_14",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_14"
            },
            {
              "field": "lloyds_premium_development/year_15",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_15"
            },
            {
              "field": "lloyds_premium_development/year_16",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_16"
            },
            {
              "field": "lloyds_premium_development/year_17",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_17"
            },
            {
              "field": "lloyds_premium_development/year_18",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_18"
            },
            {
              "field": "lloyds_premium_development/year_19",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_19"
            },
            {
              "field": "lloyds_premium_development/year_20",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_20"
            },
            {
              "field": "lloyds_premium_development/year_21",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_21"
            },
            {
              "field": "lloyds_premium_development/year_22",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_22"
            },
            {
              "field": "lloyds_premium_development/year_23",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_23"
            },
            {
              "field": "lloyds_premium_development/year_24",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_24"
            },
            {
              "field": "lloyds_premium_development/year_25",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_25"
            },
            null,
            "lloyds_risk_code_results/final_gn_ulr",
            "lloyds_risk_code_results/selected_ielr",
            "lloyds_risk_code_results/model_ielr",
            null,
            "beazley_risk_code_results/final_gn_ulr"
          ]}
            freezeLeft={1} />
        </HX.Section>
        <HX.Section title="All combinations of Selected Lob x Risk Code"
          collapsible={false}>
          <HX.Table kb-interactive={true}
            data={[
            "cds/portfolio_profile/selected_lob_and_risk_code_combination"
          ]}
            fields={[
            "selected_lob",
            "bp_class",
            "risk_code",
            "selected_premium",
            "weighting",
            null,
            {
              "field": "rate_change_with_selection_override/year_0",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_0"
            },
            {
              "field": "rate_change_with_selection_override/year_1",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_1"
            },
            {
              "field": "rate_change_with_selection_override/year_2",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_2"
            },
            {
              "field": "rate_change_with_selection_override/year_3",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_3"
            },
            {
              "field": "rate_change_with_selection_override/year_4",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_4"
            },
            {
              "field": "rate_change_with_selection_override/year_5",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_5"
            },
            {
              "field": "rate_change_with_selection_override/year_6",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_6"
            },
            {
              "field": "rate_change_with_selection_override/year_7",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_7"
            },
            {
              "field": "rate_change_with_selection_override/year_8",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_8"
            },
            {
              "field": "rate_change_with_selection_override/year_9",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_9"
            },
            {
              "field": "rate_change_with_selection_override/year_10",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_10"
            },
            {
              "field": "rate_change_with_selection_override/year_11",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_11"
            },
            {
              "field": "rate_change_with_selection_override/year_12",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_12"
            },
            {
              "field": "rate_change_with_selection_override/year_13",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_13"
            },
            {
              "field": "rate_change_with_selection_override/year_14",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_14"
            },
            {
              "field": "rate_change_with_selection_override/year_15",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_15"
            },
            {
              "field": "rate_change_with_selection_override/year_16",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_16"
            },
            {
              "field": "rate_change_with_selection_override/year_17",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_17"
            },
            {
              "field": "rate_change_with_selection_override/year_18",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_18"
            },
            {
              "field": "rate_change_with_selection_override/year_19",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_19"
            },
            {
              "field": "rate_change_with_selection_override/year_20",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_20"
            },
            {
              "field": "rate_change_with_selection_override/year_21",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_21"
            },
            {
              "field": "rate_change_with_selection_override/year_22",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_22"
            },
            {
              "field": "rate_change_with_selection_override/year_23",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_23"
            },
            {
              "field": "rate_change_with_selection_override/year_24",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_24"
            },
            {
              "field": "rate_change_with_selection_override/year_25",
              "labelBy": "non_cds/portfolio_profile/rate_change_with_selection_override/year_25"
            },
            null,
            {
              "field": "rate_change_no_override/year_0",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_0"
            },
            {
              "field": "rate_change_no_override/year_1",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_1"
            },
            {
              "field": "rate_change_no_override/year_2",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_2"
            },
            {
              "field": "rate_change_no_override/year_3",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_3"
            },
            {
              "field": "rate_change_no_override/year_4",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_4"
            },
            {
              "field": "rate_change_no_override/year_5",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_5"
            },
            {
              "field": "rate_change_no_override/year_6",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_6"
            },
            {
              "field": "rate_change_no_override/year_7",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_7"
            },
            {
              "field": "rate_change_no_override/year_8",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_8"
            },
            {
              "field": "rate_change_no_override/year_9",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_9"
            },
            {
              "field": "rate_change_no_override/year_10",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_10"
            },
            {
              "field": "rate_change_no_override/year_11",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_11"
            },
            {
              "field": "rate_change_no_override/year_12",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_12"
            },
            {
              "field": "rate_change_no_override/year_13",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_13"
            },
            {
              "field": "rate_change_no_override/year_14",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_14"
            },
            {
              "field": "rate_change_no_override/year_15",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_15"
            },
            {
              "field": "rate_change_no_override/year_16",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_16"
            },
            {
              "field": "rate_change_no_override/year_17",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_17"
            },
            {
              "field": "rate_change_no_override/year_18",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_18"
            },
            {
              "field": "rate_change_no_override/year_19",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_19"
            },
            {
              "field": "rate_change_no_override/year_20",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_20"
            },
            {
              "field": "rate_change_no_override/year_21",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_21"
            },
            {
              "field": "rate_change_no_override/year_22",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_22"
            },
            {
              "field": "rate_change_no_override/year_23",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_23"
            },
            {
              "field": "rate_change_no_override/year_24",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_24"
            },
            {
              "field": "rate_change_no_override/year_25",
              "labelBy": "non_cds/portfolio_profile/rate_change_no_override/year_25"
            },
            null,
            {
              "field": "lloyds_incurred_development/year_0",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_0"
            },
            {
              "field": "lloyds_incurred_development/year_1",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_1"
            },
            {
              "field": "lloyds_incurred_development/year_2",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_2"
            },
            {
              "field": "lloyds_incurred_development/year_3",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_3"
            },
            {
              "field": "lloyds_incurred_development/year_4",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_4"
            },
            {
              "field": "lloyds_incurred_development/year_5",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_5"
            },
            {
              "field": "lloyds_incurred_development/year_6",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_6"
            },
            {
              "field": "lloyds_incurred_development/year_7",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_7"
            },
            {
              "field": "lloyds_incurred_development/year_8",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_8"
            },
            {
              "field": "lloyds_incurred_development/year_9",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_9"
            },
            {
              "field": "lloyds_incurred_development/year_10",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_10"
            },
            {
              "field": "lloyds_incurred_development/year_11",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_11"
            },
            {
              "field": "lloyds_incurred_development/year_12",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_12"
            },
            {
              "field": "lloyds_incurred_development/year_13",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_13"
            },
            {
              "field": "lloyds_incurred_development/year_14",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_14"
            },
            {
              "field": "lloyds_incurred_development/year_15",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_15"
            },
            {
              "field": "lloyds_incurred_development/year_16",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_16"
            },
            {
              "field": "lloyds_incurred_development/year_17",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_17"
            },
            {
              "field": "lloyds_incurred_development/year_18",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_18"
            },
            {
              "field": "lloyds_incurred_development/year_19",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_19"
            },
            {
              "field": "lloyds_incurred_development/year_20",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_20"
            },
            {
              "field": "lloyds_incurred_development/year_21",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_21"
            },
            {
              "field": "lloyds_incurred_development/year_22",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_22"
            },
            {
              "field": "lloyds_incurred_development/year_23",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_23"
            },
            {
              "field": "lloyds_incurred_development/year_24",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_24"
            },
            {
              "field": "lloyds_incurred_development/year_25",
              "labelBy": "non_cds/portfolio_profile/lloyds_incurred_development/year_25"
            },
            null,
            {
              "field": "lloyds_paid_development/year_0",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_0"
            },
            {
              "field": "lloyds_paid_development/year_1",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_1"
            },
            {
              "field": "lloyds_paid_development/year_2",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_2"
            },
            {
              "field": "lloyds_paid_development/year_3",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_3"
            },
            {
              "field": "lloyds_paid_development/year_4",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_4"
            },
            {
              "field": "lloyds_paid_development/year_5",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_5"
            },
            {
              "field": "lloyds_paid_development/year_6",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_6"
            },
            {
              "field": "lloyds_paid_development/year_7",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_7"
            },
            {
              "field": "lloyds_paid_development/year_8",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_8"
            },
            {
              "field": "lloyds_paid_development/year_9",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_9"
            },
            {
              "field": "lloyds_paid_development/year_10",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_10"
            },
            {
              "field": "lloyds_paid_development/year_11",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_11"
            },
            {
              "field": "lloyds_paid_development/year_12",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_12"
            },
            {
              "field": "lloyds_paid_development/year_13",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_13"
            },
            {
              "field": "lloyds_paid_development/year_14",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_14"
            },
            {
              "field": "lloyds_paid_development/year_15",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_15"
            },
            {
              "field": "lloyds_paid_development/year_16",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_16"
            },
            {
              "field": "lloyds_paid_development/year_17",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_17"
            },
            {
              "field": "lloyds_paid_development/year_18",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_18"
            },
            {
              "field": "lloyds_paid_development/year_19",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_19"
            },
            {
              "field": "lloyds_paid_development/year_20",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_20"
            },
            {
              "field": "lloyds_paid_development/year_21",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_21"
            },
            {
              "field": "lloyds_paid_development/year_22",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_22"
            },
            {
              "field": "lloyds_paid_development/year_23",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_23"
            },
            {
              "field": "lloyds_paid_development/year_24",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_24"
            },
            {
              "field": "lloyds_paid_development/year_25",
              "labelBy": "non_cds/portfolio_profile/lloyds_paid_development/year_25"
            },
            null,
            {
              "field": "lloyds_premium_development/year_0",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_0"
            },
            {
              "field": "lloyds_premium_development/year_1",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_1"
            },
            {
              "field": "lloyds_premium_development/year_2",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_2"
            },
            {
              "field": "lloyds_premium_development/year_3",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_3"
            },
            {
              "field": "lloyds_premium_development/year_4",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_4"
            },
            {
              "field": "lloyds_premium_development/year_5",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_5"
            },
            {
              "field": "lloyds_premium_development/year_6",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_6"
            },
            {
              "field": "lloyds_premium_development/year_7",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_7"
            },
            {
              "field": "lloyds_premium_development/year_8",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_8"
            },
            {
              "field": "lloyds_premium_development/year_9",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_9"
            },
            {
              "field": "lloyds_premium_development/year_10",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_10"
            },
            {
              "field": "lloyds_premium_development/year_11",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_11"
            },
            {
              "field": "lloyds_premium_development/year_12",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_12"
            },
            {
              "field": "lloyds_premium_development/year_13",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_13"
            },
            {
              "field": "lloyds_premium_development/year_14",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_14"
            },
            {
              "field": "lloyds_premium_development/year_15",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_15"
            },
            {
              "field": "lloyds_premium_development/year_16",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_16"
            },
            {
              "field": "lloyds_premium_development/year_17",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_17"
            },
            {
              "field": "lloyds_premium_development/year_18",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_18"
            },
            {
              "field": "lloyds_premium_development/year_19",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_19"
            },
            {
              "field": "lloyds_premium_development/year_20",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_20"
            },
            {
              "field": "lloyds_premium_development/year_21",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_21"
            },
            {
              "field": "lloyds_premium_development/year_22",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_22"
            },
            {
              "field": "lloyds_premium_development/year_23",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_23"
            },
            {
              "field": "lloyds_premium_development/year_24",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_24"
            },
            {
              "field": "lloyds_premium_development/year_25",
              "labelBy": "non_cds/portfolio_profile/lloyds_premium_development/year_25"
            },
            null,
            "lloyds_risk_code_results/final_gn_ulr",
            "lloyds_risk_code_results/selected_ielr",
            "lloyds_risk_code_results/model_ielr",
            null,
            "beazley_risk_code_results/final_gn_ulr"
          ]}
            freezeLeft={1} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Own Experience"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_own_experience">
        <HX.Section title="Own Experience Summary">
          <HX.Notes field="cds/projections_own_experience/error_msg"
            shownBy="non_cds/own_experience/is_error_msg_shown" />
          <HX.Table title="Own Experience Summary"
            data={[
            "cds/projections_own_experience/summary_table"
          ]}
            fields={[
            "selected_lob",
            "claim_source",
            "claim_basis",
            "claim_to_develop_to_ultimate",
            "cat_basis",
            {
              "field": "ielr_approach",
              "shownBy": "/non_cds/risk_information/is_actuarial"
            },
            {
              "field": "ielr_approach.read_only_option",
              "shownBy": "/non_cds/risk_information/is_underwriter"
            },
            null,
            "selected_attr",
            "selected_large",
            "selected_cat",
            "selected_total",
            "selected_total_excl_cat",
            null,
            "model_default_attr",
            "model_default_large",
            "model_default_cat",
            "model_default_total",
            "model_default_total_excl_cat",
            null,
            "ovd_dev",
            "ovd_index",
            "ovd_premium",
            "ovd_ielr_weights",
            "ovd_ielr",
            "ovd_ibnr",
            "ovd_ultimate_method",
            "ovd_ultimate",
            "ovd_ulr_weights",
            "ovd_ulr"
          ]}
            filter="is_row_visible"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Selected LoB - 1"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_own_experience",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "selected_lob_1",
              "show_all_yrs",
              "show_detail",
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "claim_source",
                "claim_basis",
                "claim_to_develop_to_ultimate",
                "cat_basis",
                {
                  "field": "ielr_approach",
                  "shownBy": "/non_cds/risk_information/is_actuarial"
                },
                {
                  "field": "ielr_approach.read_only_option",
                  "shownBy": "/non_cds/risk_information/is_underwriter"
                }
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 100
                }
              ]}
                fields={[
                {
                  "field": "ielr_attr",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
                },
                {
                  "field": "ielr_large",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
                },
                {
                  "field": "ielr_cat",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
                },
                "ielr_total",
                "ielr_total_excl_cat",
                "lloyds_selected_ielr"
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
              <HX.With context={{
                "path": "selected_lob_totals_1",
                "type": "struct"
              }}>
                <HX.Table with="ielr_approaches"
                  title="Model Default - IELR Approach Analysis"
                  data={[
                  {
                    "datum": "nominal",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_all_yr",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_cl_yr",
                    "maxWidth": 100
                  }
                ]}
                  fields={[
                  "ielr_attr",
                  "ielr_large",
                  "ielr_cat",
                  "ielr_total",
                  "ielr_total_excl_cat"
                ]}
                  kb-interactive={true}
                  transpose={true}
                  shownBy="/non_cds/risk_information/is_actuarial" />
              </HX.With>
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_1",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              null,
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ielr_weighting_sel_total"
            ]}
              freezeLeft={0}
              filter="lob_visible_1"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_compact" />
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_1",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_open_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "latest_incurred_open_claims_total",
              {
                "field": "latest_incurred_closed_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "latest_incurred_closed_claims_total",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "last_year_position_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "last_year_position_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "last_year_position_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "last_year_position_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "applied_rate_change_cumulative",
              "applied_inflation_cumulative",
              "onlevel_factor_cumulative",
              null,
              {
                "field": "development_pattern_premium_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_paid_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_incurred_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              "development_pattern_premium_lloyds",
              "development_pattern_incurred_lloyds",
              {
                "field": "development_pattern_premium_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_incurred_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_premium_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "development_pattern_incurred_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_cl",
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_incurred_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ultimate_incurred_cl_total",
              "ultimate_incurred_cl_ielr",
              {
                "field": "ultimate_incurred_ielr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ultimate_incurred_ielr_total",
              {
                "field": "ultimate_incurred_bf_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ultimate_incurred_bf_total",
              {
                "field": "ielr_weighting_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ielr_weighting_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ielr_weighting_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ielr_weighting_cl_total",
              "method_incurred",
              "additional_ibnr_attr",
              "additional_ibnr_large",
              "additional_ibnr_cat",
              "additional_ibnr_total",
              {
                "field": "ultimate_incurred_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ultimate_incurred_selected_total",
              {
                "field": "ultimate_incurred_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_1/show_alc"
              },
              "ielr_weighting_sel_total",
              null,
              "exposure_weighting_onlevel_1",
              "decay_ratio_weighting_2",
              "developed_weighting_3",
              "overall_weighting_onlevel",
              null,
              "exposure_weighting_nominal_1",
              "overall_weighting_nominal",
              {
                "field": null,
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              }
            ]}
              freezeLeft={0}
              filter="lob_visible_1"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_detail" />
            <HX.Pane flow="right">
              <HX.Pane flow="right">
                <HX.With context={{
                  "path": "selected_lob_totals_1",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 1"
                    titleBy="selected_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "gn_ilr_total",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_ulr_selected_total",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "ultimate_ulr_on_levelled_total",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table title="Model Default Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "model_default_attr",
                  "model_default_large",
                  "model_default_cat_exp",
                  "model_default_cat_bp",
                  "model_default_cat_rms",
                  "model_default_cat_basis",
                  "model_default_cat",
                  null,
                  "model_default_total",
                  "model_default_total_excl_cat"
                ]}
                  filter="lob_visible_1"
                  kb-interactive={true}
                  transpose={true} />
                <HX.Table title="Selected Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "selected_attr",
                  "selected_large",
                  "selected_cat_exp",
                  "selected_cat_bp",
                  "selected_cat_rms",
                  "selected_cat_basis",
                  "selected_cat",
                  null,
                  "selected_total",
                  "selected_total_excl_cat"
                ]}
                  filter="lob_visible_1"
                  kb-interactive={true}
                  transpose={true} />
                <HX.With context={{
                  "indexBy": "/cds/projections_own_experience/selected_lob_totals_1/row",
                  "path": "summary_table",
                  "type": "list"
                }}>
                  <HX.Notes field="actuarial_notes"
                    title="Please note any rationale for selection below, and any use of overrides:" />
                </HX.With>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Selected LoB - 2"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_own_experience",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "selected_lob_2",
              "show_all_yrs",
              "show_detail",
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "claim_source",
                "claim_basis",
                "claim_to_develop_to_ultimate",
                "cat_basis",
                {
                  "field": "ielr_approach",
                  "shownBy": "/non_cds/risk_information/is_actuarial"
                },
                {
                  "field": "ielr_approach.read_only_option",
                  "shownBy": "/non_cds/risk_information/is_underwriter"
                }
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 100
                }
              ]}
                fields={[
                {
                  "field": "ielr_attr",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
                },
                {
                  "field": "ielr_large",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
                },
                {
                  "field": "ielr_cat",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
                },
                "ielr_total",
                "ielr_total_excl_cat",
                "lloyds_selected_ielr"
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
              <HX.With context={{
                "path": "selected_lob_totals_2",
                "type": "struct"
              }}>
                <HX.Table with="ielr_approaches"
                  title="Model Default - IELR Approach Analysis"
                  data={[
                  {
                    "datum": "nominal",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_all_yr",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_cl_yr",
                    "maxWidth": 100
                  }
                ]}
                  fields={[
                  "ielr_attr",
                  "ielr_large",
                  "ielr_cat",
                  "ielr_total",
                  "ielr_total_excl_cat"
                ]}
                  kb-interactive={true}
                  transpose={true}
                  shownBy="/non_cds/risk_information/is_actuarial" />
              </HX.With>
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_2",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              null,
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ielr_weighting_sel_total"
            ]}
              freezeLeft={0}
              filter="lob_visible_2"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_compact" />
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_2",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_open_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "latest_incurred_open_claims_total",
              {
                "field": "latest_incurred_closed_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "latest_incurred_closed_claims_total",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "last_year_position_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "last_year_position_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "last_year_position_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "last_year_position_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "applied_rate_change_cumulative",
              "applied_inflation_cumulative",
              "onlevel_factor_cumulative",
              null,
              {
                "field": "development_pattern_premium_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_paid_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_incurred_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              "development_pattern_premium_lloyds",
              "development_pattern_incurred_lloyds",
              {
                "field": "development_pattern_premium_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_incurred_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_premium_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "development_pattern_incurred_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_cl",
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_incurred_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ultimate_incurred_cl_total",
              "ultimate_incurred_cl_ielr",
              {
                "field": "ultimate_incurred_ielr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ultimate_incurred_ielr_total",
              {
                "field": "ultimate_incurred_bf_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ultimate_incurred_bf_total",
              {
                "field": "ielr_weighting_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ielr_weighting_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ielr_weighting_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ielr_weighting_cl_total",
              "method_incurred",
              "additional_ibnr_attr",
              "additional_ibnr_large",
              "additional_ibnr_cat",
              "additional_ibnr_total",
              {
                "field": "ultimate_incurred_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ultimate_incurred_selected_total",
              {
                "field": "ultimate_incurred_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_2/show_alc"
              },
              "ielr_weighting_sel_total",
              null,
              "exposure_weighting_onlevel_1",
              "decay_ratio_weighting_2",
              "developed_weighting_3",
              "overall_weighting_onlevel",
              null,
              "exposure_weighting_nominal_1",
              "overall_weighting_nominal",
              {
                "field": null,
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              }
            ]}
              freezeLeft={0}
              filter="lob_visible_2"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_detail" />
            <HX.Pane flow="right">
              <HX.Pane flow="right">
                <HX.With context={{
                  "path": "selected_lob_totals_2",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 2"
                    titleBy="selected_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "gn_ilr_total",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_ulr_selected_total",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "ultimate_ulr_on_levelled_total",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table title="Model Default Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "model_default_attr",
                  "model_default_large",
                  "model_default_cat_exp",
                  "model_default_cat_bp",
                  "model_default_cat_rms",
                  "model_default_cat_basis",
                  "model_default_cat",
                  null,
                  "model_default_total",
                  "model_default_total_excl_cat"
                ]}
                  filter="lob_visible_2"
                  kb-interactive={true}
                  transpose={true} />
                <HX.Table title="Selected Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "selected_attr",
                  "selected_large",
                  "selected_cat_exp",
                  "selected_cat_bp",
                  "selected_cat_rms",
                  "selected_cat_basis",
                  "selected_cat",
                  null,
                  "selected_total",
                  "selected_total_excl_cat"
                ]}
                  filter="lob_visible_2"
                  kb-interactive={true}
                  transpose={true} />
                <HX.With context={{
                  "indexBy": "/cds/projections_own_experience/selected_lob_totals_2/row",
                  "path": "summary_table",
                  "type": "list"
                }}>
                  <HX.Notes field="actuarial_notes"
                    title="Please note any rationale for selection below, and any use of overrides:" />
                </HX.With>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Selected LoB - 3"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_own_experience",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "selected_lob_3",
              "show_all_yrs",
              "show_detail",
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "claim_source",
                "claim_basis",
                "claim_to_develop_to_ultimate",
                "cat_basis",
                {
                  "field": "ielr_approach",
                  "shownBy": "/non_cds/risk_information/is_actuarial"
                },
                {
                  "field": "ielr_approach.read_only_option",
                  "shownBy": "/non_cds/risk_information/is_underwriter"
                }
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 100
                }
              ]}
                fields={[
                {
                  "field": "ielr_attr",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
                },
                {
                  "field": "ielr_large",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
                },
                {
                  "field": "ielr_cat",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
                },
                "ielr_total",
                "ielr_total_excl_cat",
                "lloyds_selected_ielr"
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
              <HX.With context={{
                "path": "selected_lob_totals_3",
                "type": "struct"
              }}>
                <HX.Table with="ielr_approaches"
                  title="Model Default - IELR Approach Analysis"
                  data={[
                  {
                    "datum": "nominal",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_all_yr",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_cl_yr",
                    "maxWidth": 100
                  }
                ]}
                  fields={[
                  "ielr_attr",
                  "ielr_large",
                  "ielr_cat",
                  "ielr_total",
                  "ielr_total_excl_cat"
                ]}
                  kb-interactive={true}
                  transpose={true}
                  shownBy="/non_cds/risk_information/is_actuarial" />
              </HX.With>
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_3",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              null,
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ielr_weighting_sel_total"
            ]}
              freezeLeft={0}
              filter="lob_visible_3"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_compact" />
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_3",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_open_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "latest_incurred_open_claims_total",
              {
                "field": "latest_incurred_closed_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "latest_incurred_closed_claims_total",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "last_year_position_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "last_year_position_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "last_year_position_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "last_year_position_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "applied_rate_change_cumulative",
              "applied_inflation_cumulative",
              "onlevel_factor_cumulative",
              null,
              {
                "field": "development_pattern_premium_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_paid_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_incurred_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              "development_pattern_premium_lloyds",
              "development_pattern_incurred_lloyds",
              {
                "field": "development_pattern_premium_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_incurred_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_premium_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "development_pattern_incurred_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_cl",
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_incurred_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ultimate_incurred_cl_total",
              "ultimate_incurred_cl_ielr",
              {
                "field": "ultimate_incurred_ielr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ultimate_incurred_ielr_total",
              {
                "field": "ultimate_incurred_bf_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ultimate_incurred_bf_total",
              {
                "field": "ielr_weighting_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ielr_weighting_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ielr_weighting_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ielr_weighting_cl_total",
              "method_incurred",
              "additional_ibnr_attr",
              "additional_ibnr_large",
              "additional_ibnr_cat",
              "additional_ibnr_total",
              {
                "field": "ultimate_incurred_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ultimate_incurred_selected_total",
              {
                "field": "ultimate_incurred_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_3/show_alc"
              },
              "ielr_weighting_sel_total",
              null,
              "exposure_weighting_onlevel_1",
              "decay_ratio_weighting_2",
              "developed_weighting_3",
              "overall_weighting_onlevel",
              null,
              "exposure_weighting_nominal_1",
              "overall_weighting_nominal",
              {
                "field": null,
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              }
            ]}
              freezeLeft={0}
              filter="lob_visible_3"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_detail" />
            <HX.Pane flow="right">
              <HX.Pane flow="right">
                <HX.With context={{
                  "path": "selected_lob_totals_3",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 3"
                    titleBy="selected_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "gn_ilr_total",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_ulr_selected_total",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "ultimate_ulr_on_levelled_total",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table title="Model Default Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "model_default_attr",
                  "model_default_large",
                  "model_default_cat_exp",
                  "model_default_cat_bp",
                  "model_default_cat_rms",
                  "model_default_cat_basis",
                  "model_default_cat",
                  null,
                  "model_default_total",
                  "model_default_total_excl_cat"
                ]}
                  filter="lob_visible_3"
                  kb-interactive={true}
                  transpose={true} />
                <HX.Table title="Selected Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "selected_attr",
                  "selected_large",
                  "selected_cat_exp",
                  "selected_cat_bp",
                  "selected_cat_rms",
                  "selected_cat_basis",
                  "selected_cat",
                  null,
                  "selected_total",
                  "selected_total_excl_cat"
                ]}
                  filter="lob_visible_3"
                  kb-interactive={true}
                  transpose={true} />
                <HX.With context={{
                  "indexBy": "/cds/projections_own_experience/selected_lob_totals_3/row",
                  "path": "summary_table",
                  "type": "list"
                }}>
                  <HX.Notes field="actuarial_notes"
                    title="Please note any rationale for selection below, and any use of overrides:" />
                </HX.With>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Selected LoB - 4"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_own_experience",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "selected_lob_4",
              "show_all_yrs",
              "show_detail",
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "claim_source",
                "claim_basis",
                "claim_to_develop_to_ultimate",
                "cat_basis",
                {
                  "field": "ielr_approach",
                  "shownBy": "/non_cds/risk_information/is_actuarial"
                },
                {
                  "field": "ielr_approach.read_only_option",
                  "shownBy": "/non_cds/risk_information/is_underwriter"
                }
              ]}
                filter="lob_visible_4"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 100
                }
              ]}
                fields={[
                {
                  "field": "ielr_attr",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
                },
                {
                  "field": "ielr_large",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
                },
                {
                  "field": "ielr_cat",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
                },
                "ielr_total",
                "ielr_total_excl_cat",
                "lloyds_selected_ielr"
              ]}
                filter="lob_visible_4"
                kb-interactive={true}
                transpose={true} />
              <HX.With context={{
                "path": "selected_lob_totals_4",
                "type": "struct"
              }}>
                <HX.Table with="ielr_approaches"
                  title="Model Default - IELR Approach Analysis"
                  data={[
                  {
                    "datum": "nominal",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_all_yr",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_cl_yr",
                    "maxWidth": 100
                  }
                ]}
                  fields={[
                  "ielr_attr",
                  "ielr_large",
                  "ielr_cat",
                  "ielr_total",
                  "ielr_total_excl_cat"
                ]}
                  kb-interactive={true}
                  transpose={true}
                  shownBy="/non_cds/risk_information/is_actuarial" />
              </HX.With>
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_4",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              null,
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ielr_weighting_sel_total"
            ]}
              freezeLeft={0}
              filter="lob_visible_4"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_compact" />
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_4",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_open_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "latest_incurred_open_claims_total",
              {
                "field": "latest_incurred_closed_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "latest_incurred_closed_claims_total",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "last_year_position_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "last_year_position_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "last_year_position_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "last_year_position_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "applied_rate_change_cumulative",
              "applied_inflation_cumulative",
              "onlevel_factor_cumulative",
              null,
              {
                "field": "development_pattern_premium_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_paid_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_incurred_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              "development_pattern_premium_lloyds",
              "development_pattern_incurred_lloyds",
              {
                "field": "development_pattern_premium_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_incurred_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_premium_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "development_pattern_incurred_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_cl",
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_incurred_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ultimate_incurred_cl_total",
              "ultimate_incurred_cl_ielr",
              {
                "field": "ultimate_incurred_ielr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ultimate_incurred_ielr_total",
              {
                "field": "ultimate_incurred_bf_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ultimate_incurred_bf_total",
              {
                "field": "ielr_weighting_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ielr_weighting_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ielr_weighting_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ielr_weighting_cl_total",
              "method_incurred",
              "additional_ibnr_attr",
              "additional_ibnr_large",
              "additional_ibnr_cat",
              "additional_ibnr_total",
              {
                "field": "ultimate_incurred_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ultimate_incurred_selected_total",
              {
                "field": "ultimate_incurred_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_4/show_alc"
              },
              "ielr_weighting_sel_total",
              null,
              "exposure_weighting_onlevel_1",
              "decay_ratio_weighting_2",
              "developed_weighting_3",
              "overall_weighting_onlevel",
              null,
              "exposure_weighting_nominal_1",
              "overall_weighting_nominal",
              {
                "field": null,
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              }
            ]}
              freezeLeft={0}
              filter="lob_visible_4"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_detail" />
            <HX.Pane flow="right">
              <HX.Pane flow="right">
                <HX.With context={{
                  "path": "selected_lob_totals_4",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 4"
                    titleBy="selected_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "gn_ilr_total",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_ulr_selected_total",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "ultimate_ulr_on_levelled_total",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table title="Model Default Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "model_default_attr",
                  "model_default_large",
                  "model_default_cat_exp",
                  "model_default_cat_bp",
                  "model_default_cat_rms",
                  "model_default_cat_basis",
                  "model_default_cat",
                  null,
                  "model_default_total",
                  "model_default_total_excl_cat"
                ]}
                  filter="lob_visible_4"
                  kb-interactive={true}
                  transpose={true} />
                <HX.Table title="Selected Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "selected_attr",
                  "selected_large",
                  "selected_cat_exp",
                  "selected_cat_bp",
                  "selected_cat_rms",
                  "selected_cat_basis",
                  "selected_cat",
                  null,
                  "selected_total",
                  "selected_total_excl_cat"
                ]}
                  filter="lob_visible_4"
                  kb-interactive={true}
                  transpose={true} />
                <HX.With context={{
                  "indexBy": "/cds/projections_own_experience/selected_lob_totals_4/row",
                  "path": "summary_table",
                  "type": "list"
                }}>
                  <HX.Notes field="actuarial_notes"
                    title="Please note any rationale for selection below, and any use of overrides:" />
                </HX.With>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Selected LoB - 5"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_own_experience",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "selected_lob_5",
              "show_all_yrs",
              "show_detail",
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "claim_source",
                "claim_basis",
                "claim_to_develop_to_ultimate",
                "cat_basis",
                {
                  "field": "ielr_approach",
                  "shownBy": "/non_cds/risk_information/is_actuarial"
                },
                {
                  "field": "ielr_approach.read_only_option",
                  "shownBy": "/non_cds/risk_information/is_underwriter"
                }
              ]}
                filter="lob_visible_5"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 100
                }
              ]}
                fields={[
                {
                  "field": "ielr_attr",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
                },
                {
                  "field": "ielr_large",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
                },
                {
                  "field": "ielr_cat",
                  "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
                },
                "ielr_total",
                "ielr_total_excl_cat",
                "lloyds_selected_ielr"
              ]}
                filter="lob_visible_5"
                kb-interactive={true}
                transpose={true} />
              <HX.With context={{
                "path": "selected_lob_totals_5",
                "type": "struct"
              }}>
                <HX.Table with="ielr_approaches"
                  title="Model Default - IELR Approach Analysis"
                  data={[
                  {
                    "datum": "nominal",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_all_yr",
                    "maxWidth": 100
                  },
                  {
                    "datum": "ol_cl_yr",
                    "maxWidth": 100
                  }
                ]}
                  fields={[
                  "ielr_attr",
                  "ielr_large",
                  "ielr_cat",
                  "ielr_total",
                  "ielr_total_excl_cat"
                ]}
                  kb-interactive={true}
                  transpose={true}
                  shownBy="/non_cds/risk_information/is_actuarial" />
              </HX.With>
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_5",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              null,
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ielr_weighting_sel_total"
            ]}
              freezeLeft={0}
              filter="lob_visible_5"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_compact" />
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_5",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_costs",
              {
                "field": "latest_incurred_open_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "latest_incurred_open_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "latest_incurred_open_claims_total",
              {
                "field": "latest_incurred_closed_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "latest_incurred_closed_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "latest_incurred_closed_claims_total",
              {
                "field": "latest_incurred_total_claims_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "latest_incurred_total_claims_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "latest_incurred_total_claims_total",
              {
                "field": "last_year_position_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "last_year_position_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "last_year_position_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "last_year_position_total",
              {
                "field": "movement_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "movement_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "movement_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "movement_total",
              {
                "field": "gn_ilr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "gn_ilr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "gn_ilr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "gn_ilr_total",
              null,
              {
                "field": "applied_rate_change.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_inflation.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "applied_rate_change",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "applied_inflation",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "applied_rate_change_cumulative",
              "applied_inflation_cumulative",
              "onlevel_factor_cumulative",
              null,
              {
                "field": "development_pattern_premium_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_paid_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "development_pattern_incurred_lloyds_unadjusted",
                "shownBy": "/cds/risk_information/show_refs"
              },
              "development_pattern_premium_lloyds",
              "development_pattern_incurred_lloyds",
              {
                "field": "development_pattern_premium_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_incurred_override.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "development_pattern_premium_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              {
                "field": "development_pattern_incurred_override",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "development_pattern_premium_selected",
              "development_pattern_incurred_selected",
              null,
              "ultimate_premium_selected_gnpi_cl",
              "ultimate_premium_selected_gnpi_override",
              "ultimate_premium_selected_gnpi_selected",
              "ultimate_premium_selected_gnpi_selected_ol",
              {
                "field": "ultimate_incurred_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_incurred_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ultimate_incurred_cl_total",
              "ultimate_incurred_cl_ielr",
              {
                "field": "ultimate_incurred_ielr_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_incurred_ielr_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ultimate_incurred_ielr_total",
              {
                "field": "ultimate_incurred_bf_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_incurred_bf_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ultimate_incurred_bf_total",
              {
                "field": "ielr_weighting_cl_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ielr_weighting_cl_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ielr_weighting_cl_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ielr_weighting_cl_total",
              "method_incurred",
              "additional_ibnr_attr",
              "additional_ibnr_large",
              "additional_ibnr_cat",
              "additional_ibnr_total",
              {
                "field": "ultimate_incurred_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_incurred_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ultimate_incurred_selected_total",
              {
                "field": "ultimate_incurred_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_ulr_selected_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ultimate_ulr_selected_total",
              {
                "field": "ultimate_ulr_selected_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              null,
              {
                "field": "ultimate_ulr_on_levelled_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ultimate_ulr_on_levelled_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ultimate_ulr_on_levelled_total",
              {
                "field": "ultimate_ulr_on_levelled_total_x_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              null,
              "modelled_weighting",
              {
                "field": "ielr_weighting_sel_attr",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ielr_weighting_sel_large",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              {
                "field": "ielr_weighting_sel_cat",
                "shownBy": "/cds/projections_own_experience/selected_lob_totals_5/show_alc"
              },
              "ielr_weighting_sel_total",
              null,
              "exposure_weighting_onlevel_1",
              "decay_ratio_weighting_2",
              "developed_weighting_3",
              "overall_weighting_onlevel",
              null,
              "exposure_weighting_nominal_1",
              "overall_weighting_nominal",
              {
                "field": null,
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_prem_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_lower",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_upper",
                "shownBy": "/cds/risk_information/show_refs"
              },
              {
                "field": "adjustments_incurred_lloyds_actual",
                "shownBy": "/cds/risk_information/show_refs"
              }
            ]}
              freezeLeft={0}
              filter="lob_visible_5"
              kb-interactive={true}
              transpose={false}
              shownBy="/cds/projections_own_experience/show_detail" />
            <HX.Pane flow="right">
              <HX.Pane flow="right">
                <HX.With context={{
                  "path": "selected_lob_totals_5",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 5"
                    titleBy="selected_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "gn_ilr_total",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_ulr_selected_total",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "ultimate_ulr_on_levelled_total",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Table title="Model Default Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "model_default_attr",
                  "model_default_large",
                  "model_default_cat_exp",
                  "model_default_cat_bp",
                  "model_default_cat_rms",
                  "model_default_cat_basis",
                  "model_default_cat",
                  null,
                  "model_default_total",
                  "model_default_total_excl_cat"
                ]}
                  filter="lob_visible_5"
                  kb-interactive={true}
                  transpose={true} />
                <HX.Table title="Selected Loss Ratios"
                  data={[
                  {
                    "datum": "summary_table",
                    "maxWidth": 150
                  }
                ]}
                  fields={[
                  "selected_attr",
                  "selected_large",
                  "selected_cat_exp",
                  "selected_cat_bp",
                  "selected_cat_rms",
                  "selected_cat_basis",
                  "selected_cat",
                  null,
                  "selected_total",
                  "selected_total_excl_cat"
                ]}
                  filter="lob_visible_5"
                  kb-interactive={true}
                  transpose={true} />
                <HX.With context={{
                  "indexBy": "/cds/projections_own_experience/selected_lob_totals_5/row",
                  "path": "summary_table",
                  "type": "list"
                }}>
                  <HX.Notes field="actuarial_notes"
                    title="Please note any rationale for selection below, and any use of overrides:" />
                </HX.With>
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Lloyds Projections"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_lloyds_proj">
        <HX.Section title="Lloyds Projection Summary">
          <HX.Notes field="cds/projections_own_experience/error_msg"
            shownBy="non_cds/own_experience/is_error_msg_shown" />
          <HX.Table title="Lloyds Projection Summary"
            data={[
            "cds/projections_lloyds/summary_table"
          ]}
            fields={[
            "risk_code",
            "selected_lob",
            "bp_class",
            "tracker_class",
            "composition",
            "model_acc_aqn",
            "projection_type.read_only_option",
            "ielr_approach",
            "selected_final_gn_ulr",
            "bp_cat",
            "bp_cat_load",
            "selected_ielr",
            "model_final_gn_ulr",
            "model_ielr",
            "checked",
            "comments"
          ]}
            maxListVisibleRows={10}
            filter="is_row_visible"
            kb-interactive={true}
            freezeLeft={1} />
        </HX.Section>
        <HX.Section title="Selected LoB - 1"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_lloyds",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "lookup_lob_1",
              "show_all_yrs",
              null,
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "risk_code",
                "bp_class",
                "tracker_class",
                "projection_type.read_only_option",
                "ielr_approach",
                "composition"
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Summary IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_ielr_nominal",
                "model_ielr_onlevel",
                "model_ielr_ol_allyr",
                "model_ielr",
                "selected_ielr"
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Model Default Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_gn_ulr",
                "model_base_aqn",
                "model_acc_aqn",
                "model_adj_gn_ulr",
                null,
                "bp_cat_load",
                "model_final_gn_ulr"
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_gn_ulr",
                "selected_base_aqn",
                "selected_acc_aqn",
                "selected_adj_gn_ulr",
                null,
                "bp_cat_load",
                "selected_final_gn_ulr"
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_1",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_ratio",
              "latest_paid",
              "latest_incurred",
              "incurred_loss_ratio",
              "dev_patterns_gnpi",
              "dev_patterns_paid",
              "dev_patterns_incurred",
              "inflation_model",
              "rate_change_model",
              "rate_change_selected",
              "ultimate_gnpi",
              "ultimate_gnpi_ol_model",
              "ultimate_gnpi_ol_selected",
              "ultimate_cl_paid",
              "ultimate_cl_paid_ulr",
              "ultimate_cl_incurred",
              "ultimate_cl_incurred_ulr",
              "ultimate_ielr_model",
              "ultimate_ielr_model_ulr",
              "ultimate_ielr_selected",
              "ultimate_ielr_selected_ulr",
              "ultimate_bf_model_paid",
              "ultimate_bf_model_incurred",
              "ultimate_bf_selected_paid",
              "ultimate_bf_selected_incurred",
              "weighting_ielr",
              "method_paid",
              "method_incurred",
              "ultimate_model",
              "ultimate_model_ulr",
              "ultimate_selected",
              "ultimate_selected_ulr",
              "on_levelled_model_ulr",
              "on_levelled_selected_ulr",
              "weighting_model",
              "weighting_selected",
              null,
              "weighting_1_exposure_onlevel",
              "weighting_2_decay_ratio",
              "weighting_3_developed",
              "weighting_onlevel",
              null,
              "weighting_1_exposure_nominal",
              "weighting_nominal",
              null,
              "inflation_model_index",
              "rate_change_model_index",
              "rate_change_selected_index",
              "loss_ratio_model_index",
              "loss_ratio_selected_index"
            ]}
              maxListVisibleRows={8}
              filter="lob_visible_1"
              kb-interactive={true}
              transpose={false}
              freezeLeft={0} />
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.With context={{
                  "path": "selected_lob_totals_1",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 1"
                    titleBy="lookup_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "incurred_loss_ratio",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_selected_ulr",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "on_levelled_selected_ulr",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.With context={{
                "indexBy": "/cds/projections_lloyds/selected_lob_totals_1/row",
                "path": "summary_table",
                "type": "list"
              }}>
                <HX.Notes field="actuarial_notes"
                  title="Please note any rationale for selection below, and any use of overrides:" />
              </HX.With>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Selected LoB - 2"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_lloyds",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "lookup_lob_2",
              "show_all_yrs",
              null,
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "risk_code",
                "bp_class",
                "tracker_class",
                "projection_type.read_only_option",
                "ielr_approach",
                "composition"
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Summary IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_ielr_nominal",
                "model_ielr_onlevel",
                "model_ielr_ol_allyr",
                "model_ielr",
                "selected_ielr"
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Model Default Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_gn_ulr",
                "model_base_aqn",
                "model_acc_aqn",
                "model_adj_gn_ulr",
                null,
                "bp_cat_load",
                "model_final_gn_ulr"
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_gn_ulr",
                "selected_base_aqn",
                "selected_acc_aqn",
                "selected_adj_gn_ulr",
                null,
                "bp_cat_load",
                "selected_final_gn_ulr"
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_2",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_ratio",
              "latest_paid",
              "latest_incurred",
              "incurred_loss_ratio",
              "dev_patterns_gnpi",
              "dev_patterns_paid",
              "dev_patterns_incurred",
              "inflation_model",
              "rate_change_model",
              "rate_change_selected",
              "ultimate_gnpi",
              "ultimate_gnpi_ol_model",
              "ultimate_gnpi_ol_selected",
              "ultimate_cl_paid",
              "ultimate_cl_paid_ulr",
              "ultimate_cl_incurred",
              "ultimate_cl_incurred_ulr",
              "ultimate_ielr_model",
              "ultimate_ielr_model_ulr",
              "ultimate_ielr_selected",
              "ultimate_ielr_selected_ulr",
              "ultimate_bf_model_paid",
              "ultimate_bf_model_incurred",
              "ultimate_bf_selected_paid",
              "ultimate_bf_selected_incurred",
              "weighting_ielr",
              "method_paid",
              "method_incurred",
              "ultimate_model",
              "ultimate_model_ulr",
              "ultimate_selected",
              "ultimate_selected_ulr",
              "on_levelled_model_ulr",
              "on_levelled_selected_ulr",
              "weighting_model",
              "weighting_selected",
              null,
              "weighting_1_exposure_onlevel",
              "weighting_2_decay_ratio",
              "weighting_3_developed",
              "weighting_onlevel",
              null,
              "weighting_1_exposure_nominal",
              "weighting_nominal",
              null,
              "inflation_model_index",
              "rate_change_model_index",
              "rate_change_selected_index",
              "loss_ratio_model_index",
              "loss_ratio_selected_index"
            ]}
              maxListVisibleRows={8}
              filter="lob_visible_2"
              kb-interactive={true}
              transpose={false}
              freezeLeft={0} />
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.With context={{
                  "path": "selected_lob_totals_2",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 2"
                    titleBy="lookup_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "incurred_loss_ratio",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_selected_ulr",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "on_levelled_selected_ulr",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.With context={{
                "indexBy": "/cds/projections_lloyds/selected_lob_totals_2/row",
                "path": "summary_table",
                "type": "list"
              }}>
                <HX.Notes field="actuarial_notes"
                  title="Please note any rationale for selection below, and any use of overrides:" />
              </HX.With>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Selected LoB - 3"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_lloyds",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "lookup_lob_3",
              "show_all_yrs",
              null,
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "risk_code",
                "bp_class",
                "tracker_class",
                "projection_type.read_only_option",
                "ielr_approach",
                "composition"
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Summary IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_ielr_nominal",
                "model_ielr_onlevel",
                "model_ielr_ol_allyr",
                "model_ielr",
                "selected_ielr"
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Model Default Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_gn_ulr",
                "model_base_aqn",
                "model_acc_aqn",
                "model_adj_gn_ulr",
                null,
                "bp_cat_load",
                "model_final_gn_ulr"
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_gn_ulr",
                "selected_base_aqn",
                "selected_acc_aqn",
                "selected_adj_gn_ulr",
                null,
                "bp_cat_load",
                "selected_final_gn_ulr"
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_3",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_ratio",
              "latest_paid",
              "latest_incurred",
              "incurred_loss_ratio",
              "dev_patterns_gnpi",
              "dev_patterns_paid",
              "dev_patterns_incurred",
              "inflation_model",
              "rate_change_model",
              "rate_change_selected",
              "ultimate_gnpi",
              "ultimate_gnpi_ol_model",
              "ultimate_gnpi_ol_selected",
              "ultimate_cl_paid",
              "ultimate_cl_paid_ulr",
              "ultimate_cl_incurred",
              "ultimate_cl_incurred_ulr",
              "ultimate_ielr_model",
              "ultimate_ielr_model_ulr",
              "ultimate_ielr_selected",
              "ultimate_ielr_selected_ulr",
              "ultimate_bf_model_paid",
              "ultimate_bf_model_incurred",
              "ultimate_bf_selected_paid",
              "ultimate_bf_selected_incurred",
              "weighting_ielr",
              "method_paid",
              "method_incurred",
              "ultimate_model",
              "ultimate_model_ulr",
              "ultimate_selected",
              "ultimate_selected_ulr",
              "on_levelled_model_ulr",
              "on_levelled_selected_ulr",
              "weighting_model",
              "weighting_selected",
              null,
              "weighting_1_exposure_onlevel",
              "weighting_2_decay_ratio",
              "weighting_3_developed",
              "weighting_onlevel",
              null,
              "weighting_1_exposure_nominal",
              "weighting_nominal",
              null,
              "inflation_model_index",
              "rate_change_model_index",
              "rate_change_selected_index",
              "loss_ratio_model_index",
              "loss_ratio_selected_index"
            ]}
              maxListVisibleRows={8}
              filter="lob_visible_3"
              kb-interactive={true}
              transpose={false}
              freezeLeft={0} />
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.With context={{
                  "path": "selected_lob_totals_3",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 3"
                    titleBy="lookup_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "incurred_loss_ratio",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_selected_ulr",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "on_levelled_selected_ulr",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.With context={{
                "indexBy": "/cds/projections_lloyds/selected_lob_totals_3/row",
                "path": "summary_table",
                "type": "list"
              }}>
                <HX.Notes field="actuarial_notes"
                  title="Please note any rationale for selection below, and any use of overrides:" />
              </HX.With>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Beazley Projections"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_beazley_proj">
        <HX.Section title="Beazley Projection Summary">
          <HX.Notes field="cds/projections_own_experience/error_msg"
            shownBy="non_cds/own_experience/is_error_msg_shown" />
          <HX.Table title="Beazley Projection Summary"
            data={[
            "cds/projections_beazley/summary_table"
          ]}
            fields={[
            "risk_code",
            "selected_lob",
            "bp_class",
            "tracker_class",
            "composition",
            "model_acc_aqn",
            "projection_type",
            "cat_lr_source",
            "ielr_source",
            "ielr_approach",
            "selected_final_gn_ulr",
            "bp_cat",
            "bp_cat_load",
            "selected_ielr",
            "model_final_gn_ulr",
            "model_ielr",
            "checked",
            "comments"
          ]}
            maxListVisibleRows={10}
            filter="is_row_visible"
            kb-interactive={true}
            freezeLeft={1} />
        </HX.Section>
        <HX.Section title="Selected LoB - 1"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_beazley",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "lookup_lob_1",
              "show_all_yrs",
              null,
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "risk_code",
                "bp_class",
                "tracker_class",
                "projection_type",
                "ielr_approach",
                "composition"
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Summary IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_ielr_nominal",
                "model_ielr_onlevel",
                "model_ielr_ol_allyr",
                null,
                "lloyds_ielr",
                "ielr_source",
                null,
                "model_ielr",
                "selected_ielr"
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Model Default Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_gn_ulr",
                "model_base_aqn",
                "model_acc_aqn",
                "model_adj_gn_ulr",
                null,
                "bp_cat_load",
                "model_final_gn_ulr"
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_gn_ulr",
                "selected_base_aqn",
                "selected_acc_aqn",
                "selected_adj_gn_ulr",
                null,
                "bp_cat_load",
                "selected_final_gn_ulr"
              ]}
                filter="lob_visible_1"
                kb-interactive={true}
                transpose={true} />
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_1",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_ratio",
              "latest_paid",
              "latest_incurred",
              "incurred_loss_ratio",
              "dev_patterns_gnpi",
              "dev_patterns_paid",
              "dev_patterns_incurred",
              "inflation_model",
              "rate_change_model",
              "rate_change_selected",
              "ultimate_gnpi",
              "ultimate_gnpi_ol_model",
              "ultimate_gnpi_ol_selected",
              "ultimate_cl_paid",
              "ultimate_cl_paid_ulr",
              "ultimate_cl_incurred",
              "ultimate_cl_incurred_ulr",
              "ultimate_ielr_model",
              "ultimate_ielr_model_ulr",
              "ultimate_ielr_selected",
              "ultimate_ielr_selected_ulr",
              "ultimate_bf_model_paid",
              "ultimate_bf_model_incurred",
              "ultimate_bf_selected_paid",
              "ultimate_bf_selected_incurred",
              "weighting_ielr",
              "method_paid",
              "method_incurred",
              "ultimate_model",
              "ultimate_model_ulr",
              "ultimate_selected",
              "ultimate_selected_ulr",
              "on_levelled_model_ulr",
              "on_levelled_selected_ulr",
              "weighting_model",
              "weighting_selected",
              null,
              "weighting_1_exposure_onlevel",
              "weighting_2_decay_ratio",
              "weighting_3_developed",
              "weighting_onlevel",
              null,
              "weighting_1_exposure_nominal",
              "weighting_nominal",
              null,
              "inflation_model_index",
              "rate_change_model_index",
              "rate_change_selected_index",
              "loss_ratio_model_index",
              "loss_ratio_selected_index"
            ]}
              maxListVisibleRows={8}
              filter="lob_visible_1"
              kb-interactive={true}
              transpose={false}
              freezeLeft={0} />
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.With context={{
                  "path": "selected_lob_totals_1",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 1"
                    titleBy="lookup_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "incurred_loss_ratio",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_selected_ulr",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "on_levelled_selected_ulr",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.With context={{
                "indexBy": "/cds/projections_beazley/selected_lob_totals_1/row",
                "path": "summary_table",
                "type": "list"
              }}>
                <HX.Notes field="actuarial_notes"
                  title="Please note any rationale for selection below, and any use of overrides:" />
              </HX.With>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Selected LoB - 2"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_beazley",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "lookup_lob_2",
              "show_all_yrs",
              null,
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "risk_code",
                "bp_class",
                "tracker_class",
                "projection_type",
                "ielr_approach",
                "composition"
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Summary IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_ielr_nominal",
                "model_ielr_onlevel",
                "model_ielr_ol_allyr",
                null,
                "lloyds_ielr",
                "ielr_source",
                null,
                "model_ielr",
                "selected_ielr"
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Model Default Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_gn_ulr",
                "model_base_aqn",
                "model_acc_aqn",
                "model_adj_gn_ulr",
                null,
                "bp_cat_load",
                "model_final_gn_ulr"
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_gn_ulr",
                "selected_base_aqn",
                "selected_acc_aqn",
                "selected_adj_gn_ulr",
                null,
                "bp_cat_load",
                "selected_final_gn_ulr"
              ]}
                filter="lob_visible_2"
                kb-interactive={true}
                transpose={true} />
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_2",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_ratio",
              "latest_paid",
              "latest_incurred",
              "incurred_loss_ratio",
              "dev_patterns_gnpi",
              "dev_patterns_paid",
              "dev_patterns_incurred",
              "inflation_model",
              "rate_change_model",
              "rate_change_selected",
              "ultimate_gnpi",
              "ultimate_gnpi_ol_model",
              "ultimate_gnpi_ol_selected",
              "ultimate_cl_paid",
              "ultimate_cl_paid_ulr",
              "ultimate_cl_incurred",
              "ultimate_cl_incurred_ulr",
              "ultimate_ielr_model",
              "ultimate_ielr_model_ulr",
              "ultimate_ielr_selected",
              "ultimate_ielr_selected_ulr",
              "ultimate_bf_model_paid",
              "ultimate_bf_model_incurred",
              "ultimate_bf_selected_paid",
              "ultimate_bf_selected_incurred",
              "weighting_ielr",
              "method_paid",
              "method_incurred",
              "ultimate_model",
              "ultimate_model_ulr",
              "ultimate_selected",
              "ultimate_selected_ulr",
              "on_levelled_model_ulr",
              "on_levelled_selected_ulr",
              "weighting_model",
              "weighting_selected",
              null,
              "weighting_1_exposure_onlevel",
              "weighting_2_decay_ratio",
              "weighting_3_developed",
              "weighting_onlevel",
              null,
              "weighting_1_exposure_nominal",
              "weighting_nominal",
              null,
              "inflation_model_index",
              "rate_change_model_index",
              "rate_change_selected_index",
              "loss_ratio_model_index",
              "loss_ratio_selected_index"
            ]}
              maxListVisibleRows={8}
              filter="lob_visible_2"
              kb-interactive={true}
              transpose={false}
              freezeLeft={0} />
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.With context={{
                  "path": "selected_lob_totals_2",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 2"
                    titleBy="lookup_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "incurred_loss_ratio",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_selected_ulr",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "on_levelled_selected_ulr",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.With context={{
                "indexBy": "/cds/projections_beazley/selected_lob_totals_2/row",
                "path": "summary_table",
                "type": "list"
              }}>
                <HX.Notes field="actuarial_notes"
                  title="Please note any rationale for selection below, and any use of overrides:" />
              </HX.With>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Selected LoB - 3"
          defaultCollapsed={true}>
          <HX.With context={{
            "path": "cds/projections_beazley",
            "type": "struct"
          }}>
            <HX.Collection title="Visual Settings"
              fields={[
              "lookup_lob_3",
              "show_all_yrs",
              null,
              null
            ]}
              horizontal={true} />
  
            <HX.Pane flow="right">
              <HX.Table title="LOB Settings"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_lob",
                "risk_code",
                "bp_class",
                "tracker_class",
                "projection_type",
                "ielr_approach",
                "composition"
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Summary IELRs"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_ielr_nominal",
                "model_ielr_onlevel",
                "model_ielr_ol_allyr",
                null,
                "lloyds_ielr",
                "ielr_source",
                null,
                "model_ielr",
                "selected_ielr"
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Model Default Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "model_gn_ulr",
                "model_base_aqn",
                "model_acc_aqn",
                "model_adj_gn_ulr",
                null,
                "bp_cat_load",
                "model_final_gn_ulr"
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
              <HX.Table title="Selected Loss Ratios"
                data={[
                {
                  "datum": "summary_table",
                  "maxWidth": 200
                }
              ]}
                fields={[
                "selected_gn_ulr",
                "selected_base_aqn",
                "selected_acc_aqn",
                "selected_adj_gn_ulr",
                null,
                "bp_cat_load",
                "selected_final_gn_ulr"
              ]}
                filter="lob_visible_3"
                kb-interactive={true}
                transpose={true} />
            </HX.Pane>
            <HX.Table title="Analysis Detail"
              data={[
              {
                "datum": "detail_table",
                "elementLabelBy": "yoa"
              },
              null,
              {
                "datum": "selected_lob_totals_3",
                "elementLabelBy": "yoa"
              }
            ]}
              fields={[
              "latest_gpi",
              "latest_gnpi",
              "acquisition_ratio",
              "latest_paid",
              "latest_incurred",
              "incurred_loss_ratio",
              "dev_patterns_gnpi",
              "dev_patterns_paid",
              "dev_patterns_incurred",
              "inflation_model",
              "rate_change_model",
              "rate_change_selected",
              "ultimate_gnpi",
              "ultimate_gnpi_ol_model",
              "ultimate_gnpi_ol_selected",
              "ultimate_cl_paid",
              "ultimate_cl_paid_ulr",
              "ultimate_cl_incurred",
              "ultimate_cl_incurred_ulr",
              "ultimate_ielr_model",
              "ultimate_ielr_model_ulr",
              "ultimate_ielr_selected",
              "ultimate_ielr_selected_ulr",
              "ultimate_bf_model_paid",
              "ultimate_bf_model_incurred",
              "ultimate_bf_selected_paid",
              "ultimate_bf_selected_incurred",
              "weighting_ielr",
              "method_paid",
              "method_incurred",
              "ultimate_model",
              "ultimate_model_ulr",
              "ultimate_selected",
              "ultimate_selected_ulr",
              "on_levelled_model_ulr",
              "on_levelled_selected_ulr",
              "weighting_model",
              "weighting_selected",
              null,
              "weighting_1_exposure_onlevel",
              "weighting_2_decay_ratio",
              "weighting_3_developed",
              "weighting_onlevel",
              null,
              "weighting_1_exposure_nominal",
              "weighting_nominal",
              null,
              "inflation_model_index",
              "rate_change_model_index",
              "rate_change_selected_index",
              "loss_ratio_model_index",
              "loss_ratio_selected_index"
            ]}
              maxListVisibleRows={8}
              filter="lob_visible_3"
              kb-interactive={true}
              transpose={false}
              freezeLeft={0} />
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.With context={{
                  "path": "selected_lob_totals_3",
                  "type": "struct"
                }}>
                  <CustomComponent title="Selected Lob - 3"
                    titleBy="lookup_lob"
                    data={[
                    {
                      "labelBy": "yoa",
                      "list": "chart_data"
                    }
                  ]}
                    traces={[
                    {
                      "color": "#DC199B",
                      "field": "incurred_loss_ratio",
                      "label": "Total GN ILR %"
                    },
                    {
                      "color": "#4B0050",
                      "field": "ultimate_selected_ulr",
                      "label": "Total GN ULR %"
                    },
                    {
                      "color": "#C8C3CD",
                      "field": "on_levelled_selected_ulr",
                      "label": "On-levelled Total GN ULR %"
                    }
                  ]}
                    series={[
                    {
                      "points": [
                        {
                          "list": "chart_data",
                          "x": "yoa",
                          "y": "pricing_basis"
                        }
                      ],
                      "seriesColor": "#4FADC7",
                      "seriesLabel": "Pricing Basis %",
                      "seriesLineType": "dash",
                      "seriesMode": "lines"
                    }
                  ]}
                    xAxisTickAngle={-45}
                    xAxisLabel="Year of Account"
                    yAxisLabel="Total GNLR (%)"
                    barMode="group"
                    gapBetweenBarsSize={0.3}
                    width={800}
                    height={500}
                    y2SeparateAxis={false} />
                </HX.With>
              </HX.Pane>
              <HX.With context={{
                "indexBy": "/cds/projections_beazley/selected_lob_totals_3/row",
                "path": "summary_table",
                "type": "list"
              }}>
                <HX.Notes field="actuarial_notes"
                  title="Please note any rationale for selection below, and any use of overrides:" />
              </HX.With>
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="BP Projections"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_bp_proj">
        <HX.Section title="Business Plan Pricing"
          collapsible={false}>
          <HX.Section title="BP Projections by Selected LoB">
            <HX.Table data={[
              "cds/bp_projections/bp_summary_by_lob"
            ]}
              fields={[
              "tracker_class",
              "selected_lob",
              "bp_class",
              "risk_code",
              "composition",
              "acc_aquisition_costs",
              null,
              "attr_base_gn_ulr",
              "attr_inflation_1_year",
              "attr_rate_change",
              "attr_rarc_margin",
              "attr_portfolio_change",
              "cat_base_gn_ulr",
              "cat_inflation_1_year",
              "cat_rate_change",
              "cat_rarc_margin",
              "cat_climate_change",
              "cat_nmp_general",
              "cat_nmp_all_other",
              "rate_change_override",
              "selected_attr_gn_ulr",
              "selected_cat_gn_ulr",
              "total_gn_ulr",
              "bp_acquisition_costs",
              "adj_attr_gn_ulr",
              "adj_cat_gn_ulr",
              "adj_total_gn_ulr"
            ]}
              filter="is_row_visible"
              kb-interactive={true} />
          </HX.Section>
          <HX.Section title="BP Projections by Selected LoB and Risk Code">
            <HX.Table data={[
              "cds/bp_projections/bp_details"
            ]}
              fields={[
              "tracker_class",
              "selected_lob",
              "bp_class",
              "risk_code",
              "composition",
              "acc_aquisition_costs",
              null,
              "attr_base_gn_ulr",
              "attr_inflation_1_year",
              "attr_rate_change",
              "attr_rarc_margin",
              "attr_portfolio_change",
              "cat_base_gn_ulr",
              "cat_inflation_1_year",
              "cat_rate_change",
              "cat_rarc_margin",
              "cat_climate_change",
              "cat_nmp_general",
              "cat_nmp_all_other",
              "rate_change_override",
              "selected_attr_gn_ulr",
              "selected_cat_gn_ulr",
              "total_gn_ulr",
              "bp_acquisition_costs",
              "adj_attr_gn_ulr",
              "adj_cat_gn_ulr",
              "adj_total_gn_ulr"
            ]}
              filter="is_row_visible"
              kb-interactive={true} />
          </HX.Section>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Anti-selection"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_anti_select">
        <HX.Section title="Anti-Selection Matrix">
          <HX.Collection fields={[
            "/cds/anti_selection/charge_required"
          ]}
            syncColumnWidthsKey="table_1" />
          <HX.Table syncColumnWidthsKey="table_1"
            with="cds/anti_selection/matrix"
            kb-interactive={true}
            data={[
            "baseline",
            "competing_portfolio",
            "delegation_scope",
            "quantity_quality",
            "cover_holder_alignment",
            "participation",
            "overall_selected"
          ]}
            fields={[
            "selection",
            "guideline_min",
            "guideline_max",
            "suggested",
            "final_selected",
            "comments"
          ]} />
        </HX.Section>
        <HX.Section title="Applied Anti-Selection Charge"
          shownBy="non_cds/risk_information/not_follow_main_syndicate">
          <HX.Table with="cds/anti_selection/applied_charge"
            kb-interactive={true}
            data={[
            "model_weighting",
            null,
            "table"
          ]}
            fields={[
            "selected_lob",
            "own_performance",
            "lloyds_performance",
            "beazley_performance",
            "business_plan",
            "case_pricing",
            "pricing_2623_623",
            "anti_selection_charge"
          ]}
            filter="is_row_visible" />
        </HX.Section>
        <HX.Section title="Anti-Selection Charge - Selection Details">
          <HX.Notes field="cds/anti_selection/matrix/overall_selected/guidelines" />
          <HX.Notes field="cds/anti_selection/matrix/baseline/guidelines" />
          <HX.Notes field="cds/anti_selection/matrix/competing_portfolio/guidelines" />
          <HX.Notes field="cds/anti_selection/matrix/delegation_scope/guidelines" />
          <HX.Notes field="cds/anti_selection/matrix/quantity_quality/guidelines" />
          <HX.Notes field="cds/anti_selection/matrix/cover_holder_alignment/guidelines" />
          <HX.Notes field="cds/anti_selection/matrix/participation/guidelines" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Uncertainty"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_uncertainty">
        <HX.Section title="Uncertainty Matrix">
          <HX.Collection fields={[
            "/cds/uncertainty/charge_required"
          ]}
            syncColumnWidthsKey="table_1" />
          <HX.Table syncColumnWidthsKey="table_1"
            with="cds/uncertainty/matrix"
            kb-interactive={true}
            data={[
            "quantity",
            "quality",
            "new_or_existing_facility",
            "perf_volatility",
            "reliance_on_ext_modelling",
            "add_subjectivity",
            null,
            "perf_discount",
            "overall_selected"
          ]}
            fields={[
            "selection",
            "guideline_min",
            "guideline_max",
            "suggested",
            "final_selected",
            "comments"
          ]} />
        </HX.Section>
        <HX.Section title="Applied Uncertainty Charge"
          shownBy="non_cds/risk_information/not_follow_main_syndicate">
          <HX.Table kb-interactive={true}
            with="cds/uncertainty/applied_charge"
            data={[
            "model_weighting",
            null,
            "table"
          ]}
            fields={[
            "selected_lob",
            "own_performance",
            "lloyds_performance",
            "beazley_performance",
            "business_plan",
            "case_pricing",
            "pricing_2623_623",
            "load"
          ]}
            filter="is_row_visible" />
        </HX.Section>
        <HX.Section title="Uncertainty Load - Selection Details/guidelines">
          <HX.Notes field="cds/uncertainty/matrix/overall_selected/guidelines" />
          <HX.Notes field="cds/uncertainty/matrix/quantity/guidelines" />
          <HX.Notes field="cds/uncertainty/matrix/quality/guidelines" />
          <HX.Notes field="cds/uncertainty/matrix/new_or_existing_facility/guidelines" />
          <HX.Notes field="cds/uncertainty/matrix/perf_volatility/guidelines" />
          <HX.Notes field="cds/uncertainty/matrix/reliance_on_ext_modelling/guidelines" />
          <HX.Notes field="cds/uncertainty/matrix/add_subjectivity/guidelines" />
          <HX.Notes field="cds/uncertainty/matrix/perf_discount/guidelines" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="PC"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_pc">
        <HX.Section title="PC Control"
          collapsible={false}>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Button title="Calculate Profit commission"
                task="calculate_profit_commission_task" />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Collection with="cds/pc/pc_control"
            numCols={6}
            fields={[
            "is_pc_interlocking",
            "allow_for_correlation",
            "show_details",
            null,
            null,
            null,
            "dcf_opt",
            {
              "field": "dcf_amount",
              "shownBy": "/non_cds/pc/pc_control/is_amount"
            },
            {
              "field": "dcf_amount_basis",
              "shownBy": "/non_cds/pc/pc_control/is_amount"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_amount"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_amount"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_amount"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_none"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_none"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_none"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_none"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_none"
            },
            {
              "field": "dcf_exper_num_yrs",
              "shownBy": "/non_cds/pc/pc_control/is_experience"
            },
            {
              "field": "dcf_exper_exc_yrs",
              "shownBy": "/non_cds/pc/pc_control/is_experience"
            },
            {
              "field": "dcf_exper_basis",
              "shownBy": "/non_cds/pc/pc_control/is_experience"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_experience"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_experience"
            },
            "ul_binders_pc",
            {
              "field": "ul_pc_as_expense",
              "shownBy": "/non_cds/pc/pc_control/is_pc_on_binders"
            },
            {
              "field": "ul_pc_as_expense_pct",
              "shownBy": "/non_cds/pc/pc_control/is_pc_on_binders"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_pc_on_binders"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_pc_on_binders"
            },
            {
              "field": null,
              "shownBy": "/non_cds/pc/pc_control/is_pc_on_binders"
            },
            "no_of_simulations"
          ]} />
        </HX.Section>
        <HX.Section title="PC Structure">
          <HX.Table syncColumnWidthsKey="table_1"
            transpose={true}
            kb-interactive={true}
            filter="is_row_visible"
            data={[
            {
              "datum": "cds/pc/pc_structure/table",
              "maxWidth": 300
            }
          ]}
            fields={[
            "selected_lob",
            "pc_type",
            "uw_expense",
            "expense_basis",
            "std_pc_percent"
          ]} />
          <HX.Selector with="cds/pc/pc_structure"
            title="Select the Line of Business to build a sliding scale for"
            data={[
            "table_sliding_scale"
          ]}
            dropdown="selected_lob">
            <HX.Table syncColumnWidthsKey="table_1"
              kb-interactive={true}
              data={[
              {
                "datum": "scale"
              }
            ]}
              fields={[
              "gn_ulr_less_than",
              "pc"
            ]} />
          </HX.Selector>
          <HX.Table shownBy="non_cds/pc/pc_structure/show_for_sliding_scale"
            title="For Sliding Scale"
            kb-interactive={true}
            data={[
            "cds/pc/pc_structure/for_sliding_scale"
          ]}
            fields={[
            {
              "field": "selected_lob_1/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_1_shown",
              "width": 200
            },
            {
              "field": "selected_lob_1/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_1_shown",
              "width": 100
            },
            {
              "field": "selected_lob_2/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_2_shown",
              "width": 200
            },
            {
              "field": "selected_lob_2/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_2_shown",
              "width": 100
            },
            {
              "field": "selected_lob_3/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_3_shown",
              "width": 200
            },
            {
              "field": "selected_lob_3/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_3_shown",
              "width": 100
            },
            {
              "field": "selected_lob_4/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_4_shown",
              "width": 200
            },
            {
              "field": "selected_lob_4/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_4_shown",
              "width": 100
            },
            {
              "field": "selected_lob_5/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_5_shown",
              "width": 200
            },
            {
              "field": "selected_lob_5/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_5_shown",
              "width": 100
            },
            {
              "field": "selected_lob_6/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_6_shown",
              "width": 200
            },
            {
              "field": "selected_lob_6/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_6_shown",
              "width": 100
            },
            {
              "field": "selected_lob_7/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_7_shown",
              "width": 200
            },
            {
              "field": "selected_lob_7/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_7_shown",
              "width": 100
            },
            {
              "field": "selected_lob_8/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_8_shown",
              "width": 200
            },
            {
              "field": "selected_lob_8/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_8_shown",
              "width": 100
            },
            {
              "field": "selected_lob_9/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_9_shown",
              "width": 200
            },
            {
              "field": "selected_lob_9/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_9_shown",
              "width": 100
            },
            {
              "field": "selected_lob_10/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_10_shown",
              "width": 200
            },
            {
              "field": "selected_lob_10/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_10_shown",
              "width": 100
            },
            {
              "field": "selected_lob_11/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_11_shown",
              "width": 200
            },
            {
              "field": "selected_lob_11/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_11_shown",
              "width": 100
            },
            {
              "field": "selected_lob_12/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_12_shown",
              "width": 200
            },
            {
              "field": "selected_lob_12/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_12_shown",
              "width": 100
            },
            {
              "field": "selected_lob_13/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_13_shown",
              "width": 200
            },
            {
              "field": "selected_lob_13/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_13_shown",
              "width": 100
            },
            {
              "field": "selected_lob_14/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_14_shown",
              "width": 200
            },
            {
              "field": "selected_lob_14/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_14_shown",
              "width": 100
            },
            {
              "field": "selected_lob_15/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_15_shown",
              "width": 200
            },
            {
              "field": "selected_lob_15/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_15_shown",
              "width": 100
            },
            {
              "field": "selected_lob_16/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_16_shown",
              "width": 200
            },
            {
              "field": "selected_lob_16/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_16_shown",
              "width": 100
            },
            {
              "field": "selected_lob_17/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_17_shown",
              "width": 200
            },
            {
              "field": "selected_lob_17/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_17_shown",
              "width": 100
            },
            {
              "field": "selected_lob_18/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_18_shown",
              "width": 200
            },
            {
              "field": "selected_lob_18/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_18_shown",
              "width": 100
            },
            {
              "field": "selected_lob_19/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_19_shown",
              "width": 200
            },
            {
              "field": "selected_lob_19/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_19_shown",
              "width": 100
            },
            {
              "field": "selected_lob_20/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_20_shown",
              "width": 200
            },
            {
              "field": "selected_lob_20/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_20_shown",
              "width": 100
            },
            {
              "field": "selected_lob_21/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_21_shown",
              "width": 200
            },
            {
              "field": "selected_lob_21/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_21_shown",
              "width": 100
            },
            {
              "field": "selected_lob_22/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_22_shown",
              "width": 200
            },
            {
              "field": "selected_lob_22/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_22_shown",
              "width": 100
            },
            {
              "field": "selected_lob_23/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_23_shown",
              "width": 200
            },
            {
              "field": "selected_lob_23/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_23_shown",
              "width": 100
            },
            {
              "field": "selected_lob_24/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_24_shown",
              "width": 200
            },
            {
              "field": "selected_lob_24/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_24_shown",
              "width": 100
            },
            {
              "field": "selected_lob_25/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_25_shown",
              "width": 200
            },
            {
              "field": "selected_lob_25/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_25_shown",
              "width": 100
            },
            {
              "field": "selected_lob_26/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_26_shown",
              "width": 200
            },
            {
              "field": "selected_lob_26/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_26_shown",
              "width": 100
            },
            {
              "field": "selected_lob_27/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_27_shown",
              "width": 200
            },
            {
              "field": "selected_lob_27/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_27_shown",
              "width": 100
            },
            {
              "field": "selected_lob_28/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_28_shown",
              "width": 200
            },
            {
              "field": "selected_lob_28/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_28_shown",
              "width": 100
            },
            {
              "field": "selected_lob_29/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_29_shown",
              "width": 200
            },
            {
              "field": "selected_lob_29/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_29_shown",
              "width": 100
            },
            {
              "field": "selected_lob_30/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_30_shown",
              "width": 200
            },
            {
              "field": "selected_lob_30/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_30_shown",
              "width": 100
            },
            {
              "field": "selected_lob_31/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_31_shown",
              "width": 200
            },
            {
              "field": "selected_lob_31/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_31_shown",
              "width": 100
            },
            {
              "field": "selected_lob_32/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_32_shown",
              "width": 200
            },
            {
              "field": "selected_lob_32/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_32_shown",
              "width": 100
            },
            {
              "field": "selected_lob_33/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_33_shown",
              "width": 200
            },
            {
              "field": "selected_lob_33/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_33_shown",
              "width": 100
            },
            {
              "field": "selected_lob_34/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_34_shown",
              "width": 200
            },
            {
              "field": "selected_lob_34/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_34_shown",
              "width": 100
            },
            {
              "field": "selected_lob_35/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_35_shown",
              "width": 200
            },
            {
              "field": "selected_lob_35/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_35_shown",
              "width": 100
            },
            {
              "field": "selected_lob_36/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_36_shown",
              "width": 200
            },
            {
              "field": "selected_lob_36/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_36_shown",
              "width": 100
            },
            {
              "field": "selected_lob_37/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_37_shown",
              "width": 200
            },
            {
              "field": "selected_lob_37/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_37_shown",
              "width": 100
            },
            {
              "field": "selected_lob_38/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_38_shown",
              "width": 200
            },
            {
              "field": "selected_lob_38/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_38_shown",
              "width": 100
            },
            {
              "field": "selected_lob_39/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_39_shown",
              "width": 200
            },
            {
              "field": "selected_lob_39/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_39_shown",
              "width": 100
            },
            {
              "field": "selected_lob_40/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_40_shown",
              "width": 200
            },
            {
              "field": "selected_lob_40/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_40_shown",
              "width": 100
            },
            {
              "field": "selected_lob_41/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_41_shown",
              "width": 200
            },
            {
              "field": "selected_lob_41/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_41_shown",
              "width": 100
            },
            {
              "field": "selected_lob_42/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_42_shown",
              "width": 200
            },
            {
              "field": "selected_lob_42/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_42_shown",
              "width": 100
            },
            {
              "field": "selected_lob_43/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_43_shown",
              "width": 200
            },
            {
              "field": "selected_lob_43/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_43_shown",
              "width": 100
            },
            {
              "field": "selected_lob_44/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_44_shown",
              "width": 200
            },
            {
              "field": "selected_lob_44/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_44_shown",
              "width": 100
            },
            {
              "field": "selected_lob_45/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_45_shown",
              "width": 200
            },
            {
              "field": "selected_lob_45/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_45_shown",
              "width": 100
            },
            {
              "field": "selected_lob_46/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_46_shown",
              "width": 200
            },
            {
              "field": "selected_lob_46/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_46_shown",
              "width": 100
            },
            {
              "field": "selected_lob_47/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_47_shown",
              "width": 200
            },
            {
              "field": "selected_lob_47/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_47_shown",
              "width": 100
            },
            {
              "field": "selected_lob_48/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_48_shown",
              "width": 200
            },
            {
              "field": "selected_lob_48/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_48_shown",
              "width": 100
            },
            {
              "field": "selected_lob_49/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_49_shown",
              "width": 200
            },
            {
              "field": "selected_lob_49/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_49_shown",
              "width": 100
            },
            {
              "field": "selected_lob_50/gn_ulr_less_than",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_50_shown",
              "width": 200
            },
            {
              "field": "selected_lob_50/pc",
              "shownBy": "non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_50_shown",
              "width": 100
            }
          ]} />
        </HX.Section>
        <HX.Section title="Correlation Matrix"
          shownBy="cds/pc/pc_control/allow_for_correlation"
          defaultCollapsed={true}>
          <CustomComponent title="Calculated Correlation Matrix"
            parentList="cds/pc/cm_calc"
            parentListName="NotUsed"
            childList="cm_col"
            field="coeff" />
          <HX.Selector with="cds/pc"
            title="Select the Line of Business to add correlation for"
            data={[
            "cm_ovd"
          ]}
            dropdown="selected_lob">
            <HX.Table kb-interactive={true}
              data={[
              {
                "datum": "cm_col",
                "maxWidth": 150
              }
            ]}
              fields={[
              "coeff"
            ]}
              transpose={true} />
          </HX.Selector>
          <HX.Selector with="cds/pc"
            title="Select the Line of Business to check correlation for"
            data={[
            "cm_sel"
          ]}
            dropdown="selected_lob">
            <HX.Table kb-interactive={true}
              data={[
              {
                "datum": "cm_col",
                "maxWidth": 150
              }
            ]}
              fields={[
              "coeff"
            ]}
              transpose={true} />
          </HX.Selector>
          <CustomComponent parentList="cds/pc/cm_sel"
            title="Selected Correlation Matrix"
            parentListName="xxx"
            childList="cm_col"
            field="coeff" />
        </HX.Section>
        <HX.Section title="PC Calculations"
          shownBy="cds/pc/pc_control/show_details"
          defaultCollapsed={true}>
          <HX.Table syncColumnWidthsKey="table_1"
            shownBy="cds/pc/pc_control/show_details"
            transpose={true}
            kb-interactive={true}
            filter="is_row_visible"
            data={[
            {
              "datum": "cds/pc/pc_calculations/details",
              "maxWidth": 300
            },
            null,
            {
              "datum": "cds/pc/pc_calculations/summary",
              "maxWidth": 300
            }
          ]}
            fields={[
            "selected_lob",
            null,
            "gwp_5623",
            "deductions",
            "nwp_5623",
            null,
            "bm_class_auto",
            "bm_class_override",
            "bm_class_applied",
            "cov_basis_attr",
            "cov_basis_large",
            "cov_basis_cat",
            "attr_gg_ulr",
            "large_gg_ulr",
            "cat_gg_ulr",
            "total_gg_ulr",
            null,
            "attr_cov",
            "large_cov",
            "cat_cov",
            null,
            "attr_el",
            "large_el",
            "cat_non_weather_el",
            "cat_weather_el",
            null,
            "attr_sd",
            "large_sd",
            "cat_non_weather_sd",
            "cat_weather_sd"
          ]} />
        </HX.Section>
        <HX.Section title="Profit Commission on Contract">
          <HX.Table syncColumnWidthsKey="table_1"
            transpose={true}
            kb-interactive={true}
            filter="is_row_visible"
            data={[
            {
              "datum": "cds/pc/profit_commission/details",
              "maxWidth": 300
            },
            null,
            {
              "datum": "cds/pc/profit_commission/summary",
              "maxWidth": 300
            }
          ]}
            fields={[
            "selected_lob",
            {
              "field": "gwp_5623",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            {
              "field": "deductions",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            {
              "field": "nwp_5623",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            null,
            {
              "field": "total_losses",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            {
              "field": "uw_expense",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            {
              "field": "dcf",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            {
              "field": "expected_pl",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            {
              "field": "pc_on_binders",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            {
              "field": "pc_on_contract",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            {
              "field": "nwp_after_pc",
              "shownBy": "cds/pc/pc_control/show_details"
            },
            null,
            "total_gn_ulr_pre",
            "total_gn_ulr_post",
            "pc_impact"
          ]} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_rat_sum_std">
        <HX.Section title="Rating Summary"
          collapsible={false}>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Button title="Calculate Profit commission"
                task="calculate_profit_commission_task"
                shownBy="cds/risk_information/is_profit_comission" />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Section title="Model GN ULR">
            <HX.Table title="Projected GN ULRs"
              data={[
              {
                "datum": "table",
                "elementLabelBy": "selected_lob",
                "maxWidth": 200
              },
              null,
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "tracker_class",
              "gn_premium",
              "portfolio_percent",
              "total_deductions",
              "own_exp_gn_ulr",
              "lloyds_gn_ulr",
              "beazley_gn_ulr",
              "bp_gn_ulr",
              "case_pricing",
              {
                "field": "own_exp_gn_ulr_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "lloyds_gn_ulr_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "beazley_gn_ulr_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "bp_gn_ulr_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "case_pricing_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              }
            ]}
              with="cds/rating_summary/model_gn_ulr/projected_gn_ulr"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true}
              filter="is_row_visible" />
            <HX.Table title="Model Weights"
              data={[
              {
                "datum": "table",
                "elementLabelBy": "selected_lob",
                "maxWidth": 200
              },
              null,
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "own_experience",
              "lloyds_proj",
              "beazley_proj",
              "bp_proj",
              "case_pricing",
              "weighting_check",
              {
                "field": "own_experience_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "lloyds_proj_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "beazley_proj_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "bp_proj_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "case_pricing_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              "model_estimate",
              {
                "field": "model_estimate_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              }
            ]}
              with="cds/rating_summary/model_gn_ulr/model_weights"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true}
              filter="is_row_visible" />
          </HX.Section>
          <HX.Section title="CAT Loadings">
            <HX.Collection fields={[
              "cds/rating_summary/cat_loadings/show_details",
              null,
              null,
              null,
              null,
              null
            ]}
              horizontal={true} />
            <HX.Table title="CAT Allocation"
              data={[
              {
                "datum": "cat_allocation",
                "elementLabelBy": "selected_lob",
                "maxWidth": 200
              },
              null,
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              {
                "field": "attr_and_lrg_exp",
                "shownBy": "show_details"
              },
              {
                "field": "cat_exp",
                "shownBy": "show_details"
              },
              {
                "field": "attr_and_lrg_bp",
                "shownBy": "show_details"
              },
              {
                "field": "cat_bp",
                "shownBy": "show_details"
              },
              "attr_and_lrg",
              "cat",
              "climate_change_load",
              "nmp_load_general",
              "nmp_load_weather"
            ]}
              with="cds/rating_summary/cat_loadings"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true}
              filter="is_row_visible" />
          </HX.Section>
          <HX.Section title="Additional Loadings">
            <HX.Table title="Additional Pricing Loads"
              data={[
              {
                "datum": "additional_pricing_loads",
                "elementLabelBy": "selected_lob",
                "maxWidth": 200
              },
              null,
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "anti_selection_charge",
              "uncertainty_charge",
              "additional_charge"
            ]}
              with="cds/rating_summary/additional_loadings"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true}
              filter="is_row_visible" />
          </HX.Section>
          <HX.Section title="Pricing Adequacy Metrics">
            <HX.Table title="Pricing Adequacy - (Pre Anti-Selection & Uncertainty)"
              data={[
              {
                "datum": "table",
                "elementLabelBy": "selected_lob",
                "maxWidth": 200
              },
              null,
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "best_estimate_pre_pc_adj",
              "pc_impact",
              "best_estimate",
              "bpi",
              "tpi",
              "roc"
            ]}
              with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_pre_adj"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true}
              filter="is_row_visible" />
            <HX.Table title="Pricing Adequacy - (Actuarial Basis)"
              data={[
              {
                "datum": "table",
                "elementLabelBy": "selected_lob",
                "maxWidth": 200
              },
              null,
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "best_estimate_pre_pc_adj",
              "pc_impact",
              "best_estimate",
              "bpi",
              "tpi",
              "roc"
            ]}
              with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_actuarial_basis"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true}
              filter="is_row_visible" />
            <HX.Table title="Pricing Adequacy - (Final Pricing Basis)"
              data={[
              {
                "datum": "table",
                "elementLabelBy": "selected_lob",
                "maxWidth": 200
              },
              null,
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "uw_adj",
              "best_estimate_gn",
              "best_estimate_gg",
              "bpi",
              "tpi",
              "roc",
              {
                "field": "best_estimate_gn_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "best_estimate_gg_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "bpi_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "tpi_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "roc_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              }
            ]}
              with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_final_pricing"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true}
              filter="is_row_visible" />
          </HX.Section>
          <HX.Section title="Catastrophe ULR Summary">
            <HX.Table data={[
              {
                "datum": "details",
                "elementLabelBy": "selected_lob",
                "maxWidth": 200
              },
              null,
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "gn_cat_ulr_excl_loads",
              "gn_cat_ulr_inc_loads"
            ]}
              with="cds/rating_summary/cat_ulr_summary"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true}
              filter="is_row_visible" />
          </HX.Section>
          <HX.Section title="Technical Premium Build Up">
            <HX.Collection fields={[
              {
                "field": "cds/rating_summary/technical_premium_build_up/tpi_year.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "cds/rating_summary/technical_premium_build_up/tpi_year",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              null,
              null,
              null,
              null,
              null
            ]}
              horizontal={true} />
            <HX.Table title="Technical Premium"
              data={[
              {
                "datum": "technical_premium",
                "elementLabelBy": "selected_lob",
                "maxWidth": 200
              },
              null,
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "el_pre_adj",
              "el_actuarial",
              "el_final",
              "net_expense",
              "inv_income",
              "ri_premium",
              "ri_recoveries",
              "capital_required",
              "target_roc",
              "tp_pre_adj",
              "tp_actuarial",
              "tp_final",
              "gg_tp_final",
              "gg_bm_final"
            ]}
              with="cds/rating_summary/technical_premium_build_up"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true}
              filter="is_row_visible" />
          </HX.Section>
          <HX.Section title="Trifocus Summary">
            <HX.Table data={[
              "model_estimate",
              "be_before_loads",
              "anti_selection",
              "uncertainty",
              "additional_charge",
              "pc_impact",
              "be_after_pc",
              "uw_adj",
              "be_post_uw",
              "bpi",
              "tpi",
              "roc"
            ]}
              fields={[
              {
                "field": "tracker_property",
                "shownBy": "show_tracker_property",
                "width": 200
              },
              {
                "field": "tracker_sr",
                "shownBy": "show_tracker_sr",
                "width": 200
              },
              {
                "field": "tracker_marine",
                "shownBy": "show_tracker_marine",
                "width": 200
              },
              {
                "field": "tracker_pac",
                "shownBy": "show_tracker_pac",
                "width": 200
              },
              {
                "field": "tracker_cyber",
                "shownBy": "show_tracker_cyber",
                "width": 200
              },
              null,
              {
                "field": "summary",
                "width": 200
              }
            ]}
              with="cds/rating_summary/trifocus_summary"
              kb-interactive={true} />
          </HX.Section>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_rat_sum_bbt">
        <HX.Section title="Rating Summary"
          collapsible={false}>
          <HX.Pane flow="right">
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Section title="623 / 2623 Pricing Outputs">
            <HX.Table title="623 / 2623 Benchmarking"
              data={[
              {
                "datum": "pricing_outputs",
                "maxWidth": 300
              }
            ]}
              fields={[
              "bbt_gn_ulr",
              "bbt_gn_cat_ulr",
              "attr_and_large",
              "cat",
              "deductions_623_2623",
              "deductions_5623",
              {
                "field": "bbt_pc",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              "bbt_class",
              "tracker_class",
              "gn_ulr_5623",
              {
                "field": "gn_ulr_5623_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              "afb_api",
              "line_size"
            ]}
              with="cds/rating_summary"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
          <HX.Section title="Additional Loadings">
            <HX.Table title="Additional Pricing Loads"
              data={[
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "anti_selection_charge",
              "uncertainty_charge",
              "additional_charge_bbt"
            ]}
              with="cds/rating_summary/additional_loadings"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
          <HX.Section title="Pricing Adequacy Metrics">
            <HX.Table title="Pricing Adequacy - (Pre Anti-Selection & Uncertainty)"
              data={[
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "best_estimate_pre_pc_adj",
              "pc_impact",
              "best_estimate",
              "bpi",
              "tpi",
              "roc"
            ]}
              with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_pre_adj"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true} />
            <HX.Table title="Pricing Adequacy - (Actuarial Basis)"
              data={[
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "best_estimate_pre_pc_adj",
              "pc_impact",
              "best_estimate",
              "bpi",
              "tpi",
              "roc"
            ]}
              with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_actuarial_basis"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true} />
            <HX.Table title="Pricing Adequacy - (Final Pricing Basis)"
              data={[
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "uw_adj_bbt",
              "best_estimate_gn",
              "best_estimate_gg",
              "bpi",
              "tpi",
              "roc",
              {
                "field": "best_estimate_gn_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "best_estimate_gg_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "bpi_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "tpi_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              },
              {
                "field": "roc_ly",
                "shownBy": "/cds/standard_fields/is_renewal"
              }
            ]}
              with="cds/rating_summary/pricing_adequacy_metrics/pricing_adequacy_final_pricing"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
          <HX.Section title="Catastrophe ULR Summary">
            <HX.Table data={[
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "gn_cat_ulr_excl_loads",
              "gn_cat_ulr_inc_loads"
            ]}
              with="cds/rating_summary/cat_ulr_summary"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
          <HX.Section title="Technical Premium Build Up">
            <HX.Collection fields={[
              {
                "field": "cds/rating_summary/technical_premium_build_up/tpi_year.read_only_option",
                "shownBy": "/non_cds/risk_information/is_underwriter"
              },
              {
                "field": "cds/rating_summary/technical_premium_build_up/tpi_year",
                "shownBy": "/non_cds/risk_information/is_actuarial"
              },
              null,
              null,
              null,
              null,
              null
            ]}
              horizontal={true} />
            <HX.Table title="Technical Premium"
              data={[
              {
                "datum": "summary",
                "maxWidth": 300
              }
            ]}
              fields={[
              "el_pre_adj",
              "el_actuarial",
              "el_final",
              "net_expense",
              "inv_income",
              "ri_premium",
              "ri_recoveries",
              "capital_required",
              "target_roc",
              "tp_pre_adj",
              "tp_actuarial",
              "tp_final",
              "gg_tp_final",
              "gg_bm_final"
            ]}
              with="cds/rating_summary/technical_premium_build_up"
              syncColumnWidthsKey="table_1"
              kb-interactive={true}
              transpose={true} />
          </HX.Section>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={false}
        shownBy="model_state/show_rat_sum_case">
        <HX.Section title="Summary">
          <HX.Collection title="Risk Details"
            numCols={4}
            fields={[
            "cds/risk_information/deal_status",
            "cds/standard_fields/policy_reference",
            "cds/rating_summary/case_pricing/brokerage",
            "cds/rating_summary/case_pricing/written_line"
          ]} />
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Priced Quotes"
              numCols={2}
              fields={[
              "/cds/rating_summary/case_pricing/quoted_premium_100",
              "/cds/rating_summary/case_pricing/bpi",
              "technical_premium_100",
              "benchmark_premium_100",
              "/cds/currencies/source_currency",
              "/cds/rating_summary/case_pricing/tracker_class"
            ]} />
            <HX.Collection title="Pricing Metrics"
              numCols={3}
              fields={[
              "/cds/rating_summary/case_pricing/tpi_override",
              "pflr",
              "/cds/rating_summary/case_pricing/roc_override"
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Case Pricing Analysis Filepath">
          <HX.Notes field="cds/rating_summary/case_pricing/case_pricing_analysis_location" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs"
        fullWidth={false}
        shownBy="model_state/show_kpi">
        <HX.Section collapsible={false}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "/cds/standard_kpis/policy_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "/cds/standard_kpis/pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}
        shownBy="model_state/show_rationale">
        <HX.With context={{
          "path": "cds/rationale",
          "type": "struct"
        }}>
          <HX.Section title="Underwriter Rationale">
            <HX.Section title="Exporting Analysis">
              <HX.Pane flow="down">
                <HX.Pane flow="right">
                  <HX.Collection fields={[
                    "/non_cds/excel_analysis/projection_complete"
                  ]} />
                </HX.Pane>
                <HX.Pane flow="right"
                  shownBy="/non_cds/excel_analysis/projection_complete">
                  <HX.Button task="generate_excel_document_task"
                    title="Generate Excel Document" />
                  <HX.File field="/non_cds/excel_analysis/output_file"
                    shownBy="/non_cds/excel_analysis/show_download" />
                </HX.Pane>
              </HX.Pane>
            </HX.Section>
            <HX.Section title="Key information about account">
              <HX.Notes field="key_information" />
            </HX.Section>
            <HX.Section title="Rationale behind assumption selection">
              <HX.Notes field="rationale_assumptions" />
            </HX.Section>
            <HX.Section title="Rationale behind methodology selection and overrides">
              <HX.Notes field="rationale_methodology" />
            </HX.Section>
            <HX.Section title="Key uncertainties">
              <HX.Notes field="key_uncertainties" />
            </HX.Section>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="JSON View"
        shownBy="model_state/show_json_view">
        <HX.Section>
          <CustomComponent title="Schema Viewer"
            stringifiedJsonPath="schema_view/stringified_json"
            shownBy="schema_view/show_view" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Timer"
        shownBy="model_profiling/show">
        <HX.Section title="Function Tree">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "selected_segment",
              "timer_threshold"
            ]}
              horizontal={true}
              with="model_profiling" />
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Notes field="function_tree"
            title="Function Call Tree"
            with="model_profiling" />
        </HX.Section>
        <HX.Section title="Timed Segments">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "selected_segment",
              "timer_threshold"
            ]}
              horizontal={true}
              with="model_profiling" />
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Table data={[
            "timed_segments"
          ]}
            fields={[
            "name",
            "time_taken",
            "start_time",
            "end_time"
          ]}
            filter="show"
            with="model_profiling"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Gantt View">
          <CustomComponent title="Profiling"
            listSegments="model_profiling/timed_segments"
            myListFields={[
            "name",
            "start_time",
            "time_taken",
            "end_time",
            "show"
          ]} />
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