import * as HX from "hx-model-components";

function vw_modifiers_details() {
  return (
    <HX.Page title="Modifier Details" fullWidth={true} shownBy="model_state/show_after_landing_page">

      <HX.Section title="Rate Modification Factors">
        <HX.Pane>
          <HX.Table kb-interactive
            title="1. Experience Modification"
            data={[{ datum: "exp_mod", maxWidth: 300 }]}
            fields={[
              { field: "incurred_loss" },
              { field: "number_of_claims" },
              { field: "number_of_incidents" },
              { field: "written_premium" },
              { field: "incurred_lr", infoBy: "exp_mod/incurred_lr_info_label" },
              { field: "exp_mod_factor", infoBy: "exp_mod/exp_mod_factor_info_label" }
            ]}
            with="cds/modifiers"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Notes title="Underwriter Comments" field="cds/modifiers/exp_mod/uw_comment" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Pane>
          <HX.Table kb-interactive
            title="2. Use of Written Contracts"
            data={[{ datum: "written_contracts", maxWidth: 300 }]}
            fields={[
              { field: "percentage" },
              { field: "written_contracts_factor" }
            ]}
            with="cds/rating_factors"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
        </HX.Pane>

        <HX.Pane>
          <HX.Table kb-interactive
            title="3. Longevity with Carrier (Applies for RENEWALS ONLY)"
            data={[{ datum: "longevity_with_carrier", maxWidth: 300 }]}
            fields={[
              { field: "yrs_insured" },
              { field: "lr" },
              { field: "longevity_with_carrier_factor" }
            ]}
            with="cds/rating_factors"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
        </HX.Pane>

        <HX.Pane>
          <HX.Table kb-interactive
            title="4. Longevity"
            data={[{ datum: "longevity", maxWidth: 300 }]}
            fields={[
              { field: "yr_start" },
              { field: "yrs_in_business" },
              { field: "longevity_factor" }
            ]}
            with="cds/rating_factors"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
        </HX.Pane>

        <HX.Pane>
          <HX.Table kb-interactive
            title="5. Extended Reporting Period"
            data={[{ datum: "erp", maxWidth: 300 }]}
            fields={[
              { field: "erp" },
              { field: "erp_factor" }
            ]}
            with="cds/rating_factors"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Residential">
        <HX.Pane>
          <HX.Table kb-interactive
            title="6. Residential"
            data={[{ datum: "resi", maxWidth: 300 }]}
            fields={[
              { field: "resi_proj" },
              { field: "multiple_units" },
              { field: "high_value" },
              { field: "condos" },
              { field: "resi_proj_factor" }
            ]}
            with="cds/rating_factors"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Optional Coverages">
        <HX.Pane>
          <HX.Table kb-interactive
            title="7. Full Prior Act"
            data={[{ datum: "opt_coverages", maxWidth: 300 }]}
            fields={[
              { field: "full_prior_act" },
              { field: "full_prior_act_date" },
              { field: "retro_factor" },
            ]}
            with="cds/rating_factors"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
          <HX.Table kb-interactive
            title="8. CPL Coverage"
            data={[{ datum: "opt_coverages", maxWidth: 300 }]}
            fields={[
              { field: "cpl" },
              { field: "cpl_factor" },
            ]}
            with="cds/rating_factors"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
          <HX.Table kb-interactive
            title="9. Tech Coverage"
            data={[{ datum: "opt_coverages", maxWidth: 300 }]}
            fields={[
              { field: "tech" },
              { field: "tech_cpl_factor" },
            ]}
            with="cds/rating_factors"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
          <HX.Table kb-interactive
            title="10. Non-Contributary"
            data={[{ datum: "opt_coverages", maxWidth: 300 }]}
            fields={[
              { field: "non_contributary" },
              { field: "non_contributary_factor" },
            ]}
            with="cds/rating_factors"
            transpose
            rowHeaderSettings={{ minWidth: 750 }}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Project Types">
        <HX.Pane>
          <HX.Table
            data={["/cds/exposure/granular/project_type"]}
            fields={[
              { field: "project_type_name", width: 400 },
              { field: "code_e_o", width: 125 },
              { field: "fee_percentage", shownBy: "/noncds/validation/fee_percentage/valid", width: 125 },
              { field: "fee_percentage.notSupported", shownBy: "/noncds/validation/fee_percentage/invalid", infoBy: "/noncds/validation/fee_percentage/info_text", width: 125 },
            ]}
            dynamic={true}
            freezeLeft={0}
            kb-interactive
            maxListVisibleRows={10}
          />
          <HX.Table kb-interactive
            title="Category Loadings"
            fields={[
              { field: "code", width: 125 },
              { field: "category_factor", width: 125 },
              { field: "fee_percentage", width: 125 },
              { field: "proportional_loading", width: 200 },

            ]}
            data={[
              "cat_type_target",
              "cat_type_average",
              "cat_type_expensive",
              "cat_type_refer",
              "cat_type_decline",
              "cat_type_total"
            ]}
            with="cds/exposure/aggregate/project_type_category"
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Schedule Rating Factor">
        <HX.Pane>
          <HX.Table kb-interactive
            data={[
              { datum: "qual_of_staff" },
              { datum: "rm_attendance" },
              { datum: "foreign_work" },
              { datum: "loss_prev" },
              { datum: "client_type" },
              { datum: "contractual_practices" },
              { datum: "engi_procure_construct" },
              { datum: "peer_review" },
              { datum: "total" }
            ]}
            fields={[
              { field: "min", width: 300 },
              { field: "max", width: 300 },
              { field: "factor", width: 300 },
              { field: "comment", width: 300 }
            ]}
            with="cds/modifiers/schedule_rating_factor"
            rowHeaderSettings={{ minWidth: 750 }}
          />
        </HX.Pane>
      </HX.Section>

    </HX.Page >

  )
}

export { vw_modifiers_details };

