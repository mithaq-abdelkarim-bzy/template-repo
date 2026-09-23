import * as HX from "hx-model-components";

function vw_pricing(scale) {
  return (
    <HX.Page title="Pricing" fullWidth={true} viewScale={scale}>

      {/* This section sests out the different coverages for GMM and GLSN, these are just selections outside any layer or options note */}
      <HX.Section title="Coverage Selection" >
        <HX.Table shownBy="cds/gmm_masking"
          data={[{ datum: "cds/rating_factors/pricing/professional_liability", labelBy: "cds/rating_factors/pricing/professional_liability/label" },
          { datum: "cds/rating_factors/pricing/general_liability", labelBy: "cds/rating_factors/pricing/general_liability/label" },
            "cds/rating_factors/pricing/product_liability",
          { datum: "cds/rating_factors/pricing/eo", labelBy: "cds/rating_factors/pricing/eo/label" },
            "cds/rating_factors/pricing/sexual_abuse",
            "cds/rating_factors/pricing/employee_benefits_liability",
            "cds/rating_factors/pricing/employers_liability",
            "cds/rating_factors/pricing/tech_eo_products_media"]}
          fields={[
            // { field: "selection", labelAlign: "left" },
            { field: "include_primary", labelAlign: "left" },
            { field: "include_excess", labelAlign: "left" },
            { field: "claims_basis", labelAlign: "left" },
            { field: "retroactive_date", labelAlign: "left" },
          ]}
          title="Coverage Selection"
          filter="show_row"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/glsn_masking"
          data={["cds/rating_factors/pricing/product_liability",
            "cds/rating_factors/pricing/eo",
            "cds/rating_factors/pricing/healthcare_professional_liability",
            "cds/rating_factors/pricing/general_liability",
            "cds/rating_factors/pricing/sexual_abuse",
            "cds/rating_factors/pricing/employee_benefits_liability",
            "cds/rating_factors/pricing/product_recall",
            "cds/rating_factors/pricing/well_tech_eo_media"]}
          fields={[
            // { field: "selection", labelAlign: "left" },
            { field: "include_primary", labelAlign: "left" },
            { field: "include_excess", labelAlign: "left" },
            { field: "claims_basis", labelAlign: "left" },
            { field: "retroactive_date", labelAlign: "left" },
            { field: "significant_coverage", labelAlign: "left" },
          ]}
          title="Coverage Selection"
          filter="show_row"
          kb-interactive
          transpose
        />
      </HX.Section>

      <HX.Section title="Set Defaults and Copy Options">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Collection fields={["cds/default_retention", "cds/default_per_claim_limit", "cds/default_aggregate_limit"]} numCols={3} />
          </HX.Pane>

          <HX.Pane flow="right">
            <HX.Button task="set_defaults_button" title="Set Default Inputs" />
            <HX.Collection fields={[null]}></HX.Collection>
          </HX.Pane >
          {/* <HX.Pane flow="right">
            <HX.Collection fields={[null]}></HX.Collection>
          </HX.Pane > */}
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Collection fields={["cds/copy_option_from", "cds/copy_option_to", null]} numCols={3} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="pricing_copy_option" title="Copy Option" />
            <HX.Collection fields={[null]}></HX.Collection>
          </HX.Pane >
          {/* <HX.Pane flow="right">
            <HX.Collection fields={[null]}></HX.Collection>
          </HX.Pane > */}
        </HX.Pane>

      </HX.Section>

      {/* This section gives the limits and retentions for each coverage (GMM) if it is selected - Primary Coverage only */}
      <HX.Section title="Coverage Details" shownBy="cds/gmm_masking" >
        <HX.Table shownBy="cds/rating_factors/pricing/professional_liability/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/professional_liability/retention", labelAlign: "left" },
          { field: "coverages/professional_liability/per_claim_limit", labelAlign: "left" },
          { field: "coverages/professional_liability/aggregate_limit", labelAlign: "left" },]}
          title="Professional Liability"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/general_liability/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/general_liability/retention", labelAlign: "left" },
          { field: "coverages/general_liability/per_claim_limit", labelAlign: "left" },
          { field: "coverages/general_liability/aggregate_limit", labelAlign: "left" },]}
          title="General Liability"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/product_liability/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/product_liability/retention", labelAlign: "left" },
          { field: "coverages/product_liability/per_claim_limit", labelAlign: "left" },
          { field: "coverages/product_liability/aggregate_limit", labelAlign: "left" },]}
          title="Product Liability"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/eo/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/eo/retention", labelAlign: "left" },
          { field: "coverages/eo/per_claim_limit", labelAlign: "left" },
          { field: "coverages/eo/aggregate_limit", labelAlign: "left" },]}
          title="E&O"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/sexual_abuse/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/sexual_abuse/retention", labelAlign: "left" },
          { field: "coverages/sexual_abuse/per_claim_limit", labelAlign: "left" },
          { field: "coverages/sexual_abuse/aggregate_limit", labelAlign: "left" },]}
          title="Sexual Abuse"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/employee_benefits_liability/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/employee_benefits_liability/retention", labelAlign: "left" },
          { field: "coverages/employee_benefits_liability/per_claim_limit", labelAlign: "left" },
          { field: "coverages/employee_benefits_liability/aggregate_limit", labelAlign: "left" },]}
          title="Employee Benefits Liability"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/employers_liability/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/employers_liability/retention", labelAlign: "left" },
          { field: "coverages/employers_liability/per_claim_limit", labelAlign: "left" },
          { field: "coverages/employers_liability/aggregate_limit", labelAlign: "left" },]}
          title="Employers Liability"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/tech_eo_products_media/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/tech_eo_products_media/retention", labelAlign: "left" },
          { field: "coverages/tech_eo_products_media/per_claim_limit", labelAlign: "left" },
          { field: "coverages/tech_eo_products_media/aggregate_limit", labelAlign: "left" },]}
          title="Tech E&O/Products/Media"
          kb-interactive
          transpose
        />
      </HX.Section>

      {/* This section gives the limits and retentions for each coverage (GLSN) if it is selected - Primary Coverage only */}
      <HX.Section title="Coverage Details" shownBy="cds/glsn_masking" >
        <HX.Table shownBy="cds/rating_factors/pricing/product_liability/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/product_liability/retention", labelAlign: "left" },
          { field: "coverages/product_liability/per_claim_limit", labelAlign: "left" },
          { field: "coverages/product_liability/aggregate_limit", labelAlign: "left" },]}
          title="Product Liability"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/eo/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/eo/retention", labelAlign: "left" },
          { field: "coverages/eo/per_claim_limit", labelAlign: "left" },
          { field: "coverages/eo/aggregate_limit", labelAlign: "left" },]}
          title="E&O"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/healthcare_professional_liability/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/healthcare_professional_liability/retention", labelAlign: "left" },
          { field: "coverages/healthcare_professional_liability/per_claim_limit", labelAlign: "left" },
          { field: "coverages/healthcare_professional_liability/aggregate_limit", labelAlign: "left" },]}
          title="Healthcare Professional Liability"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/general_liability/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/general_liability/retention", labelAlign: "left" },
          { field: "coverages/general_liability/per_claim_limit", labelAlign: "left" },
          { field: "coverages/general_liability/aggregate_limit", labelAlign: "left" },]}
          title="General Liability"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/sexual_abuse/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/sexual_abuse/retention", labelAlign: "left" },
          { field: "coverages/sexual_abuse/per_claim_limit", labelAlign: "left" },
          { field: "coverages/sexual_abuse/aggregate_limit", labelAlign: "left" },]}
          title="Sexual Abuse"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/employee_benefits_liability/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/employee_benefits_liability/retention", labelAlign: "left" },
          { field: "coverages/employee_benefits_liability/per_claim_limit", labelAlign: "left" },
          { field: "coverages/employee_benefits_liability/aggregate_limit", labelAlign: "left" },]}
          title="Employee Benefits Liability"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/product_recall/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/product_recall/retention", labelAlign: "left" },
          { field: "coverages/product_recall/per_claim_limit", labelAlign: "left" },
          { field: "coverages/product_recall/aggregate_limit", labelAlign: "left" },]}
          title="Product Recall Expenses"
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/rating_factors/pricing/well_tech_eo_media/include_primary"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "coverages/well_tech_eo_media/retention", labelAlign: "left" },
          { field: "coverages/well_tech_eo_media/per_claim_limit", labelAlign: "left" },
          { field: "coverages/well_tech_eo_media/aggregate_limit", labelAlign: "left" },]}
          title="Well Tech E&O and Media"
          kb-interactive
          transpose
        />
      </HX.Section>

      {/* This section is for any policy aggregates that apply */}
      <HX.Section title="Policy Aggregates" >
        <HX.Table shownBy="cds/gmm_masking"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "agg_limit", labelAlign: "left" },
          { field: "indemnity_only", shownBy: "cds/international_masking", labelAlign: "left" }]}
          kb-interactive
          transpose
        />
        <HX.Table shownBy="cds/glsn_masking"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "agg_retention", labelAlign: "left" },
          { field: "agg_limit", labelAlign: "left" },
          { field: "indemnity_only", shownBy: "cds/international_masking", labelAlign: "left" }]}
          kb-interactive
          transpose
        />
      </HX.Section>

      {/* This section is for coverage enhancements to be added */}
      <HX.Section title="Coverage Enhancements - Primary" >
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "include_stop_gap_primary", shownBy: "cds/us_masking", labelAlign: "left" },
          { field: "include_tria_primary", shownBy: "cds/us_masking", labelAlign: "left" },
          { field: "include_punitive_damages_primary", shownBy: "/cds/punitive_damages_masking", labelAlign: "left" },]}
          kb-interactive
          transpose
        />
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[
            { field: "include_costs_in_addition_primary", labelAlign: "left" },
            { field: "costs_in_addition_selection", labelAlign: "left" }]}
          kb-interactive
          transpose
        />
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "include_auto_primary", labelAlign: "left" },
          { field: "auto_measure", labelAlign: "left" },
          { field: "auto_amount", labelAlign: "left" }]}
          kb-interactive
          transpose
        />
      </HX.Section>

      <HX.Section title="Coverage Enhancements - Excess">
        <HX.Pane flow="right" >
          <HX.Collection
            fields={[
              { field: "cds/rating_factors/pricing/include_stop_gap_excess", shownBy: "cds/us_masking" },
              { field: "cds/rating_factors/pricing/include_tria_excess", shownBy: "cds/us_masking" },
              { field: "cds/rating_factors/pricing/include_punitive_damages_excess", shownBy: "/cds/punitive_damages_masking" },
              "cds/rating_factors/pricing/include_costs_in_addition_excess", "cds/rating_factors/pricing/include_auto_excess"
            ]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      {/* The primary layer outputs based on the inputs above*/}
      <HX.Section title="Primary Layer" >
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "brokerage_primary", labelAlign: "left" },
          { field: "cyber_premium_primary", labelAlign: "left" },
          // "uplift_for_nmp_primary",
          { field: "model_premium_primary", labelAlign: "left" },
          { field: "minimum_premium_primary", labelAlign: "left" },
          { field: "gross_premium_primary", labelAlign: "left" },
          { field: "quoted_premium_primary", labelAlign: "left" },
          { field: "bpi_primary", labelAlign: "left" }]}
          kb-interactive
          transpose
        />
        <HX.Pane flow="right">
          <HX.Collection
            fields={["cds/add_excess_1"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

      </HX.Section>

      {/* This section sets out the different excess options*/}
      <HX.Section title="Excess Layers" shownBy="cds/add_excess_1">
        <HX.Pane flow="right">
          <HX.Collection
            fields={["cds/rating_factors/pricing/claims_basis_1_excess", "cds/rating_factors/pricing/retroactive_date_1_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_1_excess", labelAlign: "left" },
          { field: "aggregate_limit_1_excess", labelAlign: "left" },
          { field: "brokerage_1_excess", labelAlign: "left" },
          { field: "supported_excess_premium_1_excess", labelAlign: "left" },
          { field: "umbrella_premium_1_excess", labelAlign: "left" },
          // "uplift_for_nmp_1_excess",
          { field: "model_premium_1_excess", labelAlign: "left" },
          { field: "minimum_premium_1_excess", labelAlign: "left" },
          { field: "gross_premium_1_excess", labelAlign: "left" },
          { field: "quoted_premium_1_excess", labelAlign: "left" },
          { field: "bpi_1_excess", labelAlign: "left" },
          { field: "comment_1_excess", labelAlign: "left" },]}
          title="1st Excess Layer"
          kb-interactive
          transpose
        />
        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/add_excess_1"
            fields={["cds/add_excess_2"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_2"
            fields={["cds/rating_factors/pricing/claims_basis_2_excess", "cds/rating_factors/pricing/retroactive_date_2_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Table shownBy="cds/add_excess_2"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_2_excess", labelAlign: "left" },
          { field: "aggregate_limit_2_excess", labelAlign: "left" },
          { field: "brokerage_2_excess", labelAlign: "left" },
          { field: "supported_excess_premium_2_excess", labelAlign: "left" },
          { field: "umbrella_premium_2_excess", labelAlign: "left" },
          // { field: "uplift_for_nmp_2_excess", labelAlign: "left" },
          { field: "model_premium_2_excess", labelAlign: "left" },
          { field: "minimum_premium_2_excess", labelAlign: "left" },
          { field: "gross_premium_2_excess", labelAlign: "left" },
          { field: "quoted_premium_2_excess", labelAlign: "left" },
          { field: "bpi_2_excess", labelAlign: "left" },
          { field: "comment_2_excess", labelAlign: "left" },]}
          title="2nd Excess Layer"
          kb-interactive
          transpose
        />

        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/add_excess_2"
            fields={["cds/add_excess_3"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_3"
            fields={["cds/rating_factors/pricing/claims_basis_3_excess", "cds/rating_factors/pricing/retroactive_date_3_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Table shownBy="cds/add_excess_3"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_3_excess", labelAlign: "left" },
          { field: "aggregate_limit_3_excess", labelAlign: "left" },
          { field: "brokerage_3_excess", labelAlign: "left" },
          { field: "supported_excess_premium_3_excess", labelAlign: "left" },
          { field: "umbrella_premium_3_excess", labelAlign: "left" },
          // "uplift_for_nmp_3_excess",
          { field: "model_premium_3_excess", labelAlign: "left" },
          { field: "minimum_premium_3_excess", labelAlign: "left" },
          { field: "gross_premium_3_excess", labelAlign: "left" },
          { field: "quoted_premium_3_excess", labelAlign: "left" },
          { field: "bpi_3_excess", labelAlign: "left" },
          { field: "comment_3_excess", labelAlign: "left" },]}
          title="3rd Excess Layer"
          kb-interactive
          transpose
        />

        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_3"
            fields={["cds/add_excess_4"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_4"
            fields={["cds/rating_factors/pricing/claims_basis_4_excess", "cds/rating_factors/pricing/retroactive_date_4_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Table shownBy="cds/add_excess_4"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_4_excess", labelAlign: "left" },
          { field: "aggregate_limit_4_excess", labelAlign: "left" },
          { field: "brokerage_4_excess", labelAlign: "left" },
          { field: "supported_excess_premium_4_excess", labelAlign: "left" },
          { field: "umbrella_premium_4_excess", labelAlign: "left" },
          // "uplift_for_nmp_4_excess",
          { field: "model_premium_4_excess", labelAlign: "left" },
          { field: "minimum_premium_4_excess", labelAlign: "left" },
          { field: "gross_premium_4_excess", labelAlign: "left" },
          { field: "quoted_premium_4_excess", labelAlign: "left" },
          { field: "bpi_4_excess", labelAlign: "left" },
          { field: "comment_4_excess", labelAlign: "left" },]}
          title="4th Excess Layer"
          kb-interactive
          transpose
        />


        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/add_excess_4"
            fields={["cds/add_excess_5"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>


        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_5"
            fields={["cds/rating_factors/pricing/claims_basis_5_excess", "cds/rating_factors/pricing/retroactive_date_5_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Table shownBy="cds/add_excess_5"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_5_excess", labelAlign: "left" },
          { field: "aggregate_limit_5_excess", labelAlign: "left" },
          { field: "brokerage_5_excess", labelAlign: "left" },
          { field: "supported_excess_premium_5_excess", labelAlign: "left" },
          { field: "umbrella_premium_5_excess", labelAlign: "left" },
          // "uplift_for_nmp_5_excess",
          { field: "model_premium_5_excess", labelAlign: "left" },
          { field: "minimum_premium_5_excess", labelAlign: "left" },
          { field: "gross_premium_5_excess", labelAlign: "left" },
          { field: "quoted_premium_5_excess", labelAlign: "left" },
          { field: "bpi_5_excess", labelAlign: "left" },
          { field: "comment_5_excess", labelAlign: "left" },]}
          title="5th Excess Layer"
          kb-interactive
          transpose
        />

        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/add_excess_5"
            fields={["cds/add_excess_6"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>


        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_6"
            fields={["cds/rating_factors/pricing/claims_basis_6_excess", "cds/rating_factors/pricing/retroactive_date_6_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Table shownBy="cds/add_excess_6"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_6_excess", labelAlign: "left" },
          { field: "aggregate_limit_6_excess", labelAlign: "left" },
          { field: "brokerage_6_excess", labelAlign: "left" },
          { field: "supported_excess_premium_6_excess", labelAlign: "left" },
          { field: "umbrella_premium_6_excess", labelAlign: "left" },
          // "uplift_for_nmp_6_excess",
          { field: "model_premium_6_excess", labelAlign: "left" },
          { field: "minimum_premium_6_excess", labelAlign: "left" },
          { field: "gross_premium_6_excess", labelAlign: "left" },
          { field: "quoted_premium_6_excess", labelAlign: "left" },
          { field: "bpi_6_excess", labelAlign: "left" },
          { field: "comment_6_excess", labelAlign: "left" },]}
          title="6th Excess Layer"
          kb-interactive
          transpose
        />

        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/add_excess_6"
            fields={["cds/add_excess_7"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>


        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_7"
            fields={["cds/rating_factors/pricing/claims_basis_7_excess", "cds/rating_factors/pricing/retroactive_date_7_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>


        <HX.Table shownBy="cds/add_excess_7"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_7_excess", labelAlign: "left" },
          { field: "aggregate_limit_7_excess", labelAlign: "left" },
          { field: "brokerage_7_excess", labelAlign: "left" },
          { field: "supported_excess_premium_7_excess", labelAlign: "left" },
          { field: "umbrella_premium_7_excess", labelAlign: "left" },
          // "uplift_for_nmp_7_excess",
          { field: "model_premium_7_excess", labelAlign: "left" },
          { field: "minimum_premium_7_excess", labelAlign: "left" },
          { field: "gross_premium_7_excess", labelAlign: "left" },
          { field: "quoted_premium_7_excess", labelAlign: "left" },
          { field: "bpi_7_excess", labelAlign: "left" },
          { field: "comment_7_excess", labelAlign: "left" },]}
          title="7th Excess Layer"
          kb-interactive
          transpose
        />

        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/add_excess_7"
            fields={["cds/add_excess_8"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_8"
            fields={["cds/rating_factors/pricing/claims_basis_8_excess", "cds/rating_factors/pricing/retroactive_date_8_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Table shownBy="cds/add_excess_8"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_8_excess", labelAlign: "left" },
          { field: "aggregate_limit_8_excess", labelAlign: "left" },
          { field: "brokerage_8_excess", labelAlign: "left" },
          { field: "supported_excess_premium_8_excess", labelAlign: "left" },
          { field: "umbrella_premium_8_excess", labelAlign: "left" },
          // "uplift_for_nmp_8_excess",
          { field: "model_premium_8_excess", labelAlign: "left" },
          { field: "minimum_premium_8_excess", labelAlign: "left" },
          { field: "gross_premium_8_excess", labelAlign: "left" },
          { field: "quoted_premium_8_excess", labelAlign: "left" },
          { field: "bpi_8_excess", labelAlign: "left" },
          { field: "comment_8_excess", labelAlign: "left" },]}
          title="8th Excess Layer"
          kb-interactive
          transpose
        />

        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/add_excess_8"
            fields={["cds/add_excess_9"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_9"
            fields={["cds/rating_factors/pricing/claims_basis_9_excess", "cds/rating_factors/pricing/retroactive_date_9_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Table shownBy="cds/add_excess_9"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_9_excess", labelAlign: "left" },
          { field: "aggregate_limit_9_excess", labelAlign: "left" },
          { field: "brokerage_9_excess", labelAlign: "left" },
          { field: "supported_excess_premium_9_excess", labelAlign: "left" },
          { field: "umbrella_premium_9_excess", labelAlign: "left" },
          // "uplift_for_nmp_9_excess",
          { field: "model_premium_9_excess", labelAlign: "left" },
          { field: "minimum_premium_9_excess", labelAlign: "left" },
          { field: "gross_premium_9_excess", labelAlign: "left" },
          { field: "quoted_premium_9_excess", labelAlign: "left" },
          { field: "bpi_9_excess", labelAlign: "left" },
          { field: "comment_9_excess", labelAlign: "left" },]}
          title="9th Excess Layer"
          kb-interactive
          transpose
        />

        <HX.Pane flow="right">
          <HX.Collection shownBy="cds/add_excess_9"
            fields={["cds/add_excess_10"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>


        <HX.Pane flow="right" >
          <HX.Collection shownBy="cds/add_excess_10"
            fields={["cds/rating_factors/pricing/claims_basis_10_excess", "cds/rating_factors/pricing/retroactive_date_10_excess"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Table shownBy="cds/add_excess_10"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[{ field: "per_claim_limit_10_excess", labelAlign: "left" },
          { field: "aggregate_limit_10_excess", labelAlign: "left" },
          { field: "brokerage_10_excess", labelAlign: "left" },
          { field: "supported_excess_premium_10_excess", labelAlign: "left" },
          { field: "umbrella_premium_10_excess", labelAlign: "left" },
          // "uplift_for_nmp_10_excess",
          { field: "model_premium_10_excess", labelAlign: "left" },
          { field: "minimum_premium_10_excess", labelAlign: "left" },
          { field: "gross_premium_10_excess", labelAlign: "left" },
          { field: "quoted_premium_10_excess", labelAlign: "left" },
          { field: "bpi_10_excess", labelAlign: "left" },
          { field: "comment_10_excess", labelAlign: "left" },]}
          title="10th Excess Layer"
          kb-interactive
          transpose
        />
      </HX.Section>

      <HX.Section title="Selected Option">
        <HX.Pane flow="right">
          <HX.Collection
            fields={["cds/option_selected"]} horizontal />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_pricing };
