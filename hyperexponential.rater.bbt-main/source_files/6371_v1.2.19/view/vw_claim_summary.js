//########### OUTSTANDING ########################
// Needs a shownby criteria 


import * as HX from "hx-model-components";

function vw_claim_summary(scale) {
  return (
    <HX.Page title="Claim Summary" fullWidth={true} shownBy="cds/model_state/show_after_landing_page">

      <HX.Section title="Large Loss Exhibits">
        <HX.Pane flow="right">
          <HX.Table
            title="Large Loss Freq/Sev Trends @100% in Settlement Fx"
            data={[{ datum: "chart_freq_sev", elementLabelBy: "yoa_label" }]}
            fields={["premium"
              , "freq_per_million"
              , "severity"
            ]}
            with="cds/claim_summary"
            filter="show_row"
            kb-interactive
            dynamic
          />

          <HX.Table
            title="Top 15 Cat Events - @100% in Settlement Fx"
            data={["cds/claim_summary/top15_cat_events"]}
            fields={["beazley_catcode"
              , "bi_paid"
              , "bi_os"
              , "bi_incurred"
              , "pre_peer_blend_incurred"
              , "pre_peer_most_likely_incurred"
            ]}
            filter="show_row"
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>




      <HX.Section title="Claims Details">
        <HX.Pane flow="right">
          <HX.Table
            title="Claims Listing - Top 100 large losses"
            data={["cds/bi_data/claims_listing"]}
            fields={["class_rank"
              , "claim_reference"
              , "yoa"
              , "claim_made_date"
              , "bi_paid"
              , "bi_os"
              , "bi_incurred"
              , "pre_peer_blend_incurred"
              , "pre_peer_most_likely_incurred"
            ]}
            filter='show_large'
            kb-interactive
            dynamic
          />

          <HX.Table
            title="Claims Listing - Top 100 cat losses"
            data={["cds/bi_data/claims_listing"]}
            fields={["class_rank"
              , "claim_reference"
              , "yoa"
              , "claim_made_date"
              , "beazley_catcode"
              , "bi_paid"
              , "bi_os"
              , "bi_incurred"
              , "pre_peer_blend_incurred"
              , "pre_peer_most_likely_incurred"
            ]}
            filter='show_cat'
            kb-interactive
            dynamic
          />
        </HX.Pane>


      </HX.Section>

    </HX.Page >
  )
}

export { vw_claim_summary };
