import * as HX from "hx-model-components";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">

      <HX.Section title="General Details">
        <HX.Pane flow="right" >

          <HX.Collection
            fields={[
              "project_name", "target_name", "transaction_value", "total_limit", "total_limit_percentage", "brokerage"
            ]} with="cds/policy_info" />
          <HX.Collection
            fields={[
              "policyholder", "buyer_name", "buyer_lawyer", "seller_name", "seller_lawyer"
            ]} with="cds/policy_info" />
          <HX.Collection
            fields={[
              "uw_expenses_flag", "uw_expenses", "distressed_business_flag"
            ]} with="cds/policy_info" />

        </HX.Pane>
      </HX.Section>

      <HX.Section title="Frequency Selections">
        <HX.Pane >

          <HX.Table kb-interactive transpose
            data={["cds/rating_factors/freq/target", "cds/rating_factors/freq/buyer"]}
            fields={["jurisdiction", "industry", "business_nature"/*, "ihs_enforcement"*/]} />

          <HX.Collection
            fields={["default_score", "freq_adjustment", "freq_adjusted"]}
            with="cds/rating_factors/freq"
            horizontal />

        </HX.Pane>
      </HX.Section>

      <HX.Section title="Severity Selections">
        <HX.Pane >

          <HX.Table kb-interactive
            with="cds/rating_factors/sev"
            data={["due_diligence", "disclosure", "general_warranties", "tax_warranties"]}
            fields={["coverage_flag", "severity_assessment", "adjustment", "term", "term_modifier", "comment"]} />

          <HX.Collection
            fields={["modified_score", "div_flag", "volatility", "multiple"]}
            with="cds/rating_factors/sev"
            horizontal />

        </HX.Pane>
      </HX.Section>


      <HX.Section title="Fundamental Top Up Coverage">
        <HX.Collection fields={["cds/policy_info/fundamental_top_up_flag"]} />
        <HX.Pane >
          <HX.Table
            with="cds/rating_factors"
            data={["fun_top_up"]}
            fields={["base_rate", "adjustment", "term", "comment"]}
            shownBy="/cds/policy_info/fundamental_top_up_flag"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_exposure_details };