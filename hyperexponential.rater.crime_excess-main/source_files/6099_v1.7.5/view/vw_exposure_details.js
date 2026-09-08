/* eslint-disable */
import * as HX from "hx-model-components";

function vw_exposure_details() {
  return (
    <HX.Page title="Exposure Details" fullWidth shownBy="model_state/show_after_landing_page" >
      <HX.Section title="General Inputs">
        <HX.Pane>
          <HX.Collection fields={["cds/standard_fields/insured_state_or_province", "cds/rating_factors/claim_basis", null]} horizontal />
          <HX.Collection fields={["code", "industry_group", "industry"]} horizontal with="/cds/key_industry" />
          <HX.Collection fields={[null, "entity_type", "excess_factor"]} horizontal with="/cds" />
          <HX.Collection fields={["revenue", "assets", "employees", "locations"]} with="/cds/exposure/aggregate" horizontal title="Company Information" />
          {/*        
          <HX.Collection fields={["has_social_engineering", "has_other_coverages", "rating_factors/endt_extensions"]}
            with="/cds" horizontal title="Additional Coverages" syncColumnWidthsKey="GenInputs" />
          <HX.Collection fields={[
            "sublimited_perils",
            { field: "other_on_premises", shownBy: "/cds/has_other_coverages" },
            { field: "other_off_premises", shownBy: "/cds/has_other_coverages" }]}
            with="/cds/rating_factors" horizontal syncColumnWidthsKey="GenInputs" /> */}
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Program Schedule">
        <HX.Pane>
          <HX.Table kb-interactive
            fields={[
              "limit",
              "excess",
              // { field: "limit_social_engineering", shownBy: "cds/has_social_engineering" },
              // // { field: "excess_social_engineering", shownBy: "cds/has_social_engineering" },
              // { field: "limit_other_cov", shownBy: "cds/has_other_coverages" },
              // // { field: "excess_other_cov", shownBy: "cds/has_other_coverages" },
              // "layer_quality",
              "lead_underwriter",
              "participating_cosurety",
              "premium",
              "lead_percentage",
              "rate_per_m",
              "percent_underlying_rate"
            ]}
            data={[
              { datum: "cds/retention" },
              { datum: "cds/layers", elementLabelBy: "layer_label" }
            ]}
            freezeLeft={1}
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Collection title="Selected Layer" fields={["beazley_layer", "beazley_share", "is_follow"]} with="cds" horizontal />
          <HX.Collection fields={["total_layer_limit", "beazley_limit", "beazley_pre_layer"]} with="cds" horizontal />
          <HX.Collection fields={["underlying_layer_limit", "underlying_premium", "underlying_rate_per_m"]} with="cds" horizontal />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Term Adjustment">
        <HX.Pane>
          <HX.Collection fields={[
            { field: "cds/underlying_inception_date", infoBy: "info_date" },
            { field: "cds/underlying_expiry_date", infoBy: "info_date" },
            "cds/term_adjustment_underlying"]} horizontal />
        </HX.Pane>
      </HX.Section>
      {/* Remove section on ESE when switching to new benchmark calcs */}
      <HX.Section title="Excess Social Engineering">
        <HX.Pane>
          <HX.Collection fields={["social_engineering_sublimit", "social_engineering_limit", "social_engineering_allocation"]} with="cds" horizontal />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_exposure_details };
