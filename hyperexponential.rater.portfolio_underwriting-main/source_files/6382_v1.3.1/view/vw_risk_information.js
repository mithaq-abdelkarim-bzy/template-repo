import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_risk_information">
      <HX.Section title="Account Details">
        <HX.Pane >
          <HX.Collection
            with="cds/risk_information"
            numCols={2}
            fields={[
              "/hx_core/inception_date",
              "/hx_core/expiry_date",
              "/cds/standard_fields/underwriter",
              "deal_status",
              "facility_type",
              "/cds/standard_fields/insured_name",
              "/cds/currencies/source_currency",
              "/cds/standard_fields/policy_reference",
              "/cds/standard_fields/is_renewal"
            ]} />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Settings">
        <HX.Pane>
          <HX.Collection
            with="cds/risk_information"
            numCols={2}
            fields={[
              "follow_main_syndicate",
              { field: "is_large_model_mode", shownBy: "/non_cds/risk_information/not_follow_main_syndicate" },
              { field: "prem_data_available", shownBy: "/non_cds/risk_information/not_follow_main_syndicate" },
              "is_profit_comission",
              { field: "insured_data_date", shownBy: "/non_cds/risk_information/not_follow_main_syndicate" },
              { field: "data_yoa_basis", shownBy: "/non_cds/risk_information/not_follow_main_syndicate" },
              { field: "det_claims_data_available", shownBy: "/non_cds/risk_information/not_follow_main_syndicate" },
              { field: "cat_modelling_available", shownBy: "/non_cds/risk_information/not_follow_main_syndicate" },
            ]}
          />
          <HX.Pane flow="right">
            <HX.Collection with="cds/risk_information" fields={["bbt_option_id"]} horizontal shownBy="follow_main_syndicate" />
            <HX.Button
              task="fetch_bbt_task"
              title="Fetch BBT Outputs"
              shownBy="cds/risk_information/follow_main_syndicate"
            />
          </HX.Pane>
          <HX.Collection
            numCols={2}
            fields={[null, "bbt_last_fetch_time"]}
            with="cds/risk_information"
            shownBy="follow_main_syndicate" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Broker Details">
        <HX.Collection
          numCols={2}
          with="cds/risk_information"
          fields={["broker_contact", "/cds/standard_fields/broker", "broker_email", "broker_location"]} />
      </HX.Section>
      <HX.Section title="Show Actuarial Details and Reference Tables" shownBy="/non_cds/risk_information/not_follow_main_syndicate">
        <HX.Collection
          numCols={2}
          with="cds/risk_information"
          fields={[

            "priced_by",
            { field: null, shownBy: "/non_cds/risk_information/is_underwriter" },
            { field: "actuary_reviewed", shownBy: "/non_cds/risk_information/is_actuarial" },
            { field: "show_refs", shownBy: "/non_cds/risk_information/is_actuarial" }
          ]} />
      </HX.Section>
      <HX.Section title="Show Actuarial Details and Reference Tables" shownBy="cds/risk_information/follow_main_syndicate">
        <HX.Collection
          numCols={2}
          with="cds/risk_information"
          fields={[
            "priced_by",
            { field: null, shownBy: "/non_cds/risk_information/is_underwriter" },
            { field: "actuary_reviewed", shownBy: "/non_cds/risk_information/is_actuarial" },
          ]} />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };