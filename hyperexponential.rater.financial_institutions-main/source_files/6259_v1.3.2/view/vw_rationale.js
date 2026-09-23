import * as HX from "hx-model-components";

function vw_rationale(scale) {
  return (
    <HX.Page title="Rationale" shownBy="model_state/show_after_landing_page" viewScale={scale}>

      <HX.Section title="1. Summary of Programme Discussion with Broker">
        <HX.Notes field="general_comments" with="cds/rationale" />
      </HX.Section>

      <HX.Section title="2. Comments on BPI and/or Rate Change">
        <HX.Notes field="bpi_comments" with="cds/rationale" />
      </HX.Section>

      <HX.Section title="3. Any other Factors not Captured Elsewhere">
        <HX.Notes field="other_factors_comments" with="cds/rationale" />
      </HX.Section>

      <HX.Section title="4. Comments on ESG">
        <HX.Notes field="esg_comments" with="cds/rationale" />
      </HX.Section>

      <HX.Section title="5. I am writing this risk because">
        <HX.Notes field="reason_comments" with="cds/rationale" />
      </HX.Section>

      <HX.Section title="6. Any other documents/attachments are stored at (including file name)">
        <HX.Notes field="additional_info_path" with="cds/rationale" />
      </HX.Section>

    </HX.Page>
  )
}

export { vw_rationale };