import * as HX from "hx-model-components";

function vw_generate_doc(scale) {
  return (
    <HX.Page title="Generate UW Doc" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">

      <HX.Section title="Policy Document">
        <HX.Pane flow="right">
          <HX.Button task="generate_uw_doc" title="Generate Policy Document in Word" 
            shownBy="policy_doc/show_generate_button"/>
          <HX.Notes field="/policy_doc/premium_check"
            shownBy="/policy_doc/show_premium_check" />
          <HX.File with="/policy_doc"
            field="output_file_doc"
            title="Click on the icon below to download the policy document"
          />
        </HX.Pane>
      </HX.Section>



    </HX.Page>
  )
}


export { vw_generate_doc };