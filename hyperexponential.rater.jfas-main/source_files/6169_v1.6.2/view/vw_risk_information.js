import * as HX from "hx-model-components";

function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" fullWidth={false} viewScale={scale} shownBy="cds/show_page/show_risk_information">
      <HX.Section title="Policy Information">
        <HX.Pane flow='right'>
          <HX.Collection fields={[
            "cds/risk_info/database_id",
            "cds/risk_info/submission_date",
            { field: "cds/standard_fields/policy_reference", shownBy: "cds/policy_reference_filled" },
            { field: "cds/standard_fields/policy_reference.invalid", shownBy: "cds/policy_reference_not_filled" },
            "cds/risk_info/policy_reference_exp",
          ]}
            numCols={1}
          />
          <HX.Collection fields={[
            // # SA: The standard field for the cds insured_name seems like it should be pointing to the selected insured name rather than 
            // the dropdown or override field. The selected name seems like the appropriate one for reporting purposes. I've retrofitted
            // matching to the spreadsheet exactly
            { field: "cds/standard_fields/insured_name", shownBy: "cds/insured_name_selected" },
            { field: "cds/standard_fields/insured_name.invalid", shownBy: "cds/insured_name_not_selected" },
            { field: "cds/risk_info/new_replacement", shownBy: "cds/insured_name_selected" },
            { field: "cds/risk_info/new_replacement.invalid", shownBy: "cds/insured_name_not_selected" },
            { field: "cds/risk_info/insured_name_final" },
            "cds/standard_fields/is_renewal",
          ]}
            numCols={1}
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Load Expiring Information" shownBy="cds/standard_fields/is_renewal">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "cds/risk_info/expiring_policy_option_id",
          ]} />
          <HX.Button task="expiring_policy_fetch_task" title="Load Expiring Policy Information" />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            { field: "cds/standard_fields/benchmark_class", shownBy: "cds/risk_class_selected" },
            { field: "cds/standard_fields/benchmark_class.invalid", shownBy: "cds/risk_class_not_selected" },
          ]} />
          <HX.Pane>
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
          <HX.Pane flow='right'>
            <HX.Collection fields={[
              { field: "/cds/standard_fields/underwriter", shownBy: "/cds/underwriter_selected" },
              { field: "/cds/standard_fields/underwriter.invalid", shownBy: "/cds/underwriter_not_selected" },
              { field: "status", shownBy: "/cds/validation/status/valid" },
              { field: "status.invalid", shownBy: "/cds/validation/status/invalid" },
              // "hx_core/inception_date",
              // "hx_core/expiry_date",
              // "policy_duration",
              "/cds/currencies/source_currency",
              // "cds/standard_fields/is_renewal",
              //"risk_class",
              // "risk_class_generated",
            ]}
              numCols={2}
            />
          </HX.Pane>
        </HX.With>
        <HX.Pane flow='right'>
          <HX.Collection fields={[
            // "underwriter",
            // "deal_status",
            "hx_core/inception_date",
            "hx_core/expiry_date",
            "cds/risk_info/policy_duration",
            // "currency",
            // "cds/standard_fields/is_renewal",
            // "risk_class",
            // "risk_class_generated",
          ]}
            numCols={2}
          />
        </HX.Pane>

      </HX.Section>
      <HX.Section title="Strikes, Riots and Civil Commotion">
        <HX.Pane>
          <HX.Collection fields={[
            "cds/risk_info/srcc_coverage_given_indicator",
            "cds/risk_info/srcc_fully_excluded_indicator",
            "cds/risk_info/srcc_sublimit_indicator",
            "cds/risk_info/srcc_sublimit",
          ]}
            numCols={2}
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Broker Details">
        <HX.Pane>
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/risk_info/broker_contact",
          ]}
            numCols={2}
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Underwriter Comments">
        <HX.Notes field="cds/standard_fields/uw_rationale" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_risk_information };