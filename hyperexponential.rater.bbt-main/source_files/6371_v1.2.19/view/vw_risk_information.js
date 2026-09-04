import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" viewScale={0.9} shownBy="cds/model_state/show_after_landing_page">
      <HX.Section title="Account Details">

        <HX.Pane >
          {/*Hux requested we remove below fields 2024-07-04 */}
          {/*<HX.Collection fields={["cds/database_id", "cds/risk_info/application_date"]} horizontal /> */}
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["underwriter", "benchmark_class"]} with="cds/standard_fields" horizontal />
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          <HX.Collection fields={["cds/standard_fields/facility_reference", "cds/currencies/source_currency", "cds/standard_fields/is_renewal"]} horizontal />
        </HX.Pane>
      </HX.Section>



      <HX.Section title="Settings" >
        <HX.Pane flow="right">
          <HX.Collection
            fields={["new_to_market", "rms_modelling_available", "pc_modelling_required", "tri_modelling_required"]}
            with="cds/risk_info"
            horizontal
          />
        </HX.Pane>
      </HX.Section>




      <HX.Section
        title="Load Facility Data"
        defaultCollapsed={true}>

        <HX.Pane flow="right">
          <HX.Collection
            fields={["cds/standard_fields/facility_reference"
              , "cds/risk_info/facility_reference2"
              , "cds/risk_info/facility_reference3"
              , "cds/risk_info/facility_reference4"
              , "cds/risk_info/facility_reference5"
              , "cds/risk_info/facility_reference6"
              , "cds/risk_info/facility_reference7"]}
            horizontal />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Collection fields={["cds/bi_data/include_all_facility_references"]} />
          <HX.Button task="bi_facility_fetch_task" title="Search Database" />
        </HX.Pane>

        <HX.Pane >
          <HX.Notes field="cds/bi_data/fetch_facility_detail_task_status" />
        </HX.Pane>

        <HX.Pane>
          <HX.Table
            title="Please select references you wish to include:"
            maxListVisibleRows={8}
            freezeLeft={1}
            data={["cds/bi_data/facility_detail"]}
            fields={["include"
              , "section_reference"
              , "insured_party"
              , "yoa"
              , "underwriter_name"
              , "written_or_estimated_premium"
            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Button task="bi_facility_include_all_task" title="Select  All" />
          <HX.Button task="bi_facility_exclude_all_task" title=" Deselect All" />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Button task="bi_clm_and_mvmt_inc_triangles_fetch_task" title="Load remaining data including triangles" />
          <HX.Button task="bi_clm_and_mvmt_exc_triangles_fetch_task" title="Load remaining data excluding triangles" />
        </HX.Pane>
        <HX.Pane >
          <HX.Notes field="cds/bi_data/fetch_clm_and_mvmt_detail_task_status" />
        </HX.Pane>

      </HX.Section>


      <HX.Section title="Business Line" >
        <HX.Pane flow="right">
          <HX.Collection
            fields={[
              "standard_fields/trifocus"
              , { field: "risk_info/proxy_trifocus", shownBy: "show_hide/node/ri_proxy_trifocus" }
              , "risk_info/division"
            ]} with="cds" horizontal />
        </HX.Pane>
      </HX.Section>



      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section>

      {/* NOTE use the below code if the model does not price multiple layers and it is required to store line size brokerage & status on teh risk Information sheet */}
      <HX.Section title="Basic Financial Details" >
        <HX.Pane flow="right">

          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection
              fields={["quoted_premium_100pct", "written_line", "quoted_premium", "status"]}
              title="Premium & Status"
            />
          </HX.With>

          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection
              fields={["commission", "brokerage", "ipt", "total_deductions"]}
              title="Deductions - Fixed"
            />
          </HX.With>
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Profit Commission Details" >
        <HX.Pane flow="right">

          <HX.With context={{ type: "list", path: "cds/profit_commission/scenarios", index: 0 }}>

            <HX.Collection
              fields={["additionalfeaturesindicator"]}
              title="Profit Commission (PC)"
            />

            <HX.Collection
              fields={["share", "expenses", "basis", "deficit"]}
              shownBy="/cds/show_hide/node/pc_standard"
            />


          </HX.With>

          <HX.With context={{ type: "list", path: "cds/profit_commission/scenarios", index: 0 }}>
            <HX.Collection
              fields={["threshold_bonus_share"
                , "threshold_lr_cutoff"
              ]}
              title="Additional Features"
              shownBy="/cds/show_hide/node/pc_threshold"
            />

            <HX.Collection
              fields={["slidingscale_bonus_lr"
                , "slidingscale_bonus_scale"
                , "slidingscale_bonus_maxtotalpc"
                , "slidingscale_clawback_lr"
                , "slidingscale_clawback_scale"
                , "slidingscale_clawback_mintotalpc"
              ]}
              title="Additional Features"
              shownBy="/cds/show_hide/node/pc_sliding_scale"
            />
          </HX.With>
        </HX.Pane>
      </HX.Section>






      <HX.Section title="Strikes, riots and civil commotions" >
        <HX.Pane flow="right">
          <HX.Collection
            fields={["srcc_coverage_given_indicator", "srcc_fully_excluded_indicator", "srcc_sublimit_indicator", "srcc_sublimit"]}
            with="cds/risk_info"
            horizontal
          />
        </HX.Pane>
      </HX.Section>



    </HX.Page >
  )
}

export { vw_risk_information };


