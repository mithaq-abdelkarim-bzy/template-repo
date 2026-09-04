//########### OUTSTANDING ########################
// Needs a shownby criteria 




import * as HX from "hx-model-components";

function vw_actuarial(scale) {
  return (
    <HX.Page title="Actuarial Info (typically hidden)" fullWidth={true} shownBy={"cds/show_hide/page/show_actuarial"}>



      <HX.Section title="Model State" defaultCollapsed={true}>
        <HX.Collection fields={["pressed_start_renewal_task", "show_landing_page", "show_after_landing_page", "show_rate_change"]} with="model_state" horizontal />
        <HX.Collection fields={["has_import_failed", "landing_page_info", null, null]} with="model_state" horizontal />
        <HX.Collection fields={["is_migrated", "not_migrated", "is_new", null]} with="model_state" horizontal />
        <HX.Collection fields={["show_rs_cvg", "show_rs_before_uw_adj", null, null]} with="model_state" horizontal />
        <HX.Collection fields={["show_rs_not_cvg_not_before_uw_adj", "show_rs_yes_cvg_not_before_uw_adj", "show_rs_not_cvg_yes_before_uw_adj", "show_rs_yes_cvg_yes_before_uw_adj"]} with="model_state" horizontal />

      </HX.Section>






      <HX.Section title="Countries Dataframe" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Table
            title="Complete List"
            maxListVisibleRows={15}
            data={["cds/exposure/granular/countries"]}
            fields={[
              "country"
              , "proxy_rating_country"
              , "rated_country"
              , "country_code_original"
              , "country_code"
              , "no_of_locations"
              , "pml"
              , "coverage"
              , "limit"
              , "excess"
              , "subcoverage"
              , "sublimit"
              , "deductible"
              , "total_sum_insured"
              , "bi_sum_insured"
              , "pd_sum_insured"
              , "liability_risk"
              , "attritional_risk"
              , "geog_risk"
              , "location_cat_risk"
              , "political"
              , "terrorism_raw"
              , "labour_strikes"
              , "protests_riots"
              , "interstate_war"
              , "civil_war"
              , "civil_unrest"
              , "war"
              , "terrorism"
              , "selected_sum_insured"
              , "warning"
              , "civil_unrest_roe_calculated"
              , "civil_unrest_roe_selected"
              , "war_roe_calculated"
              , "war_roe_selected"
              , "terrorism_roe_calculated"
              , "terrorism_roe_selected"
              , "civil_unrest_uw_adj"
              , "war_uw_adj"
              , "terrorism_uw_adj"
              , "override_civil_unrest"
              , "override_war"
              , "override_terrorism"
              , "selected_civil_unrest"
              , "selected_war"
              , "selected_terrorism"
              , "has_civil_unrest"
              , "has_war"
              , "has_terrorism"
              , "leading_peril"
              , "selected_sum_insured_contribution"
              , "country_cvg_subcvg"
              , "country_cvg_subcvg_live"
            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="ROE Dataframe" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Table
            title="Complete List"
            maxListVisibleRows={15}
            data={["cds/exposure/granular/roe"]}
            fields={[
              "country"
              , "no_of_locations"
              , "attritional_risk"
              , "geog_risk"
              , "location_cat_risk"
              , "total_sum_insured"
              , "bi_sum_insured"
              , "pd_sum_insured"
              , "civil_unrest"
              , "war"
              , "terrorism"
              , "coverage"
              , "coverage_code"
              , "subcoverage"
              , "subcoverage_code"
              , "selected_sum_insured"
              , "risk_multiplier"
              , "bi_terrorism_c"
              , "bi_terrorism_b"
              , "bi_civil_unrest_c"
              , "bi_civil_unrest_b"
              , "bi_war_c"
              , "bi_war_b"
              , "bi_terrorism_roe"
              , "bi_civil_unrest_roe"
              , "bi_war_roe"
              , "pd_terrorism_c"
              , "pd_terrorism_b"
              , "pd_civil_unrest_c"
              , "pd_civil_unrest_b"
              , "pd_war_c"
              , "pd_war_b"
              , "pd_terrorism_roe"
              , "pd_civil_unrest_roe"
              , "pd_war_roe"
              , "selected_terrorism_roe"
              , "selected_civil_unrest_roe"
              , "selected_war_roe"
              , "cvg_terrorism"
              , "cvg_civil_unrest"
              , "cvg_war"
              , "cvg_loading"
              , "subcvg_terrorism"
              , "subcvg_civil_unrest"
              , "subcvg_war"
              , "subcvg_loading"
              , "ihs_average_default"
              , "ihs_average_selected"
              , "bi_cvg_nl_roe"
              , "pd_cvg_nl_roe"
              , "total_cvg_nl_roe"
              , "bi_subcvg_nl_roe"
              , "pd_subcvg_nl_roe"
              , "total_subcvg_nl_roe"
              , "cvg_multiplier"
              , "subcvg_multiplier"
              , "nl_min_rol"
              , "liab_min_rol"

            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Curves Dataframe" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Table
            title="Complete List"
            maxListVisibleRows={15}
            data={["cds/exposure/granular/curves"]}
            fields={[
              "index"
              , "country_number"
              , "no_of_locations"
              , "location_number"
              , "country"
              , "pml"
              , "coverage"
              , "limit"
              , "excess"
              , "subcoverage"
              , "sublimit"
              , "deductible"
              , "total_sum_insured"
              , "bi_sum_insured"
              , "pd_sum_insured"
              , "selected_sum_insured"
              , "band"
              , "kth_smallest"
              , "decile"
              , "category"
              , "no_in_category"
              , "si_unscaled"
              , "si_scaled"
              , "si_scaled_2"
              , "liability_risk"
              , "attritional_risk"
              , "geog_risk"
              , "location_cat_risk"
              , "bi_cvg_nl_roe"
              , "bi_subcvg_nl_roe"
              , "pd_cvg_nl_roe"
              , "pd_subcvg_nl_roe"
              , "cvg_bi_rate_si"
              , "cvg_pd_rate_si"
              , "cvg_bi_mbbefd"
              , "cvg_pd_mbbefd"
              , "cvg_bi_base_premium"
              , "cvg_pd_base_premium"
              , "cvg_limit_usd"
              , "cvg_excess_usd"
              , "cvg_ilf_upper"
              , "cvg_ilf_lower"
              , "cvg_liab_base_premium"
              , "subcvg_bi_rate_si"
              , "subcvg_pd_rate_si"
              , "subcvg_bi_mbbefd"
              , "subcvg_pd_mbbefd"
              , "subcvg_bi_base_premium"
              , "subcvg_pd_base_premium"
              , "subcvg_sublimit_usd"
              , "subcvg_ilf_upper"
              , "subcvg_liab_base_premium"
              , "trapped_exposure"
            ]}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>



      <HX.Section title="Construction Dataframe" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.With context={{ "index": 0, "path": "cds/layers", "type": "list" }}>
            <HX.Table
              title="Complete List"
              data={["years"]}
              fields={[
                "year"
                , "end_date"
                , "build_up_calculated"
                , "build_up_override"
                , "build_up_selected"
                , "sum_insured"
                , "total_cvg_nl_roe"
                , "total_subcvg_nl_roe"
                , "cvg_expo_curve"
                , "subcvg_expo_curve"
                , "cvg_premium"
                , "subcvg_premium"
                , "total_premium"
                , "model_premium_pre_uw_adj"
                , "model_premium"
                , "benchmark_premium"
                , "model_premium_post_agg_adj"
              ]}
              kb-interactive
              dynamic
              with="coverages/construction"
            />
          </HX.With>
        </HX.Pane>
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
                // , "broker_contact"
                // , "product"
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



        <HX.With context={{ "index": 0, "path": "cds/layers", "type": "list" }}>

          <HX.Table
            title="cds - coverage fields"
            data={["coverages/property"
              , "coverages/property/bi"
              , "coverages/property/pd"
              , "coverages/property/policy_period"
              , "coverages/property/policy_period/bi"
              , "coverages/property/policy_period/pd"

              , "coverages/liability"
              , "coverages/liability/policy_period"

              , "coverages/construction"
              , "coverages/construction/policy_period"

              , "coverages/total"
              , "coverages/total/policy_period"
            ]}
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
        </HX.With>




      </HX.Section>



      <HX.Section title="Totals by Coverage Dataframe" defaultCollapsed={true}>
        <HX.Pane flow="right">

          <HX.With context={{ "index": 0, "path": "cds/layers", "type": "list" }}>
            <HX.Table
              title="Repeating Column Names - first Annual then Term"
              data={[
                "coverages/property"
                , "coverages/property/bi"
                , "coverages/property/pd"

                , "coverages/property/policy_period"
                , "coverages/property/policy_period/bi"
                , "coverages/property/policy_period/pd"

                , "coverages/liability"
                , "coverages/liability/policy_period"

                , "coverages/construction"
                , "coverages/construction/policy_period"

                , "coverages/total"
                , "coverages/total/policy_period"
              ]}
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
                , "status"
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
                , "model_premium_pre_uw_adj"
                , "model_rol_pre_uw_adj"
                , "model_rol"
                , "minimum_premium"
                , "minimum_rol"
                , "quoted_rol"
                , "quoted_roe"
                , "expected_loss_ratio"
                , "benchmark_premium_pre_uw_adj"
                , "expected_loss_ratio_pre_uw_adj"
                , "quoted_premium_annualised"
                , "benchmark_premium_annualised"
              ]}
              kb-interactive
              dynamic
              transpose
            />
          </HX.With>
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_actuarial };
