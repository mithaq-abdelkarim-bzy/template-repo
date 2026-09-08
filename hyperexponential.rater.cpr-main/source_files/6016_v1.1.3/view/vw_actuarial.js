//########### OUTSTANDING ########################
// Needs a shownby criteria 




import * as HX from "hx-model-components";

function vw_actuarial(scale) {
  return (
    <HX.Page title="Actuarial Info (typically hidden)" fullWidth={true} shownBy={"cds/show_hide/page/show_actuarial"}>


      <HX.Section title="IHS Dataframe" defaultCollapsed={true}>
        <HX.Collection
          fields={[
            "last_run_status"
            , "last_run_date"
            , "last_run_value"
            , "calc_run_value"
            , "check_run_consistent"
          ]}
          with="cds/ihs"
          horizontal
        />

        <HX.Button title="Load IHS Data" task="task_api_ihs_data" />


        <HX.Pane flow="right">
          <HX.Table
            title="IHS Outlook"
            data={["cds/ihs/ihs_outlook"]}
            fields={[
              { field: 'country', maxWidth: 100 }
              , { field: 'risk_name', maxWidth: 250 }
              , { field: 'outlook', maxWidth: 120 }
              , { field: 'outlook_description', maxWidth: 500 }
              , { field: 'last_updated_date', maxWidth: 200 }
              , { field: 'last_updated_value', maxWidth: 200 }
            ]}
            maxListVisibleRows={15}
            kb-interactive
            dynamic
          />

          <HX.Table
            title="IHS Historic Values"
            data={["cds/ihs/ihs_detail"]}
            fields={[
              { field: 'country', maxWidth: 100 }
              , { field: 'risk_name', maxWidth: 250 }
              , { field: 'historic_updated_date', maxWidth: 200 }
              , { field: 'historic_updated_value', maxWidth: 200 }
            ]}
            maxListVisibleRows={15}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>





      <HX.Section title="Simulation" defaultCollapsed={true}>
        <HX.Collection
          fields={[
            "total_sim_loss_uncapped"
            , "total_sim_loss_capped"
            , "total_det_loss_uncapped"
            , "total_det_loss_capped"
            , "total_det_loss_scaled"
          ]}
          with="cds/exposure/granular/political/simulation"
          horizontal
        />

        <HX.Collection
          fields={[
            "last_run_status"
            , "last_run_date"
            , "last_run_value"
            , "calc_run_value"
            , "check_run_consistent"
          ]}
          with="cds/exposure/granular/political/simulation"
          horizontal
        />

        <HX.Button title="Simulate loss" task="task_sim_political" />
      </HX.Section>



      <HX.Section title="Load from Beazley Intelligence" defaultCollapsed={true} >
        <HX.Pane>
          <HX.Collection
            fields={["last_run_status", "last_run_date", "last_run_value", "calc_run_value", "check_run_consistent"]}
            with="cds/bi"
            title="Enter Policy Section Reference then press button here to load latest Beazley Intelligence information."
          />
          <HX.Button title="Load from BI" task="task_sql_bi_data" stretch />
        </HX.Pane>
      </HX.Section>





      <HX.Section title="Exposure Rating Dataframe - CRCF" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Table
            title="Complete List"
            data={["cds/exposure/granular/crcf/exposure_profile"]}
            fields={[
              'year'
              , 'year_label'
              , 'year_show_hide'
              , 'month_1'
              , 'month_2'
              , 'month_3'
              , 'month_4'
              , 'month_5'
              , 'month_6'
              , 'month_7'
              , 'month_8'
              , 'month_9'
              , 'month_10'
              , 'month_11'
              , 'month_12'
              , 'average_default_month'
              , 'average_default_year_month'
              , 'average_exposure'
              , 'average_recovery_time'
              , 'expected_recovery_pct'
              , 'term_adj'
              , 'pre_uw_adj_tenor_load'
              , 'pre_uw_adj_pod_adj_inc'
              , 'pre_uw_adj_pod_adj_inc_allow_prior'
              , 'pre_uw_adj_average_severity'
              , 'pre_uw_adj_average_loss'
              , 'pre_uw_adj_average_loss_adj_lim_xs'
              , 'pre_uw_adj_premium_benchmark'
              , 'pre_uw_adj_premium_achieved'
              , 'pre_uw_adj_premium_achieved_adj_pod'
              , 'pst_uw_adj_tenor_load'
              , 'pst_uw_adj_pod_adj_inc'
              , 'pst_uw_adj_pod_adj_inc_allow_prior'
              , 'pst_uw_adj_average_severity'
              , 'pst_uw_adj_average_loss'
              , 'pst_uw_adj_average_loss_adj_lim_xs'
              , 'pst_uw_adj_premium_benchmark'
              , 'pst_uw_adj_premium_achieved'
              , 'pst_uw_adj_premium_achieved_adj_pod'
              , 'implied_lgd_average_loss_adj_lim_xs'
              , 'implied_lgd_average_loss'
              , 'implied_lgd_average_severity'
              , 'implied_lgd'
              , 'implied_grade_average_loss_adj_lim_xs'
              , 'implied_grade_average_loss'
              , 'implied_grade_pod_adj_inc_allow_prior'
              , 'implied_grade_pod_adj_inc'
              , 'implied_grade_pod_inc'
            ]}
            kb-interactive
            dynamic
          />

        </HX.Pane>


      </HX.Section>


      <HX.Section title="Exposure Rating Dataframe - Political Risk" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Table
            title="Complete List"
            data={["cds/exposure/granular/political/country_exposure"]}
            fields={[
              'id'
              , 'country'
              , 'sum_insured'
              , 'excess'
              , 'limit'
              , 'check'
              , 'country_2dig'
              , 'sublimit_pv'
              , 'deductible_pv'
              , 'sublimit_ci'
              , 'ihs_political'
              , 'ihs_violence'
              , 'ihs_ci'
              , 'prem_roe_gai'
              , 'prem_roe_pv'
              , 'prem_roe_ci'
              , 'prem_roe_crg'
              , 'prem_roe_tot'
              , 'loss_roe_gai'
              , 'loss_roe_pv'
              , 'loss_roe_ci'
              , 'loss_roe_crg'
              , 'loss_roe_tot'
              , 'struc_adj_gai'
              , 'struc_adj_pv'
              , 'struc_adj_ci'
              , 'struc_adj_crg'
              , 'net_rol_gai'
              , 'net_rol_pv'
              , 'net_rol_ci'
              , 'net_rol_crg'
              , 'net_rol_tot'
              , 'gross_rol_tot'
            ]}
            kb-interactive
            dynamic
          />

        </HX.Pane>


      </HX.Section>



















      <HX.Section title="Metrics - Political Risks" defaultCollapsed={true}>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Table
              title="Rate-on-Line & Kpis"
              data={[
                null
                , { datum: "metrics_summary_pre_uwadj", maxWidth: 140 }
                , { datum: "metrics_summary_pst_uwadj", maxWidth: 140 }
              ]}
              fields={[
                "rol_offered"
                , "rol_model"
                , "rol_technical"
                , "rol_benchmark"
                , null
                , "bpi"
                , "priced_to_plan"
                , "tpi"
                , "priced_gglr"
                , "priced_gnlr"
              ]}
              with="political"
              transpose
              syncColumnWidthsKey="metrics_1"
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>


      <HX.Section title="Premium Details - Political Risks" defaultCollapsed={true}>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Table
              title="Premium Analysis by Peril - BEFORE Underwriter Adjustment"
              data={[
                null
                , { datum: "gov_action", maxWidth: 140 }
                , { datum: "pol_violence", maxWidth: 140 }
                , { datum: "cur_inconvertibility", maxWidth: 140 }
                , { datum: "cont_relation_govt", maxWidth: 140 }
                , { datum: "total", maxWidth: 140 }
              ]}
              fields={[
                "premium_bound"
                , "premium_benchmark"
                , "premium_model"
                , null
                , "premium_technical"
                , "expected_loss"
                , "che"
                , "fixed_expenses"
                , "variable_expenses"
                , "investment_income"
                , "cost_of_reinsurance"
                , "capital"
                , "brokerage"
              ]}
              with="political/premium_composition_pre_uwadj"
              transpose
              syncColumnWidthsKey="xxxxxxxxxxxxxxxxxxxxx"
            />

            <HX.Table
              title="Premium Analysis by Peril - AFTER Underwriter Adjustment"
              data={[
                null
                , { datum: "gov_action", maxWidth: 140 }
                , { datum: "pol_violence", maxWidth: 140 }
                , { datum: "cur_inconvertibility", maxWidth: 140 }
                , { datum: "cont_relation_govt", maxWidth: 140 }
                , { datum: "total", maxWidth: 140 }
              ]}
              fields={[
                "premium_bound"
                , "premium_benchmark"
                , "premium_model"
                , null
                , "premium_technical"
                , "expected_loss"
                , "che"
                , "fixed_expenses"
                , "variable_expenses"
                , "investment_income"
                , "cost_of_reinsurance"
                , "capital"
                , "brokerage"
              ]}
              with="political/premium_composition_pst_uwadj"
              transpose
              syncColumnWidthsKey="xxxxxxxxxxxxxxxxxxxxx"
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>


      <HX.Section title="Mapping to standard fields" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Pane flow="down">
            <HX.Table
              title="hx - standard fields"
              data={["hx_core"]}
              fields={[
                "inception_date"
                , "expiry_date"
                , "model_premium"
                , "charged_premium"
                , "premium_currency"
                , "ulr"
                , "class_code"
              ]}
              transpose
            />

            <HX.Table
              title="cds - currencies"
              data={["cds/currencies"]}
              fields={[
                "target_currency"
                , "source_currency"
                , "multi_currency_support"
              ]}
              transpose
            />


            <HX.Table
              title="cds - experience rating"
              data={["cds/experience_rating"]}
              fields={[
                "claims_available"
                , "claims_fgu"
                , "claims_net_of_deductible"
              ]}
              transpose
            />

            <HX.Table
              title="cds"
              data={["cds"]}
              fields={[
                "database_id"
                , "broker_contact"
                , "product"
              ]}
              transpose
            />


          </HX.Pane>



          <HX.Table
            title="cds - standard fields"
            data={["cds/standard_fields"]}
            fields={[
              "insured_name"
              , "broker"
              , "expiry_date"
              , "inception_date"
              , "insured_country"
              , "insured_postal_code"
              , "insured_state_or_province"
              , "is_admitted_or_surplus"
              , "is_free_trade_zone"
              , "is_renewal"
              , "underwriter"
              , "policy_reference"
              , "facility_reference"
              , "benchmark_class"
              , "uw_rationale"
              , "trifocus"
              , "rating_methodology"
              , "is_case_priced"
              , "is_rater_priced"
            ]}
            transpose
          />



          <HX.Table
            title="cds - standard layer fields"
            data={["cds/layers"]}
            fields={[
              "limit"
              , "excess"
              , "deductible"
              , "aggregate_limit"
              , "aggregate_excess"
              , "aggregate_deductible"
              , "currency"
              , "section_reference"
              , "brokerage"
              , "written_line"
              , "premium"
              // "premium" field above is blank per skeleton model guide "DO NOT USE UNTIL WORKBENCH INTEGRATION."
              , "status"
              , "is_primary_excess"
              , "benchmark_premium"
              , "bpi"
              , "bpi_pre_uw_adj"
              , "model_premium"
              , "unity_premium"
              , "quoted_premium"
              , "technical_premium"
              , "technical_premium_pre_uw_adj"
              , "technical_premium_net"
              , "tpi"
              , "tpi_pre_uw_adj"
              , "pflr_att"
              , "pflr_cat"
              , "pflr"
              , "roc"
              , "uw_adj_impact"
              , "trifocus"
              , "expected_loss_cost"
              , "expected_loss_cost_pre_uw_adj"
              , "bpi_case_priced"
              , "pflr_pre_uw_adj"
              , "premium_label"
            ]}
            transpose
          />
        </HX.Pane>
      </HX.Section>



    </HX.Page>
  )
}

export { vw_actuarial };
