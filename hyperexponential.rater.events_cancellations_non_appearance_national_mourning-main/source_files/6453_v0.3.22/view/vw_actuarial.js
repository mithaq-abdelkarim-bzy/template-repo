import * as HX from "hx-model-components";
import { EC_COVERAGES } from "view/vw_constants";

function vw_actuarial(scale) {
  return (
    <HX.Page title="Actuarial Info (typically hidden)" fullWidth={true} shownBy={"model_state/show_page_actuarial"}>


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

        <HX.Button title="Load IHS Data" task="task_fetch_ihs_data" />


        <HX.Pane flow="right">
          <HX.Table
            title="IHS Outlook"
            data={["cds/ihs/ihs_detail"]}
            fields={[
              { field: 'country_code', maxWidth: 100 }
              , { field: 'risk_name', maxWidth: 250 }
              , { field: 'latest_outlook', maxWidth: 120 }
              , { field: 'latest_description', maxWidth: 500 }
              , { field: 'updated_on', maxWidth: 200 }
              , { field: 'value', maxWidth: 200 }
            ]}
            maxListVisibleRows={15}
            kb-interactive
            dynamic
          />
        </HX.Pane>
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



        <HX.Table
          title="Policy Table"
          data={["cds/experience_rating/policy_table"]}
          fields={[
            "policy_ref",
            "section_ref",
            "yoa",
            "coverage_name",
            "trifocus_name",
            "division",
            "settlement_fx",
            "index_bzly",
            "class_code",
            "bool_ec",
            "bool_na",

            "gnwp_bzly_usd",
            "incurred_bzly_usd",
            "gnwp_100_usd",
            "incurred_100_usd",
            "share_bzly",
            "rate_chg_init",
            "rate_chg",

            "fx_rate_usd_sett",
            "gnwp_bzly",
            "incurred_bzly",
            "gnwp_100",
            "incurred_100",

            "gnwp_bzly_scc",
            "incurred_bzly_scc",
            "gnwp_100_scc",
            "incurred_100_scc",
          ]}
          maxListVisibleRows={15}
          kb-interactive
          dynamic
        />



        <HX.Table
          title="Claim Table"
          data={["cds/experience_rating/claim_table"]}
          fields={[
            "policy_ref",
            "section_ref",
            "claim_ref",
            "trifocus_name",
            "division",
            "yoa",
            "settlement_fx",

            "cat_code_bzly",
            "cat_desc_bzly",
            "cat_code_mkt",
            "cat_desc_mkt",
            "cat_bzly_bool",

            "cause_of_loss",
            "bool_covid",
            "index_bzly",

            "class_code",
            "bool_ec",
            "bool_na",
            "bool_large",

            "incurred_bzly",
            "os_bzly",
            "incurred_100",
            "share_bzly",

            "incurred_bzly_scc",
            "os_bzly_scc",
            "incurred_100_scc",

            "incurred_100_scc_attr",
            "incurred_100_scc_large",
            "incurred_100_scc_cat",
          ]}
          maxListVisibleRows={15}
          kb-interactive
          dynamic
        />
      </HX.Section>


      <HX.Section title="Exposure Rating Dataframe - Event Cancellation" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Table
            title="Complete List"
            data={["cds/exposure/granular/event_cancel/events"]}
            fields={[
              "event_name",
              "country",
              "state",
              "date_start",
              "date_end",
              "tiv",
              "venue",
              "ihs_terrorism",
              "ihs_riots_and_civil_commotion",
              "ihs_strike",
              "ihs_war",
              "check",
              "country_code",
              "date_cover_start",
              "mths_diff",
              "venue_multiplier",
              "tiv_usd",
              "cap_tiv_usd",
              "m_terrorism",
              "c_terrorism",
              "m_riots_and_civil_commotion",
              "c_riots_and_civil_commotion",
              "m_strike",
              "c_strike",
              "m_war",
              "c_war",
              "base_rate_adverse_weather",
              "pat_adverse_weather",
              "base_rate_windstorm",
              "pat_windstorm",
              "base_rate_wildfire",
              "pat_wildfire",
              "base_rate_earthquake",
              "pat_earthquake",
              "season_adverse_weather",
              "season_windstorm",
              "season_wildfire",
              "nm_o75_sx",
              "nm_o75_sx_mod",
              "nm_u75_sx",
              "nm_sx",
              "nm_qx",
              "nm_qx_daily",
              "nm_u75_sx_mod",
              "nm_sx_mod",
              "nm_qx_mod",
              "nm_qx_daily_mod",
              "nm_death_rate",
              "nm_funeral_rate",
              "nm_mourning_rate",
              "nm_rate",
              "nm_death_rate_mod",
              "nm_funeral_rate_mod",
              "nm_mourning_rate_mod",
              "nm_rate_mod",
              "rate_all_risks",
              "rate_adverse_weather",
              "rate_windstorm",
              "rate_wildfire",
              "rate_earthquake",
              "rate_cyber",
              "rate_national_mourning",
              "rate_national_mourning_mod",
              "rate_terrorism",
              "rate_riots_and_civil_commotion",
              "rate_strike",
              "rate_war",
              "rate_catastrophic_non_app",
              "el_usd_total",
              "net_el_usd_total",
              "struct_pct_all_risks",
              "el_usd_all_risks",
              "net_el_usd_all_risks",
              "struct_pct_terrorism",
              "el_usd_terrorism",
              "net_el_usd_terrorism",
              "struct_pct_cyber",
              "el_usd_cyber",
              "net_el_usd_cyber",
              "struct_pct_national_mourning",
              "el_usd_national_mourning",
              "net_el_usd_national_mourning",
              "struct_pct_riots_and_civil_commotion",
              "el_usd_riots_and_civil_commotion",
              "net_el_usd_riots_and_civil_commotion",
              "struct_pct_strike",
              "el_usd_strike",
              "net_el_usd_strike",
              "struct_pct_war",
              "el_usd_war",
              "net_el_usd_war",
              "struct_pct_catastrophic_non_app",
              "el_usd_catastrophic_non_app",
              "net_el_usd_catastrophic_non_app",
              "struct_pct_adverse_weather",
              "el_usd_adverse_weather",
              "net_el_usd_adverse_weather",
              "struct_pct_windstorm",
              "el_usd_windstorm",
              "net_el_usd_windstorm",
              "struct_pct_wildfire",
              "el_usd_wildfire",
              "net_el_usd_wildfire",
              "struct_pct_earthquake",
              "el_usd_earthquake",
              "net_el_usd_earthquake",
              "el_usd_national_mourning_mod",
              "net_el_usd_national_mourning_mod"
            ]}
            kb-interactive
            dynamic
          />

        </HX.Pane>


      </HX.Section>


      <HX.Section title="Exposure Rating Dataframe - National Mourning" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Table
            title="Over 75s"
            data={["cds/exposure/granular/event_cancel/national_mourning/over_75"]}
            fields={[
              "label",
              "include",
              "name",
              "country",
              "gender",
              "date_of_birth",
              "age",
              "prob_die",
              "prob_live",
              "mod_affluence",
              "mod_health",
              "prob_die_mod",
              "prob_live_mod"

            ]}
            kb-interactive
            dynamic
          />

        </HX.Pane>


      </HX.Section>


      <HX.Section title="Experience Analysis" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Table
            title="Experience Analysis"
            data={[{ datum: "cds/experience_rating/analysis_table" },
            { datum: "cds/experience_rating/analysis_table_cy" },
            { datum: null },
            { datum: "cds/experience_rating/analysis_table_total" },
            { datum: null },
            { datum: "cds/experience_rating/analysis_table_total_included" }
            ]}
            fields={[
              "yoa",
              "yoa_label",
              "include",
              "tiv_calc",
              "tiv_ovd",
              "tiv",
              "gnwp_ol_dup",
              "total_ol_selected_ultimate_dup",
              "total_ol_selected_ulr_dup",
              "total_ol_selected_ult_to_tiv",
              "gnwp_nominal_calc",
              "gnwp_nominal_ovd",
              "gnwp_nominal",
              "attr_incurred_calc",
              "attr_incurred_ovd",
              "attr_incurred",
              "large_incurred_calc",
              "large_incurred_ovd",
              "large_incurred",
              "cat_incurred_calc",
              "cat_incurred_ovd",
              "cat_incurred",
              "rate_inc_calc",
              "rate_inc_ovd",
              "rate_inc",
              "rate_cum",
              "inf_inc_calc",
              "inf_inc_ovd",
              "inf_inc",
              "inf_cum",
              "attr_pct_ultimate_calc",
              "attr_pct_ultimate_ovd",
              "large_pct_ultimate_calc",
              "large_pct_ultimate_ovd",
              "cat_pct_ultimate_calc",
              "cat_pct_ultimate_ovd",
              "attr_ielr_calc",
              "attr_ielr_ovd",
              "large_ielr_calc",
              "large_ielr_ovd",
              "cat_ielr_calc",
              "cat_ielr_ovd",
              "gnwp_ol",
              "attr_ol_incurred",
              "large_ol_incurred",
              "cat_ol_incurred",
              "total_ol_incurred",
              "attr_pct_ultimate",
              "attr_method",
              "attr_ol_cl_ultimate",
              "attr_ol_bf_ultimate",
              "attr_ol_ielr_ultimate",
              "attr_ol_selected_ultimate",
              "attr_ol_cl_lr",
              "attr_ol_bf_lr",
              "attr_ol_ielr",
              "attr_ol_selected_ulr",
              "large_pct_ultimate",
              "large_method",
              "large_credibility",
              "large_ol_cl_ultimate",
              "large_ol_bf_ultimate",
              "large_ol_ielr_ultimate",
              "large_ol_selected_ultimate",
              "large_ol_cl_lr",
              "large_ol_bf_lr",
              "large_ol_ielr",
              "large_ol_selected_ulr",
              "cat_pct_ultimate",
              "cat_method",
              "cat_ol_cl_ultimate",
              "cat_ol_bf_ultimate",
              "cat_ol_ielr_ultimate",
              "cat_ol_selected_ultimate",
              "cat_ol_cl_lr",
              "cat_ol_bf_lr",
              "cat_ol_ielr",
              "cat_ol_selected_ulr",
              "total_pct_ultimate",
              "total_ol_cl_ultimate",
              "total_ol_bf_ultimate",
              "total_ol_ielr_ultimate",
              "total_ol_selected_ultimate",
              "total_ol_cl_lr",
              "total_ol_bf_lr",
              "total_ol_ielr",
              "total_ol_selected_ulr",
              "wgt_include",
              "wgt_decay",
              "wgt_exposure",
              "wgt_pct_ult",
              "wgt_overall_initial",
              "wgt_overall_final"
            ]}
            kb-interactive
            dynamic
          />

        </HX.Pane>


      </HX.Section>


      <HX.Section title="Layer Metric by coverage" defaultCollapsed={true}>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
          <HX.Pane flow="right">
            <HX.Table
              data={[
                null, { datum: "/cds/layers", maxWidth: 240, elementLabelBy: "rat_sum_label" },
                null, { datum: "na_total", maxWidth: 240 },
                null, { datum: "ec_total", maxWidth: 240 },
                null, ...EC_COVERAGES


              ]}

              fields={[
                "limit",
                "excess",
                "deductible",
                "aggregate_limit",
                "aggregate_excess",
                "aggregate_deductible",
                "currency",
                "section_reference",
                "brokerage",
                "written_line",
                "premium",
                "status",
                "benchmark_premium",
                "bpi",
                "bpi_pre_uw_adj",
                "model_premium",
                "unity_premium",
                "quoted_premium",
                "technical_premium",
                "technical_premium_pre_uw_adj",
                "technical_premium_net",
                "tpi",
                "tpi_pre_uw_adj",
                "pflr_att",
                "pflr_cat",
                "pflr",
                "roc",
                "uw_adj_impact",
                "trifocus",
                "expected_loss_cost",
                "expected_loss_cost_pre_uw_adj",
                "expected_loss_cost_100",
                "quoted_premium_net",
                "quoted_premium_net_100",
                "quoted_premium_100",
                "quoted_premium_annual",
                "quoted_premium_annual_100",
                "benchmark_premium_net",
                "benchmark_premium_net_100",
                "benchmark_premium_100",
                "benchmark_premium_annual",
                "benchmark_premium_annual_100",
                "benchmark_premium_pre_uw_adj",
                "technical_premium_100",
                "technical_premium_net_100",
                "pflr_pre_uw_adj",
                "bpi_case_priced",
                "premium_label",
                "technical_premium_pre_uw_adj_100",
                "technical_premium_annual_100",
                "technical_premium_annual",
                "expected_loss_cost_pre_uw_adj_100",
                "plan_premium_100",
                "plan_rol",
                "quoted_rol",
                "quoted_roe",
                "benchmark_rol",
                "technical_rol",
                "benchmark_rol_pre_uw_adj",
                "technical_rol_pre_uw_adj",
                "plan_premium_pre_uw_adj_100",
                "benchmark_premium_pre_uw_adj_100",
                "plan_rol_pre_uw_adj",
                "quoted_rol_pre_uw_adj",
                "loss_cost_layer_adj",
                "agg_adjustment",
                "loss_cost_layer_agg_adj",
                "uw_adjustment",
                "loss_cost_layer_agg_uw_adj",
                "experience_weight",
                "experience_loss_cost",
                "blended_loss_cost_no_uw_adj",
                "blended_loss_cost",

              ]}
              with="coverages"
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
