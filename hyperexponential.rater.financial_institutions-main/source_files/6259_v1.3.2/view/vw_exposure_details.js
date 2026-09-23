import * as HX from "hx-model-components";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" shownBy="/non_cds/exposure_details/regions/show" viewScale={scale}>
      <HX.Section title="Client Information" shownBy="/non_cds/exposure_details/client_info_show">
        <HX.Collection fields={[
          { field: "no_of_locations", shownBy: "/non_cds/exposure_details/no_of_locations_show" },
          { field: "currency", shownBy: "/non_cds/exposure_details/regions/show" },
          null
        ]} with="cds/rating_factors/exposure_details" horizontal syncColumnWidthsKey="client_info" />
        <HX.Collection fields={[
          "main_listing",
          "ipo_date",
          "/cds/exposure/aggregate/market_cap",
          "us_listing",
          { field: "/cds/exposure/aggregate/market_cap_us", shownBy: "/non_cds/exposure_details/market_cap_us_show" }
        ]} shownBy="/non_cds/exposure_details/client_info_public_show" with="cds/rating_factors/exposure_details" numCols={3} syncColumnWidthsKey="client_info" />
      </HX.Section>
      <HX.Section title="Exposure Details" shownBy="non_cds/exposure_details/exposure_details_show">
        <HX.Collection fields={["total_amounts/aum"]} shownBy="/non_cds/exposure_details/total_aum_show" with="cds/exposure/aggregate" syncColumnWidthsKey="client_info" />
        <HX.Table data={[
          "aggregate/total_amounts",
          null,
          "granular/regions/splits_entered_as"
        ]} fields={[
          "employees",
          "revenues",
          "assets"
        ]} shownBy="/non_cds/exposure_details/regions/show" with="cds/exposure" title="Regions" syncColumnWidthsKey="exposure_details" />
        <HX.Table data={[
          "africa", "arab_states", "asia", "oceania", "europe", "former_soviet_republics", "usa", "canada", "south_latin_america", "caribbean", "row",
          null,
          "/non_cds/exposure_details/regions/check_on_totals",
        ]} fields={[
          { field: "value/employees", shownBy: "/non_cds/exposure_details/regions/is_value/employees" },
          { field: "percent/employees", shownBy: "/non_cds/exposure_details/regions/is_percent/employees" },
          { field: "value/revenues", shownBy: "/non_cds/exposure_details/regions/is_value/revenues" },
          { field: "percent/revenues", shownBy: "/non_cds/exposure_details/regions/is_percent/revenues" },
          { field: "value/assets", shownBy: "/non_cds/exposure_details/regions/is_value/assets" },
          { field: "percent/assets", shownBy: "/non_cds/exposure_details/regions/is_percent/assets" },
        ]} shownBy="/non_cds/exposure_details/regions/show" with="cds/exposure/granular/regions/regions_list" syncColumnWidthsKey="exposure_details" kb-interactive />
        <HX.Collection fields={[
          "missing_amount_text.read_only_option",
          { field: "value/employees", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/value/employees/hide_missing" },
          { field: "percent/employees", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/employees/hide_missing" },
          { field: "value/employees.missing_values", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/value/employees/show_missing" },
          { field: "percent/employees.missing_values", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/employees/show_missing" },
          { field: "value/revenues", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/value/revenues/hide_missing" },
          { field: "percent/revenues", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/revenues/hide_missing" },
          { field: "value/revenues.missing_values", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/value/revenues/show_missing" },
          { field: "percent/revenues.missing_values", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/revenues/show_missing" },
          { field: "value/assets", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/value/assets/hide_missing" },
          { field: "percent/assets", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/assets/hide_missing" },
          { field: "value/assets.missing_values", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/value/assets/show_missing" },
          { field: "percent/assets.missing_values", shownBy: "/non_cds/exposure_details/regions/missing_amounts/toggles/percent/assets/show_missing" },
        ]} with="/non_cds/exposure_details/regions/missing_amounts" horizontal syncColumnWidthsKey="exposure_details" />
        <HX.Collection fields={["commited_capital", "invested_capital"]} shownBy="/non_cds/exposure_details/capital_show" with="cds/exposure/granular" horizontal syncColumnWidthsKey="client_info" />
        <HX.Collection fields={["no_of_directorship"]} shownBy="/non_cds/exposure_details/no_of_directorship_show" with="cds/exposure/granular" syncColumnWidthsKey="client_info" />
        <HX.Collection fields={["transactions_av_value", "transactions_av_fee"]} shownBy="/non_cds/exposure_details/transactions_av_show" with="cds/exposure/granular" horizontal syncColumnWidthsKey="client_info" />
      </HX.Section>
      <HX.Section title="Investor Profile" shownBy="non_cds/exposure_details/investor_split/show">
        <HX.Pane flow="right">
          <HX.Table title="Type" data={[
            "investor_split_type/institutional",
            "investor_split_type/retail",
            "investor_split_type/other",
            "/non_cds/exposure_details/investor_split/type_total"
          ]} fields={["percent"]} with="cds/exposure/granular" kb-interactive />
          <HX.Table title="Regions" data={[
            "investor_split_region/region_1",
            "investor_split_region/region_2",
            "investor_split_region/region_3",
            "/non_cds/exposure_details/investor_split/region_total"
          ]} fields={["region", "percent"]} with="cds/exposure/granular" kb-interactive />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Credit Rating" shownBy="non_cds/exposure_details/credit_rating_show">
        <HX.Collection fields={["cr_s_and_p", "cr_moodys", "cr_fitch"]} with="cds/rating_factors/exposure_details" horizontal />
      </HX.Section>
      <HX.Section title="Revenue Split by Activity" shownBy="non_cds/exposure_details/revenue_split_admin/show">
        <HX.Table data={[
          "est_companies",
          "est_trusts",
          "outside_board",
          "legal_advice",
          "accountancy",
          "tax",
          "other",
          "/non_cds/exposure_details/revenue_split_admin/total"
        ]} fields={["amount", "percent"]} with="cds/exposure/granular/revenue_split_admin" kb-interactive />
      </HX.Section>
      <HX.Section title="Revenue Split by Activity" shownBy="non_cds/exposure_details/revenue_split_banks/show">
        <HX.Table data={[
          "interest",
          "fee",
          "trading",
          "other",
          "/non_cds/exposure_details/revenue_split_banks/total"
        ]} fields={["amount", "percent"]} with="cds/exposure/granular/revenue_split_banks" kb-interactive />
      </HX.Section>
      <HX.Section title="Premium Income split" shownBy="non_cds/exposure_details/premium_split/show">
        <HX.Table data={[
          "life",
          "pc",
          "personal",
          "commercial",
          "healthcare",
          "ripc",
          "other",
          "/non_cds/exposure_details/premium_split/total"
        ]} fields={["amount", "percent"]} with="cds/exposure/granular/premium_split" kb-interactive />
        <HX.Collection fields={["combined_ratio", "solvency_ratio"]} with="cds/rating_factors/exposure_details" horizontal syncColumnWidthsKey="client_info" />
        <HX.Collection fields={["short_tail_pc", "direct_business_pc"]} with="cds/rating_factors/exposure_details" horizontal syncColumnWidthsKey="client_info" />
      </HX.Section>
      <HX.Section title="Revenue Split by Activity" shownBy="non_cds/exposure_details/revenue_split_brokers/show">
        <HX.Table data={[
          "institutional_advisory",
          "institutional_execution",
          "retail_advisory",
          "retail_execution",
          "retail_discretionary",
          "other",
          "/non_cds/exposure_details/revenue_split_brokers/total"
        ]} fields={["amount", "percent"]} with="cds/exposure/granular/revenue_split_brokers" kb-interactive />
      </HX.Section>
      <HX.Section title="Revenue Split by Activity" shownBy="non_cds/exposure_details/revenue_split_exchanges/show">
        <HX.Table data={[
          "exchange",
          "listing",
          "clear_settlement",
          "depositary",
          "other",
          "/non_cds/exposure_details/revenue_split_exchanges/total"
        ]} fields={["amount", "percent"]} with="cds/exposure/granular/revenue_split_exchanges" kb-interactive />
      </HX.Section>
      <HX.Section title="Revenue Split by Activity" shownBy="non_cds/exposure_details/revenue_split_investment/show">
        <HX.Table data={[
          "investment_management",
          "personal_services",
          "legal_advisory_services",
          "family_group_services",
          "other",
          "/non_cds/exposure_details/revenue_split_investment/total"
        ]} fields={["amount", "percent"]} with="cds/exposure/granular/revenue_split_investment" kb-interactive />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_exposure_details };