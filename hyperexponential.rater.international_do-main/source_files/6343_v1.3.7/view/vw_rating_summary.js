import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} viewScale={scale} shownBy="cds/risk_information/not_mmp_flag">
      {/* <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section> */}
      <HX.Section title="Risk Summary">
        <HX.Pane flow="right">
          <HX.Pane >
            <HX.Table
              data={[{ datum: "cds", width: 400 }]}
              fields={[
                "standard_fields/insured_name.read_only",
                { field: "currencies/source_currency.read_only" },
                { field: "exposure/aggregate/exposure_currency.read_only", shownBy: "cds/risk_information/private_flag" },
                { field: "exposure/aggregate/market_cap_2_year_high.read_only", shownBy: "cds/risk_information/public_flag" },
                { field: "exposure/aggregate/total_assets.read_only", shownBy: "cds/risk_information/private_flag" },
                "rating_factors/risk_information/industry_class_sic_code.read_only",
                "rating_factors/risk_information/ownership_type.read_only",
                "exposure/aggregate/us_listing_share.read_only",
                null,
                "rating_factors/risk_information/country_of_domicile.read_only",
                "rating_factors/risk_information/main_operating_country.read_only",
              ]}
              transpose
              kb-interactive
              rowHeaderSettings={{ width: 200 }}
            />


          </HX.Pane>

          <HX.Pane >
            <HX.Pane>
              <HX.Table title="Side A"
                data={["side_a_fifty_percentile", "side_a_seventyfive_percentile"]}
                fields={[
                  { field: "inclusive_dismissals", width: 150 },
                  { field: "at_cost_only", width: 150 }
                ]}
                rowHeaderSettings={{ width: 150 }}
                with="cds/rating_summary"
                kb-interactive
                syncColumnWidthsKey="SyncTable1" />

              <HX.Collection
                fields={["side_a_sca_freq"]}
                with="cds/rating_summary"
                horizontal
                syncColumnWidthsKey="SyncTable1" />
            </HX.Pane>

            <HX.Pane>
              <HX.Table title="Side AB/ABC"
                data={["side_abc_fifty_percentile", "side_abc_seventyfive_percentile"]}
                fields={
                  [
                    { field: "inclusive_dismissals", width: 150 },
                    { field: "at_cost_only", width: 150 }
                  ]}
                rowHeaderSettings={{ width: 150 }}
                with="cds/rating_summary"
                kb-interactive
                syncColumnWidthsKey="SyncTable1" />

              <HX.Collection
                fields={["side_abc_sca_freq"]}
                with="cds/rating_summary"
                horizontal
                syncColumnWidthsKey="SyncTable1" />
            </HX.Pane>
          </HX.Pane>





        </HX.Pane>
      </HX.Section>

      <HX.Section title="Layer Options" >
        <HX.Table
          title="Programme Structure"
          data={[{ datum: "cds/large_cap/layers" }]}
          fields={[
            { field: "side_selection", width: 150 },
            { field: "side_ab_discount", width: 150 },
            { field: "uw_side_ab_discount_override", infoBy: "cds/labels/uw_side_ab_discount_override_info", width: 150 },
            null,
            { field: "limit", width: 150 },
            { field: "excess", width: 150 },
            { field: "deductible", width: 150 },
            null,
            { field: "quoted_premium_100", width: 150 },
            { field: "brokerage", width: 150 },
            null,
            { field: "written_line", infoBy: "cds/labels/beazley_market_share_info", width: 150 },
            { field: "section_reference", infoBy: "cds/labels/section_reference_info", width: 150 },
            { field: "notes", width: 150 },
            { field: "slip_leader", shownBy: "/cds/validation/slip_leader/valid", width: 150 },
            { field: "slip_leader.notSupported", infoBy: "/cds/validation/slip_leader/info_text", shownBy: "/cds/validation/slip_leader/invalid", width: 150 },
            { field: "status", width: 150 },
            { field: "cover_in_uw_authority", width: 150 },
            { field: "signoff_obtained", width: 150 },
          ]}
          freezeLeft={0}
          syncColumnWidthsKey="TableSync"
          kb-interactive
        />
      </HX.Section>

      <HX.Section title="Layer Results">
        <HX.Pane flow="right">
          <HX.Notes field="cds/labels/premium_and_costs_info" />
          <HX.Pane>

          </HX.Pane>
        </HX.Pane>

        <HX.Table
          title="Modelled Premium and Costs"
          data={[{ datum: "cds/large_cap/layers" }]}
          fields={[
            "technical_premium",
            "technical_premium_pre_uw_adj",
            "benchmark_premium",
            null,
            "tpi",
            "tpi_pre_uw_adj",
            "bpi",
            null,
            "expected_loss_cost_att",
            "expected_loss_cost_cat",
            null,
            "adr_standalone",
            "contagion",
            "intl_standalone",
            "intl_large_company",
            "expected_loss_cost",
            "pflr",
            "roc"
            // "implied_ilf"
          ]}
          freezeLeft={0}
          syncColumnWidthsKey="TableSync"
          kb-interactive
        />
      </HX.Section>

      <HX.Section title="Premium Build-Up Graphs">

        <HX.Pane >
          <HX.Pane>
            <HX.Collection fields={[
              "cds/prem_build_up/selected_option",
              null]}
              numCols={2}
            />
            <HX.CategoryChart
              data={['technical_premium', 'benchmark_premium', 'bound_premium']}
              fields={['gross_att_graph', 'gross_cat_graph', 'cost_ri_graph', 'expenses_graph', 'profit_load_graph', 'brokerage_graph', 'bound_premium_graph']}
              columnType="stack"
              title="Premium Build-Up"
              primaryAxis={{ label: "Premium Build-Up" }}
              with="cds/prem_build_up"
            />

          </HX.Pane>


        </HX.Pane>

      </HX.Section>

    </HX.Page >

  )
}


export { vw_rating_summary };