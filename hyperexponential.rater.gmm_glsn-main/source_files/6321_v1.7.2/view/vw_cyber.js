import * as HX from "hx-model-components";
import { cyber_schedule_rating } from "view/vw_constants";


function vw_cyber(scale) {
  return (
    <HX.Page title="Cyber" fullWidth={true} viewScale={scale} >
      {/* shownBy="cds/cyber_selection" */}
      <HX.Section title="Product">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/rating_factors/cyber/first_or_third_party", "cds/rating_factors/cyber/first_or_third_party_note", null]} numCols={3} />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/rating_factors/cyber/product", "cds/rating_factors/cyber/include_excess", "cds/rating_factors/cyber/excess_cyber_note"]} numCols={3} />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/rating_factors/cyber/excess_cyber_calc_note"]} />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Copy Options">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/cyber_copy_option_from"]} />
          <HX.Collection fields={["cds/cyber_copy_option_to"]} />
          <HX.Button task="cyber_copy_option" title="Copy Option" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Limits" >
        <HX.Table shownBy="cds/bbr_masking"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/cyber_options", elementLabelBy: "option_label" }]}
          fields={[{ field: "notified_individuals_limit", labelAlign: "left" },
          { field: "legal_forensic_limit", labelAlign: "left" },
          { field: "additional_breach_costs_limit", labelAlign: "left" },]}
          title="Breach Response"
          kb-interactive
          transpose
        />
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/cyber_options", elementLabelBy: "option_label" }]}
          fields={[{ field: "policy_agg_limit", labelAlign: "left" },
          { field: "infosec_breach_response_limit", shownBy: "/cds/infosec_masking", labelAlign: "left" },]}
          title="Aggregate"
          kb-interactive
          transpose
        />
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/cyber_options", elementLabelBy: "option_label" }]}
          fields={[{ field: "data_network_limit", labelAlign: "left" },
          { field: "defense_penalties_limit", labelAlign: "left" },
          { field: "payment_card_limit", labelAlign: "left" },]}
          title="Liability"
          kb-interactive
          transpose
        />
      </HX.Section>

      <HX.Section title="Retentions" >
        <HX.Table shownBy="cds/bbr_masking"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/cyber_options", elementLabelBy: "option_label" }]}
          fields={[{ field: "legal_forensic_retention", labelAlign: "left" },
          { field: "legal_forensic_subretention", labelAlign: "left" },]}
          title="Breach response"
          kb-interactive
          transpose
        />
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/cyber_options", elementLabelBy: "option_label" }]}
          fields={[{ field: "policy_agg_retention", labelAlign: "left" },]}
          title="Aggregate"
          kb-interactive
          transpose
        />
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/cyber_options", elementLabelBy: "option_label" }]}
          fields={[{ field: "breach_response_retention", shownBy: "/cds/infosec_masking", labelAlign: "left" },
          { field: "data_network_retention", labelAlign: "left" },
          { field: "defense_penalties_retention", labelAlign: "left" },
          { field: "payment_card_retention", labelAlign: "left" },]}
          title="Liability"
          kb-interactive
          transpose
        />
      </HX.Section>

      <HX.Section title="Loss Rating" >
        <HX.Table
          syncColumnWidthsKey="mySyncedTables2"
          data={["cds/modifiers/cyber/cyber_loss_rating"]}
          fields={["cyber_loss_ratio", "cyber_loss_ratio_min", "cyber_loss_ratio_max", "cyber_loss_ratio_selected"]}
          kb-interactive
        />
      </HX.Section>

      <HX.Section title="Schedule Rating" >
        <HX.Table
          syncColumnWidthsKey="mySyncedTables2"
          data={cyber_schedule_rating()}
          fields={["min", "max", "value", "comment"]}
          with="cds/modifiers/cyber"
          kb-interactive
        />
      </HX.Section>

      <HX.Section title="Cyber Summary" >
        <HX.Table
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/cyber_options", elementLabelBy: "option_label" }]}
          fields={[{ field: "brokerage", labelAlign: "left" },
          { field: "model_premium_third_party", infoBy: "/cds/rating_factors/cyber/third_party_only_info_by", shownBy: "/cds/rating_factors/cyber/third_party_only_show", labelAlign: "left" },
          { field: "model_premium_bbr_rater", infoBy: "/cds/rating_factors/cyber/bbr_rater_info_by", shownBy: "/cds/rating_factors/cyber/first_and_third_party_show", labelAlign: "left" }]}
          // "model_premium_first_party",
          // null,
          // "model_premium_final"]}
          kb-interactive
          transpose
        />
      </HX.Section>

    </HX.Page>
  )
}

export { vw_cyber };
