import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" fullWidth={false} viewScale={scale} shownBy="cds/show_page/show_other">
      <HX.Section title="Insured Details">
        <HX.Pane flow="right">
          <HX.Collection
            fields={[
              "insured_name",
              "inception_date",
              "policy_ref",
            ]}
            with="cds/rationale"
            title="Current Year"
          />
          <HX.Collection shownBy="cds/standard_fields/is_renewal"
            fields={[
              "cds/rationale/insured_name_expiry",
              "cds/rationale/inception_date_expiry",
              "cds/risk_info/policy_reference_exp",
            ]}
            title="Last Year"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Coverholder Background">
        <HX.Pane flow="right">
          <HX.Notes
            field={"coverholder_background"}
            title="Current Year"
            with="cds/rationale"
          />
          <HX.Notes shownBy="/cds/standard_fields/is_renewal"
            field={"coverholder_background_expiry"}
            title="Last Year"
            with="cds/rationale"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Risk Overview">
        <HX.Pane flow="right">
          <HX.Collection
            fields={[
              "risk_type",
              "construction",
              "signed_line",
              "limit",
              "deductions",
              "avg_limit",
              "top_country",
              null,
              "avg_model_rate",
              "avg_uw_rate",
              "epi",
              "rate_change",
              "attr_lr",
              "cat_load",
              null,
              "bpi",
              "tpi",
              "roc",
            ]}
            with="cds/rationale"
            title="Current Year"
          />
          <HX.Collection shownBy="/cds/standard_fields/is_renewal"
            fields={[
              "risk_type_expiry",
              "construction_expiry",
              "signed_line_expiry",
              "limit_expiry",
              "deductions_expiry",
              "avg_limit_expiry",
              "top_country_expiry",
              null,
              "avg_model_rate_expiry",
              "avg_uw_rate_expiry",
              "epi_expiry",
              "rate_change_expiry",
              "attr_lr_expiry",
              "cat_load_expiry",
              null,
              "bpi_expiry",
              "tpi_expiry",
              "roc_expiry",
            ]}
            with="cds/rationale"
            title="Last Year"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Underwriter Commentary">
        <HX.Pane flow="right">
          <HX.Notes
            field={"uw_comments"}
            title="Current Year"
            with="cds/rationale"
          />
          <HX.Notes shownBy="/cds/standard_fields/is_renewal"
            field={"uw_comments_expiry"}
            title="Last Year"
            with="cds/rationale"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Rate Change Rationale">
        <HX.Pane flow="right">
          <HX.Notes
            field={"rate_change_rationale"}
            title="Current Year"
            with="cds/rationale"
          />
          <HX.Notes shownBy="/cds/standard_fields/is_renewal"
            field={"rate_change_expiry_rationale"}
            title="Last Year"
            with="cds/rationale"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Terms and Conditions Change">
        <HX.Pane flow="right">
          <HX.Notes
            field={"tnc_change"}
            title="Current Year"
            with="cds/rationale"
          />
          <HX.Notes shownBy="/cds/standard_fields/is_renewal"
            field={"tnc_change_expiry"}
            title="Last Year"
            with="cds/rationale"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Risk Profile">
        <HX.Pane flow="right">
          <HX.Notes
            field={"risk_profile"}
            title="Current Year"
            with="cds/rationale"
          />
          <HX.Notes shownBy="/cds/standard_fields/is_renewal"
            field={"risk_profile_expiry"}
            title="Last Year"
            with="cds/rationale"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Territory Profile and Agg Distribution">
        <HX.Pane flow="right">
          <HX.Notes
            field={"territory_and_agg_dist"}
            title="Current Year"
            with="cds/rationale"
          />
          <HX.Notes shownBy="/cds/standard_fields/is_renewal"
            field={"territory_and_agg_dist_expiry"}
            title="Last Year"
            with="cds/rationale"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Exposure Change / Management">
        <HX.Pane flow="right">
          <HX.Notes
            field={"exposure_change"}
            title="Current Year"
            with="cds/rationale"
          />
          <HX.Notes shownBy="/cds/standard_fields/is_renewal"
            field={"exposure_change_expiry"}
            title="Last Year"
            with="cds/rationale"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Large Losses">
        <HX.Pane flow="right">
          <HX.Notes
            field={"large_losses"}
            title="Current Year"
            with="cds/rationale"
          />
          <HX.Notes shownBy="/cds/standard_fields/is_renewal"
            field={"large_losses_expiry"}
            title="Last Year"
            with="cds/rationale"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Generate Rationale Document">
        <HX.Pane>
          <HX.Button task="generate_rationale_doc_task" title="Generate Rationale Document" />
          <HX.File field="rationale_file" />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_rationale };