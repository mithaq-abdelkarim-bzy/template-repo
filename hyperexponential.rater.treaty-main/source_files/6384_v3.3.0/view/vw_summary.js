import * as HX from "hx-model-components";

function vw_summary(scale) {
  return (
    <HX.Page title="Summary" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">

      <HX.Section title="Treaty Details" >
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane>
            <HX.Collection
              numCols={1}
              fields={[
                "cds/standard_fields/insured_name.read_only_option",
                "cds/programme.read_only_option",
                "cds/territorial_focus_group.read_only_option",
                "cds/standard_fields/inception_date",
                "cds/standard_fields/expiry_date",
                "cds/currency.read_only_option",
                "cds/standard_fields/is_renewal.read_only_option",
                "cds/calc_type.read_only_option"
              ]}
            />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection
              numCols={1}
              fields={[
                "cds/brokerage.read_only_option",
                "cds/adj_base.read_only_option",
                "cds/standard_fields/underwriter.read_only_option",
                "cds/standard_fields/broker.read_only_option",
                "cds/broker_contact.read_only_option",
                "cds/hours_clause.read_only_option",
                "cds/sanctions_clause.read_only_option",
                "cds/core_account.read_only_option",
                "cds/terrorism_code.read_only_option",
                "cds/cyber_code.read_only_option",
                "cds/com_disease.read_only_option"
              ]}
            />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection
              numCols={1}
              fields={[
                "cds/currency_policy_financials",
                { field: "cds/summary_fx_conversion", labelBy: "/cds/fx_conversion_label" },
                { field: "cds/summary_uwa_exposure", labelBy: "/cds/uwa_limit_label" },
                { field: "cds/summary_uwa_premium", labelBy: "/cds/uwa_premium_label" },
                { field: "cds/summary_uwa_warning" },
                { field: "cds/summary_eso_obtained", shownBy: "/cds/summary_show_eso_obtained" },
              ]}
            />
            <HX.Notes stretch={true}
              field="cds/summary_comments"
              title="Comments" />
          </HX.Pane>

          <HX.Pane>
            <HX.Table
              title="Historic GNEPI"
              data={[{ datum: "cds/experience_rating/exposure/last_eight" }]}
              fields={[
                { field: "year", width: 100 },
                { field: "gnepi_actual", maxWidth: 400 },
                { field: "gnepi_projected", maxWidth: 400 }
              ]}
              kb-interactive
            />
          </HX.Pane>

        </HX.Pane>
      </HX.Section>
      <HX.Section title="Multi-Year" shownBy="cds/show_multi_year">
        <HX.Table
          title="Multi-year Summary"
          data={["cds/summary/multi_year_summary_ty", "cds/summary/multi_year_summary_ly"]}
          fields={[
            { field: "line_written_summary_fx" },
            { field: "line_estimated_summary_fx" },
            { field: "line_signed_summary_fx" },

            { field: "epi_written_summary_fx" },
            { field: "epi_estimated_summary_fx" },
            { field: "epi_signed_summary_fx" },

            { field: "mi_250" },
            { field: "mi_250_estimate_prem_ratio" },
            { field: "mi_250_prem_ratio" }
          ]}
          kb-interactive
        />
        <HX.Table
          title="Year After Next"
          data={["cds/layers"]}
          fields={[
            { field: "layer_structure" },
            { field: "summary/ty/multi_year_period.read_only_option", shownBy: "cds/show_multi_year" },
            { field: "summary/year_after_next/section_reference" },
            { field: "leader.read_only_option" },
            { field: "layer_description.read_only_option" },
            { field: "limit_cnv", labelBy: "/cds/limit_application_ccy_label" },
            { field: "excess_cnv", labelBy: "/cds/excess_application_ccy_label" },
            { field: "quote/rol_ty/rol_quote.read_only_option" },
            { field: "quote/rol_ty/rol_fot.read_only_option" },
            { field: "quote/rol_ty/rol_afb_tech" },
            { field: "summary/ty/reinstatement_description" },
            null,
            { field: "summary/year_after_next/roc" },
            { field: "summary/year_after_next/risk_adjusted_rate_change" },
            { field: "summary/ty/bpi" },
            { field: "summary/ty/fot_adequacy" },
            { field: "summary/year_after_next/rms_adequacy" },
            { field: "summary/ty/ulr" },
            { field: "summary/ty/epi_adj_rate" },
            { field: "summary/ty/prem_full_line", labelBy: "/cds/prem_100_label" },
            null,
            { field: "quote/rol_ty/written_line.read_only_option" },
            { field: "summary/ty/line_written_summary_fx", labelBy: "/cds/written_line_label" },

            { field: "quote/rol_ty/estimated_signing.read_only_option" },
            { field: "summary/ty/line_estimated_summary_fx", labelBy: "/cds/estimated_line_label" },

            { field: "quote/rol_ty/signed_line.read_only_option" },
            { field: "summary/ty/line_signed_summary_fx", labelBy: "/cds/signed_line_label" },
            null,
            { field: "summary/ty/epi_written_summary_fx", labelBy: "/cds/written_epi_label" },
            { field: "summary/ty/epi_estimated_summary_fx", labelBy: "/cds/estimated_epi_label" },
            { field: "summary/ty/epi_signed_summary_fx", labelBy: "/cds/signed_epi_label" },
            null,
            { field: "summary/ty/mi_250" },
            { field: "summary/ty/mi_250_prem_ratio" },
            { field: "summary/ty/mi_10" },
            { field: "summary/ty/mi_10_prem_ratio" },
            null,
            { field: "summary/year_after_next/share", shownBy: "cds/show_multi_year" }
          ]}
          filter={"summary/year_after_next/show_row"}
          removeHorizontalScroll={true}
          kb-interactive
          syncColumnWidthsKey="future_year_tables"
        />
        <HX.Table
          title="Next Year"
          data={["cds/layers"]}
          fields={[
            { field: "layer_structure" },
            { field: "summary/ty/multi_year_period.read_only_option", shownBy: "cds/show_multi_year" },
            { field: "summary/next_year/section_reference" },
            { field: "leader.read_only_option" },
            { field: "layer_description.read_only_option" },
            { field: "limit_cnv", labelBy: "/cds/limit_application_ccy_label" },
            { field: "excess_cnv", labelBy: "/cds/excess_application_ccy_label" },
            { field: "quote/rol_ty/rol_quote.read_only_option" },
            { field: "quote/rol_ty/rol_fot.read_only_option" },
            { field: "quote/rol_ty/rol_afb_tech" },
            { field: "summary/ty/reinstatement_description" },
            null,
            { field: "summary/next_year/roc" },
            { field: "summary/next_year/risk_adjusted_rate_change" },
            { field: "summary/ty/bpi" },
            { field: "summary/ty/fot_adequacy" },
            { field: "summary/next_year/rms_adequacy" },
            { field: "summary/ty/ulr" },
            { field: "summary/ty/epi_adj_rate" },
            { field: "summary/ty/prem_full_line", labelBy: "/cds/prem_100_label" },
            null,
            { field: "quote/rol_ty/written_line.read_only_option" },
            { field: "summary/ty/line_written_summary_fx", labelBy: "/cds/written_line_label" },

            { field: "quote/rol_ty/estimated_signing.read_only_option" },
            { field: "summary/ty/line_estimated_summary_fx", labelBy: "/cds/estimated_line_label" },

            { field: "quote/rol_ty/signed_line.read_only_option" },
            { field: "summary/ty/line_signed_summary_fx", labelBy: "/cds/signed_line_label" },
            null,
            { field: "summary/ty/epi_written_summary_fx", labelBy: "/cds/written_epi_label" },
            { field: "summary/ty/epi_estimated_summary_fx", labelBy: "/cds/estimated_epi_label" },
            { field: "summary/ty/epi_signed_summary_fx", labelBy: "/cds/signed_epi_label" },
            null,
            { field: "summary/ty/mi_250" },
            { field: "summary/ty/mi_250_prem_ratio" },
            { field: "summary/ty/mi_10" },
            { field: "summary/ty/mi_10_prem_ratio", shownBy: "cds/show_multi_year" },
            null,
            { field: "summary/next_year/share" }
          ]}
          filter={"summary/next_year/show_row"}
          removeHorizontalScroll={true}
          kb-interactive
          syncColumnWidthsKey="future_year_tables"
        />
      </HX.Section>

      <HX.Section title="Treaty Financials">
        <HX.Pane >
          <HX.Table
            title="This Year"
            data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
            fields={[
              { field: "layer_structure" },
              { field: "summary/ty/multi_year_period", shownBy: "cds/show_multi_year" },
              { field: "section_reference.read_only_option" },
              { field: "leader.read_only_option" },
              { field: "layer_description.read_only_option" },
              { field: "limit_cnv", labelBy: "/cds/limit_application_ccy_label" },
              { field: "excess_cnv", labelBy: "/cds/excess_application_ccy_label" },
              { field: "summary/ty/rol_quote" },
              { field: "summary/ty/rol_fot" },
              { field: "quote/rol_ty/rol_afb_tech" },
              { field: "summary/ty/reinstatement_description" },
              null,
              { field: "quote/rol_ty/roc" },
              { field: "summary/ty/risk_adjusted_rate_change" },
              { field: "summary/ty/bpi" },
              { field: "summary/ty/fot_adequacy" },
              { field: "summary/ty/rms_adequacy" },
              { field: "summary/ty/ulr" },
              { field: "summary/ty/epi_adj_rate" },
              { field: "summary/ty/prem_full_line", labelBy: "/cds/prem_100_label" },
              null,
              { field: "quote/rol_ty/written_line.read_only_option" },
              { field: "summary/ty/line_written_summary_fx", labelBy: "/cds/written_line_label" },

              { field: "quote/rol_ty/estimated_signing.read_only_option" },
              { field: "summary/ty/line_estimated_summary_fx", labelBy: "/cds/estimated_line_label" },

              { field: "quote/rol_ty/signed_line.read_only_option" },
              { field: "summary/ty/line_signed_summary_fx", labelBy: "/cds/signed_line_label" },
              null,
              { field: "summary/ty/epi_written_summary_fx", labelBy: "/cds/written_epi_label" },
              { field: "summary/ty/epi_estimated_summary_fx", labelBy: "/cds/estimated_epi_label" },
              { field: "summary/ty/epi_signed_summary_fx", labelBy: "/cds/signed_epi_label" },
              null,
              { field: "summary/ty/mi_250", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/ty/mi_250_prem_ratio", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/ty/mi_10", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/ty/mi_10_prem_ratio", shownBy: "cds/show_non_risk_xl" },
              null,
              { field: "summary/ty/share", shownBy: "cds/show_multi_year" }
            ]}
            kb-interactive
            removeHorizontalScroll={true}
            syncColumnWidthsKey="this_year_and_prior_tables"
          />
          <HX.Table
            title="Previous Year"
            data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
            fields={[
              { field: "layer_structure_ly" },
              { field: "summary/ly/current_year_section_reference", shownBy: "cds/show_multi_year" },
              { field: "section_reference_ly" },
              { field: "leader_ly" },
              { field: "layer_description_ly" },
              { field: "limit_cnv_ly", labelBy: "/cds/limit_application_ccy_label" },
              { field: "excess_cnv_ly", labelBy: "/cds/excess_application_ccy_label" },
              { field: "quote/rol_ly/rol_quote" },
              { field: "quote/rol_ly/rol_fot" },
              { field: "quote/rol_ly/rol_afb_tech" },
              { field: "summary/ly/reinstatement_description" },
              null,
              { field: "quote/rol_ly/roc" },
              { field: "summary/ly/risk_adjusted_rate_change" },
              { field: "summary/ly/bpi" },
              { field: "summary/ly/fot_adequacy" },
              { field: "summary/ly/rms_adequacy" },
              { field: "summary/ly/ulr" },
              { field: "summary/ly/epi_adj_rate" },
              { field: "summary/ly/prem_full_line", labelBy: "/cds/prem_100_label" },
              null,
              { field: "quote/rol_ly/written_line" },
              { field: "summary/ly/line_written_summary_fx", labelBy: "/cds/written_line_label" },

              { field: "quote/rol_ly/estimated_signing" },
              { field: "summary/ly/line_estimated_summary_fx", labelBy: "/cds/estimated_line_label" },

              { field: "quote/rol_ly/signed_line" },
              { field: "summary/ly/line_signed_summary_fx", labelBy: "/cds/signed_line_label" },
              null,
              { field: "summary/ly/epi_written_summary_fx", labelBy: "/cds/written_epi_label" },
              { field: "summary/ly/epi_estimated_summary_fx", labelBy: "/cds/estimated_epi_label" },
              { field: "summary/ly/epi_signed_summary_fx", labelBy: "/cds/signed_epi_label" },
              null,
              { field: "summary/ly/mi_250", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/ly/mi_250_prem_ratio", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/ly/mi_10", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/ly/mi_10_prem_ratio", shownBy: "cds/show_non_risk_xl" },
              null,
              { field: "summary/ly/current_year_share", shownBy: "cds/show_multi_year" }
            ]}
            kb-interactive
            removeHorizontalScroll={true}
            syncColumnWidthsKey="this_year_and_prior_tables"
          />
          <HX.Table
            title="Year Before Last"
            data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
            fields={[
              { field: "summary/year_before_last/layer_structure_year_before_last" },
              { field: "summary/year_before_last/current_year_section_reference", shownBy: "cds/show_multi_year" },
              { field: "summary/year_before_last/section_reference" },
              { field: "summary/year_before_last/leader" },
              { field: "summary/year_before_last/layer_description" },
              { field: "summary/year_before_last/limit_cnv", labelBy: "/cds/limit_application_ccy_label" },
              { field: "summary/year_before_last/excess_cnv", labelBy: "/cds/excess_application_ccy_label" },
              { field: "summary/year_before_last/rol_quote" },
              { field: "summary/year_before_last/rol_fot" },
              { field: "summary/year_before_last/rol_afb_tech" },
              { field: "summary/year_before_last/reinstatement_description" },
              null,
              { field: "summary/year_before_last/roc" },
              { field: "summary/year_before_last/risk_adjusted_rate_change" },
              { field: "summary/year_before_last/bpi" },
              { field: "summary/year_before_last/fot_adequacy" },
              { field: "summary/year_before_last/rms_adequacy" },
              { field: "summary/year_before_last/ulr" },
              { field: "summary/year_before_last/epi_adj_rate" },
              { field: "summary/year_before_last/prem_full_line", labelBy: "/cds/prem_100_label" },
              null,
              { field: "summary/year_before_last/written_line" },
              { field: "summary/year_before_last/line_written_summary_fx", labelBy: "/cds/written_line_label" },

              { field: "summary/year_before_last/estimated_signing" },
              { field: "summary/year_before_last/line_estimated_summary_fx", labelBy: "/cds/estimated_line_label" },

              { field: "summary/year_before_last/signed_line" },
              { field: "summary/year_before_last/line_signed_summary_fx", labelBy: "/cds/signed_line_label" },
              null,
              { field: "summary/year_before_last/epi_written_summary_fx", labelBy: "/cds/written_epi_label" },
              { field: "summary/year_before_last/epi_estimated_summary_fx", labelBy: "/cds/estimated_epi_label" },
              { field: "summary/year_before_last/epi_signed_summary_fx", labelBy: "/cds/signed_epi_label" },
              null,
              { field: "summary/year_before_last/mi_250", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/year_before_last/mi_250_prem_ratio", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/year_before_last/mi_10", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/year_before_last/mi_10_prem_ratio", shownBy: "cds/show_non_risk_xl" },
              null,
              { field: "summary/year_before_last/current_year_share", shownBy: "cds/show_multi_year" }
            ]}
            kb-interactive
            removeHorizontalScroll={true}
            syncColumnWidthsKey="this_year_and_prior_tables"
          />
          <HX.Table
            title="Expiring Year"
            data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
            fields={[
              { field: "summary/expiring_year/layer_structure_expiring_year" },
              { field: "summary/expiring_year/current_year_section_reference", shownBy: "cds/show_multi_year" },
              { field: "summary/expiring_year/section_reference" },
              { field: "summary/expiring_year/leader" },
              { field: "summary/expiring_year/layer_description" },
              { field: "summary/expiring_year/limit_cnv", labelBy: "/cds/limit_application_ccy_label" },
              { field: "summary/expiring_year/excess_cnv", labelBy: "/cds/excess_application_ccy_label" },
              { field: "summary/expiring_year/rol_quote" },
              { field: "summary/expiring_year/rol_fot" },
              { field: "summary/expiring_year/rol_afb_tech" },
              { field: "summary/expiring_year/reinstatement_description" },
              null,
              { field: "summary/expiring_year/roc" },
              { field: "summary/expiring_year/risk_adjusted_rate_change" },
              { field: "summary/expiring_year/bpi" },
              { field: "summary/expiring_year/fot_adequacy" },
              { field: "summary/expiring_year/rms_adequacy" },
              { field: "summary/expiring_year/ulr" },
              { field: "summary/expiring_year/epi_adj_rate" },
              { field: "summary/expiring_year/prem_full_line", labelBy: "/cds/prem_100_label" },
              null,
              { field: "summary/expiring_year/written_line" },
              { field: "summary/expiring_year/line_written_summary_fx", labelBy: "/cds/written_line_label" },

              { field: "summary/expiring_year/estimated_signing" },
              { field: "summary/expiring_year/line_estimated_summary_fx", labelBy: "/cds/estimated_line_label" },

              { field: "summary/expiring_year/signed_line" },
              { field: "summary/expiring_year/line_signed_summary_fx", labelBy: "/cds/signed_line_label" },
              null,
              { field: "summary/expiring_year/epi_written_summary_fx", labelBy: "/cds/written_epi_label" },
              { field: "summary/expiring_year/epi_estimated_summary_fx", labelBy: "/cds/estimated_epi_label" },
              { field: "summary/expiring_year/epi_signed_summary_fx", labelBy: "/cds/signed_epi_label" },
              null,
              { field: "summary/expiring_year/mi_250", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/expiring_year/mi_250_prem_ratio", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/expiring_year/mi_10", shownBy: "cds/show_non_risk_xl" },
              { field: "summary/expiring_year/mi_10_prem_ratio", shownBy: "cds/show_non_risk_xl" },
            ]}
            kb-interactive
            removeHorizontalScroll={true}
            syncColumnWidthsKey="this_year_and_prior_tables"
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_summary };