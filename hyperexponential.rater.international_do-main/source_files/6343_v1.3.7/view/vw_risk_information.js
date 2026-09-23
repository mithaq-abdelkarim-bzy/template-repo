import * as HX from "hx-model-components";

function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">
      <HX.Section title="Account Details">
        <HX.Pane >
          {/* NOTE  uncomment if rater requires databse_id to be displayed */}
          {/* <HX.Collection fields={["database_id"]} with="cds" horizontal /> */}
          <HX.Collection fields={[
            "inception_date",
            "expiry_date"
          ]}
            with="hx_core" horizontal />
          <HX.Collection fields={[
            "cds/risk_information/date_validation",
            null
          ]}
            horizontal
            shownBy="cds/risk_information/date_validation_flag" />
          <HX.Collection fields={[
            { field: "cds/standard_fields/underwriter", shownBy: "cds/validation/underwriter/valid" },
            { field: "cds/standard_fields/underwriter.notSupported", shownBy: "cds/validation/underwriter/invalid", infoBy: "cds/validation/underwriter/info_text" },
            "cds/risk_information/beazley_branch"
            // "benchmark_class"
          ]}
            horizontal />
          <HX.Collection fields={[
            { field: "cds/risk_information/underwriting_assistant", shownBy: "cds/validation/underwriting_assistant/valid" },
            { field: "cds/risk_information/underwriting_assistant.notSupported", shownBy: "cds/validation/underwriting_assistant/invalid", infoBy: "cds/validation/underwriting_assistant/info_text" },
            null
            // "benchmark_class"
          ]}
            horizontal />
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/insured_name"
            ]}
            />
            {/* <HX.Button task="save_uw_to_pas_reference" title="Save Insured Name to PAS Reference" /> */}
          </HX.Pane>

          <HX.Collection fields={[
            "currencies/source_currency",
            "standard_fields/is_renewal",
            "risk_information/cips_policy",
            null]}
            with="cds"
            horizontal />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Collection fields={[
            "rating_factors/risk_information/ownership_type",
            { field: "risk_information/pe_backer", shownBy: "risk_information/private_flag" }
          ]}
            with="cds" />

          <HX.Collection fields={[
            { field: "rating_factors/risk_information/us_adr_exposure" },
            { field: "risk_information/other_pe_backer", shownBy: "risk_information/other_pe_backer_flag" }
          ]}
            syncColumnWidthsKey="Sync1"
            with="cds" />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "mmp_flag"
          ]}
            horizontal
            with="cds/risk_information" />
          <HX.Collection fields={[
            "macquarie_flag",
          ]} horizontal
            with="cds/risk_information" />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "cds/rating_factors/risk_information/country_of_domicile",
            "cds/rating_factors/risk_information/main_operating_country",
            { field: "cds/rating_factors/risk_information/primary_listing_location", shownBy: "cds/risk_information/public_flag" }
          ]}
            syncColumnWidthsKey="Sync1"
          />
          <HX.Collection fields={[
            "cds/rating_factors/risk_information/search_sic",
            "cds/rating_factors/risk_information/industry_class_sic_code"]}
            syncColumnWidthsKey="Sync1" />
        </HX.Pane>

      </HX.Section>
      {/* NOTE use the below code if the model does not price multiple layers and it is required to store line size
        brokerage & status on teh risk Information sheet */}
      {/* <HX.Section title="Policy Information" >
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["written_line", "brokerage", "status"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section> */}
      <HX.Section title="Broker Details">
        <HX.Collection fields={[
          { field: "standard_fields/broker", shownBy: "validation/broker/valid" },
          { field: "standard_fields/broker.notSupported", shownBy: "validation/broker/invalid", infoBy: "validation/broker/info_text" },
          "broker_sub_category",
          "broker_contact"]}
          with="cds"
          horizontal />
      </HX.Section>


      <HX.Section title="Policy Tags">
        <HX.Pane flow='right'>
          <HX.Button task="generate_tags" title="Create Policy Tags" />
          <HX.Collection fields={["policy_tag_msg"]} with="cds" />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Other Information">
        <HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "core_account",
              "afb_primary_wording_manuscript",
              "esg_syndicate",
              "esg_net_premium",
              { field: "any_one_claim", shownBy: "not_mmp_flag" }]}
              with="cds/risk_information" />
            <HX.Collection fields={[
              "platform",
              "long_term_agreement",
              "direct_ri",
              { field: "cedant_name", shownBy: "ri_flag" },
              "epl_sublimit",
              "epl_sublimit_premium"
            ]} with="cds/risk_information"

            />
          </HX.Pane>
          {/* <HX.Pane flow="right">
            <HX.Notes
              title=""
              field="cds/risk_information/climate_litigation"
            />
            <HX.Pane>

            </HX.Pane>

          </HX.Pane> */}

        </HX.Pane>

        <HX.Notes
          title="Company Description"
          field="cds/risk_information/company_description"
        />
      </HX.Section>

      <HX.Section title="Comments">
        <HX.Notes
          field="cds/risk_information/comments"
        />
      </HX.Section>
    </HX.Page >
  )
}


export { vw_risk_information };