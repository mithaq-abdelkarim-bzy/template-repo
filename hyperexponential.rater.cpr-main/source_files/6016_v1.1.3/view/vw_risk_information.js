import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">

      <HX.Section title="Account Details">
        <HX.Pane >
          {/* NOTE  uncomment if rater requires databse_id to be displayed */}
          {/* <HX.Collection fields={["database_id"]} with="cds" horizontal /> */}
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["cds/standard_fields/underwriter", "cds/product"]} horizontal />
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["section_reference", "/cds/currencies/source_currency", "/cds/standard_fields/is_renewal"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Load Policy Data from Beazley Intelligence" defaultCollapsed={true} >
        <HX.Pane>
          <HX.Collection
            fields={["last_run_status", "check_run_consistent", "calc_run_value"]}
            with="cds/bi"
            title="Enter Policy Section Reference then press button here to load latest Beazley Intelligence information."
          />
          <HX.Button title="Load from BI" task="task_sql_bi_data" stretch />
        </HX.Pane>
      </HX.Section>



      <HX.Section title="Policy Information" >
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["written_line", "limit", "excess"]} horizontal />
            <HX.Collection fields={["brokerage", "status", null]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section>


      <HX.Section
        title="Credit Risk & Contract Frustration - additional fields"
        shownBy="/cds/show_hide/node/show_crcf"
      >

        <HX.Pane flow="right">
          <HX.Pane flow="down">
            <HX.Collection
              fields={["crcf_obligor", "crcf_country", "crcf_industry_group", "crcf_industry"]}
              with="cds/risk_info"
            />
          </HX.Pane>

          <HX.Pane flow="down" stretch>
            <HX.Collection
              fields={["last_run_status", "check_run_consistent", "calc_run_value"]}
              with="cds/ihs"
              title="Select country then press button here to load latest IHS information."
            />
            <HX.Button title="Load IHS Data" task="task_api_ihs_data" stretch />
          </HX.Pane>
        </HX.Pane>

      </HX.Section>

    </HX.Page >
  )
}

export { vw_risk_information };


