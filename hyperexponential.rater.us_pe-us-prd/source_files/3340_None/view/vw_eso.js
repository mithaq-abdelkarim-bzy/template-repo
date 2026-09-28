import * as HX from "hx-model-components";

function vw_eso(scale) {
  return (
    <HX.Page title="ESO" fullWidth={false} viewScale={scale}>
      <HX.With context={{ type: "struct", path: "cds/eso" }}>
        <HX.Section title="">
          <HX.Pane>
            <HX.Collection fields={["requesting_underwriter"]} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection
                title="EXCEPTION (Include all elements over authority)"
                fields={[
                  "term_premium_figure_gross/exception",
                  "exposure_limits/exception",
                  "term/exception",
                  "over_lining/exception",
                  "unauthorised_cob_or_mop/exception",
                ]}
              />
            </HX.Pane>
            <HX.Pane flow="down">
              <HX.Collection
                title="AMOUNT (AFB Share or 100%)"
                fields={[
                  "term_premium_figure_gross/amount",
                  "exposure_limits/amount",
                  "term/amount",
                  "over_lining/amount",
                  "unauthorised_cob_or_mop/amount",
                ]}
              />
            </HX.Pane>
          </HX.Pane>

          <HX.Pane />
          <HX.Pane />

          <HX.Pane flow="down">
            <HX.Collection
              fields={[
                "amount_authorising/input",
                "amount_authorising/warning",
              ]}
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane flow="down">
              <HX.Collection title="SIGN OFF"
                fields={[
                  "sign_off/policy_reference",
                  "sign_off/bind_date",
                  "sign_off/authoriser_name",
                  "sign_off/authorisers_authority_limit",
                  "sign_off/date_of_authorisation",
                ]}
              />
            </HX.Pane>
            <HX.Button title="Generate Email" task="generate_email" />
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Collection fields={["warning"]} />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_eso };
