import * as HX from "hx-model-components";

function vw_test_api() {
  return (
    <HX.Page title="test api">

      <HX.Section title="Companies House - API Call">
        <HX.Pane flow="right">
          <HX.Pane ratio={1}>
            <HX.Collection fields={["company_id", "fetch_status"]} with="companies_house" />
            <HX.Button task="get_companies_house" title="Get Company Data" />
          </HX.Pane>
          <HX.Pane ratio={2} stretch>
            <HX.Collection fields={["company_name", "company_status", "creation_date"]} with="companies_house" stretch />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Pane ratio={1} stretch>
            <HX.Collection fields={["accounts_overdue", "has_charges", "has_insolvency_history"]} with="companies_house" stretch />
          </HX.Pane>
          <HX.Pane ratio={2}>
            <HX.Collection fields={["address_line_1", "address_line_2", "locality", "postal_code"]} with="companies_house" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

    </HX.Page>
  )
}

export { vw_test_api };