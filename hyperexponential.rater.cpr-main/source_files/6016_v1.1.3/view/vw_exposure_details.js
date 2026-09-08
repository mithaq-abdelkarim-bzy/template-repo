import * as HX from "hx-model-components";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={false} viewScale={scale} shownBy="cds/show_hide/page/show_exposure_detail">
      <HX.Section title="Exposure Details - CRCF" shownBy="/cds/show_hide/node/show_crcf">
        <HX.Pane flow="right" reflow={true}>
          <HX.Collection
            title="Cover Details"
            fields={[
              "sum_insured"
              , "indemnity"
              , "waiting_period"
              , null
              , null
            ]}
            horizontal
            with="cds/exposure/granular/crcf"
            syncColumnWidthsKey="exposure_details_crcf"
          />
        </HX.Pane>

        <HX.Pane flow="right" reflow={true}>
          <HX.Collection
            title="Pre Shipment Risk"
            fields={[
              "pre_shipment_risk"
            ]}
            with="cds/exposure/granular/crcf"
            shownBy="/cds/show_hide/node/show_pre_shipment_risk_not"
            horizontal
            syncColumnWidthsKey="exposure_details_crcf"
          />
        </HX.Pane>

        <HX.Pane flow="right" reflow={true}>
          <HX.Collection
            title="Pre Shipment Risk"

            fields={[
              "pre_shipment_risk"
              , "pre_shipment_amt"
              , "pst_shipment_amt"
            ]}
            with="cds/exposure/granular/crcf"
            shownBy="/cds/show_hide/node/show_pre_shipment_risk"
            horizontal
            syncColumnWidthsKey="exposure_details_crcf"
          />
        </HX.Pane>



        <HX.Pane flow="down">
          <HX.Pane flow="right" reflow={true}>
            <HX.Collection
              title="Amount at Risk"
              fields={["load_amt_basis"]}
              with="cds/exposure/granular/crcf"
              shownBy="/cds/show_hide/node/show_hide_flat_not"
              horizontal
              syncColumnWidthsKey="exposure_details_crcf"
            />

            <HX.Collection
              title="Amount at Risk"
              fields={["load_amt_basis", "load_amt_flat"]}
              with="cds/exposure/granular/crcf"
              shownBy="/cds/show_hide/node/show_hide_flat"
              horizontal
              syncColumnWidthsKey="exposure_details_crcf"
            />
          </HX.Pane>

          <HX.Pane flow="right" reflow={true}>
            <HX.Collection
              fields={["load_amt_step_opening_si", "load_amt_step_grace_period", "load_amt_step_instal_freq",]}
              with="cds/exposure/granular/crcf"
              shownBy="/cds/show_hide/node/show_hide_step"
              horizontal
              syncColumnWidthsKey="exposure_details_crcf"
            />
            <HX.Collection
              fields={["load_amt_step_instal_amt", "load_amt_step_term"]}
              with="cds/exposure/granular/crcf"
              shownBy="/cds/show_hide/node/show_hide_step"
              horizontal
              syncColumnWidthsKey="exposure_details_crcf"
            />
          </HX.Pane>


          {/* <HX.Pane flow="right" reflow={true} shownBy="/cds/show_hide/node/show_hide_step">
            <HX.Collection fields={["cds/exposure/granular/crcf/load_amt_step_opening_si"]} horizontal />
            <HX.Collection fields={["cds/exposure/granular/crcf/load_amt_step_grace_period"]} horizontal />
            <HX.Collection fields={["cds/exposure/granular/crcf/load_amt_step_instal_freq"]} horizontal />
            <HX.Collection fields={["cds/exposure/granular/crcf/load_amt_step_instal_amt"]} horizontal />
            <HX.Collection fields={["cds/exposure/granular/crcf/load_amt_step_term"]} horizontal />
          </HX.Pane> */}


          {/* <HX.Collection
              fields={["load_amt_step_opening_si", "load_amt_step_grace_period", "load_amt_step_instal_amt", "load_amt_step_instal_freq", "load_amt_step_term"]}
              with="cds/exposure/granular/crcf"
              shownBy="/cds/show_hide/node/show_hide_step"
              horizontal
              syncColumnWidthsKey="exposure_details_crcf"
            /> */}

          <HX.Pane flow="right" reflow={true}>
            <HX.Button
              title="Populate Automatic Exposure Profile"
              task="task_fill_exposure_profile"
            />
            <HX.Collection
              fields={["last_run_status"]}
              with="cds/exposure/granular/crcf"
              horizontal
            />
          </HX.Pane>
        </HX.Pane>


        <HX.Pane flow="right">
          <HX.Table
            title="Exposure Profile"
            data={[{ datum: "exposure_profile", elementLabelBy: "year_label" }]}
            fields={[
              { field: "month_1", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_1" }
              , { field: "month_2", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_2" }
              , { field: "month_3", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_3" }
              , { field: "month_4", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_4" }
              , { field: "month_5", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_5" }
              , { field: "month_6", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_6" }
              , { field: "month_7", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_7" }
              , { field: "month_8", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_8" }
              , { field: "month_9", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_9" }
              , { field: "month_10", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_10" }
              , { field: "month_11", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_11" }
              , { field: "month_12", maxWidth: 140, labelBy: "/cds/exposure/granular/crcf/exposure_profile_label_months/month_12" }
            ]}
            with="cds/exposure/granular/crcf"
            filter="year_show_hide"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      {/* 
      title="Pre Shipment Risk"

fields={[
  "pre_shipment_risk"
  , "pre_shipment_amt"
  , "pst_shipment_amt"
]}
with="cds/exposure/granular/crcf" */}




      <HX.Section title="Credit Rating - CRCF" shownBy="/cds/show_hide/node/show_crcf">
        <HX.Pane flow="down">
          <HX.Table
            data={[{ datum: "crcf", maxWidth: 350 }]}
            fields={[
              { field: 'rating_source', shownBy: '/cds/show_hide/node/show_cr_only' }
              , { field: 'rating_corporate', shownBy: '/cds/show_hide/node/show_cr_only' }
              , "rating_country"
              , "economic_outlook"
            ]}
            with="cds/modifiers"
            transpose
            title="Rating & Outlook"
          />
        </HX.Pane>



        <HX.Pane flow="down">
          <HX.Table
            data={[
              null
              , { datum: "default", maxWidth: 140 }
              , null
              , { datum: "override_min", maxWidth: 140 }
              , { datum: "override", maxWidth: 140 }
              , { datum: "override_max", maxWidth: 140 }
              , null
              , { datum: "selected", maxWidth: 140 }
            ]}
            fields={[
              "grade"
              , "pod"
              , "lgd"
              , "uw_adj"
            ]}
            with="cds/modifiers/crcf"
            transpose
            title="Underwriter Adjustments"
            syncColumnWidthsKey="credit_rating_crcf"
          />
          <HX.Notes field="cds/modifiers/crcf/rating_commentary" title="Please provide detail on the source of the credit rating." />
          <HX.Notes field="cds/modifiers/crcf/obligor_commentary" title="Please provide detail on the Obligor Risk Drivers" />
          <HX.Notes field="cds/modifiers/crcf/lgd_commentary" title="Please provide detail on the Security & its Impact on Average LGD" />
          <HX.Notes field="cds/modifiers/crcf/uw_adj_commentary" title="Please provide detail on the Underwriter Adjustments" />
        </HX.Pane>
      </HX.Section>



      <HX.Section title="Exposure Details - Political Risk" shownBy="/cds/show_hide/node/show_political">
        <HX.Pane flow="right">
          <HX.Collection
            fields={[
              "cds/exposure/granular/political/tenor"
              , "cds/exposure/granular/political/key_summary_outputs/tenor_rate"
              , "cds/exposure/granular/political/simulation/num_sims"
              , "cds/exposure/granular/political/exposure_curve"
              , null
            ]}
            horizontal
          />
        </HX.Pane>

        <HX.Pane flow="down">
          <HX.Table
            data={[
              { datum: "mobile_assets", maxWidth: 140 }
              , { datum: "fixed_assets", maxWidth: 140 }
              , { datum: "lenders_interest", maxWidth: 140 }
              , { datum: "sublimit", maxWidth: 140 }
              , { datum: "deductible", maxWidth: 140 }
            ]}
            fields={["gov_action", "pol_violence", "cur_inconvertibility", "cont_relation_govt"]}
            with="cds/exposure/granular/political/coverage_matrix"
            transpose
            title="Coverage Matrix"
          />
        </HX.Pane>

        <HX.Pane flow="down">
          <HX.Table
            data={[
              null
              , { datum: "override_min", maxWidth: 140 }
              , { datum: "override", maxWidth: 140 }
              , { datum: "override_max", maxWidth: 140 }
              , null
              , { datum: "selected", maxWidth: 140 }
            ]}
            fields={[null, "total", null, "industry", "insured_quality", "asset_composition"]}
            with="cds/modifiers/political"
            transpose
            title="Underwriter Adjustments"
          />

          <HX.Notes field="cds/modifiers/political/uw_adj_commentary" title="Please provide information on the Underwriter Adjustments" />
        </HX.Pane>
      </HX.Section>



      <HX.Section title="Exposure Profile - Political Risk" shownBy="/cds/show_hide/node/show_political">
        <HX.Table
          title="Country Details"
          data={["cds/exposure/granular/political/country_exposure"]}
          fields={["country", "sum_insured", "excess", "limit", "check", "country_2dig"]}
          kb-interactive
        />
      </HX.Section >


      <HX.Section title="Settings" shownBy="/cds/show_hide/node/show_political" >
        <HX.Pane flow="right">
          <HX.Pane flow="down" stretch>
            <HX.Collection
              fields={["last_run_status", "check_run_consistent", "calc_run_value"]}
              with="cds/ihs"
              title="Enter country details in sections below then press button to load IHS info."
            />
            <HX.Button title="Load IHS Data" task="task_api_ihs_data" />
          </HX.Pane>

          <HX.Pane flow="down" shownBy="/cds/show_hide/node/show_political">
            <HX.Collection
              fields={["last_run_status", "check_run_consistent", "calc_run_value"]}
              with="cds/exposure/granular/political/simulation"
              title="Enter all details in sections below then press button here to run simulation."
            />
            <HX.Button task="task_sim_political" title="Simulate Losses" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section >


    </HX.Page >


  )
}

export { vw_exposure_details };