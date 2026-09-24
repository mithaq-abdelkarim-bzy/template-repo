import * as HX from "hx-model-components";

function vw_eso(scale) {
  return (
    <HX.Page title="ESO" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">

      <HX.Section title="Send ESO">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane>
            <HX.Collection fields={[
              "cds/eso_template/email_recipients"
            ]} />
            <HX.Button task="send_eso_task"
              title="Send ESO" />
          </HX.Pane>

          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Insured Details">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Collection
              numCols={1}
              fields={[
                "cds/standard_fields/insured_name.read_only_option",
                "cds/standard_fields/inception_date",
                "cds/standard_fields/expiry_date",
                null,
                "cds/eso_template/team",
                "cds/standard_fields/underwriter.read_only_option",
                "cds/currency_policy_financials.read_only_option",
                "cds/standard_fields/is_renewal.read_only_option",
                "cds/eso_template/cob_code",
                null,
                "cds/programme.read_only_option",
                "cds/risk_carrier.read_only_option",
                { field: "cds/discussed_london.read_only_option", shownBy: "cds/show_bermuda" },
                { field: "cds/technical_underwriter.read_only_option", shownBy: "cds/show_bermuda" }
              ]}
            />
          </HX.Pane>

          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>


      </HX.Section>

      <HX.Section title="Metrics">
        <HX.Table
          title="This Year"
          data={["cds/layers", null, { datum: "cds", labelBy: "cds/total_label" }]}
          fields={[
            { field: "layer_structure" },
            { field: "section_reference.read_only_option" },
            { field: "layer_description.read_only_option" },
            { field: "limit_cnv", labelBy: "/cds/limit_application_ccy_label" },
            { field: "excess_cnv", labelBy: "/cds/excess_application_ccy_label" },
            { field: "summary/ty/rol_quote" },
            { field: "summary/ty/rol_fot" },
            { field: "quote/rol_ty/rol_afb_tech" },
            { field: "summary/ty/reinstatement_description" },
            null,
            { field: "summary/ty/risk_adjusted_rate_change" },
            { field: "summary/ty/fot_adequacy" },
            { field: "summary/ty/rms_adequacy" },
            { field: "summary/ty/ulr" },
            { field: "summary/ty/prem_full_line", labelBy: "/cds/prem_100_label" },
            null,
            { field: "quote/rol_ty/written_line.read_only_option" },
            { field: "summary/ty/line_written_summary_fx", labelBy: "/cds/written_line_label" },

            { field: "quote/rol_ty/estimated_signing.read_only_option" },
            { field: "summary/ty/line_estimated_summary_fx", labelBy: "/cds/estimated_line_label" },
            null,
            { field: "summary/ty/epi_written_summary_fx", labelBy: "/cds/written_epi_label" },
            { field: "summary/ty/epi_estimated_summary_fx", labelBy: "/cds/estimated_epi_label" },
            null,
            { field: "summary/ty/mi_250" }
          ]}
          kb-interactive
        />
      </HX.Section>

      <HX.Section title="ESO Details">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Collection
              numCols={1}
              fields={[
                "cds/eso_template/authorising_uw",
                "cds/eso_template/date_of_authorisation"
              ]}
            />
          </HX.Pane>

          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={2}>
            <HX.Table
              title="This Year"
              data={["cds/eso_template/requested", "cds/eso_template/uw_authority", "cds/eso_template/authorising_uw_authority"]}
              fields={[
                { field: "request_note" },
                null,
                { field: "loa_premium" },
                { field: "loa_exposure", shownBy: "cds/show_multi_year" },
                { field: "loa_term" },
                { field: "loa_exposure_stacking" },
                { field: "unauthorised_cob_mop" },
                null,
                { field: "authority_as_at" }
              ]}
              kb-interactive
              transpose
            />
          </HX.Pane>

          <HX.Pane ratio={1}>
          </HX.Pane>
        </HX.Pane>

        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Collection
              numCols={1}
              fields={[
                "cds/eso_template/rag_level",
                "cds/eso_template/rag_triggers",
                { field: "cds/summary_eso_obtained" },
              ]}
            />

          </HX.Pane>

          <HX.Pane ratio={2}>
          </HX.Pane>
        </HX.Pane>

        <HX.Notes stretch={true}
          field="cds/eso_template/commentary"
          title="ESO Commentary" />

      </HX.Section>

    </HX.Page >
  )
}

export { vw_eso };