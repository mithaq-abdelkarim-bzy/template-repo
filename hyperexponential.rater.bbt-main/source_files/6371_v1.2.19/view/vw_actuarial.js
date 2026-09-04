//########### OUTSTANDING ########################
// Needs a shownby criteria 




import * as HX from "hx-model-components";

function vw_actuarial(scale) {
  return (
    <HX.Page title="Actuarial Info (typically hidden)" fullWidth={true} shownBy="cds/show_hide/page/show_actuarial">

      <HX.Section title="Keep actuarial view open:">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/rationale/actuarial_view"]} />
          <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
          <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
          <HX.Pane>            <HX.Collection fields={[null]} />          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Nodes not shown to UW:">
        <HX.Pane flow="right">
          <HX.Collection
            fields={["final_data_asat", "bic_data_asat"]}
            with="cds/risk_info"
            title="Submission Details"
          />
          <HX.Collection
            fields={["migrated_record"]}
            with="cds/model_state"
          />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Loss Ratio Summary - detailed, with Actuarial Overrides Active">

        <HX.Pane flow="right">

          <HX.Pane flow="down">
            <HX.Collection
              title="Attritional Adjustments"
              fields={["cds/rating_summary/summary_ratios/attritional/uw_adjustment"
                , "cds/rating_summary/summary_ratios/attritional/gg_pst_uw_adj/ulr_uw_override"
              ]}
              syncColumnWidthsKey="att"

            />
            <HX.Collection
              fields={["cds/rating_summary/summary_ratios/attritional/uw_rationale"]}
              shownBy="cds/show_hide/node/rs_att_rationale"
            />
          </HX.Pane>

          <HX.Pane flow="down">
            <HX.Collection
              title="Large Adjustments"
              fields={["cds/rating_summary/summary_ratios/large/uw_adjustment"
                , "cds/rating_summary/summary_ratios/large/uw_override"
              ]}
              syncColumnWidthsKey="large"

            />
            <HX.Collection
              fields={["cds/rating_summary/summary_ratios/large/uw_rationale"]}
              shownBy="cds/show_hide/node/rs_lrg_rationale"
            />
          </HX.Pane>

          <HX.Pane flow="down">
            <HX.Collection
              title="Catastrophe Adjustments"
              fields={["cds/rating_summary/summary_ratios/catastrophe/uw_adjustment"
                , "cds/rating_summary/summary_ratios/catastrophe/uw_override"
              ]}
              syncColumnWidthsKey="cat"

            />
            <HX.Collection
              fields={["cds/rating_summary/summary_ratios/catastrophe/uw_rationale"]}
              shownBy="cds/show_hide/node/rs_cat_rationale"
            />
          </HX.Pane>


        </HX.Pane>

        <HX.Pane flow="right">

          <HX.Table
            title="Attritional Loss Ratio Analysis"
            data={[
              null
              , { datum: "gg_pre_uw_adj", maxWidth: 140 }
              , { datum: "gn_pre_uw_adj", maxWidth: 140 }
              , { datum: "gg_pst_uw_adj", maxWidth: 140 }
              , { datum: "gn_pst_uw_adj", maxWidth: 140 }
            ]}
            fields={[
              "ulr_initial_benchmark"
              , "ulr_initial_experience"
              , "ulr_initial_experience_weighting"
              , "ulr_initial_selected"
              , "ulr_previous_selected_inferred"
              , "ulr_previous_override"
              , "ulr_previous"
              , "ulr_previous_suggested"
              , "ulr_selected_ol_py_factors_data"
              , "ulr_selected_ol_py_factors"
              , "ulr_selected_ol_py_ol_assump"
              , "ulr_selected_ol_exc_scalant"
              , "ulr_selected_ol"
              , "ulr_uw_override"
              , "ulr_final_uw"
              , "ulr_actuarial_override"
              , "ulr_final"
            ]}
            with="cds/rating_summary/summary_ratios/attritional"
            transpose
            syncColumnWidthsKey="att"

          />

          <HX.Table
            title="Large Loss Ratio Analysis"
            data={[
              null
              , { datum: "gg_pre_uw_adj", maxWidth: 140 }
              , { datum: "gn_pre_uw_adj", maxWidth: 140 }
              , { datum: "gg_pst_uw_adj", maxWidth: 140 }
              , { datum: "gn_pst_uw_adj", maxWidth: 140 }
            ]}
            fields={[
              "ulr_previous"
              , "ulr_benchmark"
              , "ulr_experience"
              , "ulr_experience_weighting"
              , "ulr_selected_ol"
              , "ulr_uw_override"
              , "ulr_final_uw"
              , "ulr_actuarial_override"
              , "ulr_final"
            ]}
            with="cds/rating_summary/summary_ratios/large"
            transpose
            syncColumnWidthsKey="large"

          />

          <HX.Table
            title="Catastrophe Loss Ratio Analysis"
            data={[
              null
              , { datum: "gg_pre_uw_adj", maxWidth: 140 }
              , { datum: "gn_pre_uw_adj", maxWidth: 140 }
              , { datum: "gg_pst_uw_adj", maxWidth: 140 }
              , { datum: "gn_pst_uw_adj", maxWidth: 140 }
            ]}
            fields={[
              "ulr_previous_exc_nml"
              , "ulr_previous"
              , "ulr_rms"
              , "ulr_benchmark"
              , "ulr_experience"
              , "ulr_experience_weighting"
              , "ulr_selected_ol_exc_nml"
              , "ulr_selected_ol_nml"
              , "ulr_selected_ol"
              , "ulr_uw_override"
              , "ulr_final_uw"
              , "ulr_actuarial_override"
              , "ulr_final"
            ]}
            with="cds/rating_summary/summary_ratios/catastrophe"
            transpose
            syncColumnWidthsKey="cat"
          />
        </HX.Pane>
      </HX.Section>







      <HX.Section title="KPI - detailed - Summary and Exhibits" defaultCollapsed={true}>


        <HX.Pane flow="right">

          <HX.Pane flow="down" stretch>

            <HX.Table
              title="Profit Commission Summary"
              data={[
                null
                , { datum: "technical", maxWidth: 140 }
              ]}
              fields={[
                "percent_pc"
                , "percent_pc_prior"
                , "amount_pc_100"
                , "amount_pc_afb"
              ]}
              with="cds/rating_summary"
              transpose
              syncColumnWidthsKey="pc_summary"
            />

            <HX.Collection fields={["cds/profit_commission/consistent_pc_latest_param"]} />
            <HX.Button task="simulate_pc_task" title="Calculate Profit Commission" />


            <HX.Table
              data={[
                null
                , { datum: "technical", maxWidth: 140 }
              ]}
              fields={[
                "gn_premium_quoted_inc_pc_afb"
                , "gn_premium_quoted_exc_pc_afb"
                , "gg_premium_quoted_afb"
              ]}
              with="cds/rating_summary"
              transpose
              syncColumnWidthsKey="pc_summary"
            />



            <HX.Table
              title="Premium Summary"
              data={[
                null
                , { datum: "amts_pre_uw_adj", maxWidth: 140 }
                , { datum: "amts_pst_uw_adj", maxWidth: 140 }
              ]}
              fields={[
                "gn_premium_tech_inc_pc_afb"
                , "gg_premium_tech_afb"
                , null
                , "gn_premium_bench_inc_pc_afb"
                , "gg_premium_bench_afb"
              ]}
              with="cds/rating_summary/technical"
              transpose
              syncColumnWidthsKey="pc_summary"
            />
          </HX.Pane>




          <HX.Pane flow="down" stretch>

            <HX.Table
              data={[
                null
                , { datum: "gg_pre_uw_adj", maxWidth: 140 }
                , { datum: "gg_pst_uw_adj", maxWidth: 140 }
              ]}
              fields={["ulr_priced_final"]}
              with="cds/rating_summary/summary_ratios/total"
              transpose
              syncColumnWidthsKey="lr_summary"
            />

            <HX.Table
              title="Loss Ratio Summary"
              data={[
                null
                , { datum: "gn_pre_uw_adj", maxWidth: 140 }
                , { datum: "gn_pst_uw_adj", maxWidth: 140 }
              ]}
              fields={[
                "ulr_bench"
                , "ulr_plan"
                , null
                , "ulr_prior"
                , null
                , "ulr_priced_final_exc_pc"
                , "ulr_priced_final_inc_pc"
              ]}
              with="cds/rating_summary/summary_ratios/total"
              transpose
              syncColumnWidthsKey="lr_summary"
            />


            <HX.Table
              title="KPI Summary"
              data={[
                null
                , { datum: "pre_uw_adj", maxWidth: 140 }
                , { datum: "pst_uw_adj", maxWidth: 140 }
              ]}
              fields={[
                "expected_profit"
                , "allocated_capital"
                , "roc"
                , null
                , "bpi"
                , "tpi"
                , null
                , "bpi_prior"
                , "tpi_prior"
              ]}
              with="cds/rating_summary/kpi"
              transpose
              syncColumnWidthsKey="lr_summary"
            />

          </HX.Pane>



          <HX.Pane flow="down" stretch >

            <HX.Table
              title="Technical Premium Derivation"
              data={[
                null
                , { datum: "amts_pre_uw_adj", maxWidth: 140 }
                , { datum: "amts_pst_uw_adj", maxWidth: 140 }
              ]}
              fields={[
                "losses_att_afb"
                , "losses_lrg_afb"
                , "losses_cat_afb"
                , "losses_tot_afb"
                , null
                , "lae_afb"
                , "reinsurance_afb"
                , "expense_afb"
                , "investment_afb"
                , "profit_req_afb"
                , null
                , "gn_premium_tech_inc_pc_afb"
                , null
                , "aqn_comm_afb"
                , "aqn_brok_afb"
                , "aqn_iptax_afb"
                , "aqn_total_exc_pc_afb"
                , null
                , "aqn_pc_afb"
                , null
                , "gg_premium_tech_afb"
              ]}
              with="cds/rating_summary/technical"
              transpose
            />

          </HX.Pane>


        </HX.Pane>

      </HX.Section>

















      <HX.Section title="Load Facility Data" defaultCollapsed={true}>

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
            title="Please select policies you wish to include:"
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


      <HX.Section title="Facility/Policy Listing Dataframe" defaultCollapsed={true}>
        <HX.Pane>
          <HX.Table
            title="Returned Beazley Intelligence Data"
            data={["cds/bi_data/facility_detail"]}
            fields={["include"
              , "date_extracted"
              , "section_reference"
              , "insured_party"
              , "inception_date"
              , "expiry_date"
              , "underwriter_name"
              , "settlement_currency"
              , "section_is_renewal"
              , "division"
              , "written_or_estimated_signed_line"
              , "trifocus_name"
              , "external_acquisition_cost_multiplier"
              , "profit_commission_multiplier"
              , "placing_brokername"
              , "risk_class_code"
              , "yoa"
              , "written_or_estimated_premium"
              , "rate_change_divisor"
              , "spot_rate_usd_to_sett"
              , "net_beazley_premium_sett_fx"
              , "net_100pct_premium_sett_fx"
              , "gross_100pct_premium_sett_fx"
              , "net_100pct_premium_adjexp_sett_fx"
            ]}
            kb-interactive
            dynamic
          />
          <HX.Collection fields={[null, null]} horizontal={false} />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Claims Details Listing Dataframe" defaultCollapsed={true}>
        <HX.Pane>
          <HX.Table
            title="Returned Beazley Intelligence Data"
            data={["cds/bi_data/claims_listing"]}
            fields={["date_extracted"
              , "section_reference"
              , "claim_reference"
              , "exposure_reference"
              , "yoa"
              , "beazley_catcode"
              , "market_catcode"
              , "trifocus_name"
              , "settlement_currency"
              , "block_indicator"
              , "date_of_loss"
              , "claim_made_date"
              , "claim_or_circumstance"
              , "beazley_share_total_incurred"
              , "slip_order_total_incurred"
              , "slip_order_total_paid"
              , "beazley_share_pre_peer_blend"
              , "beazley_share_pre_peer_most_likely"
              , "loss_category"
              , "bi_paid"
              , "bi_os"
              , "bi_incurred"
              , "pre_peer_blend_incurred"
              , "pre_peer_most_likely_incurred"
              , "show_cat"
              , "show_large"
              , "class_rank"
            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
        <HX.Collection fields={[null, null]} horizontal={false} />
      </HX.Section>


      <HX.Section title="Claims Incurred Movements Dataframe" defaultCollapsed={true}>
        <HX.Pane>
          <HX.Table
            title="Returned Beazley Intelligence Data"
            data={["cds/bi_data/claims_movements"]}
            fields={["date_extracted"
              , "loss_category"
              , "yoa"
              , "mvmt_yr"
              , "incurredmvmt_100_sett_fx"
            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
        <HX.Collection fields={[null, null]} horizontal={false} />
      </HX.Section>


      <HX.Section title="EDM Dataframe" defaultCollapsed={true}>

        <HX.Pane>
          <HX.Table
            data={["cds/rms/edm"]}
            fields={["return_period"
              , "probability"
              , "portnum"
              , "ws_loss_amount"
              , "ws_premium"
              , "ws_currency"
              , "ws_fxrate"
              , "eq_loss_amount"
              , "eq_premium"
              , "eq_currency"
              , "eq_fxrate"
            ]}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Rating Dataframe" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Table
            title="Complete List"
            data={["cds/rating_summary/detail_by_year"]}
            fields={[
              "yoa"
              , "incept_date"
              , "expiry_date"
              , "expiry_date_annual_est"

              , "include_suggested"
              , "include_override"
              , "include_selected"
              , "include_selected_weight"


              , "policy_length_calc"
              , "policy_length_override"
              , "policy_length_selected"
              , "policy_length_scalant"
              , "maturity"


              , "port_chg_prior"
              , "port_chg_suggested"
              , "port_chg_override"
              , "port_chg_selected"
              , "port_chg_cumul_prior"
              , "port_chg_cumul_suggested"
              , "port_chg_cumul_selected"

              , "rate_chg_prior"
              , "rate_chg_account"
              , "rate_chg_portfolio"
              , "rate_chg_suggested"
              , "rate_chg_override"
              , "rate_chg_selected"
              , "rate_chg_cumul_prior"
              , "rate_chg_cumul_suggested"
              , "rate_chg_cumul_selected"

              , "infl_chg_prior"
              , "infl_chg_suggested"
              , "infl_chg_override"
              , "infl_chg_selected"
              , "infl_chg_cumul_prior"
              , "infl_chg_cumul_suggested"
              , "infl_chg_cumul_selected"

              , "experience_default_perc_ult"
              , "experience_selected_perc_ult"
              , "benchmark_default_perc_ult"
              , "benchmark_selected_perc_ult"
              , "blended_default_perc_ult"
              , "blended_selected_perc_ult"
              , "interp_blended_selected_perc_ult"

              , "premium_prior"
              , "premium_suggested"
              , "premium_override"
              , "premium_selected"
              , "premium_selected_ol"
              , "premium_selected_ol_scaled"

              , "incurred_prior"
              , "paid_listing"
              , "incurred_listing"
              , "incurred_pp_blend"
              , "incurred_pp_most_likely"
              , "incurred_triangle"
              , "incurred_suggested"
              , "incurred_override"
              , "incurred_selected"

              , "large_threshold_usd"
              , "large_threshold_sett_fx"
              , "incurred_large_prior"
              , "paid_large_listing"
              , "incurred_large_listing"
              , "incurred_large_pp_blend"
              , "incurred_large_pp_most_likely"
              , "incurred_large_triangle"
              , "incurred_large_suggested"
              , "incurred_large_override"
              , "incurred_large_selected"
              , "incurred_large_selected_lr"
              , "incurred_large_selected_inflated"

              , "incurred_cat_prior"
              , "paid_cat_listing"
              , "incurred_cat_listing"
              , "incurred_cat_pp_blend"
              , "incurred_cat_pp_most_likely"
              , "incurred_cat_triangle"
              , "incurred_cat_suggested"
              , "incurred_cat_override"
              , "incurred_cat_selected"
              , "incurred_cat_selected_lr"
              , "incurred_cat_selected_inflated"

              , "incurred_att_prior"
              , "paid_att_listing"
              , "incurred_att_listing"
              , "incurred_att_pp_blend"
              , "incurred_att_pp_most_likely"
              , "incurred_att_triangle"
              , "incurred_att_suggested"
              , "incurred_att_override"
              , "incurred_att_selected"
              , "incurred_att_selected_lr"
              , "incurred_att_selected_inflated"

              , "ultimate_att_cl_selected"
              , "ultimate_att_cl_selected_py_factors"
              , "ultimate_att_cl_selected_py_factors_data"
              , "ultimate_att_cl_selected_ol"
              , "ultimate_att_cl_selected_ol_exc_scalant"
              , "ultimate_att_cl_selected_ol_py_ol_assump"
              , "ultimate_att_cl_selected_ol_py_factors"
              , "ultimate_att_cl_selected_ol_py_factors_data"

              , "reserving_method_attritional"
              , "ultimate_att_meth_selected_ol"
              , "ultimate_att_meth_selected_ol_exc_scalant"
              , "ultimate_att_meth_selected_ol_py_ol_assump"
              , "ultimate_att_meth_selected_ol_py_factors"
              , "ultimate_att_meth_selected_ol_py_factors_data"

              , "weighting_exposure"
              , "weighting_decay"
              , "weighting_development"
              , "weighting_combined"
              , "weighting_final"

              , "display_yoa"
              , "display_premium_ol"
              , "display_attritional_weight"

              , "display_attritional_incurred_lr"
              , "display_attritional_chainladder_lr"
              , "display_attritional_approach"
              , "display_attritional_selected_lr"

              , "display_large_incurred_lr"
              , "display_large_chainladder_lr"
              , "display_large_approach"
              , "display_large_selected_lr"

              , "display_cat_incurred_lr"
              , "display_cat_chainladder_lr"
              , "display_cat_approach"
              , "display_cat_selected_lr"

              , "display_show_row_inputs"
              , "display_show_row_rating"
            ]}
            kb-interactive
            dynamic
          />

        </HX.Pane>


      </HX.Section>



    </HX.Page>
  )
}

export { vw_actuarial };
